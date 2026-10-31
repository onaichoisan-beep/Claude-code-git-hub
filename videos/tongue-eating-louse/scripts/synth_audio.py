"""Sound for "The parasite that becomes a fish's tongue": text cards + open-source sound only (NO narration — owner's rule),
STYLE_GUIDE.md section 6:

- SIGNATURE sound = the slurp. Every blood pulse the louse drinks is a wet slurp + a tick on the TONGUE % counter; the pulses
  speed up as the tongue shrinks (1.5/s -> 7/s) until the 0.25 s break and the PLOP of the tongue falling off. Afterwards a
  crunch + leg-click on every chew (MEALS counter).
- Nonstop 8-bit bed (92 -> 150 BPM with the pulses), a blip on every card, whoosh + hit on every cut, a creature squeak on
  every speech bubble, tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 30.0
B = dict(SWIM=4.0, GILL=6.6, INSIDE=8.0, FEMALE=8.7, GRAB=10.0, DRINK=11.0, BREAK=16.75, HIT=17.0, CLAMP=19.2, NEWT=20.0,
         EAT=22.0, ONLY=24.0, CTA=26.5, STOP=28.7, REWIND=29.5)

CARDS = [
    (0.10, 1.95, "THIS FISH'S TONGUE|IS *STARING* AT YOU"),
    (2.05, 3.90, "BECAUSE IT'S NOT|A *TONGUE*"),
    (4.10, 6.40, "IT'S A *TONGUE-EATING*|LOUSE"),
    (6.50, 7.90, "IT SWIMS IN THROUGH|THE *GILLS*"),
    (8.10, 9.90, "INSIDE, IT TURNS FROM|MALE TO *FEMALE*"),
    (10.00, 11.90, "THEN IT GRABS|THE *TONGUE*"),
    (12.00, 14.20, "AND DRINKS|ITS *BLOOD*"),
    (14.30, 16.70, "THE TONGUE|*SHRIVELS*..."),
    (17.00, 19.00, "...AND *FALLS OFF*"),
    (19.20, 21.85, "THE LOUSE BECOMES|THE *NEW TONGUE*"),
    (22.00, 23.90, "THE FISH KEEPS|*EATING* NORMALLY"),
    (24.00, 26.35, "THE ONLY KNOWN PARASITE|THAT *REPLACES AN ORGAN*"),
    (26.50, 28.60, "SEND THIS TO A|*SEAFOOD* LOVER"),
]
BUBBLES = [(0.55, "HIIII."), (17.45, "WHERE'S MY TONGUE?"), (22.6, "WE SHARE.")]


def pulses():
    out, t = [], B["GRAB"] + 0.6
    while t < B["BREAK"] - 0.05:
        u = (t - B["GRAB"]) / (B["BREAK"] - B["GRAB"])
        out.append(round(t, 3))
        t += 1 / (1.5 + 5.5 * u ** 1.5)
    return out


B["PULSES"] = pulses()
B["CHEWS"] = [round(B["EAT"] + 0.3 + k * 0.42, 3) for k in range(int((B["CTA"] - B["EAT"] - 0.3) / 0.42))]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed
fx.x += CT.bed([
    S(0.0, B["SWIM"], 92, 92, "kbo"),
    S(B["SWIM"], B["INSIDE"], 112, 116, "kbh"),
    S(B["INSIDE"], B["DRINK"], 116, 120, "kbha"),
    S(B["DRINK"], B["BREAK"], 120, 150, "kbhsa"),
    S(B["HIT"], B["EAT"], 96, 96, "kbo"),
    S(B["EAT"], B["CTA"], 124, 124, "kbhsal"),
    S(B["CTA"], B["STOP"] + 0.2, 136, 136, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))
amb.x += (0.18 * F.drone(DUR, 49, seed=3))[:, None]           # under water: a low hum
for k in range(int(DUR / 1.7)):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.6, 500 + 90 * (k % 4))), 0.4 + k * 1.7, 0.14, (k % 3 - 1) * 0.6)

# ---------------------------------------------------------------- 0. the stare (the story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(braam(1.8, 49), 0.05, 0.35)
for k in range(6):                                             # its legs twitch
    fx.put(F.tick(4200 + 200 * (k % 2), 0.8), 0.25 + k * 0.11, 0.3, 0.3)
fx.put(osfx.lib("glitch-1"), 2.05, 0.2)

# ---------------------------------------------------------------- speech bubbles: a creature squeak each
fx.put(osfx.sound("oga/creatures/bug_01", sweep(0.25, 1800, 2600)), BUBBLES[0][0], 0.45)
fx.put(osfx.sound("oga/creatures/misc_04", sweep(0.3, 600, 300)), BUBBLES[1][0], 0.4)
fx.put(osfx.sound("oga/creatures/weird_03", sweep(0.4, 300, 900)), BUBBLES[2][0], 0.35)

# ---------------------------------------------------------------- 1. swims in through the gills
fx.put(osfx.lib("whoosh"), B["SWIM"] - 0.15, 0.5)
fx.put(impact(0.5), B["SWIM"], 0.35)
for k in range(14):                                            # tiny paddling legs
    fx.put(F.tick(3000 + 150 * (k % 3), 0.6), B["SWIM"] + 0.4 + k * 0.16, 0.22, -0.3)
fx.put(osfx.sound("oga/water-splash/slime_03", F.splash(0.4, 5)), B["GILL"], 0.6)

# ---------------------------------------------------------------- 2. turns female, grabs the tongue
fx.put(osfx.lib("whoosh-cinematic"), B["INSIDE"] - 0.2, 0.55)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["FEMALE"], 0.45)
fx.put(osfx.sound("oga/water-splash/slime_06", thump(160, 0.12, 2)), B["GRAB"], 0.7)
fx.put(impact(0.6), B["GRAB"], 0.4)

# ---------------------------------------------------------------- 3. SIGNATURE: the slurps (TONGUE % ticks down with each)
for k, t in enumerate(B["PULSES"]):
    fx.put(osfx.sound(f"oga/water-splash/slime_{(k % 9) + 1:02d}", F.splash(0.25, k)), t, 0.36, (k % 3 - 1) * 0.3)
    fx.put(sweep(0.12, 900, 300) * 0.5, t, 0.2)
    fx.put(F.tick(2000 + 30 * k, 1.0), t + 0.02, 0.32)
fx.put(riser(B["BREAK"] - B["DRINK"], 120, 1600), B["DRINK"], 0.3)

# ---------------------------------------------------------------- 4. BREAK -> the tongue falls off: PLOP
fx.put(osfx.sound("oga/water-splash/splash_04", F.splash(1.0, 9)), B["HIT"], 0.9)
fx.put(impact(0.9), B["HIT"], 0.8)
fx.put(sub_drop(1.0), B["HIT"], 0.7)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", CT.womp(330, 3, 0.2)), B["HIT"] + 0.5, 0.4)

# ---------------------------------------------------------------- 5. clamps on: the new tongue
fx.put(osfx.lib("whoosh"), B["CLAMP"] - 0.15, 0.4)
fx.put(osfx.sound("oga/water-splash/slime_08", thump(140, 0.15, 2)), B["CLAMP"] + 0.4, 0.7)
fx.put(osfx.sound("oga/100-sfx/metal_04", F.tick(2600, 1.0)), B["CLAMP"] + 0.45, 0.4)
fx.put(osfx.sfxr("powerUp", seed=8), B["NEWT"], 0.4)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(880, 1.3)), B["NEWT"] + 0.1, 0.35)

# ---------------------------------------------------------------- 6. it eats normally: crunch + leg-click per chew (MEALS counter)
fx.put(osfx.lib("whoosh"), B["EAT"] - 0.15, 0.5)
fx.put(impact(0.5), B["EAT"], 0.3)
for k, t in enumerate(B["CHEWS"]):
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(300, 0.08, 1.5)), t, 0.45)
    fx.put(F.tick(4400, 0.7), t + 0.08, 0.28, 0.3)
fx.put(osfx.sfxr("pickupCoin", seed=5), B["ONLY"], 0.35)

# ---------------------------------------------------------------- 7. CTA
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.5)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.35)

# ---------------------------------------------------------------- 8. tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 92, 92, "kbo")], gain=0.5, crescendo=(0.8, 0.8))
amb.x += (0.18 * F.drone(DUR, 49, seed=3) * seg(B["REWIND"] + 0.1, DUR, 0.1))[:, None]

CT.card_blips(fx, CARDS, gain=0.15)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["PULSES"]), "pulses; DUR", DUR)
