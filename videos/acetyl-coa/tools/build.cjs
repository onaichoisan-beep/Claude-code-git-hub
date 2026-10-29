// Reel #2 "Teeno ka common dost" (NEET 2013, Acetyl CoA): PYQ hook -> lock answer -> elimination -> reveal -> new question.
// Brand rule: the channel name appears ONLY in the final follow frame.
const fs = require('fs');
const path = require('path');
const { hood, MOUTH_SVG } = require('./dragon_pixy.cjs');
const ROOT = path.join(__dirname, '..');
const WORDS = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/audio/transcript.json')));
const END = 50.8;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
const cue = (w, after = 0) => {
  const hit = WORDS.find((x) => x.start >= after && norm(x.text).startsWith(w));
  if (!hit) throw new Error('cue not found: ' + w);
  return +hit.start.toFixed(2);
};
const C = {
  q: cue('question'), yr: cue('2013'), fats: cue('fats'), what: cue('what'), three: cue('three'),
  lock: cue('lock'), c3: cue('3', 10), c2: cue('2', 11), c1: cue('1', 12),
  optB: cue('option'), glucose: cue('glucose'), fructose: cue('fructose'), glyco: cue('glycolysis'), fatsDont: cue('fats', 20), out: cue('out', 22),
  now: cue('now', 23), pyru: cue('pyruvic'), fatty: cue('fatty'), make: cue('make'), beta: cue('betaoxidation'), something: cue('something'),
  correct: cue('correct'), acetyl: cue('acetylcoa', 32), carbs: cue('carbs', 33), fats2: cue('fats', 33.6), prot: cue('proteins', 34),
  friend: cue('friend'), krebs: cue('krebs', 37), last: cue('last'), b: cue('b', 40), arg: cue('arginino'),
  tell: cue('tell'), co2: cue('co2s'), krebs2: cue('krebs', 46), next: cue('next', 47), follow: cue('follow'), scroll: cue('scroll'),
};
const T = { hook: 0, lock: C.lock - 0.2, elim: C.optB - 0.25, ad: C.now - 0.2, reveal: C.correct - 0.2, prev: C.last - 0.4, newq: C.tell - 0.3, end: C.follow - 0.25 };

// ---- lip-sync from loudness (15 fps) ----
const lips = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/audio/lips.json')));

// ---- Pixy expression timeline (head layers without mouths; mouths drawn on top) ----
const EXPR_T = [[0, 'shock'], [1.2, 'watching'], [T.lock, 'sly'], [T.elim, 'confusion'], [C.out, 'angry'], [C.out + 0.8, 'watching'],
  [C.make, 'gusto'], [C.correct, 'watching'], [C.acetyl, 'joy'], [C.friend, 'friendly'], [C.b, 'joy'], [C.tell, 'confusion'], [C.follow, 'joy']];
const LAYERS = [...new Set(EXPR_T.map((e) => e[1]))];
const heads = LAYERS.map((e) => `<g id="hd-${e}" class="hd" ${e === 'shock' ? '' : 'opacity="0"'}>${hood(e, 'none')}</g>`).join('');
const MOUTHS = ['closed', 'smile', 'mid', 'open', 'oh'];
const mouths = MOUTHS.map((m) => `<g id="mo-${m}" class="mo" ${m === 'oh' ? '' : 'opacity="0"'}>${MOUTH_SVG[m]}</g>`).join('');

