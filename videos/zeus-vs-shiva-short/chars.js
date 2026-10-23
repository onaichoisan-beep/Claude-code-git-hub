// Zeus vs Shiva — palette, effect helpers and the two character rigs.
// World canvas is 320x180 (landscape), upscaled 6x to 1920x1080. Everything is a pure function of t.

var C = {
  ink: "#05040c", void: "#0c0820", space1: "#1a1040", space2: "#2c1a66", nebula: "#5a2a9a", nebula2: "#8a3ac0",
  nebPink: "#d050c0", nebHot: "#ff7ad8", white: "#ffffff", paleBlue: "#cfe8ff",
  cyanDeep: "#0a5a8a", cyan: "#1ac8ff", cyanL: "#8af0ff", cyanW: "#d8fcff",
  violetD: "#3a1a8a", violet: "#8a4aff", violetL: "#c8a0ff",
  goldD: "#a86a10", gold: "#ffc020", goldL: "#ffe870", goldW: "#fff8c8",
  eBlueD: "#1a3ad0", eBlue: "#3a8aff", eBlueL: "#a0d0ff",
  marbleD: "#6a6a8a", marbleM: "#a8a8c8", marble: "#dcdcf0", marbleW: "#f6f4ff", rockD: "#3a2a4a", rock: "#5a4a6a",
  stormD: "#2a2a4a", storm: "#4a4a70", stormL: "#7a7aa0", cloudGold: "#e8a040", amber: "#c86a20",
  skyN: "#1a2a6a", snow: "#e8f0ff", snowShade: "#8aa0d0", mountain: "#3a4a8a", mountainD: "#222a5a",
  oceanD: "#08245a", ocean: "#0a5aaa", oceanL: "#2a9ae0", foam: "#e0f8ff",
  zSkin: "#eaa878", zSkinD: "#b06a48", zHair: "#f4f4f4", zHairShade: "#b0b4cc", ivory: "#fff2d8", ivoryShade: "#d4c09c",
  cape: "#d0243a", capeD: "#801428",
  sSkin: "#3a7ae0", sSkinL: "#78b4ff", sSkinD: "#1a44a0", jata: "#2a1630", jataL: "#4e2c58", tiger: "#f08a1a", tigerD: "#5a2a0a",
  ash: "#f0f0f4", moon: "#f8f4d0", snake: "#3ab05a", snakeD: "#1a6a30", beads: "#8a3a1a", tilak: "#e8203a",
  flash: "#fffbe8", portal: "#f0d8ff", portalV: "#b070ff", shadow: "#0a0414",
};

// ------------------------------------------------------------------ small helpers
function A(a) { return [Math.sin(a), Math.cos(a)]; } // angle convention: 0 = down, PI/2 = forward, PI = up
function pulse(u, a, b) { return ramp(u, a, a + (b - a) * 0.3) * (1 - ramp(u, a + (b - a) * 0.3, b)); }
function at(u, t0) { return u >= t0; }
function ringS(x, y, r, w, col, a) {
  if (r <= 0) return;
  g.globalAlpha = clamp01(a === undefined ? 1 : a);
  g.strokeStyle = col; g.lineWidth = w; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.stroke();
  g.globalAlpha = 1;
}
function ellS(x, y, rx, ry, rot, w, col, a) {
  g.globalAlpha = clamp01(a === undefined ? 1 : a);
  g.strokeStyle = col; g.lineWidth = w; g.beginPath(); g.ellipse(x, y, Math.max(rx, 0.1), Math.max(ry, 0.1), rot, 0, 6.2832); g.stroke();
  g.globalAlpha = 1;
}
function arcS(x, y, r, a0, a1, w, col, a) {
  g.globalAlpha = clamp01(a === undefined ? 1 : a);
  g.strokeStyle = col; g.lineWidth = w; g.lineCap = "round"; g.beginPath(); g.arc(x, y, Math.max(r, 0.1), a0, a1); g.stroke();
  g.globalAlpha = 1;
}
function fillAll(col) { screen(); g.fillStyle = col; g.fillRect(0, 0, W, H); }
function alpha(a, fn) { g.globalAlpha = clamp01(a); fn(); g.globalAlpha = 1; }
function frameNo(t) { return Math.floor(t * 30); }

