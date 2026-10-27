"""Narration helpers for the narrated pixel shorts.

make_voices.py writes one NN.wav + NN.json (word timings) per line of lines.json. These helpers
lay the lines end to end (long pauses inside a line squeezed), level the voices, and build what
the picture needs: small centred captions timed to the words, per-line word timings, and mouth
flaps. A project's synth_audio.py calls layout() first (it sets the film length), imports sfxlib
with SFX_DUR set, places its sound effects, then calls finish().
"""
import json
import os
import wave

import numpy as np

FPS = 30


def key(w):
    return "".join(c for c in w.lower() if c.isalnum() or c == "'")


def find(words, anchor, frm=0):
    """index of the first word at/after frm where the anchor's words start the spoken words"""
    seq = [key(a) for a in anchor.split()]
    for i in range(frm, len(words)):
        if all(i + k < len(words) and key(words[i + k][0]).startswith(s) for k, s in enumerate(seq)):
            return i
    return None


def segs(text):
    """'PLAIN *GOLD* PLAIN' -> [[text, 'p'|'g'], ...]"""
    return [[p, "g" if k % 2 else "p"] for k, p in enumerate(text.split("*")) if p]


def read_mono(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float) / 32768
    return x, sr


def squeeze(x, sr, words, max_pause):
    """Shorten silences longer than max_pause inside a line; shift the word timings to match."""
    hop = int(0.01 * sr)
    fr = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same")[::hop] + 1e-12)
    quiet = fr < np.max(fr) * 10 ** (-38 / 20)
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if i > 0 and j < len(quiet) and (j - i) * 0.01 > max_pause:
                runs.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    out, pos, cuts = [], 0, []
    for a, b in runs:
        ca, cb = a + max_pause / 2, b - max_pause / 2
        out.append(x[int(pos * sr): int(ca * sr)])
        cuts.append((ca, cb - ca))
        pos = cb
    out.append(x[int(pos * sr):])
    y = np.concatenate(out)

    def mapt(tt):
        s = 0.0
        for c, r in cuts:
            if tt > c:
                s += min(r, tt - c)
        return tt - s
    return y, [[w, round(mapt(a), 3), round(mapt(b), 3)] for w, a, b in words]


def layout(vo_dir, lines, start=0.2, gap=0.3, gaps=None, max_pause=0.42, pauses=None):
    """Lay the lines end to end. gaps: {line: silence before it}; pauses: {line: max pause inside it}."""
    gaps, pauses = gaps or {}, pauses or {}
    clips, t0 = [], start
    for i, (who, _text) in enumerate(lines):
        x, sr = read_mono(os.path.join(vo_dir, f"{i:02d}.wav"))
        words = json.load(open(os.path.join(vo_dir, f"{i:02d}.json")))
        x, words = squeeze(x, sr, words, pauses.get(i, max_pause))
        if i > 0:
            t0 = clips[-1]["b"] + gaps.get(i, gap)
        L = len(x) / sr
        clips.append({"who": who, "a": round(t0, 3), "b": round(t0 + L, 3), "x": x, "sr": sr,
                      "w": [[w, round(t0 + a, 3), round(t0 + b, 3)] for w, a, b in words]})
    return clips


class Words:
    """Word-time lookups for placing sounds: W(i, 'word', n) -> start of the n-th match in line i."""

    def __init__(self, clips):
        self.c = clips

    def W(self, i, word, n=0):
        j = -1
        for _ in range(n + 1):
            j = find(self.c[i]["w"], word, j + 1)
            if j is None:
                raise SystemExit(f"line {i}: word '{word}' not found in {[w[0] for w in self.c[i]['w']]}")
        return self.c[i]["w"][j][1]

    def E(self, i, word, n=0):
        """end time of that word"""
        j = -1
        for _ in range(n + 1):
            j = find(self.c[i]["w"], word, j + 1)
        return self.c[i]["w"][j][2]

    def A(self, i):
        return self.c[i]["a"]

    def B(self, i):
        return self.c[i]["b"]


