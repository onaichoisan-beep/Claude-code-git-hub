"""Make a slow voice-over fast: cut dead air, shorten pauses, then speed up to a target pace.

Usage: python tighten_vo.py in.m4a out.wav [--wpm 185] [--max-gap 0.12]
Prints the before/after pace and the list of cuts it made, so the edit can be checked.
"""
import argparse, subprocess, json, tempfile, os
import numpy as np, librosa, soundfile as sf
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--wpm", type=float, default=185, help="target words per minute (reference vlog: 187)")
ap.add_argument("--max-gap", type=float, default=0.12, help="longest pause kept between words, seconds")
ap.add_argument("--silence-db", type=float, default=-40, help="below this RMS level counts as silence")
ap.add_argument("--max-speed", type=float, default=1.35, help="never speed up more than this (keeps voice natural)")
a = ap.parse_args()

y, sr = librosa.load(a.inp, sr=44100, mono=True)
model = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = model.transcribe(librosa.resample(y, orig_sr=sr, target_sr=16000), language="hi",
                           word_timestamps=True, vad_filter=True)
words = [w for s in segs for w in s.words]
if not words:
    raise SystemExit("no speech found")

# 1. Find real silences from the waveform (Whisper word times stretch over pauses),
#    and squeeze every pause longer than max_gap down to max_gap.
hop = 441  # 10 ms
rms = librosa.feature.rms(y=y, frame_length=1764, hop_length=hop)[0]
db = 20 * np.log10(rms + 1e-9)
loud = db > a.silence_db
iv, st = [], None
for i, v in enumerate(loud):
    if v and st is None: st = i
    if not v and st is not None: iv.append([st, i]); st = None
if st is not None: iv.append([st, len(loud)])
iv = [[s * hop / sr, e * hop / sr] for s, e in iv]
merged = [iv[0]]
for s, e in iv[1:]:
    if s - merged[-1][1] < a.max_gap: merged[-1][1] = e
    else: merged.append([s, e])
pad = 0.03
fade = int(0.008 * sr)
parts, cuts = [], []
for k, (s, e) in enumerate(merged):
    seg = y[int(max(0, s - pad) * sr):int(min(len(y) / sr, e + pad) * sr)].copy()
    if len(seg) > 2 * fade:
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    parts.append(seg)
    if k + 1 < len(merged):
        gap = merged[k + 1][0] - e
        cuts.append([round(e, 2), round(gap, 2)])
        parts.append(np.zeros(int(max(0.0, a.max_gap - 2 * pad) * sr), dtype=seg.dtype))
tight = np.concatenate(parts)

speech_words = len(words)
orig_wpm = speech_words / (words[-1].end - words[0].start) * 60
tight_wpm = speech_words / (len(tight) / sr) * 60
speed = float(np.clip(a.wpm / tight_wpm, 1.0, a.max_speed))

# 2. Pitch-preserving speed-up + light compression + loudness to -14 LUFS / -1 dBTP.
with tempfile.TemporaryDirectory() as d:
    tmp = os.path.join(d, "t.wav"); sf.write(tmp, tight, sr)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af",
                    f"atempo={speed:.3f},highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
                    "loudnorm=I=-14:TP=-1:LRA=6", "-ar", "44100", a.out], check=True)

print(json.dumps(dict(
    original_s=round(len(y) / sr, 2), after_gap_cuts_s=round(len(tight) / sr, 2),
    final_s=round(len(tight) / sr / speed, 2), words=speech_words,
    wpm_before=round(orig_wpm), wpm_after_cuts=round(tight_wpm), speed_factor=round(speed, 3),
    wpm_final=round(tight_wpm * speed), pauses_cut=len(cuts), cuts=cuts), ensure_ascii=False, indent=1))
