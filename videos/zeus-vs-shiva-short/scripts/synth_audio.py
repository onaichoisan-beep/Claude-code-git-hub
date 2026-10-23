"""Cinematic sound effects for the Zeus vs Shiva final-clash short (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def thunder(d=3.0, seed=2):
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    rumble = band(r.standard_normal(n), 25, 380) * np.exp(-tt / (d * 0.35))
    crack = np.zeros(n)
    c = noise_hit(0.12, 900, 9000)
    crack[: len(c)] += c
    return norm(norm(rumble) + 0.7 * crack)


def crackle_s(d=1.0, density=0.004, seed=3):
    n = int(d * SR)
    r = np.random.default_rng(seed)
    x = band((r.random(n) < density) * r.standard_normal(n), 1500, 9000)
    return norm(x) * env(n, 0.01, min(0.3, d * 0.3))


def shimmer(d=2.0, base=1800, seed=4):
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    s = sum(np.sin(2 * np.pi * base * m * tt + r.random() * 6) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + r.random() * 5) * tt)) for m in (1, 1.26, 1.5, 1.89))
    return norm(s) * env(n, d * 0.3, d * 0.4)


def choir(d, f=146.8, seed=8):
    n = int(d * SR)
    tt = np.arange(n) / SR
    r = np.random.default_rng(seed)
    x = np.zeros(n)
    for v in range(5):
        ph = 2 * np.pi * f * (1 + (r.random() - 0.5) * 0.012) * tt + r.random() * 6
        for h in range(1, 12):
            x += np.sin(h * ph) / h
    return norm(band(x, 400, 900) + 0.5 * band(x, 1000, 1400)) * env(n, d * 0.35, d * 0.4)


def strange_tone(d=3.0, f=211.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt + 3 * np.sin(2 * np.pi * 0.7 * tt)) + 0.6 * np.sin(2 * np.pi * f * 1.414 * tt)
    return norm(s) * env(n, d * 0.4, d * 0.3)


# ---- bed: low cosmic drone, dropping out for the heartbeat and the flash
drone = norm(band(rng.standard_normal(N), 30, 160))
for ch in range(2):
    amb.x[:, ch] += 0.5 * drone * (seg(1.6, 17.0, 0.4) + 0.6 * seg(23.0, 30, 0.6))

# ---- 0 HOOK: the collision
fx.put(impact(1.4), 0.0, 1.0)
fx.put(braam(2.2, 41.2), 0.0, 0.8)
fx.put(thunder(2.0, 11), 0.05, 0.6)
fx.put(shing(0.8), 0.1, 0.3)
fx.put(rewind(0.45), 1.4, 0.55)
# ---- 1 Zeus gathers the storm
fx.put(riser(3.4, 120, 1600), 1.9, 0.3)
fx.put(crackle_s(3.6, 0.006, 21), 1.8, 0.4)
fx.put(thunder(2.5, 22), 3.2, 0.7)
for tt_, sig in drum_roll(2.0, 5.4, 0.5, 0.14, 70):
    fx.put(sig, tt_, 0.45)
# ---- 2 Shiva answers with stillness
fx.put(gong(98, 4.0), 5.6, 0.55)
fx.put(bell(392, 3.0), 5.7, 0.35)
fx.put(conch(2.2, 290), 6.4, 0.3)
fx.put(choir(3.6, 196.0), 5.8, 0.35)
fx.put(shimmer(1.6, 2200, 41), 8.0, 0.3)
# ---- 3 both launch
fx.put(add(noise_hit(0.12, 600, 10000), shing(0.5) * 0.5), 9.95, 0.75)
fx.put(sweep(1.4, 300, 4000), 10.0, 0.5)
fx.put(thunder(2.5, 51), 10.1, 0.5)
for tt_, sig in drum_roll(10.1, 12.95, 0.35, 0.06, 76):
    fx.put(sig, tt_, 0.5)
fx.put(riser(2.9, 80, 1200), 10.1, 0.35)
# ---- 4 the collision bends the arena
fx.put(impact(1.5), 13.0, 1.0)
fx.put(braam(3.0, 36.7), 13.0, 0.8)
fx.put(sub_drop(1.8, 70, 24), 13.0, 0.7)
fx.put(sweep(3.6, 1800, 120), 13.2, 0.4)
fx.put(add(thump(32, 1.2, 2.5), noise_hit(0.3, 80, 3000) * 0.5), 15.5, 0.8)
for k in range(12):
    fx.put(add(noise_hit(0.07, 200, 4000), thump(140, 0.08, 0.5) * 0.5), 13.4 + k * 0.28, 0.3, (k % 5 - 2) / 3)
# ---- 5 one heartbeat
fx.put(heartbeat(), 17.4, 0.7)
fx.put(heartbeat(), 18.6, 0.6)
fx.put(norm(add(blip(3200, 0.03), noise_hit(0.01, 4000, 10000))), 19.7, 0.45)
fx.put(riser(0.7, 60, 400), 19.8, 0.5)
# ---- 6 the flash: a beat of silence, then everything
fx.put(impact(1.6), 20.5, 1.0)
fx.put(braam(3.5, 32.7), 20.5, 0.85)
fx.put(sub_drop(2.5, 60, 20), 20.5, 0.8)
fx.put(tone(2960, 2.5, 0.01, 0.95) * 0.5, 20.6, 0.14)
fx.put(reverb(np.pad(thunder(2.5, 61), (0, SR)), 2.0, 0.5), 20.8, 0.5)
# ---- 7 neither fell
for k in range(8):
    fx.put(add(noise_hit(0.06, 300, 3000), thump(160, 0.08, 0.5) * 0.4), 23.3 + k * 0.33, 0.2, (k % 5 - 2) / 3)
fx.put(crackle_s(2.6, 0.002, 71), 23.2, 0.25)
fx.put(bell(293.7, 2.5), 23.6, 0.25)
# ---- 8 something else woke up
fx.put(strange_tone(2.4, 211.0), 26.1, 0.4)
fx.put(sub_drop(0.7, 50, 28), 26.4, 0.6)
fx.put(sub_drop(0.7, 50, 28), 27.3, 0.6)
fx.put(thunder(2.0, 81), 26.9, 0.4)
# ---- back to the collision (loops into the cold open)
fx.put(sweep(1.5, 200, 3500), 28.4, 0.5)
fx.put(riser(1.6, 80, 900), 28.4, 0.4)
fx.put(crackle_s(1.6, 0.008, 91), 28.4, 0.35)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
