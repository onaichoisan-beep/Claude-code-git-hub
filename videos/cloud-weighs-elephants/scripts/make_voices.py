"""Generate the narration in many female voices (Microsoft neural voices via edge-tts).

  python make_voices.py <out_dir> [voice ...]

Writes <out_dir>/<voice>/<NN>.wav (24 kHz mono, trimmed to the first word) and <NN>.json (word
timings [word, start, end] in seconds) for every line in lines.json,
plus <out_dir>/<voice>/sample.wav — the whole script read straight through, for auditioning.
"""
import asyncio, json, os, subprocess, sys

import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = json.load(open(os.path.join(HERE, "lines.json")))

VOICES = [
    "en-US-AvaMultilingualNeural", "en-US-EmmaMultilingualNeural", "en-US-AvaNeural", "en-US-JennyNeural",
    "en-US-AriaNeural", "en-US-MichelleNeural", "en-US-AnaNeural", "en-GB-SoniaNeural", "en-GB-LibbyNeural",
    "en-GB-MaisieNeural", "en-AU-NatashaNeural", "en-CA-ClaraNeural", "en-IE-EmilyNeural",
    "en-IN-NeerjaExpressiveNeural", "en-NZ-MollyNeural",
]
RATE = "+6%"  # a touch faster than default: Reels energy


def trim(src, dst, lead):
    # cut to just before the first word, strip trailing silence, mono 24 kHz
    af = (f"atrim=start={lead:.3f},asetpts=PTS-STARTPTS,"
          "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ac", "1", "-ar", "24000", dst], check=True)


async def one(voice, text, mp3):
    for attempt in range(4):
        try:
            words = []
            with open(mp3, "wb") as f:
                async for ch in edge_tts.Communicate(text, voice, rate=RATE, boundary="WordBoundary").stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        a = ch["offset"] / 1e7
                        words.append([ch["text"], a, a + ch["duration"] / 1e7])
            return words
        except Exception:
            await asyncio.sleep(2 ** attempt)
    raise RuntimeError(f"tts failed: {voice}: {text}")


async def main(out, voices):
    for v in voices:
        d = os.path.join(out, v)
        os.makedirs(d, exist_ok=True)
        for i, text in enumerate(LINES):
            mp3 = os.path.join(d, f"{i:02d}.mp3")
            words = await one(v, text, mp3)
            lead = max(0.0, words[0][1] - 0.03)
            trim(mp3, os.path.join(d, f"{i:02d}.wav"), lead)
            json.dump([[w, round(a - lead, 3), round(b - lead, 3)] for w, a, b in words],
                      open(os.path.join(d, f"{i:02d}.json"), "w"))
            os.remove(mp3)
        lst = os.path.join(d, "list.txt")
        with open(lst, "w") as f:
            for i in range(len(LINES)):
                f.write(f"file '{i:02d}.wav'\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-af", "apad=pad_dur=0", os.path.join(d, "sample.wav")], check=True)
        os.remove(lst)
        print("done", v, flush=True)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2:] or VOICES))
