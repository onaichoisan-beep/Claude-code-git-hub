"""Narration + fast creepy sound for "One Inch Every Night" (a story set in Japan, told in our own words).

- Voices: Kokoro-82M — narrator am_michael, mom af_bella, dad am_fenrir, Yui af_sky, the seller am_onyx (low, smug, a little room).
- Captions: 1-3 words per card, word-synced (the fast story-mode look of memory-loss-except-you).
- SIGNATURE = the scrape: every night on the DAY counter is one wooden drag ("one inch"); the nights speed up from 1 per
  second to a rattle by day 30. Under it a dark pulse (kick + hats, no melody) + a low drone + a soft music-box motif.
  Literal effects: kotatsu/shelf/TV thuds, a camera beep + static, flour puff, footsteps, a sold stamp, a handshake,
  0.3 s silence, then the reveal hit; tape-stop + rewind into frame 1.

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
GAPS = {1: 0.15, 2: 0.15, 3: 0.12, 4: 0.08, 5: 0.15, 6: 0.15, 7: 0.2, 8: 0.15, 9: 0.15, 10: 0.2}
GOLD = {"japan,", "inch.", "one", "kotatsu.", "shelf.", "tv.", "ten,", "table?", "fifteen,", "wall.", "static.", "flour",
        "footprints,", "key.", "thirty.", "half", "price.", "familiar.", "ago.", "movement.", "spare", "caught", "comment"}

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.15, gaps=GAPS, max_pause=0.45)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E


def auto_caps():
    caps = []
    for c in clips:
        chunks, cur = [], []
        for w in c["w"]:
            cur.append(w[0])
            if re.search(r"[.,!?:]$", w[0]) or len(cur) == 3:
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
        out = []
        for ch in chunks:
            words = [f"*{w.upper()}*" if w.lower() in GOLD else w.upper() for w in ch]
            out.append((" ".join(words).replace("* *", " "), re.sub(r"[^A-Za-z0-9']", "", ch[0]).lower() or ch[0]))
        caps.append(out)
    return caps


CAPS = auto_caps()
B = {f"L{i}": round(A(i), 3) for i in range(len(clips))}
B["INCH"] = W(0, "inch")
B["KOT"], B["SHOE"], B["TV"] = W(1, "kotatsu"), W(1, "shoe"), W(1, "tv")
B["DAY10"] = A(2)
B["NOTICE"] = B["DAY10"]
B["MOM"], B["DAD"] = A(3), A(4)
B["DAY15"] = B["CAM"] = B["STATIC"] = B["FLOUR"] = A(5)
B["PRINTS"] = W(5, "next")
B["KEY"] = A(6)
B["DAY30"] = A(7)
B["SELL"] = W(7, "they")
B["BUYER"] = A(8)
B["HIT"] = W(8, "man")
B["BREAK"] = B["HIT"] - 0.3
B["SELLER"] = A(9)
B["SPARE"] = A(10)
B["CTA"] = W(10, "would")
B["STOP"] = Bn(10) + 0.3
B["REWIND"] = B["STOP"] + 0.6
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)

# DAY counter keys (also = inches moved); the picture reads them
DAYK = [[0.0, 1], [B["INCH"], 1], [B["DAY10"], 10], [B["FLOUR"], 18], [B["KEY"], 26], [B["DAY30"], 30]]
B["DAYK"] = [[round(a, 3), d] for a, d in DAYK]


def day(t):
    for (a, da), (b, db) in zip(DAYK, DAYK[1:]):
        if t < b:
            return da + (db - da) * (t - a) / (b - a)
    return 30.0


nights, last = [], 1
for k in range(int(B["DAY30"] * 200) + 2):
    d = int(day(k / 200) + 1e-6)
    if d != last:
        nights.append((k / 200, d))
        last = d
B["NIGHTS"] = [round(t, 3) for t, _ in nights]
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}, {len(nights)} nights")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band, level_db=-14.0)
tracks["narrator"] = reverb(tracks["narrator"], length=0.6, wet=0.08)[:N]
tracks["seller"] = reverb(tracks["seller"] + 0.3 * band(tracks["seller"], 60, 260), length=1.2, wet=0.22)[:N]
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.5)
captions = V.make_captions(clips, CAPS, DUR, hold=0.25)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- dark pulse (no melody) + drone + a music-box motif
fx.x += CT.bed([
    S(0.0, B["NOTICE"], 96, 96, "k"),
    S(B["NOTICE"], B["CAM"], 112, 120, "kh"),
    S(B["CAM"], B["KEY"], 120, 132, "khs"),
    S(B["DAY30"], B["BREAK"], 132, 150, "khs"),
    S(B["SELLER"] + 0.3, B["CTA"], 100, 100, "k"),
    S(B["CTA"], B["STOP"] + 0.2, 120, 120, "kh"),
], gain=0.5, crescendo=(0.85, 1.15))
amb.x += (0.22 * F.drone(DUR, 52, seed=5))[:, None]
MB = [659.3, 587.3, 523.3, 493.9, 523.3, 440.0, 392.0, 440.0]          # a sad little music box
for k in range(int(DUR / 0.55)):
    t = 0.3 + k * 0.55
    if B["BREAK"] - 0.2 < t < B["SELLER"]:
        continue
    f = MB[k % len(MB)] * 2
    tt = np.arange(int(0.5 * SR)) / SR
    fx.put((np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 3.01 * tt)) * np.exp(-tt * 7), t, 0.05, ((k % 3) - 1) * 0.4)


# ---------------------------------------------------------------- SIGNATURE: one wooden scrape per night
def scrape(d, seed):
    n = int(d * SR)
    r = np.random.default_rng(seed)
    x = band(r.standard_normal(n), 180, 1800)
    am = 0.6 + 0.4 * np.sin(2 * np.pi * (35 + 10 * r.random()) * np.arange(n) / SR) ** 2
    return x * am * np.minimum(1, np.arange(n) / (0.02 * SR)) * np.linspace(1, 0.2, n) / (np.max(np.abs(x)) + 1e-9)


for k, (t, d) in enumerate(nights):
    fx.put(scrape(0.22, d), t, 0.45, ((d % 3) - 1) * 0.4)
    fx.put(F.tick(1500 + 30 * d, 1.0), t, 0.25)
fx.put(scrape(0.4, 1), B["INCH"] - 0.1, 0.6)
for tw in (B["KOT"], B["SHOE"], B["TV"]):
    fx.put(scrape(0.25, int(tw * 10)), tw, 0.5)
    fx.put(osfx.sound("oga/100-sfx/wooden_02", thump(140, 0.1, 1.5)), tw + 0.2, 0.4)

# ---------------------------------------------------------------- 0. the opening
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(880, 1.4)), 0.15, 0.25)
fx.put(osfx.sound("oga/100-sfx/key_open_01", F.tick(2400, 1.0)), W(0, "every") - 0.1, 0.5)          # a key turns
fx.put(braam(1.6, 52), B["INCH"], 0.3)

# ---------------------------------------------------------------- day 10: the table; the argument
fx.put(osfx.lib("whoosh"), B["DAY10"] - 0.12, 0.4)
fx.put(F.page_flip(3), B["DAY10"], 0.4)                                                            # calendar flip
fx.put(osfx.sound("oga/100-sfx/slam_01", thump(90, 0.25, 1.5)), W(2, "blocks"), 0.45)
fx.put(osfx.sound("oga/creatures/misc_04", sweep(0.25, 600, 400)), B["MOM"] + 0.05, 0.15)
fx.put(CT.womp(392, 3, 0.14), E(4, "did") + 0.15, 0.2)

# ---------------------------------------------------------------- flour + footprints
fx.put(F.poof(5), B["FLOUR"] + 0.4, 0.5)
fx.put(F.poof(6), B["FLOUR"] + 1.0, 0.4)
for k in range(6):
    fx.put(thump(160 + 10 * (k % 2), 0.06, 1.2), B["PRINTS"] + 0.5 + k * 0.25, 0.35, (k % 2) * 0.6 - 0.3)    # step, step
fx.put(heartbeat(), B["KEY"] - 0.3, 0.45)
fx.put(osfx.sound("oga/100-sfx/key_open_02", F.tick(2600, 1.0)), W(6, "key") + 0.1, 0.5)
fx.put(sub_drop(0.9), W(6, "key") + 0.15, 0.5)

# ---------------------------------------------------------------- day 30: sold at half price
fx.put(F.page_flip(5), B["DAY30"], 0.4)
fx.put(osfx.sound("oga/100-sfx/slam_03", impact(0.6)), W(7, "half") - 0.05, 0.55)                     # SOLD stamp
fx.put(CT.womp(330, 4, 0.16), E(7, "price") + 0.1, 0.25)
fx.put(osfx.lib("whoosh"), B["BUYER"] - 0.12, 0.4)
fx.put(riser(B["BREAK"] - B["BUYER"], 200, 1800), B["BUYER"], 0.35)

# ---------------------------------------------------------------- the reveal
fx.put(osfx.sound("oga/bangs-fireworks/bang_03", impact(1.0)), B["HIT"], 0.7)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(sub_drop(1.2), B["HIT"], 0.6)
fx.put(braam(2.2, 46), B["HIT"] + 0.05, 0.4)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(659, 1.6)), B["SELLER"] + 0.1, 0.25)
fx.put(osfx.sound("oga/100-sfx/key_open_01", F.tick(2400, 1.0)), W(10, "key") + 0.05, 0.55)            # the spare key jingles
fx.put(F.sparkle(0.8, seed=4), W(10, "key") + 0.1, 0.3)
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.12, 0.4)
fx.put(osfx.sfxr("blipSelect", seed=5), B["CTA"] + 0.1, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)

CT.card_blips(fx, [(c["a"], c["b"], "") for c in captions], gain=0.06)
for c in captions:
    fx.put(osfx.lib("whoosh-short"), c["a"] - 0.04, 0.07)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=1.0, makeup_db=5.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8, makeup_db=2.0)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write("window.BEATS = " + json.dumps({k: (round(v, 3) if not isinstance(v, list) else v) for k, v in B.items()}) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:8s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
print("DUR", DUR, "captions", len(captions))
