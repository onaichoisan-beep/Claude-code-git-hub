"""Narration + sound for "This beetle navigates by the galaxy" (dung beetle + the Milky Way; story mode, STYLE 7 + 9).

Voice: Kokoro af_heart. SIGNATURE sound = the ROLL: a crunchy rolling scrape + tiny leg ticks while the ball moves
(steady when straight, wobbling + a sad womp when lost in circles), a twinkle when the stars switch on, a sparkle swell
for the Milky Way, a projector click for the planetarium, a hat "pop" for the caps. Night crickets, soft 8-bit bed,
tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import narrate as NR  # noqa: E402

GAPS = {1: 0.2, 2: 0.35, 3: 0.2, 4: 0.3, 5: 0.35, 6: 0.2, 7: 0.35, 8: 0.25, 9: 0.3, 10: 0.4, 11: 0.3, 12: 0.25, 13: 0.35,
        14: 0.2, 15: 0.4, 16: 0.25, 17: 0.4, 18: 0.25, 19: 0.3}
S = NR.Story(ROOT, gaps=GAPS, gold={"milky", "way.", "poop.", "straight", "steal", "dance.", "picture", "sun.", "night.",
                                    "dark?", "planetarium.", "circles.", "stripe.", "again.", "hats.", "lost.", "galaxy",
                                    "first"}, red={"steal", "lost.", "circles."})
A, W, E, Bn = S.A, S.W, S.E, S.B
B = dict(POOP=A(1), AFRICA=A(2), STEAL=A(3), TRICK=A(4), DANCE=A(5), PICTURE=A(6), SUN=A(7), NIGHT=A(8), HOW=A(9),
         PLANET=A(10), ON=A(11), OFF=A(12), MILKY=A(13), AGAIN=A(14), HATS=A(15), HATSON=A(16), BRAIN=A(17), FIRST=A(18),
         END=A(19))
B["HIT"] = W(13, "milky")
B["BREAK"] = B["HIT"] - 0.25
B["LOST"] = W(16, "lost.")
B["OFFHAT"] = W(16, "off,")
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
    Sec(0.0, B["AFRICA"], 96, 96, "kbo"),
    Sec(B["AFRICA"], B["NIGHT"], 116, 116, "kbha"),
    Sec(B["NIGHT"], B["BREAK"], 100, 104, "kbh"),
    Sec(B["HIT"] + 0.3, B["BRAIN"], 112, 112, "kbhal"),
    Sec(B["BRAIN"], B["STOP"] + 0.2, 120, 120, "kbhsal"),
], gain=0.38, crescendo=(0.8, 1.1))
amb.x += (0.16 * F.crickets(DUR, seed=4) * (seg(0, B["AFRICA"], 0.3) + seg(B["NIGHT"], DUR, 0.3)))[:, None]


def roll(t0, t1, wobble=False, g=1.0):
    n = int((t1 - t0) * SR)
    if n <= 0:
        return
    r = np.random.default_rng(int(t0 * 100))
    x = band(r.standard_normal(n), 200, 2500)
    am = 0.6 + 0.4 * np.sin(2 * np.pi * np.arange(n) / SR * (2.5 if not wobble else 1.2))
    fx.put(x * am * 0.5, t0, 0.22 * g)
    t, k = t0, 0
    while t < t1:
        fx.put(F.tick(3600 + 200 * (k % 3), 0.5), t, 0.12 * g, ((k % 2) - 0.5) * 0.6)
        t += 0.11
        k += 1


roll(0.1, B["POOP"] - 0.1)
roll(B["AFRICA"] + 1.0, B["TRICK"] + 2.5)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(F.sparkle(1.2, seed=2), 0.2, 0.25)
for k in range(3):
    fx.put(osfx.sound("oga/creatures/bug_0" + str(1 + k), blip(1600)), W(3, "steal") + k * 0.25, 0.3, (k - 1) * 0.6)
for k in range(6):
    fx.put(F.tick(2400 + 300 * (k % 2), 1.0), W(5, "dance.") + k * 0.12, 0.25)
fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(5000, 1.0)), W(6, "picture"), 0.45)
fx.put(noise_hit(0.12, 3000, 9000), W(6, "picture") + 0.02, 0.25)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["SUN"] + 0.3, 0.2)
roll(B["SUN"] + 0.4, B["NIGHT"] - 0.1, g=0.8)
fx.put(CT.womp(392, 3, 0.22), B["HOW"] + 0.4, 0.15)
fx.put(osfx.sound("oga/100-sfx/switch_02", F.tick(1500, 1.0)), B["PLANET"] + 0.4, 0.45)
fx.put(F.sparkle(1.0, seed=6), B["ON"], 0.35)
roll(B["ON"] + 0.3, B["OFF"] - 0.1)
fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(1500, 1.0)), B["OFF"], 0.45)
roll(B["OFF"] + 0.3, B["MILKY"] - 0.4, wobble=True)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", CT.womp(330, 3, 0.2)), W(12, "circles.") + 0.3, 0.3)
fx.put(riser(B["BREAK"] - B["MILKY"] + 0.6, 200, 1800), B["MILKY"] - 0.6, 0.2)
fx.put(impact(0.7), B["HIT"], 0.45)
fx.put(F.sparkle(2.0, seed=9, lo=3000, hi=7000), B["HIT"] + 0.05, 0.45)
fx.put(osfx.sound("oga/100-sfx/bell_03", bell(1046, 1.6)), W(13, "stripe."), 0.25)
roll(B["AGAIN"], B["HATS"] - 0.1)
fx.put(osfx.lib("pop"), W(15, "hats.") , 0.45)
roll(B["HATSON"], B["LOST"] + 0.5, wobble=True)
fx.put(osfx.lib("pop"), B["OFFHAT"], 0.4)
roll(B["OFFHAT"] + 0.3, B["BRAIN"] - 0.1)
for k in range(5):
    fx.put(F.tick(2000 + 200 * k, 0.9), W(17, "grain") + k * 0.08, 0.2)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.6)), B["FIRST"] + 0.5, 0.3)
fx.put(osfx.sound("oga/100-sfx/plop_02", thump(140, 0.15, 2)), W(19, "poop."), 0.5)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
S.mix(fx, amb, master, write_wav, band, reverb, B, SR, N)
