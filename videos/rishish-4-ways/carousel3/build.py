"""Minimal Instagram carousel (8 slides, 1080x1350). PIXY's face appears on slides 1 and 2 only."""


def sym(t):
    return t.replace("+", '<i class="sym">+</i>').replace("–", '<i class="sym">–</i>')


def foot(n):
    return f'<div class="foot"><span>{n:02d} / 08</span><span>save for later</span></div>'


def nxt(t):
    return f'<div class="next">{t} <b>→</b></div>'


def way(i, n, title, lines, big, small, teaser):
    ls = "".join(f"<p>{x}</p>" for x in lines)
    return f'''<section class="s" id="s{i}">
  <div class="kick">way {n}</div>
  <h2>{title}</h2>
  <div class="rule"></div>
  <div class="lines">{ls}</div>
  <div class="stat"><b>{sym(big)}</b><span>{small}</span></div>
  {nxt(teaser)}
  {foot(i)}
</section>'''


S = [
    f'''<section class="s" id="s1">
  <div class="kick">1st year MBBS · real numbers</div>
  <h1>why you need<br>your <em>own</em><br>money.</h1>
  <p class="sub">and the 4 ways I made ₹80,000<br>in my first year of college.</p>
  <img class="face f1" src="face_sly.png" alt="">
  <div class="swipe">swipe <b>→</b></div>
  {foot(1)}
</section>''',
    f'''<section class="s" id="s2">
  <div class="kick">the problem</div>
  <h2>ghar se paise?<br>ajeeb lagta hai.</h2>
  <div class="rule"></div>
  <div class="lines"><p>every ₹500 comes with a question.</p><p>meanwhile, most of us spend</p></div>
  <div class="bignum">7<i class="sym">+</i> hrs<span>a day on our phones.</span></div>
  <img class="face f2" src="face_shock.png" alt="">
  {nxt("what if those hours paid you?")}
  {foot(2)}
</section>''',
    f'''<section class="s" id="s3">
  <div class="kick">the mindset</div>
  <h2>your skills are<br>your salary.</h2>
  <div class="rule"></div>
  <div class="ladder">
    <p><i>01</i>more skill = more money</p>
    <p><i>02</i>better skill = more money</p>
    <p><i>03</i>₹0 investment. just start.</p>
  </div>
  {nxt("here are the 4 ways I tested")}
  {foot(3)}
</section>''',
    way(4, "01", "UGC content<br>creation", ["short videos for brands.", "paid in money + products.", "can be 100% faceless."],
        "₹60K+", "earned from this alone", "the forms brands use to find you? in the video"),
    way(5, "02", "content<br>creation", ["start a page. stay consistent.", "one viral video changes everything.", "brands send free books &amp; courses."],
        "800", "subs when I got my first paid collab", "how I pitched brands at 800 subs"),
    way(6, "03", "online<br>tutoring", ["only good at studies? enough.", "teach what juniors find hard.", "local coachings value real knowledge."],
        "₹0", "investment needed", "where to find your first students"),
    way(7, "04", "freelancing", ["learn video editing.", "DM creators &amp; YouTubers.", "send samples, raise your price."],
        "₹3–4K", "per video edit", "how to land your first client"),
    f'''<section class="s" id="s8">
  <div class="kick">watch the full video</div>
  <h2>the full breakdown<br>is on YouTube.</h2>
  <div class="tv"><img src="thumb.png" alt=""></div>
  <p class="title">How to Earn Money as a Medical Student<br>(4 Ways, No Investment)</p>
  <div class="bio">link in bio <b>↗</b></div>
  {foot(8)}
</section>''',
]

open("carousel.html", "w").write(f'''<!doctype html><html><head><meta charset="utf-8"><style>{open("style.css").read()}</style></head><body>
{"".join(S)}
</body></html>''')
print("ok", len(S))