def voice_tracks(clips, SR, N, band, level_db=-13.5, gains=None):
    """One levelled mono track per speaker (every line at the same loudness, gentle saturation)."""
    gains = gains or {}
    tracks = {}
    for c in clips:
        tracks.setdefault(c["who"], np.zeros(N))
    for c in clips:
        x = c["x"]
        x = np.interp(np.arange(int(len(x) * SR / c["sr"])) * c["sr"] / SR, np.arange(len(x)), x)
        x = band(x, 70, 14000)
        act = np.abs(x) > 2e-3
        x = x / (np.sqrt(np.mean(x[act] ** 2)) + 1e-9) * 10 ** ((level_db + gains.get(c["who"], 0)) / 20)
        i0 = int(c["a"] * SR)
        tracks[c["who"]][i0: i0 + len(x)] += x[: N - i0]
    for k in tracks:
        tracks[k] = np.tanh(tracks[k] * 1.5) / 1.5
    return tracks


def mouths(tracks, SR):
    """per-frame mouth opening 0-9 per speaker, as a digit string"""
    out = {}
    for k, v in tracks.items():
        hop = SR // FPS
        fr = np.sqrt(np.convolve(v ** 2, np.ones(hop) / hop, mode="same")[::hop] + 1e-12)
        ref = np.percentile(fr[fr > 0.01], 80) if np.any(fr > 0.01) else 1
        m = np.clip(fr / ref, 0, 1) ** 0.8
        out[k] = "".join(str(int(round(z * 9))) for z in m)
    return out


def make_captions(clips, caps, dur, lead=0.05, hold=0.4):
    """caps[i] = [(display text, first spoken word(s) of the chunk), ...]; *word* = gold"""
    captions = []
    for i, c in enumerate(clips):
        idx, times = 0, []
        for text, anchor in caps[i]:
            j = find(c["w"], anchor, idx)
            if j is None:
                raise SystemExit(f"line {i}: anchor '{anchor}' not found in {[w[0] for w in c['w']]}")
            times.append(c["w"][j][1])
            idx = j + 1
        nxt = clips[i + 1]["a"] if i + 1 < len(clips) else dur
        for k, (text, _) in enumerate(caps[i]):
            a = max(c["a"], times[k] - lead)
            b = times[k + 1] - lead if k + 1 < len(times) else min(c["b"] + hold, nxt - 0.03)
            captions.append({"a": round(a, 3), "b": round(b, 3), "segs": [s for ln in text.split("|") for s in [segs(ln)]]})
    return captions


def duck_env(voice, SR, depth=0.65):
    """1 when quiet, down to 1-depth under speech (smooth)."""
    active = np.abs(voice) > 1e-4
    e = np.convolve(np.abs(voice), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
    e = np.clip(e / (np.percentile(e[active], 60) + 1e-9), 0, 1)
    k = int(0.25 * SR)
    e = np.convolve(e, np.ones(k) / k, mode="same")
    return 1 - depth * np.clip(e * 1.4, 0, 1)


def finish(sfx, voice, duck, path, write_wav, SR, sfx_gain=0.75, makeup_db=1.5):
    """voice over ducked SFX, look-ahead peak limit to -1 dBFS, edge fades, write."""
    N = len(voice)
    mix = (sfx[:N] * (sfx_gain * duck)[:, None] + voice[:, None]) * 10 ** (makeup_db / 20)
    ceiling = 10 ** (-1 / 20)
    pk = np.max(np.abs(mix), axis=1)
    win = int(0.005 * SR)
    held = np.repeat([pk[max(0, i - win): i + 2 * win].max() for i in range(0, N, win)], win)[:N]
    gain = np.minimum(1, ceiling / np.maximum(held, 1e-9))
    k = int(0.01 * SR)
    gain = np.minimum(np.convolve(gain, np.ones(k) / k, mode="same"), ceiling / np.maximum(pk, 1e-9))
    mix = mix * gain[:, None]
    fade = int(0.02 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)[:, None]
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    write_wav(path, mix)
    db = 20 * np.log10(np.sqrt(np.mean(mix ** 2)) + 1e-12)
    print(f"wrote {os.path.basename(path)} (RMS {db:.1f} dBFS, peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS)")


def write_captions_js(path, dur, captions, clips, mouth):
    vo = [{"who": c["who"], "a": c["a"], "b": c["b"], "w": c["w"]} for c in clips]
    with open(path, "w") as f:
        f.write("// generated by scripts/synth_audio.py: captions, line/word timings and mouth flaps for the narration\n")
        f.write(f"window.DUR = {dur};\n")
        f.write("window.CAPS = " + json.dumps(captions) + ";\n")
        f.write("window.VO = " + json.dumps(vo) + ";\n")
        f.write("window.MOUTH = " + json.dumps(mouth) + ";\n")
    print(f"wrote {os.path.basename(path)} ({len(captions)} caption chunks)")
