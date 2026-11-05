"""Sound for "These aren't its eyes" (the zombie snail, Leucochloridium): text cards + open-source sound (NO narration).

SIGNATURE sound = the PULSE: a wet squelchy throb on every pulse of the swollen eye-stalks (the PULSES counter), steady
at first and speeding up as the snail climbs into the sun and the bird comes; after the reveal the same throb becomes
the worm's heartbeat through the life cycle (bird gulp, plop of the poop, snail munch). 8-bit bed, card blips, whooshes,
a bird chirp + peck, tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(PULSE=2.0, SHADE=4.0, SUN=6.0, WHY=8.0, BIRD=10.0, BREAK=11.75, HIT=12.0, NAME=14.0, NEED=16.0, DRIVE=18.0,
         BITE=20.0, GROW=22.0, POOP=24.0, EATS=26.0, STOP=27.9, REWIND=28.7)
CARDS = [
    (0.10, 1.90, "THESE AREN'T|ITS *EYES*"),
    (2.00, 3.90, "THEY'RE *PULSING*"),
    (4.00, 5.90, "A NORMAL SNAIL|HIDES IN *SHADE*"),
    (6.00, 7.90, "THIS ONE CLIMBS|INTO THE *SUN*"),
    (8.00, 9.90, "WHY WOULD IT|*WANT* TO BE SEEN?"),
    (10.00, 11.70, "A BIRD THINKS:|*CATERPILLARS!*"),
    (12.00, 13.90, "IT'S A *WORM*|INSIDE THE SNAIL"),
    (14.00, 15.90, "LEUCOCHLORIDIUM|*A PARASITE*"),
    (16.00, 17.90, "IT NEEDS TO GET|INTO A *BIRD*"),
    (18.00, 19.90, "SO IT DRIVES|THE SNAIL *UP*"),
    (20.00, 21.90, "THE BIRD BITES|THE *EYE-STALK*"),
    (22.00, 23.90, "THE WORM GROWS|IN THE BIRD..."),
    (24.00, 25.90, "...EGGS IN|ITS *POOP*..."),
    (26.00, 27.80, "...A SNAIL EATS|IT. *REPEAT*."),
]
P, t = [], 0.15
while t < B["BREAK"]:
    P.append(round(t, 3))
    u = t / B["BREAK"]
    t += 1 / (1.4 + 3.6 * u ** 2)
B["PULSES"] = P

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec
fx.x += CT.bed([
    S(0.0, B["SHADE"], 96, 96, "kbo"),
    S(B["SHADE"], B["BREAK"], 112, 132, "kbha"),
    S(B["HIT"] + 0.1, B["BITE"], 100, 100, "kbhl"),
    S(B["BITE"], B["STOP"] + 0.2, 124, 124, "kbhsa"),
], gain=0.46, crescendo=(0.8, 1.15))
amb.x += (0.14 * F.crickets(DUR, seed=6))[:, None]
for k, pt in enumerate(P):
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 16 + 1:02d}", F.splash(0.25, k)), pt, 0.3, 0.3 * ((k % 3) - 1))
    fx.put(thump(70 + 2 * k, 0.12, 2.0), pt, 0.4)
    fx.put(F.tick(1800 + 25 * k, 0.8), pt + 0.02, 0.15)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
for c in [B["PULSE"], B["SHADE"], B["SUN"], B["WHY"], B["BIRD"], B["NAME"], B["NEED"], B["DRIVE"], B["BITE"], B["GROW"], B["POOP"], B["EATS"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["SUN"] + 0.4, 0.25)
fx.put(CT.womp(392, 3, 0.22), B["WHY"] + 0.5, 0.15)
fx.put(F.chirp(seed=3), B["BIRD"] + 0.2, 0.45, 0.4)
fx.put(F.chirp(seed=9), B["BIRD"] + 0.9, 0.4, 0.4)
fx.put(riser(B["BREAK"] - B["WHY"], 200, 1800), B["WHY"], 0.25)
fx.put(impact(0.9), B["HIT"], 0.7)
fx.put(braam(1.5, 52), B["HIT"], 0.35)
fx.put(osfx.sound("oga/creatures/weird_05", blip(500)), B["NAME"] + 0.4, 0.3)
for k in range(5):
    fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_footstep_wet_0" + str(1 + k % 3), F.tick(700, 0.6)), B["DRIVE"] + 0.3 + k * 0.3, 0.3)
fx.put(F.chirp(seed=5), B["BITE"] + 0.1, 0.45)
fx.put(osfx.sound("oga/creatures/eat_02", thump(260, 0.08, 2)), B["BITE"] + 0.8, 0.6)
fx.put(osfx.sound("oga/creatures/burp_01", thump(140, 0.2, 1.5)), B["GROW"] + 1.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/plop_01", F.splash(0.5, 3)), B["POOP"] + 0.6, 0.6)
for k in range(5):
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(300, 0.08, 1.5)), B["EATS"] + 0.3 + k * 0.25, 0.35)
for k in range(6):
    fx.put(osfx.sound(f"oga/water-splash/slime_0{k % 9 + 1}", F.splash(0.25, k)), B["EATS"] + 1.0 + k * 0.15, 0.25)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 96, 96, "kbo")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)
master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(P), "pulses; DUR", DUR)
