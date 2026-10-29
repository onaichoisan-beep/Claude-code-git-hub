// Builds index.html for the v3 reel: all-animated scenes + Pixy's face lip-syncing to the user's voice.
// Cue times come from the whisper transcript of assets/audio/vo.mp3 (assets/audio/transcript.json).
const fs = require('fs');
const path = require('path');
const { rig, PIVOTS } = require('./pixy_rig.cjs');
const ROOT = path.join(__dirname, '..');
const LIPS = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/audio/lips.json')));
const WORDS = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/audio/transcript.json')));
const END = 29.4;

// first transcript word (after `after` seconds) starting with `w`
const cue = (w, after = 0) => {
  const hit = WORDS.find((x) => x.start >= after && x.text.toLowerCase().replace(/[^a-z]/g, '').startsWith(w));
  if (!hit) throw new Error('cue not found: ' + w);
  return +hit.start.toFixed(2);
};
const C = {
  stop: cue('stop'), bicycle: cue('bicycle'), liver: cue('liver'), urea: cue('urea'), krebs: cue('krebs'),
  molecule: cue('molecule'), breaks: cue('breaks'), fum: cue('fumarate'), chain: cue('chain'), krebs2: cue('krebs', 14),
  back: cue('back'), asp: cue('aspartate'), that: cue('that', 17.5), kbike: cue('krebs', 19), neat: cue('neat'),
  enzyme: cue('enzyme'), comment: cue('comment'), next: cue('next'), follow: cue('follow'), score: cue('score'),
};
const T = { hook: 0, wheels: C.urea - 1.3, molecule: C.molecule - 0.25, chain: C.fum + 0.6, name: C.that - 0.2, question: C.neat - 0.2, cta: C.comment - 0.2 };

// one keyword on screen at a time
const KEYS = [['RUKO!', C.stop], ['BICYCLE?!', C.bicycle], ['LIVER mein!', C.liver], ['UREA cycle', C.urea], ['KREBS cycle', C.krebs],
  ['toot-ta hai…', C.breaks], ['FUMARATE!', C.fum], ['CHAIN', C.chain], ['wapas…', C.back], ['ASPARTATE', C.asp],
  ['KREBS BIcycle!', C.kbike], ['NEET Q', C.neat], ['COMMENT', C.comment], ['FOLLOW!', C.follow]];
const keys = KEYS.map(([txt, t], i) => {
  const next = i + 1 < KEYS.length ? KEYS[i + 1][1] : END;
  const d = Math.min(next - t, 1.6);
  return `<div id="key-${i}" class="key clip" data-start="${t}" data-duration="${d.toFixed(2)}" data-track-index="5"><span>${txt}</span></div>`;
}).join('\n      ');

// Pixy's head only, pulled out of the full rig
const full = rig();
const head = full.slice(full.indexOf('<g id="px-head">'), full.lastIndexOf('  </g>\n</g>'));

const FX = {
  bang: '<circle cx="85" cy="85" r="70" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><text x="85" y="124" text-anchor="middle" font-family="Bagel Fat One" font-size="108" fill="#432f2e">!</text>',
  q: '<circle cx="85" cy="85" r="70" fill="#432f2e"/><text x="85" y="122" text-anchor="middle" font-family="Bagel Fat One" font-size="100" fill="#feefb8">?</text>',
  spark: '<path d="M85 5 L 102 68 L 165 85 L 102 102 L 85 165 L 68 102 L 5 85 L 68 68 Z" fill="#F6D365" stroke="#432f2e" stroke-width="7" stroke-linejoin="round"/>',
  heart: '<path d="M85 150 C 20 105 10 70 30 45 C 50 22 78 30 85 52 C 92 30 120 22 140 45 C 160 70 150 105 85 150 Z" fill="#e8743b" stroke="#432f2e" stroke-width="8" stroke-linejoin="round"/>',
  sweat: '<path d="M85 20 C 110 70 130 95 120 125 C 110 150 60 150 50 125 C 40 95 60 70 85 20 Z" fill="#c4dae8" stroke="#432f2e" stroke-width="8"/>',
};
const POPS = [['bang', C.stop, 'R'], ['bang', C.liver, 'L'], ['sweat', C.breaks, 'R'], ['spark', C.fum, 'L'], ['spark', C.fum + 0.15, 'R'],
  ['spark', C.kbike, 'L'], ['spark', C.kbike + 0.2, 'R'], ['q', C.enzyme - 0.3, 'R'], ['heart', C.follow, 'R'], ['heart', C.score, 'L']];
