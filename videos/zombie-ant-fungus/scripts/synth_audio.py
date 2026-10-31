"""Sound for "The zombie ant" — sound follows the counter (STYLE_GUIDE.md section 6), no narration, no cold-open hook:
- INFECTION %: a creeping fungus crackle whose density follows the infection (2 -> 40 crackles/s), a creepy pulse slowing;
- HEIGHT: tiny footsteps whose pitch rises with every centimetre climbed; TIME: clock ticks to noon, a 0.25 s break, CHOMP;
- the heartbeat slows and stops at death; the stalk grows with a rising creak; spores puff down; the trail marches again.

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
B = dict(INFECT=0.6, XRAY=3.0, LEAVE=7.5, CLIMB=9.5, NOON=14.0, BREAK=15.75, HIT=16.0, DEATH=17.8, STALK=20.0,
         SPORES=22.5, AGAIN=24.5, CTA=26.3, STOP=28.5, REWIND=29.3)

CARDS = [
    (0.10, 2.90, "THIS ANT JUST GOT|*INFECTED*"),
    (3.00, 5.40, "A ZOMBIE FUNGUS GROWS|THROUGH ITS *BODY*"),
    (5.50, 7.40, "IT TAKES OVER|ITS *MUSCLES*"),
    (7.50, 9.40, "THE ANT *LEAVES*|ITS COLONY"),
    (9.50, 11.90, "IT CLIMBS UP|A PLANT..."),
    (12.00, 13.90, "TO ABOUT|*25 CM* HIGH"),
    (14.00, 15.70, "AROUND *NOON*..."),
    (16.00, 17.70, "IT BITES A LEAF|AND *LOCKS* ITS JAW"),
    (17.80, 19.90, "THEN IT *DIES*|RIGHT THERE"),
    (20.00, 22.40, "A STALK GROWS OUT|OF ITS *HEAD*"),
    (22.50, 24.40, "SPORES RAIN DOWN|ON THE ANTS *BELOW*"),
    (24.50, 26.20, "AND IT STARTS *AGAIN*"),
    (26.30, 28.40, "NATURE IS *TERRIFYING*.|SEND THIS."),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec


def infection(t):
    return min(1.0, max(0.0, (t - B["INFECT"]) / (B["LEAVE"] - B["INFECT"])))


# ---------------------------------------------------------------- creepy bed: minor 8-bit, tempo creeping up to the bite
fx.x += CT.bed([
    S(0.0, B["XRAY"], 96, 96, "kb"),
    S(B["XRAY"], B["LEAVE"], 96, 104, "kbo"),
    S(B["LEAVE"], B["NOON"], 104, 140, "kbha"),
    S(B["NOON"], B["BREAK"], 140, 160, "kbhs"),
    S(B["DEATH"], B["STALK"], 70, 70, "ko"),
    S(B["STALK"], B["AGAIN"], 110, 120, "kbha"),
    S(B["AGAIN"], B["STOP"] + 0.2, 128, 132, "kbhsal"),
], gain=0.45, crescendo=(0.8, 1.2))
amb.x += (0.3 * F.drone(DUR, 55, seed=7))[:, None]

# ---------------------------------------------------------------- the marching trail (start and end)
for k in range(int(B["XRAY"] / 0.16)):
    fx.put(F.tick(5000 + 300 * (k % 3), 0.5), 0.05 + k * 0.16, 0.16, (k % 5 - 2) * 0.3)
for k in range(int((B["STOP"] - B["AGAIN"]) / 0.16)):
    fx.put(F.tick(5000 + 300 * (k % 3), 0.5), B["AGAIN"] + k * 0.16, 0.16, (k % 5 - 2) * 0.3)
fx.put(osfx.lib("sparkle"), B["INFECT"] - 0.3, 0.4)
fx.put(osfx.sound("oga/water-splash/slime_02", F.splash(0.3, 2)), B["INFECT"], 0.7)
fx.put(braam(1.8, 48), B["INFECT"], 0.5)

# ---------------------------------------------------------------- SIGNATURE 1: the fungus crackle = INFECTION %
fx.put(CT.crackle(lambda t: 2 + 38 * infection(t) ** 1.3, B["INFECT"], B["LEAVE"], seed=3, pitch_fn=lambda t: 0.5 + 0.5 * infection(t), base=1800), B["INFECT"], 0.4)
for k in range(10):                                                 # a tick per 10% of infection
    fx.put(F.tick(2200 + 120 * k, 1.0), B["INFECT"] + (k + 1) * (B["LEAVE"] - B["INFECT"]) / 10, 0.4)
fx.put(osfx.lib("whoosh-cinematic"), B["XRAY"] - 0.2, 0.6)

# ---------------------------------------------------------------- SIGNATURE 2: footsteps whose pitch = HEIGHT
t = B["LEAVE"]
while t < B["NOON"] - 0.2:
    h = 0 if t < B["CLIMB"] else 25 * (0.5 - 0.5 * np.cos(np.pi * min(1, (t - B["CLIMB"]) / (B["NOON"] - B["CLIMB"] - 0.2))))
    fx.put(F.tick(1400 + 120 * h, 0.9), t, 0.35)
    fx.put(CT.square(220 * 2 ** (h / 12), 0.05, 0.25), t, 0.06)
    t += 0.2
for c in range(5, 26, 5):                                          # every 5 cm: a blip
    tc = B["CLIMB"] + (B["NOON"] - B["CLIMB"] - 0.2) * np.arccos(1 - 2 * c / 25) / np.pi
    fx.put(osfx.sfxr("blipSelect", seed=c), tc, 0.35)

# ---------------------------------------------------------------- noon: clock ticks, break, CHOMP
for k in range(int((B["BREAK"] - B["NOON"]) / 0.25)):
    fx.put(F.tick(3200 if k % 2 else 2600, 1.0), B["NOON"] + k * 0.25, 0.55)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(880, 1.2)), B["BREAK"] - 0.35, 0.4)
fx.put(sweep(B["HIT"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.5)
fx.put(osfx.sound("oga/creatures/eat_03", thump(220, 0.1, 2.0)), B["HIT"], 1.0)
fx.put(impact(1.0), B["HIT"], 0.9)
fx.put(osfx.sound("oga/100-sfx/slam_03", impact(0.8)), B["HIT"], 0.6)

# ---------------------------------------------------------------- the heartbeat slows and stops at death
hb, gap = B["HIT"] + 0.3, 0.42
while hb < B["DEATH"] + 0.6:
    fx.put(heartbeat(), hb, 0.8)
    hb += gap
    gap *= 1.35
fx.put(CT.tone_glide(880, 878, 1.4, "sine", 0.5, 0.25), B["DEATH"] + 0.7, 0.4)     # flatline
fx.put(CT.womp(262, 3, 0.3), B["DEATH"] + 0.2, 0.25)

# ---------------------------------------------------------------- the stalk grows (rising creak), spores puff out
fx.put(F.creak(B["SPORES"] - B["STALK"], 90, seed=13) * np.linspace(0.3, 1, int((B["SPORES"] - B["STALK"]) * SR)), B["STALK"], 0.45)
fx.put(riser(B["SPORES"] - B["STALK"], 120, 900), B["STALK"], 0.35)
for k in range(10):
    fx.put(F.poof(113 + k) if hasattr(F, "poof") else noise_hit(0.2, 400, 3000), B["SPORES"] + k * 0.18, 0.35, (k % 3 - 1) * 0.6)
fx.put(osfx.lib("sparkle"), B["SPORES"] + 0.1, 0.4)
fx.put(braam(1.6, 48), B["AGAIN"], 0.45)

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.15)
for tc in (B["XRAY"], B["LEAVE"], B["AGAIN"] - 0.3):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.5)
    fx.put(impact(0.5), tc, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 96, 96, "kb")], gain=0.45, crescendo=(0.8, 0.8))
amb.x += (0.3 * F.drone(DUR, 55, seed=7) * seg(B["REWIND"] + 0.1, DUR, 0.2))[:, None]

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=7.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
