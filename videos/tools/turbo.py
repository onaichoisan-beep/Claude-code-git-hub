"""Turbo edit: turn a finished Field Notebook reel into a fast-paced cut.

  python3 -I videos/tools/turbo.py <project_dir> <source_video> "<next-up label>" "<next-up title>"

Reads <project>/index.html (the calm cut) and <project>/transcript.json, writes
<project>/turbo.html plus assets/voice-turbo.wav, music-turbo.wav, sfx-turbo.wav.

- removes dead air between sentences (every animation time is remapped)
- splits facecam windows into jump cuts with alternating wide/tight framing
- whip + flash + punch-zoom on every scene change, screen shake on stamps
- popping captions, top progress bar, "next up" end card
- recorded SFX from the bundled media-use library, timed to the graphics
"""
import json, os, re, subprocess, sys, wave
import numpy as np

proj, source, next_label, next_title = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.join(HERE, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
SR = 48000
GAP_MAX = 0.16      # pauses longer than this are cut down
PAD_OUT, PAD_IN = 0.07, 0.04
RATE = 1.08         # pitch-corrected speed-up; footage plays at the same rate so lips stay synced
TAIL = 1.5          # end card after the last word

# ---------------- keep-segments from word timings ----------------
words = [w for seg in json.load(open(f"{proj}/transcript.json")) for w in seg["words"]]
segs, s0 = [], 0.0
for a, b in zip(words, words[1:]):
    if b["s"] - a["e"] > GAP_MAX:
        segs.append([s0, a["e"] + PAD_OUT]); s0 = b["s"] - PAD_IN
segs.append([s0, words[-1]["e"] + 0.25])
out_starts, acc = [], 0.0
for a, b in segs:
    out_starts.append(acc); acc += (b - a) / RATE
VOICE_LEN = acc
DUR = round(VOICE_LEN + TAIL, 3)

def M(t):
    for (a, b), o in zip(segs, out_starts):
        if t < a: return round(o, 4)          # inside a removed gap: snap to the cut
        if t <= b: return round(o + (t - a) / RATE, 4)
    return round(VOICE_LEN + (t - segs[-1][1]) / RATE, 4)

orig_len = words[-1]["e"]
print(f"{proj}: {len(segs)} segments, speech {orig_len:.2f}s -> {VOICE_LEN:.2f}s, total {DUR:.2f}s")

# ---------------- voice: concat kept segments ----------------
chain = "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=4000:t=q:w=1:g=2"
parts = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b-a-0.015:.3f}:d=0.015[s{i}];" for i, (a, b) in enumerate(segs))
fc = parts + "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1,atempo={RATE},{chain},apad=whole_dur={DUR}[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", source, "-filter_complex", fc, "-map", "[o]", "-ar", str(SR), "-ac", "2", f"{proj}/assets/voice-turbo.wav"], check=True)

# ---------------- HTML transform ----------------
src = open(f"{proj}/index.html").read()
html = src

def remap_clip(m):
    st, du = float(m.group(2)), float(m.group(3))
    ns, ne = M(st), M(st + du)
    return f'{m.group(1)}data-start="{ns}" data-duration="{round(ne - ns, 4)}"'
html = re.sub(r'(<section [^>]*?)data-start="([\d.]+)" data-duration="([\d.]+)"', remap_clip, html)

# the last scene runs to the end of the video
last = max(re.finditer(r'(<section [^>]*?data-start=")([\d.]+)(" data-duration=")([\d.]+)', html), key=lambda m: float(m.group(2)))
html = html[:last.start(4)] + str(round(DUR - float(last.group(2)), 4)) + html[last.end(4):]

