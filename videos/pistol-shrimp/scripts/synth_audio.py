"""Sound for "A shrimp that snaps hotter than the Sun" (pistol shrimp): text cards + open-source sound only (NO narration).

SIGNATURE sound = the SNAP: a sharp crack (noise hit + shot + click). Frame 1 snaps; the slow-motion section stretches
it into a low whoosh + a bubble that swells (rising tone with the TEMP counter) until the 0.25 s break and the giant
POP; later a whole colony crackles (the snap rate rises from 5/s to 60/s like the WWII sonar noise). 8-bit bed under
everything, card blips, whooshes, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 28.4
B = dict(MEET=2.1, CLAW=4.2, SLOW=6.3, BUBBLE=8.4, BREAK=10.25, HIT=10.5, SUN=12.6, LIGHT=14.7, LOUD=16.8,
         STUN=18.9, WAR=21.0, HIDE=23.1, CTA=25.2, STOP=27.1, REWIND=27.9)

CARDS = [
    (0.10, 2.00, "THIS SHRIMP JUST|HIT *4,700°C*"),
    (2.10, 4.10, "THE *PISTOL*|SHRIMP"),
    (4.20, 6.20, "ITS CLAW: UP TO|*HALF* ITS SIZE"),
    (6.30, 8.30, "IT SNAPS SHUT|SO *FAST*..."),
    (8.40, 10.20, "...IT MAKES A|*BUBBLE*"),
    (10.50, 12.50, "IT POPS AT|*4,700°C*"),
    (12.60, 14.60, "ALMOST AS HOT|AS THE *SUN*"),
    (14.70, 16.70, "IT EVEN MAKES|A *FLASH*"),
    (16.80, 18.80, "ONE OF THE|*LOUDEST* ANIMALS"),
    (18.90, 20.90, "THE BANG|*STUNS* PREY"),
    (21.00, 23.00, "WWII: SHRIMP|*JAMMED* SONAR"),
    (23.10, 25.10, "SUBS *HID*|IN THE NOISE"),
    (25.20, 27.00, "TAG YOUR|*LOUDEST* FRIEND"),
]
# the colony crackle (WAR..CTA): snap times, rate 5/s -> 60/s
CR, t = [], B["WAR"] + 0.1
while t < B["CTA"] - 0.1:
    CR.append(round(t, 4))
    u = (t - B["WAR"]) / (B["CTA"] - B["WAR"])
    t += 1 / (5 + 55 * u ** 1.4)
B["COLONY"] = CR
B["SNAPS"] = [0.35, B["MEET"] + 1.2, B["HIT"], B["LIGHT"] + 0.3, B["LOUD"] + 0.3, B["STUN"] + 0.3, B["CTA"] + 0.6]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["MEET"], 100, 100, "kbo"),
    S(B["MEET"], B["SLOW"], 118, 118, "kbha"),
    S(B["SLOW"], B["BREAK"], 72, 72, "kbo"),
    S(B["HIT"] + 0.2, B["WAR"], 124, 124, "kbhal"),
    S(B["WAR"], B["CTA"], 126, 150, "kbhsa"),
    S(B["CTA"], B["STOP"] + 0.2, 128, 128, "kbhsal"),
], gain=0.46, crescendo=(0.8, 1.2))
amb.x += (0.15 * F.drone(DUR, 52, seed=2))[:, None]
for k in range(int(DUR / 1.6)):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.5, 600)), 0.4 + k * 1.6, 0.1, (k % 3 - 1) * 0.6)


def snap(t, g=1.0):
    fx.put(noise_hit(0.06, 2000, 12000), t, 0.9 * g)
    fx.put(osfx.sound("oga/bangs-fireworks/shot_01", impact(0.4)), t, 0.5 * g)
    fx.put(F.tick(5200, 1.0), t, 0.5 * g)
    fx.put(thump(90, 0.12, 2.5), t, 0.4 * g)


for st in B["SNAPS"]:
    snap(st, 1.4 if st == B["HIT"] else 0.9)
# 0. frame 1: stunned fish
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(osfx.sound("oga/creatures/hurt_03", sweep(0.3, 900, 400)), 0.7, 0.35, 0.4)
fx.put(F.sparkle(0.8, seed=3), 0.8, 0.2)
# 1. meet
fx.put(osfx.lib("whoosh"), B["MEET"] - 0.15, 0.45)
fx.put(osfx.sound("oga/creatures/bug_02", blip(1500)), B["MEET"] + 0.5, 0.35)
# 2. claw: measuring ticks
fx.put(osfx.lib("whoosh"), B["CLAW"] - 0.15, 0.4)
for k in range(10):
    fx.put(F.tick(3000 + 80 * k, 0.8), B["CLAW"] + 0.4 + k * 0.09, 0.22)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["CLAW"] + 1.4, 0.3)
# 3. slow motion: everything drops, the claw closes with a long low whoosh
fx.put(osfx.lib("whoosh-cinematic"), B["SLOW"] - 0.2, 0.5)
fx.put(CT.tone_glide(400, 90, 1.8, "square", 0.5, 0.5), B["SLOW"] + 0.2, 0.15)
fx.put(sweep(1.6, 200, 60) * 0.6, B["SLOW"] + 0.3, 0.3)
# 4. the bubble grows: rising tone + bubbling, then BREAK -> POP
fx.put(riser(B["BREAK"] - B["BUBBLE"], 120, 2200), B["BUBBLE"], 0.35)
fx.put(osfx.sound("oga/water-splash/loop_bubbles_02", F.boil(1.8)), B["BUBBLE"], 0.3)
for k in range(12):
    fx.put(F.tick(1200 + 150 * k, 0.8), B["BUBBLE"] + 0.15 * k, 0.2)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(braam(1.4, 55), B["HIT"], 0.4)
fx.put(sub_drop(1.0), B["HIT"], 0.5)
# 5-6. sun compare
fx.put(osfx.lib("whoosh"), B["SUN"] - 0.15, 0.45)
fx.put(F.fire(1.4, seed=2), B["SUN"] + 0.3, 0.3)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["SUN"] + 1.0, 0.25)
# 7. flash
fx.put(osfx.lib("whoosh"), B["LIGHT"] - 0.15, 0.4)
fx.put(F.sparkle(1.0, seed=6), B["LIGHT"] + 0.35, 0.35)
# 8. loud: dB meter ticks
fx.put(osfx.lib("whoosh"), B["LOUD"] - 0.15, 0.4)
for k in range(8):
    fx.put(CT.square(440 + 110 * k, 0.05, 0.5), B["LOUD"] + 0.4 + k * 0.08, 0.1)
# 9. stun: dizzy
fx.put(osfx.lib("whoosh"), B["STUN"] - 0.15, 0.4)
fx.put(osfx.sound("oga/creatures/weird_02", CT.tone_glide(900, 500, 0.6, "square", 0.5, 0.5)), B["STUN"] + 0.6, 0.35)
fx.put(osfx.sound("oga/creatures/eat_01", thump(300, 0.08, 1.5)), B["STUN"] + 1.4, 0.4)
# 10. SIGNATURE colony crackle (WWII sonar)
fx.put(osfx.lib("whoosh-cinematic"), B["WAR"] - 0.2, 0.45)
fx.put(CT.ping(1200, 1.0), B["WAR"] + 0.2, 0.2)
for k, ct in enumerate(CR):
    fx.put(noise_hit(0.025, 2500, 12000), ct, 0.35 + 0.2 * (k % 3) / 2, (hash(k) % 7 - 3) / 4)
fx.put(osfx.lib("whoosh"), B["HIDE"] - 0.15, 0.4)
fx.put(CT.ping(900, 1.2), B["HIDE"] + 0.6, 0.15)
# 11. CTA
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kbo")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(CR), "colony snaps; DUR", DUR)
