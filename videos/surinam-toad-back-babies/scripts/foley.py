"""Story foley for the narrated fable shorts, built on sfxlib (import this after setting SFX_DUR).

Everything is synthesised and deterministic: sea, splashes, sizzle, creaks, gulls, crickets, wind,
ice, fire, fireworks, rowing, choir pads and drones, cat sounds, clockwork, paper, glass, rockets.
Each function returns a mono float array; place it with Bus.put().
"""
import numpy as np

from sfxlib import SR, add, band, bell, env, noise_hit, norm, reverb, thump, tone  # noqa: F401

_r = np.random.default_rng(4321)


def _n(d):
    return int(d * SR)


def _tt(d):
    return np.arange(_n(d)) / SR


def _bp_sweep(x, f_of_t, q=0.35, blk=2048):
    """overlap-add band-pass whose centre follows f_of_t(s) (seconds -> Hz)"""
    y = np.zeros(len(x))
    for s in range(0, len(x), blk // 2):
        seg = x[s: s + blk]
        if len(seg) < 64:
            break
        fc = f_of_t(s / SR)
        y[s: s + len(seg)] += band(seg, fc * (1 - q), fc * (1 + q)) * np.hanning(len(seg))
    return y


# ------------------------------------------------------------------ water
def sea(d, swell=6.5, seed=1):
    """ocean surf bed: low rumble + hiss that swell and wash on slow cycles"""
    r = np.random.default_rng(seed)
    tt = _tt(d)
    lo = band(r.standard_normal(len(tt)), 50, 500)
    hi = band(r.standard_normal(len(tt)), 900, 7000)
    ph = 2 * np.pi * tt / swell
    s1 = 0.55 + 0.45 * np.sin(ph) ** 2
    s2 = np.clip(np.sin(ph - 0.6), 0, 1) ** 3  # the wash after each crest
    return norm(0.8 * norm(lo) * s1 + 0.55 * norm(hi) * (0.15 + s2))


def splash(size=1.0, seed=3):
    r = np.random.default_rng(seed)
    d = 0.5 + 0.5 * size
    n = _n(d)
    tt = np.arange(n) / SR
    body = band(r.standard_normal(n), 250, 7000) * np.exp(-tt / (0.12 * size + 0.05))
    out = norm(body) * 0.9
    out[: _n(0.35 * size)] += 0.5 * thump(80 / max(size, 0.4), 0.35 * size, 1.0)[: _n(0.35 * size)]
    for k in range(int(10 * size) + 4):  # droplets
        i = int(r.uniform(0.05, d * 0.9) * SR)
        f = r.uniform(900, 2600)
        dl = _n(0.05)
        tq = np.arange(dl) / SR
        drop = np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * tq / 0.05)) / SR) * np.exp(-tq / 0.012)
        out[i: i + dl] += 0.18 * drop[: len(out[i: i + dl])]
    return norm(out)


def sizzle(d=1.0, seed=5):
    r = np.random.default_rng(seed)
    n = _n(d)
    x = band(r.standard_normal(n), 2500, 11000)
    crack = (r.random(n) > 0.9993).astype(float)
    crack = np.convolve(crack, np.exp(-np.arange(200) / 30), mode="same")
    return norm(x * (0.5 + 0.5 * np.abs(np.sin(np.arange(n) / SR * 23))) + 3 * band(crack * r.standard_normal(n), 1500, 9000)) * env(n, 0.05, d * 0.5)


def boil(d=2.0, rate=25, seed=7):
    """rolling boil / bubbling: many bubbles, rising density"""
    r = np.random.default_rng(seed)
    out = np.zeros(_n(d))
    k = 0
    tq = 0.0
    while tq < d:
        dens = rate * (0.3 + 0.7 * tq / d)
        tq += r.exponential(1 / dens)
        sz = r.uniform(0.4, 1.4)
        b = bubble_(sz, r.uniform(500, 1400))
        i = _n(tq)
        out[i: i + len(b)] += 0.4 * b[: len(out[i: i + len(b)])]
        k += 1
    return out + 0.2 * norm(band(r.standard_normal(len(out)), 100, 600)) * np.linspace(0.3, 1, len(out))


