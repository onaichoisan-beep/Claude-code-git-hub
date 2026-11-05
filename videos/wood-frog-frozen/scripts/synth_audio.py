"""Sound for "The frog that freezes solid" (Alaskan wood frog): text cards + open-source sound only (NO narration).

SIGNATURE sound = the HEART MONITOR. A beep + heartbeat thump per beat: steady in autumn, slowing as it freezes,
then the flatline tone (the HIT). Months pass as day-ticks (accelerating with the DAY counter), ice creaks, then in
spring a single beep... beep... that speeds back up to a normal rhythm. 8-bit bed, card blips, whooshes, tape-stop.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 28.4
B = dict(MEET=2.1, WINTER=4.2, SUGAR=6.3, ICE=8.4, BREAK=10.25, HIT=10.5, DAYS=12.6, RECORD=14.7, SPRING=16.8,
         BEAT=18.9, HOP=21.0, SCI=23.1, CTA=25.2, STOP=27.1, REWIND=27.9)

CARDS = [
    (0.10, 2.00, "ITS HEART|HAS *STOPPED*"),
    (2.10, 4.10, "MEET THE|*WOOD FROG*"),
    (4.20, 6.20, "WINTER IS|*COMING*"),
    (6.30, 8.30, "IT FLOODS ITS|CELLS WITH *SUGAR*"),
    (8.40, 10.20, "THEN IT|*FREEZES*"),
    (10.50, 12.50, "NO HEARTBEAT.|NO *BREATH*."),
    (12.60, 14.60, "FOR *MONTHS*"),
    (14.70, 16.70, "UP TO *7 MONTHS*|AT -18°C"),
    (16.80, 18.80, "THEN SPRING|*ARRIVES*"),
    (18.90, 20.90, "THE HEART|*RESTARTS*"),
    (21.00, 23.00, "AND IT HOPS|*AWAY*"),
    (23.10, 25.10, "IT MAY HELP US|*FREEZE ORGANS*"),
    (25.20, 27.00, "TAG SOMEONE|ALWAYS *COLD*"),
]


def beats_between(t0, t1, r0, r1):
    out, t = [], t0
    while t < t1:
        out.append(round(t, 3))
        u = (t - t0) / max(1e-6, t1 - t0)
        t += 1 / (r0 + (r1 - r0) * u)
    return out


# heartbeats shared with the picture (the ECG line): steady -> slowing -> none -> restart and speed up
B["HB"] = beats_between(B["MEET"] + 0.2, B["ICE"], 1.6, 1.4) + beats_between(B["ICE"], B["BREAK"] - 0.2, 1.2, 0.45) \
    + beats_between(B["BEAT"] + 0.3, B["STOP"], 0.6, 1.8)
B["DAYTICKS"] = beats_between(B["DAYS"], B["SPRING"], 2.0, 12.0)

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["MEET"], 84, 84, "kbo"),
    S(B["MEET"], B["WINTER"], 116, 116, "kbha"),
    S(B["WINTER"], B["BREAK"], 112, 96, "kbh"),
    S(B["HIT"] + 0.3, B["SPRING"], 90, 90, "kbo"),
    S(B["SPRING"], B["HOP"], 104, 124, "kbha"),
    S(B["HOP"], B["STOP"] + 0.2, 128, 128, "kbhsal"),
], gain=0.46, crescendo=(0.8, 1.2))
amb.x += (0.3 * F.wind(DUR, 300, 700, 0.5, seed=21) * seg(B["WINTER"], B["SPRING"] + 0.5, 0.5))[:, None]
amb.x += (0.18 * F.crickets(DUR, seed=3) * (seg(B["MEET"], B["WINTER"], 0.3) + seg(B["HOP"], B["REWIND"], 0.3)))[:, None]


def monitor_beep(t, g=1.0):
    fx.put(CT.square(1046.5, 0.09, 0.5), t, 0.16 * g)
    fx.put(heartbeat(), t, 0.5 * g)


# 0. frame 1: the flatline
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
_fl = CT.square(1046.5, 1.9, 0.5)
fx.put(_fl * np.linspace(1, 0.6, len(_fl)), 0.1, 0.08)
fx.put(F.ice_crack(seed=2, big=0.6), 0.6, 0.4)
# heartbeats (the signature)
for k, hb in enumerate(B["HB"]):
    monitor_beep(hb, 1.0 if hb < B["BREAK"] else 0.6 + 0.4 * min(1, (hb - B["BEAT"]) / 3))
# 1. meet: a ribbit + hop
fx.put(osfx.lib("whoosh"), B["MEET"] - 0.15, 0.4)
fx.put(osfx.sound("oga/creatures/burble_02", CT.womp(220, 2, 0.15)), B["MEET"] + 0.5, 0.45)
fx.put(osfx.sound("oga/100-sfx/spring_02", blip(500)), B["MEET"] + 1.2, 0.35)
# 2. winter: wind gust, snow
fx.put(osfx.lib("whoosh-cinematic"), B["WINTER"] - 0.2, 0.45)
fx.put(F.wind(1.5, 600, 1200, 0.9, seed=4), B["WINTER"] + 0.2, 0.4)
fx.put(osfx.sound("oga/creatures/misc_02", sweep(0.3, 500, 300)), B["WINTER"] + 1.2, 0.35)
# 3. sugar: sparkly fills
fx.put(osfx.lib("whoosh"), B["SUGAR"] - 0.15, 0.4)
for k in range(8):
    fx.put(osfx.sound("oga/retro-synth/retro_coin_0" + str(1 + k % 2), blip(1200 + 100 * k)), B["SUGAR"] + 0.3 + k * 0.18, 0.2, (k % 2) - 0.5)
# 4. ice spreads: crackles accelerate
fx.put(osfx.lib("whoosh"), B["ICE"] - 0.15, 0.4)
for k, ct in enumerate(beats_between(B["ICE"] + 0.2, B["BREAK"], 3, 14)):
    fx.put(F.ice_crack(seed=10 + k, big=0.3 + 0.03 * k), ct, 0.3, (k % 3 - 1) * 0.4)
fx.put(riser(B["BREAK"] - B["ICE"], 300, 2000), B["ICE"], 0.2)
# 5. HIT: flatline
fx.put(impact(0.8), B["HIT"], 0.6)
fx.put(F.ice_crack(seed=5, big=1.2), B["HIT"], 0.6)
fx.put(CT.square(1046.5, 2.0, 0.5), B["HIT"], 0.13)
fx.put(sub_drop(1.2), B["HIT"], 0.5)
# 6-7. months pass: day ticks accelerate, snow
fx.put(osfx.lib("whoosh-cinematic"), B["DAYS"] - 0.2, 0.45)
for k, dt in enumerate(B["DAYTICKS"]):
    fx.put(F.tick(2200 + 40 * (k % 20), 0.9), dt, 0.25, (k % 2) * 0.4 - 0.2)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.6)), B["RECORD"] + 1.6, 0.3)
# 8. spring: drips + birds
fx.put(osfx.lib("whoosh"), B["SPRING"] - 0.15, 0.4)
for k in range(9):
    fx.put(osfx.sound("oga/water-splash/bubble_0" + str(1 + k % 3), F.bubble_(0.4, 900)), B["SPRING"] + 0.2 + k * 0.22, 0.3, (k % 3 - 1) * 0.5)
fx.put(F.chirp(seed=3), B["SPRING"] + 0.8, 0.35, 0.4)
fx.put(F.chirp(seed=7), B["SPRING"] + 1.5, 0.3, -0.4)
# 9. restart: first beep is the punch
fx.put(osfx.lib("whoosh"), B["BEAT"] - 0.15, 0.4)
fx.put(impact(0.6), B["BEAT"] + 0.3, 0.4)
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up()), B["BEAT"] + 1.6, 0.3)
# 10. hop away
fx.put(osfx.lib("whoosh"), B["HOP"] - 0.15, 0.4)
for k in range(3):
    fx.put(osfx.sound("oga/100-sfx/spring_0" + str(4 + k), blip(500 + 100 * k)), B["HOP"] + 0.4 + k * 0.5, 0.4)
fx.put(osfx.sound("oga/creatures/burble_01", CT.womp(260, 2, 0.15)), B["HOP"] + 1.6, 0.4)
# 11. science
fx.put(osfx.lib("whoosh"), B["SCI"] - 0.15, 0.4)
fx.put(osfx.sound("oga/scifi/beep_01", blip(1500)), B["SCI"] + 0.4, 0.3)
fx.put(osfx.sound("oga/scifi/terminal_02", blip(1300)), B["SCI"] + 1.0, 0.3)
# 12. CTA
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.4)
fx.put(F.wind(1.2, 500, 1000, 0.8, seed=9), B["CTA"] + 0.6, 0.3)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 84, 84, "kbo")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["HB"]), "heartbeats;", len(B["DAYTICKS"]), "day ticks; DUR", DUR)
