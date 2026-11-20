"""Generate index.html (HyperFrames composition) from edl.json + overlay design."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
edl = json.loads((ROOT / "edl.json").read_text())
DUR = 60.0

# per-shot camera move: (from_scale, to_scale)
MOVES = {}
for i, s in enumerate(edl):
    MOVES[s["id"]] = (1.0, 1.07) if i % 2 == 0 else (1.07, 1.0)
for k in ("s07", "s10", "s11", "s28"):
    MOVES[k] = (1.0, 1.04)

videos = "\n".join(
    f'        <div class="shot" id="w_{s["id"]}"><video id="{s["id"]}" src="{s["file"]}" muted playsinline '
    f'data-start="{s["start"]:.4f}" data-duration="{s["dur"]:.4f}" data-track-index="{1 + i % 2}"></video></div>'
    for i, s in enumerate(edl))

moves_js = ",\n      ".join(
    f'["#w_{s["id"]}", {s["start"]:.4f}, {s["dur"]:.4f}, {MOVES[s["id"]][0]}, {MOVES[s["id"]][1]}]' for s in edl)

SFX = [  # (id, file, t, vol)
    ("x_w1", "whoosh", 1.84, 0.35), ("x_w2", "whoosh", 5.84, 0.3), ("x_w3", "whoosh", 15.34, 0.35),
    ("x_w4", "whoosh_long", 18.6, 0.35), ("x_w5", "whoosh", 21.1, 0.3), ("x_w6", "whoosh", 23.94, 0.3),
    ("x_w7", "whoosh", 27.94, 0.35), ("x_w8", "whoosh_long", 36.45, 0.3), ("x_w9", "whoosh", 43.47, 0.35),
    ("x_p1", "pop", 0.12, 0.35), ("x_p2", "pop", 8.45, 0.35), ("x_p3", "pop", 25.0, 0.35),
    ("x_p4", "pop", 28.05, 0.3), ("x_p5", "pop", 31.75, 0.3), ("x_p6", "pop", 33.8, 0.3),
    ("x_p7", "pop", 45.56, 0.45), ("x_p8", "pop", 46.2, 0.35), ("x_p9", "pop", 21.2, 0.35),
]
SFX += [(f"x_t{k}", "tick", 22.2 + k * 0.08, 0.25) for k in range(10)]
sfx_html = "\n".join(
    f'      <audio id="{i}" src="assets/sfx/{f}.wav" data-start="{t:.3f}" data-duration="1" data-volume="{v}" data-track-index="{20 + n % 3}"></audio>'
    for n, (i, f, t, v) in enumerate(SFX))

PHONE_SVG = ('<svg viewBox="0 0 24 24" class="ico"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 '
             '11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>')

html = f"""<!doctype html>
<html lang="hi" data-resolution="portrait" data-composition-variables='[{{"id":"phone","type":"string","label":"Contact number","default":"+91 XXXXX XXXXX"}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Playvanta – Counselling Ad</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Anton"; src: url("assets/fonts/anton.woff2") format("woff2"); font-weight: 400; }}
      @font-face {{ font-family: "Mont"; src: url("assets/fonts/montserrat800.woff2") format("woff2"); font-weight: 800; }}
      @font-face {{ font-family: "Mont"; src: url("assets/fonts/montserrat600.woff2") format("woff2"); font-weight: 600; }}
      @font-face {{ font-family: "Baloo2"; src: url("assets/fonts/baloo-2-devanagari-800-normal.woff2") format("woff2"); font-weight: 800;
        unicode-range: U+0900-097F, U+1CD0-1CF9, U+200C-200D, U+20A8, U+20B9, U+25CC, U+A830-A839, U+A8E0-A8FF; }}
      @font-face {{ font-family: "Baloo2"; src: url("assets/fonts/baloo-2-latin-800-normal.woff2") format("woff2"); font-weight: 800; unicode-range: U+0000-00FF; }}
      :root {{ --navy: #0b1d5e; --navy2: #06103a; --orange: #ff6a13; --orange2: #ff8a1f; --white: #ffffff; --orangeD: #cf4a00; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; font-family: "Mont", sans-serif; }}
      .shot {{ position: absolute; inset: 0; overflow: hidden; }}
      .shot video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #grade {{ position: absolute; inset: 0; pointer-events: none;
        background: radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.42) 100%),
                    linear-gradient(180deg, rgba(0,0,0,.28) 0%, rgba(0,0,0,0) 14%, rgba(0,0,0,0) 52%, rgba(3,8,30,.55) 78%, rgba(3,8,30,.35) 100%); }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
      /* corner logo – whole video */
      #corner {{ position: absolute; top: 56px; right: 44px; width: 170px; height: 170px; border-radius: 50%;
        box-shadow: 0 6px 22px rgba(0,0,0,.45); }}
      #corner img {{ width: 100%; height: 100%; display: block; }}
      /* headline text */
      .hl {{ position: absolute; left: 110px; right: 150px; top: 930px; text-align: center; color: #fff; opacity: 0;
        font-family: "Anton", sans-serif; text-transform: uppercase; letter-spacing: 1px; line-height: 1.02;
        text-shadow: 0 4px 18px rgba(0,0,0,.6); }}
      .hl, .hi {{ background: radial-gradient(ellipse 60% 55% at 50% 50%, rgba(0,0,0,.5), rgba(0,0,0,0) 100%); padding-top: 40px; padding-bottom: 40px; }}
      .hl .ln {{ display: block; overflow: hidden; padding: 4px 0; }}
      .hl .in {{ display: block; }}
      .hl .o {{ color: var(--orange2); }}
      .bar {{ display: block; width: 150px; height: 10px; margin: 18px auto 0; background: var(--orange); border-radius: 6px; }}
      .hi {{ position: absolute; left: 110px; right: 150px; text-align: center; color: #fff; opacity: 0;
        font-family: "Baloo2", sans-serif; font-weight: 800; line-height: 1.25; text-shadow: 0 4px 18px rgba(0,0,0,.7); }}
      .hi .ln {{ display: block; }}
      .hi .o {{ color: var(--orange2); }}
      /* logo reveal */
      #reveal {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }}
      #rv-wrap {{ position: relative; width: 640px; height: 640px; opacity: 0; }}
      #rv-wrap img {{ width: 100%; height: 100%; display: block; border-radius: 50%;
        box-shadow: 0 0 80px rgba(255,120,30,.55), 0 20px 60px rgba(0,0,0,.6); }}
      #rv-shine {{ position: absolute; inset: 0; border-radius: 50%; overflow: hidden; }}
      #rv-shine i {{ position: absolute; top: -20%; left: 0; width: 120px; height: 140%;
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.75), rgba(255,255,255,0)); }}
      #rv-ring {{ position: absolute; left: 50%; top: 50%; width: 640px; height: 640px; margin: -320px 0 0 -320px;
        border-radius: 50%; border: 10px solid var(--orange); opacity: 0; }}
      /* kadi graphic */
      #kadi {{ position: absolute; inset: 0; }}
      .chip {{ position: absolute; top: 980px; width: 340px; padding: 26px 10px; border-radius: 22px; text-align: center; color: #fff;
        font-family: "Anton", sans-serif; font-size: 58px; line-height: 1.05; text-transform: uppercase; opacity: 0;
        background: rgba(6,16,58,.82); border: 4px solid var(--orange); box-shadow: 0 10px 30px rgba(0,0,0,.5); }}
      #chipA {{ left: 70px; }} #chipB {{ right: 150px; }}
      #kline {{ position: absolute; top: 1058px; left: 410px; width: 180px; height: 8px; background: var(--orange); transform-origin: 0 50%; }}
      #knode {{ position: absolute; top: 992px; left: 430px; width: 140px; height: 140px; border-radius: 50%; opacity: 0;
        box-shadow: 0 0 0 6px #fff, 0 0 40px rgba(255,120,30,.9); }}
      #knode img {{ width: 100%; height: 100%; border-radius: 50%; }}
      #ktitle {{ position: absolute; left: 70px; right: 150px; top: 1200px; text-align: center; color: #fff; opacity: 0;
        font-family: "Anton", sans-serif; font-size: 70px; text-transform: uppercase; text-shadow: 0 4px 18px rgba(0,0,0,.7); }}
      /* stats */
      #stats {{ position: absolute; left: 60px; right: 140px; top: 930px; display: flex; justify-content: center; align-items: flex-start; gap: 40px; }}
      .stat {{ text-align: center; color: #fff; opacity: 0; }}
      .stat .num {{ font-family: "Anton", sans-serif; font-size: 170px; line-height: .95; color: #fff;
        text-shadow: 0 0 40px rgba(255,120,30,.6), 0 6px 20px rgba(0,0,0,.6); }}
      .stat .lab {{ font-family: "Anton", sans-serif; font-size: 62px; letter-spacing: 3px; color: var(--orange2); text-transform: uppercase; }}
      #sdiv {{ width: 8px; height: 240px; background: rgba(255,255,255,.85); border-radius: 4px; margin-top: 20px; opacity: 0; }}
      #dots {{ display: flex; gap: 22px; justify-content: center; margin-top: 18px; }}
      #dots b {{ width: 30px; height: 30px; border-radius: 50%; background: rgba(255,255,255,.25); display: block; }}
      /* lower third */
      #l3 {{ position: absolute; left: 70px; right: 150px; top: 960px; opacity: 0; }}
      #l3 .card {{ background: rgba(6,16,58,.9); border-left: 16px solid var(--orange); border-radius: 18px; padding: 34px 40px 38px;
        box-shadow: 0 16px 40px rgba(0,0,0,.5); }}
      #l3 .k {{ font-family: "Mont"; font-weight: 800; font-size: 40px; letter-spacing: 8px; color: var(--orange2); }}
      #l3 .t {{ font-family: "Anton"; font-size: 80px; line-height: 1.05; color: #fff; text-transform: uppercase; }}
      /* chips: talent / age / need */
      #tags {{ position: absolute; left: 70px; right: 150px; top: 1150px; display: flex; justify-content: center; gap: 22px; }}
      .tag {{ font-family: "Mont"; font-weight: 800; font-size: 44px; color: #fff; padding: 14px 30px; border-radius: 60px;
        background: rgba(255,255,255,.14); border: 3px solid rgba(255,255,255,.5); opacity: 0; }}
      /* CTA */
      #cta {{ position: absolute; left: 60px; right: 140px; top: 880px; text-align: center; opacity: 0; }}
      #cta .t1 {{ font-family: "Anton"; font-size: 110px; color: #fff; line-height: 1; text-shadow: 0 6px 22px rgba(0,0,0,.6); }}
      #cta .pill {{ display: inline-block; margin-top: 22px; padding: 24px 46px; border-radius: 90px; background: var(--orangeD);
        font-family: "Anton"; font-size: 84px; color: #fff; line-height: 1; box-shadow: 0 14px 40px rgba(255,106,19,.55); }}
      #cta .hin {{ margin-top: 30px; font-family: "Baloo2"; font-weight: 800; font-size: 60px; color: #fff; text-shadow: 0 4px 16px rgba(0,0,0,.7); }}
      #team {{ position: absolute; left: 70px; right: 150px; top: 1000px; display: flex; align-items: center; gap: 34px; opacity: 0;
        background: rgba(6,16,58,.88); border-radius: 26px; padding: 34px 40px; border: 4px solid var(--orange); }}
      #team .ring {{ flex: none; width: 130px; height: 130px; border-radius: 50%; background: var(--orangeD); color: #fff;
        display: flex; align-items: center; justify-content: center; }}
      .ico {{ width: 60%; height: 60%; display: block; }}
      #team .tx {{ font-family: "Anton"; font-size: 64px; line-height: 1.05; color: #fff; text-transform: uppercase; }}
      /* end card */
      #end {{ position: absolute; inset: 0; }}
      #e-logo {{ position: absolute; left: 310px; top: 210px; width: 440px; height: 440px; opacity: 0; }}
      #e-logo img {{ width: 100%; height: 100%; border-radius: 50%; box-shadow: 0 0 90px rgba(255,120,30,.5), 0 20px 60px rgba(0,0,0,.6); }}
      #e-tag {{ position: absolute; left: 90px; right: 150px; top: 690px; text-align: center; font-family: "Baloo2"; font-weight: 800;
        font-size: 66px; line-height: 1.25; color: #fff; opacity: 0; }}
      #e-tag .o {{ color: var(--orange2); }}
      #e-cta {{ position: absolute; left: 110px; right: 160px; top: 900px; text-align: center; opacity: 0; padding: 30px 20px; border-radius: 30px;
        background: var(--orangeD); font-family: "Anton"; font-size: 70px; color: #fff; line-height: 1.02;
        box-shadow: 0 16px 50px rgba(255,106,19,.5); }}
      #e-hin {{ position: absolute; left: 90px; right: 150px; top: 1120px; text-align: center; font-family: "Baloo2"; font-weight: 800;
        font-size: 50px; color: #fff; opacity: 0; }}
      #e-team {{ position: absolute; left: 90px; right: 150px; top: 1200px; text-align: center; font-family: "Mont"; font-weight: 600;
        font-size: 40px; color: rgba(255,255,255,.92); opacity: 0; }}
      #e-ph {{ position: absolute; left: 90px; right: 150px; top: 1275px; display: flex; justify-content: center; opacity: 0; }}
      #e-ph .box {{ display: flex; align-items: center; gap: 22px; padding: 18px 40px; border-radius: 80px; border: 4px solid #fff;
        font-family: "Mont"; font-weight: 800; font-size: 48px; color: #fff; background: rgba(6,16,58,.6); }}
      #e-ph .ic {{ width: 62px; height: 62px; border-radius: 50%; background: var(--orangeD); color: #fff; display: flex; align-items: center; justify-content: center; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="shots">
{videos}
      </div>
      <div id="grade"></div>

      <!-- SCENE 1 -->
      <div id="t_bihar" class="hl clip" data-start="0" data-duration="5.75" data-track-index="5" style="font-size:134px">
        <span class="ln"><span class="in">Bihar has</span></span><span class="ln"><span class="in o">talent.</span></span><span class="bar"></span>
      </div>
      <div id="t_dir" class="hl clip" data-start="8.35" data-duration="3.05" data-track-index="5" style="font-size:100px">
        <span class="ln"><span class="in">It needs the</span></span><span class="ln"><span class="in o">right direction.</span></span><span class="bar"></span>
      </div>

      <!-- SCENE 2: logo reveal -->
      <div id="reveal" class="clip" data-start="12.4" data-duration="3.0" data-track-index="6">
        <div id="rv-ring"></div>
        <div id="rv-wrap"><img src="assets/img/logo.png" alt="" /><div id="rv-shine"><i id="rv-bar"></i></div></div>
      </div>
      <div id="kadi" class="clip" data-start="18.77" data-duration="2.39" data-track-index="6">
        <div id="chipA" class="chip">Cricket<br />Dreams</div>
        <div id="kline"></div>
        <div id="knode"><img src="assets/img/logo.png" alt="" /></div>
        <div id="chipB" class="chip">Right<br />Academy</div>
        <div id="ktitle">The Better Bridge</div>
      </div>
      <div id="stats" class="clip" data-start="21.17" data-duration="2.83" data-track-index="6">
        <div class="stat" id="st5"><div class="num">5</div><div class="lab">Cities</div><div id="dots"><b></b><b></b><b></b><b></b><b></b></div></div>
        <div id="sdiv"></div>
        <div class="stat" id="st20"><div class="num" id="n20">0</div><div class="lab">Branches</div></div>
      </div>
      <div id="l3" class="clip" data-start="24.9" data-duration="3.1" data-track-index="6">
        <div class="card"><div class="k">PROFESSIONAL</div><div class="t">Cricket Academy</div><div class="t" style="color:var(--orange2)">Counselling &amp; Guidance</div></div>
      </div>

      <!-- SCENE 3 -->
      <div id="t_every" class="hl clip" data-start="28.0" data-duration="3.69" data-track-index="5" style="font-size:104px; top:900px">
        <span class="ln"><span class="in">Every child</span></span><span class="ln"><span class="in o">is different.</span></span>
      </div>
      <div id="tags" class="clip" data-start="28.0" data-duration="3.69" data-track-index="7">
        <div class="tag" id="tg1">TALENT</div><div class="tag" id="tg2">AGE</div><div class="tag" id="tg3">NEEDS</div>
      </div>
      <div id="t_right" class="hl clip" data-start="31.7" data-duration="2.03" data-track-index="5" style="font-size:100px">
        <span class="ln"><span class="in">Right guidance</span></span><span class="ln"><span class="in o">matters.</span></span><span class="bar"></span>
      </div>
      <div id="t_pers" class="hl clip" data-start="33.73" data-duration="2.9" data-track-index="5" style="font-size:92px">
        <span class="ln"><span class="in o">Personalized</span></span><span class="ln"><span class="in">academy guidance.</span></span><span class="bar"></span>
      </div>

      <!-- SCENE 4 -->
      <div id="h_dream" class="hi clip" data-start="41.03" data-duration="2.5" data-track-index="5" style="top:1000px; font-size:70px">
        <span class="ln">सपने को सिर्फ <span class="o">सपना</span></span><span class="ln">मत रहने दीजिए</span>
      </div>
      <div id="cta" class="clip" data-start="43.53" data-duration="2.6" data-track-index="6">
        <div class="t1">BOOK YOUR</div><div class="pill" id="ctapill">COUNSELLING TODAY</div>
      </div>
      <div id="team" class="clip" data-start="46.13" data-duration="2.47" data-track-index="6">
        <div class="ring" id="tring">{PHONE_SVG}</div><div class="tx">Our team will<br />connect with you</div>
      </div>
      <div id="h_step" class="hi clip" data-start="51.7" data-duration="3.27" data-track-index="5" style="top:1000px; font-size:70px">
        <span class="ln">हर बड़े सपने की शुरुआत</span><span class="ln"><span class="o">एक सही कदम</span> से</span>
      </div>

      <!-- END CARD -->
      <div id="end" class="clip" data-start="54.97" data-duration="5.03" data-track-index="6">
        <div id="e-logo"><img src="assets/img/logo.png" alt="" /></div>
        <div id="e-tag">सपने आपके,<br /><span class="o">सही मार्गदर्शन हमारा!</span></div>
        <div id="e-cta">BOOK YOUR COUNSELLING TODAY</div>
        <div id="e-hin">आज ही अपनी Counselling Book करें।</div>
        <div id="e-team">Our Team Will Connect With You.</div>
        <div id="e-ph"><div class="box"><div class="ic">{PHONE_SVG}</div><span id="phone" data-var-text="phone">+91 XXXXX XXXXX</span></div></div>
      </div>

      <div id="flash"></div>
      <div id="corner"><img src="assets/img/logo.png" alt="Playvanta" /></div>

      <audio id="vo" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-volume="1" data-track-index="10"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{DUR}" data-volume="0.3" data-track-index="11"></audio>
{sfx_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // camera moves on every shot wrapper
      [
      {moves_js}
      ].forEach(([sel, st, d, a, b]) => tl.fromTo(sel, {{ scale: a }}, {{ scale: b, duration: d, ease: "none" }}, st));

      // headline in/out helper: lines slide up, whole block fades out
      function headline(id, tin, tout) {{
        const el = "#" + id;
        tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, tin);
        tl.fromTo(el + " .in", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.42, ease: "power3.out", stagger: 0.09 }}, tin);
        if (document.querySelector(el + " .bar")) tl.fromTo(el + " .bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power2.out" }}, tin + 0.2);
        tl.to(el, {{ opacity: 0, duration: 0.18 }}, tout - 0.18);
      }}
      function hindi(id, tin, tout) {{
        const el = "#" + id;
        tl.fromTo(el, {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, tin);
        tl.to(el, {{ opacity: 0, duration: 0.2 }}, tout - 0.2);
      }}
      headline("t_bihar", 0.0, 5.75);
      tl.fromTo("#t_bihar .o", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.15, yoyo: true, repeat: 1 }}, 0.75);
      headline("t_dir", 8.35, 11.4);
      tl.fromTo("#t_dir .o", {{ color: "#ffffff" }}, {{ color: "#ff8a1f", duration: 0.3 }}, 9.5);

      // logo reveal: rises from blur, slams on "PLAYVANTA" (14.0)
      tl.fromTo("#rv-wrap", {{ opacity: 0, scale: 0.45, filter: "blur(30px)" }}, {{ opacity: 1, scale: 0.92, filter: "blur(0px)", duration: 1.5, ease: "power2.in" }}, 12.5);
      tl.to("#rv-wrap", {{ scale: 1.0, duration: 0.25, ease: "back.out(3)" }}, 14.0);
      tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.05 }}, 13.98);
      tl.to("#flash", {{ opacity: 0, duration: 0.45, ease: "power2.out" }}, 14.03);
      tl.fromTo("#rv-ring", {{ opacity: 0.9, scale: 1 }}, {{ opacity: 0, scale: 1.7, duration: 0.8, ease: "power2.out", immediateRender: false }}, 14.0);
      tl.fromTo("#rv-bar", {{ x: -200, rotation: 18 }}, {{ x: 760, rotation: 18, duration: 0.7, ease: "power2.inOut" }}, 14.3);
      tl.to("#rv-wrap", {{ scale: 1.05, duration: 0.95, ease: "none" }}, 14.25);
      tl.to("#rv-wrap", {{ opacity: 0, scale: 1.25, filter: "blur(12px)", duration: 0.2 }}, 15.2);

      // kadi: dreams <-> right academy, Playvanta in the middle
      tl.fromTo("#chipA", {{ opacity: 0, x: -80 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, 18.8);
      tl.fromTo("#chipB", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, 19.0);
      tl.fromTo("#kline", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power2.inOut" }}, 19.25);
      tl.fromTo("#knode", {{ opacity: 0, scale: 0.2 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, 19.55);
      tl.fromTo("#ktitle", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 19.8);
      tl.to("#kadi", {{ opacity: 0, duration: 0.15 }}, 21.0);

      // stats: 5 cities (dots light one by one) | 20 branches counter
      tl.fromTo("#st5", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 21.17);
      ["#dots b:nth-child(1)", "#dots b:nth-child(2)", "#dots b:nth-child(3)", "#dots b:nth-child(4)", "#dots b:nth-child(5)"].forEach((s, k) =>
        tl.fromTo(s, {{ backgroundColor: "rgba(255,255,255,0.25)", scale: 1 }}, {{ backgroundColor: "#ff6a13", scale: 1.25, duration: 0.12 }}, 21.35 + k * 0.14));
      tl.fromTo("#sdiv", {{ opacity: 0, scaleY: 0 }}, {{ opacity: 1, scaleY: 1, duration: 0.3 }}, 21.9);
      tl.fromTo("#st20", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 22.1);
      const ctr = {{ v: 0 }};
      tl.fromTo(ctr, {{ v: 0 }}, {{ v: 20, duration: 0.8, ease: "power1.out", onUpdate: () => {{ document.getElementById("n20").textContent = Math.round(ctr.v); }} }}, 22.18);
      tl.fromTo("#n20", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.12, yoyo: true, repeat: 1 }}, 22.98);
      tl.to("#stats", {{ opacity: 0, duration: 0.15 }}, 23.85);

      // lower third
      tl.fromTo("#l3", {{ opacity: 0, x: -120 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 24.95);
      tl.fromTo("#l3 .t", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.18 }}, 25.2);
      tl.to("#l3", {{ opacity: 0, duration: 0.18 }}, 27.82);

      // scene 3
      headline("t_every", 28.0, 31.69);
      [["#tg1", 28.9], ["#tg2", 29.6], ["#tg3", 30.22]].forEach(([s, t]) => {{
        tl.fromTo(s, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }}, t);
        tl.fromTo(s, {{ backgroundColor: "rgba(207,74,0,1)" }}, {{ backgroundColor: "rgba(255,255,255,0.14)", duration: 0.6 }}, t + 0.35);
      }});
      tl.to("#tags", {{ opacity: 0, duration: 0.18 }}, 31.5);
      headline("t_right", 31.7, 33.73);
      headline("t_pers", 33.73, 36.63);

      // scene 4
      hindi("h_dream", 41.1, 43.53);
      tl.fromTo("#cta", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 43.55);
      tl.fromTo("#ctapill", {{ scale: 0.7 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2.2)" }}, 43.75);
      tl.to("#ctapill", {{ scale: 1.08, duration: 0.14, yoyo: true, repeat: 1, ease: "power1.inOut" }}, 45.52);
      tl.to("#cta", {{ opacity: 0, duration: 0.15 }}, 45.98);
      tl.fromTo("#team", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 46.15);
      tl.fromTo("#tring", {{ rotation: -14 }}, {{ rotation: 14, duration: 0.09, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 46.5);
      tl.to("#team", {{ opacity: 0, duration: 0.15 }}, 48.45);
      hindi("h_step", 51.75, 54.97);

      // end card
      tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.7, duration: 0.05 }}, 54.95);
      tl.to("#flash", {{ opacity: 0, duration: 0.4 }}, 55.0);
      tl.fromTo("#e-logo", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.8)" }}, 54.98);
      tl.to("#e-logo", {{ scale: 1.04, duration: 4.3, ease: "none" }}, 55.6);
      tl.fromTo("#e-tag", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 55.35);
      tl.fromTo("#e-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, 56.2);
      tl.fromTo("#e-hin", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, 56.6);
      tl.fromTo("#e-team", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, 56.85);
      tl.fromTo("#e-ph", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, 57.1);
      tl.to("#e-cta", {{ scale: 1.04, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 57.0);

      // corner logo: settle in at frame 0 and stay
      tl.fromTo("#corner", {{ opacity: 0.0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(html)
print("wrote index.html")
