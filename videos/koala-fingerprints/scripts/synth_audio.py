"""Sound for "The koala did it" (koala fingerprints): text cards + open-source sound only (NO narration).

SIGNATURE sound = the SCANNER: a sweep + rising beeps while each suspect's print is scanned; the MATCH % ticks with
the beeps (fast clicks), a low buzz for "no match", a big alarm stab for the koala's 99 %. Detective noir 8-bit bed,
camera-flash clicks at the crime scene, card blips, whooshes, tape-stop + rewind into frame 1.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 27.9
B = dict(SCENE=2.1, LID=4.2, RIDGE=6.3, LINEUP=8.4, BREAK=12.35, HIT=12.6, LOOK=14.6, MICRO=16.6, EVOLVE=18.6,
         GRIP=20.6, EUCA=22.6, WHO=24.6, STOP=26.6, REWIND=27.4)

CARDS = [
    (0.10, 2.00, "THESE PRINTS ARE|NOT *HUMAN*"),
    (2.10, 4.10, "CRIME SCENE:|THE *COOKIE JAR*"),
    (4.20, 6.20, "PRINTS FOUND|ON THE *LID*"),
    (6.30, 8.30, "LOOPS. WHORLS.|*HUMAN-LIKE*"),
    (8.40, 12.20, "TIME FOR A|*LINE-UP*"),
    (12.60, 14.50, "IT'S A *KOALA*"),
    (14.60, 16.50, "KOALA PRINTS|LOOK *HUMAN*"),
    (16.60, 18.50, "EVEN UNDER A|*MICROSCOPE*"),
    (18.60, 20.50, "THEY EVOLVED|*SEPARATELY*"),
    (20.60, 22.50, "PROBABLY FOR|*GRIPPING*"),
    (22.60, 24.50, "BUT KOALAS ONLY|EAT *EUCALYPTUS*"),
    (24.60, 26.50, "SO WHO ATE|THE *COOKIES*?"),
]
# the line-up scans: suspect k scanned from SCANS[k] for 0.85 s
B["SCANS"] = [round(B["LINEUP"] + 0.5 + k * 0.9, 3) for k in range(4)]
B["RESULTS"] = [12, 31, 8, 99]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

fx.x += CT.bed([
    S(0.0, B["SCENE"], 96, 96, "kbo"),
    S(B["SCENE"], B["LINEUP"], 108, 108, "kbhl"),
    S(B["LINEUP"], B["BREAK"], 118, 140, "kbhsa"),
    S(B["HIT"] + 0.1, B["EUCA"], 116, 116, "kbhal"),
    S(B["EUCA"], B["STOP"] + 0.2, 100, 100, "kbhs"),
], gain=0.46, crescendo=(0.8, 1.2))
amb.x += (0.12 * F.drone(DUR, 55, seed=8))[:, None]


def scan(t, result, g=1.0):
    fx.put(sweep(0.7, 400, 2400) * 0.5, t, 0.2 * g)
    for k in range(7):
        fx.put(CT.square(880 + 110 * k, 0.05, 0.25), t + k * 0.1, 0.12 * g)
        fx.put(F.tick(3000 + 100 * k, 0.8), t + k * 0.1 + 0.05, 0.18 * g)
    if result > 90:
        return
    fx.put(CT.square(110, 0.25, 0.5), t + 0.75, 0.2 * g)
    fx.put(osfx.sound("oga/scifi/beep_02", blip(220)), t + 0.75, 0.25 * g)


# 0. frame 1: MATCH 99 %: scan + stamp
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.3)
scan(0.15, 99, 0.7)
fx.put(osfx.sound("oga/100-sfx/slam_01", impact(0.6)), 0.95, 0.45)
# 1. crime scene: camera flashes
fx.put(osfx.lib("whoosh"), B["SCENE"] - 0.15, 0.45)
for k in range(3):
    fx.put(osfx.sound("oga/100-sfx/switch_01", F.tick(5000, 1.0)), B["SCENE"] + 0.5 + k * 0.45, 0.45)
    fx.put(noise_hit(0.12, 3000, 9000), B["SCENE"] + 0.52 + k * 0.45, 0.2)
fx.put(osfx.sound("oga/100-sfx/glass_03", F.glass_smash(5)), B["SCENE"] + 0.2, 0.3)
# 2. lid: brush dusting
fx.put(osfx.lib("whoosh"), B["LID"] - 0.15, 0.4)
for k in range(6):
    fx.put(noise_hit(0.18, 2000, 7000), B["LID"] + 0.4 + k * 0.22, 0.18, (k % 2) - 0.5)
fx.put(osfx.sound("oga/retro-synth/retro_coin_02", bell(1318, 0.5)), B["LID"] + 1.6, 0.3)
# 3. ridges: zoom
fx.put(osfx.lib("whoosh-cinematic"), B["RIDGE"] - 0.2, 0.45)
fx.put(osfx.sound("oga/scifi/terminal_03", blip(1600)), B["RIDGE"] + 0.6, 0.3)
fx.put(osfx.sound("oga/scifi/terminal_05", blip(1400)), B["RIDGE"] + 1.2, 0.3)
# 4. SIGNATURE: the line-up scans
fx.put(osfx.lib("whoosh"), B["LINEUP"] - 0.15, 0.4)
fx.put(osfx.sound("oga/100-sfx/door_close_02", thump(90, 0.2, 2)), B["LINEUP"] + 0.1, 0.4)
for k, st in enumerate(B["SCANS"]):
    scan(st, B["RESULTS"][k], 1.0 + 0.15 * k)
fx.put(riser(B["BREAK"] - B["SCANS"][3], 300, 2000), B["SCANS"][3], 0.3)
# 5. HIT: koala!
fx.put(impact(1.0), B["HIT"], 0.8)
fx.put(braam(1.5, 55), B["HIT"], 0.4)
for k in range(4):
    fx.put(CT.square(1318 if k % 2 else 988, 0.12, 0.5), B["HIT"] + 0.1 + k * 0.15, 0.12)
fx.put(osfx.sound("oga/creatures/cute_09", blip(900)), B["HIT"] + 0.8, 0.45)
# 6-7. compare + microscope
fx.put(osfx.lib("whoosh"), B["LOOK"] - 0.15, 0.45)
fx.put(osfx.sound("oga/retro-synth/synth_misc_04", blip(1000)), B["LOOK"] + 0.6, 0.3)
fx.put(osfx.lib("whoosh-cinematic"), B["MICRO"] - 0.2, 0.45)
for k in range(5):
    fx.put(F.tick(2600 - 200 * k, 0.9), B["MICRO"] + 0.3 + k * 0.12, 0.25)
fx.put(osfx.sound("oga/scifi/beep_03", blip(1700)), B["MICRO"] + 1.1, 0.3)
# 8. evolved separately: two branches
fx.put(osfx.lib("whoosh"), B["EVOLVE"] - 0.15, 0.4)
fx.put(osfx.sound("oga/retro-synth/power_up_05", F.harp_up(392.0)), B["EVOLVE"] + 0.4, 0.3)
# 9. gripping: branch creak + leaves
fx.put(osfx.lib("whoosh"), B["GRIP"] - 0.15, 0.4)
fx.put(F.creak(0.6, 120, seed=7), B["GRIP"] + 0.4, 0.4)
fx.put(noise_hit(0.4, 2000, 6000), B["GRIP"] + 0.7, 0.2)
# 10. eucalyptus: munching
fx.put(osfx.lib("whoosh"), B["EUCA"] - 0.15, 0.4)
for k in range(8):
    fx.put(osfx.sound(f"oga/creatures/eat_0{k % 4 + 1}", thump(300, 0.08, 1.5)), B["EUCA"] + 0.3 + k * 0.22, 0.35)
# 11. who? suspense sting + gulp
fx.put(osfx.lib("whoosh"), B["WHO"] - 0.15, 0.45)
fx.put(CT.womp(392, 3, 0.25), B["WHO"] + 0.5, 0.18)
fx.put(osfx.sound("oga/creatures/burp_02", thump(140, 0.2, 1.5)), B["WHO"] + 1.4, 0.4)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.35)
fx.x += CT.bed([S(B["REWIND"] + 0.1, DUR, 96, 96, "kbo")], gain=0.46, crescendo=(0.8, 0.8))
CT.card_blips(fx, CARDS, gain=0.14)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR)
