"""Shared deterministic sound-effect library for the pixel science shorts.

Usage from a project script:
    import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sfxlib import *
    amb, fx = Bus(), Bus()
    ...place sounds with fx.put(sig, t, gain, pan)...
    master(amb, fx, out_path)
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(1234)
t = np.arange(N) / SR


def read_wav(path):
    with wave.open(path, "rb") as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(float) / 32768
    x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        x = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)
    return x


def write_wav(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X = np.fft.rfft(x)
    lo_g = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) if lo > 0 else 1
    hi_g = 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * lo_g * hi_g, len(x))


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-9)


def env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def reverb(x, length=1.2, wet=0.3, seed=7):
    """Convolution with a decaying-noise impulse response (FFT)."""
    n = int(length * SR)
    ir = np.random.default_rng(seed).standard_normal(n) * np.exp(-np.arange(n) / (length * SR / 5))
    ir = band(ir, 120, 5000)
    ir /= np.sqrt(np.sum(ir ** 2))
    m = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]
    return x + wet * y


class Bus:
    def __init__(self):
        self.x = np.zeros((N, 2))

    def put(self, sig, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= N:
            return
        sig = sig[: N - i]
        l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
        self.x[i : i + len(sig), 0] += sig * gain * l
        self.x[i : i + len(sig), 1] += sig * gain * r


# ------------------------------------------------------------------ sounds
def bubble(size=1.0):
    d = 0.09 * size
    n = int(d * SR)
    tt = np.arange(n) / SR
    freq = (900 / size) * (1 + 2.5 * tt / d)
    return np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt / (d * 0.35))


def click():
    n = int(0.014 * SR)
    return norm(band(rng.standard_normal(n * 4), 2000, 7000))[:n] * np.exp(-np.arange(n) / (0.0025 * SR))


def blip(f=880, d=0.09):
    n = int(d * SR)
    tt = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + np.sign(np.sin(2 * np.pi * f * 1.5 * tt)) * 0.25
    return band(sq, 200, 5000) * env(n, 0.002, d * 0.6)


def sweep(d, f_from, f_to):
    n = int(d * SR)
    x = rng.standard_normal(n)
    y = np.zeros(n)
    blk = 2048
    for s in range(0, n, blk // 2):
        seg = x[s : s + blk]
        fc = f_from * (f_to / f_from) ** (s / n)
        y[s : s + len(seg)] += band(seg, fc * 0.6, fc * 1.6) * np.hanning(len(seg))
    return norm(y) * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5


def thump(f=60, d=0.5, punch=2.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    fr = f * (1 + punch * np.exp(-tt / 0.03))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (d * 0.3))


def heartbeat():
    # lub-dub
    return np.concatenate([thump(50, 0.18, 1.2), np.zeros(int(0.09 * SR)), 0.7 * thump(45, 0.2, 1.0)])


def tone(f, d, a=0.35, r=0.5):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.01 * tt) + 0.2 * np.sin(2 * np.pi * f * 3 * tt)
    return s * env(n, d * a, d * r)


def bell(f, d=2.5):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (1.2 + k)) / k for k in (1, 2.76, 5.4))
    return s * env(n, 0.003, 0.3)


def riser(d, f_from, f_to):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = f_from * (f_to / f_from) ** (tt / d)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    return s * (tt / d) ** 2


def noise_hit(d, lo, hi):
    n = int(d * SR)
    return norm(band(rng.standard_normal(n), lo, hi)) * env(n, 0.003, d * 0.9)


def add(*sigs):
    out = np.zeros(max(len(x) for x in sigs))
    for x in sigs:
        out[: len(x)] += x
    return out


def seg(a, b, fade=0.4):
    e = np.zeros(N)
    i, j = max(0, int(a * SR)), min(N, int(b * SR))
    e[i:j] = 1
    f = int(fade * SR)
    if a > 0:
        e[i : i + f] *= np.linspace(0, 1, f)
    if b < DUR:
        e[j - f : j] *= np.linspace(1, 0, f)
    return e



def master(amb, fx, path, amb_gain=0.6, makeup_db=6.5):
    """Sum buses, soft-clip, look-ahead limit to -1 dBFS, edge fades, write."""
    sfx = amb.x * amb_gain + fx.x
    sfx = np.tanh(sfx * 1.1) / 1.1
    total = sfx * 10 ** (makeup_db / 20)
    peak = np.max(np.abs(total), axis=1)
    win = int(0.01 * SR)
    held = np.array([peak[max(0, i - win) : i + win].max() for i in range(0, N, win)])
    held = np.repeat(held, win)[:N]
    ceiling = 10 ** (-1 / 20)
    gain = np.minimum(1, ceiling / np.maximum(held, 1e-9))
    k = int(0.02 * SR)
    gain = np.convolve(gain, np.ones(k) / k, mode="same")
    gain = np.minimum(gain, ceiling / np.maximum(peak, 1e-9))
    out = sfx * (10 ** (makeup_db / 20) * gain)[:, None]
    fade = int(0.03 * SR)
    out[:fade] *= np.linspace(0, 1, fade)[:, None]
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_wav(path, out)
    db = 20 * np.log10(np.sqrt(np.mean(out ** 2)) + 1e-12)
    print(f"wrote {os.path.basename(path)} (RMS {db:.1f} dBFS, peak {20*np.log10(np.max(np.abs(out))):.1f} dBFS)")
