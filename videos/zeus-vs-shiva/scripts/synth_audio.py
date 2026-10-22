"""Zeus vs Shiva — voice-over + score bed + sound effects, following the blueprint's per-shot sound notes.

Writes assets/audio/mix.wav (voice-over + score + SFX, used by the composition) and
assets/audio/sfx_only.wav (same mix without narration). Run scripts/make_vo.sh first.
"""
import os
import sys

os.environ["SFX_DUR"] = "240"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, "..", "assets", "audio")
END = 239.6  # cut to silence with the picture
amb, fx, vo = Bus(), Bus(), Bus()


def S(k, u=0.0):
    """global time of shot k (1-based, as in the blueprint) + local offset u"""
    return (k - 1) * 5.0 + u


# ------------------------------------------------------------------ extra kit
def wind(d, lo=200, hi=1400, rate=0.4, seed=1):
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = band(np.random.default_rng(seed).standard_normal(n), lo, hi)
    m = 0.6 + 0.4 * np.sin(2 * np.pi * rate * tt + seed) * np.sin(2 * np.pi * rate * 0.37 * tt)
    return norm(x * m) * env(n, min(0.6, d * 0.3), min(0.8, d * 0.3))


def thunder(d=3.0, seed=2):
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    rumble = band(r.standard_normal(n), 25, 380) * np.exp(-tt / (d * 0.35))
    rumble *= 0.7 + 0.3 * np.abs(np.sin(2 * np.pi * 3 * tt))
    crack = np.zeros(n)
    c = noise_hit(0.12, 900, 9000)
    crack[: len(c)] += c
    return norm(norm(rumble) + 0.7 * crack)


def crackle_s(d=1.0, density=0.004, seed=3):
    n = int(d * SR)
    r = np.random.default_rng(seed)
    clicks = (r.random(n) < density) * r.standard_normal(n)
    x = band(clicks, 1500, 9000) + 0.15 * band(r.standard_normal(n), 3000, 8000) * (r.random(n) < 0.3)
    return norm(x) * env(n, 0.01, min(0.3, d * 0.3))


def zap(d=0.35, f0=3000, f1=300):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (tt / d)
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    return norm(band(saw, 200, 9000) + 0.5 * band(rng.standard_normal(n), 2000, 9000)) * env(n, 0.005, d * 0.6)


def charge(d=2.0, f0=200, f1=1600):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (tt / d)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.4 + np.sin(2 * np.pi * np.cumsum(f * 2.01) / SR) * 0.4
    return norm(band(s, 150, 7000) + 0.6 * crackle_s(d, 0.004, 9)[:n]) * (tt / d) ** 1.5


def shimmer(d=2.0, base=1800, seed=4):
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    s = sum(np.sin(2 * np.pi * base * m * tt + r.random() * 6) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + r.random() * 5) * tt + r.random() * 6)) for m in (1, 1.26, 1.5, 1.89, 2.24))
    return norm(s) * env(n, d * 0.3, d * 0.4)


def water_crash(d=2.0, seed=5):
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    x = band(r.standard_normal(n), 80, 5000) * np.exp(-tt / (d * 0.4))
    hiss = band(r.standard_normal(n), 3000, 10000) * np.exp(-tt / (d * 0.25)) * 0.4
    return norm(x + hiss) * env(n, 0.01, d * 0.3)


def swirl(d=3.0, seed=6):
    n = int(d * SR)
    tt = np.arange(n) / SR
    a = sweep(d / 2, 300, 2400)
    b = sweep(d / 2, 2400, 300)
    s = np.concatenate([a, b])[:n]
    if len(s) < n:
        s = np.pad(s, (0, n - len(s)))
    return norm(s * (0.7 + 0.3 * np.sin(2 * np.pi * 2.5 * tt)) + 0.4 * wind(d, 300, 1800, 1.2, seed))


def clang(f=520, d=2.2):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (2 + k * 1.3)) / k for k in (1, 2.41, 3.77, 5.2, 6.9))
    hit = np.zeros(n)
    nh = noise_hit(0.05, 2000, 10000)
    hit[: len(nh)] = nh
    return norm(s + hit) * env(n, 0.002, 0.4)


def stone_crack(seed=7, n_hits=6, spread=0.6):
    out = np.zeros(int((spread + 0.6) * SR))
    r = np.random.default_rng(seed)
    for i in range(n_hits):
        s = add(noise_hit(0.08, 200, 4000), 0.6 * thump(120 + r.random() * 80, 0.15, 0.8))
        st = int(r.random() * spread * SR)
        out[st : st + len(s)] += s * (0.5 + 0.5 * r.random())
    return norm(out)


