"""Sound effects for the rubbing-two-matches video (no narration, no text sounds).

Writes assets/audio/sfx.wav. Event times mirror index.html.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def scratch(d=0.12, seed=0):
    """One match-head stroke: gritty sandpaper rasp."""
    n = int(d * SR)
    r = np.random.default_rng(seed)
    grit = band(r.standard_normal(n), 1500, 9000) * (0.5 + 0.5 * (r.random(n) > 0.9))
    return norm(grit) * np.sin(np.pi * np.arange(n) / n) ** 0.7


def fwoosh(d=1.6):
    """Ignition: fast airy swell into a roaring burst."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    body = band(rng.standard_normal(n), 120, 4000)
    e = np.minimum(1, tt / 0.05) * np.exp(-tt / (d * 0.35))
    return norm(body * e)


def crackle(d, density=0.004, seed=3):
    """Fire crackle: sparse tiny pops over a soft roar."""
    n = int(d * SR)
    r = np.random.default_rng(seed)
    pops = (r.random(n) < density / 10) * r.uniform(0.3, 1, n)
    pops = band(np.convolve(pops, np.exp(-np.arange(200) / 30), "same"), 800, 9000)
    roar_ = band(r.standard_normal(n), 60, 600) * 0.35
    return norm(pops + roar_)


def ignition(t0, big=1.0):
    fx.put(fwoosh(1.6), t0, 0.95 * big)
    fx.put(impact(big), t0, 0.85 * big)
    fx.put(braam(2.2, 55), t0, 0.55 * big)
    fx.put(sub_drop(1.0, 90, 30), t0, 0.5 * big)
    fx.put(noise_hit(0.08, 2500, 12000), t0, 0.7 * big)


# ---- hook: strike-anywhere tips rubbed -> FWOOSH (and the same lead-in at the loop end)
for k in range(5):
    fx.put(scratch(0.11, k), 0.0 + k / 6 + 0.04, 0.45, (-1) ** k * 0.3)
fx.put(riser(0.6, 400, 3000), 0.15, 0.35)
ignition(0.75)
fx.put(crackle(0.9, seed=4), 0.9, 0.35)
fx.put(rewind(0.4), 1.45, 0.55)

# ---- safety matches: scrape, scrape... nothing
for k in range(15):
    tk = 1.8 + 0.15 + k / 6
    if tk < 1.8 + 2.6:
        fx.put(scratch(0.13, 20 + k), tk, 0.5, (-1) ** k * 0.35)
fx.put(riser(1.6, 200, 1600), 2.6, 0.3)
# the build-up cuts out to a dull thud: dud
fx.put(add(thump(55, 0.6, 1.5), 0.3 * noise_hit(0.1, 80, 600)), 4.35, 0.9)
fx.put(sweep(1.0, 200, 3500), 4.3, 0.5)

# ---- inside the head: low lab drone, a taiko for each ingredient
amb.put(norm(band(rng.standard_normal(int(7.6 * SR)), 40, 300)) * env(int(7.6 * SR), 0.4, 0.6), 5.0, 0.5)
fx.put(taiko(65), 5.25, 0.8)
for tt_, f in [(5.9, 70), (6.8, 80), (7.6, 90)]:
    fx.put(taiko(f), tt_, 0.65)
    fx.put(shing(0.5), tt_ + 0.02, 0.18)

# ---- the box, dive into the strip
fx.put(taiko(60), 9.0, 0.8)
fx.put(sweep(1.0, 150, 3500), 9.6, 0.5)
fx.put(taiko(75), 10.45, 0.7)
for tt_ in (10.9, 11.5):
    fx.put(taiko(85), tt_, 0.6)
    fx.put(shing(0.4), tt_ + 0.02, 0.15)

# ---- the strike, slowed down: long gravelly drag, rising tension, pops, then ERUPTION
n = int(1.9 * SR)
tt = np.arange(n) / SR
drag = band(rng.standard_normal(n), 200, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt) ** 2)
fx.put(norm(drag) * env(n, 0.2, 0.5), 12.6, 0.55)
fx.put(braam(2.0, 41), 12.6, 0.45)
fx.put(riser(1.8, 150, 2400), 12.7, 0.35)
# white phosphorus specks pop
for i, tt_ in enumerate([14.40, 14.48, 14.55, 14.66, 14.72, 14.85]):
    fx.put(add(noise_hit(0.05, 1500, 12000), 0.4 * thump(120 + i * 15, 0.1, 0.5)), tt_, 0.6, (i % 3 - 1) * 0.5)
fx.put(impact(0.6), 14.4, 0.5)
# heat soaking into the head + oxygen fizz
fx.put(riser(2.0, 100, 2000), 14.6, 0.4)
n = int(1.4 * SR)
fizz = band(rng.standard_normal(n), 3000, 10000) * (rng.random(n) > 0.6)
fx.put(norm(fizz) * env(n, 0.3, 0.3), 15.4, 0.22)
for b in range(8):
    fx.put(bubble(0.7 + 0.1 * (b % 3)), 15.5 + b * 0.13, 0.25, (b % 3 - 1) * 0.4)
ignition(16.6, 1.15)
for x, s in drum_roll(15.5, 16.55, 0.3, 0.07, 75):
    fx.put(s, x, 0.55)

# ---- burning match: roaring crackle bed
fx.put(crackle(6.0, seed=7) * env(int(6.0 * SR), 0.3, 0.6), 16.8, 0.45)
fx.put(sweep(0.8, 3000, 300), 18.7, 0.35)

# ---- strike-anywhere: taiko roll building, rub, second FWOOSH
for x, s in drum_roll(22.5, 24.85, 0.5, 0.09, 68):
    fx.put(s, x, 0.6)
for k in range(10):
    tk = 24.15 - 0.9 + k / 6 + 0.04
    if tk < 24.9:
        fx.put(scratch(0.11, 40 + k), tk, 0.45, (-1) ** k * 0.3)
ignition(24.9, 1.05)
fx.put(crackle(1.3, seed=9), 25.05, 0.35)

# ---- twist: gong, halves slide together, spark
fx.put(gong(98, 3.0), 26.2, 0.6)
fx.put(sweep(0.75, 300, 2500), 27.0, 0.35)
fx.put(add(noise_hit(0.15, 1500, 12000), thump(70, 0.4, 2.0)), 27.75, 0.8)

# ---- loop lead-in: scratches building straight into the hook again
fx.put(riser(1.6, 200, 2200), 28.4, 0.3)
for k in range(4):
    fx.put(scratch(0.11, 60 + k), 29.4 + k / 6 + 0.04, 0.45, (-1) ** k * 0.3)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
