"""Sound for "The Heart That Beats 20 Times a Second" (hummingbird) — no narration, text cards + sound (STYLE_GUIDE.md s.6).

Signature sound: THE HEARTBEAT, at exactly the BPM on the counter (bpm() below is mirrored in index.html). At 1,200 BPM the
beats blur into a buzz; at night they slow to single deep thumps 1.2 s apart; at sunrise they speed back up into the buzz.
A wing hum under the hovering, a pop per flower, a slow human lub-dub in the split screen; tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.4
B = dict(VS=2.4, WINGS=5.2, FLOWERS=8.0, NIGHT=11.0, TORPOR=13.6, LOW=16.1, DEAD=18.6, BREAK=21.25, HIT=21.5, BACK=23.5,
         CTA=25.0, STOP=28.0, REWIND=28.8)

# max 16 characters a line, max 2 lines (safe zone, STYLE_GUIDE.md section 8)
CARDS = [
    (0.10, 2.30, "ITS HEART BEATS|*20* TIMES A SEC"),
    (2.40, 5.10, "YOURS? ABOUT|*70* A MINUTE"),
    (5.20, 7.90, "*53* WING FLAPS|EVERY SECOND"),
    (8.00, 10.90, "*1,000+* FLOWERS|EVERY DAY"),
    (11.00, 13.50, "NIGHT: NO FOOD|= *DANGER*"),
    (13.60, 16.00, "SO IT GOES INTO|*TORPOR*"),
    (16.10, 18.50, "BODY DROPS TO|AS LOW AS *3°C*"),
    (18.60, 21.10, "IS IT...|*DEAD*?"),
    (21.50, 23.40, "NOPE.|*REBOOTING*"),
    (23.50, 24.90, "BACK TO|*1,200* BPM"),
    (25.00, 27.90, "SEND TO A|*NO CHILL* FRIEND"),
]


def bpm(t):
    """the counter. Must match bpm() in index.html."""
    if t < B["NIGHT"]:
        return 1200.0
    if t < B["TORPOR"]:
        return 1200.0 - 300.0 * (t - B["NIGHT"]) / (B["TORPOR"] - B["NIGHT"])
    if t < B["HIT"]:
        u = min(1.0, (t - B["TORPOR"]) / 3.2)
        return 50.0 + 850.0 * (1 - u) ** 2.2
    if t < B["BACK"]:
        u = min(1.0, (t - B["HIT"]) / (B["BACK"] - B["HIT"]))
        return 50.0 * (1200.0 / 50.0) ** (u ** 1.3)
    return 1200.0


os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the 8-bit bed: tight -> slows into the night -> slams back
fx.x += CT.bed([
    S(0.0, B["NIGHT"], 132, 136, "kbha"),
    S(B["NIGHT"], B["TORPOR"], 120, 96, "kbh"),
    S(B["TORPOR"], B["BREAK"], 80, 72, "o"),
    S(B["HIT"] + 0.1, B["CTA"], 120, 136, "kbhsa"),
    S(B["CTA"], B["STOP"] + 0.2, 136, 136, "kbhsal"),
], gain=0.36, crescendo=(0.8, 1.2))
amb.x += (0.22 * F.drone(DUR, 62, seed=8))[:, None]

# ---------------------------------------------------------------- SIGNATURE: the bird's heartbeat at bpm(t)
t = 0.05
while t < B["STOP"] + 0.3:
    if B["VS"] <= t < B["WINGS"]:
        pan = 0.45
    else:
        pan = 0.0
    r = bpm(t)
    gap = 60.0 / r
    slow = r < 300
    if slow:                                              # night: a deep lub-dub you can count
        fx.put(heartbeat(), t, 0.95, pan)
    else:                                                 # day: short bright thumps that blur into a buzz
        d = min(0.09, gap * 0.85)
        fx.put(add(thump(150, d, 1.4), 0.3 * thump(320, d * 0.6, 0.8)), t, 0.38, pan)
    t += gap
fx.put(sweep(0.4, 900, 120) * 0.25, B["TORPOR"] + 0.2, 0.3)

# the human heart in the split screen: 70 BPM, panned left
t = B["VS"] + 0.2
while t < B["WINGS"] - 0.1:
    fx.put(heartbeat(), t, 0.9, -0.45)
    t += 60.0 / 70.0

# ---------------------------------------------------------------- wing hum (53 flaps/s) while hovering
for a, b, g0 in ((0.0, B["NIGHT"] + 0.6, 0.18), (B["HIT"] + 1.2, B["STOP"] + 0.2, 0.16)):
    fx.put(CT.buzz(a, b, lambda x: 106.0, lambda x: 1.0, voices=3, seed=5, harmonics=5), a, g0)
fx.put(CT.buzz(B["WINGS"], B["FLOWERS"], lambda x: 106.0, lambda x: 1.0, voices=4, seed=6, harmonics=7), B["WINGS"], 0.22)

# ---------------------------------------------------------------- flowers: a pop + sip per flower, speeding up
ft = [B["FLOWERS"] + 0.3 + k * (0.75 * 0.86 ** k) for k in range(9)]
for k, tf in enumerate(ft):
    if tf < B["NIGHT"] - 0.1:
        fx.put(osfx.lib("pop"), tf, 0.35, (k % 3 - 1) * 0.5)
        fx.put(CT.square(988 * 2 ** (k / 12), 0.04, 0.25), tf + 0.03, 0.12)
fx.put(osfx.lib("whoosh"), B["FLOWERS"] + 0.1, 0.35)

# ---------------------------------------------------------------- night falls, energy drains, frost
fx.put(CT.womp(392, 4, 0.3), B["NIGHT"] + 0.6, 0.25)
fx.put(F.crickets(B["HIT"] - B["NIGHT"] - 0.3), B["NIGHT"] + 0.3, 0.12)
for k in range(5):
    fx.put(F.ice_crack(60 + k, 0.4), B["LOW"] + 0.2 + k * 0.45, 0.2, (k % 3 - 1) * 0.6)
fx.put(F.sparkle(1.4, 67), B["LOW"] + 0.3, 0.25)

# ---------------------------------------------------------------- the bug pokes it
for k in range(3):
    fx.put(F.tick(2600, 0.6), B["DEAD"] + 0.8 + k * 0.35, 0.3)
fx.put(CT.tone_glide(700, 1100, 0.2, "square", 0.5, 0.3), B["DEAD"] + 1.9, 0.2)

# ---------------------------------------------------------------- sunrise: break -> hit -> heart reboots
fx.put(riser(B["HIT"] - B["DEAD"] - 0.6, 150, 1800), B["DEAD"] + 0.6, 0.22)
fx.put(impact(1.0), B["HIT"], 0.7)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["HIT"] + 0.1, 0.45)
fx.put(F.chirp(19), B["HIT"] + 0.8, 0.35)
fx.put(F.chirp(23), B["HIT"] + 1.4, 0.3, 0.4)
for i, f0 in enumerate([523.25, 659.25, 783.99, 1046.5]):
    fx.put(bell(f0, 1.2), B["BACK"] + i * 0.07, 0.22)

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.14)
for tc in (B["VS"], B["WINGS"], B["FLOWERS"], B["NIGHT"], B["TORPOR"], B["CTA"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.4)
    fx.put(impact(0.4), tc, 0.22)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 132, 132, "kbha")], gain=0.36, crescendo=(0.8, 0.8))
t = B["REWIND"] + 0.15
while t < DUR:
    fx.put(thump(150, 0.04, 1.4), t, 0.38)
    t += 0.05

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=4.5)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