def whoosh(d=0.6, a=250, b=3200):
    return sweep(d, a, b)


def choir(d, f=146.8, seed=8):
    """soft 'aah' pad: detuned harmonics through vowel formants"""
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    x = np.zeros(n)
    for v in range(5):
        ff = f * (1 + (r.random() - 0.5) * 0.012)
        ph = 2 * np.pi * ff * tt + r.random() * 6
        for h in range(1, 12):
            x += np.sin(h * ph) / h
    x = band(x, 400, 900) * 1.0 + band(x, 1000, 1400) * 0.5
    return norm(x) * env(n, d * 0.35, d * 0.4)


def drone(d, freqs, lo=35, hi=700, seed=9):
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.4, 0.3):
            x += 2 * ((tt * (f + det)) % 1) - 1
    x = band(x, lo, hi)
    return norm(x) * env(n, min(2, d * 0.3), min(2, d * 0.3))


def brass(d=2.5, f=73.4):
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = braam(d, f)
    return x * np.minimum(1, tt / (d * 0.4))


def strange_tone(d=4.0, f=211.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt + 3 * np.sin(2 * np.pi * 0.7 * tt)) + 0.6 * np.sin(2 * np.pi * f * 1.414 * tt) + 0.4 * np.sin(2 * np.pi * f * 0.5 * tt)
    return norm(s) * env(n, d * 0.4, d * 0.3)


def tick():
    return norm(add(blip(3200, 0.03), noise_hit(0.01, 4000, 10000)))


def pulse_seq(t0, t1, period, sig, gain, bus=None):
    x = t0
    while x < t1:
        (bus or fx).put(sig, x, gain)
        x += period


# ------------------------------------------------------------------ score bed (quiet, under everything)
amb.put(drone(19.5, [36.7, 55.0, 73.4]) * 0.5, S(1, 1.0), 1.0)                 # cosmic awe
amb.put(choir(8, 146.8) * 0.35, S(3, 0.5), 1.0)                                # Shiva's hum
amb.put(drone(55, [41.2, 61.7, 82.4], hi=500), S(5, 0), 0.55)                  # first battle
amb.put(drone(55, [43.65, 65.4, 87.3], hi=500), S(16, 0), 0.6)                 # ocean + hurricane
amb.put(drone(9.5, [36.7, 55.0]) * 0.8, S(22, 0), 0.6)
amb.put(choir(12, 196.0) * 0.5, S(25, 0), 1.0)                                 # stillness
amb.put(drone(40, [38.9, 58.3, 77.8], hi=600), S(25, 0), 0.5)
amb.put(drone(5.5, [32.7, 49.0], hi=300), S(33, 0), 0.5)                       # the pause
amb.put(drone(40, [36.7, 55.0, 73.4, 110.0], hi=900), S(34, 0), 0.55)         # final build
amb.put(choir(10, 220.0) * 0.6, S(35, 0), 1.0)
amb.put(choir(12, 293.7) * 0.5, S(39, 0), 1.0)
amb.put(drone(10, [36.7, 55.0], hi=400) * 0.6, S(44, 0), 0.5)                  # restrained aftermath
amb.put(drone(16, [34.6, 51.9, 69.3], hi=500), S(46, 0), 0.4)                  # tense drone to the end
# battle pulse: soft taiko on the beat through the duels
pulse_seq(S(5, 0.0), S(13, 0), 0.6, taiko(62), 0.18)
pulse_seq(S(14, 0.0), S(16, 0), 0.4, taiko(70), 0.2)                           # rhythmic percussion (pursuit)
pulse_seq(S(17, 0.0), S(23, 0), 0.6, taiko(58), 0.16)

