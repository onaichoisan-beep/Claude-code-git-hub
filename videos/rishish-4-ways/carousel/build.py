"""Instagram carousel (8 slides, 1080x1350) promoting the YouTube video. Writes carousel.html."""

# Dr. Dragon: a chibi doctor dragon. `prop` is drawn in his right hand.
def dragon(prop="", flip=False, size=330):
    props = {
        "coin": '<g transform="translate(150 132)"><circle r="24" fill="#f2b632"/><circle r="18" fill="#ffd45c"/>'
                '<text y="9" text-anchor="middle" font-family="Inter" font-weight="900" font-size="24" fill="#a26b00">₹</text></g>',
        "phone": '<g transform="translate(140 104) rotate(12)"><rect width="30" height="54" rx="6" fill="#2b2b33"/>'
                 '<rect x="3" y="5" width="24" height="42" rx="3" fill="#8fd0ff"/><rect x="7" y="12" width="16" height="4" rx="2" fill="#fff"/>'
                 '<rect x="7" y="20" width="12" height="4" rx="2" fill="#fff"/></g>',
        "book": '<g transform="translate(128 118) rotate(-8)"><rect width="56" height="40" rx="3" fill="#c0392b"/>'
                '<rect x="4" y="4" width="48" height="32" rx="2" fill="#fff6e3"/><path d="M28 4 V36" stroke="#c0392b" stroke-width="3"/>'
                '<path d="M9 13 H23 M9 20 H23 M33 13 H47 M33 20 H47" stroke="#b9a98a" stroke-width="2.5"/></g>',
        "camera": '<g transform="translate(132 112)"><rect width="50" height="36" rx="7" fill="#33333d"/><rect x="12" y="-6" width="16" height="8" rx="2" fill="#33333d"/>'
                  '<circle cx="25" cy="18" r="11" fill="#9fb4c8"/><circle cx="25" cy="18" r="6" fill="#2b2b33"/><circle cx="42" cy="8" r="3" fill="#ff5a5a"/></g>',
        "play": '<g transform="translate(130 112)"><rect width="56" height="40" rx="11" fill="#ff2a2a"/><path d="M22 11 L37 20 L22 29 Z" fill="#fff"/></g>',
        "chalk": '<g transform="translate(124 96)"><rect width="64" height="46" rx="4" fill="#2f5d46" stroke="#a0754a" stroke-width="5"/>'
                 '<text x="32" y="30" text-anchor="middle" font-family="Inter" font-weight="900" font-size="15" fill="#fff">A+B</text></g>',
        "laptop": '<g transform="translate(120 116)"><rect x="6" width="60" height="38" rx="4" fill="#a8d672"/><rect x="11" y="5" width="50" height="28" rx="2" fill="#e9f7d6"/>'
                  '<path d="M17 24 L27 14 L35 20 L47 10" stroke="#3b8f2e" stroke-width="3" fill="none"/><rect y="38" width="72" height="7" rx="3" fill="#7fb24a"/></g>',
        "point": '<g transform="translate(150 70)"><path d="M0 40 L26 4" stroke="#6dbb6a" stroke-width="12" stroke-linecap="round"/></g>',
    }
    tr = ' transform="translate(200 0) scale(-1 1)"' if flip else ""
    return f'''<svg class="dragon" viewBox="0 0 200 230" width="{size}" height="{size * 1.15:.0f}"><g{tr}>
  <ellipse cx="100" cy="222" rx="62" ry="7" fill="rgba(0,0,0,.12)"/>
  <path d="M40 170 C 4 176, 6 140, 20 132 C 18 150, 30 156, 48 150 Z" fill="#5fae5b"/>
  <path d="M46 92 C 18 70, 10 104, 30 112 Z M154 92 C 182 70, 190 104, 170 112 Z" fill="#9c86d8"/>
  <ellipse cx="100" cy="160" rx="56" ry="58" fill="#77c372"/>
  <ellipse cx="100" cy="170" rx="36" ry="42" fill="#f8ecc6"/>
  <path d="M72 136 C 64 160, 66 196, 76 214 L 124 214 C 134 196, 136 160, 128 136 C 120 150, 80 150, 72 136 Z" fill="#fff" opacity=".96"/>
  <path d="M100 150 V214" stroke="#e5e5ea" stroke-width="2"/>
  <ellipse cx="78" cy="214" rx="16" ry="9" fill="#5fae5b"/><ellipse cx="122" cy="214" rx="16" ry="9" fill="#5fae5b"/>
  <path d="M60 128 C 46 136, 46 150, 54 158" stroke="#77c372" stroke-width="16" stroke-linecap="round" fill="none"/>
  <path d="M140 128 C 152 134, 156 140, 152 150" stroke="#77c372" stroke-width="16" stroke-linecap="round" fill="none"/>
  <path d="M74 128 C 70 160, 92 170, 100 160 C 108 170, 130 160, 126 128" stroke="#4b5563" stroke-width="4" fill="none"/>
  <circle cx="100" cy="166" r="7" fill="#c9cdd4" stroke="#6b7280" stroke-width="3"/>
  <path d="M70 34 L64 8 L84 28 Z M130 34 L136 8 L116 28 Z" fill="#fff1c9"/>
  <ellipse cx="100" cy="74" rx="58" ry="52" fill="#77c372"/>
  <path d="M100 22 C 106 30, 106 38, 100 44 C 94 38, 94 30, 100 22 Z" fill="#9c86d8"/>
  <ellipse cx="100" cy="98" rx="30" ry="18" fill="#a9db97"/>
  <circle cx="91" cy="96" r="2.6" fill="#3e7a3a"/><circle cx="109" cy="96" r="2.6" fill="#3e7a3a"/>
  <path d="M92 108 Q100 114 108 108" stroke="#2f4f2c" stroke-width="3" fill="none" stroke-linecap="round"/>
  <ellipse cx="78" cy="72" rx="11" ry="13" fill="#1f2a1f"/><ellipse cx="122" cy="72" rx="11" ry="13" fill="#1f2a1f"/>
  <circle cx="82" cy="67" r="4" fill="#fff"/><circle cx="126" cy="67" r="4" fill="#fff"/>
  <circle cx="78" cy="72" r="17" fill="none" stroke="#3b3b44" stroke-width="3.5"/><circle cx="122" cy="72" r="17" fill="none" stroke="#3b3b44" stroke-width="3.5"/>
  <path d="M95 72 H105" stroke="#3b3b44" stroke-width="3.5"/>
  <ellipse cx="64" cy="92" rx="8" ry="5" fill="#ff9aa8" opacity=".8"/><ellipse cx="136" cy="92" rx="8" ry="5" fill="#ff9aa8" opacity=".8"/>
  {props.get(prop, "")}
</g></svg>'''


