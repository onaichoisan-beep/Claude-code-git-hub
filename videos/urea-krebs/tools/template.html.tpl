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
      @font-face { font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-600.ttf"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-800.ttf"); }
      :root {
        --blue: #c4dae8; --blue-d: #9fc0d6; --butter: #feefb8; --choco: #432f2e; --cream: #fffcf2; --orange: #e8743b;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--butter); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; color: var(--choco);
        background: radial-gradient(circle, rgba(159, 192, 214, 0.45) 3px, transparent 4px) 0 0 / 46px 46px, var(--butter); }
      .scene { position: absolute; inset: 0; }
      .abs { position: absolute; }

      /* header */
      #header { position: absolute; inset: 0; }
      #logo { position: absolute; left: 40px; top: 70px; width: 470px; height: 140px; }
      #topic { position: absolute; right: 52px; top: 104px; height: 64px; padding: 0 28px; border-radius: 32px; background: var(--choco);
        color: var(--butter); font: 800 30px/64px "Inter"; letter-spacing: 0.06em; }

      /* hook */
      #hook-title { position: absolute; left: 0; top: 230px; width: 1080px; text-align: center; font: 900 170px/1 "Playfair Display"; }
      #bike-card { position: absolute; left: 50px; top: 470px; width: 980px; height: 653px; border-radius: 34px; overflow: hidden;
        border: 10px solid var(--choco); background: var(--cream); }
      #bike-img { position: absolute; left: 0; top: 0; width: 980px; height: 653px; object-fit: cover; }
      #bike-rings { position: absolute; left: 50px; top: 470px; width: 980px; height: 653px; overflow: visible; }
      .wheel-tag { font: 800 40px "Inter"; }

      /* diagram */
      #diagram-svg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
      .node-text { font: 800 30px "Inter"; fill: var(--choco); }
      .ring-title { font: 900 50px "Playfair Display"; fill: var(--choco); }
      .chip { position: absolute; width: 300px; height: 230px; border-radius: 26px; overflow: hidden; border: 8px solid var(--choco); background: var(--cream); }
      .chip img { position: absolute; }
      .chip-label { position: absolute; left: 0; bottom: 0; width: 100%; height: 48px; background: var(--choco); color: var(--butter);
        font: 800 30px/48px "Inter"; text-align: center; letter-spacing: 0.06em; }
      .banner { position: absolute; left: 60px; top: 1075px; width: 960px; height: 104px; border-radius: 52px; background: var(--choco);
        color: var(--butter); font: 800 40px/104px "Inter"; text-align: center; white-space: nowrap; }
      .banner em { font-style: normal; color: var(--orange); }
      .token { position: absolute; left: 0; top: 0; height: 64px; padding: 0 26px; border-radius: 32px; font: 800 32px/58px "Inter";
        white-space: nowrap; border: 4px solid var(--choco); }
      .tag { position: absolute; height: 58px; padding: 0 22px; border-radius: 12px; font: 800 28px/58px "Inter"; white-space: nowrap;
        background: var(--cream); border: 4px dashed var(--choco); }
      #name-title { position: absolute; left: 0; top: 1060px; width: 1080px; text-align: center; font: 900 104px/1.1 "Playfair Display"; }
      #name-title span { font-style: italic; font-weight: 700; color: var(--orange-text); }
      #sticky { position: absolute; left: 360px; top: 1430px; width: 400px; height: 190px; background: var(--blue); border: 6px solid var(--choco);
        border-radius: 10px; text-align: center; padding-top: 22px; }
      #sticky .s1 { font: 800 30px "Inter"; letter-spacing: 0.06em; }
      #sticky .s2 { font: 400 66px/1.3 "Bagel Fat One"; color: var(--orange-text); }

      /* question */
      #q-card { position: absolute; left: 60px; top: 300px; width: 960px; height: 900px; border-radius: 40px; background: var(--cream);
        border: 10px solid var(--choco); padding: 50px 54px; }
      #q-tag { display: inline-block; height: 66px; padding: 0 30px; border-radius: 33px; background: var(--orange); color: var(--cream);
        font: 800 34px/66px "Inter"; letter-spacing: 0.08em; }
      #q-text { margin-top: 30px; font: 900 70px/1.12 "Playfair Display"; }
      .opt { margin-top: 26px; height: 92px; border-radius: 46px; border: 5px solid var(--choco); background: var(--butter);
        font: 800 38px/82px "Inter"; padding-left: 28px; white-space: nowrap; }
      .opt b { display: inline-block; width: 60px; height: 60px; border-radius: 30px; background: var(--choco); color: var(--butter);
        text-align: center; line-height: 60px; margin-right: 18px; font-size: 32px; }

      /* cta */
      #cta-logo { position: absolute; left: 40px; top: 300px; width: 1000px; height: 460px; }
      #cta-answer { position: absolute; left: 0; top: 820px; width: 1080px; text-align: center; font: 700 italic 66px "Playfair Display"; }
      #cta-answer span { color: var(--orange-text); }
      #follow-btn { position: absolute; left: 290px; top: 960px; width: 500px; height: 130px; border-radius: 65px; background: var(--choco);
        color: var(--butter); font: 400 66px/130px "Bagel Fat One"; text-align: center; }
      #tap { position: absolute; left: 640px; top: 1000px; width: 110px; height: 110px; border-radius: 55px; border: 8px solid var(--orange); }
      #comment-bubble { position: absolute; left: 640px; top: 1430px; width: 330px; height: 150px; }

      /* pixy + captions */
      .pixy { position: absolute; inset: 0; }
      .pixy img { position: absolute; left: 14px; top: 1405px; width: 340px; height: 448px; }
      .cap { position: absolute; left: 0; top: 1240px; width: 1080px; height: 120px; text-align: center; }
      .capt { display: inline-block; padding: 6px 30px 14px; border-radius: 30px; background: rgba(255, 252, 242, 0.92); border: 5px solid var(--choco);
        font: 400 64px/1.25 "Bagel Fat One"; color: var(--choco); white-space: nowrap; }
      .capt .hl { color: var(--orange-text); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1080" data-height="1920">

      <!-- persistent header -->
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

      <!-- 1. hook -->
      <div id="s-hook" class="scene clip" data-start="@hook@" data-duration="@wheels@" data-track-index="1">
        <div id="hook-title">RUKO!</div>
        <div id="bike-card"><img id="bike-img" src="assets/img/bicycle.jpg" alt="bicycle" /></div>
        <svg id="bike-rings" viewBox="0 0 980 653">
          <circle id="bw1" cx="165" cy="468" r="150" fill="none" stroke="#c4dae8" stroke-width="18" />
          <circle id="bw2" cx="733" cy="468" r="150" fill="none" stroke="#e8743b" stroke-width="18" />
          <g id="bt1"><rect x="55" y="250" width="220" height="70" rx="35" fill="#c4dae8" stroke="#432f2e" stroke-width="5" /><text x="165" y="300" text-anchor="middle" class="wheel-tag" fill="#432f2e">UREA</text></g>
          <g id="bt2"><rect x="613" y="250" width="240" height="70" rx="35" fill="#e8743b" stroke="#432f2e" stroke-width="5" /><text x="733" y="300" text-anchor="middle" class="wheel-tag" fill="#fffcf2">KREBS</text></g>
        </svg>
      </div>

      <!-- 2-7. the two-wheel diagram -->
      <div id="s-diagram" class="scene clip" data-start="@wheels@" data-duration="0" data-track-index="2">
        <svg id="diagram-svg" viewBox="0 0 1080 1920"></svg>
        <div id="chip-liver" class="chip abs" style="left: 60px; top: 260px"><img src="assets/img/abdomen.jpg" alt="liver" style="left: -230px; top: -175px; width: 823px; height: 768px" /><div class="chip-label">LIVER</div></div>
        <div id="chip-mito" class="chip abs" style="left: 720px; top: 260px"><img src="assets/img/mitochondria.jpg" alt="mitochondria" style="left: -40px; top: -20px; width: 420px; height: 315px" /><div class="chip-label">MITOCHONDRIA</div></div>
        <div id="tok-asp" class="token" style="background: #c4dae8">Aspartate</div>
        <div id="tok-fum" class="token" style="background: #e8743b; color: #fffcf2">Fumarate</div>
        <div id="tag-asl" class="tag" style="left: 40px; top: 655px">✂ ASA lyase</div>
        <div id="tag-ast" class="tag" style="left: 640px; top: 1010px">transamination</div>
        <div id="ban-1" class="banner">Citrulline + <em>Aspartate</em> → ASA</div>
        <div id="ban-2" class="banner">ASA → Arginine + <em>Fumarate</em></div>
        <div id="ban-3" class="banner"><em>Fumarate</em> → Malate → OAA</div>
        <div id="ban-4" class="banner">OAA → <em>Aspartate</em> → back to urea</div>
        <div id="name-title">KREBS <span>bi</span>CYCLE</div>
        <div id="sticky"><div class="s1">LINK YAAD RAKHO</div><div class="s2">fumarate!</div></div>
      </div>

      <!-- 8. question -->
      <div id="s-question" class="scene clip" data-start="@question@" data-duration="0" data-track-index="3">
        <div id="q-card">
          <div id="q-tag">NEET QUESTION</div>
          <div id="q-text">Urea cycle mein fumarate kaunsa enzyme release karta hai?</div>
          <div id="q-opts">
            <div class="opt"><b>A</b>Arginase</div>
            <div class="opt"><b>B</b>Argininosuccinate lyase</div>
            <div class="opt"><b>C</b>Fumarase</div>
            <div class="opt"><b>D</b>Argininosuccinate synthetase</div>
          </div>
        </div>
      </div>

      <!-- 9. cta -->
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
        <div id="tap"></div>
        <svg id="comment-bubble" viewBox="0 0 330 150">
          <path d="M 20 20 H 310 Q 320 20 320 30 V 100 Q 320 110 310 110 H 90 L 50 140 L 58 110 H 20 Q 10 110 10 100 V 30 Q 10 20 20 20 Z" fill="#fffcf2" stroke="#432f2e" stroke-width="6" />
          <text x="165" y="80" text-anchor="middle" font-family="Bagel Fat One" font-size="44" fill="#432f2e">A/B/C/D?</text>
        </svg>
      </div>

      <!-- pixy -->
      __PIXY__

      <!-- captions -->
      __CAPS__

      <!-- audio -->
      <audio id="vo" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="__TOTAL__" data-track-index="10" data-volume="1"></audio>
      __SFX__
    </div>

    <script>
      const T = __T__;
      const C = __CUES__;
      const NS = "http://www.w3.org/2000/svg";

      // ---- set real durations on the scene clips (start + length from the voice timing) ----
      const setDur = (id, a, b) => document.getElementById(id).setAttribute("data-duration", (b - a).toFixed(3));
      setDur("s-diagram", T.wheels, T.question);
      setDur("s-question", T.question, T.cta);
      setDur("s-cta", T.cta, T.end);

      // ---- build the two-wheel diagram ----
      const svg = document.getElementById("diagram-svg");
      const el = (tag, attrs, parent = svg) => { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); parent.appendChild(n); return n; };
      const U = { x: 270, y: 770 }, K = { x: 810, y: 770 }, R = 185;
      const pt = (c, deg, r = R) => [c.x + r * Math.cos((deg * Math.PI) / 180), c.y + r * Math.sin((deg * Math.PI) / 180)];
      const defs = el("defs", {});
      const mk = el("marker", { id: "arrow", viewBox: "0 0 10 10", refX: "6", refY: "5", markerWidth: "5", markerHeight: "5", orient: "auto" }, defs);
      el("path", { d: "M0 0 L10 5 L0 10 z", fill: "#432f2e" }, mk);

      // chain loop around both wheels
      const chainD = "M 270 530 L 810 530 A 240 240 0 0 1 810 1010 L 270 1010 A 240 240 0 0 1 270 530 Z";
      el("path", { id: "chain", d: chainD, fill: "none", stroke: "#432f2e", "stroke-width": 12, "stroke-dasharray": "22 12", opacity: 0 });
      el("path", { id: "chain-top", d: "M 270 530 L 810 530", fill: "none", stroke: "#e8743b", "stroke-width": 14, "stroke-linecap": "round", opacity: 0 });
      el("path", { id: "chain-bot", d: "M 810 1010 L 270 1010", fill: "none", stroke: "#9fc0d6", "stroke-width": 14, "stroke-linecap": "round", opacity: 0 });

      // bicycle frame (drawn in the "name" beat)
      const frame = el("g", { id: "frame", opacity: 0 });
      [["270,770", "540,830"], ["540,830", "455,575"], ["270,770", "455,575"], ["455,575", "760,590"], ["540,830", "760,590"], ["760,590", "810,770"]]
        .forEach(([a, b]) => el("line", { x1: a.split(",")[0], y1: a.split(",")[1], x2: b.split(",")[0], y2: b.split(",")[1], stroke: "#432f2e", "stroke-width": 12, "stroke-linecap": "round" }, frame));
      el("rect", { x: 405, y: 545, width: 110, height: 26, rx: 13, fill: "#432f2e" }, frame);
      el("path", { d: "M 730 560 Q 760 540 800 552", fill: "none", stroke: "#432f2e", "stroke-width": 12, "stroke-linecap": "round" }, frame);
      el("circle", { cx: 540, cy: 830, r: 26, fill: "#fffcf2", stroke: "#432f2e", "stroke-width": 8 }, frame);

      // wheels: tread (spins), ring, hub title
      [[U, "#c4dae8", "uw", "UREA"], [K, "#e8743b", "kw", "KREBS"]].forEach(([c, col, id, name]) => {
        const g = el("g", { id });
        el("circle", { id: id + "-tread", cx: c.x, cy: c.y, r: R + 18, fill: "none", stroke: "#432f2e", "stroke-width": 6, "stroke-dasharray": "6 18" }, g);
        el("circle", { id: id + "-ring", cx: c.x, cy: c.y, r: R, fill: "#fffcf2", stroke: col, "stroke-width": 22 }, g);
        const t = el("text", { x: c.x, y: c.y - 6, "text-anchor": "middle", class: "ring-title" }, g); t.textContent = name;
        const t2 = el("text", { x: c.x, y: c.y + 46, "text-anchor": "middle", class: "ring-title", "font-size": 40 }, g); t2.textContent = "cycle";
      });

      // arrows: urea clockwise bottom→left→top→right, krebs clockwise top→right→bottom
      const arc = (c, a0, a1, id) => { const [x0, y0] = pt(c, a0), [x1, y1] = pt(c, a1);
        return el("path", { id, d: `M ${x0} ${y0} A ${R} ${R} 0 0 1 ${x1} ${y1}`, fill: "none", stroke: "#432f2e", "stroke-width": 7, "marker-end": "url(#arrow)", opacity: 0 }); };
      arc(U, 112, 160, "ua1"); arc(U, 202, 250, "ua2"); arc(U, 292, 340, "ua3"); arc(U, 22, 70, "ua4");
      arc(K, 292, 340, "ka1"); arc(K, 22, 70, "ka2"); arc(K, 112, 160, "ka3"); arc(K, 202, 250, "ka4");

      // nodes
      const node = (id, x, y, label, fill = "#feefb8", txt = "#432f2e") => {
        const g = el("g", { id, opacity: 0 });
        const w = label.length * 18 + 44;
        el("rect", { x: x - w / 2, y: y - 30, width: w, height: 60, rx: 30, fill, stroke: "#432f2e", "stroke-width": 5 }, g);
        const t = el("text", { x, y: y + 11, "text-anchor": "middle", class: "node-text", fill: txt }, g); t.textContent = label;
        t.setAttribute("style", `fill:${txt}`);
        return g;
      };
      node("n-cit", 270, 955, "Citrulline"); node("n-asa", 85, 770, "ASA"); node("n-arg", 270, 585, "Arginine"); node("n-orn", 455, 770, "Ornithine");
      node("n-fum", 810, 585, "Fumarate", "#e8743b", "#fffcf2"); node("n-mal", 990, 770, "Malate"); node("n-oaa", 810, 955, "OAA"); node("n-akg", 625, 770, "···");

      // ---- timeline ----
      const tl = gsap.timeline({ paused: true });
      const pop = (sel, t, from = 0.6) => tl.fromTo(sel, { opacity: 0, scale: from, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }, t);
      const out = (sel, t, d = 0.25) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, t);

      // header
      tl.fromTo("#logo", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, 0.05);
      tl.fromTo("#topic", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, 0.1);

      // hook
      tl.fromTo("#hook-title", { opacity: 0, scale: 2.2, rotation: -8 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.35, ease: "back.out(2)" }, C.ruko - 0.05);
      tl.fromTo("#bike-card", { opacity: 0, y: 120, rotation: 6 }, { opacity: 1, y: 0, rotation: -2, duration: 0.5, ease: "power3.out" }, 0.2);
      tl.fromTo("#bike-img", { scale: 1.0 }, { scale: 1.12, duration: T.wheels - 0.2, ease: "none" }, 0.2);
      tl.fromTo("#bike-rings", { opacity: 0 }, { opacity: 1, duration: 0.01 }, C.bicycle - 0.3);
      ["#bw1", "#bw2"].forEach((s, i) => tl.fromTo(s, { strokeDasharray: 950, strokeDashoffset: 950 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, C.bicycle - 0.3 + i * 0.2));
      pop("#bt1", C.bicycle + 0.1); pop("#bt2", C.bicycle + 0.3);
      tl.to("#bike-card, #bike-rings", { scale: 0.6, opacity: 0, duration: 0.35, ease: "power2.in" }, T.wheels - 0.4);
      tl.to("#hook-title", { y: -60, opacity: 0, duration: 0.3, ease: "power2.in" }, T.wheels - 0.4);

      // wheels appear
      tl.fromTo("#uw", { opacity: 0, scale: 0.4, transformOrigin: "270px 770px" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, C.urea1 - 0.1);
      tl.fromTo("#kw", { opacity: 0, scale: 0.4, transformOrigin: "810px 770px" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, C.krebs1 - 0.1);
      tl.fromTo("#chip-liver", { opacity: 0, y: -40, rotation: -6 }, { opacity: 1, y: 0, rotation: -4, duration: 0.4, ease: "back.out(2)" }, C.urea1);
      tl.fromTo("#chip-mito", { opacity: 0, y: -40, rotation: 6 }, { opacity: 1, y: 0, rotation: 4, duration: 0.4, ease: "back.out(2)" }, C.krebs1);
      out("#chip-liver, #chip-mito", T.step1 + 0.2);
      // all urea + krebs nodes appear faint, the chain goes in quietly
      ["#n-orn", "#n-akg"].forEach((s, i) => tl.fromTo(s, { opacity: 0 }, { opacity: 0.55, duration: 0.3 }, T.step1 + 0.1 + i * 0.1));
      tl.fromTo("#chain", { opacity: 0 }, { opacity: 0.35, duration: 0.4 }, T.step1 + 0.2);

      // step 1: citrulline + aspartate -> ASA
      pop("#ban-1", T.step1 + 0.2);
      pop("#n-cit", C.citrulline - 0.1);
      tl.fromTo("#tok-asp", { opacity: 0, x: 140, y: 1160 }, { opacity: 1, x: 140, y: 1060, duration: 0.3, ease: "power2.out" }, C.aspartate - 0.2);
      tl.to("#tok-asp", { x: 190, y: 960, scale: 0.6, duration: 0.5, ease: "power2.in" }, C.aspartate + 0.4);
      out("#tok-asp", C.aspartate + 0.85, 0.15);
      tl.fromTo("#ua1", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.asa - 0.3);
      pop("#n-asa", C.asa);
      out("#ban-1", T.step2 - 0.2);

      // step 2: ASA lyase splits ASA -> arginine + fumarate
      pop("#ban-2", T.step2 + 0.05);
      pop("#tag-asl", C.lyase - 0.1, 0.3);
      tl.to("#n-asa", { x: -12, duration: 0.06, repeat: 5, yoyo: true, ease: "none" }, C.todta);
      tl.fromTo("#ua2", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.arginine - 0.3);
      pop("#n-arg", C.arginine);
      tl.fromTo("#tok-fum", { opacity: 0, x: 40, y: 600, scale: 0.4 }, { opacity: 1, x: 60, y: 420, scale: 1, duration: 0.45, ease: "back.out(2)" }, C.fum1 - 0.05);
      out("#tag-asl", T.chain - 0.3);
      out("#ban-2", T.chain - 0.2);
      tl.fromTo("#ua3", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.chain - 0.6);
      tl.to("#n-orn", { opacity: 1, duration: 0.3 }, T.chain - 0.6);

      // chain: fumarate rides the top chain into the Krebs wheel
      tl.to("#chain", { opacity: 1, duration: 0.3 }, C.chain - 0.2);
      tl.fromTo("#chain-top", { opacity: 0, strokeDasharray: 560, strokeDashoffset: 560 }, { opacity: 1, strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }, C.chain - 0.1);
      tl.to("#tok-fum", { x: 220, y: 498, duration: 0.35, ease: "power2.inOut" }, C.chain);
      tl.to("#tok-fum", { x: 700, y: 498, duration: Math.max(0.4, C.krebs2 - 0.15 - (C.chain + 0.4)), ease: "power1.inOut" }, C.chain + 0.4);
      tl.to("#tok-fum", { x: 730, y: 553, scale: 0.6, opacity: 0, duration: 0.3, ease: "power2.in" }, C.krebs2 - 0.1);
      pop("#n-fum", C.krebs2 + 0.1);
      pop("#ban-3", C.chain + 0.2);
      tl.fromTo("#ka1", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.malate - 0.3);
      pop("#n-mal", C.malate);
      tl.fromTo("#ka2", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.oaa - 0.3);
      pop("#n-oaa", C.oaa);
      out("#ban-3", T.back - 0.2);

      // back: OAA -> aspartate along the bottom chain to citrulline
      pop("#ban-4", T.back + 0.05);
      pop("#tag-ast", C.transam - 0.1, 0.3);
      tl.fromTo("#chain-bot", { opacity: 0, strokeDasharray: 560, strokeDashoffset: 560 }, { opacity: 1, strokeDashoffset: 0, duration: 0.8, ease: "power2.inOut" }, C.asp2 - 0.4);
      tl.fromTo("#tok-asp", { opacity: 0, x: 730, y: 978, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, C.asp2 - 0.1);
      tl.to("#tok-asp", { x: 200, y: 978, duration: 1.1, ease: "power1.inOut" }, C.asp2 + 0.3);
      tl.to("#tok-asp", { opacity: 0, scale: 0.6, duration: 0.25 }, C.urea3 + 0.2);
      tl.fromTo("#ua4", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.urea3);
      tl.fromTo("#ka3, #ka4", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.urea3);
      out("#tag-ast", T.name - 0.2);
      out("#ban-4", T.name - 0.2);
      // both wheels start rolling
      tl.fromTo("#uw-tread", { rotation: 0, svgOrigin: "270 770" }, { rotation: 360, svgOrigin: "270 770", duration: T.question - C.urea3, ease: "none" }, C.urea3);
      tl.fromTo("#kw-tread", { rotation: 0, svgOrigin: "810 770" }, { rotation: 360, svgOrigin: "810 770", duration: T.question - C.urea3, ease: "none" }, C.urea3);
      tl.fromTo("#chain", { strokeDashoffset: 0 }, { strokeDashoffset: -340, duration: T.question - C.urea3, ease: "none" }, C.urea3);

      // name: it's a bicycle!
      tl.fromTo("#frame", { opacity: 0 }, { opacity: 1, duration: 0.4 }, C.kbicycle - 0.3);
      tl.fromTo("#name-title", { opacity: 0, y: 40, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(2)" }, C.kbicycle);
      tl.fromTo("#sticky", { opacity: 0, rotation: 10, scale: 0.6 }, { opacity: 1, rotation: 4, scale: 1, duration: 0.45, ease: "back.out(2)" }, C.fum3 - 0.5);
      tl.to("#n-fum", { scale: 1.25, transformOrigin: "50% 50%", duration: 0.25, yoyo: true, repeat: 3, ease: "power1.inOut" }, C.fum3);

      // question
      tl.fromTo("#q-card", { opacity: 0, y: 160, rotation: 3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }, T.question);
      tl.fromTo("#q-tag", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, C.neet);
      gsap.utils.toArray(".opt").forEach((o, i) => tl.fromTo(o, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, C.enzyme - 0.2 + i * 0.12));

      // cta
      tl.fromTo("#cta-logo", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, T.cta);
      tl.fromTo("#comment-bubble", { opacity: 0, scale: 0.4, transformOrigin: "20% 100%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, C.comment);
      tl.fromTo("#cta-answer", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, C.agli - 0.2);
      tl.fromTo("#follow-btn", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, C.follow - 0.15);
      tl.fromTo("#tap", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1.4, duration: 0.45, ease: "power2.out" }, C.follow + 0.2);
      tl.to("#tap", { opacity: 0, duration: 0.25 }, C.follow + 0.65);
      tl.to("#follow-btn", { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1 }, C.follow + 0.3);
      tl.fromTo("#follow-btn", { backgroundColor: "#432f2e" }, { backgroundColor: "#e8743b", duration: 0.2, immediateRender: false }, C.follow + 0.4);

      // pixy: bounce in at each expression change, gentle bob while talking
      gsap.utils.toArray(".pixy").forEach((p) => {
        const s = parseFloat(p.getAttribute("data-start")), d = parseFloat(p.getAttribute("data-duration"));
        const img = p.querySelector("img");
        tl.fromTo(img, { y: 30, scale: 0.92, transformOrigin: "50% 100%" }, { y: 0, scale: 1, duration: 0.3, ease: "back.out(2.5)" }, s);
        const bobs = Math.max(1, Math.floor((d - 0.4) / 0.9));
        tl.to(img, { y: -10, duration: 0.45, yoyo: true, repeat: bobs * 2 - 1, ease: "sine.inOut" }, s + 0.35);
      });

      // captions pop
      gsap.utils.toArray(".capt").forEach((c) => {
        const s = parseFloat(c.parentElement.getAttribute("data-start"));
        tl.fromTo(c, { scale: 0.85, y: 10 }, { scale: 1, y: 0, duration: 0.18, ease: "back.out(3)" }, s);
      });

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
