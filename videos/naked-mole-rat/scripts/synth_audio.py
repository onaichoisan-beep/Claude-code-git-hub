"""Sound for "This rat shouldn't exist" (naked mole-rat): text cards + open-source sound (NO narration).

SIGNATURE sound = the RULE STAMP: every broken rule of biology gets a heavy stamp + a "rule-break" glitch, and the
RULES BROKEN counter ticks up (1 -> 6); between stamps, the digging scratch of tiny claws keeps going. The 0.25 s break
before rule 6 (it barely ages), a big hit, a queen fanfare, 8-bit bed, card blips, tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(UGLY=2.0, R1=4.0, R2=6.4, R3=8.8, R4=11.2, R5=13.6, BREAK=16.25, HIT=16.5, WHY=18.8, QUEEN=21.0, SCI=23.3,
         CTA=25.6, STOP=27.9, REWIND=28.7)
CARDS = [
    (0.10, 1.90, "THIS RAT|SHOULDN'T *EXIST*"),
    (2.00, 3.90, "IT BREAKS|*6 RULES* OF LIFE"),
    (4.00, 6.30, "RULE 1: LIVE|*37 YEARS*"),
    (6.40, 8.70, "RULE 2: ALMOST|NEVER *CANCER*"),
    (8.80, 11.10, "RULE 3: ACID?|IT FEELS *NO BURN*"),
    (11.20, 13.50, "RULE 4: NO AIR|FOR *18 MINUTES*"),
    (13.60, 16.20, "RULE 5: IT LIVES|LIKE *BEES*"),
    (16.50, 18.70, "RULE 6: IT|BARELY *AGES*"),
    (18.80, 20.90, "ITS DEATH RISK|*DOESN'T RISE*"),
    (21.00, 23.20, "ONE *QUEEN*,|UP TO 300 RATS"),
    (23.30, 25.50, "SCIENTISTS STUDY|IT FOR *ANTI-AGING*"),
    (25.60, 27.80, "UGLY? OR|*IMMORTAL*?"),
]
B["STAMPS"] = [B["R1"] + 0.9, B["R2"] + 0.9, B["R3"] + 0.9, B["R4"] + 0.9, B["R5"] + 0.9, B["HIT"]]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec
fx.x += CT.bed([
    S(0.0, B["R1"], 100, 104, "kbh"),
    S(B["R1"], B["BREAK"], 116, 136, "kbhsa"),
    S(B["HIT"] + 0.1, B["QUEEN"], 112, 112, "kbhl"),
    S(B["QUEEN"], B["STOP"] + 0.2, 124, 124, "kbhsal"),
], gain=0.46, crescendo=(0.8, 1.15))
amb.x += (0.12 * F.rumble(DUR, 30, 200, seed=5))[:, None]
t = 0.2
k = 0
while t < DUR - 1:
    fx.put(noise_hit(0.05, 1500, 6000), t, 0.12, ((k % 3) - 1) * 0.5)          # tiny claws digging
    t += 0.28 + 0.06 * (k % 3)
    k += 1
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(osfx.sound("oga/creatures/misc_03", blip(900)), 0.6, 0.35)
for c in [B["UGLY"], B["R1"], B["R2"], B["R3"], B["R4"], B["R5"], B["WHY"], B["QUEEN"], B["SCI"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
for i, st in enumerate(B["STAMPS"]):
    fx.put(osfx.sound("oga/100-sfx/slam_0" + str(1 + i % 7), impact(0.7)), st, 0.55)
    fx.put(osfx.lib("glitch-1"), st + 0.05, 0.25)
    fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(988 + 110 * i, 0.4)), st + 0.15, 0.2)
for k in range(12):
    fx.put(F.tick(2000 + 150 * k, 0.8), B["R1"] + 0.3 + k * 0.05, 0.2)
fx.put(F.sizzle(1.0, seed=3), B["R3"] + 0.3, 0.35)
for k in range(18):
    fx.put(F.tick(1500, 0.9), B["R4"] + 0.3 + k * 0.1, 0.18)
fx.put(riser(B["BREAK"] - B["R5"], 200, 1800), B["R5"], 0.25)
fx.put(impact(1.0), B["HIT"], 0.6)
fx.put(braam(1.5, 52), B["HIT"], 0.35)
fx.put(osfx.sound("oga/retro-synth/power_up_01", F.harp_up(523.25)), B["QUEEN"] + 0.3, 0.3)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(784, 1.2)), B["QUEEN"] + 0.9, 0.3)
fx.put(osfx.sound("oga/scifi/terminal_02", blip(1300)), B["SCI"] + 0.6, 0.3)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kbh")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)
master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