// ---- pop-up reactions ----
const FX = {
  bang: '<circle cx="85" cy="85" r="70" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><text x="85" y="124" text-anchor="middle" font-family="Bagel Fat One" font-size="108" fill="#432f2e">!</text>',
  q: '<circle cx="85" cy="85" r="70" fill="#432f2e"/><text x="85" y="122" text-anchor="middle" font-family="Bagel Fat One" font-size="100" fill="#feefb8">?</text>',
  spark: '<path d="M85 5 L 102 68 L 165 85 L 102 102 L 85 165 L 68 102 L 5 85 L 68 68 Z" fill="#F6D365" stroke="#432f2e" stroke-width="7" stroke-linejoin="round"/>',
  heart: '<path d="M85 150 C 20 105 10 70 30 45 C 50 22 78 30 85 52 C 92 30 120 22 140 45 C 160 70 150 105 85 150 Z" fill="#e8743b" stroke="#432f2e" stroke-width="8" stroke-linejoin="round"/>',
  lock: '<rect x="35" y="75" width="100" height="80" rx="14" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><path d="M 55 75 V 55 Q 55 25 85 25 Q 115 25 115 55 V 75" fill="none" stroke="#432f2e" stroke-width="10"/><circle cx="85" cy="112" r="10" fill="#432f2e"/>',
  no: '<circle cx="85" cy="85" r="70" fill="#fffcf2" stroke="#e8743b" stroke-width="10"/><path d="M 40 130 L 130 40" stroke="#e8743b" stroke-width="12"/>',
  bulb: '<path d="M85 20 C 45 20 30 55 40 80 C 48 100 62 104 62 124 L 108 124 C 108 104 122 100 130 80 C 140 55 125 20 85 20 Z" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><rect x="62" y="128" width="46" height="22" rx="6" fill="#c4dae8" stroke="#432f2e" stroke-width="6"/>',
};
const POPS = [['bang', C.yr, 'R'], ['lock', C.lock, 'R'], ['q', C.optB, 'L'], ['no', C.out, 'R'], ['bulb', C.make, 'R'],
  ['spark', C.acetyl, 'L'], ['spark', C.acetyl + 0.15, 'R'], ['heart', C.b, 'R'], ['q', C.co2, 'R'], ['heart', C.follow, 'L'], ['spark', C.scroll, 'R']];
const fx = POPS.map(([k], i) => `<svg id="fx-${i}" class="fx" viewBox="-10 -10 190 190" width="160" height="160">${FX[k]}</svg>`).join('\n      ');

// ---- molecule buddies (fat / carb / protein / acetyl CoA) ----
const buddy = (id, fill, label, extra = '') => `<g id="${id}" opacity="0"><g class="bob">
  <circle r="58" fill="${fill}" stroke="#432f2e" stroke-width="8"/>${extra}
  <circle cx="-19" cy="-8" r="9" fill="#432f2e"/><circle cx="19" cy="-8" r="9" fill="#432f2e"/><circle cx="-16" cy="-11" r="3" fill="#fff"/><circle cx="22" cy="-11" r="3" fill="#fff"/>
  <path d="M -14 14 Q 0 28 14 14" fill="none" stroke="#432f2e" stroke-width="6" stroke-linecap="round"/>
  <text y="-74" text-anchor="middle" font-family="Bagel Fat One" font-size="38" fill="#432f2e" stroke="#feefb8" stroke-width="8" paint-order="stroke">${label}</text></g></g>`;

const opt = (k, txt, y) => `<g id="opt-${k}" transform="translate(110 ${y})">
  <g class="opt-in"><rect width="860" height="92" rx="46" fill="#feefb8" stroke="#432f2e" stroke-width="6"/>
  <circle cx="50" cy="46" r="32" fill="#432f2e"/><text x="50" y="58" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#feefb8">${k}</text>
  <text x="104" y="60" font-family="Inter" font-weight="800" font-size="38" fill="#432f2e">${txt}</text>
  <g class="x" opacity="0"><path d="M 790 22 L 838 70 M 838 22 L 790 70" stroke="#e8743b" stroke-width="12" stroke-linecap="round"/></g>
  <g class="tick" opacity="0"><path d="M 786 48 L 808 70 L 842 24" fill="none" stroke="#2f9e5b" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>`;

