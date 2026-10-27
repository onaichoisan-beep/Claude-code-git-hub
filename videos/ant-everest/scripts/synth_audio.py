"""Trailer narration + sound effects for "Ant Everest" (20 s).

  python3 scripts/synth_audio.py

Voice lines (assets/audio/vo/NN.wav + NN.json, made by make_voices.py) are placed at fixed SLOTS,
SFX duck under the voice, and the mix goes to assets/audio/mix.wav. Also writes captions.js:
small centred captions synced word by word to the voice.
"""
import json
import wave
import os
import subprocess
import sys
import tempfile

DUR = 20.0
os.environ["SFX_DUR"] = str(DUR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import *  # noqa: E402,F403

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
VO = os.path.join(ROOT, "assets", "audio", "vo")

SLOTS = [0.25, 2.70, 5.30, 6.70, 7.90, 11.00, 12.10, 13.60, 17.00]
CAPS = [
    [("THEY SAID NO ANT", "they"), ("COULD *CLIMB* IT.", "could")],
    [("THE *DEADLIEST PEAK*", "the"), ("HE HAD EVER SEEN.", "he")],
    [("*AVALANCHES*.", "avalanches")],
    [("*BLIZZARDS*.", "blizzards")],
    [("*THREE DAYS*...", "three"), ("WITHOUT A SINGLE *CRUMB*.", "without")],
    [("BUT AT LAST...", "but")],
    [("HE MADE *HISTORY*.", "he")],
    [("OOH, CAN YOU PASS", "ooh"), ("THE *SUGAR*?", "the")],
    [("*LEGENDS*...", "legends"), ("NEVER *QUIT*.", "never")],
]
NARRATOR = {0, 1, 2, 3, 4, 5, 6, 8}  # line 7 is the human at the table (kept dry)


def key(w):
    return "".join(c for c in w.lower() if c.isalnum() or c == "'")


def find(words, anchor, frm):
    seq = [key(a) for a in anchor.split()]
    for i in range(frm, len(words)):
        if all(i + k < len(words) and key(words[i + k][0]).startswith(s) for k, s in enumerate(seq)):
            return i
    return None


def segs(text):
    return [[p, "g" if k % 2 else "p"] for k, p in enumerate(text.split("*")) if p]


# ------------------------------------------------------------------ voice
voice = np.zeros(N)
captions = []
for i, start in enumerate(SLOTS):
    wav = os.path.join(VO, f"{i:02d}.wav")
    words = json.load(open(os.path.join(VO, f"{i:02d}.json")))
    x = read_wav(wav)
    room = (SLOTS[i + 1] if i + 1 < len(SLOTS) else DUR - 0.3) - start - 0.08
    L = len(x) / SR
    tempo = 1.0
    if L > room:
        tempo = min(1.25, L / room)
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "f.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", f"atempo={tempo:.4f}", out], check=True)
            x = read_wav(out)
        print(f"line {i}: {L:.2f}s > {room:.2f}s, atempo {tempo:.3f}")
    if i in NARRATOR:
        x = x + 0.5 * band(x, 60, 220)
        x = reverb(np.concatenate([x, np.zeros(int(0.8 * SR))]), 1.6, 0.22, 3)
    j = int(start * SR)
    voice[j: j + len(x)] += x[: N - j]
    end = start + (len(x) / SR - (0.8 if i in NARRATOR else 0))
    idx, times = 0, []
    for text, anchor in CAPS[i]:
        k = find(words, anchor, idx)
        if k is None:
            raise SystemExit(f"line {i}: anchor '{anchor}' not found in {[w[0] for w in words]}")
        times.append(start + words[k][1] / tempo)
        idx = k + 1
    nxt = SLOTS[i + 1] if i + 1 < len(SLOTS) else DUR
    for k, (text, _) in enumerate(CAPS[i]):
        a = max(start, times[k] - 0.05)
        b = times[k + 1] - 0.05 if k + 1 < len(times) else min(end + 0.35, nxt - 0.02)
        captions.append({"a": round(a, 3), "b": round(b, 3), "segs": segs(text)})

