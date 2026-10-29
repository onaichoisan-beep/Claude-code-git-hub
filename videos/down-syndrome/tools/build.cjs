// Reel #3 "Down's syndrome" (NEET 2013, Q1926): PYQ hook -> elimination -> reveal (karyotype) -> new question.
// Short format: no lock countdown, no previous-answer segment (that goes in a pinned comment). SFX on every beat.
// Brand rule: the channel name appears ONLY in the final follow frame.
const fs = require('fs');
const path = require('path');
const { hood, MOUTH_SVG } = require('./dragon_pixy.cjs');
const ROOT = path.join(__dirname, '..');
const WORDS = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/audio/transcript.json')));
const VO_END = WORDS[WORDS.length - 1].end;
const END = +(VO_END + 1.4).toFixed(2);

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
const cue = (w, after = 0) => {
  const hit = WORDS.find((x) => x.start >= after && norm(x.text).startsWith(w));
  if (!hit) throw new Error('cue not found: ' + w + ' after ' + after);
  return +hit.start.toFixed(2);
};
const CUES = require('./cues.cjs')(cue);
const C = CUES;
const T = { elim: C.doY - 0.25, reveal: C.sahi - 0.2, nd: C.reason - 0.25, newq: C.ab - 0.3, end: C.follow - 0.25 };

// ---- lip-sync from loudness (15 fps) ----
const lips = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/audio/lips.json')));

// ---- Pixy expression timeline (head layers without mouths; mouths drawn on top) ----
const EXPR_T = [[0, 'shock'], [C.syndrome, 'watching'], [T.elim, 'confusion'], [C.out1, 'angry'], [C.out1 + 0.7, 'sly'],
  [C.out2, 'angry'], [C.out2 + 0.7, 'watching'], [C.out3, 'angry'], [C.out3 + 0.7, 'watching'], [C.sahi, 'joy'],
  [C.reason, 'gusto'], [C.ab, 'friendly'], [C.kary, 'confusion'], [C.follow, 'joy']];
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
  no: '<circle cx="85" cy="85" r="70" fill="#fffcf2" stroke="#e8743b" stroke-width="10"/><path d="M 40 130 L 130 40" stroke="#e8743b" stroke-width="12"/>',
  bulb: '<path d="M85 20 C 45 20 30 55 40 80 C 48 100 62 104 62 124 L 108 124 C 108 104 122 100 130 80 C 140 55 125 20 85 20 Z" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><rect x="62" y="128" width="46" height="22" rx="6" fill="#c4dae8" stroke="#432f2e" stroke-width="6"/>',
};
const POPS = [['bang', C.yr, 'R'], ['q', C.syndrome + 0.3, 'L'], ['no', C.out1, 'R'], ['no', C.out2, 'L'], ['no', C.out3, 'R'],
  ['spark', C.sahi + 0.3, 'L'], ['spark', C.sahi + 0.45, 'R'], ['bulb', C.reason, 'R'], ['q', C.kary, 'R'], ['heart', C.follow, 'L']];
const fx = POPS.map(([k], i) => `<svg id="fx-${i}" class="fx" viewBox="-10 -10 190 190" width="160" height="160">${FX[k]}</svg>`).join('\n      ');

// ---- SFX (bundled HyperFrames library, mixed under the voice) ----
const SFX = [['whoosh', 0.05, 0.35], ['impact-bass-1', C.yr - 0.05, 0.4], ['whoosh-short', C.opts - 0.05, 0.3],
  ['pop', C.doY, 0.3], ['error', C.out1, 0.28], ['pop', C.teen, 0.3], ['error', C.out2, 0.28], ['pop', C.mono, 0.3], ['error', C.out3, 0.28],
  ['ping', C.sahi, 0.35], ['sparkle', C.sahi + 0.3, 0.35], ['whoosh-short', C.trisomy - 0.2, 0.3], ['chime', C.forty - 0.05, 0.25],
  ['whoosh', T.nd, 0.3], ['click', C.alag, 0.3], ['whoosh', T.newq, 0.3], ['pop', C.kary + 0.1, 0.25], ['click', C.comment, 0.3],
  ['impact-bass-1', T.end + 0.15, 0.35], ['sparkle', C.follow + 0.1, 0.3]];
