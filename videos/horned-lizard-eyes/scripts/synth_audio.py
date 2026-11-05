"""Sound for "The lizard that cries blood" (Texas horned lizard): text cards + open-source sound only (NO narration).

SIGNATURE sound = the PRESSURE PUMP: a heartbeat thump that speeds up (1.2/s -> 9/s) and rises in pitch with the
PRESSURE % counter, until the 0.25 s break and the SQUIRT (a hiss-spray + splat). 8-bit bed under everything, desert
wind, a blip on every card, whoosh + hit on every cut, coyote sniffs/gags, a hawk screech, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 27.9
B = dict(MEET=2.1, COYOTE=4.1, PUFF=6.1, FAIL=8.1, PRESS=10.1, BREAK=12.6, HIT=12.85, RANGE=14.7, TASTE=16.7,
         FLEE=18.7, HAWK=20.7, HIDE=22.7, CTA=24.7, STOP=26.6, REWIND=27.4)

CARDS = [
    (0.10, 2.00, "THIS LIZARD|CRIES *BLOOD*"),
    (2.10, 4.00, "THE TEXAS|*HORNED LIZARD*"),
    (4.10, 6.00, "A COYOTE|WANTS *LUNCH*"),
    (6.10, 8.00, "PLAN A:|*PUFF UP*"),
    (8.10, 10.00, "IT DOESN'T|*WORK*"),
    (10.10, 12.50, "PLAN B: BLOOD|PRESSURE *RISES*"),
    (12.85, 14.60, "IT SHOOTS BLOOD|FROM ITS *EYES*"),
    (14.70, 16.60, "UP TO *1.5 M*|AWAY"),
    (16.70, 18.60, "IT TASTES *AWFUL*|TO DOGS"),
    (18.70, 20.60, "THE COYOTE|*RUNS*"),
    (20.70, 22.60, "BUT HAWKS?|*DON'T CARE*"),
    (22.70, 24.60, "SO IT *HIDES*|INSTEAD"),
    (24.70, 26.50, "TAG A FRIEND|WHO *CRIES* A LOT"),
]
PUMPS, t = [], B["PRESS"] + 0.1
while t < B["BREAK"] - 0.05:
    PUMPS.append(round(t, 3))
    u = (t - B["PRESS"]) / (B["BREAK"] - B["PRESS"])
    t += 1 / (1.2 + 7.8 * u ** 1.5)
B["PUMPS"] = PUMPS

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
    S(B["MEET"], B["PUFF"], 116, 116, "kbh"),
    S(B["PUFF"], B["PRESS"], 120, 120, "kbha"),
    S(B["PRESS"], B["BREAK"], 120, 156, "kbhsa"),
    S(B["HIT"] + 0.1, B["HAWK"], 126, 126, "kbhal"),
    S(B["HAWK"], B["CTA"], 110, 110, "kbhs"),
    S(B["CTA"], B["STOP"] + 0.2, 128, 128, "kbhsal"),
], gain=0.48, crescendo=(0.8, 1.2))
amb.x += (0.3 * F.wind(DUR, 300, 800, 0.4, seed=11))[:, None]


def squirt(t, g=1.0):
    fx.put(noise_hit(0.45, 1500, 6000), t, 0.45 * g)
    fx.put(sweep(0.35, 2400, 900) * 0.6, t, 0.25 * g)
    fx.put(osfx.sound("oga/creatures/spit_01", F.splash(0.4, 2)), t + 0.02, 0.6 * g)
    fx.put(osfx.sound("oga/water-splash/slime_07", F.splash(0.3, 4)), t + 0.35, 0.45 * g, -0.4)


# 0. frame 1: the squirt
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
squirt(0.2)
fx.put(osfx.sound("oga/creatures/hurt_02", sweep(0.3, 700, 300)), 0.75, 0.4, -0.4)
# 1. meet
fx.put(osfx.lib("whoosh"), B["MEET"] - 0.15, 0.45)
for k in range(5):
    fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_footstep_0" + str(1 + k % 2), F.tick(900, 0.6)), B["MEET"] + 0.3 + k * 0.3, 0.25)
fx.put(osfx.sound("oga/creatures/cute_04", blip(1200)), B["MEET"] + 1.0, 0.35)
# 2. coyote sniffs
fx.put(osfx.lib("whoosh"), B["COYOTE"] - 0.15, 0.45)
for k in range(4):
    fx.put(osfx.sound("oga/creatures/nose", noise_hit(0.15, 800, 3000)), B["COYOTE"] + 0.5 + k * 0.3, 0.45, 0.4)
fx.put(osfx.sound("oga/creatures/grunt_01", roar(0.4, 140)), B["COYOTE"] + 1.5, 0.4)
# 3. puff up: inflating squeak
fx.put(osfx.lib("whoosh"), B["PUFF"] - 0.15, 0.4)
fx.put(CT.tone_glide(200, 900, 0.9, "square", 0.3, 0.6), B["PUFF"] + 0.2, 0.18)
fx.put(osfx.sound("oga/100-sfx/spring_03", blip(600)), B["PUFF"] + 1.1, 0.4)
# 4. fail
fx.put(osfx.sound("oga/retro-synth/retro_die_02", CT.womp(330, 4, 0.22)), B["FAIL"] + 0.3, 0.35)
fx.put(osfx.sound("oga/creatures/barking_01", roar(0.4, 160)), B["FAIL"] + 1.0, 0.4)
# 5. SIGNATURE: pressure pump speeds up
fx.put(osfx.lib("whoosh"), B["PRESS"] - 0.15, 0.4)
fx.put(riser(B["BREAK"] - B["PRESS"], 120, 1500), B["PRESS"], 0.3)
for k, pt in enumerate(PUMPS):
    f = 55 + 2.5 * k
    fx.put(thump(f, 0.18, 2.0), pt, 0.75)
    fx.put(thump(f * 1.3, 0.12, 2.0), pt + 0.11 * (1 - k / len(PUMPS)) + 0.03, 0.45)
    fx.put(F.tick(1500 + 50 * k, 0.8), pt, 0.18)
# 6. HIT: the squirt
fx.put(impact(0.8), B["HIT"], 0.6)
squirt(B["HIT"], 1.2)
fx.put(osfx.sound("oga/creatures/hurt_04", sweep(0.4, 800, 300)), B["HIT"] + 0.5, 0.5, -0.4)
# 7. range ruler ticks
fx.put(osfx.lib("whoosh"), B["RANGE"] - 0.15, 0.45)
for k in range(15):
    fx.put(F.tick(3000 + 60 * k, 0.8), B["RANGE"] + 0.3 + k * 0.07, 0.22)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["RANGE"] + 1.4, 0.3)
# 8. taste: gag + cough
fx.put(osfx.lib("whoosh"), B["TASTE"] - 0.15, 0.4)
fx.put(osfx.sound("oga/creatures/cough_02", thump(140, 0.2, 1.5)), B["TASTE"] + 0.4, 0.5)
fx.put(osfx.sound("oga/creatures/spit_03", noise_hit(0.2, 600, 3000)), B["TASTE"] + 1.1, 0.5)
# 9. flee
fx.put(osfx.lib("whoosh-cinematic"), B["FLEE"] + 0.1, 0.5)
fx.put(osfx.sound("oga/creatures/howl", sweep(0.8, 700, 400)), B["FLEE"] + 0.3, 0.35)
for k in range(8):
    fx.put(F.tick(800, 0.7), B["FLEE"] + 0.2 + k * 0.12, 0.25, 0.5)
fx.put(osfx.sfxr("pickupCoin", seed=6), B["FLEE"] + 1.2, 0.3)
# 10. hawk
fx.put(osfx.lib("whoosh-cinematic"), B["HAWK"] + 0.2, 0.6)
fx.put(F.squawk(seed=3), B["HAWK"] + 0.5, 0.5)
fx.put(osfx.sound("oga/creatures/scream_01", sweep(0.5, 2200, 1400)), B["HAWK"] + 0.55, 0.3)
# 11. hide: flatten + blend in
fx.put(osfx.lib("whoosh"), B["HIDE"] - 0.15, 0.4)
fx.put(CT.tone_glide(900, 200, 0.6, "square", 0.3, 0.6), B["HIDE"] + 0.2, 0.16)
fx.put(F.sparkle(0.8, seed=2), B["HIDE"] + 0.6, 0.25)
fx.put(F.squawk(seed=9), B["HIDE"] + 1.3, 0.35)
# 12. CTA
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
squirt(B["CTA"] + 0.8, 0.7)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kbo")], gain=0.48, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(PUMPS), "pumps; DUR", DUR)