const fx = POPS.map(([k], i) => `<svg id="fx-${i}" class="fx" viewBox="-10 -10 190 190" width="170" height="170">${FX[k]}</svg>`).join('\n        ');

// a cute molecule character
const blob = (id, fill, label, labelFill = '#432f2e') => `<g id="${id}" opacity="0">
  <circle r="62" fill="${fill}" stroke="#432f2e" stroke-width="8"/>
  <circle cx="-20" cy="-10" r="9" fill="#432f2e"/><circle cx="20" cy="-10" r="9" fill="#432f2e"/>
  <circle cx="-17" cy="-13" r="3" fill="#fff"/><circle cx="23" cy="-13" r="3" fill="#fff"/>
  <path d="M -16 14 Q 0 30 16 14" fill="none" stroke="#432f2e" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="-36" cy="12" rx="9" ry="5" fill="#FF9AAE" opacity="0.8"/><ellipse cx="36" cy="12" rx="9" ry="5" fill="#FF9AAE" opacity="0.8"/>
  ${label ? `<text y="-82" text-anchor="middle" font-family="Bagel Fat One" font-size="40" fill="${labelFill}" stroke="#fffcf2" stroke-width="8" paint-order="stroke">${label}</text>` : ''}
</g>`;
const wheel = (id, cx, cy, tire) => `<g id="${id}">
  <circle cx="${cx}" cy="${cy}" r="150" fill="#fffcf2" stroke="${tire}" stroke-width="26"/>
  <circle cx="${cx}" cy="${cy}" r="150" fill="none" stroke="#432f2e" stroke-width="5"/>
  <g id="${id}-spokes">${[0, 30, 60, 90, 120, 150].map((a) => `<line x1="${cx - 135 * Math.cos(a * Math.PI / 180)}" y1="${cy - 135 * Math.sin(a * Math.PI / 180)}" x2="${cx + 135 * Math.cos(a * Math.PI / 180)}" y2="${cy + 135 * Math.sin(a * Math.PI / 180)}" stroke="#432f2e" stroke-width="4" opacity="0.6"/>`).join('')}</g>
  <circle cx="${cx}" cy="${cy}" r="16" fill="#432f2e"/>
</g>`;

