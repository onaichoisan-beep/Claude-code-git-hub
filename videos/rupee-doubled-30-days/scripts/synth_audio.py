"""Narration + fast sound for "₹1 crore, or ₹1 doubled for 30 days?" (narrated on the owner's request, like the ancestors hit).

- Narrated: narrator (the ancestors-video voice), YOU (the same kid), the uncle — each their own voice.
- SIGNATURE = the coins. Every DAY on the counter is a coin clink a semitone higher than the last; as the money grows the
  clink becomes a pour (more coins per day) and finally a cash avalanche. Crossing ₹1 crore (day 25) = 0.3 s break + slam;
  day 30 = a register KA-CHING + the tower rising (riser) + impact.
- Fast pacing: a nonstop 8-bit bed 120 -> 170 BPM, a blip on every caption chunk, whoosh + hit on every cut, a tick on every
  counter change, a riser into each reveal, tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

LINES = json.load(open(os.path.join(HERE, "lines.json")))
GAPS = {1: 0.2, 2: 0.25, 3: 0.15, 4: 0.2, 5: 0.2, 6: 0.15, 7: 0.2, 8: 0.45, 9: 0.3, 10: 0.3}

CAPS = [
    [("*₹1 CRORE* NOW...", "one"), ("OR *₹1* THAT DOUBLES|EVERY DAY FOR 30 DAYS?", "or")],
    [("*1 CRORE!*|OBVIOUSLY.", "one")],
    [("DAY 1: *₹1*", "day"), ("DAY 2: *₹2*", "day"), ("DAY 5: *₹16*", "day")],
    [("HA! *TOLD YOU.*", "ha")],
    [("DAY 10: *₹512*", "day"), ("NOT EVEN A *PIZZA*", "not")],
    [("DAY 20: *₹5 LAKH*", "day"), ("STILL *LOSING*", "still")],
    [("WAIT... IT'S|*SPEEDING UP*", "wait")],
    [("DAY 25: *₹1.67 CRORE*", "day"), ("YOU JUST *LOST*", "you")],
    [("DAY 30:", "day"), ("*₹53.68 CRORE*", "fifty")],
    [("SHOULD HAVE PICKED|THE RUPEE, *BETA*", "should")],
    [("THE POWER OF *DOUBLING*", "that's"), ("COMMENT: *1 CRORE*|OR *₹1 DOUBLED*?", "comment")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.3, gaps=GAPS, max_pause=0.3)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E

B = {}
B["COIN"] = W(0, "or")
B["YOU1"] = A(1)
B["D1"], B["D2"], B["D5"] = W(2, "day", 0), W(2, "day", 1), W(2, "day", 2)
B["HA"] = A(3)
B["D10"], B["PIZZA"] = W(4, "day"), W(4, "pizza")
B["D20"], B["LOSING"] = W(5, "day"), W(5, "losing")
B["WAIT"] = A(6)
B["HIT"] = W(7, "day")
B["BREAK"] = B["HIT"] - 0.3
B["LOST"] = W(7, "lost")
B["D30"] = W(8, "day")
B["BIG"] = W(8, "fifty")
B["UNCLE"] = A(9)
B["CTA"] = A(10)
B["STOP"] = Bn(10) + 0.35
B["REWIND"] = B["STOP"] + 0.8
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)

DAYK = [[0.0, 0], [B["D1"], 1], [B["D2"], 2], [B["D2"] + 0.25, 2], [B["D5"], 5], [B["D5"] + 0.3, 5], [B["D10"], 10],
        [B["PIZZA"] + 0.4, 10], [B["D20"], 20], [B["WAIT"] + 0.2, 20], [B["BREAK"], 24], [B["HIT"], 25], [B["LOST"] + 0.3, 25],
        [B["D30"], 26], [B["BIG"], 30]]


def day(t):
    for (a, ga), (b, gb) in zip(DAYK, DAYK[1:]):
        if t < b:
            return ga if gb - ga <= 1 else ga + (gb - ga) * (t - a) / (b - a)
    return 30


steps, last = [], 0
for k in range(int(B["BIG"] * 200) + 2):
    d = int(day(k / 200) + 1e-6)
    if d != last:
        steps.append((k / 200, d))
        last = d
B["DAYK"] = [[round(a, 3), g] for a, g in DAYK]
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band)
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.45)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed: tempo climbs with the money
fx.x += CT.bed([
    S(0.0, B["D1"], 120, 120, "kbh"),
    S(B["D1"], B["D10"], 124, 132, "kbhs"),
    S(B["D10"], B["WAIT"], 132, 146, "kbhsa"),
    S(B["WAIT"], B["BREAK"], 146, 172, "kbhsa"),
    S(B["HIT"], B["D30"], 136, 136, "kbhsal"),
    S(B["D30"], B["UNCLE"], 150, 150, "kbhsal"),
    S(B["UNCLE"], B["CTA"], 112, 112, "kbh"),
    S(B["CTA"], B["STOP"] + 0.2, 140, 140, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- SIGNATURE: a clink per day, rising; then a pour
def clink(f, seed):
    n = int(0.12 * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    x = sum(np.sin(2 * np.pi * f * m * (1 + 0.003 * r.standard_normal()) * tt) * np.exp(-tt * (30 + 10 * m)) / m for m in (1, 2.76, 5.4))
    return x * 0.6


for t, d in steps:
    f = 1200 * 2 ** ((d - 1) / 12)
    fx.put(clink(f, d), t, 0.32, ((d % 3) - 1) * 0.4)
    fx.put(F.tick(2600 + 60 * d, 1.0), t, 0.22)
    pours = min(14, int(d / 3))                                   # more coins per day as the money grows
    for p in range(pours):
        fx.put(clink(f * (0.8 + 0.4 * ((p * 7) % 5) / 5), d * 31 + p), t + 0.03 + p * 0.025, 0.12, ((p % 5) - 2) * 0.3)
fx.put(CT.crackle(lambda t: 2 + 2.6 * day(t) ** 1.3, B["D10"], B["BREAK"], seed=7, base=3400), B["D10"], 0.12)
fx.put(riser(B["BREAK"] - B["WAIT"], 200, 2200), B["WAIT"], 0.3)

# ---------------------------------------------------------------- 0. the choice (story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(1046, 1.2)), 0.1, 0.25)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", blip(1600, 0.15)), B["COIN"], 0.45)
fx.put(F.sparkle(0.8, seed=3), B["COIN"] + 0.05, 0.25)
fx.put(osfx.sound("oga/100-sfx/slam_02", thump(90, 0.3, 1.5)), B["YOU1"] + 0.1, 0.4)     # YOU grabs the bag
fx.put(osfx.sfxr("pickupCoin", seed=3), B["YOU1"] + 0.15, 0.3)
fx.put(osfx.sfxr("jump", seed=7), B["HA"], 0.25)
fx.put(osfx.lib("whoosh"), B["D1"] - 0.15, 0.4)

# ---------------------------------------------------------------- milestones: pizza / 5 lakh / speeding up
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(392, 3, 0.15)), B["PIZZA"] + 0.3, 0.3)
fx.put(osfx.lib("whoosh"), B["D20"] - 0.15, 0.4)
fx.put(impact(0.5), B["D20"], 0.35)
fx.put(CT.womp(330, 3, 0.15), B["LOSING"] + 0.3, 0.2)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.3, 500, 900)), B["WAIT"] + 0.05, 0.25)

# ---------------------------------------------------------------- BREAK -> crossing ₹1 crore: slam
fx.put(sweep(0.3, 1400, 3000) * 0.3, B["BREAK"], 0.4)
fx.put(osfx.sound("oga/bangs-fireworks/bang_03", impact(1.0)), B["HIT"], 0.7)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(sub_drop(1.0), B["HIT"], 0.6)
fx.put(osfx.sfxr("powerUp", seed=5), B["HIT"] + 0.05, 0.35)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", CT.womp(330, 4, 0.18)), B["LOST"] + 0.2, 0.4)   # YOU lost

# ---------------------------------------------------------------- day 30: the tower rockets up
fx.put(riser(B["BIG"] - B["D30"], 300, 2400), B["D30"], 0.4)
fx.put(osfx.lib("whoosh-cinematic"), B["BIG"] - 0.2, 0.5)
fx.put(osfx.sound("oga/bangs-fireworks/cannon_01", impact(1.0)), B["BIG"], 0.6)
fx.put(impact(0.9), B["BIG"], 0.6)
fx.put(add(bell(1318.5, 1.0), bell(1975.5, 1.0)), B["BIG"] + 0.05, 0.3)          # ka-ching
for k in range(6):
    fx.put(osfx.sound(f"oga/bangs-fireworks/fw_0{k % 5 + 1}", F.firework(10 + k)), B["BIG"] + 0.3 + k * 0.28, 0.25, (k % 3 - 1) * 0.6)

# ---------------------------------------------------------------- uncle + CTA
fx.put(osfx.lib("whoosh"), B["UNCLE"] - 0.2, 0.45)
fx.put(impact(0.4), B["UNCLE"] - 0.05, 0.3)
fx.put(osfx.sound("oga/creatures/grunt_01", sweep(0.3, 220, 160)), B["UNCLE"] + E(9, "beta") - A(9) + 0.3, 0.2)
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sfxr("blipSelect", seed=4), W(10, "comment"), 0.35)
fx.put(osfx.sfxr("blipSelect", seed=6), W(10, "comment") + 0.4, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 120, 120, "kbh")], gain=0.5, crescendo=(0.8, 0.8))

CT.card_blips(fx, [(c["a"], c["b"], "") for c in captions], gain=0.14)
for c in captions:                                                   # a soft whoosh under every new card (fast pacing)
    fx.put(osfx.lib("whoosh-short") if hasattr(osfx, "lib") else sweep(0.1, 800, 2000), c["a"] - 0.05, 0.12)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=1.0, makeup_db=5.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.85, makeup_db=2.0)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({k: (round(v, 3) if not isinstance(v, list) else v) for k, v in B.items()}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
print("BEATS", {k: v for k, v in B.items() if not isinstance(v, list)})
print("DUR", DUR)
