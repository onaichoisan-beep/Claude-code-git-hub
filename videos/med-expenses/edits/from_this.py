# "From this... to this" - no narration. Fresh clips only. Fog/desk/lonely -> white-flash drop at 7.2 s -> college life.
DROP = 7.2
END = 18.0
SINGLE_LINE = True
XFADE = "dissolve"
XFADE_DUR = 0.35
SHOTS = [
    {"t": 0.0,  "src": "IMG_8965", "in": 0.4, "text": "from this…", "text_until": 7.2},
    {"t": 2.0,  "src": "IMG_8965", "in": 9.0},
    {"t": 3.8,  "src": "studyclip", "in": 4.6},
    {"t": 5.4,  "src": "IMG_9242", "in": 12.0},
    {"t": 7.2,  "src": "IMG_9246", "in": 40.4, "speed": 0.6, "text": "…to this.", "text_until": 14.4, "xfade": "fadewhite"},
    {"t": 9.2,  "src": "bc1a3ac4", "in": 12.6},
    {"t": 11.0, "src": "IMG_2515", "in": 0.3, "cx": 0.62},
    {"t": 12.6, "src": "walkinginapron", "in": 3.0},
    {"t": 14.4, "src": "MeinLAB", "in": 9.0, "pushin": 0.06, "py": 0.12, "ty": 0.17, "text": "same you. one exam later."},
]
SFX = [
    ("Thunder_Sfx", 0.5, -13),
    ("Quick_whoosh", 2.0, -10), ("tick", 4.3, -22), ("tick", 4.8, -22),
    ("Lit_heartbeat1", 5.6, -4), ("Lit_heartbeat1", 6.5, -6),
    ("Reverse_Bass", 7.2, -5),
    ("Lit_whoosh_impact", 7.2, -2), ("THE_Boom_Sound_Effect", 7.3, -3), ("Lit_body_punch", 7.75, -9),   # jump landing
    ("Whoosh_2", 9.2, -5), ("pop", 9.45, -18),
    ("Whoosh_4", 11.0, -5), ("Lit_cloth_roll_2", 11.4, -8),
    ("Quick_whoosh", 12.6, -6), ("step", 12.9, -12), ("step", 13.4, -13), ("step", 13.9, -12),
    ("My_fav_whoosh", 14.4, -5), ("Bass_Explosion", 14.5, -10), ("Lit_heartbeat1", 15.8, -9),
]