// ------------------------------------------------------------------ lightning
// jagged bolt between two points; re-jitters 15x a second so it crackles
function boltPts(x1, y1, x2, y2, seed, rough, t) {
  var r = rng(seed * 977 + Math.floor((t || 0) * 15) * 13 + 1);
  var pts = [[x1, y1], [x2, y2]];
  var dx = x2 - x1, dy = y2 - y1, len = Math.sqrt(dx * dx + dy * dy) + 0.001;
  var off = len * (rough || 0.22);
  for (var it = 0; it < 4; it++) {
    var np = [pts[0]];
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1];
      var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
      var o = (r() - 0.5) * off;
      np.push([mx - dy / len * o, my + dx / len * o], b);
    }
    pts = np; off *= 0.5;
  }
  return pts;
}
function strokePts(pts, w, col) {
  g.strokeStyle = col; g.lineWidth = w; g.lineCap = "round"; g.lineJoin = "round";
  g.beginPath(); g.moveTo(pts[0][0], pts[0][1]);
  for (var i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]);
  g.stroke();
}
// a full lightning bolt: glow + blue body + white core (+ optional branches)
function lightning(x1, y1, x2, y2, seed, t, w, opts) {
  opts = opts || {};
  w = w || 1.6;
  var pts = boltPts(x1, y1, x2, y2, seed, opts.rough, t);
  lighter();
  glow((x1 + x2) / 2, (y1 + y2) / 2, Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) * 0.5 + 8, opts.glowCol || C.eBlue, opts.glowA || 0.35);
  normalBlend();
  strokePts(pts, w * 2.6, opts.body || C.eBlue);
  strokePts(pts, w * 1.3, opts.mid || C.eBlueL);
  strokePts(pts, Math.max(0.6, w * 0.6), C.white);
  if (opts.branches) {
    var r = rng(seed * 31 + Math.floor((t || 0) * 15));
    for (var b = 0; b < opts.branches; b++) {
      var p = pts[2 + Math.floor(r() * (pts.length - 4))];
      var ang = Math.atan2(y2 - y1, x2 - x1) + (r() - 0.5) * 2;
      var L = 6 + r() * 14;
      var bp = boltPts(p[0], p[1], p[0] + Math.cos(ang) * L, p[1] + Math.sin(ang) * L, seed + b * 7, 0.4, t);
      strokePts(bp, w * 1.2, C.eBlue); strokePts(bp, 0.6, C.eBlueL);
    }
  }
}
// little crackling arcs around a point (Zeus's charge)
function crackle(x, y, r, n, seed, t, col) {
  var rr = rng(seed + Math.floor(t * 15) * 7);
  for (var i = 0; i < n; i++) {
    var a = rr() * 6.2832, a2 = a + (rr() - 0.5) * 1.6;
    var r1 = r * (0.3 + rr() * 0.5), r2 = r * (0.8 + rr() * 0.6);
    var pts = boltPts(x + Math.cos(a) * r1, y + Math.sin(a) * r1, x + Math.cos(a2) * r2, y + Math.sin(a2) * r2, seed + i, 0.5, t);
    strokePts(pts, 1.1, col || C.eBlue); strokePts(pts, 0.5, C.white);
  }
}

// ------------------------------------------------------------------ particles
// burst of square pixels flying out from (x,y); k = time since burst
function burst(x, y, k, n, seed, speed, cols, grav, life) {
  if (k < 0) return;
  life = life || 1.4;
  if (k > life) return;
  var r = rng(seed);
  for (var i = 0; i < n; i++) {
    var a = r() * 6.2832, v = speed * (0.3 + r() * 0.9), sz = 0.8 + r() * 1.8;
    var px = x + Math.cos(a) * v * k, py = y + Math.sin(a) * v * k + (grav || 0) * k * k;
    var fade = 1 - k / life;
    if (r() > fade + 0.1) continue;
    rect(px - sz / 2, py - sz / 2, sz, sz, cols[i % cols.length]);
  }
}
// floating dust / embers that drift (deterministic)
function motes(seed, n, x0, y0, w, h, t, cols, vx, vy, size) {
  var r = rng(seed);
  for (var i = 0; i < n; i++) {
    var bx = r() * w, by = r() * h, sp = 0.5 + r(), sz = (size || 1) * (0.6 + r() * 0.9), c = cols[i % cols.length];
    var x = x0 + ((bx + (vx || 0) * t * sp) % w + w) % w, y = y0 + ((by + (vy || 0) * t * sp) % h + h) % h;
    var tw = 0.6 + 0.4 * Math.sin(t * 3 + i);
    if (tw > 0.35) rect(x, y, sz, sz, c);
  }
}
function shockRing(x, y, k, maxR, col, w, ry) {
  if (k < 0 || k > 1) return;
  var r = maxR * easeOut(k);
  g.globalAlpha = 1 - k;
  g.strokeStyle = col; g.lineWidth = (w || 3) * (1 - k * 0.6);
  g.beginPath(); g.ellipse(x, y, Math.max(r, 0.1), Math.max(r * (ry || 1), 0.1), 0, 0, 6.2832); g.stroke();
  g.globalAlpha = 1;
}

