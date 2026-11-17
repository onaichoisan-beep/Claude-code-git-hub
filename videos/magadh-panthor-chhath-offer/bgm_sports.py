"""Synthesised sports-anthem BGM: stadium stomp-stomp-clap, rock drums, distorted power chords,
brass stabs, tom fills, crowd bed; big impact at the logo outro. Also writes whoosh SFX."""
import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys

SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 50.6
OUTRO = DUR - 3.0
BPM = 120.0
B = 60 / BPM
N = int(DUR * SR)
rng = np.random.default_rng(11)
dry = np.zeros((N, 2)); wet = np.zeros((N, 2))


def put(buf, sig, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    s = sig[:N - i] * g
    buf[i:i + len(s), 0] += s * np.sqrt(0.5 * (1 - pan)); buf[i:i + len(s), 1] += s * np.sqrt(0.5 * (1 + pan))


def add(sig, t, g=1.0, pan=0.0, send=0.0):
    put(dry, sig, t, g, pan)
    if send: put(wet, sig, t, g * send, pan)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def filt(x, kind, f, order=2):
    b, a = ss.butter(order, np.array(f) / (SR / 2), kind); return ss.lfilter(b, a, x)


noise = lambda n: rng.standard_normal(n)
midi = lambda m: 440 * 2 ** ((m - 69) / 12)


def kick():
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 48 + 120 * np.exp(-t * 30)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.2)) + filt(noise(n), 'high', 3000) * env(n, 0.0005, 0.004) * 0.4


def snare():
    n = int(0.4 * SR); t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * (185 + 40 * np.exp(-t * 40)) * t) * env(n, 0.001, 0.06)
    nz = filt(noise(n), 'band', [1200, 8000]) * env(n, 0.001, 0.12)
    return (tone * 0.7 + nz) * 0.8


def stomp():
    n = int(0.6 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-t * 25)) / SR) * env(n, 0.002, 0.18)
    wood = filt(noise(n), 'band', [90, 500]) * env(n, 0.002, 0.06)
    return body + wood * 0.8


def clap():  # a crowd of claps, slightly spread
    n = int(0.35 * SR); x = np.zeros(n)
    for k in range(7):
        d = int(rng.uniform(0, 0.022) * SR)
        c = filt(noise(n), 'band', [rng.uniform(800, 1300), rng.uniform(2500, 5000)]) * env(n, 0.001, rng.uniform(0.03, 0.06))
        x[d:] += c[:n - d]
    return x * 0.35


def hat(op=False):
    n = int((0.3 if op else 0.07) * SR)
    return filt(noise(n), 'high', 7500) * env(n, 0.0005, 0.12 if op else 0.02) * 0.3


def tom(f0):
    n = int(0.5 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.6 * np.exp(-t * 20))) / SR) * env(n, 0.001, 0.22) + filt(noise(n), 'band', [200, 2000]) * env(n, 0.001, 0.03) * 0.3


def saw(f, n, det=(0.0,)):
    t = np.arange(n) / SR
    return sum(ss.sawtooth(2 * np.pi * f * (1 + d) * t + rng.uniform(0, 6)) for d in det) / len(det)


def guitar(root, n, mute=True):
    x = sum(saw(midi(m), n, (-0.003, 0.004)) for m in (root, root + 7, root + 12))
    x = filt(x, 'high', 90)
    x = np.tanh(x * 6) * 0.6
    x = filt(x, 'low', 3200 if not mute else 1800, 4)
    return x * env(n, 0.003, 0.09 if mute else 0.8)


def brass(notes, n):
    t = np.arange(n) / SR
    x = sum(saw(midi(m), n, (-0.005, 0.0, 0.006)) for m in notes)
    fc = 600 + 2600 * np.exp(-t * 6)
    y = np.zeros(n); seg = 256; zi = None
    for i in range(0, n, seg):  # time-varying low-pass
        b, a = ss.butter(2, min(fc[i], 18000) / (SR / 2))
        y[i:i + seg] = ss.lfilter(b, a, x[i:i + seg])
    return y * env(n, 0.02, 0.35)