SLIDES = [
    # (top photo, bottom photo, title, body html, teaser, dragon prop, flip)
    dict(kind="cover"),
    dict(top="phone.jpg", bot="desk.jpg", title="ghar se paise?<br>ajeeb lagta hai.",
         body='<p>Every ₹500 you ask for comes with a question. <b>Earning your own money isn’t about greed. It’s about freedom.</b></p>'
              '<p class="r">And you already have the time: most students spend <b>7+ hours a day</b> on their phone.</p>',
         teaser="so what if those 7 hours paid you? →", prop="phone"),
    dict(top="desk.jpg", bot="steth.jpg", title="your skills<br>are your salary.",
         body='<p><b>More skill, more money. Better skill, more money.</b> That’s the whole game.</p>'
              '<p class="r">You don’t need an investment. You need <b>one skill</b> and the stubbornness to start, even in 1st year.</p>',
         teaser="here are the 4 ways I tested →", prop="book"),
    dict(top="unboxing.jpg", bot="phone.jpg", num="01", title="UGC content<br>creation",
         body='<p>Make short videos for brands. <b>They pay you in money and products.</b></p>'
              '<ul><li>can be completely <b>faceless</b></li><li>tech · brand · affiliate UGC</li><li>this alone earned me <b>₹60K+</b></li></ul>',
         teaser="the forms brands use to find you? they’re in the video ↗", prop="camera"),
    dict(top="rupees.jpg", bot="desk.jpg", num="02", title="content<br>creation",
         body='<p>Start a page. <b>One viral video can change everything.</b></p>'
              '<ul><li>first paid collab at just <b>800 subscribers</b></li><li>before my page was even monetized</li><li>free courses &amp; books to resell or give away</li></ul>',
         teaser="how I pitched brands at 800 subs → full video ↗", prop="play"),
    dict(top="teacher.jpg", bot="steth.jpg", num="03", title="online<br>tutoring",
         body='<p>Only good at studies? <b>That’s enough.</b></p>'
              '<ul><li>teach topics your juniors find hard</li><li><b>zero investment</b>: you sell what you already know</li><li>local coachings value real knowledge</li></ul>',
         teaser="where to find your first students → in the video ↗", prop="chalk"),
    dict(top="steth.jpg", bot="rupees.jpg", num="04", title="freelancing",
         body='<p>Video editing pays <b>₹3–4K per video</b> and grows with your skill.</p>'
              '<ul><li>DM creators &amp; YouTubers</li><li>send samples, start small</li><li>practice → better edits → higher price</li></ul>',
         teaser="the editor behind my video + how to get clients ↗", prop="laptop"),
    dict(kind="end"),
]

