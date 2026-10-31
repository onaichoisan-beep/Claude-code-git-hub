"""Sound for "GPS only works because of Einstein": open-source sound effects only (no narration, owner's request), loud.

  python3 scripts/synth_audio.py

Layers from OPEN-SOURCE sources (osfx.py): CC0 OpenGameArt recordings (sci-fi beeps/terminals/teleport, slams, retro
synth, switches), jsfxr, the bundled HyperFrames library, and the numpy kits (sfxlib, foley). Everything used is frozen
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
B = dict(GLITCH=1.55, SATS=1.8, CLOCKS=6.0, NET=8.3, LIGHT=10.4, ERR=12.5, DRIFT=14.6, FIX=18.6, SNAP=19.9, BACK=20.6)

CARDS = [
    (0.10, 1.55, "WITHOUT *EINSTEIN*, YOUR|MAP DRIFTS 10 KM A DAY"),
    (2.00, 5.80, "GPS SATELLITES CARRY|*ATOMIC CLOCKS*"),
    (6.20, 8.20, "UP HIGH, WEAKER GRAVITY:|TIME RUNS *FASTER*"),
    (8.35, 10.30, "THEIR CLOCKS GAIN *38*|MICROSECONDS A DAY"),
    (10.60, 12.40, "SIGNALS TRAVEL AT THE|*SPEED OF LIGHT*"),
    (12.55, 14.45, "38 MICROSECONDS =|ABOUT *11 KM* OF ERROR"),
    (14.80, 18.40, "UNFIXED, YOUR DOT DRIFTS|*KILOMETRES* EVERY DAY"),
    (18.80, 20.45, "SO THE CLOCKS ARE SET|TO TICK *SLOWER*"),
    (20.70, 21.85, "THANKS, *EINSTEIN*"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()

# ---------------------------------------------------------------- 0. hook: the dot drifts into the sea — alarm beeps + slam
fx.put(osfx.sound("oga/100-sfx/slam_06", impact(1.0)), 0.0, 0.9)
fx.put(impact(1.0), 0.0, 0.6)
for k in range(4):
    fx.put(osfx.sound("oga/retro-synth/synth_beep_02", blip(1300)), 0.6 + k * 0.2, 0.6)
fx.put(braam(1.2, 58), 1.2, 0.6)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", sweep(0.5, 700, 150)), 1.2, 0.6)
fx.put(rewind(0.4), B["GLITCH"] - 0.05, 0.7)
fx.put(osfx.lib("glitch-2"), B["GLITCH"], 0.5)

# ---------------------------------------------------------------- 1. orbit: space drone, satellite beeps, the atomic clock zoom
space = seg(B["SATS"], B["DRIFT"], 0.3)
amb.x += (0.4 * F.drone(DUR, 55, seed=5) * space)[:, None]
fx.put(osfx.lib("whoosh-cinematic"), B["SATS"] - 0.2, 0.8)
for k in range(5):
    fx.put(osfx.sound(f"oga/scifi/beep_0{k % 3 + 1}", blip(1000 + 200 * k)), B["SATS"] + 0.4 + k * 0.6, 0.35, (k % 3 - 1) * 0.7)
fx.put(osfx.sound("oga/scifi/teleport_01", sweep(0.5, 300, 1500)), B["SATS"] + 1.6, 0.6)
for k in range(10):
    fx.put(F.tick(2800, 1.0), B["SATS"] + 1.8 + k * 0.2, 0.45)

# ---------------------------------------------------------------- 2. clocks: two tickings, orbit one creeping ahead; +38 hit
fx.put(osfx.lib("whoosh"), B["CLOCKS"] - 0.2, 0.7)
for k in range(20):
    fx.put(F.tick(3000, 1.0), B["CLOCKS"] + 0.2 + k * 0.205, 0.45, 0.6)
    fx.put(F.tick(2200, 1.0), B["CLOCKS"] + 0.2 + k * 0.215, 0.45, -0.6)
fx.put(riser(1.2, 300, 1300), B["NET"] - 0.2, 0.45)
fx.put(osfx.sound("oga/100-sfx/slam_02", impact(0.9)), B["NET"], 0.8)
fx.put(impact(1.0), B["NET"], 0.6)
fx.put(osfx.sfxr("pickupCoin", seed=4), B["NET"] + 1.2, 0.45)

# ---------------------------------------------------------------- 3. light-speed signals zap down; the 11 km error ruler
fx.put(osfx.lib("whoosh-cinematic"), B["LIGHT"] - 0.2, 0.7)
for k in range(8):
    fx.put(osfx.sound(f"oga/retro-synth/synth_laser_0{k % 8 + 1}", sweep(0.2, 2000, 600)), B["LIGHT"] + 0.2 + k * 0.25, 0.35, (k % 3 - 1) * 0.6)
fx.put(braam(1.6, 52), B["ERR"], 0.75)
fx.put(osfx.sound("oga/100-sfx/slam_04", impact(0.8)), B["ERR"], 0.8)
fx.put(osfx.sound("oga/scifi/terminal_02", blip(800)), B["ERR"] + 0.8, 0.5)

# ---------------------------------------------------------------- 4. drift: day ticks, alarm beeps get faster
fx.put(osfx.lib("whoosh"), B["DRIFT"] - 0.2, 0.7)
for d in range(3):
    td = B["DRIFT"] + d * (B["FIX"] - B["DRIFT"] - 0.3) / 3
    fx.put(taiko(70), td, 0.8)
    fx.put(osfx.sound("oga/scifi/terminal_04", blip(600)), td + 0.05, 0.5)
    for k in range(3 + d * 2):
        fx.put(osfx.sound("oga/retro-synth/synth_beep_02", blip(1300)), td + 0.3 + k * (0.9 / (3 + d * 2)), 0.45)

# ---------------------------------------------------------------- 5. the fix: dial ratchets down, the dot snaps back (ding)
fx.put(osfx.lib("whoosh"), B["FIX"] - 0.2, 0.6)
fx.put(F.ratchet(1.0), B["FIX"] + 0.2, 0.6)
fx.put(sweep(0.9, 1200, 300), B["FIX"] + 0.25, 0.35)
fx.put(osfx.sound("oga/retro-synth/power_up_01", F.harp_up()), B["SNAP"], 0.6)
fx.put(add(bell(1046.5, 1.5), 0.5 * bell(1568, 1.5)), B["SNAP"] + 0.05, 0.5)
fx.put(impact(0.7), B["SNAP"], 0.5)

# ---------------------------------------------------------------- 6. thanks, Einstein: pop-up, sparkle, whoosh into the loop
fx.put(osfx.lib("pop"), B["BACK"] + 0.2, 0.7)
fx.put(osfx.lib("sparkle"), B["BACK"] + 0.3, 0.5)
fx.put(osfx.sound("oga/creatures/cute_04", F.chatter(0.4)), B["BACK"] + 0.5, 0.4)
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
