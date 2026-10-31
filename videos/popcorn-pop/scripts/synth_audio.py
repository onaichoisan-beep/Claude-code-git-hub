"""Sound for "Why popcorn pops": text cards + open-source / synthesised sound only (no narration), built the way the
owner's reference reels do it (STYLE_GUIDE.md section 6):

- the SIGNATURE sound is the oil crackle: its click rate follows the temperature counter (2/s at 20 C -> 70/s at 180 C,
  blurring into a sizzle), the steam bounces inside the kernel tick on the same train, and the bowl's popping frenzy at
  the end accelerates into a buzz;
- a nonstop 8-bit bed (chiptune.py) whose tempo climbs with the tension (100 -> 160 BPM), stops dead for 0.25 s before the
  POP, then slams back; half-time + octave-down during the slow-motion jump; a slow crescendo;
- a sound on every change (card blips, counter ticks, whoosh + hit on every cut), a tape-stop and rewind into the loop.

  python3 scripts/synth_audio.py      -> assets/audio/mix.wav + captions.js
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

DUR = 32.0
B = dict(GLITCH=1.6, HEAT=2.0, INSIDE=5.0, STEAM=6.8, PRESS=9.5, BREAK=13.75, POP=14.0, FOAM=15.2, LEG=19.0, PUSH=20.3,
         JUMP=21.3, HISS=23.5, DUD=25.7, BOWL=27.6, STOP=30.5, REWIND=31.3)

CARDS = [
    (0.10, 1.55, "THIS KERNEL IS ABOUT|TO *EXPLODE*"),
    (2.20, 4.90, "IT'S HIDING *WATER*|INSIDE"),
    (5.20, 7.30, "AT *100°C* THE WATER|TURNS TO STEAM"),
    (7.45, 9.40, "...BUT THE SHELL WON'T|LET IT *OUT*"),
    (9.70, 11.90, "PRESSURE: *9 TIMES*|THE AIR AROUND YOU"),
    (12.00, 13.70, "AT 180°C THE SHELL|HITS ITS *LIMIT*"),
    (14.00, 15.10, "*POP!*"),
    (15.30, 17.20, "THE STARCH TURNS|INTO *FOAM*"),
    (17.30, 19.00, "UP TO *40X* BIGGER"),
    (19.20, 21.20, "IN SLOW MOTION IT|GROWS A *LEG*..."),
    (21.30, 23.40, "...AND *JUMPS*!"),
    (23.60, 25.60, "THE POP SOUND? THAT'S|THE *STEAM* ESCAPING"),
    (25.75, 27.60, "DUDS? A *CRACKED* SHELL|LET THE STEAM LEAK"),
    (27.80, 30.40, "SEND THIS TO YOUR|*MOVIE BUDDY*"),
    (31.40, 32.00, "THIS KERNEL IS ABOUT|TO *EXPLODE*"),
]


def temp(t):
    """the temperature counter (shared with the picture through BEATS)"""
    if t < B["GLITCH"] or t >= B["REWIND"]:
        return 150 + 25 * min(1.0, (t if t < 5 else t - B["REWIND"]) / 1.6)
    if t < B["HEAT"]:
        return 20
    if t < B["POP"]:
        return 20 + 160 * ((t - B["HEAT"]) / (B["POP"] - B["HEAT"])) ** 0.75
    return 180


os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import chiptune as CT  # noqa: E402
import foley as F  # noqa: E402
import osfx  # noqa: E402

osfx.project(ROOT)
amb, fx = Bus(), Bus()

# ---------------------------------------------------------------- the nonstop 8-bit bed: tempo follows the tension
S = CT.Sec
fx.x += CT.bed([
    S(0.0, B["GLITCH"], 140, 150, "kbh"),                  # hook: already tense
    S(B["HEAT"], B["INSIDE"], 100, 108, "kb"),               # calm kitchen
    S(B["INSIDE"], B["PRESS"], 108, 120, "kbha"),            # inside the kernel, heating
    S(B["PRESS"], B["BREAK"], 120, 165, "kbhas"),            # pressure: the beat races
    #                                                         BREAK -> POP: dead silence (only a rising tick)
    S(B["POP"], B["LEG"], 128, 128, "kbhsal"),               # after the pop: full song with lead
    S(B["LEG"], B["HISS"], 64, 64, "kbo"),                   # slow motion: half-time, octave down
    S(B["HISS"], B["BOWL"], 128, 128, "kbhsa"),
    S(B["BOWL"], B["STOP"] + 0.2, 150, 156, "kbhsal"),       # the bowl frenzy: double-time hats
], gain=0.55, crescendo=(0.8, 1.2))

# ---------------------------------------------------------------- SIGNATURE: oil crackle, rate = temperature
def rate(t):
    return 2 + 68 * ((temp(t) - 20) / 160) ** 1.6


def pitch(t):
    return 0.8 + 0.6 * (temp(t) - 20) / 160


fx.put(CT.crackle(rate, 0.0, B["GLITCH"], seed=1, pitch_fn=pitch), 0.0, 0.35)
fx.put(CT.crackle(rate, B["HEAT"], B["BREAK"], seed=2, pitch_fn=pitch), B["HEAT"], 0.35)
sizzle = np.zeros(N)
for i0, i1 in ((0.0, B["GLITCH"]), (B["HEAT"], B["BREAK"])):
    n0, n1 = int(i0 * SR), int(i1 * SR)
    lev = np.array([(temp(i0 + k / SR) - 20) / 160 for k in range(0, n1 - n0, 480)])
    lev = np.repeat(lev, 480)[: n1 - n0]
    sizzle[n0:n1] = band(CT.noise(i1 - i0, 9)[: n1 - n0], 3000, 9000) * lev * 0.09
amb.x += sizzle[:, None]

# pressure whine: pitch climbs with the PRESSURE counter, cut at the break
fx.put(CT.tone_glide(180, 1400, B["BREAK"] - B["PRESS"], "square", 0.25, 0.10), B["PRESS"], 1.0)
fx.put(riser(B["BREAK"] - B["PRESS"], 200, 2000), B["PRESS"], 0.35)

# ---------------------------------------------------------------- a sound on every change
for a, b, text in CARDS:                                   # every new text card blips
    fx.put(CT.square(1760, 0.04, 0.25), a, 0.18); fx.put(CT.square(2637, 0.03, 0.25), a + 0.04, 0.12)
for k in range(int((B["POP"] - B["HEAT"]) / 0.5)):          # counter ticks every 0.5 s while heating
    fx.put(F.tick(3200, 0.8), B["HEAT"] + 0.25 + k * 0.5, 0.25, 0.5)
for tc in (B["INSIDE"], B["PRESS"], B["HISS"], B["DUD"], B["BOWL"]):   # every cut: whoosh + hit
    fx.put(osfx.lib("whoosh"), tc - 0.18, 0.55)
    fx.put(impact(0.5), tc, 0.35)

# ---------------------------------------------------------------- 0. hook (and the rewind glitch)
fx.put(osfx.sound("oga/100-sfx/slam_01", impact(1.0)), 0.0, 0.7)
fx.put(impact(1.0), 0.0, 0.5)
fx.put(osfx.sound("oga/creatures/hurt_01", sweep(0.3, 600, 900)), 0.6, 0.45)
fx.put(rewind(0.4), B["GLITCH"] - 0.02, 0.7)
fx.put(osfx.lib("glitch-1"), B["GLITCH"], 0.5)

# ---------------------------------------------------------------- 1-2. heating, inside the kernel: water jiggles, steam bounces
fx.put(osfx.sound("oga/water-splash/bubble_01", F.bubble_(1.0, 500)), B["INSIDE"] + 0.3, 0.5)
for k in range(8):
    fx.put(osfx.sound(f"oga/water-splash/bubble_0{k % 3 + 1}", F.bubble_(0.8, 600)), B["INSIDE"] + 0.5 + k * 0.22, 0.3, (k % 3 - 1) * 0.6)
fx.put(osfx.sound("oga/scifi/teleport_02", sweep(0.5, 300, 1500)), B["STEAM"], 0.5)
fx.put(F.boil(B["PRESS"] - B["STEAM"], rate=30), B["STEAM"], 0.35)

# ---------------------------------------------------------------- 3. pressure: creaks + heartbeat-fast kicks; "HELP."
for k in range(5):
    fx.put(osfx.sound("oga/100-sfx/metal_02", F.creak(0.4, 110 + 30 * k)), B["PRESS"] + 0.4 + k * 0.8, 0.35, (k % 2) * 1.2 - 0.6)
fx.put(osfx.sound("oga/creatures/cute_06", sweep(0.3, 700, 1100)), B["PRESS"] + 2.6, 0.5)

# ---------------------------------------------------------------- 4. BREAK -> POP
fx.put(sweep(B["POP"] - B["BREAK"], 1200, 2600) * 0.3, B["BREAK"], 0.6)
fx.put(osfx.sound("oga/bangs-fireworks/bang_01", impact(1.0)), B["POP"], 1.0)
fx.put(osfx.lib("pop"), B["POP"], 1.0)
fx.put(impact(1.0), B["POP"], 0.9)
fx.put(sub_drop(1.0), B["POP"], 0.8)
fx.put(osfx.lib("whoosh-cinematic"), B["POP"] + 0.05, 0.5)

# ---------------------------------------------------------------- 5. foam grows: rising arpeggio + fizz, counter x1 -> x40 ticks
fx.put(F.harp_up(392.0, 12, 0.12), B["FOAM"], 0.45)
fx.put(riser(B["LEG"] - B["FOAM"], 300, 1600), B["FOAM"], 0.3)
fx.put(CT.crackle(lambda t: 6 + 20 * (t - B["FOAM"]) / 3.8, B["FOAM"], B["LEG"], seed=5, base=4200), B["FOAM"], 0.2)
fx.put(osfx.sfxr("powerUp", seed=17), B["LEG"] - 0.4, 0.35)

# ---------------------------------------------------------------- 6. slow motion: a deep boing push, a whoosh up, a flip
fx.put(rewind(0.5)[::-1] * 0.6, B["LEG"], 0.5)
fx.put(osfx.sound("oga/100-sfx/spring_02", sweep(0.6, 200, 90)), B["PUSH"], 0.8)
fx.put(thump(60, 0.6, 2.0), B["PUSH"], 0.7)
fx.put(osfx.lib("whoosh-cinematic"), B["JUMP"], 0.7)
fx.put(CT.tone_glide(200, 900, 1.2, "square", 0.5, 0.12), B["JUMP"], 0.8)

# ---------------------------------------------------------------- 7. the hiss (the pop is steam) + the dud's sad trombone
fx.put(band(CT.noise(1.2, 21), 2500, 10000) * np.linspace(1, 0, int(1.2 * SR)) ** 2 * 0.5, B["HISS"] + 0.3, 0.8)
fx.put(osfx.lib("pop"), B["HISS"] + 0.3, 0.6)
fx.put(CT.womp(330, 4, 0.28), B["DUD"] + 0.3, 0.6)

# ---------------------------------------------------------------- 8. the bowl: popping frenzy accelerating into a buzz
t = B["BOWL"]
k = 0
while t < B["STOP"]:
    u = (t - B["BOWL"]) / (B["STOP"] - B["BOWL"])
    fx.put(osfx.lib("pop") if k % 3 == 0 else CT.square(900 + 600 * ((k * 7) % 5) / 4, 0.03, 0.5) * 0.6, t, 0.35, ((k * 37) % 11) / 5.5 - 1)
    t += 1.0 / (4 + 36 * u * u)
    k += 1
fx.put(osfx.lib("sparkle"), B["BOWL"] + 0.2, 0.4)

# ---------------------------------------------------------------- 9. tape-stop -> rewind -> the hook again (loop)
fx.x = CT.tape_stop(fx.x, B["STOP"], B["REWIND"])
amb.x = CT.tape_stop(amb.x, B["STOP"], B["REWIND"])
fx.put(rewind(0.5), B["REWIND"] - 0.05, 0.8)
fx.put(osfx.lib("glitch-2"), B["REWIND"], 0.4)
fx.x += CT.bed([S(B["REWIND"] + 0.15, DUR, 140, 142, "kbh")], gain=0.55, crescendo=(0.8, 0.8))
fx.put(CT.crackle(rate, B["REWIND"] + 0.1, DUR, seed=4, pitch_fn=pitch), B["REWIND"] + 0.1, 0.35)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "mix.wav"), amb_gain=1.0, makeup_db=6.0)

caps = [{"a": a, "b": b, "segs": [V.segs(ln) for ln in text.split("|")]} for a, b, text in CARDS]
with open(os.path.join(ROOT, "captions.js"), "w") as f:
    f.write("// generated by scripts/synth_audio.py: text cards + shared beats (no narration)\n")
    f.write(f"window.DUR = {DUR};\n")
    f.write("window.CAPS = " + json.dumps(caps) + ";\n")
    f.write("window.VO = [];\nwindow.MOUTH = {};\n")
    f.write("window.BEATS = " + json.dumps(B) + ";\n")
print("DUR", DUR)
