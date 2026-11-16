# Sound for the edit (skill chapter 9), applied from v1:
#  voice chain -> synthesised warm SFX on graphic events (thinned) -> master -14 LUFS / -1.5 dBTP.
#  No music bed: the reference has none (AUDIO.md).
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
FPS = 30
rng = np.random.default_rng(7)

# ---------- 1. voice chain ----------
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'aroll/voice.wav', '-af',
    'highpass=f=70,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=3:attack=8:release=120,'
    'equalizer=f=3000:t=q:w=1:g=2.5,loudnorm=I=-15:TP=-2:LRA=9', '-ar', str(SR), '-ac', '1',
    'audio/voice_proc.wav'], check=True)
voice, _ = sf.read('audio/voice_proc.wav')
N = len(voice)

# ---------- 2. synthesised SFX (warm, low-mid, nothing hissy) ----------
def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def pop(semi=0.0):
    """soft 'premium click': damped low-mid sine body + a tiny filtered transient"""
    n = int(0.16 * SR); t = np.arange(n) / SR; k = 2 ** (semi / 12)
    f = 260 * k * (1 + 0.6 * np.exp(-t / 0.012))          # quick downward pitch drop
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.035)
    tr = sosfilt(butter(2, [700, 2200], 'bandpass', fs=SR, output='sos'), rng.standard_normal(n)) * env(n, 0.0005, 0.006) * 0.35
    s = body + tr
    return s / np.abs(s).max()

def whoosh(dur=0.42):
    """warm swipe: band-passed noise whose band sweeps 250->1100 Hz and back, lowpassed"""
    n = int(dur * SR); x = rng.standard_normal(n); out = np.zeros(n); hop = 512
    for i in range(0, n, hop):
        p = i / n; fc = 250 + 850 * np.sin(np.pi * p)
        sos = butter(2, [fc * 0.6, fc * 1.5], 'bandpass', fs=SR, output='sos')
        out[i:i + hop] = sosfilt(sos, x[max(0, i - 2048):i + hop])[-len(out[i:i + hop]):]
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6
    out = sosfilt(butter(2, 2500, 'lowpass', fs=SR, output='sos'), out * e)
    return out / np.abs(out).max()

# ---------- 3. events (logged by the render page) ----------
ev = json.load(open('audio/events.json'))
picks = json.load(open('src/picks_v1.json'))['picks']
# risers/whooshes only on 4 shot-type changes (speaker -> card / frame); every other cut is dry
WHOOSH_T = [4.067, 38.267, 52.5, 68.767]
prio = {'type': 3, 'accent': 3, 'art': 3, 'note': 3, 'group': 2, 'word': 2}
cands = []
for e in ev:
    k = e['k']
    if k in ('cap', 'card'):
        continue
    cands.append((e['t'], prio.get(k, 1), k))
# thinning rule (skill ch.9): >=18 f between pops, >=12 f from a whoosh, keep higher priority first
cands.sort(key=lambda x: (-x[1], x[0]))
chosen = []
for t, p, k in cands:
    if any(abs(t - c) * FPS < 18 for c, _, _ in chosen):
        continue
    if any(abs(t - w) * FPS < 12 for w in WHOOSH_T):
        continue
    if t < 0.5:
        continue
    chosen.append((t, p, k))
chosen.sort()
# first 5 s must not be crowded: max 2 pops there
early = [c for c in chosen if c[0] < 5]
chosen = [c for c in chosen if c[0] >= 5] + early[:2]
chosen.sort()

mix = voice.copy()
sfx = np.zeros(N)
def place(sig, t, gain_db):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: sfx[i:j] += sig[:j - i] * 10 ** (gain_db / 20)
for t, p, k in chosen:
    place(pop(rng.uniform(-0.7, 0.7)), t, -21)
for t in WHOOSH_T:
    place(whoosh(), t - 0.2, -24)
mix = voice + sfx
sf.write('audio/mix_pre.wav', mix.astype(np.float32), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'audio/mix_pre.wav', '-af',
    'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', str(SR), 'audio/mix.wav'], check=True)
json.dump({'pops': [round(c[0], 3) for c in chosen], 'whoosh': WHOOSH_T}, open('audio/sfx_log.json', 'w'))
print('pops', len(chosen), 'whooshes', len(WHOOSH_T))
