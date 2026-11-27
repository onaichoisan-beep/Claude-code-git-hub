"""Generate index.html from beats.json (the beats approved in the Reel Builder).

Run:  python3 build.py
"""
import html
import json

from PIL import Image

W, H, DUR = 1080, 1920, 38.6
VID = 37.6
beats = json.load(open("beats.json"))

SFX = {
    "Pop": ("pop.mp3", 0.49, 0.32),
    "Whoosh": ("whoosh-a.mp3", 0.33, 0.38),
    "Swish": ("swish.mp3", 0.3, 0.35),
    "Sparkle": ("sparkle.mp3", 1.3, 0.45),
    "Click": ("click.mp3", 0.05, 0.5),
    "Ding": ("ding.mp3", 1.6, 0.22),
    "Record scratch": ("scratch.mp3", 0.4, 0.4),
    "Camera shutter": ("click.mp3", 0.05, 0.5),
}
SONG_NO = {"b02": "No. 1", "b04": "No. 2", "b05": "No. 3", "b07": "No. 4", "b09": "bonus", "b12": "No. 5"}
FRAMED = 0.74

# Picture-card spots per count for the "pictures" layout: (left, top, width, rotation)
PIC_SPOTS = {
    1: [(180, 560, 720, -2)],
    2: [(60, 520, 560, -5), (460, 900, 560, 4)],
    3: [(50, 520, 520, -6), (510, 620, 500, 5), (200, 1010, 580, -2)],
}
# One picture shown on top of the talking head (framed / full layouts)
PIC_OVER = {"framed": (30, 1120, 360, -5), "full": (650, 1420, 340, 5)}
# Sticker spots at the edges, away from the face: (left, top, width, rotation)
STK_SPOTS = [(-10, 960, 290, -8), (800, 800, 280, 7), (30, 1320, 270, 6), (770, 1290, 290, -6)]
STK_SPOTS_FULL = [(10, 1400, 280, -8), (790, 1150, 260, 7), (380, 1560, 260, 6), (60, 650, 240, -6)]
CAP_TOP = {"framed": 330, "pictures": 300, "full": 960}


def img_h(path, w):
    iw, ih = Image.open(path).size
    return round(w * ih / iw)


out = []
js = []
audio = []
aid = 0


def add_sfx(name, t):
    global aid
    if name not in SFX:
        return
    f, d, v = SFX[name]
    t = max(0.0, round(t, 3))
    d = min(d, DUR - t)
    aid += 1
    audio.append(
        f'<audio id="sfx-{aid:02d}" class="clip" src="assets/sfx/{f}" data-start="{t}" '
        f'data-duration="{round(d, 3)}" data-track-index="{20 + aid}" data-volume="{v}"></audio>'
    )


