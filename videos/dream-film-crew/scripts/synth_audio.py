"""Narration + sound effects for "Your Dream's Film Crew" (20 s).

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

SLOTS = [0.15, 3.30, 6.50, 9.50, 10.35, 12.30, 13.95, 15.55, 18.40]
CAPS = [
    [("YOU'VE NEVER SEEN *THIS*...", "you've"), ("BECAUSE YOU'RE ALWAYS", "because"), ("*ASLEEP* FOR IT.", "asleep")],
    [("THE SECOND YOUR", "the"), ("EYES *CLOSE*,", "eyes"), ("A *SECRET CREW*", "a"), ("SNEAKS IN.", "sneaks")],
    [("*LIGHTS*.", "lights"), ("*FOG*.", "fog"), ("A *DRAGON* ON STRINGS.", "a")],
    [("*ACTION!*", "action")],
    [("TONIGHT'S DREAM?", "tonight's"), ("YOU CAN *FLY*.", "you")],
    [("BUT THE MOMENT", "but"), ("YOUR *ALARM* RINGS...", "your")],
    [("THEY *TEAR* THE", "they"), ("WHOLE SET DOWN.", "whole")],
    [("AND THAT *FALLING* FEELING", "and"), ("THAT *JOLTS* YOU AWAKE?", "that jolts")],
    [("SOMEONE *DROPPED* YOU.", "someone")],
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
    j = int(start * SR)
    voice[j: j + len(x)] += x[: N - j]
    end = start + len(x) / SR
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


def pluck(f, d=0.35):
    """Karplus-Strong pizzicato (the sneaky tiptoe)."""
    n = int(d * SR)
    p = int(SR / f)
    buf = np.random.default_rng(int(f)).uniform(-1, 1, p)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.995
    return out * env(n, 0.002, d * 0.5)


def tiptoe(t0, t1, notes, gap=0.28):
    out, x, i = [], t0, 0
    while x < t1:
        out.append((x, pluck(notes[i % len(notes)])))
        x += gap
        i += 1
    return out


def snore(d=1.2):
    n = int(d * SR)
    tt = np.arange(n) / SR
    rattle = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 26 * tt))
    x = band(rng.standard_normal(n), 70, 600) * (0.4 + 0.6 * rattle)
    e = np.sin(np.pi * np.minimum(1, tt / (d * 0.7))) ** 2 * (tt < d * 0.7)
    return norm(x * e)


def shh(d=0.7):
    n = int(d * SR)
    return norm(band(rng.standard_normal(n), 2200, 8000)) * env(n, 0.06, 0.25)


def creak(d=0.7, f=120):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.5 * tt / d) * (1 + 0.05 * np.sin(2 * np.pi * 19 * tt))
    s = 2 * ((np.cumsum(ff) / SR) % 1) - 1
    return norm(band(s, 200, 2600)) * np.sin(np.pi * tt / d)


def switch():
    return norm(add(click() * 1.0, 0.5 * thump(900, 0.03, 0.2)))


def clunk_on():
    n = int(0.8 * SR)
    tt = np.arange(n) / SR
    hum = np.sin(2 * np.pi * 100 * tt) * 0.25 * np.exp(-tt * 2)
    return norm(add(thump(60, 0.3, 2.0), 0.7 * noise_hit(0.05, 300, 4000), hum))


def ring(d=1.6):
    """Old bell alarm clock: hammer rattling between two bells."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 2350 * tt) + np.sin(2 * np.pi * 2960 * tt) * 0.8 + np.sin(2 * np.pi * 5100 * tt) * 0.3)
    hammer = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * tt))
    return norm(s * hammer) * env(n, 0.005, 0.1)


def siren(d=1.6):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = 700 + 300 * np.sin(2 * np.pi * 2.5 * tt)
    return norm(np.sign(np.sin(2 * np.pi * np.cumsum(ff) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(ff) / SR)) * env(n, 0.05, 0.2)


def rip(d=0.45):
    n = int(d * SR)
    x = band(rng.standard_normal(n), 800, 7000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 60 * np.arange(n) / SR)))
    return norm(x) * env(n, 0.005, 0.15)


def slide_down(d=1.1, f0=1500, f1=180):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f0 * (f1 / f0) ** (tt / d) * (1 + 0.015 * np.sin(2 * np.pi * 6 * tt))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * env(n, 0.02, 0.1)


def boing(f=180, d=0.6):
    n = int(d * SR)
    tt = np.arange(n) / SR
    ff = f * (1 + 0.5 * np.sin(2 * np.pi * 11 * tt) * np.exp(-tt * 5))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-tt * 4)


def fan(d):
    n = int(d * SR)
    tt = np.arange(n) / SR
    return norm(band(rng.standard_normal(n), 100, 900) * (0.8 + 0.2 * np.sin(2 * np.pi * 30 * tt)) + 0.3 * np.sin(2 * np.pi * 120 * tt)) * env(n, 0.2, 0.2)


def footsteps(t0, t1, gap=0.09):
    out, x = [], t0
    while x < t1:
        out.append((x, noise_hit(0.04, 300, 3000) * (0.6 + 0.4 * hash1_(x))))
        x += gap
    return out


def hash1_(v):
    s = np.sin(v * 127.1 + 311.7) * 43758.5453
    return s - np.floor(s)


amb, fx = Bus(), Bus()

