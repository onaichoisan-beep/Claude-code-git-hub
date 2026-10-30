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
DUR_MAX = 5.0              # an intro: 5 seconds, no more

# ---------------------------------------------------------------- the beats (shared with the picture via window.BEATS)
T_TURN = 1.3               # the dragon curls round toward the camera
T_INHALE = 2.0             # its head fills the frame, rears back, throat glows
T_FIRE = 2.25              # fire bursts in every direction
T_FADE = 2.85              # fire starts fading out
T_TITLE = 2.95             # "WELCOME BACK TO" banner unrolls

# no burned-in captions: the title card IS the text
CAPS = [[]]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=3.0, max_pause=0.25)
DUR = DUR_MAX
assert clips[-1]["b"] < DUR - 0.15, clips[-1]["b"]
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
duck = V.duck_env(voice, SR, depth=0.45)
captions = []
amb, fx = Bus(), Bus()
T_HANDLE = W(0, "hey")
T_NAME = W(0, "rishish")

# ---------------------------------------------------------------- 1. the dragon swims in from the left (air rushing past)
amb.x += (0.5 * F.wind(DUR, 400, 900, 0.5, seed=4) * seg(0, T_FIRE, 0.3))[:, None]
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.5, -0.6)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_air_02", sweep(0.3, 300, 120)), 0.45, 0.4, -0.3)
fx.put(osfx.sound("oga/creatures/monster_03", roar(0.6, 160)), 0.7, 0.3, -0.2)     # a low growl on the way in

# ---------------------------------------------------------------- 2. curls round and comes at the camera
fx.put(osfx.lib("whoosh"), T_TURN - 0.05, 0.55, 0.3)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_air_03", sweep(0.3, 200, 600)), T_TURN + 0.3, 0.45)
fx.put(riser(T_FIRE - T_TURN, 150, 1000), T_TURN, 0.2)

# ---------------------------------------------------------------- 3. inhale + ROAR + fire everywhere
fx.put(osfx.sound("oga/creatures/breath", sweep(0.3, 200, 900)), T_INHALE - 0.05, 0.5)
fx.put(osfx.sound("oga/creatures/roar_02", roar(1.2, 85)), T_FIRE - 0.1, 0.85)
fx.put(roar(1.0, 70), T_FIRE - 0.08, 0.4)
fx.put(osfx.sound("oga/scifi/rocket_01", F.fire(1.2, 3)), T_FIRE, 0.7)
fx.put(F.fire(1.3, 53), T_FIRE, 0.75)
fx.put(osfx.sound("oga/bangs-fireworks/cannon_02", impact(1.0)), T_FIRE, 0.6)
fx.put(impact(1.2), T_FIRE, 0.7)
fx.put(sub_drop(1.0, 80, 28), T_FIRE, 0.6)

# ---------------------------------------------------------------- 4. the fire fades: crackle tail
fx.put(F.fire(0.9, 61) * np.linspace(1, 0, int(0.9 * SR)), T_FADE, 0.3)

# ---------------------------------------------------------------- 5. WELCOME BACK TO @hey.rishish
fx.put(osfx.lib("whoosh-short"), T_TITLE, 0.3)
for i in range(12):                       # each handle letter drops in with a pop: "@hey." on "hey", "rishish" on "Rishish"
    fx.put(osfx.lib("pop"), (T_HANDLE + i * 0.035) if i < 5 else (T_NAME + (i - 5) * 0.035), 0.18, -0.6 + i * 0.1)
fx.put(osfx.sound("oga/retro-synth/power_up_03", osfx.sfxr("powerUp", seed=7)), T_HANDLE, 0.35)
fx.put(impact(0.6), T_HANDLE, 0.3)
chord = [523.25, 659.25, 783.99, 1046.5]
for i, f in enumerate(chord):             # a bright arpeggio into a held chord on the name
    fx.put(bell(f, 1.2), T_NAME - 0.2 + i * 0.05, 0.15)
fx.put(add(*[bell(f, 1.2) for f in chord]), T_NAME + 0.05, 0.1)
fx.put(osfx.lib("sparkle"), T_NAME + 0.1, 0.35)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.55, makeup_db=7.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.85)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
beats = {"TURN": T_TURN, "INHALE": T_INHALE, "FIRE": T_FIRE, "FADE": T_FADE, "TITLE": T_TITLE,
         "HANDLE": round(T_HANDLE, 3), "NAME": round(T_NAME, 3)}
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps(beats) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
