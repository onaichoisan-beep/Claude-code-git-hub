"""Narration + cinematic SFX for "How heavy is a cloud?".

  python3 scripts/synth_audio.py [voice_dir]

voice_dir (default assets/audio/vo) holds NN.wav + NN.json (word timings) per line, made by
make_voices.py. Each line is placed at its fixed slot in SLOTS (time-squeezed a little if a voice
runs long), SFX duck under the voice, and the result is written to assets/audio/mix.wav.
Also writes captions.js: small centred word-synced captions, timed to this voice.
"""
import json
import os
import subprocess
import sys
import tempfile

DUR = 61.5
os.environ["SFX_DUR"] = str(DUR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
VO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets", "audio", "vo")

# start time of each narration line (lines.json); the picture is cut to these
SLOTS = [0.20, 2.95, 8.60, 11.75, 12.75, 15.20, 21.80, 28.40, 31.10, 33.85, 38.80, 42.45, 46.45, 49.15, 52.35, 57.10]

# caption chunks per line: (display text, first spoken word(s) of the chunk); *word* = gold
CAPS = [
    [("CLOUDS ARE WAY *HEAVIER*", "clouds"), ("THAN MOST PEOPLE THINK.", "than")],
    [("IF YOU SEE A CLOUD", "if"), ("LIKE THIS,", "like"), ("IT'S A *CUMULUS* CLOUD.", "it's"),
     ("FOR A COMMON ONE,", "for"), ("*1 KILOMETER* WIDE...", "a kilometer")],
    [("GUESS HOW MANY", "guess"), ("*ELEPHANTS*", "elephants"), ("THIS CLOUD WEIGHS?", "this")],
    [("*83!*", "eighty")],
    [("*ELEPHANTS*", "elephants"), ("FLOATING IN THE SKY!", "floating")],
    [("IF YOU SEE ONE", "if"), ("THAT LOOKS LIKE THIS,", "that"), ("IT'S ONLY PROBABLY", "it's"),
     ("ABOUT *5 ELEPHANTS*", "about"), ("FOR THE SAME SIZE,", "for"), ("BUT WAY *HIGHER* IN THE SKY.", "but")],
    [("BUT IF YOU EVER SEE ONE", "but"), ("THAT LOOKS LIKE THIS...", "that"), ("A *THUNDERCLOUD*", "a thundercloud"),
     ("*10 KILOMETERS* ACROSS", "ten"), ("AND PACKED WITH", "and"), ("WAY MORE *WATER*...", "way")],
    [("THAT WHOPPER CAN WEIGH...", "that"), ("YOU WANNA GUESS?", "you")],
    [("*330,000 ELEPHANTS!*", "three")],
    [("THAT'S AS MUCH WATER AS", "that's"), ("*800 OLYMPIC POOLS*", "eight"), ("RIGHT THERE", "right"),
     ("OVER YOUR HEAD.", "over")],
    [("SO WHY DON'T ALL", "so"), ("THE WATER DROPLETS", "the water"), ("IN THAT CLOUD", "in"), ("*FALL DOWN?*", "fall")],
    [("WELL, THEY EACH ONLY START", "well"), ("ABOUT *20 MICRONS* ACROSS.", "about")],
    [("THAT'S LESS THAN HALF", "that's"), ("THE WIDTH OF A", "the width"), ("*HUMAN HAIR*.", "human")],
    [("SO THE GENTLEST", "so"), ("*RISING AIR*", "rising"), ("HOLDS THEM ALL UP.", "holds")],
    [("BUT WHEN THEY CRASH", "but"), ("TOGETHER AND GROW", "together"), ("*A MILLION TIMES* BIGGER...", "a million"),
     ("THEY FALL AS *RAIN*.", "they fall")],
    [("SO NEXT TIME YOU LOOK UP,", "so"), ("REMEMBER:", "remember"), ("THERE ARE *ELEPHANTS*", "there"),
     ("FLOATING OVER YOUR HEAD.", "floating")],
]


def key(w):
    return "".join(c for c in w.lower() if c.isalnum() or c == "'")


def find(words, anchor, frm):
    seq = [key(a) for a in anchor.split()]
    for i in range(frm, len(words)):
        if all(i + k < len(words) and key(words[i + k][0]).startswith(s) for k, s in enumerate(seq)):
            return i
    return None


def segs(text):
    out = []
    for k, part in enumerate(text.split("*")):
        if part:
            out.append([part, "g" if k % 2 else "p"])
    return out


# ------------------------------------------------------------------ voice
voice = np.zeros(N)
captions = []
for i, start in enumerate(SLOTS):
    wav = os.path.join(VO, f"{i:02d}.wav")
    words = json.load(open(os.path.join(VO, f"{i:02d}.json")))
    x = read_wav(wav)
    room = (SLOTS[i + 1] if i + 1 < len(SLOTS) else DUR - 0.2) - start - 0.1
    L = len(x) / SR
    tempo = 1.0
    if L > room:
        tempo = min(1.3, L / room)
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "f.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", f"atempo={tempo:.4f}", out], check=True)
            x = read_wav(out)
        print(f"line {i}: {L:.2f}s > {room:.2f}s, atempo {tempo:.3f}")
    voice[int(start * SR): int(start * SR) + len(x)] += x[: N - int(start * SR)]
    end = start + len(x) / SR
    # caption chunks
    idx, times = 0, []
    for text, anchor in CAPS[i]:
        j = find(words, anchor, idx)
        if j is None:
            raise SystemExit(f"line {i}: anchor '{anchor}' not found in {[w[0] for w in words]}")
        times.append(start + words[j][1] / tempo)
        idx = j + 1
    nxt = SLOTS[i + 1] if i + 1 < len(SLOTS) else DUR
    for k, (text, _) in enumerate(CAPS[i]):
        a = max(start, times[k] - 0.06)
        b = times[k + 1] - 0.06 if k + 1 < len(times) else min(end + 0.35, nxt - 0.02)
        captions.append({"a": round(a, 3), "b": round(b, 3), "segs": segs(text)})

