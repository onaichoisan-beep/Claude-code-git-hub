# v2 sound: SFX matched to the reference's own sound map (AUDIO.md, measured on the Demucs "no vocals" stem).
# Each graphic type gets the sound type the reference uses for it, at the reference's level relative to the voice.
# Sounds are synthesised (nothing is lifted from the reference audio).
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR, FPS = 48000, 30
rng = np.random.default_rng(11)
bp = lambda lo, hi: butter(2, [lo, hi], 'bandpass', fs=SR, output='sos')
lp = lambda f: butter(2, f, 'lowpass', fs=SR, output='sos')
hp = lambda f: butter(2, f, 'highpass', fs=SR, output='sos')

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def norm(x): return x / (np.abs(x).max() + 1e-9)

# ---------- sound designs ----------
def key_click():                      # ref typing: centroid ~1.6 kHz, mechanical, soft
    n = int(0.05 * SR)
    clk = sosfilt(bp(900, 2600), rng.standard_normal(n)) * env(n, 0.0004, 0.006)
    thock = np.sin(2 * np.pi * rng.uniform(170, 210) * np.arange(n) / SR) * env(n, 0.0005, 0.012) * 0.5
    return norm(clk + thock) * rng.uniform(0.7, 1.0)
def typing(nchars):                   # one click per typed char, 2 f/char (TypeBox speed)
    step = int(2 / FPS * SR); out = np.zeros(step * nchars + int(0.06 * SR))
    for k in range(nchars):
        j = k * step + int(rng.uniform(-0.008, 0.008) * SR); j = max(0, j)
        c = key_click(); out[j:j + len(c)] += c
    return norm(out)
def thump():                          # ref "working": low-heavy hit (low ratio .52, centroid 1.25 kHz)
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 46 + 70 * np.exp(-t / 0.05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.16)
    knock = sosfilt(bp(700, 2000), rng.standard_normal(n)) * env(n, 0.0005, 0.012) * 0.35
    return norm(body + knock)
def ding():                           # ref side notes: short bright click/ding (centroid 3-7 kHz)
    n = int(0.35 * SR); t = np.arange(n) / SR; f0 = rng.uniform(2300, 2600)
    s = sum(a * np.sin(2 * np.pi * f0 * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, .09), (2.01, .35, .05), (2.98, .15, .03)])
    return norm(s * np.minimum(1, t / 0.001))
def sparkle(dur=0.45, lo=3000, hi=8500, n_part=10, decay=0.12):   # ref lime/script/arc: shimmer, centroid 6-8 kHz, tonal (not hiss)
    n = int(dur * SR); out = np.zeros(n); t = np.arange(n) / SR
    for k in range(n_part):
        st = rng.uniform(0, dur * 0.55); f = rng.uniform(lo, hi); a = rng.uniform(.4, 1)
        tt = np.clip(t - st, 0, None); e = (t >= st) * np.exp(-tt / decay) * np.minimum(1, tt / 0.002)
        out += a * np.sin(2 * np.pi * f * tt) * e
    out = sosfilt(lp(10000), out)
    return norm(out * np.sin(np.pi * np.linspace(0, 1, n)) ** 0.3)
def shutter():                        # retro camera: two soft mechanical clicks
    out = np.zeros(int(0.25 * SR))
    for j, g in [(0, 1), (int(0.085 * SR), .7)]:
        n = int(0.03 * SR); c = sosfilt(bp(1200, 4000), rng.standard_normal(n)) * env(n, 0.0003, 0.005) * g
        out[j:j + n] += c
    return norm(out)
def pop(semi=0.0):                    # soft click for chest words / card lines (skill ch.9)
    n = int(0.16 * SR); t = np.arange(n) / SR; k = 2 ** (semi / 12)
    f = 260 * k * (1 + 0.6 * np.exp(-t / 0.012))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.035)
    tr = sosfilt(bp(700, 2200), rng.standard_normal(n)) * env(n, 0.0005, 0.006) * 0.35
    return norm(body + tr)