voice = band(voice, 85, 14000)
active = np.abs(voice) > 1e-4
voice = voice / (np.sqrt(np.mean(voice[active] ** 2)) + 1e-9) * 10 ** (-14 / 20)
voice = np.tanh(voice * 1.5) / 1.5
e = np.convolve(np.abs(voice), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
e = np.clip(e / (np.percentile(e[active], 60) + 1e-9), 0, 1)
k = int(0.25 * SR)
e = np.convolve(e, np.ones(k) / k, mode="same")
duck = 1 - 0.6 * np.clip(e * 1.4, 0, 1)


# ------------------------------------------------------------------ sfx kit
def rec(name, fallback, dur=None):
    x = load(os.path.join(ROOT, "assets", "sfx", name + ".wav"), dur=dur)
    return fallback() if x is None else fade_out(x, 0.1)


def lib(name, dur=None):
    return load(os.path.join(LIB, name + ".mp3"), dur=dur)


def choir(d, freqs, vowel=(700, 1150)):
    """Synth 'aah' choir: detuned saws through two vowel formants, slow swell."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.4, 0.0, 0.5):
            ff = (f + det) * (1 + 0.006 * np.sin(2 * np.pi * (5 + det) * tt))
            x += 2 * ((np.cumsum(ff) / SR) % 1) - 1
    y = band(x, vowel[0] * 0.7, vowel[0] * 1.3) + 0.6 * band(x, vowel[1] * 0.8, vowel[1] * 1.2) + 0.3 * band(x, 150, 500)
    return norm(y) * env(n, d * 0.35, d * 0.35)


def howl(d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = np.zeros(n)
    for k, f in enumerate([380, 520, 760]):
        fc = f * (1 + 0.3 * np.sin(2 * np.pi * (0.3 + 0.17 * k) * tt + k))
        y = rng.standard_normal(n)
        blk = 4096
        out = np.zeros(n)
        for s in range(0, n, blk // 2):
            sg = y[s: s + blk]
            out[s: s + len(sg)] += band(sg, fc[s] * 0.85, fc[s] * 1.15) * np.hanning(len(sg))
        x += out
    return norm(x + 0.5 * band(rng.standard_normal(n), 200, 3000)) * env(n, 0.3, 0.3)


def rumble(d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return norm(band(rng.standard_normal(n), 25, 180) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt))) * env(n, 0.05, 0.4)


def tumble(d, rate=30):
    n = int(d * SR)
    out = np.zeros(n)
    for i in range(int(d * rate)):
        c = noise_hit(0.03, 1500, 9000) * (0.4 + 0.6 * hash_(i))
        j = int(hash_(i * 3.1) * (n - len(c)))
        out[j: j + len(c)] += c
    return out


def rattle(d):
    n = int(d * SR)
    out = np.zeros(n)
    for i in range(int(d * 14)):
        c = add(noise_hit(0.04, 2500, 9000), 0.5 * thump(900, 0.03, 0.2))
        j = int(i / 14 * SR)
        out[j: j + len(c)] += c[: n - j]
    return out


def plop():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    f = 300 * (1 + 3 * np.exp(-tt / 0.03))
    return norm(add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12), 0.5 * noise_hit(0.15, 500, 4000)))


def hash_(i):
    v = np.sin(i * 127.1 + 311.7) * 43758.5453
    return v - np.floor(v)


amb, fx = Bus(), Bus()

# ------------------------------------------------------------------ beds
wind = loop_to(load(os.path.join(ROOT, "assets", "sfx", "blizzard.wav")), N)
if wind is None:
    wind = howl(DUR)
kitchen_room = norm(band(rng.standard_normal(N), 80, 600)) * 0.5 + 0.2 * np.sin(2 * np.pi * 60 * t)  # fridge hum
for ch in range(2):
    amb.x[:, ch] += 0.55 * wind * (seg(0, 2.4, 0.05) + seg(6.6, 7.9, 0.15)) + 0.2 * wind * seg(2.4, 6.6, 0.3) + 0.15 * wind * seg(7.9, 11.0, 0.3)
    amb.x[:, ch] += 0.25 * kitchen_room * seg(13.4, 17.0, 0.1)

# ------------------------------------------------------------------ COLD OPEN: the blizzard
fx.put(braam(2.4, 41), 0.0, 0.8)
fx.put(impact(1.0), 0.0, 0.8)
fx.put(choir(2.3, [110, 131, 165]), 0.0, 0.35)
fx.put(rattle(2.0), 0.1, 0.18)
fx.put(heartbeat(), 0.9, 0.5)
fx.put(rewind(0.45), 2.15, 0.55)
fx.put(lib("glitch-1", 0.6), 2.18, 0.35)

# ------------------------------------------------------------------ the peak
fx.put(choir(2.6, [98, 147, 196, 233]), 2.6, 0.4)
fx.put(sweep(1.6, 150, 2500), 3.2, 0.35)
fx.put(braam(3.0, 37), 4.75, 0.9)
fx.put(impact(1.0), 4.8, 0.7)
fx.put(lib("sparkle"), 4.85, 0.3)

# ------------------------------------------------------------------ avalanche, blizzard, three days
fx.put(rumble(1.5), 5.0, 0.8)
fx.put(tumble(1.4, 40), 5.05, 0.45)
fx.put(rec("crunch", lambda: tumble(0.5, 20), dur=1.2), 5.2, 0.4)
fx.put(impact(0.9), 5.25, 0.7)
fx.put(howl(1.4), 6.6, 0.6)
fx.put(rattle(1.2), 6.6, 0.35)
fx.put(braam(1.4, 46), 6.65, 0.5)
for k, tt_ in enumerate([8.1, 8.9, 9.7]):
    fx.put(lib("whoosh-short"), tt_ + 0.15, 0.3)
    fx.put(heartbeat(), tt_ + 0.45, 0.45 - 0.08 * k)
fx.put(tumble(0.35, 30), 9.95, 0.35)  # munching the crumb

# ------------------------------------------------------------------ at last: history
fx.put(riser(1.5, 120, 900), 11.0, 0.3)
for tt_, sig in drum_roll(11.05, 12.45, 0.35, 0.08, 66):
    fx.put(sig, tt_, 0.55)
fx.put(impact(1.3), 12.5, 1.0)
fx.put(braam(3.0, 41), 12.5, 0.9)
fx.put(gong(98, 3.0), 12.52, 0.45)
fx.put(choir(2.2, [131, 165, 196, 262]), 12.5, 0.5)
fx.put(rec("flag", lambda: noise_hit(1.0, 400, 3000) * 0.3, dur=1.0), 12.55, 0.3)

# ------------------------------------------------------------------ the kitchen
fx.put(sub_drop(0.5, 120, 60), 13.38, 0.4)  # the epic music collapses
fx.put(click(), 13.4, 0.4)
fx.put(add(thump(260, 0.08, 0.5), noise_hit(0.04, 1500, 6000)), 14.8, 0.5)  # pinch
fx.put(lib("whoosh-short"), 14.9, 0.45)
fx.put(sweep(0.35, 2400, 500), 15.65, 0.4)
fx.put(rec("plop", plop), 15.95, 0.8)
fx.put(noise_hit(0.5, 400, 5000), 15.97, 0.45)
fx.put(impact(0.5), 15.97, 0.4)
for k in range(10):
    fx.put(bubble(0.9 + 0.2 * (k % 3)), 16.1 + 0.11 * k, 0.25, (k % 3 - 1) / 2)
fx.put(rec("spoon", lambda: bell(2600, 0.5), dur=1.2), 16.4, 0.25)

# ------------------------------------------------------------------ legends never quit
fx.put(braam(2.6, 44), 16.95, 0.7)
fx.put(choir(2.8, [110, 139, 165, 220]), 16.95, 0.45)
fx.put(sweep(1.0, 300, 2200), 18.0, 0.35)
for tt_, sig in drum_roll(18.6, 19.5, 0.3, 0.09, 70):
    fx.put(sig, tt_, 0.5)
fx.put(lib("sparkle"), 19.1, 0.3)

master(amb, fx, os.path.join(ROOT, "assets", "audio", "sfx.wav"), amb_gain=0.5, makeup_db=4.0)
with wave.open(os.path.join(ROOT, "assets", "audio", "sfx.wav"), "rb") as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float).reshape(-1, 2) / 32768
os.remove(os.path.join(ROOT, "assets", "audio", "sfx.wav"))

mix = sfx[:N] * (0.85 * duck)[:, None] + voice[:, None]
ceiling = 10 ** (-1 / 20)
if np.max(np.abs(mix)) > ceiling:
    mix = np.tanh(mix / ceiling * 1.05) * ceiling
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
