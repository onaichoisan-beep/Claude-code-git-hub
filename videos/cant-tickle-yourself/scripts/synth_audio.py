"""Sound for "Why you can't tickle yourself": text cards + open-source sound only (NO narration).

SIGNATURE sound = the TICKLE: a fast finger-patter "brrrr" (soft ticks) whose rate follows the TICKLE % meter,
with giggles on top when it works and a flat "womp" when it doesn't; the cerebellum's prediction beeps; a big
CANCELLED stamp on the hit; the robot's servo whine and a delay-timer tick. 8-bit bed, card blips, whooshes,
tape-stop + rewind.

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
B = dict(WHY=2.0, FRIEND=4.0, CERE=6.0, PRED=8.0, EXP=10.0, BREAK=11.75, HIT=12.0, SURP=14.0, ROBOT=16.0,
         DELAY=18.0, WORKS=20.0, FOOL=22.0, CTA=24.0, STOP=25.9, REWIND=26.7)

CARDS = [
    (0.10, 1.90, "TRY TICKLING|*YOURSELF*"),
    (2.00, 3.90, "NOTHING. *WHY?*"),
    (4.00, 5.90, "WHEN A FRIEND|DOES IT: *HA!*"),
    (6.00, 7.90, "MEET YOUR|*CEREBELLUM*"),
    (8.00, 9.90, "IT *PREDICTS*|EVERY MOVE"),
    (10.00, 11.70, "YOUR OWN TOUCH?|*EXPECTED*."),
    (12.00, 13.90, "SO IT GETS|*CANCELLED*"),
    (14.00, 15.90, "SURPRISE IS|WHAT *TICKLES*"),
    (16.00, 17.90, "SCIENTISTS USED|A *ROBOT*"),
    (18.00, 19.90, "ADD A *0.2 S*|DELAY..."),
    (20.00, 21.90, "...AND IT|*TICKLES*!"),
    (22.00, 23.90, "THE BRAIN|GOT *FOOLED*"),
    (24.00, 25.80, "TRY IT. FAILED?|*SAME*."),
]
# tickle sessions (shared with the picture): start, end, works?
B["TICKLE"] = [[0.1, 1.9, 0], [B["FRIEND"] + 0.3, B["CERE"] - 0.1, 1], [B["WORKS"] + 0.1, B["FOOL"] - 0.1, 1], [B["CTA"] + 0.2, B["STOP"], 0]]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["WHY"], 100, 100, "kbh"),
    S(B["WHY"], B["FRIEND"], 92, 92, "kbo"),
    S(B["FRIEND"], B["CERE"], 132, 132, "kbhsal"),
    S(B["CERE"], B["BREAK"], 112, 124, "kbha"),
    S(B["HIT"] + 0.1, B["ROBOT"], 116, 116, "kbhl"),
    S(B["ROBOT"], B["WORKS"], 110, 110, "kbh"),
    S(B["WORKS"], B["FOOL"], 134, 134, "kbhsal"),
    S(B["FOOL"], B["STOP"] + 0.2, 116, 116, "kbha"),
], gain=0.44, crescendo=(0.8, 1.15))


def giggle(t, k, g=1.0):
    for j in range(4):
        fx.put(CT.tone_glide(900 + 120 * ((j + k) % 3), 1300 + 120 * ((j + k) % 3), 0.07, "square", 0.25, 0.5), t + j * 0.11, 0.13 * g, (j % 2) - 0.5)
    fx.put(osfx.sound(f"oga/creatures/cute_0{(k % 9) + 1}", blip(1300)), t, 0.28 * g)


# SIGNATURE: finger patter (+ giggles when it works, a womp when it doesn't)
for k, (a, b, works) in enumerate(B["TICKLE"]):
    tt = a
    while tt < b:
        fx.put(F.tick(3200 + 400 * ((int(tt * 50)) % 3), 0.5), tt, 0.16 if works else 0.12, ((int(tt * 30)) % 3 - 1) * 0.4)
        tt += 1 / (14 if works else 9)
    if works:
        for j in range(int((b - a) / 0.55)):
            giggle(a + 0.2 + j * 0.55, j + k)
    else:
        fx.put(CT.womp(330, 3, 0.22), a + 0.9, 0.15)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
for c in [B["WHY"], B["FRIEND"], B["CERE"], B["PRED"], B["EXP"], B["SURP"], B["ROBOT"], B["DELAY"], B["WORKS"], B["FOOL"], B["CTA"]]:
    fx.put(osfx.lib("whoosh"), c - 0.15, 0.35)
fx.put(osfx.sound("oga/creatures/misc_06", blip(500)), B["WHY"] + 0.5, 0.3)
fx.put(osfx.sound("oga/retro-synth/power_up_06", F.harp_up()), B["CERE"] + 0.4, 0.3)
for k in range(6):                                                   # prediction beeps
    fx.put(osfx.sound("oga/scifi/retro_beep_0" + str(1 + k % 6), blip(1500 + 100 * k)), B["PRED"] + 0.3 + k * 0.28, 0.22)
fx.put(osfx.sound("oga/scifi/terminal_04", blip(1200)), B["EXP"] + 0.5, 0.3)
fx.put(riser(B["BREAK"] - B["EXP"], 200, 1500), B["EXP"], 0.25)
fx.put(osfx.sound("oga/100-sfx/slam_05", impact(1.0)), B["HIT"], 0.8)
fx.put(impact(0.8), B["HIT"], 0.5)
fx.put(CT.square(110, 0.4, 0.5), B["HIT"] + 0.05, 0.15)
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up(659.3)), B["SURP"] + 0.5, 0.25)
fx.put(osfx.sound("oga/100-sfx/machine_02", F.gears(1.4)), B["ROBOT"] + 0.3, 0.3)
fx.put(CT.tone_glide(300, 900, 0.5, "square", 0.25, 0.5), B["ROBOT"] + 1.0, 0.12)
for k in range(10):
    fx.put(F.tick(2000 + 100 * k, 0.9), B["DELAY"] + 0.3 + k * 0.12, 0.22)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["DELAY"] + 1.6, 0.3)
fx.put(osfx.sound("oga/creatures/weird_01", CT.tone_glide(900, 400, 0.6, "square", 0.5, 0.4)), B["FOOL"] + 0.5, 0.35)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kbh")], gain=0.44, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=6.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
