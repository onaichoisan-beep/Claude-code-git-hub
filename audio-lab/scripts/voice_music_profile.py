"""Pitch of narrator only inside word spans, plus BGM tempo/key estimate."""
import json, numpy as np, librosa

d = json.load(open("analysis.json"))
KEYS = "C C# D D# E F F# G G# A A# B".split()
for path, v in d.items():
    y, sr = librosa.load(path, sr=16000)
    res = {}
    if v["wpm"] > 60:
        f0, _, _ = librosa.pyin(y, fmin=70, fmax=350, sr=sr, frame_length=1024)
        t = librosa.times_like(f0, sr=sr, hop_length=256)
        mask = np.zeros_like(t, bool)
        for _, s, e in v["word_timings"]:
            mask |= (t >= s) & (t <= e)
        p = f0[mask & ~np.isnan(f0)]
        res["voice_pitch_median_hz"] = round(float(np.median(p)), 1)
        res["voice_pitch_p10_p90"] = [round(float(np.percentile(p, q)), 1) for q in (10, 90)]
        res["words_per_sec"] = round(v["words"] / v["last_word_end_s"], 2)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr).mean(1)
    res["bgm_tempo_bpm"] = round(float(np.atleast_1d(tempo)[0]), 1)
    res["bgm_strongest_pitch_class"] = KEYS[int(chroma.argmax())]
    print(path, res)
