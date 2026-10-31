"""Sound for "The bombardier beetle that escapes from inside a toad" — sound follows the story (STYLE_GUIDE.md section 6):

- SIGNATURE: the spray blasts. Each blast is a burst of ~500 pulses/s (the real beetle's pulse rate), heard as a hot
  "PFFRT!"; inside the toad they come faster and faster (1/s -> 5/s, the same BLASTS list the picture uses) and the BLASTS
  counter climbs with them; the toad's stomach gurgles and groans grow with its sickness, then the 0.25 s break, BLEURGH.
- a nonstop 8-bit bed whose tempo climbs inside the toad (110 -> 170 BPM); a blip on every card; ticks on the TIME INSIDE
  counter; whoosh + hit on every cut; a crescendo; tape-stop + rewind into frame 1 (no cold-open hook).

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
B = dict(GLITCH=-1.0, MEET=0.0, GULP=3.0, INSIDE=5.6, SPRAY=7.8, BREAK=17.25, BLEURGH=17.5, ALIVE=19.5, SCIENCE=23.0,
         CTA=25.6, STOP=28.5, REWIND=29.3)

CARDS = [
    (0.10, 2.80, "THIS BEETLE IS ABOUT|TO GET *EATEN*..."),
    (3.10, 5.40, "A TOAD SWALLOWS IT|*WHOLE*"),
    (5.80, 7.60, "BUT INSIDE THE TOAD..."),
    (7.90, 9.90, "IT FIRES A *100°C*|CHEMICAL SPRAY"),
    (10.00, 11.90, "*500* PULSES|EVERY SECOND"),
    (12.10, 14.60, "AGAIN, AND AGAIN|*AND AGAIN*"),
    (14.70, 17.20, "THE TOAD STARTS|FEELING *SICK*"),
    (17.50, 19.30, "*BLEURGH!*"),
    (19.60, 21.40, "OUT COMES THE BEETLE..."),
    (21.50, 22.90, "*ALIVE!*"),
    (23.20, 25.40, "UP TO *107 MINUTES*|INSIDE A TOAD"),
    (25.80, 28.40, "SEND THIS TO SOMEONE|WHO *NEVER GIVES UP*"),
]

os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()
S = CT.Sec

# the same blast schedule as the picture (index.html BLASTS)
BLASTS = []
t = B["SPRAY"]
while t < B["BREAK"] - 0.1:
    BLASTS.append(t)
    u = (t - B["SPRAY"]) / (B["BREAK"] - B["SPRAY"])
    t += 1 / (1 + 4 * u * u)

# ---------------------------------------------------------------- the nonstop 8-bit bed
fx.x += CT.bed([
    S(B["MEET"], B["GULP"], 104, 108, "kb"),
    S(B["GULP"], B["INSIDE"], 110, 110, "kbh"),
    S(B["INSIDE"], B["SPRAY"], 110, 116, "kbo"),             # inside: muffled, octave down
    S(B["SPRAY"], B["BREAK"], 116, 170, "kbhsa"),
    S(B["BLEURGH"], B["ALIVE"], 128, 128, "kbhs"),
    S(B["ALIVE"], B["SCIENCE"], 128, 128, "kbhsal"),
    S(B["SCIENCE"], B["CTA"], 120, 120, "kbha"),
    S(B["CTA"], B["STOP"] + 0.2, 150, 154, "kbhsal"),
], gain=0.5, crescendo=(0.8, 1.2))


# ---------------------------------------------------------------- SIGNATURE: the spray blasts (500 pulses/s bursts)
def spray(d=0.14, seed=0, pitch=1.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    pulses = (np.sin(2 * np.pi * 500 * pitch * tt) > 0.6).astype(float)
    noise = CT.noise(d, seed)[:n]
    hiss = band(noise, 1500, 9000)
    return (0.7 * pulses * np.exp(-tt * 14) + 0.9 * hiss / (np.max(np.abs(hiss)) + 1e-9) * np.exp(-tt * 9)) * np.minimum(1, tt / 0.003)


for i, bt in enumerate(BLASTS):
    u = (bt - B["SPRAY"]) / (B["BREAK"] - B["SPRAY"])
    fx.put(spray(0.14, i, 1.0 + 0.3 * u), bt, 0.55, (i % 3 - 1) * 0.4)
    fx.put(thump(70 + 30 * u, 0.12, 2.0), bt, 0.45)              # the stomach wall flinches
    if i % 3 == 0:
        fx.put(osfx.lib("pop"), bt + 0.02, 0.35)

# the toad's stomach gurgles + groans grow with its sickness
for k in range(8):
    tk = B["INSIDE"] + 0.4 + k * 1.4
    fx.put(osfx.sound(f"oga/creatures/burble_0{k % 2 + 1}", F.boil(0.6)), tk, 0.35 + 0.04 * k, (k % 2) * 1.0 - 0.5)
for k, tk in enumerate((B["SPRAY"] + 4.0, B["SPRAY"] + 6.6, B["SPRAY"] + 8.6)):
    fx.put(osfx.sound(f"oga/creatures/grunt_0{k + 1}", sweep(0.5, 200, 120)), tk, 0.45 + 0.1 * k)

# ---------------------------------------------------------------- a sound on every change
CT.card_blips(fx, CARDS)
for k in range(int((B["BLEURGH"] - B["INSIDE"]) / 0.5)):               # TIME INSIDE ticks
    fx.put(F.tick(3000, 0.8), B["INSIDE"] + 0.25 + k * 0.5, 0.25, 0.5)
for tc in (B["INSIDE"], B["ALIVE"], B["SCIENCE"], B["CTA"]):
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.55)
    fx.put(impact(0.5), tc, 0.35)

# ---------------------------------------------------------------- 0. the beetle walks in, the toad strikes: tongue + GULP
for k in range(10):
    fx.put(F.tick(5200, 0.5), 0.2 + k * 0.26, 0.18, -0.4)                # tiny footsteps
fx.put(osfx.sound("oga/creatures/misc_03", sweep(0.3, 300, 150)), 1.4, 0.4, 0.5)   # the toad croaks
fx.put(osfx.sound("oga/water-splash/slime_05", F.splash(0.3, 4)), B["GULP"], 0.8)
fx.put(CT.tone_glide(300, 1600, 0.15, "square", 0.5, 0.25), B["GULP"], 0.6)        # tongue zip
fx.put(osfx.sound("oga/creatures/eat_02", thump(180, 0.1, 1.5)), B["GULP"] + 0.55, 0.9)
fx.put(impact(0.9), B["GULP"] + 0.55, 0.7)
fx.put(CT.tone_glide(400, 120, 0.4, "square", 0.5, 0.2), B["GULP"] + 0.6, 0.6)      # down the throat

# ---------------------------------------------------------------- 1. inside: muffled, then the first blast
fx.put(osfx.lib("whoosh-cinematic"), B["INSIDE"] - 0.2, 0.6)
fx.put(braam(1.5, 50), B["SPRAY"], 0.5)
fx.put(riser(B["BREAK"] - B["SPRAY"], 150, 1600), B["SPRAY"], 0.25)

# ---------------------------------------------------------------- 2. BREAK -> BLEURGH
fx.put(sweep(B["BLEURGH"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.5)
fx.put(osfx.sound("oga/creatures/burp_02", sweep(0.6, 250, 90)), B["BLEURGH"], 1.0)
fx.put(osfx.sound("oga/water-splash/splash_03", F.splash(1.0, 9)), B["BLEURGH"] + 0.05, 0.9)
fx.put(impact(1.0), B["BLEURGH"], 0.8)
fx.put(sub_drop(0.9), B["BLEURGH"], 0.6)
fx.put(osfx.sound("oga/water-splash/slime_08", F.splash(0.4, 7)), B["BLEURGH"] + 0.7, 0.7)

# ---------------------------------------------------------------- 3. alive! a little victory sting
for k in range(8):
    fx.put(F.tick(5200, 0.5), B["ALIVE"] + 0.2 + k * 0.3, 0.18, 0.4)
fx.put(osfx.sfxr("powerUp", seed=8), B["ALIVE"] + 1.9, 0.45)
fx.put(add(bell(1046.5, 1.2), 0.5 * bell(1568, 1.2)), B["ALIVE"] + 2.0, 0.4)

# ---------------------------------------------------------------- 4. the study: a retch per toad that threw up, a ticker to 43%
for k in range(4):
    fx.put(osfx.sound("oga/creatures/burp_01", sweep(0.3, 220, 100)), B["SCIENCE"] + 0.4 + k * 0.25, 0.45, -0.6 + k * 0.4)
for k in range(12):
    fx.put(F.tick(2600 + 80 * k, 1.0), B["SCIENCE"] + 0.3 + k * 0.1, 0.35)

# ---------------------------------------------------------------- 5. CTA: confetti
fx.put(osfx.sound("oga/retro-synth/power_up_03", F.harp_up()), B["CTA"], 0.5)
for k in range(4):
    fx.put(osfx.sound(f"oga/bangs-fireworks/fw_0{k % 6 + 1}", F.firework(71 + k)), B["CTA"] + 0.3 + k * 0.5, 0.35, (k % 3 - 1) * 0.6)

# ---------------------------------------------------------------- 6. tape-stop -> rewind -> frame 1 (loop)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 104, 104, "kb")], gain=0.5, crescendo=(0.8, 0.8))

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=5.0)
CT.write_captions(ROOT, DUR, CARDS, B, V.segs)
print("DUR", DUR, "blasts", len(BLASTS))
