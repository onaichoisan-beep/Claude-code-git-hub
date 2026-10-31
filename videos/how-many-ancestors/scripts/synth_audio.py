"""Narration + sound for "How many people did it take to make you?" (house style + STYLE_GUIDE.md section 6).

- Narrated: a narrator, YOU (a kid) and a Bronze-Age ancestor, each with their own voice; captions follow the words.
- SIGNATURE sound = the doubling. Every generation that appears on the ANCESTORS counter plays one 8-bit pluck a
  semitone higher than the last; a click train underneath runs at a rate that follows the counter (log of the number
  of ancestors) until it blurs into a buzz at 8.6 BILLION. When the tree folds in, the same plucks run back down.
- A nonstop 8-bit bed whose tempo climbs with the counter (100 -> 168 BPM), cut for 0.3 s before the 8.6 billion
  slam, half-time for the "only 300 million" reveal, a warm pad + gong for the ancestor, then a tape-stop and a rewind
  into frame 1 (the loop).
- A blip on every caption card, a tick on every counter change, a whoosh + hit on every cut.

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
GAPS = {1: 0.35, 2: 0.2, 3: 0.25, 4: 0.15, 5: 0.25, 6: 0.55, 7: 0.25, 8: 0.25, 9: 0.45, 10: 0.45, 11: 0.4}
TAIL = 1.6   # after the last line: tape-stop + rewind into frame 1

CAPS = [
    [("HOW MANY PEOPLE DID IT|TAKE TO *MAKE YOU*?", "how")],
    [("*2* PARENTS", "two"), ("*4* GRANDPARENTS", "four"), ("*8* GREAT-|GRANDPARENTS", "eight")],
    [("OKAY, *EASY*.", "okay")],
    [("EVERY GENERATION,|IT *DOUBLES*", "every"), ("*64*", "sixty"), ("*1,000*", "a"), ("*1 MILLION*", "a")],
    [("WAIT, IT KEEPS|*GOING*?", "wait")],
    [("33 GENERATIONS BACK,|AROUND *1036*", "thirty"), ("OVER *8.5 BILLION*|ANCESTORS", "you'd")],
    [("MORE THAN ARE|*ALIVE TODAY*", "that's"), ("BUT IN 1036: ONLY|*~300 MILLION* PEOPLE", "but")],
    [("SO WHERE DID|EVERYONE *GO*?", "so")],
    [("THEY'RE THE|*SAME PEOPLE*!", "they're"), ("YOUR TREE|*FOLDS IN*", "distant"),
     ("1 ANCESTOR, *1000S*|OF SPOTS", "and")],
    [("A FEW *THOUSAND* YEARS|BACK...", "go"), ("WE ALL SHARE THE|*SAME ANCESTORS*", "everyone")],
    [("HELLO, *GRANDCHILDREN*.", "hello"), ("ALL *8 BILLION* OF YOU.", "all")],
    [("SEND THIS TO YOUR|*LONG-LOST COUSIN*", "send")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.35, gaps=GAPS, max_pause=0.3)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E

# ---------------------------------------------------------------- beats the picture shares
B = {}
B["G1"], B["G2"], B["G3"] = W(1, "two"), W(1, "four"), W(1, "eight")
B["EASY"] = A(2)
B["DOUBLE"] = A(3)
B["G6"], B["G10"], B["G20"] = W(3, "sixty"), W(3, "thousand"), W(3, "million")
B["WAIT"] = A(4)
B["Y1036"] = W(5, "around")
B["PEAK"] = W(5, "eight")
B["BREAK"] = B["PEAK"] - 0.3
B["MORE"] = A(6)
B["FEW"] = W(6, "but")
B["WHERE"] = A(7)
B["FOLD"] = A(8)
B["ONE"] = W(8, "one")
B["ALL"] = A(9)
B["SHARE"] = W(9, "everyone")
B["ANC"] = A(10)
B["EIGHTB"] = W(10, "all")
B["CTA"] = A(11)
B["STOP"] = Bn(11) + 0.35
B["REWIND"] = B["STOP"] + 0.8
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)

# the generation counter: [time, generation]; the picture reads this too (ANCESTORS = 2^floor(gen))
GENK = [[0.0, 0], [B["G1"], 1], [B["G2"], 2], [B["G3"], 3], [B["DOUBLE"] + 0.3, 3], [B["G6"], 6], [E(3, "sixty") + 0.05, 6],
        [W(3, "thousand"), 10], [E(3, "thousand") + 0.05, 10], [W(3, "million"), 20], [E(3, "million") + 0.1, 20],
        [B["Y1036"], 30], [B["PEAK"], 33]]


def gen(t):
    if t < GENK[0][0]:
        return 0.0
    for (a, ga), (b, gb) in zip(GENK, GENK[1:]):
        if t < b:
            if gb - ga <= 1:                 # the first three: a jump on the word
                return ga
            return ga + (gb - ga) * (t - a) / (b - a)
    return 33.0


def gen_steps():
    """(time, generation) for every new row on the counter"""
    out, last = [], 0
    for k in range(int(B["PEAK"] * 200) + 2):
        t = k / 200
        gn = int(np.floor(gen(t) + 1e-6))
        if gn != last:
            out.append((t, gn))
            last = gn
    return out


B["GENK"] = [[round(a, 3), g] for a, g in GENK]
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band, gains={"ancestor": 1.0})
# the ancestor speaks from deep time: a low boost + hall reverb
anc = tracks["ancestor"]
tracks["ancestor"] = reverb(anc + 0.4 * band(anc, 60, 260), length=2.2, wet=0.35)[:N]
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.5)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed: tempo follows the counter
fx.x += CT.bed([
    S(0.0, B["G1"], 100, 100, "kb"),
    S(B["G1"], B["DOUBLE"], 104, 110, "kbh"),
    S(B["DOUBLE"], B["WAIT"], 112, 140, "kbha"),
    S(B["WAIT"], B["BREAK"], 140, 168, "kbhsa"),
    #                                                     BREAK -> PEAK: 0.3 s of silence, then the slam
    S(B["PEAK"], B["FEW"], 128, 128, "kbhsal"),
    S(B["FEW"], B["FOLD"], 64, 64, "kbo"),               # "only 300 million": half-time, octave down
    S(B["FOLD"], B["ANC"], 118, 128, "kbhsa"),
    S(B["ANC"], B["CTA"], 96, 96, "kb"),                 # the ancestor speaks: soft
    S(B["CTA"], B["STOP"] + 0.2, 140, 144, "kbhsal"),
], gain=0.5, crescendo=(0.75, 1.15))

# ---------------------------------------------------------------- SIGNATURE: one pluck per generation, rising
steps = gen_steps()
for t, gn in steps:
    f = 330 * 2 ** ((gn - 1) / 12)
    fx.put(add(CT.square(f, 0.09, 0.25), 0.5 * CT.square(f * 2, 0.05, 0.125)), t, 0.22, ((gn % 3) - 1) * 0.4)
    fx.put(F.tick(2600 + 60 * gn, 1.0), t, 0.3)
for t, gn in steps[:3]:                                   # parents / grandparents / great-grandparents pop in
    fx.put(osfx.lib("pop"), t, 0.45)
    fx.put(osfx.sound("oga/retro-synth/retro_coin_0" + str(gn % 2 + 1), blip(880 * gn)), t + 0.02, 0.25)
# a click train whose rate follows log2(ancestors): it blurs into a buzz at 8.6 billion
fx.put(CT.crackle(lambda t: 1.5 * gen(t) ** 1.25, B["DOUBLE"], B["BREAK"], seed=5,
                  pitch_fn=lambda t: 0.8 + gen(t) / 40), B["DOUBLE"], 0.18)
fx.put(riser(B["BREAK"] - B["WAIT"], 200, 2200), B["WAIT"], 0.3)

# ---------------------------------------------------------------- 0. YOU, alone (no cold-open hook: the story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(880, 1.5)), 0.15, 0.25)
fx.put(osfx.sfxr("jump", seed=7), B["EASY"] + 0.1, 0.25)                      # YOU shrugs
fx.put(osfx.lib("whoosh"), B["DOUBLE"] - 0.15, 0.4)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.3, 500, 900)), B["WAIT"] + 0.05, 0.2)

# ---------------------------------------------------------------- 1. BREAK -> 8.6 BILLION slam
fx.put(sweep(B["PEAK"] - B["BREAK"], 1400, 3000) * 0.25, B["BREAK"], 0.4)
fx.put(osfx.sound("oga/bangs-fireworks/bang_03", impact(1.0)), B["PEAK"], 0.7)
fx.put(impact(1.0), B["PEAK"], 0.8)
fx.put(sub_drop(1.2), B["PEAK"], 0.7)
fx.put(osfx.sfxr("powerUp", seed=33), B["PEAK"] + 0.1, 0.3)
for k in range(6):                                                              # the counter digits flicker
    fx.put(F.tick(3600, 1.0), B["PEAK"] + 0.08 * k, 0.25)

# ---------------------------------------------------------------- 2. more than alive today / only 300 million
fx.put(osfx.lib("whoosh"), B["MORE"] - 0.15, 0.45)
fx.put(osfx.sound("oga/100-sfx/slam_01", thump(80, 0.3, 1.5)), B["MORE"], 0.35)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(392, 4, 0.2)), B["FEW"] + 0.4, 0.35)
fx.put(CT.womp(392, 4, 0.22), W(6, "three") + 0.2, 0.18)
fx.put(osfx.sound("oga/creatures/misc_02", sweep(0.3, 700, 400)), B["WHERE"] + 0.05, 0.2)
fx.put(osfx.sfxr("blipSelect", seed=9), W(7, "go") + 0.1, 0.3)

# ---------------------------------------------------------------- 3. the tree folds in: the plucks run back DOWN
fx.put(osfx.lib("whoosh-cinematic"), B["FOLD"] - 0.2, 0.55)
fx.put(impact(0.6), B["FOLD"], 0.4)
for k in range(16):
    t = B["FOLD"] + 0.6 + k * 0.17
    f = 330 * 2 ** ((32 - 2 * k) / 12)
    fx.put(CT.square(f, 0.08, 0.25), t, 0.16, ((k % 3) - 1) * 0.4)
    fx.put(F.tick(4200 - 120 * k, 0.8), t, 0.18)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(1046.5, 2.0)), B["ONE"], 0.4)
fx.put(F.sparkle(1.2, seed=12), B["ONE"] + 0.05, 0.3)

# ---------------------------------------------------------------- 4. zoom out to everyone alive: one ancestor on top
fx.put(osfx.lib("whoosh"), B["ALL"] - 0.15, 0.45)
fx.put(riser(B["ANC"] - B["ALL"], 180, 900), B["ALL"], 0.2)
fx.put(F.harp_up(), B["SHARE"], 0.35)
fx.put(osfx.lib("chime"), B["SHARE"] + 0.6, 0.3)

# ---------------------------------------------------------------- 5. the ancestor speaks: gong + warm pad
fx.put(osfx.sound("oga/100-sfx/gong_01", gong(110, 4.0)), B["ANC"] - 0.3, 0.55)
fx.put(gong(98, 4.0), B["ANC"] - 0.3, 0.25)
amb.put(F.pad(B["CTA"] - B["ANC"] + 0.6, [110, 164.8, 220, 277.2], a=0.8, r_=1.0), B["ANC"] - 0.2, 0.3)
fx.put(osfx.sound("oga/bangs-fireworks/fw_01", F.firework(3)), B["EIGHTB"] + 0.4, 0.3)
fx.put(F.sparkle(1.5, seed=21), B["EIGHTB"] + 0.2, 0.3)

# ---------------------------------------------------------------- 6. CTA: YOU meets a cousin
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.35)
fx.put(osfx.sound("oga/creatures/cute_03", blip(1200, 0.2)), B["CTA"] + 0.7, 0.3)
for k in range(4):
    fx.put(osfx.sound(f"oga/bangs-fireworks/fw_0{k % 5 + 2}", F.firework(40 + k)), B["CTA"] + 0.5 + 0.35 * k, 0.22, (k % 3 - 1) * 0.6)

# ---------------------------------------------------------------- 7. tape-stop -> rewind -> frame 1 (the loop)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 100, 100, "kb")], gain=0.5, crescendo=(0.75, 0.75))   # = how the video starts

# ---------------------------------------------------------------- a sound on every card + whoosh on every cut
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
print("BEATS", {k: v for k, v in B.items() if k != "GENK"})
print("DUR", DUR)
