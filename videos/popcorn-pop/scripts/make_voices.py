"""Generate narration lines with Microsoft neural voices (edge-tts).

  python3 make_voices.py <project_dir>

Reads <project>/scripts/lines.json ([speaker, text] per line) and <project>/scripts/voices.json
({speaker: [voice, rate, pitch]}), writes <project>/assets/audio/vo/NN.wav (24 kHz mono, trimmed
to the first word) and NN.json (word timings [word, start, end] in seconds), plus sample.wav.
"""
import asyncio
import json
import os
import subprocess
import sys

import edge_tts
import edge_tts.communicate

# behind a TLS-inspecting proxy, trust its CA too (edge-tts only trusts certifi's bundle)
if os.environ.get("SSL_CERT_FILE"):
    edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ["SSL_CERT_FILE"])


def trim(src, dst, lead):
    af = (f"atrim=start={lead:.3f},asetpts=PTS-STARTPTS,"
          "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ac", "1", "-ar", "24000", dst], check=True)


async def one(voice, rate, pitch, text, mp3):
    for attempt in range(5):
        try:
            words = []
            with open(mp3, "wb") as f:
                async for ch in edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary").stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        a = ch["offset"] / 1e7
                        words.append([ch["text"], a, a + ch["duration"] / 1e7])
            if words:
                return words
        except Exception as e:
            print("  retry:", e)
        await asyncio.sleep(2 ** attempt)
    raise RuntimeError(f"tts failed: {voice}: {text}")


async def main(proj):
    lines = json.load(open(os.path.join(proj, "scripts", "lines.json")))
    voices = json.load(open(os.path.join(proj, "scripts", "voices.json")))
    out = os.path.join(proj, "assets", "audio", "vo")
    os.makedirs(out, exist_ok=True)
    for i, (who, text) in enumerate(lines):
        voice, rate, pitch = voices[who]
        mp3 = os.path.join(out, f"{i:02d}.mp3")
        words = await one(voice, rate, pitch, text, mp3)
        lead = max(0.0, words[0][1] - 0.03)
        trim(mp3, os.path.join(out, f"{i:02d}.wav"), lead)
        json.dump([[w, round(a - lead, 3), round(b - lead, 3)] for w, a, b in words],
                  open(os.path.join(out, f"{i:02d}.json"), "w"))
        os.remove(mp3)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  os.path.join(out, f"{i:02d}.wav")], capture_output=True, text=True).stdout)
        print(f"{i:02d} {who} {d:.2f}s: {text}", flush=True)
    lst = os.path.join(out, "list.txt")
    with open(lst, "w") as f:
        for i in range(len(lines)):
            f.write(f"file '{i:02d}.wav'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    os.path.join(out, "sample.wav")], check=True)
    os.remove(lst)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
