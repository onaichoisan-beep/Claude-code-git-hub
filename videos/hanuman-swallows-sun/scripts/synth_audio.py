"""Cinematic sound effects for the Hanuman video (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def chirp(f=3200, d=0.12):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.6 * np.sin(2 * np.pi * 18 * tt))) / SR) * env(n, 0.01, d * 0.6)


def gulp(d=0.5):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(500 * np.exp(-tt * 6) + 80) / SR) * np.exp(-tt / 0.22)
    return add(s, 0.6 * thump(90, 0.3, 1.0))


def trumpet(d=1.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = 380 + 260 * np.minimum(1, tt / 0.25) - 80 * tt
    saw = 2 * ((np.cumsum(ff * (1 + 0.03 * np.sin(2 * np.pi * 7 * tt))) / SR) % 1) - 1
    return norm(band(saw, 200, 4000)) * env(n, 0.05, 0.4)


def whistle_down(d=1.4):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(1800 * (0.25 ** (tt / d))) / SR) * env(n, 0.05, 0.2)


# ---- ambience
forest = seg(1.6, 8.9, 0.4)
space = seg(8.8, 15.5, 0.3)
windy = seg(15.5, 17.0, 0.2)
divine = seg(20.0, 28.7, 0.5)
for ch in range(2):
    air = norm(band(rng.standard_normal(N), 300, 2500))
    hush = norm(band(rng.standard_normal(N), 40, 200))
    howl = norm(band(rng.standard_normal(N), 250, 900)) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 1.3 + ch))
    amb.x[:, ch] += 0.18 * air * forest + 0.5 * hush * space + 0.8 * howl * windy + 0.25 * hush * divine
# leap: rushing wind that grows with speed
n = int(3.4 * SR)
rush = norm(band(rng.standard_normal(n), 200, 3000)) * np.linspace(0.2, 1, n) ** 1.5
fx.put(rush * env(n, 0.05, 0.3), 5.4, 0.55)

# ---- cold open: the gulp that darkens the world
fx.put(sweep(0.3, 400, 3000), 0.0, 0.5)
fx.put(gulp(), 0.28, 1.0)
fx.put(impact(), 0.3, 0.9)
fx.put(sub_drop(1.2), 0.3, 0.8)
fx.put(braam(1.8, 52), 0.32, 0.55)
fx.put(rewind(0.45), 1.4, 0.55)

# ---- dawn: birds, a rumbling tummy, the mango idea
for k in range(10):
    fx.put(chirp(2800 + (k % 4) * 400), 1.8 + k * 0.32 + (k % 3) * 0.05, 0.12, (k % 5 - 2) / 3)
n = int(0.8 * SR)
fx.put(norm(band(rng.standard_normal(n), 60, 300)) * env(n, 0.1, 0.3) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 12 * np.arange(n) / SR))), 1.8, 0.45)
fx.put(add(bubble(1.2), bell(1568, 0.6) * 0.5), 2.3, 0.4)
fx.put(riser(0.8, 200, 900), 4.6, 0.3)

# ---- the leap
fx.put(add(impact(0.5), sweep(0.6, 200, 4000)), 5.4, 0.85)
for tt_, sig in drum_roll(5.6, 8.7, 0.45, 0.12, 74):
    fx.put(sig, tt_, 0.5)
fx.put(riser(3.0, 120, 1400), 5.7, 0.25)

# ---- the gulp
fx.put(sweep(0.7, 3000, 150), 9.3, 0.6)
fx.put(gulp(0.6), 9.95, 1.0)
fx.put(impact(1.1), 10.0, 1.0)
fx.put(braam(2.6, 46), 10.0, 0.8)
fx.put(sub_drop(1.5), 10.0, 0.8)
fx.put(gong(82, 3.0), 10.4, 0.25)

# ---- Indra: thunder, conch + elephant trumpet, the vajra strike, the fall
fx.put(norm(band(rng.standard_normal(int(2.0 * SR)), 30, 300)) * env(int(2.0 * SR), 0.3, 1.2), 12.0, 0.5)
fx.put(conch(1.2, 330), 12.1, 0.35)
fx.put(trumpet(0.9), 12.6, 0.4)
fx.put(sweep(0.35, 600, 5000), 13.25, 0.6)
fx.put(add(impact(1.3), noise_hit(0.15, 3000, 12000)), 13.6, 1.0)
fx.put(braam(2.0, 49), 13.6, 0.6)
for k, f in enumerate([1046, 1318, 1568]):
    fx.put(bell(f, 0.9), 13.7 + k * 0.07, 0.25)
fx.put(whistle_down(1.5), 13.85, 0.3)
fx.put(add(thump(70, 0.4, 1.0), noise_hit(0.12, 100, 1200) * 0.5), 15.35, 0.7)

# ---- Vayu: the howl, then sudden total silence (all air stopped) with a slow heartbeat
fx.put(sub_drop(1.0, 70, 25), 17.0, 0.8)
for b in np.arange(17.4, 19.9, 0.9):
    fx.put(heartbeat(), b, 0.7)

# ---- blessing and transformation
fx.put(conch(2.0, 290), 20.1, 0.4)
for k, f in enumerate([523, 659, 784, 1046, 1318]):
    fx.put(bell(f, 1.5), 20.4 + k * 0.25, 0.18, (k - 2) / 3)
for k in range(12):
    fx.put(bell(2093 + (k % 4) * 300, 0.4), 20.9 + k * 0.16, 0.08, (k % 5 - 2) / 3)
fx.put(riser(1.4, 150, 1500), 21.4, 0.3)
fx.put(impact(1.2), 22.8, 1.0)
fx.put(braam(2.6, 55), 22.8, 0.7)
fx.put(gong(98, 3.5), 22.85, 0.35)
for k in range(8):
    fx.put(taiko(76 if k % 2 else 64), 23.2 + k * 0.28, 0.55)

# ---- the name reveal
fx.put(sweep(0.6, 3000, 300), 25.2, 0.4)
fx.put(add(taiko(70), bell(880, 1.0) * 0.4), 25.7, 0.8)
fx.put(braam(2.0, 55), 27.1, 0.7)
fx.put(gong(110, 2.5), 27.1, 0.35)
fx.put(riser(1.3, 120, 1200), 28.6, 0.35)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
