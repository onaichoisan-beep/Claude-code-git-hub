"""Generate the two-voice dialogue (Microsoft neural voices via edge-tts).

  python make_voices.py <out_dir> [ai_voice kid_voice]

Writes <out_dir>/<NN>.wav (24 kHz mono, trimmed to the first word) and <NN>.json (word timings
[word, start, end] in seconds) for every line in lines.json ([speaker, text]), plus
<out_dir>/sample.wav — the whole script read straight through, for auditioning.
"""
import asyncio, json, os, subprocess, sys

import edge_tts
import edge_tts.communicate

# behind a TLS-inspecting proxy, trust its CA too (edge-tts only trusts certifi's bundle)
if os.environ.get("SSL_CERT_FILE"):
    edge_tts.communicate._SSL_CTX.load_verify_locations(os.environ["SSL_CERT_FILE"])

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = json.load(open(os.path.join(HERE, "lines.json")))

# the robot: warm, clear, natural; the kid: the child voice
VOICE = {"ai": "en-US-AndrewMultilingualNeural", "kid": "en-US-AnaNeural"}
RATE = {"ai": "+12%", "kid": "+6%"}  # a touch faster than default: Reels energy
PITCH = {"ai": "+0Hz", "kid": "+0Hz"}


def trim(src, dst, lead):
    # cut to just before the first word, strip trailing silence, mono 24 kHz
    af = (f"atrim=start={lead:.3f},asetpts=PTS-STARTPTS,"
          "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ac", "1", "-ar", "24000", dst], check=True)


async def one(voice, rate, pitch, text, mp3):
    for attempt in range(4):
        try:
            words = []
            with open(mp3, "wb") as f:
                async for ch in edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary").stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        a = ch["offset"] / 1e7
                        words.append([ch["text"], a, a + ch["duration"] / 1e7])
            return words
        except Exception:
            await asyncio.sleep(2 ** attempt)
    raise RuntimeError(f"tts failed: {voice}: {text}")


async def main(out):
    os.makedirs(out, exist_ok=True)
    for i, (who, text) in enumerate(LINES):
        mp3 = os.path.join(out, f"{i:02d}.mp3")
        words = await one(VOICE[who], RATE[who], PITCH[who], text, mp3)
        lead = max(0.0, words[0][1] - 0.03)
        trim(mp3, os.path.join(out, f"{i:02d}.wav"), lead)
        json.dump([[w, round(a - lead, 3), round(b - lead, 3)] for w, a, b in words],
                  open(os.path.join(out, f"{i:02d}.json"), "w"))
        os.remove(mp3)
        print(f"{i:02d} {who}: {text}", flush=True)
    lst = os.path.join(out, "list.txt")
    with open(lst, "w") as f:
        for i in range(len(LINES)):
            f.write(f"file '{i:02d}.wav'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    os.path.join(out, "sample.wav")], check=True)
    os.remove(lst)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        VOICE["ai"], VOICE["kid"] = sys.argv[2], sys.argv[3]
    asyncio.run(main(sys.argv[1]))
