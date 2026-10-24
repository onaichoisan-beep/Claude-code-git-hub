"""Sound effects for the pencil-sharpener-crew video (no narration, no text sounds).

Writes assets/audio/sfx.wav. Event times mirror index.html.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def crunch(d=0.09, seed=0):
    """Beaver bite into cedar: woody crack with a short body."""
    n = int(d * SR)
    r = np.random.default_rng(seed)
    e = np.exp(-np.arange(n) / SR / (d * 0.3))
    return norm(band(r.standard_normal(n), 400, 6000) * e) + 0.4 * thump(150, d, 2.0)[:n]


def chop():
    """Axe into wood: thock + bright crack."""
    return add(thump(95, 0.25, 3.0), 0.6 * noise_hit(0.05, 1500, 9000), 0.3 * crunch(0.12, 5))


def rasp(d=0.12, seed=0):
    """File stroke on graphite."""
    n = int(d * SR)
    r = np.random.default_rng(seed)
    return norm(band(r.standard_normal(n), 2500, 10000)) * np.sin(np.pi * np.arange(n) / n) ** 0.8


def scribble(d, seed=0, rate=7.0):
    """Pencil hatching on paper: airy scratch pulsing with each stroke."""
    n = int(d * SR)
    r = np.random.default_rng(seed)
    tt = np.arange(n) / SR
    s = band(r.standard_normal(n), 2500, 11000) * (0.35 + 0.65 * np.abs(np.sin(np.pi * rate * tt)))
    return norm(s) * env(n, 0.02, 0.05)


def ratchet(t0, t1, rate):
    for k in range(int((t1 - t0) * rate)):
        fx.put(click(), t0 + k / rate, 0.35, 0.3)


def machine(d, lo=50, hi=400):
    n = int(d * SR)
    return norm(band(rng.standard_normal(n), lo, hi)) * env(n, 0.3, 0.4)


# ---- hook: pencil bursts into the workshop (also the loop landing point)
fx.put(sweep(0.5, 300, 3000), 0.0, 0.4)
fx.put(impact(1.0), 0.45, 0.9)
fx.put(braam(2.0, 49), 0.45, 0.5)
fx.put(sub_drop(1.0, 90, 30), 0.45, 0.5)
for k in range(6):
    fx.put(crunch(0.08, 10 + k), 0.47 + k * 0.05, 0.5, (k % 3 - 1) * 0.5)
fx.put(blip(1400, 0.12), 0.55, 0.25)  # beaver squeak
fx.put(rewind(0.4), 1.45, 0.55)

# ---- desk: pencil slides in, crank ratchets, dive into the window
fx.put(thump(60, 0.4, 1.5), 1.85, 0.5)
fx.put(sweep(0.6, 800, 2500), 2.05, 0.3)
fx.put(add(click(), 0.5 * thump(120, 0.15, 2.0)), 2.8, 0.7)
ratchet(2.95, 5.0, 9)
amb.put(machine(2.3, 120, 1500), 2.95, 0.35)
fx.put(riser(1.0, 300, 3500), 4.2, 0.4)
fx.put(sweep(0.7, 200, 4000), 4.7, 0.5)

# ---- gears: metal clank train
fx.put(taiko(62), 5.2, 0.8)
amb.put(machine(4.4, 40, 300), 5.2, 0.6)
for k in range(10):
    fx.put(add(click(), 0.4 * shing(0.15)), 5.35 + k * 0.17, 0.3, (k % 2 - 0.5) * 0.6)

# ---- power: T-rex ROAR, fox sprints, treadmill rumbles up
fx.put(roar(1.3, 90), 7.5, 0.85)
fx.put(impact(0.8), 7.55, 0.6)
for k in range(28):
    fx.put(thump(170 + 20 * (k % 3), 0.06, 2.5), 7.7 + k * 0.06, 0.25, (k % 2 - 0.5) * 0.5)
amb.put(machine(1.8, 60, 700), 7.65, 0.5)
fx.put(riser(1.5, 150, 1800), 7.8, 0.3)

# ---- workshop: beaver chomps (cedar), axe chops (cone), file rasps (graphite)
for k in range(int((16.4 - 9.6) * 4.1)):
    fx.put(crunch(0.08, 30 + k), 9.6 + k / 4.1, 0.45, -0.3)
for k in range(int((16.4 - 12.0) * 1.43)):
    tk = 12.15 + k / 1.43
    fx.put(sweep(0.18, 600, 2400), tk - 0.16, 0.18, 0.3)
    fx.put(chop(), tk, 0.6, 0.3)
for k in range(int((16.4 - 14.2) * 7.6)):
    fx.put(rasp(0.1, 60 + k), 14.2 + k / 7.6, 0.25, 0.2)
amb.put(machine(13.8, 40, 260), 9.4, 0.45)

# ---- test 1: thick smudge, buzzer
fx.put(scribble(0.45, 3, 3), 16.9, 0.4)
fx.put(add(tone(120, 0.35, 0.01, 0.05), 0.8 * tone(127, 0.35, 0.01, 0.05)), 17.55, 0.45)
fx.put(add(tone(120, 0.45, 0.01, 0.2), 0.8 * tone(127, 0.45, 0.01, 0.2)), 17.95, 0.45)

# ---- montage: everything faster, taiko roll
for x, s in drum_roll(18.8, 21.0, 0.35, 0.1, 70):
    fx.put(s, x, 0.55)
for k in range(int(2.2 * 7.3)):
    fx.put(crunch(0.07, 90 + k), 18.85 + k / 7.3, 0.35, -0.3)
for k in range(int(2.2 * 3.5)):
    fx.put(chop(), 18.95 + k / 3.5, 0.45, 0.3)
for k in range(int(2.2 * 12.7)):
    fx.put(rasp(0.07, 120 + k), 18.85 + k / 12.7, 0.18, 0.2)
fx.put(riser(2.0, 200, 3000), 19.0, 0.35)

# ---- test 2: crisp fine line, ding + sparkle
fx.put(scribble(0.45, 4, 3), 21.45, 0.3)
fx.put(bell(1320, 1.6), 21.95, 0.45)
fx.put(shing(0.6), 21.97, 0.3)
fx.put(taiko(80), 21.95, 0.5)

# ---- desk drawing: hatching... SNAP
fx.put(scribble(1.8, 9, 7), 23.2, 0.45)
fx.put(add(noise_hit(0.04, 2500, 14000), 0.5 * thump(300, 0.08, 4.0)), 25.0, 0.9)
fx.put(impact(0.6), 25.0, 0.45)
fx.put(blip(2400, 0.04), 25.55, 0.2)

# ---- panic: dread braam, heartbeat, light grows -> loop into the hook
fx.put(braam(2.2, 41), 26.0, 0.6)
fx.put(sub_drop(1.2, 80, 30), 26.05, 0.5)
for k in range(4):
    fx.put(heartbeat(), 26.6 + k * 0.55, 0.5)
fx.put(riser(2.0, 150, 2600), 28.0, 0.4)
fx.put(sweep(0.5, 300, 3000), 29.55, 0.35)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