# ------------------------------------------------------------------ per shot
# 01 the universe trembles: 1 s silence, cosmic rumble, crystalline shimmer, bass impact at 4.5
amb.put(norm(band(rng.standard_normal(int(4 * SR)), 25, 160)) * env(int(4 * SR), 1.5, 0.5), S(1, 1.0), 0.9)
fx.put(shimmer(3.5, 2200), S(1, 1.2), 0.18)
fx.put(riser(2.6, 60, 400), S(1, 1.6), 0.25)
fx.put(thunder(2.5, 11), S(1, 4.15), 0.6)
fx.put(impact(1.2), S(1, 4.5), 0.85)
# 02 Zeus descends: wind builds, electricity crackles, thunderclap on landing, stone tail
fx.put(wind(3.2, 300, 1600, 0.6, 21), S(2, 0), 0.5)
fx.put(crackle_s(2.6, 0.006, 22), S(2, 0.4), 0.35)
fx.put(zap(0.4), S(2, 0.4), 0.3)
fx.put(zap(0.4), S(2, 1.6), 0.3)
fx.put(thunder(3.0, 23), S(2, 3.05), 0.9)
fx.put(impact(1.0), S(2, 3.05), 0.8)
fx.put(stone_crack(24, 8, 0.8), S(2, 3.15), 0.5)
# 03 Shiva awakens: soft bell, gentle conch, low cosmic hum rising
fx.put(bell(523, 3.0), S(3, 0.4), 0.3)
fx.put(bell(784, 2.5), S(3, 1.4), 0.18)
fx.put(conch(2.4, 280), S(3, 2.0), 0.32)
amb.put(riser(2.5, 50, 160), S(3, 2.6), 0.4)
fx.put(shimmer(2.0, 1600), S(3, 3.0), 0.15)
# 04 the challenge: wind swells, distant thunder, low tension, sting at the cuts
fx.put(wind(5, 200, 1200, 0.3, 41), S(4, 0), 0.35)
fx.put(thunder(3, 42), S(4, 0.4), 0.3)
fx.put(add(brass(1.4, 82.4), shing(0.6) * 0.3), S(4, 1.65), 0.45)
fx.put(add(brass(1.4, 110.0), shing(0.6) * 0.3), S(4, 3.25), 0.45)
# 05 face to face: metallic resonance, two-tone energy hum, rolling thunder
fx.put(clang(330, 3.0), S(5, 0.3), 0.18)
fx.put(tone(110, 4.6, 0.3, 0.3), S(5, 0.2), 0.12)
fx.put(tone(146.8, 4.6, 0.3, 0.3), S(5, 0.2), 0.1)
fx.put(thunder(4, 51), S(5, 0.6), 0.3)
# 06 Zeus launches the thunderbolt: charging, launch crack, projectile whoosh, rising thunder
fx.put(charge(1.9, 150, 1400), S(6, 1.0), 0.4)
fx.put(add(noise_hit(0.1, 800, 10000), zap(0.3, 4000, 600)), S(6, 3.0), 0.7)
fx.put(whoosh(1.2, 400, 4000), S(6, 3.05), 0.45)
fx.put(thunder(2, 61), S(6, 3.2), 0.45)
# 07 Shiva's defence: trident sweep, energy clang, explosive thunder, shimmering echo
fx.put(whoosh(0.5, 300, 2500), S(7, 0.2), 0.4)
fx.put(clang(392, 3.0), S(7, 1.0), 0.3)
fx.put(impact(1.3), S(7, 1.8), 0.95)
fx.put(thunder(2.5, 71), S(7, 1.8), 0.7)
fx.put(reverb(np.pad(shimmer(1.5, 2400), (0, SR)), 2.0, 0.6), S(7, 2.2), 0.25)
# 08 the shockwave: crumbling stone, rushing wind, bass swell, thunder rolling on
fx.put(stone_crack(81, 14, 2.5), S(8, 0.2), 0.5)
fx.put(wind(4.6, 150, 2400, 0.8, 82), S(8, 0), 0.55)
fx.put(sub_drop(2.0, 70, 26), S(8, 0), 0.6)
fx.put(thunder(4, 83), S(8, 2.4), 0.45)
# 09 lightning barrage: rapid thunderclaps, crackling, pounding drums, successive whooshes
for k, u in enumerate([0.45, 1.6, 3.1]):
    fx.put(whoosh(0.5, 500, 4500), S(9, u), 0.4)
    fx.put(zap(0.35), S(9, u), 0.35)
    if k < 2:
        fx.put(add(thunder(1.6, 90 + k), noise_hit(0.08, 600, 9000)), S(9, u + 0.55), 0.75)
for tt_, sig in drum_roll(S(9, 0.0), S(9, 5.0), 0.45, 0.2, 76):
    fx.put(sig, tt_, 0.35)
fx.put(crackle_s(5, 0.004, 95), S(9, 0), 0.25)
# 10 Shiva redirects the storm: trident resonance, swirling wind, electric snaps, orchestral rise
fx.put(tone(196, 4.5, 0.2, 0.4), S(10, 0.2), 0.12)
fx.put(swirl(4.0, 101), S(10, 0.3), 0.4)
for u in [0.8, 1.6, 2.4, 3.0, 3.6]:
    fx.put(zap(0.2, 5000, 1500), S(10, u), 0.25)