def bubble_(size, f0):
    d = 0.06 * size + 0.02
    tq = _tt(d)
    return np.sin(2 * np.pi * np.cumsum(f0 / size * (1 + 2.2 * tq / d)) / SR) * np.exp(-tq / (d * 0.3))


def oar(seed=11):
    """one rowing stroke: wood knock, swish through water, drips"""
    r = np.random.default_rng(seed)
    n = _n(0.9)
    tt = np.arange(n) / SR
    sw = band(r.standard_normal(n), 300, 3000) * np.exp(-((tt - 0.3) / 0.12) ** 2)
    out = 0.8 * norm(sw)
    out[: _n(0.08)] += 0.4 * noise_hit(0.08, 400, 2500)
    for k in range(4):
        i = _n(0.45 + 0.1 * k + r.uniform(0, 0.05))
        b = bubble_(r.uniform(0.3, 0.6), r.uniform(1200, 2200))
        out[i: i + len(b)] += 0.25 * b
    return out


# ------------------------------------------------------------------ wood, air, creatures
def creak(d=0.8, f=110, seed=13):
    """wooden creak: stick-slip pulse train with wandering rate, through a woody band"""
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    wob = f * (1 + 0.35 * np.sin(2 * np.pi * r.uniform(1.5, 3) * tt + r.uniform(0, 6)) + 0.25 * tt / d)
    ph = np.cumsum(wob) / SR
    pulses = (np.diff(np.floor(ph), prepend=0) > 0).astype(float)
    x = np.convolve(pulses, np.exp(-np.arange(300) / 40) * np.sin(np.arange(300) * 0.25), mode="same")
    return norm(band(x, 250, 2500)) * env(n, 0.06, 0.2)


def gull(seed=17):
    """seagull 'kee-ow': bright harmonic glide down"""
    r = np.random.default_rng(seed)
    d = r.uniform(0.32, 0.45)
    tt = _tt(d)
    f = 1500 * (0.62 + 0.38 * np.cos(np.pi * tt / d)) * (1 + 0.04 * np.sin(2 * np.pi * 18 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    return norm(band(s, 700, 7000)) * env(len(tt), 0.03, d * 0.5)


def chirp(seed=19):
    """small songbird chirp"""
    r = np.random.default_rng(seed)
    out = np.zeros(0)
    for k in range(r.integers(2, 5)):
        d = r.uniform(0.04, 0.09)
        tt = _tt(d)
        f0, f1 = r.uniform(3000, 4500), r.uniform(2200, 5200)
        f = f0 + (f1 - f0) * tt / d
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d)
        out = np.concatenate([out, s, np.zeros(_n(r.uniform(0.02, 0.06)))])
    return out


def crickets(d, seed=23):
    r = np.random.default_rng(seed)
    tt = _tt(d)
    out = np.zeros(len(tt))
    for v in range(3):
        f = r.uniform(4200, 5200)
        trill = (np.sin(2 * np.pi * r.uniform(13, 18) * tt) > 0.2).astype(float)
        burst = (np.sin(2 * np.pi * r.uniform(0.6, 0.9) * tt + r.uniform(0, 6)) > -0.1).astype(float)
        out += np.sin(2 * np.pi * f * tt) * np.convolve(trill * burst, np.ones(80) / 80, mode="same")
    return norm(out)


def wind(d, f0=500, f1=900, howl=0.5, seed=29):
    """wind: broadband rush + a resonant howl whose pitch wanders between f0 and f1"""
    r = np.random.default_rng(seed)
    x = r.standard_normal(_n(d))
    ph = r.uniform(0, 6)
    rush = band(x, 150, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * _tt(d) + ph))
    hw = _bp_sweep(r.standard_normal(_n(d)),
                   lambda s: f0 + (f1 - f0) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * s + ph)), q=0.06)
    return norm(norm(rush) * (1 - howl) + norm(hw) * howl)


