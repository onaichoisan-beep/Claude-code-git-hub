"""Sound effects for the firework-colours video: launches, bursts, crackle, sparkle. No narration, no text sounds."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def whistle(d=0.7):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(900 + 1500 * tt / d) / SR) * 0.5 + band(rng.standard_normal(n), 2000, 6000) * 0.3
    return s * env(n, 0.05, 0.05) * (0.4 + 0.6 * tt / d)


def burst(big=1.0):
    n = int(0.12 * SR)
    hit = add(thump(55, 0.9, 2.0) * 1.2, noise_hit(0.4, 60, 3000) * 0.9, noise_hit(0.05, 2000, 9000) * 0.5)
    return norm(reverb(np.concatenate([hit, np.zeros(SR)]), 1.6, 0.4 * big, 4))


def crackle(d=1.6, seed=0):
    r = np.random.default_rng(seed)
    n = int(d * SR)
    out = np.zeros(n)
    for _ in range(int(40 * d)):
        i = int(r.uniform(0, d - 0.02) * SR)
        c = noise_hit(0.012, 2500, 10000)
        out[i : i + len(c)] += c[: n - i] * r.uniform(0.3, 1)
    return out * np.linspace(1, 0.2, n)


def shell(t0, big=1.0, seed=0, pan=0.0):
    fx.put(whistle(0.68), t0, 0.22 * big, pan)
    fx.put(burst(big), t0 + 0.7, 0.75 * big, pan)
    fx.put(crackle(1.6, seed), t0 + 0.85, 0.3 * big, pan)


# ---- night ambience: distant crowd hum + far-off fireworks
for ch in range(2):
    crowd = norm(band(rng.standard_normal(N), 200, 1500)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 4.0 + ch))
    amb.x[:, ch] += 0.18 * crowd
for k in range(14):
    fx.put(burst(0.3), 0.5 + k * 2.1 + (k % 3) * 0.3, 0.08, (k % 5 - 2) / 3)

# ---- hook: five shells together
for k, (t0, pan) in enumerate([(-0.6, 0), (-0.45, -0.5), (-0.3, 0.5), (-0.1, -0.2), (0.0, 0.3)]):
    tt0 = max(0.0, t0 + 0.7) - 0.7
    fx.put(burst(1.0), max(0.0, t0 + 0.7), 0.7, pan)
    fx.put(crackle(1.6, k), max(0.0, t0 + 0.85), 0.3, pan)

# ---- into the atom: whoosh, heat rush, electron jump (up) and photon (sparkle)
fx.put(sweep(0.6, 300, 4000), 1.6, 0.45)
n = int(0.9 * SR)
fx.put(norm(band(rng.standard_normal(n), 200, 2000)) * env(n, 0.2, 0.2), 2.6, 0.3)
fx.put(riser(0.5, 300, 1400), 3.0, 0.4)
fx.put(sweep(0.3, 2000, 400), 4.6, 0.3)
fx.put(bell(1568, 1.2), 4.78, 0.35)
fx.put(bell(2093, 1.0), 4.85, 0.2)

# ---- the parade: one big shell + two small per colour, chime on the element card
for k, tp in enumerate([6.4, 9.4, 12.4, 15.4, 18.4]):
    shell(tp, 1.0, 10 + k)
    shell(tp + 0.35, 0.6, 20 + k, -0.6)
    shell(tp + 0.55, 0.6, 30 + k, 0.6)
    fx.put(bell([784, 880, 988, 1046, 1175][k], 1.0), tp + 0.75, 0.22)

# ---- blue: launch, then the heat rises and the colour fizzles
shell(21.3, 1.0, 50)
fx.put(riser(1.2, 200, 1200), 22.4, 0.25)
n = int(1.0 * SR)
fx.put(norm(band(rng.standard_normal(n), 3000, 9000)) * np.linspace(1, 0, n), 23.6, 0.3)
fx.put(add(thump(110, 0.25, 0.6), blip(220, 0.25) * 0.5), 23.65, 0.4)

# ---- finale: the grand show
for k, (t0, pan) in enumerate([(25.0, 0), (25.25, -0.6), (25.45, 0.6), (25.7, -0.3), (25.9, 0.3)]):
    shell(t0, 1.0, 60 + k, pan)
for k, f in enumerate([523, 659, 784, 1046]):
    fx.put(bell(f, 1.6), 25.6 + k * 0.12, 0.15)
# launches for the loop back into the hook
for k, t0 in enumerate([29.4, 29.55, 29.7]):
    fx.put(whistle(0.6), t0, 0.2, (k - 1) / 2)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
