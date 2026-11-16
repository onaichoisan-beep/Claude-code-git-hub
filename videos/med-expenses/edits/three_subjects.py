# "MBBS first year in 3 subjects" - no voice, full single-line text, clean transitions, lots of SFX.
# Every clip window was picked by measured camera shake + checked first/last frames.
DROP = None
END = 17.8
SINGLE_LINE = True
XFADE = "dissolve"          # inside a section
XFADE_DUR = 0.4
SLIDE = "smoothleft"        # between sections (always with a whoosh)

SHOTS = [
    {"t": 0.0,   "src": "IMG_8307", "in": 15.0, "text": "mbbs first year in 3 subjects"},
    # 1. anatomy
    {"t": 2.4,   "src": "IMG_0396", "zoom": 0.10, "text": "1. anatomy 🦴", "xfade": SLIDE},
    {"t": 4.6,   "src": "IMG_1366", "in": 0.5, "text": "every bone. every muscle."},
    # 2. physiology
    {"t": 7.0,   "src": "IMG_6455", "in": 7.0, "vzoom": 2.0, "cx": 0.5, "cy": 0.8, "ty": 0.2,
     "text": "2. physiology 🫀", "xfade": SLIDE},
    {"t": 9.6,   "src": "IMG_1480", "in": 4.0, "text": "how the body actually works"},
    # 3. biochemistry
    {"t": 11.8,  "src": "67168F2A", "in": 2.65, "stabilize": True, "text": "3. biochemistry 🧪", "xfade": SLIDE},
    {"t": 13.05, "src": "IMG_4318", "in": 3.3, "text": "reactions, colours, chaos"},
    # ending
    {"t": 15.05, "src": "IMG_9328", "in": 1.3, "text": "1 year. 3 subjects. 0 sleep.", "xfade": "fadewhite"},
]

SFX = [
    # intro
    ("pop", 0.30, -16),
    ("Reverse_Bass", 2.40, -8),            # rises into the first section
    # anatomy
    ("My_fav_whoosh", 2.40, 0),
    ("Bone_Crack_Sound_Effect", 2.62, -1),
    ("pop", 2.65, -15),
    ("Bone_Crack_Sound_Effect", 3.70, -9),
    ("Quick_whoosh", 4.60, -4),
    ("tick", 4.82, -20), ("pop", 4.85, -17),
    ("Lit_cloth_roll_2", 5.90, -6),        # model spinning on the iPad
    # physiology
    ("Whoosh_2", 7.00, -2),
    ("pop", 7.25, -15),
    ("Lit_heartbeat1", 7.45, 0),
    ("beep", 7.95, -17),
    ("Lit_heartbeat1", 8.35, -2),
    ("beep", 8.85, -17),
    ("Lit_heartbeat1", 9.25, -4),
    ("Quick_whoosh", 9.60, -4),
    ("pop", 9.85, -17),
    ("tick", 10.40, -20), ("tick", 10.75, -21), ("tick", 11.10, -20),   # pen on paper
    # biochemistry
    ("Whoosh_4", 11.80, 0),
    ("pop", 12.00, -15),
    ("bubble", 12.10, -14), ("bubble", 12.30, -15), ("bubble", 12.48, -14),
    ("Lit_energy_release", 12.55, -8),     # the reaction "works"
    ("bubble", 12.75, -16), ("bubble", 12.92, -15),
    ("Quick_whoosh", 13.05, -4),
    ("pop", 13.30, -17),
    ("bubble", 13.70, -18), ("bubble", 14.20, -18), ("bubble", 14.65, -19),
    # ending
    ("Lit_whoosh_impact", 15.10, -3),
    ("THE_Boom_Sound_Effect", 15.30, -4),
    ("Lit_body_punch", 15.30, -8),
    ("Lit_cloth_roll_3", 15.90, -7),       # coat swish
    ("Lit_heartbeat1", 16.70, -6),
]