// ------------------------------------------------------------------ weapons
var BOLT_SHAPE = [[-9, 0], [-3, -2.6], [-1.2, 0.6], [5, -2.4], [6.6, 1.2], [13, -1.4], [21, 0], [12, 2.8], [9.6, -0.2], [4, 3.2], [0.8, 0.2], [-4, 2.8]];
// Zeus's thunderbolt, gripped at (x,y), pointing along angle a (A() convention)
function thunderbolt(x, y, a, sc, charge, t) {
  var d = A(a), nx = d[1], ny = -d[0];
  function P(p) { return [x + (d[0] * p[0] + nx * p[1]) * sc, y + (d[1] * p[0] + ny * p[1]) * sc]; }
  lighter();
  glow(x + d[0] * 6 * sc, y + d[1] * 6 * sc, (12 + 18 * charge) * sc, C.eBlue, 0.35 + 0.4 * charge);
  if (charge > 0.2) glow(x + d[0] * 6 * sc, y + d[1] * 6 * sc, (6 + 10 * charge) * sc, C.gold, 0.5 * charge);
  normalBlend();
  poly(BOLT_SHAPE.map(P), C.goldD);
  poly(BOLT_SHAPE.map(function (p) { return P([p[0] * 0.92, p[1] * 0.7]); }), C.gold);
  poly(BOLT_SHAPE.map(function (p) { return P([p[0] * 0.8, p[1] * 0.32]); }), charge > 0.4 ? C.white : C.goldW);
  if (charge > 0.05) crackle(x + d[0] * 6 * sc, y + d[1] * 6 * sc, (8 + 10 * charge) * sc, 2 + Math.round(4 * charge), 41, t, C.eBlue);
}
// Shiva's trishul gripped at (x,y), shaft along angle a; glow 0..1
function trishul(x, y, a, sc, glowK, t, grip) {
  var d = A(a), nx = d[1], ny = -d[0];
  grip = grip === undefined ? 22 : grip; // shaft length below the hand
  function P(u, v) { return [x + (d[0] * u + nx * v) * sc, y + (d[1] * u + ny * v) * sc]; }
  var b0 = P(-grip, 0), top = P(44, 0);
  if (glowK > 0) {
    lighter();
    var hp = P(48, 0);
    glow(hp[0], hp[1], (10 + 16 * glowK) * sc, C.cyan, 0.3 + 0.5 * glowK);
    if (glowK > 0.5) glow(hp[0], hp[1], 8 * sc, C.violet, 0.4 * glowK);
    normalBlend();
  }
  line(b0[0], b0[1], top[0], top[1], 2.0 * sc, C.goldD);
  line(b0[0], b0[1], top[0], top[1], 0.9 * sc, C.gold);
  // damaru (small drum) with ribbon, tied just below the head
  var dm = P(38, 0);
  var dA = P(36, -3), dB = P(36, 3), dC = P(40, -3), dD = P(40, 3);
  poly([dA, dB, dm], C.beads); poly([dC, dD, dm], C.beads);
  var rb = P(37, 4 + Math.sin(t * 5) * 1.5), rb2 = P(33, 7 + Math.sin(t * 5 + 1) * 2);
  line(dm[0], dm[1], rb[0], rb[1], 0.8 * sc, C.tilak); line(rb[0], rb[1], rb2[0], rb2[1], 0.8 * sc, C.tilak);
  // crossbar + three prongs
  var prong = glowK > 0.3 ? C.cyanW : C.marbleW, prongD = glowK > 0.3 ? C.cyanL : C.marbleM;
  var c1 = P(44, -6), c2 = P(44, 6);
  line(c1[0], c1[1], c2[0], c2[1], 1.6 * sc, prongD);
  poly([P(44, -1.2), P(44, 1.2), P(56, 0)], prong);
  poly([P(44, -6), P(44, -3.8), P(49, -5.6), P(54, -7.6), P(50, -7.6)], prong);
  poly([P(44, 6), P(44, 3.8), P(49, 5.6), P(54, 7.6), P(50, 7.6)], prong);
  return { tip: P(56, 0), base: b0 };
}

