"""Narration + sound for "The crows that never forget" (story mode, STYLE_GUIDE sections 7 + 9).

Voice: Kokoro af_heart (scripts/make_voices_kokoro.py), natural pauses, small room.
SIGNATURE sound = the CAW: crow caws whose number follows the SCOLDING % counter (a few at first, a whole mob by
year five), dive-bomb whooshes, wing flaps. A soft 8-bit bed under everything that drops out on "But here's the thing"
and "Then it got weird", a hit on the twist, near-silence + one caw on "They're watching", tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import narrate as NR  # noqa: E402

GAPS = {1: 0.2, 2: 0.35, 3: 0.2, 4: 0.3, 5: 0.25, 6: 0.15, 7: 0.25, 8: 0.35, 9: 0.25, 10: 0.2, 11: 0.3, 12: 0.2,
        13: 0.35, 14: 0.2, 15: 0.15, 16: 0.35, 17: 0.3, 18: 0.4, 19: 0.3}
S = NR.Story(ROOT, gaps=GAPS, gold={"hated", "crow", "mask,", "mask", "seven", "thing.", "remembered", "weird.", "two,",
                                    "five,", "baby", "taught", "face.", "watching."},
             red={"screaming.", "screaming", "screamed", "dangerous"})
A, W, E, Bn = S.A, S.W, S.E, S.B
B = dict(HOOK=A(0), MASK=A(2), TAG=A(3), THING=A(4), WALK=A(5), SCREAM=A(6), SEVEN=A(7), WEIRD=A(8), Y2=A(9), Y5=A(10),
         HOW=A(11), TAUGHT=A(12), TEST=A(13), INNOCENT=A(14), ANYWAY=A(15), FACE=A(16), WITHOUT=A(17), NICE=A(18),
         WATCH=A(19))
B["HIT"] = W(15, "anyway")
B["BREAK"] = B["HIT"] - 0.25
DUR = S.finalize(B, tail=1.0)

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
Sec = CT.Sec
fx.x += CT.bed([
    Sec(0.0, B["THING"], 104, 104, "kbh"),
    Sec(B["THING"] + 0.9, B["WEIRD"], 118, 118, "kbha"),
    Sec(B["WEIRD"] + 0.9, B["BREAK"], 112, 128, "kbhs"),
    Sec(B["HIT"] + 0.2, B["NICE"], 116, 116, "kbhl"),
    Sec(B["NICE"], B["WATCH"], 90, 90, "kbo"),
], gain=0.42, crescendo=(0.8, 1.1))
amb.x += (0.12 * F.wind(DUR, 400, 900, 0.3, seed=4))[:, None]


def caw(t, k, g=1.0):
    fx.put(F.squawk(seed=k), t, 0.45 * g, ((k * 7) % 5 - 2) * 0.35)


def caws(t0, t1, rate, k0, g=1.0):
    t, k = t0, k0
    while t < t1:
        caw(t, k, g)
        k += 1
        t += 1 / rate + 0.07 * ((k * 3) % 4)


# 0. hook: a mob screaming at the masked man
caws(0.05, B["MASK"] - 0.3, 3.0, 1)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
# 2-3. the mask, the net, the tags
fx.put(osfx.lib("whoosh"), B["MASK"] - 0.15, 0.4)
fx.put(osfx.sound("oga/100-sfx/spring_05", thump(120, 0.15, 2)), W(2, "caught"), 0.5)
for k in range(7):
    fx.put(F.tick(2600 + 100 * k, 0.9), W(2, "seven") + 0.1 + k * 0.08, 0.25)
fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(4200, 1.0)), W(3, "tagged"), 0.4)
fx.put(osfx.sound("oga/100-sfx/metal_02", F.tick(3000, 1.0)), W(3, "measured"), 0.35)
for k in range(5):
    fx.put(noise_hit(0.12, 800, 3000), W(3, "go.") + k * 0.09, 0.25, (k % 2) - 0.5)       # wing flaps
# 4. "but here's the thing": the bed drops, a low hit
fx.put(sub_drop(0.9), B["THING"], 0.5)
fx.put(braam(1.0, 55), B["THING"] + 0.05, 0.3)
# 5-6. the attack
fx.put(osfx.lib("whoosh-cinematic"), B["WALK"] - 0.2, 0.45)
caws(W(5, "lost"), B["SEVEN"] - 0.2, 4.0, 20)
for k in range(4):
    fx.put(osfx.lib("whoosh"), W(6, "diving.") + k * 0.35, 0.35, (k % 2) - 0.5)
# 8. "then it got weird"
fx.put(CT.womp(392, 3, 0.25), B["WEIRD"] + 0.2, 0.16)
fx.put(sub_drop(0.8), B["WEIRD"], 0.4)
# 9-10. years: calendar flips + more and more caws
for i in (9, 10):
    fx.put(F.page_flip(i), A(i) - 0.05, 0.45)
    fx.put(impact(0.4), A(i), 0.3)
caws(A(9) + 0.4, B["HOW"] - 0.2, 5.0, 40, 0.8)
fx.put(osfx.sound("oga/creatures/cute_04", blip(1800)), W(10, "baby"), 0.35)
# 11-12. how? the parents teach
fx.put(osfx.sound("oga/creatures/misc_05", blip(700)), B["HOW"] + 0.3, 0.25)
caw(W(12, "point"), 70, 0.8)
caw(W(12, "kids,") , 71, 0.5)
fx.put(riser(B["BREAK"] - B["TEST"], 200, 1800), B["TEST"], 0.25)
# 15. HIT: the innocent person gets screamed at too
fx.put(impact(1.0), B["HIT"], 0.7)
fx.put(braam(1.5, 49), B["HIT"], 0.35)
caws(B["HIT"] + 0.05, B["FACE"] - 0.1, 6.0, 90)
# 16-17. the face; without the mask: silence
fx.put(osfx.lib("whoosh"), B["WITHOUT"] - 0.15, 0.4)
for k in range(6):
    fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_footstep_0" + str(1 + k % 2), F.tick(900, 0.6)), B["WITHOUT"] + 0.2 + k * 0.4, 0.25)
# 18-19. be nice. they're watching (one caw)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["NICE"] + 0.1, 0.2)
caw(B["WATCH"] + 0.85, 120, 1.0)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
caws(B["REWIND"] + 0.1, DUR, 3.0, 130, 0.6)

S.mix(fx, amb, master, write_wav, band, reverb, B, SR, N)
