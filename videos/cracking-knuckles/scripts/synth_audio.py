"""Sound effects for the cracking-knuckles video (no narration, no text sounds).

Writes assets/audio/sfx.wav. Event times mirror index.html.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()

# ---- ambience: light room tone outside, fluid "inside the joint" swirl, warm hall for the doctor
outside = np.clip(seg(-1, 4.0, 0.3) + seg(26.2, 31, 0.3), 0, 1)
joint = seg(3.8, 19.5, 0.3)
doc = seg(19.3, 26.4, 0.3)
for ch in range(2):
    air = norm(band(rng.standard_normal(N), 200, 2500))
    swirl = norm(band(rng.standard_normal(N), 60, 500)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 3.1 + ch))
    hall = norm(band(rng.standard_normal(N), 100, 1200))
    amb.x[:, ch] += 0.2 * air * outside + 0.6 * swirl * joint + 0.15 * hall * doc


def crack(gain_hi=1.0):
    return add(noise_hit(0.04, 1500, 12000) * gain_hi, thump(320, 0.07, 2.5) * 0.7, noise_hit(0.12, 200, 2000) * 0.4)


# ---- the hook: grip, pull, CRACK
n = int(0.6 * SR)
rub = norm(band(rng.standard_normal(n), 800, 5000)) * env(n, 0.1, 0.3)
fx.put(rub, 1.0, 0.25, 0.5)
n = int(0.6 * SR)
tt = np.arange(n) / SR
strain = band(np.sign(np.sin(2 * np.pi * np.cumsum(30 + 60 * tt / 0.6) / SR)), 80, 1500) * (tt / 0.6) ** 2
fx.put(norm(strain), 2.0, 0.2)
fx.put(reverb(np.concatenate([crack(), np.zeros(SR // 2)]), 0.6, 0.35, 2), 2.6, 1.0)
fx.put(sweep(0.9, 200, 3500), 3.2, 0.5)
fx.put(blip(1320, 0.1), 3.9, 0.18)

# ---- inside the joint: fluid shimmer, pulling creak, the cavitation POP, then ticking time
for k, f in enumerate([660, 880, 990]):
    fx.put(bell(f, 1.2), 4.6 + k * 0.4, 0.12)
n = int(3.8 * SR)
tt = np.arange(n) / SR
creak = band(rng.standard_normal(n), 80, 700) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (14 + 20 * tt / 3.8) * tt)))
fx.put(norm(creak) * env(n, 0.5, 0.3) * (0.4 + 0.6 * tt / 3.8), 7.6, 0.4)
fx.put(riser(3.8, 90, 500), 7.6, 0.15)
pop = add(crack(1.3), thump(55, 1.0, 3.0) * 1.2, bubble(2.5) * 0.8)
fx.put(reverb(np.concatenate([pop, np.zeros(SR)]), 1.4, 0.4, 9), 11.6, 1.0)
for k in range(10):
    fx.put(bubble(0.5 + 0.1 * k), 11.75 + k * 0.05, 0.25, (k % 5 - 2) / 3)
# stopwatch ticks while the gas slowly re-dissolves
for k in range(22):
    fx.put(add(noise_hit(0.015, 3000, 9000), blip(2400, 0.015) * 0.5), 15.0 + k * 0.18, 0.3, 0.3 if k % 2 else -0.3)
fx.put(bell(1568, 0.8), 18.95, 0.18)
fx.put(sweep(0.9, 3500, 200), 19.0, 0.45)

# ---- the doctor: rapid cracks over 60 years, then a success chime
for k in range(9):
    fx.put(crack(0.8), 20.0 + k * 0.38, 0.55, 0.6)
for k, f in enumerate([523, 659, 784, 1046]):
    fx.put(bell(f, 1.4), 23.6 + k * 0.1, 0.25, (k - 1.5) / 3)
fx.put(add(thump(70, 0.3, 1.2), noise_hit(0.1, 300, 4000) * 0.4), 23.6, 0.5)

# ---- back to the hand
fx.put(sweep(0.9, 3000, 200), 25.6, 0.45)
fx.put(blip(1320, 0.1), 26.3, 0.18)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"), amb_gain=0.9, makeup_db=9.5)
