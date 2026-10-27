"""Sound for "Raindrop Race" (18 s): sound effects only, no narration.

  python3 scripts/synth_audio.py

Real foley from assets/sfx/*.wav when present (Openverse CC0/CC BY, credited in assets/sfx/CREDITS.md)
plus the bundled HyperFrames library; everything else is procedural (sfxlib + the race kit below).
"""
import os
import sys

DUR = 18.0
os.environ["SFX_DUR"] = str(DUR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def rec(name, fallback, dur=None):
    x = load(os.path.join(ROOT, "assets", "sfx", name + ".wav"), dur=dur)
    return fallback() if x is None else fade_out(x, 0.1)


def lib(name, dur=None):
    return load(os.path.join(LIB, name + ".mp3"), dur=dur)


# ------------------------------------------------------------------ race kit
def engine(d, f0, f1, rough=0.3):
    """Tiny F1 engine: buzzy saw + square, pitch gliding f0 -> f1, with firing-rate grit."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f0 * (f1 / f0) ** (tt / d)
    ph = np.cumsum(ff) / SR
    x = (2 * (ph % 1) - 1) + 0.5 * np.sign(np.sin(2 * np.pi * ph * 2)) + 0.3 * np.sin(2 * np.pi * ph * 3)
    x *= 1 + rough * np.sign(np.sin(2 * np.pi * ph * 0.5))
    return norm(band(x, 150, 5000)) * env(n, 0.04, min(0.2, d * 0.3))


def passby(d, f, pan_from=-1.0):
    """Engine whizzing past: pitch drops through the pass (doppler), loudness peaks in the middle."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    k = tt / d
    ff = f * (1.25 - 0.5 / (1 + np.exp(-(k - 0.5) * 12)))
    ph = np.cumsum(ff) / SR
    x = (2 * (ph % 1) - 1) + 0.5 * np.sign(np.sin(2 * np.pi * ph * 2))
    return norm(band(x, 150, 5000)) * np.exp(-((k - 0.5) ** 2) / 0.05)


def beep(f, d=0.22):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return (np.sign(np.sin(2 * np.pi * f * tt)) * 0.6 + np.sin(2 * np.pi * f * tt) * 0.4) * env(n, 0.005, 0.03)


def squeak(d, f=1900):
    """Wet rubber blade dragging on glass."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.15 * np.sin(2 * np.pi * 7 * tt) + 0.05 * rng.standard_normal(n).cumsum() / np.sqrt(n) * 0)
    stick = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 38 * tt))
    s = np.sin(2 * np.pi * np.cumsum(ff) / SR) * stick + 0.4 * band(rng.standard_normal(n), 1500, 4000)
    return norm(s) * np.sin(np.pi * tt / d) ** 0.6


def clunk():
    return norm(add(thump(70, 0.25, 1.5), 0.7 * noise_hit(0.08, 300, 2500), 0.4 * thump(160, 0.1, 0.5)))


def slide_down(d=0.6, f0=1400, f1=300):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f0 * (f1 / f0) ** (tt / d) * (1 + 0.02 * np.sin(2 * np.pi * 6 * tt))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env(n, 0.02, 0.15)


def splat():
    return norm(add(thump(110, 0.15, 1.0), 0.8 * noise_hit(0.12, 600, 6000)))


def crowd(d):
    """Stadium roar stand-in: many band-limited noise voices with slow swells."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(6):
        x += band(rng.standard_normal(n), 300 + 120 * k, 1200 + 300 * k) * (0.7 + 0.3 * np.sin(2 * np.pi * (0.7 + 0.3 * k) * tt + k))
    return norm(x) * env(n, 0.25, 0.6)


def sizzle(d):
    n = int(d * SR)
    x = band(rng.standard_normal(n), 3000, 11000)
    crack = np.zeros(n)
    for i in range(int(d * 60)):
        j = int(hash_(i) * (n - 200))
        crack[j: j + 120] += rng.standard_normal(120) * 0.8
    return norm(x * 0.6 + band(crack, 1500, 9000)) * env(n, 0.2, 0.4)


def boing(f=300, d=0.4):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.6 * np.sin(2 * np.pi * 9 * tt) * np.exp(-tt * 6))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-tt * 5)


def hash_(i):
    v = np.sin(i * 127.1 + 311.7) * 43758.5453
    return v - np.floor(v)


def wind(d, lo=200, hi=1500):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return norm(band(rng.standard_normal(n), lo, hi)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.6 * tt))


amb, fx = Bus(), Bus()

# ------------------------------------------------------------------ ambience beds
rain = loop_to(load(os.path.join(ROOT, "assets", "sfx", "rain_window.wav")), N)
if rain is None:
    rain = norm(band(rng.standard_normal(N), 2000, 9000))
    for i in range(160):  # drips tapping the glass
        tap = noise_hit(0.02, 2500, 7000) * (0.3 + 0.7 * hash_(i))
        j = int(hash_(i * 3.3) * (N - len(tap)))
        rain[j: j + len(tap)] += tap * 1.5
