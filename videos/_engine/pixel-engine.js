// Pixel explainer engine v2 — SHARP HD pixel art (the owner's house style since Oct 2026).
// Scenes are written in a 180x320 world coordinate space, but render on a 360x640 pixel
// buffer (RES 2: each art pixel is 3x3 screen pixels at 1080x1920), palette-locked with a
// LIGHT 4x4 Bayer dither (DAMP 6), so shapes stay crisp and gradients don't turn into dots.
// Living characters go through character(fn): an automatic dark outline around their silhouette.
// Captions: a 360x640 canvas (small 5x7 bitmap text centred mid-frame, upscaled 3x).
// Each project defines its palette, scenes, cuts and captions, then calls PX.render(t) from a
// paused GSAP proxy tween. Everything is a pure function of t.
//
// Overrides (set before this script): PX_W/PX_H (world size; landscape), PX_RES (render scale,
// default 2 = sharp; 1 = the old chunky look), PX_DITHER (dither strength, default 6; old = 22).

var W = window.PX_W || 180, H = window.PX_H || 320; // portrait by default; set PX_W/PX_H for landscape
var RES = window.PX_RES || 2, PW = Math.round(W * RES), PH = Math.round(H * RES);
var DAMP = window.PX_DITHER === undefined ? 6 : window.PX_DITHER;
var world = document.getElementById("world");
world.width = PW; world.height = PH;
var wctx = world.getContext("2d");
var buf = document.createElement("canvas");
buf.width = PW; buf.height = PH;
var g = buf.getContext("2d", { willReadFrequently: true });
var ui = document.getElementById("ui");
var u = ui.getContext("2d", { willReadFrequently: true });

