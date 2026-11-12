"""Synthesize the music bed (music box + pads + clock ticks) and every sound effect, so the
film carries no third-party audio. Writes assets/audio/music.wav, assets/sfx/*.wav, tools/sfx.json."""
import json, os
import numpy as np, soundfile as sf
from scipy.signal import lfilter, butter, sosfilt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
TOTAL = 122.0
rng = np.random.default_rng(7)
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def env(n, a, d):  # attack seconds, exponential decay time-constant
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def reverb(x, mix=0.3):
    y = np.zeros_like(x)
    for dl, g in [(1557, 0.78), (1617, 0.77), (1491, 0.79), (1422, 0.8)]:
        y += lfilter([1], np.r_[1, np.zeros(dl - 1), -g], x)
    for dl in [225, 556]:
        y = lfilter(np.r_[-0.5, np.zeros(dl - 1), 1], np.r_[1, np.zeros(dl - 1), -0.5], y)
    return x * (1 - mix) + y * mix * 0.25
def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)
def add(buf, x, t):
    i = int(t * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]
    buf[i:i + len(x)] += x

# ---------------- music ----------------
N = int(TOTAL * SR)
mb, pad, low, tick = (np.zeros(N) for _ in range(4))
def musicbox(m, dur=1.6, detune=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = mtof(m) * (1 + detune)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)
    return x * env(n, 0.002, 0.55)
def padnote(ms, dur, att=0.8):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * mtof(m) * t + 0.3 * np.sin(2 * np.pi * 0.2 * t)) + 0.5 * np.sin(2 * np.pi * mtof(m) * 1.003 * t) for m in ms)
    e = np.minimum(1, t / att) * np.minimum(1, (dur - t) / 0.8)
    return x * e / len(ms)
