"""Instagram carousel v2 — PIXY (Dr. Dragon) character, character-sheet palette, no stock photos.
Writes carousel.html; shoot.cjs renders slide_1..8.png (1080x1350)."""

FOOT = '<div class="foot">save for later &amp; follow for more</div>'


def head(tag):
    return f'<div class="head"><span class="brand">DR. DRAGON’S MONEY NOTES</span><span class="tag">{tag}</span></div>'


def pixy(pose, cls, h):
    return f'<img class="pixy {cls}" src="pixy/{pose}.png" style="height:{h}px" alt="">'


def bubble(text, cls):
    return f'<div class="bubble {cls}">{text}</div>'


def sticker(big, small, color, cls):
    return f'<div class="sticker {color} {cls}"><b>{big}</b><span>{small}</span></div>'


def card(items, cls=""):
    lis = "".join(f"<li>{x}</li>" for x in items)
    return f'<div class="card {cls}"><ul>{lis}</ul></div>'


def next_(text):
    return f'<div class="next"><span>next</span>{text}</div>'


def way(i, n, title, pose, ph, items, st, teaser, extra=""):
    return f'''<section class="s" id="s{i}">{head("WAY " + n + " / 04")}
  <div class="wnum">{n}</div>
  <h2 class="wt">{title}</h2>
  {card(items, "wc")}
  {st}
  {pixy(pose, "wp", ph)}
  {extra}
  {next_(teaser)}
  {FOOT}
</section>'''


S = []
S.append(f'''<section class="s" id="s1">{head("1ST YEAR MBBS · REAL NUMBERS")}
  <h1 class="c1">why you<br>need your<br>own money</h1>
  <div class="c1sub">(and the 4 ways I made it in college)</div>
  {sticker("₹80,000", "earned in<br>1st year", "gold", "c1st")}
  {pixy("attitude", "c1p", 700)}
  {bubble("ghar se paise?<br>not anymore.", "c1b")}
  <div class="swipe">swipe &nbsp;→</div>
  {FOOT}
</section>''')

S.append(f'''<section class="s" id="s2">{head("THE PROBLEM")}
  <h2 class="t2">ghar se paise?<br>ajeeb lagta hai.</h2>
  {pixy("facepalm", "p2", 600)}
  {bubble("every ₹500 =<br>a full interrogation", "b2")}
  <div class="card stat"><div class="lbl">most students spend</div><div class="num">7+ hrs</div>
    <div class="lbl">a day on their phone</div><div class="small">that’s 200+ hours a month</div></div>
  {next_("what if those hours paid you?")}
  {FOOT}
</section>''')

S.append(f'''<section class="s" id="s3">{head("THE MINDSET")}
  <h2 class="t2">your skills are<br>your salary.</h2>
  {pixy("think", "p3", 600)}
  <div class="ladder">
    <div class="step s1"><i>1</i>more skill → more money</div>
    <div class="step s2"><i>2</i>better skill → more money</div>
    <div class="step s3"><i>3</i>₹0 investment. just start.</div>
  </div>
  {bubble("hmm… so which<br>skills pay?", "b3")}
  {next_("the 4 ways I actually tested")}
  {FOOT}
</section>''')

S.append(way(4, "01", "UGC content<br>creation", "point", 560,
             ["short videos <b>for brands</b>", "paid in <b>money + products</b>", "<b>100% faceless</b> option"],
             sticker("₹60K+", "earned from<br>this alone", "orange", "wst"),
             "the forms brands use to find you → in the video", ))
S.append(way(5, "02", "content<br>creation", "celebrate", 560,
             ["start a page, <b>stay consistent</b>", "<b>1 viral video</b> changes everything", "free books &amp; courses from brands"],
             sticker("800", "subs → my 1st<br>paid collab", "gold", "wst"),
             "how I pitched brands at 800 subs → video"))
S.append(way(6, "03", "online<br>tutoring", "wave", 560,
             ["only good at studies? <b>enough</b>", "teach what <b>juniors find hard</b>", "local coachings value real knowledge"],
             sticker("₹0", "investment<br>needed", "sky", "wst"),
             "where to find your first students → video"))
S.append(way(7, "04", "freelancing", "hips", 560,
             ["learn <b>video editing</b>", "<b>DM</b> creators &amp; YouTubers", "send samples, <b>raise your price</b>"],
             sticker("₹3–4K", "per video<br>edit", "orange", "wst"),
             "how to land your first client → video"))

S.append(f'''<section class="s" id="s8">{head("WATCH THE FULL VIDEO")}
  <h2 class="t8">the full breakdown<br>is on YouTube</h2>
  <div class="tv"><img src="thumb.png" alt=""></div>
  <div class="yt"><span class="play"></span>How to Earn Money as a Medical Student (4 Ways, No Investment)</div>
  {pixy("point", "p8", 430)}
  <div class="bio">link in bio ↗</div>
  {FOOT}
</section>''')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{open("style.css").read()}</style></head><body>
{"".join(S)}
</body></html>'''
open("carousel.html", "w").write(html)
print("ok", len(S))
