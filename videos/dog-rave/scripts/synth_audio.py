"""Sound for "What if all dogs got together and threw a rave?" — like the owner's cat-rave reference: NO narration, an EDM
track (~150 BPM four-on-the-floor) that drives everything, info chips with real dog facts, sound effects on every chip.

- EDM (pure numpy): kick, clap, off-beat hats, off-beat saw bass, supersaw chord stabs with a sidechain pump, a 16th lead
  arp in the drop; filtered intro -> groove -> snare-roll build + riser -> 0.25 s break -> DROP -> siren/howl break ->
  "4 hours later" tape-slow to silence -> calm dawn (birds, a pad) -> alarm -> the beat sneaks back for the CTA -> rewind.
- Dog FX (OpenGameArt CC0 creatures + synth): barks, a howl chorus, tennis-ball squeak, bacon sizzle, siren, crowd, zoomies.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js (chips in window.BEATS.CHIPS)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 51.0
BPM = 150.0
BEAT = 60 / BPM
B = dict(SNEAK=3.0, STREAM=5.5, COUNT=8.5, BOUNCER=12.0, DJ=15.0, BUILD=17.5, BREAK=19.75, HIT=20.0, BACON=23.0, FRAP=26.0,
         TAILS=29.0, BALL=32.0, SIREN=35.0, LATER=37.5, FIVE=40.0, SEVEN=42.5, WAIT=45.0, CTA=47.5, STOP=49.8, REWIND=50.5)
CHIPS = [
    [3.0, 5.4, "11:58 PM", "THE HUMANS ARE ASLEEP", "gold"],
    [5.5, 8.4, "EVERY DOG ON EARTH", "HAD THE SAME IDEA", "pink"],
    [8.5, 11.9, "~900 MILLION DOGS", "ROUGHLY HOW MANY LIVE ON EARTH", "cyan"],
    [12.0, 14.9, "HEAD OF SECURITY", "STRICTLY NO CATS", "pink"],
    [15.0, 17.4, "DJ BISCUIT", "DOGS HEAR UP TO ~45,000 HZ", "cyan"],
    [17.5, 19.7, "THE BUILD...", "HUMANS HEAR ONLY TO 20,000 HZ", "gold"],
    [20.0, 22.9, "45,000 HZ DROP", "THE NEIGHBOURS HEAR: NOTHING", "green"],
    [23.0, 25.9, "BACON FOG", "A DOG'S NOSE: 10,000X+ STRONGER", "amber"],
    [26.0, 28.9, "FRAP PIT", "ZOOMIES' REAL NAME: FRAPS", "pink"],
    [29.0, 31.9, "TAIL CHECK", "WAGGING TO THE RIGHT = HAPPY", "green"],
    [32.0, 34.9, "ONE TENNIS BALL", "900 MILLION DOGS. ONE BALL.", "gold"],
    [35.0, 37.4, "THE SIREN DROP", "ONE SIREN. 900 MILLION HOWLS.", "red"],
    [40.0, 42.4, "5:00 AM", "DOGS SLEEP 12-14 HOURS A DAY", "cyan"],
    [42.5, 44.9, "7:00 AM", "'AWW, HE SLEPT ALL NIGHT'", "gold"],
    [45.0, 47.4, "WAIT...", "IS THAT A VIP WRISTBAND?", "green"],
]
B["CHIPS"] = CHIPS
B["BEAT0"] = B["SNEAK"]                     # the picture bobs on the beat grid from here
B["BPM"] = BPM

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx, mus = Bus(), Bus(), Bus()
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- EDM instruments
def kick():
    n = int(0.32 * SR); tt = np.arange(n) / SR
    f = 48 + 110 * np.exp(-tt * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 1.1 + 0.3 * np.random.default_rng(1).standard_normal(n) * np.exp(-tt * 300)


def clap(seed):
    n = int(0.18 * SR); tt = np.arange(n) / SR
    x = band(np.random.default_rng(seed).standard_normal(n), 900, 4000)
    e = np.exp(-tt * 22) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * tt) > 0) * (tt < 0.03))
    return x * e / (np.max(np.abs(x)) + 1e-9)


def hat(seed, open_=True):
    n = int((0.12 if open_ else 0.04) * SR); tt = np.arange(n) / SR
    x = np.diff(np.concatenate([[0], np.random.default_rng(seed).standard_normal(n)]))
    return x * np.exp(-tt * (25 if open_ else 90)) * 0.4


def saw(f, d, det=0.0):
    n = int(d * SR)
    ph = np.cumsum(np.full(n, f * (1 + det)) / SR)
    return 2 * (ph % 1) - 1


def supersaw(freqs, d):
    out = np.zeros(int(d * SR))
    for f in freqs:
        for dt in (-0.012, -0.005, 0, 0.006, 0.013):
            out += saw(f, d, dt)
    return out / (len(freqs) * 5)


PROG = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]   # Am F C G


def put(bus, sig, t, g=1.0, pan=0.0):
    if 0 <= t < DUR:
        bus.put(sig, t, g, pan)


def beats(t0, t1):
    k = int(np.ceil((t0 - B["SNEAK"]) / BEAT - 1e-6))
    while True:
        t = B["SNEAK"] + k * BEAT
        if t >= t1:
            return
        if t >= t0:
            yield k, t
        k += 1


def chord_at(k):
    return PROG[(k // 4) % 4]


# intro: a muffled chord pad from behind the door (the party is somewhere else)
for k in range(4):
    c = PROG[k % 4]
    put(mus, band(supersaw([f / 2 for f in c] + list(c), 0.75 * 4 * BEAT), 80, 700) * 0.5, k * 4 * BEAT * 0.75, 0.35)

# groove sections (start, end, layers): k kick, c clap, h hats, b bass, s stabs, l lead
SECTIONS = [
    (B["SNEAK"], B["COUNT"], "kh"),
    (B["COUNT"], B["BUILD"], "kchbs"),
    (B["HIT"], B["SIREN"], "kchbsl"),
    (B["SIREN"], B["LATER"], "khb"),
    (B["CTA"], B["STOP"], "kchb"),
]
KICKS = []
for t0, t1, L in SECTIONS:
    for k, t in beats(t0, t1):
        c = chord_at(k)
        if "k" in L:
            put(mus, kick(), t, 0.9); KICKS.append(t)
        if "c" in L and k % 2 == 1:
            put(mus, clap(k), t, 0.45)
        if "h" in L:
            put(mus, hat(k), t + BEAT / 2, 0.35, 0.3)
            put(mus, hat(k + 99, False), t + BEAT / 4, 0.15, -0.3)
            put(mus, hat(k + 199, False), t + 3 * BEAT / 4, 0.15, -0.3)
        if "b" in L:
            put(mus, band(saw(c[0] / 4, BEAT * 0.45), 40, 400) * 0.9, t + BEAT / 2, 0.45)
        if "s" in L:
            put(mus, band(supersaw(list(c), BEAT * 0.4), 200, 5000), t + BEAT / 2, 0.3, (k % 2) * 0.4 - 0.2)
        if "l" in L:
            notes = [c[0] * 2, c[1] * 2, c[2] * 2, c[1] * 4]
            for q in range(4):
                put(mus, band(saw(notes[(q + k) % 4], BEAT / 4 * 0.7), 300, 7000) * np.linspace(1, 0.2, int(BEAT / 4 * 0.7 * SR)), t + q * BEAT / 4, 0.16, 0.3 - 0.2 * q)

# the build: snare roll accelerating + riser + rising stabs; then a 0.25 s break
t = B["BUILD"]
while t < B["BREAK"]:
    u = (t - B["BUILD"]) / (B["BREAK"] - B["BUILD"])
    put(mus, clap(int(t * 100)), t, 0.25 + 0.35 * u)
    t += BEAT / (1 if u < 0.3 else 2 if u < 0.6 else 4 if u < 0.85 else 8)
put(mus, riser(B["BREAK"] - B["BUILD"], 200, 3000), B["BUILD"], 0.45)
for k, tb in beats(B["BUILD"], B["BREAK"]):
    put(mus, band(supersaw(list(PROG[3]), BEAT * 0.3), 300 + 200 * (tb - B["BUILD"]), 6000), tb, 0.25)

# sidechain pump: duck the music right after every kick
pump = np.ones(N)
for t in KICKS:
    i = int(t * SR); n = int(BEAT * 0.8 * SR)
    seg = 0.45 + 0.55 * np.minimum(1, np.arange(n) / (0.6 * n))
    pump[i:i + n] = np.minimum(pump[i:i + n], seg[: max(0, min(n, N - i))])
for t in KICKS:                                       # but not the kick itself
    i = int(t * SR); pump[i:i + int(0.02 * SR)] = 1
mus.x *= pump[:, None]

# "4 hours later": tape-slow the music to a halt, then a calm dawn
mus.x = CT.tape_stop(mus.x, B["LATER"], B["LATER"] + 0.9)
put(mus, F.pad(B["CTA"] - B["FIVE"], [130.81, 196.0, 261.63, 329.63], a=1.2, r_=1.0), B["FIVE"], 0.25)
for k in range(8):
    put(fx, F.chirp(40 + k), B["FIVE"] + 0.6 + k * 0.9, 0.12, (k % 3 - 1) * 0.7)
for k, t in beats(B["CTA"], B["STOP"]):               # the CTA beat comes back
    pass

# ---------------------------------------------------------------- FX on every chip
def bark(i, t, g=0.5, pan=0.0):
    put(fx, osfx.sound(f"oga/creatures/barking_0{i % 2 + 1}", sweep(0.18, 700, 400)), t, g, pan)


put(fx, osfx.lib("whoosh-cinematic"), 0.0, 0.3)
put(fx, osfx.sound("oga/creatures/cute_02", blip(1300, 0.12)), 1.6, 0.35)                     # ears up
put(fx, osfx.sound("oga/100-sfx/door_open", F.creak(0.6, 140, seed=2)), B["SNEAK"] + 0.3, 0.45)   # sneaks out
for k in range(6):
    put(fx, F.tick(3200 + 200 * (k % 2), 0.7), B["SNEAK"] + 0.9 + k * 0.18, 0.3, 0.3)          # tiptoe claws
for k in range(10):
    bark(k, B["STREAM"] + 0.2 + k * 0.27, 0.3, (k % 5 - 2) * 0.4)
for k in range(14):
    put(fx, F.tick(2400 + 90 * k, 1.0), B["COUNT"] + 0.1 + k * 0.22, 0.28)                    # counter ticks
put(fx, 0.5 * F.chatter(3.2, seed=4), B["COUNT"] + 0.2, 0.3)
put(fx, osfx.sound("oga/100-sfx/slam_02", impact(0.6)), B["BOUNCER"] + 0.1, 0.5)               # "NO CATS"
put(fx, osfx.sound("oga/creatures/hurt_02", F.meow(0.5, 600)), B["BOUNCER"] + 1.2, 0.35)        # a cat, refused
put(fx, CT.womp(392, 3, 0.15), B["BOUNCER"] + 1.6, 0.2)
put(fx, sweep(0.35, 1800, 300) * 0.5, B["DJ"] + 0.1, 0.4)                                       # a scratch
put(fx, sweep(0.25, 300, 1600) * 0.5, B["DJ"] + 0.5, 0.35)
bark(0, B["DJ"] + 1.2, 0.45)
put(fx, sweep(0.25, 1400, 3000) * 0.3, B["BREAK"], 0.4)
put(fx, impact(1.0), B["HIT"], 0.8); put(fx, sub_drop(1.0), B["HIT"], 0.6)
for k in range(5):
    put(fx, osfx.sound(f"oga/bangs-fireworks/fw_0{k + 1}", F.firework(k)), B["HIT"] + 0.2 + k * 0.4, 0.25, (k % 3 - 1) * 0.6)
for k in range(8):
    bark(k, B["HIT"] + 0.1 + k * BEAT, 0.25, (k % 3 - 1) * 0.5)                                # the crowd barks on the beat
put(fx, F.sizzle(2.4, seed=5), B["BACON"] + 0.1, 0.35)
put(fx, osfx.sound("oga/creatures/nose", sweep(0.3, 900, 1500)), B["BACON"] + 0.3, 0.45)       # sniff
put(fx, osfx.sound("oga/creatures/nose", sweep(0.3, 900, 1500)), B["BACON"] + 0.8, 0.4)
for k in range(10):
    put(fx, osfx.lib("whoosh-short"), B["FRAP"] + 0.1 + k * 0.26, 0.3, (k % 2) * 1.2 - 0.6)      # zoomies
for k in range(8):
    put(fx, sweep(0.12, 500, 900) * 0.5, B["TAILS"] + 0.2 + k * BEAT / 2, 0.25, 0.6)              # wags to the right
put(fx, osfx.sfxr("pickupCoin", seed=3), B["TAILS"] + 1.0, 0.3)
put(fx, add(sweep(0.18, 1800, 2600), sweep(0.18, 2600, 1800)) * 0.4, B["BALL"] + 0.1, 0.5)     # squeak
put(fx, osfx.lib("whoosh-cinematic"), B["BALL"] + 0.3, 0.5)
put(fx, 0.6 * F.chatter(2.0, seed=8), B["BALL"] + 0.5, 0.4)
put(fx, osfx.sound("oga/100-sfx/spring_01", sweep(0.3, 300, 900)), B["BALL"] + 2.0, 0.4)


def siren(d):
    n = int(d * SR); tt = np.arange(n) / SR
    f = 700 + 250 * (np.sin(2 * np.pi * 1.2 * tt) > 0)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 * np.minimum(1, tt / 0.3)


put(fx, siren(1.2), B["SIREN"], 0.35)
for k in range(6):
    put(fx, osfx.sound("oga/creatures/howl", tone(440 + 40 * k, 1.4)), B["SIREN"] + 0.8 + k * 0.12, 0.28, (k % 3 - 1) * 0.7)
put(fx, braam(1.4, 55), B["SIREN"] + 0.8, 0.3)
put(fx, osfx.lib("whoosh"), B["LATER"] - 0.1, 0.4)
for k in range(4):
    put(fx, F.tick(1400, 0.8), B["LATER"] + 0.6 + k * 0.45, 0.3)                                 # a clock
put(fx, band(rng.standard_normal(int(1.5 * SR)), 100, 400) * 0.15, B["FIVE"] + 0.2, 0.3)   # snoring
for k in range(3):
    put(fx, F.tick(2000, 0.6), B["FIVE"] + 0.4 + k * 0.7, 0.15)
for k in range(4):
    put(fx, add(CT.square(1760, 0.08, 0.5), CT.square(1760, 0.08, 0.5)), B["SEVEN"] + 0.1 + k * 0.22, 0.2)   # alarm beeps
put(fx, osfx.sound("oga/creatures/cute_04", blip(1100, 0.15)), B["SEVEN"] + 1.3, 0.3)
put(fx, osfx.lib("whoosh"), B["WAIT"] - 0.1, 0.4)
put(fx, osfx.sfxr("powerUp", seed=9), B["WAIT"] + 0.2, 0.35)
put(fx, F.sparkle(1.0, seed=9), B["WAIT"] + 0.25, 0.3)
put(fx, osfx.sfxr("blipSelect", seed=5), B["CTA"] + 0.1, 0.35)
bark(1, B["CTA"] + 0.6, 0.45)

# a blip + whoosh on every chip (a sound on every change)
for a, b, *_ in CHIPS:
    put(fx, CT.square(1760, 0.04, 0.25), a, 0.12); put(fx, CT.square(2637, 0.03, 0.25), a + 0.04, 0.08)
    put(fx, osfx.lib("whoosh-short"), a - 0.05, 0.15)

# ---------------------------------------------------------------- loop: tape-stop -> rewind -> frame 1
fx.x += mus.x * 1.0
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
put(fx, rewind(0.5), B["REWIND"] - 0.05, 0.8)
put(fx, osfx.lib("glitch-2"), B["REWIND"], 0.35)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=4.0)
CT.write_captions(ROOT, DUR, [], B, V.segs)
print("DUR", DUR)
