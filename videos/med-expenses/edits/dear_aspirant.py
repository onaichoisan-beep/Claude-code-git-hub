# "Dear NEET aspirant" - no narration. Fresh clips only. Sad, foggy first half -> white-flash drop at 10.8 s -> lab.
DROP = 10.8
END = 21.2
SINGLE_LINE = True
XFADE = "dissolve"
XFADE_DUR = 0.4
SHOTS = [
    {"t": 0.0,  "src": "IMG_8965", "in": 0.4,  "text": "dear aspirant, i know it feels foggy right now."},
    {"t": 3.0,  "src": "studyclip", "in": 0.5, "text": "i know you're tired of this same desk."},
    {"t": 5.6,  "src": "IMG_9242", "in": 12.0, "text": "and some days, you just want to quit."},
    {"t": 8.4,  "src": "IMG_8965", "in": 8.7,  "text": "but i promise, this road goes somewhere."},
    {"t": 10.8, "src": "walkinginapron", "in": 3.0, "text": "it goes here.", "xfade": "fadewhite"},
    {"t": 13.0, "src": "IMG_6273", "in": 0.0, "speed": 0.7, "text": "to rooms like this,"},
    {"t": 14.6, "src": "MeinLAB", "in": 3.5, "pushin": 0.06, "py": 0.12, "ty": 0.17, "text": "to a coat with your name on it."},
    {"t": 17.6, "src": "MeinLAB", "in": 14.0, "pushin": 0.05, "py": 0.12, "ty": 0.17, "text": "keep going. we're waiting for you 🤍"},
]
SFX = [
    ("Thunder_Sfx", 0.6, -12),            # distant rumble under the fog
    ("pop", 3.15, -20), ("tick", 4.1, -22), ("tick", 4.6, -22),
    ("Lit_heartbeat1", 6.1, -3), ("Lit_heartbeat1", 7.0, -5), ("Lit_heartbeat1", 7.9, -7),
    ("Quick_whoosh", 8.4, -8),
    ("Reverse_Bass", 10.8, -5),            # builds into the drop
    ("Lit_whoosh_impact", 10.8, -2), ("THE_Boom_Sound_Effect", 10.9, -3),
    ("step", 11.25, -12), ("step", 11.75, -13), ("step", 12.25, -12), ("step", 12.75, -13),
    ("Lit_cloth_roll_1", 11.5, -2),
    ("Quick_whoosh", 13.0, -6), ("pop", 13.25, -18),
    ("My_fav_whoosh", 14.6, -6), ("Lit_cloth_roll_3", 15.2, -9),
    ("Bass_Explosion", 17.6, -10), ("Lit_heartbeat1", 18.6, -9),
]
