// Shots 33–48 (2:40–4:00): a measured pause → the cliffhanger.

var CX = 160, CY = 84; // where the two forces meet
var FZX = 60, FSX = 260, FGY = 122; // final stage positions

function finalStage(cam, t, o) {
  o = o || {};
  cosmicArena(cam, t, { pull: o.pull });
  setCam(cam, 1);
  if (o.platform !== false) finalPlatform(160, FGY, 150, { glowL: o.glowL || 0.4, glowR: o.glowR || 0.4, crack: o.crack || 0 });
}
// draw fn() as a flat silhouette of one colour (onto the main canvas, same camera)
var SIL = document.createElement("canvas");
SIL.width = W; SIL.height = H;
var silCtx = SIL.getContext("2d");
function silhouette(cam, fn, col, a) {
  var main = g;
  g = silCtx;
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1;
  g.clearRect(0, 0, W, H);
  setCam(cam, 1);
  fn();
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.globalCompositeOperation = "source-in"; g.globalAlpha = 1;
  g.fillStyle = col; g.fillRect(0, 0, W, H);
  g.globalCompositeOperation = "source-over";
  g = main;
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = a === undefined ? 1 : a; g.drawImage(SIL, 0, 0); g.restore();
}
// Zeus's golden-blue lightning stream and Shiva's cyan-violet energy wave
function zeusStream(x1, y1, x2, y2, t, w) {
  w = w || 1;
  lighter(); glow((x1 + x2) / 2, (y1 + y2) / 2, Math.abs(x2 - x1) * 0.5 + 12, C.gold, 0.3 * w); normalBlend();
  for (var i = 0; i < 3; i++) lightning(x1, y1, x2, y2 + (i - 1) * 2, 3600 + i, t, (1.4 - i * 0.3) * w, { body: i === 1 ? C.gold : C.eBlue, mid: i === 1 ? C.goldL : C.eBlueL, glowCol: i === 1 ? C.gold : C.eBlue, glowA: 0.2, rough: 0.12 });
}
function shivaStream(x1, y1, x2, y2, t, w) {
  w = w || 1;
  var len = Math.hypot(x2 - x1, y2 - y1), nx = -(y2 - y1) / (len + 0.01), ny = (x2 - x1) / (len + 0.01);
  lighter(); glow((x1 + x2) / 2, (y1 + y2) / 2, len * 0.5 + 12, C.cyan, 0.3 * w); glow((x1 + x2) / 2, (y1 + y2) / 2, len * 0.4 + 10, C.violet, 0.25 * w); normalBlend();
  for (var b = 0; b < 3; b++) {
    var pts = [];
    for (var k = 0; k <= 24; k++) {
      var f = k / 24, amp = (2 + b * 1.5) * w * Math.sin(f * Math.PI);
      var o = Math.sin(f * 18 - t * 9 + b * 2) * amp;
      pts.push([lerp(x1, x2, f) + nx * o, lerp(y1, y2, f) + ny * o]);
    }
    strokePts(pts, (3 - b * 0.7) * w, b === 1 ? C.violet : C.cyan);
    strokePts(pts, 1 * w, b === 1 ? C.violetL : C.cyanW);
  }
}
function mist(t, a) {
  for (var i = 0; i < 9; i++) {
    var x = -40 + i * 50 + Math.sin(t * 0.3 + i) * 20, y = 60 + Math.sin(i * 2.3) * 50;
    glow(x, y, 60, i % 3 === 0 ? C.portal : i % 3 === 1 ? C.violetL : C.paleBlue, 0.25 * a);
  }
}
var AFTER_DEBRIS = (function () {
  var r = rng(4401), a = [];
  for (var i = 0; i < 30; i++) a.push({ x: -120 + r() * 560, y: 10 + r() * 170, w: 6 + r() * 18, rot: r() * 6, sp: (r() - 0.5) * 0.4, depth: 0.5 + r() * 1.0 });
  return a;
})();
function afterDebris(cam, t, front) {
  AFTER_DEBRIS.forEach(function (d, i) {
    if (front ? d.depth < 1.2 : d.depth >= 1.2) return;
    setCam(cam, d.depth);
    slab(d.x + Math.sin(t * 0.3 + i) * 6, d.y + Math.cos(t * 0.4 + i) * 4, d.w, d.rot + d.sp * t, 4410 + i);
  });
  setCam(cam, 1);
}