# clean up the voice: high-pass, gentle saturation-compression, level to about -17 dBFS RMS
voice = band(voice, 85, 14000)
active = np.abs(voice) > 1e-4
voice = voice / (np.sqrt(np.mean(voice[active] ** 2)) + 1e-9) * 10 ** (-15 / 20)
voice = np.tanh(voice * 1.6) / 1.6

# ducking envelope: SFX drop ~9 dB while she speaks
e = np.convolve(np.abs(voice), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
e = np.clip(e / (np.percentile(e[active], 60) + 1e-9), 0, 1)
k = int(0.25 * SR)
e = np.convolve(e, np.ones(k) / k, mode="same")
duck = 1 - 0.65 * np.clip(e * 1.4, 0, 1)

# ------------------------------------------------------------------ sfx
amb, fx = Bus(), Bus()


def trumpet(d=0.9, f=420.0):
    """Elephant trumpet: buzzy saw sliding up with fast vibrato, through a nasal band."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.5 * np.minimum(1, tt / (d * 0.3))) * (1 + 0.03 * np.sin(2 * np.pi * 11 * tt))
    ph = np.cumsum(ff) / SR
    x = 2 * (ph % 1) - 1 + 0.5 * (2 * ((ph * 2.01) % 1) - 1)
    x = band(x, 400, 3500) + 0.3 * band(rng.standard_normal(n), 800, 3000)
    return norm(x) * env(n, 0.04, d * 0.5)


def thunder(d=3.0, crack=1.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    rum = band(rng.standard_normal(n), 25, 260) * (np.exp(-tt / (d * 0.35)) * (1 - np.exp(-tt / 0.08)))
    flutter = 0.6 + 0.4 * band(rng.standard_normal(n), 1, 9) / 0.05
    cr = band(rng.standard_normal(n), 900, 9000) * np.exp(-tt / 0.06) * crack
    return norm(rum * np.clip(flutter, 0.2, 1.5) + 0.6 * cr)


def splash(d=1.0):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return norm(band(rng.standard_normal(n), 400, 7000) * np.exp(-tt / 0.18) * np.minimum(1, tt / 0.01))


# ambience: soft high-altitude wind the whole way, darker rumble under the storm, rain beds
for ch in range(2):
    wind = norm(band(rng.standard_normal(N), 150, 1100))
    storm = norm(band(rng.standard_normal(N), 30, 160))
    rain = norm(band(rng.standard_normal(N), 2500, 9000))
    amb.x[:, ch] += 0.30 * wind + 0.45 * storm * seg(21.8, 31.0, 0.8) + 0.18 * rain * (seg(23.0, 30.8, 1.0) + seg(54.0, 57.6, 0.8))

# COLD OPEN: the cloud slams the scale down
fx.put(impact(1.1), 0.0, 1.0)
fx.put(braam(2.2, 52), 0.0, 0.55)
fx.put(add(thump(140, 0.15, 0.4), 0.6 * noise_hit(0.05, 2000, 9000)), 0.05, 0.5)  # metal clank
fx.put(rewind(0.45), 2.55, 0.55)

# cumulus reveal + 1 km ruler
fx.put(sweep(0.8, 200, 2500), 3.3, 0.45)
fx.put(sweep(0.7, 2500, 300), 5.9, 0.3)
for k in range(5):
    fx.put(blip(660 + 110 * k, 0.07), 7.15 + 0.1 * k, 0.22)

# elephants pop in, guesses flicker, drum roll, 83!
for k in range(9):
    fx.put(bubble(1.4 - 0.08 * k), 8.7 + 0.13 * k, 0.45, (k % 5 - 2) / 3)
for k, tc in enumerate([9.7, 10.05, 10.4, 10.75]):
    fx.put(blip(520 + 140 * k, 0.1), tc, 0.35)
for tt_, sig in drum_roll(10.95, 11.7, 0.22, 0.07, 74):
    fx.put(sig, tt_, 0.6)
fx.put(impact(0.8), 11.75, 0.9)
fx.put(shing(0.5), 11.78, 0.35)
fx.put(add(thump(150, 0.12, 0.4), 0.5 * noise_hit(0.04, 2000, 9000)), 11.8, 0.4)
fx.put(trumpet(0.9, 430), 12.75, 0.55, -0.4)
fx.put(trumpet(0.8, 520), 13.35, 0.4, 0.4)

# up to the cirrus: whoosh up, airy shimmer, 5 elephants clank onto the scale
fx.put(sweep(1.2, 300, 5000), 15.05, 0.45)
for k, f in enumerate([1568, 1976, 2349]):
    fx.put(bell(f, 1.4), 16.2 + 0.25 * k, 0.12)
fx.put(taiko(90), 18.2, 0.6)
fx.put(add(thump(150, 0.12, 0.4), 0.5 * noise_hit(0.04, 2000, 9000)), 18.25, 0.35)

# thundercloud
fx.put(braam(3.0, 44), 21.75, 0.7)
fx.put(thunder(3.5, 0.6), 22.0, 0.8)
fx.put(thunder(3.0, 1.2), 24.3, 0.8, 0.3)
fx.put(thunder(2.5, 1.0), 26.6, 0.6, -0.3)

# "you wanna guess?" -> counter spins -> 330,000
fx.put(riser(2.6, 90, 900), 28.4, 0.3)
for tt_, sig in drum_roll(29.4, 31.05, 0.3, 0.06, 70):
    fx.put(sig, tt_, 0.6)
for k in range(16):
    fx.put(blip(700 + 40 * k, 0.05), 29.5 + 0.1 * k, 0.15)
fx.put(impact(1.3), 31.1, 1.0)
fx.put(braam(3.0, 41), 31.1, 0.8)
fx.put(sub_drop(1.5), 31.1, 0.7)
for k in range(5):
    fx.put(trumpet(0.9, 380 + 45 * k), 31.4 + 0.22 * k, 0.32, (k % 3 - 1) * 0.6)

# 800 Olympic pools: splash
fx.put(splash(1.0), 33.9, 0.7)
fx.put(sweep(1.0, 250, 3000), 34.6, 0.35)
fx.put(sub_drop(1.0, 70, 30), 36.3, 0.4)

# inside the cloud: droplets
fx.put(sweep(1.0, 3000, 250), 38.6, 0.45)
for k in range(24):
    fx.put(bubble(0.5 + 0.03 * (k % 7)), 39.0 + 0.15 * k + 0.05 * (k % 3), 0.18, ((k * 7) % 5 - 2) / 3)
fx.put(blip(1320, 0.08), 43.3, 0.3)
fx.put(blip(990, 0.08), 43.45, 0.3)
fx.put(shing(0.5), 47.3, 0.35)

# rising air holds them up
fx.put(riser(2.6, 120, 700), 49.1, 0.22)
fx.put(sweep(2.4, 200, 1800), 49.3, 0.4)

# droplets merge and fall as rain
for k in range(8):
    fx.put(bubble(0.6 + 0.25 * k), 52.4 + 0.24 * k, 0.4, ((k * 3) % 5 - 2) / 3)
fx.put(sub_drop(1.0, 120, 40), 54.3, 0.45)
for k in range(30):
    fx.put(bubble(0.35), 54.4 + 0.1 * k + 0.03 * (k % 4), 0.12, ((k * 7) % 5 - 2) / 3)

# outro -> back to the scale (loops into the cold open)
for k, f in enumerate([784, 988, 1175]):
    fx.put(bell(f, 1.8), 57.2 + 0.3 * k, 0.14)
fx.put(trumpet(1.0, 440), 59.2, 0.35)
fx.put(sweep(0.9, 200, 3500), 60.6, 0.45)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.5, makeup_db=4.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))

mix = sfx[:N] * (0.8 * duck)[:, None] + voice[:, None]
peak = np.max(np.abs(mix))
ceiling = 10 ** (-1 / 20)
mix = np.tanh(mix / ceiling * 1.05) * ceiling if peak > ceiling else mix
fade = int(0.02 * SR)
mix[:fade] *= np.linspace(0, 1, fade)[:, None]
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
write_wav(os.path.join(ROOT, "assets", "audio", "mix.wav"), mix)
db = 20 * np.log10(np.sqrt(np.mean(mix ** 2)) + 1e-12)
print(f"wrote mix.wav (RMS {db:.1f} dBFS, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS)")

with open(os.path.join(ROOT, "captions.js"), "w") as f:
    f.write("// generated by scripts/synth_audio.py: caption chunks timed to the narration\n")
    f.write("window.CAPS = " + json.dumps(captions) + ";\n")
print(f"wrote captions.js ({len(captions)} chunks)")
