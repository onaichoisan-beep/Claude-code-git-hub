"""Cinematic sound effects for the Narasimha video (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()

# ---- ambience: low temple drone + lamp crackle in the palace, wind at dusk
palace = seg(1.7, 24.6, 0.4)
for ch in range(2):
    drone = norm(band(rng.standard_normal(N), 40, 180))
    crackle = norm(band(rng.standard_normal(N), 2000, 6000)) * (rng.random(N) > 0.997)
    wind = norm(band(rng.standard_normal(N), 300, 1500))
    amb.x[:, ch] += 0.5 * drone * palace + 0.25 * band(crackle, 1500, 7000) * seg(1.7, 14.2) + 0.2 * wind * seg(16, 30, 0.5)

# ---- COLD OPEN: boom + roar, debris, then rewind
fx.put(impact(), 0.0, 1.0)
fx.put(roar(1.4), 0.05, 0.9)
fx.put(braam(2.0, 49), 0.0, 0.6)
fx.put(rewind(0.45), 1.4, 0.55)

# ---- the boon: a taiko + metal clank per condition, brass hit on "unkillable"
for k, tc in enumerate([2.4, 3.1, 3.8, 4.5, 5.2]):
    fx.put(taiko(70 + k * 4), tc, 0.85)
    fx.put(shing(0.3), tc + 0.02, 0.18)
fx.put(braam(2.2, 55), 5.8, 0.75)
fx.put(sweep(0.6, 300, 3000), 7.1, 0.4)

# ---- the hall: drum roll of rising tension, temple bell for Prahlad, the strike
for tt_, sig in drum_roll(7.6, 11.5, 0.55, 0.14, 66):
    fx.put(sig, tt_, 0.55)
fx.put(bell(660, 2.0), 9.8, 0.3)
fx.put(sweep(0.5, 200, 2500), 11.05, 0.5)
fx.put(add(impact(0.6), noise_hit(0.2, 300, 6000)), 11.6, 0.9)
n = int(2.6 * SR)
rumble = norm(band(rng.standard_normal(n), 25, 200)) * np.linspace(0.2, 1, n) ** 1.5
fx.put(rumble, 11.65, 0.8)
for k in range(14):
    fx.put(noise_hit(0.05, 1500, 8000), 11.8 + k * 0.15, 0.25 + 0.02 * k, (k % 5 - 2) / 3)
fx.put(riser(2.4, 80, 900), 11.8, 0.3)

# ---- the burst: huge hit, roar, conch, falling debris
fx.put(impact(1.3), 14.2, 1.0)
fx.put(braam(3.0, 41), 14.2, 0.85)
fx.put(roar(1.8, 85), 14.3, 1.0)
fx.put(sub_drop(1.4), 14.2, 0.7)
fx.put(conch(1.6), 14.9, 0.35)
for k in range(10):
    fx.put(add(noise_hit(0.08, 200, 3000), thump(140, 0.08, 0.5) * 0.5), 14.6 + k * 0.13, 0.35, (k % 5 - 2) / 3)

# ---- the loophole: a stamp + chime for each beaten condition, a glint for the claws
fx.put(sweep(0.5, 3000, 300), 15.9, 0.4)
for k, tc in enumerate([16.4, 18.0, 19.6, 21.2, 22.8]):
    fx.put(taiko(80), tc, 0.9)
    fx.put(bell(880 * (1 + 0.12 * k), 1.0), tc + 0.05, 0.3)
fx.put(shing(0.6), 22.85, 0.5)
fx.put(riser(1.6, 100, 1200), 22.9, 0.25)
# the final blow happens in the flash
fx.put(impact(1.2), 24.7, 1.0)
fx.put(gong(98, 4.0), 24.7, 0.6)

# ---- peace: conch, bells
fx.put(conch(2.2, 300), 25.2, 0.45)
for k, f in enumerate([523, 659, 784]):
    fx.put(bell(f, 1.6), 25.6 + k * 0.35, 0.2)

# ---- back to the roar (loops into the cold open)
fx.put(sweep(0.8, 200, 3000), 27.3, 0.45)
fx.put(roar(1.4), 28.6, 0.8)
fx.put(riser(1.4, 120, 900), 28.6, 0.3)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
