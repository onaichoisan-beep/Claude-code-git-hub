"""Sound for "Why Doesn't Your Stomach Digest Itself?" — no narration, text cards + sound (STYLE_GUIDE.md section 6).

Signature sound: the ACID. A bubbling boil that never stops, its bubble rate following the acid's activity on screen
(busy while it digests the steak, a tink every time an acid ion bounces off the mucus shield, a pop every time
bicarbonate neutralises one, a hissing surge when the shield cracks). On top: a steak plop + sizzle, a zoom riser with
counter ticks, slime oozing, cells flaking off, a glass crack + alarm, the corkscrew bacterium's drill, pills rattling,
a "wrong" buzzer for the spicy-food myth, a power-up shield. Tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 34.4
B = dict(MEAT=2.3, ASK=4.5, ZOOM=6.7, MUCUS=8.9, BICARB=11.1, NEUT=13.3, RENEW=15.5, BREAK=17.65, HIT=17.9, ULCER=20.3,
         PYLORI=22.5, PAIN=24.6, SPICY=26.7, TWIST=28.8, CTA=30.9, STOP=33.0, REWIND=33.8)

CARDS = [
    (0.10, 2.20, "YOUR STOMACH|IS FULL OF *ACID*"),
    (2.30, 4.40, "STRONG ENOUGH|TO DIGEST *MEAT*"),
    (4.50, 6.60, "SO WHY DOESN'T|IT EAT *ITSELF*?"),
    (6.70, 8.80, "ZOOM INTO|THE *WALL*"),
    (8.90, 11.00, "A SHIELD OF|*MUCUS*"),
    (11.10, 13.20, "PACKED WITH|*BICARBONATE*"),
    (13.30, 15.40, "IT *NEUTRALISES*|THE ACID"),
    (15.50, 17.60, "AND THE LINING|*RENEWS* ITSELF"),
    (17.90, 20.20, "BUT IF THE|SHIELD *FAILS*..."),
    (20.30, 22.40, "YOU GET AN|*ULCER*"),
    (22.50, 24.50, "TOP CAUSE:|*H. PYLORI*"),
    (24.60, 26.60, "OR TOO MANY|*PAINKILLERS*"),
    (26.70, 28.70, "SPICY FOOD?|*NOT* THE CAUSE"),
    (28.80, 30.80, "NOT UNBREAKABLE|JUST *DEFENDED*"),
    (30.90, 32.80, "TAG A *CHILLI*|LOVER"),
]


def every(a, b, gap):
    out, t = [], a
    while t < b - 0.05:
        out.append(round(t, 3))
        t += gap
    return out


DEFL = every(B["MUCUS"] + 0.5, B["NEUT"], 0.3)            # acid ions bouncing off the mucus
RISE = every(B["BICARB"] + 0.2, B["RENEW"], 0.35)         # bicarbonate leaving the cells
NEUT = every(B["NEUT"] + 0.15, B["RENEW"] + 1.6, 0.24)    # ion + bicarbonate -> pop
FLAKE = [round(B["RENEW"] + 0.4 + k * 0.5, 3) for k in range(3)]
PILLS = [round(B["PAIN"] + 0.3 + k * 0.13, 3) for k in range(12)]
B.update(DEFL=DEFL, RISE=RISE, NEUTS=NEUT, FLAKE=FLAKE, PILLS=PILLS)

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec


def alarm(d=1.6):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = np.where((tt * 4).astype(int) % 2 == 0, 880.0, 660.0)
    ph = np.cumsum(f) / SR
    return (np.sign(np.sin(2 * np.pi * ph)) * 0.6) * np.minimum(1, (d - tt) / 0.1)


# ---------------------------------------------------------------- the 8-bit bed
fx.x += CT.bed([
    S(0.0, B["ZOOM"], 120, 120, "kbha"),
    S(B["ZOOM"], B["MUCUS"], 120, 150, "kbh"),
    S(B["MUCUS"], B["NEUT"], 124, 124, "kbhs"),
    S(B["NEUT"], B["BREAK"], 128, 128, "kbhsal"),
    S(B["HIT"] + 0.1, B["PYLORI"], 100, 100, "kbo"),
    S(B["PYLORI"], B["TWIST"], 130, 136, "kbhsa"),
    S(B["TWIST"], B["STOP"] + 0.2, 124, 124, "kbhsal"),
], gain=0.4, crescendo=(0.8, 1.15))
amb.x += (0.18 * F.drone(DUR, 49, seed=11))[:, None]

# ---------------------------------------------------------------- SIGNATURE: the acid bubbling (rate follows the acid)
seg_rates = [(0.0, B["MEAT"], 14), (B["MEAT"], B["ZOOM"], 34), (B["ZOOM"], B["MUCUS"], 10), (B["MUCUS"], B["HIT"], 12),
             (B["HIT"], B["ULCER"] + 1.0, 40), (B["ULCER"] + 1.0, B["STOP"], 14)]
for a, b, r in seg_rates:
    fx.put(F.boil(b - a, rate=r, seed=int(a * 10) + 1), a, 0.22 if r < 20 else 0.32)
for k in range(10):
    fx.put(osfx.sound("oga/water-splash/bubble_0" + str(1 + k % 3), F.bubble_(0.4, 500)), 0.3 + k * 0.62, 0.18, (k % 3 - 1) * 0.5)

# ---------------------------------------------------------------- 1. the steak drops in and dissolves
fx.put(osfx.lib("whoosh"), B["MEAT"] - 0.2, 0.3)
fx.put(osfx.sound("oga/water-splash/splash_03", F.splash(0.8)), B["MEAT"] + 0.25, 0.6)
fx.put(F.sizzle(1.9, seed=4), B["MEAT"] + 0.4, 0.35)
fx.put(osfx.sound("oga/water-splash/slime_02", F.bubble_(0.4, 300)), B["MEAT"] + 1.2, 0.35)
for k in range(8):
    fx.put(CT.square(900 - k * 60, 0.03, 0.5), B["MEAT"] + 0.5 + k * 0.2, 0.11)       # MEAT % ticking down
fx.put(osfx.sound("oga/creatures/burp_01", blip(200)), B["MEAT"] + 1.95, 0.35)
# ---------------------------------------------------------------- 2. the question
fx.put(osfx.sound("oga/scifi/beep_02", blip(900)), B["ASK"] + 0.3, 0.3)
fx.put(CT.tone_glide(500, 900, 0.25, "square", 0.5, 0.3), B["ASK"] + 0.9, 0.3)
fx.put(osfx.sound("oga/creatures/ooh", blip(500)), B["ASK"] + 1.3, 0.3)
# ---------------------------------------------------------------- 3. the zoom: riser + a tick per zoom step
fx.put(riser(B["MUCUS"] - B["ZOOM"], 150, 2400), B["ZOOM"], 0.3)
fx.put(osfx.lib("whoosh-cinematic"), B["ZOOM"] + 0.1, 0.4)
for k in range(14):
    fx.put(F.tick(2000 + k * 120), B["ZOOM"] + 0.15 + k * 0.14, 0.32)
fx.put(osfx.sound("oga/scifi/teleport_01", sweep(0.4, 400, 2000)), B["MUCUS"] - 0.3, 0.35)
# ---------------------------------------------------------------- 4. the mucus shield: slime ooze + a tink per bounce
for k in range(4):
    fx.put(osfx.sound("oga/water-splash/slime_0" + str(3 + k), F.bubble_(0.4, 250)), B["MUCUS"] + 0.05 + k * 0.18, 0.4, (k % 2) - 0.5)
for k, t in enumerate(DEFL):
    fx.put(osfx.sound("oga/100-sfx/glass_0" + str(1 + k % 5), bell(2400, 0.5)), t, 0.16, (k % 3 - 1) * 0.6)
    fx.put(CT.square(1800 + (k % 4) * 200, 0.03, 0.5), t, 0.08)
# ---------------------------------------------------------------- 5. bicarbonate rises, 6. neutralises (pop + sparkle)
for k, t in enumerate(RISE):
    fx.put(CT.tone_glide(400, 800, 0.12, "square", 0.25, 0.4), t, 0.1, (k % 2) - 0.5)
for k, t in enumerate(NEUT):
    fx.put(osfx.lib("pop"), t, 0.35, (k % 3 - 1) * 0.5)
    fx.put(bell(1568 + (k % 3) * 200, 0.5), t + 0.03, 0.08)
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up()), B["NEUT"] + 0.1, 0.3)
# ---------------------------------------------------------------- 7. renewal: three old cells wave bye, new ones slide in
for t in FLAKE:
    fx.put(osfx.sound("oga/creatures/cute_0" + str(4 + FLAKE.index(t)), blip(1200)), t, 0.35)
    fx.put(sweep(0.25, 600, 1500) * 0.5, t + 0.1, 0.2)
    fx.put(osfx.sound("oga/100-sfx/plop_01", F.bubble_(0.3, 400)), t + 0.3, 0.3)
# ---------------------------------------------------------------- 8. the shield fails: break -> CRACK, acid floods, alarm
fx.put(riser(B["BREAK"] - B["RENEW"] - 0.2, 200, 2000), B["RENEW"] + 0.2, 0.2)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_glass_02", F.glass_smash()), B["HIT"], 0.7)
fx.put(F.ice_crack(seed=5, big=1.2), B["HIT"], 0.5)
fx.put(impact(1.0), B["HIT"], 0.6)
fx.put(braam(2.0, 44), B["HIT"], 0.4)
fx.put(F.sizzle(1.8, seed=8), B["HIT"] + 0.2, 0.45)
fx.put(alarm(2.0), B["HIT"] + 0.3, 0.12)
fx.put(osfx.sound("oga/creatures/scream_02", blip(700)), B["HIT"] + 0.5, 0.3)
# ---------------------------------------------------------------- 9. the ulcer: ouch
fx.put(osfx.sound("oga/creatures/hurt_01", blip(300)), B["ULCER"] + 0.3, 0.5)
fx.put(taiko(60), B["ULCER"] + 0.3, 0.5)
fx.put(osfx.sound("oga/creatures/hurt_03", blip(300)), B["ULCER"] + 1.3, 0.35)
fx.put(CT.womp(330, 4, 0.28), B["ULCER"] + 0.7, 0.18)
# ---------------------------------------------------------------- 10. H. pylori drills in (corkscrew whirr)
d = B["PAIN"] - B["PYLORI"] - 0.4
n = int(d * SR)
tt = np.arange(n) / SR
drill = np.sign(np.sin(2 * np.pi * (180 + 60 * np.sin(2 * np.pi * 6 * tt)) * tt)) * 0.4 * np.minimum(1, tt / 0.1) * np.minimum(1, (d - tt) / 0.1)
fx.put(drill, B["PYLORI"] + 0.3, 0.14)
fx.put(osfx.sound("oga/creatures/bug_01", blip(800)), B["PYLORI"] + 0.2, 0.4)
fx.put(osfx.sound("oga/creatures/troll_01", blip(400)), B["PYLORI"] + 1.3, 0.3)          # evil giggle
fx.put(osfx.sound("oga/water-splash/slime_08", F.bubble_(0.4, 250)), B["PYLORI"] + 0.9, 0.3)
# ---------------------------------------------------------------- 11. painkillers rattle in
fx.put(osfx.sound("oga/100-sfx/key_open_01", F.tick(1500)), B["PAIN"] + 0.05, 0.4)       # the bottle cap
for k, t in enumerate(PILLS):
    fx.put(F.tick(3000 + (k % 5) * 300, 0.8), t, 0.4, (k % 3 - 1) * 0.5)
    fx.put(osfx.sound("oga/water-splash/bubble_0" + str(1 + k % 3), F.bubble_(0.2, 700)), t + 0.25, 0.15)
# ---------------------------------------------------------------- 12. the spicy myth: boing, wrong buzzer
fx.put(osfx.sound("oga/100-sfx/spring_02", F.harp_up()), B["SPICY"] + 0.2, 0.45)
fx.put(osfx.sound("oga/100-sfx/spring_04", F.harp_up()), B["SPICY"] + 0.6, 0.35)
fx.put(CT.womp(), B["SPICY"] + 1.0, 0.22)
fx.put(osfx.sound("oga/creatures/cute_02", blip(1000)), B["SPICY"] + 1.4, 0.3)
# ---------------------------------------------------------------- 13. defended: shield power-up, CTA
fx.put(osfx.sound("oga/retro-synth/power_up_05", F.harp_up()), B["TWIST"] + 0.2, 0.45)
fx.put(osfx.sound("oga/scifi/teleport_02", riser(0.6, 300, 1500)), B["TWIST"] + 0.25, 0.3)
for i, f0 in enumerate([523.25, 659.25, 783.99, 1046.5]):
    fx.put(bell(f0, 1.0), B["TWIST"] + 0.6 + i * 0.08, 0.2)
fx.put(F.sparkle(1.2, seed=9), B["TWIST"] + 0.5, 0.25)
fx.put(osfx.sound("oga/100-sfx/spring_05", F.harp_up()), B["CTA"] + 0.3, 0.35)
fx.put(osfx.lib("chime"), B["CTA"] + 0.8, 0.3)
fx.put(F.sizzle(0.6, seed=12), B["CTA"] + 1.1, 0.2)

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.14)
for tc in (B["ZOOM"], B["MUCUS"], B["ULCER"], B["PYLORI"], B["PAIN"], B["SPICY"], B["TWIST"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.4)
    fx.put(impact(0.4), tc, 0.25)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 120, 120, "kbh")], gain=0.4, crescendo=(0.8, 0.8))
fx.put(F.boil(DUR - B["REWIND"] - 0.1, rate=14, seed=99), B["REWIND"] + 0.1, 0.22)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=4.5)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
