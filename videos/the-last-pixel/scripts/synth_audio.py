"""Sound for "The Last Pixel" (18 s): sound effects only, no narration.

  python3 scripts/synth_audio.py

8-bit game sounds are synthesised (square-wave jumps, coins, power-ups); the phone side uses the
bundled HyperFrames library (notification, error, chime, glitches) and any Openverse foley in
assets/sfx/ (credited in assets/sfx/CREDITS.md), with procedural fallbacks.
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


# ------------------------------------------------------------------ 8-bit kit
def sq(f, d, duty=0.5):
    n = int(d * SR)
    ph = (np.arange(n) * f / SR) % 1
    return np.where(ph < duty, 1.0, -1.0) * 0.6


def chip_sweep(d, f0, f1, duty=0.5):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f0 * (f1 / f0) ** (tt / d)
    ph = np.cumsum(ff) / SR % 1
    return np.where(ph < duty, 0.6, -0.6) * env(n, 0.003, d * 0.3)


def jump():
    return chip_sweep(0.16, 300, 900, 0.25)


def coin():
    return np.concatenate([sq(988, 0.06) * 0.8, sq(1319, 0.22) * np.linspace(0.8, 0, int(0.22 * SR))])


def notes(fs, d=0.09, duty=0.5, gap=None):
    gap = gap or d
    out = np.zeros(int((gap * len(fs) + d) * SR))
    for i, f in enumerate(fs):
        s = sq(f, d, duty) * env(int(d * SR), 0.003, d * 0.3)
        j = int(i * gap * SR)
        out[j: j + len(s)] += s
    return out


def tick():
    return sq(140, 0.02, 0.25) * np.linspace(1, 0, int(0.02 * SR))


def steps(t0, t1, gap=0.09):
    out, x = [], t0
    while x < t1:
        out.append((x, tick()))
        x += gap
    return out


def tink(f=3200):
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.3 * tt)) * np.exp(-tt * 18)


def crack(k=1.0):
    n = int(0.35 * SR)
    x = np.zeros(n)
    for i in range(int(8 + 14 * k)):
        j = int(hash_(i * 7.7 + k) * n * 0.6)
        x[j: j + 90] += rng.standard_normal(90) * (1 - j / n)
    return norm(band(x, 1500, 10000) + 0.6 * band(rng.standard_normal(n), 2000, 8000) * np.exp(-np.arange(n) / SR * 25))


def shatter():
    out = np.zeros(int(1.4 * SR))
    for i in range(40):
        s = tink(2200 + 3000 * hash_(i)) * (0.3 + 0.7 * hash_(i * 3))
        j = int((hash_(i * 5) ** 2) * 0.9 * SR)
        out[j: j + len(s)] += s[: len(out) - j]
    nh = noise_hit(0.5, 1500, 11000)
    out[: len(nh)] += 1.5 * nh
    return norm(out)


def hash_(i):
    v = np.sin(i * 127.1 + 311.7) * 43758.5453
    return v - np.floor(v)


def buzz(d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = 120 * (1 + 2 * tt / d)
    return norm(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + band(rng.standard_normal(n), 2000, 6000) * 0.3) * env(n, 0.05, 0.1)


def power_down(d=0.8):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = 900 * (0.05) ** (tt / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.3)


amb, fx = Bus(), Bus()
room = norm(band(rng.standard_normal(N), 60, 400))
for ch in range(2):
    amb.x[:, ch] += 0.12 * room * (1 - seg(16.4, 17.2, 0.1))

# ------------------------------------------------------------------ COLD OPEN: the battery heist
for k in range(6):
    fx.put(notes([660 + 40 * k], 0.06, 0.25), 0.1 + 0.18 * k, 0.3)  # tug squeaks
fx.put(braam(1.6, 55), 0.0, 0.4)
fx.put(lib("pop"), 1.24, 0.7)
fx.put(notes([523, 659, 784, 1047, 1319], 0.07), 1.26, 0.35)
fx.put(impact(0.6), 1.25, 0.5)
fx.put(rewind(0.45), 1.42, 0.5)
fx.put(lib("glitch-1", 0.6), 1.45, 0.4)

# ------------------------------------------------------------------ the same old level
for tt_, sig in steps(1.65, 3.6):
    fx.put(sig, tt_, 0.35)
fx.put(jump(), 2.25, 0.45)
for tt_ in [2.5, 3.0, 3.2]:
    fx.put(coin(), tt_, 0.35)
fx.put(notes([392, 370, 349, 330], 0.16, 0.5, 0.18), 3.65, 0.35)  # wah-wah-wah
for tt_, sig in steps(4.2, 5.4, 0.07):
    fx.put(sig, tt_, 0.35)
fx.put(lib("glitch-3", 1.0), 4.55, 0.3)
fx.put(add(thump(90, 0.25, 1.2), sq(110, 0.15) * 0.4 * np.linspace(1, 0, int(0.15 * SR))), 5.4, 0.8)  # BONK
fx.put(tink(3400), 5.62, 0.35)
fx.put(tink(3400), 5.82, 0.35)
for k, tt_ in enumerate([6.05, 6.5, 6.95, 7.4]):
    fx.put(thump(80, 0.2, 1.6), tt_, 0.55)
    fx.put(rec("crack", lambda: crack(0.4 + 0.2 * k)), tt_, 0.25 + 0.12 * k)
fx.put(shatter(), 7.6, 0.75)
fx.put(impact(1.0), 7.6, 0.85)
fx.put(lib("glitch-2", 1.2), 7.62, 0.35)

# ------------------------------------------------------------------ out on the home screen
fx.put(lib("whoosh-short"), 7.75, 0.5)
fx.put(chip_sweep(0.8, 900, 200), 7.9, 0.3)
fx.put(thump(160, 0.12, 0.5), 8.75, 0.5)
for k, tt_ in enumerate([9.2, 9.6, 10.0, 10.4]):
    fx.put(chip_sweep(0.14, 300 + 80 * k, 800 + 160 * k, 0.25), tt_, 0.42)
fx.put(lib("notification"), 9.8, 0.55)
fx.put(chip_sweep(0.35, 200, 1500, 0.5), 10.78, 0.4)  # springboard
for tt_, sig in steps(11.2, 12.35, 0.12):
    fx.put(sig, tt_, 0.3)

# ------------------------------------------------------------------ the battery
for k in range(5):
    fx.put(notes([620 + 50 * k], 0.06, 0.25), 12.45 + 0.11 * k, 0.32)
fx.put(lib("pop"), 12.98, 0.75)
fx.put(notes([523, 659, 784, 1047, 1319, 1568], 0.07), 13.0, 0.38)
fx.put(lib("sparkle"), 13.05, 0.35)
fx.put(buzz(1.0), 13.15, 0.3)
fx.put(chip_sweep(1.0, 200, 1200, 0.25), 13.2, 0.25)
fx.put(lib("error"), 13.95, 0.55)  # LOW BATTERY
for tt_, sig in steps(14.6, 15.8, 0.08):
    fx.put(sig, tt_, 0.3)
fx.put(chip_sweep(0.3, 900, 250), 15.8, 0.35)

# ------------------------------------------------------------------ the phone dies, reboots
fx.put(rec("power_down", power_down), 16.2, 0.6)
fx.put(click(), 16.55, 0.8)
fx.put(lib("chime"), 17.2, 0.4)
for tt_, sig in steps(17.4, 17.95, 0.1):
    fx.put(sig, tt_, 0.3)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.5, makeup_db=5.0)