fx.put(brass(3.0, 98.0), S(10, 2.0), 0.4)
# 11 Zeus changes angle: air rush, crackling trail, drum roll, sharp weapon whoosh
fx.put(wind(2.0, 400, 3000, 1.5, 111), S(11, 0), 0.5)
fx.put(crackle_s(2.0, 0.008, 112), S(11, 0.0), 0.35)
for tt_, sig in drum_roll(S(11, 2.3), S(11, 4.2), 0.25, 0.08, 90):
    fx.put(sig, tt_, 0.4)
fx.put(whoosh(0.7, 300, 5000), S(11, 3.6), 0.55)
# 12 trident against thunderbolt: clash, crackling, bass hit, ringing silence after separation
fx.put(add(clang(440, 2.5), noise_hit(0.15, 300, 9000)), S(12, 0.8), 0.8)
fx.put(impact(0.8), S(12, 0.8), 0.6)
fx.put(crackle_s(2.0, 0.01, 121), S(12, 0.8), 0.45)
fx.put(thump(45, 1.2, 3), S(12, 2.8), 0.8)
fx.put(add(noise_hit(0.2, 200, 9000), impact(0.6)), S(12, 2.8), 0.7)
fx.put(tone(2637, 2.0, 0.01, 0.9) * 0.4, S(12, 3.0), 0.12)  # ringing
# 13 the arena breaks: stone cracking, debris rumble, wind through gaps, low pulse
fx.put(stone_crack(131, 18, 3.5), S(13, 0), 0.55)
fx.put(norm(band(rng.standard_normal(int(4.5 * SR)), 30, 250)) * env(int(4.5 * SR), 0.1, 2), S(13, 0), 0.5)
fx.put(wind(5, 500, 2500, 1.0, 132), S(13, 0), 0.3)
fx.put(thump(60, 0.6, 1.5), S(13, 2.6), 0.6)
# 14 aerial pursuit: fast wind, electric zips, stone taps
fx.put(wind(5, 400, 3000, 2.0, 141), S(14, 0), 0.45)
for k in range(5):
    fx.put(zap(0.25, 3500, 900), S(14, k * 1.0 + 0.1), 0.3)
    fx.put(add(thump(180, 0.1, 0.5), noise_hit(0.05, 800, 5000)), S(14, k * 1.0 + 0.98), 0.35)
# 15 Shiva's precise counter: lightning slice, air-cut, trident pulse, rising water energy
fx.put(add(zap(0.4, 6000, 800), noise_hit(0.1, 1000, 9000)), S(15, 0.62), 0.6)
fx.put(whoosh(0.4, 1500, 6000), S(15, 0.9), 0.45)
fx.put(add(thump(80, 0.6, 2), bell(330, 1.5) * 0.4), S(15, 2.0), 0.6)
fx.put(add(water_crash(3, 151) * 0.6, riser(2.5, 100, 600) * 0.4), S(15, 2.1), 0.55)
# 16 the arena becomes an ocean: huge wave roar, wind, distant thunder, cosmic undertone
fx.put(water_crash(4.5, 161), S(16, 1.4), 0.3)
fx.put(wind(5, 300, 1500, 0.5, 162), S(16, 0), 0.35)
fx.put(thunder(3, 163), S(16, 0.5), 0.3)
fx.put(add(water_crash(2.5, 164), sub_drop(1.6, 60, 28)), S(16, 3.6), 0.4)
# 17 Zeus splits the wave: thunder strike, water crash, sizzling steam, deep rumble
fx.put(add(thunder(2.5, 171), impact(1.0) * 0.6), S(17, 1.1), 0.9)
fx.put(water_crash(3.5, 172), S(17, 1.2), 0.5)
fx.put(band(rng.standard_normal(int(3 * SR)), 3000, 10000) * env(int(3 * SR), 0.05, 2.0) * 0.6, S(17, 1.3), 0.45)
fx.put(sub_drop(2.5, 55, 25), S(17, 1.2), 0.5)
# 18 Shiva commands the current: water swirl, trident tone, soft bass pulse, spray impacts
fx.put(swirl(4.5, 181), S(18, 0.3), 0.45)
fx.put(tone(220, 4.0, 0.2, 0.4), S(18, 0.5), 0.12)
pulse_seq(S(18, 0.5), S(18, 4.8), 1.0, thump(50, 0.6, 1.0), 0.4)
for u in [1.4, 2.3, 3.2, 4.0]:
    fx.put(water_crash(0.5, 183 + int(u * 10)), S(18, u), 0.25)