vid_re = re.compile(r'<video id="(\w+)"( class="camvid")? src="assets/facecam.mp4" muted playsinline data-start="([\d.]+)" data-duration="([\d.]+)" data-media-start="([\d.]+)" data-track-index="(\d+)"></video>')
def split_video(m):
    vid, cls, st, du, ms, tr = m.group(1), m.group(2) or "", float(m.group(3)), float(m.group(4)), float(m.group(5)), m.group(6)
    a0, a1 = ms, ms + du
    out, k = [], 0
    for a, b in segs:
        lo, hi = max(a, a0), min(b, a1)
        if hi - lo < 0.05: continue
        zoom = ' style="transform: scale(1.1); transform-origin: 50% 36%"' if cls and k % 2 else ""
        out.append(f'<video id="{vid}-{k}"{cls} src="assets/facecam.mov" muted playsinline data-start="{M(lo)}" data-duration="{round((hi - lo) / RATE, 4)}" data-media-start="{round(lo, 4)}" data-playback-rate="{RATE}" data-track-index="{tr}"{zoom}></video>')
        k += 1
    return "\n    ".join(out)
html = vid_re.sub(split_video, html)

html = re.sub(r'(<div id="root"[^>]*data-duration=")[\d.]+', lambda m: m.group(1) + str(DUR), html)
html = re.sub(r'<audio id="vo" src="assets/voice.wav" data-start="0" data-duration="[\d.]+"', f'<audio id="vo" src="assets/voice-turbo.wav" data-start="0" data-duration="{DUR}"', html)
html = re.sub(r'<audio id="bed" src="assets/music.wav" data-start="0" data-duration="[\d.]+"', f'<audio id="bed" src="assets/music-turbo.wav" data-start="0" data-duration="{DUR}"', html)
html = re.sub(r'<audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="[\d.]+" data-track-index="7" data-volume="[\d.]+"', f'<audio id="sfx" src="assets/sfx-turbo.wav" data-start="0" data-duration="{DUR}" data-track-index="7" data-volume="1"', html)

# wrap everything visual in a shakeable stage; overlays sit above it
root_open = re.search(r'<div id="root"[^>]*>', html)
html = html[:root_open.end()] + '\n<div id="stage">' + html[root_open.end():]
first_audio = html.index("<audio")
overlay = f'''</div>
  <div id="whip"><div class="band b1"></div><div class="band b2"></div></div>
  <div id="flash"></div>
  <div id="progT"></div><div id="prog"></div>
  <div id="endc">
    <div class="mono" style="position:absolute; left:92px; top:700px; font-size:34px; font-weight:700; letter-spacing:.3em; color:#ff8f7f">NEXT IN THE FILE ›</div>
    <div id="endc-l" style="position:absolute; left:92px; top:760px; font-size:110px; color:var(--cream)">{next_label}</div>
    <div id="endc-t" style="position:absolute; left:86px; top:880px; font-size:150px; color:var(--red)">{next_title}</div>
    <div class="mono" style="position:absolute; left:92px; top:1080px; font-size:26px; color:rgba(237,227,204,.7)">7 enzyme classes · one at a time</div>
  </div>
  '''
html = html[:first_audio] + overlay + html[first_audio:]

css = '''
#stage { position: absolute; inset: 0; transform-origin: 50% 45%; }
#whip { position: absolute; inset: 0; z-index: 15; overflow: hidden; pointer-events: none; }
#whip .band { position: absolute; top: -300px; left: 0; width: 640px; height: 2600px; rotate: 14deg; }
#whip .b1 { background: var(--red); }
#whip .b2 { background: var(--dark); width: 260px; }
#flash { position: absolute; inset: 0; z-index: 16; background: #FFF6E2; opacity: 0; }
#progT { position: absolute; left: 0; right: 0; top: 0; height: 10px; z-index: 18; background: rgba(20,14,8,.35); }
#prog { position: absolute; left: 0; top: 0; width: 100%; height: 10px; z-index: 19; background: var(--red); transform-origin: 0 50%; box-shadow: 0 0 12px rgba(192,57,43,.8); }
#endc { position: absolute; inset: 0; z-index: 17; opacity: 0; background: radial-gradient(ellipse 80% 55% at 50% 40%, #3a332b, #1E1B18 70%); }
'''
html = html.replace("</style>", css + "</style>", 1)

