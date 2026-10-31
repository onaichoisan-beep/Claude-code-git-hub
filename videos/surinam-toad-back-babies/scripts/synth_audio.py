"""Sound for "Babies hatching out of their mother's back" (Surinam toad): text cards + open-source sound only (no narration),
STYLE_GUIDE.md section 6:

- SIGNATURE sound = the pop. Every toadlet that pushes out of its pocket is one wet pop (+ a tick on the BABIES OUT counter);
  the pops start slow and speed up (2/s -> 25/s) until they blur into a bubbling fizz, then the skin peels off.
- before that: wet squelches as the eggs land and the skin swallows them, a tick for every DAY (1 -> 100) that blurs into a
  buzz, a heartbeat under the wait; the river: bubbles + a murky drone.
- Nonstop 8-bit bed, 0.25 s break before the first pop, blip on every card, whoosh + hit on every cut, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 30.0
B = dict(RIVER=4.0, FLIP=8.0, SWALLOW=12.5, WAIT=15.5, BREAK=19.75, HIT=20.0, SHED=24.5, CTA=26.5, STOP=28.7, REWIND=29.5)
NPOCK = 72

CARDS = [
    (0.10, 1.95, "THESE HOLES ARE|FULL OF *BABIES*"),
    (2.05, 3.90, "AND THEY'RE ALL|*HER* KIDS"),
    (4.10, 5.90, "THE *SURINAM TOAD*"),
    (6.00, 7.90, "FLAT AS A LEAF, IN|SOUTH AMERICAN *RIVERS*"),
    (8.10, 10.30, "WHEN THEY MATE, THEY DO|UNDERWATER *FLIPS*"),
    (10.40, 12.30, "UP TO *100 EGGS*|LAND ON HER BACK"),
    (12.50, 15.30, "HER SKIN *SWALLOWS*|EVERY EGG"),
    (15.50, 17.60, "THE BABIES GROW|*INSIDE* HER SKIN"),
    (17.70, 19.70, "FOR 3-4 MONTHS.|*NO TADPOLES.*"),
    (20.00, 22.20, "THEN THEY|*PUSH OUT*"),
    (22.30, 24.40, "FULLY FORMED|*BABY TOADS*"),
    (24.50, 26.40, "THEN SHE *SHEDS*|THE SKIN"),
    (26.50, 28.60, "TAG SOMEONE WHO|CAN'T LOOK AT *HOLES*"),
]


def opens():
    """the moment each pocket opens: 2/s -> 25/s, all NPOCK done before SHED"""
    out, t = [], B["HIT"]
    while len(out) < NPOCK:
        out.append(round(t, 3))
        u = len(out) / NPOCK
        t += 1 / (2 + 23 * u ** 1.6)
    k = (B["SHED"] - 0.5 - B["HIT"]) / (out[-1] - B["HIT"])
    return [round(B["HIT"] + (x - B["HIT"]) * k, 3) for x in out]


def flips():
    """the top of each underwater loop: a batch of eggs is released"""
    return [round(B["FLIP"] + 0.7 + k * 1.25, 3) for k in range(3)]


def days():
    out = []
    for d in range(1, 101):
        u = (d - 1) / 99
        out.append(round(B["WAIT"] + 0.2 + (B["BREAK"] - 0.4 - B["WAIT"]) * (1 - (1 - u) ** 1.8), 3))
    return out


B["OPENS"] = opens()
B["FLIPS"] = flips()
B["DAYS"] = days()

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed
fx.x += CT.bed([
    S(0.0, B["RIVER"], 100, 100, "kbh"),
    S(B["RIVER"], B["FLIP"], 96, 100, "kbo"),
    S(B["FLIP"], B["SWALLOW"], 116, 120, "kbha"),
    S(B["SWALLOW"], B["WAIT"], 110, 110, "kbh"),
    S(B["WAIT"], B["BREAK"], 110, 150, "kbhsa"),
    S(B["HIT"], B["SHED"], 132, 132, "kbhsal"),
    S(B["SHED"], B["STOP"] + 0.2, 124, 124, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))
amb.x += (0.2 * F.drone(DUR, 55, seed=11))[:, None]           # murky river
for k in range(int(DUR / 1.9)):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.6, 400 + 80 * (k % 4))), 0.6 + k * 1.9, 0.12, (k % 3 - 1) * 0.6)

# ---------------------------------------------------------------- 0. the holes (the story starts here): babies peek, squirm
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(braam(1.8, 52), 0.05, 0.3)
for k in range(8):
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 9 + 1:02d}", F.splash(0.2, k)), 0.15 + k * 0.42, 0.18, (k % 3 - 1) * 0.5)
fx.put(osfx.sound("oga/creatures/cute_02", blip(1300, 0.15)), 0.6, 0.45)        # HI MOM!
fx.put(osfx.lib("glitch-1"), 2.05, 0.2)

# ---------------------------------------------------------------- 1. the river
fx.put(osfx.lib("whoosh"), B["RIVER"] - 0.15, 0.5)
fx.put(impact(0.5), B["RIVER"], 0.35)
fx.put(osfx.sound("oga/water-splash/loop_water_01", F.sea(3.5, seed=2)), B["RIVER"] + 0.1, 0.25)

# ---------------------------------------------------------------- 2. the flips: a swoosh per loop, eggs land (squelch + tick per batch)
fx.put(osfx.lib("whoosh-cinematic"), B["FLIP"] - 0.2, 0.5)
for k, t in enumerate(B["FLIPS"]):
    fx.put(osfx.lib("whoosh"), t - 0.5, 0.45, (k % 2) * 0.6 - 0.3)
    fx.put(osfx.sfxr("jump", seed=30 + k), t - 0.1, 0.25)
    for e in range(6):
        fx.put(osfx.sound(f"oga/water-splash/slime_{(e + 3 * k) % 9 + 1:02d}", F.splash(0.2, e)), t + 0.35 + e * 0.07, 0.25, (e % 3 - 1) * 0.4)
        fx.put(F.tick(2600 + 100 * e, 0.8), t + 0.35 + e * 0.07, 0.2)

# ---------------------------------------------------------------- 3. the skin swallows the eggs: a long wet stretch
fx.put(osfx.lib("whoosh"), B["SWALLOW"] - 0.15, 0.45)
for k in range(10):
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 9 + 1:02d}", thump(120 + 15 * k, 0.1, 1.5)), B["SWALLOW"] + 0.3 + k * 0.24, 0.3, (k % 3 - 1) * 0.5)
fx.put(sweep(2.6, 180, 90) * 0.4, B["SWALLOW"] + 0.2, 0.4)

# ---------------------------------------------------------------- 4. the wait: a tick per DAY (blurring into a buzz) + heartbeat
for k, t in enumerate(B["DAYS"]):
    fx.put(F.tick(1800 + 14 * k, 0.8), t, 0.22)
for k in range(5):
    fx.put(heartbeat(), B["WAIT"] + 0.3 + k * 0.8, 0.35)
fx.put(riser(B["BREAK"] - B["WAIT"], 150, 1700), B["WAIT"], 0.3)

# ---------------------------------------------------------------- 5. SIGNATURE: the pops
fx.put(osfx.sound("oga/water-splash/splash_02", F.splash(0.8, 4)), B["HIT"], 0.8)
fx.put(impact(0.8), B["HIT"], 0.6)
for k, t in enumerate(B["OPENS"]):
    g = 0.5 if k < 6 else 0.3
    fx.put(osfx.lib("pop") if k % 2 == 0 else osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.5, 600)), t, g, ((k * 7) % 5 - 2) * 0.3)
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 9 + 1:02d}", F.splash(0.2, k)), t + 0.01, g * 0.5)
    if k < 10:
        fx.put(osfx.sound(f"oga/creatures/cute_0{k % 9 + 1}", blip(1200 + 80 * k, 0.1)), t + 0.15, 0.2)

# ---------------------------------------------------------------- 6. the skin peels off
fx.put(osfx.lib("whoosh-cinematic"), B["SHED"] - 0.1, 0.5)
fx.put(osfx.sound("oga/water-splash/slime_05", sweep(0.9, 400, 120)), B["SHED"] + 0.1, 0.6)
fx.put(F.creak(0.9, 140, seed=4), B["SHED"] + 0.1, 0.25)
fx.put(osfx.sfxr("powerUp", seed=14), B["SHED"] + 1.2, 0.35)
fx.put(F.sparkle(1.0, seed=6), B["SHED"] + 1.25, 0.3)

# ---------------------------------------------------------------- 7. CTA: the babies hop around her
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
for k in range(6):
    fx.put(osfx.sfxr("jump", seed=40 + k), B["CTA"] + 0.2 + k * 0.32, 0.18, (k % 3 - 1) * 0.6)
fx.put(osfx.sound("oga/creatures/grunt_02", sweep(0.3, 300, 200)), B["CTA"] + 0.3, 0.3)

# ---------------------------------------------------------------- 8. tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kbh")], gain=0.5, crescendo=(0.8, 0.8))
amb.x += (0.2 * F.drone(DUR, 55, seed=11) * seg(B["REWIND"] + 0.1, DUR, 0.1))[:, None]

CT.card_blips(fx, CARDS, gain=0.15)
for tc in (B["WAIT"],):
    fx.put(osfx.lib("whoosh"), tc - 0.15, 0.4)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("opens", B["OPENS"][:5], "...", B["OPENS"][-1], "DUR", DUR)
