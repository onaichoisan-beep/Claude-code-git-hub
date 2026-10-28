#!/usr/bin/env python3
"""Generates index.html from the voice timing (assets/audio/vo_timing.json).

Re-run after regenerating the voice-over so every cue stays on its word.
"""
import json, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(os.path.join(HERE, 'assets/audio/vo_timing.json')))
LINES = {l['key']: l for l in V['lines']}
TOTAL = V['total']

def kw(key, word, which=0, end=False):
    """Absolute time of the n-th word in a line whose text starts with `word`."""
    l = LINES[key]
    hits = [w for w in l['words'] if re.sub(r'[^a-z]', '', w['t'].lower()).startswith(word.lower())]
    w = hits[which]
    return round(l['start'] + (w['e'] if end else w['s']), 3)

def start(key): return LINES[key]['start']
def stop(key): return round(LINES[key]['start'] + LINES[key]['dur'], 3)

T = {
    'hook': 0, 'wheels': start('wheels') - 0.1, 'step1': start('step1'), 'step2': start('step2'),
    'chain': start('chain'), 'back': start('back'), 'name': start('name') - 0.1,
    'question': start('question') - 0.15, 'cta': start('cta') - 0.1, 'end': TOTAL,
}
CUES = {
    'ruko': kw('hook', 'ruko'), 'liver': kw('hook', 'liver'), 'bicycle': kw('hook', 'bicycle'),
    'urea1': kw('wheels', 'urea'), 'krebs1': kw('wheels', 'krebs'),
    'citrulline': kw('step1', 'citrulline'), 'aspartate': kw('step1', 'aspartate'), 'asa': kw('step1', 'argininosuccinate'),
    'lyase': kw('step2', 'lyase'), 'todta': kw('step2', 'todta'), 'arginine': kw('step2', 'arginine'), 'fum1': kw('step2', 'fumarate'),
    'chain': kw('chain', 'chain'), 'krebs2': kw('chain', 'krebs'), 'malate': kw('chain', 'malate'), 'oaa': kw('chain', 'oxaloacetate'),
    'transam': kw('back', 'transamination'), 'asp2': kw('back', 'aspartate'), 'urea3': kw('back', 'urea'),
    'kbicycle': kw('name', 'krebs'), 'fum3': kw('name', 'fumarate'),
    'neet': kw('question', 'neet'), 'enzyme': kw('question', 'enzyme'),
    'comment': kw('cta', 'comment'), 'agli': kw('cta', 'agli'), 'follow': kw('cta', 'follow'), 'scroll': kw('cta', 'scroll'),
}

# ---- captions: chunks of up to 3 words, breaking after punctuation ----
HL = {'urea', 'krebs', 'fumarate', 'aspartate', 'citrulline', 'argininosuccinate', 'arginine', 'malate',
      'oxaloacetate', 'bicycle', 'liver', 'transamination', 'lyase', 'neet', 'follow', 'chain', 'enzyme', 'score'}
caps = []
for l in V['lines']:
    chunk = []
    for i, w in enumerate(l['words']):
        chunk.append(w)
        last = i == len(l['words']) - 1
        if len(chunk) == 3 or last or re.search(r'[,.!?:]$', w['t']):
            s = l['start'] + chunk[0]['s']
            e = l['start'] + (l['words'][i + 1]['s'] if not last else chunk[-1]['e'] + 0.15)
            caps.append((round(s, 3), round(e - s, 3), chunk))
            chunk = []
def cap_html(i, s, d, chunk):
    words = []
    for w in chunk:
        bare = re.sub(r'[^A-Za-z]', '', w['t']).lower()
        cls = ' class="hl"' if bare in HL else ''
        words.append(f'<b{cls}>{w["t"]}</b>')
    return (f'<div id="cap-{i}" class="cap clip" data-start="{s}" data-duration="{d}" data-track-index="9">'
            f'<span id="cap-{i}-t" class="capt">{" ".join(words)}</span></div>')
CAPS = '\n      '.join(cap_html(i, *c) for i, c in enumerate(caps))

# ---- pixy expression windows ----
PIXY = [('p1_shock', T['hook'], T['wheels']), ('p4_smile', T['wheels'], T['step2']), ('p4_grin', T['step2'], T['chain']),
        ('p4_smile', T['chain'], T['name']), ('p4_wink', T['name'], T['question']), ('p1_question', T['question'], T['cta']),
        ('p1_wink', T['cta'], T['end'])]
PIX = '\n      '.join(
    f'<div id="pixy-{i}" class="pixy clip" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="8">'
    f'<img id="pixy-{i}-img" src="assets/pixy/{n}.svg" alt=""></div>' for i, (n, s, e) in enumerate(PIXY))

# ---- sound effects ----
SFX_FILES = {'whoosh': 'assets/sfx/whoosh.mp3', 'pop': 'assets/sfx/pop.mp3',
             'ding': 'assets/sfx/chime.mp3', 'snip': 'assets/sfx/snip.mp3'}
SFX = [('pop', CUES['ruko'] - 0.05, 0.35), ('whoosh', T['wheels'], 0.3), ('pop', CUES['aspartate'], 0.3),
       ('pop', CUES['asa'], 0.3), ('snip', CUES['todta'], 0.45), ('pop', CUES['fum1'], 0.35),
       ('whoosh', CUES['chain'], 0.3), ('pop', CUES['malate'], 0.25), ('pop', CUES['oaa'], 0.25),
       ('whoosh', CUES['transam'], 0.25), ('ding', CUES['kbicycle'], 0.3), ('whoosh', T['question'], 0.3),
       ('pop', CUES['follow'], 0.35)]
sfx_tags = []
for i, (k, t, vol) in enumerate(SFX):
    f = SFX_FILES[k]
    if not os.path.exists(os.path.join(HERE, f)):
        continue
    dur = 2.4 if k == 'ding' else 0.7
    sfx_tags.append(f'<audio id="sfx-{i}" class="clip" src="{f}" data-start="{round(t, 3)}" data-duration="{dur}" '
                    f'data-track-index="{11 + i % 3}" data-volume="{vol}"></audio>')
SFXH = '\n      '.join(sfx_tags)

html = open(os.path.join(HERE, 'tools/template.html.tpl')).read()
for k, v in {'__CAPS__': CAPS, '__PIXY__': PIX, '__SFX__': SFXH, '__TOTAL__': str(TOTAL),
             '__T__': json.dumps(T), '__CUES__': json.dumps(CUES)}.items():
    html = html.replace(k, v)
for k, v in T.items():
    html = html.replace(f'@{k}@', str(round(v, 3)))
open(os.path.join(HERE, 'index.html'), 'w').write(html)
print('index.html written; total', TOTAL, 'captions', len(caps), 'sfx', len(sfx_tags))
