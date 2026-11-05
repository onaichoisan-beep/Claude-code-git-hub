"""Sound for "Hiccups are a fish thing" (hiccups + the tadpole theory): text cards + open-source sound only (NO narration).

SIGNATURE sound = the HIC: a sharp glottal click (noise burst + rising chirp + a chest thump). Every hiccup on screen
gets one and ticks the HICCUPS counter; the tadpole's gulp-and-shut gets the same sound underwater (bubbly); in the
record section the hics speed up from 1/s to 12/s while the counter races to ~430,000,000. 8-bit bed, card blips,
whooshes, a calendar-flip ratchet, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 27.2
B = dict(DIAP=2.0, AIR=4.0, SHUT=6.0, WHY=8.0, BREAK=9.75, HIT=10.0, GULP=12.0, KEPT=14.0, REC=16.0, NAME=18.0,
         MILL=20.0, KIDS=22.0, CTA=24.0, STOP=25.9, REWIND=26.7)

CARDS = [
    (0.10, 1.90, "HIC! THAT'S A|*FISH* THING"),
    (2.00, 3.90, "YOUR *DIAPHRAGM*|SPASMS..."),
    (4.00, 5.90, "...AIR RUSHES|IN..."),
    (6.00, 7.90, "...THEN THE|THROAT *SHUTS*"),
    (8.00, 9.70, "BUT WHY DO WE|*HAVE* THIS?"),
    (10.00, 11.90, "ONE THEORY:|*TADPOLES*"),
    (12.00, 13.90, "THEY GULP, THEN|*SNAP SHUT*"),
    (14.00, 15.90, "WE MAY HAVE KEPT|THE *REFLEX*"),
    (16.00, 17.90, "THE RECORD?|*68 YEARS*"),
    (18.00, 19.90, "CHARLES OSBORNE|*1922-1990*"),
    (20.00, 21.90, "~430 MILLION|*HICCUPS*"),
    (22.00, 23.90, "HE STILL HAD|*8 KIDS*"),
    (24.00, 25.80, "TAG SOMEONE|WHO *HICCUPS*"),
]
# hiccups (shared with the picture)
H = [0.25]
H += [B["DIAP"] + 0.6, B["DIAP"] + 1.7, B["AIR"] + 0.9, B["SHUT"] + 0.5, B["SHUT"] + 1.6, B["WHY"] + 0.8]
GULPS = [B["HIT"] + 0.6, B["HIT"] + 1.5, B["GULP"] + 0.4, B["GULP"] + 1.2, B["KEPT"] + 0.5, B["KEPT"] + 1.4]
t = B["REC"] + 0.2
while t < B["KIDS"]:
    H.append(round(t, 3))
    u = (t - B["REC"]) / (B["KIDS"] - B["REC"])
    t += 1 / (1.0 + 11 * u ** 1.5)
H += [B["KIDS"] + 0.7, B["CTA"] + 0.4, B["CTA"] + 1.4]
B["HICS"] = [round(x, 3) for x in sorted(H)]
B["GULPS"] = GULPS

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["DIAP"], 104, 104, "kbh"),
    S(B["DIAP"], B["WHY"], 112, 112, "kbha"),
    S(B["WHY"], B["BREAK"], 100, 120, "kbhs"),
    S(B["HIT"] + 0.1, B["REC"], 96, 96, "kbo"),
    S(B["REC"], B["KIDS"], 120, 150, "kbhsa"),
    S(B["KIDS"], B["STOP"] + 0.2, 128, 128, "kbhsal"),
], gain=0.44, crescendo=(0.8, 1.15))
amb.x += (0.16 * F.drone(DUR, 60, seed=4) * seg(B["HIT"], B["REC"], 0.3))[:, None]


def hic(t, g=1.0, wet=False):
    fx.put(noise_hit(0.04, 1200, 6000), t, 0.6 * g)
    fx.put(CT.tone_glide(220, 520, 0.08, "square", 0.4, 0.6), t + 0.01, 0.22 * g)
    fx.put(thump(110, 0.12, 2.0), t, 0.5 * g)
    if wet:
        fx.put(osfx.sound("oga/water-splash/bubble_0" + str(1 + int(t * 10) % 3), F.bubble_(0.5, 700)), t + 0.05, 0.4 * g)


for k, h in enumerate(B["HICS"]):
    hic(h, 0.6 if B["REC"] + 1 < h < B["KIDS"] else 1.0)
    fx.put(F.tick(2000 + 30 * (k % 30), 0.8), h + 0.02, 0.15)
for gt in GULPS:
    fx.put(osfx.sound("oga/water-splash/slime_0" + str(1 + int(gt * 7) % 9), F.splash(0.3, 2)), gt - 0.3, 0.3)
    hic(gt, 0.9, wet=True)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
for c in [B["DIAP"], B["AIR"], B["SHUT"], B["WHY"], B["GULP"], B["KEPT"], B["REC"], B["NAME"], B["MILL"], B["KIDS"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(noise_hit(1.2, 300, 1500), B["AIR"] + 0.2, 0.2)
fx.put(CT.womp(392, 3, 0.22), B["WHY"] + 0.4, 0.15)
fx.put(riser(B["BREAK"] - B["WHY"], 200, 1600), B["WHY"], 0.25)
fx.put(impact(0.8), B["HIT"], 0.6)
fx.put(osfx.sound("oga/water-splash/splash_03", F.splash(0.8, 5)), B["HIT"], 0.6)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["KEPT"] + 0.8, 0.25)
fx.put(F.ratchet(1.6, 18, 1600, seed=3), B["REC"] + 0.2, 0.25)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.6)), B["MILL"] + 1.4, 0.3)
for k in range(8):
    fx.put(osfx.sound(f"oga/creatures/cute_0{k % 9 + 1}", blip(1200 + 80 * k)), B["KIDS"] + 0.2 + k * 0.14, 0.22, (k % 2) - 0.5)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 104, 104, "kbh")], gain=0.44, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["HICS"]), "hics; DUR", DUR)
