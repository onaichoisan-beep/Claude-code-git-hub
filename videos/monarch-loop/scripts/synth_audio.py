"""Sound for "Egg to butterfly to egg" (monarch life cycle loop): text cards + open-source sound only (NO narration),
STYLE_GUIDE.md section 6.

- SIGNATURE sound = the life inside. Egg wiggle ticks -> shell crack -> a CHOMP per bite that speeds up (3/s -> 9/s) and drops
  in pitch as the caterpillar gets 2,000x heavier -> a wet BLORP per soup bubble inside the chrysalis (speeding up while it
  dissolves) -> sparkles as the new body forms -> a soft wing whoosh per pump -> a little plip as the egg is laid.
- Nonstop 8-bit bed, a blip on every card, whoosh + hit on every cut, tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 25.0
B = dict(HATCH=2.05, CRACK=2.6, EAT=4.05, GROW=6.05, HANG=8.05, CHRYS=10.05, SPLIT=10.5, INSIDE=12.05, DISCS=14.05,
         BUILD=16.05, BREAK=17.95, HIT=18.2, PUMP=20.25, LAY=22.05, EGG=23.0, CTA=23.6, STOP=24.4, REWIND=24.75)

CARDS = [
    (0.10, 1.95, "THIS EGG WILL ONE DAY|TURN INTO *SOUP*"),
    (2.05, 3.95, "DAY 4: IT HATCHES|AND EATS ITS *SHELL*"),
    (4.05, 5.95, "THEN IT EATS|*NONSTOP*"),
    (6.05, 7.95, "AND GETS *2,000X*|HEAVIER"),
    (8.05, 9.95, "DAY 16: IT HANGS|UPSIDE DOWN..."),
    (10.05, 11.95, "...AND SHEDS INTO|A *CHRYSALIS*"),
    (12.05, 13.95, "INSIDE, IT DIGESTS|*ITSELF* INTO SOUP"),
    (14.05, 15.95, "A FEW TINY CELL GROUPS|*SURVIVE*"),
    (16.05, 17.90, "AND BUILD A|*NEW BODY*"),
    (18.25, 20.15, "DAY 26: A|*BUTTERFLY*"),
    (20.25, 21.95, "IT PUMPS ITS|*WINGS* OPEN"),
    (22.05, 23.50, "THEN LAYS|AN *EGG*..."),
    (23.60, 24.40, "AND IT ALL|STARTS *AGAIN*"),
]
BUBBLES = [(0.6, "SOON."), (2.9, "CRUNCH."), (12.3, "WAIT, WHAT?"), (19.0, "TA-DA!"), (22.6, "GOOD LUCK.")]

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


B["WIGGLE"] = schedule(0.3, B["CRACK"] - 0.05, 2, 7, 1.5)
B["CHOMPS"] = schedule(B["CRACK"] + 0.5, B["HANG"] - 0.15, 3, 9, 1.4)
B["BLORPS"] = schedule(B["INSIDE"] + 0.2, B["DISCS"] + 0.9, 3, 9, 1.5)
B["SPARKS"] = schedule(B["DISCS"] + 0.2, B["BREAK"] - 0.1, 2, 6, 1.2)
B["PUMPS"] = [round(B["PUMP"] + 0.15 + k * 0.42, 3) for k in range(4)]

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# ---------------------------------------------------------------- the nonstop 8-bit bed (tightens with the story)
fx.x += CT.bed([
    S(0.0, B["EAT"], 100, 100, "kbo"),
    S(B["EAT"], B["HANG"], 120, 132, "kbha"),
    S(B["HANG"], B["INSIDE"], 112, 112, "kbh"),
    S(B["INSIDE"], B["BREAK"], 116, 146, "kbhsa"),
    S(B["HIT"], B["LAY"], 128, 128, "kbhsal"),
    S(B["LAY"], B["STOP"] + 0.2, 128, 128, "kbhal"),
], gain=0.5, crescendo=(0.8, 1.2))
amb.x += (0.1 * F.drone(DUR, 65, seed=6))[:, None]

# ---------------------------------------------------------------- 0. the egg wiggles, cracks
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
fx.put(braam(1.4, 65), 0.05, 0.25)
for k, t in enumerate(B["WIGGLE"]):
    fx.put(F.tick(3200 + 200 * (k % 2), 0.8), t, 0.3, (k % 2 - 0.5) * 0.5)
fx.put(osfx.sound("oga/creatures/cute_04", sweep(0.25, 900, 1400)), BUBBLES[0][0], 0.4)
fx.put(F.ice_crack(seed=5, big=0.5), B["CRACK"], 0.6)
fx.put(osfx.sfxr("powerUp", seed=2), B["CRACK"] + 0.05, 0.3)
fx.put(osfx.sound("oga/creatures/cute_01", sweep(0.2, 1400, 2000)), BUBBLES[1][0], 0.35)

# ---------------------------------------------------------------- 1. SIGNATURE: chomps speed up and drop in pitch as it grows
fx.put(osfx.lib("whoosh"), B["EAT"] - 0.15, 0.4)
for k, t in enumerate(B["CHOMPS"]):
    u = (t - B["CRACK"]) / (B["HANG"] - B["CRACK"])
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(320, 0.08, 1.5)), t, 0.28 + 0.25 * u, (k % 3 - 1) * 0.3)
    fx.put(thump(420 - 300 * u, 0.06, 1.5), t, 0.3 + 0.3 * u)
fx.put(riser(B["HANG"] - B["GROW"], 120, 900), B["GROW"], 0.2)
fx.put(osfx.sfxr("pickupCoin", seed=6), B["GROW"], 0.3)

# ---------------------------------------------------------------- 2. hangs, splits into a chrysalis
fx.put(osfx.lib("whoosh-cinematic"), B["HANG"] - 0.2, 0.5)
fx.put(impact(0.5), B["HANG"], 0.3)
for k in range(6):
    fx.put(F.creak(0.2, 180 + 15 * k, seed=k), B["CHRYS"] + 0.05 + k * 0.08, 0.2)
fx.put(osfx.sound("oga/water-splash/slime_05", F.splash(0.4, 3)), B["SPLIT"], 0.6)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(880, 1.2)), B["SPLIT"] + 0.5, 0.3)

# ---------------------------------------------------------------- 3. the soup: a blorp per bubble, then sparkles as cells build
fx.put(osfx.lib("whoosh-cinematic"), B["INSIDE"] - 0.2, 0.5)
fx.put(osfx.sound("oga/creatures/misc_04", sweep(0.3, 600, 900)), BUBBLES[2][0], 0.35)
for k, t in enumerate(B["BLORPS"]):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.5, 400 + 70 * (k % 6))), t, 0.32, (k % 3 - 1) * 0.4)
    fx.put(F.tick(1800 + 40 * k, 0.6), t + 0.02, 0.16)
for k, t in enumerate(B["SPARKS"]):
    fx.put(F.sparkle(0.3, seed=k, lo=3000, hi=7000), t, 0.25, (k % 3 - 1) * 0.4)
fx.put(riser(B["BREAK"] - B["BUILD"], 150, 1600), B["BUILD"], 0.3)

# ---------------------------------------------------------------- 4. BREAK -> it bursts out
fx.put(impact(0.9), B["HIT"], 0.7)
fx.put(F.ice_crack(seed=9, big=1.0), B["HIT"], 0.5)
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["HIT"] + 0.1, 0.4)
fx.put(osfx.sound("oga/creatures/cute_06", sweep(0.25, 1000, 1700)), BUBBLES[3][0], 0.4)

# ---------------------------------------------------------------- 5. pumps its wings: a whoosh per pump
for k, t in enumerate(B["PUMPS"]):
    fx.put(osfx.lib("whoosh"), t, 0.25 + 0.05 * k)
    fx.put(thump(200, 0.1, 2), t, 0.25)

# ---------------------------------------------------------------- 6. flies to the leaf, lays the egg
fx.put(osfx.lib("whoosh"), B["LAY"] - 0.15, 0.45)
for k in range(10):
    fx.put(thump(260, 0.05, 1.5), B["LAY"] + 0.1 + k * 0.09, 0.12)
fx.put(osfx.sound("oga/creatures/cute_03", sweep(0.25, 900, 1300)), BUBBLES[4][0], 0.35)
fx.put(osfx.sound("oga/water-splash/slime_02", thump(500, 0.05, 2)), B["EGG"], 0.5)
fx.put(osfx.sound("oga/100-sfx/bell_02", bell(1320, 0.9)), B["EGG"] + 0.05, 0.25)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up(659.3)), B["CTA"] + 0.05, 0.3)

# ---------------------------------------------------------------- 7. tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.4), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.3)
fx.x += CT.bed([S(B["REWIND"] + 0.05, DUR, 100, 100, "kbo")], gain=0.5, crescendo=(0.8, 0.8))

CT.card_blips(fx, CARDS, gain=0.15)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print(len(B["CHOMPS"]), "chomps;", len(B["BLORPS"]), "blorps; DUR", DUR)
