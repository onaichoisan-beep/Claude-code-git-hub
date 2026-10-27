"""Narration + SFX for "The Library of Unlived Lives".

  python3 scripts/synth_audio.py

A hushed British librarian narrates. Soft, eerie, intimate sound: library air, whispers, page
turns, a door of light, footsteps on a road, rain, a heartbeat for the secret, a phone swipe and
a glitch as the newest book unwrites itself. Writes assets/audio/mix.wav + captions.js.
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

LINES = json.load(open(os.path.join(HERE, "lines.json")))["lines"]
GAPS = {1: 0.6, 2: 0.45, 3: 0.45, 4: 0.45, 5: 0.6, 6: 0.45, 7: 0.6, 8: 0.35, 9: 0.6}
TAIL = 1.7  # the last book crumbles to dust; the camera flies back down the aisle

CAPS = [
    [("SOMEWHERE,", "somewhere"), ("THERE'S A *LIBRARY*...", "there's"), ("WITH A BOOK FOR EVERY|LIFE YOU *DIDN'T LIVE*.", "with")],
    [("EVERY TIME YOU *CHOOSE*,", "every"), ("THE WORLD *SPLITS* IN TWO.", "the"), ("AND A *NEW BOOK* APPEARS.", "and")],
    [("THE LIFE WHERE|YOU SAID *YES*.", "the")],
    [("THE ONE WHERE YOU|TOOK THE *OTHER ROAD*.", "the")],
    [("THE ONE WHERE YOU|*NEVER MET THEM*.", "the")],
    [("PEOPLE COME HERE LOOKING|FOR A *HAPPIER ENDING*.", "people"), ("BUT HERE'S THE *SECRET*.", "but")],
    [("IN EVERY SINGLE BOOK...", "in"), ("THE OTHER YOU|IS READING ABOUT *YOU*.", "the"), ("*WISHING THEY WERE YOU*.", "wishing")],
    [("OH. LOOK.", "oh"), ("A *NEW BOOK*. JUST NOW.", "a")],
    [("THE LIFE WHERE YOU|*SCROLLED PAST* THIS VIDEO.", "the")],
    [("YOU *DIDN'T*.", "you"), ("*GOOD CHOICE*.", "good")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.35, gaps=GAPS, max_pause=0.45)
DUR = round(np.ceil((clips[-1]["b"] + TAIL) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")
os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402

K = V.Words(clips)
A, B, W, E = K.A, K.B, K.W, K.E
tracks = V.voice_tracks(clips, SR, N, band, level_db=-13.0)
voice = sum(tracks.values())
# a touch of room on the narrator: she is in a big quiet hall
voice = voice + 0.12 * (reverb(voice, 1.6, 1.0, 5) - voice)
duck = V.duck_env(voice, SR, depth=0.55)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()


def R(name, fallback, dur=None):
    x = load(os.path.join(ROOT, "assets", "sfx", name + ".wav"), 0, dur)
    return fade_out(x, 0.08) if x is not None else fallback


def L(name):
    x = load(os.path.join(LIB, name + ".mp3")) if LIB else None
    return x if x is not None else np.zeros(10)


def bed(sig, a, b, gain, fade=0.5, pan=0.0):
    n = int((b - a) * SR)
    x = np.tile(sig, int(np.ceil(n / len(sig))))[:n].copy()
    f = int(fade * SR)
    if f and len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
    amb.put(x, a, gain, pan)


T_NEW = A(7)
T_SWIPE = W(8, "scrolled")
T_DUST = W(9, "didn't")

# ---------------------------------------------------------------- the hall: air, a low choir-ish drone, whispers
for ch in range(2):
    amb.x[:, ch] += 0.30 * norm(band(rng.standard_normal(N), 50, 500)) + 0.05 * norm(band(rng.standard_normal(N), 3000, 8000))
drone = F.pad(DUR, [110, 164.8, 220, 277.2], a=2.0, r_=2.0, seed=3)
amb.x += (0.22 * drone * (1 - 0.7 * seg(A(6) - 0.2, A(7), 0.5)))[:, None]
amb.x += (0.16 * F.pad(DUR, [138.6, 207.7, 329.6], a=1.0, r_=1.0, seed=4) * seg(A(6) - 0.2, A(7), 0.6))[:, None]  # the secret: darker
bed(R("roomtone", F.whispers(8, seed=5)), 0, DUR, 0.14)
bed(F.whispers(6, seed=6), A(5), A(7), 0.22, pan=-0.3)
for k in range(int(DUR / 1.0)):  # a slow old clock somewhere in the stacks
    fx.put(F.tick(1400 if k % 2 else 1100, 0.4), 0.5 + 1.0 * k, 0.06, 0.5)

# ---------------------------------------------------------------- HOOK: flying down the endless aisle
fx.put(impact(1.0), 0.0, 0.7)
fx.put(braam(3.0, 55), 0.0, 0.35)
fx.put(L("whoosh-cinematic"), 0.0, 0.45)
fx.put(F.page_flip(11, 0.6), 0.2, 0.3, -0.4)
fx.put(F.page_flip(12, 0.5), 0.5, 0.25, 0.4)
fx.put(add(bell(880, 3.0), 0.5 * bell(1318.5, 3.0)), W(0, "library"), 0.18)
fx.put(F.harp_up(523.25, 8, 0.07), W(0, "didn't") - 0.3, 0.14)
fx.put(rewind(0.5), A(1) - 0.62, 0.45)

# ---------------------------------------------------------------- the world splits; a new book
fx.put(F.stab(110, 1.2), W(1, "choose"), 0.2)
fx.put(add(F.ice_crack(3, 1.0), sweep(0.8, 300, 4000)), W(1, "splits"), 0.4)
fx.put(L("sparkle"), W(1, "new") - 0.05, 0.4)
fx.put(add(R("bookclose", F.book_thud(), 1.0), 0.5 * F.page_flip(14)), W(1, "appears") + 0.1, 0.4)

# ---------------------------------------------------------------- three unlived lives, each in an open book
for i in (2, 3, 4):
    fx.put(R("page", F.page_flip(20 + i, 0.5), 1.0), A(i) - 0.35, 0.45, (i - 3) * 0.3)
fx.put(R("door", F.creak(0.9, 140, seed=31), 1.5), A(2) + 0.1, 0.35)
fx.put(F.pad(1.8, [523.3, 659.3, 784], a=0.3, r_=1.0, seed=32), W(2, "yes"), 0.22)
for k in range(5):
    fx.put(R("footsteps", thump(120, 0.08, 1.0), 0.35), A(3) + 0.2 + 0.36 * k, 0.25, -0.2 + 0.1 * k)
fx.put(F.wind(B(3) - A(3) + 0.5, 500, 900, 0.3, seed=33), A(3), 0.12)
rain = band(rng.standard_normal(int((B(4) - A(4) + 0.8) * SR)), 2000, 9000)
rain *= 0.5 + 0.5 * (rng.random(len(rain)) > 0.997)
fx.put(norm(rain) * env(len(rain), 0.3, 0.4), A(4) - 0.1, 0.18)
fx.put(add(bell(659.3, 1.5), 0.6 * bell(622.3, 1.5)), W(4, "never"), 0.15)  # the heart that never was

# ---------------------------------------------------------------- the visitors; the secret
for k in range(3):
    fx.put(R("footsteps", thump(110, 0.08, 1.0), 0.35), A(5) + 0.3 + 0.5 * k, 0.15, 0.4)
fx.put(R("page", F.page_flip(41, 0.4), 1.0), W(5, "happier"), 0.25)
fx.put(add(sub_drop(1.4, 80, 30), 0.5 * F.stab(98, 1.6)), W(5, "secret"), 0.4)
for k in range(5):
    fx.put(heartbeat(), A(6) + 0.2 + 0.8 * k, 0.35)
fx.put(F.whispers(2.5, seed=61), W(6, "reading") - 0.3, 0.3, 0.3)
fx.put(F.pad(3.0, [440, 523.3, 659.3], a=0.4, r_=2.0, seed=62), W(6, "wishing"), 0.25)
fx.put(L("chime"), W(6, "wishing") + 0.2, 0.2)

# ---------------------------------------------------------------- a new book, just now; the swipe; dust
fx.put(L("sparkle"), T_NEW + 0.05, 0.45)
fx.put(F.harp_up(659.3, 7, 0.06), W(7, "new"), 0.18)
fx.put(R("writing", F.page_flip(71, 1.0), 1.6), W(7, "just") - 0.1, 0.35)
fx.put(L("whoosh-short"), T_SWIPE + 0.1, 0.5)
fx.put(L("glitch-3"), T_SWIPE + 0.35, 0.3)
fx.put(L("glitch-1"), T_DUST - 0.05, 0.35)
fx.put(add(sweep(1.2, 4000, 400), 0.4 * F.sparkle(1.2, seed=91, lo=1500, hi=4000)), T_DUST, 0.4)
fx.put(add(bell(523.3, 3.0), 0.6 * bell(784, 3.0), 0.4 * bell(1046.5, 3.0)), W(9, "good"), 0.25)
fx.put(L("whoosh-cinematic"), DUR - 3.2, 0.35)
fx.put(impact(0.6), DUR - 0.05, 0.3)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.6, makeup_db=3.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.85)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:2s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
