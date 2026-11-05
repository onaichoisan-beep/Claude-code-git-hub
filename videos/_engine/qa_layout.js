// qa_layout.js — measures every frame of a pixel short for text covering the subject (STYLE_GUIDE.md section 8).
//   node videos/_engine/qa_layout.js videos/<slug> [step=0.1]
// Wraps character() / bubble() / drawCaption() in the page, renders t = 0 .. REWIND, and reports any frame where
//   - a caption box covers > 4% of a living character's pixels (or > 60 px of it)
//   - a speech bubble covers a character (> 25 px), another bubble, the caption, the counter band, or leaves the safe box
//   - a character sits in the counter band (canvas y < 112)
// Coordinates are caption-canvas px (360x640; x3 = 1080x1920).
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const dir = path.resolve(process.argv[2]);
  const step = parseFloat(process.argv[3] || "0.1");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("pageerror", (e) => console.log("PAGE ERROR", e.message));
  await page.goto("file://" + path.join(dir, "index.html"));
  await page.waitForFunction(() => window.PX && PX.cfg, null, { timeout: 30000 });
  const out = await page.evaluate((step) => {
    var F = { chars: [], bubbles: [], caps: [] };
    var origChar = window.character;
    window.character = function (fn, o) {
      origChar(fn, o);
      var d = cbuf.getContext("2d").getImageData(0, 0, PW, PH).data, xs = [];
      var n = 0, x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
      var mask = new Uint8Array(PW * PH);
      for (var i = 0, p = 0; i < d.length; i += 4, p++) if (d[i + 3] > 128) { mask[p] = 1; n++; var x = p % PW, y = (p / PW) | 0; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (n > 30) F.chars.push({ n: n, box: [x0, y0, x1, y1], mask: mask });
    };
    var origBubble = window.bubble;
    window.bubble = function (x, y, str, col) {
      var w = str.length * 6 + 5, m = g.getTransform();
      var a = m.transformPoint(new DOMPoint(x - w / 2, y - 6)), b = m.transformPoint(new DOMPoint(x + w / 2, y + 10));
      F.bubbles.push({ s: str, box: [Math.min(a.x, b.x), Math.min(a.y, b.y), Math.max(a.x, b.x), Math.max(a.y, b.y)] });
      origBubble(x, y, str, col);
    };
    var origCap = window.drawCaption;
    window.drawCaption = function (cap, t) {
      var S = 2, widths = cap.lines.map(function (l) { return lineText(l).length * 6 * S - S; });
      var w = Math.max.apply(null, widths) + 10, h = 8 + cap.lines.length * 18 - 4;
      var x0 = Math.round(180 - w / 2), top = Math.round((cap.y || 320) - h / 2);
      F.caps.push({ s: cap.lines.map(lineText).join(" / "), box: [x0, top, x0 + w, top + h] });
      origCap(cap, t);
    };
    function inter(a, b) { return Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0])) * Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1])); }
    function covered(c, box) { var n = 0; for (var y = Math.max(0, box[1] | 0); y < Math.min(PH, box[3]); y++) for (var x = Math.max(0, box[0] | 0); x < Math.min(PW, box[2]); x++) if (c.mask[y * PW + x]) n++; return n; }
    var T = window.BEATS, end = T.REWIND || window.DUR, issues = [];
    var COUNTER = [40, 60, 320, 112];
    for (var t = 0.05; t < end - 0.05; t += step) {
      F = { chars: [], bubbles: [], caps: [] };
      PX.render(t);
      var tt = t.toFixed(2);
      F.chars.forEach(function (c, ci) {
        F.caps.forEach(function (cp) { var k = covered(c, cp.box); if (k > 60 || k / c.n > 0.04) issues.push([tt, "CAPTION covers character#" + ci + " (" + k + " px, " + Math.round(100 * k / c.n) + "%) '" + cp.s + "'"]); });
        var kc = covered(c, COUNTER); if (kc > 40) issues.push([tt, "character#" + ci + " in the COUNTER band (" + kc + " px)"]);
      });
      F.bubbles.forEach(function (b, bi) {
        F.chars.forEach(function (c, ci) { var k = covered(c, b.box); if (k > 25) issues.push([tt, "BUBBLE '" + b.s + "' covers character#" + ci + " (" + k + " px)"]); });
        F.caps.forEach(function (cp) { if (inter(b.box, cp.box) > 0) issues.push([tt, "BUBBLE '" + b.s + "' overlaps caption"]); });
        if (inter(b.box, COUNTER) > 0) issues.push([tt, "BUBBLE '" + b.s + "' overlaps the counter band"]);
        if (b.box[0] < 34 || b.box[2] > 290 || b.box[1] < 60 || b.box[3] > 452) issues.push([tt, "BUBBLE '" + b.s + "' leaves the safe box " + b.box.map(Math.round)]);
        F.bubbles.forEach(function (b2, bj) { if (bj > bi && b2.s !== b.s && inter(b.box, b2.box) > 0) issues.push([tt, "BUBBLE '" + b.s + "' overlaps bubble '" + b2.s + "'"]); });
      });
    }
    return issues;
  }, step);
  // collapse runs of the same message
  const runs = [];
  for (const [t, m] of out) { const r = runs.find((r) => r.m.replace(/\(.*?\)/, "") === m.replace(/\(.*?\)/, "") && Math.abs(parseFloat(t) - r.t1) < step * 1.6); if (r) { r.t1 = parseFloat(t); r.m = m; } else runs.push({ t0: parseFloat(t), t1: parseFloat(t), m }); }
  for (const r of runs) console.log(`${r.t0.toFixed(2)}-${r.t1.toFixed(2)}s  ${r.m}`);
  console.log(runs.length ? `${runs.length} layout problem(s)` : "layout OK: no text covers a character");
  await browser.close();
})();
