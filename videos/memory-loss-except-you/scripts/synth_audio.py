"""Narration + fast thriller sound for "Every human lost their memory overnight. Except you." (story mode, fast cut).

- Voices: Kokoro-82M (make_voices_kokoro.py) — narrator af_heart, mom af_bella, the man am_fenrir, the note af_nicole —
  much more human than edge-tts. Light processing only (no squeezing of natural pauses beyond 0.45 s).
- Captions: built automatically, 1-3 words at a time, word-synced (the reference's word-by-word captions, but faster).
- Sound (the owner asked for fast pacing, not the reference's slow drone): a dark pulse (sub kick + ticking hats, no 8-bit
  melody) 124 -> 152 BPM, a heartbeat in the chase, and a literal effect on almost every phrase; it drops to a drone + clock
  for the twist, then silence and one deep hit on the last question; tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import json
import os
import re
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

LINES = json.load(open(os.path.join(HERE, "lines.json")))
GAPS = {1: 0.25, 2: 0.3, 3: 0.2, 4: 0.2, 5: 0.3, 6: 0.25, 7: 0.15, 8: 0.1, 9: 0.35, 10: 0.2, 11: 0.25, 12: 0.25,
        13: 0.45, 14: 0.3, 15: 0.35, 16: 0.4, 17: 0.45}
GOLD = {"memory", "except", "you.", "mom.", "name.", "billion", "rule", "one.", "two.", "three.", "anyone.", "hands.", "drive.",
        "run.", "everything", "four.", "nine.", "notebook.", "handwriting.", "trust", "remember.", "forget?", "full."}
RED = {"get", "out", "house!", "strangers.", "run.", "don't", "trust", "forget?"}

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.25, gaps=GAPS, max_pause=0.45)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E


def auto_caps():
    """1-3 words per card, a new card at every comma/full stop; *gold* keywords"""
    caps = []
    for c in clips:
        chunks, cur = [], []
        for w in c["w"]:
            cur.append(w[0])
            if re.search(r"[.,!?]$", w[0]) or len(cur) == 3:
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
        out = []
        for ch in chunks:
            words = []
            for w in ch:
                lw = w.lower()
                words.append(f"*{w.upper()}*" if lw in GOLD or lw.strip(".,!?") in GOLD else w.upper())
            out.append((" ".join(words).replace("* *", " "), re.sub(r"[^A-Za-z0-9']", "", ch[0]).lower() or ch[0]))
        caps.append(out)
    return caps


CAPS = auto_caps()

B = {f"L{i}": round(A(i), 3) for i in range(len(clips))}
B["EXCEPT"] = A(1)
B["MOM"] = A(2)
B["CROWD"] = A(4)
B["R1"] = A(5)
B["STREET"] = A(6)
B["CARS"] = W(6, "cars")
B["MAN"] = A(7)
B["RUN"] = A(8)
B["R2"] = A(9)
B["NOTES"] = [W(10, "names"), W(10, "faces"), W(10, "phone"), W(10, "your")]
B["DAY4"] = A(11)
B["R3"] = A(12)
B["DAY9"] = A(13)
B["PAGE"] = A(14)
B["NOTE"] = A(15)
B["BUT"] = A(16)
B["LAST"] = A(17)
B["HIT"] = W(17, "forget")
B["BREAK"] = B["HIT"] - 0.25
B["STOP"] = Bn(17) + 0.9
B["REWIND"] = B["STOP"] + 0.7
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band, level_db=-14.0, gains={"note": 1.0})
tracks["narrator"] = reverb(tracks["narrator"], length=0.6, wet=0.08)[:N]                    # a small room, natural
tracks["note"] = reverb(tracks["note"] + 0.3 * band(tracks["note"], 60, 300), length=2.4, wet=0.4)[:N]   # the eerie note
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.5)
captions = V.make_captions(clips, CAPS, DUR, hold=0.25)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the dark pulse (kick + hats + snare only: no 8-bit melody)
fx.x += CT.bed([
    S(0.0, B["EXCEPT"], 96, 96, "k"),
    S(B["EXCEPT"] + 0.3, B["R1"], 124, 124, "kh"),
    S(B["R1"], B["MAN"], 128, 132, "khs"),
    S(B["RUN"], B["R2"], 152, 152, "khs"),
    S(B["R2"], B["DAY9"] - 0.3, 132, 136, "khs"),
], gain=0.55, crescendo=(0.9, 1.1))


def sub_pulse(t0, t1, bpm, f=49.0, gain=1.0):
    t = t0
    while t < t1:
        n = int(0.35 * SR)
        tt = np.arange(n) / SR
        fx.put(np.sin(2 * np.pi * f * tt) * np.exp(-tt * 9) * np.minimum(1, tt / 0.01), t, 0.35 * gain)
        t += 60 / bpm


sub_pulse(B["EXCEPT"] + 0.3, B["MAN"], 124)
sub_pulse(B["RUN"], B["R2"], 152, gain=1.2)
sub_pulse(B["R2"], B["DAY9"] - 0.3, 132)
amb.x += (0.22 * F.drone(DUR, 52, seed=5))[:, None]                                          # the tension drone, always under

# ---------------------------------------------------------------- 0. the globe: a "?" pops over every city
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.45)
fx.put(braam(2.2, 49), 0.05, 0.4)
for k in range(28):
    t = 0.35 + 2.0 * (k / 28) ** 0.7
    fx.put(osfx.lib("pop") if k % 2 else CT.square(900 + 40 * k, 0.04, 0.25), t, 0.22 if k % 2 else 0.12, ((k * 7) % 5 - 2) * 0.35)

# ---------------------------------------------------------------- 1. except you
fx.put(impact(0.8), B["EXCEPT"], 0.6)
fx.put(sub_drop(0.9), B["EXCEPT"], 0.5)
fx.put(F.sparkle(1.0, seed=3), B["EXCEPT"] + 0.05, 0.35)
fx.put(heartbeat(), B["EXCEPT"] + 0.35, 0.45)

# ---------------------------------------------------------------- 2-3. mom
fx.put(osfx.sound("oga/100-sfx/door_close_01", thump(90, 0.3, 1.5)), B["MOM"] - 0.15, 0.55)
fx.put(osfx.sound("oga/100-sfx/pot_01", F.tick(1800, 1.0)), W(2, "get") - 0.05, 0.6)               # the frying pan
fx.put(osfx.lib("whoosh"), W(2, "get") - 0.1, 0.35)
fx.put(osfx.sound("oga/100-sfx/glass_02", F.tick(4200, 0.8)), A(3) + 0.1, 0.3)                    # the photo frame
fx.put(CT.womp(330, 3, 0.18), W(3, "name") + 0.2, 0.18)

# ---------------------------------------------------------------- 4. 8 billion strangers
fx.put(osfx.lib("whoosh-cinematic"), B["CROWD"] - 0.15, 0.5)
fx.put((0.5 * F.chatter(3.0, seed=4)), B["CROWD"], 0.35)
for k in range(10):
    fx.put(F.tick(2600 + 120 * k, 1.0), B["CROWD"] + 0.1 + k * 0.12, 0.25)

# ---------------------------------------------------------------- rules: a stamp each
for i, r in ((1, B["R1"]), (2, B["R2"]), (3, B["R3"])):
    fx.put(osfx.lib("whoosh"), r - 0.15, 0.45)
    fx.put(osfx.sound("oga/100-sfx/slam_0" + str(i + 1), impact(0.8)), r + 0.02, 0.6)
    fx.put(impact(0.6), r, 0.4)
fx.put(band(np.random.default_rng(3).standard_normal(int(0.35 * SR)), 2000, 7000) * np.linspace(1, 0, int(0.35 * SR)) * 0.4,
       W(5, "don't") + 0.05, 0.4)                                                             # "shh"

# ---------------------------------------------------------------- 6. the street: hands, horns, a crash
fx.put(osfx.lib("whoosh-cinematic"), B["STREET"] - 0.2, 0.5)
fx.put((0.5 * F.chatter(6.0, seed=9)), B["STREET"], 0.3)
for k in range(3):
    fx.put(add(CT.square(415, 0.35, 0.5), CT.square(523, 0.35, 0.5)) * 0.5, B["CARS"] + 0.1 + k * 0.45, 0.22, (k - 1) * 0.6)  # horns
fx.put(osfx.sound("oga/100-sfx/explosion_01", impact(0.8)), W(6, "road"), 0.35)                    # crunch
fx.put(osfx.sound("oga/100-sfx/glass_04", F.glass_smash(5) if hasattr(F, "glass_smash") else impact(0.4)), W(6, "road") + 0.05, 0.3)
fx.put(CT.womp(392, 3, 0.15), W(6, "drive") + 0.25, 0.18)

# ---------------------------------------------------------------- 7-8. the man, RUN
fx.put(osfx.lib("whoosh"), B["MAN"] - 0.12, 0.45)
fx.put(impact(0.5), B["MAN"], 0.4)
fx.put(braam(1.2, 55), B["RUN"] - 0.05, 0.4)
for k in range(16):                                                                          # running feet
    fx.put(osfx.sound(f"oga/100-sfx-2/sfx100v2_footstep_0{k % 2 + 1}", thump(140, 0.06, 1.5)), B["RUN"] + 0.15 + k * 0.17, 0.45, (k % 2) * 0.6 - 0.3)
for k in range(5):
    fx.put(heartbeat(), B["RUN"] + 0.2 + k * 0.42, 0.4)
fx.put(riser(B["R2"] - B["RUN"], 200, 1800), B["RUN"], 0.25)

# ---------------------------------------------------------------- 9-11. write everything down
def scribble(d, seed):
    n = int(d * SR)
    r = np.random.default_rng(seed)
    x = band(r.standard_normal(n), 1500, 6000)
    am = (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(14 + 8 * r.random(n)) / SR)) ** 2
    return x * am / (np.max(np.abs(x)) + 1e-9)


fx.put(scribble(0.5, 1), W(9, "write"), 0.35)
for k, t in enumerate(B["NOTES"]):
    fx.put(F.page_flip(10 + k), t - 0.05, 0.45)
    fx.put(scribble(0.35, k + 2), t + 0.08, 0.3)
    fx.put(F.tick(3000 + 300 * k, 1.0), t, 0.25)
fx.put(F.page_flip(20), B["DAY4"] - 0.05, 0.5)                                                # calendar flip
for k in range(3):
    fx.put(F.book_thud(30 + k), W(11, "three") + 0.1 + k * 0.22, 0.55)
fx.put(scribble(0.6, 9), W(12, "never") + 0.1, 0.3)

# ---------------------------------------------------------------- 13-15. day nine: the clock, the notebook, the note
fx.put(osfx.lib("whoosh-cinematic"), B["DAY9"] - 0.2, 0.5)
fx.put(F.page_flip(40), B["DAY9"], 0.5)
for k in range(int((B["BREAK"] - B["DAY9"]) / 0.5)):
    fx.put(F.tick(1800, 1.0), B["DAY9"] + 0.3 + k * 0.5, 0.35)                                 # a clock, slow and loud
fx.put(osfx.sound("oga/100-sfx/paper_02", F.page_flip(41)), W(13, "open") + 0.1, 0.5)
fx.put(heartbeat(), B["PAGE"], 0.4)
fx.put(heartbeat(), B["PAGE"] + 0.8, 0.4)
fx.put(F.whispers(2.6, seed=6), B["NOTE"] - 0.1, 0.45)
fx.put(sweep(1.0, 200, 1200) * np.linspace(0, 1, int(1.0 * SR)) * 0.4, B["NOTE"] - 1.0, 0.35)   # reverse swell
fx.put(osfx.lib("glitch-1"), W(15, "remember") + 0.1, 0.3)
fx.put(sub_drop(1.4), B["BUT"], 0.6)
fx.put(braam(2.0, 46), B["BUT"] + 0.05, 0.35)

# ---------------------------------------------------------------- 17. the question: silence, then one deep hit
fx.put(impact(1.0), B["HIT"], 0.7)
fx.put(sub_drop(1.4), B["HIT"], 0.6)
fx.put(gong(73, 3.0), B["HIT"] + 0.05, 0.3)

# ---------------------------------------------------------------- the twist gets quieter: duck the pulse after DAY9; tape-stop
env = np.ones(N)
i0 = int((B["DAY9"] - 0.3) * SR)
env[i0:] = 0.55
fx.x *= env[:, None]
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.put(braam(0.5, 49), B["REWIND"] + 0.1, 0.25)

CT.card_blips(fx, [(c["a"], c["b"], "") for c in captions], gain=0.06)
for c in captions:
    fx.put(osfx.lib("whoosh-short"), c["a"] - 0.04, 0.08)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=1.0, makeup_db=5.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8, makeup_db=2.0)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({k: (round(v, 3) if not isinstance(v, list) else [round(x, 3) for x in v]) for k, v in B.items()}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
print("DUR", DUR, "captions", len(captions))
