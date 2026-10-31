"""Sound for "Japanese honeybees cook a giant hornet alive" — sound follows the story (STYLE_GUIDE.md section 6):

- SIGNATURE: the swarm buzz. It starts as a few guard bees, thickens as the BEES counter climbs to 500, and its pitch and
  loudness rise with the TEMP counter (35 -> 46 C) until it screams; it cuts dead at the 0.25 s break, then the K.O.
- the hornet's deep drone grows as the DISTANCE counter shrinks; stings bounce off its armour with metallic "tinks";
- a nonstop 8-bit bed whose tempo climbs with the heat (112 -> 168 BPM), a tick on every degree, a blip on every card,
  whoosh + hit on every cut, a crescendo, a tape-stop + rewind into the loop.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 30.0
B = dict(GLITCH=-1.0, APPROACH=0.0, ARMOR=4.0, SWARM=7.0, HEAT=10.0, BREAK=18.25, KO=18.5, THERMO=20.5, CHEER=25.0,
         STOP=28.5, REWIND=29.3)

CARDS = [
    (0.10, 1.90, "THIS GIANT HORNET CAN|KILL *40 BEES* A MINUTE"),
    (2.00, 3.85, "AND IT'S COMING FOR|THE *HIVE*"),
    (4.10, 6.80, "BEE STINGS CAN'T GET|THROUGH ITS *ARMOUR*"),
    (7.20, 9.80, "SO 500 BEES|*SWARM* IT"),
    (10.10, 12.40, "THEY SHIVER THEIR|*FLIGHT MUSCLES*"),
    (12.50, 15.00, "THE BALL HEATS UP|TO *46°C*"),
    (15.10, 18.10, "THE HORNET IS|BEING *COOKED*"),
    (18.50, 20.30, "*K.O.*"),
    (20.60, 22.70, "HORNETS DIE AT|*44-46°C*"),
    (22.80, 24.90, "BEES SURVIVE UP TO|*48-50°C*"),
    (25.10, 28.40, "THEY WIN BY A FEW|DEGREES. *TEAMWORK*!"),
]


def temp(t):
    if t < B["HEAT"]:
        return 35.0
    u = min(1.0, max(0.0, (t - B["HEAT"] - 0.3) / (B["BREAK"] - 0.3 - B["HEAT"] - 0.3)))
    return 35 + 11 * (0.5 - 0.5 * np.cos(np.pi * u))


os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed: tempo follows the heat
fx.x += CT.bed([
    S(B["APPROACH"], B["ARMOR"], 100, 112, "kb"),
    S(B["ARMOR"], B["SWARM"], 112, 118, "kbhs"),
    S(B["SWARM"], B["HEAT"], 118, 124, "kbhsa"),
    S(B["HEAT"], B["BREAK"], 124, 168, "kbhsa"),
    S(B["KO"], B["THERMO"], 128, 128, "kbhsal"),
    S(B["THERMO"], B["CHEER"], 120, 120, "kbha"),
    S(B["CHEER"], B["STOP"] + 0.2, 150, 154, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- SIGNATURE: the swarm buzz (pitch + loudness = TEMP, thickness = BEES)
def bees_amp(t):
    if t < B["GLITCH"]:
        return 0.5
    if t < B["SWARM"]:
        return 0.18
    if t < B["BREAK"]:
        n = min(1.0, (t - B["SWARM"]) / (B["HEAT"] - 0.2 - B["SWARM"]))
        return 0.18 + 0.4 * n + 0.35 * (temp(t) - 35) / 11
    if t < B["KO"]:
        return 0.0
    return 0.22


def bees_f(t):
    return 230 + 210 * (temp(t) - 35) / 11


fx.put(CT.buzz(B["APPROACH"], B["BREAK"], bees_f, bees_amp, voices=6, seed=2), B["APPROACH"], 0.45)
fx.put(CT.buzz(B["KO"], B["STOP"] + 0.2, lambda t: 260 + 30 * np.sin(t * 3), lambda t: 0.22, voices=4, seed=3), B["KO"], 0.45)

# the hornet's deep drone: louder as DISTANCE shrinks, gone at the K.O.
def hornet_amp(t):
    if t < B["GLITCH"]:
        return 0.7
    if t < B["APPROACH"]:
        return 0.0
    if t < B["ARMOR"]:
        return 0.15 + 0.6 * (t - B["APPROACH"]) / (B["ARMOR"] - B["APPROACH"])
    return 0.75 if t < B["HEAT"] else max(0.0, 0.75 - 0.75 * (t - B["HEAT"]) / (B["BREAK"] - B["HEAT"]))


fx.put(CT.buzz(0.0, B["BREAK"], lambda t: 105 + 4 * np.sin(t * 2), hornet_amp, voices=3, seed=9, harmonics=10), 0.0, 0.5)

# ---------------------------------------------------------------- a sound on every change
CT.card_blips(fx, CARDS)
last = 35
for k in range(int((B["BREAK"] - B["HEAT"]) * 50)):                   # a tick on every degree of TEMP
    t = B["HEAT"] + k / 50
    if int(temp(t)) != last:
        last = int(temp(t))
        fx.put(F.tick(2400 + 120 * (last - 35), 1.0), t, 0.45)
for k in range(10):                                                   # BEES counter ticks while they pile on
    fx.put(osfx.lib("pop"), B["SWARM"] + 0.2 + k * 0.28, 0.25, (k % 3 - 1) * 0.6)
for tc in (B["SWARM"], B["THERMO"], B["CHEER"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.55)
    fx.put(impact(0.5), tc, 0.35)

# ---------------------------------------------------------------- 0. the hornet flies in (no cold-open hook: the story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.5)
fx.put(braam(1.6, 55), 0.3, 0.35)

# ---------------------------------------------------------------- 1. stings bounce off the armour: tink tink tink
for s in range(6):
    tk = B["ARMOR"] + 0.3 + s * 0.42
    fx.put(osfx.sound(f"oga/100-sfx/metal_0{s % 9 + 1}", F.tick(3500, 1.0)), tk, 0.55, (s % 3 - 1) * 0.5)
    fx.put(CT.square(2200 + 200 * (s % 3), 0.05, 0.25), tk, 0.12)
fx.put(CT.womp(330, 3, 0.2), B["ARMOR"] + 2.2, 0.35)

# ---------------------------------------------------------------- 2. the swarm closes in, the heat builds
fx.put(osfx.lib("whoosh-cinematic"), B["SWARM"] - 0.2, 0.7)
fx.put(riser(B["BREAK"] - B["HEAT"], 150, 1800), B["HEAT"], 0.3)
fx.put(F.fire(B["BREAK"] - B["HEAT"] - 3, 41) * np.linspace(0, 1, int((B["BREAK"] - B["HEAT"] - 3) * SR)), B["HEAT"] + 3, 0.35)
fx.put(osfx.sound("oga/creatures/hurt_02", sweep(0.4, 400, 700)), B["HEAT"] + 2.2, 0.5)
fx.put(osfx.sound("oga/creatures/hurt_03", sweep(0.4, 450, 800)), B["HEAT"] + 5.4, 0.5)

# ---------------------------------------------------------------- 3. BREAK -> K.O.
fx.put(sweep(B["KO"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.5)
fx.put(osfx.sound("oga/bangs-fireworks/bang_02", impact(1.0)), B["KO"], 0.9)
fx.put(impact(1.0), B["KO"], 0.9)
fx.put(sub_drop(1.0), B["KO"], 0.8)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(1200, 1.5)), B["KO"] + 0.6, 0.6)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", sweep(0.6, 500, 120)), B["KO"] + 0.15, 0.6)

# ---------------------------------------------------------------- 4. the thermometer climbs, the zones pop in
fx.put(riser(1.2, 300, 1300), B["THERMO"] + 0.2, 0.4)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", tone(220, 0.3)), B["THERMO"] + 1.4, 0.5)
fx.put(osfx.sfxr("pickupCoin", seed=4), B["THERMO"] + 2.4, 0.5)
fx.put(osfx.sfxr("powerUp", seed=12), B["THERMO"] + 2.45, 0.35)

# ---------------------------------------------------------------- 5. victory dance + confetti
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up()), B["CHEER"], 0.5)
for k in range(5):
    fx.put(osfx.sound(f"oga/bangs-fireworks/fw_0{k % 6 + 1}", F.firework(71 + k)), B["CHEER"] + 0.3 + k * 0.5, 0.35, (k % 3 - 1) * 0.6)

# ---------------------------------------------------------------- 6. tape-stop -> rewind -> hook (loop)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 100, 100, "kb")], gain=0.5, crescendo=(0.8, 0.8))   # = how the video starts
fx.put(CT.buzz(B["REWIND"] + 0.1, DUR, lambda t: 230, lambda t: 0.18, voices=4, seed=2), B["REWIND"] + 0.1, 0.45)
fx.put(CT.buzz(B["REWIND"] + 0.1, DUR, lambda t: 105, lambda t: 0.15, voices=3, seed=9, harmonics=10), B["REWIND"] + 0.1, 0.5)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
