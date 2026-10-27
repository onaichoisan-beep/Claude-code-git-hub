"""Narration + SFX for "The Cat on Its 9th Life".

  python3 scripts/synth_audio.py

Mittens (the cat) narrates in a dry British voice; the owner shouts once. Each of the eight lost
lives gets its own little sound world and a comic "poof" as the soul floats away. Writes
assets/audio/mix.wav plus captions.js (captions, word timings, mouth flaps) for the picture.
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
GAPS = {1: 0.6, 2: 0.6, 3: 0.55, 4: 0.65, 5: 0.9, 6: 0.75, 7: 0.75, 8: 0.6, 9: 0.75, 10: 0.35, 11: 0.55}
TAIL = 2.2  # the paw nudges the glass... it falls... smash -> back to the opening

CAPS = [
    [("I'M ON MY *9TH LIFE*.", "i'm"), ("WANT TO KNOW WHAT|HAPPENED TO THE OTHER *8*?", "want")],
    [("*1*. EGYPT.", "one"), ("THEY *WORSHIPPED* ME.", "they"), ("THE *CROCODILE* DIDN'T.", "the")],
    [("*2*. A VIKING SHIP.", "two"), ("I CHASED A *FISH*.", "i"), ("*OVERBOARD*.", "overboard")],
    [("*3*. CHINA.", "three"), ("I NAPPED IN A|*FIREWORKS* SHOP.", "i")],
    [("*4*. PIRATES.", "four"), ("I ATE THE|CAPTAIN'S *PARROT*.", "i")],
    [("*5*. PARIS.", "five"), ("I CLIMBED THE|*EIFFEL TOWER*.", "i"), ("FORGOT ABOUT *DOWN*.", "forgot")],
    [("*6*. I SNUCK ONTO|A *ROCKET*.", "six"), ("SPACE HAS *NO FISH*.", "space")],
    [("*7*. A SCIENTIST|PUT ME IN A *BOX*.", "seven"), ("LONG STORY.", "long")],
    [("*8*. LAST TUESDAY.", "eight"), ("A *CUCUMBER*.", "a")],
    [("SO NOW...", "so"), ("I'M BEING VERY, VERY|*CAREFUL*.", "i'm")],
    [("*MITTENS!*", "mittens"), ("GET OFF THE *COUNTER!*", "get")],
    [("VERY *CAREFUL*.", "very")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.3, gaps=GAPS, max_pause=0.34)
DUR = round(np.ceil((clips[-1]["b"] + TAIL) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")
os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402

K = V.Words(clips)
A, B, W, E = K.A, K.B, K.W, K.E
tracks = V.voice_tracks(clips, SR, N, band, gains={"human": 0.8})
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.6)
captions = V.make_captions(clips, CAPS, DUR)
amb, fx = Bus(), Bus()


def R(name, fallback, dur=None):
    """a real recording from assets/sfx (fetched from Openverse) if we have it, else the synthesised one"""
    x = load(os.path.join(ROOT, "assets", "sfx", name + ".wav"), 0, dur)
    return fade_out(x, 0.08) if x is not None else fallback


def L(name):
    """the bundled HyperFrames sound library"""
    x = load(os.path.join(LIB, name + ".mp3")) if LIB else None
    return x if x is not None else np.zeros(10)


def bed(sig, a, b, gain, fade=0.3, pan=0.0):
    n = int((b - a) * SR)
    x = np.tile(sig, int(np.ceil(n / len(sig))))[:n].copy()
    f = int(fade * SR)
    if f and len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
    amb.put(x, a, gain, pan)


def death(tt, big=1.0):
    """the punchline lands: a soft hit, then the soul poofs out and floats up with a harp"""
    fx.put(add(impact(0.5 * big), 0.4 * noise_hit(0.1, 300, 6000)), tt, 0.45 * big)
    fx.put(F.poof(), tt + 0.12, 0.4)
    fx.put(L("pop"), tt + 0.1, 0.35)
    fx.put(L("sparkle"), tt + 0.2, 0.3)
    fx.put(F.harp_up(784, 6, 0.05), tt + 0.18, 0.14)


# scene spans + the moment each life ends (the picture reads DEATHS from captions.js)
S = [A(i) for i in range(len(clips))] + [DUR]
DEATHS = [W(1, "didn't") + 0.05, W(2, "overboard") + 0.4, W(3, "shop") + 0.3, E(4, "parrot") + 0.6,
          W(5, "down") + 0.75, E(6, "fish") + 0.35, E(7, "story") + 0.1, E(8, "cucumber") + 0.2]
T_BOOM = W(3, "shop")
T_KICK = E(4, "parrot") + 0.15
T_PUSH = B(11) + 0.35                      # paw nudges the glass
T_SMASH = T_PUSH + 0.85                    # it hits the floor

# ---------------------------------------------------------------- HOOK: Mittens + eight ghosts
fx.put(impact(0.9), 0.0, 0.8)
fx.put(braam(2.0, 55), 0.0, 0.4)
fx.put(R("purr", F.purr(3.0), 3.0), 0.1, 0.35)
fx.put(R("meow", F.meow(0.55, 560), 1.2), 0.05, 0.3)
for k in range(8):
    fx.put(bell(1046.5 * 2 ** (k / 12 * 2), 1.6), W(0, "eight") - 0.3 + 0.06 * k, 0.07, (k - 3.5) / 4)
fx.put(add(thump(80, 0.3, 1.0), shing(0.4)), W(0, "eight"), 0.35)
fx.put(rewind(0.5), A(1) - 0.6, 0.55)
for ch in range(2):
    amb.x[:, ch] += 0.18 * norm(band(rng.standard_normal(N), 60, 300)) * seg(0, A(1), 0.3)  # room tone

# ---------------------------------------------------------------- 1. EGYPT: worship... the crocodile
bed(F.wind(S[2] - S[1] + 0.5, 300, 700, 0.3, seed=11), S[1], S[2], 0.35)
fx.put(gong(110, 3.0), A(1) + 0.05, 0.3)
fx.put(F.pad(2.0, [293.7, 440, 587.3], a=0.4, r_=1.0), W(1, "worshipped") - 0.1, 0.18)
for k in range(3):
    fx.put(thump(120, 0.15, 1.0), W(1, "worshipped") + 0.25 * k, 0.25)  # bowing
fx.put(R("splash", F.splash(1.0, seed=12), 1.2), W(1, "crocodile") - 0.3, 0.35)
fx.put(R("croc", F.roar_croc(0.9), 1.0), W(1, "crocodile") - 0.15, 0.55)
fx.put(add(thump(150, 0.15, 2.5), noise_hit(0.04, 1500, 8000)), DEATHS[0] - 0.03, 0.6)  # SNAP
death(DEATHS[0])

# ---------------------------------------------------------------- 2. VIKING SHIP: storm, fish, overboard
bed(R("storm", F.sea(6, swell=3.5, seed=21)), S[2], S[3], 0.5)
bed(R("wind", F.wind(5, 400, 1000, 0.6, seed=22)), S[2], S[3], 0.3)
fx.put(F.creak(1.2, 80, seed=23), A(2) + 0.3, 0.35)
fx.put(R("thunder", add(noise_hit(0.6, 40, 3000), thump(40, 1.2, 2.0)), 3.0), A(2) + 0.15, 0.4)  # thunder
fx.put(F.splash(0.5, seed=24), W(2, "fish") - 0.1, 0.35)
fx.put(sweep(0.5, 600, 3000), W(2, "overboard") - 0.35, 0.4)
fx.put(R("splash", F.splash(1.5, seed=25), 1.5), DEATHS[1] - 0.1, 0.7)
death(DEATHS[1])

# ---------------------------------------------------------------- 3. CHINA: snoring cat, fuse, KABOOM
bed(F.crickets(4, seed=31), S[3], S[4], 0.1)
fx.put(gong(196, 2.5), A(3) + 0.05, 0.22)
fx.put(F.purr(1.6, seed=32), W(3, "napped") - 0.1, 0.35)
fx.put(F.sizzle(1.0, seed=33), W(3, "fireworks") - 0.2, 0.4)
tb = T_BOOM
fx.put(add(impact(1.3), 0.8 * braam(1.6, 60)), tb, 0.7)
fx.put(R("boom", L("impact-bass-1"), 2.5), tb, 0.8)
fx.put(R("crackers", np.zeros(10), 3.0), tb + 0.2, 0.5)
for k in range(6):
    fx.put(F.firework(34 + k, dist=1.0), tb + 0.05 + 0.12 * k - 0.55, 0.35, (k % 3 - 1) * 0.7)
death(DEATHS[2], 0.6)

# ---------------------------------------------------------------- 4. PIRATES: squawk, gulp, the plank
bed(F.sea(5, swell=4.5, seed=41), S[4], S[5], 0.45)
fx.put(F.creak(1.0, 95, seed=42), A(4) + 0.2, 0.3)
fx.put(F.gull(43), A(4) + 0.4, 0.15, 0.6)
fx.put(R("parrot", F.squawk(44), 1.0), W(4, "parrot") + 0.05, 0.5)
fx.put(R("gulp", thump(150, 0.2, 2.0), 0.8), W(4, "ate"), 0.45)   # gulp
fx.put(F.stab(146.8, 1.2), W(4, "parrot") + 0.2, 0.4)        # the captain's glare
fx.put(add(thump(90, 0.25, 1.5), 0.5 * noise_hit(0.05, 300, 3000)), T_KICK, 0.5)  # boot
fx.put(sweep(0.4, 800, 3000), T_KICK + 0.05, 0.3)
fx.put(F.splash(1.3, seed=45), DEATHS[3] - 0.1, 0.55)
death(DEATHS[3])

# ---------------------------------------------------------------- 5. PARIS: wind up top, gulp, the long fall
bed(F.wind(5, 600, 1200, 0.7, seed=51), S[5], S[6], 0.4)
fx.put(add(bell(1318.5, 2.0), 0.6 * bell(1975.5, 2.0)), W(5, "eiffel"), 0.18)
fx.put(thump(160, 0.2, 2.0), W(5, "forgot") - 0.05, 0.4)  # gulp
n = int(1.1 * SR)
tq = np.arange(n) / SR
fall = np.sin(2 * np.pi * np.cumsum(2200 * (0.3 / 2.2) ** (tq / 1.1)) / SR) * env(n, 0.02, 0.1)
fx.put(R("fallwhistle", fall, 1.2), W(5, "down") - 0.1, 0.35)
fx.put(add(thump(60, 0.4, 2.0), noise_hit(0.1, 200, 4000)), DEATHS[4] - 0.05, 0.6)
death(DEATHS[4])

# ---------------------------------------------------------------- 6. ROCKET: countdown beeps, launch, silence of space
for k in range(3):
    fx.put(blip(880, 0.12), A(6) + 0.05 + 0.3 * k, 0.25)
fx.put(R("rocket", F.rumble(2.0, 25, 400, seed=61), 2.4), W(6, "snuck"), 0.7)
fx.put(add(impact(1.0), sub_drop(1.2)), W(6, "rocket") - 0.05, 0.6)
fx.put(F.pad(3.0, [220, 261.6, 329.6], a=0.6, r_=1.5), W(6, "space") - 0.3, 0.2)  # weightless
fx.put(F.meow(0.8, 420, seed=62, sad=True), E(6, "fish") + 0.05, 0.35)
death(DEATHS[5], 0.7)

# ---------------------------------------------------------------- 7. THE BOX: lab hum, lid, rattle
bed(0.6 * F.pad(4.5, [55, 110], a=0.2, r_=0.2) + 0.4 * F.whispers(4.5, seed=71), S[7], S[8], 0.12)
for k in range(4):
    fx.put(blip(1200 + 200 * (k % 2), 0.06), A(7) + 0.2 + 0.25 * k, 0.15)
fx.put(add(thump(110, 0.3, 1.2), 0.5 * noise_hit(0.05, 400, 3000)), W(7, "box") + 0.2, 0.55)  # lid shuts
for k in range(5):
    fx.put(thump(140 + 20 * k, 0.12, 1.0), W(7, "long") - 0.2 + 0.12 * k, 0.3, (k % 2) * 0.6 - 0.3)
fx.put(F.poof(seed=72), DEATHS[6], 0.45, 0.5)
death(DEATHS[6], 0.6)

# ---------------------------------------------------------------- 8. CUCUMBER: crunching, the reveal, the leap
fx.put(R("crunch", F.ratchet(0.6, 9, 600, seed=81), 1.4), A(8) + 0.1, 0.25)   # nom nom
fx.put(F.stab(233, 1.0), W(8, "cucumber") - 0.1, 0.5)
fx.put(F.hiss_cat(0.5), W(8, "cucumber") + 0.05, 0.45)
fx.put(R("hiss", F.meow(0.5, 900, seed=82), 1.0), W(8, "cucumber") + 0.15, 0.4)
fx.put(R("boing", np.zeros(10), 1.0), W(8, "cucumber") + 0.15, 0.3)
fx.put(riser(0.5, 300, 1800), W(8, "cucumber") + 0.1, 0.25)
death(DEATHS[7])

# ---------------------------------------------------------------- now: careful, the counter, the glass
bed(F.purr(3.0, seed=91), S[9], S[10], 0.25)
for k in range(int((DUR - S[9]) / 0.5)):
    fx.put(F.tick(2600 if k % 2 else 2000, 0.6), S[9] + 0.5 * k, 0.12)  # kitchen clock
fx.put(add(bell(659.3, 1.0), 0.5 * bell(987.8, 1.0)), W(9, "careful") - 0.05, 0.15)
fx.put(add(thump(70, 0.4, 1.2), 0.4 * noise_hit(0.05, 300, 3000)), A(10) - 0.05, 0.35)  # door
fx.put(F.stab(196, 0.8), W(10, "counter"), 0.3)
fx.put(R("meow", F.meow(0.45, 600, seed=92), 1.2), B(10) + 0.1, 0.18)
for k in range(3):  # paw... nudge... nudge
    fx.put(add(F.tick(1500, 0.3), 0.4 * noise_hit(0.03, 2000, 6000)), T_PUSH - 0.6 + 0.3 * k, 0.3)
fx.put(sweep(0.7, 2500, 600), T_PUSH + 0.1, 0.35)
fx.put(R("glass", F.glass_smash(), 2.0), T_SMASH, 0.85)
fx.put(impact(0.7), T_SMASH, 0.4)
fx.put(sweep(0.6, 300, 4000), DUR - 0.6, 0.3)

for i in range(2, 11):
    fx.put(L("whoosh-short"), A(i) - 0.2, 0.3)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.55, makeup_db=4.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
with open(os.path.join(ROOT, "captions.js"), "a") as f:
    f.write(f"window.T_PUSH = {T_PUSH:.3f}; window.T_SMASH = {T_SMASH:.3f}; window.T_BOOM = {T_BOOM:.3f}; window.T_KICK = {T_KICK:.3f};\n")
    f.write("window.DEATHS = " + json.dumps([round(d, 3) for d in DEATHS]) + ";\n")
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:5s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