const html = `<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Playfair Display"; font-weight: 900; font-style: normal; src: url("assets/fonts/playfair-900.ttf"); }
      @font-face { font-family: "Playfair Display"; font-weight: 700; font-style: italic; src: url("assets/fonts/playfair-700i.ttf"); }
      @font-face { font-family: "Bagel Fat One"; src: url("assets/fonts/bagel.ttf"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-800.ttf"); }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #feefb8; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; color: #432f2e;
        background: radial-gradient(circle, rgba(159, 192, 214, 0.45) 3px, transparent 4px) 0 0 / 46px 46px, #feefb8; }
      #stage { position: absolute; inset: 0; }
      #logo { position: absolute; left: 40px; top: 60px; width: 470px; height: 140px; }
      #world { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
      .key { position: absolute; left: 0; top: 1035px; width: 1080px; text-align: center; }
      .key span { display: inline-block; padding: 0 36px; border-radius: 40px; background: #432f2e; color: #feefb8;
        font: 400 84px/1.35 "Bagel Fat One"; white-space: nowrap; }
      #face { position: absolute; left: 250px; top: 1215px; width: 580px; height: 677px; overflow: visible; }
      .fx { position: absolute; left: 0; top: 0; opacity: 0; }
      #q-card { position: absolute; left: 70px; top: 250px; width: 940px; height: 740px; border-radius: 40px; background: #fffcf2;
        border: 10px solid #432f2e; padding: 40px 46px; opacity: 0; }
      #q-tag { display: inline-block; height: 60px; padding: 0 26px; border-radius: 30px; background: #e8743b; color: #fffcf2; font: 800 30px/60px "Inter"; letter-spacing: 0.08em; }
      #q-text { margin-top: 20px; font: 900 62px/1.12 "Playfair Display"; }
      .opt { margin-top: 18px; height: 80px; border-radius: 40px; border: 5px solid #432f2e; background: #feefb8; font: 800 34px/70px "Inter"; padding-left: 22px; white-space: nowrap; opacity: 0; }
      .opt b { display: inline-block; width: 54px; height: 54px; border-radius: 27px; background: #432f2e; color: #feefb8; text-align: center; line-height: 54px; margin-right: 14px; font-size: 28px; }
      #cta { position: absolute; inset: 0; opacity: 0; }
      #cta-logo { position: absolute; left: 40px; top: 230px; width: 1000px; height: 460px; }
      #follow-btn { position: absolute; left: 290px; top: 760px; width: 500px; height: 124px; border-radius: 62px; background: #432f2e; color: #feefb8; font: 400 64px/124px "Bagel Fat One"; text-align: center; }
      #comment { position: absolute; left: 600px; top: 560px; width: 380px; height: 170px; opacity: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${END}" data-width="1080" data-height="1920">
      <div id="stage" class="clip" data-start="0" data-duration="${END}" data-track-index="1">
        <svg id="world" viewBox="0 0 1080 1920">
          <defs><clipPath id="stage-clip"><rect x="0" y="210" width="1080" height="820"/></clipPath></defs>
          <g clip-path="url(#stage-clip)">
          <g id="cam">
            <path id="liver" opacity="0" d="M 90 560 C 110 400 360 340 560 360 C 780 380 1000 400 1000 540 C 1000 680 820 760 630 820 C 470 870 290 920 180 850 C 100 800 75 680 90 560 Z" fill="#a8604f" stroke="#432f2e" stroke-width="10"/>
            <path id="liver-shine" opacity="0" d="M 180 520 C 220 440 360 410 470 420" fill="none" stroke="#c98571" stroke-width="22" stroke-linecap="round"/>
            <path id="chain" opacity="0" d="M 330 470 L 750 470 A 170 170 0 0 1 750 810 L 330 810 A 170 170 0 0 1 330 470 Z" fill="none" stroke="#432f2e" stroke-width="14" stroke-dasharray="24 12"/>
            <path id="chain-top" opacity="0" d="M 330 470 L 750 470" fill="none" stroke="#e8743b" stroke-width="18" stroke-linecap="round"/>
            <path id="chain-bot" opacity="0" d="M 750 810 L 330 810" fill="none" stroke="#9fc0d6" stroke-width="18" stroke-linecap="round"/>
            <g id="bike">
              <g id="frame" stroke="#432f2e" stroke-width="16" stroke-linecap="round" fill="none">
                <line x1="330" y1="640" x2="520" y2="660"/><line x1="520" y1="660" x2="470" y2="450"/><line x1="330" y1="640" x2="470" y2="450"/>
                <line x1="470" y1="450" x2="710" y2="455"/><line x1="520" y1="660" x2="700" y2="520"/><line x1="700" y1="520" x2="750" y2="640"/>
                <line x1="710" y1="455" x2="700" y2="520"/><path d="M 690 420 Q 720 395 770 410"/>
                <rect x="420" y="420" width="110" height="26" rx="13" fill="#432f2e" stroke="none"/>
                <circle cx="520" cy="660" r="30" fill="#fffcf2"/>
              </g>
              ${wheel('wU', 330, 640, '#c4dae8')}
              ${wheel('wK', 750, 640, '#e8743b')}
              <text id="lbl-u" opacity="0" x="330" y="655" text-anchor="middle" font-family="Bagel Fat One" font-size="52" fill="#432f2e">UREA</text>
              <text id="lbl-k" opacity="0" x="750" y="655" text-anchor="middle" font-family="Bagel Fat One" font-size="52" fill="#432f2e">KREBS</text>
            </g>
            <g id="mol-wrap" transform="translate(330 395)">${blob('mol', '#fffcf2', '')}
              <g id="half-a" opacity="0"><path d="M -6 -62 A 62 62 0 0 0 -6 62 L 4 30 L -10 0 L 6 -30 Z" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/></g>
              <g id="half-b" opacity="0"><path d="M 6 -62 A 62 62 0 0 1 6 62 L 16 30 L 2 0 L 18 -30 Z" fill="#fffcf2" stroke="#432f2e" stroke-width="8"/></g>
            </g>
            <g id="fum-wrap" transform="translate(330 395)">${blob('fum', '#e8743b', 'Fumarate')}</g>
            <g id="asp-wrap" transform="translate(750 880)">${blob('asp', '#c4dae8', 'Aspartate')}</g>
          </g>
          </g>
        </svg>
        <svg id="logo" viewBox="0 0 470 140">
          <g transform="rotate(-9 235 70)">
            <text x="12" y="96" font-family="Playfair Display" font-weight="900" font-size="44" fill="#432f2e">SCROLL</text>
            <text x="196" y="108" font-family="Playfair Display" font-weight="900" font-size="88" fill="#c4dae8" stroke="#432f2e" stroke-width="3" paint-order="stroke">2</text>
            <text x="250" y="74" font-family="Playfair Display" font-weight="900" font-size="44" fill="#432f2e">SCORE</text>
          </g>
        </svg>
        <div id="q-card">
          <div id="q-tag">NEET QUESTION</div>
          <div id="q-text">Fumarate kaunsa enzyme release karta hai?</div>
          <div class="opt"><b>A</b>Arginase</div>
          <div class="opt"><b>B</b>Argininosuccinate lyase</div>
          <div class="opt"><b>C</b>Fumarase</div>
          <div class="opt"><b>D</b>Argininosuccinate synthetase</div>
        </div>
        <div id="cta">
          <svg id="cta-logo" viewBox="0 0 1000 460">
            <g transform="rotate(-12 500 230)">
              <text x="30" y="300" font-family="Playfair Display" font-weight="900" font-size="104" fill="#432f2e">SCROLL</text>
              <text x="455" y="330" font-family="Playfair Display" font-weight="900" font-size="250" fill="#c4dae8" stroke="#432f2e" stroke-width="6" paint-order="stroke">2</text>
              <text x="600" y="235" font-family="Playfair Display" font-weight="900" font-size="104" fill="#432f2e">SCORE</text>
            </g>
          </svg>
          <div id="follow-btn">FOLLOW</div>
        </div>
        <svg id="comment" viewBox="0 0 380 170"><path d="M 20 20 H 360 Q 370 20 370 30 V 115 Q 370 125 360 125 H 100 L 55 160 L 64 125 H 20 Q 10 125 10 115 V 30 Q 10 20 20 20 Z" fill="#fffcf2" stroke="#432f2e" stroke-width="7"/><text x="190" y="92" text-anchor="middle" font-family="Bagel Fat One" font-size="48" fill="#432f2e">A / B / C / D?</text></svg>
        <svg id="face" viewBox="120 40 360 420"><g id="face-root">${head}</g></svg>
        ${fx}
      </div>
      ${keys}
      <audio id="vo" class="clip" src="assets/audio/vo.mp3" data-start="0" data-duration="${END}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      const C = ${JSON.stringify(C)};
      const T = ${JSON.stringify(T)};
      const LIPS = ${JSON.stringify(LIPS)};
      const POPS = ${JSON.stringify(POPS)};
      const P = ${JSON.stringify(PIVOTS)};
      const END = ${END};
      const tl = gsap.timeline({ paused: true });
      const at = (sel, vars, t, d = 0.3, ease = "power2.out") => tl.to(sel, { ...vars, duration: d, ease }, t);
      const show = (sel, t, d = 0.3) => tl.fromTo(sel, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2.6)", immediateRender: false }, t);
      const hide = (sel, t, d = 0.2) => tl.to(sel, { opacity: 0, duration: d }, t);
      ["head", "hair", "eyeL", "eyeR", "browL", "browR"].forEach((k) => gsap.set("#px-" + k, { svgOrigin: P[k] }));
      gsap.set("#face-root", { svgOrigin: "300 430" });

      // ---------- Pixy's face ----------
      // pop in, then keep a lively idle: sway + bob for the whole reel (finite repeats)
      tl.fromTo("#face", { y: 700, rotation: -12 }, { y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.6)" }, 0);
      tl.fromTo("#face-root", { rotation: -4 }, { rotation: 4, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(END / 1.1) - 1) }, 0.3);
      tl.fromTo("#face", { scale: 1 }, { scale: 1.025, duration: 0.55, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(END / 0.55) - 1), transformOrigin: "50% 100%" }, 0.3);
      // lip-sync from the voice loudness
      const MOUTHS = ["closed", "smile", "mid", "open", "oh", "ee"];
      let prevM = "smile";
      const setMouth = (m, t) => { if (m === prevM) return; tl.set("#px-m-" + prevM, { opacity: 0 }, t); tl.set("#px-m-" + m, { opacity: 1 }, t); prevM = m; };
      // expression windows force an "oh" mouth while shocked
      const OH = [[C.stop, C.stop + 0.6], [C.breaks, C.breaks + 0.5]];
      LIPS.forEach(([t, m]) => setMouth(m !== "closed" && OH.some(([a, b]) => t >= a && t < b) ? "oh" : m, t));
      // eyes
      const EYES = ["norm", "shock", "happy", "wink"];
      let prevE = "norm";
      const eyes = (k, t) => { if (k === prevE) return; tl.set("#px-eyes-" + prevE, { opacity: 0 }, t); tl.set("#px-eyes-" + k, { opacity: 1 }, t); prevE = k; };
      const brows = (y, t, rotL = 0, rotR = 0) => { at("#px-browL", { y, rotation: rotL }, t, 0.18, "back.out(3)"); at("#px-browR", { y, rotation: rotR }, t, 0.18, "back.out(3)"); };
      const look = (x, y, t) => at(".px-pupil", { x, y }, t, 0.2);
      const nod = (t, amt = 1) => { tl.to("#face-root", { y: 14 * amt, duration: 0.1, yoyo: true, repeat: 1, ease: "power1.inOut" }, t); };
      const jolt = (t) => { tl.to("#face", { y: -60, duration: 0.12, ease: "power2.out" }, t); tl.to("#face", { y: 0, duration: 0.4, ease: "bounce.out" }, t + 0.12);
        tl.fromTo("#px-hair", { scaleY: 1 }, { scaleY: 1.15, duration: 0.1, yoyo: true, repeat: 1, immediateRender: false }, t); };
      const blink = (t) => { tl.to("#px-eyeL, #px-eyeR", { scaleY: 0.08, duration: 0.06 }, t); tl.to("#px-eyeL, #px-eyeR", { scaleY: 1, duration: 0.08 }, t + 0.08); };

      eyes("shock", C.stop); brows(-22, C.stop);
      eyes("norm", C.stop + 0.9); brows(0, C.stop + 0.9);
      nod(C.bicycle); look(0, -8, C.bicycle);
      eyes("shock", C.liver); brows(-18, C.liver); jolt(C.liver); look(0, 0, C.liver);
      eyes("norm", C.liver + 0.7); brows(0, C.liver + 0.7);
      look(-8, -6, C.urea); nod(C.urea, 0.6); look(8, -6, C.krebs); nod(C.krebs, 0.6);
      look(-6, -8, C.molecule); brows(-8, C.molecule, 0, -10);
      eyes("shock", C.breaks); brows(-20, C.breaks); jolt(C.breaks);
      eyes("norm", C.breaks + 0.6); brows(0, C.breaks + 0.6); look(0, 0, C.breaks + 0.6);
      eyes("happy", C.fum); jolt(C.fum); eyes("norm", C.fum + 0.7);
      look(-8, -6, C.chain); look(8, -6, C.krebs2); look(8, 2, C.back); look(-8, 2, C.asp + 0.2); nod(C.asp);
      look(0, 0, C.that); eyes("happy", C.kbike); jolt(C.kbike); eyes("wink", C.kbike + 0.6); eyes("norm", C.neat - 0.1);
      brows(0, C.neat, 0, -12); at("#px-browR", { y: -16 }, C.neat, 0.2); look(5, -9, C.enzyme - 0.2); at("#face-root", { x: 0 }, C.neat, 0.1);
      brows(0, C.comment); look(0, 0, C.comment);
      eyes("wink", C.follow); jolt(C.follow); eyes("happy", C.score);
      [1.6, 5.0, 10.2, 15.0, 18.0, 24.2].forEach(blink);
      // reaction pop-ups beside his head
      POPS.forEach(([k, t, side], i) => {
        const x = side === "R" ? 790 : 120, y = 1200;
        tl.fromTo("#fx-" + i, { opacity: 0, x, y, scale: 0.2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t);
        tl.to("#fx-" + i, { y: y - 50, duration: 0.6, ease: "sine.out" }, t + 0.3);
        tl.to("#fx-" + i, { opacity: 0, scale: 0.5, duration: 0.2 }, t + 1.0);
      });

      // ---------- keywords ----------
      gsap.utils.toArray(".key span").forEach((s) => {
        const t = parseFloat(s.parentElement.getAttribute("data-start"));
        tl.fromTo(s, { scale: 0.4, rotation: -6 }, { scale: 1, rotation: -2, duration: 0.3, ease: "back.out(3)" }, t);
      });
      tl.fromTo("#logo", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35 }, 0.1);

      // ---------- 1. hook: bicycle rolls in, liver appears around it ----------
      gsap.set("#wU-spokes", { svgOrigin: "330 640" }); gsap.set("#wK-spokes", { svgOrigin: "750 640" });
      tl.fromTo("#bike", { x: -1100 }, { x: 0, duration: 0.9, ease: "power3.out" }, 0.1);
      tl.fromTo("#wU-spokes, #wK-spokes", { rotation: 0 }, { rotation: 540, duration: 0.9, ease: "power3.out" }, 0.1);
      tl.to("#bike", { y: -30, duration: 0.12, yoyo: true, repeat: 1 }, C.bicycle);
      tl.to("#liver", { opacity: 1, duration: 0.01 }, C.liver - 0.05);
      tl.fromTo("#liver", { scale: 0.2, transformOrigin: "540px 600px" }, { scale: 1, duration: 0.4, ease: "back.out(1.7)", immediateRender: false }, C.liver - 0.05);
      tl.to("#liver-shine", { opacity: 1, duration: 0.2 }, C.liver + 0.3);
      // dive into the liver
      tl.to("#liver, #liver-shine", { scale: 3, opacity: 0, duration: 0.5, ease: "power2.in", transformOrigin: "540px 600px" }, T.wheels - 0.1);

      // ---------- 2. two wheels = two cycles ----------
      tl.to("#frame", { opacity: 0.25, duration: 0.3 }, T.wheels);
      tl.to("#lbl-u", { opacity: 1, duration: 0.01 }, C.urea);
      tl.fromTo("#wU", { scale: 1, transformOrigin: "330px 640px" }, { scale: 1.15, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }, C.urea);
      tl.to("#lbl-k", { opacity: 1, duration: 0.01 }, C.krebs);
      tl.fromTo("#wK", { scale: 1, transformOrigin: "750px 640px" }, { scale: 1.15, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }, C.krebs);
      tl.to("#frame", { opacity: 0, duration: 0.3 }, T.molecule);

      // ---------- 3. a molecule cracks on the urea wheel -> fumarate pops out ----------
      show("#mol", C.molecule);
      tl.to("#mol", { x: -8, duration: 0.05, yoyo: true, repeat: 9, ease: "none" }, C.breaks - 0.3);
      hide("#mol", C.breaks + 0.25, 0.01);
      tl.set("#half-a, #half-b", { opacity: 1 }, C.breaks + 0.25);
      tl.to("#half-a", { x: -90, y: 60, rotation: -40, opacity: 0, duration: 0.9, ease: "power2.out" }, C.breaks + 0.25);
      tl.to("#half-b", { x: 90, y: 60, rotation: 40, opacity: 0, duration: 0.9, ease: "power2.out" }, C.breaks + 0.25);
      show("#fum", C.fum - 0.1, 0.4);
      tl.fromTo("#fum", { y: 0 }, { y: -40, duration: 0.25, yoyo: true, repeat: 1 }, C.fum + 0.35);

      // ---------- 4. fumarate rides the chain into Krebs, comes back as aspartate ----------
      tl.to("#chain", { opacity: 1, duration: 0.3 }, T.chain);
      tl.fromTo("#chain", { strokeDashoffset: 0 }, { strokeDashoffset: -360, duration: C.that - T.chain, ease: "none" }, T.chain);
      tl.fromTo("#chain-top", { opacity: 1, strokeDasharray: 420, strokeDashoffset: 420 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut", immediateRender: false }, C.chain - 0.2);
      tl.to("#fum-wrap", { x: 420, duration: Math.max(0.6, C.krebs2 - C.chain + 0.2), ease: "power1.inOut" }, C.chain);
      tl.to("#fum", { y: -26, duration: 0.18, yoyo: true, repeat: 5, ease: "sine.inOut" }, C.chain);
      tl.fromTo("#wK-spokes", { rotation: 540 }, { rotation: 1260, duration: 1.4, ease: "power2.inOut", immediateRender: false }, C.krebs2);
      tl.to("#fum", { y: 245, scale: 0.4, opacity: 0, duration: 0.5, ease: "power2.in" }, C.krebs2 + 0.3);
      tl.fromTo("#chain-bot", { opacity: 1, strokeDasharray: 420, strokeDashoffset: 420 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut", immediateRender: false }, C.back - 0.2);
      show("#asp", C.back, 0.35);
      tl.to("#asp-wrap", { x: -420, duration: Math.max(0.8, C.that - C.back - 0.2), ease: "power1.inOut" }, C.back + 0.3);
      tl.to("#asp", { y: 22, duration: 0.18, yoyo: true, repeat: 5, ease: "sine.inOut" }, C.back + 0.3);
      tl.fromTo("#wU-spokes", { rotation: 540 }, { rotation: -180, duration: 1.4, ease: "power2.inOut", immediateRender: false }, C.asp);

      // ---------- 5. it IS a bicycle ----------
      hide("#asp, #chain-top, #chain-bot", T.name, 0.25);
      tl.to("#chain", { opacity: 0.5, duration: 0.3 }, T.name);
      tl.to("#frame", { opacity: 1, duration: 0.35 }, T.name + 0.1);
      tl.fromTo("#frame line, #frame path", { strokeDasharray: 400, strokeDashoffset: 400 }, { strokeDashoffset: 0, duration: 0.6, ease: "power2.out", stagger: 0.05, immediateRender: false }, T.name + 0.1);
      tl.to("#bike, #chain", { x: 60, duration: 0.6, ease: "power2.inOut" }, C.kbike);
      tl.to("#wU-spokes, #wK-spokes", { rotation: "+=360", duration: 0.6, ease: "power2.inOut" }, C.kbike);
      tl.to("#bike", { y: -24, duration: 0.15, yoyo: true, repeat: 1 }, C.kbike + 0.6);

      // ---------- 6. NEET question ----------
      hide("#cam", T.question, 0.25);
      tl.fromTo("#q-card", { opacity: 0, y: 140, rotation: 3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, T.question);
      gsap.utils.toArray(".opt").forEach((o, i) => tl.fromTo(o, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, C.enzyme + i * 0.12));

      // ---------- 7. call to action ----------
      hide("#q-card", T.cta, 0.25); hide("#logo", T.cta, 0.2);
      tl.to("#cta", { opacity: 1, duration: 0.3 }, T.cta + 0.1);
      tl.fromTo("#cta-logo", { scale: 0.6 }, { scale: 1, duration: 0.45, ease: "back.out(2)" }, T.cta + 0.1);
      tl.fromTo("#comment", { opacity: 0, scale: 0.3, transformOrigin: "15% 100%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, C.comment);
      tl.fromTo("#follow-btn", { scale: 0.5 }, { scale: 1, duration: 0.4, ease: "back.out(2.4)" }, C.follow - 0.2);
      tl.to("#follow-btn", { scale: 0.9, duration: 0.1, yoyo: true, repeat: 1 }, C.follow + 0.4);
      tl.fromTo("#follow-btn", { backgroundColor: "#432f2e" }, { backgroundColor: "#e8743b", duration: 0.2, immediateRender: false }, C.follow + 0.5);

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>`;
fs.writeFileSync(path.join(ROOT, 'index.html'), html);
console.log('index.html written', JSON.stringify(C));
