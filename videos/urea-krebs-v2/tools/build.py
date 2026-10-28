#!/usr/bin/env python3
"""Generates index.html from assets/audio/vo.wav + vo_timing.json.

Lip-sync comes from the voice loudness (15 mouth frames a second); every other cue
is tied to a word in the script, so re-running after a new voice-over keeps sync.
"""
import json, os, re, wave
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(HERE, 'assets/audio/vo_timing.json')))
LINES = {l['key']: l for l in V['lines']}
TOTAL = V['total']

def kw(key, word, which=0, end=False):
    l = LINES[key]
    hits = [w for w in l['words'] if re.sub(r'[^a-z]', '', w['t'].lower()).startswith(word.lower())]
    w = hits[which]
    return round(l['start'] + (w['e'] if end else w['s']), 3)
start = lambda k: LINES[k]['start']

T = {'hook': 0, 'wheels': start('wheels') - 0.1, 'split': start('split') - 0.05, 'chain': start('chain') - 0.05,
     'back': start('back'), 'name': start('name') - 0.1, 'question': start('question') - 0.15, 'cta': start('cta') - 0.1, 'end': TOTAL}
C = {'ruko': kw('hook', 'ruko'), 'bicycle': kw('hook', 'bicycle'), 'urea': kw('wheels', 'urea'), 'krebs': kw('wheels', 'krebs'),
     'asa': kw('split', 'argininosuccinate'), 'tootta': kw('split', 'tootta'), 'fum1': kw('split', 'fumarate'),
     'chainw': kw('chain', 'chain'), 'jaata': kw('chain', 'jaata'), 'aspartate': kw('back', 'aspartate'), 'aata': kw('back', 'aata'),
     'kbike': kw('name', 'krebs'), 'enzyme': kw('question', 'enzyme'), 'follow': kw('cta', 'follow')}

# ---- lip-sync from loudness ----
w = wave.open(os.path.join(HERE, 'assets/audio/vo.wav'))
sr, n = w.getframerate(), w.getnframes()
a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
if w.getnchannels() == 2: a = a.reshape(-1, 2).mean(1)
hop = sr // 15
rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
ref = np.percentile(rms[rms > 0], 95)
EXPR_T = [(0, 'p1_shock_down'), (T['wheels'], 'p1_smile_down'), (C['fum1'] - 0.1, 'p1_shock_down'), (T['chain'] + 0.4, 'p1_smile_down'),
          (T['name'], 'p1_wink_wave'), (T['question'], 'p1_question_down'), (T['cta'], 'p1_wink_wave')]
def face_at(t):
    f = EXPR_T[0][1]
    for s, l in EXPR_T:
        if t >= s: f = l
    return f
lips, prev = [], None
for i, v in enumerate(rms):
    t = round(i / 15, 3)
    r = v / ref
    m = 'closed' if r < 0.12 else ('mid' if r < 0.45 else 'open')
    if m != 'closed' and 'shock' in face_at(t): m = 'oh'
    if m != prev:
        lips.append([t, m]); prev = m
EXPR = [{'t': round(t, 3), 'layer': l, 'prev': EXPR_T[i - 1][1] if i else None} for i, (t, l) in enumerate(EXPR_T)]

# ---- rig placement: full body for hook / name / cta, bust (peeking up from the bottom) while explaining ----
FULL = {'x': 240, 'y': 1150, 's': 0.92}
BUST = {'x': 240, 'y': 1215, 's': 1.25}
RIG = [dict(t=0, **FULL), dict(t=round(T['wheels'], 3), **BUST), dict(t=round(T['name'] - 0.1, 3), **FULL),
       dict(t=round(T['question'], 3), **BUST), dict(t=round(T['cta'], 3), **FULL)]
def head_spot(t):
    mode = FULL
    for r in RIG:
        if t >= r['t']: mode = r
    return (690, 1150) if mode['s'] < 1 else (700, 1215)
POPDEF = [('fx-bang', C['ruko'] + 0.1), ('fx-bang2', C['fum1']), ('fx-snip', C['tootta'] - 0.1), ('fx-bulb', C['chainw']),
          ('fx-spark', C['kbike']), ('fx-q', T['question'] + 0.1), ('fx-heart', C['follow'])]
POPS = [{'id': i, 't': round(t, 3), 'x': head_spot(t)[0], 'y': head_spot(t)[1]} for i, t in POPDEF]