def meow(d=0.7, f0=520, seed=31, sad=False):
    """cat meow: pitch rises then falls, vowel 'ee-ah-oo' formants"""
    tt = _tt(d)
    u = tt / d
    contour = (1 + 0.45 * np.sin(np.pi * u ** 0.8)) if not sad else (1.2 - 0.35 * u)
    f = f0 * contour * (1 + 0.012 * np.sin(2 * np.pi * 6 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    src = sum(np.sin(k * ph) / k ** 0.9 for k in range(1, 14))
    # formant glide: F1 400->900->500, F2 2200->1300->900
    out = np.zeros(len(tt))
    blk = 1024
    for s in range(0, len(tt), blk // 2):
        seg = src[s: s + blk]
        if len(seg) < 64:
            break
        v = s / len(tt)
        F1 = 400 + 500 * np.sin(np.pi * min(1, v * 1.4)) if v < 0.7 else 900 - 400 * (v - 0.7) / 0.3
        F2 = 2200 - 1300 * v
        y = band(seg, F1 * 0.7, F1 * 1.4) + 0.6 * band(seg, F2 * 0.8, F2 * 1.25)
        out[s: s + len(seg)] += y * np.hanning(len(seg))
    return norm(out) * env(len(tt), 0.05, d * 0.45)


def hiss_cat(d=0.6, seed=37):
    r = np.random.default_rng(seed)
    n = _n(d)
    return norm(band(r.standard_normal(n), 2500, 10000)) * env(n, 0.02, d * 0.4)


def purr(d=2.0, seed=41):
    r = np.random.default_rng(seed)
    tt = _tt(d)
    pulse = 0.5 + 0.5 * np.sin(2 * np.pi * 26 * tt) ** 2
    breath = 0.6 + 0.4 * np.sin(2 * np.pi * 0.55 * tt)
    return norm(band(r.standard_normal(len(tt)), 40, 400) * pulse * breath) * env(len(tt), 0.2, 0.3)


def roar_croc(d=1.0, seed=43):
    """deep reptile hiss-growl + jaw snap at the end"""
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    g = band(r.standard_normal(n), 60, 700) * (0.6 + 0.4 * np.sin(2 * np.pi * 21 * tt))
    out = norm(g) * env(n, 0.1, 0.3) * 0.7
    snap = add(noise_hit(0.05, 800, 6000), 0.8 * thump(140, 0.12, 2.0))
    i = n - len(snap)
    out[i:] += snap
    return norm(out)


def squawk(seed=47):
    """parrot squawk: harsh nasal FM burst"""
    r = np.random.default_rng(seed)
    d = 0.32
    tt = _tt(d)
    f = 900 + 500 * np.sin(np.pi * tt / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph + 3 * np.sin(ph * 2.01))) + 0.3 * r.standard_normal(len(tt))
    return norm(band(s, 600, 5000)) * env(len(tt), 0.01, 0.1)


# ------------------------------------------------------------------ fire, ice, light
def fire(d=2.0, seed=53):
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    roar_ = band(r.standard_normal(n), 120, 1600) * (0.7 + 0.3 * np.sin(2 * np.pi * 3.3 * tt) * np.sin(2 * np.pi * 1.7 * tt))
    cr = (r.random(n) > 0.9992).astype(float) * r.uniform(0.3, 1, n)
    cr = band(np.convolve(cr, np.exp(-np.arange(120) / 18), mode="same") * r.standard_normal(n), 1200, 9000)
    return norm(norm(roar_) * 0.7 + norm(cr) * 0.6) * env(n, 0.15, 0.4)


def ice_crack(seed=59, big=1.0):
    """a crack + the laser-like 'pew' that frozen sheets ring with"""
    r = np.random.default_rng(seed)
    d = 0.35 * big + 0.1
    tt = _tt(d)
    f = r.uniform(2400, 3600) * np.exp(-tt / 0.07) + 500
    pew = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / (0.08 * big + 0.02))
    out = 0.7 * pew
    out[: _n(0.03)] += noise_hit(0.03, 1500, 12000)
    if big > 0.8:
        out += 0.5 * thump(55, d, 1.5)[: len(out)]
    return norm(out)


def chatter(d=1.2, seed=61):
    """teeth chattering"""
    r = np.random.default_rng(seed)
    out = np.zeros(_n(d))
    x = 0.0
    while x < d - 0.03:
        c = noise_hit(0.012, 2500, 9000) * r.uniform(0.4, 1)
        i = _n(x)
        out[i: i + len(c)] += c
        x += r.uniform(0.045, 0.07)
    return out


def sparkle(d=1.2, seed=67, lo=2500, hi=6000):
    """glittering tiny bells"""
    r = np.random.default_rng(seed)
    out = np.zeros(_n(d) + _n(0.6))
    for k in range(int(14 * d)):
        b = bell(r.uniform(lo, hi), 0.5) * r.uniform(0.2, 0.6)
        i = _n(r.uniform(0, d))
        out[i: i + len(b)] += b
    return out


def firework(seed=71, dist=1.0):
    """launch whistle, pop, crackling tail (dist>1 = further away: duller, quieter)"""
    r = np.random.default_rng(seed)
    wh = _tt(0.5)
    f = 1800 + 1500 * wh / 0.5
    whistle = 0.25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(wh), 0.05, 0.1)
    pop = add(thump(60, 0.6, 3.0), noise_hit(0.25, 100, 5000 / dist))
    tail = np.zeros(_n(1.4))
    for k in range(60):
        c = noise_hit(0.01, 2000, 9000 / dist) * r.uniform(0.1, 0.5)
        i = _n(r.uniform(0.05, 1.3) ** 1.2)
        tail[i: i + len(c)] += c
    out = np.concatenate([whistle, np.zeros(_n(0.05)), add(pop, tail)])
    return reverb(out, 1.5, 0.35 * dist) / dist


