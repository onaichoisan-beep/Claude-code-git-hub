"""Soft, awe-inspiring ambient sound for the Big Bang -> Earth video.

No booms, no dramatic hits: gentle swells, shimmer, chimes and a warm pad. No narration, no text sounds.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def pad(freqs, d, a=0.4, r=0.4):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for det in (-0.6, 0.6):
            s += np.sin(2 * np.pi * (f + det) * tt) + 0.25 * np.sin(2 * np.pi * 2 * (f + det) * tt)
    return norm(s) * env(n, d * a, d * r)


def swell(d, lo, hi):
    n = int(d * SR)
    x = norm(band(rng.standard_normal(n), lo, hi))
    return x * np.sin(np.pi * np.linspace(0, 1, n)) ** 2


# ---- a slowly evolving cosmic pad under everything (chords drift with the eras)
CHORDS = [
    (0.0, 4.6, [65.4, 98.0, 130.8]),          # C (deep, quiet)
    (4.4, 8.4, [73.4, 110.0, 146.8, 220.0]),  # D
    (8.2, 11.4, [87.3, 130.8, 174.6, 261.6]), # F
    (11.2, 15.0, [98.0, 146.8, 196.0, 293.7]),# G
    (14.8, 18.6, [82.4, 123.5, 164.8, 246.9]),# E
    (18.4, 22.2, [87.3, 130.8, 220.0, 329.6]),# F
    (22.0, 26.4, [73.4, 110.0, 174.6, 293.7]),# D
    (26.2, 30.0, [65.4, 98.0, 164.8, 261.6, 392.0]),  # C (home)
]
for a, b, fr in CHORDS:
    fx.put(pad(fr, b - a + 0.6, 0.3, 0.35), a, 0.16)

# ---- the dot: a soft heartbeat-like glow pulse + faint hum
n = int(2.0 * SR)
tt = np.arange(n) / SR
hum = np.sin(2 * np.pi * 55 * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.6 * tt))
fx.put(hum * env(n, 0.3, 0.3), 0.0, 0.25)
for k, f in enumerate([1568, 2093]):
    fx.put(bell(f, 1.6), 0.2 + k * 0.6, 0.08)

# ---- the Big Bang: a gentle, airy swell, not an explosion
fx.put(swell(2.6, 120, 3000), 1.4, 0.5)
fx.put(riser(1.0, 200, 800) * 0.5, 1.2, 0.15)
for k, f in enumerate([523, 659, 784, 1046, 1318, 1568]):
    fx.put(bell(f, 2.2), 2.0 + k * 0.09, 0.1, (k - 2.5) / 3)

# ---- the hot soup: soft crackle and bubbling
n = int(3.6 * SR)
crackle = band(rng.standard_normal(n), 1500, 7000) * (rng.random(n) > 0.993)
fx.put(norm(band(crackle, 1500, 7000)) * env(n, 0.4, 0.6), 4.6, 0.18)
for k in range(12):
    fx.put(bubble(0.6 + 0.3 * (k % 4)), 5.0 + k * 0.26, 0.12, (k % 5 - 2) / 3)

# ---- first light: a shimmering cascade as the fog clears
for k in range(14):
    fx.put(bell(1046 * 2 ** ((k % 7) / 7), 1.2), 8.5 + k * 0.12, 0.07, (k % 5 - 2) / 3)
fx.put(swell(2.0, 2000, 9000), 8.4, 0.12)

# ---- first stars: a soft twinkle as each one lights
for k in range(9):
    fx.put(bell(1568 + (k % 4) * 262, 1.4), 12.2 + k * 0.28, 0.12, (k % 5 - 2) / 3)

# ---- galaxies + the supernova: slow whoosh, a gentle reverse bloom
fx.put(swell(3.0, 200, 1500), 14.8, 0.25)
n = int(1.5 * SR)
bloom = norm(band(rng.standard_normal(n), 300, 4000)) * np.linspace(0, 1, n) ** 3
fx.put(np.concatenate([bloom, norm(band(rng.standard_normal(int(1.2 * SR)), 300, 3000)) * np.linspace(1, 0, int(1.2 * SR)) ** 2]), 14.1, 0.28)
for k, f in enumerate([659, 880, 1175]):
    fx.put(bell(f, 1.6), 16.1 + k * 0.2, 0.1)

# ---- the Sun ignites: a warm rising swell
fx.put(swell(2.4, 80, 900), 18.8, 0.4)
fx.put(tone(110, 2.2, 0.5, 0.4), 19.8, 0.15)
fx.put(bell(784, 2.0), 20.3, 0.14)

# ---- Earth forms: soft pebble clicks, a muffled distant thud for Theia, then calm
for k in range(16):
    fx.put(add(noise_hit(0.03, 800, 5000) * 0.6, thump(200, 0.05, 0.3) * 0.4), 22.1 + k * 0.11, 0.18, (k % 5 - 2) / 3)
n = int(2.5 * SR)
thud = reverb(np.concatenate([band(thump(45, 0.8, 0.8), 20, 300), np.zeros(int(1.7 * SR))]), 2.0, 0.5, 33)
fx.put(norm(thud), 24.4, 0.4)

# ---- today: ocean-like air and a final gentle chime; shimmer back down into the dot
fx.put(swell(3.4, 150, 1200), 26.2, 0.18)
for k, f in enumerate([523, 659, 784, 1046]):
    fx.put(bell(f, 2.0), 26.6 + k * 0.25, 0.12)
for k in range(6):
    fx.put(bell(2093 - k * 200, 0.8), 29.0 + k * 0.15, 0.06)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"), amb_gain=0.0, makeup_db=10.0)
