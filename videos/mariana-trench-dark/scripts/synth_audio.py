"""Sound for "Where Sunlight Never Reaches" (the Mariana Trench) — no narration, text cards + sound (STYLE_GUIDE.md section 6).

Signature sound: the submarine's SONAR PING. It never stops: bright and short at the surface, then lower, slower and
with a longer echo the deeper the sub goes (the echo time grows with the depth on the counter). On top: a depth tick
per 250 m that speeds up with the dive, hull creaks that get louder with the pressure, waves + gulls + a splash at the
surface, a wind howl for Everest, the sunbeam's "bye", the anglerfish's lure hum, a foam cup crunching, a snailfish
hello, the touchdown thud, amphipod squeaks. Tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 34.0
B = dict(SURF=2.4, DIVE=4.5, EVER=6.7, FADE=8.9, DARK=11.0, GLOW=13.1, PRESS=15.2, CUP=17.3, FISH=19.4, BREAK=21.35,
         HIT=21.6, LIFE=23.9, STILL=26.2, AWAY=28.4, CTA=30.6, STOP=32.6, REWIND=33.4)

CARDS = [
    (0.10, 2.30, "SUNLIGHT NEVER|REACHES *HERE*"),
    (2.40, 4.40, "THE *MARIANA*|TRENCH"),
    (4.50, 6.60, "NEARLY *11 KM*|DOWN"),
    (6.70, 8.80, "EVEREST WOULD|FIT *INSIDE*"),
    (8.90, 10.90, "LIGHT FADES|BY *200 M*"),
    (11.00, 13.00, "BY 1,000 M:|*TOTAL DARK*"),
    (13.10, 15.10, "ONLY LIGHT:|*ANIMAL GLOW*"),
    (15.20, 17.20, "PRESSURE:|*1,000X* MORE"),
    (17.30, 19.30, "A FOAM CUP|*SHRINKS*"),
    (19.40, 21.30, "FISH AT|*8,000 M*"),
    (21.60, 23.80, "CHALLENGER|*DEEP*"),
    (23.90, 26.10, "AND YET...|*LIFE*"),
    (26.20, 28.30, "CRUSHED. DARK.|STILL *ALIVE*"),
    (28.40, 30.50, "LIFE FINDS|*A WAY*"),
    (30.60, 32.50, "WOULD YOU|*GO DOWN*?"),
]

# depth (m) keyframes, shared with the picture: (time, depth); eased between keys in both
DEPTH = [[0.0, 10935], [B["SURF"] - 0.01, 10935], [B["SURF"], 0], [B["DIVE"], 0], [B["EVER"], 120], [B["FADE"], 200],
         [B["DARK"], 1000], [B["GLOW"], 1000], [B["PRESS"], 2500], [B["CUP"], 4500], [B["FISH"], 8000], [B["HIT"], 10935],
         [DUR, 10935]]
B["DEPTH"] = DEPTH


def depth(t):
    for (t0, d0), (t1, d1) in zip(DEPTH, DEPTH[1:]):
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0)
            u = 0.5 - 0.5 * np.cos(np.pi * u)
            return d0 + (d1 - d0) * u
    return DEPTH[-1][1]


PINGS = []
t = 0.15
while t < B["STOP"]:
    PINGS.append(round(t, 3))
    t += 1.0 if (B["SURF"] <= t < B["HIT"]) else 1.4
B["PINGS"] = PINGS
TICKS = []                                          # a tick every 250 m on the way down
for k in range(1, 44):
    target = k * 250
    for i in range(int(B["DIVE"] * 100), int(B["HIT"] * 100)):
        if depth(i / 100) >= target:
            TICKS.append(round(i / 100, 2))
            break
B["TICKS"] = TICKS

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the 8-bit bed: deep, never stops, drops before touchdown
fx.x += CT.bed([
    S(0.0, B["SURF"], 96, 96, "kbo"),
    S(B["SURF"], B["DIVE"], 120, 120, "kbha"),
    S(B["DIVE"], B["DARK"], 120, 124, "kbhs"),
    S(B["DARK"], B["PRESS"], 108, 108, "kbo"),
    S(B["PRESS"], B["BREAK"], 126, 146, "kbhsa"),
    S(B["HIT"] + 0.1, B["LIFE"], 96, 96, "kbo"),
    S(B["LIFE"], B["STOP"] + 0.2, 118, 118, "kbhal"),
], gain=0.38, crescendo=(0.8, 1.15))
amb.x += (0.25 * F.drone(DUR, 41, seed=5))[:, None]

# ---------------------------------------------------------------- SIGNATURE: the sonar ping, deeper + longer echo with depth
for p in PINGS:
    d = depth(p)
    k = min(1.0, d / 10935)
    f = 1700 - 900 * k
    fx.put(CT.ping(f, 0.7 + 0.8 * k), p, 0.2, -0.2)
    fx.put(CT.ping(f, 0.5 + 0.6 * k), p + 0.12 + 0.45 * k, 0.07 + 0.04 * k, 0.4)      # the echo off the bottom
# depth ticks
for k, t in enumerate(TICKS):
    fx.put(F.tick(2600 - min(k, 40) * 25, 0.9), t, 0.22, (k % 2) * 0.4 - 0.2)

# ---------------------------------------------------------------- frame 1: the bottom (amphipods)
for k in range(4):
    fx.put(osfx.sound("oga/creatures/bug_0" + str(1 + k % 4), blip(1400)), 0.4 + k * 0.45, 0.22, (k % 2) - 0.5)
fx.put(osfx.sound("oga/water-splash/bubble_02", F.bubble_(0.4, 500)), 1.2, 0.25)

# ---------------------------------------------------------------- the surface: waves, gulls, splash, sunbeam says hi
fx.put(F.sea(B["DIVE"] - B["SURF"] + 0.6, seed=3), B["SURF"], 0.4)
fx.put(F.gull(seed=4), B["SURF"] + 0.3, 0.3, 0.5)
fx.put(F.gull(seed=8), B["SURF"] + 1.3, 0.2, -0.5)
fx.put(osfx.sound("oga/creatures/cute_05", blip(1300)), B["SURF"] + 1.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/splash_01", F.splash(1.0)), B["DIVE"] + 0.05, 0.7)
fx.put(osfx.sound("oga/water-splash/loop_bubbles_1", F.boil(1.5)), B["DIVE"] + 0.2, 0.35)
fx.put(sweep(0.6, 1500, 200) * 0.5, B["DIVE"] + 0.1, 0.3)
# ---------------------------------------------------------------- Everest drops into the trench
fx.put(F.wind(1.6, 400, 900, 0.8, seed=6), B["EVER"] + 0.1, 0.35)
fx.put(sweep(0.8, 1800, 200) * 0.4, B["EVER"] + 0.3, 0.3)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_stones_02", impact(0.6)), B["EVER"] + 1.1, 0.6)
fx.put(taiko(55), B["EVER"] + 1.1, 0.5)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["EVER"] + 1.6, 0.25)     # "2 KM SPARE"
# ---------------------------------------------------------------- light fades: the sunbeam yawns, says bye at 1,000 m
fx.put(CT.tone_glide(1200, 300, 1.4, "square", 0.25, 0.4), B["FADE"] + 0.3, 0.1)
fx.put(osfx.sound("oga/creatures/snore", blip(300)), B["FADE"] + 1.2, 0.25)
fx.put(osfx.sound("oga/creatures/cute_07", blip(900)), B["DARK"] + 0.4, 0.35)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", sweep(0.4, 600, 150)), B["DARK"] + 0.9, 0.3)
fx.put(F.poof(9), B["DARK"] + 1.0, 0.3)
# ---------------------------------------------------------------- the anglerfish glow
n = int(1.8 * SR)
tt = np.arange(n) / SR
hum = np.sin(2 * np.pi * 220 * tt + 3 * np.sin(2 * np.pi * 5 * tt)) * np.minimum(1, tt / 0.3) * np.minimum(1, (1.8 - tt) / 0.3)
fx.put(hum, B["GLOW"] + 0.3, 0.12)
fx.put(F.sparkle(1.0, seed=4, lo=1500, hi=4000), B["GLOW"] + 0.3, 0.25)
fx.put(osfx.sound("oga/creatures/monster_04", roar(0.6)), B["GLOW"] + 1.2, 0.35)
fx.put(osfx.sound("oga/creatures/eat_03", F.tick(700)), B["GLOW"] + 1.6, 0.4)
# ---------------------------------------------------------------- pressure: creaks grow, metal groans
for k in range(7):
    t0 = B["PRESS"] + k * 0.85
    fx.put(osfx.sound("oga/100-sfx/metal_0" + str(1 + k % 9), F.creak(0.7)), t0, 0.15 + 0.04 * k, (k % 2) - 0.5)
    fx.put(F.creak(0.6, 70 + k * 6, seed=k + 3), t0 + 0.4, 0.2 + 0.03 * k)
fx.put(sub_drop(1.0), B["PRESS"] + 0.1, 0.45)
# ---------------------------------------------------------------- the foam cup crunches smaller (3 crunches)
for k in range(3):
    fx.put(osfx.sound("oga/100-sfx/paper_0" + str(1 + k), F.ice_crack(seed=k)), B["CUP"] + 0.4 + k * 0.45, 0.5, (k - 1) * 0.4)
    fx.put(CT.square(700 - k * 150, 0.05, 0.5), B["CUP"] + 0.4 + k * 0.45, 0.12)
fx.put(osfx.sound("oga/creatures/ooh", blip(500)), B["CUP"] + 1.7, 0.3)
# ---------------------------------------------------------------- the snailfish says hi
fx.put(osfx.sound("oga/creatures/cute_03", blip(1100)), B["FISH"] + 0.6, 0.35)
fx.put(osfx.sound("oga/water-splash/bubble_03", F.bubble_(0.3, 700)), B["FISH"] + 0.3, 0.3)
# ---------------------------------------------------------------- touchdown at Challenger Deep: break -> THUD
fx.put(riser(B["BREAK"] - B["FISH"], 120, 1600), B["FISH"], 0.22)
fx.put(impact(1.0), B["HIT"], 0.6)
fx.put(sub_drop(1.4), B["HIT"], 0.7)
fx.put(osfx.sound("oga/100-sfx/slam_02", thump(50)), B["HIT"], 0.55)
fx.put(braam(2.0, 41), B["HIT"] + 0.05, 0.35)
fx.put(F.rumble(1.6, 25, 300), B["HIT"], 0.4)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(880, 1.5)), B["HIT"] + 1.2, 0.2)
# ---------------------------------------------------------------- life: amphipods swarm in (a squeak each)
for k in range(12):
    fx.put(osfx.sound("oga/creatures/bug_0" + str(1 + k % 4), blip(1300 + (k % 3) * 200)), B["LIFE"] + 0.2 + k * 0.17, 0.2, (k % 3 - 1) * 0.5)
fx.put(F.harp_up(), B["LIFE"] + 0.3, 0.3)
fx.put(osfx.sound("oga/water-splash/slime_05", F.bubble_(0.4, 250)), B["STILL"] + 0.4, 0.3)   # the xenophyophore blob
fx.put(osfx.sound("oga/creatures/cute_08", blip(1200)), B["STILL"] + 1.0, 0.3)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["AWAY"] + 0.2, 0.35)
for i, f0 in enumerate([523.25, 659.25, 783.99, 1046.5]):
    fx.put(bell(f0, 1.2), B["AWAY"] + 0.6 + i * 0.08, 0.18)
fx.put(CT.tone_glide(500, 900, 0.25, "square", 0.5, 0.3), B["CTA"] + 0.6, 0.3)        # "?"
fx.put(osfx.sound("oga/creatures/cute_01", blip(1200)), B["CTA"] + 1.0, 0.3)

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.14)
for tc in (B["SURF"], B["EVER"], B["FADE"], B["LIFE"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.45)
    fx.put(impact(0.4), tc, 0.25)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 96, 96, "kbo")], gain=0.38, crescendo=(0.8, 0.8))

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=4.5)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR, "ticks", len(TICKS), "pings", len(PINGS))