prev_layout = None
for i, b in enumerate(beats):
    bid, s, e, lay = b["id"], b["start"], b["end"], b.get("layout", "full")
    last = i == len(beats) - 1
    if last:
        e = DUR
    exit_t = e - 0.18

    # ---- talking-head frame state
    if lay == "full":
        state = "{scale:1, y:0, opacity:1, borderWidth:0, borderRadius:0}"
    elif lay == "framed":
        state = f"{{scale:{FRAMED}, y:150, opacity:1, borderWidth:14, borderRadius:44}}"
    else:
        state = f"{{scale:{FRAMED * 0.9}, y:150, opacity:0, borderWidth:14, borderRadius:44}}"
    dur = 0.9 if i == 0 else 0.45
    js.append(f'tl.to("#face", Object.assign({state}, {{duration:{dur}, ease:"power3.out"}}), {s});')
    if lay == "framed":  # slow drift so a framed shot never sits still
        js.append(f'tl.to("#face", {{scale:{FRAMED - 0.025}, duration:{round(e - s - dur, 2)}, ease:"none"}}, {s + dur});')
    if last:  # ending card: shrink the clip away, text and stickers stay
        js.append(f'tl.to("#face", {{scale:0.6, opacity:0, borderWidth:14, borderRadius:44, duration:0.5, ease:"power2.in"}}, {VID - 0.45});')
    if lay == "full":  # gentle punch-in for emphasis
        js.append(f'tl.to("#face-in", {{scale:1.1, duration:{round(e - s, 2)}, ease:"power1.inOut"}}, {s});')
        js.append(f'tl.set("#face-in", {{scale:1}}, {e});')

    events = []  # moments for pops

    # ---- pictures
    pics = b.get("pictures", [])
    if lay == "pictures":
        spots = PIC_SPOTS[min(3, max(1, len(pics)))] if pics else []
    else:
        spots = [PIC_OVER["framed" if lay == "framed" else "full"]] if pics else []
        pics = pics[:1]
    for j, (pid, sp) in enumerate(zip(pics, spots)):
        x, y, w, r = sp
        h = img_h(f"assets/img/{pid}.jpg", w - 24)
        eid = f"{bid}-pic{j}"
        out.append(
            f'<div id="{eid}" class="pic" style="left:{x}px;top:{y}px;width:{w}px">'
            f'<img src="assets/img/{pid}.jpg" style="height:{h}px" alt=""></div>'
        )
        t = s + 0.15 + j * 0.35
        events.append(t)
        js.append(f'tl.fromTo("#{eid}", {{opacity:0, scale:0.4, rotation:{r - 14}}}, {{opacity:1, scale:1, rotation:{r}, duration:0.42, ease:"back.out(1.8)"}}, {round(t, 3)});')
        js.append(f'tl.to("#{eid}", {{y:-14, duration:{round(e - t - 0.6, 2)}, ease:"sine.inOut"}}, {round(t + 0.42, 3)});')
        if not last:
            js.append(f'tl.to("#{eid}", {{opacity:0, scale:0.85, duration:0.18, ease:"power2.in"}}, {round(exit_t, 3)});')

    # ---- stickers (pop in, then wiggle)
    for j, sid in enumerate(b.get("stickers", [])[:4]):
        x, y, w, r = (STK_SPOTS_FULL if lay == "full" else STK_SPOTS)[j]
        eid = f"{bid}-st{j}"
        out.append(f'<div id="{eid}" class="stk" style="left:{x}px;top:{y}px;width:{w}px"><img id="{eid}-i" src="assets/st/{sid}.png" alt=""></div>')
        t = s + 0.3 + j * 0.22
        events.append(t)
        js.append(f'tl.fromTo("#{eid}", {{opacity:0, scale:0, rotation:{r - 20}}}, {{opacity:1, scale:1, rotation:{r}, duration:0.4, ease:"back.out(2.6)"}}, {round(t, 3)});')
        period = 0.55 + 0.07 * j
        reps = max(1, int((e - t - 0.4) / period))
        sign = 1 if j % 2 == 0 else -1
        js.append(
            f'tl.fromTo("#{eid}-i", {{rotation:{-6 * sign}, y:0, scale:1}}, {{rotation:{6 * sign}, y:-8, scale:1.05, duration:{period:.2f}, '
            f'ease:"sine.inOut", yoyo:true, repeat:{reps}}}, {round(t + 0.4, 3)});'
        )
        if not last:
            js.append(f'tl.to("#{eid}", {{opacity:0, scale:0.3, duration:0.16, ease:"power2.in"}}, {round(exit_t, 3)});')

    # ---- caption (word by word)
    cap = (b.get("caption") or "").strip()
    cap_t = s + 0.08
    if cap:
        color = b.get("color", "butter")
        hand = " hand" if b.get("hand") else ""
        size = 88 if len(cap) <= 18 else (76 if len(cap) <= 26 else 66)
        if lay == "full":
            size = min(size, 74)
        if hand:
            size = int(size * 1.15)
        words = "".join(f'<span class="w">{html.escape(wd)}</span> ' for wd in cap.split())
        label = SONG_NO.get(bid)
        lab = f'<div class="no" id="{bid}-no">{label}</div>' if label else ""
        out.append(
            f'<div id="{bid}-cap" class="cap {color}{hand}{' low' if lay == 'full' else ''}" style="top:{CAP_TOP[lay]}px;font-size:{size}px">{lab}<div class="txt">{words.strip()}</div></div>'
        )
        if label:
            js.append(f'tl.fromTo("#{bid}-no", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3, ease:"power2.out"}}, {round(cap_t, 3)});')
        js.append(
            f'tl.fromTo("#{bid}-cap .w", {{opacity:0, y:36, scale:0.8}}, {{opacity:1, y:0, scale:1, duration:0.32, '
            f'ease:"back.out(2.2)", stagger:0.07}}, {round(cap_t + 0.05, 3)});'
        )
        if not last:
            js.append(f'tl.to("#{bid}-cap", {{opacity:0, y:-18, duration:0.16, ease:"power2.in"}}, {round(exit_t, 3)});')
        else:  # ending card: lift the last line to the middle and enlarge it
            js.append(f'tl.to("#{bid}-cap", {{y:-260, scale:1.35, duration:0.6, ease:"back.out(1.6)"}}, {VID - 0.2});')

    # ---- sound effects, timed to what happens on screen
    for name in b.get("sfx", []):
        if name in ("Whoosh", "Swish"):
            add_sfx(name, s - 0.08)
        elif name == "Pop":
            for t in (events or [s + 0.3])[:3]:
                add_sfx("Pop", t)
        elif name in ("Click", "Camera shutter"):
            add_sfx(name, cap_t + 0.05)
        elif name == "Sparkle":
            add_sfx(name, cap_t)
        elif name == "Ding":
            add_sfx(name, cap_t + 0.25)
        elif name == "Record scratch":
            add_sfx(name, s + 0.35)
    prev_layout = lay

