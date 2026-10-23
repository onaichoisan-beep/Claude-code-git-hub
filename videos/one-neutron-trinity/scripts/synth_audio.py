"""Sound effects for the one-neutron / Trinity video (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def rumble(d, lo=30, hi=220, decay=None):
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = norm(band(rng.standard_normal(n), lo, hi)) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.3 * tt) ** 2)
    e = np.exp(-tt / decay) if decay else 1
    return x * e * env(n, 0.02, d * 0.3)


def crackle(d, rate=40):
    n = int(d * SR)
    x = np.zeros(n)
    r = np.random.default_rng(9)
    for _ in range(int(d * rate)):
        i = r.integers(0, n - 400)
        x[i : i + 400] += band(r.standard_normal(400), 1500, 9000) * np.exp(-np.arange(400) / 60) * r.uniform(0.3, 1)
    return norm(x)


# ---- ambience: a cold low hum for the atom scenes, desert wind after the blast
hum = np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 82.5 * t) * 0.25
amb.x[:, 0] += 0.18 * hum * (seg(1.8, 16.4, 0.4) + seg(25.5, 30, 0.3))
amb.x[:, 1] += 0.18 * hum * (seg(1.8, 16.4, 0.4) + seg(25.5, 30, 0.3))
wind = norm(band(rng.standard_normal(N), 200, 1200))
amb.x[:, 0] += 0.12 * wind * seg(22.5, 25.6, 0.5)
amb.x[:, 1] += 0.12 * np.roll(wind, 2000) * seg(22.5, 25.6, 0.5)

# ---- cold open: the blast, then rewind
fx.put(impact(1.2), 0.0, 1.0)
fx.put(braam(2.0, 41), 0.0, 0.7)
fx.put(sub_drop(1.6, 80, 26), 0.0, 0.8)
fx.put(rumble(1.8, decay=1.2), 0.05, 0.6)
fx.put(rewind(0.45), 1.6, 0.5)

# ---- the neutron streaks in; the nucleus wobbles; it snaps
fx.put(sweep(2.6, 400, 4000), 2.1, 0.35, -0.4)
fx.put(add(thump(120, 0.3, 2.5), noise_hit(0.05, 2000, 9000) * 0.5), 4.7, 0.7)
n = int(0.9 * SR)
tt = np.arange(n) / SR
wob = np.sin(2 * np.pi * np.cumsum(180 + 500 * (tt / 0.9) ** 2 + 40 * np.sin(2 * np.pi * 14 * tt)) / SR) * (tt / 0.9)
fx.put(wob, 4.75, 0.3)
fx.put(impact(1.0), 5.6, 0.9)
fx.put(shing(0.6), 5.6, 0.5)
for k, p in enumerate([-0.6, 0.6, 0.0]):
    fx.put(sweep(0.5, 3000, 600), 5.65 + k * 0.08, 0.3, p)

# ---- chain reaction: each generation pings higher and more at once; drums speed up
for gen in range(1, 9):
    tg = 8.7 + gen * 0.72
    for j in range(min(gen + 1, 6)):
        fx.put(blip(500 * 2 ** (gen / 8) * (1 + 0.12 * j), 0.07), tg + j * 0.04, 0.16, (j % 3 - 1) * 0.5)
    fx.put(noise_hit(0.12, 1500, 8000), tg, 0.15 + 0.03 * gen)
for x, s in drum_roll(9.0, 16.3, 0.7, 0.07):
    fx.put(s, x, 0.55)
fx.put(riser(3.0, 120, 1800), 13.4, 0.35)
fx.put(sweep(1.8, 300, 8000), 14.6, 0.35)
fx.put(crackle(1.8, 120), 14.6, 0.3)

# ---- Trinity: the real blast, rolling thunder
fx.put(impact(1.3), 16.5, 1.0)
fx.put(braam(3.5, 36), 16.5, 0.8)
fx.put(sub_drop(2.4, 70, 22), 16.5, 0.9)
fx.put(rumble(6.5, 25, 260, decay=3.0), 16.6, 0.7)
fx.put(crackle(3.0, 50), 16.8, 0.15)
fx.put(add(thump(45, 1.0, 1.0), rumble(2.5, 30, 150, decay=1.0)), 19.6, 0.6)  # the shock wave arrives
fx.put(braam(3.0, 49), 19.9, 0.35)

# ---- the ground: sizzling sand, then glass tinkles
fx.put(sweep(0.7, 3000, 400), 22.8, 0.3)
n = int(1.6 * SR)
fx.put(norm(band(rng.standard_normal(n), 3000, 11000)) * env(n, 0.05, 1.0), 23.1, 0.22)
fx.put(crackle(1.6, 70), 23.1, 0.25)
for k, f in enumerate([2093, 2637, 3136, 2349, 2794, 3520]):
    fx.put(bell(f, 0.9), 24.1 + k * 0.2, 0.12, (k % 3 - 1) * 0.6)

# ---- the twist: the paperclip lands on a scale; beep; E=mc2; a heavy hit on "1 gram"
fx.put(sweep(0.6, 2400, 300), 25.35, 0.3)
fx.put(add(bell(3200, 0.5), click()), 26.05, 0.4)
fx.put(blip(1760, 0.08), 26.3, 0.25)
fx.put(blip(1760, 0.08), 26.42, 0.25)
fx.put(shing(0.8), 25.85, 0.3)
fx.put(add(impact(0.8), braam(2.0, 44) * 0.6), 27.05, 0.75)

# ---- loop: the next neutron streaks in, building to the flash at 0:00
fx.put(sweep(1.8, 300, 6000), 28.2, 0.35, 0.3)
fx.put(riser(1.8, 80, 900), 28.2, 0.4)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"), makeup_db=4.5)
