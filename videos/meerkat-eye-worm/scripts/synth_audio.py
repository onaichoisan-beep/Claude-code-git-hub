"""Narration + open-source sound effects for this short (house-style template).

  python3 scripts/synth_audio.py

1. Lays out the narration made by make_voices.py (assets/audio/vo/NN.wav + NN.json): one voice per
   character, captions synced to the words.
2. Builds the sound from OPEN-SOURCE sources (osfx.py): CC0 recordings from Kenney.nl / OpenGameArt
   (`python3 ../_engine/osfx.py find <word>`), Openverse CC0/CC BY, jsfxr 8-bit effects, the bundled
   HyperFrames library, and the numpy kits (sfxlib cinematic hits, foley story sounds) as layers and
   fallbacks. Everything used is frozen into assets/sfx/ (CC BY credits in assets/sfx/CREDITS.md).
3. Ducks the SFX under the voices and writes assets/audio/mix.wav + captions.js.
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

LINES = json.load(open(os.path.join(HERE, "lines.json")))
GAPS = {1: 0.55, 3: 0.2, 4: 0.2, 5: 0.35, 6: 0.25, 7: 0.5, 8: 0.3, 9: 0.4}   # silence before line i (default 0.3)
TAIL = 1.2                 # after the last line: the bird leans in + the loop flash

# caption chunks per line: (display text, first spoken word(s) of the chunk); *word* = gold, | = new line
CAPS = [
    [("A BIRD PULLED A *WORM*|OUT OF A MEERKAT'S EYE", "a")],
    [("NOTHING SEEMS *WRONG*", "at")],
    [("BUT THIS BIRD KEEPS|COMING *BACK*", "but"), ("TO THE *SAME SPOT*", "to")],
    [("\"THAT'S MY *EYE*, MATE!\"", "oi")],
    [("\"SOMETHING'S *MOVING*|IN THERE.\"", "hold")],
    [("IT PULLS... AND PULLS...", "then"), ("A *PARASITE*!", "and")],
    [("\"WAS THAT *INSIDE* ME?!\"", "was")],
    [("EYE WORMS ARE *REAL*", "eye"), ("FLIES SPREAD THEM|SIPPING *TEARS*", "flies")],
    [("REAL ONES: *THREAD-THIN*|UNDER 2 CM", "but"), ("THIS FAT GRUB?", "grub"), ("PROBABLY *AI*", "that")],
    [("\"WANT ME TO|CHECK *YOURS*?\"", "still")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.35, gaps=GAPS, max_pause=0.4)
DUR = round(np.ceil((clips[-1]["b"] + TAIL) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")
os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
K = V.Words(clips)
A, B, W, E = K.A, K.B, K.W, K.E
tracks = V.voice_tracks(clips, SR, N, band)
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.6)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()

# beats the picture shares (written into captions.js as window.BEATS)
T_PULL = A(5)
T_OUT = W(5, "parasite")
T_AI = W(8, "AI")

def buzz(d=1.6, f=190, seed=3):
    t = np.arange(int(SR * d)) / SR
    fm = f + 18 * np.sin(2 * np.pi * 6.5 * t) + 8 * np.sin(2 * np.pi * 1.3 * t + seed)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    x = (np.mod(ph, 2 * np.pi) / np.pi - 1) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.9 * t + seed) ** 2)
    x = band(x, 150, 3000) * env(len(x), 0.15, 0.3)
    return x * 0.5

# ---------------------------------------------------------------- ambience: dry savanna, wind + insects
amb.x += (0.22 * F.wind(DUR, 300, 700, 0.25, seed=4))[:, None]
amb.x += (0.10 * F.crickets(DUR, seed=5))[:, None]

# ---------------------------------------------------------------- hook: the yank
fx.put(braam(2.0, 55.0), 0.0, 0.55)
fx.put(osfx.sound("oga/water-splash/slime_03", F.splash(0.5)), 0.15, 0.6)
fx.put(osfx.sound("oga/water-splash/slime_05", F.splash(0.4)), 0.7, 0.45)
fx.put(F.squawk(seed=5), 0.4, 0.3, 0.4)
fx.put(osfx.sound("oga/water-splash/slime_12", F.splash(0.6)), W(0, "eye") - 0.08, 0.6)
fx.put(impact(0.8), W(0, "eye"), 0.45)
fx.put(rewind(0.45), A(1) - 0.5, 0.45)
fx.put(osfx.lib("glitch-1"), A(1) - 0.4, 0.3)

# ---------------------------------------------------------------- calm eye, the bird keeps coming back
for k in range(4):
    fx.put(F.chirp(30 + k), A(1) + 0.4 + 0.8 * k, 0.16, 0.6)
fx.put(osfx.lib("whoosh"), W(2, "bird") - 0.3, 0.3, 0.5)
for k in range(6):
    fx.put(osfx.sound(f"sfx100v2_wood_hit_0{1 + k % 3}", click()), W(2, "coming") + 0.38 * k, 0.4, 0.3)
fx.put(osfx.sound("oga/creatures/grunt_02", thump(200, 0.1)), A(3), 0.35, -0.3)
for k in range(3):
    fx.put(osfx.sound(f"sfx100v2_wood_hit_0{1 + k}", click()), A(4) + 0.3 + 0.9 * k, 0.35, 0.3)

# ---------------------------------------------------------------- the pull
fx.put(riser(B(5) - T_PULL, 120, 900), T_PULL, 0.35)
fx.put(osfx.sound("oga/water-splash/slime_07", F.splash(0.4)), W(5, "pulls"), 0.55)
fx.put(osfx.sound("oga/water-splash/slime_09", F.splash(0.4)), W(5, "pulls", 1), 0.6)
fx.put(osfx.sound("oga/water-splash/slime_12", F.splash(0.6)), T_OUT - 0.1, 0.7)
fx.put(impact(1.0), T_OUT, 0.55)
fx.put(osfx.sound("oga/creatures/ooh", F.squawk(seed=7)), A(6) - 0.15, 0.3, -0.3)

# ---------------------------------------------------------------- the facts: flies + tears, thread-thin, AI
fx.put(buzz(2.6), A(7) + 0.9, 0.35, 0.4)
fx.put(bubble(0.6), W(7, "tears"), 0.4)
fx.put(osfx.lib("pop"), W(8, "thread"), 0.4)
fx.put(osfx.lib("whoosh"), W(8, "grub") - 0.2, 0.35)
fx.put(osfx.lib("glitch-2"), T_AI - 0.05, 0.5)
fx.put(impact(0.7), T_AI, 0.4)

# ---------------------------------------------------------------- the bird leans at YOU -> back to the hook
fx.put(F.chirp(44), A(9) - 0.2, 0.25, 0.3)
fx.put(osfx.lib("whoosh-short"), DUR - 0.5, 0.4)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.55, makeup_db=8.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({"PULL": round(T_PULL, 3), "OUT": round(T_OUT, 3), "AI": round(T_AI, 3)}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
