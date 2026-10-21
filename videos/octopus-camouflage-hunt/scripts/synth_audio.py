"""Deterministic soundtrack for the octopus hunt (no music, no voiceover).

Writes assets/audio/soundtrack.wav (30s, 48kHz, stereo). Event times mirror
the story beats in index.html.
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(1234)
out = np.zeros((N, 2))


def band(x, lo, hi):
    """Brick-ish band-pass in the frequency domain with soft edges."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X = np.fft.rfft(x)
    lo_g = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) if lo > 0 else 1
    hi_g = 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * lo_g * hi_g, len(x))


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def put(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    out[i : i + len(sig), 0] += sig * gain * l
    out[i : i + len(sig), 1] += sig * gain * r


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-9)


# ---- ambience bed: low swell + muffled hiss, periodic so the loop is seamless
t = np.arange(N) / SR
for ch in range(2):
    rumble = norm(band(rng.standard_normal(N), 25, 180))
    hiss = norm(band(rng.standard_normal(N), 300, 1400))
    swell = 0.75 + 0.25 * np.sin(2 * np.pi * t / 7.5 + ch)
    out[:, ch] += (0.30 * rumble + 0.05 * hiss) * swell


def bubble(size=1.0):
    d = 0.09 * size
    n = int(d * SR)
    tt = np.arange(n) / SR
    f0 = 900 / size
    freq = f0 * (1 + 2.5 * tt / d)  # rising chirp, like a real bubble
    ph = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(ph) * np.exp(-tt / (d * 0.35))


def click():
    n = int(0.012 * SR)
    return norm(band(rng.standard_normal(n * 4), 2500, 7000))[:n] * np.exp(-np.arange(n) / (0.002 * SR))


def blip(f=880, d=0.07):
    n = int(d * SR)
    tt = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + np.sign(np.sin(2 * np.pi * f * 1.5 * tt)) * 0.25
    return band(sq, 200, 5000) * env(n, 0.002, d * 0.6)


def sweep(d, f_from, f_to, gain_curve="up"):
    n = int(d * SR)
    x = rng.standard_normal(n)
    # crude moving band via short blocks
    y = np.zeros(n)
    blk = 2048
    for s in range(0, n, blk // 2):
        seg = x[s : s + blk]
        k = s / n
        fc = f_from * (f_to / f_from) ** k
        w = np.hanning(len(seg))
        y[s : s + len(seg)] += band(seg, fc * 0.6, fc * 1.6) * w
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    return norm(y) * e


def thump(f=60, d=0.5):
    n = int(d * SR)
    tt = np.arange(n) / SR
    fr = f * (1 + 2 * np.exp(-tt / 0.03))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (d * 0.3))


def tone(f, d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.01 * tt) + 0.2 * np.sin(2 * np.pi * f * 3 * tt)
    return s * env(n, d * 0.35, d * 0.5)


# ---- caption blips (8-bit, quiet) at each caption pop
for tc, f in [(0.0, 660), (5.0, 660), (10.0, 880), (14.4, 660), (19.3, 990), (23.0, 520), (28.9, 660)]:
    put(blip(f), tc + 0.01, 0.10)

# ---- hook bubbles + blink
for tb, s, p in [(0.6, 1.0, -0.4), (1.3, 0.7, -0.3), (2.0, 1.3, 0.5), (3.4, 0.8, 0.3)]:
    put(bubble(s), tb, 0.35, p)
put(tone(220, 0.25), 2.55, 0.06, 0.3)

# ---- crab walking: leg clicks at the sprite's 10 fps cadence
for k in range(int((8.5 - 4.0) * 10)):
    tc = 4.0 + k * 0.1
    pan = -0.8 + 0.9 * (k / 45)
    put(click(), tc, 0.16 * (0.6 + 0.4 * (k % 2)), pan)
# eye opens
put(tone(110, 0.6), 5.4, 0.18, 0.2)

# ---- dive into the skin (8.5-11) and pull back (13.6-15)
put(sweep(2.5, 120, 1800), 8.5, 0.35)
put(sweep(1.4, 1600, 150), 13.6, 0.3)
# chromatophore pops while the cells flex
for k in range(16):
    tb = 10.2 + k * 0.21
    put(bubble(0.45 + 0.3 * ((k * 7) % 5) / 5), tb, 0.22, ((k * 3) % 7) / 3.5 - 1)

# ---- texture: low creak as papillae rise
n = int(1.2 * SR)
creak = band(rng.standard_normal(n), 60, 400) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * np.linspace(18, 40, n) * np.arange(n) / SR)))
put(norm(creak) * env(n, 0.3, 0.4), 15.8, 0.25)

# ---- crab creeps closer (distant clicks)
for k in range(10):
    put(click(), 17.6 + k * 0.16, 0.08, -0.3)

# ---- strike
put(sweep(0.3, 400, 3000), 19.0, 0.6)
put(thump(55, 0.6), 19.2, 0.9)
put(norm(band(rng.standard_normal(int(0.25 * SR)), 300, 2500)) * env(int(0.25 * SR), 0.005, 0.2), 19.22, 0.35)
for k in range(5):
    put(bubble(0.6 + 0.2 * k), 19.35 + k * 0.08, 0.3, (k - 2) / 3)

# ---- twist: low swell under "colourblind"
put(tone(55, 3.0), 23.0, 0.35)
put(tone(82.5, 3.0), 23.1, 0.12)

# ---- loop: pull back, last bubbles
put(sweep(2.4, 1200, 120), 26.8, 0.22)
for tb, s, p in [(27.6, 1.1, 0.4), (28.3, 0.8, -0.2), (29.2, 1.0, 0.3)]:
    put(bubble(s), tb, 0.3, p)

# ---- master: gentle soft-clip, normalise to -1 dBFS, 30ms edge fades
out = np.tanh(out * 1.2)
out *= 10 ** (-1 / 20) / np.max(np.abs(out))
fade = int(0.03 * SR)
out[:fade] *= np.linspace(0, 1, fade)[:, None]
out[-fade:] *= np.linspace(1, 0, fade)[:, None]

here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, "..", "assets", "audio", "soundtrack.wav")
os.makedirs(os.path.dirname(dst), exist_ok=True)
with wave.open(dst, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
print("wrote", os.path.normpath(dst))
