"""8-bit music bed + "sound follows the story" helpers (STYLE_GUIDE.md section 6). Pure numpy, deterministic.

Import AFTER setting os.environ["SFX_DUR"] (it uses sfxlib's SR and N):

    import chiptune as CT
    bed = CT.bed([CT.Sec(2.0, 9.5, 100, 120, "kb"), CT.Sec(9.5, 13.75, 120, 160, "kbha"), ...], gain=...)
    fx.x += bed                                   # stereo (N, 2)
    fx.put(CT.crackle(rate_fn, t0, t1), t0, 0.5)  # a click train whose rate follows the on-screen counter
    fx.x = CT.tape_stop(fx.x, 30.5, 31.3)         # everything slows down and pitches to a halt

Section layers: k kick, b bass, h hats, s snare, a arpeggio, l lead melody, o octave-down (slow-motion feel).
"""
import numpy as np

from sfxlib import SR, N

# A minor: Am F C G (root, third, fifth in Hz, octave 3)
PROG = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
LEAD = [0, 2, 4, 2, 5, 4, 2, 0, 4, 5, 7, 5, 4, 2, 4, 0]   # scale steps, one per 8th note, loops every 2 bars
SCALE = [220.0, 246.94, 261.63, 293.66, 329.63, 349.23, 392.0, 440.0]


class Sec:
    def __init__(self, t0, t1, bpm0, bpm1, layers, gain=1.0):
        self.t0, self.t1, self.bpm0, self.bpm1, self.layers, self.gain = t0, t1, bpm0, bpm1, layers, gain


def _env(n, a=0.002, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    nr = n - na if r is None else min(n - na, int(r * SR))
    e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def square(f, d, duty=0.5, vol=1.0, slide=0.0):
    n = max(1, int(d * SR))
    ff = f * (1 + slide * np.linspace(0, 1, n))
    ph = np.cumsum(ff / SR) % 1
    return vol * np.where(ph < duty, 1.0, -1.0) * _env(n)


def triangle(f, d, vol=1.0):
    n = max(1, int(d * SR))
    ph = (np.arange(n) * f / SR) % 1
    return vol * (4 * np.abs(ph - 0.5) - 1) * _env(n)


def kick(vol=1.0):
    n = int(0.16 * SR)
    tt = np.arange(n) / SR
    f = 45 + 110 * np.exp(-tt * 38)
    return vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 18)


def noise(d, seed, hp=True):
    r = np.random.default_rng(seed)
    x = r.standard_normal(int(d * SR))
    if hp:
        x = np.diff(np.concatenate([[0], x]))
    return x


def hat(vol=1.0, seed=0):
    x = noise(0.035, seed)
    return 0.35 * vol * x * np.exp(-np.arange(len(x)) / SR * 90)


def snare(vol=1.0, seed=0):
    x = noise(0.12, seed, hp=False)
    tt = np.arange(len(x)) / SR
    return 0.45 * vol * (x * np.exp(-tt * 28) + 0.6 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 30))


