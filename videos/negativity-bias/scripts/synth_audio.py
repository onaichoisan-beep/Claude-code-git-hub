"""Sound for "Your Brain Doesn't Care If You're Happy" (negativity bias) — no narration, text cards + sound
(STYLE_GUIDE.md section 6).

Signature sound: the brain's THREAT RADAR ping. It never stops: calm at 2 pings/s, racing at 4-6/s when one bad comment
lands, when it imagines the worst and when the tiger appears, then slowing to 1.5/s at the calm ending. The counter
on screen counts the same pings (SCANS 0001...). Lots of hits on top: comment pops, cringe-replay thuds, a siren, rain,
thought-bubble pops, a scale slam, a roar, a wind blow, sparkles. Tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 33.4
B = dict(SURV=4.1, MEM=6.4, FEED=10.7, BAD=12.7, RUIN=14.7, WORST=16.7, BREAK=18.95, HIT=19.2, CAVE=22.0, PRED=24.0,
         SAME=25.7, CALM=27.8, CTA=30.0, STOP=32.0, REWIND=32.8)

# max 16 characters a line, max 2 lines (safe zone, STYLE_GUIDE.md section 8)
CARDS = [
    (0.10, 2.10, "YOUR *BRAIN*|DOESN'T CARE"),
    (2.20, 4.00, "IF YOU'RE|*HAPPY*"),
    (4.10, 6.30, "JOB #1:|STAY *ALIVE*"),
    (6.40, 8.60, "YOU REPLAY|THE *CRINGE*"),
    (8.70, 10.60, "NOT THE|*COMPLIMENTS*"),
    (10.70, 12.60, "99 NICE|COMMENTS..."),
    (12.70, 14.60, "*1* BAD ONE"),
    (14.70, 16.60, "RUINS YOUR|*WHOLE DAY*"),
    (16.70, 18.90, "ALWAYS READY|FOR THE *WORST*"),
    (19.30, 21.90, "IT'S CALLED|*NEGATIVITY BIAS*"),
    (22.00, 23.90, "MISS ONE|*PREDATOR*..."),
    (24.00, 25.60, "AND YOU'RE|*LUNCH*"),
    (25.70, 27.70, "SAME ALARM|FOR A *COMMENT*"),
    (27.80, 29.90, "NOT EVERY|*THOUGHT* MATTERS"),
    (30.00, 31.90, "SEND TO AN|*OVERTHINKER*"),
]


def ping_times():
    """the radar pings (shared with the picture through BEATS.PINGS)"""
    secs = [(0.2, B["BAD"], 2.0), (B["BAD"], B["BREAK"], 4.0), (B["HIT"] + 0.1, B["PRED"], 2.0),
            (B["PRED"], B["SAME"], 6.0), (B["SAME"], B["CALM"], 4.0), (B["CALM"], B["STOP"], 1.5)]
    out = []
    for a, b, r in secs:
        t = a
        while t < b - 0.05:
            out.append(round(t, 3))
            t += 1.0 / r
    return out


PINGS = ping_times()
B["PINGS"] = PINGS
REPLAYS = [round(B["MEM"] + 0.5 + k * 0.62, 3) for k in range(7)]          # the cringe clip, on repeat
B["REPLAYS"] = REPLAYS
COMMENTS = [round(B["FEED"] + 0.15 + 1.85 * (k / 22) ** 0.8, 3) for k in range(23)]   # 23 visible, the counter says 99
B["COMMENTS"] = COMMENTS
WORSTS = [round(B["WORST"] + 0.2 + k * 0.42, 3) for k in range(5)]          # thought bubbles of disasters
B["WORSTS"] = WORSTS

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec


def siren(d=1.6, lo=700.0, hi=1100.0, rate=4.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = lo + (hi - lo) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rate / 2 * tt)))
    ph = np.cumsum(f) / SR
    x = np.sign(np.sin(2 * np.pi * ph)) * 0.5 + 0.5 * np.sin(2 * np.pi * ph * 2)
    return x * np.minimum(1, tt / 0.01) * np.minimum(1, (d - tt) / 0.1)


# ---------------------------------------------------------------- the 8-bit bed (never stops; drops for the reveal)
fx.x += CT.bed([
    S(0.0, B["BAD"], 122, 122, "kbha"),
    S(B["BAD"], B["RUIN"], 128, 136, "kbhs"),
    S(B["RUIN"], B["WORST"], 104, 100, "kbo"),
    S(B["WORST"], B["BREAK"], 132, 150, "kbhsa"),
    S(B["HIT"] + 0.1, B["CAVE"], 126, 126, "kbhsal"),
    S(B["CAVE"], B["PRED"], 112, 120, "kbh"),
    S(B["PRED"], B["CALM"], 140, 146, "kbhsa"),
    S(B["CALM"], B["STOP"] + 0.2, 118, 118, "kbhl"),
], gain=0.4, crescendo=(0.8, 1.15))
amb.x += (0.2 * F.drone(DUR, 55, seed=6))[:, None]

# ---------------------------------------------------------------- SIGNATURE: the threat radar
for t in PINGS:
    alarm = B["BAD"] <= t < B["BREAK"] or B["PRED"] <= t < B["CALM"]
    f = 1900 if alarm else 1400 if t < B["CALM"] else 1150
    fx.put(CT.ping(f, 0.3), t, 0.16 if alarm else 0.12, 0.25)

# ---------------------------------------------------------------- 1. hook: a happy heart floats in, NOPE.
fx.put(F.sparkle(0.9, seed=3), 0.1, 0.25)
fx.put(osfx.sound("oga/creatures/cute_01", blip(1200)), 0.5, 0.35)
fx.put(osfx.sound("oga/100-sfx/hit_01", impact(0.5)), 1.55, 0.6)
fx.put(osfx.sound("oga/scifi/terminal_03", CT.womp()), 1.65, 0.35)
fx.put(sweep(0.35, 1800, 300) * 0.5, 1.6, 0.3)                    # the heart flies off
fx.put(osfx.sound("oga/scifi/beep_02", blip(900)), B["SURV"] - 1.5, 0.35)
# ---------------------------------------------------------------- 2. job #1: the helmet clanks on, the radar starts
fx.put(osfx.sound("oga/100-sfx/metal_02", impact(0.4)), B["SURV"] + 0.35, 0.55)
fx.put(osfx.sound("oga/retro-synth/power_up_02", F.harp_up()), B["SURV"] + 0.5, 0.35)
fx.put(osfx.sound("oga/scifi/teleport_01", riser(0.6, 300, 900)), B["SURV"] + 0.9, 0.3)
for k in range(3):
    fx.put(osfx.sound("oga/scifi/retro_beep_01", blip(1500)), B["SURV"] + 1.2 + k * 0.25, 0.25)

# ---------------------------------------------------------------- 3. the cringe on repeat: whoosh, trip, thud, rewind
for k, t in enumerate(REPLAYS):
    fx.put(osfx.lib("whoosh"), t - 0.12, 0.25)
    fx.put(osfx.sound("oga/100-sfx/slam_0" + str(1 + k % 4), thump(70)), t + 0.12, 0.6, (k % 2) - 0.5)
    fx.put(rewind(0.22), t + 0.36, 0.3)
    fx.put(F.tick(2400 + k * 140), t + 0.12, 0.35)
fx.put(osfx.sound("oga/creatures/eat_01", F.tick(800)), B["MEM"] + 0.2, 0.3)       # popcorn
fx.put(osfx.sound("oga/creatures/eat_02", F.tick(800)), B["MEM"] + 2.6, 0.3)
fx.put(osfx.sound("oga/retro-synth/synth_misc_03", sweep(0.3, 1200, 300)), B["MEM"] + 2.4, 0.35)    # the compliment note shrinks away
fx.put(osfx.sound("oga/creatures/ooh", blip(500)), B["MEM"] + 3.1, 0.3)

# ---------------------------------------------------------------- 4. the feed: a pop per comment, then MID.
for k, t in enumerate(COMMENTS):
    fx.put(CT.square(880 * 2 ** ((k % 12) / 12), 0.04, 0.25), t, 0.18, (k % 3 - 1) * 0.4)
    fx.put(osfx.sound("oga/100-sfx/plop_0" + str(1 + k % 2), click()), t, 0.22)
fx.put(osfx.sound("oga/retro-synth/retro_coin_01", bell(1318, 0.5)), B["BAD"] - 0.25, 0.3)   # 99!
fx.put(osfx.sound("scratch_001", sweep(0.3, 3000, 400)), B["BAD"], 0.6)                       # record stops
fx.put(osfx.sound("oga/scifi/terminal_05", CT.womp()), B["BAD"] + 0.15, 0.4)
fx.put(sub_drop(1.0), B["BAD"], 0.6)
fx.put(siren(1.8), B["BAD"] + 0.35, 0.16)
fx.put(impact(0.6), B["BAD"] + 0.05, 0.45)
fx.put(osfx.sound("oga/creatures/hurt_02", blip(300)), B["BAD"] + 1.1, 0.3)
# ---------------------------------------------------------------- 5. ruins the day: rain + thunder + mood ticks down
fx.put(fade_out(osfx.sound("oga/water-splash/loop_rain", F.sea(2.0)), 0.4), B["RUIN"], 0.35)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_thunder", F.rumble(1.5)), B["RUIN"] + 0.2, 0.6)
fx.put(CT.womp(330, 4, 0.3), B["RUIN"] + 0.6, 0.18)
for k in range(10):
    fx.put(CT.square(1200 - k * 70, 0.03, 0.5), B["RUIN"] + 0.1 + k * 0.17, 0.12)          # MOOD % ticking down
fx.put(osfx.sound("oga/creatures/cough_01", blip(300)), B["RUIN"] + 1.5, 0.15)

# ---------------------------------------------------------------- 6. expecting the worst: a pop + sting per disaster
stings = ["oga/100-sfx-2/sfx100v2_thunder", "oga/scifi/terminal_07", "oga/100-sfx/glass_01", "oga/retro-synth/retro_die_01", "oga/creatures/monster_02"]
for k, t in enumerate(WORSTS):
    fx.put(osfx.lib("pop"), t, 0.45, (k % 3 - 1) * 0.5)
    fx.put(osfx.sound(stings[k], impact(0.3)), t + 0.08, 0.28, (k % 2) - 0.5)
fx.put(riser(B["BREAK"] - B["WORST"], 200, 2200), B["WORST"], 0.25)
for tt_, sig in drum_roll(B["WORST"] + 0.3, B["BREAK"], 0.3, 0.07):
    fx.put(sig, tt_, 0.35)

# ---------------------------------------------------------------- 7. the reveal: break -> HIT, the scale slams down
fx.put(braam(2.2, 46), B["HIT"], 0.45)
fx.put(impact(1.0), B["HIT"], 0.65)
fx.put(osfx.sound("oga/100-sfx/slam_05", thump(55)), B["HIT"] + 0.05, 0.6)
fx.put(osfx.lib("whoosh-cinematic"), B["HIT"] - 0.25, 0.4)
for k in range(5):                                                                      # good hearts drop onto the scale
    fx.put(osfx.sound("oga/100-sfx/glass_0" + str(1 + k), blip(1500)), B["HIT"] + 0.6 + k * 0.22, 0.3, 0.4)
fx.put(osfx.sound("oga/100-sfx-2/sfx100v2_stones_01", thump(50)), B["HIT"] + 1.9, 0.55, -0.4)           # one bad rock outweighs them
fx.put(osfx.sound("oga/100-sfx/metal_03", impact(0.3)), B["HIT"] + 2.0, 0.3)

# ---------------------------------------------------------------- 8. 50,000 BC: berries, a rustle, the tiger, run
fx.put(F.crickets(B["SAME"] - B["CAVE"], seed=8), B["CAVE"], 0.2)
fx.put(F.wind(B["SAME"] - B["CAVE"], 300, 700, 0.3, seed=9), B["CAVE"], 0.15)
for k in range(3):
    fx.put(osfx.sound("oga/creatures/eat_0" + str(1 + k % 3), F.tick(900)), B["CAVE"] + 0.3 + k * 0.45, 0.3)
for k in range(4):
    fx.put(noise_hit(0.25, 800, 4000) * 0.6, B["CAVE"] + 1.0 + k * 0.22, 0.35, 0.5)      # the bush rustles
fx.put(osfx.sound("oga/creatures/roar_01", roar()), B["PRED"], 0.75)
fx.put(taiko(65), B["PRED"], 0.6)
fx.put(osfx.sound("oga/creatures/scream_01", blip(600)), B["PRED"] + 0.25, 0.35)
for k in range(6):
    fx.put(osfx.sound("footstep_grass_00" + str(k % 5), thump(90, 0.15)), B["PRED"] + 0.5 + k * 0.17, 0.45, (k % 2) - 0.5)
fx.put(osfx.lib("whoosh"), B["PRED"] + 1.3, 0.35)

# ---------------------------------------------------------------- 9. same alarm: roar = "MID."
fx.put(osfx.sound("oga/creatures/roar_02", roar(0.8)), B["SAME"] + 0.3, 0.35, -0.5)
fx.put(siren(0.8), B["SAME"] + 0.3, 0.13, -0.3)
fx.put(osfx.lib("notification"), B["SAME"] + 1.1, 0.4, 0.5)
fx.put(siren(0.8), B["SAME"] + 1.1, 0.13, 0.3)
fx.put(osfx.sound("oga/retro-synth/synth_beep_01", blip(1000)), B["SAME"] + 0.7, 0.3)   # "="

# ---------------------------------------------------------------- 10. calm: blow the cloud away, mood refills, CTA
fx.put(F.wind(1.2, 600, 1400, 0.6, seed=12), B["CALM"] + 0.3, 0.45)
fx.put(osfx.lib("whoosh-cinematic"), B["CALM"] + 0.4, 0.4)
fx.put(F.poof(5), B["CALM"] + 1.2, 0.5)
fx.put(F.sparkle(1.4, seed=7), B["CALM"] + 1.3, 0.3)
fx.put(F.harp_up(), B["CALM"] + 1.4, 0.35)
for k in range(10):
    fx.put(CT.square(700 + k * 80, 0.03, 0.5), B["CALM"] + 1.3 + k * 0.08, 0.12)          # MOOD refilling
fx.put(osfx.sound("oga/retro-synth/power_up_04", bell(1046, 0.8)), B["CTA"] + 0.1, 0.4)
fx.put(osfx.lib("chime"), B["CTA"] + 0.6, 0.3)
fx.put(osfx.sound("oga/creatures/cute_03", blip(1200)), B["CTA"] + 1.0, 0.3)

# ---------------------------------------------------------------- every change
CT.card_blips(fx, CARDS, gain=0.14)
for tc in (B["MEM"], B["FEED"], B["WORST"], B["CAVE"], B["SAME"], B["CALM"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.45)
    fx.put(impact(0.4), tc, 0.25)

# ---------------------------------------------------------------- tape-stop -> rewind -> frame 1
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 122, 122, "kbh")], gain=0.4, crescendo=(0.8, 0.8))
fx.put(F.sparkle(0.5, seed=3), B["REWIND"] + 0.15, 0.2)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=4.5)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
