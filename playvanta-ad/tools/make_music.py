"""Original cinematic-sports music bed + SFX for the Playvanta ad (synthesised, royalty-free).

Grid: beat = 14.0/24 s so the logo hit (t=14.0) lands on a bar downbeat.
Sections (final VO time):
  0.0-11.4  hook: pads + plucked arp + soft pulse
  11.4-14.0 riser into logo
  14.0-28.0 brand: full drums, bass, strings  ("powerful")
  28.0-36.6 what we do: lighter, arp + pads + soft kick
  36.6-55.0 close: build back to full, bigger
  55.0-60.0 end card: final hit + sustained chord, fade
"""
import numpy as np, wave
from pathlib import Path

SR = 48000
DUR = 60.0
N = int(SR * DUR)
BEAT = 14.0 / 24
BAR = BEAT * 4
rng = np.random.default_rng(7)
OUT = Path(__file__).resolve().parent.parent / "assets"

def t_(d): return np.arange(int(SR * d)) / SR
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def env_adsr(n, a, d, s, r):
    e = np.ones(n) * s
    A, D, Rr = int(a * SR), int(d * SR), int(r * SR)
    A = min(A, n); e[:A] = np.linspace(0, 1, A)
    D = min(D, n - A); e[A:A + D] = np.linspace(1, s, D)
    if Rr > 0 and Rr < n: e[-Rr:] *= np.linspace(1, 0, Rr)
    return e

def lowpass(x, fc):
    # one-pole x2
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); z = 0.0
    for _ in range(2):
        z = 0.0
        for i in range(len(x)):
            z = (1 - a) * x[i] + a * z; y[i] = z
        x = y.copy()
    return y

def fast_lp(x, fc):
    # FFT brickwall-ish smooth lowpass (fast)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / fc) ** 4)
    return np.fft.irfft(X, len(x))

def fast_hp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (fc / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))

L = np.zeros(N); R = np.zeros(N)
def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N: return
    sig = sig[: N - i]
    gl, gr = gain * np.sqrt((1 - pan) / 2) * np.sqrt(2), gain * np.sqrt((1 + pan) / 2) * np.sqrt(2)
    L[i:i + len(sig)] += sig * gl; R[i:i + len(sig)] += sig * gr

# chords: Dm  Bb  F  C   (i VI III VII) — voicings as midi
CH = [[50, 57, 62, 65, 69], [46, 53, 58, 62, 65], [41, 53, 57, 60, 65], [48, 55, 60, 64, 67]]
BASS = [38, 34, 41, 36]

def chord_at(t): return int((t // BAR) % 4)

def pad(notes, d, bright=1800, amp=0.06):
    tt = t_(d); s = np.zeros_like(tt)
    for m in notes:
        f = midi(m)
        for det in (-0.12, 0.0, 0.11):
            ph = rng.random() * 2 * np.pi
            s += 2 * ((tt * f * 2 ** (det / 12) + ph / (2 * np.pi)) % 1) - 1
    s = fast_lp(s, bright)
    return s * env_adsr(len(s), 0.6, 0.3, 0.9, 0.8) * amp

def pluck(m, d=0.5, amp=0.18):
    f = midi(m); n = int(SR * d); p = int(SR / f)
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * amp

def kick(amp=0.9):
    tt = t_(0.45); f = 48 + 110 * np.exp(-tt * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt * 7) * amp

def tom(f0=90, amp=0.6):
    tt = t_(0.6); f = f0 + 60 * np.exp(-tt * 15)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-tt * 6) + 0.2 * rng.uniform(-1, 1, len(tt)) * np.exp(-tt * 30)) * amp

def clap(amp=0.35):
    tt = t_(0.3); n = rng.uniform(-1, 1, len(tt))
    e = np.exp(-tt * 22) + 0.6 * np.exp(-((tt - 0.012) % 0.012) * 200) * (tt < 0.036)
    return fast_hp(n * e, 900) * amp

def hat(amp=0.08, d=0.06):
    tt = t_(d); return fast_hp(rng.uniform(-1, 1, len(tt)), 7000) * np.exp(-tt * 60) * amp

def bass(m, d, amp=0.22):
    tt = t_(d); f = midi(m)
    s = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt)
    return s * env_adsr(len(s), 0.01, 0.2, 0.7, 0.08) * amp

def boom(amp=1.0):
    tt = t_(3.5); f = 32 + 80 * np.exp(-tt * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt * 1.4)
    crack = fast_lp(rng.uniform(-1, 1, len(tt)), 3500) * np.exp(-tt * 9) * 0.6
    return (body + crack) * amp

def riser(d, amp=0.25):
    tt = t_(d); n = rng.uniform(-1, 1, len(tt))
    x = np.zeros_like(n)
    seg = int(SR * 0.05)
    for i in range(0, len(n), seg):  # sweep the filter upward
        fc = 400 + 9000 * (i / len(n)) ** 2
        x[i:i + seg] = fast_hp(n[i:i + seg], max(80, fc * 0.3))
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / d) ** 2) / SR) * 0.3
    return (x + tone) * (tt / d) ** 2 * amp

