"""Narration + fast sound for "How many humans have EVER lived?" (Part 2 of the ancestors hit), narrated on request.

- Narrated: narrator + YOU (the same voices as the ancestors video) + the ancestor (the same elder, low + hall reverb).
- SIGNATURE = the births. Every little person that pops onto the timeline is a pop/blip; the births speed up from 1.5/s
  to 28/s while the HUMANS EVER BORN counter races to 117 billion, blurring into a buzz; 0.3 s break; slam on 117,000,000,000.
- "Gone": the 109 billion fade into ghosts (a falling shimmer + wind); "7%": a bell; the ancestor: gong + warm pad.
- Fast pacing: nonstop 8-bit bed 110 -> 168 BPM, blip on every caption chunk, whoosh + hit on every cut, tape-stop + rewind.

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
GAPS = {1: 0.2, 2: 0.25, 3: 0.2, 4: 0.2, 5: 0.3, 6: 0.2, 7: 0.25, 8: 0.3, 9: 0.4, 10: 0.35}

CAPS = [
    [("*8 BILLION* PEOPLE ARE|ALIVE RIGHT NOW", "eight"), ("SO HOW MANY HAVE|*EVER* LIVED?", "so")],
    [("LIKE... *20 BILLION*?", "like")],
    [("LET'S *COUNT*.", "let's"), ("STARTING *200,000*|YEARS AGO", "scientists")],
    [("FOR MOST OF HISTORY:|ONLY *A FEW MILLION*", "for"), ("BUT BABIES KEPT|BEING *BORN*", "but")],
    [("*HUNTERS*", "hunters"), ("*FARMERS*", "farmers"), ("*KINGS*", "kings"), ("AND EVERY ONE OF|YOUR *ANCESTORS*", "and")],
    [("THE BEST ESTIMATE?", "the"), ("*117 BILLION*|HUMANS EVER BORN", "about")],
    [("SO WHERE ARE|THEY *ALL*?", "so")],
    [("*GONE.*", "gone"), ("FOR EVERY PERSON ALIVE,|*~14* LIVED AND DIED BEFORE", "for")],
    [("ONLY *7%* OF ALL HUMANS|EVER ARE ALIVE NOW", "only")],
    [("YOU'RE IN THE *7%*,|GRANDCHILD.", "you're"), ("MAKE IT *COUNT*.", "make")],
    [("SEND THIS TO SOMEONE|IN THE *7%*", "send")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.3, gaps=GAPS, max_pause=0.3)
K = V.Words(clips)
A, Bn, W, E = K.A, K.B, K.W, K.E

B = {}
B["GUESS"] = A(1)
B["COUNT"] = A(2)
B["START"] = W(2, "scientists")
B["FEW"] = A(3)
B["BABIES"] = W(3, "babies")
B["HUNT"], B["FARM"], B["KING"], B["ANCS"] = W(4, "hunters"), W(4, "farmers"), W(4, "kings"), W(4, "ancestors")
B["EST"] = A(5)
B["HIT"] = W(5, "one")
B["BREAK"] = B["HIT"] - 0.3
B["WHERE"] = A(6)
B["GONE"] = A(7)
B["FOURTEEN"] = W(7, "fourteen")
B["SEVEN"] = A(8)
B["ANC"] = A(9)
B["CTA"] = A(10)
B["STOP"] = Bn(10) + 0.35
B["REWIND"] = B["STOP"] + 0.8
DUR = round(np.ceil((B["REWIND"] + 0.45) * 10) / 10, 1)


def births():
    out, t = [], B["START"]
    while t < B["BREAK"] - 0.05:
        u = (t - B["START"]) / (B["BREAK"] - B["START"])
        out.append(round(t, 3))
        t += 1 / (1.5 + 26.5 * u ** 2.2)
    return out


B["BIRTHS"] = births()
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}, {len(B['BIRTHS'])} births")

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
tracks = V.voice_tracks(clips, SR, N, band)
anc = tracks["ancestor"]
tracks["ancestor"] = reverb(anc + 0.4 * band(anc, 60, 260), length=2.2, wet=0.35)[:N]
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.45)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed
fx.x += CT.bed([
    S(0.0, B["COUNT"], 110, 110, "kbh"),
    S(B["COUNT"], B["HUNT"], 116, 132, "kbhs"),
    S(B["HUNT"], B["BREAK"], 132, 168, "kbhsa"),
    S(B["HIT"], B["GONE"], 128, 128, "kbhsal"),
    S(B["GONE"], B["SEVEN"], 64, 64, "kbo"),
    S(B["SEVEN"], B["ANC"], 120, 120, "kbhsa"),
    S(B["ANC"], B["CTA"], 96, 96, "kb"),
    S(B["CTA"], B["STOP"] + 0.2, 136, 136, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- SIGNATURE: a pop per birth, faster and faster, rising
for k, t in enumerate(B["BIRTHS"]):
    u = (t - B["START"]) / (B["BREAK"] - B["START"])
    f = 600 * 2 ** (u * 2)
    fx.put(add(CT.square(f, 0.04, 0.25), 0.5 * CT.square(f * 1.5, 0.03, 0.125)), t, 0.16, ((k * 7) % 5 - 2) * 0.3)
    if k % 3 == 0:
        fx.put(osfx.lib("pop"), t, 0.22, ((k * 3) % 5 - 2) * 0.3)
fx.put(riser(B["BREAK"] - B["HUNT"], 200, 2200), B["HUNT"], 0.3)
for tw in (B["HUNT"], B["FARM"], B["KING"], B["ANCS"]):                      # each era stamps in
    fx.put(osfx.sound("oga/100-sfx/slam_02", thump(110, 0.2, 1.5)), tw, 0.35)
    fx.put(osfx.sfxr("blipSelect", seed=int(tw * 10) % 50), tw + 0.02, 0.25)

# ---------------------------------------------------------------- 0. now: 8 billion (story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/100-sfx/bell_01", bell(1046, 1.2)), 0.1, 0.25)
for k in range(8):
    fx.put(osfx.lib("pop"), 0.25 + k * 0.12, 0.25, (k % 3 - 1) * 0.5)
fx.put(osfx.sfxr("jump", seed=11), B["GUESS"] + 0.1, 0.25)
fx.put(osfx.lib("whoosh-cinematic"), B["COUNT"] - 0.2, 0.5)
fx.put(rewind(0.6), B["COUNT"] + 0.2, 0.35)                                  # back to 200,000 years ago
fx.put(F.fire(2.0, 5), B["START"], 0.3)                                      # the first campfire

# ---------------------------------------------------------------- BREAK -> 117 billion
fx.put(sweep(0.3, 1400, 3000) * 0.3, B["BREAK"], 0.4)
fx.put(osfx.sound("oga/bangs-fireworks/bang_03", impact(1.0)), B["HIT"], 0.7)
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(sub_drop(1.0), B["HIT"], 0.6)
fx.put(osfx.sfxr("powerUp", seed=5), B["HIT"] + 0.05, 0.3)
fx.put(osfx.sound("oga/creatures/ooh", sweep(0.3, 500, 900)), B["WHERE"] + 0.05, 0.22)

# ---------------------------------------------------------------- gone: ghosts rise + 1 vs 14
fx.put(osfx.lib("whoosh"), B["GONE"] - 0.15, 0.45)
fx.put(sweep(1.6, 2400, 300) * 0.35, B["GONE"], 0.35)
fx.put((0.4 * F.wind(3.0, 300, 700, 0.6, seed=4)), B["GONE"], 0.3)
for k in range(14):
    fx.put(CT.square(880 * 2 ** (-k / 24), 0.05, 0.25), B["FOURTEEN"] + 0.1 + k * 0.08, 0.12, (k % 3 - 1) * 0.5)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(1318.5, 1.5)), W(8, "seven"), 0.4)
fx.put(F.sparkle(1.0, seed=8), W(8, "seven") + 0.05, 0.3)

# ---------------------------------------------------------------- the ancestor returns
fx.put(osfx.sound("oga/100-sfx/gong_01", gong(110, 3.0)), B["ANC"] - 0.3, 0.5)
amb.put(F.pad(B["CTA"] - B["ANC"] + 0.6, [110, 164.8, 220, 277.2], a=0.8, r_=1.0), B["ANC"] - 0.2, 0.3)
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.3)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 110, 110, "kbh")], gain=0.5, crescendo=(0.8, 0.8))

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
