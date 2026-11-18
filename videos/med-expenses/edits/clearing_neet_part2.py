# "This is what clearing NEET feels like - part 2": sequel to the top performer. Wide, cinematic,
# aspirational shots only (no close selfies). Calm build -> drop at 5.8 s -> achievements -> podium.
DROP = None
END = 13.6
FADE_OUT = 0.6
MID_CAPTIONS = True
CAPTION_BOX = False
XFADE = "dissolve"
XFADE_DUR = 0.35
WATERMARK = ("@hey.rishish", 0.79)
SHOTS = [
    {"t": 0.0,  "src": "F1D19DE4", "in": 0.0,  "smooth": True, "text": "remember the day your NEET result came?"},
    {"t": 2.4,  "src": "IMG_6262", "in": 0.0,  "smooth": True, "text": "now these corridors are your daily walk"},
    {"t": 4.2,  "src": "IMG_6261", "in": 0.0,  "smooth": True, "text": "this name is on your ID card now"},
    # drop
    {"t": 5.8,  "src": "IMG_0752", "in": 11.0, "fit": True, "text": "you sit in rooms full of future doctors"},
    {"t": 7.4,  "src": "bc1a3ac4", "in": 12.8, "smooth": True, "text": "you explain topics you once feared"},
    {"t": 9.0,  "src": "MeinLAB",  "in": 1.9,  "text": "the white coat isn't a dream anymore"},
    {"t": 10.5, "src": "E56BD187", "in": 0.75, "denoise": True, "text": "even the late nights feel different"},
    {"t": 11.6, "src": "bc1a3ac4", "in": 19.0, "smooth": True, "text": "and it all started with one exam 🤍"},
]
SFX = [("Quick_whoosh", 5.8, -10), ("Lit_heartbeat1", 12.0, -13)]
