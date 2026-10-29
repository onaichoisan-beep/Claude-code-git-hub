// Builds index.html: a 12 s silent move test for the Pixy rig.
const fs = require('fs');
const path = require('path');
const { rig, PIVOTS } = require('./pixy_rig.cjs');
const ROOT = path.join(__dirname, '..');

const SEGMENTS = [
  [0.0, 'Jump in'], [1.0, 'Wave + talk'], [2.8, 'Shock!'], [4.2, 'Point left'],
  [6.0, 'Point right'], [7.8, 'Thinking'], [9.4, 'Celebrate'], [11.0, 'Wink'],
];
const END = 12;
const labels = SEGMENTS.map(([t, txt], i) => {
  const e = i + 1 < SEGMENTS.length ? SEGMENTS[i + 1][0] : END;
  return `<div id="lab-${i}" class="lab clip" data-start="${t}" data-duration="${(e - t).toFixed(2)}" data-track-index="3"><span>${i + 1}. ${txt}</span></div>`;
}).join('\n      ');

const html = `<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Bagel Fat One"; src: url("assets/fonts/bagel.ttf"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-800.ttf"); }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #feefb8; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden;
        background: radial-gradient(circle, rgba(159, 192, 214, 0.45) 3px, transparent 4px) 0 0 / 46px 46px, #feefb8; }
      #stage { position: absolute; inset: 0; }
      #title { position: absolute; left: 0; top: 90px; width: 1080px; text-align: center; font: 400 64px "Bagel Fat One"; color: #432f2e; }
      .lab { position: absolute; left: 0; top: 190px; width: 1080px; text-align: center; }
      .lab span { display: inline-block; padding: 8px 34px; border-radius: 40px; background: #432f2e; color: #feefb8; font: 800 44px/1.3 "Inter"; }
      .target { position: absolute; top: 470px; width: 250px; height: 250px; border-radius: 125px; background: #fffcf2;
        border: 18px solid; font: 400 48px/214px "Bagel Fat One"; color: #432f2e; text-align: center; }
      #pixy-svg { position: absolute; left: 130px; top: 780px; width: 820px; height: 1080px; overflow: visible; }
      .fx { position: absolute; left: 0; top: 0; opacity: 0; font: 400 120px "Bagel Fat One"; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${END}" data-width="1080" data-height="1920">
      <div id="stage" class="clip" data-start="0" data-duration="${END}" data-track-index="1">
        <div id="title">PIXY · MOVE TEST</div>
        <div id="t-urea" class="target" style="left: 60px; border-color: #c4dae8">UREA</div>
        <div id="t-krebs" class="target" style="left: 770px; border-color: #e8743b">KREBS</div>
        <svg id="pixy-svg" viewBox="0 0 600 790">${rig()}</svg>
        <svg id="fx-bang" class="fx" viewBox="0 0 170 170" width="170" height="170"><circle cx="85" cy="85" r="70" fill="#F6D365" stroke="#432f2e" stroke-width="8"/><text x="85" y="124" text-anchor="middle" font-family="Bagel Fat One" font-size="108" fill="#432f2e">!</text></svg>
        <svg id="fx-q" class="fx" viewBox="0 0 170 170" width="170" height="170"><circle cx="85" cy="85" r="70" fill="#432f2e"/><text x="85" y="122" text-anchor="middle" font-family="Bagel Fat One" font-size="100" fill="#feefb8">?</text></svg>
        <svg id="fx-spark1" class="fx" viewBox="0 0 170 170" width="140" height="140"><path d="M85 5 L 102 68 L 165 85 L 102 102 L 85 165 L 68 102 L 5 85 L 68 68 Z" fill="#F6D365" stroke="#432f2e" stroke-width="7" stroke-linejoin="round"/></svg>
        <svg id="fx-spark2" class="fx" viewBox="0 0 170 170" width="100" height="100"><path d="M85 5 L 102 68 L 165 85 L 102 102 L 85 165 L 68 102 L 5 85 L 68 68 Z" fill="#c4dae8" stroke="#432f2e" stroke-width="8" stroke-linejoin="round"/></svg>
        <svg id="fx-dust" class="fx" viewBox="0 0 400 80" width="560" height="112"><g fill="#fffcf2" stroke="#432f2e" stroke-width="5"><circle cx="40" cy="50" r="24"/><circle cx="90" cy="40" r="30"/><circle cx="310" cy="40" r="30"/><circle cx="360" cy="50" r="24"/></g></svg>
      </div>
      ${labels}
    </div>
    <script>
      const P = ${JSON.stringify(PIVOTS)};
      const tl = gsap.timeline({ paused: true });
      const at = (sel, vars, t, d = 0.3, ease = "power2.out") => tl.to(sel, { ...vars, duration: d, ease }, t);
      const piv = (sel, key) => gsap.set(sel, { svgOrigin: P[key] });
      piv("#px-root", "root"); piv("#px-body", "body"); piv("#px-head", "head"); piv("#px-hair", "hair");
      piv("#px-armL", "armL"); piv("#px-armR", "armR"); piv("#px-legL", "legL"); piv("#px-legR", "legR");
      piv("#px-eyeL", "eyeL"); piv("#px-eyeR", "eyeR"); piv("#px-browL", "browL"); piv("#px-browR", "browR");

      // ---- helpers ----
      const EYES = ["norm", "shock", "happy", "wink"];
      const eyes = (k, t) => EYES.forEach((e) => tl.set("#px-eyes-" + e, { opacity: e === k ? 1 : 0 }, t));
      const MOUTHS = ["closed", "smile", "mid", "open", "oh", "ee"];
      const mouth = (k, t) => MOUTHS.forEach((m) => tl.set("#px-m-" + m, { opacity: m === k ? 1 : 0 }, t));
      // talking: a fixed, varied open/close pattern (real reels use the voice loudness instead)
      const TALK = ["mid", "open", "closed", "ee", "open", "mid", "closed", "oh", "mid", "open", "closed", "ee"];
      const talk = (t0, t1, rest = "smile") => { let i = 0; for (let t = t0; t < t1 - 0.05; t += 0.09, i++) mouth(TALK[i % TALK.length], t); mouth(rest, t1); };
      const blink = (t) => { tl.to("#px-eyeL, #px-eyeR", { scaleY: 0.08, duration: 0.06, ease: "power1.in" }, t); tl.to("#px-eyeL, #px-eyeR", { scaleY: 1, duration: 0.08, ease: "power1.out" }, t + 0.08); };
      const squash = (t, amt = 1) => {
        tl.to("#px-root", { scaleY: 1 - 0.16 * amt, scaleX: 1 + 0.12 * amt, duration: 0.08, ease: "power2.out" }, t);
        tl.to("#px-root", { scaleY: 1, scaleX: 1, duration: 0.45, ease: "elastic.out(1.1, 0.4)" }, t + 0.08);
        tl.fromTo("#px-hair", { scaleY: 1 }, { scaleY: 1.12, duration: 0.08, yoyo: true, repeat: 1, ease: "power1.out", immediateRender: false }, t);
      };
      const popFx = (id, x, y, t, life = 1.1) => {
        tl.fromTo(id, { opacity: 0, x, y, scale: 0.2, rotation: -30 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t);
        tl.to(id, { y: y - 40, duration: 0.6, ease: "sine.out" }, t + 0.3);
        tl.to(id, { opacity: 0, scale: 0.5, duration: 0.2 }, t + life);
      };
      const arm = (side, rot, t, d = 0.3, ease = "back.out(1.8)") => at("#px-arm" + side, { rotation: rot }, t, d, ease);
      const finger = (side, on, t) => tl.set("#px-finger" + side, { opacity: on ? 1 : 0 }, t);
      const look = (x, y, t) => at(".px-pupil", { x, y }, t, 0.2);

      // idle breathing for the whole clip (finite repeats)
      tl.fromTo("#px-body", { scaleY: 1 }, { scaleY: 1.015, duration: 0.7, yoyo: true, repeat: Math.max(0, Math.floor(${END} / 0.7) - 1), ease: "sine.inOut" }, 0);
      [0.5, 2.3, 5.4, 7.2, 10.8].forEach(blink);

      // 1. jump in from below, land with squash + dust
      tl.fromTo("#px-root", { y: 1000 }, { y: -160, duration: 0.42, ease: "power2.out" }, 0.05);
      tl.to("#px-root", { y: 0, duration: 0.25, ease: "power2.in" }, 0.47);
      arm("L", 40, 0.05, 0.2); arm("R", -40, 0.05, 0.2); arm("L", 0, 0.72, 0.3); arm("R", 0, 0.72, 0.3);
      squash(0.72, 1.2); popFx("#fx-dust", 260, 1690, 0.72, 0.5);
      eyes("happy", 0.05); eyes("norm", 0.8); mouth("open", 0.05); mouth("smile", 0.8);

      // 2. wave + talk
      arm("R", -150, 1.0, 0.3);
      for (let i = 0; i < 6; i++) at("#px-armR", { rotation: i % 2 ? -150 : -125 }, 1.3 + i * 0.22, 0.22, "sine.inOut");
      arm("R", 0, 2.6, 0.25, "power2.inOut");
      at("#px-head", { rotation: 7 }, 1.0, 0.4, "sine.inOut"); at("#px-head", { rotation: 0 }, 2.4, 0.4, "sine.inOut");
      talk(1.05, 2.7);

      // 3. shock: hop, eyes pop, brows fly up
      eyes("shock", 2.8); mouth("oh", 2.8);
      at("#px-browL, #px-browR", { y: -22 }, 2.8, 0.15, "back.out(3)");
      tl.to("#px-root", { y: -110, duration: 0.18, ease: "power2.out" }, 2.8);
      tl.to("#px-root", { y: 0, duration: 0.2, ease: "power2.in" }, 2.98);
      squash(3.18, 0.8);
      arm("L", 55, 2.8, 0.15); arm("R", -55, 2.8, 0.15);
      popFx("#fx-bang", 780, 900, 2.85);
      tl.to("#px-head", { x: -6, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }, 3.3);
      arm("L", 0, 4.0, 0.25, "power2.inOut"); arm("R", 0, 4.0, 0.25, "power2.inOut");
      at("#px-browL, #px-browR", { y: 0 }, 4.0, 0.2); eyes("norm", 4.1); mouth("smile", 4.1);

      // 4. point left at UREA: side-step, arm out, look left
      tl.to("#px-root", { x: -30, duration: 0.35, ease: "power2.inOut" }, 4.2);
      tl.to("#px-legL", { rotation: 12, duration: 0.17, yoyo: true, repeat: 1 }, 4.2);
      tl.to("#px-legR", { rotation: -12, duration: 0.17, yoyo: true, repeat: 1 }, 4.2);
      arm("L", 105, 4.3); finger("L", true, 4.35);
      at("#px-head", { rotation: -9 }, 4.3, 0.3); look(-7, -2, 4.3);
      at("#px-body", { rotation: -4 }, 4.3, 0.3);
      tl.fromTo("#t-urea", { scale: 1 }, { scale: 1.12, duration: 0.2, yoyo: true, repeat: 1, ease: "power1.inOut" }, 4.55);
      talk(4.5, 5.8);

      // 5. point right at KREBS
      arm("L", 0, 5.95, 0.25, "power2.inOut"); finger("L", false, 6.05);
      tl.to("#px-root", { x: 30, duration: 0.4, ease: "power2.inOut" }, 6.0);
      tl.to("#px-legL", { rotation: -12, duration: 0.2, yoyo: true, repeat: 1 }, 6.0);
      tl.to("#px-legR", { rotation: 12, duration: 0.2, yoyo: true, repeat: 1 }, 6.0);
      arm("R", -105, 6.1); finger("R", true, 6.15);
      at("#px-head", { rotation: 9 }, 6.1, 0.3); look(7, -2, 6.1);
      at("#px-body", { rotation: 4 }, 6.1, 0.3);
      tl.fromTo("#t-krebs", { scale: 1 }, { scale: 1.12, duration: 0.2, yoyo: true, repeat: 1, ease: "power1.inOut" }, 6.35);
      talk(6.3, 7.6);

      // 6. thinking: hand to chin, eyes up, one brow raised
      arm("R", 0, 7.75, 0.2, "power2.inOut"); finger("R", false, 7.8);
      tl.to("#px-root", { x: 0, duration: 0.3, ease: "power2.inOut" }, 7.8);
      at("#px-body", { rotation: 0 }, 7.8, 0.3);
      arm("L", -134, 7.95, 0.35); tl.set("#px-chinhand", { opacity: 1 }, 8.2);
      at("#px-head", { rotation: 10 }, 7.95, 0.35); look(4, -8, 7.95);
      at("#px-browR", { y: -16, rotation: -8 }, 7.95, 0.25); at("#px-browL", { y: 4 }, 7.95, 0.25);
      mouth("closed", 7.95);
      popFx("#fx-q", 760, 880, 8.1, 1.1);
      tl.to("#px-chinhand", { y: -6, duration: 0.15, yoyo: true, repeat: 3, ease: "sine.inOut" }, 8.4);

      // 7. celebrate: big jump, arms up, happy eyes, sparkles
      arm("L", 0, 9.3, 0.15); tl.set("#px-chinhand", { opacity: 0 }, 9.3); look(0, 0, 9.3);
      at("#px-browR", { y: 0, rotation: 0 }, 9.3, 0.2); at("#px-browL", { y: 0 }, 9.3, 0.2); at("#px-head", { rotation: 0 }, 9.3, 0.2);
      squash(9.4, 0.6);
      tl.to("#px-root", { y: -240, duration: 0.3, ease: "power2.out" }, 9.5);
      tl.to("#px-root", { y: 0, duration: 0.28, ease: "power2.in" }, 9.8);
      squash(10.08, 1);
      arm("L", 165, 9.5, 0.25); arm("R", -165, 9.5, 0.25);
      eyes("happy", 9.5); mouth("open", 9.5);
      popFx("#fx-spark1", 200, 860, 9.6); popFx("#fx-spark2", 820, 820, 9.75); popFx("#fx-dust", 260, 1690, 10.08, 0.5);
      arm("L", 0, 10.6, 0.3, "power2.inOut"); arm("R", 0, 10.6, 0.3, "power2.inOut");

      // 8. wink + little wave, bounce
      eyes("wink", 11.0); mouth("ee", 11.0);
      arm("R", -140, 11.0, 0.25);
      for (let i = 0; i < 3; i++) at("#px-armR", { rotation: i % 2 ? -140 : -118 }, 11.25 + i * 0.2, 0.2, "sine.inOut");
      at("#px-head", { rotation: -6 }, 11.0, 0.3);
      popFx("#fx-spark1", 790, 860, 11.05, 0.8);

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>`;
fs.writeFileSync(path.join(ROOT, 'index.html'), html);
console.log('index.html written');
