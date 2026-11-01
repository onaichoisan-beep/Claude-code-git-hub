"""Narration + fast sound for "The king who lost to a grain of rice" (the chessboard doubling legend), narrated on request.

- Narrated: narrator (the ancestors-video voice), the king (deep Indian voice), the sage (an older Indian voice).
- SIGNATURE = the rice pour. Every new SQUARE on the counter is a wooden tick + a grain trickle a semitone higher than the
  last; the trickle thickens with the square number until it is a roaring avalanche; 0.3 s break; square 64 slams.
- Court: gong + fanfare; "Granted!" laugh; "Checkmate" = a wooden chess-piece clack + bell. Fast pacing: nonstop 8-bit bed
  120 -> 172 BPM, a blip on every caption chunk, whoosh + hit on every cut, tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
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
GAPS = {1: 0.25, 2: 0.2, 3: 0.2, 4: 0.3, 5: 0.2, 6: 0.15, 7: 0.25, 8: 0.35, 9: 0.3, 10: 0.35}

CAPS = [
    [("A KING LOST *EVERYTHING*|TO A FEW GRAINS OF RICE", "a")],
    [("YOU INVENTED *CHESS*?", "you"), ("NAME YOUR *REWARD*!", "name")],
    [("JUST *RICE*.", "just"), ("1 GRAIN ON THE FIRST SQUARE,|THEN *DOUBLE IT* ON EVERY SQUARE", "one")],
    [("ONLY RICE?|*GRANTED!*", "only")],
    [("SQUARE 1: *1 GRAIN*", "square"), ("SQUARE 10: *512*", "square"), ("SQUARE 20: *HALF A MILLION*", "square")],
    [("SQUARE 32: *2 BILLION*", "square"), ("ABOUT *50 TONNES*|OF RICE", "about")],
    [("BRING *MORE* RICE!", "bring")],
    [("SQUARE 64:", "square"), ("OVER *9 QUINTILLION*|GRAINS", "over"), ("MORE RICE THAN HUMANS|HAVE *EVER GROWN*", "more")],
    [("THE KING COULD|*NEVER PAY*", "the")],
    [("*CHECKMATE*,|YOUR MAJESTY.", "checkmate")],
    [("NEVER UNDERESTIMATE|*DOUBLING*", "never"), ("TAG YOUR|*SMARTEST* FRIEND", "tag")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.3, gaps=GAPS, max_pause=0.3)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E

B = {}
B["REWARD"] = A(1)
B["SAGE"] = A(2)
B["DOUBLE"] = W(2, "double")
B["GRANT"] = A(3)
B["S1"], B["S10"], B["S20"] = W(4, "square", 0), W(4, "square", 1), W(4, "square", 2)
B["S32"] = W(5, "square")
B["TONNES"] = W(5, "about")
B["MORE"] = A(6)
B["HIT"] = W(7, "square")
B["BREAK"] = B["HIT"] - 0.3
B["QUINT"] = W(7, "over")
B["EVER"] = W(7, "more")
B["NEVER"] = A(8)
B["CHECK"] = A(9)
B["CTA"] = A(10)
B["STOP"] = Bn(10) + 0.35
B["REWIND"] = B["STOP"] + 0.8
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)

SQK = [[0.0, 0], [B["S1"], 1], [B["S1"] + 0.5, 1], [B["S10"], 10], [B["S10"] + 0.5, 10], [B["S20"], 20],
       [E(4, "million") + 0.1, 20], [B["S32"], 32], [B["MORE"], 32], [B["BREAK"], 63], [B["HIT"], 64]]


def sq(t):
    for (a, ga), (b, gb) in zip(SQK, SQK[1:]):
        if t < b:
            return ga if gb - ga <= 1 else ga + (gb - ga) * (t - a) / (b - a)
    return 64


steps, last = [], 0
for k in range(int(B["HIT"] * 200) + 2):
    d = int(sq(k / 200) + 1e-6)
    if d != last:
        steps.append((k / 200, d))
        last = d
B["SQK"] = [[round(a, 3), g] for a, g in SQK]
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band)
tracks["king"] = reverb(tracks["king"] + 0.3 * band(tracks["king"], 60, 240), length=1.4, wet=0.18)[:N]   # a throne room
tracks["sage"] = reverb(tracks["sage"], length=1.4, wet=0.15)[:N]
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.45)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed
fx.x += CT.bed([
    S(0.0, B["S1"], 112, 112, "kbh"),
    S(B["S1"], B["S20"], 124, 134, "kbhs"),
    S(B["S20"], B["MORE"], 136, 150, "kbhsa"),
    S(B["MORE"], B["BREAK"], 150, 172, "kbhsa"),
    S(B["HIT"], B["NEVER"], 132, 132, "kbhsal"),
    S(B["NEVER"], B["CTA"], 100, 100, "kbo"),
    S(B["CTA"], B["STOP"] + 0.2, 140, 140, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- SIGNATURE: a tick + rice trickle per square, rising, thickening
def trickle(d, seed, dens):
    n = int(d * SR)
    r = np.random.default_rng(seed)
    out = np.zeros(n)
    for _ in range(int(dens * d)):
        i = r.integers(0, max(1, n - 200))
        m = int(0.004 * SR)
        tt = np.arange(m) / SR
        out[i:i + m] += np.sin(2 * np.pi * (3000 + 3000 * r.random()) * tt) * np.exp(-tt * 900) * (0.4 + 0.6 * r.random())
    return out * np.linspace(1, 0.3, n)


for t, d in steps:
    f = 220 * 2 ** ((d - 1) / 12 * 0.6)
    fx.put(osfx.sound("oga/100-sfx/wooden_02", F.tick(1400, 1.0)), t, 0.25)
    fx.put(CT.square(f * 2, 0.07, 0.25), t, 0.13, ((d % 3) - 1) * 0.4)
    fx.put(trickle(0.35, d, 40 + 14 * d), t + 0.02, 0.25, ((d % 5) - 2) * 0.2)
fx.put(CT.crackle(lambda t: 3 + 1.2 * sq(t) ** 1.25, B["S20"], B["BREAK"], seed=9, base=3600), B["S20"], 0.14)
fx.put(F.rumble(B["BREAK"] - B["S32"], seed=4) * np.linspace(0.2, 1, int((B["BREAK"] - B["S32"]) * SR)), B["S32"], 0.35)
fx.put(riser(B["BREAK"] - B["MORE"], 200, 2400), B["MORE"], 0.35)

# ---------------------------------------------------------------- 0. the court (story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/gong_01", gong(110, 3.0)), 0.05, 0.4)
fx.put(osfx.sfxr("powerUp", seed=21), B["REWARD"] - 0.1, 0.25)                                    # royal fanfare
fx.put(add(bell(784, 0.8), bell(1046.5, 0.8)), B["REWARD"] + 0.1, 0.2)
fx.put(osfx.sound("oga/100-sfx/wooden_01", F.tick(1200, 1.0)), B["SAGE"] - 0.1, 0.4)             # a pawn set down
fx.put(osfx.sound("oga/retro-synth/retro_coin_02", blip(1500, 0.12)), B["DOUBLE"], 0.35)
fx.put(osfx.sound("oga/creatures/grunt_04", sweep(0.4, 200, 140)), B["GRANT"] + 0.6, 0.3)         # the king laughs it off
fx.put(osfx.sound("oga/100-sfx/slam_04", impact(0.6)), E(3, "granted") - 0.05, 0.4)

# ---------------------------------------------------------------- cuts + reveals
for tc in (B["S1"], B["NEVER"], B["CHECK"], B["CTA"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.45)
    fx.put(impact(0.4), tc, 0.28)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.3, 500, 900)), B["S20"] + 0.6, 0.2)
fx.put(osfx.sound("oga/100-sfx/slam_01", thump(80, 0.4, 1.5)), B["TONNES"] + 0.1, 0.45)          # sacks pile up
fx.put(osfx.sound("oga/creatures/scream_01", sweep(0.3, 500, 800)), B["MORE"] + 0.05, 0.12)

# ---------------------------------------------------------------- BREAK -> square 64: avalanche
fx.put(sweep(0.3, 1400, 3000) * 0.3, B["BREAK"], 0.4)
fx.put(osfx.sound("oga/bangs-fireworks/cannon_02", impact(1.0)), B["HIT"], 0.7)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(braam(2.0, 49), B["HIT"], 0.45)
fx.put(sub_drop(1.2), B["HIT"], 0.6)
fx.put(trickle(3.0, 99, 4000), B["HIT"] + 0.05, 0.35)
fx.put(osfx.lib("sparkle"), B["EVER"], 0.3)

# ---------------------------------------------------------------- the king can't pay / checkmate / CTA
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(330, 4, 0.2)), B["NEVER"] + 0.3, 0.35)
fx.put(osfx.sound("oga/100-sfx/wooden_03", F.tick(900, 1.0)), W(9, "checkmate") + 0.05, 0.6)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(880, 1.5)), W(9, "checkmate") + 0.1, 0.4)
fx.put(osfx.sfxr("pickupCoin", seed=8), W(10, "tag"), 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 112, 112, "kbh")], gain=0.5, crescendo=(0.8, 0.8))

CT.card_blips(fx, [(c["a"], c["b"], "") for c in captions], gain=0.14)
for c in captions:
    fx.put(osfx.lib("whoosh-short"), c["a"] - 0.05, 0.12)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=1.0, makeup_db=5.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.85, makeup_db=2.0)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({k: (round(v, 3) if not isinstance(v, list) else v) for k, v in B.items()}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
print("BEATS", {k: v for k, v in B.items() if not isinstance(v, list)})
print("DUR", DUR)
