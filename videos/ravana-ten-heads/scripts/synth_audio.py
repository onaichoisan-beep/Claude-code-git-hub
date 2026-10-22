"""Cinematic sound effects for the Ravana video (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def evil_laugh(d=1.4, f=95.0):
    """Deep 'HA-HA-HA': pulses of a low voiced buzz."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    pulses = (np.sin(2 * np.pi * 5.2 * tt) > 0.1).astype(float)
    ff = f * (1 - 0.15 * tt / d)
    saw = 2 * ((np.cumsum(ff) / SR) % 1) - 1
    voice = band(saw, 80, 1600) + 0.4 * band(rng.standard_normal(n), 300, 2500)
    k = int(0.01 * SR)
    pulses = np.convolve(pulses, np.ones(k) / k, mode="same")
    return norm(voice * pulses) * env(n, 0.02, 0.3)


def fire_crackle(d, seed=0, rate=30):
    r = np.random.default_rng(seed)
    n = int(d * SR)
    out = norm(band(r.standard_normal(n), 100, 900)) * 0.35
    for _ in range(int(rate * d)):
        i = int(r.uniform(0, d - 0.02) * SR)
        c = noise_hit(0.015, 1500, 8000)
        out[i : i + len(c)] += c[: n - i] * r.uniform(0.2, 0.8)
    return out


def arrow_whoosh(d=0.3):
    n = int(d * SR)
    x = norm(band(rng.standard_normal(n), 1500, 7000)) * np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return x


# ---- ambience: fire for the penance and the effigy, desert wind for the battle
firezone = seg(1.6, 11.2, 0.3)
battle = seg(15.4, 24.6, 0.3)
effigy = seg(24.6, 28.3, 0.3)
for ch in range(2):
    wind = norm(band(rng.standard_normal(N), 250, 1200)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 3.0 + ch))
    drone = norm(band(rng.standard_normal(N), 35, 160))
    amb.x[:, ch] += 0.4 * drone * firezone + 0.3 * wind * battle + 0.25 * drone * (battle + effigy)
fx.put(fire_crackle(9.6, 1), 1.6, 0.45)
fx.put(fire_crackle(3.8, 2, 60), 24.6, 0.7)

# ---- cold open: impact + evil laugh + rewind
fx.put(impact(), 0.0, 1.0)
fx.put(braam(2.0, 46), 0.0, 0.7)
fx.put(evil_laugh(1.4), 0.15, 0.8)
fx.put(rewind(0.45), 1.4, 0.55)

# ---- penance: a gong strike + whoosh into the fire for each offered head
for k in range(9):
    tc = 2.6 + k * 0.5
    fx.put(taiko(68), tc, 0.6)
    fx.put(bell(660 + k * 40, 0.9), tc + 0.02, 0.15)
    fx.put(sweep(0.4, 2400, 300), tc + 0.05, 0.25)
fx.put(riser(1.4, 100, 900), 6.2, 0.3)

# ---- Brahma appears: holy flash, conch, gong, bells; heads restored
fx.put(add(impact(0.5), noise_hit(0.2, 2000, 10000) * 0.4), 7.5, 0.7)
fx.put(conch(2.2, 300), 7.8, 0.45)
fx.put(gong(98, 3.5), 7.7, 0.4)
for k, f in enumerate([523, 659, 784, 1046, 1318]):
    fx.put(bell(f, 1.6), 8.9 + k * 0.09, 0.18, (k - 2) / 3)

# ---- the boon: a stamp per card, then the human card + laugh
fx.put(sweep(0.5, 3000, 300), 11.1, 0.35)
for k in range(3):
    fx.put(taiko(80), 11.6 + k * 0.5, 0.85)
    fx.put(shing(0.3), 11.62 + k * 0.5, 0.2)
fx.put(blip(440, 0.18), 13.6, 0.35)
fx.put(evil_laugh(1.5, 100), 13.7, 0.7)

# ---- Rama: a heroic rising swell, conch, bow creak
fx.put(sweep(0.6, 300, 3000), 15.3, 0.4)
fx.put(braam(2.4, 65), 15.6, 0.55)
fx.put(conch(1.8, 330), 15.9, 0.45)
n = int(0.9 * SR)
creak = band(rng.standard_normal(n), 200, 1200) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * np.linspace(10, 30, n) * np.arange(n) / SR)))
fx.put(norm(creak) * env(n, 0.3, 0.2), 17.4, 0.3)

# ---- the battle: arrow, hit, sparkle regrow, war drums under it
for tt_, sig in drum_roll(18.6, 22.8, 0.45, 0.22, 64):
    fx.put(sig, tt_, 0.45)
for ta in [19.0, 19.5, 20.0, 20.5, 21.0, 21.5]:
    fx.put(arrow_whoosh(0.28), ta, 0.5, -0.4)
    fx.put(add(thump(120, 0.15, 1.5), noise_hit(0.08, 1500, 9000) * 0.6), ta + 0.25, 0.7, 0.4)
    fx.put(bell(1568, 0.6), ta + 0.6, 0.15, 0.4)

# ---- the divine arrow
fx.put(riser(1.3, 150, 2000), 22.8, 0.45)
fx.put(add(norm(band(rng.standard_normal(int(1.3 * SR)), 2000, 9000)) * np.linspace(0, 1, int(1.3 * SR)) ** 2), 22.8, 0.25)
fx.put(arrow_whoosh(0.4), 24.0, 0.8)
fx.put(impact(1.3), 24.4, 1.0)
fx.put(braam(3.0, 41), 24.4, 0.8)
fx.put(sub_drop(1.5), 24.4, 0.7)

# ---- Dussehra: the effigy roars into flame, fireworks pop, crowd cheers
fx.put(sweep(1.2, 100, 1500), 25.0, 0.5)
for k, tb in enumerate([26.0, 26.4, 26.9]):
    fx.put(add(thump(60, 0.6, 2.0), noise_hit(0.3, 100, 3000) * 0.6), tb, 0.55, (k - 1) / 2)
n = int(2.8 * SR)
cheer = norm(band(rng.standard_normal(n), 400, 3500)) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * np.arange(n) / SR)) * env(n, 0.5, 1.0)
fx.put(cheer, 25.4, 0.3)
fx.put(conch(1.6, 300), 26.2, 0.35)
# back into the laugh (loop)
fx.put(riser(1.4, 100, 900), 28.4, 0.3)
fx.put(evil_laugh(1.2), 28.6, 0.6)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
