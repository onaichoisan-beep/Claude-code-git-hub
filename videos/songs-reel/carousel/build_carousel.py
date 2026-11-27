"""Build the 6-page Instagram carousel (1080x1350) and export each page as PNG.

Run from videos/songs-reel:  python3 carousel/build_carousel.py && node carousel/export.cjs
Same look as the reel: striped butter background, straight bold sans text,
straight picture cards, cut-out stickers that never overlap anything.
"""
import html

from PIL import Image

W, H = 1080, 1350
A = "../assets"

SLIDES = [
    {"kind": "cover"},
    {"no": "No. 1", "title": "Dreams, Books, Power and Walls", "artist": "Jannabi",
     "pics": ["BPW-7334", "BPW-7335", "BPW-7336"], "line": "very soothing, and the last part kills it",
     "stickers": ["st-star"]},
    {"no": "No. 2", "title": "Vodka Cranberry", "artist": "Conan Gray",
     "pics": ["VC-7328", "VC-7329", "VC-7330"], "line": "", "stickers": ["st-crying"]},
    {"no": "No. 3", "title": "TV", "artist": "Billie Eilish",
     "pics": ["TV-7331", "TV-7332", "TV-7333"], "line": "", "stickers": ["st-kitten-earphones"]},
    {"no": "No. 4", "title": "All Too Well", "artist": "Taylor Swift · 10 minute version",
     "pics": ["ATW-7337", "ATW-7339", "ATW-7338"], "line": "our favourite. bonus: So Long, London",
     "stickers": ["st-dancers"]},
    {"no": "No. 5", "title": "Glimpse of Us", "artist": "Joji",
     "pics": ["GOU-7342", "GOU-7343", "GOU-7344"], "line": "my personal favourite, and my sister's too",
     "stickers": ["st-cat-ipod", "st-headphones"], "follow": True},
]

STK_SPOTS = [(60, 1085, 190), (830, 1085, 190)]  # bottom corners, clear of text and pictures
BAND = (380, 1060)


def size(p):
    return Image.open(p).size


def pack(ids, band, x0=90, x1=990):
    top, bot = band
    rows = [[0]] if len(ids) == 1 else [[0, 1]] if len(ids) == 2 else [[0, 1], [2]]
    dims = [size(f"assets/img/{i}.jpg") for i in ids]
    gap, pad = 30, 12

    def lay(w):
        out, y = [], 0
        for r in rows:
            hs = [w * dims[k][1] / dims[k][0] + 2 * pad for k in r]
            rw = len(r) * (w + 2 * pad) + (len(r) - 1) * gap
            xs = (x0 + x1) / 2 - rw / 2
            for n, k in enumerate(r):
                out.append((k, xs + n * (w + 2 * pad + gap), y, w + 2 * pad, hs[n]))
            y += max(hs) + gap
        return out, y - gap

    w = 470
    while True:
        cards, total = lay(w)
        if total <= bot - top or w < 150:
            break
        w -= 8
    y0 = top + ((bot - top) - total) / 2
    return [(ids[k], round(x), round(y0 + y), round(cw), round(ch)) for k, x, y, cw, ch in cards]


def sticker(sid, x, y, w, rot_class=""):
    return f'<img class="stk {rot_class}" src="{A}/st/{sid}.png" style="left:{x}px;top:{y}px;width:{w}px" alt="">'


pages = []
for n, s in enumerate(SLIDES, 1):
    parts = [f'<img class="bg" src="{A}/img/bg-45.jpg" alt="">']
    if s.get("kind") == "cover":
        parts.append('<div class="eyebrow">study playlist</div>')
        parts.append('<h1 class="title big"><span class="b">my top 5 songs</span><br><span class="y">to study to</span></h1>')
        cw = 470
        ch = round(cw * 16 / 9)
        cx = (W - cw) // 2
        parts.append(f'<div class="face" style="left:{cx}px;top:400px;width:{cw}px;height:{ch - 60}px"><img src="{A}/img/cover-still.jpg" alt=""></div>')
        parts.append(sticker("st-headphones", 70, 470, 200))
        parts.append(sticker("st-cat-sing", 820, 880, 190))
        parts.append(sticker("st-star", 95, 1010, 150))
        parts.append('<div class="pill swipe">swipe for the list →</div>')
    else:
        parts.append(f'<header class="head"><div class="no">{html.escape(s["no"])}</div>'
                     f'<h2 class="title">{html.escape(s["title"])}</h2>'
                     f'<div class="artist">{html.escape(s["artist"])}</div></header>')
        for pid, x, y, w, h in pack(s["pics"], (300 if len(s["title"]) <= 16 else 360, 1075)):
            parts.append(f'<div class="pic" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><img src="{A}/img/{pid}.jpg" alt=""></div>')
        if s["line"]:
            parts.append(f'<div class="line">{html.escape(s["line"])}</div>')
        for (sid, (x, y, w)) in zip(s["stickers"], STK_SPOTS):
            parts.append(sticker(sid, x, y, w))
        if s.get("follow"):
            parts.append('<div class="pill follow">follow for more</div>')
    parts.append(f'<div class="count">{n}/6</div>')
    pages.append(f'<section class="slide" id="s{n}">' + "".join(parts) + "</section>")

doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Songs carousel</title>
<style>
@font-face {{ font-family: "Inter Tight"; src: url("{A}/fonts/inter-tight-latin-800-normal.woff2") format("woff2"); font-weight: 800; }}
@font-face {{ font-family: "Inter Tight"; src: url("{A}/fonts/inter-tight-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Inter Tight"; src: url("{A}/fonts/inter-tight-latin-500-normal.woff2") format("woff2"); font-weight: 500; }}
:root {{ --butter:#F7EFA0; --blue:#2F5FD0; --navy:#1D3E96; --cream:#FFFDF0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#ddd; font-family:"Inter Tight", "Helvetica Neue", Helvetica, Arial, sans-serif; }}
.slide {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; margin:0 0 20px; background:#F8EFB8; }}
.bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.head {{ position:absolute; left:200px; right:200px; top:90px; display:flex; flex-direction:column; align-items:center; gap:14px; }}
.no {{ padding:8px 26px; border-radius:999px; background:var(--blue); color:var(--butter); font-weight:700; font-size:30px; letter-spacing:.08em; text-transform:uppercase; }}
.title {{ text-align:center; font-weight:800; font-size:66px; line-height:1.04; letter-spacing:-.02em; color:var(--blue);
  paint-order:stroke fill; -webkit-text-stroke:8px var(--cream); text-wrap:balance; }}
.title.big {{ position:absolute; left:110px; right:110px; top:120px; font-size:84px; }}
.title .y {{ color:var(--butter); -webkit-text-stroke:4px var(--navy); text-shadow:0 5px 0 var(--navy); }}
.eyebrow {{ position:absolute; left:0; right:0; top:70px; text-align:center; font-weight:700; font-size:26px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--navy); }}
.artist {{ text-align:center; font-weight:700; font-size:32px; color:var(--navy); }}
.title:not(.big) + .artist {{ }}
.pic {{ position:absolute; background:#fff; padding:12px; border-radius:6px; box-shadow:0 16px 36px rgba(29,62,150,.25); }}
.pic img {{ display:block; width:100%; height:100%; object-fit:cover; }}
.face {{ position:absolute; border:16px solid #fff; border-radius:44px; overflow:hidden; box-shadow:0 26px 50px rgba(29,62,150,.28); }}
.face img {{ width:100%; height:100%; object-fit:cover; object-position:50% 20%; display:block; }}
.stk {{ position:absolute; filter:drop-shadow(0 10px 14px rgba(29,62,150,.3)); }}
.line {{ position:absolute; left:270px; right:270px; top:1105px; text-align:center; font-weight:800; font-size:38px; line-height:1.18;
  color:var(--navy); text-wrap:balance; }}
.pill {{ position:absolute; left:50%; transform:translateX(-50%); padding:14px 34px; border-radius:999px; background:var(--blue); color:var(--butter);
  font-weight:800; font-size:34px; white-space:nowrap; box-shadow:0 10px 24px rgba(29,62,150,.3); }}
.swipe {{ top:1225px; }}
.follow {{ top:1235px; font-size:28px; padding:10px 28px; }}
.count {{ position:absolute; right:40px; top:40px; font-weight:700; font-size:22px; color:var(--navy); opacity:.7; }}
</style></head><body>
{chr(10).join(pages)}
</body></html>"""
open("carousel/carousel.html", "w").write(doc)
print("wrote carousel/carousel.html")