# 19 Zeus pierces the shield: focused charge, sharp whistle, distant explosion, water column roar
fx.put(charge(1.5, 300, 2400), S(19, 0.2), 0.45)
fx.put(add(zap(0.9, 6000, 3000), whoosh(1.0, 2000, 7000) * 0.5), S(19, 1.6), 0.5)
fx.put(add(impact(0.8), water_crash(3, 191)), S(19, 2.65), 0.8)
fx.put(wind(2.2, 200, 1200, 0.5, 192), S(19, 2.8), 0.4)
# 20 Shiva closes the distance: water rush, trident sweep, bolt crack, brief resonant silence
fx.put(water_crash(2.5, 201), S(20, 0), 0.35)
fx.put(whoosh(0.8, 300, 2400), S(20, 0.4), 0.35)
fx.put(add(zap(0.3), noise_hit(0.1, 800, 9000)), S(20, 2.15), 0.5)
fx.put(add(clang(523, 1.6), noise_hit(0.12, 600, 9000)), S(20, 2.7), 0.6)
fx.put(bell(392, 2.0), S(20, 3.3), 0.15)
# 21 Zeus summons the hurricane: wind into a roar, layered thunder, low brass swell, snaps
fx.put(wind(5, 150, 1800, 0.7, 211) * np.linspace(0.3, 1, int(5 * SR)), S(21, 0), 0.6)
fx.put(thunder(3, 212), S(21, 0.6), 0.5)
fx.put(thunder(3, 213), S(21, 2.1), 0.6)
fx.put(brass(3.5, 55.0), S(21, 1.2), 0.5)
for u in [0.9, 1.7, 2.6, 3.4, 4.2]:
    fx.put(zap(0.2, 4500, 1200), S(21, u), 0.2)
# 22 the storm lifts them: whirling wind, rushing water, debris rattle, rising tension
fx.put(swirl(5, 221), S(22, 0), 0.32)
fx.put(water_crash(3, 222), S(22, 0.2), 0.3)
fx.put(stone_crack(223, 20, 4), S(22, 0.3), 0.2)
fx.put(riser(4.5, 70, 500), S(22, 0.3), 0.3)
for u in [3.4, 4.0, 4.6]:
    fx.put(thunder(1.5, 224 + int(u)), S(22, u), 0.4)
# 23 Zeus gains the advantage: thunder impact, bass drop, shield crackle, wind rushing past
fx.put(whoosh(1.6, 200, 4000), S(23, 0.2), 0.5)
fx.put(add(impact(1.2), thunder(2.5, 231)), S(23, 1.8), 1.0)
fx.put(sub_drop(1.6, 80, 25), S(23, 1.8), 0.7)
fx.put(crackle_s(2.5, 0.01, 232), S(23, 2.0), 0.4)
fx.put(wind(3, 300, 2500, 1.2, 233), S(23, 2.0), 0.45)
# 24 the midpoint reversal: near-silence for two seconds, one deep bell, cosmic pulse, harmonics
fx.put(wind(2.2, 200, 700, 0.2, 241), S(24, 0), 0.06)
fx.put(gong(73.4, 5.0), S(24, 2.3), 0.5)
fx.put(bell(293.7, 4.0), S(24, 2.3), 0.4)
fx.put(thump(40, 1.5, 1), S(24, 2.3), 0.6)
fx.put(shimmer(2.8, 1400), S(24, 2.6), 0.25)
amb.put(choir(2.8, 293.7), S(24, 2.4), 0.5)
# 25 the storm falls still: suspended droplets shimmer, harmonic drone, distant thunder fading
fx.put(shimmer(5, 2600, 251), S(25, 0), 0.22)
fx.put(tone(98, 5.0, 0.3, 0.3), S(25, 0), 0.15)
fx.put(thunder(4, 252) * np.linspace(1, 0.2, int(4 * SR)), S(25, 1.0), 0.18)
# 26 Shiva releases the field: deep resonant pulse, expanding whoosh, cloud rush, bright chime
fx.put(add(thump(38, 1.6, 1.5), gong(98, 3) * 0.4), S(26, 0.9), 0.7)
fx.put(whoosh(3.0, 120, 2000), S(26, 1.0), 0.45)
fx.put(wind(3.5, 300, 2400, 1.0, 261), S(26, 1.4), 0.4)
fx.put(bell(1046, 2.0), S(26, 4.0), 0.3)
# 27 Zeus adapts: crackle tightening, heartbeat-like drum, rising brass
fx.put(crackle_s(3.4, 0.003, 271) * np.linspace(0.4, 1, int(3.4 * SR)), S(27, 0.3), 0.4)
pulse_seq(S(27, 0.4), S(27, 4.8), 0.7, heartbeat(), 0.55)
fx.put(brass(3.5, 82.4), S(27, 1.4), 0.4)
# 28 a focused thunder spear: tight electrical whine, two directional zips, sharp launch tail
fx.put(add(zap(0.4, 5000, 1000), noise_hit(0.1, 1000, 9000)), S(28, 0.6), 0.55)
fx.put(tone(1760, 4.2, 0.05, 0.3) * 0.5, S(28, 0.7), 0.1)
fx.put(zap(0.3, 2000, 6000), S(28, 1.55), 0.45)
fx.put(zap(0.3, 6000, 2000), S(28, 3.0), 0.45)
fx.put(whoosh(1.2, 600, 5000), S(28, 3.6), 0.4)
# 29 Shiva slips past: air sweep, projectile hiss, distant rock burst, falling fragments
fx.put(whoosh(1.5, 300, 2000), S(29, 0.3), 0.4)
fx.put(band(rng.standard_normal(int(1.3 * SR)), 3000, 9000) * env(int(1.3 * SR), 0.3, 0.6), S(29, 1.1), 0.35)
fx.put(add(impact(0.6), stone_crack(291, 6, 0.3)), S(29, 2.4), 0.5)
fx.put(stone_crack(292, 12, 2.0), S(29, 2.7), 0.25)
# 30 trident arc: trident resonance, three layered energy sweeps, deep pulse
fx.put(tone(196, 4.0, 0.1, 0.5), S(30, 0.3), 0.12)
for k in range(3):
    fx.put(whoosh(1.6, 200 + 100 * k, 2500 + 500 * k), S(30, 0.8 + 0.15 * k), 0.35)
