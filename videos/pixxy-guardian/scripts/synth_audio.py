"""Cinematic sound effects for PIXXY (no narration, no text sounds).

Hit points follow the cut/impact rhythm of the reference spot: car glare ~0.6-1.6s, cut whoosh 2.27,
light-beam hit 4.07-4.4, train 8.1-9.2, crash 14.6, bus rumble 16.3-17.3, final hit 18.27.
Every sound is synthesised here; nothing is taken from the reference audio.
"""
import os
import sys

os.environ["SFX_DUR"] = "19.2"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def screech(d=0.6, f=2600):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.04 * np.sin(2 * np.pi * 38 * tt))) / SR)
    return norm(s * 0.4 + band(rng.standard_normal(n), 1800, 5000)) * env(n, 0.02, d * 0.5)


def horn(d=0.5, f1=350, f2=440):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * f1 * tt)) + np.sign(np.sin(2 * np.pi * f2 * tt))
    return norm(band(s, 200, 3000)) * env(n, 0.01, 0.08)


def engine(d, f0, f1):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (tt / d)
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    return norm(band(saw, 30, 700) + 0.4 * band(rng.standard_normal(n), 40, 300)) * env(n, d * 0.6, d * 0.25)


def shimmer(d=1.4, f=1320):
    """Angelic arrival: stacked bell partials + airy noise."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * m * tt) * np.exp(-tt * (2 + m)) for m in (1, 1.5, 2, 3))
    air = band(rng.standard_normal(n), 4000, 11000) * np.exp(-tt * 3)
    return norm(reverb(s + 0.5 * air, 1.5, 0.5, 3)) * env(n, 0.01, 0.4)


def arrive(t0, g=1.0):
    fx.put(sweep(0.35, 400, 6000), t0 - 0.3, 0.45 * g)
    fx.put(shimmer(), t0, 0.35 * g)
    fx.put(sub_drop(0.8, 70, 30), t0, 0.45 * g)


# ---- ambience: steady rain + low city hum, airy angelic pad that swells at each rescue
for ch in range(2):
    rain = norm(band(rng.standard_normal(N), 900, 9000))
    hum = norm(band(rng.standard_normal(N), 35, 160))
    amb.x[:, ch] += (0.5 * rain + 0.45 * hum) * seg(0, 18.27, 0.05)
pad = sum(np.sin(2 * np.pi * f * t + k) for k, f in enumerate([146.8, 220.0, 293.7, 369.9, 440.0]))
pad *= 1 + 0.05 * np.sin(2 * np.pi * 0.3 * t)
swell = np.full(N, 0.35)
for a in [1.0, 2.9, 4.4, 6.5, 8.4, 10.8, 12.5, 14.7, 17.2]:
    swell += 0.5 * np.exp(-np.maximum(0, t - a) / 0.9) * (t >= a)
amb.x[:, 0] += 0.22 * norm(pad) * swell * seg(0, 18.27, 0.1)
amb.x[:, 1] += 0.22 * norm(pad) * swell * seg(0, 18.27, 0.1)

# ---- 1. crossing: car roars in, brakes screech, flash, guardian blooms
fx.put(engine(1.0, 60, 140), 0.0, 0.6, 0.5)
fx.put(screech(0.6), 0.45, 0.45, 0.3)
fx.put(add(impact(0.8), noise_hit(0.15, 2000, 10000)), 0.9, 0.85)
fx.put(braam(1.8, 49), 0.9, 0.55)
fx.put(shimmer(1.6, 1175), 0.95, 0.4)
fx.put(sweep(0.4, 6000, 500), 2.0, 0.35)

# ---- 2. scaffold: whoosh into the cut, falling wind, caught
fx.put(sweep(0.4, 300, 5000), 2.1, 0.55)
fx.put(sweep(0.45, 2000, 300), 2.5, 0.35)
arrive(2.92, 0.9)
fx.put(thump(70, 0.4, 1.5), 2.92, 0.5)

# ---- 3. pillar of light slams down; steel beam drops and is held
fx.put(add(impact(1.2), shing(0.6)), 4.07, 0.95)
fx.put(braam(2.0, 41), 4.07, 0.6)
fx.put(sweep(0.2, 3000, 800), 4.6, 0.3)
fx.put(add(noise_hit(0.25, 300, 6000), thump(90, 0.4, 1.0)), 4.82, 0.7)
fx.put(bell(2093, 1.2), 4.84, 0.18)

# ---- 4. wet stairs: slip, tumble, cushioned
fx.put(sweep(0.4, 300, 5000), 5.75, 0.5)
fx.put(noise_hit(0.08, 1500, 7000), 6.25, 0.35)
fx.put(sweep(0.35, 1800, 300), 6.3, 0.3)
arrive(6.5, 0.8)

# ---- 5. platform: train horn + rumble, flash save, train rushes past
fx.put(horn(0.9, 220, 277), 8.1, 0.35, -0.5)
n = int(1.6 * SR)
rumble = norm(band(rng.standard_normal(n), 30, 400)) * np.sin(np.pi * np.linspace(0, 1, n))
fx.put(rumble, 8.3, 0.8)
fx.put(add(impact(0.7), shing(0.5)), 8.36, 0.75)
fx.put(shimmer(1.2, 1397), 8.38, 0.35)
fx.put(sweep(1.0, 200, 3000), 8.9, 0.5, -0.6)
for k in range(8):
    fx.put(noise_hit(0.05, 400, 3000), 8.95 + k * 0.11, 0.18, 0.6 - k * 0.15)

# ---- 6. flowerpot: wobble, fall whistle, caught
fx.put(sweep(0.4, 300, 5000), 9.7, 0.45)
fx.put(add(click(), click()), 9.95, 0.4)
fx.put(riser(0.6, 1800, 500), 10.15, 0.2)
arrive(10.76, 0.9)
fx.put(thump(110, 0.25, 1.0), 10.76, 0.4)

# ---- 7. car door: bike bell, door click, door slammed shut by the guardian
fx.put(sweep(0.4, 300, 5000), 11.65, 0.45)
fx.put(bell(2400, 0.6), 11.95, 0.2)
fx.put(add(click(), noise_hit(0.05, 800, 4000)), 12.2, 0.4)
arrive(12.4, 0.8)
fx.put(add(thump(80, 0.3, 1.2), noise_hit(0.08, 300, 3000)), 12.55, 0.6)

# ---- 8. motorbike: engine whine, skid, crash, caught
fx.put(engine(1.0, 90, 220), 13.6, 0.5)
fx.put(screech(0.5, 3100), 14.4, 0.4)
fx.put(add(impact(1.3), noise_hit(0.3, 300, 9000)), 14.6, 1.0)
fx.put(braam(2.0, 44), 14.6, 0.55)
for k in range(10):
    fx.put(noise_hit(0.04, 3000, 10000), 14.6 + k * 0.09, 0.15, (k % 5 - 2) / 3)
fx.put(shimmer(1.6, 1175), 14.7, 0.4)

# ---- 9. POV bus: deep engine rumble and horn, light swells behind you
fx.put(engine(1.4, 40, 70), 15.9, 0.75)
fx.put(horn(0.7, 300, 380), 16.4, 0.35)
fx.put(riser(1.2, 120, 1400), 16.0, 0.3)
fx.put(sweep(0.4, 500, 8000), 16.85, 0.4)

# ---- 10. reveal: big hit, choir shimmer, white-out, cut to black
fx.put(add(impact(1.3), shing(0.7)), 17.2, 0.9)
fx.put(braam(1.2, 55), 17.2, 0.45)
for k, f in enumerate([1047, 1319, 1568, 2093]):
    fx.put(bell(f, 1.5), 17.3 + k * 0.12, 0.15)
fx.put(riser(1.0, 300, 3000), 17.25, 0.25)
fx.put(add(impact(1.0), sub_drop(0.9)), 18.27, 0.9)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"), amb_gain=0.45, makeup_db=4.5)
