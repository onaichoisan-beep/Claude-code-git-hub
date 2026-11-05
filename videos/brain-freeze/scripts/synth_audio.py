"""Sound for "Your brain isn't freezing" (brain freeze): text cards + open-source sound (NO narration).

SIGNATURE sound = the FREEZE ZAP: an icy crackle + a rising electric whine that follows the PAIN % counter (0 -> 100),
then cuts on the fix (tongue on the roof of the mouth) with a warm "aah" chord as PAIN drops to 0. Slurps and crunches
for the ice cream, a heartbeat thump for the blood vessels widening, 8-bit bed, card blips, tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(NOT=2.0, COLD=4.0, VESSEL=6.0, NERVE=8.0, WRONG=10.0, BREAK=11.75, HIT=12.0, MYTH=14.0, NAME=16.0, FIX=18.0,
         TONGUE=20.0, WARM=22.0, GONE=24.0, CTA=26.0, STOP=27.9, REWIND=28.7)
CARDS = [
    (0.10, 1.90, "*OWW!* MY HEAD!"),
    (2.00, 3.90, "BUT YOUR BRAIN|ISN'T *FREEZING*"),
    (4.00, 5.90, "COLD HITS YOUR|MOUTH'S *ROOF*"),
    (6.00, 7.90, "BLOOD VESSELS|THERE *WIDEN* FAST"),
    (8.00, 9.90, "A NERVE SENDS|A *PAIN* SIGNAL..."),
    (10.00, 11.70, "...BUT THE BRAIN|GETS THE *SPOT*..."),
    (12.00, 13.90, "*WRONG*!"),
    (14.00, 15.90, "IT FEELS IT|IN YOUR *FOREHEAD*"),
    (16.00, 17.90, "DOCTORS CALL IT|*REFERRED PAIN*"),
    (18.00, 19.90, "THE *5-SECOND*|FIX:"),
    (20.00, 21.90, "PUSH YOUR *TONGUE*|TO THE ROOF"),
    (22.00, 23.90, "IT *WARMS* IT|BACK UP"),
    (24.00, 25.90, "PAIN: *GONE*."),
    (26.00, 27.80, "*SAVE* THIS|FOR SUMMER"),
]
os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec
fx.x += CT.bed([
    S(0.0, B["NOT"], 112, 112, "kbh"),
    S(B["NOT"], B["BREAK"], 112, 132, "kbha"),
    S(B["HIT"] + 0.1, B["FIX"], 120, 120, "kbhs"),
    S(B["FIX"], B["STOP"] + 0.2, 116, 116, "kbhal"),
], gain=0.46, crescendo=(0.8, 1.15))


def zap(t0, t1, g=1.0):
    n = int((t1 - t0) * SR)
    tt = np.arange(n) / SR
    f = 300 + 1500 * (tt / (t1 - t0)) ** 1.5
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 + np.random.default_rng(int(t0)).standard_normal(n) * 0.15
    fx.put(band(x, 300, 6000) * np.minimum(1, tt / 0.2), t0, 0.12 * g)
    k = 0
    while t0 + k * 0.2 < t1:
        fx.put(F.ice_crack(seed=k + int(t0), big=0.25 + 0.03 * k), t0 + k * 0.2, 0.3 * g, ((k % 3) - 1) * 0.4)
        k += 1


fx.put(osfx.sound("oga/creatures/eat_01", thump(300, 0.08, 1.5)), 0.1, 0.4)
zap(0.2, 1.9, 1.2)
fx.put(osfx.sound("oga/creatures/hurt_01", sweep(0.4, 700, 300)), 0.5, 0.45)
for c in [B["NOT"], B["COLD"], B["VESSEL"], B["NERVE"], B["WRONG"], B["MYTH"], B["NAME"], B["FIX"], B["TONGUE"], B["WARM"], B["GONE"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(osfx.sound("oga/water-splash/slime_02", F.splash(0.3, 3)), B["COLD"] + 0.3, 0.4)
fx.put(F.ice_crack(seed=4, big=0.6), B["COLD"] + 0.8, 0.45)
for k in range(4):
    fx.put(heartbeat(), B["VESSEL"] + 0.3 + k * 0.4, 0.45)
zap(B["NERVE"] + 0.2, B["BREAK"], 1.0)
fx.put(riser(B["BREAK"] - B["NERVE"], 200, 1800), B["NERVE"], 0.2)
fx.put(impact(1.0), B["HIT"], 0.7)
fx.put(osfx.sound("oga/retro-synth/retro_die_03", CT.womp(392, 3, 0.2)), B["HIT"] + 0.2, 0.35)
zap(B["MYTH"] + 0.2, B["FIX"] - 0.2, 0.7)
fx.put(osfx.sound("oga/scifi/terminal_06", blip(1300)), B["NAME"] + 0.4, 0.3)
fx.put(osfx.sound("oga/retro-synth/power_up_06", F.harp_up()), B["FIX"] + 0.3, 0.3)
fx.put(osfx.sound("oga/water-splash/slime_05", F.splash(0.25, 2)), B["TONGUE"] + 0.4, 0.4)
fx.put(F.pad(2.0, [261.63, 329.63, 392.0], seed=3), B["WARM"] + 0.2, 0.3)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(1046, 1.2)), B["GONE"] + 0.2, 0.3)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.4, 400, 600)), B["GONE"] + 0.4, 0.3)
fx.put(osfx.sound("oga/creatures/eat_02", thump(300, 0.08, 1.5)), B["CTA"] + 0.5, 0.35)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 112, 112, "kbh")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)
master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