fx.put(thump(42, 1.4, 1.5), S(30, 3.2), 0.6)
# 31 Zeus breaks the ring: rapid wind rush, electric flare, ringing energy break, thunder roll
fx.put(wind(3, 400, 4000, 2, 311), S(31, 0.5), 0.5)
fx.put(add(zap(0.6, 1000, 6000), crackle_s(1.5, 0.01, 312)), S(31, 0.7), 0.5)
fx.put(add(shing(0.8), clang(880, 1.5) * 0.5), S(31, 1.6), 0.4)
fx.put(thunder(3.5, 313), S(31, 1.8), 0.55)
fx.put(shimmer(1.6, 3000), S(31, 3.5), 0.25)
# 32 the cosmic arena appears: cosmic rumble, shimmering stars, orchestral rise, distant thunder
fx.put(norm(band(rng.standard_normal(int(5 * SR)), 25, 180)) * env(int(5 * SR), 1, 1.5), S(32, 0), 0.4)
fx.put(shimmer(4.5, 2000, 321), S(32, 0.2), 0.22)
fx.put(brass(4.0, 73.4), S(32, 0.8), 0.4)
fx.put(thunder(3, 322), S(32, 1.5), 0.2)
# 33 a measured pause: low drone, one heartbeat thump, faint crackle
fx.put(heartbeat(), S(33, 2.0), 0.7)
fx.put(crackle_s(1.5, 0.002, 331), S(33, 3.6), 0.25)
# 34 Zeus's full charge: rising electric charge, rolling thunder, layered drums
fx.put(charge(4.2, 120, 1800), S(34, 0.6), 0.45)
fx.put(thunder(4, 341), S(34, 0.8), 0.45)
for tt_, sig in drum_roll(S(34, 0.8), S(34, 5.0), 0.5, 0.12, 68):
    fx.put(sig, tt_, 0.45)
# 35 Shiva's cosmic focus: deep bell, soft choral texture, trident hum, rising shimmer
fx.put(bell(196, 4.5), S(35, 0.3), 0.4)
fx.put(gong(98, 4.0), S(35, 0.3), 0.25)
fx.put(tone(146.8, 4.5, 0.4, 0.3), S(35, 0.5), 0.12)
fx.put(shimmer(3.5, 1800, 351) * np.linspace(0.2, 1, int(3.5 * SR)), S(35, 1.4), 0.3)
# 36 both launch: simultaneous launch cracks, thunder, energy roar, drums accelerating
fx.put(add(noise_hit(0.12, 600, 10000), zap(0.4, 5000, 700)), S(36, 0.85), 0.75)
fx.put(add(whoosh(1.0, 2000, 300), tone(110, 1.0, 0.01, 0.5) * 0.3), S(36, 0.85), 0.5)
fx.put(thunder(3, 361), S(36, 1.0), 0.3)
fx.put(add(wind(4, 80, 1200, 1.5, 362), riser(4, 60, 500) * 0.6), S(36, 1.0), 0.25)
for tt_, sig in drum_roll(S(36, 1.0), S(36, 5.0), 0.4, 0.07, 74):
    fx.put(sig, tt_, 0.28)
