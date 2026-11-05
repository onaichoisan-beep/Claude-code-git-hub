"""Sound for "Your fingers wrinkle on purpose": text cards + open-source sound (NO narration).

SIGNATURE sound = the PRUNE: a soft squeaky "wrinkle" crinkle for every new wrinkle line on the fingertip (WRINKLES
counter), slow in the bath and speeding up; a nerve "zap" when the nerve signal fires, a dead "click" when the nerve is
cut (no wrinkles), then rain + a grip squeak test (dry vs wrinkled). Bath water ambience, 8-bit bed, card blips,
tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 29.2
B = dict(SOAK=2.0, ONLY=4.0, TIME=6.0, WHY=8.0, NERVE=10.0, BREAK=11.75, HIT=12.0, CUT=14.0, TEST=16.0, THEORY=18.0,
         GRIP=20.0, MIXED=22.0, TYRES=24.0, CTA=26.0, STOP=27.9, REWIND=28.7)
CARDS = [
    (0.10, 1.90, "THIS ISN'T WATER|SOAKING *IN*"),
    (2.00, 3.90, "WE ALL THOUGHT|SKIN *SWELLS*..."),
    (4.00, 5.90, "BUT ONLY FINGERS|AND *TOES* DO IT"),
    (6.00, 7.90, "AND IT TAKES|ABOUT *5 MINUTES*"),
    (8.00, 9.90, "SO WHAT'S|*REALLY* GOING ON?"),
    (10.00, 11.70, "YOUR *NERVES*|SEND A SIGNAL..."),
    (12.00, 13.90, "...VESSELS|*SHRINK* ON CUE"),
    (14.00, 15.90, "CUT THE NERVE?|*NO WRINKLES*"),
    (16.00, 17.90, "DOCTORS USED IT|AS A *NERVE TEST*"),
    (18.00, 19.90, "BUT *WHY*?|ONE THEORY..."),
    (20.00, 21.90, "*RAIN TREADS*|FOR GRIP"),
    (22.00, 23.90, "(STUDIES ARE|STILL *MIXED*)"),
    (24.00, 25.90, "YOUR FINGERS|HAVE *TYRES*"),
    (26.00, 27.80, "TAG SOMEONE IN|THE *BATH* NOW"),
]
W, t = [], 0.3
while t < B["WHY"]:
    W.append(round(t, 3))
    t += 1 / (1.5 + 3.5 * (t / B["WHY"]) ** 1.5)
B["WRINKS"] = W

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec
fx.x += CT.bed([
    S(0.0, B["NERVE"], 104, 112, "kbh"),
    S(B["NERVE"], B["BREAK"], 120, 132, "kbhsa"),
    S(B["HIT"] + 0.1, B["THEORY"], 116, 116, "kbha"),
    S(B["THEORY"], B["STOP"] + 0.2, 120, 120, "kbhal"),
], gain=0.46, crescendo=(0.8, 1.15))
amb.x += (0.2 * F.sea(DUR, swell=3.0, seed=4) * (seg(0, B["NERVE"], 0.4) + seg(B["CTA"], DUR, 0.4)))[:, None]
for k, wt in enumerate(W):
    fx.put(CT.tone_glide(1400 + 60 * (k % 6), 900, 0.09, "square", 0.25, 0.5), wt, 0.08)
    fx.put(noise_hit(0.07, 2000, 7000), wt, 0.2, ((k % 3) - 1) * 0.4)
    fx.put(F.tick(2400 + 40 * k, 0.8), wt + 0.02, 0.15)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(osfx.sound("oga/water-splash/splash_02", F.splash(0.5, 2)), 0.1, 0.35)
for c in [B["SOAK"], B["ONLY"], B["TIME"], B["WHY"], B["NERVE"], B["CUT"], B["TEST"], B["THEORY"], B["GRIP"], B["MIXED"], B["TYRES"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(CT.womp(392, 3, 0.22), B["WHY"] + 0.4, 0.15)
for k in range(6):
    fx.put(osfx.sound("oga/retro-synth/synth_laser_0" + str(1 + k % 8), sweep(0.12, 2400, 1200)), B["NERVE"] + 0.3 + k * 0.22, 0.2)
fx.put(riser(B["BREAK"] - B["NERVE"], 200, 1800), B["NERVE"], 0.25)
fx.put(impact(0.9), B["HIT"], 0.6)
fx.put(osfx.sound("oga/100-sfx/tools_02", F.tick(1200, 1.0)), B["CUT"] + 0.4, 0.5)
fx.put(CT.square(110, 0.4, 0.5), B["CUT"] + 0.9, 0.15)
fx.put(osfx.sound("oga/scifi/beep_02", blip(1500)), B["TEST"] + 0.5, 0.3)
fx.put(osfx.sound("oga/water-splash/loop_rain", F.boil(2.0)), B["GRIP"], 0.35)
for k in range(3):
    fx.put(CT.tone_glide(900, 1800, 0.15, "square", 0.4, 0.5), B["GRIP"] + 0.6 + k * 0.4, 0.1)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["TYRES"] + 0.4, 0.3)
fx.put(osfx.sound("oga/water-splash/splash_05", F.splash(0.6, 3)), B["CTA"] + 0.4, 0.4)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 104, 104, "kbh")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)
master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.6)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(W), "wrinkles; DUR", DUR)
