#!/usr/bin/env python3
"""Joins the per-line voice clips into assets/audio/vo.wav and writes vo_timing.json.

usage: make_vo.py <dir with N_key.wav clips> <script.json>
Chatterbox gives no word timestamps, so each line's speech span (found from loudness)
is shared across its words in proportion to their length.
"""
import json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, script = sys.argv[1], json.load(open(sys.argv[2]))
GAPS = {'hook': 0.25, 'name': 0.3, 'question': 0.2}

def speech_span(path):
    w = wave.open(path); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    hop = sr // 100
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    on = np.where(e > e.max() * 0.06)[0]
    return on[0] / 100, (on[-1] + 1) / 100

t, lines, inputs = 0.12, [], []
for i, (k, _, ro) in enumerate(script):
    raw = os.path.join(src, f'{i}_{k}.wav'); clip = os.path.join(src, f'{i}_{k}.trim.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-ar', '44100', '-ac', '1', '-sample_fmt', 's16', clip + '.tmp.wav'], check=True)
    s, e = speech_span(clip + '.tmp.wav')
    s, e = max(0, s - 0.04), e + 0.12
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', clip + '.tmp.wav', '-ss', str(s), '-to', str(e), clip], check=True)
    dur = round(e - s, 3)
    words = ro.split(); weights = [len(x) + 2 for x in words]; tot = sum(weights)
    span0, span1 = 0.04, dur - 0.12
    acc, wl = span0, []
    for x, wt in zip(words, weights):
        d = (span1 - span0) * wt / tot
        wl.append({'t': x, 's': round(acc, 3), 'e': round(acc + d, 3)}); acc += d
    lines.append({'key': k, 'start': round(t, 3), 'dur': dur, 'words': wl})
    inputs.append(clip)
    t += dur + GAPS.get(k, 0.12)
fc = ''.join(f"[{i}:a]adelay={int(l['start'] * 1000)}|{int(l['start'] * 1000)}[a{i}];" for i, l in enumerate(lines))
fc += ''.join(f'[a{i}]' for i in range(len(lines))) + f'amix=inputs={len(lines)}:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[o]'
args = sum([['-i', p] for p in inputs], [])
out = os.path.join(HERE, 'assets/audio/vo.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-filter_complex', fc, '-map', '[o]', '-ar', '44100', '-ac', '1', out], check=True)
json.dump({'total': round(t + 0.5, 2), 'lines': lines}, open(os.path.join(HERE, 'assets/audio/vo_timing.json'), 'w'), ensure_ascii=False, indent=1)
print('total', round(t + 0.5, 2)); [print(l['key'], l['start'], l['dur']) for l in lines]