// ---------------------------------------------------------------- math
function rng(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function hash1(n) {
  var x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
}
function clamp01(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
function sstep(a, b, x) { var t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); }
function ease(t) { return 0.5 - 0.5 * Math.cos(Math.PI * clamp01(t)); }
function ramp(t, a, b) { return ease((t - a) / (b - a)); }
function easeOut(t) { t = clamp01(t); return 1 - Math.pow(1 - t, 3); }
function lerp(a, b, k) { return a + (b - a) * k; }

// ---------------------------------------------------------------- colour
function hex(h) {
  return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
}
function mix(a, b, t) {
  var x = hex(a), y = hex(b);
  t = clamp01(t);
  return "rgb(" + Math.round(x[0] + (y[0] - x[0]) * t) + "," + Math.round(x[1] + (y[1] - x[1]) * t) + "," + Math.round(x[2] + (y[2] - x[2]) * t) + ")";
}

// ---------------------------------------------------------------- camera
// keys: [time, x, y, zoom]; zoom eases in log space, position follows the zoom
function camAt(keys, t) {
  if (t <= keys[0][0]) return { x: keys[0][1], y: keys[0][2], z: keys[0][3] };
  var L = keys[keys.length - 1];
  if (t >= L[0]) return { x: L[1], y: L[2], z: L[3] };
  var i = 0;
  while (t > keys[i + 1][0]) i++;
  var a = keys[i], b = keys[i + 1];
  var e = ease((t - a[0]) / (b[0] - a[0]));
  var z = Math.exp(Math.log(a[3]) + (Math.log(b[3]) - Math.log(a[3])) * e);
  var k = e;
  if (Math.abs(Math.log(b[3] / a[3])) > 0.1) k = (1 - a[3] / z) / (1 - a[3] / b[3]);
  return { x: a[1] + (b[1] - a[1]) * k, y: a[2] + (b[2] - a[2]) * k, z: z };
}
function shake(cam, t, t0, amp, dur) {
  dur = dur || 0.45;
  var s = 1 - clamp01((t - t0) / dur);
  if (t >= t0 && s > 0) {
    var f = Math.floor(t * 30);
    cam.x += (hash1(f) - 0.5) * amp * s / cam.z;
    cam.y += (hash1(f + 99) - 0.5) * amp * s / cam.z;
  }
  return cam;
}
function setCam(cam, f) {
  f = f === undefined ? 1 : f;
  var z = Math.pow(cam.z, f);
  var cx = W / 2 + (cam.x - W / 2) * f, cy = H / 2 + (cam.y - H / 2) * f;
  g.setTransform(z * RES, 0, 0, z * RES, (W / 2 - cx * z) * RES, (H / 2 - cy * z) * RES);
}
function screen() { g.setTransform(RES, 0, 0, RES, 0, 0); }

// ---------------------------------------------------------------- drawing
function disc(x, y, r, col) {
  g.fillStyle = col; g.beginPath(); g.arc(x, y, Math.max(r, 0.01), 0, 6.2832); g.fill();
}
function ell(x, y, rx, ry, rot, col) {
  g.fillStyle = col; g.beginPath(); g.ellipse(x, y, Math.max(rx, 0.01), Math.max(ry, 0.01), rot, 0, 6.2832); g.fill();
}
function line(x1, y1, x2, y2, w, col) {
  g.strokeStyle = col; g.lineWidth = w; g.lineCap = "round";
  g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke();
}
function rect(x, y, w, h, col) { g.fillStyle = col; g.fillRect(x, y, w, h); }
function rrect(x, y, w, h, r, col) {
  g.fillStyle = col; g.beginPath();
  r = Math.min(r, w / 2, h / 2);
  g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
  g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); g.fill();
}
function poly(pts, col) {
  g.fillStyle = col; g.beginPath(); g.moveTo(pts[0][0], pts[0][1]);
  for (var i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]);
  g.closePath(); g.fill();
}
function vgrad(y0, y1, stops) {
  var gr = g.createLinearGradient(0, y0, 0, y1);
  stops.forEach(function (s) { gr.addColorStop(s[0], s[1]); });
  return gr;
}
function vignette(alpha, tint) {
  screen();
  var vg = g.createRadialGradient(W / 2, H / 2, H * 0.32, W / 2, H / 2, H * 0.7);
  vg.addColorStop(0, "rgba(0,0,0,0)");
  vg.addColorStop(1, (tint || "rgba(40,10,30,") + alpha + ")");
  g.fillStyle = vg; g.fillRect(0, 0, W, H);
}
// in-world pixel text (5x7 glyphs, 1 world px per dot at scale 1)
function worldText(str, cx, y, s, col) {
  var w = str.length * 6 * s - s, x = Math.round(cx - w / 2);
  y = Math.round(y);
  g.fillStyle = col;
  for (var i = 0; i < str.length; i++) {
    var gl = FONT[str[i]] || FONT[" "];
    for (var p = 0; p < 35; p++) if (gl[p] === "1") g.fillRect(x + i * 6 * s + (p % 5) * s, y + Math.floor(p / 5) * s, s, s);
  }
}

