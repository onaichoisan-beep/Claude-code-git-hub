"""Sound for "Hagfish: a bucket of slime in one second": text cards + open-source sound only (NO narration).

SIGNATURE sound = the SQUELCH. Wet slime squelches whose rate follows the SLIME X counter (1/s -> 14/s while it
grows 10,000x), then slower squelches as the knot scrapes the slime off (CLEANING %), and the big wet SPLAT of the
truck crash. 8-bit bed under everything, a blip on every card, whoosh + hit on every cut, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(MEET=2.1, GLAND=4.0, BURST=6.0, GROWN=8.0, CLOG=10.0, SPIT=12.0, KNOT=14.0, SCRAPE=16.0, ROAD=18.0,
         BREAK=19.75, HIT=20.0, SPILL=22.0, CARS=24.0, CTA=26.0, STOP=27.9, REWIND=28.7)

CARDS = [
    (0.10, 2.00, "THE SHARK BIT|THE *WRONG FISH*"),
    (2.10, 3.90, "MEET THE|*HAGFISH*"),
    (4.00, 5.90, "ATTACKED? IT|MAKES *SLIME*"),
    (6.00, 7.90, "IN UNDER|*ONE SECOND*..."),
    (8.00, 9.90, "...IT GROWS|*10,000X*"),
    (10.00, 11.90, "THE SHARK'S|GILLS *CLOG*"),
    (12.00, 13.90, "SO IT *SPITS*|AND FLEES"),
    (14.00, 15.90, "TO CLEAN UP, IT|TIES A *KNOT*"),
    (16.00, 17.90, "...AND SCRAPES|IT *OFF*"),
    (18.00, 19.70, "OREGON,|*JULY 2017*"),
    (20.00, 21.90, "A HAGFISH TRUCK|*CRASHED*"),
    (22.00, 23.90, "3,400 KG OF|*SLIME FISH*"),
    (24.00, 25.90, "CARS GOT|*SLIMED*"),
    (26.00, 27.80, "SEND THIS TO|SOMEONE *SLIMY*"),
]
# the squelches (SLIME X counter): accelerating 1/s -> 14/s from BURST to GROWN+0.6
SQ, t = [], B["BURST"] + 0.15
while t < B["GROWN"] + 0.6:
    SQ.append(round(t, 3))
    u = (t - B["BURST"]) / (B["GROWN"] + 0.6 - B["BURST"])
    t += 1 / (1.5 + 12.5 * u ** 1.5)
B["SQUELCH"] = SQ
B["SCRAPES"] = [round(B["KNOT"] + 1.0 + k * 0.42, 3) for k in range(int((B["ROAD"] - B["KNOT"] - 1.2) / 0.42))]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["BURST"], 112, 116, "kbh"),
    S(B["BURST"], B["GROWN"] + 0.6, 120, 150, "kbhsa"),
    S(B["GROWN"] + 0.6, B["KNOT"], 120, 120, "kbha"),
    S(B["KNOT"], B["ROAD"], 104, 104, "kbo"),
    S(B["ROAD"], B["BREAK"], 126, 140, "kbhsa"),
    S(B["HIT"] + 0.1, B["STOP"] + 0.2, 124, 124, "kbhsal"),
], gain=0.48, crescendo=(0.8, 1.2))
amb.x += (0.14 * F.drone(DUR, 49, seed=6) * seg(0, B["ROAD"], 0.3))[:, None]
amb.x += (0.25 * F.wind(DUR, 300, 700, 0.3, seed=2) * seg(B["ROAD"], B["REWIND"], 0.3))[:, None]


def squelch(t, k, g=1.0):
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 16 + 1:02d}", F.splash(0.3, k)), t, 0.42 * g, (k % 3 - 1) * 0.35)


# 0. frame 1: the bite, slime starts
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(osfx.sound("oga/creatures/monster_03", roar(0.6, 110)), 0.15, 0.35)
fx.put(osfx.sound("oga/creatures/eat_03", thump(180, 0.1, 2)), 0.3, 0.6)
for k in range(4):
    squelch(0.6 + k * 0.35, k, 0.7)
# 1. meet the hagfish
fx.put(osfx.lib("whoosh"), B["MEET"] - 0.15, 0.45)
fx.put(osfx.sound("oga/creatures/cute_02", blip(1100)), B["MEET"] + 0.5, 0.4)
# 2. glands light up
fx.put(osfx.lib("whoosh"), B["GLAND"] - 0.15, 0.4)
for k in range(8):
    fx.put(F.tick(2600 + 140 * k, 0.8), B["GLAND"] + 0.3 + k * 0.1, 0.25)
fx.put(riser(B["BURST"] - B["GLAND"] - 0.2, 200, 1500), B["GLAND"] + 0.2, 0.25)
# 3. SIGNATURE: squelches speed up with SLIME X
fx.put(impact(0.7), B["BURST"], 0.5)
for k, st in enumerate(SQ):
    squelch(st, k + 3)
    fx.put(F.tick(1500 + 40 * k, 0.9), st + 0.02, 0.2)
fx.put(osfx.sound("oga/retro-synth/retro_coin_02", bell(1318, 0.6)), B["GROWN"] + 0.65, 0.35)
fx.put(osfx.lib("whoosh"), B["GROWN"] - 0.15, 0.35)
# 4. gills clog: gag, cough
fx.put(osfx.lib("whoosh"), B["CLOG"] - 0.15, 0.4)
fx.put(osfx.sound("oga/creatures/cough_01", thump(120, 0.2, 1.5)), B["CLOG"] + 0.5, 0.55)
fx.put(osfx.sound("oga/creatures/cough_03", thump(110, 0.2, 1.5)), B["CLOG"] + 1.3, 0.5)
# 5. spit + flee
fx.put(osfx.sound("oga/creatures/spit_02", F.splash(0.5, 2)), B["SPIT"] + 0.2, 0.8)
fx.put(osfx.sound("oga/water-splash/splash_08", F.splash(0.6, 5)), B["SPIT"] + 0.3, 0.5)
fx.put(osfx.lib("whoosh-cinematic"), B["SPIT"] + 0.7, 0.5)
fx.put(osfx.sound("oga/retro-synth/retro_die_03", CT.womp(330, 3, 0.2)), B["SPIT"] + 1.0, 0.3)
fx.put(osfx.sfxr("pickupCoin", seed=4), B["SPIT"] + 1.4, 0.3)
# 6. the knot scrapes the slime off
fx.put(osfx.lib("whoosh"), B["KNOT"] - 0.15, 0.45)
fx.put(F.creak(0.5, 160, seed=4), B["KNOT"] + 0.4, 0.4)
for k, st in enumerate(B["SCRAPES"]):
    squelch(st, k + 8, 0.7)
    fx.put(sweep(0.15, 900, 400) * 0.5, st, 0.18)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["ROAD"] - 0.6, 0.3)
# 7. the road: engine, then BREAK -> CRASH
fx.put(osfx.lib("whoosh-cinematic"), B["ROAD"] - 0.2, 0.45)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_loop_highway", F.rumble(1.8)), B["ROAD"], 0.4)
fx.put(F.rumble(B["BREAK"] - B["ROAD"], 30, 200, seed=4), B["ROAD"], 0.4)
fx.put(osfx.sound("oga/100-sfx/slam_03", impact(1.0)), B["HIT"], 0.9)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(osfx.sound("oga/100-sfx/glass_02", F.glass_smash(3)), B["HIT"] + 0.05, 0.4)
fx.put(osfx.sound("oga/water-splash/splash_12", F.splash(1.0, 9)), B["HIT"] + 0.2, 0.8)
fx.put(sub_drop(1.0), B["HIT"], 0.6)
# 8. spill: many slimy plops
for k in range(10):
    squelch(B["SPILL"] + 0.1 + k * 0.18, k + 20, 0.6)
# 9. cars: honk-ish + wipers
fx.put(osfx.lib("whoosh"), B["CARS"] - 0.15, 0.4)
fx.put(CT.square(415, 0.35, 0.5) * 0.5, B["CARS"] + 0.3, 0.2)
fx.put(CT.square(370, 0.35, 0.5) * 0.5, B["CARS"] + 0.3, 0.2)
for k in range(4):
    fx.put(osfx.sound(f"oga/water-splash/slime_{(k % 4) + 5:02d}", sweep(0.2, 600, 300)), B["CARS"] + 0.8 + k * 0.4, 0.35)
# 10. CTA
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sound("oga/creatures/cute_08", blip(1200)), B["CTA"] + 0.5, 0.35)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 112, 112, "kbh")], gain=0.48, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(SQ), "squelches; DUR", DUR)
