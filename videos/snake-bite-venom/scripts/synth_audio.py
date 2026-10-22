"""Deterministic soundtrack for the snake bite video.

Writes the 30s 48kHz stereo SFX track index.html plays (narration support kept but unused):
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
# no narration: the story is told by picture, on-screen text and sound effects only
VO = []


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
    x = norm(read_wav(os.path.join(AUDIO, "vo", name + ".wav")))
    x = x + 0.35 * norm(band(x, 0, 220))
    i = int(t0 * SR)
    vo_mono[i : i + len(x)] += x[: N - i]
vo_mono = reverb(vo_mono, length=1.0, wet=0.18)
vo.x[:, 0] = vo_mono
vo.x[:, 1] = vo_mono
k = int(0.12 * SR)
speech_env = np.convolve(np.abs(vo_mono), np.ones(k) / k, mode="same")
speech_env = np.clip(speech_env / (np.max(speech_env) * 0.25 + 1e-9), 0, 1)
k2 = int(0.25 * SR)
speech_env = np.convolve(speech_env, np.ones(k2) / k2, mode="same")

amb = Bus()
fx = Bus()
t = np.arange(N) / SR


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


# ---- ambience: desert wind outside, low body rumble inside
desert = np.clip(seg(-1, 8.75, 0.3) + seg(26.9, 31, 0.3), 0, 1)
inside = seg(8.5, 27.1, 0.3)
gust = 0.7 + 0.3 * np.sin(2 * np.pi * t / 5.0) * np.sin(2 * np.pi * t / 2.3)
for ch in range(2):
    wind = norm(band(rng.standard_normal(N), 250, 1800)) * gust
    rumble = norm(band(rng.standard_normal(N), 25, 140))
    amb.x[:, ch] += 0.35 * wind * desert + 0.6 * rumble * inside + 0.25 * rumble * desert

# ---- the rattle: AM noise buzz, louder as the boot arrives; same level at 0s and 30s for the loop
def rattle(d, rate=58):
    n = int(d * SR)
    tt = np.arange(n) / SR
    am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rate * tt + 2 * np.sin(2 * np.pi * 3 * tt)))
    return norm(band(rng.standard_normal(n), 2500, 9000)) * am


rat = np.zeros(N)
r = rattle(DUR)
lvl = 0.25 + 0.75 * seg(3.2, 6.9, 0.8) + 0.0 * t
lvl *= np.clip(seg(-1, 7.0, 0.1) + seg(27.4, 31, 0.6), 0, 1)
rat = r * lvl
fx.x[:, 0] += 0.45 * rat
fx.x[:, 1] += 0.35 * rat

# ---- footsteps on sand
def step():
    return add(noise_hit(0.12, 80, 900) * 0.8, thump(90, 0.15, 0.5) * 0.5)


for ts in [3.55, 3.95, 4.35, 4.7]:
    fx.put(step(), ts, 0.7, 0.4)
for ts in [28.55, 28.9, 29.25]:
    fx.put(step(), ts, 0.6, 0.6)

# ---- the strike: whoosh -> slow-mo drone -> impact
fx.put(sweep(0.35, 400, 4000), 4.85, 0.9)
n = int(1.9 * SR)
tt = np.arange(n) / SR
drone = (np.sin(2 * np.pi * 48 * tt) + 0.5 * np.sin(2 * np.pi * 72.5 * tt)) * env(n, 0.3, 0.3)
fx.put(drone, 5.1, 0.45)
fx.put(riser(1.6, 120, 900), 5.25, 0.2)
hit = np.zeros(int(2.4 * SR))
h = thump(40, 1.3, 3.0)
hit[: len(h)] += 1.4 * h
c = noise_hit(0.35, 300, 4000)
hit[: len(c)] += 0.7 * c
fx.put(reverb(hit, 1.6, 0.45, 11), 6.9, 1.0)
# dive into the bite
fx.put(sweep(1.7, 150, 3500), 7.0, 0.55)
fx.put(blip(1320, 0.12), 8.55, 0.25)

# ---- skin: fangs sink (squelch), venom flows (gurgles + drips)
n = int(1.1 * SR)
sq = band(rng.standard_normal(n), 120, 900) * np.exp(-np.arange(n) / (0.35 * SR))
fx.put(norm(sq), 8.75, 0.6)
fx.put(thump(65, 0.6, 1.0), 8.8, 0.5)
for i in range(16):
    fx.put(bubble(0.7 + 0.5 * ((i * 5) % 3) / 3), 9.9 + i * 0.18, 0.45, -0.5 if i % 2 else 0.5)
for td in [10.4, 11.2, 12.0, 12.6]:
    fx.put(bubble(1.8), td, 0.5)
fx.put(sweep(1.0, 300, 2500), 12.75, 0.45)
fx.put(blip(1320, 0.12), 13.55, 0.25)

# ---- blood: heartbeat pulses on the same heart-rate curve as the picture
def RATE(x):
    if x < 18:
        return 1.3
    if x < 21.5:
        return 1.3 + 0.7 * ((x - 18) / 3.5)
    if x < 26.3:
        return 2.0 - 1.0 * min(1, (x - 21.5) / 3.5)
    return 1.0


ph, last, x = 0.0, 0, 0.0
dt = 1 / 120
while x < 27.0:
    ph += RATE(x) * dt
    if x > 13.6 and int(ph) != last:
        pulse = np.concatenate([thump(48, 0.25, 1.0), np.zeros(int(0.08 * SR)), 0.7 * thump(42, 0.25, 0.8)])
        pulse = add(pulse, 0.4 * noise_hit(0.3, 60, 400))
        fx.put(pulse, x, 0.75)
    last = int(ph)
    x += dt

# clot breaking: fizzy crackles
for i in range(14):
    fx.put(noise_hit(0.05, 3000, 9000), 15.9 + i * 0.12 + (i % 3) * 0.02, 0.35, (i % 5 - 2) / 3)
# tissue: cells popping
for i in range(10):
    fx.put(add(noise_hit(0.07, 800, 6000), 0.5 * thump(120, 0.07, 0.5)), 19.5 + i * 0.17, 0.55, (i % 5 - 2) / 3)
fx.put(tone(73, 2.0, 0.4, 0.5), 19.3, 0.3)

# ---- the cure: shimmer + a lock click per antibody
for k, f in enumerate([523, 659, 784, 1046]):
    fx.put(reverb(np.concatenate([bell(f, 1.6), np.zeros(SR)]), 1.4, 0.4), 21.9 + k * 0.12, 0.25)
for i in range(22):
    ta = 22.3 + (i % 20) * 0.16
    fx.put(blip(1760, 0.04), ta, 0.18, (i % 5 - 2) / 3)

# ---- back out to the desert
fx.put(sweep(1.6, 3500, 150), 26.4, 0.6)
fx.put(thump(55, 0.6, 1.2), 27.0, 0.5)

# ------------------------------------------------------------------ mix
duck_amb = 1 - 0.7 * speech_env
duck_fx = 1 - 0.5 * speech_env
sfx = amb.x * 0.6 * duck_amb[:, None] + fx.x * duck_fx[:, None]
sfx = np.tanh(sfx * 1.1) / 1.1
narr = vo.x / (np.max(np.abs(vo.x)) + 1e-9) * 0.95

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
if VO:
    write_wav(os.path.join(AUDIO, "narration.wav"), narr)
mix_db = 20 * np.log10(np.sqrt(np.mean((sfx + narr) ** 2)) + 1e-12)
print(f"wrote sfx.wav{' + narration.wav' if VO else ''} (RMS {mix_db:.1f} dBFS)")
