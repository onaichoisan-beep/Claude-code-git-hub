"""Sound for "The 400-year-old shark" (Greenland shark) — sound follows the counter (STYLE_GUIDE.md section 6), no narration,
no cold-open hook: a slow deep Arctic drone + ice creaks; the carbon-dating scan beeps faster to the reveal (0.25 s break,
hit); then a tick for every DECADE of the YEAR counter (1624 -> 2016) that speeds up as history races past, with a chime
on every milestone; a party horn at 150; a crown fanfare; tape-stop + rewind into frame 1.

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
B = dict(SLOW=2.6, GROW=5.0, LENS=8.0, BREAK=10.75, HIT=11.0, TIMELINE=13.0, TEEN=21.5, LONG=23.5, CTA=25.5, STOP=28.5, REWIND=29.3)

CARDS = [
    (0.10, 2.50, "THIS SHARK MIGHT BE|OLDER THAN THE *USA*"),
    (2.60, 4.90, "THE *GREENLAND SHARK*|LIVES IN ICY WATER"),
    (5.00, 7.90, "IT GROWS LESS THAN|*1 CM* A YEAR"),
    (8.00, 10.60, "SCIENTISTS DATED|THE LENS OF ITS *EYE*"),
    (11.00, 12.90, "ABOUT *392 YEARS* OLD"),
    (13.10, 15.40, "IT WAS PROBABLY BORN|AROUND *1624*"),
    (15.50, 17.60, "BEFORE NEWTON'S|*LAWS OF MOTION*"),
    (17.70, 19.60, "BEFORE THE *USA*|EXISTED"),
    (19.70, 21.40, "STILL SWIMMING IN *2016*"),
    (21.50, 23.40, "IT BECOMES AN ADULT|AT ABOUT *150*"),
    (23.50, 25.40, "THE LONGEST-LIVING|*VERTEBRATE* KNOWN"),
    (25.50, 28.40, "WHAT WOULD YOU DO|WITH *400 YEARS*?"),
]


def year_at(t):
    u = min(1.0, max(0.0, (t - B["TIMELINE"]) / (B["TEEN"] - B["TIMELINE"] - 0.4)))
    return 1624 + 392 * u ** 1.6


os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the slow Arctic bed + an 8-bit pulse that speeds up with time
amb.x += (0.4 * F.drone(DUR, 49, seed=5))[:, None]
fx.x += CT.bed([
    S(0.0, B["LENS"], 72, 76, "kbo"),
    S(B["LENS"], B["BREAK"], 100, 150, "kbh"),
    S(B["HIT"] + 0.2, B["TIMELINE"], 120, 120, "kbha"),
    S(B["TIMELINE"], B["TEEN"], 110, 168, "kbhsa"),
    S(B["TEEN"], B["CTA"], 128, 128, "kbhsal"),
    S(B["CTA"], B["STOP"] + 0.2, 120, 124, "kbha"),
], gain=0.45, crescendo=(0.8, 1.2))
for k in range(5):
    fx.put(F.ice_crack(59 + k, 0.6), 0.6 + k * 1.5, 0.35, (k % 3 - 1) * 0.6)
fx.put(braam(2.0, 44), 0.0, 0.4)

# the growth ruler: one painfully slow tick
fx.put(F.tick(1800, 1.0), B["GROW"] + 1.0, 0.5)
fx.put(CT.womp(330, 3, 0.35), B["GROW"] + 1.6, 0.25)

# ---------------------------------------------------------------- the carbon-dating scan: beeps faster -> break -> reveal
t = B["LENS"] + 0.3
gap = 0.45
while t < B["BREAK"] - 0.05:
    fx.put(CT.square(1500 + 800 * (t - B["LENS"]) / 3, 0.05, 0.25), t, 0.35)
    t += gap
    gap = max(0.06, gap * 0.82)
fx.put(osfx.sound("oga/scifi/teleport_01", sweep(0.5, 300, 1500)), B["LENS"] + 0.1, 0.4)
fx.put(sweep(B["HIT"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.5)
fx.put(osfx.sound("oga/100-sfx/slam_02", impact(1.0)), B["HIT"], 0.9)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(sub_drop(1.2), B["HIT"], 0.8)
fx.put(osfx.sound("oga/100-sfx/gong_01", gong(98)), B["HIT"] + 0.05, 0.5)

# ---------------------------------------------------------------- SIGNATURE: a tick per decade of the YEAR counter + milestone chimes
last = 1620
tt = B["TIMELINE"]
while tt < B["TEEN"]:
    y = year_at(tt)
    if y // 10 * 10 > last:
        last = int(y // 10 * 10)
        fx.put(F.tick(2200 + (last - 1620) * 3, 1.0), tt, 0.45, 0.4)
    tt += 0.005
for y, f0 in ((1687, 784), (1776, 880), (1903, 988), (1969, 1047), (2016, 1319)):
    ty = B["TIMELINE"] + (B["TEEN"] - B["TIMELINE"] - 0.4) * ((y - 1624) / 392) ** (1 / 1.6)
    fx.put(add(bell(f0, 1.2), 0.5 * bell(f0 * 1.5, 1.2)), ty, 0.45)
    fx.put(osfx.lib("pop"), ty, 0.3)
fx.put(riser(B["TEEN"] - B["TIMELINE"], 150, 1600), B["TIMELINE"], 0.3)

# ---------------------------------------------------------------- 150th birthday: party horn + confetti pops; crown fanfare
fx.put(CT.tone_glide(400, 900, 0.35, "square", 0.5, 0.35), B["TEEN"] + 0.2, 0.6)
fx.put(CT.tone_glide(900, 600, 0.25, "square", 0.5, 0.3), B["TEEN"] + 0.55, 0.5)
for k in range(4):
    fx.put(osfx.lib("pop"), B["TEEN"] + 0.3 + k * 0.12, 0.35, (k % 2) * 1.0 - 0.5)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["LONG"], 0.55)
for i, f0 in enumerate([523.25, 659.25, 783.99, 1046.5]):
    fx.put(bell(f0, 1.6), B["LONG"] + 0.1 + i * 0.08, 0.3)

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.15)
for tc in (B["LENS"], B["TIMELINE"], B["TEEN"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.5)
    fx.put(impact(0.5), tc, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 72, 72, "kbo")], gain=0.45, crescendo=(0.8, 0.8))
amb.x += (0.4 * F.drone(DUR, 49, seed=5) * seg(B["REWIND"] + 0.1, DUR, 0.2))[:, None]

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=7.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
