"""Natural-sounding narration with Kokoro-82M (open-source, Apache-2.0, runs locally) + word timings from Whisper.

  python3 scripts/make_voices_kokoro.py .

Reads scripts/lines.json ([[speaker, text], ...]) and scripts/voices_kokoro.json ({speaker: [voice, speed]}), writes
assets/audio/vo/NN.wav + NN.json ([[word, start, end], ...]) in the same format as make_voices.py, so voicelib/synth_audio
work unchanged. Voice quality (Kokoro's own grades): af_heart A, af_bella A-, af_nicole B-, am_fenrir/am_michael/am_puck C+,
bf_emma B-, bm_george/bm_fable C. Blend voices with "voiceA+voiceB" (50/50).

Needs: pip install kokoro-onnx soundfile; the model files are fetched by `npx hyperframes tts` into ~/.cache/hyperframes/tts.
Timings: all lines are joined with 1.2 s gaps, transcribed once with `npx hyperframes transcribe` (whisper small.en), split back.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
HERE = os.path.join(ROOT, "scripts")
CACHE = os.path.expanduser("~/.cache/hyperframes/tts")
MODEL, VOICES = os.path.join(CACHE, "models", "kokoro-v1.0.onnx"), os.path.join(CACHE, "voices", "voices-v1.0.bin")
if not os.path.exists(MODEL):
    subprocess.run(["npx", "hyperframes", "tts", "warm up", "-o", os.path.join(tempfile.gettempdir(), "kk.wav")], check=True)

lines = json.load(open(os.path.join(HERE, "lines.json")))
cast = json.load(open(os.path.join(HERE, "voices_kokoro.json")))
k = Kokoro(MODEL, VOICES)
out = os.path.join(ROOT, "assets", "audio", "vo")
os.makedirs(out, exist_ok=True)


def voice_of(v):
    if "+" in v:
        a, b = v.split("+")
        return 0.5 * k.get_voice_style(a) + 0.5 * k.get_voice_style(b)
    return v


clips, sr = [], 24000
for i, (who, text) in enumerate(lines):
    v, speed = cast[who][0], cast[who][1]
    lang = "en-gb" if v.startswith("b") else "en-us"
    x, sr = k.create(text, voice=voice_of(v), speed=speed, lang=lang)
    x = np.asarray(x, dtype=np.float32)
    nz = np.where(np.abs(x) > 0.01)[0]                                    # trim leading/trailing silence
    if len(nz):
        x = x[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.06 * sr)]
    sf.write(os.path.join(out, f"{i:02d}.wav"), x, sr)
    clips.append(x)
    print(f"{i:02d} {who:9s} {len(x) / sr:5.2f}s  {text}")

# one transcription pass for word timings
gap = np.zeros(int(1.2 * sr), dtype=np.float32)
starts, cat, t = [], [], 0.0
for x in clips:
    starts.append(t)
    cat += [x, gap]
    t += (len(x) + len(gap)) / sr
tmp = tempfile.mkdtemp()
sf.write(os.path.join(tmp, "all.wav"), np.concatenate(cat), sr)
subprocess.run(["npx", "hyperframes", "transcribe", os.path.join(tmp, "all.wav"), "--dir", tmp, "--model", "small.en", "--json"],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
words = json.load(open(os.path.join(tmp, "transcript.json")))
words = words if isinstance(words, list) else words["words"]
import difflib
import re


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


for i, x in enumerate(clips):
    a, b = starts[i], starts[i] + len(x) / sr
    heard = [w for w in words if a - 0.3 <= w["start"] < b + 0.1]
    toks = lines[i][1].split()                                            # the real script words (never lose one)
    times = [None] * len(toks)
    sm = difflib.SequenceMatcher(None, [norm(t) for t in toks], [norm(w["text"]) for w in heard])
    for blk in sm.get_matching_blocks():
        for j in range(blk.size):
            w = heard[blk.b + j]
            times[blk.a + j] = [max(0.0, w["start"] - a), min(b, w["end"]) - a]
    L = (b - a)
    known = [j for j, tm in enumerate(times) if tm]
    for j in range(len(toks)):                                            # interpolate the unmatched words
        if times[j]:
            continue
        prev = max([q for q in known if q < j], default=None)
        nxt = min([q for q in known if q > j], default=None)
        t0 = times[prev][1] if prev is not None else 0.0
        t1 = times[nxt][0] if nxt is not None else L
        lo = [q for q in range(len(toks)) if (prev is None or q > prev) and (nxt is None or q < nxt)]
        k_ = lo.index(j)
        step = (t1 - t0) / len(lo)
        times[j] = [t0 + k_ * step, t0 + (k_ + 1) * step]
    mine = [[toks[j], round(times[j][0], 3), round(max(times[j][0] + 0.05, times[j][1]), 3)] for j in range(len(toks))]
    json.dump(mine, open(os.path.join(out, f"{i:02d}.json"), "w"))
print("wrote", len(clips), "lines with word timings")
