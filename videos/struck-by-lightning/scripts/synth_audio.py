"""Sound effects for the lightning video (no narration, no text sounds).

Writes assets/audio/sfx.wav. Event times mirror index.html.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()

# ---- ambience: rain + wind outside (same level at 0s and 30s for the loop), body hum inside
outside = np.clip(seg(-1, 8.1, 0.25) + seg(22.4, 31, 0.25), 0, 1)
inside = seg(7.9, 22.6, 0.3)
for ch in range(2):
    rain = norm(band(rng.standard_normal(N), 1500, 9000))
    patter = norm(band(rng.standard_normal(N), 300, 1500))
    rumble = norm(band(rng.standard_normal(N), 25, 120))
    amb.x[:, ch] += (0.45 * rain + 0.3 * patter) * outside + 0.55 * rumble * inside + 0.2 * rumble * outside


def thunder(d, seed):
    n = int(d * SR)
    r = np.random.default_rng(seed)
    x = band(r.standard_normal(n), 30, 400)
    # rolling bumps
    bumps = np.zeros(n)
    for _ in range(8):
        c = r.uniform(0, d * 0.7)
        bumps += np.exp(-((np.arange(n) / SR - c) ** 2) / (2 * 0.12 ** 2)) * r.uniform(0.4, 1)
    return norm(x * (0.3 + bumps) * np.exp(-np.arange(n) / (d * 0.45 * SR)))


# distant thunder in the hook and at the end
fx.put(thunder(3.0, 5), 1.35, 0.5)
fx.put(thunder(2.8, 6), 27.15, 0.45)

# ---- the strike
fx.put(riser(0.45, 300, 2400) * 0.6 + 0.4 * norm(band(rng.standard_normal(int(0.45 * SR)), 3000, 9000)) * np.linspace(0, 1, int(0.45 * SR)) ** 2, 3.55, 0.45)
crack = add(1.0 * noise_hit(0.25, 40, 12000), 1.3 * thump(38, 1.2, 4.0), 0.8 * noise_hit(0.08, 2000, 12000))
fx.put(reverb(np.concatenate([crack, np.zeros(SR)]), 1.8, 0.5, 3), 4.0, 1.0)
fx.put(thunder(3.4, 7), 4.15, 0.9)
# x-ray electric buzz while the bolt flickers
n = int(0.5 * SR)
tt = np.arange(n) / SR
buzz = band(np.sign(np.sin(2 * np.pi * 120 * tt)) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)), 100, 4000)
fx.put(norm(buzz) * env(n, 0.005, 0.1), 4.0, 0.45)
# body hits the ground, then smoke sizzle
fx.put(add(thump(70, 0.35, 0.8), 0.6 * noise_hit(0.2, 80, 900)), 5.1, 0.8)
n = int(3.0 * SR)
sizzle = norm(band(rng.standard_normal(n), 3000, 9000)) * (0.5 + 0.5 * (rng.random(n) > 0.995))
fx.put(sizzle * env(n, 0.2, 1.5), 4.6, 0.12)
# dive into the arm
fx.put(sweep(1.4, 150, 3500), 6.8, 0.55)

# ---- skin: zaps as current races across, then a crystalline swell as the ferns grow
for i in range(26):
    t0 = 8.1 + i * 0.125
    fx.put(add(noise_hit(0.06, 2500, 11000), 0.5 * blip(1800 + (i % 5) * 300, 0.05)), t0, 0.32, (i % 7 - 3) / 4)
n = int(2.3 * SR)
tt = np.arange(n) / SR
hum = band(np.sign(np.sin(2 * np.pi * 60 * tt)), 50, 2000) * env(n, 0.05, 0.3)
fx.put(norm(hum), 8.1, 0.18)
for k, f in enumerate([784, 988, 1175, 1568, 1976]):
    fx.put(bell(f, 1.8), 11.6 + k * 0.55, 0.16, (k - 2) / 3)
fx.put(sweep(1.0, 200, 3000), 15.0, 0.4)

# ---- heart: beats + monitor beeps, flatline, spark restart
beats = [b for b in np.arange(16.1, 15.0, -0.8)] + [b for b in np.arange(19.25, 22.5, 0.86)]
for b in beats:
    if 15.6 <= b < 22.5:
        fx.put(heartbeat(), b - 0.03, 0.75)
        fx.put(blip(1000, 0.08), b, 0.18)
# flatline tone while stopped
n = int((19.15 - 16.45) * SR)
tt = np.arange(n) / SR
flat = np.sin(2 * np.pi * 1000 * tt) * env(n, 0.01, 0.05)
fx.put(flat, 16.45, 0.16)
# the spark
fx.put(add(noise_hit(0.15, 1500, 10000), thump(60, 0.5, 2.0)), 19.2, 0.9)
fx.put(riser(0.3, 400, 1600), 18.95, 0.3)
fx.put(sweep(0.9, 3000, 200), 22.0, 0.45)

# ---- CPR compressions (2 per second), getting up, helper leaves
for k in range(6):
    fx.put(add(thump(85, 0.12, 0.4), 0.3 * noise_hit(0.06, 150, 1200)), 22.95 + k * 0.5, 0.55)
for ts in [27.65, 28.1, 28.55, 29.0]:
    fx.put(add(noise_hit(0.1, 100, 1500), 0.4 * thump(90, 0.12, 0.4)), ts, 0.45, 0.5)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
