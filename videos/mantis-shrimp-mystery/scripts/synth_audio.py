"""Narration + sound for "Who keeps breaking my aquarium?" (mantis shrimp mystery; story mode, STYLE_GUIDE 7 + 9).

Voice: Kokoro af_heart, natural pauses. SIGNATURE sound = the CLICK: the mantis shrimp's punch, a dry crack + a tiny
cavitation pop. Heard alone in the dark first (the mystery), then with the reveal it comes in fast bursts (PUNCH km/h
counter), and once more at the very end. Suspect stamps, a glass crack on the turn, aquarium hum + bubbles, a light
switch, a low 8-bit detective bed, tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import narrate as NR  # noqa: E402

GAPS = {1: 0.3, 2: 0.2, 3: 0.3, 4: 1.0, 5: 0.25, 6: 0.25, 7: 0.25, 8: 0.4, 9: 0.3, 10: 0.5, 11: 0.3, 12: 0.2, 13: 0.2,
        14: 0.4, 15: 0.25, 16: 0.3, 17: 0.3, 18: 0.4, 19: 0.45}
S = NR.Story(ROOT, gaps=GAPS, gold={"breaking", "smashed.", "cracked", "sound.", "suspects.", "eel.", "octopus.",
                                    "pufferfish.", "glass", "mantis", "shrimp.", "eighty", "bubbles.", "sixteen", "three.",
                                    "wrong.", "worse", "punch.", "click."}, red={"smashed.", "cracked", "wrong."})
A, W, E, Bn = S.A, S.W, S.E, S.B
B = dict(CRAB=A(1), SHELL=A(2), NIGHT=A(3), LIST=A(4), EEL=A(5), OCTO=A(6), PUFF=A(7), CRACK=A(8), LIGHT=A(9), NAME=A(10),
         PUNCH=A(11), BUBBLE=A(12), GLASS=A(13), EYES=A(14), RIGHT=A(15), WRONG=A(16), NEED=A(17), TANK=A(18), CLICK=A(19))
B["HIT"] = W(9, "there")
B["BREAK"] = B["HIT"] - 0.25
B["CLICKS"] = [Bn(3) + 0.25, Bn(3) + 0.6, W(8, "glass") + 0.4] + [round(W(11, "punches") + k * 0.33, 3) for k in range(5)] + [Bn(19) + 0.35]
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
    Sec(0.0, B["NIGHT"], 96, 96, "kbo"),
    Sec(B["LIST"], B["CRACK"], 108, 108, "kbhl"),
    Sec(B["HIT"] + 0.2, B["EYES"], 124, 124, "kbhsa"),
    Sec(B["EYES"], B["TANK"], 112, 112, "kbha"),
    Sec(B["TANK"], B["CLICK"], 90, 90, "kbo"),
], gain=0.4, crescendo=(0.8, 1.1))
amb.x += (0.14 * F.drone(DUR, 60, seed=3))[:, None]
for k in range(int(DUR / 1.4)):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.4, 700)), 0.3 + k * 1.4, 0.1, (k % 3 - 1) * 0.6)


def click(t, g=1.0):
    fx.put(noise_hit(0.03, 2500, 12000), t, 0.9 * g)
    fx.put(F.tick(4800, 1.0), t, 0.6 * g)
    fx.put(thump(120, 0.08, 3.0), t, 0.45 * g)
    fx.put(osfx.sound("oga/water-splash/bubble_01", F.bubble_(0.3, 1500)), t + 0.03, 0.3 * g)


for c in B["CLICKS"]:
    click(c, 1.2 if c >= B["PUNCH"] else 1.0)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(F.ice_crack(seed=2, big=0.6), 0.25, 0.4)
fx.put(osfx.sound("oga/creatures/eat_03", F.ice_crack(seed=4, big=0.4)), W(1, "smashed.") , 0.5)
for k in range(3):
    fx.put(F.ice_crack(seed=8 + k, big=0.25), W(2, "cracked") + k * 0.2, 0.35)
fx.put(sub_drop(0.6), B["NIGHT"], 0.3)
# suspects: a stamp each, then a "no" buzz
for i in (5, 6, 7):
    fx.put(osfx.sound("oga/100-sfx/slam_0" + str(i - 3), impact(0.5)), A(i), 0.4)
    fx.put(CT.square(110, 0.2, 0.5), Bn(i) - 0.2, 0.15)
fx.put(osfx.sound("oga/creatures/snore", thump(100, 0.3, 1.5)), W(7, "asleep"), 0.3)
# the crack + the light
fx.put(F.ice_crack(seed=21, big=1.2), W(8, "glass") + 0.35, 0.7)
fx.put(osfx.sound("oga/100-sfx/glass_03", F.glass_smash(5)), W(8, "cracked.") + 0.05, 0.4)
fx.put(riser(B["BREAK"] - B["CRACK"], 200, 1600), B["CRACK"], 0.25)
fx.put(osfx.sound("oga/100-sfx/switch_02", F.tick(1500, 1.0)), W(9, "light."), 0.5)
fx.put(impact(1.0), B["HIT"], 0.7)
fx.put(braam(1.5, 52), B["HIT"], 0.35)
# punch counter ticks + the bubble burst
for k in range(16):
    fx.put(F.tick(2000 + 120 * k, 0.9), W(11, "eighty") + k * 0.05, 0.2)
for k in range(10):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.3, 1200 + 80 * k)), W(12, "bursts") + k * 0.06, 0.25)
fx.put(F.ice_crack(seed=30, big=0.6), B["GLASS"] + 0.3, 0.4)
# eyes: sensors pop up one by one (16 vs 3)
for k in range(16):
    fx.put(CT.square(660 + 50 * k, 0.04, 0.25), W(14, "sixteen") + k * 0.06, 0.1)
fx.put(osfx.sound("oga/retro-synth/power_up_05", F.harp_up()), B["RIGHT"] + 0.3, 0.25)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(392, 4, 0.2)), B["WRONG"], 0.35)
fx.put(osfx.sound("oga/100-sfx/wooden_01", thump(150, 0.15, 2)), B["TANK"] + 1.4, 0.4)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
S.mix(fx, amb, master, write_wav, band, reverb, B, SR, N)