def whoosh(d=0.6, amp=0.3):
    tt = t_(d); n = rng.uniform(-1, 1, len(tt))
    e = np.sin(np.pi * tt / d) ** 2
    return fast_lp(fast_hp(n, 500), 4000) * e * amp

def tick(amp=0.25):
    tt = t_(0.05); return np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 120) * amp

# ---------- arrangement ----------
def section_energy(t):
    if t < 11.4: return "hook"
    if t < 14.0: return "rise"
    if t < 28.0: return "brand"
    if t < 36.6: return "what"
    if t < 55.0: return "close"
    return "end"

# pads every bar
nb = int(DUR / BAR) + 1
for b in range(nb):
    t0 = b * BAR
    if t0 >= 55.0: break
    sec = section_energy(t0)
    amp = {"hook": 0.045, "rise": 0.05, "brand": 0.06, "what": 0.05, "close": 0.065}[sec]
    br = {"hook": 1300, "rise": 2000, "brand": 2600, "what": 1700, "close": 3000}[sec]
    add(pad(CH[b % 4], BAR + 0.8, br, amp), t0, 1.0, 0.0)

# arp (16ths in hook/what, 8ths elsewhere)
for k in range(int(55.0 / (BEAT / 2))):
    t0 = k * BEAT / 2
    sec = section_energy(t0)
    if sec == "rise": continue
    notes = CH[chord_at(t0)][1:] + [CH[chord_at(t0)][2] + 12]
    m = notes[k % len(notes)] + 12
    g = {"hook": 0.55, "brand": 0.45, "what": 0.6, "close": 0.5}[sec]
    add(pluck(m, 0.45), t0, g, 0.35 if k % 2 else -0.35)

# drums
for k in range(int(55.0 / BEAT)):
    t0 = k * BEAT; sec = section_energy(t0); beat_in_bar = k % 4
    if sec == "hook":
        if beat_in_bar in (0, 2) and t0 > 1.5: add(kick(0.45), t0)
    elif sec == "brand" or (sec == "close" and t0 > 38.5):
        add(kick(0.9), t0)
        if beat_in_bar in (1, 3): add(clap(0.32), t0, 1.0, 0.1)
        add(hat(0.07), t0 + BEAT / 2, 1.0, -0.3)
        if beat_in_bar == 3: add(tom(85, 0.35), t0 + BEAT / 2, 1.0, 0.4)
    elif sec == "what" or sec == "close":
        if beat_in_bar in (0, 2): add(kick(0.6), t0)
        add(hat(0.05), t0 + BEAT / 2, 1.0, 0.3)
# bass
for b in range(nb):
    t0 = b * BAR; sec = section_energy(t0)
    if sec in ("brand", "close", "what") and t0 < 55.0:
        for q in range(8):
            tq = t0 + q * BEAT / 2
            if tq >= 55.0: break
            add(bass(BASS[b % 4], BEAT / 2 * 0.95, 0.2 if sec != "what" else 0.12), tq)

# big moments
add(riser(2.6, 0.22), 14.0 - 2.6)
add(boom(0.9), 14.0)
add(riser(1.8, 0.16), 55.0 - 1.8)
add(boom(1.0), 54.98)
# final sustained chord + soft arp tail
add(pad([50, 57, 62, 65, 69, 74], 5.0, 2400, 0.07), 54.98)
for k, m in enumerate([74, 77, 81, 86, 81, 77, 74, 69]):
    add(pluck(m, 0.9, 0.14), 55.3 + k * BEAT / 2, 1.0, (-1) ** k * 0.3)

# ---------- simple stereo reverb ----------
ir_t = t_(2.2)
irL = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.0); irR = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.0)
irL[: int(0.02 * SR)] = 0; irR[: int(0.025 * SR)] = 0
def conv(x, ir):
    n = len(x) + len(ir); nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(ir, nf), nf)[: len(x)]
wetL = conv(fast_hp(L, 200), irL) * 0.012; wetR = conv(fast_hp(R, 200), irR) * 0.012
L2, R2 = L + wetL, R + wetR

# master: fade end, soft-clip, normalise
fade = np.ones(N); fi = int(58.2 * SR); fade[fi:] = np.linspace(1, 0, N - fi) ** 1.5
L2 *= fade; R2 *= fade
mx = max(np.abs(L2).max(), np.abs(R2).max()); L2 /= mx; R2 /= mx
L2 = np.tanh(L2 * 1.4) / np.tanh(1.4); R2 = np.tanh(R2 * 1.4) / np.tanh(1.4)

def write(path, l, r, peak=0.89):
    st = np.stack([l, r], 1); st = st / max(1e-9, np.abs(st).max()) * peak
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

write(OUT / "audio" / "music.wav", L2, R2)

# separate SFX one-shots
for name, sig in {"whoosh": whoosh(0.55, 1.0), "whoosh_long": whoosh(0.9, 1.0), "tick": tick(1.0),
                  "pop": fast_lp(np.sin(2*np.pi*np.cumsum(900*np.exp(-t_(0.12)*25)+300)/SR)*np.exp(-t_(0.12)*30), 5000)}.items():
    write(OUT / "sfx" / f"{name}.wav", sig, sig, 0.8)
print("ok")
