"""Deterministic soundtrack for the octopus hunt.

Writes two 30s 48kHz stereo tracks that index.html plays together:
  assets/audio/narration.wav  — Kokoro am_onyx lines (assets/audio/vo/*.wav), placed and sweetened
  assets/audio/sfx.wav        — ambience + dramatic SFX, ducked under the narration
Both are scaled by the same factor so their sum peaks at -1 dBFS.
Event times mirror the story beats in index.html.
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 30.0
N = int(SR * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(HERE, "..", "assets", "audio")
rng = np.random.default_rng(1234)

# narration line -> start time (s); each sits inside its caption window
VO = [("vo1", 0.3), ("vo2", 5.1), ("vo3", 10.0), ("vo4", 14.5), ("vo5", 19.75), ("vo6", 23.1)]


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


# ------------------------------------------------------------------ narration
vo = Bus()
vo_mono = np.zeros(N)
for name, t0 in VO:
    x = read_wav(os.path.join(AUDIO, "vo", name + ".wav"))
    x = norm(x)
    x = x + 0.35 * norm(band(x, 0, 220))  # chest / warmth
    i = int(t0 * SR)
    vo_mono[i : i + len(x)] += x[: N - i]
vo_mono = reverb(vo_mono, length=1.0, wet=0.18)
vo.x[:, 0] = vo_mono
vo.x[:, 1] = vo_mono

# envelope for ducking the effects bus under speech
k = int(0.12 * SR)
speech_env = np.convolve(np.abs(vo_mono), np.ones(k) / k, mode="same")
speech_env = np.clip(speech_env / (np.max(speech_env) * 0.25), 0, 1)
k2 = int(0.25 * SR)
speech_env = np.convolve(speech_env, np.ones(k2) / k2, mode="same")

# ------------------------------------------------------------------ effects
amb = Bus()  # ambience: ducked hard under speech
fx = Bus()  # dramatic effects: ducked lightly

t = np.arange(N) / SR
swell = 0.75 + 0.25 * np.sin(2 * np.pi * t / 7.5)
for ch in range(2):
    rumble = norm(band(rng.standard_normal(N), 25, 160))
    hiss = norm(band(rng.standard_normal(N), 300, 1400))
    amb.x[:, ch] += (0.5 * rumble + 0.08 * hiss) * swell
# the breath before the strike: ambience sucks out, then returns with the hit
suck = np.ones(N)
a, b, c = int(18.7 * SR), int(19.2 * SR), int(20.2 * SR)
suck[a:b] = np.linspace(1, 0.1, b - a)
suck[b:c] = np.linspace(0.1, 1, c - b)
amb.x *= suck[:, None]

# caption hits: 8-bit blip + soft sub punch
for tc, f, big in [(0.0, 660, 1), (5.0, 660, 1), (10.0, 880, 0), (14.4, 660, 0), (19.3, 990, 0), (23.0, 520, 1), (28.9, 660, 1)]:
    fx.put(blip(f), tc + 0.01, 0.35)
    if big:
        fx.put(thump(70, 0.35, 1.5), tc, 0.5)

# hook
for tb, s, p in [(0.6, 1.0, -0.4), (1.3, 0.7, -0.3), (2.2, 1.3, 0.5), (3.4, 0.8, 0.3)]:
    fx.put(bubble(s), tb, 0.6, p)
fx.put(tone(220, 0.3), 2.55, 0.2, 0.3)  # the sneaky blink

# crab walk: leg clicks at the sprite's 10 fps cadence
for i in range(45):
    fx.put(click(), 4.0 + i * 0.1, 0.45 * (0.6 + 0.4 * (i % 2)), -0.8 + 0.9 * (i / 45))
# eye snaps open
fx.put(tone(110, 0.7, 0.1, 0.6), 5.4, 0.45)
fx.put(sweep(0.4, 300, 1200), 5.3, 0.25)

# heartbeat tension: 6s -> strike, accelerating
tb = 6.0
gap = 1.05
while tb < 18.9:
    if not (8.4 < tb < 9.0):
        fx.put(heartbeat(), tb, 0.55 + 0.35 * (tb - 6) / 13)
    tb += gap
    gap = max(0.42, gap * 0.94)

# dive into the skin and back out
fx.put(sweep(2.5, 120, 2200), 8.5, 0.6)
fx.put(riser(2.4, 80, 300), 8.6, 0.12)
fx.put(sweep(1.4, 1800, 150), 13.6, 0.5)
for i in range(18):
    fx.put(bubble(0.45 + 0.3 * ((i * 7) % 5) / 5), 10.1 + i * 0.2, 0.4, ((i * 3) % 7) / 3.5 - 1)

# texture: creak as the spikes rise
n = int(1.2 * SR)
creak = band(rng.standard_normal(n), 60, 500) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * np.linspace(18, 40, n) * np.arange(n) / SR)))
fx.put(norm(creak) * env(n, 0.3, 0.4), 15.8, 0.55)
fx.put(tone(98, 1.2, 0.5, 0.4), 15.9, 0.25)

# the approach: closer clicks + riser into the hit
for i in range(10):
    fx.put(click(), 17.6 + i * 0.16, 0.3, -0.3)
fx.put(riser(1.5, 110, 880), 17.7, 0.22)
fx.put(sweep(1.5, 200, 4000), 17.7, 0.35)

# STRIKE
strike = np.zeros(int(2.5 * SR))
w = sweep(0.3, 500, 3500)
strike[: len(w)] += 0.8 * w
h = thump(42, 1.4, 3.0)
o = int(0.2 * SR)
strike[o : o + len(h)] += 1.4 * h
s = noise_hit(0.5, 200, 3000)
strike[o : o + len(s)] += 0.6 * s
strike = reverb(strike, length=1.6, wet=0.45, seed=11)
fx.put(strike, 19.0, 1.0)
for i in range(6):
    fx.put(bubble(0.6 + 0.2 * i), 19.35 + i * 0.07, 0.5, (i - 2.5) / 3)

# twist: low drone + reveal bell under "colourblind"
fx.put(tone(55, 3.2), 22.9, 0.6)
fx.put(tone(82.5, 3.2), 23.0, 0.2)
fx.put(reverb(np.concatenate([bell(660), np.zeros(SR)]), 1.5, 0.4), 23.85, 0.35)

# loop: pull back, bubbles, soft landing
fx.put(sweep(2.4, 1400, 120), 26.8, 0.45)
for tb, s, p in [(27.6, 1.1, 0.4), (28.3, 0.8, -0.2), (29.3, 1.0, 0.3)]:
    fx.put(bubble(s), tb, 0.55, p)

# ------------------------------------------------------------------ mix
duck_amb = 1 - 0.7 * speech_env
duck_fx = 1 - 0.5 * speech_env
sfx = amb.x * 0.55 * duck_amb[:, None] + fx.x * duck_fx[:, None]
sfx = np.tanh(sfx * 1.1) / 1.1
narr = vo.x / np.max(np.abs(vo.x)) * 0.95

# shared look-ahead limiter: +3.5 dB of make-up gain, peaks held at -1 dBFS
total = (sfx + narr) * 10 ** (3.5 / 20)
peak = np.max(np.abs(total), axis=1)
win = int(0.01 * SR)
held = np.array([peak[max(0, i - win) : i + win].max() for i in range(0, N, win)])
held = np.repeat(held, win)[:N]
ceiling = 10 ** (-1 / 20)
gain = np.minimum(1, ceiling / np.maximum(held, 1e-9))
k = int(0.02 * SR)
gain = np.convolve(gain, np.ones(k) / k, mode="same")
gain = np.minimum(gain, ceiling / np.maximum(peak, 1e-9))
scale = 10 ** (3.5 / 20) * gain[:, None]
sfx = sfx * scale
narr = narr * scale
fade = int(0.03 * SR)
for x in (sfx, narr):
    x[:fade] *= np.linspace(0, 1, fade)[:, None]
    x[-fade:] *= np.linspace(1, 0, fade)[:, None]

write_wav(os.path.join(AUDIO, "sfx.wav"), sfx)
write_wav(os.path.join(AUDIO, "narration.wav"), narr)
mix_db = 20 * np.log10(np.sqrt(np.mean((sfx + narr) ** 2)) + 1e-12)
print(f"wrote sfx.wav + narration.wav (combined RMS {mix_db:.1f} dBFS)")
