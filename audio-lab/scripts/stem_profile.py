"""Profile Demucs stems: clean narrator voice vs background (music + SFX) layer."""
import json, os, numpy as np, librosa, pyloudnorm as pyln

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
KEYS = "C C# D D# E F F# G G# A A# B".split()


def voice_stats(y, sr):
    f0, _, _ = librosa.pyin(y, fmin=65, fmax=400, sr=sr, frame_length=1024)
    f0 = f0[~np.isnan(f0)]
    return dict(pitch_median_hz=round(float(np.median(f0)), 1),
                pitch_p10_p90=[round(float(np.percentile(f0, q)), 1) for q in (10, 90)],
                pitch_spread_semitones=round(float(12 * np.log2(np.percentile(f0, 90) / np.percentile(f0, 10))), 1))


out = {}
for name in sorted(os.listdir(os.path.join(ROOT, "stems", "htdemucs"))):
    d = os.path.join(ROOT, "stems", "htdemucs", name)
    v, sr = librosa.load(os.path.join(d, "vocals.wav"), sr=16000)
    b, _ = librosa.load(os.path.join(d, "no_vocals.wav"), sr=16000)
    meter = pyln.Meter(sr)
    lv, lb = meter.integrated_loudness(v), meter.integrated_loudness(b)
    tempo, _ = librosa.beat.beat_track(y=b, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=b, sr=sr).mean(1)
    onsets = librosa.onset.onset_detect(y=b, sr=sr, units="time")
    res = dict(voice_lufs=round(lv, 1), background_lufs=round(lb, 1), voice_over_bg_db=round(lv - lb, 1),
               bg_tempo_bpm=round(float(np.atleast_1d(tempo)[0]), 1),
               bg_key_guess=KEYS[int(chroma.argmax())],
               bg_hits_per_sec=round(len(onsets) / (len(b) / sr), 2))
    if lv > -40:
        res.update(voice_stats(v, sr))
    out[name] = res
    print(name, res)
json.dump(out, open(os.path.join(ROOT, "stem_profile.json"), "w"), indent=1)