# timeline: every authored position goes through M()
html = html.replace("const tl = gsap.timeline({ paused: true });", f'''const SEGS = {json.dumps([[round(a, 4), round(b, 4), round(o, 4)] for (a, b), o in zip(segs, out_starts)])};
const VLEN = {round(VOICE_LEN, 4)};
const RATE = {RATE};
function M(t) {{
  for (const [a, b, o] of SEGS) {{ if (t < a) return o; if (t <= b) return o + (t - a) / RATE; }}
  return VLEN + (t - SEGS[SEGS.length - 1][1]) / RATE;
}}
const TL = gsap.timeline({{ paused: true }});
const tl = {{
  fromTo: (s, a, b, p) => TL.fromTo(s, a, b, M(p)),
  to: (s, a, p) => TL.to(s, a, M(p)),
  set: (s, a, p) => TL.set(s, a, M(p)),
}};''', 1)
html = html.replace('function pushIn(sel, t, d, s0 = 1, s1 = 1.05) { tl.fromTo(sel, { scale: s0 }, { scale: s1, duration: d, ease: "none" }, t); }',
                    'function pushIn(sel, t, d, s0 = 1, s1 = 1.05) { tl.fromTo(sel, { scale: s0 }, { scale: s1 + 0.02, duration: Math.max(0.1, M(t + d) - M(t)), ease: "none" }, t); }', 1)

# captions pop in, the spoken word grows
html = html.replace('tl.fromTo(cap, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.1, ease: "power2.out" }',
                    'tl.fromTo(cap, { opacity: 0, y: 24, scale: 0.78 }, { opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "back.out(2.6)" }')
html = html.replace('{ opacity: 0.3, color: "#2B1D14" }, { opacity: 1, color: "#C0392B", duration: 0.08 }',
                    '{ opacity: 0.3, color: "#2B1D14", y: 0 }, { opacity: 1, color: "#C0392B", y: -7, duration: 0.08 }')
html = html.replace('tl.to(s, { color: "#2B1D14", duration: 0.08 }, next);', 'tl.to(s, { color: "#2B1D14", y: 0, duration: 0.08 }, next);')

# scene changes and stamps, in output time
scene_starts = sorted({M(float(x)) for x in re.findall(r'<section [^>]*?data-start="([\d.]+)"', src)} - {0.0})
slams = sorted({M(float(t)) for t in re.findall(r'slam\("[^"]+", ([\d.]+)\)', src)})
extras = f'''
// ================= turbo layer =================
const CUTS = {json.dumps(scene_starts)};
const SLAMS = {json.dumps(slams)};
TL.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {DUR}, ease: "none" }}, 0);
TL.fromTo("#stage", {{ scale: 1.16 }}, {{ scale: 1, duration: 0.55, ease: "power3.out" }}, 0);
TL.fromTo("#flash", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out" }}, 0);
CUTS.forEach((c, i) => {{
  const ir = i > 0 ? {{ immediateRender: false }} : {{}};
  TL.fromTo("#whip .b1", {{ x: -1500 }}, {{ x: 1700, duration: 0.34, ease: "power2.inOut", ...ir }}, c - 0.17);
  TL.fromTo("#whip .b2", {{ x: -1700 }}, {{ x: 1500, duration: 0.34, ease: "power2.inOut", ...ir }}, c - 0.13);
  TL.fromTo("#flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.18, immediateRender: false }}, c);
  TL.fromTo("#stage", {{ scale: 1.07 }}, {{ scale: 1, duration: 0.32, ease: "power2.out", immediateRender: false }}, c);
}});
SLAMS.forEach((t) => {{
  TL.to("#stage", {{ x: 11, y: -8, duration: 0.035, yoyo: true, repeat: 5, ease: "none" }}, t + 0.16);
  TL.set("#stage", {{ x: 0, y: 0 }}, t + 0.38);
}});
TL.fromTo("#endc", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {round(VOICE_LEN + 0.1, 3)});
TL.fromTo("#endc-l", {{ opacity: 0, x: -200 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {round(VOICE_LEN + 0.2, 3)});
TL.fromTo("#endc-t", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "power3.in" }}, {round(VOICE_LEN + 0.45, 3)});
window.__timelines["main"] = TL;'''
html = html.replace('window.__timelines["main"] = tl;', extras, 1)
open(f"{proj}/turbo.html", "w").write(html)