// ------------------------------------------------------------------ 33 · A measured pause
SHOTS[32] = function (u, t) {
  var cam = camAt([[0, 160, 92, 1.0], [5, 160, 92, 1.28]], u);
  finalStage(cam, t, {});
  var roll = Math.sin(clamp01((u - 0.9) / 1.4) * Math.PI);
  var zp = poseMix(ZPOSE, "ready", "low", ramp(u, 0.2, 1.0));
  zp.aB += -0.6 * roll; zp.bB += 0.4 * roll;
  zp.charge = ramp(u, 3.8, 5) * 0.9; zp.eyeGlow = 0.5 + 0.5 * ramp(u, 3.8, 5); zp.wind = 0.3; zp.legs = "wide";
  zeus(FZX, FGY, 1.05, 1, zp, t);
  var sp = poseMix(SPOSE, "stand", "plant", ramp(u, 0.5, 1.6));
  sp.triGlow = 0.5; sp.eyes = "calm"; sp.aura = 0.25;
  shiva(FSX, FGY, 1.05, -1, sp, t);
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 34 · Zeus's full charge
SHOTS[33] = function (u, t) {
  var cam = camAt([[0, 92, 96, 1.5], [5, 74, 82, 2.15]], u);
  var ch = ramp(u, 0.6, 4.2);
  finalStage(cam, t, { glowL: 0.5 + 1.5 * ch });
  setCam(cam, 1);
  lighter(); glow(FZX + 60, FGY, 90 * ch, C.gold, 0.4 * ch); normalBlend(); // light spills toward Shiva
  var zp = poseMix(ZPOSE, "low", "raise", ramp(u, 0.2, 1.2));
  zp.charge = ch; zp.eyeGlow = ch; zp.wind = 0.5 + 0.5 * ch; zp.legs = "wide";
  var z = zeus(FZX, FGY, 1.05, 1, zp, t);
  // the storm crown: gold coils around electric blue above the raised bolt
  if (ch > 0.1) {
    var cx = z.hand[0], cy = z.hand[1] - 16;
    lighter(); glow(cx, cy, 30 * ch, C.gold, 0.5 * ch); glow(cx, cy, 18 * ch, C.eBlue, 0.6 * ch); normalBlend();
    for (var i = 0; i < 6; i++) {
      var a0 = t * 3 + i * 1.047, a1 = a0 + 0.8;
      arcS(cx, cy, 10 + 8 * ch, a0, a1, 1.6, i % 2 ? C.gold : C.goldL, ch);
      var px = cx + Math.cos(a0) * (10 + 8 * ch), py = cy + Math.sin(a0) * (10 + 8 * ch) * 0.5;
      if (i % 2 === 0) lightning(cx, cy, px, py - 10 * ch, 3410 + i, t, 0.7);
    }
    crackle(cx, cy, 14 + 10 * ch, 4, 3420, t, C.eBlue);
  }
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 35 · Shiva's cosmic focus (mandala)
function mandala(x, y, R, k, t) {
  if (k <= 0) return;
  lighter(); glow(x, y, R * 1.3, C.violet, 0.35 * k); glow(x, y, R * 0.8, C.cyan, 0.3 * k); normalBlend();
  ringS(x, y, R, 1.4, C.cyanL, k); ringS(x, y, R * 0.82, 0.8, C.violetL, k); ringS(x, y, R * 0.45, 1, C.cyanW, k);
  var rot = t * 0.3;
  [[3, rot, C.cyanL], [3, rot + Math.PI, C.violetL], [6, -rot * 0.7, C.cyanW]].forEach(function (pg, j) {
    var n = pg[0], rr = j === 2 ? R * 0.82 : R * 0.7;
    var pts = [];
    for (var i = 0; i < n; i++) { var a = pg[1] + i * 6.2832 / n; pts.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
    pts.push(pts[0]);
    alpha(k, function () { strokePts(pts, 1, pg[2]); });
  });
  for (var p = 0; p < 12; p++) {
    var a = -rot * 1.3 + p * 0.5236;
    alpha(k * 0.9, function () { ell(x + Math.cos(a) * R * 0.92, y + Math.sin(a) * R * 0.92, 4, 1.6, a, p % 2 ? C.cyan : C.violet); });
  }
}
SHOTS[34] = function (u, t) {
  var cam = camAt([[0, FSX, 90, 1.5], [5, FSX, 78, 2.2]], u);
  finalStage(cam, t, { glowR: 1 });
  setCam(cam, 1);
  var k = ramp(u, 0.8, 3.0);
  // stars around him turning slowly
  for (var i = 0; i < 40; i++) {
    var a = i * 0.157 + t * 0.15, r = 60 + (i % 5) * 12;
    rect(FSX + Math.cos(a) * r, 70 + Math.sin(a) * r * 0.7, 1, 1, i % 3 ? C.white : C.cyanL);
  }
  mandala(FSX, 66, 44, k, t);
  var sp = pose(SPOSE, "plant", { triGlow: 0.4 + 0.6 * k, eyes: u > 1.2 ? "glow" : "calm", aura: 0.3 + 0.6 * k });
  var s = shiva(FSX, FGY, 1.05, -1, sp, t);
  // geometry converging on the trident tip
  var conv = ramp(u, 3.4, 4.8);
  if (conv > 0) {
    for (var j = 0; j < 12; j++) {
      var aa = j * 0.5236 + t * 0.3, px = FSX + Math.cos(aa) * 44 * (1 - conv), py = 66 + Math.sin(aa) * 44 * (1 - conv);
      line(px, py, lerp(px, s.tip[0], conv), lerp(py, s.tip[1], conv), 0.8, j % 2 ? C.cyanW : C.violetL);
    }
    lighter(); glow(s.tip[0], s.tip[1], 10 + 14 * conv, C.cyan, 0.8 * conv); glow(s.tip[0], s.tip[1], 8 * conv, C.violetL, 0.8 * conv); normalBlend();
  }
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 36 · Both launch
SHOTS[35] = function (u, t) {
  var cam = camAt([[0, 160, 90, 0.95], [5, 160, 88, 1.08]], u);
  finalStage(cam, t, { glowL: 1, glowR: 1 });
  var go = u > 0.8;
  var zp = go ? poseMix(ZPOSE, "raise", "thrust", ramp(u, 0.8, 1.0)) : pose(ZPOSE, "raise", { charge: 1 });
  zp.charge = 1; zp.eyeGlow = 1; zp.wind = 1;
  var sp = go ? poseMix(SPOSE, "plant", "thrust", ramp(u, 0.8, 1.0)) : pose(SPOSE, "plant", {});
  sp.triGlow = 1; sp.eyes = "glow"; sp.aura = 0.7;
  var z = zeus(FZX, FGY, 1.05, 1, zp, t);
  var s = shiva(FSX, FGY, 1.05, -1, sp, t);
  var k = ramp(u, 0.9, 5.0) * 0.93;
  if (go) {
    var zh = [z.hand[0] + 14, z.hand[1]];
    zeusStream(zh[0], zh[1], lerp(zh[0], CX - 3, k), lerp(zh[1], CY, k), t, 1);
    shivaStream(s.tip[0], s.tip[1], lerp(s.tip[0], CX + 3, k), lerp(s.tip[1], CY, k), t, 1);
    lighter(); glow(lerp(zh[0], CX - 3, k), lerp(zh[1], CY, k), 10, C.goldW, 0.9); glow(lerp(s.tip[0], CX + 3, k), lerp(s.tip[1], CY, k), 10, C.cyanW, 0.9); normalBlend();
  }
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 37 · First collision
function duel(cam, u, t, o) {
  o = o || {};
  var zp = pose(ZPOSE, "thrust", { charge: 1, eyeGlow: 1, wind: o.wind === undefined ? 1 : o.wind, lean: o.zLean === undefined ? 0.25 : o.zLean, legs: o.zLegs || "brace" });
  var sp = pose(SPOSE, o.sPose || "thrust", { triGlow: 1, eyes: "glow", aura: 0.6 });
  var z = zeus(o.zx || FZX, o.zy || FGY, 1.05, 1, zp, o.tz === undefined ? t : o.tz);
  var s = shiva(o.sx || FSX, o.sy || FGY, 1.05, -1, sp, o.tz === undefined ? t : o.tz);
  return { z: [z.hand[0] + 14, z.hand[1]], s: s.tip };
}
SHOTS[36] = function (u, t) {
  var cam = camAt([[0, 160, 90, 1.08], [0.75, 160, 85, 2.0], [1.05, 160, 88, 1.0], [5, 160, 88, 1.0]], u);
  shake(cam, u, 0.05, 10, 0.8);
  shake(cam, u, 1.0, 8, 0.5);
  finalStage(cam, t, { glowL: 1, glowR: 1 });
  var d = duel(cam, u, t);
  zeusStream(d.z[0], d.z[1], CX, CY, t, 1);
  shivaStream(d.s[0], d.s[1], CX, CY, t, 1);
  var r = 4 + 10 * easeOut(clamp01(u / 1.0)) + 2 * Math.sin(t * 8);
  energySphere(CX, CY, r, t, 0, 1, {});
  for (var i = 0; i < 4; i++) shockRing(CX, CY, (u - i * 0.6) / 1.4, 140, i % 2 ? C.cyanL : C.goldL, 2.4);
  burst(CX, CY, u, 80, 3701, 100, [C.goldL, C.cyanL, C.white, C.violetL, C.marble], 0, 2.2);
  vignette(0.3, "rgba(10,0,30,");
};
FLASH.push([180.0, 180.35, "#ffffff", 0.85]);

// ------------------------------------------------------------------ 38 · The pull of power
var PULLED = (function () {
  var r = rng(3801), a = [];
  for (var i = 0; i < 40; i++) { var an = r() * 6.28, d = 60 + r() * 120; a.push({ x: CX + Math.cos(an) * d, y: CY + Math.sin(an) * d * 0.7, s: 1 + r() * 3, star: r() < 0.5, ph: r() }); }
  return a;
})();
SHOTS[37] = function (u, t) {
  var cam = camAt([[0, 160, 88, 1.0], [5, 160, 86, 1.3]], u);
  cam.x += (hash1(frameNo(t)) - 0.5) * 1.2; cam.y += (hash1(frameNo(t) + 7) - 0.5) * 1.2;
  var p2 = pulse(u, 3.2, 4.2);
  finalStage(cam, t, { glowL: 1, glowR: 1, pull: { x: CX, y: CY, k: 0.15 + 0.8 * ramp(u, 3.2, 3.8) } });
  var d = duel(cam, u, t, { zLean: 0.35 });
  zeusStream(d.z[0], d.z[1], CX, CY, t, 1);
  shivaStream(d.s[0], d.s[1], CX, CY, t, 1);
  // stones and small stars drifting toward the sphere
  PULLED.forEach(function (p, i) {
    var f = clamp01(((u / 5) + p.ph * 0.5) % 1) * 0.85;
    var x = lerp(p.x, CX, f * f), y = lerp(p.y, CY, f * f);
    if (p.star) rect(x, y, 1.2, 1.2, C.white);
    else { g.save(); g.translate(x, y); g.rotate(u * 2 + i); rect(-p.s / 2, -p.s / 2, p.s, p.s * 0.7, C.rock); rect(-p.s / 2, -p.s / 2, p.s, p.s * 0.25, C.marble); g.restore(); }
  });
  var pu = pulse(u, 1.2, 2.0) + p2;
  energySphere(CX, CY, 14 + 5 * pu + 1.5 * Math.sin(t * 8), t, 0, 1, {});
  shockRing(CX, CY, (u - 1.2) / 1.0, 70, C.white, 2);
  shockRing(CX, CY, (u - 3.2) / 1.0, 110, C.violetL, 3);
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 39 · The arena fractures (overhead, quarter turn)
var CRACKS39 = (function () {
  var r = rng(3901), a = [];
  for (var i = 0; i < 14; i++) {
    var an = i / 14 * 6.2832 + r() * 0.3, x = 0, y = 0, pts = [[0, 0]];
    for (var k = 0; k < 12; k++) { an += (r() - 0.5) * 0.5; x += Math.cos(an) * 16; y += Math.sin(an) * 16; pts.push([x, y]); }
    a.push(pts);
  }
  return a;
})();
SHOTS[38] = function (u, t) {
  var rot = ramp(u, 0, 5) * 1.5708;
  var cam = { x: 160, y: 90, z: 0.95 };
  fillAll(C.void);
  setCamR(cam, rot * 0.3);
  NEB.forEach(function (b) { glow(b.x * 0.6 + 60, b.y * 0.6 + 30, b.r, b.c, b.a); });
  STARS.forEach(function (s, i) { if (Math.sin(t * s.sp + s.ph) > -0.3) rect(s.x * 0.5 + 80, s.y * 0.4 + 50, s.s, s.s, s.c); });
  setCamR(cam, rot);
  var k = ramp(u, 1.8, 4.8) * 0.8;
  var cs = WEDGES.map(function (w) { return wedge(160, 90, 120, 0.62, w, k); });
  // fissures of light: across the platform and out into space
  var spread = ramp(u, 0, 2.2);
  CRACKS39.forEach(function (pts, i) {
    var n = Math.max(2, Math.round(pts.length * spread));
    var sp = pts.slice(0, n).map(function (p) { return [160 + p[0], 90 + p[1] * 0.62]; });
    strokePts(sp, 2, C.violetL); strokePts(sp, 0.8, C.white);
  });
  // both gods, small, balanced on opposite sections
  var zc = cs[3], sc = cs[0];
  zeus(zc[0] - 30, zc[1] + 6, 0.55, 1, pose(ZPOSE, "thrust", { charge: 1, wind: 1, legs: "brace" }), t);
  shiva(sc[0] + 30, sc[1] + 6, 0.55, -1, pose(SPOSE, "thrust", { triGlow: 1, aura: 0.5, eyes: "glow" }), t);
  energySphere(160, 70, 12 + Math.sin(t * 8), t, 0, 1, {});
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 40 · Zeus pushes forward
SHOTS[39] = function (u, t) {
  var cam = camAt([[0, 76, 92, 1.85], [5, 124, 86, 1.6]], u);
  finalStage(cam, t, { platform: false });
  setCam(cam, 1);
  var step = ramp(u, 0.3, 1.2);
  var zx = 50 + 14 * step;
  slab(zx + 4, FGY + 3, 60, 0.04, 4001);
  slab(FSX - 4, FGY + 3, 60, -0.04, 4002);
  var bal = -0.5 * ramp(u, 1.2, 4.2);
  var zp = pose(ZPOSE, "thrust", { charge: 1, eyeGlow: 1, wind: 1, lean: 0.3, legs: "brace" });
  var z = zeus(zx, FGY, 1.05, 1, zp, t);
  var s = shiva(FSX, FGY, 1.05, -1, pose(SPOSE, "thrust", { triGlow: 1, eyes: "glow", aura: 0.6 }), t);
  var w = 1 + 0.8 * ramp(u, 1.0, 3.0);
  zeusStream(z.hand[0] + 14, z.hand[1], CX - 12, CY, t, w);
  shivaStream(s.tip[0], s.tip[1], CX + 12, CY, t, 1);
  energySphere(CX, CY, 15 + Math.sin(t * 13) * 1.6, t, bal, 1, {});
  // energy wind: streaks blowing back past Zeus
  for (var i = 0; i < 16; i++) {
    var y = 40 + hash1(i * 3.3) * 100, x = 150 - ((t * 160 + i * 37) % 160);
    line(x, y, x - 8, y, 0.6, i % 2 ? C.goldL : C.white);
  }
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 41 · Shiva answers
SHOTS[40] = function (u, t) {
  var cam = camAt([[0, 246, 104, 2.3], [2.0, 254, 68, 2.4], [5, 204, 82, 1.5]], u);
  finalStage(cam, t, { platform: false });
  setCam(cam, 1);
  slab(46 + 14, FGY + 3, 60, 0.04, 4001);
  slab(FSX - 4, FGY + 3, 60, -0.04, 4002);
  var bal = -0.5 + 0.5 * ramp(u, 1.0, 4.0);
  var z = zeus(64, FGY, 1.05, 1, pose(ZPOSE, "thrust", { charge: 1, eyeGlow: 1, wind: 1, lean: 0.3, legs: "brace" }), t);
  var sp = poseMix(SPOSE, "thrust", "two", ramp(u, 0.2, 1.0));
  sp.triGlow = 1; sp.eyes = "glow"; sp.aura = 0.8;
  var s = shiva(FSX, FGY, 1.05, -1, sp, t);
  zeusStream(z.hand[0] + 14, z.hand[1], CX - 12, CY, t, 1.5);
  shivaStream(s.tip[0], s.tip[1], CX + 12, CY, t, 1 + 0.6 * ramp(u, 1.0, 3.0));
  var tr = u > 3.5 ? Math.sin(t * 40) * 1.2 : 0;
  energySphere(CX + tr, CY, 15 + Math.sin(t * 11) * 1.2, t, bal, 1, {});
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 42 · The world holds its breath (slow motion)
SHOTS[41] = function (u, t) {
  var ts = 205 + u * 0.12; // everything crawls
  var cam = camAt([[0, 146, 84, 1.55], [5, 174, 82, 1.85]], u);
  finalStage(cam, ts, { platform: false });
  setCam(cam, 1);
  slab(60, FGY + 3, 60, 0.04, 4001);
  slab(FSX - 4, FGY + 3, 60, -0.04, 4002);
  var z = zeus(64, FGY, 1.05, 1, pose(ZPOSE, "thrust", { charge: 1, eyeGlow: 1, wind: 1, lean: 0.3, legs: "brace" }), ts);
  var s = shiva(FSX, FGY, 1.05, -1, pose(SPOSE, "two", { triGlow: 1, eyes: "glow", aura: 0.8 }), ts);
  zeusStream(z.hand[0] + 14, z.hand[1], CX - 12, CY, ts, 1.5);
  shivaStream(s.tip[0], s.tip[1], CX + 12, CY, ts, 1.5);
  motes(4201, 60, 40, 20, 240, 140, ts, [C.white, C.goldL, C.cyanL, C.violetL], 0, 0, 1.2);
  var fl = Math.floor(u / 0.35) % 3;
  energySphere(CX, CY, 16, ts, 0, 1, { flick: fl, seam: ramp(u, 4.2, 4.9) });
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 43 · A flash beyond the arena
SHOTS[42] = function (u, t) {
  var cam = camAt([[0, 160, 86, 1.7], [5, 160, 86, 0.62]], u);
  finalStage(cam, t, { platform: false });
  setCam(cam, 1);
  var f = ramp(u, 0.1, 3.0);
  lighter();
  glow(CX, CY, 20 + 260 * f, C.goldW, 0.9);
  glow(CX, CY, 10 + 160 * f, C.white, 1);
  normalBlend();
  rays(CX, CY, t, 24, C.goldW, 0.35 * f, 500);
  disc(CX, CY, 8 + 120 * f * f, C.white);
  silhouette(cam, function () {
    slab(60, FGY + 3, 60, 0.04, 4001);
    slab(FSX - 4, FGY + 3, 60, -0.04, 4002);
    zeus(64, FGY, 1.05, 1, pose(ZPOSE, "brace", { wind: 1, lean: -0.2 }), t);
    shiva(FSX, FGY, 1.05, -1, pose(SPOSE, "guard", { lean: -0.1 }), t);
  }, C.shadow, 1 - ramp(u, 3.2, 4.4));
};
FLASH.push([210.0, 210.5, "#ffffff", 0.9], [213.6, 215.4, "#ffffff", 1.0]);
NOCUT[43] = true;

// ------------------------------------------------------------------ 44 · After the collision
SHOTS[43] = function (u, t) {
  var cam = camAt([[0, 148, 88, 1.0], [5, 172, 88, 1.05]], u);
  spaceBg(cam, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD });
  afterDebris(cam, t, false);
  setCam(cam, 1);
  lighter(); mist(t, 1); normalBlend();
  slab(50, 128, 46, 0.1, 4430);
  slab(272, 126, 46, -0.12, 4431);
  zeus(50, 124, 1.0, 1, pose(ZPOSE, "low", { wind: 0.3, legs: "wide", charge: 0.2, eyeGlow: 0.4 }), t);
  shiva(272, 122, 1.0, -1, pose(SPOSE, "stand", { triGlow: 0.4, eyes: "calm", aura: 0.2 }), t);
  lighter(); mist(t + 4, 0.6 * (1 - ramp(u, 0.5, 3.5)) + 0.25); normalBlend();
  afterDebris(cam, t, true);
  vignette(0.35, "rgba(10,0,30,");
};
SHOTPOST[43] = function (u, img) { if (u < 1.6) tintImg(img, "#ffffff", 1 - ramp(u, 0, 1.6)); };

// ------------------------------------------------------------------ 45 · Two powers remain
SHOTS[44] = function (u, t) {
  if (u < 1.8) {
    var cam = camAt([[-0.2, 58, 84, 2.3], [1.8, 60, 82, 2.5]], u);
    spaceBg(cam, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD });
    setCam(cam, 1);
    lighter(); mist(t, 0.4); normalBlend();
    slab(50, 128, 46, 0.1, 4430);
    var flick = hash1(frameNo(t) * 0.37) > 0.55 ? 1 : 0;
    var z = zeus(50, 124, 1.0, 1, pose(ZPOSE, "low", { wind: 0.3, legs: "wide", charge: 0.3, eyeGlow: 0.6, breathe: 1 }), t);
    if (flick) crackle(z.hand[0], z.hand[1], 10, 3, 4501, t, C.eBlue);
  } else if (u < 3.4) {
    var cam2 = camAt([[1.8, 264, 82, 2.3], [3.4, 262, 80, 2.5]], u);
    spaceBg(cam2, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD });
    setCam(cam2, 1);
    lighter(); mist(t, 0.4); normalBlend();
    slab(272, 126, 46, -0.12, 4431);
    shiva(272, 122, 1.0, -1, pose(SPOSE, "stand", { triGlow: 0.5, eyes: "glow", aura: 0.35 + 0.1 * Math.sin(t * 2) }), t);
  } else {
    var cam3 = camAt([[3.4, 160, 88, 1.05], [5.2, 160, 86, 1.12]], u);
    spaceBg(cam3, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD });
    afterDebris(cam3, t, false);
    setCam(cam3, 1);
    lighter(); mist(t, 0.4); normalBlend();
    slab(50, 128, 46, 0.1, 4430);
    slab(272, 126, 46, -0.12, 4431);
    zeus(50, 124, 1.0, 1, pose(ZPOSE, "low", { wind: 0.3, legs: "wide", charge: 0.3, eyeGlow: 0.6, breathe: 1 }), t);
    shiva(272, 122, 1.0, -1, pose(SPOSE, "stand", { triGlow: 0.5, eyes: "glow", aura: 0.35 }), t);
    fissure(CX, 86, 100, 0.8, t, 0.6 * ramp(u, 3.5, 4.6));
  }
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 46 · The strange signal
SHOTS[45] = function (u, t) {
  var cam = camAt([[0, 160, 88, 1.12], [5, 160, 84, 1.9]], u);
  var bend = ramp(u, 0.5, 4.5);
  spaceBg(cam, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD, pull: { x: CX, y: 86, k: 0.5 * bend } });
  setCam(cam, 1);
  lighter(); mist(t, 0.35); normalBlend();
  slab(50, 128, 46, 0.1, 4430);
  slab(272, 126, 46, -0.12, 4431);
  var wd = 0.8 + 9 * ramp(u, 3.2, 5.0);
  fissure(CX, 86, 104, wd, t, 0.7 + 0.3 * bend, function () {
    if (wd > 2) { fillAll(C.portal); setCam(cam, 1); lighter(); glow(CX, 86, 40, C.white, 0.9); normalBlend(); }
  });
  zeus(50, 124, 1.0, 1, pose(ZPOSE, "low", { wind: 0.3, legs: "wide", charge: 0.4, eyeGlow: 0.8 }), t);
  shiva(272, 122, 1.0, -1, pose(SPOSE, "stand", { triGlow: 0.6, eyes: "glow", aura: 0.35 }), t);
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 47 · The unknown presence
SHOTS[46] = function (u, t) {
  var cam = camAt([[0, 160, 92, 1.0], [5, 160, 90, 1.12]], u);
  spaceBg(cam, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD, pull: { x: CX, y: 70, k: 0.5 } });
  setCam(cam, 1);
  lighter(); mist(t, 0.3); normalBlend();
  var near = ramp(u, 0.3, 5);
  fissure(CX, 72, 120, 12 + 3 * near, t, 1, function () {
    fillAll(C.portal); setCam(cam, 1);
    lighter(); glow(CX, 72, 50, C.white, 0.9); normalBlend();
    shadowMass(CX + 10 - 16 * near, 80 - 6 * near, 0.6 + 0.6 * near, t, 0.85);
  });
  // both gods in the foreground, facing the fissure together
  var raise = ramp(u, 0.8, 1.8);
  var zp = poseMix(ZPOSE, "low", "raise", raise);
  zp.charge = 0.5 + 0.5 * raise; zp.eyeGlow = 1; zp.wind = 0.6; zp.legs = "wide";
  zeus(52, 196, 1.75, 1, zp, t);
  var sp = poseMix(SPOSE, "stand", "raise", raise);
  sp.triGlow = 1; sp.eyes = "glow"; sp.aura = 0.6;
  shiva(268, 196, 1.75, -1, sp, t);
  vignette(0.4, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 48 · Cliffhanger
SHOTS[47] = function (u, t) {
  var cam = camAt([[0, 160, 86, 1.12], [3.9, 160, 74, 3.4], [4.6, 160, 74, 3.55]], u);
  var b = ramp(u, 0.6, 2.4);
  spaceBg(cam, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.violetD, pull: { x: CX, y: 72, k: 0.5 + 0.4 * b } });
  setCam(cam, 1);
  lighter(); glow(CX, 72, 60 + 200 * b, C.portalV, 0.5 * b); glow(CX, 72, 30 + 120 * b, C.portal, 0.6 * b); normalBlend();
  rays(CX, 72, t, 20, C.portal, 0.3 * b, 400);
  // the fissure bursts open into a portal
  var pr = 14 + 46 * b;
  fissure(CX, 72, 120 + 30 * b, pr, t, 1, function () {
    fillAll(C.white); setCam(cam, 1);
    for (var i = 0; i < 6; i++) ringS(CX, 72, ((t * 20 + i * 12) % 72), 1.4, C.portalV, 0.8);
    shadowMass(CX - 6, 72, 1.2 + 0.4 * b, t, 0.35 * (1 - b));
  });
  // both flare as they prepare to respond
  var zp = pose(ZPOSE, "raise", { charge: 1, eyeGlow: 1, wind: 1, legs: "wide" });
  var z = zeus(52, 196, 1.75, 1, zp, t);
  crackle(z.hand[0], z.hand[1], 18, 5, 4801, t, C.eBlue);
  lightning(z.hand[0], z.hand[1], z.hand[0] + 20, z.hand[1] - 40, 4802, t, 1.4, { branches: 3 });
  shiva(268, 196, 1.75, -1, pose(SPOSE, "raise", { triGlow: 1, eyes: "glow", aura: 1 }), t);
  lighter(); glow(268, 120, 60, C.violet, 0.5 * b); glow(268, 120, 40, C.cyan, 0.5 * b); normalBlend();
  vignette(0.3, "rgba(30,10,60,");
};
