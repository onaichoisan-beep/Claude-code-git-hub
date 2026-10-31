"""Vertical YouTube Short (1080x1920) cut from the base clips: curiosity beats only, ending on a
"watch the full video" card that points at the Shorts related-video link. Writes short.html."""
import html, json, os, re

KIT = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(KIT, "fonts.css")).read().replace("../assets/", "assets/")
E = html.escape

# (clip, from, to, headline html) — headlines tease, never name the method
SEGS = [
    ("06", 0.00, 6.72, '<span class="g">₹80,000</span> in 1st year MBBS'),
    ("08", 8.00, 10.45, '4 ways. <span class="r">zero</span> investment.'),
    ("01", 2.15, 8.70, 'way 1: <span class="g">₹60K+</span> … faceless?'),
    ("02", 11.05, 18.30, 'way 2: paid at <span class="g">800</span> subs'),
    ("03", 0.00, 4.25, 'way 3: you <span class="r">already</span> have it'),
    ("04", 2.85, 10.50, 'way 4: <span class="g">₹3–4K</span> per project'),
    ("10", 15.45, 18.75, 'more skill = <span class="g">more money</span>'),
]
END = 3.2
KEYS = {"80000": "g", "60k": "g", "800": "g", "faceless": "r", "-4k": "g", "money.": "g", "money,": "g", "4": "r"}
FIX = {"80000": "₹80,000", "60k": "₹60K", "-4k": "₹3–4K", "3": ""}


def norm(w):
    return re.sub(r"[^a-z0-9₹+-]", "", w.lower())


js, vids, caps, sfx, heads = [], [], [], [], []
t = 0.0
lane_end = []


def add_sfx(at, name, vol, dur):
    k = next((j for j, e in enumerate(lane_end) if e <= at), None)
    if k is None:
        lane_end.append(0); k = len(lane_end) - 1
    lane_end[k] = at + dur
    sfx.append(f'<audio id="sfx{len(sfx)}" class="clip" src="assets/sfx/{name}.mp3" data-start="{at:.3f}" '
               f'data-duration="{dur:.3f}" data-track-index="{10 + k}" data-volume="{vol}"></audio>')


for i, (clip, a, b, head) in enumerate(SEGS):
    d = b - a
    vids.append(f'<video id="v{i}" class="clip" src="assets/video/clip{clip}.mp4" playsinline data-has-audio="true" '
                f'data-start="{t:.3f}" data-duration="{d:.3f}" data-media-start="{a:.3f}" data-track-index="0" data-volume="1"></video>')
    heads.append(f'<div id="h{i}" class="head"><div>{head}</div></div>')
    js.append(f'tl.set("#cam",{{scale:{[1.0, 1.12][i % 2]}}},{t:.3f});')
    js.append(f'tl.fromTo("#h{i}",{{opacity:0,y:30,scale:.92}},{{opacity:1,y:0,scale:1,duration:.22,ease:"back.out(2)"}},{t:.3f});')
    js.append(f'tl.set("#h{i}",{{opacity:0}},{t + d:.3f});')
    if i:
        add_sfx(max(0, t - .12), "whoosh-short", .4, .6)
    add_sfx(t + .02, "impact-bass-1", .35, 1.4)
    # word captions, 1–2 words per beat, keyword beats on their own
    words = [w for w in json.load(open(f"../work/base/clip{clip}.words.json")) if a - .02 <= w["s"] < b - .05]
    groups, cur = [], []
    for w in words:
        k = KEYS.get(norm(w["w"]))
        if k:
            if cur: groups.append((cur, None)); cur = []
            groups.append(([w], k)); continue
        cur.append(w)
        if len(cur) >= 2 or len(" ".join(x["w"] for x in cur)) > 11 or re.search(r"[.,?!]$", w["w"]):
            groups.append((cur, None)); cur = []
    if cur: groups.append((cur, None))
    for gi, (ws, k) in enumerate(groups):
        s = ws[0]["s"] - a + t
        e = (groups[gi + 1][0][0]["s"] - a + t) if gi + 1 < len(groups) else t + d
        e = min(e, ws[-1]["e"] - a + t + .35, t + d)
        txt = " ".join(FIX.get(norm(x["w"]), x["w"]) for x in ws).strip(" ,").rstrip(".")
        if not txt or e - s < .08:
            continue
        cid = f"c{len(caps)}"
        caps.append(f'<div id="{cid}" class="cap {"key " + k if k else ""}"><span>{E(txt)}</span></div>')
        js.append(f'tl.fromTo("#{cid}",{{opacity:0,scale:{.7 if k else .88}}},{{opacity:1,scale:1,duration:.12,ease:"back.out(2.5)"}},{s:.3f});')
        js.append(f'tl.set("#{cid}",{{opacity:0}},{e:.3f});')
    t += d