PILL = '<div class="pill">save for later and follow for more</div>'


def slide(i, s):
    n = f'<div class="pg">{i}/8</div>'
    if s.get("kind") == "cover":
        return f'''<section class="s cover" id="s{i}">
  <img class="full" src="img/desk.jpg" alt="">
  <div class="note">
    <div class="tape"></div>
    <div class="kick">a 1st year MBBS student’s</div>
    <h1>why you need<br>your own money<br>in college</h1>
    <div class="sub">(+ the 4 ways I made ₹80,000)</div>
    <div class="swipe">swipe →</div>
  </div>
  <div class="dr cov">{dragon("coin", size=300)}</div>
</section>'''
    if s.get("kind") == "end":
        return f'''<section class="s" id="s{i}">{n}
  <div class="band top" style="background-image:url(img/rupees.jpg)"></div>
  <div class="page end">
    <h2>the full breakdown<br>is on YouTube</h2>
    <div class="tv"><img src="img/thumb.png" alt=""></div>
    <div class="yt"><span class="play"></span>How to Earn Money as a Medical Student (4 Ways, No Investment)</div>
    <div class="cta">watch now · <b>link in bio</b></div>
    <div class="dr endr">{dragon("point", flip=True, size=210)}</div>
  </div>
  <div class="band bot" style="background-image:url(img/desk.jpg)"></div>
  {PILL}
</section>'''
    num = f'<div class="num">way {s["num"]}</div>' if s.get("num") else ""
    return f'''<section class="s" id="s{i}">{n}
  <div class="band top" style="background-image:url(img/{s["top"]})"></div>
  <div class="page">
    {num}<h2>{s["title"]}</h2>
    <div class="row">
      <div class="body">{s["body"]}</div>
      <div class="dr">{dragon(s["prop"], size=300)}</div>
    </div>
    <div class="teaser">{s["teaser"]}</div>
  </div>
  <div class="band bot" style="background-image:url(img/{s["bot"]})"></div>
  {PILL}
</section>'''


CSS = open("style.css").read()
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
{"".join(slide(i, s) for i, s in enumerate(SLIDES, 1))}
</body></html>'''
open("carousel.html", "w").write(html)
print("ok", len(SLIDES))
