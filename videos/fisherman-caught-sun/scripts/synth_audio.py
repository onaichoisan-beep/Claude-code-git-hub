"""Narration + cinematic SFX for "The Fisherman Who Caught the Sun".

  python3 scripts/synth_audio.py

Reads the narration made by make_voices.py (assets/audio/vo/NN.wav + NN.json), lays the lines out,
builds the story's sound (sea, net, fire, ice, wind, oars, dawn, Diwali) ducked under the voice, and
writes assets/audio/mix.wav plus captions.js (captions, word timings) for the picture.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import voicelib as V  # noqa: E402

LINES = json.load(open(os.path.join(HERE, "lines.json")))["lines"]
GAPS = {1: 0.6, 2: 0.35, 3: 0.4, 4: 0.55, 5: 0.25, 6: 0.4, 7: 0.95, 8: 0.65}
TAIL = 1.7  # the camera dives into the diya flame, which becomes the Sun again

# caption chunks per line: (display text, first spoken word(s)); *word* = gold, | = new line
CAPS = [
    [("ONE EVENING...", "one"), ("A FISHERMAN|CAUGHT THE *SUN*.", "a fisherman")],
    [("EVERY NIGHT,", "every"), ("THE SUN SINKS INTO|THE SEA TO *SLEEP*.", "the sun")],
    [("BUT THAT NIGHT,", "but"), ("OLD *RAGHU*'S NET|CAME UP...", "old"), ("*BURNING*.", "burning")],
    [("HE HID THE *SUN*|IN HIS HUT.", "he"), ("AND MORNING...", "and"), ("*NEVER CAME*.", "never")],
    [("THE SEA *FROZE*.", "the sea"), ("THE BIRDS|WENT *SILENT*.", "the birds"), ("THE WHOLE VILLAGE|SHIVERED IN THE *DARK*.", "the whole")],
    [("RAGHU!", "raghu"), ("*GIVE IT BACK!*", "give")],
    [("SO HE ROWED INTO|THE BLACK SEA,", "so"), ("AND SET THE SUN *FREE*.", "and")],
    [("BUT FIRST...", "but"), ("HE BROKE OFF|ONE TINY *CRUMB*.", "he")],
    [("THAT'S WHY WE|LIGHT *DIYAS*.", "that's"), ("EVERY LITTLE FLAME...", "every"), ("IS A *CRUMB*|OF THE *SUN*.", "is")],
]

clips = V.layout(os.path.join(ROOT, "assets", "audio", "vo"), LINES, start=0.35, gaps=GAPS, max_pause=0.4)
DUR = round(np.ceil((clips[-1]["b"] + TAIL) * 10) / 10, 1)
print(f"voice ends {clips[-1]['b']:.2f}s -> DUR {DUR}")
os.environ["SFX_DUR"] = str(DUR)
from sfxlib import *  # noqa: E402,F403
import foley as F  # noqa: E402

K = V.Words(clips)
A, B, W, E = K.A, K.B, K.W, K.E
tracks = V.voice_tracks(clips, SR, N, band, gains={"wife": 0.5})
voice = sum(tracks.values())
duck = V.duck_env(voice, SR, depth=0.6)
captions = V.make_captions(clips, CAPS, DUR)

amb, fx = Bus(), Bus()


def bed(sig, a, b, gain, fade=0.6, pan=0.0):
    """loop/trim a bed signal into [a, b] with fades"""
    n = int((b - a) * SR)
    reps = int(np.ceil(n / len(sig)))
    x = np.tile(sig, reps)[:n].copy()
    f = int(fade * SR)
    if f and len(x) > 2 * f:
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
    amb.put(x, a, gain, pan)


# scene boundaries (match index.html)
T_SUNSET, T_NET, T_HUT, T_COLD, T_WIFE, T_ROW, T_CRUMB, T_DIYA = A(1) - 0.3, A(2), A(3), A(4), A(5), A(6), A(7), A(8)
T_DAWN = W(6, "free")

# ---------------------------------------------------------------- ambience beds
sea_bed = F.sea(12, swell=6.0)
bed(sea_bed, 0, T_HUT + 0.3, 0.55)                      # open sea, sunset, the net
bed(F.sea(10, swell=8, seed=4), T_ROW - 0.2, T_DIYA + 0.5, 0.5)  # rowing into the black sea
bed(F.wind(T_WIFE - T_HUT + 1, 300, 600, 0.35, seed=2), T_HUT + 0.6, T_WIFE + 0.3, 0.32)  # night wind
bed(F.wind(T_ROW - T_COLD + 1, 500, 1100, 0.7, seed=9), T_COLD - 0.2, T_ROW + 0.2, 0.55)  # freezing howl
bed(F.crickets(4, seed=5), T_HUT + 0.2, T_COLD + 0.1, 0.12, pan=0.3)               # night insects (then they stop)
# warm drone under the storytelling; cold and thin while the world freezes; glowing again at the end
dr = F.drone(DUR, 110)
amb.x += (0.16 * dr * (seg(0.6, T_COLD + 0.3, 1.2) + seg(T_DIYA - 0.4, DUR, 1.0)))[:, None]
amb.x += (0.10 * F.pad(DUR, [220, 277.2, 329.6], a=2, r_=2) * seg(T_COLD, T_ROW + 1, 1.0))[:, None]
# Diwali night: distant fireworks and festival bells
for k in range(7):
    fx.put(F.firework(200 + k, dist=2.2), T_DIYA + 0.3 + 0.85 * k, 0.35, (k % 3 - 1) * 0.7)
for k, f in enumerate([1318.5, 1567.98, 1318.5]):
    fx.put(bell(f, 2.5), T_DIYA + 0.15 + 1.6 * k, 0.12, 0.4 - 0.4 * k)

# ---------------------------------------------------------------- HOOK: the net bursts out with the Sun
fx.put(impact(1.2), 0.0, 1.0)
fx.put(braam(2.6, 49), 0.0, 0.6)
fx.put(sub_drop(1.4), 0.02, 0.55)
fx.put(F.splash(1.6), 0.0, 0.7)
fx.put(F.sizzle(2.4), 0.05, 0.4)
fx.put(F.fire(2.6), 0.1, 0.35)
fx.put(F.creak(0.9, 90), 0.5, 0.35, -0.4)
fx.put(add(impact(0.6), 0.7 * shing(0.6)), W(0, "sun") - 0.03, 0.6)
fx.put(rewind(0.5), A(1) - 0.62, 0.55)

# ---------------------------------------------------------------- the sun sinks to sleep (gulls, sizzle)
for k, tt_ in enumerate([T_SUNSET + 0.3, T_SUNSET + 1.1, T_SUNSET + 2.3]):
    fx.put(F.gull(30 + k), tt_, 0.22, 0.6 - 0.5 * k)
fx.put(sweep(1.4, 1200, 200), W(1, "sinks") - 0.1, 0.3)
fx.put(F.sizzle(1.6, seed=8), W(1, "sea") - 0.1, 0.35)
fx.put(F.harp_up(392, 6, 0.09), W(1, "sleep") - 0.15, 0.12)

# ---------------------------------------------------------------- the net: cast, sink, heavy, BURNING
fx.put(sweep(0.5, 400, 2500), T_NET + 0.15, 0.35, -0.3)
fx.put(F.splash(0.8, seed=21), T_NET + 0.6, 0.45, 0.2)
fx.put(F.creak(1.2, 70, seed=22), W(2, "net") - 0.2, 0.45, -0.3)
fx.put(F.boil(W(2, "burning") - W(2, "net") + 0.2, rate=30), W(2, "net"), 0.4)
fx.put(riser(W(2, "burning") - W(2, "night") + 0.1, 70, 420), W(2, "night"), 0.18)
fx.put(impact(1.0), W(2, "burning") - 0.04, 0.8)
fx.put(F.fire(2.2, seed=24), W(2, "burning"), 0.45)
fx.put(F.splash(1.3, seed=25), W(2, "burning") - 0.02, 0.5)
fx.put(F.sizzle(1.8, seed=26), W(2, "burning"), 0.4)

# ---------------------------------------------------------------- the hut; morning never comes
fx.put(F.creak(0.7, 130, seed=31), T_HUT + 0.2, 0.4, 0.3)     # door
fx.put(add(thump(70, 0.4, 1.4), 0.4 * noise_hit(0.05, 300, 3000)), W(3, "hut") - 0.05, 0.6)  # door shut
fx.put(F.fire(2.0, seed=33), T_HUT, 0.12)                       # the Sun glowing inside
fx.put(braam(3.0, 41), W(3, "never") - 0.05, 0.45)
fx.put(sub_drop(1.6, 70, 25), W(3, "never"), 0.5)
fx.put(gong(98, 4.0), W(3, "never") + 0.05, 0.22)

# ---------------------------------------------------------------- the freeze
for k in range(7):
    fx.put(F.ice_crack(40 + k, big=1.2 if k == 0 else 0.6), W(4, "froze") - 0.1 + 0.18 * k, 0.55 if k == 0 else 0.3, (k % 3 - 1) * 0.6)
fx.put(sweep(1.2, 3000, 300), W(4, "birds") - 0.2, 0.2)
fx.put(F.chatter(1.4), W(4, "shivered") - 0.1, 0.35, 0.2)
for k in range(3):
    fx.put(heartbeat(), W(4, "dark") + 0.2 + 0.75 * k, 0.4)

# ---------------------------------------------------------------- "Raghu! Give it back!"
fx.put(add(thump(60, 0.5, 2.0), 0.5 * noise_hit(0.08, 200, 4000)), A(5) - 0.05, 0.5)
fx.put(F.stab(196, 1.4), W(5, "give") - 0.03, 0.4)

# ---------------------------------------------------------------- rowing out; the Sun set free; dawn
for k in range(4):
    fx.put(F.oar(60 + k), T_ROW + 0.1 + 0.95 * k, 0.4, (k % 2) * 0.5 - 0.25)
    fx.put(F.creak(0.5, 100 + 15 * k, seed=70 + k), T_ROW + 0.35 + 0.95 * k, 0.18)
fx.put(riser(T_DAWN - T_ROW + 0.3, 90, 700), T_ROW + 0.4, 0.2)
fx.put(add(impact(1.0), 0.8 * braam(3.0, 65.4)), T_DAWN - 0.05, 0.8)
fx.put(sweep(1.4, 300, 6000), T_DAWN - 0.2, 0.45)
fx.put(F.pad(4.0, [261.6, 329.6, 392, 523.3], a=0.5, r_=2.5), T_DAWN, 0.35)
fx.put(gong(130.8, 4.5), T_DAWN + 0.05, 0.3)
for k in range(6):
    fx.put(F.chirp(80 + k), T_DAWN + 0.8 + 0.35 * k, 0.12, (k % 3 - 1) * 0.7)

# ---------------------------------------------------------------- "but first...": rewind to the crumb
fx.put(rewind(0.4), T_CRUMB - 0.42, 0.45)
fx.put(F.fire(2.5, seed=90), T_CRUMB, 0.18)
fx.put(add(noise_hit(0.05, 1500, 9000), 0.6 * thump(300, 0.08, 1.0)), W(7, "broke") + 0.05, 0.6)
fx.put(add(shing(0.7), 0.6 * F.sparkle(1.0, seed=91)), W(7, "crumb") - 0.02, 0.5)

# ---------------------------------------------------------------- diyas: each lights; the flame becomes the Sun
for k in range(6):
    fx.put(add(noise_hit(0.08, 800, 5000), 0.4 * F.sizzle(0.25, seed=95 + k)), T_DIYA + 0.25 + 0.22 * k, 0.25, (k - 2.5) / 3)
fx.put(F.sparkle(1.4, seed=97, lo=3000, hi=7000), W(8, "crumb") - 0.1, 0.35)
fx.put(add(bell(1046.5, 3.0), 0.6 * bell(1568, 3.0)), W(8, "sun") - 0.05, 0.3)
fx.put(sweep(1.4, 200, 5000), DUR - 1.45, 0.45)
fx.put(riser(1.3, 80, 600), DUR - 1.35, 0.25)
fx.put(F.fire(1.4, seed=99), DUR - 1.3, 0.3)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.55, makeup_db=4.0)
import wave  # noqa: E402

with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))
V.finish(sfx, voice, duck, os.path.join(ROOT, "assets", "audio", "mix.wav"), write_wav, SR, sfx_gain=0.8)
V.write_captions_js(os.path.join(ROOT, "captions.js"), DUR, captions, clips, V.mouths(tracks, SR))
for i, c in enumerate(clips):
    print(f"  {i:02d} {c['who']:4s} {c['a']:6.2f}-{c['b']:6.2f}  {LINES[i][1]}")