const DUR = { whoosh: 0.57, 'whoosh-short': 0.57, pop: 0.72, 'impact-bass-1': 2.12, error: 1.62, sparkle: 1.8, chime: 2.5, ping: 1.32, click: 0.37 };
const sfx = SFX.map(([n, t, v], i) => `<audio id="sfx-${i}" class="clip" src="assets/sfx/${n}.mp3" data-start="${Math.max(0, t).toFixed(2)}" data-duration="${Math.min(DUR[n], END - t).toFixed(2)}" data-track-index="${11 + i}" data-volume="${v}"></audio>`).join('\n      ');

// ---- chromosome buddy: an X with eyes; Y is a short stubby one ----
const chrom = (x, y, fill, label, kind = 'X', s = 1) => {
  const arm = kind === 'Y' ? 'M -14 -55 Q -6 0 -14 34' : 'M -26 -70 Q 0 0 -26 70';
  const arm2 = kind === 'Y' ? 'M 14 -55 Q 6 0 14 34' : 'M 26 -70 Q 0 0 26 70';
  return `<g transform="translate(${x} ${y}) scale(${s})"><g class="bob">
    <path d="${arm}" fill="none" stroke="#432f2e" stroke-width="44" stroke-linecap="round"/><path d="${arm}" fill="none" stroke="${fill}" stroke-width="30" stroke-linecap="round"/>
    <path d="${arm2}" fill="none" stroke="#432f2e" stroke-width="44" stroke-linecap="round"/><path d="${arm2}" fill="none" stroke="${fill}" stroke-width="30" stroke-linecap="round"/>
    <circle cx="-8" cy="${kind === 'Y' ? -14 : -6}" r="5" fill="#432f2e"/><circle cx="8" cy="${kind === 'Y' ? -14 : -6}" r="5" fill="#432f2e"/>
    <text y="${kind === 'Y' ? 96 : 122}" text-anchor="middle" font-family="Bagel Fat One" font-size="44" fill="#432f2e">${label}</text></g></g>`;
};
const XC = '#c4dae8', YC = '#e8743b', AC = '#F6D365';

const opt = (k, txt, y) => `<g id="opt-${k}" transform="translate(110 ${y})">
  <g class="opt-in"><rect width="860" height="92" rx="46" fill="#feefb8" stroke="#432f2e" stroke-width="6"/>
  <circle cx="50" cy="46" r="32" fill="#432f2e"/><text x="50" y="58" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#feefb8">${k}</text>
  <text x="104" y="60" font-family="Inter" font-weight="800" font-size="38" fill="#432f2e">${txt}</text>
  <g class="x" opacity="0"><path d="M 790 22 L 838 70 M 838 22 L 790 70" stroke="#e8743b" stroke-width="12" stroke-linecap="round"/></g>
  <g class="tick" opacity="0"><path d="M 786 48 L 808 70 L 842 24" fill="none" stroke="#2f9e5b" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>`;

