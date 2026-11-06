"""Transcribe + analyze reference audio: word timings, speaking rate, loudness, pitch, music/silence."""
import sys, json, numpy as np, librosa, pyloudnorm as pyln, soundfile as sf
from faster_whisper import WhisperModel

model = WhisperModel("small.en", device="cpu", compute_type="int8")
out = {}
for path in sys.argv[1:]:
    y16, _ = librosa.load(path, sr=16000)
    segs, _ = model.transcribe(y16, word_timestamps=True, vad_filter=False)
    words = [w for s in segs for w in s.words]
    text = " ".join(w.word.strip() for w in words)
    y, sr = sf.read(path); y = y.astype(np.float32)
    dur = len(y) / sr
    speech = sum(w.end - w.start for w in words)
    gaps = [b.start - a.end for a, b in zip(words, words[1:])]
    f0, vf, _ = librosa.pyin(librosa.resample(y, orig_sr=sr, target_sr=16000), fmin=60, fmax=400, sr=16000)
    f0 = f0[~np.isnan(f0)]
    S = np.abs(librosa.stft(y))
    out[path] = dict(
        duration_s=round(dur, 2), words=len(words),
        wpm=round(len(words) / (words[-1].end - words[0].start) * 60, 1) if words else 0,
        first_word_at_s=round(words[0].start, 2) if words else None,
        last_word_end_s=round(words[-1].end, 2) if words else None,
        mean_gap_s=round(float(np.mean(gaps)), 3) if gaps else None,
        long_pauses_over_0_4s=int(sum(g > 0.4 for g in gaps)),
        lufs=round(pyln.Meter(sr).integrated_loudness(y), 1),
        pitch_median_hz=round(float(np.median(f0)), 1) if len(f0) else None,
        pitch_range_hz=[round(float(np.percentile(f0, 5)), 1), round(float(np.percentile(f0, 95)), 1)] if len(f0) else None,
        spectral_centroid_hz=round(float(librosa.feature.spectral_centroid(S=S, sr=sr).mean()), 0),
        onsets_per_s=round(len(librosa.onset.onset_detect(y=y, sr=sr)) / dur, 2),
        transcript=text,
        word_timings=[[w.word.strip(), round(w.start, 2), round(w.end, 2)] for w in words],
    )
json.dump(out, sys.stdout, indent=1, default=float)