airy = wind(DUR, 250, 1400)
for ch in range(2):
    amb.x[:, ch] += 0.4 * rain * (seg(0, 1.6, 0.05) + seg(6.5, 12.9, 0.2))
    amb.x[:, ch] += 0.45 * airy * (seg(1.6, 4.0, 0.3) + seg(16.2, 18.0, 0.3))
    amb.x[:, ch] += 0.8 * wind(DUR, 300, 2400) * seg(3.6, 6.6, 0.3)  # the dive

# ------------------------------------------------------------------ COLD OPEN: the wiper over the leaders
fx.put(impact(0.9), 0.0, 0.8)
fx.put(engine(1.6, 520, 640), 0.0, 0.35, -0.4)
fx.put(engine(1.6, 470, 600), 0.0, 0.3, 0.4)
fx.put(clunk(), 0.15, 0.5)
fx.put(squeak(1.0, 1700), 0.45, 0.4, 0.2)
fx.put(lib("whoosh-short"), 0.8, 0.55)
fx.put(braam(1.8, 52), 0.85, 0.5)
fx.put(rewind(0.45), 1.42, 0.55)
fx.put(lib("glitch-1", 0.6), 1.45, 0.35)

# ------------------------------------------------------------------ the grid in the cloud
THUNDER = rec("thunder", lambda: impact(0.6))
fx.put(THUNDER, 1.8, 0.45)
fx.put(engine(1.6, 140, 330, 0.6), 1.85, 0.35)  # revving
for k, tt_ in enumerate([2.2, 2.6, 3.0]):
    fx.put(beep(620), tt_, 0.4)
fx.put(beep(1240, 0.4), 3.45, 0.45)
fx.put(lib("whoosh"), 3.45, 0.6)
fx.put(engine(0.9, 420, 900), 3.45, 0.4)

# ------------------------------------------------------------------ the dive
fx.put(sweep(2.4, 400, 3000), 4.0, 0.35)
for k, tt_ in enumerate([4.45, 5.25, 5.85]):
    fx.put(lib("whoosh-short"), tt_, 0.45, (-1) ** k * 0.6)
fx.put(thump(240, 0.18, 1.2), 5.02, 0.6)  # BONK
fx.put(boing(300), 5.05, 0.4)
fx.put(riser(0.9, 200, 1400), 5.7, 0.25)
fx.put(impact(0.8), 6.6, 0.85)
for k, p in enumerate([0.0, -0.6, 0.6]):
    fx.put(rec("drip", splat), 6.6 + 0.06 * k, 0.6, p)

# ------------------------------------------------------------------ the windscreen GP
fx.put(engine(5.5, 300, 520), 6.9, 0.22, 0.0)
fx.put(engine(5.5, 280, 480), 6.95, 0.18, -0.5)
fx.put(engine(4.0, 260, 330), 6.95, 0.14, 0.5)
fx.put(rec("gulp", lambda: bubble(2.0)), 8.18, 0.5, -0.4)  # the rival swallows a droplet: boost
fx.put(passby(1.0, 600), 8.2, 0.45, -0.4)
fx.put(lib("whoosh-short"), 8.25, 0.4, -0.4)
fx.put(clunk(), 10.55, 0.8)  # wiper motor
fx.put(squeak(0.55, 1800), 10.6, 0.45, -0.2)
fx.put(squeak(0.55, 1600), 11.15, 0.45, 0.2)
fx.put(lib("whoosh"), 10.65, 0.5)
fx.put(lib("whoosh"), 11.2, 0.45)
fx.put(slide_down(0.7, 1500, 260), 10.95, 0.35, 0.6)  # the underdog flung off
fx.put(braam(1.6, 58), 10.6, 0.45)
fx.put(bubble(2.2), 11.78, 0.55)  # hero takes the boost droplet
fx.put(passby(0.9, 700), 11.8, 0.55)
fx.put(riser(0.6, 300, 1800), 11.85, 0.3)
fx.put(impact(1.0), 12.45, 0.85)  # FINISH
fx.put(bell(1568, 1.6), 12.47, 0.3)
fx.put(bell(2093, 1.6), 12.55, 0.25)
CROWD = rec("crowd", lambda: crowd(3.5), dur=3.5)
fx.put(CROWD, 12.45, 0.45)

# ------------------------------------------------------------------ podium, sun, evaporation
fx.put(lib("pop"), 13.15, 0.45)  # bottle pops
fx.put(noise_hit(0.9, 3000, 9000), 13.2, 0.3)  # spray fizz
for k, f in enumerate([523, 659, 784, 1047, 1319]):
    fx.put(bell(f, 2.5), 13.7 + 0.08 * k, 0.12)  # the clouds part
fx.put(shing(0.7), 13.9, 0.35)
fx.put(rec("sizzle", lambda: sizzle(1.6), dur=1.8), 14.35, 0.45)
fx.put(sizzle(1.4), 14.6, 0.2)
fx.put(riser(1.6, 300, 2000), 14.9, 0.2)
fx.put(sweep(1.8, 300, 4000), 15.0, 0.35)

# ------------------------------------------------------------------ back in the cloud: again
fx.put(lib("sparkle"), 16.6, 0.4)
for tt_ in [17.0, 17.25, 17.5]:
    fx.put(beep(620), tt_, 0.4)
fx.put(beep(1240, 0.3), 17.78, 0.45)
fx.put(engine(0.3, 300, 700), 17.7, 0.35)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.45, makeup_db=4.0)