// panel = the top card area (x 70–1010, y 280–550) reused for each elimination mini-scene
const panel = (id, title, body, sub) => `<g id="${id}" opacity="0">
  <rect x="70" y="280" width="940" height="270" rx="36" fill="#fffcf2" stroke="#432f2e" stroke-width="9"/>
  ${body}
  <text x="760" y="390" text-anchor="middle" font-family="Bagel Fat One" font-size="62" fill="#432f2e">${title}</text>
  <text x="760" y="460" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#b2461a">${sub}</text></g>`;

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
          <g id="stamp" opacity="0" transform="translate(540 190)">
            <g id="stamp-in"><rect x="-300" y="-66" width="600" height="132" rx="22" fill="#e8743b" stroke="#432f2e" stroke-width="8"/>
            <text y="30" text-anchor="middle" font-family="Bagel Fat One" font-size="84" fill="#fffcf2">NEET 2013</text></g>
          </g>
          <!-- question card -->
          <g id="qcard" opacity="0">
            <rect x="70" y="280" width="940" height="270" rx="36" fill="#fffcf2" stroke="#432f2e" stroke-width="9"/>
            <text x="540" y="350" text-anchor="middle" font-family="Inter" font-weight="800" font-size="36" fill="#432f2e">Humans mein</text>
            <text x="540" y="430" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="66" fill="#432f2e">Down's syndrome</text>
            <text x="540" y="505" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="50" fill="#b2461a">kis wajah se hota hai?</text>
          </g>
          ${panel('pB', 'XYY', chrom(170, 400, XC, 'X') + chrom(290, 400, YC, 'Y', 'Y') + chrom(400, 400, YC, 'Y', 'Y'), 'alag condition')}
          ${panel('pD', 'XXX', chrom(170, 400, XC, 'X') + chrom(290, 400, XC, 'X') + chrom(410, 400, XC, 'X'), 'triple X female')}
          ${panel('pC', '45, XO', chrom(200, 400, XC, 'X') + `<g transform="translate(360 400)"><circle r="62" fill="none" stroke="#432f2e" stroke-width="7" stroke-dasharray="14 12"/><text y="22" text-anchor="middle" font-family="Bagel Fat One" font-size="64" fill="#432f2e">?</text></g>`, 'Monosomy = 1 kam')}
          ${opt('A', 'Three copies of chromosome 21', 590)}
          ${opt('B', "Two 'Y' chromosomes", 700)}
          ${opt('C', 'Monosomy', 810)}
          ${opt('D', "Three 'X' chromosomes", 920)}

          <!-- reveal: real karyotype (public domain, US DOE Human Genome Program via Wikimedia Commons) -->
          <g id="kcard" opacity="0">
            <rect x="70" y="250" width="940" height="640" rx="36" fill="#fffcf2" stroke="#432f2e" stroke-width="9"/>
            <image href="assets/img/karyotype.png" x="105" y="285" width="870" height="538" preserveAspectRatio="xMidYMid meet"/>
            <g id="k21"><rect x="481" y="747" width="104" height="47" rx="10" fill="none" stroke="#e8743b" stroke-width="10"/></g>
            <text x="540" y="868" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="#432f2e" opacity="0.6">Real karyotype · Trisomy 21</text>
          </g>
          <g id="tri" opacity="0" transform="translate(540 990)"><rect x="-330" y="-56" width="660" height="112" rx="56" fill="#432f2e"/>
            <text y="20" text-anchor="middle" font-family="Bagel Fat One" font-size="58" fill="#feefb8">TRISOMY 21</text></g>
          <g id="n47" opacity="0" transform="translate(880 990)"><circle r="78" fill="#F6D365" stroke="#432f2e" stroke-width="8"/>
            <text y="22" text-anchor="middle" font-family="Bagel Fat One" font-size="70" fill="#432f2e">47</text></g>

          <!-- nondisjunction: chr 21 pair refuses to separate -->
          <g id="nd" opacity="0">
            <text x="540" y="330" text-anchor="middle" font-family="Bagel Fat One" font-size="64" fill="#432f2e">Nondisjunction</text>
            <text x="540" y="390" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#b2461a">meiosis mein 21 alag hi nahi hua</text>
            <circle cx="540" cy="620" r="170" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/>
            <g id="arrows" opacity="0" stroke="#432f2e" stroke-width="10" stroke-linecap="round" fill="none"><path d="M 430 760 L 340 800 M 340 800 L 372 770 M 340 800 L 380 808"/><path d="M 650 760 L 740 800 M 740 800 L 708 770 M 740 800 L 700 808"/></g>
            <g id="gL" opacity="0"><circle cx="270" cy="860" r="110" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/><text x="270" y="1010" text-anchor="middle" font-family="Bagel Fat One" font-size="40" fill="#b2461a">2 copies!</text></g>
            <g id="gR" opacity="0"><circle cx="810" cy="860" r="110" fill="#fffcf2" stroke="#432f2e" stroke-width="8" stroke-dasharray="16 12"/><text x="810" y="1010" text-anchor="middle" font-family="Bagel Fat One" font-size="40" fill="#432f2e">0 copies</text></g>
          </g>
          <g id="pair" opacity="0" transform="translate(540 610)"><g id="pairIn">${chrom(-45, 0, AC, '', 'X', 0.8)}${chrom(45, 0, AC, '', 'X', 0.8)}
            <text y="125" text-anchor="middle" font-family="Bagel Fat One" font-size="40" fill="#432f2e">21 + 21</text></g></g>

          <!-- new question -->
          <g id="newq" opacity="0">
            <rect x="70" y="280" width="940" height="270" rx="36" fill="#432f2e"/>
            <text x="540" y="355" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="#feefb8">AB TUMHARI BAARI 👀</text>
            <text x="540" y="432" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="58" fill="#feefb8">Klinefelter's syndrome</text>
            <text x="540" y="503" text-anchor="middle" font-family="Playfair Display" font-weight="900" font-size="54" fill="#F6D365">ka karyotype?</text>
            ${['45, XO', '47, XXY', '47, XYY', '47, +21'].map((v, i) => `<g class="nq" opacity="0" transform="translate(${i % 2 ? 785 : 295} ${660 + Math.floor(i / 2) * 130})"><rect x="-220" y="-52" width="440" height="104" rx="52" fill="#fffcf2" stroke="#432f2e" stroke-width="7"/><circle cx="-165" r="32" fill="#432f2e"/><text x="-165" y="12" text-anchor="middle" font-family="Inter" font-weight="800" font-size="32" fill="#feefb8">${'ABCD'[i]}</text><text x="30" y="17" text-anchor="middle" font-family="Bagel Fat One" font-size="50" fill="#432f2e">${v}</text></g>`).join('')}
            <text id="nq-hint" opacity="0" x="540" y="1000" text-anchor="middle" font-family="Bagel Fat One" font-size="58" fill="#b2461a">Answer → agli reel mein!</text>
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
      ${sfx}
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

      // ---------- Pixy: pop in, idle sway, expressions, lip-sync, reactions ----------
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
        let mm = m;
        if (mm === "closed") mm = ["joy", "friendly", "sly", "gusto"].includes(exp) ? "smile" : "closed";
        if ((exp === "shock" || exp === "confusion") && mm === "open") mm = "oh";
        if (mm === prevM) return;
        tl.set("#mo-" + prevM, { opacity: 0 }, t); tl.set("#mo-" + mm, { opacity: 1 }, t); prevM = mm;
      });
      const jolt = (t) => { tl.to("#face", { y: -50, duration: 0.12, ease: "power2.out" }, t); tl.to("#face", { y: 0, duration: 0.45, ease: "bounce.out" }, t + 0.12); };
      [C.yr, C.sahi, C.forty, C.follow].forEach(jolt);
      [C.out1, C.out2, C.out3].forEach((t) => tl.to("#face", { x: -18, duration: 0.07, yoyo: true, repeat: 5, ease: "none" }, t + 0.1));
      POPS.forEach(([k, t, side], i) => {
        const x = side === "R" ? 720 : 200, y = 1120;
        tl.fromTo("#fx-" + i, { opacity: 0, x, y, scale: 0.2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t);
        tl.to("#fx-" + i, { y: y - 50, duration: 0.6, ease: "sine.out" }, t + 0.3);
        tl.to("#fx-" + i, { opacity: 0, scale: 0.5, duration: 0.2 }, t + 1.1);
      });
      tl.to(".bob", { y: -8, duration: 0.35, yoyo: true, repeat: Math.max(0, Math.floor(END / 0.35) - 1), ease: "sine.inOut" }, 0);

      // ---------- 1. hook: NEET 2013 + MCQ ----------
      tl.set("#stamp", { opacity: 1 }, C.yr - 0.2);
      tl.fromTo("#stamp-in", { scale: 3, rotation: -18, transformOrigin: "50% 50%" }, { scale: 1, rotation: -4, duration: 0.3, ease: "power4.in" }, C.yr - 0.2);
      tl.fromTo("#stage", { x: 0 }, { x: 14, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, C.yr + 0.1);
      show("#qcard", C.down - 0.15, 0.4);
      ["A", "B", "C", "D"].forEach((k, i) => optIn(k, C.opts + i * 0.12));

      // ---------- 2. elimination: one mini-panel per wrong option, X + fly-off on each "Out!" ----------
      const elim = (k, p, start, out, dir, prevPanel) => {
        fade(prevPanel, start - 0.15, 0, 0.15);
        show(p, start, 0.35);
        tl.to("#opt-" + k + " .opt-in", { scale: 1.05, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, start + 0.1);
        tl.set("#opt-" + k + " .x", { opacity: 1 }, out);
        tl.to("#opt-" + k + " .opt-in", { x: dir * 1100, rotation: dir * 12, opacity: 0, duration: 0.45, ease: "power2.in" }, out + 0.35);
      };
      elim("B", "#pB", C.doY, C.out1, 1, "#qcard");
      elim("D", "#pD", C.teen, C.out2, -1, "#pB");
      elim("C", "#pC", C.mono, C.out3, 1, "#pD");

      // ---------- 3. reveal: A turns green, then the real karyotype ----------
      fade("#pC", T.reveal, 0, 0.2);
      fade("#qcard", T.reveal + 0.05, 1, 0.2);
      tl.set("#opt-A .tick", { opacity: 1 }, C.sahi + 0.3);
      tl.to("#opt-A rect", { attr: { fill: "#bfe8c8" }, duration: 0.2 }, C.sahi + 0.3);
      tl.to("#opt-A .opt-in", { y: 300, duration: 0.45, ease: "back.out(1.4)" }, C.sahi);
      tl.fromTo("#opt-A .opt-in", { scale: 1 }, { scale: 1.1, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 50%", immediateRender: false }, C.sahi + 0.45);
      fade("#qcard, #opt-A, #stamp", C.trisomy - 0.3, 0, 0.2);
      tl.fromTo("#kcard", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)", immediateRender: false }, C.trisomy - 0.2);
      show("#tri", C.trisomy, 0.35);
      tl.fromTo("#k21", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.25, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, C.trisomy + 0.3);
      tl.to("#tri", { x: 430, scale: 0.85, duration: 0.3, ease: "power2.out" }, C.forty - 0.1);
      show("#n47", C.forty - 0.05, 0.4);

      // ---------- 4. nondisjunction ----------
      fade("#kcard, #tri, #n47", T.nd, 0, 0.25);
      fade("#nd", T.nd + 0.1, 1, 0.3);
      show("#pair", T.nd + 0.3, 0.35);
      tl.to("#pairIn", { x: -270, y: 250, scale: 0.75, duration: 0.6, ease: "power2.inOut" }, C.alag - 0.2);
      fade("#arrows, #gL, #gR", C.alag - 0.1, 1, 0.3);
      tl.to("#pairIn", { x: -280, duration: 0.08, yoyo: true, repeat: 5, ease: "none" }, C.alag + 0.5);

      // ---------- 5. new question ----------
      fade("#nd, #pair", T.newq, 0, 0.25);
      tl.fromTo("#newq", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, T.newq + 0.1);
      gsap.utils.toArray(".nq").forEach((n, i) => tl.fromTo(n, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.6)", immediateRender: false }, C.kary + 0.1 + i * 0.12));
      show("#nq-hint", C.comment, 0.35);

      // ---------- 6. final frame: brand + follow (only place the name appears) ----------
      fade("#newq", T.end, 0, 0.2);
      tl.set("#brand", { opacity: 1 }, T.end + 0.15);
      tl.fromTo("#brand > g:first-child", { scale: 0.5, opacity: 0, transformOrigin: "540px 520px" }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)", immediateRender: false }, T.end + 0.15);
      show("#follow", C.follow + 0.1);
      tl.to("#follow", { scale: 0.9, duration: 0.1, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }, C.follow + 0.7);

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>`;
fs.writeFileSync(path.join(ROOT, 'index.html'), html);
console.log('index.html written, END', END, JSON.stringify(C));
