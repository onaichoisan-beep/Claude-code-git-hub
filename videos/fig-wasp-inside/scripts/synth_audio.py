"""Sound for "There's a wasp in this fig": text cards + open-source sound only (NO narration — owner's rule),
STYLE_GUIDE.md section 6.

- SIGNATURE sound = the wasp herself. A tiny buzz while she flies (pitch rises as she nears the hole), a squeak + cloth
  rip per lost wing, a pollen POP per flower she touches (speeding up 2/s -> 8/s on the POLLINATED counter), silence on
  her death, then a fizz per tick as the fig digests her (WASP LEFT %), and a crunch per bite (seeds, not legs).
- Nonstop 8-bit bed, a blip on every card, whoosh + hit on every cut, a squeak on every speech bubble,
  tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 25.0
B = dict(FLOWERS=2.05, FLY=4.0, SQUEEZE=7.8, RIP1=9.9, RIP2=10.5, SLIDE=11.3, INSIDE=11.8, TRAP=13.8, BREAK=15.55,
         HIT=15.8, DIGEST=17.8, SEEDS=19.9, EAT=21.5, CTA=23.2, STOP=24.3, REWIND=24.7)

CARDS = [
    (0.10, 1.95, "THERE'S A *WASP*|IN THIS FIG"),
    (2.05, 3.90, "A FIG IS *FLOWERS*|GROWING INSIDE-OUT"),
    (4.05, 5.85, "ONLY ONE BUG|CAN REACH THEM"),
    (5.95, 7.65, "A TINY *FIG WASP*"),
    (7.90, 9.75, "SHE SQUEEZES IN|A TINY *HOLE*..."),
    (9.85, 11.70, "...SO TIGHT HER|*WINGS* RIP OFF"),
    (11.90, 13.70, "INSIDE, SHE|*POLLINATES* THEM"),
    (13.80, 15.50, "BUT WITH NO WINGS..."),
    (15.80, 17.65, "...SHE *DIES*|IN THERE"),
    (17.80, 19.75, "THE FIG *DIGESTS* HER|(AN ENZYME: FICIN)"),
    (19.90, 21.40, "THE CRUNCH? *SEEDS*,|NOT WASP LEGS"),
    (21.50, 23.10, "SO YOU MAY HAVE|EATEN A *WASP*"),
    (23.20, 24.30, "SEND THIS TO A|*FIG* LOVER"),
]
BUBBLES = [(0.5, "SHHH."), (10.75, "WORTH IT."), (16.3, "BYE."), (22.0, "CRUNCHY!"), (23.35, "SHHH.")]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402


def schedule(t0, t1, r0, r1, pw=2.0):
    out, t = [], t0
    while t < t1:
        out.append(round(t, 3))
        u = (t - t0) / (t1 - t0)
        t += 1 / (r0 + (r1 - r0) * u ** pw)
    return out


B["POLLEN"] = schedule(B["INSIDE"] + 0.5, B["BREAK"] - 0.1, 2.0, 8.0)
B["FLOWERTICK"] = schedule(B["FLOWERS"] + 0.1, B["FLY"] - 0.2, 4, 12, 1.2)
B["FIZZ"] = schedule(B["DIGEST"] + 0.2, B["SEEDS"] - 0.15, 3, 9, 1.5)
B["BITES"] = [B["EAT"] + 0.35, B["EAT"] + 0.9, B["EAT"] + 1.45]

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed (tightens with the story)
fx.x += CT.bed([
    S(0.0, B["FLY"], 100, 100, "kbo"),
    S(B["FLY"], B["SQUEEZE"], 118, 122, "kbh"),
    S(B["SQUEEZE"], B["INSIDE"], 122, 128, "kbha"),
    S(B["INSIDE"], B["BREAK"], 128, 150, "kbhsa"),
    S(B["HIT"], B["EAT"], 92, 92, "kbo"),
    S(B["EAT"], B["STOP"] + 0.2, 132, 132, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))
amb.x += (0.12 * F.drone(DUR, 55, seed=4))[:, None]

# ---------------------------------------------------------------- 0. the fig with a secret
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.35)
fx.put(braam(1.6, 55), 0.05, 0.3)
fx.put(osfx.sound("oga/creatures/cute_03", sweep(0.25, 900, 1400)), BUBBLES[0][0], 0.45)
fx.put(osfx.lib("glitch-1"), B["FLOWERS"], 0.18)
for k, t in enumerate(B["FLOWERTICK"]):                      # flowers bloom: a tick each (FLOWERS counter)
    fx.put(F.tick(2600 + 40 * (k % 8), 0.8), t, 0.28, (k % 3 - 1) * 0.4)
fx.put(osfx.sfxr("powerUp", seed=3), B["FLOWERS"] + 0.2, 0.25)

# ---------------------------------------------------------------- 1. the wasp flies in: her buzz (pitch rises toward the hole)
fx.put(osfx.lib("whoosh"), B["FLY"] - 0.15, 0.5)
fx.put(impact(0.5), B["FLY"], 0.3)
fl = B["SQUEEZE"] + 0.1
fx.put(CT.buzz(B["FLY"], fl, lambda t: 210 + 140 * ((t - B["FLY"]) / (fl - B["FLY"])) ** 2,
               lambda t: 0.5 + 0.4 * ((t - B["FLY"]) / (fl - B["FLY"])), voices=3, seed=5), B["FLY"], 0.32)
fx.put(osfx.sound("oga/creatures/bug_01", sweep(0.25, 1800, 2600)), B["FLY"] + 2.0, 0.35)
fx.put(osfx.sfxr("pickupCoin", seed=4), 5.95, 0.25)

# ---------------------------------------------------------------- 2. the squeeze: creaks, then two wing rips
fx.put(osfx.lib("whoosh-cinematic"), B["SQUEEZE"] - 0.2, 0.5)
for k in range(8):                                             # pushing: a wet creak per shove
    t = B["SQUEEZE"] + 0.35 + k * 0.28
    fx.put(osfx.sound(f"oga/water-splash/slime_{(k % 9) + 4:02d}", F.splash(0.2, k)), t, 0.3, (k % 2 - 0.5) * 0.4)
    fx.put(F.creak(0.25, 160 + 12 * k, seed=k), t, 0.25)
for t in (B["RIP1"], B["RIP2"]):
    fx.put(osfx.sound("oga/water-splash/slime_11", F.ice_crack(int(t * 10), 0.6)), t, 0.7)
    fx.put(osfx.sound("oga/creatures/hurt_02", sweep(0.2, 2000, 1200)), t + 0.03, 0.3)
    fx.put(impact(0.4), t, 0.35)
fx.put(osfx.sound("oga/creatures/cute_05", sweep(0.25, 1200, 1800)), BUBBLES[1][0], 0.4)
fx.put(osfx.sound("oga/water-splash/slime_02", thump(150, 0.15, 2)), B["SLIDE"], 0.6)

# ---------------------------------------------------------------- 3. SIGNATURE: pollen pops (POLLINATED counter)
fx.put(osfx.lib("whoosh-cinematic"), B["INSIDE"] - 0.2, 0.5)
for k, t in enumerate(B["POLLEN"]):
    fx.put(osfx.lib("pop"), t, 0.32, (k % 3 - 1) * 0.4)
    fx.put(F.tick(3000 + 60 * (k % 10), 0.8), t + 0.02, 0.22)
fx.put(riser(B["BREAK"] - B["TRAP"], 150, 1500), B["TRAP"], 0.28)
fx.put(osfx.sound("oga/creatures/misc_04", sweep(0.3, 700, 400)), B["TRAP"] + 0.1, 0.3)

# ---------------------------------------------------------------- 4. BREAK -> she dies (soft, no gore)
fx.put(impact(0.9), B["HIT"], 0.7)
fx.put(sub_drop(1.0), B["HIT"], 0.6)
fx.put(osfx.sound("oga/retro-synth/retro_die_02", CT.womp(330, 3, 0.2)), B["HIT"] + 0.3, 0.4)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(660, 1.4)), B["HIT"] + 0.45, 0.25)
fx.put(osfx.sound("oga/creatures/cute_07", sweep(0.3, 900, 500)), BUBBLES[2][0], 0.35)

# ---------------------------------------------------------------- 5. the fig digests her: fizz per tick (WASP LEFT %)
fx.put(osfx.lib("whoosh"), B["DIGEST"] - 0.15, 0.4)
for k, t in enumerate(B["FIZZ"]):
    fx.put(F.sizzle(0.18, seed=k), t, 0.35, (k % 3 - 1) * 0.3)
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.4, 600 + 80 * (k % 5))), t + 0.03, 0.18)
fx.put(osfx.sfxr("pickupCoin", seed=9), B["SEEDS"], 0.3)
for k in range(5):
    fx.put(F.tick(4200, 0.8), B["SEEDS"] + 0.2 + k * 0.22, 0.25)

# ---------------------------------------------------------------- 6. you eat the fig: crunch per bite
fx.put(osfx.lib("whoosh"), B["EAT"] - 0.15, 0.5)
fx.put(impact(0.5), B["EAT"], 0.3)
for k, t in enumerate(B["BITES"]):
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(300, 0.08, 1.5)), t, 0.55)
    fx.put(F.ice_crack(seed=30 + k, big=0.3), t + 0.02, 0.25)
fx.put(osfx.sound("oga/creatures/cute_02", sweep(0.25, 1000, 1500)), BUBBLES[3][0], 0.35)

# ---------------------------------------------------------------- 7. CTA, then tape-stop -> rewind -> frame 1
fx.put(osfx.lib("whoosh"), B["CTA"] - 0.15, 0.5)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.3)
fx.put(osfx.sound("oga/creatures/cute_03", sweep(0.25, 900, 1400)), BUBBLES[4][0], 0.35)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.4), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.05, DUR, 100, 100, "kbo")], gain=0.5, crescendo=(0.8, 0.8))

CT.card_blips(fx, CARDS, gain=0.15)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["POLLEN"]), "pollen pops;", len(B["FIZZ"]), "fizz; DUR", DUR)
