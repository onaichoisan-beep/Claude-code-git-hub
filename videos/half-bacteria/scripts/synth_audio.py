"""Sound for "Half of you isn't you": open-source sound effects only (no narration, owner's request), loud.

  python3 scripts/synth_audio.py

Layers from OPEN-SOURCE sources (osfx.py): CC0 OpenGameArt recordings (creatures, water/slime, impacts, retro synth),
jsfxr 8-bit effects, the bundled HyperFrames library, and the numpy kits (sfxlib, foley). Everything used is frozen
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
B = dict(GLITCH=1.55, COUNT=1.8, HUMAN=2.1, BACT=4.8, GUT=7.6, FOOD=11.4, VIT=13.6, IMMUNE=15.6,
         SCALE=17.9, BALANCE=18.9, BACK=20.4)

CARDS = [
    (0.10, 1.55, "HALF OF *YOU*|ISN'T EVEN YOU"),
    (2.00, 4.65, "YOU HAVE *30 TRILLION*|HUMAN CELLS"),
    (4.80, 7.45, "AND *38 TRILLION*|BACTERIA!"),
    (7.80, 11.20, "MOST OF THEM LIVE|IN YOUR *GUT*"),
    (11.50, 13.45, "THEY DIGEST FOOD|*YOU* CAN'T"),
    (13.65, 15.45, "THEY MAKE|*VITAMINS*"),
    (15.65, 17.75, "THEY TRAIN YOUR|*IMMUNE SYSTEM*"),
    (18.05, 20.25, "ALL OF THEM WEIGH|ABOUT *0.2 KG*"),
    (20.55, 21.85, "SO WHO'S REALLY|IN *CHARGE*?"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()

# ---------------------------------------------------------------- 0. hook: slam + braam, the body squelches into bacteria
fx.put(osfx.sound("oga/100-sfx/slam_02", impact(1.0)), 0.0, 0.9)
fx.put(impact(1.0), 0.0, 0.7)
fx.put(braam(1.4, 55), 0.0, 0.6)
fx.put(osfx.sound("oga/water-splash/slime_03", F.splash(0.6, 3)), 0.15, 0.8)
fx.put(osfx.sound("oga/creatures/bug_01", F.chatter(0.8)), 0.3, 0.6, 0.5)
fx.put(osfx.sound("oga/creatures/bug_02", F.chatter(0.8)), 0.8, 0.5, -0.4)
fx.put(rewind(0.4), B["GLITCH"] - 0.05, 0.7)
fx.put(osfx.lib("glitch-1"), B["GLITCH"], 0.5)

# ---------------------------------------------------------------- 1. counting: cells stack with pops, then the bacteria tower wins
hu0, hu1 = B["HUMAN"], B["BACT"] - 0.5
for k in range(12):
    fx.put(osfx.lib("pop"), hu0 + (hu1 - hu0) * k / 12, 0.45, -0.5)
fx.put(osfx.sfxr("pickupCoin", seed=3), hu1, 0.4, -0.5)
fx.put(osfx.sound("oga/100-sfx/slam_03", impact(0.8)), B["BACT"], 0.8)
for k in range(16):
    fx.put(osfx.sfxr("blipSelect", seed=40 + k % 4), B["BACT"] + 2.0 * k / 16, 0.3, 0.5)
fx.put(riser(2.0, 300, 1400), B["BACT"], 0.45)
fx.put(osfx.sound("oga/100-sfx/gong_01", gong(110)), B["BACT"] + 2.0, 0.6)
fx.put(impact(1.0), B["BACT"] + 2.0, 0.7)
fx.put(osfx.sound("oga/creatures/cute_03", F.chatter(0.6)), B["BACT"] + 2.15, 0.6, 0.5)

# ---------------------------------------------------------------- 2. into the gut: a squishy dive, gurgles, the swarm chatters
fx.put(osfx.lib("whoosh-cinematic"), B["GUT"] - 0.25, 0.8)
fx.put(osfx.sound("oga/water-splash/splash_02", F.splash(1.0, 9)), B["GUT"], 0.8)
gut = seg(B["GUT"], B["SCALE"], 0.4)
amb.x += (0.6 * band(F.boil(DUR, rate=8, seed=3), 80, 2500) * gut)[:, None]
amb.x += (0.35 * F.rumble(DUR, 30, 160, seed=11) * gut)[:, None]
for k in range(6):
    fx.put(osfx.sound(f"oga/creatures/bug_0{k % 4 + 1}", F.chatter(0.6, seed=k)), B["GUT"] + 0.6 + k * 0.55, 0.4, (k % 3 - 1) * 0.6)
for k in range(4):
    fx.put(osfx.sound(f"oga/creatures/burble_0{k % 2 + 1}", F.boil(0.6)), B["GUT"] + 1.0 + k * 0.8, 0.5, (k % 2) * 1.2 - 0.6)
# chomp chomp
for k in range(8):
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(300, 0.08, 1.0)), B["FOOD"] + 0.3 + k * 0.24, 0.7, (k % 3 - 1) * 0.6)
fx.put(osfx.sound("oga/creatures/burp_01", sweep(0.4, 200, 90)), B["VIT"] - 0.35, 0.7)
# vitamins pop out
for p in range(6):
    fx.put(osfx.sfxr("pickupCoin", seed=60 + p), B["VIT"] + 0.15 + p * 0.22, 0.45, (p % 2) * 1.0 - 0.5)
fx.put(osfx.lib("sparkle"), B["VIT"] + 0.3, 0.4)
# the white blood cell rolls in, fist bump
fx.put(osfx.lib("whoosh"), B["IMMUNE"] - 0.3, 0.7, 0.6)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["IMMUNE"] + 0.2, 0.5)
fx.put(osfx.sound("oga/100-sfx/hit_02", thump(200, 0.1, 1.5)), B["IMMUNE"] + 1.0, 0.9)
fx.put(impact(0.7), B["IMMUNE"] + 1.0, 0.6)
fx.put(osfx.sfxr("powerUp", seed=5), B["IMMUNE"] + 1.05, 0.4)
fx.put(osfx.sound("oga/creatures/cute_05", F.chatter(0.5)), B["IMMUNE"] + 1.2, 0.5)

# ---------------------------------------------------------------- 3. the scale wobbles, then balances: one apple
fx.put(osfx.lib("whoosh"), B["SCALE"] - 0.2, 0.7)
fx.put(osfx.sound("oga/100-sfx/metal_03", F.creak(0.8)), B["SCALE"] + 0.1, 0.6)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_metal_hit_01", thump(180, 0.2, 1.5)), B["BALANCE"], 0.9)
fx.put(add(bell(1046.5, 1.5), 0.5 * bell(1568, 1.5)), B["BALANCE"] + 0.05, 0.4)
fx.put(taiko(70), B["BALANCE"], 0.7)

# ---------------------------------------------------------------- 4. back to the split body: chatter, whoosh into the loop
fx.put(osfx.lib("whoosh-cinematic"), B["BACK"] - 0.25, 0.8)
fx.put(braam(1.4, 55), B["BACK"], 0.4)
fx.put(osfx.sound("oga/creatures/cute_07", F.chatter(0.6)), B["BACK"] + 0.4, 0.6, 0.5)
fx.put(osfx.sound("oga/creatures/bug_03", F.chatter(0.6)), B["BACK"] + 0.9, 0.5, -0.4)
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
