"""Render the reference ear-hack script with many voices, then score pitch/pace vs the real narrator."""
import json, os, subprocess, sys, numpy as np, librosa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "samples")
os.makedirs(OUT, exist_ok=True)
TEXT = json.load(open(os.path.join(HERE, "..", "analysis.json")))["reference_audio/ear_hack.wav"]["transcript"]
_ref = json.load(open(os.path.join(HERE, "..", "stem_profile.json")))["ear_hack"]  # clean Demucs voice stem
REF = dict(pitch=_ref["pitch_median_hz"], spread=_ref["pitch_spread_semitones"], dur=29.34)

CANDIDATES = [
    ("kokoro", v, 1.15) for v in ["am_michael", "am_adam", "am_eric", "am_liam", "am_puck", "am_echo",
                                   "am_fenrir", "am_onyx", "af_heart", "af_bella", "af_nicole", "bm_george", "bm_lewis"]
] + [
    ("piper", v, 1.2) for v in ["en_US-ryan-high", "en_US-lessac-high", "en_US-joe-medium",
                                 "en_US-hfc_male-medium", "en_US-amy-medium", "en_GB-alan-medium"]
] + [
    ("edge", v, "+20%") for v in ["en-US-AndrewNeural", "en-US-BrianNeural", "en-US-ChristopherNeural",
                                   "en-US-GuyNeural", "en-US-EricNeural", "en-US-AvaNeural", "en-US-EmmaNeural"]
]

rows = []
for engine, voice, sp in CANDIDATES:
    path = os.path.join(OUT, f"{engine}__{voice}.wav")
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        args = [sys.executable, os.path.join(HERE, "tts.py"), "--engine", engine, "--voice", voice, "--text", TEXT, "-o", path]
        args += ["--rate", sp] if engine == "edge" else ["--speed", str(sp)]
        if subprocess.run(args, capture_output=True).returncode:
            print("FAILED", engine, voice); continue
    y, sr = librosa.load(path, sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=65, fmax=400, sr=sr, frame_length=1024)
    f0 = f0[~np.isnan(f0)]
    dur = len(librosa.effects.trim(y, top_db=35)[0]) / sr
    pitch = float(np.median(f0))
    spread = float(12 * np.log2(np.percentile(f0, 90) / np.percentile(f0, 10)))
    # lower = closer: pitch distance + expressiveness gap (both semitones) + pace gap (seconds/3)
    score = abs(12 * np.log2(pitch / REF["pitch"])) + abs(spread - REF["spread"]) / 2 + abs(dur - REF["dur"]) / 3
    rows.append(dict(engine=engine, voice=voice, pitch_hz=round(pitch), spread_st=round(spread, 1),
                     dur_s=round(dur, 1), score=round(float(score), 2), file=os.path.relpath(path, os.path.join(HERE, ".."))))

rows.sort(key=lambda r: r["score"])
json.dump(rows, open(os.path.join(HERE, "..", "voice_scores.json"), "w"), indent=1)
for r in rows:
    print(f"{r['score']:6.2f}  {r['engine']:6} {r['voice']:26} pitch={r['pitch_hz']:4} spread={r["spread_st"]:5}st dur={r['dur_s']}")
