"""Sound for "A fish that lives in a sea cucumber's butt": text cards + open-source sound only (no narration),
STYLE_GUIDE.md section 6:

- SIGNATURE sound = the butt-breathing pump. Every breath on the BUTT BREATHS counter is a wet "fwoop" in, then out (its
  pitch rises on the way in, falls on the way out). Calm at ~0.6 breaths/s, it panics up to 3/s as the crab closes in, stops
  dead for the 0.25 s break, then the GUTS fire. While the guts regrow it comes back slow and deep.
- the pearlfish wriggles in tail first (squelch + slide whistle), nibbles (a crunch per SNACK), clanks off the butt teeth.
- Nonstop 8-bit bed, blip on every card, whoosh + hit on every cut, tape-stop + rewind into frame 1.

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
B = dict(BREATHE=4.0, WAIT=8.0, SLIDE=10.1, INSIDE=12.0, TEETH=15.5, CRAB=17.4, BREAK=18.75, HIT=19.0, REGROW=23.3,
         CTA=26.5, STOP=28.7, REWIND=29.5)

CARDS = [
    (0.10, 1.95, "THIS FISH LIVES IN A|SEA CUCUMBER'S *BUTT*"),
    (2.05, 3.90, "AND IT'S *NOT*|AN ACCIDENT"),
    (4.10, 6.20, "SEA CUCUMBERS *BREATHE*|THROUGH THEIR BUTT"),
    (6.30, 7.90, "IN... AND *OUT*"),
    (8.10, 10.00, "THE PEARLFISH WAITS|FOR IT TO *OPEN*"),
    (10.10, 11.90, "AND SLIDES IN|*TAIL FIRST*"),
    (12.10, 13.80, "SOME EVEN NIBBLE|THEIR HOST'S *INSIDES*"),
    (13.90, 15.40, "*RUDE.*"),
    (15.60, 17.30, "SO SOME SEA CUCUMBERS|GREW *BUTT TEETH*"),
    (17.40, 18.70, "AND WHEN A CRAB|*ATTACKS*..."),
    (19.00, 21.00, "IT SHOOTS ITS OWN|*GUTS* OUT"),
    (21.10, 23.20, "A DECOY SNACK|FOR THE *CRAB*"),
    (23.30, 26.40, "THEN IT *REGROWS* THEM|IN A FEW WEEKS"),
    (26.50, 28.60, "SEND THIS TO A FRIEND|WHO NEEDED THIS *FACT*"),
]


def breaths():
    """breath times (each one = in, then out). rate: calm 0.6/s, panics to 3/s as the crab closes in, slow while regrowing"""
    out, t = [], 0.3
    while t < B["STOP"]:
        if B["BREAK"] - 0.1 <= t < B["REGROW"]:
            t = B["REGROW"] + 0.2
            continue
        out.append(round(t, 3))
        if t < B["CRAB"] - 1.0:
            r = 0.65
        elif t < B["BREAK"]:
            r = 0.65 + 2.4 * min(1.0, (t - B["CRAB"] + 1.0) / 2.3) ** 1.5
        else:
            r = 0.5
        t += 1 / r
    return out


B["BREATHS"] = breaths()
B["NIBBLES"] = [round(B["INSIDE"] + 0.6 + k * 0.45, 3) for k in range(int((B["TEETH"] - B["INSIDE"] - 0.8) / 0.45))]
B["CLANKS"] = [round(B["TEETH"] + 0.9 + k * 0.5, 3) for k in range(3)]

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
    S(0.0, B["BREATHE"], 104, 104, "kbh"),
    S(B["BREATHE"], B["SLIDE"], 100, 104, "kbo"),
    S(B["SLIDE"], B["TEETH"], 112, 118, "kbha"),
    S(B["TEETH"], B["CRAB"], 118, 120, "kbhs"),
    S(B["CRAB"], B["BREAK"], 130, 160, "kbhsa"),
    S(B["HIT"], B["REGROW"], 128, 128, "kbhsal"),
    S(B["REGROW"], B["CTA"], 64, 64, "kbo"),
    S(B["CTA"], B["STOP"] + 0.2, 128, 128, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))
amb.x += (0.16 * F.drone(DUR, 52, seed=5))[:, None]
for k in range(int(DUR / 2.1)):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.6, 450 + 90 * (k % 4))), 0.8 + k * 2.1, 0.12, (k % 3 - 1) * 0.6)


# ---------------------------------------------------------------- SIGNATURE: the butt-breathing pump
def fwoop(up, d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = np.geomspace(140, 420, n) if up else np.geomspace(420, 120, n)
    tone_ = np.sin(2 * np.pi * np.cumsum(f) / SR)
    nz = band(np.random.default_rng(3 if up else 4).standard_normal(n), 200, 1600)
    e = np.sin(np.pi * tt / d) ** 1.5
    return (0.6 * tone_ + 0.5 * nz / (np.max(np.abs(nz)) + 1e-9)) * e


for k, t in enumerate(B["BREATHS"]):
    nxt = B["BREATHS"][k + 1] if k + 1 < len(B["BREATHS"]) else t + 1.5
    half = min(0.6, (nxt - t) / 2 * 0.9)
    panic = B["CRAB"] - 1.0 < t < B["BREAK"]
    deep = t > B["REGROW"]
    fx.put(fwoop(True, half), t, 0.45 if not deep else 0.4)
    fx.put(fwoop(False, half), t + half + 0.02, 0.4)
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 9 + 1:02d}", F.splash(0.2, k)), t + 0.02, 0.12 if not panic else 0.2)
    fx.put(F.tick(2400 if not panic else 3200, 0.8), t, 0.22)

# ---------------------------------------------------------------- 0. the tenant (the story starts here)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(osfx.sound("oga/water-splash/slime_04", F.splash(0.5, 3)), 0.1, 0.5)
fx.put(CT.tone_glide(900, 300, 0.5, "sine", 0.5, 0.5), 0.15, 0.25)            # slide whistle down (in it goes)
fx.put(osfx.sound("oga/creatures/cute_05", blip(1100, 0.15)), 0.7, 0.4)
fx.put(osfx.lib("glitch-1"), 2.05, 0.2)

# ---------------------------------------------------------------- 1. the reef: whoosh in
fx.put(osfx.lib("whoosh"), B["BREATHE"] - 0.15, 0.5)
fx.put(impact(0.5), B["BREATHE"], 0.35)

# ---------------------------------------------------------------- 2. the pearlfish waits ... slides in tail first
for k in range(6):
    fx.put(F.tick(3600, 0.6), B["WAIT"] + 0.3 + k * 0.3, 0.15, 0.4)
fx.put(CT.tone_glide(1200, 260, 0.9, "sine", 0.5, 0.5), B["SLIDE"], 0.3)
fx.put(osfx.sound("oga/water-splash/slime_07", F.splash(0.6, 7)), B["SLIDE"] + 0.5, 0.6)
fx.put(osfx.sfxr("jump", seed=12), B["SLIDE"] + 1.2, 0.25)

# ---------------------------------------------------------------- 3. x-ray: nibbles (SNACKS counter)
fx.put(osfx.lib("whoosh-cinematic"), B["INSIDE"] - 0.2, 0.5)
for k, t in enumerate(B["NIBBLES"]):
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(320, 0.06, 1.5)), t, 0.4, (k % 2) * 0.4 - 0.2)
    fx.put(F.tick(3000, 0.8), t + 0.03, 0.22)
fx.put(osfx.sound("oga/creatures/grunt_03", sweep(0.4, 200, 120)), B["INSIDE"] + 0.3, 0.4)
fx.put(osfx.sound("oga/retro-synth/retro_die_01", CT.womp(330, 3, 0.18)), 13.95, 0.35)

# ---------------------------------------------------------------- 4. the butt teeth: clank clank clank
fx.put(osfx.lib("whoosh"), B["TEETH"] - 0.15, 0.5)
fx.put(osfx.sound("oga/100-sfx/metal_02", F.tick(2600, 1.0)), B["TEETH"] + 0.3, 0.35)
for k, t in enumerate(B["CLANKS"]):
    fx.put(osfx.sound(f"oga/100-sfx/metal_0{k + 5}", impact(0.4)), t, 0.6, 0.2)
    fx.put(CT.square(1800 + 300 * k, 0.05, 0.25), t, 0.15)
fx.put(osfx.sound("oga/creatures/hurt_01", sweep(0.3, 900, 500)), B["CLANKS"][-1] + 0.1, 0.3)

# ---------------------------------------------------------------- 5. the crab attacks: claws snap, riser, 0.25 s break, GUTS
fx.put(osfx.lib("whoosh"), B["CRAB"] - 0.15, 0.5)
for k in range(5):
    fx.put(osfx.sound("oga/100-sfx/wooden_01", F.tick(1500, 1.0)), B["CRAB"] + 0.2 + k * 0.25, 0.4, 0.5)
fx.put(riser(B["BREAK"] - B["CRAB"], 200, 1800), B["CRAB"], 0.35)
fx.put(osfx.sound("oga/water-splash/splash_07", F.splash(1.2, 11)), B["HIT"], 0.9)
fx.put(osfx.sound("oga/bangs-fireworks/bang_05", impact(1.0)), B["HIT"], 0.6)
fx.put(impact(1.0), B["HIT"], 0.7)
fx.put(sub_drop(1.0), B["HIT"], 0.6)
for k in range(10):                                                          # guts splatting out
    fx.put(osfx.sound(f"oga/water-splash/slime_{k % 9 + 1:02d}", F.splash(0.3, 20 + k)), B["HIT"] + 0.05 + k * 0.09, 0.4, (k % 3 - 1) * 0.5)
for k in range(6):                                                           # the crab munches the decoy
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(260, 0.06, 1.5)), B["HIT"] + 2.2 + k * 0.3, 0.35, 0.4)

# ---------------------------------------------------------------- 6. regrow: GUTS 0 -> 100% (a rising tick per 10%)
fx.put(osfx.lib("whoosh"), B["REGROW"] - 0.15, 0.4)
for k in range(10):
    fx.put(CT.square(330 * 2 ** (k / 12 * 1.2), 0.08, 0.25), B["REGROW"] + 0.3 + k * 0.28, 0.16)
    fx.put(F.tick(2000 + 150 * k, 0.9), B["REGROW"] + 0.3 + k * 0.28, 0.25)
fx.put(osfx.sfxr("powerUp", seed=17), B["REGROW"] + 3.0, 0.35)

# ---------------------------------------------------------------- 7. CTA: the tenant is back
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.45)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.3)
fx.put(osfx.sound("oga/creatures/cute_05", blip(1100, 0.15)), B["CTA"] + 0.8, 0.35)

# ---------------------------------------------------------------- 8. tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 104, 104, "kbh")], gain=0.5, crescendo=(0.8, 0.8))
amb.x += (0.16 * F.drone(DUR, 52, seed=5) * seg(B["REWIND"] + 0.1, DUR, 0.1))[:, None]

CT.card_blips(fx, CARDS, gain=0.15)
for tc in (B["SLIDE"], B["REGROW"]):
    fx.put(impact(0.4), tc, 0.25)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["BREATHS"]), "breaths; DUR", DUR)
