"""Sound for "Who's Fishing Who" (18 s): sound effects only, no narration.

  python3 scripts/synth_audio.py

Real foley from assets/sfx/*.wav (Openverse CC0/CC BY, see assets/sfx/CREDITS.md, fetched with
../_engine/fetch_sfx.py) and the bundled HyperFrames library, on top of procedural sounds from
sfxlib. Any missing recording falls back to a procedural stand-in, so the script always runs.
"""
import os
import sys

DUR = 18.0
os.environ["SFX_DUR"] = str(DUR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def rec(name, fallback, dur=None):
    x = load(os.path.join(ROOT, "assets", "sfx", name + ".wav"), dur=dur)
    return fallback() if x is None else fade_out(x, 0.1)


def lib(name, dur=None):
    return load(os.path.join(LIB, name + ".mp3"), dur=dur)


# ------------------------------------------------------------------ story-specific sounds
def snore(d=1.1):
    n = int(d * SR)
    tt = np.arange(n) / SR
    rattle = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 28 * tt))
    x = band(rng.standard_normal(n), 70, 600) * (0.4 + 0.6 * rattle) + 0.4 * np.sin(2 * np.pi * 95 * tt) * rattle
    e = np.sin(np.pi * np.minimum(1, tt / (d * 0.7))) ** 2 * (tt < d * 0.7)
    whistle = np.sin(2 * np.pi * np.cumsum(1300 - 500 * tt / d) / SR) * np.sin(np.pi * np.clip((tt - d * 0.72) / (d * 0.28), 0, 1)) * 0.15
    return norm(x * e + whistle)


def crunch(k=3):
    out = np.zeros(int(0.32 * SR))
    for i in range(k):
        h = noise_hit(0.06, 900, 6000) * (0.8 + 0.2 * i)
        j = int(i * 0.09 * SR)
        out[j: j + len(h)] += h[: len(out) - j]
    return norm(add(out, 0.6 * thump(180, 0.12, 0.5)))


def boing(f=330, d=0.45):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.6 * np.sin(2 * np.pi * 9 * tt) * np.exp(-tt * 6))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-tt * 5)


def zip_line(d=0.35):
    """Fishing line ripping off the reel: fast clicking ratchet."""
    n = int(d * SR)
    out = np.zeros(n)
    rate = 70
    for i in range(int(d * rate)):
        c = click()
        j = int(i / rate * SR)
        out[j: j + len(c)] += c[: n - j] * (1 - i / (d * rate) * 0.5)
    return norm(add(out, 0.4 * sweep(d, 800, 3000)))


def ratchet(d):
    """Reel being cranked: slower regular clicks."""
    n = int(d * SR)
    out = np.zeros(n)
    for i in range(int(d * 22)):
        c = click() * (0.7 + 0.3 * (i % 2))
        j = int(i / 22 * SR)
        out[j: j + len(c)] += c[: n - j]
    return out