// ---------------------------------------------------------------- palette lock
var BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
var PAL = [];
var QCACHE = new Int16Array(64 * 64 * 64);
function setPalette(C) {
  PAL = Object.keys(C).map(function (k) { return hex(C[k]); });
  QCACHE.fill(-1);
}
function nearest(r, gg, b) {
  var best = 0, bd = 1e12;
  for (var i = 0; i < PAL.length; i++) {
    var p = PAL[i], dr = r - p[0], dg = gg - p[1], db = b - p[2];
    var d = 2 * dr * dr + 4 * dg * dg + 3 * db * db;
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}
function quantize(img) {
  var d = img.data;
  for (var y = 0; y < PH; y++) {
    for (var x = 0; x < PW; x++) {
      var i = (y * PW + x) * 4;
      var off = (BAYER[(y & 3) * 4 + (x & 3)] / 16 - 0.47) * DAMP;
      var r = d[i] + off, gg = d[i + 1] + off, b = d[i + 2] + off;
      r = r < 0 ? 0 : r > 255 ? 255 : r; gg = gg < 0 ? 0 : gg > 255 ? 255 : gg; b = b < 0 ? 0 : b > 255 ? 255 : b;
      var key = ((r >> 2) << 12) | ((gg >> 2) << 6) | (b >> 2);
      var q = QCACHE[key];
      if (q < 0) { q = nearest(r, gg, b); QCACHE[key] = q; }
      var p = PAL[q];
      d[i] = p[0]; d[i + 1] = p[1]; d[i + 2] = p[2]; d[i + 3] = 255;
    }
  }
  wctx.putImageData(img, 0, 0);
}

// ---------------------------------------------------------------- captions
var FONT = {
  A: "01110100011000111111100011000110001", B: "11110100011000111110100011000111110", C: "01110100011000010000100001000101110",
  D: "11110100011000110001100011000111110", E: "11111100001000011110100001000011111", F: "11111100001000011110100001000010000",
  G: "01110100011000010111100011000101111", H: "10001100011000111111100011000110001", I: "01110001000010000100001000010001110",
  J: "00111000100001000010000101001001100", K: "10001100101010011000101001001010001", L: "10000100001000010000100001000011111",
  M: "10001110111010110101100011000110001", N: "10001100011100110101100111000110001", O: "01110100011000110001100011000101110",
  P: "11110100011000111110100001000010000", Q: "01110100011000110001101011001001101", R: "11110100011000111110101001001010001",
  S: "01111100001000001110000010000111110", T: "11111001000010000100001000010000100", U: "10001100011000110001100011000101110",
  V: "10001100011000110001100010101000100", W: "10001100011000110101101011010101010", X: "10001100010101000100010101000110001",
  Y: "10001100010101000100001000010000100", Z: "11111000010001000100010001000011111",
  "0": "01110100011001110101110011000101110", "1": "00100011000010000100001000010001110", "2": "01110100010000100010001000100011111",
  "3": "11111000100010000010000011000101110", "4": "00010001100101010010111110001000010", "5": "11111100001111000001000011000101110",
  "6": "00110010001000011110100011000101110", "7": "11111000010001000100010000100001000", "8": "01110100011000101110100011000101110",
  "9": "01110100011000101111000010001001100",
  "?": "01110100010000100010001000000000100", ".": "00000000000000000000000000110001100", ",": "00000000000000000000011000010001000",
  "'": "00100001000100000000000000000000000", "!": "00100001000010000100001000000000100", ":": "00000011000110000000011000110000000",
  "-": "00000000000000011111000000000000000", "%": "11001110010001000100010001001110011", "/": "00001000010001000100010001000010000",
  "+": "00000001000010011111001000010000000", "=": "00000000001111100000111110000000000", "~": "00000000000100010101000100000000000",
  "$": "00100011111010001110001011111000100", "#": "01010010101111101010111110101001010", "[": "01110010000100001000010000100001110", "]": "01110000100001000010000100001001110", "(": "00010001000100001000010000010000010", ")": "01000001000001000010000100010001000",
  " ": "00000000000000000000000000000000000",
};
var CAPTIONS = [];
var DISSOLVE = 0.4, CAP_S = 2;
function lineText(l) { return l.map(function (s) { return s[0]; }).join(""); }
function drawCaption(cap, t) {
  var S = CAP_S, padX = 5, padY = 4, gap = 4;
  var widths = cap.lines.map(function (l) { return lineText(l).length * 6 * S - S; });
  var w = Math.max.apply(null, widths) + padX * 2;
  var h = padY * 2 + cap.lines.length * (7 * S + gap) - gap;
  var x0 = Math.round(180 - w / 2), top = Math.round((cap.y || 320) - h / 2);
  u.fillStyle = "rgba(6,5,10,0.9)";
  u.fillRect(x0, top, w, h);
  var y = top + padY;
  cap.lines.forEach(function (l, li) {
    var cx = Math.round(180 - widths[li] / 2);
    l.forEach(function (seg) {
      u.fillStyle = seg[1];
      for (var ci = 0; ci < seg[0].length; ci++) {
        var gl = FONT[seg[0][ci]] || FONT[" "];
        for (var p = 0; p < 35; p++) if (gl[p] === "1") u.fillRect(cx + (p % 5) * S, y + Math.floor(p / 5) * S, S, S);
        cx += 6 * S;
      }
    });
    y += 7 * S + gap;
  });
  // pop on; dither-dissolve out
  var p = clamp01((t - (cap.b - DISSOLVE)) / DISSOLVE);
  if (p > 0) {
    var img = u.getImageData(x0, top, w, h), d = img.data;
    for (var yy = 0; yy < h; yy++) for (var xx = 0; xx < w; xx++) {
      var k = (yy * w + xx) * 4;
      var th = BAYER[(((top + yy) >> 1) & 3) * 4 + (((x0 + xx) >> 1) & 3)] / 16;
      if (th < p * 1.15) d[k + 3] = 0;
      else d[k + 3] = d[k + 3] * (1 - p * 0.5);
    }
    u.putImageData(img, x0, top);
  }
}

// ---------------------------------------------------------------- frame
// cfg: { scenes: {name: fn(t)}, sceneAt: fn(t) -> name, cuts: [[time, from, to]], captions: [...] }
var PX = { cfg: null, RES: RES, W: W, H: H };
PX.setup = function (C, cfg) {
  setPalette(C);
  PX.cfg = cfg;
  CAPTIONS = cfg.captions || [];
};
PX.scene = function (name, t) {
  // a fresh context per scene: a draw call that throws mid-clip can't leak its clip/transform into later frames
  if (g.reset) g.reset();
  g.globalAlpha = 1;
  g.globalCompositeOperation = "source-over";
  g.setTransform(RES, 0, 0, RES, 0, 0);
  PX.cfg.scenes[name](t);
  g.globalAlpha = 1;
  g.globalCompositeOperation = "source-over";
  return g.getImageData(0, 0, PW, PH);
};
PX.render = function (t) {
  var cfg = PX.cfg, img = null;
  for (var i = 0; i < cfg.cuts.length; i++) {
    var c = cfg.cuts[i];
    if (Math.abs(t - c[0]) < 0.15) {
      var p = (t - (c[0] - 0.15)) / 0.3;
      var A = PX.scene(c[1], t), B = PX.scene(c[2], t), a = A.data, b = B.data;
      for (var y = 0; y < PH; y++) for (var x = 0; x < PW; x++) {
        if (BAYER[(y & 3) * 4 + (x & 3)] / 16 < p) {
          var k = (y * PW + x) * 4;
          a[k] = b[k]; a[k + 1] = b[k + 1]; a[k + 2] = b[k + 2];
        }
      }
      img = A;
    }
  }
  if (!img) img = PX.scene(cfg.sceneAt(t), t);
  if (cfg.post) cfg.post(t, img);
  quantize(img);
  u.clearRect(0, 0, ui.width, ui.height);
  CAPTIONS.forEach(function (c) { if (t >= c.a && t < c.b) drawCaption(c, t); });
  if (cfg.ui) cfg.ui(t);
};

// ---------------------------------------------------------------- post effects (operate on ImageData)
// VHS-style rewind tear: rows slide sideways in bands, with bright scan lines
function glitchRows(img, amount, seed) {
  var d = img.data, row = new Uint8ClampedArray(PW * 4);
  for (var y = 0; y < PH; y++) {
    var band = Math.floor(y / (6 * RES));
    var off = Math.round((hash1(band * 7.3 + seed) - 0.5) * 2 * amount * RES);
    if (off === 0) continue;
    var base = y * PW * 4;
    for (var x = 0; x < PW; x++) {
      var sx = ((x - off) % PW + PW) % PW;
      row[x * 4] = d[base + sx * 4]; row[x * 4 + 1] = d[base + sx * 4 + 1]; row[x * 4 + 2] = d[base + sx * 4 + 2];
    }
    for (var x2 = 0; x2 < PW; x2++) { d[base + x2 * 4] = row[x2 * 4]; d[base + x2 * 4 + 1] = row[x2 * 4 + 1]; d[base + x2 * 4 + 2] = row[x2 * 4 + 2]; }
    if (hash1(band + seed * 3.1) > 0.82) for (var x3 = 0; x3 < PW; x3++) { d[base + x3 * 4] = 255; d[base + x3 * 4 + 1] = 255; d[base + x3 * 4 + 2] = 255; }
  }
}
// blend the whole frame toward a colour (flash / fade)
function tintImg(img, hexCol, k) {
  if (k <= 0) return;
  var c = hex(hexCol), d = img.data;
  for (var i = 0; i < d.length; i += 4) {
    d[i] += (c[0] - d[i]) * k; d[i + 1] += (c[1] - d[i + 1]) * k; d[i + 2] += (c[2] - d[i + 2]) * k;
  }
}

// ---------------------------------------------------------------- light helpers
function glow(x, y, r, col, a) {
  var c = hex(col);
  var gr = g.createRadialGradient(x, y, 0, x, y, Math.max(r, 0.1));
  gr.addColorStop(0, "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")");
  gr.addColorStop(1, "rgba(" + c[0] + "," + c[1] + "," + c[2] + ",0)");
  g.fillStyle = gr; g.beginPath(); g.arc(x, y, Math.max(r, 0.1), 0, 6.2832); g.fill();
}
function lighter() { g.globalCompositeOperation = "lighter"; }
function normalBlend() { g.globalCompositeOperation = "source-over"; }

// ---------------------------------------------------------------- living characters: automatic dark outline
// House rule: EVERY person, animal or creature has a dark outline. Draw it inside character(fn):
//   character(function () { cat(90, 250, 1.2, { t: t }); });
// The shape is rendered off-screen with the current camera, a 1-render-pixel (3 screen px) dark
// outline is stamped around its silhouette, then the shape goes on top. Transparency is kept
// (a ghost gets a ghostly outline). opts: { col: outline colour (default OUTLINE), px: thickness }.
var OUTLINE = window.PX_OUTLINE || "#0a0614";
var cbuf = document.createElement("canvas"); cbuf.width = PW; cbuf.height = PH;
var cg = cbuf.getContext("2d");
var obuf = document.createElement("canvas"); obuf.width = PW; obuf.height = PH;
var og = obuf.getContext("2d");
function character(drawFn, opts) {
  opts = opts || {};
  var m = g.getTransform(), alpha = g.globalAlpha, main = g;
  cg.setTransform(1, 0, 0, 1, 0, 0); cg.globalAlpha = 1; cg.globalCompositeOperation = "source-over"; cg.clearRect(0, 0, PW, PH);
  cg.setTransform(m);
  g = cg;
  try { drawFn(); } finally { g = main; cg.globalAlpha = 1; cg.globalCompositeOperation = "source-over"; }
  og.setTransform(1, 0, 0, 1, 0, 0); og.globalCompositeOperation = "source-over"; og.clearRect(0, 0, PW, PH);
  og.drawImage(cbuf, 0, 0);
  og.globalCompositeOperation = "source-in"; og.fillStyle = opts.col || OUTLINE; og.fillRect(0, 0, PW, PH);
  og.globalCompositeOperation = "source-over";
  var r = opts.px || 1;
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = alpha; g.globalCompositeOperation = "source-over";
  for (var dy = -r; dy <= r; dy++) for (var dx = -r; dx <= r; dx++) if ((dx || dy) && dx * dx + dy * dy <= r * r + 0.5) g.drawImage(obuf, dx, dy);
  g.drawImage(cbuf, 0, 0);
  g.restore();
}