FXSVG = {
    'bang': '<circle cx="85" cy="85" r="66" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><text x="85" y="122" text-anchor="middle" font-family="Bagel Fat One" font-size="104" fill="#432f2e">!</text>',
    'q': '<circle cx="85" cy="85" r="66" fill="#432f2e"/><text x="85" y="120" text-anchor="middle" font-family="Bagel Fat One" font-size="96" fill="#feefb8">?</text>',
    'bulb': '<path d="M85 20 C 45 20 30 55 40 80 C 48 100 62 104 62 124 L 108 124 C 108 104 122 100 130 80 C 140 55 125 20 85 20 Z" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><rect x="62" y="128" width="46" height="22" rx="6" fill="#c4dae8" stroke="#432f2e" stroke-width="6"/><path d="M20 30 L 8 18 M150 30 L 162 18 M85 4 L 85 -8" stroke="#432f2e" stroke-width="8" stroke-linecap="round"/>',
    'snip': '<circle cx="85" cy="85" r="66" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/><text x="85" y="118" text-anchor="middle" font-size="90">✂</text>',
    'spark': '<path d="M85 5 L 102 68 L 165 85 L 102 102 L 85 165 L 68 102 L 5 85 L 68 68 Z" fill="#F6D365" stroke="#432f2e" stroke-width="7" stroke-linejoin="round"/>',
    'heart': '<path d="M85 150 C 20 105 10 70 30 45 C 50 22 78 30 85 52 C 92 30 120 22 140 45 C 160 70 150 105 85 150 Z" fill="#e8743b" stroke="#432f2e" stroke-width="8" stroke-linejoin="round"/>',
}
FX = '\n        '.join(f'<svg id="{i}" class="fx" viewBox="-10 -10 190 190">{FXSVG[i.split("-")[1].rstrip("2")]}</svg>' for i, _ in POPDEF)

LAYERS = sorted({l for _, l in EXPR_T})
BODIES = '\n          '.join(f'<img id="body-{l}" class="body" src="assets/pixy/{l}.svg" alt="" />' for l in LAYERS)
MOUTHS = '\n          '.join(f'<img id="mouth-{m}" class="mouth" src="assets/pixy/mouth_{m}.svg" alt="" />' for m in ['closed', 'mid', 'open', 'oh'])

# ---- captions ----
HL = {'urea', 'krebs', 'fumarate', 'aspartate', 'argininosuccinate', 'bicycle', 'liver', 'neet', 'follow', 'chain', 'enzyme'}
caps = []
for l in V['lines']:
    chunk = []
    for i, wd in enumerate(l['words']):
        chunk.append(wd)
        last = i == len(l['words']) - 1
        if len(chunk) == 3 or last or re.search(r'[,.!?:]$', wd['t']):
            s = l['start'] + chunk[0]['s']
            e = l['start'] + (l['words'][i + 1]['s'] if not last else chunk[-1]['e'] + 0.15)
            caps.append((round(s, 3), round(e - s, 3), chunk)); chunk = []
def cap_html(i, s, d, chunk):
    ws = ' '.join(f'<b class="hl">{x["t"]}</b>' if re.sub(r'[^a-z]', '', x['t'].lower()) in HL else f'<b>{x["t"]}</b>' for x in chunk)
    return f'<div id="cap-{i}" class="cap clip" data-start="{s}" data-duration="{d}" data-track-index="9"><span id="cap-{i}-t" class="capt">{ws}</span></div>'
CAPS = '\n      '.join(cap_html(i, *c) for i, c in enumerate(caps))

SFX = [('pop', C['ruko'], 0.35), ('whoosh', T['wheels'], 0.3), ('pop', C['tootta'], 0.3), ('pop', C['fum1'], 0.35),
       ('whoosh', C['chainw'], 0.3), ('whoosh', C['aspartate'], 0.25), ('chime', C['kbike'], 0.3), ('whoosh', T['question'], 0.3), ('pop', C['follow'], 0.35)]
SFXH = '\n      '.join(f'<audio id="sfx-{i}" class="clip" src="assets/sfx/{k}.mp3" data-start="{round(t, 3)}" data-duration="{2.4 if k == "chime" else 0.7}" data-track-index="{11 + i % 3}" data-volume="{v}"></audio>' for i, (k, t, v) in enumerate(SFX))

html = open(os.path.join(HERE, 'tools/template.html.tpl')).read()
for k, v in {'__CAPS__': CAPS, '__SFX__': SFXH, '__TOTAL__': str(TOTAL), '__BODIES__': BODIES, '__MOUTHS__': MOUTHS, '__FX__': FX,
             '__T__': json.dumps(T), '__CUES__': json.dumps(C), '__LIPS__': json.dumps(lips), '__EXPR__': json.dumps(EXPR),
             '__RIG__': json.dumps(RIG), '__POPS__': json.dumps(POPS)}.items():
    html = html.replace(k, v)
for k, v in T.items():
    html = html.replace(f'@{k}@', str(round(v, 3)))
open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('index.html written; total', TOTAL, 'captions', len(caps), 'mouth changes', len(lips))
