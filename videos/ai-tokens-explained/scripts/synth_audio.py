"""Two-voice dialogue + cinematic SFX for "What is a token?".

  python3 scripts/synth_audio.py [voice_dir]

voice_dir (default assets/audio/vo) holds NN.wav + NN.json (word timings) per line of lines.json,
made by make_voices.py. Long pauses inside a line are trimmed, the robot's jargon line is cut off
mid-word (the kid interrupts), and the lines are laid end to end with the gaps in GAP. SFX duck under
the voices and the result is written to assets/audio/mix.wav.

Also writes captions.js for the picture:
  CAPS   small centred captions, timed to the words
  VO     every line's speaker, start, end and word timings (seconds), so scenes key off the words
  MOUTH  per-frame (30 fps) mouth opening 0-9 for each speaker, for lip flaps
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
VO_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets", "audio", "vo")
LINES = json.load(open(os.path.join(HERE, "lines.json")))
FPS = 30
MAX_PAUSE = 0.42      # longest silence kept inside a line
GAP = 0.30            # default silence between lines
GAPS = {1: 0.62, 3: 0.04, 4: 0.50, 6: 0.34, 7: 0.34, 9: 0.34, 11: 0.30, 16: 0.30, 18: 0.85}
CUT = {2: "inside"}   # line -> word where the kid cuts the robot off
TAIL = 1.45           # after the last line: the reveal settles, then the loop flash

# caption chunks per line: (display text, first spoken word(s) of the chunk); *word* = gold
CAPS = [
    [("I DON'T READ YOUR *WORDS*.", "i"), ("I READ... *THESE*.", "i read")],
    [("HEY *A.I.*!", "hey"), ("WHAT'S A *TOKEN*?", "what's"), ("EXPLAIN IT LIKE I'M *FIVE*.", "explain")],
    [("EASY! A TOKEN IS A", "easy"), ("*SUB-WORD UNIT*", "sub-word"), ("FROM *BYTE-PAIR ENCODING*,", "from"),
     ("MAPPED TO AN *INTEGER ID*", "mapped"), ("INSIDE A-", "inside")],
    [("I'M *FIVE*.", "i'm")],
    [("RIGHT. OKAY.", "right"), ("THINK OF *BUILDING BLOCKS*.", "think")],
    [("WHEN YOU TYPE,", "when"), ("I SNAP YOUR SENTENCE", "i"), ("INTO LITTLE *BLOCKS*.", "into"),
     ("EACH BLOCK IS A *TOKEN*.", "each")],
    [("SMALL WORDS, LIKE *CAT*,", "small"), ("ARE *ONE BLOCK*.", "are"), ("BIGGER WORDS *SPLIT UP*.", "bigger"),
     ("*JELLY*...", "jelly"), ("*JELLY* + *FISH*", "plus")],
    [("OOH!", "ooh"), ("DO *TYRANNOSAURUS*!", "do")],
    [("*4 BLOCKS*.", "four"), ("*TYR*", "tyre"), ("TYR *ANN*", "ann"), ("TYR ANN *OS*", "oss"), ("TYR ANN OS *AURUS*", "aurus")],
    [("ON AVERAGE,", "on"), ("*1 TOKEN* IS ABOUT", "one"), ("*3/4* OF A WORD.", "three")],
    [("WHY DOES THAT *MATTER*?", "why")],
    [("BECAUSE A.I. IS PRICED", "because"), ("*BY THE TOKEN*.", "by"), ("EVERY BLOCK COSTS", "every"), ("A *TINY BIT*.", "a tiny")],
    [("AND MY *MEMORY*", "and"), ("ONLY FITS SO MANY", "only"), ("BLOCKS AT ONCE.", "blocks"), ("IT'S CALLED THE", "it's"),
     ("*CONTEXT WINDOW*.", "context")],
    [("WHAT HAPPENS", "what"), ("WHEN IT'S *FULL*?", "when")],
    [("OLDER BLOCKS", "older"), ("GET *PUSHED OUT*...", "get"), ("AND I CAN START", "and"), ("TO *FORGET*.", "to")],
    [("WAIT.", "wait"), ("SO YOU DON'T SEE *LETTERS*?", "so")],
    [("NOPE.", "nope"), ("TO ME, *STRAWBERRY*", "to"), ("IS *ONE BLOCK*.", "is"), ("THAT'S A BIG REASON", "that's"),
     ("A.I. USED TO *MISCOUNT*", "a.i."), ("ITS *R'S*.", "its")],
    [("SO HOW MANY *R'S*", "so"), ("ARE IN *STRAWBERRY*?", "are")],
    [("*THREE*.", "three"), ("I CHECKED.", "i")],
]


def key(w):
    return "".join(c for c in w.lower() if c.isalnum() or c == "'")


def find(words, anchor, frm=0):
    seq = [key(a) for a in anchor.split()]
    for i in range(frm, len(words)):
        if all(i + k < len(words) and key(words[i + k][0]).startswith(s) for k, s in enumerate(seq)):
            return i
    return None


def segs(text):
    return [[p, "g" if k % 2 else "p"] for k, p in enumerate(text.split("*")) if p]


def read24(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float) / 32768
    return x, sr


def squeeze(x, sr, words):
    """Shorten silences longer than MAX_PAUSE inside the line; shift the word timings to match."""
    hop = int(0.01 * sr)
    fr = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same")[::hop] + 1e-12)
    quiet = fr < np.max(fr) * 10 ** (-38 / 20)
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if i > 0 and j < len(quiet) and (j - i) * 0.01 > MAX_PAUSE:
                runs.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    out, pos, shift, cuts = [], 0, 0.0, []
    for a, b in runs:
        ca, cb = a + MAX_PAUSE / 2, b - MAX_PAUSE / 2
        out.append(x[int(pos * sr): int(ca * sr)])
        cuts.append((ca, cb - ca))
        pos = cb
    out.append(x[int(pos * sr):])
    y = np.concatenate(out)

    def mapt(tt):
        s = 0.0
        for c, r in cuts:
            if tt > c:
                s += min(r, tt - c)
        return tt - s
    return y, [[w, round(mapt(a), 3), round(mapt(b), 3)] for w, a, b in words]


# ------------------------------------------------------------------ lay out the voice
clips, t0 = [], 0.20
for i, (who, text) in enumerate(LINES):
    x, sr = read24(os.path.join(VO_DIR, f"{i:02d}.wav"))
    words = json.load(open(os.path.join(VO_DIR, f"{i:02d}.json")))
    x, words = squeeze(x, sr, words)
    if i in CUT:  # cut off mid-word, with a quick fade
        j = find(words, CUT[i])
        c = words[j][1] + 0.55 * (words[j][2] - words[j][1])
        x = x[: int(c * sr)]
        f = int(0.025 * sr)
        x[-f:] *= np.linspace(1, 0, f)
        words = words[: j + 1]
        words[-1][2] = round(c, 3)
    if i > 0:
        t0 = clips[-1]["b"] + GAPS.get(i, GAP)
    L = len(x) / sr
    clips.append({"who": who, "a": round(t0, 3), "b": round(t0 + L, 3), "x": x, "sr": sr,
                  "w": [[w, round(t0 + a, 3), round(t0 + b, 3)] for w, a, b in words]})

DUR = round(np.ceil((clips[-1]["b"] + TAIL) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")
os.environ["SFX_DUR"] = str(DUR)
sys.path.insert(0, HERE)
from sfxlib import *  # noqa: E402,F403


def W(i, word, n=0):
    """absolute time of the n-th occurrence of a spoken word in line i"""
    j = -1
    for _ in range(n + 1):
        j = find(clips[i]["w"], word, j + 1)
    return clips[i]["w"][j][1]


def A(i):
    return clips[i]["a"]


def B(i):
    return clips[i]["b"]


tracks = {"ai": np.zeros(N), "kid": np.zeros(N)}
for c in clips:
    x = c["x"]
    x = np.interp(np.arange(int(len(x) * SR / c["sr"])) * c["sr"] / SR, np.arange(len(x)), x)
    x = band(x, 80, 14000)
    act = np.abs(x) > 2e-3
    x = x / (np.sqrt(np.mean(x[act] ** 2)) + 1e-9) * 10 ** (-13.5 / 20)  # every line at the same level
    i0 = int(c["a"] * SR)
    tracks[c["who"]][i0: i0 + len(x)] += x[: N - i0]
for k in tracks:
    tracks[k] = np.tanh(tracks[k] * 1.5) / 1.5
voice = tracks["ai"] + tracks["kid"]
active = np.abs(voice) > 1e-4

# mouth openings for the lip flaps
mouth = {}
for k, v in tracks.items():
    hop = SR // FPS
    fr = np.sqrt(np.convolve(v ** 2, np.ones(hop) / hop, mode="same")[::hop] + 1e-12)
    ref = np.percentile(fr[fr > 0.01], 80)
    m = np.clip(fr / ref, 0, 1) ** 0.8
    mouth[k] = "".join(str(int(round(z * 9))) for z in m)

# captions
captions = []
for i, c in enumerate(clips):
    idx, times = 0, []
    for text, anchor in CAPS[i]:
        j = find(c["w"], anchor, idx)
        if j is None:
            raise SystemExit(f"line {i}: anchor '{anchor}' not found in {[w[0] for w in c['w']]}")
        times.append(c["w"][j][1])
        idx = j + 1
    nxt = clips[i + 1]["a"] if i + 1 < len(clips) else DUR
    for k, (text, _) in enumerate(CAPS[i]):
        a = max(c["a"], times[k] - 0.05)
        b = times[k + 1] - 0.05 if k + 1 < len(times) else min(c["b"] + 0.4, nxt - 0.03)
        captions.append({"a": round(a, 3), "b": round(b, 3), "segs": segs(text)})

# ducking envelope: SFX drop ~9 dB under speech
e = np.convolve(np.abs(voice), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
e = np.clip(e / (np.percentile(e[active], 60) + 1e-9), 0, 1)
k = int(0.25 * SR)
e = np.convolve(e, np.ones(k) / k, mode="same")
duck = 1 - 0.65 * np.clip(e * 1.4, 0, 1)

# ------------------------------------------------------------------ sfx
amb, fx = Bus(), Bus()


def clack(f=1.0):
    """A toy block landing: woody knock + tiny click."""
    return add(0.8 * thump(180 * f, 0.12, 1.2), 0.5 * noise_hit(0.03, 1500, 6000))


def snap():
    return add(0.7 * noise_hit(0.04, 2500, 11000), 0.5 * thump(320, 0.06, 1.5))


def key_click():
    return 0.6 * noise_hit(0.025, 1800, 7000)


def coin(f=1.0):
    return add(bell(2093 * f, 0.5), 0.7 * bell(2637 * f, 0.4))


def buzzer(d=0.35):
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * 110 * tt)) + 0.5 * np.sign(np.sin(2 * np.pi * 117 * tt))
    return band(s, 80, 2500) * env(n, 0.005, 0.08)


def scratch(d=0.32):
    """Record scratch: band-passed noise sweeping up then down fast."""
    return add(sweep(d * 0.45, 600, 4500), np.concatenate([np.zeros(int(d * 0.4 * SR)), sweep(d * 0.6, 4000, 500)]))


def stomp():
    return add(taiko(48), 0.8 * thump(34, 0.7, 2.5))


def wobble(d=0.8, f0=900, f1=240):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f0 * (f1 / f0) ** (tt / d) * (1 + 0.08 * np.sin(2 * np.pi * 9 * tt))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env(n, 0.01, d * 0.4)


# room tone the whole way: soft, warm, low
for ch in range(2):
    amb.x[:, ch] += 0.35 * norm(band(rng.standard_normal(N), 60, 400)) + 0.06 * norm(band(rng.standard_normal(N), 2000, 6000))
# a soft digital pad under the "inside the AI" block scenes
pad = sum(np.sin(2 * np.pi * f * t + p) for f, p in [(110, 0), (164.8, 1), (220.5, 2), (329.6, 3)]) / 4
pad *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.25 * t)
amb.x += (0.10 * pad * (seg(A(4) + 1.0, A(7), 0.8) + seg(W(7, "tyrannosaurus"), A(10), 0.6) + seg(A(11), A(13), 0.6)
                         + seg(A(14), A(15), 0.5) + seg(A(16), A(17), 0.5)))[:, None]

# COLD OPEN: the sentence slams down and shatters into blocks
fx.put(impact(1.1), 0.0, 1.0)
fx.put(braam(2.0, 52), 0.0, 0.5)
fx.put(sub_drop(1.0), 0.02, 0.5)
for k in range(5):
    fx.put(snap(), 0.12 + 0.09 * k, 0.5, (k - 2) / 3)
fx.put(add(impact(0.6), 0.6 * shing(0.5)), W(0, "these") - 0.02, 0.55)
fx.put(rewind(0.45), A(1) - 0.55, 0.55)

# the room: laptop chime as the robot pops out, "?" boing
for k, f in enumerate([1319, 1760, 2349]):
    fx.put(bell(f, 0.9), W(1, "a.i.") + 0.08 * k, 0.16)
fx.put(bubble(1.6), W(1, "a.i.") + 0.05, 0.5)
fx.put(blip(660, 0.08), W(1, "token") + 0.1, 0.3)
fx.put(blip(990, 0.08), W(1, "token") + 0.2, 0.3)

# jargon floods in: whooshes and blips, a dizzy riser
for k, wd in enumerate(["sub-word", "byte-pair", "encoding", "mapped", "integer", "i.d."]):
    fx.put(sweep(0.35, 400, 3000), W(2, wd) - 0.05, 0.28, (k % 3 - 1) * 0.6)
    fx.put(blip(500 + 120 * k, 0.06), W(2, wd), 0.18)
fx.put(riser(B(2) - W(2, "byte-pair"), 200, 1400), W(2, "byte-pair"), 0.16)
# "I'm five." record scratch, then a flat comedic thud
fx.put(scratch(), B(2) - 0.08, 0.6)
fx.put(thump(90, 0.3, 1.0), W(3, "five"), 0.5)

# building blocks rain down and stack
for k in range(6):
    fx.put(clack(1 + 0.08 * k), W(4, "blocks") + 0.12 + 0.13 * k, 0.55, (k % 3 - 1) * 0.5)
fx.put(sweep(0.6, 300, 2500), W(4, "think") - 0.3, 0.3)

# typing, the zap, six snaps, counter
for k in range(12):
    fx.put(key_click(), A(5) + 0.05 + 0.07 * k, 0.45, (k % 2) * 0.4 - 0.2)
fx.put(sweep(0.45, 1500, 7000), W(5, "snap") - 0.1, 0.4)
for k in range(6):
    fx.put(snap(), W(5, "snap") + 0.1 + 0.1 * k, 0.55, (k - 2.5) / 3)
fx.put(add(blip(880, 0.1), 0.6 * blip(1320, 0.12)), W(5, "token") - 0.1, 0.35)

# cat block, jellyfish splits
fx.put(clack(1.2), W(6, "cat"), 0.6)
fx.put(bubble(1.2), W(6, "cat") + 0.05, 0.4)
fx.put(clack(0.9), W(6, "bigger"), 0.5)
fx.put(add(snap(), 0.5 * shing(0.3)), W(6, "plus") - 0.05, 0.6)
for k in range(4):
    fx.put(bubble(0.6 + 0.2 * k), W(6, "fish") + 0.08 * k, 0.3, (k - 1.5) / 2)

# "Ooh!" sparkle, then the T-rex stomps in and roars
for k, f in enumerate([1568, 2093, 2637]):
    fx.put(bell(f, 0.8), A(7) + 0.05 * k, 0.14)
tr = W(7, "tyrannosaurus")
for k in range(3):
    fx.put(stomp(), tr + 0.05 + 0.42 * k, 0.75)
fx.put(roar(1.4, 85), tr + 1.15, 0.7)
# four blocks snap off one by one
for k, wd in enumerate(["tyre", "ann", "oss", "aurus"]):
    fx.put(add(snap(), 0.6 * clack(1 + 0.1 * k)), W(8, wd) - 0.02, 0.55, (k - 1.5) / 2)

# 3/4 of a word: slide + ding
fx.put(sweep(0.6, 300, 2200), W(9, "one") - 0.1, 0.35)
fx.put(add(bell(1760, 1.0), 0.5 * bell(2637, 0.8)), W(9, "three"), 0.22)

# "why does that matter?" - a curious blip
fx.put(blip(700, 0.08), W(10, "matter"), 0.25)

# priced by the token: conveyor hum, coins
amb.x += (0.25 * norm(band(rng.standard_normal(N), 90, 300)) * seg(A(11), B(11) + 0.2, 0.3))[:, None]
for k in range(9):
    fx.put(coin(1 + 0.03 * (k % 3)), W(11, "by") + 0.1 + 0.32 * k, 0.22, (k % 3 - 1) * 0.5)
fx.put(add(bell(1319, 1.2), bell(1760, 1.2), 0.6 * noise_hit(0.15, 3000, 9000)), W(11, "tiny"), 0.25)

# the context window fills, then the "full" alarm
for k in range(14):
    fx.put(clack(0.8 + 0.03 * (k % 5)), A(12) + 0.15 + 0.2 * k, 0.4, ((k * 3) % 5 - 2) / 3)
fx.put(add(bell(988, 1.2), 0.6 * bell(1480, 1.2)), W(12, "context"), 0.25)
for k in range(4):
    fx.put(blip(1046 if k % 2 == 0 else 784, 0.14), A(13) + 0.1 + 0.3 * k, 0.28)

# older blocks get pushed out and fall away; forgetting wobble
for k in range(5):
    fx.put(clack(1.1), W(14, "pushed") - 0.1 + 0.2 * k, 0.4)
fx.put(sweep(0.9, 2500, 200), W(14, "out"), 0.35)
fx.put(sub_drop(0.8, 120, 40), W(14, "out") + 0.4, 0.4)
fx.put(wobble(0.9), W(14, "forget"), 0.35)

# letters? strawberry fuses into one block; wrong-count buzzer
fx.put(blip(880, 0.07), W(15, "letters"), 0.25)
for k in range(10):
    fx.put(blip(660 + 50 * k, 0.04), A(16) + 0.1 + 0.05 * k, 0.15)
fx.put(add(clack(0.7), thump(70, 0.4, 2.0)), W(16, "one") - 0.05, 0.6)
fx.put(bubble(1.4), W(16, "reason"), 0.35)
fx.put(buzzer(), W(16, "r's") + 0.05, 0.35)

# "how many R's?" drum roll -> "Three." reveal
for tt_, sig in drum_roll(W(17, "strawberry") + 0.25, A(18) - 0.05, 0.28, 0.07, 76):
    fx.put(sig, tt_, 0.45)
fx.put(impact(0.7), A(18), 0.75)
fx.put(shing(0.6), A(18) + 0.02, 0.4)
for k, f in enumerate([1568, 1976, 2349, 3136]):
    fx.put(bell(f, 1.2), A(18) + 0.12 + 0.09 * k, 0.15)
fx.put(blip(1320, 0.07), W(18, "checked") + 0.25, 0.3)
fx.put(blip(1760, 0.09), W(18, "checked") + 0.33, 0.3)
# back to the cold open
fx.put(sweep(0.9, 200, 4000), DUR - 0.9, 0.45)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.5, makeup_db=4.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))

mix = (sfx[:N] * (0.75 * duck)[:, None] + voice[:, None]) * 10 ** (1.5 / 20)
# look-ahead peak limiter to -1 dBFS (no clipping on the voices)
ceiling = 10 ** (-1 / 20)
pk = np.max(np.abs(mix), axis=1)
win = int(0.005 * SR)
held = np.repeat([pk[max(0, i - win): i + 2 * win].max() for i in range(0, N, win)], win)[:N]
gain = np.minimum(1, ceiling / np.maximum(held, 1e-9))
k = int(0.01 * SR)
gain = np.minimum(np.convolve(gain, np.ones(k) / k, mode="same"), ceiling / np.maximum(pk, 1e-9))
mix = mix * gain[:, None]
fade = int(0.02 * SR)
mix[:fade] *= np.linspace(0, 1, fade)[:, None]
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
write_wav(os.path.join(ROOT, "assets", "audio", "mix.wav"), mix)
db = 20 * np.log10(np.sqrt(np.mean(mix ** 2)) + 1e-12)
print(f"wrote mix.wav (RMS {db:.1f} dBFS, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS)")

vo = [{"who": c["who"], "a": c["a"], "b": c["b"], "w": c["w"]} for c in clips]
with open(os.path.join(ROOT, "captions.js"), "w") as f:
    f.write("// generated by scripts/synth_audio.py: captions, line/word timings and mouth flaps for the dialogue\n")
    f.write(f"window.DUR = {DUR};\n")
    f.write("window.CAPS = " + json.dumps(captions) + ";\n")
    f.write("window.VO = " + json.dumps(vo) + ";\n")
    f.write("window.MOUTH = " + json.dumps(mouth) + ";\n")
print(f"wrote captions.js ({len(captions)} chunks)")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:3s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
