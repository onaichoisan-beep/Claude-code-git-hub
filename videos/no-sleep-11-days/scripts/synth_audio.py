"""Sound effects for the no-sleep video (no narration, no text sounds)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
amb, fx = Bus(), Bus()


def tick(f=3200):
    return add(noise_hit(0.012, 2500, 9000), blip(f, 0.02) * 0.4)


def snore(d=1.6):
    n = int(d * SR)
    tt = np.arange(n) / SR
    breath = np.sin(np.pi * tt / d) ** 2
    rasp = band(rng.standard_normal(n), 80, 700) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 32 * tt)))
    return norm(rasp) * breath


def chirp(f=3200, d=0.12):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.6 * np.sin(2 * np.pi * 18 * tt))) / SR) * env(n, 0.01, d * 0.6)


# ---- room tone; an eerie low hum that grows with exhaustion
for ch in range(2):
    room = norm(band(rng.standard_normal(N), 150, 1500))
    amb.x[:, ch] += 0.12 * room
n = N
tt = np.arange(n) / SR
tired = np.clip((tt - 1.8) / 23.7, 0, 1) * (tt < 25.6)
whine = np.sin(2 * np.pi * 6200 * tt) * 0.08 * tired ** 2 + np.sin(2 * np.pi * 55 * tt) * 0.3 * tired
fx.put(whine, 0.0, 0.35)

# ---- cold open: an alarm-bell sting and a heartbeat on the twitching eyes, then rewind
fx.put(impact(0.8), 0.0, 0.8)
for k in range(8):
    fx.put(blip(1600 if k % 2 else 1800, 0.06), 0.05 + k * 0.08, 0.25)
fx.put(heartbeat(), 0.6, 0.6)
fx.put(heartbeat(), 1.15, 0.6)
fx.put(rewind(0.45), 1.6, 0.5)

# ---- the clock: ticks get faster and more frantic as the days pass
x, gap = 1.9, 0.5
while x < 25.4:
    fx.put(tick(3000 + 600 * (x > 13)), x, 0.35, 0.5)
    x += gap
    gap = max(0.16, gap * 0.985)
# day 1: pencil scribbles
for k in range(10):
    fx.put(noise_hit(0.08, 2000, 7000) * 0.6, 2.4 + k * 0.22, 0.15, 0.3)
# day 2: pencil drops, big yawn (falling hum)
fx.put(add(blip(2400, 0.03), noise_hit(0.04, 1500, 6000)), 6.7, 0.4, 0.4)
fx.put(blip(2000, 0.03), 6.85, 0.25, 0.4)
n = int(0.9 * SR)
tt = np.arange(n) / SR
yawn = band(rng.standard_normal(n), 300, 1800) * np.sin(np.pi * tt / 0.9) + 0.4 * np.sin(2 * np.pi * np.cumsum(260 - 120 * tt) / SR) * np.sin(np.pi * tt / 0.9)
fx.put(norm(yawn), 7.2, 0.35)

# ---- brain cleaning: flowing water, then it stops and gunk thuds in
fx.put(sweep(0.6, 300, 3000), 8.9, 0.35)
for k in range(10):
    fx.put(bubble(1.0 + 0.4 * (k % 3)), 9.7 + k * 0.17, 0.3, (k % 5 - 2) / 3)
n = int(1.8 * SR)
fx.put(norm(band(rng.standard_normal(n), 300, 2500)) * env(n, 0.2, 0.4), 9.6, 0.25)
for k in range(8):
    fx.put(add(thump(90, 0.15, 0.6), noise_hit(0.08, 100, 900) * 0.5), 11.7 + k * 0.18, 0.4)

# ---- hallucination: warbling detuned tones, whoosh as the sign turns into a person, helmet clunk
fx.put(sweep(0.6, 3000, 300), 13.4, 0.35)
n = int(3.4 * SR)
tt = np.arange(n) / SR
warble = np.sin(2 * np.pi * (440 + 60 * np.sin(2 * np.pi * 3 * tt)) * tt) + np.sin(2 * np.pi * (466 + 50 * np.sin(2 * np.pi * 2.3 * tt)) * tt)
fx.put(warble * env(n, 0.6, 0.6), 14.0, 0.12)
fx.put(riser(1.1, 200, 1400), 14.4, 0.3)
fx.put(add(impact(0.4), bell(988, 1.0) * 0.4), 15.5, 0.55)
fx.put(add(thump(160, 0.15, 2.0), noise_hit(0.06, 1500, 8000)), 16.6, 0.6)
# a stadium cheer in his head
n = int(1.3 * SR)
fx.put(norm(band(rng.standard_normal(n), 500, 3500)) * env(n, 0.3, 0.6), 16.7, 0.25)

# ---- microsleeps: the sound cuts out briefly each time a patch of brain goes dark
for k in range(9):
    tk = 18.6 + k / 2.2
    fx.put(sub_drop(0.3, 80, 40), tk, 0.35)
    fx.put(blip(660 - (k % 3) * 80, 0.06), tk + 0.02, 0.15)

# ---- day 11: slow heartbeat, a dull note for each number, a buzzer on "...?"
for b in np.arange(22.6, 25.5, 1.0):
    fx.put(heartbeat(), b, 0.55)
for k in range(6):
    fx.put(blip(880 - k * 70, 0.12), 23.2 + k * 0.32, 0.2)
n = int(0.5 * SR)
fx.put(band(np.sign(np.sin(2 * np.pi * 110 * np.arange(n) / SR)), 80, 2000) * env(n, 0.01, 0.1), 25.12, 0.25)

# ---- sleep: everything softens; snores, then morning birds
fx.put(sweep(1.0, 1500, 150), 25.4, 0.3)
for k in range(3):
    fx.put(snore(0.9), 25.7 + k * 0.9, 0.4)
for k in range(8):
    fx.put(chirp(2800 + (k % 4) * 350), 26.9 + k * 0.17, 0.15, (k % 5 - 2) / 3)
for k, f in enumerate([523, 659, 784]):
    fx.put(bell(f, 1.4), 27.0 + k * 0.15, 0.15)

master(amb, fx, os.path.join(HERE, "..", "assets", "audio", "sfx.wav"))
