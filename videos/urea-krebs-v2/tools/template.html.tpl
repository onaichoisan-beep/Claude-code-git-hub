<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Playfair Display"; font-weight: 900; font-style: normal; src: url("assets/fonts/playfair-900.ttf"); }
      @font-face { font-family: "Playfair Display"; font-weight: 700; font-style: italic; src: url("assets/fonts/playfair-700i.ttf"); }
      @font-face { font-family: "Bagel Fat One"; font-weight: 400; src: url("assets/fonts/bagel.ttf"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-800.ttf"); }
      :root { --blue: #c4dae8; --butter: #feefb8; --choco: #432f2e; --cream: #fffcf2; --orange: #e8743b; --orange-text: #b2461a; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--butter); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; color: var(--choco);
        background: radial-gradient(circle, rgba(159, 192, 214, 0.45) 3px, transparent 4px) 0 0 / 46px 46px, var(--butter); }
      .scene { position: absolute; inset: 0; }

      #logo { position: absolute; left: 40px; top: 60px; width: 470px; height: 140px; }
      #topic { position: absolute; right: 52px; top: 94px; height: 64px; padding: 0 28px; border-radius: 32px; background: var(--choco);
        color: var(--butter); font: 800 30px/64px "Inter"; letter-spacing: 0.06em; }

      /* hook */
      #hook-title { position: absolute; left: 0; top: 215px; width: 1080px; text-align: center; font: 900 150px/1 "Playfair Display"; }
      #bike-card { position: absolute; left: 90px; top: 400px; width: 900px; height: 600px; border-radius: 34px; overflow: hidden; border: 10px solid var(--choco); }
      #bike-img { position: absolute; left: 0; top: 0; width: 900px; height: 600px; object-fit: cover; }
      #bike-rings { position: absolute; left: 90px; top: 400px; width: 900px; height: 600px; overflow: visible; }

      /* diagram */
      #diagram-svg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
      .node-text { font: 800 30px "Inter"; }
      .ring-title { font: 900 46px "Playfair Display"; fill: var(--choco); }
      #chip-liver { position: absolute; left: 380px; top: 230px; width: 320px; height: 210px; border-radius: 24px; overflow: hidden; border: 8px solid var(--choco); }
      #chip-liver img { position: absolute; left: -220px; top: -185px; width: 823px; height: 768px; }
      #chip-liver div { position: absolute; left: 0; bottom: 0; width: 100%; height: 46px; background: var(--choco); color: var(--butter); font: 800 30px/46px "Inter"; text-align: center; }
      .banner { opacity: 0; position: absolute; left: 60px; top: 905px; width: 960px; height: 96px; border-radius: 48px; background: var(--choco);
        color: var(--butter); font: 800 40px/96px "Inter"; text-align: center; white-space: nowrap; }
      .banner em { font-style: normal; color: var(--orange); }
      .token { opacity: 0; position: absolute; left: 0; top: 0; height: 62px; padding: 0 24px; border-radius: 31px; font: 800 32px/54px "Inter"; white-space: nowrap; border: 4px solid var(--choco); }
      #name-title { opacity: 0; position: absolute; left: 0; top: 890px; width: 1080px; text-align: center; font: 900 110px/1.1 "Playfair Display"; }
      #name-title span { font-style: italic; font-weight: 700; color: var(--orange-text); }

      /* question + cta */
      #q-card { position: absolute; left: 60px; top: 240px; width: 960px; height: 780px; border-radius: 40px; background: var(--cream); border: 10px solid var(--choco); padding: 44px 50px; }
      #q-tag { display: inline-block; height: 62px; padding: 0 28px; border-radius: 31px; background: var(--orange); color: var(--cream); font: 800 32px/62px "Inter"; letter-spacing: 0.08em; }
      #q-text { margin-top: 24px; font: 900 64px/1.12 "Playfair Display"; }
      .opt { margin-top: 20px; height: 84px; border-radius: 42px; border: 5px solid var(--choco); background: var(--butter); font: 800 36px/74px "Inter"; padding-left: 24px; white-space: nowrap; }
      .opt b { display: inline-block; width: 56px; height: 56px; border-radius: 28px; background: var(--choco); color: var(--butter); text-align: center; line-height: 56px; margin-right: 16px; font-size: 30px; }
      #cta-logo { position: absolute; left: 40px; top: 230px; width: 1000px; height: 460px; }
      #cta-answer { position: absolute; left: 0; top: 690px; width: 1080px; text-align: center; font: 700 italic 64px "Playfair Display"; }
      #cta-answer span { color: var(--orange-text); }
      #follow-btn { position: absolute; left: 290px; top: 820px; width: 500px; height: 124px; border-radius: 62px; background: var(--choco); color: var(--butter); font: 400 64px/124px "Bagel Fat One"; text-align: center; }

      /* pixy rig */
      #pixy { position: absolute; inset: 0; }
      #rig { position: absolute; left: 0; top: 0; width: 600px; height: 790px; }
      #rig img { position: absolute; left: 0; top: 0; width: 600px; height: 790px; }
      .fx { position: absolute; left: 0; top: 0; width: 170px; height: 170px; opacity: 0; }
      .body, .mouth { opacity: 0; }
      #body-p1_shock_down, #mouth-closed { opacity: 1; }

      /* captions */
      .cap { position: absolute; left: 0; top: 1062px; width: 1080px; height: 110px; text-align: center; }
      .capt { display: inline-block; padding: 4px 30px 12px; border-radius: 30px; background: rgba(255, 252, 242, 0.94); border: 5px solid var(--choco);
        font: 400 62px/1.25 "Bagel Fat One"; color: var(--choco); white-space: nowrap; }
      .capt .hl { color: var(--orange-text); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1080" data-height="1920">

      <div id="header" class="clip" data-start="0" data-duration="@question@" data-track-index="7">
        <svg id="logo" viewBox="0 0 470 140">
          <g transform="rotate(-9 235 70)">
            <text x="12" y="96" font-family="Playfair Display" font-weight="900" font-size="44" fill="#432f2e">SCROLL</text>
            <text x="196" y="108" font-family="Playfair Display" font-weight="900" font-size="88" fill="#c4dae8" stroke="#432f2e" stroke-width="3" paint-order="stroke">2</text>
            <text x="250" y="74" font-family="Playfair Display" font-weight="900" font-size="44" fill="#432f2e">SCORE</text>
          </g>
        </svg>
        <div id="topic">UREA × KREBS</div>
      </div>

      <div id="s-hook" class="scene clip" data-start="0" data-duration="@wheels@" data-track-index="1">
        <div id="bike-card"><img id="bike-img" src="assets/img/bicycle.jpg" alt="bicycle" /></div>
        <svg id="bike-rings" viewBox="0 0 900 600">
          <circle id="bw1" cx="152" cy="430" r="138" fill="none" stroke="#c4dae8" stroke-width="18" />
          <circle id="bw2" cx="673" cy="430" r="138" fill="none" stroke="#e8743b" stroke-width="18" />
          <g id="bt1"><rect x="52" y="230" width="200" height="66" rx="33" fill="#c4dae8" stroke="#432f2e" stroke-width="5" /><text x="152" y="276" text-anchor="middle" font-family="Inter" font-weight="800" font-size="38" fill="#432f2e">UREA</text></g>
          <g id="bt2"><rect x="563" y="230" width="220" height="66" rx="33" fill="#e8743b" stroke="#432f2e" stroke-width="5" /><text x="673" y="276" text-anchor="middle" font-family="Inter" font-weight="800" font-size="38" fill="#fffcf2">KREBS</text></g>
        </svg>
        <div id="hook-title">RUKO!</div>
      </div>

      <div id="s-diagram" class="scene clip" data-start="@wheels@" data-duration="0" data-track-index="2">
        <svg id="diagram-svg" viewBox="0 0 1080 1920"></svg>
        <div id="chip-liver"><img src="assets/img/abdomen.jpg" alt="liver" /><div>LIVER</div></div>
        <div id="tok-fum" class="token" style="background: #e8743b; color: #fffcf2">Fumarate</div>
        <div id="tok-asp" class="token" style="background: #c4dae8">Aspartate</div>
        <div id="ban-1" class="banner">ASA <em>✂ lyase</em> → Arginine + <em>Fumarate</em></div>
        <div id="ban-2" class="banner"><em>Fumarate</em> → Malate → OAA → <em>Aspartate</em></div>
        <div id="name-title">KREBS <span>bi</span>CYCLE</div>
      </div>

      <div id="s-question" class="scene clip" data-start="@question@" data-duration="0" data-track-index="3">
        <div id="q-card">
          <div id="q-tag">NEET QUESTION</div>
          <div id="q-text">Fumarate kaunsa enzyme release karta hai?</div>
          <div class="opt"><b>A</b>Arginase</div>
          <div class="opt"><b>B</b>Argininosuccinate lyase</div>
          <div class="opt"><b>C</b>Fumarase</div>
          <div class="opt"><b>D</b>Argininosuccinate synthetase</div>
        </div>
      </div>

      <div id="s-cta" class="scene clip" data-start="@cta@" data-duration="0" data-track-index="4">
        <svg id="cta-logo" viewBox="0 0 1000 460">
          <g transform="rotate(-12 500 230)">
            <text x="30" y="300" font-family="Playfair Display" font-weight="900" font-size="104" fill="#432f2e">SCROLL</text>
            <text x="455" y="330" font-family="Playfair Display" font-weight="900" font-size="250" fill="#c4dae8" stroke="#432f2e" stroke-width="6" paint-order="stroke">2</text>
            <text x="600" y="235" font-family="Playfair Display" font-weight="900" font-size="104" fill="#432f2e">SCORE</text>
          </g>
        </svg>
        <div id="cta-answer">Answer → <span>agli reel</span> mein</div>
        <div id="follow-btn">FOLLOW</div>
      </div>

      <!-- Pixy: one rig for the whole film; body layers swap expression, mouth layers lip-sync to the voice -->
      <div id="pixy" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="8">
        <div id="rig">
          __BODIES__
          __MOUTHS__
        </div>
        __FX__
      </div>

      __CAPS__

      <audio id="vo" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="__TOTAL__" data-track-index="10" data-volume="1"></audio>
      __SFX__
    </div>

    <script>
      const T = __T__;
      const C = __CUES__;
      const LIPS = __LIPS__;
      const EXPR = __EXPR__;
      const RIG = __RIG__;
      const POPS = __POPS__;
      const NS = "http://www.w3.org/2000/svg";
      const setDur = (id, a, b) => document.getElementById(id).setAttribute("data-duration", (b - a).toFixed(3));
      setDur("s-diagram", T.wheels, T.question); setDur("s-question", T.question, T.cta); setDur("s-cta", T.cta, T.end);

      // ---- diagram ----
      const svg = document.getElementById("diagram-svg");
      const el = (tag, a, p = svg) => { const n = document.createElementNS(NS, tag); for (const k in a) n.setAttribute(k, a[k]); p.appendChild(n); return n; };
      const U = { x: 275, y: 640 }, K = { x: 805, y: 640 }, R = 165;
      el("path", { id: "chain", d: "M 275 425 L 805 425 A 215 215 0 0 1 805 855 L 275 855 A 215 215 0 0 1 275 425 Z", fill: "none", stroke: "#432f2e", "stroke-width": 12, "stroke-dasharray": "22 12" });
      el("path", { id: "chain-top", opacity: 0, d: "M 275 425 L 805 425", fill: "none", stroke: "#e8743b", "stroke-width": 16, "stroke-linecap": "round" });
      el("path", { id: "chain-bot", opacity: 0, d: "M 805 855 L 275 855", fill: "none", stroke: "#9fc0d6", "stroke-width": 16, "stroke-linecap": "round" });
      const frame = el("g", { id: "frame", opacity: 0 });
      [[275, 640, 540, 700], [540, 700, 460, 470], [275, 640, 460, 470], [460, 470, 760, 485], [540, 700, 760, 485], [760, 485, 805, 640]]
        .forEach(([a, b, c, d]) => el("line", { x1: a, y1: b, x2: c, y2: d, stroke: "#432f2e", "stroke-width": 12, "stroke-linecap": "round" }, frame));
      el("rect", { x: 410, y: 442, width: 110, height: 26, rx: 13, fill: "#432f2e" }, frame);
      el("circle", { cx: 540, cy: 700, r: 24, fill: "#fffcf2", stroke: "#432f2e", "stroke-width": 8 }, frame);
      [[U, "#c4dae8", "uw", "UREA"], [K, "#e8743b", "kw", "KREBS"]].forEach(([c, col, id, name]) => {
        const g = el("g", { id });
        el("circle", { id: id + "-tread", cx: c.x, cy: c.y, r: R + 16, fill: "none", stroke: "#432f2e", "stroke-width": 6, "stroke-dasharray": "6 18" }, g);
        el("circle", { cx: c.x, cy: c.y, r: R, fill: "#fffcf2", stroke: col, "stroke-width": 22 }, g);
        el("text", { x: c.x, y: c.y - 4, "text-anchor": "middle", class: "ring-title" }, g).textContent = name;
        el("text", { x: c.x, y: c.y + 42, "text-anchor": "middle", class: "ring-title", "font-size": 36 }, g).textContent = "cycle";
      });
      const node = (id, x, y, label, fill = "#feefb8", txt = "#432f2e") => {
        const g = el("g", { id, opacity: 0 }); const w = label.length * 18 + 44;
        el("rect", { x: x - w / 2, y: y - 30, width: w, height: 60, rx: 30, fill, stroke: "#432f2e", "stroke-width": 5 }, g);
        const t = el("text", { x, y: y + 11, "text-anchor": "middle", class: "node-text" }, g); t.textContent = label; t.setAttribute("style", `fill:${txt}`);
      };
      node("n-cit", 275, 805, "Citrulline"); node("n-asa", 110, 640, "ASA"); node("n-arg", 275, 475, "Arginine");
      node("n-fum", 805, 475, "Fumarate", "#e8743b", "#fffcf2"); node("n-mal", 970, 640, "Malate"); node("n-oaa", 805, 805, "OAA");

      // ---- timeline ----
      const tl = gsap.timeline({ paused: true });
      const pop = (sel, t, from = 0.5) => tl.fromTo(sel, { opacity: 0, scale: from, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)" }, t);
      const out = (sel, t) => tl.to(sel, { opacity: 0, duration: 0.2, ease: "power2.in" }, t);

      tl.fromTo("#logo", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 0.05);
      tl.fromTo("#topic", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 0.1);

      // hook
      tl.fromTo("#hook-title", { opacity: 0, scale: 2.4, rotation: -10 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.3, ease: "back.out(2)" }, C.ruko);
      tl.fromTo("#bike-card", { opacity: 0, y: 140, rotation: 7 }, { opacity: 1, y: 0, rotation: -2, duration: 0.45, ease: "power3.out" }, 0.1);
      tl.fromTo("#bike-img", { scale: 1 }, { scale: 1.15, duration: T.wheels, ease: "none" }, 0.1);
      tl.fromTo("#bike-rings", { opacity: 0 }, { opacity: 1, duration: 0.01 }, C.bicycle - 0.25);
      ["#bw1", "#bw2"].forEach((s, i) => tl.fromTo(s, { strokeDasharray: 880, strokeDashoffset: 880 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, C.bicycle - 0.25 + i * 0.15));
      pop("#bt1", C.bicycle); pop("#bt2", C.bicycle + 0.15);
      tl.to("#bike-card, #bike-rings", { scale: 0.5, opacity: 0, duration: 0.3, ease: "power2.in" }, T.wheels - 0.3);
      tl.to("#hook-title", { y: -60, opacity: 0, duration: 0.25 }, T.wheels - 0.3);

      // wheels
      tl.fromTo("#uw", { opacity: 0, scale: 0.3, transformOrigin: "275px 640px" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, C.urea - 0.15);
      tl.fromTo("#kw", { opacity: 0, scale: 0.3, transformOrigin: "805px 640px" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, C.krebs - 0.15);
      tl.fromTo("#chip-liver", { opacity: 0, y: -30, rotation: -8 }, { opacity: 1, y: 0, rotation: -3, duration: 0.35, ease: "back.out(2)" }, T.wheels + 0.05);
      out("#chip-liver", T.split - 0.1);
      tl.fromTo("#chain", { opacity: 0 }, { opacity: 0.3, duration: 0.3 }, T.split);

      // split: ASA cut -> fumarate
      pop("#n-cit", T.split); pop("#n-asa", C.asa - 0.1); pop("#ban-1", C.asa);
      tl.to("#n-asa", { x: -10, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }, C.tootta);
      pop("#n-arg", C.tootta + 0.3);
      tl.fromTo("#tok-fum", { opacity: 0, x: 60, y: 520, scale: 0.3 }, { opacity: 1, x: 150, y: 520, scale: 1.15, duration: 0.4, ease: "back.out(2.4)", immediateRender: false }, C.fum1 - 0.05);
      out("#ban-1", T.chain - 0.15);

      // chain: fumarate rides the top chain into Krebs
      tl.to("#chain", { opacity: 1, duration: 0.25 }, T.chain);
      tl.fromTo("#chain-top", { opacity: 1, strokeDasharray: 530, strokeDashoffset: 530 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut", immediateRender: false }, C.chainw - 0.2);
      tl.to("#tok-fum", { x: 240, y: 394, scale: 1, duration: 0.3, ease: "power2.inOut" }, C.chainw);
      tl.to("#tok-fum", { x: 700, y: 394, duration: Math.max(0.4, C.jaata - C.chainw - 0.45), ease: "power1.inOut" }, C.chainw + 0.32);
      tl.to("#tok-fum", { opacity: 0, scale: 0.5, duration: 0.2 }, C.jaata - 0.1);
      pop("#n-fum", C.jaata); pop("#ban-2", T.chain + 0.2);
      pop("#n-mal", C.jaata + 0.3); pop("#n-oaa", C.jaata + 0.55);

      // back: aspartate returns on the bottom chain
      tl.fromTo("#chain-bot", { opacity: 1, strokeDasharray: 530, strokeDashoffset: 530 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut", immediateRender: false }, C.aspartate - 0.2);
      tl.fromTo("#tok-asp", { opacity: 0, x: 720, y: 824, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, C.aspartate - 0.1);
      tl.to("#tok-asp", { x: 190, y: 824, duration: Math.max(0.5, C.aata - C.aspartate), ease: "power1.inOut" }, C.aspartate + 0.22);
      tl.to("#tok-asp", { opacity: 0, scale: 0.5, duration: 0.2 }, C.aata + 0.3);
      out("#ban-2", T.name - 0.15);
      const roll = T.question - C.aspartate;
      tl.fromTo("#uw-tread", { rotation: 0, svgOrigin: "275 640" }, { rotation: 360, svgOrigin: "275 640", duration: roll, ease: "none" }, C.aspartate);
      tl.fromTo("#kw-tread", { rotation: 0, svgOrigin: "805 640" }, { rotation: 360, svgOrigin: "805 640", duration: roll, ease: "none" }, C.aspartate);
      tl.fromTo("#chain", { strokeDashoffset: 0 }, { strokeDashoffset: -300, duration: roll, ease: "none" }, C.aspartate);

      // name
      tl.to("#frame", { opacity: 1, duration: 0.35 }, C.kbike - 0.4);
      tl.fromTo("#name-title", { opacity: 0, y: 40, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2.2)", immediateRender: false }, C.kbike);

      // question
      tl.fromTo("#q-card", { opacity: 0, y: 160, rotation: 3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.6)" }, T.question);
      tl.fromTo("#q-tag", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, T.question + 0.2);
      gsap.utils.toArray(".opt").forEach((o, i) => tl.fromTo(o, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }, C.enzyme - 0.3 + i * 0.1));

      // cta
      tl.fromTo("#cta-logo", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, T.cta);
      tl.fromTo("#cta-answer", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, T.cta + 0.2);
      tl.fromTo("#follow-btn", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, C.follow - 0.2);
      tl.to("#follow-btn", { scale: 0.9, duration: 0.1, yoyo: true, repeat: 1 }, C.follow + 0.3);
      tl.fromTo("#follow-btn", { backgroundColor: "#432f2e" }, { backgroundColor: "#e8743b", duration: 0.2, immediateRender: false }, C.follow + 0.4);

      // ---- Pixy rig: placement moves (full body <-> bust), sway, expression pops, lip-sync ----
      tl.set("#rig", { x: RIG[0].x, y: RIG[0].y, scale: RIG[0].s, transformOrigin: "50% 0%" }, 0);
      RIG.slice(1).forEach((r) => tl.to("#rig", { x: r.x, y: r.y, scale: r.s, duration: 0.45, ease: "back.out(1.4)" }, r.t));
      // idle sway + talking bob (finite repeats inside the root duration)
      tl.fromTo("#rig", { rotation: -2.5 }, { rotation: 2.5, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: Math.floor(T.end / 0.8) - 1, transformOrigin: "50% 100%" }, 0);
      // expressions: swap body layer, squash-stretch pop
      EXPR.forEach((e) => {
        if (e.t > 0) tl.set("#body-" + e.layer, { opacity: 1 }, e.t);
        if (e.prev) tl.set("#body-" + e.prev, { opacity: 0 }, e.t);
        tl.fromTo("#rig img", { scaleY: 0.9, scaleX: 1.08, transformOrigin: "50% 100%" }, { scaleY: 1, scaleX: 1, duration: 0.35, ease: "elastic.out(1.2, 0.45)", immediateRender: false }, e.t);
      });
      // lip-sync
      let prevM = "closed";
      LIPS.forEach(([t, m]) => { if (m === prevM) return; tl.set("#mouth-" + prevM, { opacity: 0 }, t); tl.set("#mouth-" + m, { opacity: 1 }, t); prevM = m; });
      // pop-up reactions next to his head
      POPS.forEach((p) => {
        tl.fromTo("#" + p.id, { opacity: 0, scale: 0.2, rotation: -25, x: p.x, y: p.y, transformOrigin: "50% 50%" },
          { opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(3)", immediateRender: false }, p.t);
        tl.to("#" + p.id, { y: p.y - 30, duration: 0.6, ease: "sine.out" }, p.t + 0.35);
        tl.to("#" + p.id, { opacity: 0, scale: 0.6, duration: 0.2 }, p.t + 1.0);
      });

      gsap.utils.toArray(".capt").forEach((c) => {
        const s = parseFloat(c.parentElement.getAttribute("data-start"));
        tl.fromTo(c, { scale: 0.8, y: 12 }, { scale: 1, y: 0, duration: 0.16, ease: "back.out(3)" }, s);
      });

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
