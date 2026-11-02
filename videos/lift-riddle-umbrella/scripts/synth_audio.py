"""Narration + sound for "The Lift Riddle" (the classic short-man-and-the-lift riddle, told in our own words).
NO on-screen text (owner's request): narration + sound effects only (the @SCROLL2STUDY.IN handle stays).

- Voices: Kokoro-82M — narrator am_michael, the night guard bm_george.
- Sound: a light 8-bit bed (quiet under the voice), lift ding + doors + button clicks, a stairwell climb (footsteps that
  slow down + panting), rain + thunder on the rainy day, a 5-second countdown (one clock tick per second + heartbeat +
  riser), a buzzer on "time's up", then the reveal: a sparkle, the umbrella popping open, the tip tapping 20, the ding,
  the guard's laugh; tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js (no caption cards)
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

LINES = json.load(open(os.path.join(HERE, "lines.json")))
COUNT = 5.0
GAPS = {1: 0.3, 2: 0.25, 3: 0.5, 4: 0.3, 5: 0.2, 6: 0.4, 7: COUNT + 0.2, 8: 0.3, 9: 0.3, 10: 0.25, 11: 0.3, 12: 0.35}

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.3, gaps=GAPS, max_pause=0.45)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E

B = {f"L{i}": round(A(i), 3) for i in range(len(clips))}
B["TEN"] = W(0, "ten")
B["CLIMB"] = A(1)
B["G1"] = A(2)
B["RAIN"] = A(3)
B["UP20"] = A(4)
B["TWENTY"] = W(4, "twenty")
B["G2"] = A(5)
B["Q"] = A(6)
B["COUNT0"] = Bn(6) + 0.2
B["TIMESUP"] = A(7)
B["SHORT"] = A(8)
B["REACH"] = W(8, "floor")
B["UMB"] = A(9)
B["TAP"] = A(10)
B["LIGHT"] = W(10, "floor")
B["LAUGH"] = A(11)
B["CTA"] = A(12)
B["STOP"] = Bn(12) + 0.4
B["REWIND"] = B["STOP"] + 0.7
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band, level_db=-14.0)
tracks["narrator"] = reverb(tracks["narrator"], length=0.6, wet=0.08)[:N]
tracks["guard"] = reverb(tracks["guard"], length=0.8, wet=0.12)[:N]
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.5)
captions = V.make_captions(clips, [[] for _ in clips], DUR)      # no on-screen text
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- a light bed; it holds its breath for the countdown
fx.x += CT.bed([
    S(0.0, B["RAIN"], 104, 108, "kbh"),
    S(B["RAIN"], B["Q"], 100, 104, "kb"),
    S(B["Q"], B["COUNT0"], 96, 96, "k"),
    S(B["SHORT"], B["LAUGH"], 112, 120, "kbha"),
    S(B["LAUGH"], B["STOP"] + 0.2, 128, 128, "kbhsal"),
], gain=0.42, crescendo=(0.85, 1.1))


def ding(f=1318.5):
    return add(bell(f, 1.2), 0.6 * bell(f * 0.75, 1.2))


def doors(d=0.7):
    n = int(d * SR)
    x = band(np.random.default_rng(3).standard_normal(n), 200, 2500) * np.sin(np.pi * np.arange(n) / n) * 0.5
    return x


def click():
    return F.tick(2200, 1.0)


# ---------------------------------------------------------------- 0. the evening ride (to 10 only)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(click(), 1.0, 0.4)                                                   # presses a button
fx.put(doors(), 1.2, 0.35)
fx.put(sweep(2.2, 90, 140) * 0.18, 1.6, 0.35)                               # the lift hums up
for k in range(10):
    fx.put(F.tick(2800 + 40 * k, 0.6), 1.7 + k * 0.28, 0.12)                 # floors passing
fx.put(ding(), B["TEN"], 0.35)
fx.put(doors(), B["TEN"] + 0.25, 0.3)

# ---------------------------------------------------------------- 1. ten floors of stairs: footsteps slow down, panting
for k in range(18):
    t = B["CLIMB"] + 0.1 + k * (0.22 + 0.012 * k)
    fx.put(osfx.sound(f"oga/100-sfx-2/sfx100v2_footstep_0{k % 2 + 1}", thump(150, 0.06, 1.4)), t, 0.35, (k % 2) * 0.5 - 0.25)
for k in range(4):
    fx.put(osfx.sound("oga/creatures/breath", F.whispers(0.4, seed=k)), B["CLIMB"] + 1.6 + k * 0.6, 0.18)
fx.put(osfx.sound("oga/100-sfx/door_close_01", thump(90, 0.25, 1.5)), B["G1"] - 0.2, 0.35)       # stairwell door

# ---------------------------------------------------------------- the guard's room
fx.put(osfx.lib("whoosh"), B["G1"] - 0.12, 0.35)
fx.put(F.creak(0.5, 120, seed=3), B["G1"] + 0.1, 0.25)                                         # his chair
fx.put(osfx.sfxr("blipSelect", seed=2), B["G1"] - 0.05, 0.2)                                   # CCTV switch

# ---------------------------------------------------------------- 2. rain
rain_len = B["Q"] - B["RAIN"]
amb.put(F.wind(rain_len, 2000, 6000, 0.1, seed=6) * 0.5 + band(np.random.default_rng(8).standard_normal(int(rain_len * SR)), 1500, 9000) * 0.12, B["RAIN"], 0.6)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_thunder", sub_drop(1.5)), B["RAIN"] + 0.1, 0.45)
fx.put(click(), B["UP20"] + 0.4, 0.4)
fx.put(doors(), B["UP20"] + 0.6, 0.3)
fx.put(sweep(2.4, 90, 160) * 0.18, B["UP20"] + 0.9, 0.35)
for k in range(20):
    fx.put(F.tick(2800 + 30 * k, 0.6), B["UP20"] + 0.9 + k * 0.13, 0.12)
fx.put(ding(1567.98), B["TWENTY"] + 0.3, 0.4)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.3, 500, 900)), B["G2"] + 0.05, 0.15)

# ---------------------------------------------------------------- 3. the question + the 5-second countdown
fx.put(osfx.lib("whoosh-cinematic"), B["Q"] - 0.15, 0.4)
fx.put(braam(1.6, 52), W(6, "so"), 0.3)
for k in range(5):
    t = B["COUNT0"] + k * 1.0
    fx.put(F.tick(1500, 1.0), t, 0.55)                                       # a big clock tick per second
    fx.put(F.tick(1100, 0.8), t + 0.5, 0.3)
    fx.put(heartbeat(), t + 0.1, 0.35)
fx.put(riser(COUNT, 150, 1400), B["COUNT0"], 0.3)
fx.put(add(CT.square(220, 0.45, 0.5), CT.square(233, 0.45, 0.5)) * 0.6, B["TIMESUP"] - 0.1, 0.35)    # buzzer

# ---------------------------------------------------------------- 4. the reveal
fx.put(osfx.lib("whoosh"), B["SHORT"] - 0.12, 0.4)
fx.put(CT.tone_glide(700, 300, 0.4, "square", 0.5, 0.4), W(8, "short") + 0.05, 0.2)          # "he's very short" boing-down
for k in range(3):
    fx.put(osfx.sound("oga/100-sfx/spring_01", sweep(0.2, 300, 700)), B["REACH"] + 0.2 + k * 0.4, 0.25)   # a stretch, a hop
fx.put(osfx.lib("sparkle"), B["UMB"] + 0.05, 0.3)
fx.put(add(sweep(0.18, 400, 1600), F.poof(9)), W(9, "umbrella"), 0.5)                         # the umbrella pops open
fx.put(click(), W(10, "tap") + 0.05, 0.5)                                                       # tip taps 20
fx.put(osfx.sfxr("pickupCoin", seed=11), W(10, "lights") - 0.05, 0.35)
fx.put(ding(1567.98), W(10, "lights") + 0.25, 0.45)
fx.put(F.harp_up(), W(10, "lights") + 0.3, 0.3)
fx.put(osfx.sound("oga/creatures/grunt_02", sweep(0.3, 300, 200)), B["LAUGH"] + 0.6, 0.15)
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.12, 0.4)
fx.put(osfx.sfxr("powerUp", seed=4), B["CTA"] + 0.05, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
for i in range(1, len(clips)):                                              # a soft whoosh on every new line (fast cuts)
    fx.put(osfx.lib("whoosh-short"), A(i) - 0.06, 0.08)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=1.0, makeup_db=5.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.85, makeup_db=2.0)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({k: round(v, 3) for k, v in B.items()}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
print("DUR", DUR, "captions", len(captions))