# 37 first collision: huge layered impact, bass hit, crackling energy, high ringing overtone
fx.put(impact(1.5), S(37, 0.0), 1.0)
fx.put(braam(3.5, 41.2), S(37, 0.0), 0.8)
fx.put(sub_drop(1.8, 70, 24), S(37, 0.0), 0.7)
fx.put(crackle_s(4.5, 0.008, 371), S(37, 0.2), 0.35)
fx.put(tone(3136, 3.5, 0.02, 0.9) * 0.4, S(37, 0.1), 0.12)
# 38 the pull of power: suction rumble, debris rattle, electrical snaps, low pulsing rhythm
fx.put(sweep(4.8, 1800, 120), S(38, 0.1), 0.3)
fx.put(norm(band(rng.standard_normal(int(5 * SR)), 25, 140)) * env(int(5 * SR), 0.5, 0.5), S(38, 0), 0.35)
fx.put(stone_crack(381, 16, 4), S(38, 0.3), 0.2)
pulse_seq(S(38, 0.2), S(38, 5.0), 0.8, thump(46, 0.5, 1), 0.5)
fx.put(add(thump(35, 1.0, 2), noise_hit(0.2, 100, 3000) * 0.4), S(38, 1.2), 0.6)
fx.put(add(thump(32, 1.4, 2.5), noise_hit(0.3, 80, 3000) * 0.5), S(38, 3.2), 0.8)
# 39 the arena fractures: stone cracking, glass-like chimes, thunder rolling underneath
fx.put(stone_crack(391, 22, 3.5), S(39, 0.2), 0.5)
for k, f in enumerate([1568, 2093, 1760, 2637, 2349]):
    fx.put(bell(f, 1.4), S(39, 0.4 + k * 0.45), 0.12)
fx.put(thunder(5, 392), S(39, 0.5), 0.4)
# 40 Zeus pushes forward: electricity surges, pounding drums, heavy wind, sharp rising tone
fx.put(crackle_s(4.8, 0.012, 401), S(40, 0.1), 0.22)
pulse_seq(S(40, 0.3), S(40, 5.0), 0.45, taiko(66), 0.3)
fx.put(wind(5, 150, 2500, 1.6, 402), S(40, 0), 0.28)
fx.put(riser(4.0, 300, 2000), S(40, 1.0), 0.25)
# 41 Shiva answers: trident resonance, deep bell, harmonic swell, low rumble
fx.put(tone(196, 4.5, 0.2, 0.4), S(41, 0.3), 0.14)
fx.put(bell(146.8, 4.5), S(41, 0.4), 0.45)
fx.put(add(choir(4.0, 293.7), choir(4.0, 440.0) * 0.6), S(41, 0.8), 0.35)
fx.put(norm(band(rng.standard_normal(int(4.5 * SR)), 25, 150)) * env(int(4.5 * SR), 1, 1), S(41, 0.4), 0.4)
# 42 the world holds its breath: near-silence, faint heartbeat, crystalline tick, low rising tone
fx.put(heartbeat(), S(42, 0.6), 0.35)
fx.put(heartbeat(), S(42, 2.0), 0.3)
fx.put(tick(), S(42, 3.2), 0.4)
fx.put(riser(1.6, 50, 200), S(42, 3.4), 0.45)
# 43 a flash beyond the arena: a fraction of silence, enormous impact, high ringing tail, deep bass
fx.put(impact(1.6), S(43, 0.12), 1.0)
fx.put(braam(4.5, 36.7), S(43, 0.12), 0.6)
fx.put(sub_drop(3.0, 60, 20), S(43, 0.12), 0.6)
fx.put(tone(2960, 4.5, 0.01, 0.95) * 0.5, S(43, 0.2), 0.14)
fx.put(reverb(np.pad(thunder(3, 431), (0, SR)), 2.5, 0.5), S(43, 0.4), 0.28)
# 44 after the collision: falling debris, distant thunder, soft energy crackle
fx.put(stone_crack(441, 14, 4.0), S(44, 0.4), 0.22)
fx.put(thunder(4, 442) * 0.6, S(44, 0.8), 0.25)
fx.put(crackle_s(4.5, 0.0015, 443), S(44, 0.3), 0.2)
# 45 two powers remain: low pulse, faint crackle, trident hum, slow heartbeat
fx.put(crackle_s(1.6, 0.003, 451), S(45, 0.1), 0.3)
fx.put(tone(196, 1.5, 0.2, 0.4), S(45, 1.9), 0.12)
pulse_seq(S(45, 0.3), S(45, 5.0), 1.1, heartbeat(), 0.35)
# 46 the strange signal: a new unfamiliar resonant tone, low rumble, tense drone
fx.put(strange_tone(5.0, 211.0), S(46, 0.3), 0.2)
fx.put(norm(band(rng.standard_normal(int(5 * SR)), 25, 120)) * env(int(5 * SR), 1, 0.5), S(46, 0), 0.22)
# 47 the unknown presence: thunder + trident resonance overlap, strange bass pulse, crackle
fx.put(add(thunder(3, 471), tone(196, 3, 0.1, 0.5) * 0.3), S(47, 0.8), 0.28)
fx.put(strange_tone(5.0, 105.5), S(47, 0), 0.2)
pulse_seq(S(47, 0.5), S(47, 5.0), 0.9, sub_drop(0.7, 50, 28), 0.35)
fx.put(crackle_s(4, 0.004, 472), S(47, 0.8), 0.15)
# 48 cliffhanger: rising energy roar, layered thunder + cosmic resonance — abrupt cut at the end
fx.put(add(riser(4.6, 60, 900), wind(4.6, 80, 2500, 2, 481) * 0.6), S(48, 0.0), 0.38)
fx.put(thunder(4, 482), S(48, 0.6), 0.35)
fx.put(add(braam(4.0, 55.0), strange_tone(4.0, 211.0) * 0.5), S(48, 0.6), 0.42)
for tt_, sig in drum_roll(S(48, 1.0), S(48, 4.6), 0.35, 0.06, 80):
    fx.put(sig, tt_, 0.32)

