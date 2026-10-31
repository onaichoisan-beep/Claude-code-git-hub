"""Sound for "You glow in the dark": open-source sound effects only (no narration, owner's request), loud.

  python3 scripts/synth_audio.py

Layers from OPEN-SOURCE sources (osfx.py): CC0 OpenGameArt recordings (sci-fi, impacts, switches), jsfxr 8-bit
effects, the bundled HyperFrames library, and the numpy kits (sfxlib, foley). Everything used is frozen into
assets/sfx/. Writes assets/audio/mix.wav + captions.js (text cards + the beats the picture shares).
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 21.0
B = dict(GLITCH=1.55, CELL=1.8, BURN=4.2, LAB=6.4, SNAP=7.2, EYE=10.6, FACE=13.8, CLOCK=16.4, BACK=19.4, OFF=20.0)

CARDS = [
    (0.10, 1.55, "YOU ARE *GLOWING*|RIGHT NOW"),
    (2.00, 4.10, "YOUR CELLS GIVE OFF|REAL *LIGHT*"),
    (4.20, 6.30, "A SIDE EFFECT OF|BURNING *ENERGY*"),
    (6.60, 8.50, "SCIENTISTS IN JAPAN|*FILMED* IT IN 2009"),
    (8.60, 10.45, "IN TOTAL DARKNESS, WITH|SUPER-SENSITIVE *CAMERAS*"),
    (10.80, 13.65, "BUT IT'S *1,000X* TOO|FAINT FOR YOUR EYES"),
    (14.00, 16.25, "IT'S BRIGHTEST|ON YOUR *FACE*"),
    (16.60, 19.25, "DIMMEST AT 10 AM,|BRIGHTEST AT *4 PM*"),
    (19.55, 20.85, "LIGHTS OFF... YOU'RE|STILL *GLOWING*"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()

# ---------------------------------------------------------------- 0. hook: a deep hit in the dark, an eerie shimmer
fx.put(osfx.sound("oga/100-sfx/slam_04", impact(1.0)), 0.0, 0.9)
fx.put(impact(1.0), 0.0, 0.7)
fx.put(sub_drop(1.2), 0.0, 0.8)
fx.put(osfx.sound("oga/scifi/teleport_01", F.sparkle(1.2)), 0.05, 0.6)
fx.put(F.sparkle(1.4, seed=9), 0.2, 0.5)
amb.x += (0.35 * F.drone(DUR, 55, seed=3) * (seg(0, B["CELL"], 0.2) + seg(B["OFF"] - 0.05, DUR, 0.1)))[:, None]
fx.put(rewind(0.4), B["GLITCH"] - 0.05, 0.7)
fx.put(osfx.lib("glitch-2"), B["GLITCH"], 0.5)

# ---------------------------------------------------------------- 1. inside the cell: bubbling, then the mitochondria fire up
fx.put(osfx.lib("whoosh-cinematic"), B["CELL"] - 0.1, 0.7)
amb.x += (0.45 * band(F.boil(DUR, rate=10, seed=5), 80, 2000) * seg(B["CELL"], B["LAB"], 0.3))[:, None]
fx.put(osfx.sound("oga/scifi/loop_machine_01", F.gears(2.0)), B["BURN"] - 0.3, 0.5)
fx.put(braam(1.6, 62), B["BURN"], 0.7)
fx.put(F.fire(2.0, 41), B["BURN"], 0.6)
for k in range(10):
    fx.put(osfx.sfxr("pickupCoin", seed=80 + k % 5), B["BURN"] + 0.1 + k * 0.2, 0.25, (k % 3 - 1) * 0.7)

# ---------------------------------------------------------------- 2. the lab: dark hum, camera shutters, the monitor scans
fx.put(osfx.lib("whoosh"), B["LAB"] - 0.2, 0.7)
hum = sum(0.04 * np.sin(2 * np.pi * f * np.arange(N) / SR) for f in (110, 220)) * seg(B["LAB"], B["EYE"], 0.3)
amb.x += hum[:, None]
for k in range(3):
    tk = B["SNAP"] + k * 1.1
    fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(1800, 1.0)), tk, 0.9)
    fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_switch_01", thump(400, 0.06, 1.0)), tk + 0.07, 0.7)
    fx.put(thump(80, 0.25, 2.0), tk, 0.6)
fx.put(osfx.sound("oga/scifi/terminal_01", blip(1200)), B["SNAP"] + 0.2, 0.5)
fx.put(osfx.sound("oga/scifi/terminal_03", blip(900)), B["SNAP"] + 1.4, 0.5)
fx.put(osfx.sound("oga/scifi/beep_01", blip(1500)), B["SNAP"] + 2.6, 0.6)

# ---------------------------------------------------------------- 3. the eye: the meter fills, the tiny glow bar fails ("wrong")
fx.put(osfx.lib("whoosh"), B["EYE"] - 0.2, 0.7)
fx.put(riser(0.8, 300, 1200), B["EYE"] + 0.2, 0.5)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", sweep(0.6, 600, 150)), B["EYE"] + 1.4, 0.8)
fx.put(impact(0.9), B["EYE"] + 1.4, 0.7)
fx.put(osfx.sound("oga/retro-synth/synth_beep_01", blip(500)), B["EYE"] + 1.55, 0.4)

# ---------------------------------------------------------------- 4. the photon map scans in; the clock ticks to 4 pm
fx.put(osfx.lib("whoosh-cinematic"), B["FACE"] - 0.2, 0.7)
fx.put(osfx.sound("oga/scifi/teleport_02", sweep(0.8, 300, 2000)), B["FACE"] + 0.2, 0.6)
fx.put(osfx.sfxr("powerUp", seed=14), B["FACE"] + 1.1, 0.45)
fx.put(osfx.lib("whoosh"), B["CLOCK"] - 0.2, 0.6)
for k in range(12):
    fx.put(F.tick(3000 if k % 2 else 2400, 1.0), B["CLOCK"] + 0.3 + k * 0.2, 0.6)
fx.put(riser(2.4, 200, 1500), B["CLOCK"] + 0.3, 0.45)
fx.put(add(bell(1046.5, 1.5), 0.5 * bell(1568, 1.5)), B["BACK"] - 0.5, 0.5)
fx.put(osfx.sound("oga/100-sfx/gong_02", gong(110)), B["BACK"] - 0.5, 0.5)

# ---------------------------------------------------------------- 5. lights on, CLICK, lights off: the glow again (loop)
fx.put(osfx.lib("whoosh"), B["BACK"] - 0.2, 0.6)
fx.put(osfx.sound("oga/100-sfx/switch_02", F.tick(1500, 1.0)), B["OFF"] - 0.15, 1.0)
fx.put(sub_drop(0.8), B["OFF"], 0.7)
fx.put(F.sparkle(1.0, seed=21), B["OFF"] + 0.05, 0.5)
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