def whoosh(dur=0.42):
    n = int(dur * SR); x = rng.standard_normal(n); out = np.zeros(n); hop = 512
    for i in range(0, n, hop):
        p = i / n; fc = 250 + 850 * np.sin(np.pi * p)
        seg = sosfilt(bp(fc * 0.6, fc * 1.5), x[max(0, i - 2048):i + hop]); out[i:i + hop] = seg[-len(out[i:i + hop]):]
    return norm(sosfilt(lp(2500), out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6))

# ---------- voice (same chain as v1) ----------
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'aroll/voice.wav', '-af',
    'highpass=f=70,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=3:attack=8:release=120,'
    'equalizer=f=3000:t=q:w=1:g=2.5,loudnorm=I=-15:TP=-2:LRA=9', '-ar', str(SR), '-ac', '1',
    'audio/voice_proc.wav'], check=True)
voice, _ = sf.read('audio/voice_proc.wav'); N = len(voice)
fr = SR // FPS
vrms = np.array([np.sqrt((voice[i:i + fr] ** 2).mean()) for i in range(0, N - fr, fr)])
VMED = 20 * np.log10(np.median(vrms[vrms > 10 ** (-50 / 20)]))     # median voiced-frame level

sfx = np.zeros(N); log = []
def place(sig, t, rel_db, name):
    """rel_db = loudest 33 ms frame of the sound vs the median voice frame (the reference's own measure)"""
    pk = max(np.sqrt((sig[i:i + fr] ** 2).mean()) for i in range(0, max(1, len(sig) - fr), fr // 2))
    g = 10 ** ((VMED + rel_db) / 20) / (pk + 1e-9)
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: sfx[i:j] += sig[:j - i] * g; log.append((round(t, 2), name, rel_db))

# ---------- placement (reference map; levels = reference rel-to-voice, softened only where the ref is extreme) ----------
ev = json.load(open('audio/events.json'))
last_pop = -9
for e in sorted(ev, key=lambda x: x['t']):
    t, k = e['t'], e['k']
    if k == 'type':    place(typing(e['n']), t + 2 / FPS, -7, 'typing')          # ref f325: -6.4 dB
    elif k == 'serif': place(thump(), t, -3, 'thump')                             # ref f779: -1.2 dB
    elif k == 'note':  place(ding(), t, -9, 'ding')                               # ref f937/1251: -7.6..-18
    elif k == 'lime':  place(sparkle(0.35, 4000, 9000, 8, 0.08), t, -3, 'sparkle')  # ref f1717: +0.4 dB
    elif k == 'script':place(sparkle(0.8, 3000, 8000, 14, 0.18), t, -8, 'shimmer')  # ref f1814: -7.5 dB, 23 f
    elif k == 'arc':   place(sparkle(0.9, 3500, 8500, 16, 0.2), t, -12, 'shimmer')  # ref f1148: -16.6 dB, 27 f
    elif k == 'pink':  place(sparkle(0.6, 3000, 7000, 10, 0.15), t, -11, 'sparkle')
    elif k == 'camera':place(shutter(), t + 0.05, -8, 'shutter')
for t in [4.067, 38.267, 52.42, 68.767]:                                          # 4 shot-type changes only
    place(whoosh(), t - 0.2, -12, 'whoosh')
# soft pops where the reference has no sound type (chest words, card lines): skill thinning rule
hits = [t for t, _, _ in log]
for e in sorted(ev, key=lambda x: x['t']):
    t = e['t']
    if e['k'] not in ('word', 'cardtext') or t < 0.5: continue
    if t - last_pop < 18 / FPS or any(abs(t - h) < 12 / FPS for h in hits): continue
    place(pop(rng.uniform(-0.7, 0.7)), t, -14, 'pop'); last_pop = t; hits.append(t)

mix = voice + sfx
sf.write('audio/mix_pre.wav', mix.astype(np.float32), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'audio/mix_pre.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), 'audio/mix.wav'], check=True)
json.dump(log, open('audio/sfx_log.json', 'w'))
from collections import Counter
print(len(log), 'sfx', Counter(n for _, n, _ in log))