page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/instrument-serif-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
      @font-face {{ font-family: "Caveat"; src: url("assets/fonts/caveat-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
      @font-face {{ font-family: "DM Sans"; src: url("assets/fonts/dm-sans-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
      :root {{
        --butter: #F7EFA0;
        --blue: #2F5FD0;
        --navy: #1D3E96;
        --cream: #FFFDF0;
        --ground: #F8EFB8;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--ground); }}
      #bg {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #face {{ position: absolute; inset: 0; overflow: hidden; border: 0 solid #fff; box-shadow: 0 30px 60px rgba(29, 62, 150, 0.28); transform-origin: 50% 50%; }}
      #face-in {{ position: absolute; inset: 0; transform-origin: 50% 30%; }}
      #rf {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .pic {{ position: absolute; background: #fff; padding: 12px; box-shadow: 0 18px 40px rgba(29, 62, 150, 0.3); opacity: 0; }}
      .pic img {{ display: block; width: 100%; object-fit: cover; }}
      .stk {{ position: absolute; opacity: 0; }}
      .stk img {{ display: block; width: 100%; filter: drop-shadow(0 10px 14px rgba(29, 62, 150, 0.3)); }}
      .cap {{ position: absolute; left: 120px; right: 192px; text-align: center; font-family: "Instrument Serif", serif; line-height: 1.02; }}
      .cap .txt {{ text-wrap: balance; }}
      .cap.low {{ right: 300px; }}
      .cap .w {{ display: inline-block; paint-order: stroke fill; }}
      .cap.butter .w {{ color: var(--butter); -webkit-text-stroke: 7px var(--navy); text-shadow: 0 5px 0 var(--navy), 0 10px 24px rgba(29, 62, 150, 0.45); }}
      .cap.blue .w {{ color: var(--blue); -webkit-text-stroke: 9px var(--cream); text-shadow: 0 8px 22px rgba(29, 62, 150, 0.25); }}
      .cap.hand {{ font-family: "Caveat", cursive; font-weight: 700; line-height: 0.95; }}
      .cap .no {{ display: inline-block; margin-bottom: 14px; padding: 8px 26px; border-radius: 999px; background: var(--blue); color: var(--butter);
        font-family: "DM Sans", sans-serif; font-weight: 700; font-size: 34px; letter-spacing: 0.06em; text-transform: uppercase; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <img id="bg" src="assets/img/bg.jpg" alt="" />
      <div id="face"><div id="face-in">
        <video id="rf" class="clip" src="assets/video/rf.mp4" data-start="0" data-duration="{VID}" data-track-index="1" muted playsinline></video>
      </div></div>
      {chr(10).join('      ' + o for o in out).strip()}
      <audio id="vo" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="{VID}" data-track-index="10" data-volume="1"></audio>
      {chr(10).join('      ' + a for a in audio).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#face", {{ scale: 1, y: 0, opacity: 1, borderWidth: 0, borderRadius: 0 }}, 0);
      tl.set("#face-in", {{ scale: 1 }}, 0);
      {chr(10).join('      ' + j for j in js).strip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(page)
print(f"wrote index.html: {len(out)} overlays, {len(audio)} sound effects")
