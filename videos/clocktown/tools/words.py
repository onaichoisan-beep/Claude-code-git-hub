"""Word timestamps for the narration (faster-whisper). Usage: python words.py vo.wav > words.json"""
import sys, json, soundfile as sf, numpy as np
from faster_whisper import WhisperModel
a, sr = sf.read(sys.argv[1], dtype="float32")
if sr != 16000:
    import subprocess
    a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-f", "f32le", "-ac", "1", "-ar", "16000", "-"]), np.float32)
m = WhisperModel("base.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, word_timestamps=True)
json.dump([[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words], sys.stdout)