// ------------------------------------------------------------------ ZEUS
// p: aF,bF (front/right arm angle + elbow bend), aB,bB (back arm), bolt (bolt angle, absolute A() convention),
//    boltOn, charge, legs ('stand'|'wide'|'fly'|'crouch'|'brace'), lean, wind, eyeGlow, look (head tilt), breathe
var ZPOSE = {
  stand: { aF: 0.5, bF: 0.9, aB: -0.25, bB: 0.2, bolt: 2.3, legs: "stand" },
  ready: { aF: 1.1, bF: 0.6, aB: -0.5, bB: 0.4, bolt: 2.1, legs: "wide" },
  windup: { aF: -1.9, bF: -0.6, aB: 0.9, bB: 0.6, bolt: -2.2, legs: "brace", lean: -0.12 },
  throw: { aF: 1.75, bF: 0.15, aB: -0.8, bB: 0.3, bolt: 1.7, legs: "brace", lean: 0.2 },
  raise: { aF: 2.9, bF: 0.1, aB: -0.5, bB: 0.6, bolt: 3.1, legs: "wide" },
  arms: { aF: 2.3, bF: 0.2, aB: -2.3, bB: -0.2, bolt: 2.6, legs: "wide" },
  fly: { aF: 1.7, bF: 0.2, aB: -0.9, bB: 0.3, bolt: 1.6, legs: "fly", lean: 0.9 },
  dive: { aF: 2.7, bF: 0.3, aB: -0.6, bB: 0.4, bolt: 2.9, legs: "fly", lean: 0.7 },
  swing: { aF: 1.2, bF: 0.3, aB: -0.7, bB: 0.3, bolt: 1.0, legs: "brace", lean: 0.35 },
  low: { aF: 0.4, bF: 0.5, aB: -0.3, bB: 0.3, bolt: 1.2, legs: "wide" },
  brace: { aF: 0.9, bF: 0.9, aB: 0.6, bB: 0.8, bolt: 2.4, legs: "brace", lean: -0.1 },
  hover: { aF: 0.9, bF: 0.8, aB: -0.4, bB: 0.4, bolt: 2.0, legs: "fly", lean: 0.15 },
  thrust: { aF: 1.6, bF: 0.0, aB: -1.0, bB: 0.2, bolt: 1.57, legs: "brace", lean: 0.25 },
};
function poseMix(P, a, b, k) {
  var A_ = P[a], B_ = P[b], o = {};
  k = clamp01(k);
  Object.keys(A_).forEach(function (key) {
    if (typeof A_[key] === "number") o[key] = A_[key] + ((B_[key] === undefined ? 0 : B_[key]) - A_[key]) * k;
    else o[key] = k < 0.5 ? A_[key] : B_[key];
  });
  Object.keys(B_).forEach(function (key) { if (o[key] === undefined) o[key] = typeof B_[key] === "number" ? B_[key] * k : B_[key]; });
  return o;
}
function pose(P, name, extra) {
  var o = {}, b = P[name];
  Object.keys(b).forEach(function (k) { o[k] = b[k]; });
  if (extra) Object.keys(extra).forEach(function (k) { o[k] = extra[k]; });
  return o;
}
function arm(sx, sy, a, b, l1, l2, w, col, colD) {
  var e = A(a), ex = sx + e[0] * l1, ey = sy + e[1] * l1;
  var h = A(a + b), hx = ex + h[0] * l2, hy = ey + h[1] * l2;
  line(sx, sy, ex, ey, w + 1, colD); line(ex, ey, hx, hy, w + 0.6, colD);
  line(sx, sy, ex, ey, w, col); line(ex, ey, hx, hy, w * 0.9, col);
  return [ex, ey, hx, hy];
}
var ZLEGS = {
  stand: [[-2, -12, -4, 0], [3, -12, 5, 0]],
  wide: [[-5, -12, -9, 0], [5, -12, 9, 0]],
  brace: [[-6, -11, -12, 0], [6, -13, 7, 0]],
  crouch: [[-6, -8, -9, 0], [7, -9, 6, 0]],
  fly: [[-7, -14, -15, -8], [-3, -15, -10, -3]],
};
function zeus(x, y, s, dir, p, t) {
  p = p || ZPOSE.stand;
  var wind = p.wind === undefined ? 0.4 : p.wind;
  var hipY = p.legs === "crouch" ? -20 : -24;
  var br = (p.breathe || 0) * Math.sin(t * 7) * 0.8;
  g.save();
  g.translate(x, y); g.scale(dir * s, s); g.rotate(p.lean || 0);
  // cape
  var fl = Math.sin(t * 9) * 1.5 * (0.4 + wind), fl2 = Math.sin(t * 11 + 1) * 1.5 * (0.4 + wind);
  var cbx = -9 - 16 * wind, cby = -4 - 12 * wind;
  poly([[-5, -46 + br], [3, -45 + br], [-2, -26], [cbx + 4, cby + 2 + fl], [cbx - 2, cby - 4 + fl2], [cbx - 6 + fl, cby - 12], [-8 - 6 * wind, -38]], C.capeD);
  poly([[-4, -45 + br], [2, -44 + br], [-3, -28], [cbx + 4, cby + fl], [cbx - 1, cby - 6 + fl2], [-7 - 5 * wind, -38]], C.cape);
  // back arm
  arm(-4, -43 + br, p.aB, p.bB, 9, 9, 3.2, C.zSkinD, C.capeD);
  // legs
  var L = ZLEGS[p.legs] || ZLEGS.stand;
  L.forEach(function (lg, i) {
    var hx = i === 0 ? -2 : 2;
    line(hx, hipY, lg[0], lg[1] + (hipY + 24), 4.4, C.zSkinD); line(lg[0], lg[1] + (hipY + 24), lg[2], lg[3], 4, C.zSkinD);
    line(hx, hipY, lg[0], lg[1] + (hipY + 24), 3.4, i === 0 ? C.zSkinD : C.zSkin); line(lg[0], lg[1] + (hipY + 24), lg[2], lg[3], 3, i === 0 ? C.zSkinD : C.zSkin);
    rect(lg[2] - 2, lg[3] - 3, 4, 1, C.gold); rect(lg[2] - 2, lg[3] - 1, 5, 1.6, C.goldD);
  });
  // kilt (pteruges) + belt
  poly([[-6, hipY - 1], [6, hipY - 1], [9, hipY + 10], [-9, hipY + 10]], C.ivoryShade);
  poly([[-6, hipY - 1], [6, hipY - 1], [8, hipY + 9], [-8, hipY + 9]], C.ivory);
  for (var k = -6; k <= 6; k += 3) line(k * 0.9, hipY + 1, k * 1.2, hipY + 9, 0.6, C.ivoryShade);
  rect(-7, hipY - 2, 14, 2.4, C.gold);
  // torso
  poly([[-6.5, -47 + br], [6.5, -47 + br], [5.5, -35], [4.5, hipY], [-4.5, hipY], [-6, -35]], C.zSkinD);
  poly([[-6, -46.5 + br], [6, -46.5 + br], [5, -35], [4, hipY], [-4, hipY], [-5.5, -35]], C.zSkin);
  line(0, -44 + br, 0, -39, 0.6, C.zSkinD); line(-4, -39.5, 4, -39.5, 0.6, C.zSkinD);
  // gold cuirass on the belly with ab lines
  poly([[-5.4, -38], [5.4, -38], [4.4, hipY - 1], [-4.4, hipY - 1]], C.gold);
  line(-4.5, -37.5, 4.5, -37.5, 0.8, C.goldL);
  line(0, -37, 0, hipY - 1.5, 0.6, C.goldD); line(-4, -33, 4, -33, 0.6, C.goldD); line(-4, -29, 4, -29, 0.6, C.goldD);
  // ivory toga sash over the back shoulder
  poly([[-6.5, -47 + br], [-2.5, -47 + br], [5.5, -30], [2, -28]], C.ivory);
  line(-4, -45 + br, 3.5, -30, 0.6, C.ivoryShade);
  // head: hair, face, beard, laurel
  var hx = 1, hy = -53.5 + br;
  var hw = 1.5 + 2.5 * wind;
  poly([[hx - 7, hy - 3], [hx - 9 - hw, hy + 1 + fl * 0.4], [hx - 8 - hw * 1.3, hy + 6], [hx - 4, hy + 5]], C.zHairShade);
  disc(hx - 1.2, hy - 0.8, 6.8, C.zHair);
  disc(hx + 1.6, hy + 0.4, 5.2, C.zSkin);
  rect(hx + 1, hy - 5.6, 5.4, 2.6, C.zHair); // hair over brow
  poly([[hx - 1.5, hy + 1], [hx + 7, hy + 1.5], [hx + 6, hy + 6], [hx + 3, hy + 10.5 + fl * 0.3], [hx - 1, hy + 9 - wind * 1.5], [hx - 3, hy + 4]], C.zHairShade);
  poly([[hx - 1, hy + 1], [hx + 6.8, hy + 1.6], [hx + 5.6, hy + 6], [hx + 2.8, hy + 9.6 + fl * 0.3], [hx - 0.6, hy + 8 - wind * 1.5], [hx - 2.4, hy + 4]], C.zHair);
  line(hx + 2.5, hy + 2.6, hx + 6.6, hy + 2.6, 0.8, C.zHairShade); // moustache
  rect(hx + 6.2, hy - 0.8, 1.4, 1.8, C.zSkin); // nose
  rect(hx + 3, hy - 2.8, 3.6, 1, C.zHair); // brow
  var eg = p.eyeGlow || 0;
  rect(hx + 3.8, hy - 1.5, 2, 1, C.white); rect(hx + 5, hy - 1.5, 0.9, 1, eg > 0.3 ? C.cyan : C.eBlueD);
  if (eg > 0) { lighter(); glow(hx + 5, hy - 1, 1.5 + 2.5 * eg, C.cyan, 0.5 * eg); normalBlend(); }
  // laurel
  for (var lf = 0; lf < 5; lf++) { var la = -2.6 + lf * 0.45; ell(hx - 1 + Math.cos(la) * 6.6, hy - 1 + Math.sin(la) * 6.6, 1.6, 0.9, la + 1.2, C.gold); }
  // front arm + bolt
  var fa = arm(4, -43 + br, p.aF, p.bF, 9, 9, 3.4, C.zSkin, C.zSkinD);
  disc(4.6, -43 + br, 2.3, C.gold); disc(4.4, -43.6 + br, 1.1, C.goldL); // pauldron
  line(fa[0] + (fa[2] - fa[0]) * 0.45, fa[1] + (fa[3] - fa[1]) * 0.45, fa[0] + (fa[2] - fa[0]) * 0.8, fa[1] + (fa[3] - fa[1]) * 0.8, 3.8, C.gold); // bracer
  if (p.boltOn !== 0) thunderbolt(fa[2], fa[3], p.bolt, 0.85, p.charge || 0, t);
  disc(fa[2], fa[3], 2, C.zSkin);
  g.restore();
  // return the world position of the bolt hand (for effects)
  var m = handWorld(x, y, s, dir, p.lean || 0, fa[2], fa[3]);
  return { hand: m, head: handWorld(x, y, s, dir, p.lean || 0, hx + 3, hy) };
}
function handWorld(x, y, s, dir, lean, lx, ly) {
  var c = Math.cos(lean), sn = Math.sin(lean);
  var rx = lx * c - ly * sn, ry = lx * sn + ly * c;
  return [x + rx * s * dir, y + ry * s];
}