# ------------------------------------------------------------------ tonal beds
def pad(d, freqs, a=1.0, r_=1.5, seed=73):
    """soft choir-ish pad: detuned sine stacks with slow swell"""
    r = np.random.default_rng(seed)
    tt = _tt(d)
    s = np.zeros(len(tt))
    for f in freqs:
        for det in (-0.004, 0, 0.005):
            s += np.sin(2 * np.pi * f * (1 + det) * tt + 0.15 * np.sin(2 * np.pi * r.uniform(4, 6) * tt) + r.uniform(0, 6))
            s += 0.3 * np.sin(2 * np.pi * 2 * f * (1 + det) * tt + r.uniform(0, 6))
    return norm(s) * env(len(tt), a, r_)


def drone(d, f0=110, seed=79):
    """warm tanpura-like drone (Pa-Sa-Sa-Sa shimmer, no melody)"""
    r = np.random.default_rng(seed)
    tt = _tt(d)
    s = np.zeros(len(tt))
    for k in range(1, 12):
        amp = 1 / k ** 1.1 * (0.6 + 0.4 * np.sin(2 * np.pi * (0.13 * k + 0.05) * tt + r.uniform(0, 6)))
        s += amp * np.sin(2 * np.pi * f0 * k * tt + r.uniform(0, 6))
        s += 0.5 * amp * np.sin(2 * np.pi * f0 * 1.5 * k * tt + r.uniform(0, 6)) / (1 + k)
    return norm(s)


# ------------------------------------------------------------------ mechanical, paper, glass, space
def tick(f=3200, hard=1.0):
    """clock tick: tiny metallic click through a resonant band"""
    n = _n(0.06)
    tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.006) + 0.6 * np.sin(2 * np.pi * f * 1.7 * tt) * np.exp(-tt / 0.004)
    x[: _n(0.004)] += noise_hit(0.004, 2000, 12000) * hard
    return norm(x)


def ratchet(d=0.6, rate=22, f=1800, seed=83):
    """gear ratchet / winding: a fast train of ticks"""
    r = np.random.default_rng(seed)
    out = np.zeros(_n(d) + _n(0.06))
    x = 0.0
    while x < d:
        tk = tick(f * r.uniform(0.9, 1.1), 0.5) * r.uniform(0.5, 1)
        i = _n(x)
        out[i: i + len(tk)] += tk
        x += 1 / rate
    return out


