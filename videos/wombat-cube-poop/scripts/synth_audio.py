"""Sound for "The animal that poops cubes": open-source sound effects only (no narration, owner's request), loud.

  python3 scripts/synth_audio.py

Layers from OPEN-SOURCE sources (osfx.py): CC0 OpenGameArt recordings (plops, slime, stones, creature grunts/sniffs,
cute squeaks), jsfxr, the bundled HyperFrames library, and the numpy kits (sfxlib, foley). Everything used is frozen
into assets/sfx/. Writes assets/audio/mix.wav + captions.js (text cards + the beats the picture shares).
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 22.0
B = dict(DROP=0.35, GLITCH=1.55, MEET=1.8, COUNT=3.8, GUT=5.6, SQUEEZE=9.0, OUT=12.2, ROLL=15.4, BALL=15.9, SNIFF=17.4, NOBEL=19.4)

CARDS = [
    (0.10, 1.55, "THIS ANIMAL|POOPS *CUBES*"),
    (2.00, 3.65, "MEET THE *WOMBAT*"),
    (3.80, 5.45, "UP TO *100 CUBES*|EVERY NIGHT"),
    (5.80, 8.85, "ITS GUT HAS *STIFF*|AND *STRETCHY* PATCHES"),
    (9.00, 12.00, "THEY SQUEEZE THE POOP|INTO *CORNERS*"),
    (12.40, 15.20, "OUT COME *2 CM* CUBES.|LIKE DICE!"),
    (15.60, 17.30, "CUBES DON'T *ROLL AWAY*"),
    (17.45, 19.20, "PERFECT FOR MARKING|*TERRITORY*"),
    (19.60, 21.85, "IT WON AN *IG NOBEL*|PRIZE IN 2019"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
night = seg(0, B["GUT"], 0.2) + seg(B["ROLL"], B["NOBEL"], 0.3) + seg(DUR - 0.5, DUR, 0.1)
amb.x += (0.5 * F.crickets(DUR, seed=6) * night)[:, None]

# ---------------------------------------------------------------- 0. hook: a falling whistle, then a big THUNK on the rock
fx.put(sweep(0.3, 1800, 500), B["DROP"] - 0.05, 0.4)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_wood_hit_01", thump(200, 0.15, 2.0)), B["DROP"] + 0.25, 1.0)
fx.put(impact(1.0), B["DROP"] + 0.25, 0.8)
fx.put(osfx.sound("oga/100-sfx/slam_05", impact(0.8)), B["DROP"] + 0.25, 0.7)
fx.put(osfx.sound("oga/100-sfx/plop_01", F.splash(0.3)), B["DROP"] + 0.3, 0.6)
fx.put(rewind(0.4), B["GLITCH"] - 0.05, 0.7)
fx.put(osfx.lib("glitch-1"), B["GLITCH"], 0.5)

# ---------------------------------------------------------------- 1. the wombat waddles in, then cubes pop out (counter)
for k in range(6):
    fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_footstep_01", thump(160, 0.06, 1.0)), B["MEET"] + 0.1 + k * 0.23, 0.6, -0.6 + k * 0.15)
fx.put(osfx.sound("oga/creatures/grunt_02", F.chatter(0.4)), B["MEET"] + 1.5, 0.8)
n = 14
for k in range(n):
    tk = B["COUNT"] + (B["GUT"] - 0.2 - B["COUNT"]) * k / n
    fx.put(osfx.sound(f"oga/100-sfx/plop_0{k % 2 + 1}", F.splash(0.2, k)), tk, 0.7, -0.4)
    fx.put(osfx.sfxr("blipSelect", seed=30 + k % 3), tk, 0.25)
fx.put(osfx.sfxr("pickupCoin", seed=3), B["GUT"] - 0.25, 0.45)

# ---------------------------------------------------------------- 2. x-ray: gut gurgles, squelches, the squeeze
fx.put(osfx.lib("whoosh-cinematic"), B["GUT"] - 0.25, 0.8)
gut = seg(B["GUT"], B["OUT"], 0.3)
amb.x += (0.55 * band(F.boil(DUR, rate=7, seed=4), 60, 1800) * gut)[:, None]
for k in range(6):
    fx.put(osfx.sound(f"oga/water-splash/slime_0{k % 9 + 1}", F.splash(0.4, k)), B["GUT"] + 0.5 + k * 0.55, 0.6, (k % 3 - 1) * 0.5)
for k in range(4):
    tk = B["SQUEEZE"] + k * 0.7
    fx.put(taiko(70), tk, 0.8)
    fx.put(osfx.sound(f"oga/water-splash/slime_1{k % 6}", F.splash(0.5, 9 + k)), tk + 0.05, 0.8)
fx.put(osfx.sound("oga/100-sfx/spring_03", sweep(0.3, 800, 300)), B["OUT"] - 0.4, 0.7)
fx.put(osfx.sfxr("powerUp", seed=9), B["OUT"] - 0.4, 0.4)

# ---------------------------------------------------------------- 3. the cube lands next to a die, ruler snaps on
fx.put(osfx.lib("whoosh"), B["OUT"] - 0.2, 0.6)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_wood_hit_02", thump(220, 0.12, 2.0)), B["OUT"] + 0.4, 1.0)
fx.put(impact(0.8), B["OUT"] + 0.4, 0.6)
fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(2000, 1.0)), B["OUT"] + 0.8, 0.7)
fx.put(osfx.sound("oga/creatures/cute_02", F.chatter(0.4)), B["OUT"] + 1.6, 0.6, -0.5)

# ---------------------------------------------------------------- 4. the round one rolls away (bounces), cubes stay; a sniff
fx.put(osfx.lib("whoosh"), B["ROLL"] - 0.2, 0.6)
fx.put(sweep(0.9, 900, 250), B["BALL"], 0.5, 0.5)
for k in range(3):
    fx.put(osfx.sound("oga/100-sfx/spring_05", thump(260, 0.08, 1.0)), B["BALL"] + 0.9 + k * 0.28, 0.7 - k * 0.15, 0.7)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", tone(200, 0.3)), B["BALL"] + 0.95, 0.5)
fx.put(osfx.sound("oga/creatures/nose", noise_hit(0.3, 500, 4000)), B["SNIFF"] + 1.0, 0.8, 0.6)
fx.put(osfx.sound("oga/creatures/nose", noise_hit(0.3, 500, 4000)), B["SNIFF"] + 1.4, 0.7, 0.6)
fx.put(osfx.sound("oga/creatures/grunt_04", F.chatter(0.4)), B["SNIFF"] + 1.2, 0.6, -0.5)

# ---------------------------------------------------------------- 5. Ig Nobel: fanfare, crowd pops, confetti
fx.put(osfx.lib("whoosh-cinematic"), B["NOBEL"] - 0.25, 0.8)
fx.put(impact(1.0), B["NOBEL"] + 0.3, 0.7)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["NOBEL"] + 0.3, 0.6)
chord = [523.25, 659.25, 783.99, 1046.5]
for i, f0 in enumerate(chord):
    fx.put(bell(f0, 1.6), B["NOBEL"] + 0.35 + i * 0.08, 0.3)
for k in range(5):
    fx.put(osfx.sound(f"oga/bangs-fireworks/fw_0{k % 6 + 1}", F.firework(71 + k)), B["NOBEL"] + 0.4 + k * 0.3, 0.45, (k % 3 - 1) * 0.6)
fx.put(osfx.lib("whoosh-cinematic"), DUR - 0.6, 0.7)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=0.6, makeup_db=10.0)

caps = [{"a": a, "b": b, "segs": [V.segs(ln) for ln in text.split("|")]} for a, b, text in CARDS]
with open(os.path.join(ROOT, "captions.js"), "w") as f:
    f.write("// generated by scripts/synth_audio.py: text cards + shared beats (no narration)\n")
    f.write(f"window.DUR = {DUR};\n")
    f.write("window.CAPS = " + json.dumps(caps) + ";\n")
    f.write("window.VO = [];\nwindow.MOUTH = {};\n")
    f.write("window.BEATS = " + json.dumps(B) + ";\n")
print("DUR", DUR)