def _put(buf, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0:
        return
    sig = sig[: N - i]
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    buf[i: i + len(sig), 0] += sig * gain * l
    buf[i: i + len(sig), 1] += sig * gain * r


def beats(sec):
    """beat times inside a section whose tempo glides from bpm0 to bpm1"""
    out, t = [], sec.t0
    while t < sec.t1 - 1e-6:
        bpm = sec.bpm0 + (sec.bpm1 - sec.bpm0) * (t - sec.t0) / max(1e-6, sec.t1 - sec.t0)
        dt = 60.0 / bpm
        out.append((t, dt))
        t += dt
    return out


def bed(sections, gain=0.3, crescendo=(0.75, 1.15), seed=1):
    """the nonstop 8-bit bed: every section restarts on a downbeat; gain rises over the video (crescendo)"""
    buf = np.zeros((N, 2))
    dur = N / SR
    for si, sec in enumerate(sections):
        L = sec.layers
        oct_ = 0.5 if "o" in L else 1.0
        for bi, (t, dt) in enumerate(beats(sec)):
            if t >= sec.t1:
                break
            g = gain * sec.gain * (crescendo[0] + (crescendo[1] - crescendo[0]) * t / dur)
            chord = PROG[(bi // 4) % 4]
            if "k" in L:
                _put(buf, kick(), t, 1.0 * g)
            if "s" in L and bi % 2 == 1:
                _put(buf, snare(seed=bi + si * 100), t, 0.8 * g)
            if "h" in L:
                _put(buf, hat(seed=bi * 3 + si), t + dt / 2, 0.8 * g, 0.3)
                if dt < 0.42:
                    _put(buf, hat(seed=bi * 3 + si + 1), t + dt / 4, 0.4 * g, -0.3)
                    _put(buf, hat(seed=bi * 3 + si + 2), t + 3 * dt / 4, 0.4 * g, -0.3)
            if "b" in L:
                root = chord[0] / 2 * oct_
                _put(buf, square(root, dt * 0.45, 0.5), t, 0.16 * g)
                _put(buf, square(root * 2, dt * 0.4, 0.5), t + dt / 2, 0.12 * g)
            if "a" in L:
                notes = [chord[0], chord[1], chord[2], chord[1] * 2]
                for k in range(4):
                    _put(buf, square(notes[k] * 2 * oct_, dt / 4 * 0.8, 0.25), t + k * dt / 4, 0.07 * g, (k % 2) * 0.6 - 0.3)
            if "l" in L:
                for k in range(2):
                    step = LEAD[(bi * 2 + k) % len(LEAD)]
                    f = SCALE[step % 8] * (2 if step >= 8 else 1) * 2 * oct_
                    _put(buf, square(f, dt / 2 * 0.85, 0.125), t + k * dt / 2, 0.075 * g, 0.2)
    return buf


def crackle(rate_fn, t0, t1, seed=3, pitch_fn=None, base=2600.0):
    """a click train whose rate (clicks/s) follows the story: rate_fn(t) -> clicks per second.
    At high rates the clicks blur into a buzz, exactly like the counter on screen."""
    n = int((t1 - t0) * SR)
    out = np.zeros(n)
    r = np.random.default_rng(seed)
    t = 0.0
    while t < t1 - t0:
        rate = max(0.5, rate_fn(t0 + t))
        f = base * (pitch_fn(t0 + t) if pitch_fn else 1.0) * (0.8 + 0.4 * r.random())
        m = int(0.012 * SR)
        tt = np.arange(m) / SR
        click = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 420) + 0.5 * r.standard_normal(m) * np.exp(-tt * 700)
        i = int(t * SR)
        seg = click[: max(0, n - i)]
        out[i: i + len(seg)] += seg * (0.6 + 0.4 * r.random())
        t += (1.0 / rate) * (0.7 + 0.6 * r.random())
    return out


def tone_glide(f0, f1, d, wave="square", duty=0.5, vol=1.0):
    n = int(d * SR)
    f = np.geomspace(f0, f1, n)
    ph = np.cumsum(f / SR) % 1
    x = np.where(ph < duty, 1.0, -1.0) if wave == "square" else np.sin(2 * np.pi * ph)
    return vol * x * _env(n, 0.01, 0.05)


def womp(start=392.0, steps=4, d=0.32):
    """sad-trombone 8-bit: descending notes, the last one wobbles down"""
    parts = []
    for k in range(steps):
        f = start * (2 ** (-k / 12 * 1.5))
        last = k == steps - 1
        parts.append(square(f, d * (2.2 if last else 1), 0.5, slide=-0.25 if last else 0))
    return np.concatenate(parts) * 0.5


def tape_stop(x, t0, t1):
    """everything slows down and pitches to a halt between t0 and t1 (silence after t1)"""
    i0, i1 = int(t0 * SR), int(t1 * SR)
    y = x.copy()
    tau = (np.arange(i1 - i0)) / SR
    T = t1 - t0
    pos = (t0 + tau - tau ** 2 / (2 * T)) * SR
    for c in range(x.shape[1]):
        y[i0:i1, c] = np.interp(pos, np.arange(len(x)), x[:, c]) * np.linspace(1, 0.3, i1 - i0)
    y[i1:] = 0
    return y
