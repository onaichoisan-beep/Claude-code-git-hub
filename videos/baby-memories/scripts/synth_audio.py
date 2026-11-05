"""Narration + sound for "Where did your first 3 years go?" (infantile amnesia; story mode, STYLE 7 + 9).

Voice: Kokoro af_heart, gentle. SIGNATURE sound = the MEMORY: a soft polaroid shutter + a music-box note for every memory
(first steps, word, cake), each one then "fading" with a reversed swell (DAYS REMEMBERED stays 0); the scanner hum + beeps
for the 2025 study, a heartbeat while the baby stares, a padlock click on "locked", a light switch for the mice, a key
jingle at the end. Soft music-box bed (no drums at the start), tape-stop + rewind.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import narrate as NR  # noqa: E402

GAPS = {1: 0.3, 2: 0.35, 3: 0.5, 4: 0.25, 5: 0.35, 6: 0.3, 7: 0.4, 8: 0.25, 9: 0.3, 10: 0.25, 11: 0.4, 12: 0.35, 13: 0.3,
        14: 0.4, 15: 0.35, 16: 0.25, 17: 0.5}
S = NR.Story(ROOT, gaps=GAPS, gold={"thousand", "steps.", "word.", "cake.", "gone.", "amnesia.", "three.", "saved?",
                                    "2025,", "scanner.", "remembered.", "one", "locked.", "light.", "key.", "earliest"},
             red={"gone.", "locked."})
A, W, E, Bn = S.A, S.W, S.E, S.B
B = dict(FIRSTS=A(1), GONE=A(2), NAME=A(3), THREE=A(4), Q=A(5), THOUGHT=A(6), SCAN=A(7), PICS=A(8), AGAIN=A(9), LIT=A(10),
         REMEMBERED=A(11), ONE=A(12), LOCKED=A(13), MICE=A(14), STILL=A(15), KEY=A(16), ASK=A(17))
B["MEMS"] = [W(1, "steps."), W(1, "word."), W(1, "cake.")]
B["PICT"] = [W(8, "face."), W(8, "toy."), W(8, "beach.")]
B["HIT"] = W(11, "remembered.")
B["BREAK"] = B["HIT"] - 0.25
DUR = S.finalize(B, tail=1.3)

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
Sec = CT.Sec
fx.x += CT.bed([
    Sec(B["NAME"], B["SCAN"], 96, 96, "kbo"),
    Sec(B["SCAN"], B["BREAK"], 108, 116, "kbh"),
    Sec(B["HIT"] + 0.3, B["KEY"], 112, 112, "kbhal"),
], gain=0.34, crescendo=(0.8, 1.1))
amb.x += (0.12 * F.pad(DUR, [261.63, 329.63, 392.0, 493.88], seed=5))[:, None]
MB = [1046.5, 1318.5, 1568.0, 1318.5, 1174.7, 1046.5, 987.8, 1046.5]
for k in range(int(B["NAME"] / 0.45)):
    fx.put(bell(MB[k % 8], 0.9) * 0.5, 0.2 + k * 0.45, 0.14, ((k % 3) - 1) * 0.4)


def memory(t, k):
    fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(5000, 1.0)), t, 0.4)
    fx.put(noise_hit(0.12, 3000, 9000), t + 0.02, 0.2)
    fx.put(bell(MB[k % 8] * 1.5, 1.2), t + 0.05, 0.2)
    fx.put(sweep(0.8, 1600, 300) * np.linspace(1, 0, int(0.8 * SR)) * 0.4, t + 0.5, 0.18)


for k, m in enumerate(B["MEMS"]):
    memory(m, k)
fx.put(sub_drop(1.0), B["GONE"], 0.45)
fx.put(osfx.lib("glitch-3"), B["GONE"] + 0.05, 0.3)
fx.put(osfx.lib("whoosh"), B["NAME"] - 0.15, 0.35)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), W(4, "three.") + 0.1, 0.25)
fx.put(CT.womp(392, 3, 0.25), B["Q"] + 0.8, 0.15)
fx.put(osfx.lib("whoosh-cinematic"), B["SCAN"] - 0.2, 0.4)
n = int((B["REMEMBERED"] - B["SCAN"]) * SR)
tt = np.arange(n) / SR
fx.put(np.sin(2 * np.pi * 110 * tt) * 0.3 + 0.15 * np.sin(2 * np.pi * 220 * tt), B["SCAN"], 0.15)
for k, p in enumerate(B["PICT"]):
    fx.put(osfx.sound("oga/scifi/beep_0" + str(1 + k % 3), blip(1500 + 200 * k)), p, 0.3)
for k in range(5):
    fx.put(heartbeat(), B["LIT"] + 0.6 + k * 0.55, 0.35)
fx.put(riser(B["BREAK"] - B["LIT"], 200, 1500), B["LIT"], 0.2)
fx.put(impact(0.7), B["HIT"], 0.45)
fx.put(F.sparkle(1.4, seed=7), B["HIT"] + 0.05, 0.4)
fx.put(osfx.sound("oga/100-sfx/key_open_01", F.tick(2200, 1.0)), W(13, "locked."), 0.5)
fx.put(osfx.sound("oga/100-sfx/switch_02", F.tick(1500, 1.0)), W(14, "light."), 0.45)
fx.put(F.sparkle(1.0, seed=9), W(14, "light.") + 0.1, 0.3)
fx.put(osfx.sound("oga/100-sfx/key_open_02", F.tick(3000, 1.0)), B["KEY"] + 0.5, 0.45)
for k in range(4):
    fx.put(bell(MB[k] * 1.5, 0.9) * 0.5, B["ASK"] + 0.2 + k * 0.3, 0.15)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
S.mix(fx, amb, master, write_wav, band, reverb, B, SR, N)
