# "Food tour of my MBBS life" - photo piles with pops, grouped, clips in between. Upbeat song.
DROP = 1.8
END = 21.6
def pops(t0, n, gap): return [round(t0 + i * gap, 2) for i in range(n)]
SHOTS = [
    {"t": 0.0,  "src": "FFC484C5", "in": 0.0, "speed": 0.9, "text": "food tour of my MBBS life 🍜"},
    {"t": 1.8,  "stack": ["IMG_5030", "IMG_3981", "IMG_0029", "IMG_0678", "IMG_0681"], "pops": pops(1.8, 5, 0.6),
     "text": "street food", "ty": 0.15},
    {"t": 5.0,  "src": "IMG_6575", "in": 1.0, "text": "+ juice, obviously"},
    {"t": 6.2,  "stack": ["IMG_0094", "IMG_3599", "IMG_2148", "IMG_3701", "IMG_8621", "IMG_8623", "IMG_4636"],
     "pops": pops(6.2, 7, 0.5), "text": "café hopping", "ty": 0.15},
    {"t": 9.8,  "src": "2A473245", "in": 1.0, "text": "11 PM…"},
    {"t": 11.0, "stack": ["IMG_6714", "IMG_8510", "IMG_0465", "IMG_0712", "IMG_0868", "IMG_0181", "IMG_0924"],
     "pops": pops(11.0, 7, 0.45), "text": "late-night cravings", "ty": 0.15},
    {"t": 14.2, "stack": ["IMG_3781", "IMG_0676", "IMG_0885"], "pops": pops(14.2, 3, 0.6),
     "text": "sweet tooth", "ty": 0.15},
    {"t": 16.2, "stack": ["IMG_4056", "IMG_0863"], "pops": [16.2, 16.9],
     "text": "mess (we don't talk about it)", "ty": 0.15},
    {"t": 18.0, "src": "0E716FE9", "in": 0.3, "pop_on_cut": False},
    {"t": 19.4, "src": "IMG_2134", "in": 0.0, "speed": 0.7, "text": "worth every rupee 🤤"},
]
SFX = [("Lit_body_punch", 18.0, -8)]
