"""Narration + SFX for "The Clockmaker Who Stole One Second".

  python3 scripts/synth_audio.py

A deep, dark-fairy-tale narrator (hall reverb, low boost) and the clockmaker's little daughter.
Clocks tick everywhere; the theft is a rising river of shimmering seconds; the cure is a heartbeat
that steadies; the years fly past as birdsong; the twist lands on a digital beep at 23:59:60.
Writes assets/audio/mix.wav + captions.js (plus the beat times the picture needs).
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

LINES = json.load(open(os.path.join(HERE, "lines.json")))["lines"]
GAPS = {1: 0.65, 2: 0.4, 3: 0.55, 4: 0.45, 5: 0.5, 6: 0.7, 7: 0.45}
TAIL = 1.8  # he tips his hat; the paid-back second falls into the city -> the opening

CAPS = [
    [("EVERY PERSON ALIVE IS|MISSING *ONE SECOND*.", "every"), ("HE *TOOK* IT.", "he")],
    [("IN A CITY OF *CLOCKS*,", "in"), ("A CLOCKMAKER'S DAUGHTER|WAS *DYING*.", "a")],
    [("PAPA...", "papa"), ("WILL I SEE THE *SPRING*?", "will")],
    [("SO HE BUILT A CLOCK|THAT COULD *STEAL TIME*.", "so"), ("JUST *ONE SECOND*...", "just"), ("FROM *EVERY PERSON*|ON EARTH.", "from")],
    [("*8 BILLION* SECONDS.", "eight"), ("THAT'S *250 YEARS*|OF LIFE.", "that's")],
    [("SHE SAW *EVERY SPRING*|AFTER THAT.", "she")],
    [("BUT A THIEF|ALWAYS *PAYS*.", "but"), ("SINCE *1972*, THE WORLD'S|CLOCKS HAVE ADDED", "since"), ("*27 EXTRA SECONDS*.", "twenty-seven")],
    [("SCIENTISTS CALL THEM|*LEAP SECONDS*.", "scientists"), ("SOME SAY...", "some"), ("HE'S *PAYING IT BACK*.", "he's")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.35, gaps=GAPS, max_pause=0.45)
DUR = round(np.ceil((clips[-1]["b"] + TAIL) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")
os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402

K = V.Words(clips)
A, B, W, E = K.A, K.B, K.W, K.E
tracks = V.voice_tracks(clips, SR, N, band, level_db=-13.0, gains={"girl": -0.5})
# the narrator: low boost + a little hall, like an old storyteller in a stone tower
n = tracks["n"]
n = n + 0.35 * band(n, 60, 220)
n = n + 0.14 * (reverb(n, 2.2, 1.0, 9) - n)
tracks["n"] = np.tanh(n * 1.2) / 1.2
voice = tracks["n"] + tracks["girl"]
duck = V.duck_env(voice, SR, depth=0.6)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()


def R(name, fallback, dur=None):
    x = load(os.path.join(ROOT, "assets", "sfx", name + ".wav"), 0, dur)
    return fade_out(x, 0.08) if x is not None else fallback


def L(name):
    x = load(os.path.join(LIB, name + ".mp3")) if LIB else None
    return x if x is not None else np.zeros(10)


def bed(sig, a, b, gain, fade=0.5, pan=0.0):
    n_ = int((b - a) * SR)
    x = np.tile(sig, int(np.ceil(n_ / len(sig))))[:n_].copy()
    f = int(fade * SR)
    if f and len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
    amb.put(x, a, gain, pan)


# beats the picture shares (written into captions.js)
T_TOOK = W(0, "took")
T_BUILD = A(3)
T_EARTH = W(3, "from")
T_POUR = A(4)
T_SPRING = A(5)
T_LEAP = A(6)
T_6060 = W(7, "leap")
T_BACK = W(7, "paying")

# ---------------------------------------------------------------- ticking: the city of clocks never stops
for k in range(int(DUR / 0.5)):
    tt_ = 0.5 * k
    if T_LEAP - 0.3 < tt_ < DUR - 1.8:  # the modern lab: digital silence, only the twist beeps
        continue
    fx.put(F.tick(2400 if k % 2 else 1700, 0.7), tt_, 0.16, -0.3)
for k in range(int(DUR / 0.37)):
    tt_ = 0.37 * k + 0.11
    if A(1) - 0.2 < tt_ < A(3) or tt_ > T_LEAP - 0.3:
        continue
    fx.put(F.tick(3300, 0.4), tt_, 0.06, 0.5)
drone = F.pad(DUR, [73.4, 110, 146.8], a=2.0, r_=2.0, seed=2)
amb.x += (0.2 * drone * (1 - seg(T_SPRING - 0.2, T_LEAP, 0.6)))[:, None]

# ---------------------------------------------------------------- HOOK: seconds pulled out of a whole city
fx.put(impact(1.1), 0.0, 0.8)
fx.put(braam(2.8, 46), 0.0, 0.45)
fx.put(R("bell", gong(98, 4.0), 4.0), 0.05, 0.4)
fx.put(add(riser(T_TOOK, 120, 900), 0.5 * F.sparkle(T_TOOK, seed=3)), 0.15, 0.22)
fx.put(add(impact(0.8), 0.6 * shing(0.6)), T_TOOK - 0.03, 0.6)
fx.put(R("clockwork", F.ratchet(0.8, 18, 1500), 1.2), T_TOOK + 0.1, 0.35)
fx.put(rewind(0.5), A(1) - 0.62, 0.5)

# ---------------------------------------------------------------- the city of clocks; the dying girl; winter
bed(R("winterwind", F.wind(6, 400, 800, 0.6, seed=11)), A(1) - 0.3, A(3), 0.35)
fx.put(R("chime", add(bell(523.3, 3.0), 0.6 * bell(392, 3.0)), 3.0), A(1) + 0.1, 0.3)
fx.put(R("gears", F.gears(2.5), 2.5), A(1) + 0.2, 0.25)
for k in range(5):
    fx.put(heartbeat(), W(1, "dying") + 0.2 + 1.05 * k, 0.32 * (1 - 0.12 * k))
fx.put(R("cough", np.zeros(10), 1.0), A(2) - 0.35, 0.25)
fx.put(F.pad(2.2, [261.6, 311.1, 392], a=0.5, r_=1.2, seed=12), A(2), 0.2)   # her question, minor and fragile

# ---------------------------------------------------------------- the machine: hammering, sparks, steam, power
for k in range(6):
    fx.put(add(bell(1800 + 300 * (k % 3), 0.5), 0.6 * noise_hit(0.04, 1500, 8000)), T_BUILD + 0.15 + 0.32 * k, 0.28, (k % 3 - 1) * 0.5)
fx.put(F.sizzle(1.4, seed=21), T_BUILD + 0.5, 0.22)
fx.put(R("steam", F.sizzle(1.0, seed=22), 1.4), W(3, "steal") - 0.1, 0.35)
fx.put(R("zap", add(noise_hit(0.3, 2000, 9000), blip(220, 0.3)), 1.0), W(3, "steal"), 0.35)
fx.put(R("clockwork", F.ratchet(1.2, 14, 1300), 1.5), W(3, "steal") + 0.3, 0.3)
fx.put(add(F.tick(1200, 1.0), thump(80, 0.3, 1.5)), W(3, "second") - 0.05, 0.6)   # THE tick
fx.put(L("whoosh-cinematic"), T_EARTH - 2.6, 0.3)
fx.put(add(sub_drop(1.6, 90, 30), 0.8 * F.sparkle(2.5, seed=23, lo=1500, hi=5000)), T_EARTH, 0.35)
fx.put(riser(A(4) - T_EARTH, 150, 1200), T_EARTH, 0.18)

# ---------------------------------------------------------------- 8 billion seconds pour into her heart
fx.put(add(impact(0.8), 0.6 * gong(110, 3.0)), T_POUR, 0.45)
fx.put(F.ratchet(B(4) - T_POUR, 30, 2200, seed=31), T_POUR + 0.1, 0.12)      # the counter spinning
fx.put(L("sparkle"), W(4, "two"), 0.35)
for k in range(4):                                                             # her heart steadies
    fx.put(heartbeat(), W(4, "two") + 0.3 + 0.75 * k, 0.4)
fx.put(F.pad(2.5, [261.6, 329.6, 392, 523.3], a=0.3, r_=1.5, seed=32), W(4, "years"), 0.3)

# ---------------------------------------------------------------- every spring after that (the years fly)
bed(R("birds", add(F.chirp(41), np.zeros(SR), F.chirp(42), np.zeros(SR // 2), F.chirp(43))), T_SPRING, T_LEAP, 0.3)
fx.put(F.harp_up(523.25, 10, 0.08), T_SPRING + 0.1, 0.2)
fx.put(F.ratchet(T_LEAP - T_SPRING - 0.4, 12, 1600, seed=51), T_SPRING + 0.2, 0.12)
fx.put(L("whoosh-cinematic"), T_LEAP - 4.5, 0.3)

# ---------------------------------------------------------------- the leap seconds; 23:59:60; he pays it back
fx.put(add(F.stab(98, 1.6), sub_drop(1.4)), T_LEAP, 0.45)
for k in range(9):  # +1, +1, +1 ... (27 of them, shown in threes)
    fx.put(L("ping") if k % 3 == 2 else blip(1320 + 60 * (k % 3), 0.07), W(6, "since") + 0.6 + 0.32 * k, 0.12)
fx.put(L("notification"), W(6, "seconds"), 0.25)
for k in range(3):
    fx.put(blip(880, 0.12), T_6060 - 1.0 + 0.33 * k, 0.25)
fx.put(add(blip(1760, 0.3), 0.6 * bell(1760, 1.5)), T_6060 + 0.05, 0.3)     # 23:59:60
fx.put(braam(2.4, 55), W(7, "some") - 0.05, 0.3)
fx.put(add(F.tick(1500, 1.0), 0.6 * reverb(np.concatenate([F.tick(1500, 1.0), np.zeros(SR)]), 2.0, 2.0, 4)), T_BACK, 0.5)
fx.put(L("sparkle"), T_BACK + 0.2, 0.35)
fx.put(R("chime", add(bell(392, 3.0), 0.6 * bell(523.3, 3.0)), 3.0), B(7) + 0.3, 0.3)
fx.put(sweep(1.0, 4000, 200), DUR - 1.0, 0.3)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.55, makeup_db=4.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({k: round(v, 3) for k, v in dict(
        TOOK=T_TOOK, BUILD=T_BUILD, EARTH=T_EARTH, POUR=T_POUR, SPRING=T_SPRING, LEAP=T_LEAP, T6060=T_6060, BACK=T_BACK).items()}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:4s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
