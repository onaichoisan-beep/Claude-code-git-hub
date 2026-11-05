"""Narration + sound for "This is not her baby" (the cuckoo chick; story mode, STYLE_GUIDE sections 7 + 9).

Voice: Kokoro af_heart, natural pauses. SIGNATURE sound = the BEGGING: a chick's cheep; one cheep at first, then on
"Listen." the bed drops out and the cuckoo's call swells into a whole nest of cheeps (many overlapping voices) — the
twist is something you HEAR. Egg pushes get a scrape + a drop + a crack, each ticking the EGGS counter down; feeding
trips get a wing flap + a gulp (FOOD TRIPS counter), day/night ticks speed up. Soft 8-bit bed, tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import narrate as NR  # noqa: E402

GAPS = {1: 0.2, 2: 0.35, 3: 0.25, 4: 0.2, 5: 0.3, 6: 0.35, 7: 0.2, 8: 0.25, 9: 0.3, 10: 0.3, 11: 0.5, 12: 0.9, 13: 0.3,
        14: 0.25, 15: 0.3, 16: 0.25, 17: 0.45}
S = NR.Story(ROOT, gaps=GAPS, gold={"eight", "hers.", "four", "five.", "bigger.", "cuckoo", "ten", "first.", "horrible.",
                                    "every", "anyway.", "thing.", "listen.", "whole", "hungry", "four.", "africa."},
             red={"horrible.", "pushes"})
A, W, E, Bn = S.A, S.W, S.E, S.B
B = dict(MEET=A(2), FIVE=A(3), BIG=A(4), CUCKOO=A(5), HATCH=A(6), HORRIBLE=A(7), PUSH=A(8), ONLY=A(9), THING=A(10),
         LISTEN=A(11), CHORUS=A(12), WORKS=A(13), TOOBIG=A(14), FLY=A(15), THANKS=A(16), SPRING=A(17))
B["PUSHES"] = [W(8, "pushes") + 0.3, W(8, "one."), W(8, "by."), W(8, "one.", 1)]
B["BREAK"] = B["LISTEN"] - 0.25
B["HIT"] = W(12, "whole")
B["FEEDS"] = [round(B["ONLY"] + 0.8 + k * 0.55, 3) for k in range(int((B["THING"] - B["ONLY"] - 0.8) / 0.55))]
B["FEEDS"] += [round(B["WORKS"] + 0.2 + k * 0.32, 3) for k in range(int((B["FLY"] - B["WORKS"] - 0.2) / 0.32))]
DUR = S.finalize(B, tail=1.2)

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
Sec = CT.Sec
fx.x += CT.bed([
    Sec(0.0, B["HORRIBLE"], 104, 104, "kbh"),
    Sec(B["HORRIBLE"], B["ONLY"], 92, 92, "kbo"),
    Sec(B["ONLY"], B["BREAK"], 112, 112, "kbha"),
    Sec(B["CHORUS"] + 1.5, B["SPRING"], 120, 124, "kbhal"),
    Sec(B["SPRING"], B["STOP"] + 0.2, 96, 96, "kbo"),
], gain=0.4, crescendo=(0.8, 1.1))
amb.x += (0.12 * F.wind(DUR, 600, 1200, 0.2, seed=8) * seg(0, B["LISTEN"], 0.3))[:, None]


def cheep(t, k, g=1.0, hi=1.0):
    f0 = (3000 + 400 * ((k * 7) % 5)) * hi
    fx.put(CT.tone_glide(f0, f0 * 1.35, 0.07, "square", 0.25, 0.4), t, 0.1 * g, ((k * 3) % 5 - 2) * 0.4)


def feed(t, k):
    fx.put(noise_hit(0.1, 800, 3000), t - 0.15, 0.2)
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(300, 0.08, 1.5)), t, 0.35)
    for j in range(3):
        cheep(t + 0.05 + j * 0.08, k + j, 0.8)


# 0. hook: the giant chick begs, mom feeds
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
for k in range(10):
    cheep(0.2 + k * 0.16, k)
feed(1.5, 0)
# 2-5. nest, eggs, the cuckoo
fx.put(F.chirp(seed=2), B["MEET"] + 0.2, 0.4)
for k in range(4):
    fx.put(osfx.sound("oga/100-sfx/plop_0" + str(1 + k % 2), blip(900 + 120 * k)), W(2, "four") + 0.1 + k * 0.15, 0.3)
fx.put(noise_hit(0.3, 600, 2500), W(2, "flies"), 0.3)
fx.put(osfx.sound("oga/100-sfx/plop_02", blip(700)), B["FIVE"] + 0.6, 0.45)
fx.put(CT.womp(392, 2, 0.2), B["BIG"] + 0.6, 0.14)
fx.put(osfx.lib("whoosh"), B["CUCKOO"] - 0.15, 0.4)
for k in range(10):
    fx.put(F.tick(2400, 0.8), W(5, "ten") + k * 0.1, 0.2)
fx.put(F.cuckoo(seed=1) if hasattr(F, "cuckoo") else add(CT.tone_glide(660, 660, 0.18, "square", 0.5, 0.4), np.concatenate([np.zeros(int(0.22 * SR)), CT.tone_glide(523, 523, 0.25, "square", 0.5, 0.4)])), W(5, "flew"), 0.3)
# 6-8. hatch, horrible, pushes (EGGS counter)
fx.put(osfx.lib("whoosh"), B["HATCH"] - 0.15, 0.4)
fx.put(F.ice_crack(seed=3, big=0.3), W(6, "hatches"), 0.5)
fx.put(sub_drop(0.8), B["HORRIBLE"] + 0.3, 0.45)
fx.put(braam(1.2, 52), W(7, "horrible."), 0.35)
for k, pt in enumerate(B["PUSHES"]):
    fx.put(noise_hit(0.2, 300, 1500), pt - 0.2, 0.3)
    fx.put(sweep(0.25, 900, 200) * 0.5, pt, 0.3)
    fx.put(F.ice_crack(seed=10 + k, big=0.4), pt + 0.28, 0.45)
    fx.put(F.tick(1500 - 150 * k, 1.0), pt, 0.3)
# 9. feeding trips
for k, ft in enumerate(B["FEEDS"]):
    feed(ft, k)
# 10-12. why doesn't she notice? -> "Listen." (silence) -> the chorus
fx.put(riser(B["BREAK"] - B["THING"], 200, 1500), B["THING"], 0.2)
fx.put(impact(0.9), B["HIT"], 0.5)
for k in range(70):
    tt = B["LISTEN"] + 0.7 + k * 0.035
    cheep(tt, k, 0.45 + 0.55 * min(1, k / 25), 0.9 + 0.25 * ((k * 5) % 7) / 7)
# 13-16. day + night, too big, Africa
for k in range(6):
    fx.put(F.tick(2200, 1.0), B["WORKS"] + 0.3 + k * 0.42, 0.25)
fx.put(osfx.sound("oga/100-sfx/wooden_02", thump(160, 0.15, 2)), B["TOOBIG"] + 0.8, 0.4)
fx.put(osfx.lib("whoosh-cinematic"), B["FLY"] + 0.5, 0.5)
for k in range(6):
    fx.put(noise_hit(0.1, 800, 3000), B["FLY"] + 0.6 + k * 0.14, 0.2)
fx.put(CT.womp(330, 3, 0.25), B["THANKS"] + 0.3, 0.16)
# 17. next spring: four eggs ... and a cuckoo calls
for k in range(4):
    fx.put(osfx.sound("oga/100-sfx/plop_0" + str(1 + k % 2), blip(900 + 120 * k)), W(17, "four") + 0.15 + k * 0.15, 0.3)
fx.put(add(CT.tone_glide(660, 660, 0.18, "square", 0.5, 0.4), np.concatenate([np.zeros(int(0.22 * SR)), CT.tone_glide(523, 523, 0.25, "square", 0.5, 0.4)])), Bn(17) + 0.3, 0.3)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
for k in range(8):
    cheep(B["REWIND"] + 0.2 + k * 0.05, k)
S.mix(fx, amb, master, write_wav, band, reverb, B, SR, N)
