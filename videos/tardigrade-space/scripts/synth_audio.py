"""Sound for "The Animal That Survived Space" (tardigrade) — no narration, text cards + sound (STYLE_GUIDE.md section 6).

Signature sound: the tardigrade's LIFE-SIGN monitor beep. Steady at the start, slowing and dropping in pitch as it dries
into a tun, a flatline, then silence through orbit (Geiger crackle + a tick per DAY instead), then the water drop lands
(0.25 s break, hit) and the beeps come back fast. Egg pops, a Moon crash, a questioning beep; tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 31.0
B = dict(SIZE=2.4, TUN=5.0, FLAT=7.6, LAUNCH=8.6, ORBIT=11.6, RAYS=13.6, POWERS=16.6, BACK=19.0, BREAK=20.25, HIT=20.5,
         BABIES=23.0, MOON=25.5, CRASH=26.1, ASK=27.5, STOP=29.6, REWIND=30.4)

# max 16 characters a line, max 2 lines (safe zone, STYLE_GUIDE.md section 8)
CARDS = [
    (0.10, 2.30, "IT SURVIVED|*SPACE*"),
    (2.40, 4.90, "ONLY *0.5 MM*|LONG"),
    (5.00, 6.80, "IT CAN DRY UP|INTO A *TUN*"),
    (6.90, 8.50, "ALMOST *NO*|WATER LEFT"),
    (8.60, 11.50, "2007: SENT|INTO *ORBIT*"),
    (11.60, 13.50, "LID OPENS:|*NO* AIR"),
    (13.60, 16.50, "10 DAYS OF|*COSMIC RAYS*"),
    (16.60, 18.90, "BASICALLY|*UNKILLABLE*"),
    (19.00, 20.20, "BACK HOME:|ADD *WATER*"),
    (20.50, 22.90, "IT CAME|BACK *ALIVE*"),
    (23.00, 25.40, "AND LAID EGGS|THAT *HATCHED*"),
    (25.50, 27.40, "2019: CRASHED|ON THE *MOON*"),
    (27.50, 29.50, "STILL ALIVE?|*YES* OR *NO*?"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec


def beep(f=1000.0, d=0.07):
    return CT.square(f, d, 0.5) * 0.8 + 0.4 * np.sin(2 * np.pi * f * 2 * np.arange(int(d * SR)) / SR)


# ---------------------------------------------------------------- the 8-bit bed: steady -> slows as it dries -> builds in orbit
fx.x += CT.bed([
    S(0.0, B["TUN"], 118, 118, "kbh"),
    S(B["TUN"], B["LAUNCH"], 112, 92, "kbo"),
    S(B["LAUNCH"], B["ORBIT"], 120, 140, "kbhs"),
    S(B["ORBIT"], B["POWERS"], 124, 124, "kbha"),
    S(B["POWERS"], B["BREAK"], 128, 128, "kbhsa"),
    S(B["HIT"] + 0.15, B["MOON"], 128, 128, "kbhsal"),
    S(B["MOON"], B["STOP"] + 0.2, 124, 124, "kbha"),
], gain=0.42, crescendo=(0.8, 1.2))
amb.x += (0.25 * F.drone(DUR, 55, seed=4))[:, None]

# ---------------------------------------------------------------- SIGNATURE: the life-sign monitor
t = 0.25
while t < B["TUN"]:                                   # alive and well: a steady beep
    fx.put(beep(1000), t, 0.3, 0.2)
    t += 0.6
gap, f0 = 0.6, 1000.0
while t < B["FLAT"]:                                  # drying out: slower, lower
    fx.put(beep(f0), t, 0.3, 0.2)
    t += gap
    gap *= 1.28
    f0 *= 0.93
flat = beep(700, B["LAUNCH"] - B["FLAT"] - 0.1) * np.linspace(1, 0.2, int((B["LAUNCH"] - B["FLAT"] - 0.1) * SR))
fx.put(flat, B["FLAT"], 0.18, 0.2)                    # the flatline ("BRB.")
fx.put(osfx.sound("oga/retro-synth/retro_die_01", sweep(0.4, 600, 150)), B["TUN"] + 0.3, 0.3)
fx.put(F.poof(113), B["TUN"] + 1.2, 0.4)
t = B["HIT"] + 0.05                                   # revived: fast beeps that settle
gap = 0.18
while t < B["MOON"] + 0.4:
    fx.put(beep(1150), t, 0.3, 0.2)
    t += gap
    gap = min(0.55, gap * 1.12)

# ---------------------------------------------------------------- launch 2007
fx.put(osfx.sound("oga/scifi/rocket", F.rumble(2.5)), B["LAUNCH"] + 0.4, 0.7)
fx.put(F.rumble(2.6, 25, 400), B["LAUNCH"] + 0.4, 0.6)
fx.put(riser(2.4, 120, 1400), B["LAUNCH"] + 0.4, 0.3)
for k in range(3):
    fx.put(F.tick(1800, 1.0), B["LAUNCH"] - 0.4 + k * 0.33 - 0.66, 0.3)

# ---------------------------------------------------------------- orbit: lid opens, a tick per DAY, Geiger crackle for the rays
fx.put(osfx.sound("oga/100-sfx/door_open", F.creak(0.6)), B["ORBIT"] + 0.15, 0.5)
fx.put(sweep(0.6, 3000, 200) * 0.5, B["ORBIT"] + 0.3, 0.3)       # the air hisses out
for d in range(11):
    fx.put(F.tick(2400 + d * 90, 1.0), B["ORBIT"] + 0.3 + d * (B["POWERS"] - B["ORBIT"] - 0.5) / 10, 0.4, 0.3)
fx.put(CT.crackle(lambda x: 4 + 40 * ((x - B["RAYS"]) / (B["POWERS"] - B["RAYS"])) ** 1.5, B["RAYS"], B["POWERS"], seed=9), B["RAYS"], 0.25, -0.3)
for k in range(4):
    fx.put(osfx.sound("oga/scifi/retro_laser_01", sweep(0.2, 2000, 400)), B["RAYS"] + 0.3 + k * 0.7, 0.25, (k % 2) - 0.5)

# ---------------------------------------------------------------- powers: three hits + braam
for k in range(3):
    fx.put(impact(0.6), B["POWERS"] + 0.1 + k * 0.75, 0.45)
    fx.put(osfx.lib("pop"), B["POWERS"] + 0.1 + k * 0.75, 0.3)
fx.put(braam(2.0, 48), B["POWERS"] + 0.1, 0.35)

# ---------------------------------------------------------------- the water drop: break -> hit
fx.put(osfx.sound("oga/water-splash/bubble", F.bubble_(0.5, 600)), B["BACK"] + 0.3, 0.35)
fx.put(riser(B["HIT"] - B["BACK"] - 0.1, 200, 2000), B["BACK"], 0.25)
fx.put(osfx.sound("oga/water-splash/splash", F.splash(0.6)), B["HIT"], 0.7)
fx.put(impact(0.9), B["HIT"], 0.6)
fx.put(osfx.sound("oga/retro-synth/power_up", F.harp_up()), B["HIT"] + 0.25, 0.4)
for i, f0 in enumerate([523.25, 659.25, 783.99, 1046.5]):
    fx.put(bell(f0, 1.2), B["HIT"] + 0.6 + i * 0.07, 0.22)

# ---------------------------------------------------------------- eggs hatch: a pop per egg (7)
for k in range(7):
    fx.put(osfx.lib("pop"), B["BABIES"] + 0.4 + k * 0.28, 0.35, (k % 3 - 1) * 0.5)
    fx.put(CT.square(880 * 2 ** (k / 12 * 2), 0.05, 0.25), B["BABIES"] + 0.4 + k * 0.28, 0.12)

# ---------------------------------------------------------------- the Moon crash, the question
fx.put(sweep(0.6, 1800, 200) * 0.4, B["CRASH"] - 0.6, 0.4)
fx.put(osfx.sound("oga/scifi/explosion_01", impact(1.0)), B["CRASH"], 0.8)
fx.put(sub_drop(1.2), B["CRASH"], 0.7)
fx.put(beep(1150, 0.08), B["ASK"] + 0.3, 0.3)
fx.put(CT.tone_glide(500, 900, 0.25, "square", 0.5, 0.3), B["ASK"] + 0.7, 0.3)   # "?"

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.14)
for tc in (B["TUN"], B["LAUNCH"], B["ORBIT"], B["POWERS"], B["BACK"], B["BABIES"], B["MOON"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.45)
    fx.put(impact(0.4), tc, 0.25)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 118, 118, "kbh")], gain=0.42, crescendo=(0.8, 0.8))
fx.put(beep(1000), B["REWIND"] + 0.25, 0.3, 0.2)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=4.5)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