# ------------------------------------------------------------------ ambience: a quiet night room + clock tick
night = norm(band(rng.standard_normal(N), 150, 1200))
tick = np.zeros(N)
for i in range(int(DUR * 2)):
    c = click() * (1 if i % 2 else 0.7)
    j = int(i * 0.5 * SR)
    tick[j: j + len(c)] += c[: N - j]
for ch in range(2):
    amb.x[:, ch] += 0.18 * night * (seg(0, 6.5, 0.2) + seg(15.45, 20, 0.2))
    amb.x[:, ch] += 0.35 * tick * (seg(0, 6.45, 0.1) + seg(15.45, 16.98, 0.1) + seg(17.3, 20, 0.1))

# ------------------------------------------------------------------ HOOK: caught sneaking
SNORE = rec("snore", snore, dur=1.6)
fx.put(SNORE, 0.05, 0.35, -0.3)
for tt_, sig in tiptoe(0.05, 1.1, [196, 247, 294, 247], 0.26):
    fx.put(sig, tt_, 0.5)
fx.put(add(thump(160, 0.15, 0.6), 0.5 * noise_hit(0.05, 400, 3000)), 1.15, 0.6)  # bump
fx.put(boing(260, 0.4), 1.18, 0.3)
fx.put(braam(1.4, 62), 1.3, 0.35)
fx.put(shh(0.7), 1.38, 0.45, 0.3)
fx.put(rewind(0.45), 3.0, 0.55)
fx.put(lib("glitch-1", 0.6), 3.03, 0.35)

# ------------------------------------------------------------------ eyes close, the crew sneaks in
fx.put(SNORE, 3.5, 0.3, -0.3)
fx.put(rec("switch", switch), 4.1, 0.6)
fx.put(creak(0.75, 110), 4.55, 0.45, 0.6)
for tt_, sig in tiptoe(4.9, 6.4, [196, 247, 294, 247, 220, 262], 0.25):
    fx.put(sig, tt_, 0.45, 0.4)

# ------------------------------------------------------------------ the set goes up
fx.put(clunk_on(), 6.53, 0.75, -0.5)
fx.put(clunk_on(), 6.6, 0.7, 0.5)
fx.put(lib("whoosh-short"), 6.45, 0.4)
fx.put(noise_hit(1.0, 300, 3000), 7.45, 0.45)  # fog machine
fx.put(thump(55, 0.3, 1.0), 7.45, 0.4)
fx.put(creak(0.4, 300), 8.2, 0.35, 0.2)  # pulley
fx.put(creak(0.4, 340), 8.5, 0.35, 0.2)
fx.put(lib("sparkle"), 8.4, 0.3)

# ------------------------------------------------------------------ ACTION + flight
CLAP = rec("clapper", lambda: norm(add(noise_hit(0.04, 1500, 9000), thump(300, 0.06, 0.3))))
fx.put(CLAP, 9.55, 0.85)
fx.put(impact(0.5), 9.55, 0.45)
fx.put(sweep(1.6, 300, 3500), 10.3, 0.35)
fx.put(lib("sparkle"), 10.35, 0.35)
for k, f in enumerate([784, 988, 1175, 1568]):
    fx.put(bell(f, 1.6), 10.5 + 0.12 * k, 0.12)
fx.put(lib("glitch-3", 0.4), 11.25, 0.3)
fx.put(fan(1.0), 11.3, 0.3, 0.5)

# ------------------------------------------------------------------ alarm
fx.put(braam(1.2, 70), 12.25, 0.3)
RING = rec("alarm", lambda: ring(1.8), dur=1.8)
fx.put(rip(0.45), 12.88, 0.55)
fx.put(impact(0.9), 12.9, 0.85)
fx.put(RING, 12.9, 0.7)
fx.put(siren(1.0), 13.0, 0.25)
for k in range(4):
    fx.put(blip(1047, 0.06), 13.0 + 0.06 * k, 0.15)

# ------------------------------------------------------------------ teardown
fx.put(RING, 13.95, 0.35)
fx.put(rec("collapse", lambda: impact(0.8)), 13.95, 0.55)
for tt_, sig in footsteps(13.95, 15.4):
    fx.put(sig, tt_, 0.35, (hash1_(tt_) - 0.5))
fx.put(impact(0.7), 14.4, 0.6)  # dragon hits the floor
fx.put(add(thump(200, 0.1, 0.4), noise_hit(0.2, 600, 5000)), 14.42, 0.45)
fx.put(lib("whoosh-short"), 14.1, 0.35, -0.6)
fx.put(lib("whoosh-short"), 14.7, 0.35, 0.6)

# ------------------------------------------------------------------ the drop + the jolt
fx.put(blip(523, 0.12), 15.6, 0.15)
fx.put(slide_down(1.1, 1600, 170), 15.85, 0.4)
fx.put(sweep(1.0, 3000, 300), 15.95, 0.35)
fx.put(impact(1.2), 16.98, 1.0)
fx.put(boing(110, 0.7), 17.0, 0.45)  # bed springs
fx.put(noise_hit(0.25, 1200, 6000), 17.02, 0.25)  # gasp of air
fx.put(rec("switch", switch), 17.25, 0.5)
fx.put(creak(0.5, 160), 18.7, 0.3, 0.3)
fx.put(shh(0.6), 19.25, 0.35, 0.3)
for tt_, sig in tiptoe(19.5, 20.0, [196, 247], 0.25):
    fx.put(sig, tt_, 0.4)

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
