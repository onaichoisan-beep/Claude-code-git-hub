"""Sound effects for the swallowing-gum video (no narration, no text sounds).

Writes assets/audio/sfx.wav. Event times mirror index.html.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()

# ---- ambience: airy room tone outside, deep body rumble inside
outside = np.clip(seg(-1, 3.8, 0.3) + seg(24.9, 31, 0.3), 0, 1)
inside = seg(3.6, 25.1, 0.3)
for ch in range(2):
    air = norm(band(rng.standard_normal(N), 200, 2500))
    rumble = norm(band(rng.standard_normal(N), 25, 150))
    amb.x[:, ch] += 0.18 * air * outside + 0.6 * rumble * inside


def smack():
    return add(noise_hit(0.05, 600, 5000) * 0.7, thump(220, 0.06, 0.4) * 0.4)


def gurgle(d=0.5, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros(int(d * SR))
    for _ in range(6):
        b = bubble(0.8 + r.random() * 1.6)
        i = int(r.uniform(0, d - 0.15) * SR)
        out[i : i + len(b)] += b[: len(out) - i] * r.uniform(0.4, 1)
    return out


# ---- hook: chew, inflate, POP, chew, GULP
fx.put(smack(), 0.05, 0.6)
n = int(1.9 * SR)
tt = np.arange(n) / SR
inflate = np.sin(2 * np.pi * np.cumsum(180 + 260 * tt / 1.9) / SR) * 0.3 + norm(band(rng.standard_normal(n), 800, 4000)) * 0.5
fx.put(inflate * env(n, 0.2, 0.05) * (tt / 1.9 + 0.2), 0.3, 0.35)
fx.put(add(noise_hit(0.08, 500, 9000), 0.8 * thump(300, 0.08, 1.5)), 2.2, 1.0)
for ts in [2.6, 2.75]:
    fx.put(smack(), ts, 0.55)
n = int(0.45 * SR)
tt = np.arange(n) / SR
gulp = np.sin(2 * np.pi * np.cumsum(420 * np.exp(-tt * 5) + 90) / SR) * np.exp(-tt / 0.2)
fx.put(add(gulp, 0.7 * thump(80, 0.3, 1.0)), 2.95, 0.9)
# x-ray reveal
fx.put(sweep(0.6, 300, 4000), 3.4, 0.5)
fx.put(blip(1320, 0.1), 3.7, 0.2)

# ---- oesophagus: a squelchy squeeze per muscle wave
for k in range(7):
    s = add(noise_hit(0.25, 80, 700) * 0.8, thump(110, 0.25, 0.6) * 0.5)
    fx.put(s, 4.5 + k * 0.55, 0.55, 0.1 * ((k % 3) - 1))
fx.put(sweep(1.2, 600, 120), 7.2, 0.35)

# ---- stomach: splash, bubbling acid, sugar fizz
fx.put(add(noise_hit(0.35, 300, 6000), thump(90, 0.3, 1.0) * 0.6), 8.5, 0.85)
for k in range(9):
    fx.put(gurgle(0.6, k), 8.8 + k * 0.5, 0.4, ((k % 5) - 2) / 3)
n = int(3.2 * SR)
fizz = norm(band(rng.standard_normal(n), 4000, 11000)) * (rng.random(n) > 0.985)
fx.put(band(fizz, 3000, 11000) * env(n, 0.3, 1.0), 9.0, 0.6)
for k, f in enumerate([1568, 1976, 2349]):
    fx.put(bell(f, 0.8), 9.1 + k * 0.7, 0.12)

# ---- the gut: slurp in, rolling gurgles and squelches as it rides along
fx.put(sweep(0.5, 800, 200), 13.5, 0.45)
for k in range(20):
    fx.put(gurgle(0.5, 40 + k), 13.9 + k * 0.48, 0.45, ((k % 7) - 3) / 4)
    if k % 2 == 0:
        fx.put(add(noise_hit(0.2, 90, 600), thump(70, 0.2, 0.4) * 0.5), 14.0 + k * 0.48, 0.4)
fx.put(sweep(0.4, 300, 2000), 23.4, 0.4)
fx.put(add(thump(160, 0.12, 2.0), noise_hit(0.05, 800, 5000) * 0.5), 23.6, 0.6)

# ---- back outside: whoosh, thumbs-up sparkle, happy chewing to the loop
fx.put(sweep(1.0, 3000, 200), 24.2, 0.5)
fx.put(blip(1320, 0.1), 25.0, 0.2)
for k, f in enumerate([1046, 1318, 1568]):
    fx.put(bell(f, 1.0), 25.5 + k * 0.08, 0.2)
for k in range(12):
    fx.put(smack(), 25.0 + k * 0.42, 0.45, 0.1)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
