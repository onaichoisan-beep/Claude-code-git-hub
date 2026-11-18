# POV-style (like the best performer): ~10 s, slow aspirant build -> drop at 4.0 s -> fast montage -> smile.
# Hard cuts, few words, centred small captions, @hey.rishish watermark, 2 soft SFX.
DROP = None
END = 10.3
FADE_OUT = 0.5
MID_CAPTIONS = True
WATERMARK = ("@hey.rishish", 0.79)
M = 0.55   # montage shot length
SHOTS = [
    {"t": 0.0, "src": "IMG_0959", "in": 8.7, "text": "pov: you were a NEET aspirant…"},
    {"t": 2.0, "src": "IMG_9247", "in": 0.4, "transpose": 2, "fit": True, "smooth": True, "text": "doubting yourself every single day"},
    # drop: fast montage, one caption across it
    {"t": 4.0,       "src": "IMG_6261", "in": 0.3,  "smooth": True, "text": "…now you're an MBBS student 🩺", "text_until": 8.4},
    {"t": 4.0+M,     "src": "IMG_6262", "in": 0.4,  "smooth": True},
    {"t": 4.0+2*M,   "src": "IMG_8307", "in": 14.6, "smooth": True},
    {"t": 4.0+3*M,   "src": "IMG_4318", "in": 7.2},
    {"t": 4.0+4*M,   "src": "IMG_1366", "in": 1.2},
    {"t": 4.0+5*M,   "src": "bc1a3ac4", "in": 11.2, "smooth": True},
    {"t": 4.0+6*M,   "src": "E56BD187", "in": 1.1,  "smooth": True},
    {"t": 4.0+7*M,   "src": "IMG_9242", "in": 2.0},
    # ending on the smile
    {"t": 8.4, "src": "IMG_0773", "in": 3.85, "smooth": True, "text": "worth every sleepless night 🤍"},
]
SFX = [("Lit_heartbeat1", 1.0, -12), ("Quick_whoosh", 4.0, -9)]
