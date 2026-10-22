"""Cinematic sound effects for the black hole collision video (no narration, no text sounds).

The centrepiece is a gravitational-wave 'chirp': a tone whose pitch and loudness rise faster and
faster into the merger (like LIGO's GW150914 sonification), then a ringdown.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()
MERGE = 19.0

# ---- deep space drone the whole way, with a slow beating
for ch in range(2):
    rumble = norm(band(rng.standard_normal(N), 25, 120))
    air = norm(band(rng.standard_normal(N), 200, 900))
    beat = 0.75 + 0.25 * np.sin(2 * np.pi * t / 6.0 + ch)
    amb.x[:, ch] += (0.6 * rumble + 0.12 * air) * beat
n = N
tt = np.arange(n) / SR
drone = (np.sin(2 * np.pi * 41.2 * tt) + 0.6 * np.sin(2 * np.pi * 61.7 * tt + 1) + 0.3 * np.sin(2 * np.pi * 82.4 * tt)) * 0.5
fx.put(norm(drone) * 0.6, 0.0, 0.2)

# ---- cold open: impact + whoosh orbit + rewind
fx.put(impact(1.1), 0.0, 1.0)
fx.put(braam(2.0, 44), 0.0, 0.7)
for k in range(6):
    fx.put(sweep(0.25, 300, 2500), 0.15 + k * 0.28, 0.25, -0.6 if k % 2 else 0.6)
fx.put(rewind(0.45), 1.6, 0.5)

# ---- the galaxy: shimmer + the blazar jet hum
for k, f in enumerate([523, 784, 1046, 1568]):
    fx.put(bell(f, 2.0), 2.2 + k * 0.18, 0.12, (k - 1.5) / 2)
n = int(3.4 * SR)
tt = np.arange(n) / SR
jet = band(np.sign(np.sin(2 * np.pi * 110 * tt)) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)), 200, 5000)
fx.put(norm(jet) * env(n, 0.5, 0.6), 2.4, 0.08)
fx.put(sweep(1.0, 150, 3500), 5.2, 0.5)  # dive into the core

# ---- the binary: two slow heavy whooshes per orbit
for k in range(8):
    fx.put(sweep(0.6, 120, 900), 6.4 + k * 0.62, 0.3, -0.7 if k % 2 else 0.7)
fx.put(braam(2.6, 49), 6.6, 0.4)

# ---- THE CHIRP: from the waves scene into the merger
start = 11.4
n = int((MERGE - start) * SR)
tt = np.arange(n) / SR
tau = np.maximum(MERGE - start - tt, 0.004)
f = np.minimum(35 * tau ** (-3 / 8) * 2.2, 900)
ph = 2 * np.pi * np.cumsum(f) / SR
amp = np.minimum(1.0, 0.12 * tau ** (-1 / 4) * 1.6)
chirp = (np.sin(ph) + 0.35 * np.sin(2 * ph)) * amp
fx.put(norm(chirp) * np.linspace(0.3, 1, n), start, 0.55)
# heartbeat-like pulses of the warped grid
for x in np.arange(11.6, 16.2, 0.8):
    fx.put(thump(48, 0.4, 0.8), x, 0.4)
for tt_, sig in drum_roll(16.2, MERGE - 0.05, 0.42, 0.07, 60):
    fx.put(sig, tt_, 0.45)
fx.put(riser(2.6, 100, 1200), MERGE - 2.6, 0.3)

# ---- MERGER: huge hit, then the ringdown tone
fx.put(impact(1.4), MERGE, 1.0)
fx.put(braam(3.6, 41), MERGE, 0.85)
fx.put(sub_drop(1.8, 110, 25), MERGE, 0.8)
n = int(2.2 * SR)
tt = np.arange(n) / SR
ring = np.sin(2 * np.pi * 250 * tt) * np.exp(-tt * 3) + 0.4 * np.sin(2 * np.pi * 375 * tt) * np.exp(-tt * 4)
fx.put(reverb(np.concatenate([ring, np.zeros(SR)]), 1.8, 0.5), MERGE + 0.05, 0.35)

# ---- "more power than all the stars": a wide shimmering swell
for k, f2 in enumerate([261, 329, 392, 523, 659]):
    fx.put(tone(f2, 2.6, 0.3, 0.4), 21.0 + k * 0.05, 0.08)
for k in range(10):
    fx.put(bell(1046 * 2 ** ((k % 5) / 5), 1.0), 21.2 + k * 0.17, 0.08, (k % 5 - 2) / 3)

# ---- ripples reach Earth: soft pulsing whooshes, then the laser hum of the detector
for k in range(5):
    fx.put(sweep(0.7, 400, 120), 23.6 + k * 0.5, 0.3)
n = int(2.0 * SR)
tt = np.arange(n) / SR
laser = np.sin(2 * np.pi * 880 * tt) * (0.7 + 0.3 * np.sin(2 * np.pi * 14 * tt))
fx.put(laser * env(n, 0.1, 0.3), 26.0, 0.12)
fx.put(blip(1760, 0.08), 26.05, 0.15)

# ---- back to the pair (loop)
fx.put(sweep(0.8, 200, 3000), 27.3, 0.4)
fx.put(riser(1.0, 100, 700), 28.6, 0.25)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