const html = `<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Playfair Display"; font-weight: 900; src: url("assets/fonts/playfair-900.ttf"); }
      @font-face { font-family: "Bagel Fat One"; src: url("assets/fonts/bagel.ttf"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-800.ttf"); }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #feefb8; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; color: #432f2e;
        background: radial-gradient(circle, rgba(159, 192, 214, 0.45) 3px, transparent 4px) 0 0 / 46px 46px, #feefb8; }
      #stage { position: absolute; inset: 0; }
      #world { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
      #face { position: absolute; left: 335px; top: 1135px; width: 410px; height: 421px; overflow: visible; }
      .fx { position: absolute; left: 0; top: 0; opacity: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${END}" data-width="1080" data-height="1920">
      <div id="stage" class="clip" data-start="0" data-duration="${END}" data-track-index="1">
        <svg id="world" viewBox="0 0 1080 1920">
          <!-- hook: NEET 2013 stamp -->
          <g id="stamp" opacity="0" transform="translate(540 205)">
            <g id="stamp-in"><rect x="-300" y="-70" width="600" height="140" rx="22" fill="#e8743b" stroke="#432f2e" stroke-width="8"/>
            <text y="30" text-anchor="middle" font-family="Bagel Fat One" font-size="88" fill="#fffcf2">NEET 2013</text></g>
          </g>
          <!-- question card -->
          <g id="qcard" opacity="0">
            <rect x="70" y="280" width="940" height="270" rx="36" fill="#fffcf2" stroke="#432f2e" stroke-width="9"/>
            <text x="540" y="345" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#432f2e">Fats, Carbs aur Proteins —</text>
            <text x="540" y="408" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="50" fill="#432f2e">teeno ke breakdown mein</text>
            <text x="540" y="470" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="50" fill="#432f2e">COMMON metabolite?</text>
            <g id="trio"><text x="540" y="522" text-anchor="middle" font-size="36">🧈 🍞 🍗</text></g>
          </g>
          ${opt('A', 'Acetyl CoA', 590)}
          ${opt('B', 'Fructose 1,6-bisphosphate', 700)}
          ${opt('C', 'Glucose-6-phosphate', 810)}
          ${opt('D', 'Pyruvic acid', 920)}
          <!-- lock countdown -->
          <g id="count" opacity="0" transform="translate(540 205)"><circle r="70" fill="#432f2e"/><text id="count-t" y="30" text-anchor="middle" font-family="Bagel Fat One" font-size="96" fill="#feefb8"> </text></g>

          <!-- elimination scene: glycolysis road -->
          <g id="road" opacity="0">
            <text x="540" y="320" text-anchor="middle" font-family="Bagel Fat One" font-size="56" fill="#432f2e">Glycolysis Road 🚧</text>
            <path d="M 80 560 C 300 470 760 650 1000 560" fill="none" stroke="#c4dae8" stroke-width="90" stroke-linecap="round"/>
            <path d="M 80 560 C 300 470 760 650 1000 560" fill="none" stroke="#fffcf2" stroke-width="8" stroke-dasharray="30 24"/>
            <g transform="translate(360 470)"><rect x="-150" y="-110" width="300" height="70" rx="16" fill="#feefb8" stroke="#432f2e" stroke-width="6"/><text y="-63" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" fill="#432f2e">Glucose-6-P</text><line y1="-40" y2="40" stroke="#432f2e" stroke-width="8"/></g>
            <g transform="translate(720 520)"><rect x="-160" y="-110" width="320" height="70" rx="16" fill="#feefb8" stroke="#432f2e" stroke-width="6"/><text y="-63" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" fill="#432f2e">Fructose 1,6-BP</text><line y1="-40" y2="40" stroke="#432f2e" stroke-width="8"/></g>
            <g id="gate" opacity="0" transform="translate(200 700)"><rect x="-130" y="-40" width="260" height="80" rx="14" fill="#e8743b" stroke="#432f2e" stroke-width="6"/><text y="16" text-anchor="middle" font-family="Bagel Fat One" font-size="44" fill="#fffcf2">FATS ✋</text></g>
          </g>
          <g id="glu-wrap" transform="translate(110 560)">${buddy('glu', '#fffcf2', 'Glucose')}</g>
          <g id="fat-wrap" transform="translate(-120 760)">${buddy('fat', '#F6D365', 'Fat')}</g>

          <!-- A or D scene: beta-oxidation -->
          <g id="ad" opacity="0">
            <text x="540" y="320" text-anchor="middle" font-family="Bagel Fat One" font-size="56" fill="#432f2e">A ya D? 🤔</text>
            <g transform="translate(300 600)"><rect x="-150" y="-170" width="300" height="300" rx="30" fill="#c4dae8" stroke="#432f2e" stroke-width="8"/>
              <text y="-100" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#432f2e">PYRUVATE</text>
              <text y="-60" text-anchor="middle" font-family="Inter" font-weight="800" font-size="28" fill="#432f2e">door 🚪</text>
              <g id="no-entry" opacity="0"><circle cy="30" r="70" fill="none" stroke="#e8743b" stroke-width="14"/><line x1="-50" y1="80" x2="50" y2="-20" stroke="#e8743b" stroke-width="14"/></g></g>
            <g id="beta" opacity="0" transform="translate(760 820)"><rect x="-210" y="-48" width="420" height="96" rx="48" fill="#432f2e"/><text y="16" text-anchor="middle" font-family="Bagel Fat One" font-size="48" fill="#feefb8">β-oxidation ➜</text></g>
            <g id="mystery" opacity="0" transform="translate(800 520)"><circle r="90" fill="#fffcf2" stroke="#432f2e" stroke-width="8" stroke-dasharray="16 10"/><text y="40" text-anchor="middle" font-family="Bagel Fat One" font-size="120" fill="#432f2e">?</text></g>
          </g>

          <!-- reveal: three roads merge into Acetyl CoA -->
          <g id="reveal" opacity="0">
            <path id="r1" d="M 120 300 C 300 330 420 470 540 600" fill="none" stroke="#fffcf2" stroke-width="40" stroke-linecap="round"/>
            <path id="r2" d="M 540 260 L 540 600" fill="none" stroke="#fffcf2" stroke-width="40" stroke-linecap="round"/>
            <path id="r3" d="M 960 300 C 780 330 660 470 540 600" fill="none" stroke="#fffcf2" stroke-width="40" stroke-linecap="round"/>
            <path d="M 540 600 L 540 900" fill="none" stroke="#e8743b" stroke-width="40" stroke-linecap="round"/>
            <g id="krebs" opacity="0" transform="translate(540 960)"><circle r="110" fill="#fffcf2" stroke="#e8743b" stroke-width="24"/>
              <g id="krebs-spokes">${[0, 45, 90, 135].map((a) => `<line x1="${-95 * Math.cos(a * Math.PI / 180)}" y1="${-95 * Math.sin(a * Math.PI / 180)}" x2="${95 * Math.cos(a * Math.PI / 180)}" y2="${95 * Math.sin(a * Math.PI / 180)}" stroke="#432f2e" stroke-width="4" opacity="0.5"/>`).join('')}</g>
              <text y="14" text-anchor="middle" font-family="Bagel Fat One" font-size="40" fill="#432f2e">KREBS</text></g>
          </g>
          <g id="carb-wrap" transform="translate(120 300)">${buddy('carb', '#fffcf2', 'Carbs')}</g>
          <g id="fat2-wrap" transform="translate(540 250)">${buddy('fat2', '#F6D365', 'Fats')}</g>
          <g id="prot-wrap" transform="translate(960 300)">${buddy('prot', '#c4dae8', 'Proteins')}</g>
          <g id="acoa-wrap" transform="translate(540 640)">${buddy('acoa', '#e8743b', 'Acetyl CoA', '<circle r="76" fill="none" stroke="#F6D365" stroke-width="8" stroke-dasharray="10 12"/>')}</g>

          <!-- previous reel answer -->
          <g id="prev" opacity="0" transform="translate(540 620)"><rect x="-460" y="-70" width="920" height="140" rx="30" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/>
            <text y="-12" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#432f2e">Pichli reel ka answer ✅</text>
            <text y="40" text-anchor="middle" font-family="Bagel Fat One" font-size="44" fill="#b2461a">B — Argininosuccinate lyase</text></g>

          <!-- new question -->
          <g id="newq" opacity="0">
            <rect x="70" y="300" width="940" height="250" rx="36" fill="#432f2e"/>
            <text x="540" y="380" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#feefb8">AGLA SAWAAL 👀</text>
            <text x="540" y="452" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="54" fill="#feefb8">1 Acetyl CoA ➜ Krebs cycle</text>
            <text x="540" y="515" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="54" fill="#F6D365">kitne CO₂ niklenge?</text>
            ${['1', '2', '3', '4'].map((v, i) => `<g class="nq" opacity="0" transform="translate(${190 + i * 233} 680)"><circle r="82" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/><text y="-12" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#432f2e">${'ABCD'[i]}</text><text y="46" text-anchor="middle" font-family="Bagel Fat One" font-size="64" fill="#432f2e">${v}</text></g>`).join('')}
            <text id="nq-hint" opacity="0" x="540" y="880" text-anchor="middle" font-family="Bagel Fat One" font-size="58" fill="#b2461a">Answer → agli reel mein!</text>
          </g>

          <!-- final frame ONLY: brand -->
          <g id="brand" opacity="0">
            <g transform="rotate(-12 540 520)">
              <text x="120" y="560" font-family="Playfair Display" font-weight="900" font-size="104" fill="#432f2e">SCROLL</text>
              <text x="540" y="590" font-family="Playfair Display" font-weight="900" font-size="250" fill="#c4dae8" stroke="#432f2e" stroke-width="6" paint-order="stroke">2</text>
              <text x="690" y="495" font-family="Playfair Display" font-weight="900" font-size="104" fill="#432f2e">SCORE</text>
            </g>
            <g id="follow" transform="translate(540 900)"><rect x="-250" y="-62" width="500" height="124" rx="62" fill="#432f2e"/><text y="22" text-anchor="middle" font-family="Bagel Fat One" font-size="64" fill="#feefb8">FOLLOW</text></g>
          </g>
        </svg>
        <svg id="face" viewBox="110 40 380 390"><g id="face-root">${heads}${mouths}</g></svg>
        ${fx}
      </div>
      <audio id="vo" class="clip" src="assets/audio/vo.mp3" data-start="0" data-duration="${END}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const C = ${JSON.stringify(C)};
      const T = ${JSON.stringify(T)};
      const LIPS = ${JSON.stringify(lips)};
      const EXPR_T = ${JSON.stringify(EXPR_T)};
      const POPS = ${JSON.stringify(POPS)};
      const END = ${END};
      const tl = gsap.timeline({ paused: true });
      const show = (sel, t, d = 0.35) => tl.fromTo(sel, { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2.4)", immediateRender: false }, t);
      const fade = (sel, t, v = 1, d = 0.25) => tl.to(sel, { opacity: v, duration: d }, t);
      const optIn = (k, t) => tl.fromTo("#opt-" + k + " .opt-in", { x: -1200 }, { x: 0, duration: 0.35, ease: "back.out(1.5)" }, t);

      // ---------- Pixy: pop in, idle sway/bob, expressions, lip-sync, reactions ----------
      gsap.set("#face-root", { svgOrigin: "300 400" });
      tl.fromTo("#face", { y: 900, rotation: -14 }, { y: 0, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }, 0);
      tl.fromTo("#face-root", { rotation: -4 }, { rotation: 4, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor((END - 0.6) / 1.1) - 1) }, 0.6);
      let prevE = "shock";
      EXPR_T.slice(1).forEach(([t, e]) => {
        if (e === prevE) return;
        tl.set("#hd-" + prevE, { opacity: 0 }, t); tl.set("#hd-" + e, { opacity: 1 }, t); prevE = e;
        tl.fromTo("#face-root", { scaleY: 0.92, scaleX: 1.06 }, { scaleY: 1, scaleX: 1, duration: 0.4, ease: "elastic.out(1.2, 0.45)", immediateRender: false }, t);
      });
      let prevM = "oh";
      LIPS.forEach(([t, m]) => {
        const exp = EXPR_T.filter((e) => e[0] <= t).pop()[1];
        let mm = m === "ee" ? "open" : m;
        if (mm === "closed") mm = ["joy", "friendly", "sly", "gusto"].includes(exp) ? "smile" : "closed";
        if ((exp === "shock" || exp === "confusion") && mm === "open") mm = "oh";
        if (mm === prevM) return;
        tl.set("#mo-" + prevM, { opacity: 0 }, t); tl.set("#mo-" + mm, { opacity: 1 }, t); prevM = mm;
      });
      const jolt = (t) => { tl.to("#face", { y: -50, duration: 0.12, ease: "power2.out" }, t); tl.to("#face", { y: 0, duration: 0.45, ease: "bounce.out" }, t + 0.12); };
      [C.yr, C.out, C.acetyl, C.b, C.follow].forEach(jolt);
      tl.to("#face", { x: -18, duration: 0.07, yoyo: true, repeat: 5, ease: "none" }, C.out + 0.2);
      POPS.forEach(([k, t, side], i) => {
        const x = side === "R" ? 720 : 200, y = 1120;
        tl.fromTo("#fx-" + i, { opacity: 0, x, y, scale: 0.2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t);
        tl.to("#fx-" + i, { y: y - 50, duration: 0.6, ease: "sine.out" }, t + 0.3);
        tl.to("#fx-" + i, { opacity: 0, scale: 0.5, duration: 0.2 }, t + 1.1);
      });
      tl.to(".bob", { y: -10, duration: 0.35, yoyo: true, repeat: Math.floor(END / 0.35) - 1, ease: "sine.inOut" }, 0);

      // ---------- 1. hook: NEET 2013 + MCQ ----------
      tl.set("#stamp", { opacity: 1 }, C.yr - 0.2);
      tl.fromTo("#stamp-in", { scale: 3, rotation: -18, transformOrigin: "50% 50%" }, { scale: 1, rotation: -4, duration: 0.3, ease: "power4.in" }, C.yr - 0.2);
      tl.fromTo("#stage", { x: 0 }, { x: 14, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.yr + 0.1);
      show("#qcard", C.fats - 0.1, 0.4);
      ["A", "B", "C", "D"].forEach((k, i) => optIn(k, C.what + i * 0.12));

      // ---------- 2. lock your answer ----------
      tl.to("#stamp", { opacity: 0, duration: 0.2 }, T.lock);
      show("#count", C.c3 - 0.1);
      [["3", C.c3], ["2", C.c2], ["1", C.c1]].forEach(([n, t]) => {
        tl.set("#count-t", { textContent: n }, t);
        tl.fromTo("#count", { scale: 1.5 }, { scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, t);
      });
      fade("#count", C.c1 + 0.7, 0);

      // ---------- 3. eliminate B & C on the glycolysis road ----------
      tl.to("#opt-B .opt-in, #opt-C .opt-in", { scale: 1.05, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, C.optB + 0.6);
      fade("#qcard, #opt-A, #opt-B, #opt-C, #opt-D", C.glucose - 0.1, 0, 0.25);
      fade("#road", C.glucose, 1, 0.3);
      fade("#glu", C.glucose + 0.1, 1, 0.2);
      tl.to("#glu-wrap", { x: 980, duration: Math.max(1.2, C.fatsDont - C.glucose - 0.6), ease: "power1.inOut" }, C.glucose + 0.3);
      fade("#fat", C.fatsDont - 0.3, 1, 0.2);
      tl.to("#fat-wrap", { x: 120, duration: 0.5, ease: "power2.out" }, C.fatsDont - 0.3);
      show("#gate", C.fatsDont + 0.3);
      tl.to("#fat-wrap", { x: 60, duration: 0.15, yoyo: true, repeat: 1 }, C.fatsDont + 0.6);
      fade("#road, #glu, #fat", C.out - 0.3, 0, 0.2);
      fade("#qcard, #opt-A, #opt-B, #opt-C, #opt-D", C.out - 0.3, 1, 0.2);
      tl.set("#opt-B .x, #opt-C .x", { opacity: 1 }, C.out);
      tl.to("#opt-B .opt-in", { x: 1100, rotation: 12, opacity: 0, duration: 0.45, ease: "power2.in" }, C.out + 0.3);
      tl.to("#opt-C .opt-in", { x: -1100, rotation: -12, opacity: 0, duration: 0.45, ease: "power2.in" }, C.out + 0.4);

      // ---------- 4. A or D? fats skip the pyruvate door ----------
      fade("#qcard, #opt-A, #opt-D", T.ad, 0, 0.25);
      fade("#ad", T.ad + 0.1, 1, 0.3);
      fade("#fat", C.fatty - 0.2, 1, 0.01);
      tl.fromTo("#fat-wrap", { x: -120, y: 0 }, { x: 160, y: -170, duration: 0.6, ease: "power2.out", immediateRender: false }, C.fatty - 0.2);
      show("#no-entry", C.make);
      tl.to("#fat-wrap", { x: 640, y: -150, duration: 0.7, ease: "power1.inOut" }, C.make + 0.3);
      show("#beta", C.beta - 0.1);
      show("#mystery", C.something);
      tl.to("#mystery", { rotation: 360, duration: 0.6, ease: "power2.inOut" }, C.something + 0.3);

      // ---------- 5. reveal: Acetyl CoA, all three roads merge ----------
      fade("#ad, #fat", T.reveal, 0, 0.25);
      fade("#qcard, #opt-A, #opt-D", T.reveal + 0.1, 1, 0.25);
      tl.to("#opt-A .opt-in, #opt-D .opt-in", { scale: 1.04, duration: 0.1, yoyo: true, repeat: 5, transformOrigin: "50% 50%" }, C.correct + 0.2);
      tl.set("#opt-D .x", { opacity: 1 }, C.acetyl);
      tl.to("#opt-D .opt-in", { opacity: 0.25, duration: 0.2 }, C.acetyl);
      tl.set("#opt-A .tick", { opacity: 1 }, C.acetyl);
      tl.to("#opt-A rect", { attr: { fill: "#bfe8c8" }, duration: 0.2 }, C.acetyl);
      tl.fromTo("#opt-A .opt-in", { scale: 1 }, { scale: 1.12, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 50%", immediateRender: false }, C.acetyl);
      fade("#qcard, #opt-A, #opt-D", C.carbs - 0.25, 0, 0.2);
      fade("#reveal", C.carbs - 0.2, 1, 0.2);
      [["#carb", C.carbs], ["#fat2", C.fats2], ["#prot", C.prot]].forEach(([s, t]) => show(s, t, 0.3));
      show("#acoa", C.prot + 0.3);
      tl.to("#carb-wrap", { x: 470, y: 600, scale: 0.4, duration: 0.6, ease: "power2.in" }, C.friend);
      tl.to("#fat2-wrap", { y: 590, scale: 0.4, duration: 0.6, ease: "power2.in" }, C.friend + 0.1);
      tl.to("#prot-wrap", { x: 610, y: 600, scale: 0.4, duration: 0.6, ease: "power2.in" }, C.friend + 0.2);
      fade("#carb, #fat2, #prot", C.friend + 0.7, 0, 0.15);
      tl.fromTo("#acoa", { scale: 1 }, { scale: 1.25, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "50% 50%", immediateRender: false }, C.friend + 0.8);
      show("#krebs", C.krebs - 0.4);
      tl.to("#acoa-wrap", { y: 900, scale: 0.5, duration: 0.5, ease: "power2.in" }, C.krebs);
      tl.fromTo("#krebs-spokes", { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, svgOrigin: "0 0", duration: 1.0, ease: "power2.out", immediateRender: false }, C.krebs + 0.4);
      fade("#acoa", C.krebs + 0.45, 0, 0.1);

      // ---------- 6. previous reel answer ----------
      fade("#reveal", T.prev, 0, 0.3);
      show("#prev", C.b - 0.3);
      fade("#prev", T.newq, 0, 0.25);

      // ---------- 7. new question ----------
      tl.fromTo("#newq", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, T.newq + 0.1);
      gsap.utils.toArray(".nq").forEach((n, i) => tl.fromTo(n, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.6)", immediateRender: false }, C.co2 + i * 0.12));
      show("#nq-hint", C.next - 0.3);

      // ---------- 8. final frame: brand + follow (only place the name appears) ----------
      fade("#newq", T.end, 0, 0.2);
      tl.set("#brand", { opacity: 1 }, T.end + 0.15);
      tl.fromTo("#brand > g:first-child", { scale: 0.5, opacity: 0, transformOrigin: "540px 520px" }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }, T.end + 0.15);
      show("#follow", C.follow + 0.1);
      tl.to("#follow", { scale: 0.9, duration: 0.1, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, C.scroll);
      tl.to("#follow rect", { attr: { fill: "#e8743b" }, duration: 0.15 }, C.scroll + 0.1);

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>`;
fs.writeFileSync(path.join(ROOT, 'index.html'), html);
console.log('index.html written', JSON.stringify(C));
