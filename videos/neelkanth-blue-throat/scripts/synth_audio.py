"""Cinematic sound effects for the Neelkanth video (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def om(d=3.0, f=136.1):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * 2 * f * tt) + 0.25 * np.sin(2 * np.pi * 3 * f * tt)
    return s * env(n, d * 0.3, d * 0.4)


def damaru(t0, d=0.8):
    out, x = [], t0
    while x < t0 + d:
        out.append(x)
        x += 0.06
    return out


def gulp(d=0.6):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(260 * np.exp(-tt * 5) + 60) / SR) * np.exp(-tt / 0.25)
    return add(s, 0.6 * thump(60, 0.4, 1.0))


# ---- ambience: ocean, eerie poison hiss, mountain wind
ocean_ = seg(1.6, 10.2, 0.3)
poison_ = seg(6.4, 10.2, 0.3) + seg(13.4, 16.2, 0.3)
mountain = seg(10.2, 13.4, 0.3)
heaven = seg(19.0, 28.3, 0.4)
for ch in range(2):
    waves = norm(band(rng.standard_normal(N), 150, 1200)) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 2.6 + ch))
    hiss = norm(band(rng.standard_normal(N), 2500, 9000))
    wind = norm(band(rng.standard_normal(N), 300, 1200)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 3.3))
    low = norm(band(rng.standard_normal(N), 30, 160))
    amb.x[:, ch] += 0.3 * waves * ocean_ + 0.18 * hiss * poison_ + 0.3 * wind * mountain + 0.35 * low * (poison_ + heaven * 0.5)

# ---- cold open: dread, the throat flares, rewind
fx.put(braam(2.0, 44), 0.0, 0.7)
fx.put(sweep(0.5, 200, 2500), 0.0, 0.3)
fx.put(gulp(), 0.3, 0.8)
fx.put(impact(1.1), 0.45, 0.9)
fx.put(sub_drop(1.2), 0.45, 0.7)
for k, f in enumerate([1318, 1760, 2093]):
    fx.put(bell(f, 1.0), 0.5 + k * 0.05, 0.2)
fx.put(rewind(0.45), 1.4, 0.55)

# ---- the churning: a taiko on every heave, groaning rope, grinding mountain
for x in np.arange(2.0, 6.4, 1.047):
    fx.put(taiko(64), x, 0.8)
    n = int(0.6 * SR)
    creak = band(rng.standard_normal(n), 100, 700) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 24 * np.arange(n) / SR)))
    fx.put(norm(creak) * env(n, 0.1, 0.3), x + 0.1, 0.22)
n = int(4.6 * SR)
fx.put(norm(band(rng.standard_normal(n), 40, 300)) * env(n, 0.4, 0.4), 1.8, 0.35)

# ---- poison erupts
fx.put(impact(1.3), 6.5, 1.0)
fx.put(braam(3.4, 41), 6.5, 0.85)
n = int(3.6 * SR)
tt = np.arange(n) / SR
dissonant = (np.sin(2 * np.pi * 110 * tt) + np.sin(2 * np.pi * 116.5 * tt) + 0.5 * np.sin(2 * np.pi * 164 * tt)) * env(n, 0.5, 0.8)
fx.put(dissonant, 6.6, 0.25)
for k in range(10):
    fx.put(add(noise_hit(0.08, 200, 2000), thump(110, 0.08, 0.4) * 0.4), 7.6 + k * 0.17, 0.35, -0.7 if k % 2 else 0.7)
fx.put(riser(1.4, 100, 900), 8.8, 0.25)

# ---- Kailash: om drone, conch; Shiva opens his eyes (damaru + bell)
fx.put(sweep(0.6, 3000, 300), 10.0, 0.35)
fx.put(om(3.2), 10.2, 0.35)
fx.put(conch(1.8, 280), 10.4, 0.4)
for x in damaru(11.55, 0.7):
    fx.put(taiko(180), x, 0.25)
fx.put(bell(880, 1.6), 11.6, 0.35)
fx.put(gong(98, 3.0), 11.65, 0.3)

# ---- the drink
fx.put(riser(1.8, 80, 700), 13.5, 0.3)
n = int(1.7 * SR)
swirl = norm(band(rng.standard_normal(n), 300, 3000)) * (0.5 + 0.5 * np.sin(2 * np.pi * np.linspace(2, 9, n) * np.arange(n) / SR))
fx.put(swirl * env(n, 0.3, 0.2), 13.5, 0.4)
fx.put(gulp(0.7), 15.25, 0.9)
fx.put(gulp(0.6), 15.7, 0.7)
fx.put(impact(1.3), 16.1, 1.0)
fx.put(braam(2.4, 49), 16.1, 0.7)
for k, f in enumerate([1046, 1318, 1568, 2093]):
    fx.put(bell(f, 1.2), 16.15 + k * 0.05, 0.18)
fx.put(sweep(0.4, 400, 3000), 16.2, 0.45)
fx.put(gong(110, 3.0), 16.85, 0.35)

# ---- trapped: shimmering pad, slow pulse
for k, f in enumerate([261, 329, 392, 523]):
    fx.put(tone(f, 4.2, 0.3, 0.4), 19.1 + k * 0.08, 0.06)
for b in np.arange(19.4, 23.4, 1.0):
    fx.put(thump(52, 0.5, 0.6), b, 0.45)

# ---- NEELKANTH
fx.put(impact(1.1), 23.6, 0.9)
fx.put(braam(3.0, 55), 23.6, 0.75)
fx.put(gong(98, 4.0), 23.65, 0.45)
fx.put(conch(2.2, 300), 24.1, 0.45)
for k in range(10):
    fx.put(taiko(72 if k % 2 else 60), 24.3 + k * 0.33, 0.55)
for k, f in enumerate([523, 659, 784, 1046]):
    fx.put(bell(f, 1.4), 25.0 + k * 0.3, 0.18)
fx.put(riser(1.6, 90, 800), 28.2, 0.35)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
