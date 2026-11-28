# For each line: align the AI clip's own speech to the voiceover (DTW on audio features),
# then rebuild the clip so its picture follows the VO timing. Pieces whose speed had to be
# changed a lot are reported as "weak" so the edit can cover them with B-roll.
import numpy as np, subprocess, librosa, json, os, sys
SR = 16000; HOP = 160
VO = "assets/audio/vo.mp3"
# name, clip, VO start, VO end, clip ranges kept (repeats / dead air removed)
LINES = [
    ("S0", "a12", 0.00, 2.62, [(1.00, 4.70)]),                # new opener: bill on table -> meter
    ("S1", "a3", 0.00, 2.62, [(2.10, 3.92), (4.42, 5.70)]),   # drop the repeated "बिजली बिल"
    ("S2", "a4", 2.88, 7.36, [(3.05, 8.95)]),
    ("S3", "a2", 7.79, 15.40, [(1.70, 7.70)]),
    ("S4", "a1", 15.40, 24.59, [(0.00, 5.95)]),
    ("S5", "a8", 24.91, 32.48, [(1.45, 7.62)]),
    ("S6", "a7", 35.11, 41.94, [(0.00, 7.62)]),
    ("S7", "a6", 42.25, 49.62, [(0.95, 8.02)]),
    ("S8", "a5", 49.75, 55.80, [(0.00, 6.02)]),
    ("S9", "a9", 56.13, 62.43, [(0.00, 7.60)]),
    ("S10", "a11", 62.84, 65.15, [(1.75, 5.15)]),
]
PIECE = 0.4

def load(f, ss=None, to=None):
    a = ["ffmpeg", "-v", "error"] + (["-ss", str(ss), "-to", str(to)] if ss is not None else []) + ["-i", f, "-af", "highpass=f=200,lowpass=f=4000", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(a, capture_output=True).stdout, np.int16).astype(np.float32) / 32768

def feat(a):
    m = librosa.feature.mfcc(y=a, sr=SR, n_mfcc=13, hop_length=HOP, n_fft=512)[1:]
    m = (m - m.mean(1, keepdims=True)) / (m.std(1, keepdims=True) + 1e-6)
    e = np.log(librosa.feature.rms(y=a, frame_length=400, hop_length=HOP) + 1e-4); e = (e - e.mean()) / (e.std() + 1e-6)
    d = np.diff(e, prepend=e[:, :1], axis=1); d = d / (d.std() + 1e-6)
    return np.vstack([0.5 * m, 2 * e, 1.5 * d])

report = {}
only = sys.argv[1:]
for name, clip, v0, v1, keep in LINES:
    if only and name not in only: continue
    src = f"assets/ai/{clip}.mp4"
    ca = np.concatenate([load(src, a, b) for a, b in keep])
    va = load(VO, v0, v1)
    D, wp = librosa.sequence.dtw(X=feat(va), Y=feat(ca), metric="euclidean", global_constraints=True, band_rad=0.2)
    wp = wp[::-1]; fq = wp[:, 0] * HOP / SR; fr = wp[:, 1] * HOP / SR
    L = sum(b - a for a, b in keep); T = v1 - v0
    anc = list(np.arange(0, T - PIECE * 0.5, PIECE)) + [T]
    raw = [0.0] + [float(np.interp(t, fq, fr)) for t in anc[1:-1]] + [L]
    tgt = raw[:]; weak = []
    for i in range(1, len(tgt)):
        d = anc[i] - anc[i - 1]; sp = (raw[i] - raw[i - 1]) / d
        weak.append(not (0.8 <= sp <= 1.25))
        tgt[i] = min(L, tgt[i - 1] + min(max(raw[i] - tgt[i - 1], 0.7 * d), 1.4 * d))  # catch back up to the true mapping
    def to_src(t):
        acc = 0.0
        for a, b in keep:
            if t < acc + (b - a) - 1e-6: return a + (t - acc), b
            acc += b - a
        return keep[-1][1], keep[-1][1]
    tmp = f"/tmp/sync_{name}"; os.makedirs(tmp, exist_ok=True); parts = []
    for i in range(len(anc) - 1):
        c0, c1 = tgt[i], tgt[i + 1]; out_d = anc[i + 1] - anc[i]; t = c0; segs = []
        if c1 - c0 < 1e-3:  # clip ran out: hold last frame
            c0 = max(0, c1 - 0.04)
        while t < c1 - 1e-4:
            s0, b = to_src(t); take = min(c1 - t, b - s0)
            if take < 1e-4: break
            segs.append((s0, s0 + take)); t += take
        for s0, s1 in segs:
            d = out_d * (s1 - s0) / (c1 - c0); f = f"{tmp}/p{len(parts):03d}.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s0:.3f}", "-t", f"{s1 - s0:.3f}", "-i", src, "-vf", f"setpts=(PTS-STARTPTS)*{d / (s1 - s0):.4f},fps=30", "-an", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-t", f"{d:.3f}", f], check=True)
            parts.append(f)
    open(f"{tmp}/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    out = f"assets/ai/{name}_{clip}_synced.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", out], check=True)
    # weak windows in VO time
    wins = [];
    for i, w in enumerate(weak):
        if w:
            a, b = v0 + anc[i], v0 + anc[i + 1]
            if wins and abs(wins[-1][1] - a) < 1e-6: wins[-1][1] = b
            else: wins.append([a, b])
    report[name] = dict(clip=clip, vo=[v0, v1], file=out, weak=[[round(a, 2), round(b, 2)] for a, b in wins])
    print(name, clip, f"VO {v0}-{v1}", "weak:", report[name]["weak"])
old = json.load(open("tools/sync_report.json")) if os.path.exists("tools/sync_report.json") else {}
old.update(report); json.dump(old, open("tools/sync_report.json", "w"), indent=1, ensure_ascii=False)