# ---------------- SFX from the bundled library ----------------
def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX_DIR, name), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)
LIB = {k: load(k + ".mp3") for k in ["whoosh-short", "whoosh", "impact-bass-1", "pop", "key-press", "sparkle", "ping", "glitch-3", "click-soft"]}
N = int(DUR * SR); sfx = np.zeros(N, np.float32)
def add(t, name, g):
    x = LIB[name]; s = int(max(0, t) * SR); L = min(len(x), N - s)
    if L > 0: sfx[s:s + L] += x[:L] * g

ev = []  # (time, kind)
for t in re.findall(r'slam\("[^"]+", ([\d.]+)\)', src): ev.append((M(float(t)), "stamp"))
for t in re.findall(r'\bpop\("[^"]+", ([\d.]+)', src): ev.append((M(float(t)), "pop"))
for t in re.findall(r'\bdrop\("[^"]+", ([\d.]+)\)', src): ev.append((M(float(t)), "drop"))
for t in re.findall(r'\bhop\("[^"]+", ([\d.]+)', src): ev.append((M(float(t)), "hop"))
for t in re.findall(r'"#b-name", \{[^}]*\}, \{[^}]*\}, ([\d.]+)\)', src): ev.append((M(float(t)), "reveal"))
for t in re.findall(r'"#pip", \{ opacity: 0, scale: 0\.4 \}, \{[^}]*\}, ([\d.]+)\)', src): ev.append((M(float(t)), "pop"))
for t in re.findall(r'flapRoll\([^,]+, ([\d.]+)', src): ev.append((M(float(t)), "flap"))
for t in re.findall(r'draw\("#\w-circ", ([\d.]+)', src): ev.append((M(float(t)), "circle"))
ev.sort()
last_t = -1
for t, kind in ev:
    if kind in ("pop", "drop", "hop", "flap", "circle") and t - last_t < 0.14: continue
    if kind == "stamp": add(t + 0.12, "impact-bass-1", 0.42); add(t + 0.12, "click-soft", 0.35)
    elif kind == "reveal": add(t - 0.05, "whoosh", 0.4)
    elif kind == "pop": add(t, "pop", 0.22)
    elif kind == "drop": add(t, "whoosh-short", 0.14)
    elif kind == "hop": add(t, "whoosh-short", 0.18)
    elif kind == "circle": add(t, "ping", 0.16)
    elif kind == "flap":
        for k in range(4): add(t + k * 0.06, "key-press", 0.22)
    last_t = t
for c in scene_starts: add(c - 0.2, "whoosh-short", 0.45)
add(0.0, "impact-bass-1", 0.5); add(0.0, "glitch-3", 0.12)
add(VOICE_LEN + 0.15, "whoosh", 0.45); add(VOICE_LEN + 0.45, "impact-bass-1", 0.35); add(VOICE_LEN + 0.5, "sparkle", 0.22)
peak = np.abs(sfx).max()
if peak > 0.6: sfx *= 0.6 / peak
w = wave.open(f"{proj}/assets/sfx-turbo.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.repeat(np.clip(sfx, -1, 1)[:, None], 2, 1) * 32767).astype(np.int16).tobytes()); w.close()
json.dump({"duration": DUR, "thud": [], "stamp": [], "whoosh": [], "ticks": []}, open(f"{proj}/events-turbo.json", "w"))
print(f"  {len(scene_starts)} cuts, {len(slams)} stamps, {len(ev)} sfx cues")
