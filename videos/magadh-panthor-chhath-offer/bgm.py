"""Synthesised BGM: festive dhol groove + epic sports bed (D minor), plus whoosh/hit SFX."""
import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys, json

SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 50.6
BPM = 112.0
BEAT = 60 / BPM
N = int(DUR * SR)
rng = np.random.default_rng(7)
out = np.zeros((N, 2))


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    out[i:i + len(s), 0] += s * np.sqrt(0.5 * (1 - pan))
    out[i:i + len(s), 1] += s * np.sqrt(0.5 * (1 + pan))


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def bp(x, lo, hi, order=2):
    b, a = ss.butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band'); return ss.lfilter(b, a, x)


def lp(x, f, order=2):
    b, a = ss.butter(order, f / (SR / 2)); return ss.lfilter(b, a, x)


def hp(x, f, order=2):
    b, a = ss.butter(order, f / (SR / 2), 'high'); return ss.lfilter(b, a, x)


# ---- drum voices ----
def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.16) * 1.0


def dagga():  # dhol bass side
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 62 + 70 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.2)
    slap = bp(rng.standard_normal(n), 150, 900) * env(n, 0.0005, 0.02) * 0.6
    return body + slap


def tilli():  # dhol treble stick
    n = int(0.18 * SR); t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 420 * t) * env(n, 0.0005, 0.03)
    crack = bp(rng.standard_normal(n), 1800, 6000) * env(n, 0.0003, 0.012) * 1.6
    return (tone * 0.5 + crack) * 0.6


def clap():
    n = int(0.3 * SR)
    x = bp(rng.standard_normal(n), 900, 3500) * env(n, 0.001, 0.07)
    for d in (0.008, 0.017):
        k = int(d * SR); x[k:] += x[:-k] * 0.5
    return x * 0.5


def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    return hp(rng.standard_normal(n), 7000) * env(n, 0.0005, 0.08 if open_ else 0.018) * 0.25


def saw(freq, n, detune=(0.0,)):
    t = np.arange(n) / SR; s = 0
    for d in detune:
        s = s + ss.sawtooth(2 * np.pi * freq * (1 + d) * t + rng.uniform(0, 6))
    return s / len(detune)


def midi(m): return 440 * 2 ** ((m - 69) / 12)


# D minor epic: Dm - Bb - F - C  (one chord per bar)
CH = [(50, [62, 65, 69]), (46, [62, 65, 70]), (53, [60, 65, 69]), (48, [60, 64, 67])]
BAR = 4 * BEAT
nbars = int(np.ceil(DUR / BAR)) + 1
OUTRO = DUR - 3.0  # big hit on the logo outro

for b in range(nbars):
    t0 = b * BAR
    if t0 >= DUR: break
    root, notes = CH[b % 4]
    full = t0 >= BAR * 1 and t0 < OUTRO
    # pad (every bar, slow attack)
    n = int(BAR * SR) + int(0.4 * SR)
    pad = sum(saw(midi(m), n, (-0.006, 0.0, 0.007)) for m in notes)
    pad = lp(pad, 1400 if full else 900) * env(n, 0.25, 3.0)
    add(pad, t0, 0.05, -0.1)
    if t0 >= OUTRO: continue
    # bass: 8th-note pulse on root
    for k in range(8):
        tt = t0 + k * BEAT / 2
        if tt >= OUTRO: break
        nn = int(BEAT / 2 * SR * 0.9)
        f = midi(root - 12) * (2 if k in (3, 7) else 1)
        s = lp(saw(f, nn, (-0.004, 0.004)), 380) * env(nn, 0.004, 0.18)
        add(s, tt, 0.20 if full else 0.08)
    # drums
    for k in range(16):  # 16ths
        tt = t0 + k * BEAT / 4
        if tt >= OUTRO: break
        if full:
            if k in (0, 8): add(kick(), tt, 0.55)
            if k in (4, 12): add(clap(), tt, 0.35, 0.05)
            add(hat(k % 4 == 2), tt, 0.5 if k % 2 == 0 else 0.3, 0.3)
        # dhol bhangra-ish pattern (dha .. ti ti dha .. ti dha)
        if k in (0, 3, 6, 10, 11 if b % 2 else 14):
            add(dagga(), tt, 0.32 if full else 0.22, -0.15)
        if k in (2, 4, 5, 8, 9, 12, 13, 15):
            add(tilli(), tt, 0.28 if full else 0.15, 0.2)
    # small riser into each 4-bar phrase
    if b % 4 == 3 and full:
        n = int(BAR * SR)
        r = bp(rng.standard_normal(n), 2000, 8000) * np.linspace(0, 1, n) ** 3
        add(r, t0, 0.06)

# outro: big hit + boom on the logo
n = int(3.2 * SR); t = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 6)) / SR) * env(n, 0.002, 0.9)
crash = hp(rng.standard_normal(n), 3000) * env(n, 0.001, 0.9) * 0.25
add(boom + crash, OUTRO, 0.6)
add(dagga(), OUTRO, 0.5); add(kick(), OUTRO, 0.6)

# simple stereo reverb-ish smear
rev = np.zeros_like(out)
for d, g in ((0.031, 0.25), (0.047, 0.2), (0.071, 0.15), (0.113, 0.1)):
    k = int(d * SR); rev[k:, 0] += out[:-k, 1] * g; rev[k:, 1] += out[:-k, 0] * g
out += lp(rev.T, 5000).T
# fades
fi = int(0.3 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
out /= np.abs(out).max() / 0.89
wf.write('bgm.wav', SR, (out * 32767).astype(np.int16))


# ---- transition SFX: whoosh (peaks at cut) + soft hit ----
def whoosh(seed):
    r = np.random.default_rng(seed)
    n = int(0.7 * SR); t = np.arange(n) / SR
    x = r.standard_normal(n)
    # sweeping band-pass via short-time filtering
    y = np.zeros(n); seg = 512
    for i in range(0, n, seg):
        p = i / n
        fc = 300 + 4200 * np.sin(np.pi * min(p / 0.72, 1)) ** 2
        y[i:i + seg] = bp(x[max(0, i - 2048):i + seg], fc * 0.6, min(fc * 1.6, 20000))[-len(y[i:i + seg]):]
    e = np.where(t < 0.5, (t / 0.5) ** 2.2, np.exp(-(t - 0.5) / 0.07))
    y = y * e
    st = np.stack([y * np.linspace(1.2, 0.5, n), y * np.linspace(0.5, 1.2, n)], 1)
    return st / np.abs(st).max()


def hit():
    n = int(0.6 * SR); t = np.arange(n) / SR
    b = np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-t * 20)) / SR) * env(n, 0.001, 0.18)
    s = hp(rng.standard_normal(n), 4000) * env(n, 0.001, 0.12) * 0.3
    y = b + s
    return np.stack([y, y], 1) / np.abs(y).max()


for i in range(4):
    wf.write(f'whoosh{i}.wav', SR, (whoosh(100 + i) * 0.9 * 32767).astype(np.int16))
wf.write('hit.wav', SR, (hit() * 0.9 * 32767).astype(np.int16))
print('ok')
