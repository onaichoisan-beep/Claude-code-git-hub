"""Sound for "The bird that copies a chainsaw" (superb lyrebird). The sound IS the story (STYLE_GUIDE.md section 6):
every copied sound (chainsaw, kookaburra, whipbird, songbirds, camera shutter, car alarm) is synthesised and plays exactly
while the beak is open (MIMIC list -> window.BEATS.MIMIC, shared with the picture), the SOUNDS COPIED counter ticks with
each; in the dance the copies land on the beat of an 8-bit groove and come faster and faster. No cold-open hook.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 30.0
B = dict(MEET=2.6, KOOK=5.1, CAMERA=10.0, BREAK=15.75, HIT=16.0, DANCE=17.5, FEMALE=22.5, CTA=25.5, STOP=28.5, REWIND=29.3)

# [time, kind, duration, how many it adds to the counter]
MIMIC = [[0.3, "saw", 1.9, 1], [5.2, "kook", 1.4, 1], [6.9, "whip", 0.9, 1], [8.0, "bird", 0.6, 1], [8.8, "bird", 0.6, 1],
         [10.0, "cam", 1.3, 1], [11.7, "alarm", 1.4, 1], [13.3, "saw", 2.2, 1]]
kinds = ["saw", "cam", "alarm", "kook", "whip", "bird"]
beat = 60 / 128
t = B["DANCE"]
i = 0
while t < B["FEMALE"] - 0.2:
    MIMIC.append([round(t, 3), kinds[i % 6], round(beat * 0.8, 3), 2 if i > 6 else 1])
    t += beat if i < 6 else beat / 2
    i += 1
B["MIMIC"] = MIMIC

CARDS = [
    (0.10, 2.50, "THIS SOUND IS COMING|FROM A *BIRD*"),
    (2.60, 5.00, "MEET THE *LYREBIRD*|FROM AUSTRALIA"),
    (5.10, 7.80, "IT COPIES OTHER BIRDS|*PERFECTLY*"),
    (7.90, 9.80, "KOOKABURRAS, WHIPBIRDS|AND *MORE*"),
    (10.00, 11.60, "SOME HAVE COPIED|*CAMERA SHUTTERS*"),
    (11.70, 13.20, "*CAR ALARMS*..."),
    (13.30, 15.60, "...AND *CHAINSAWS*"),
    (16.00, 17.40, "*WHY?*"),
    (17.50, 20.00, "TO IMPRESS A *FEMALE*"),
    (20.10, 22.40, "IT SINGS AND *DANCES*|AT THE SAME TIME"),
    (22.50, 25.40, "SHE'S *THINKING*|ABOUT IT..."),
    (25.50, 28.40, "TURN YOUR SOUND ON|AND *SEND THIS*"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec
R = np.random.default_rng(5)


def env(n, a=0.01, r=0.06):
    e = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def saw_wave(f):
    ph = np.cumsum(f / SR) % 1
    return 2 * ph - 1


# ---------------------------------------------------------------- the copied sounds (all synthesised)
def chainsaw(d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    rev = 0.5 - 0.5 * np.cos(2 * np.pi * np.minimum(tt / d, 1) * 1.5)          # rev up, down, up
    f = 70 + 85 * rev
    body = saw_wave(f) * 0.6 + 0.4 * np.sign(np.sin(np.cumsum(f / 2 / SR) * 2 * np.pi))
    chain = band(R.standard_normal(n), 900, 5000) * (0.6 + 0.4 * np.sign(np.sin(np.cumsum(f / SR) * 2 * np.pi)))
    x = body * 0.55 + chain / (np.max(np.abs(chain)) + 1e-9) * 0.5
    return np.tanh(x * 1.8) * env(n, 0.03, 0.12) * 0.8


def camera(d):
    out = np.zeros(int(d * SR))
    for k in range(int(d / 0.28)):
        i = int(k * 0.28 * SR)
        n = int(0.16 * SR)
        tt = np.arange(n) / SR
        click = R.standard_normal(n) * np.exp(-tt * 300) + np.sin(2 * np.pi * 2300 * tt) * np.exp(-tt * 80) * 0.6
        whirr = saw_wave(np.linspace(380, 620, n)) * np.exp(-((tt - 0.07) / 0.04) ** 2) * 0.35
        seg = (click + whirr)[: len(out) - i]
        out[i: i + len(seg)] += seg
    return out * 0.7


def car_alarm(d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = np.where((tt // 0.18) % 2 == 0, 760.0, 1080.0) * (1 + 0.15 * np.sin(2 * np.pi * 7 * tt))
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * env(n, 0.005, 0.05) * 0.45


def kookaburra(d):
    notes = [520, 600, 700, 820, 900, 980, 900, 980, 900, 820, 700, 620, 520]
    parts = []
    for k, f0 in enumerate(notes):
        nd = d / len(notes)
        n = int(nd * SR)
        tt = np.arange(n) / SR
        f = f0 * (1 + 0.25 * np.sin(2 * np.pi * 28 * tt))
        x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + band(R.standard_normal(n), 800, 3000) * 0.3
        parts.append(x * np.sin(np.pi * np.arange(n) / n))
    return np.concatenate(parts) * 0.6


def whipbird(d):
    n1 = int((d - 0.12) * SR)
    tt = np.arange(n1) / SR
    whistle = np.sin(2 * np.pi * np.cumsum(np.linspace(1150, 1350, n1)) / SR) * env(n1, 0.05, 0.02)
    crack = CT.tone_glide(1500, 7000, 0.1, "sine", 0.5, 1.0) + 0.6 * np.concatenate([R.standard_normal(int(0.004 * SR)), np.zeros(int(0.096 * SR))])[: int(0.1 * SR)]
    return np.concatenate([whistle * 0.5, crack[: int(0.12 * SR)] * 0.8])


def songbird(seed):
    return F.chirp(seed) * 1.2


MAKERS = {"saw": chainsaw, "cam": camera, "alarm": car_alarm, "kook": kookaburra, "whip": whipbird}
for k, (tm, kind, d, _) in enumerate(MIMIC):
    sig = songbird(40 + k) if kind == "bird" else MAKERS[kind](d)
    fx.put(sig, tm, 0.75, -0.25)

# ---------------------------------------------------------------- the 8-bit bed: quiet under the copies, a full groove for the dance
fx.x += CT.bed([
    S(0.0, B["KOOK"], 96, 96, "kb", gain=0.6),
    S(B["KOOK"], B["CAMERA"], 104, 108, "kbh", gain=0.7),
    S(B["CAMERA"], B["BREAK"], 110, 124, "kbha", gain=0.8),
    S(B["DANCE"], B["FEMALE"], 128, 128, "kbhsal"),
    S(B["FEMALE"], B["CTA"], 112, 112, "kbha", gain=0.8),
    S(B["CTA"], B["STOP"] + 0.2, 128, 132, "kbhsal"),
], gain=0.45, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- a sound on every change
CT.card_blips(fx, CARDS, gain=0.14)
for tm, kind, d, c in MIMIC:                                       # the counter ticks with every copy
    fx.put(F.tick(3200, 0.8), tm + 0.02, 0.3, 0.6)
amb.x += (0.25 * F.wind(DUR, 400, 900, 0.2, seed=3) * seg(0, B["BREAK"], 0.5))[:, None]
for k in range(6):
    fx.put(F.chirp(80 + k), 3.0 + k * 0.35, 0.2, 0.7)              # real forest birds in the background while we meet it

# ---------------------------------------------------------------- BREAK -> the tail fans out (SHOWTIME)
fx.put(sweep(B["HIT"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.5)
fx.put(osfx.lib("whoosh-cinematic"), B["HIT"] - 0.05, 0.8)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(F.harp_up(523.25, 10, 0.05), B["HIT"] + 0.1, 0.45)
fx.put(osfx.lib("sparkle"), B["HIT"] + 0.2, 0.5)

# ---------------------------------------------------------------- the female arrives, thinks, likes it
for k in range(5):
    fx.put(F.tick(4800, 0.5), B["FEMALE"] - 0.5 + k * 0.18, 0.2, -0.6)
fx.put(osfx.sound("oga/retro-synth/synth_beep_03", blip(700)), B["FEMALE"] + 0.9, 0.35)
fx.put(add(bell(1046.5, 1.4), 0.5 * bell(1318.5, 1.4)), B["CTA"] + 0.1, 0.45)
fx.put(osfx.sfxr("powerUp", seed=14), B["CTA"] + 0.15, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 96, 96, "kb", gain=0.6)], gain=0.45, crescendo=(0.8, 0.8))

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=6.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR, "mimics", len(MIMIC), "count", sum(m[3] for m in MIMIC))
