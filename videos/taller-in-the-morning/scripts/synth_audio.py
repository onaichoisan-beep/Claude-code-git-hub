"""Sound for "You shrink 1 cm every day": open-source sound effects only (no narration, owner's request), loud.

  python3 scripts/synth_audio.py

Layers from OPEN-SOURCE sources (osfx.py): CC0 Kenney.nl / OpenGameArt recordings, jsfxr 8-bit effects, the bundled
HyperFrames library, and the numpy kits (sfxlib cinematic hits, foley). Everything used is frozen into assets/sfx/.
Writes assets/audio/mix.wav + captions.js (text cards + the beats the picture shares).
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
B = dict(SQUASH=0.45, GLITCH=1.55, MORN=1.8, MARK_AM=3.4, SPINE=5.0, SQUEEZE=7.6, NIGHT=11.0, MARK_PM=12.6,
         SLEEP=14.6, REFILL=15.2, SPACE=17.8, GROW=18.6, BACK=20.7)

# text cards: (start, end, text); *word* = gold, | = new line
CARDS = [
    (0.10, 1.55, "YOU SHRINK *1 CM*|EVERY SINGLE DAY"),
    (2.00, 4.90, "7 AM: YOU'RE AT|YOUR *TALLEST*"),
    (5.20, 7.55, "BETWEEN YOUR SPINE|BONES: SOFT *DISCS*"),
    (7.65, 10.90, "ALL DAY, *GRAVITY*|SQUEEZES WATER OUT"),
    (11.20, 14.45, "BY 10 PM: ABOUT|*1 CM* SHORTER"),
    (14.80, 17.70, "LYING DOWN, THEY|*REFILL* OVERNIGHT"),
    (17.95, 20.60, "NO GRAVITY IN SPACE:|UP TO *5 CM* TALLER!"),
    (20.80, 21.85, "MEASURE YOURSELF|*TONIGHT*"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()

# ---------------------------------------------------------------- 0. hook: a slam, then the body gets squashed down
fx.put(osfx.sound("oga/100-sfx/slam_01", impact(1.0)), 0.0, 0.9)
fx.put(impact(1.0), 0.0, 0.7)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.5)
fx.put(sweep(0.35, 700, 120), B["SQUASH"], 0.5)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_hit_01", thump(90, 0.3, 2.0)), B["SQUASH"] + 0.25, 0.9)
fx.put(sub_drop(0.9), B["SQUASH"] + 0.25, 0.8)
fx.put(osfx.sound("oga/100-sfx/spring_01", sweep(0.3, 400, 200)), B["SQUASH"] + 0.05, 0.5)
fx.put(osfx.sfxr("hitHurt", seed=3), B["SQUASH"] + 0.3, 0.35)
# rewind glitch back to the morning
fx.put(rewind(0.4), B["GLITCH"] - 0.05, 0.7)
fx.put(osfx.lib("glitch-1"), B["GLITCH"], 0.5)

# ---------------------------------------------------------------- 1. morning: birds, alarm clock, a big stretch, the green mark
for k in range(7):
    fx.put(F.chirp(30 + k), B["MORN"] + 0.3 + 0.45 * k, 0.25, (k % 3 - 1) * 0.6)
for k in range(8):
    fx.put(osfx.sound("oga/100-sfx/bell_01", bell(2200, 0.5)) [: int(0.13 * SR)], B["MORN"] + 0.2 + k * 0.15, 0.4, 0.5)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_air_01", noise_hit(0.3, 300, 3000)), B["MORN"] + 1.3, 0.6)
fx.put(osfx.sound("oga/creatures/breath", sweep(0.4, 200, 600)), B["MORN"] + 1.35, 0.5)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_wood_hit_01", thump(300, 0.08, 1.0)), B["MARK_AM"], 0.8)
fx.put(osfx.sfxr("pickupCoin", seed=12), B["MARK_AM"] + 0.02, 0.45)

# ---------------------------------------------------------------- 2. x-ray: hum, gravity thumps, the discs squish out water
fx.put(osfx.lib("whoosh"), B["SPINE"] - 0.2, 0.7)
fx.put(osfx.sound("oga/scifi/teleport_01", sweep(0.8, 900, 300)), B["SPINE"], 0.5)
hum = sum(0.05 * np.sin(2 * np.pi * f * np.arange(N) / SR) for f in (60, 120, 180)) * seg(B["SPINE"], B["NIGHT"], 0.3)
amb.x += hum[:, None]
for k in range(4):
    tk = B["SQUEEZE"] + k * 0.8
    fx.put(taiko(65), tk, 0.9)
    fx.put(osfx.sound(f"oga/100-sfx/hit_0{k % 4 + 1}", thump(70, 0.3, 2.0)), tk, 0.7)
    fx.put(osfx.sound(f"oga/water-splash/slime_0{k % 9 + 1}", F.splash(0.4, 5 + k)), tk + 0.1, 0.7, (k % 2) * 1.2 - 0.6)
for k in range(10):
    fx.put(F.tick(2600, 0.8), B["SPINE"] + 0.6 + k * 0.5, 0.3)

# ---------------------------------------------------------------- 3. night: crickets, a yawn, the red mark + a low "uh-oh" hit
fx.put(osfx.lib("whoosh"), B["NIGHT"] - 0.2, 0.7)
amb.x += (0.45 * F.crickets(DUR, seed=4) * seg(B["NIGHT"], B["SPACE"], 0.4))[:, None]
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.8, 300, 150)), B["NIGHT"] + 0.3, 0.6)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_wood_hit_02", thump(260, 0.08, 1.0)), B["MARK_PM"], 0.8)
fx.put(braam(1.6, 55), B["MARK_PM"] + 0.05, 0.75)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", tone(220, 0.3)), B["MARK_PM"] + 0.1, 0.6)

# ---------------------------------------------------------------- 4. asleep: snores, the discs bubble back up
fx.put(osfx.lib("whoosh"), B["SLEEP"] - 0.2, 0.6)
for k in range(3):
    fx.put(osfx.sound("oga/creatures/snore", F.purr(0.9)), B["SLEEP"] + 0.2 + k * 1.05, 0.7)
fx.put(osfx.sound("oga/water-splash/loop_bubbles_02", F.boil(2.0)), B["REFILL"], 0.6)
fx.put(F.harp_up(523.25, 8, 0.07), B["REFILL"] + 0.6, 0.45)
fx.put(osfx.sfxr("powerUp", seed=8), B["SPACE"] - 0.55, 0.35)

# ---------------------------------------------------------------- 5. space: whoosh into orbit, a stretch riser, "+5 cm" hit
fx.put(osfx.lib("whoosh-cinematic"), B["SPACE"] - 0.25, 0.8)
amb.x += (0.3 * band(F.rumble(DUR, 30, 200, seed=5), 30, 300) * seg(B["SPACE"], B["BACK"], 0.3))[:, None]
fx.put(osfx.sound("oga/scifi/loop_ambient_01", sweep(1.0, 80, 120)), B["SPACE"], 0.4)
fx.put(riser(1.0, 200, 1200), B["GROW"], 0.6)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_metal_hit_01", impact(0.8)), B["GROW"] + 1.0, 0.8)
fx.put(impact(1.0), B["GROW"] + 1.0, 0.6)
fx.put(osfx.sfxr("powerUp", seed=21), B["GROW"] + 1.0, 0.45)
fx.put(osfx.lib("sparkle"), B["GROW"] + 1.05, 0.5)

# ---------------------------------------------------------------- 6. back to the morning, whoosh into the loop
fx.put(osfx.lib("whoosh"), B["BACK"] - 0.2, 0.7)
for k in range(3):
    fx.put(F.chirp(60 + k), B["BACK"] + 0.2 + 0.35 * k, 0.25)
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
