"""Generate index.html from beats.json (the beats approved in the Reel Builder).

Run:  python3 build.py

Layout rules (from feedback):
- Straight, bold sans text (Inter Tight, Helvetica-style). No italics, no handwriting.
- Nothing tilted: pictures and stickers rest straight (stickers still wiggle).
- No sticker overlaps another sticker or a picture.
- Everything sits inside the area the app leaves clear (no captions/buttons over it).
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
SONG_NO = {"b02": "No. 1", "b04": "No. 2", "b05": "No. 3", "b07": "No. 4", "b09": "Bonus", "b12": "No. 5"}

# The framed talking head: a card fully inside the clear area.
FR_S = 0.56
FR_W, FR_H = round(W * FR_S), round(H * FR_S)          # 605 x 1075
FR_X, FR_Y = (W - FR_W) // 2, 430                      # 237..842, 430..1505
FR_DY = FR_Y + FR_H / 2 - H / 2                         # translate from centre

CAP_TOP = {"framed": 300, "pictures": 300, "full": 980}
PIC_BAND = (450, 1470)        # pictures layout band (top, bottom)
PIC_BAND_STK = (450, 1270)    # leave a strip for stickers
PIC_X = (130, 900)

# Candidate sticker spots (left, top, width), first free one wins.
STK_CAND = {
    "framed": [(40, 470, 220), (690, 880, 190), (40, 1150, 220), (690, 1240, 190), (40, 820, 200)],
    "full": [(130, 1180, 200), (700, 1200, 190), (430, 1210, 180), (700, 330, 160)],
    "pictures": [(150, 1290, 170), (560, 1290, 170), (360, 1290, 170), (740, 1290, 150)],
}
PIC_OVER = {"framed": (70, 1110, 250), "full": (620, 1170, 250)}


def size(path):
    return Image.open(path).size


def inter(a, b, m=12):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw + m <= bx or bx + bw + m <= ax or ay + ah + m <= by or by + bh + m <= ay)


def pack_pictures(ids, band):
    """Rows of straight cards (1 / 2 / 2+1), scaled to fit the band, centred."""
    top, bot = band
    rows = [[0]] if len(ids) == 1 else [[0, 1]] if len(ids) == 2 else [[0, 1], [2]]
    gap, pad = 34, 12
    base_w = 600 if len(ids) == 1 else 360
    dims = [size(f"assets/img/{i}.jpg") for i in ids]

    def layout(scale):
        w = base_w * scale
        out, y = [], 0
        for r in rows:
            hs = [w * dims[k][1] / dims[k][0] + 2 * pad for k in r]
            rw = len(r) * (w + 2 * pad) + (len(r) - 1) * gap
            x0 = (PIC_X[0] + PIC_X[1]) / 2 - rw / 2
            for n, k in enumerate(r):
                out.append((k, x0 + n * (w + 2 * pad + gap), y, w + 2 * pad, hs[n]))
            y += max(hs) + gap
        return out, y - gap

    scale = 1.0
    while True:
        cards, total = layout(scale)
        if total <= bot - top or scale < 0.4:
            break
        scale *= 0.95
    y0 = top + ((bot - top) - total) / 2
    return [(ids[k], round(x), round(y0 + y), round(w), round(h)) for k, x, y, w, h in cards]


out, js, audio = [], [], []
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
        state = f"{{scale:{FR_S}, y:{FR_DY:.0f}, opacity:1, borderWidth:18, borderRadius:56}}"
    else:
        state = f"{{scale:{FR_S * 0.9:.3f}, y:{FR_DY:.0f}, opacity:0, borderWidth:18, borderRadius:56}}"
    dur = 0.9 if i == 0 else 0.45
    js.append(f'tl.to("#face", Object.assign({state}, {{duration:{dur}, ease:"power3.out"}}), {s});')
    if lay == "framed":  # slow drift so a framed shot never sits still
        js.append(f'tl.to("#face", {{scale:{FR_S - 0.015}, duration:{round(e - s - dur, 2)}, ease:"none"}}, {s + dur});')
    if last:  # ending card: shrink the clip away, text and stickers stay
        js.append(f'tl.to("#face", {{scale:0.45, opacity:0, borderWidth:18, borderRadius:56, duration:0.5, ease:"power2.in"}}, {VID - 0.45});')
    if lay == "full":  # gentle punch-in for emphasis
        js.append(f'tl.to("#face-in", {{scale:1.08, duration:{round(min(e, VID) - s, 2)}, ease:"power1.inOut"}}, {s});')
        js.append(f'tl.set("#face-in", {{scale:1}}, {min(e, VID)});')

    events, taken = [], []

    # ---- pictures (straight cards)
    pics = b.get("pictures", [])
    stickers = b.get("stickers", [])[:4]
    cards = []
    if pics and lay == "pictures":
        cards = pack_pictures(pics[:3], PIC_BAND_STK if stickers else PIC_BAND)
    elif pics:
        x, y, w = PIC_OVER["framed" if lay == "framed" else "full"]
        iw, ih = size(f"assets/img/{pics[0]}.jpg")
        cards = [(pics[0], x, y, w, round((w - 24) * ih / iw + 24))]
    for j, (pid, x, y, w, h) in enumerate(cards):
        eid = f"{bid}-pic{j}"
        taken.append((x, y, w, h))
        out.append(
            f'<div id="{eid}" class="pic" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<img src="assets/img/{pid}.jpg" alt=""></div>'
        )
        t = s + 0.15 + j * 0.3
        events.append(t)
        js.append(f'tl.fromTo("#{eid}", {{opacity:0, scale:0.6, y:30}}, {{opacity:1, scale:1, y:0, duration:0.4, ease:"back.out(1.7)"}}, {round(t, 3)});')
        js.append(f'tl.to("#{eid}", {{y:-10, duration:{round(e - t - 0.6, 2)}, ease:"sine.inOut"}}, {round(t + 0.4, 3)});')
        if not last:
            js.append(f'tl.to("#{eid}", {{opacity:0, scale:0.9, duration:0.18, ease:"power2.in"}}, {round(exit_t, 3)});')

    # ---- stickers: first free spot, never over another sticker or a picture
    placed = 0
    for sid in stickers:
        iw, ih = size(f"assets/st/{sid}.png")
        spot = None
        for (x, y, w) in STK_CAND[lay]:
            h = round(w * ih / iw)
            box = (x - 14, y - 14, w + 28, h + 28)  # room for the wiggle
            if not any(inter(box, t) for t in taken):
                spot = (x, y, w, h)
                taken.append(box)
                break
        if not spot:
            print(f"  {bid}: no free spot for {sid}, skipped")
            continue
        x, y, w, h = spot
        j = placed
        placed += 1
        eid = f"{bid}-st{j}"
        out.append(f'<div id="{eid}" class="stk" style="left:{x}px;top:{y}px;width:{w}px"><img id="{eid}-i" src="assets/st/{sid}.png" alt=""></div>')
        t = s + 0.3 + j * 0.22
        events.append(t)
        js.append(f'tl.fromTo("#{eid}", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(2.6)"}}, {round(t, 3)});')
        period = 0.55 + 0.07 * j
        reps = max(1, int((e - t - 0.4) / period))
        sign = 1 if j % 2 == 0 else -1
        js.append(
            f'tl.fromTo("#{eid}-i", {{rotation:{-5 * sign}, y:0, scale:1}}, {{rotation:{5 * sign}, y:-8, scale:1.05, duration:{period:.2f}, '
            f'ease:"sine.inOut", yoyo:true, repeat:{reps}}}, {round(t + 0.4, 3)});'
        )
        if not last:
            js.append(f'tl.to("#{eid}", {{opacity:0, scale:0.3, duration:0.16, ease:"power2.in"}}, {round(exit_t, 3)});')

    # ---- caption (straight bold sans, word by word)
    cap = (b.get("caption") or "").strip()
    cap_t = s + 0.08
    if cap:
        color = b.get("color", "butter")
        n = len(cap)
        fsize = 72 if n <= 18 else (62 if n <= 26 else 56)
        if lay == "full":
            fsize = min(fsize, 58)
        words = "".join(f'<span class="w">{html.escape(wd)}</span> ' for wd in cap.split())
        label = SONG_NO.get(bid)
        lab = f'<div class="no" id="{bid}-no">{label}</div>' if label else ""
        low = " low" if lay == "full" else ""
        top = CAP_TOP[lay] + (0 if label or lay == "full" else 24)
        out.append(
            f'<div id="{bid}-cap" class="cap {color}{low}" style="top:{top}px;font-size:{fsize}px">{lab}<div class="txt">{words.strip()}</div></div>'
        )
        if label:
            js.append(f'tl.fromTo("#{bid}-no", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3, ease:"power2.out"}}, {round(cap_t, 3)});')
        js.append(
            f'tl.fromTo("#{bid}-cap .w", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3, '
            f'ease:"back.out(2)", stagger:0.07}}, {round(cap_t + 0.05, 3)});'
        )
        if not last:
            js.append(f'tl.to("#{bid}-cap", {{opacity:0, y:-18, duration:0.16, ease:"power2.in"}}, {round(exit_t, 3)});')
        else:  # ending card: lift the last line to the middle and enlarge it
            js.append(f'tl.to("#{bid}-cap", {{x:90, y:-240, scale:1.3, duration:0.6, ease:"back.out(1.6)"}}, {VID - 0.2});')

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

page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Inter Tight"; src: url("assets/fonts/inter-tight-latin-800-normal.woff2") format("woff2"); font-weight: 800; }}
      @font-face {{ font-family: "Inter Tight"; src: url("assets/fonts/inter-tight-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
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
      .pic {{ position: absolute; background: #fff; padding: 12px; border-radius: 6px; box-shadow: 0 16px 36px rgba(29, 62, 150, 0.28); opacity: 0; }}
      .pic img {{ display: block; width: 100%; height: 100%; object-fit: cover; }}
      .stk {{ position: absolute; opacity: 0; }}
      .stk img {{ display: block; width: 100%; filter: drop-shadow(0 10px 14px rgba(29, 62, 150, 0.3)); }}
      .cap {{ position: absolute; left: 120px; right: 192px; text-align: center; font-family: "Inter Tight", "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-weight: 800; font-style: normal; letter-spacing: -0.02em; line-height: 1.08; }}
      .cap.low {{ right: 300px; }}
      .cap .txt {{ text-wrap: balance; }}
      .cap .w {{ display: inline-block; paint-order: stroke fill; }}
      .cap.butter .w {{ color: var(--butter); -webkit-text-stroke: 5px var(--navy); text-shadow: 0 5px 0 var(--navy), 0 10px 22px rgba(29, 62, 150, 0.4); }}
      .cap.blue .w {{ color: var(--blue); -webkit-text-stroke: 7px var(--cream); text-shadow: 0 8px 20px rgba(29, 62, 150, 0.22); }}
      .cap .no {{ display: inline-block; margin-bottom: 12px; padding: 7px 24px; border-radius: 999px; background: var(--blue); color: var(--butter);
        font-family: "Inter Tight", Helvetica, Arial, sans-serif; font-weight: 700; font-size: 30px; letter-spacing: 0.08em; text-transform: uppercase; }}
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
