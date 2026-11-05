"""Sound for "You can't unsee your nose now": text cards + open-source sound (NO narration), interactive.

SIGNATURE sound = the NOSE ALERT: a two-tone "notice" ping each time the nose pops back into view (the NOSE VISIBLE %
counter jumps), and an eraser "rub-rub" + soft glitch every time the brain deletes it. Sniffs, socks/watch/fridge
foley (rustle, tick, hum), the 0.25 s break before "BUT NOW YOU NOTICED IT", 8-bit bed, card blips, tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(EVERY=2.0, PAGE=4.0, WHY=6.0, DELETE=8.0, IGNORE=10.0, SOCKS=12.0, FRIDGE=14.0, BREAK=15.75, HIT=16.0,
         UNSEE=18.0, CLOSE=20.0, TWO=22.0, FADE=24.0, CTA=26.0, STOP=27.9, REWIND=28.7)
CARDS = [
    (0.10, 1.90, "LOOK AT YOUR|*NOSE*."),
    (2.00, 3.90, "IT'S IN *EVERY*|THING YOU SEE"),
    (4.00, 5.90, "EVERY PAGE.|EVERY *SCREEN*."),
    (6.00, 7.90, "SO WHY DO YOU|*NEVER* SEE IT?"),
    (8.00, 9.90, "YOUR BRAIN|*DELETES* IT"),
    (10.00, 11.90, "IT IGNORES WHAT|*NEVER CHANGES*"),
    (12.00, 13.90, "LIKE YOUR SOCKS.|OR YOUR *WATCH*."),
    (14.00, 15.70, "OR A FRIDGE|*HUMMING*"),
    (16.00, 17.90, "BUT NOW YOU|*NOTICED* IT"),
    (18.00, 19.90, "AND NOW YOU|*CAN'T UNSEE IT*"),
    (20.00, 21.90, "TRY CLOSING|*ONE EYE*..."),
    (22.00, 23.90, "TWO NOSES. ONE|FOR EACH *EYE*"),
    (24.00, 25.90, "DON'T WORRY. IT|*FADES* SOON"),
    (26.00, 27.80, "SEND THIS TO|*RUIN* A FRIEND"),
]
B["ALERTS"] = [0.3, B["HIT"], B["CLOSE"] + 0.6, B["TWO"] + 0.3]
B["ERASE"] = [B["DELETE"] + 0.4, B["FADE"] + 0.6]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec
fx.x += CT.bed([
    S(0.0, B["DELETE"], 108, 112, "kbh"),
    S(B["DELETE"], B["BREAK"], 112, 128, "kbha"),
    S(B["HIT"] + 0.1, B["FADE"], 124, 124, "kbhsal"),
    S(B["FADE"], B["STOP"] + 0.2, 112, 112, "kbha"),
], gain=0.46, crescendo=(0.8, 1.15))


def alert(t, g=1.0):
    fx.put(CT.square(988, 0.08, 0.5), t, 0.18 * g)
    fx.put(CT.square(1319, 0.12, 0.5), t + 0.09, 0.18 * g)
    fx.put(osfx.sound("oga/creatures/nose", noise_hit(0.2, 800, 3000)), t + 0.25, 0.4 * g)          # a sniff


def erase(t, d=1.4):
    k = 0
    while k * 0.16 < d:
        fx.put(noise_hit(0.12, 1500, 5000), t + k * 0.16, 0.3, (k % 2) - 0.5)
        k += 1
    fx.put(osfx.lib("glitch-1"), t + d, 0.3)


for a in B["ALERTS"]:
    alert(a, 1.3 if a == B["HIT"] else 1.0)
for e in B["ERASE"]:
    erase(e)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
for c in [B["EVERY"], B["PAGE"], B["WHY"], B["DELETE"], B["IGNORE"], B["SOCKS"], B["FRIDGE"], B["UNSEE"], B["CLOSE"], B["TWO"], B["FADE"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
for k in range(3):
    fx.put(osfx.sound("oga/100-sfx/paper_0" + str(1 + k), F.page_flip(k)), B["PAGE"] + 0.3 + k * 0.4, 0.3)
fx.put(CT.womp(392, 3, 0.22), B["WHY"] + 0.5, 0.15)
fx.put(osfx.sound("oga/retro-synth/synth_misc_08", blip(800)), B["IGNORE"] + 0.4, 0.25)
fx.put(noise_hit(0.4, 400, 2000), B["SOCKS"] + 0.3, 0.25)
for k in range(8):
    fx.put(F.tick(3000, 0.9), B["SOCKS"] + 1.0 + k * 0.12, 0.18)
n = int(1.6 * SR)
tt = np.arange(n) / SR
fx.put(np.sin(2 * np.pi * 60 * tt) * 0.5 + 0.2 * np.sin(2 * np.pi * 120 * tt) * np.exp(-((tt - 0.8) ** 2) * 2), B["FRIDGE"] + 0.1, 0.25)
fx.put(riser(B["BREAK"] - B["FRIDGE"], 200, 1600), B["FRIDGE"], 0.22)
fx.put(impact(0.9), B["HIT"], 0.6)
fx.put(braam(1.2, 55), B["HIT"], 0.3)
fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(1500, 1.0)), B["CLOSE"] + 0.4, 0.35)
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up()), B["FADE"] + 0.2, 0.2)
fx.put(osfx.sound("oga/creatures/misc_07", blip(700)), B["CTA"] + 0.6, 0.3)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 108, 108, "kbh")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)
master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=6.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