// ------------------------------------------------------------------ SHIVA
// p: aF,bF (front arm, holds the trishul), aB,bB, tri (trishul angle), grip, triGlow, legs, sit (0..1 lotus),
//    eyes: 'closed' | 'calm' | 'glow', aura (0..1), lean
var SPOSE = {
  stand: { aF: 0.9, bF: 1.4, aB: -0.2, bB: 0.3, tri: 3.14, legs: "stand" },
  raise: { aF: 1.9, bF: 0.9, aB: -0.3, bB: 0.4, tri: 3.14, legs: "stand", grip: 30 },
  guard: { aF: 1.3, bF: 0.5, aB: 1.0, bB: 0.6, tri: 2.2, legs: "wide" },
  across: { aF: 1.5, bF: 0.3, aB: 0.9, bB: 0.9, tri: 1.9, legs: "wide" },
  sweep: { aF: 1.8, bF: 0.2, aB: -0.6, bB: 0.4, tri: 2.0, legs: "wide", lean: 0.12 },
  low: { aF: 1.0, bF: 0.6, aB: -0.4, bB: 0.4, tri: 1.15, legs: "wide", lean: 0.1, grip: 12 },
  up: { aF: 2.6, bF: 0.2, aB: -0.5, bB: 0.5, tri: 2.8, legs: "wide", lean: 0.05 },
  plant: { aF: 1.2, bF: 1.0, aB: 0.8, bB: 1.2, tri: 3.14, legs: "wide", grip: 28 },
  two: { aF: 2.1, bF: 0.4, aB: 2.0, bB: 0.6, tri: 2.0, legs: "wide", grip: 16 },
  glide: { aF: 1.1, bF: 0.8, aB: -0.6, bB: 0.3, tri: 1.4, legs: "glide", lean: 0.2, grip: 16 },
  thrust: { aF: 1.65, bF: 0.0, aB: -0.8, bB: 0.3, tri: 1.6, legs: "wide", lean: 0.2, grip: 10 },
  block: { aF: 1.6, bF: 0.5, aB: 0.9, bB: 0.8, tri: 2.75, legs: "wide", grip: 30, lean: -0.05 },
};
var SLEGS = {
  stand: [[-2, -12, -3, 0], [2.5, -12, 4, 0]],
  wide: [[-5, -12, -8, 0], [5, -12, 8, 0]],
  glide: [[-4, -13, -9, -4], [2, -13, 0, -2]],
};
function shiva(x, y, s, dir, p, t) {
  p = p || SPOSE.stand;
  var sit = p.sit || 0, aura = p.aura || 0;
  g.save();
  g.translate(x, y); g.scale(dir * s, s); g.rotate(p.lean || 0);
  var dy = sit * 13;
  if (aura > 0) {
    lighter();
    glow(0, -36 + dy, 40 + 10 * Math.sin(t * 2), C.violet, 0.35 * aura);
    glow(0, -36 + dy, 26, C.cyan, 0.4 * aura);
    normalBlend();
  }
  g.translate(0, dy);
  // hanging jata locks behind
  var sway = Math.sin(t * 2.2) * 1;
  poly([[-3, -58], [-8, -55], [-10 + sway, -44], [-7 + sway, -38], [-4, -46]], C.jata);
  // back arm
  arm(-4, -43, p.aB, p.bB, 9, 9, 3, C.sSkinD, C.jata);
  // legs / lotus
  if (sit > 0.5) {
    ell(0, -16, 13, 4.5, 0, C.tigerD);
    ell(0, -16.5, 12, 4, 0, C.tiger);
    ell(-6, -14, 4.5, 2.4, 0.2, C.sSkin); ell(6, -14, 4.5, 2.4, -0.2, C.sSkin);
    for (var q = -9; q <= 9; q += 4) line(q, -19, q + 1.5, -15, 0.7, C.tigerD);
  } else {
    var L = SLEGS[p.legs] || SLEGS.stand;
    L.forEach(function (lg, i) {
      var hx = i === 0 ? -2 : 2;
      line(hx, -25, lg[0], lg[1], 4.2, C.sSkinD); line(lg[0], lg[1], lg[2], lg[3], 3.8, C.sSkinD);
      line(hx, -25, lg[0], lg[1], 3.2, i === 0 ? C.sSkinD : C.sSkin); line(lg[0], lg[1], lg[2], lg[3], 2.8, i === 0 ? C.sSkinD : C.sSkin);
      rect(lg[2] - 1.5, lg[3] - 2, 3, 1, C.gold); // anklet
    });
    // tiger-skin dhoti
    poly([[-6, -27], [6, -27], [8.5, -14], [5, -12.5], [2, -14], [-1, -12.5], [-4, -14], [-8.5, -13]], C.tigerD);
    poly([[-5.6, -26.5], [5.6, -26.5], [7.8, -14.5], [5, -13.4], [2, -14.8], [-1, -13.4], [-4, -14.8], [-7.8, -14]], C.tiger);
    for (var st = -5; st <= 5; st += 3.3) line(st, -25, st + 1.6, -21, 0.8, C.tigerD);
    for (var st2 = -6; st2 <= 6; st2 += 3.6) line(st2, -20, st2 + 1.4, -16, 0.8, C.tigerD);
  }
  rect(-6.5, -28, 13, 2, C.beads);
  // torso
  poly([[-6.4, -46.5], [6.4, -46.5], [5.4, -35], [4.4, -27], [-4.4, -27], [-5.8, -35]], C.sSkinD);
  poly([[-6, -46], [6, -46], [5, -35], [4, -27.5], [-4, -27.5], [-5.4, -35]], C.sSkin);
  poly([[1, -45.5], [5.4, -45.5], [4.4, -35], [3.4, -28]], C.sSkinL);
  line(-1, -43, -1, -39, 0.6, C.sSkinD);
  // rudraksha beads + serpent
  g.strokeStyle = C.beads; g.lineWidth = 1.1; g.beginPath(); g.arc(0.5, -46, 6, 0.35, Math.PI - 0.35); g.stroke();
  for (var bd = 0; bd < 6; bd++) { var ba = 0.45 + bd * 0.45; disc(0.5 + Math.cos(ba) * 6, -46 + Math.sin(ba) * 6, 0.8, C.beads); }
  g.strokeStyle = C.snakeD; g.lineWidth = 2; g.beginPath(); g.moveTo(-6, -47); g.quadraticCurveTo(0, -42, 5, -46); g.stroke();
  g.strokeStyle = C.snake; g.lineWidth = 1.2; g.stroke();
  ell(5.6, -48.6, 1.8, 1.3, -0.4, C.snake); rect(6.2, -49.2, 0.7, 0.7, C.ink);
  // head
  var hx = 1, hy = -52.5;
  // jata bun + crescent moon
  ell(hx - 1.5, hy - 9, 4.6, 6, 0, C.jata);
  ell(hx - 1, hy - 10, 3.2, 4.2, 0, C.jataL);
  line(hx - 4, hy - 7, hx + 1, hy - 12, 0.6, C.jata);
  g.strokeStyle = C.moon; g.lineWidth = 1.3; g.beginPath(); g.arc(hx + 1.6, hy - 11, 2.6, -1.2, 1.4); g.stroke();
  lighter(); glow(hx + 2.4, hy - 11, 4, C.moon, 0.35); normalBlend();
  disc(hx - 2.6, hy - 0.6, 5.2, C.jata);
  disc(hx + 1.6, hy + 0.4, 5.4, C.sSkin);
  ell(hx + 3.6, hy + 1.2, 2.6, 3.4, 0, C.sSkinL);
  poly([[hx - 3, hy - 5.8], [hx + 6.6, hy - 5.2], [hx + 6.6, hy - 4.2], [hx - 1, hy - 3.6]], C.jata); // hairline
  rect(hx + 6.1, hy - 0.3, 1.2, 1.8, C.sSkin); // nose
  // tripundra (three ash lines) + third eye
  rect(hx + 2.6, hy - 3.6, 3.6, 0.45, C.ash); rect(hx + 2.6, hy - 2.9, 3.6, 0.45, C.ash);
  var ey = p.eyes || "calm";
  rect(hx + 4.2, hy - 4.4, 0.6, 1.6, ey === "glow" ? C.cyanW : C.tilak);
  if (ey === "closed") line(hx + 3.2, hy - 0.8, hx + 5.6, hy - 0.6, 0.7, C.sSkinD);
  else if (ey === "glow") { rect(hx + 3.6, hy - 1.5, 2, 1, C.cyanW); lighter(); glow(hx + 4.6, hy - 1, 2.6, C.cyan, 0.5); normalBlend(); }
  else { rect(hx + 3.6, hy - 1.5, 2, 1, C.white); rect(hx + 4.8, hy - 1.5, 0.9, 1, C.ink); }
  line(hx + 3.2, hy - 2.2, hx + 6, hy - 2.4, 0.6, C.jata); // brow
  line(hx + 4, hy + 3, hx + 6, hy + 3, 0.6, C.sSkinD); // calm mouth
  disc(hx - 1.6, hy + 2.6, 1.3, C.gold); // earring
  // trishul + front arm
  var e = A(p.aF), ex = 4 + e[0] * 9, eyy = -43 + e[1] * 9, h2 = A(p.aF + p.bF), hxx = ex + h2[0] * 8, hyy = eyy + h2[1] * 8;
  var tr = trishul(hxx, hyy, p.tri, 1, p.triGlow || 0, t, p.grip);
  arm(4, -43, p.aF, p.bF, 9, 8, 3, C.sSkin, C.sSkinD);
  rect(ex - 1.5, eyy - 1, 3, 1.2, C.ash); // ash stripe on arm
  disc(hxx, hyy, 1.9, C.sSkin);
  g.restore();
  var lean = p.lean || 0;
  return {
    hand: handWorld(x, y + dy * s, s, dir, lean, hxx, hyy),
    tip: handWorld(x, y + dy * s, s, dir, lean, hxx + A(p.tri)[0] * 56, hyy + A(p.tri)[1] * 56),
    head: handWorld(x, y + dy * s, s, dir, lean, hx + 3, hy),
  };
}
// copy of a pose with some fields overridden
function withP(p, extra) {
  var o = {};
  Object.keys(p).forEach(function (k) { o[k] = p[k]; });
  Object.keys(extra).forEach(function (k) { o[k] = extra[k]; });
  return o;
}
// world position of Zeus's bolt hand and bolt tip for a pose (same geometry as zeus())
function zeusTip(x, y, s, dir, p, reach) {
  var e = A(p.aF), ex = 4 + e[0] * 9, ey = -43 + e[1] * 9, h = A(p.aF + p.bF), hx = ex + h[0] * 9, hy = ey + h[1] * 9;
  var b = A(p.bolt), r = reach === undefined ? 16 : reach;
  return { hand: handWorld(x, y, s, dir, p.lean || 0, hx, hy), tip: handWorld(x, y, s, dir, p.lean || 0, hx + b[0] * r * 0.85, hy + b[1] * r * 0.85) };
}
// world point on Shiva's trishul shaft, `along` units above the hand (same geometry as shiva())
function shivaGrip(x, y, s, dir, p, along) {
  var e = A(p.aF), ex = 4 + e[0] * 9, ey = -43 + e[1] * 9, h = A(p.aF + p.bF), hx = ex + h[0] * 8, hy = ey + h[1] * 8;
  var d = A(p.tri);
  return handWorld(x, y, s, dir, p.lean || 0, hx + d[0] * along, hy + d[1] * along);
}