def gears(d=2.0, seed=89):
    """big clockwork: low grind + slow heavy clunks"""
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    grind = band(r.standard_normal(n), 80, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt) ** 2)
    out = 0.5 * norm(grind)
    for k in range(int(d / 0.5)):
        c = add(thump(90, 0.25, 1.5), 0.5 * noise_hit(0.04, 600, 4000))
        i = _n(k * 0.5)
        out[i: i + len(c)] += 0.7 * c[: len(out[i: i + len(c)])]
    return norm(out)


def page_flip(seed=97, d=0.35):
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    flutter = 0.5 + 0.5 * np.sin(2 * np.pi * r.uniform(30, 45) * tt) ** 2
    x = band(r.standard_normal(n), 1200, 9000) * flutter * np.sin(np.pi * tt / d) ** 2
    return norm(x)


def book_thud(seed=101):
    return add(thump(85, 0.3, 1.2), 0.5 * noise_hit(0.06, 300, 3000))


def whispers(d, seed=103):
    """breathy unvoiced murmurs: band noise shaped into syllables"""
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    out = np.zeros(n)
    for v in range(5):
        f = r.uniform(1500, 3500)
        x = band(r.standard_normal(n), f * 0.7, f * 1.4)
        syl = np.clip(np.sin(2 * np.pi * r.uniform(2.5, 4.5) * tt + r.uniform(0, 6)), 0, 1) ** 2
        phrase = np.clip(np.sin(2 * np.pi * r.uniform(0.15, 0.3) * tt + r.uniform(0, 6)), 0, 1)
        out += norm(x) * syl * phrase
    return norm(out)


def glass_smash(seed=107):
    r = np.random.default_rng(seed)
    hit = add(noise_hit(0.15, 1500, 12000), 0.5 * thump(200, 0.1, 1.0))
    tail = np.zeros(_n(1.2))
    for k in range(40):
        b = bell(r.uniform(3000, 8000), 0.4) * r.uniform(0.1, 0.5)
        i = _n(r.uniform(0.0, 0.8) ** 1.5)
        tail[i: i + len(b)] += b[: len(tail[i: i + len(b)])]
    return norm(add(hit, 0.7 * tail))


def rumble(d=3.0, lo=25, hi=300, seed=109):
    """rocket / earthquake rumble"""
    r = np.random.default_rng(seed)
    n = _n(d)
    tt = np.arange(n) / SR
    x = band(r.standard_normal(n), lo, hi) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * tt) * np.sin(2 * np.pi * 2.3 * tt))
    return norm(x) * env(n, 0.3, 0.6)


def poof(seed=113):
    """cartoon soul-poof: soft burst + rising whistle"""
    r = np.random.default_rng(seed)
    n = _n(0.6)
    tt = np.arange(n) / SR
    burst = band(r.standard_normal(n), 300, 4000) * np.exp(-tt / 0.08)
    rise = np.sin(2 * np.pi * np.cumsum(600 + 1800 * tt / 0.6) / SR) * env(n, 0.05, 0.25) * 0.35
    return norm(norm(burst) + rise)


def harp_up(f0=523.25, steps=8, gap=0.06, seed=127):
    """quick rising harp gliss (major pentatonic)"""
    sc = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3]
    out = np.zeros(_n(gap * steps + 1.5))
    for k in range(steps):
        f = f0 * sc[k % 5] * 2 ** (k // 5)
        n = _n(1.2)
        tq = np.arange(n) / SR
        s = (np.sin(2 * np.pi * f * tq) + 0.3 * np.sin(4 * np.pi * f * tq)) * np.exp(-tq * 3.5)
        i = _n(k * gap)
        out[i: i + n] += 0.5 * s
    return out


def stab(f=220, d=1.6):
    """tense low string stab"""
    tt = _tt(d)
    s = sum(((tt * f * m * (1 + det)) % 1 - 0.5) for m, det in [(1, 0), (1, 0.006), (2, -0.004), (0.5, 0)])
    return norm(band(s, 60, 2400)) * np.minimum(1, tt / 0.01) * np.exp(-tt / (d * 0.35))
