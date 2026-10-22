# Generates a dark documentary music bed (ducked under the voice) and an SFX track
# whose hits line up with the composition's visual events.
import sys, wave, numpy as np
SR = 48000; DUR = 34.6; N = int(SR * DUR)
out = sys.argv[1]
rng = np.random.default_rng(7)
t = np.arange(N) / SR

def write(path, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()

def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y

# ---------- music bed ----------
f = lambda n: 440 * 2 ** ((n - 69) / 12)
chords = [[45, 52, 60, 64], [41, 48, 57, 60], [48, 55, 60, 64], [43, 50, 55, 59]]  # Am F C G
CL = 4.8
pad = np.zeros(N)
for k in range(int(DUR / CL) + 1):
    s0 = int(k * CL * SR); s1 = min(N, int((k + 1) * CL * SR + 0.6 * SR))
    if s0 >= N: break
    seg = t[s0:s1] - k * CL
    env = np.minimum(1, seg / 0.8) * np.minimum(1, np.maximum(0, (CL + 0.6 - seg) / 0.8))
    for n in chords[k % 4]:
        for det in (-0.12, 0.12):
            ph = 2 * np.pi * f(n) * (1 + det / 100) * seg
            pad[s0:s1] += env * (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)) * 0.05
pad *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.25 * t)
# pulse: soft kick every beat at 100 bpm + a low tick off-beat
beat = 0.6; pulse = np.zeros(N)
for b in np.arange(0, DUR, beat):
    s0 = int(b * SR); L = min(int(0.35 * SR), N - s0); tt = np.arange(L) / SR
    pulse[s0:s0 + L] += np.sin(2 * np.pi * (48 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.32
    s1 = int((b + beat / 2) * SR); L2 = min(int(0.05 * SR), N - s1)
    if L2 > 0: pulse[s1:s1 + L2] += rng.standard_normal(L2) * np.exp(-np.arange(L2) / SR * 90) * 0.03
music = pad + pulse
music *= np.minimum(1, t / 0.4) * np.minimum(1, (DUR - t) / 1.0)
# duck under the voice (envelope follower on the narration)
w = wave.open(sys.argv[2]); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)[:, 0] / 32768.0
v = np.pad(v, (0, max(0, N - len(v))))[:N]
env = np.sqrt(np.convolve(v ** 2, np.ones(4800) / 4800, mode="same"))
env = env / (env.max() + 1e-9)
duck = 1 - 0.55 * np.clip(env * 3, 0, 1)
duck = np.convolve(duck, np.ones(2400) / 2400, mode="same")
music = music * duck
music = music / np.abs(music).max() * 0.16
write(out + "/music.wav", music)

# ---------- SFX ----------
sfx = np.zeros(N)
def add(t0, x, g):
    s0 = int(t0 * SR); L = min(len(x), N - s0)
    if L > 0: sfx[s0:s0 + L] += x[:L] * g
def thud():
    tt = np.arange(int(.5 * SR)) / SR
    return np.sin(2 * np.pi * (40 + 90 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 7) + lp(rng.standard_normal(len(tt)), .05) * np.exp(-tt * 40) * .6
def stamp():
    tt = np.arange(int(.35 * SR)) / SR
    return lp(rng.standard_normal(len(tt)), .25) * np.exp(-tt * 28) * 1.4 + np.sin(2 * np.pi * 95 * tt) * np.exp(-tt * 18) * .8
def whoosh(d=.45):
    L = int(d * SR); tt = np.arange(L) / SR; n = rng.standard_normal(L)
    a = 0.02 + 0.25 * np.sin(np.pi * tt / d) ** 2
    y = np.empty(L); acc = 0.0
    for i in range(L): acc += a[i] * (n[i] - acc); y[i] = acc
    return y * np.sin(np.pi * tt / d) ** 1.5 * 1.6
def rustle():
    L = int(.3 * SR); tt = np.arange(L) / SR
    return (rng.standard_normal(L) - lp(rng.standard_normal(L), .3)) * (rng.random(L) > .6) * np.exp(-tt * 9) * .5
def tick():
    L = int(.02 * SR); return rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 400)
def blip(fr=1300):
    tt = np.arange(int(.12 * SR)) / SR
    return np.sin(2 * np.pi * fr * tt * (1 + tt * 3)) * np.exp(-tt * 30)
def scribble(d=.4):
    L = int(d * SR); tt = np.arange(L) / SR
    return (rng.standard_normal(L) - lp(rng.standard_normal(L), .2)) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * tt)) * np.sin(np.pi * tt / d) * .35
def riser(d=1.0):
    tt = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * (300 + 900 * tt / d) * tt) * (tt / d) ** 2 * np.exp(-np.maximum(0, tt - d + .1) * 30) * .4

for x in [1.78, 2.98, 7.06, 9.14, 13.16, 19.5, 22.68, 26.0, 27.18, 30.94]: add(x - .02, thud(), .55)
for x in [2.0, 3.05, 7.7, 14.7, 32.98]: add(x + .14, stamp(), .7)
for x in [2.45, 5.6, 10.6, 17.9, 23.6, 28.4]: add(x - .3, whoosh(), .45)
add(3.8, whoosh(.3), .3)
for x in [0.05, 0.75, 1.6, 5.8, 12.4, 18.1, 20.1, 25.54, 29.0]: add(x, rustle(), .5)
for a, b in [(19.45, 19.95), (22.5, 22.7), (32.28, 32.66)]:
    for x in np.arange(a, b, .055): add(x, tick(), .5)
for x in [1.14, 8.48, 13.75, 14.62, 15.98, 16.86, 18.6, 19.5, 32.62]: add(x, scribble(), .45)
for x, fr in [(7.2, 1200), (7.35, 1400), (7.5, 1000), (9.14, 1500), (9.4, 1500), (9.92, 1100), (20.64, 1100), (21.6, 1500), (21.8, 1500)]: add(x, blip(fr), .25)
add(10.6, riser(.5), .5); add(26.25, riser(.95), .6)
sfx = sfx / np.abs(sfx).max() * 0.35
write(out + "/sfx.wav", sfx)
print("ok")
