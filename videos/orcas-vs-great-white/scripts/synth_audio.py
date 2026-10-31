"""Sound for "Orcas vs great white sharks" — sound follows the story (STYLE_GUIDE.md section 6):

- SIGNATURE: sonar pings. They start far apart when the orcas are 500 m away and speed up (0.7/s -> 6.7/s, the same PINGS
  list the picture uses) as the DISTANCE counter drops, rising in pitch, until the FLIP; then the shark's heartbeat slows
  while it is frozen, the 0.25 s break, and the hit (a white flash, no gore).
- a deep underwater drone + a nonstop 8-bit bed whose tempo climbs with the chase (96 -> 168 BPM); orca calls; a blip on
  every card; ticks on the SIGHTINGS counter; whoosh + hit on every cut; a crescendo; tape-stop + rewind into frame 1.

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
B = dict(PINGS=3.0, ORCAS=5.5, FLIP=9.5, FREEZE=11.5, BREAK=14.25, CHOMP=14.5, MAP=18.5, APEX=23.5, CTA=26.0,
         STOP=28.5, REWIND=29.3)

CARDS = [
    (0.10, 2.90, "THE GREAT WHITE: THE|OCEAN'S *TOP PREDATOR*..."),
    (3.10, 5.40, "...UNTIL IT HEARS|*THIS*"),
    (5.60, 7.50, "TWO ORCAS: *PORT*|AND *STARBOARD*"),
    (7.60, 9.40, "EACH ONE IS NEARLY|*TWICE ITS SIZE*"),
    (9.60, 11.40, "THEY FLIP THE SHARK|*UPSIDE DOWN*"),
    (11.50, 14.20, "UPSIDE DOWN, A SHARK|GOES *LIMP*"),
    (14.70, 16.50, "THEY TAKE ONLY|THE *LIVER*"),
    (16.60, 18.40, "IT'S PACKED WITH|*ENERGY-RICH OIL*"),
    (18.70, 21.00, "THE OTHER SHARKS|*FLED* THE BAY"),
    (21.10, 23.40, "SOME STAYED AWAY|FOR *MONTHS*"),
    (23.70, 25.90, "THE REAL APEX|PREDATOR: *ORCAS*"),
    (26.10, 28.40, "SHARK OR ORCA?|*COMMENT* BELOW"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

PINGS = []
t = B["PINGS"]
while t < B["FLIP"]:
    PINGS.append(t)
    u = (t - B["PINGS"]) / (B["FLIP"] - B["PINGS"])
    t += 1 / (0.7 + 6 * u * u)

# ---------------------------------------------------------------- the deep underwater bed + the 8-bit beat
amb.x += (0.35 * band(F.rumble(DUR, 25, 220, seed=3), 25, 260) * seg(0, B["CHOMP"], 0.5))[:, None]
amb.x += (0.25 * band(F.rumble(DUR, 25, 220, seed=4), 25, 260) * seg(B["APEX"], DUR, 0.5))[:, None]
fx.x += CT.bed([
    S(0.0, B["PINGS"], 96, 100, "kbo"),
    S(B["PINGS"], B["FLIP"], 100, 168, "kbha"),
    S(B["FLIP"], B["FREEZE"], 128, 128, "kbhs"),
    S(B["FREEZE"], B["BREAK"], 80, 70, "kbo"),             # frozen: the beat slows down with the heartbeat
    S(B["CHOMP"] + 0.3, B["MAP"], 128, 128, "kbha"),
    S(B["MAP"], B["APEX"], 120, 124, "kbhsa"),
    S(B["APEX"], B["STOP"] + 0.2, 140, 148, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- SIGNATURE: sonar pings, faster + higher as the orcas close in
for i, p in enumerate(PINGS):
    u = (p - B["PINGS"]) / (B["FLIP"] - B["PINGS"])
    fx.put(CT.ping(1100 + 900 * u, 0.6), p, 0.45, -0.6 + 1.2 * u)
fx.put(CT.tone_glide(800, 2400, 0.6, "sine", 0.5, 0.4), B["FLIP"] - 0.6, 0.6)

# orca calls (whistles) as they arrive
for k, tk in enumerate((B["ORCAS"] + 0.2, B["ORCAS"] + 1.4, B["ORCAS"] + 2.6)):
    fx.put(CT.tone_glide(700 + 200 * k, 1800 + 300 * k, 0.5, "sine", 0.5, 0.5), tk, 0.35, -0.6 + 0.6 * k)
    fx.put(CT.tone_glide(1800, 900, 0.35, "sine", 0.5, 0.4), tk + 0.5, 0.3, -0.6 + 0.6 * k)

# the shark's heartbeat slows while it is frozen
hb_t, gap = B["FREEZE"] + 0.2, 0.45
while hb_t < B["BREAK"] - 0.2:
    fx.put(heartbeat(), hb_t, 0.8)
    hb_t += gap
    gap *= 1.18

# ---------------------------------------------------------------- a sound on every change
CT.card_blips(fx, CARDS)
for k in range(int((B["FLIP"] - B["PINGS"]) / 0.4)):                 # DISTANCE counter ticks
    fx.put(F.tick(2800, 0.7), B["PINGS"] + 0.2 + k * 0.4, 0.2, 0.5)
for k in range(12):                                                   # SIGHTINGS drop, one tick per shark leaving
    fx.put(F.tick(2600 - 80 * k, 1.0), B["MAP"] + 0.6 + k * 0.38, 0.4, (k % 3 - 1) * 0.5)
    fx.put(sweep(0.2, 900, 300), B["MAP"] + 0.6 + k * 0.38, 0.12)
for tc in (B["MAP"], B["APEX"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.55)
    fx.put(impact(0.5), tc, 0.35)

# ---------------------------------------------------------------- 0. the shark cruises (calm, deep)
fx.put(osfx.lib("whoosh-cinematic"), 0.0, 0.4)
for k in range(5):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.8, 500)), 0.5 + k * 0.5, 0.25, (k % 3 - 1) * 0.5)
fx.put(braam(1.6, 50), B["PINGS"], 0.5)

# ---------------------------------------------------------------- 1. the flip: big splash + whoosh
fx.put(osfx.sound("oga/water-splash/splash_05", F.splash(1.2, 3)), B["FLIP"], 0.9)
fx.put(impact(1.0), B["FLIP"], 0.8)
fx.put(osfx.lib("whoosh-cinematic"), B["FLIP"] + 0.1, 0.6)

# ---------------------------------------------------------------- 2. BREAK -> CHOMP (white flash, no gore)
fx.put(sweep(B["CHOMP"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.5)
fx.put(osfx.sound("oga/bangs-fireworks/bang_03", impact(1.0)), B["CHOMP"], 0.9)
fx.put(impact(1.0), B["CHOMP"], 0.9)
fx.put(sub_drop(1.2), B["CHOMP"], 0.8)
fx.put(osfx.sound("oga/scifi/teleport_02", sweep(0.6, 300, 1500)), B["CHOMP"] + 0.6, 0.5)   # x-ray on
fx.put(osfx.sfxr("pickupCoin", seed=6), B["CHOMP"] + 1.2, 0.45)                             # liver lights up

# ---------------------------------------------------------------- 3. the map: the sharks leave
fx.put(CT.womp(330, 4, 0.3), B["APEX"] - 1.6, 0.4)

# ---------------------------------------------------------------- 4. the apex predator: crown fanfare
fx.put(osfx.sound("oga/retro-synth/power_up_04", F.harp_up()), B["APEX"], 0.55)
for i, f0 in enumerate([523.25, 659.25, 783.99, 1046.5]):
    fx.put(bell(f0, 1.6), B["APEX"] + 0.1 + i * 0.08, 0.3)
fx.put(CT.tone_glide(800, 2000, 0.5, "sine", 0.5, 0.45), B["APEX"] + 0.8, 0.35)
fx.put(CT.tone_glide(600, 400, 0.5, "square", 0.5, 0.25), B["CTA"] + 0.2, 0.3)       # "NOT AGAIN."

# ---------------------------------------------------------------- 5. tape-stop -> rewind -> frame 1 (loop)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 96, 96, "kbo")], gain=0.5, crescendo=(0.8, 0.8))
amb.x += (0.35 * band(F.rumble(DUR, 25, 220, seed=3), 25, 260) * seg(B["REWIND"] + 0.1, DUR, 0.2))[:, None]

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=9.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR, "pings", len(PINGS))
