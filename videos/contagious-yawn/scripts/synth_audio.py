"""Sound for "You'll yawn before this ends" (contagious yawning): text cards + open-source sound only (NO narration).

SIGNATURE sound = the YAWN: a synthesized "aaaah" (a buzzy glottal tone gliding up then down through vowel formants,
plus breath noise). Every yawn on screen gets one, and the YAWNS counter ticks with it; in the chain section they come
faster and overlap (one person sets off the next). 8-bit lullaby-ish bed, card blips, whooshes, tape-stop + rewind.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 27.2
B = dict(SEE=2.0, CHAIN=4.0, HALF=6.0, READ=8.0, THINK=10.0, BREAK=11.75, HIT=12.0, FRIEND=14.0, WHY=16.0,
         COOL=18.0, KIDS=20.0, YOU=22.0, CTA=24.0, STOP=25.9, REWIND=26.7)

CARDS = [
    (0.10, 1.90, "DON'T *YAWN*."),
    (2.00, 3.90, "SEEING ONE...|*SPREADS* IT"),
    (4.00, 5.90, "IT'S *CONTAGIOUS*"),
    (6.00, 7.90, "ABOUT *HALF* OF|ADULTS CATCH IT"),
    (8.00, 9.90, "EVEN *READING*|ABOUT IT"),
    (10.00, 11.70, "EVEN *THINKING*|ABOUT IT"),
    (12.00, 13.90, "DOGS CATCH|*OUR* YAWNS"),
    (14.00, 15.90, "CLOSE FRIENDS|CATCH IT *MORE*"),
    (16.00, 17.90, "WHY? NOBODY|KNOWS *FOR SURE*"),
    (18.00, 19.90, "ONE IDEA: IT|*COOLS* THE BRAIN"),
    (20.00, 21.90, "KIDS UNDER ~4|*DON'T* CATCH IT"),
    (22.00, 23.90, "SO... DID YOU|*YAWN*?"),
    (24.00, 25.80, "COMMENT IF|YOU *YAWNED*"),
]
# every yawn on screen (shared with the picture): time, who
Y = [(0.2, "face"), (B["SEE"] + 0.2, "a"), (B["SEE"] + 1.1, "b")]
t = B["CHAIN"] + 0.1
for k in range(4):
    Y.append((round(t, 3), f"c{k}"))
    t += 0.5 - 0.06 * k
Y += [(B["HALF"] + 0.3 + 0.18 * k, f"h{k}") for k in range(5)]
Y += [(B["READ"] + 0.9, "reader"), (B["THINK"] + 0.9, "thinker"), (B["HIT"], "dog"), (B["FRIEND"] + 0.3, "f1"),
      (B["FRIEND"] + 0.9, "f2"), (B["KIDS"] + 0.3, "adult"), (B["YOU"] + 0.6, "face2"), (B["CTA"] + 0.5, "face3")]
B["YAWNS"] = [round(a, 3) for a, _ in Y]
B["WHO"] = [w for _, w in Y]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec


def yawn(d=1.3, f0=150, seed=1):
    """'aaaah': a glottal pulse train gliding up then down, filtered through moving vowel formants + breath"""
    n = int(d * SR)
    tt = np.arange(n) / SR
    u = tt / d
    f = f0 * (1 + 0.6 * np.sin(np.pi * np.minimum(1, u * 1.4)) - 0.25 * u)
    ph = np.cumsum(f / SR)
    src = (2 * (ph % 1) - 1) * 0.6
    rng = np.random.default_rng(seed)
    src += rng.standard_normal(n) * 0.25
    env = np.minimum(1, tt / 0.15) * np.clip((d - tt) / 0.45, 0, 1) ** 1.5
    out = np.zeros(n)
    blk = 1024
    for i in range(0, n, blk):
        uu = (i / n)
        f1 = 500 + 400 * np.sin(np.pi * min(1, uu * 1.3))   # mouth opens: a -> aa
        seg_ = src[i:i + blk]
        X = np.fft.rfft(seg_, blk)
        fr = np.fft.rfftfreq(blk, 1 / SR)
        H = np.exp(-((fr - f1) / 180) ** 2) + 0.6 * np.exp(-((fr - 1200) / 260) ** 2) + 0.15
        out[i:i + blk] = np.fft.irfft(X * H, blk)[:len(seg_)]
    return out * env / (np.max(np.abs(out)) + 1e-9)


fx.x += CT.bed([
    S(0.0, B["SEE"], 84, 84, "kbo"),
    S(B["SEE"], B["READ"], 108, 116, "kbha"),
    S(B["READ"], B["BREAK"], 112, 128, "kbhs"),
    S(B["HIT"] + 0.1, B["YOU"], 118, 118, "kbhal"),
    S(B["YOU"], B["STOP"] + 0.2, 96, 96, "kbhl"),
], gain=0.42, crescendo=(0.8, 1.15))

# SIGNATURE: a yawn for every yawn on screen (pitch by who: kid higher, dog = whine)
for k, (yt, who) in enumerate(Y):
    f0 = 120 + 25 * (k % 4)
    if who == "dog":
        fx.put(CT.tone_glide(700, 1100, 0.5, "square", 0.5, 0.4) * 0.5, yt, 0.18)
        fx.put(osfx.sound("oga/creatures/cute_10", sweep(0.5, 900, 500)), yt + 0.4, 0.4)
        continue
    fx.put(yawn(1.2 if who.startswith("h") else 1.4, f0, seed=k), yt, 0.42 if not who.startswith("h") else 0.25, (k % 3 - 1) * 0.4)
    fx.put(F.tick(1800 + 80 * k, 0.8), yt, 0.2)                     # the YAWNS counter tick
# cuts + scene sounds
for c in [B["SEE"], B["CHAIN"], B["HALF"], B["READ"], B["THINK"], B["FRIEND"], B["WHY"], B["COOL"], B["KIDS"], B["YOU"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
for k in range(4):
    fx.put(osfx.sound("oga/100-sfx/paper_0" + str(1 + k % 4), F.page_flip(k)), B["READ"] + 0.2 + k * 0.15, 0.25)
fx.put(osfx.sound("oga/retro-synth/synth_misc_06", blip(900)), B["THINK"] + 0.3, 0.3)
fx.put(riser(B["BREAK"] - B["THINK"], 200, 1500), B["THINK"], 0.25)
fx.put(impact(0.8), B["HIT"], 0.6)
fx.put(osfx.sound("oga/creatures/barking_02", roar(0.3, 200)), B["HIT"] + 1.1, 0.35)
fx.put(osfx.sound("oga/retro-synth/power_up_01", F.harp_up()), B["FRIEND"] + 1.3, 0.25)
fx.put(CT.womp(392, 3, 0.22), B["WHY"] + 0.4, 0.15)
fx.put(F.wind(1.2, 800, 1400, 0.3, seed=3), B["COOL"] + 0.3, 0.3)
fx.put(osfx.sound("oga/creatures/cute_01", blip(1500)), B["KIDS"] + 1.2, 0.35)
fx.put(osfx.sound("oga/creatures/snore", thump(100, 0.3, 1.5)), B["CTA"] + 1.0, 0.3)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 84, 84, "kbo")], gain=0.42, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(Y), "yawns; DUR", DUR)