# ------------------------------------------------------------------ voice-over: one line per shot
VO_OFFSET = {1: 0.95, 24: 0.4, 43: 1.0, 48: 0.25}
VO_BOOST = {16: 1.6, 17: 1.25, 22: 1.25, 36: 1.6, 38: 1.25, 40: 1.35, 43: 1.6}  # lines over the busiest beds
vo_files = sorted(f for f in os.listdir(os.path.join(AUD, "vo")) if f.endswith(".wav"))
assert len(vo_files) == 48, len(vo_files)
for k in range(1, 49):
    x = read_wav(os.path.join(AUD, "vo", "vo%02d.wav" % k))
    nz = np.nonzero(np.abs(x) > 0.01)[0]
    x = x[max(0, nz[0] - int(0.02 * SR)) : nz[-1] + int(0.1 * SR)]  # trim TTS silence
    x = x / (np.max(np.abs(x)) + 1e-9)
    x = add(x, 0.18 * reverb(np.pad(x, (0, int(0.6 * SR))), 0.9, 1.0, 77))  # a touch of space
    start = S(k, VO_OFFSET.get(k, 0.35))
    if start + len(x) / SR > S(k + 1, 0.15):
        start = max(S(k, 0.1), S(k + 1, 0.15) - len(x) / SR)
    vo.put(x, start, 0.9 * VO_BOOST.get(k, 1.0))

# duck the score/effects under the voice (about -7 dB), smoothly
lvl = np.abs(vo.x).max(axis=1)
win = int(0.25 * SR)
lvl = np.convolve(lvl, np.ones(win) / win, mode="same")
duck = 1 - 0.68 * np.clip(lvl / 0.05, 0, 1)
duck = np.convolve(duck, np.ones(win) / win, mode="same")[:, None]

# abrupt cut to silence at the end of the picture
cut = int(END * SR)
for b in (amb, fx, vo):
    b.x[cut:] = 0

sfx_only = Bus()
sfx_only.x = fx.x.copy()
master(amb, sfx_only, os.path.join(AUD, "sfx_only.wav"), amb_gain=0.55, makeup_db=7.0)

amb.x *= duck
fx.x = fx.x * duck + vo.x
master(amb, fx, os.path.join(AUD, "mix.wav"), amb_gain=0.55, makeup_db=7.0)

# report how far the narration sits above the ducked bed, per shot
bed = amb.x * 0.55 + (fx.x - vo.x)
for k in range(48):
    a, b = int((k * 5 + 0.5) * SR), int((k * 5 + 4.3) * SR)
    v = 20 * np.log10(np.sqrt(np.mean(vo.x[a:b] ** 2)) + 1e-9)
    e = 20 * np.log10(np.sqrt(np.mean(bed[a:b] ** 2)) + 1e-9)
    print("%02d vo-bed %+.1f dB" % (k + 1, v - e), end="  " if (k + 1) % 6 else "\n")
