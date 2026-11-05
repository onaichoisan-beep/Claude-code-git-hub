"""Sound for "There's a hole in your vision" (the blind spot test): text cards + open-source sound only (NO narration).

SIGNATURE sound = the TEST CLOCK: a soft tick every half second while the viewer does the test (closing an eye,
staring at the X, moving the phone closer), rising in pitch as the STEP counter advances; the bed thins out to let
them concentrate, then the 0.25 s break and a "POOF" + sparkle when the dot should vanish. Calm 8-bit bed, card blips,
whooshes, a paint-brush swish when the brain fills the gap, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(PROVE=2.0, CLOSE=4.0, STARE=6.0, MOVE=8.0, KEEP=10.5, BREAK=13.75, HIT=14.0, SPOT=16.0, NERVE=18.0,
         FILL=20.0, BOTH=22.0, FAKE=24.0, CTA=26.0, STOP=27.9, REWIND=28.7)

CARDS = [
    (0.10, 1.90, "THERE'S A *HOLE*|IN YOUR VISION"),
    (2.00, 3.90, "LET'S *PROVE* IT"),
    (4.00, 5.90, "CLOSE YOUR|*LEFT* EYE"),
    (6.00, 7.90, "STARE AT THE *X*|WITH YOUR RIGHT"),
    (8.00, 10.40, "MOVE YOUR PHONE|*CLOSER*... SLOWLY"),
    (10.50, 13.70, "KEEP STARING|AT THE *X*"),
    (14.00, 15.90, "THE DOT|*VANISHED*?"),
    (16.00, 17.90, "THAT'S YOUR|*BLIND SPOT*"),
    (18.00, 19.90, "THE NERVE EXITS|HERE: *NO SENSORS*"),
    (20.00, 21.90, "YOUR BRAIN|*FILLS IT IN*"),
    (22.00, 23.90, "EVERY SECOND.|*BOTH EYES*."),
    (24.00, 25.90, "WHAT ELSE IS|IT *FAKING*?"),
    (26.00, 27.80, "DID THE DOT|*DISAPPEAR*?"),
]
B["TICKS"] = [round(B["CLOSE"] + 0.25 + 0.5 * k, 3) for k in range(int((B["BREAK"] - B["CLOSE"] - 0.3) / 0.5))]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["PROVE"], 96, 96, "kbo"),
    S(B["PROVE"], B["CLOSE"], 112, 112, "kbha"),
    S(B["CLOSE"], B["BREAK"], 90, 90, "kb", 0.6),
    S(B["HIT"] + 0.1, B["FILL"], 116, 116, "kbhal"),
    S(B["FILL"], B["STOP"] + 0.2, 122, 122, "kbhsal"),
], gain=0.42, crescendo=(0.8, 1.15))
amb.x += (0.1 * F.pad(DUR, [220.0, 277.18, 329.63], seed=2) * seg(B["CLOSE"], B["BREAK"], 0.5))[:, None]

# SIGNATURE: the test clock (pitch climbs with the STEP)
for k, tt in enumerate(B["TICKS"]):
    f = 1800 if tt < B["STARE"] else 2200 if tt < B["MOVE"] else 2600 + 15 * k
    fx.put(F.tick(f, 0.9), tt, 0.3, (k % 2) * 0.4 - 0.2)
# frame 1: the eye + the hole
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(sub_drop(0.8), 0.3, 0.35)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.4, 500, 700)), 0.9, 0.35)
for c in [B["PROVE"], B["CLOSE"], B["STARE"], B["MOVE"], B["SPOT"], B["NERVE"], B["FILL"], B["BOTH"], B["FAKE"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(osfx.sound("oga/retro-synth/power_up_05", F.harp_up()), B["PROVE"] + 0.3, 0.25)
fx.put(osfx.sound("oga/100-sfx/switch_02", F.tick(1500, 1.0)), B["CLOSE"] + 0.6, 0.4)      # eye shut "click"
fx.put(osfx.sound("oga/scifi/beep_01", blip(1400)), B["STARE"] + 0.4, 0.25)
fx.put(riser(B["BREAK"] - B["KEEP"], 150, 1200), B["KEEP"], 0.18)
# HIT: poof
fx.put(F.poof(3), B["HIT"], 0.6)
fx.put(F.sparkle(1.2, seed=4), B["HIT"] + 0.05, 0.4)
fx.put(impact(0.6), B["HIT"], 0.45)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.5, 600, 900)), B["HIT"] + 0.6, 0.4)
# explanation
for k in range(6):
    fx.put(CT.square(660 + 110 * k, 0.05, 0.25), B["NERVE"] + 0.3 + k * 0.1, 0.1)
for k in range(5):
    fx.put(noise_hit(0.25, 1500, 5000), B["FILL"] + 0.4 + k * 0.28, 0.2, (k % 2) - 0.5)
fx.put(osfx.sound("oga/retro-synth/retro_coin_02", bell(1318, 0.5)), B["FILL"] + 1.8, 0.25)
fx.put(CT.womp(392, 3, 0.22), B["FAKE"] + 0.5, 0.16)
fx.put(osfx.sound("oga/creatures/weird_04", blip(700)), B["FAKE"] + 1.1, 0.3)
fx.put(osfx.sound("oga/creatures/cute_05", blip(1300)), B["CTA"] + 0.6, 0.3)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 96, 96, "kbo")], gain=0.42, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=6.5)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["TICKS"]), "ticks; DUR", DUR)