# E minor anthem: E5 E5 C5 D5
PROG = [40, 40, 36, 38]
CHORD = {40: [64, 67, 71], 36: [64, 67, 72], 38: [62, 66, 69]}
BAR = 4 * B
nb = int(np.ceil(DUR / BAR))
for b in range(nb):
    t0 = b * BAR
    if t0 >= OUTRO: break
    root = PROG[b % 4]
    intro = b < 1
    for k in range(8):  # 8th grid
        tt = t0 + k * B / 2
        if tt >= OUTRO: break
        # stadium stomp-stomp-clap on every bar
        if k in (0, 1, 4, 5): add(stomp(), tt, 0.55, 0, 0.5)
        if k in (2, 6): add(clap(), tt, 0.75, 0.05, 0.6)
        if intro: continue
        if k in (0, 3, 4): add(kick(), tt, 0.6)
        if k in (2, 6): add(snare(), tt, 0.45, 0, 0.35)
        add(hat(k == 7), tt, 0.5 if k % 2 == 0 else 0.35, 0.35)
        # chugging power chords + bass
        n = int(B / 2 * SR)
        add(guitar(root, n, mute=k not in (0,)), tt, 0.22, -0.4)
        add(guitar(root, n, mute=k not in (0,)), tt + 0.012, 0.22, 0.4)
        add(filt(saw(midi(root - 12), n), 'low', 300) * env(n, 0.003, 0.15), tt, 0.35)
    if not intro and b % 2 == 0:
        add(brass(CHORD[root], int(BAR * 0.45 * SR)), t0, 0.07, 0, 0.3)
    if b % 4 == 3 and not intro:  # tom fill on the last beat
        for j, f in enumerate((210, 170, 135, 100)):
            add(tom(f), t0 + 3 * B + j * B / 4, 0.4, -0.3 + j * 0.2, 0.3)

# crowd bed (soft) with cheer swells at start and outro
cn = filt(noise(N), 'band', [350, 2600])
mod = 0.6 + 0.4 * filt(noise(N), 'low', 2) * 30
tt = np.arange(N) / SR
swell = 0.25 + 0.9 * np.exp(-tt / 1.5) + 1.3 * np.exp(-((tt - OUTRO - 0.6) / 0.9) ** 2)
crowd = cn * np.clip(mod, 0.2, 1.4) * swell * 0.05
dry[:, 0] += crowd; dry[:, 1] += np.roll(crowd, 300)

# riser into outro + big impact
rn = int(2.0 * SR)
riser = filt(noise(rn), 'band', [1500, 9000]) * np.linspace(0, 1, rn) ** 3
add(riser, OUTRO - 2.0, 0.12)
n = int(3.0 * SR); t = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(36 + 70 * np.exp(-t * 5)) / SR) * env(n, 0.002, 1.0)
add(boom, OUTRO, 0.7); add(kick(), OUTRO, 0.7); add(clap(), OUTRO, 0.9, 0, 0.8)
add(filt(noise(n), 'high', 2500) * env(n, 0.001, 1.1) * 0.35, OUTRO, 1.0, 0, 0.6)
add(brass(CHORD[40] + [52], int(2.8 * SR)) * np.linspace(1, 0.3, int(2.8 * SR)), OUTRO, 0.12, 0, 0.5)

# stadium reverb: exponentially decaying noise IR
irn = int(1.4 * SR)
ir = noise(irn) * np.exp(-np.arange(irn) / SR / 0.35)
ir = filt(ir, 'low', 6000) / np.sqrt((ir ** 2).sum())
for c in range(2):
    dry[:, c] += ss.fftconvolve(wet[:, c], np.roll(ir, c * 97), 'full')[:N] * 0.9

out = dry
fi = int(0.05 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.0 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
out = np.tanh(out / np.abs(out).max() * 1.4) / np.tanh(1.4) * 0.9
wf.write('bgm_sports.wav', SR, (out * 32767).astype(np.int16))
print('ok')