body_end = t
dur = t + END
add_sfx(body_end - 1.0, "riser", .3, 1.0)
add_sfx(body_end, "impact-bass-2", .55, 2.2)
add_sfx(body_end + .9, "pop", .45, .7)
js.append(f'tl.fromTo("#bar",{{scaleX:0}},{{scaleX:1,duration:{body_end:.3f},ease:"none"}},0);')
js.append(f'tl.set("#endc",{{opacity:1}},{body_end:.3f});')
js.append(f'tl.fromTo("#endc .e1",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{body_end + .05:.3f});')
js.append(f'tl.fromTo("#endc .e2",{{opacity:0,scale:1.6,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.35,ease:"power3.out"}},{body_end + .2:.3f});')
js.append(f'tl.fromTo("#endc .e3",{{opacity:0}},{{opacity:1,duration:.3}},{body_end + .6:.3f});')
js.append(f'tl.fromTo("#endc .arrow",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{body_end + .9:.3f});')
js.append(f'tl.to("#endc .arrow",{{y:26,duration:.45,ease:"sine.inOut",yoyo:true,repeat:3}},{body_end + 1.25:.3f});')

page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<title>short</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{FONTS}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0a; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; color: #fff;
  background: radial-gradient(ellipse at 50% 45%, #3a0508 0%, #140203 50%, #050505 100%); }}
#bar {{ position: absolute; left: 0; top: 0; width: 100%; height: 12px; background: #e0141e; transform-origin: 0 50%; box-shadow: 0 0 20px rgba(255,42,42,.8); }}
#win {{ position: absolute; left: 40px; right: 40px; top: 330px; height: 1250px; border-radius: 36px; overflow: hidden;
  box-shadow: 0 0 0 4px rgba(255,255,255,.12), 0 40px 90px rgba(0,0,0,.7); }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 30%; }}
#cam video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%;
  filter: contrast(1.08) saturate(1.12); }}
.head {{ position: absolute; left: 50px; right: 50px; top: 50px; height: 260px; display: flex; align-items: center; justify-content: center;
  text-align: center; font-family: "Anton", sans-serif; font-size: 108px; line-height: .98; text-transform: uppercase; opacity: 0; }}
.g {{ color: #d8ff4f; text-shadow: 0 0 30px rgba(216,255,79,.45); }} .r {{ color: #ff2a2a; text-shadow: 0 0 30px rgba(255,42,42,.5); }}
#caps {{ position: absolute; left: 40px; right: 40px; top: 1360px; height: 200px; }}
.cap {{ position: absolute; inset: 0; display: flex; justify-content: center; align-items: center; opacity: 0; }}
.cap span {{ font-weight: 900; font-size: 86px; letter-spacing: -2px; white-space: nowrap; text-shadow: 0 6px 24px rgba(0,0,0,.85), 0 2px 2px rgba(0,0,0,.6); }}
.cap.key span {{ font-family: "Anton", sans-serif; font-weight: 400; font-size: 130px; letter-spacing: 1px; text-transform: uppercase; }}
.cap.g span {{ color: #d8ff4f; }} .cap.r span {{ color: #ff2a2a; }}
.sub {{ position: absolute; left: 0; right: 0; top: 1640px; text-align: center; font-family: "JetBrains Mono", monospace; font-weight: 700;
  font-size: 30px; letter-spacing: 6px; color: rgba(255,255,255,.55); text-transform: uppercase; }}
#endc {{ position: absolute; inset: 0; opacity: 0; display: flex; flex-direction: column; align-items: center; padding-top: 420px;
  background: radial-gradient(ellipse at 50% 40%, #4a060b 0%, #120203 55%, #050505 100%); }}
#endc .e1 {{ font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 40px; letter-spacing: 10px; color: #ff2a2a; }}
#endc .e2 {{ margin-top: 30px; font-family: "Anton", sans-serif; font-size: 200px; line-height: .92; text-align: center; text-transform: uppercase; }}
#endc .e3 {{ margin-top: 40px; font-weight: 800; font-size: 50px; text-align: center; line-height: 1.25; color: #d8ff4f; }}
#endc .arrow {{ position: absolute; left: 120px; top: 1330px; width: 200px; height: 260px; }}
</style></head>
<body>
<div id="root" data-composition-id="short" data-start="0" data-duration="{dur:.3f}" data-width="1080" data-height="1920">
  <div id="bar"></div>
  {chr(10).join("  " + h for h in heads)}
  <div id="win"><div id="cam">
    {chr(10).join("    " + v for v in vids)}
  </div></div>
  <div id="caps">
{chr(10).join("    " + c for c in caps)}
  </div>
  <div class="sub">full video ↓ related video</div>
  <div id="endc">
    <div class="e1">ALL 4 WAYS + EXACT STEPS</div>
    <div class="e2">watch the<br>full video</div>
    <div class="e3">tap the link below ⬇</div>
    <svg class="arrow" viewBox="0 0 200 260"><path d="M100 10 V220" stroke="#d8ff4f" stroke-width="26" stroke-linecap="round"/>
      <path d="M30 160 L100 236 L170 160" stroke="#d8ff4f" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>
{chr(10).join("  " + s for s in sfx)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["short"] = tl;
</script>
</body></html>
"""
open("short.html", "w").write(page)
print(f"short.html {dur:.1f}s, {len(caps)} captions")
