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
GAPS = {1: 0.5, 2: 0.45}   # silence before line i (default 0.3)
TAIL = 1.6                 # after the last line: the closing beat + the loop flash

# caption chunks per line: (display text, first spoken word(s) of the chunk); *word* = gold, | = new line
CAPS = [
    [("NEW HOUSE STYLE.", "new"), ("*SHARP*, CLEAN PIXELS.", "sharp")],
    [("EVERY CHARACTER GETS|A *DARK OUTLINE*!", "and")],
    [("PLUS A *VOICE*|THAT ACTUALLY FITS.", "plus")],
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
T_OUTLINE = W(1, "outline")
T_CAT = A(2) - 0.35

# ---------------------------------------------------------------- ambience: a breezy hill at sunset
amb.x += (0.25 * F.wind(DUR, 300, 700, 0.3, seed=2))[:, None]
for k in range(6):
    fx.put(F.chirp(10 + k), 1.0 + 1.3 * k, 0.1, (k % 3 - 1) * 0.7)

# ---------------------------------------------------------------- hook
fx.put(osfx.sound("impactPlate_heavy_002", impact(0.8)), 0.0, 0.6)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(osfx.sfxr("powerUp", seed=4), W(0, "sharp"), 0.25)

# ---------------------------------------------------------------- the kid walks in on the grass, the outline pops
for k in range(6):
    fx.put(osfx.sound(f"footstep_grass_00{k % 5}", thump(120, 0.08, 1.0)), 0.6 + 0.33 * k, 0.35, -0.3)
fx.put(osfx.sfxr("pickupCoin", seed=11), T_OUTLINE, 0.35)
fx.put(osfx.lib("sparkle"), T_OUTLINE + 0.05, 0.35)

# ---------------------------------------------------------------- the cat leaps onto the rock
fx.put(osfx.sfxr("jump", seed=21), T_CAT, 0.3)
fx.put(osfx.sound("impactSoft_medium_001", thump(140, 0.1, 1.2)), T_CAT + 0.32, 0.4)
fx.put(osfx.sound("oga/creatures/cute_01", F.meow(0.5, 600)), T_CAT + 0.4, 0.35, 0.4)
fx.put(add(bell(1046.5, 1.5), 0.5 * bell(1568, 1.5)), W(2, "fits"), 0.18)

# ---------------------------------------------------------------- the loop back to the start
fx.put(osfx.lib("whoosh-short"), DUR - 0.5, 0.35)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.55, makeup_db=8.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({"OUTLINE": round(T_OUTLINE, 3), "CAT": round(T_CAT, 3)}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