E8 = 60 / 84 / 2  # eighth note
MEL_MIN = [69, 72, 76, 81, 79, 76, 72, 74, 76, 74, 72, 71, 72, 69, 64, 69]
MEL_MAJ = [72, 76, 79, 84, 83, 79, 76, 77, 79, 77, 76, 74, 76, 72, 67, 72]
CH_MIN = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [52, 56, 59]]
CH_MAJ = [[48, 52, 55], [53, 57, 60], [55, 59, 62], [48, 52, 55]]
def melody(t0, t1, mel, chords, vol=0.22, every=1, detune=0.0, slow=1.0):
    k, t = 0, t0
    while t < t1:
        if k % every == 0:
            add(mb, musicbox(mel[k % len(mel)], detune=detune) * vol, t)
        if k % 8 == 0:
            add(pad, padnote(chords[(k // 8) % len(chords)], E8 * 8 * slow + 0.6) * vol * 0.5, t)
        k += 1; t += E8 * slow
melody(0.0, 31.3, MEL_MIN, CH_MIN)
melody(31.3, 41.9, MEL_MIN, CH_MIN, vol=0.2)
melody(41.9, 60.6, MEL_MIN, [[50, 53, 57], [46, 50, 53], [45, 48, 52], [44, 48, 52]], vol=0.18, every=2)
melody(83.7, 91.2, MEL_MAJ, CH_MAJ, vol=0.16, every=2)
melody(91.2, 110.5, MEL_MAJ, CH_MAJ, vol=0.24)
melody(112.2, 122.0, MEL_MIN, CH_MIN, vol=0.2, every=2, detune=-0.012, slow=1.6)
# tension pulse
def pulse(t0, t1, vol, rate=E8):
    t = t0
    while t < t1:
        n = int(0.25 * SR); tt = np.arange(n) / SR
        x = np.tanh(3 * np.sin(2 * np.pi * 55 * tt)) * env(n, 0.005, 0.09)
        add(low, lp(x, 400) * vol, t); t += rate
pulse(31.3, 41.9, 0.12, E8 * 2)
pulse(60.6, 83.7, 0.22, E8)
pulse(91.2, 102.8, 0.14, E8 * 2)
# swell into the flip
n = int(7.5 * SR); tt = np.arange(n) / SR
add(pad, padnote([57, 64, 69, 73], 7.5, att=5.0) * 0.25, 83.7)
# clock ticks: run until the gears stop, come back in the morning, stop on "blank"
for t0, t1 in [(0.0, 82.75), (102.8, 112.2)]:
    t, k = t0, 0
    while t < t1:
        nn = int(0.03 * SR)
        x = bp(rng.standard_normal(nn), 2500 if k % 2 == 0 else 1900, 6000) * env(nn, 0.0005, 0.006)
        add(tick, x * 0.5, t); t += 0.5; k += 1
music = reverb(mb + pad, 0.35) + low + tick * 0.6
# duck under the voice gently: the bed sits far below speech already; normalise to a quiet bed
music = music / np.max(np.abs(music)) * 0.22
fade = np.ones(N); fe = int(1.0 * SR); fade[-fe:] = np.linspace(1, 0, fe)
sf.write(os.path.join(ROOT, "assets/audio/music.wav"), (music * fade).astype(np.float32), SR)

# ---------------- sound effects ----------------
FX = {}
def tone(f, d, dec, parts=((1, 1),)):
    n = int(d * SR); t = np.arange(n) / SR
    return sum(a * np.sin(2 * np.pi * f * r * t) for r, a in parts) * env(n, 0.002, dec)
FX["beep"] = tone(1760, 0.12, 0.2) * np.r_[np.ones(int(0.1 * SR)), np.linspace(1, 0, int(0.02 * SR))][: int(0.12 * SR)]
FX["beepbig"] = tone(1320, 0.3, 0.25, ((1, 1), (2, 0.3)))
FX["pop"] = (lambda n: np.sin(2 * np.pi * np.cumsum(np.linspace(900, 300, n)) / SR) * env(n, 0.001, 0.05))(int(0.15 * SR))
FX["bell"] = reverb(tone(196, 4.5, 1.6, ((0.5, 0.6), (1, 1), (1.19, 0.5), (1.56, 0.35), (2, 0.4), (2.51, 0.2), (3.01, 0.15))), 0.4)
FX["chime_c"] = reverb(tone(1046, 1.4, 0.5, ((1, 1), (2.76, 0.3))), 0.3)
FX["chime_e"] = reverb(tone(1318, 1.4, 0.5, ((1, 1), (2.76, 0.3))), 0.3)
FX["chime_g"] = reverb(tone(1568, 1.8, 0.7, ((1, 1), (2.76, 0.3), (1.5, 0.3))), 0.3)
FX["gold"] = reverb(tone(784, 1.6, 0.6, ((1, 1), (1.5, 0.5), (2, 0.4))), 0.35)
def whoosh(d, lo=300, hi=3000):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); k = 16
    for i in range(k):
        a, b = i * n // k, (i + 1) * n // k
        f = lo + (hi - lo) * np.sin(np.pi * i / k)
        out[a:b] = bp(x, f * 0.7, min(f * 1.4, 18000))[a:b]
    t = np.arange(n) / n
    return out * np.sin(np.pi * t) ** 2 * 1.5
FX["whoosh"] = whoosh(0.6)
FX["whoosh_long"] = whoosh(1.6, 200, 2500)
def hit(f0=55, d=2.5):
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f0 * t + 3 * np.exp(-t * 8)) * env(n, 0.003, 0.7) + lp(rng.standard_normal(n), 300) * env(n, 0.002, 0.15) * 0.6
    return reverb(x, 0.35)
FX["hit"] = hit()
FX["drone"] = reverb(hit(41, 3.5) + tone(220, 3.5, 1.5, ((1, 0.3), (1.06, 0.3))) * 0.6, 0.5)
n = int(0.9 * SR); t = np.arange(n) / SR
FX["slam"] = reverb(np.sin(2 * np.pi * 50 * t) * env(n, 0.001, 0.18) * 1.2 + lp(rng.standard_normal(n), 900) * env(n, 0.001, 0.05), 0.3)
FX["clunk"] = reverb(np.sin(2 * np.pi * 80 * t) * env(n, 0.001, 0.12) + tone(410, 0.9, 0.25, ((1, 0.5), (2.3, 0.4), (3.7, 0.3))) + hp(rng.standard_normal(n), 2000) * env(n, 0.001, 0.02), 0.3)
def screech(d=1.2):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); k = 24
    for i in range(k):
        a, b = i * n // k, (i + 1) * n // k
        f = 2600 * (1 - i / k) + 250
        out[a:b] = bp(x, f * 0.9, f * 1.1, 4)[a:b] * 4
    tt = np.arange(n) / SR
    saw = 2 * ((np.cumsum(np.linspace(400, 90, n)) / SR) % 1) - 1
    return (out + lp(saw, 1500) * 0.4) * np.minimum(1, tt / 0.02) * np.linspace(1, 0, n) ** 0.6
FX["screech"] = reverb(screech(), 0.25)
def shimmer(d=2.0, count=40, lo=1500, hi=4500):
    n = int(d * SR); out = np.zeros(n)
    for i in range(count):
        st = rng.uniform(0, d * 0.75); f = rng.uniform(lo, hi)
        add_n = tone(f, 0.5, 0.15) * rng.uniform(0.3, 1)
        a = int(st * SR); out[a:a + len(add_n)] += add_n[: n - a]
    return reverb(out * 0.35, 0.45)
FX["shimmer"] = shimmer()
FX["glitch"] = np.concatenate([tone(rng.uniform(900, 2400), 0.05, 0.05) for _ in range(18)])
def crack():
    n = int(0.8 * SR); out = hp(rng.standard_normal(n), 2500) * env(n, 0.0005, 0.03) * 1.5
    for i in range(30):
        a = int(rng.uniform(0, 0.5) * SR); m = int(0.01 * SR)
        out[a:a + m] += hp(rng.standard_normal(m), 3000) * rng.uniform(0.2, 0.8)
    return reverb(out, 0.3)
FX["crack"] = crack()
n = int(1.6 * SR); t = np.arange(n) / SR
gr = np.zeros(n)
for i in range(400):
    a = int(rng.uniform(0, 1.3) * SR); m = int(0.006 * SR)
    gr[a:a + m] += rng.standard_normal(m) * rng.uniform(0.1, 0.5) * np.exp(-a / SR * 1.5)
FX["crumble"] = bp(gr + rng.standard_normal(n) * np.exp(-t * 2.2) * 0.25, 600, 6000) * 1.4
for k, x in FX.items():
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    sf.write(os.path.join(ROOT, "assets/sfx", k + ".wav"), x.astype(np.float32), SR)

cues = [(0.0, "whoosh", 0.3), (1.62, "pop", 0.3), (11.62, "beep", 0.35), (11.8, "beep", 0.35), (11.62, "hit", 0.35),
        (19.2, "whoosh", 0.25), (26.16, "pop", 0.3), (28.06, "pop", 0.3), (34.76, "bell", 0.7), (36.14, "hit", 0.45),
        (36.14, "whoosh", 0.3), (40.64, "gold", 0.4), (41.9, "whoosh_long", 0.25), (44.85, "shimmer", 0.45),
        (52.62, "hit", 0.3), (54.2, "shimmer", 0.3), (62.1, "slam", 0.85), (63.14, "hit", 0.4),
        (70.32, "beepbig", 0.45), (71.38, "beepbig", 0.45), (72.1, "beepbig", 0.45), (79.42, "beepbig", 0.5),
        (80.58, "whoosh", 0.35), (81.04, "clunk", 0.7), (82.74, "screech", 0.5), (84.9, "whoosh_long", 0.4),
        (87.16, "shimmer", 0.55), (91.62, "glitch", 0.2), (92.64, "chime_c", 0.4), (93.26, "chime_e", 0.4), (94.38, "chime_g", 0.45),
        (97.1, "whoosh_long", 0.3), (100.56, "crack", 0.65), (101.42, "crumble", 0.6), (102.8, "whoosh", 0.22),
        (112.46, "hit", 0.35), (118.84, "drone", 0.5)]
cues += [(68.8 + i * 0.25, "beep", 0.25) for i in range(6)]
cues.sort()
json.dump([{"t": round(t, 3), "f": f, "d": round(len(FX[f]) / SR, 3), "v": v} for t, f, v in cues], open(os.path.join(ROOT, "tools", "sfx.json"), "w"), indent=1)
print("music + %d sfx, %d cues" % (len(FX), len(cues)))
