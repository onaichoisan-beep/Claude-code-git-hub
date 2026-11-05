"""Sound for "The jellyfish that ages backwards" (Turritopsis dohrnii): text cards + open-source sound only (NO narration).

SIGNATURE sound = the RESTART: a tape-rewind zip + a reversed clock tick every time the jellyfish turns back into a baby.
In the RESTART section the restarts speed up (1/s -> 6/s) with the LIFE # counter, until the 0.25 s break and the
"IMMORTAL" hit. 8-bit bed under everything, a blip on every card, whoosh + hit on every cut, the fish's CHOMP,
tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 28.2
B = dict(SHRINK=2.3, POLYP=4.5, GROW=6.7, TINY=8.9, STRESS=11.0, AGAIN=13.1, BREAK=16.85, HIT=17.1, WORLD=19.3,
         FISH=21.5, CHOMP=22.7, CTA=24.6, STOP=26.8, REWIND=27.6)

CARDS = [
    (0.10, 2.20, "THIS JELLYFISH|IS *DYING*..."),
    (2.30, 4.40, "SO IT TURNS|BACK INTO A *BABY*"),
    (4.50, 6.60, "IT BECOMES A|*POLYP* AGAIN"),
    (6.70, 8.80, "THEN GROWS UP|*ALL OVER AGAIN*"),
    (8.90, 10.90, "ONLY *4.5 MM*|WIDE"),
    (11.00, 13.00, "HURT? HUNGRY?|*OLD*?"),
    (13.10, 16.70, "IT JUST HITS|*RESTART*"),
    (17.10, 19.20, "*BIOLOGICALLY*|IMMORTAL"),
    (19.30, 21.40, "NOW IN OCEANS|*WORLDWIDE*"),
    (21.50, 24.50, "IMMORTAL...|UNTIL *LUNCH*"),
    (24.60, 26.70, "WOULD YOU HIT|*RESTART*?"),
]
# accelerating restarts (shared with the picture: each one = LIFE +1)
R, t = [], B["AGAIN"] + 0.3
while t < B["BREAK"] - 0.1:
    R.append(round(t, 3))
    u = (t - B["AGAIN"]) / (B["BREAK"] - B["AGAIN"])
    t += 1 / (1.0 + 5.0 * u ** 1.6)
B["RESTARTS"] = R
B["STRESSES"] = [B["STRESS"] + 0.3, B["STRESS"] + 0.9, B["STRESS"] + 1.5]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["SHRINK"], 92, 92, "kbo"),
    S(B["SHRINK"], B["TINY"], 112, 116, "kbh"),
    S(B["TINY"], B["AGAIN"], 118, 120, "kbha"),
    S(B["AGAIN"], B["BREAK"], 120, 152, "kbhsa"),
    S(B["HIT"] + 0.1, B["FISH"], 124, 124, "kbhal"),
    S(B["FISH"], B["CHOMP"], 100, 100, "kbo"),
    S(B["CHOMP"] + 0.3, B["STOP"] + 0.2, 126, 126, "kbhsal"),
], gain=0.48, crescendo=(0.8, 1.2))
amb.x += (0.16 * F.drone(DUR, 52, seed=4))[:, None]
for k in range(int(DUR / 1.5)):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.5, 600)), 0.5 + k * 1.5, 0.12, (k % 3 - 1) * 0.6)


def restart(t, g=1.0, short=False):
    """the signature: rewind zip + reversed tick-tock"""
    fx.put(rewind(0.25 if short else 0.45), t, 0.45 * g)
    fx.put(F.tick(3600, 1.0), t + 0.02, 0.3 * g, 0.3)
    fx.put(F.tick(2400, 0.8), t + (0.08 if short else 0.16), 0.25 * g, -0.3)


# 0. frame 1: the old jelly creaks
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(osfx.sound("oga/creatures/grunt_02", sweep(0.3, 300, 200)), 0.7, 0.35)
for k in range(4):
    fx.put(F.creak(0.25, 140 + 20 * k, seed=k), 0.4 + k * 0.45, 0.18)
# 1. shrinks back
fx.put(osfx.lib("whoosh"), B["SHRINK"] - 0.15, 0.45)
restart(B["SHRINK"] + 0.1)
fx.put(CT.tone_glide(900, 200, 1.6, "square", 0.25, 0.4), B["SHRINK"] + 0.2, 0.12)
fx.put(osfx.sound("oga/water-splash/slime_04", thump(150, 0.1, 2)), B["SHRINK"] + 1.8, 0.5)
# 2. polyp
fx.put(osfx.lib("whoosh"), B["POLYP"] - 0.15, 0.4)
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up()), B["POLYP"] + 0.3, 0.35)
fx.put(osfx.sound("oga/creatures/cute_03", blip(1200)), B["POLYP"] + 0.9, 0.4)
# 3. buds baby jellies that grow
fx.put(osfx.lib("whoosh"), B["GROW"] - 0.15, 0.4)
for k in range(4):
    fx.put(osfx.sound("oga/100-sfx/plop_0" + str(1 + k % 2), blip(900 + 200 * k)), B["GROW"] + 0.2 + k * 0.35, 0.35, (k % 2) - 0.5)
fx.put(osfx.sfxr("powerUp", seed=3), B["GROW"] + 1.6, 0.3)
# 4. tiny: ruler ticks
fx.put(osfx.lib("whoosh-cinematic"), B["TINY"] - 0.2, 0.5)
fx.put(impact(0.5), B["TINY"], 0.3)
for k in range(6):
    fx.put(F.tick(4000, 0.8), B["TINY"] + 0.5 + k * 0.12, 0.25)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["TINY"] + 1.3, 0.25)
# 5. stresses: zap, rumble, creak
fx.put(osfx.lib("whoosh"), B["STRESS"] - 0.15, 0.4)
fx.put(osfx.sound("oga/retro-synth/synth_laser_03", sweep(0.2, 2000, 400)), B["STRESSES"][0], 0.4)
fx.put(osfx.sound("oga/creatures/burble_01", thump(90, 0.3, 1.5)), B["STRESSES"][1], 0.45)
fx.put(osfx.sound("oga/creatures/grunt_03", sweep(0.3, 300, 200)), B["STRESSES"][2], 0.4)
# 6. SIGNATURE: the restarts speed up with LIFE #
fx.put(riser(B["BREAK"] - B["AGAIN"], 150, 1800), B["AGAIN"], 0.3)
for k, rt in enumerate(R):
    restart(rt, 0.7 + 0.3 * k / len(R), short=k > 4)
    fx.put(F.tick(1800 + 60 * k, 1.0), rt + 0.03, 0.25)
# 7. HIT: immortal
fx.put(impact(0.9), B["HIT"], 0.8)
fx.put(braam(1.6, 55), B["HIT"], 0.4)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(880, 1.5)), B["HIT"] + 0.1, 0.4)
fx.put(F.sparkle(1.2, seed=5), B["HIT"] + 0.2, 0.3)
# 8. worldwide: pops on the globe
fx.put(osfx.lib("whoosh"), B["WORLD"] - 0.15, 0.45)
for k in range(9):
    fx.put(osfx.sound("oga/100-sfx/plop_0" + str(1 + k % 2), blip(1000 + 90 * k)), B["WORLD"] + 0.3 + k * 0.17, 0.3, (k % 3 - 1) * 0.5)
# 9. the fish: swim in, CHOMP, burp
fx.put(osfx.lib("whoosh"), B["FISH"] - 0.15, 0.45)
fx.put(osfx.sound("oga/creatures/cute_06", blip(1300)), B["FISH"] + 0.3, 0.35)
fx.put(osfx.sound("oga/water-splash/splash_06", F.splash(0.5, 3)), B["CHOMP"] - 0.3, 0.4)
fx.put(osfx.sound("oga/creatures/eat_02", thump(200, 0.1, 2)), B["CHOMP"], 0.9)
fx.put(impact(0.7), B["CHOMP"], 0.6)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(330, 3, 0.2)), B["CHOMP"] + 0.4, 0.35)
fx.put(osfx.sound("oga/creatures/burp_01", thump(120, 0.2, 1.5)), B["CHOMP"] + 1.1, 0.45)
# 10. CTA
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.3)
restart(B["CTA"] + 1.0, 0.6)
# tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 92, 92, "kbo")], gain=0.48, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(R), "restarts; DUR", DUR)
