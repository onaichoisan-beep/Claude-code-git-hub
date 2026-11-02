"""Narration + sound for "How many descendants will YOU have?" (Part 3 of the how-many-ancestors hit, 300k views).

- Voices: Kokoro-82M (make_voices_kokoro.py): narrator af_heart, YOU af_sky.
- Same sound as the hit: the nonstop 8-bit bed, one pluck per generation a semitone higher each time + a click train that
  follows the DESCENDANTS counter into a buzz, 0.3 s break, slam on 8.6 billion. Twist: the music cuts ("here's the crazy
  part"), the plucks fall to nothing for "dies out", a golden harp + chime flood for "everyone alive", a gong for "nothing in
  between", the beat returns for the CTA, tape-stop + rewind into frame 1.

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
GAPS = {1: 0.4, 2: 0.25, 3: 0.2, 4: 0.25, 5: 0.25, 6: 0.3, 7: 0.45, 8: 0.25, 9: 0.35, 10: 0.3, 11: 0.35, 12: 0.4}

CAPS = [
    [("YOU NEEDED *8.5 BILLION*|ANCESTORS TO EXIST.", "you"), ("BUT HOW MANY PEOPLE|WILL NEED *YOU*?", "but")],
    [("SAY YOU HAVE|*2 KIDS*", "say")],
    [("THEY EACH HAVE *2*.", "they"), ("THEN THEIR KIDS|HAVE *2*.", "then")],
    [("EVERY GENERATION,|IT *DOUBLES*", "every")],
    [("IN 300 YEARS:|*1,000* DESCENDANTS", "in"), ("IN 600 YEARS:|*A MILLION*", "in")],
    [("IN 1,000 YEARS:|*8 BILLION+*", "in")],
    [("WAIT... THAT'S|*EVERYONE*?", "wait")],
    [("HERE'S THE|*CRAZY* PART", "here's")],
    [("SCIENTISTS *MODELLED* THIS.", "scientists"), ("GO FAR ENOUGH INTO|THE FUTURE...", "go"), ("THERE'S *NO MIDDLE*|GROUND", "and")],
    [("EITHER YOUR LINE|*DIES OUT*...", "either")],
    [("OR IN A FEW THOUSAND|YEARS...", "or"), ("YOU'RE THE ANCESTOR OF|*EVERY PERSON ALIVE*", "you're")],
    [("*NOTHING*|IN BETWEEN.", "nothing")],
    [("WHICH ONE WILL|YOU BE?", "so"), ("COMMENT *0* OR *ALL*", "comment")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.3, gaps=GAPS, max_pause=0.45)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E

B = {}
B["NEED"] = W(0, "but")
B["G1"] = W(1, "two")
B["G2"] = W(2, "two")
B["G3"] = W(2, "kids")
B["DOUBLE"] = A(3)
B["G10"] = W(4, "thousand")
B["G20"] = W(4, "million")
B["PEAK"] = W(5, "eight")
B["BREAK"] = B["PEAK"] - 0.3
B["WAIT"] = A(6)
B["CRAZY"] = A(7)
B["MODEL"] = A(8)
B["DIE"] = A(9)
B["ALL"] = A(10)
B["EVERY"] = W(10, "every")
B["NOTHING"] = A(11)
B["CTA"] = A(12)
B["COMMENT"] = W(12, "comment")
B["STOP"] = Bn(12) + 0.45
B["REWIND"] = B["STOP"] + 0.8
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)

GENK = [[0.0, 0], [B["G1"], 1], [B["G2"], 2], [B["G3"], 3], [B["DOUBLE"] + 0.3, 3], [A(4), 6], [B["G10"], 10],
        [E(4, "descendants") + 0.05, 10], [B["G20"], 20], [E(4, "million") + 0.1, 20], [A(5), 24], [B["PEAK"], 33]]
B["GENK"] = [[round(a, 3), g] for a, g in GENK]


def gen(t):
    for (a, ga), (b, gb) in zip(GENK, GENK[1:]):
        if t < b:
            return ga if gb - ga <= 1 else ga + (gb - ga) * (t - a) / (b - a)
    return 33.0


steps, last = [], 0
for k in range(int(B["PEAK"] * 200) + 2):
    d = int(np.floor(gen(k / 200) + 1e-6))
    if d != last:
        steps.append((k / 200, d))
        last = d
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band, level_db=-14.0)
tracks["narrator"] = reverb(tracks["narrator"], length=0.6, wet=0.08)[:N]
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.45)
captions = V.make_captions(clips, CAPS, DUR, hold=0.3)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the 8-bit bed (the hit's sound), cut for the twist
fx.x += CT.bed([
    S(0.0, B["G1"], 100, 100, "kb"),
    S(B["G1"], B["DOUBLE"], 104, 110, "kbh"),
    S(B["DOUBLE"], B["WAIT"] - 1.6, 112, 150, "kbha"),
    S(B["WAIT"] - 1.6, B["BREAK"], 150, 168, "kbhsa"),
    S(B["PEAK"], B["CRAZY"], 128, 128, "kbhsal"),
    #                                       CRAZY -> MODEL: dead quiet (a low drone only)
    S(B["MODEL"] + 0.2, B["DIE"], 64, 64, "ko"),
    S(B["ALL"], B["NOTHING"], 120, 128, "kbhsa"),
    S(B["CTA"], B["STOP"] + 0.2, 140, 140, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))
amb.put(F.drone(B["ALL"] - B["CRAZY"], 49, seed=3), B["CRAZY"], 0.3)

# ---------------------------------------------------------------- SIGNATURE: a pluck per generation, rising; clicks blur into a buzz
for t, gn in steps:
    f = 330 * 2 ** ((gn - 1) / 12)
    fx.put(add(CT.square(f, 0.09, 0.25), 0.5 * CT.square(f * 2, 0.05, 0.125)), t, 0.22, ((gn % 3) - 1) * 0.4)
    fx.put(F.tick(2600 + 60 * gn, 1.0), t, 0.3)
for t, gn in steps[:3]:
    fx.put(osfx.lib("pop"), t, 0.45)
    fx.put(osfx.sound("oga/creatures/cute_0" + str(gn + 1), blip(880 * gn)), t + 0.05, 0.25)        # the babies
fx.put(CT.crackle(lambda t: 1.5 * gen(t) ** 1.25, B["DOUBLE"], B["BREAK"], seed=5, pitch_fn=lambda t: 0.8 + gen(t) / 40), B["DOUBLE"], 0.18)
fx.put(riser(B["BREAK"] - (B["G20"] - 0.5), 200, 2200), B["G20"] - 0.5, 0.3)

# ---------------------------------------------------------------- the hook + the slam
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(880, 1.5)), 0.15, 0.25)
fx.put(osfx.lib("whoosh"), B["NEED"] - 0.15, 0.4)
fx.put(impact(0.5), B["NEED"], 0.3)
fx.put(sweep(0.3, 1400, 3000) * 0.25, B["BREAK"], 0.4)
fx.put(osfx.sound("oga/bangs-fireworks/bang_03", impact(1.0)), B["PEAK"], 0.7)
fx.put(impact(1.0), B["PEAK"], 0.8)
fx.put(sub_drop(1.2), B["PEAK"], 0.7)
for k in range(6):
    fx.put(F.tick(3600, 1.0), B["PEAK"] + 0.08 * k, 0.25)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.3, 500, 900)), B["WAIT"] + 0.05, 0.22)

# ---------------------------------------------------------------- the twist
fx.put(osfx.lib("whoosh-cinematic"), B["CRAZY"] - 0.2, 0.5)
fx.put(braam(2.4, 46), B["CRAZY"], 0.45)
fx.put(heartbeat(), B["MODEL"] + 0.4, 0.35)
fx.put(heartbeat(), B["MODEL"] + 1.4, 0.35)
fx.put(osfx.lib("whoosh"), W(8, "there's") - 0.1, 0.4)
fx.put(impact(0.6), W(8, "there's"), 0.4)                                                          # the split
# "dies out": the plucks fall away to nothing
for k in range(12):
    fx.put(CT.square(330 * 2 ** ((32 - 3 * k) / 12), 0.08, 0.25), B["DIE"] + 0.2 + k * 0.15, 0.16 * (1 - k / 14), ((k % 3) - 1) * 0.4)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(392, 4, 0.2)), E(9, "completely") - 0.2, 0.4)
fx.put(sweep(1.2, 600, 120) * 0.3, B["DIE"] + 0.3, 0.3)
# "everyone alive": a golden flood
fx.put(F.harp_up(), B["EVERY"] - 0.3, 0.45)
fx.put(osfx.lib("chime"), B["EVERY"] + 0.2, 0.4)
fx.put(F.sparkle(1.6, seed=9), B["EVERY"], 0.35)
for k in range(6):
    fx.put(osfx.sound(f"oga/bangs-fireworks/fw_0{k % 5 + 1}", F.firework(20 + k)), B["EVERY"] + 0.4 + k * 0.3, 0.2, (k % 3 - 1) * 0.6)
# "nothing in between": a gong
fx.put(osfx.sound("oga/100-sfx/gong_01", gong(110, 3.0)), B["NOTHING"] - 0.05, 0.5)
fx.put(impact(0.7), B["NOTHING"], 0.5)
# CTA: two buttons
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sfxr("blipSelect", seed=4), B["COMMENT"], 0.35)
fx.put(osfx.sfxr("blipSelect", seed=6), B["COMMENT"] + 0.45, 0.35)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kb")], gain=0.5, crescendo=(0.8, 0.8))

CT.card_blips(fx, [(c["a"], c["b"], "") for c in captions], gain=0.12)

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