def scratch(d=0.5):
    """Record scratch: noisy band swept down then back up."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = 1800 * np.where(tt < d * 0.55, 1 - 0.8 * tt / (d * 0.55), 0.2 + 1.4 * (tt - d * 0.55) / (d * 0.45))
    s = np.sign(np.sin(2 * np.pi * np.cumsum(ff) / SR))
    return norm(band(s, 200, 5000) * 0.6 + band(rng.standard_normal(n), 1500, 6000) * 0.4) * env(n, 0.005, 0.08)


def creak(d=0.7, f=140):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.25 * tt / d) * (1 + 0.04 * np.sin(2 * np.pi * 23 * tt))
    s = 2 * ((np.cumsum(ff) / SR) % 1) - 1
    return norm(band(s, 200, 2500)) * np.sin(np.pi * tt / d)


def arp(freqs, gap=0.07, d=0.12):
    out = np.zeros(int((gap * len(freqs) + d) * SR))
    for i, f in enumerate(freqs):
        b = blip(f, d)
        j = int(i * gap * SR)
        out[j: j + len(b)] += b
    return out


amb, fx = Bus(), Bus()

# ------------------------------------------------------------------ ambience
waves = norm(band(rng.standard_normal(N), 120, 1600)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t))
deep = loop_to(load(os.path.join(ROOT, "assets", "sfx", "underwater.wav")), N)
if deep is None:
    deep = norm(band(rng.standard_normal(N), 40, 380))
deep = band(deep, 30, 900)
for ch in range(2):
    amb.x[:, ch] += 0.45 * waves * (seg(1.6, 4.7, 0.3) + seg(17.75, 18.0, 0.05))
    amb.x[:, ch] += 0.55 * deep * (seg(0.45, 1.6, 0.15) + seg(4.6, 17.4, 0.3))

# ------------------------------------------------------------------ COLD OPEN (slow-motion splash)
fx.put(braam(2.0, 49), 0.0, 0.55)
fx.put(zip_line(0.4), 0.0, 0.45)
fx.put(rec("whoosh_water", lambda: lib("whoosh")), 0.05, 0.5)
SPLASH = rec("splash_big", lambda: noise_hit(1.0, 300, 7000))
fx.put(impact(1.1), 0.43, 0.95)
fx.put(SPLASH, 0.40, 0.95)
fx.put(sub_drop(1.1, 80, 30), 0.45, 0.6)
for k in range(10):
    fx.put(bubble(0.7 + 0.1 * (k % 4)), 0.6 + 0.09 * k, 0.25, (k % 5 - 2) / 3)
fx.put(rewind(0.45), 1.42, 0.55)
fx.put(lib("glitch-1", 0.6), 1.45, 0.35)

# ------------------------------------------------------------------ surface: the nap
GULL = rec("seagull", lambda: boing(1400, 0.3), dur=1.6)
fx.put(GULL, 1.9, 0.3, -0.5)
fx.put(snore(1.1), 1.75, 0.5)
fx.put(snore(1.1), 2.95, 0.5)
fx.put(rec("plop", lambda: bubble(2.2)), 2.3, 0.4)
fx.put(lib("sparkle"), 3.15, 0.35, 0.3)
fx.put(noise_hit(0.12, 2500, 8000), 3.55, 0.25)  # sniff
fx.put(noise_hit(0.12, 2500, 8000), 3.75, 0.25)
fx.put(crunch(3), 4.08, 0.6)  # CHOMP
fx.put(zip_line(0.3), 4.38, 0.5)
fx.put(lib("whoosh"), 4.4, 0.45)
fx.put(SPLASH, 4.57, 0.85)
fx.put(impact(0.7), 4.6, 0.7)

# ------------------------------------------------------------------ underwater: the chain
REEL = rec("reel", lambda: ratchet(1.4), dur=1.4)
fx.put(REEL, 4.75, 0.35, -0.3)
fx.put(ratchet(1.2), 4.75, 0.25, -0.3)
for k in range(8):
    fx.put(bubble(0.6 + 0.12 * (k % 3)), 4.9 + 0.17 * k, 0.22, (k % 3 - 1) / 2)
fx.put(arp([523, 659, 784, 1047]), 6.0, 0.35, -0.3)  # small fish cheers
fx.put(boing(380), 6.9, 0.3, -0.5)  # worm wiggles in
fx.put(rec("gulp", lambda: bubble(2.0)), 7.78, 0.55)
fx.put(zip_line(0.3), 7.93, 0.45)
fx.put(taiko(85), 7.95, 0.5)
fx.put(REEL, 8.1, 0.3, 0.3)
fx.put(ratchet(1.1), 8.1, 0.25, 0.3)
fx.put(arp([392, 494, 587, 784]), 9.2, 0.35, 0.3)  # medium fish cheers
fx.put(shing(0.5), 9.55, 0.25, 0.5)  # the lure glints
fx.put(shing(0.5), 9.95, 0.25, 0.5)
fx.put(rec("gulp", lambda: bubble(2.0)), 10.28, 0.55)
fx.put(zip_line(0.3), 10.43, 0.45)
fx.put(taiko(75), 10.45, 0.55)
fx.put(ratchet(1.3), 10.6, 0.3)

# ------------------------------------------------------------------ the giant
fx.put(braam(3.2, 41), 11.75, 0.8)
fx.put(sub_drop(1.6, 70, 26), 11.8, 0.6)
fx.put(heartbeat(), 12.2, 0.6)
fx.put(heartbeat(), 12.8, 0.7)
fx.put(boing(260, 0.4), 12.6, 0.25)
fx.put(impact(1.2), 13.3, 1.0)  # the giant bites the fisherman's worm
fx.put(rec("gulp", lambda: bubble(2.4)), 13.28, 0.6)
fx.put(scratch(0.45), 13.38, 0.55)
for k, f in enumerate([880, 1047, 1319, 1568]):
    fx.put(blip(f, 0.1), 13.45 + 0.08 * k, 0.32, (k - 1.5) / 2)  # four "!"

# ------------------------------------------------------------------ the ring
fx.put(sweep(1.1, 2500, 200), 13.85, 0.45)
fx.put(braam(3.0, 55), 14.55, 0.45)
fx.put(creak(0.8, 130), 15.3, 0.35, -0.4)
fx.put(creak(0.8, 150), 16.1, 0.35, 0.4)
fx.put(taiko(70), 16.8, 0.7)
fx.put(taiko(66), 17.02, 0.75)
fx.put(creak(0.5, 170), 16.85, 0.45)
fx.put(sweep(0.5, 250, 6000), 17.28, 0.6)  # whip back to the surface
fx.put(riser(0.45, 200, 1600), 17.3, 0.25)
fx.put(crunch(2), 17.86, 0.45)  # -> loops into the cold open's yank

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.45, makeup_db=5.0)
