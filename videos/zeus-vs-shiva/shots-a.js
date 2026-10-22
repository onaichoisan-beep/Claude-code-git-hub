// Shots 01–16 (0:00–1:20): the universe trembles → the arena becomes an ocean.

// ------------------------------------------------------------------ shared pieces
var ZX = 95, SX = 225, GY = 118; // arena world: Zeus left, Shiva right, standing line
function bob(t, ph, a) { return Math.sin(t * 2.2 + (ph || 0)) * (a || 1.5); }
// the floating arena world used by shots 5–12
function arenaWorld(cam, u, t, o) {
  o = o || {};
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.nebula });
  setCam(cam, 0.4);
  lighter();
  glow(-40, 40, 170, C.gold, 0.3 * (o.gold === undefined ? 1 : o.gold));
  glow(380, 40, 170, C.cyan, 0.3 * (o.cyan === undefined ? 1 : o.cyan));
  normalBlend();
  if (o.cloudsTop) {
    setCam(cam, 0.6);
    var sp = o.cloudSplit || 0;
    clouds(-160 - sp * 120, -70, 300, 30, 81, STORM_COLS, t, 2, 34);
    clouds(160 + sp * 120, -70, 300, 30, 82, STORM_COLS, t, -2, 34);
  }
  setCam(cam, 1);
  if (o.arena !== false) arena(160, GY, 120, { crack: o.crack || 0, glowL: 0.6, glowR: 0.6 });
}
// a projectile thunder spear travelling from (x1,y1) to (x2,y2); k 0..1 = head progress
function spear(x1, y1, x2, y2, k, seed, t, w, tailLen) {
  if (k <= 0) return null;
  var hx = lerp(x1, x2, Math.min(k, 1)), hy = lerp(y1, y2, Math.min(k, 1));
  var tk = Math.max(0, k - (tailLen || 0.3));
  var tx = lerp(x1, x2, tk), ty = lerp(y1, y2, tk);
  lightning(tx, ty, hx, hy, seed, t, w || 1.4, { branches: 2 });
  lighter(); glow(hx, hy, 10, C.eBlueL, 0.8); glow(hx, hy, 4, C.white, 1); normalBlend();
  return [hx, hy];
}
function shield(x, y, r, k, t) {
  if (k <= 0) return;
  lighter();
  glow(x, y, r * 1.5, C.cyan, 0.35 * k);
  normalBlend();
  alpha(0.25 * k, function () { disc(x, y, r, C.cyan); });
  ringS(x, y, r, 1.6, C.cyanL, k);
  ringS(x, y, r * 0.75, 0.8, C.cyanW, 0.7 * k);
  for (var i = 0; i < 6; i++) arcS(x, y, r * 0.9, t * 2 + i * 1.047, t * 2 + i * 1.047 + 0.5, 1, C.white, k);
}
// a single wide establishing composition used by shot 4 (golden storm left, cyan cosmos right)
function splitSky(cam, t, k) {
  spaceBg(cam, t, { neb: 0.7, top: C.void, mid: C.space2, low: C.violetD });
  setCam(cam, 0.5);
  lighter(); glow(-30, 60, 200, C.gold, 0.45 * k); glow(350, 60, 200, C.cyan, 0.45 * k); glow(160, 50, 60, C.white, 0.25 * k); normalBlend();
  clouds(-330, -60, 330, 260, 91, GOLD_COLS, t, 3, 170); clouds(-60, 120, 180, 40, 92, GOLD_COLS, t, 3, 26);
  for (var i = 0; i < 6; i++) {
    var a = t * 0.5 + i;
    arcS(330, 70, 40 + i * 18, a, a + 1.4, 1.4, i % 2 ? C.cyanL : C.violetL, 0.6);
  }
  setCam(cam, 1);
}

// ------------------------------------------------------------------ 01 · The universe trembles
var NEB3D = (function () {
  var r = rng(101), a = [], cols = [C.nebula2, C.nebPink, C.violet, C.cyan, C.nebHot, C.gold];
  for (var i = 0; i < 40; i++) a.push({ x: (r() - 0.5) * 520, y: (r() - 0.5) * 300, z: 0.6 + r() * 7, r: 30 + r() * 60, c: cols[i % cols.length], a: 0.25 + r() * 0.3 });
  return a;
})();
var WARP = (function () {
  var r = rng(102), a = [];
  for (var i = 0; i < 160; i++) a.push({ x: (r() - 0.5) * 360, y: (r() - 0.5) * 220, z: r() * 6, c: r() < 0.3 ? C.cyanL : r() < 0.5 ? C.goldW : C.white });
  return a;
})();
SHOTS[0] = function (u, t) {
  fillAll(C.ink);
  if (u < 0.95) return;
  var fade = ramp(u, 0.95, 1.9);
  var trav = Math.pow(clamp01((u - 0.95) / 3.0), 1.7) * 6.5;
  var cam = { x: 160, y: 90, z: 1 };
  spaceBg(cam, t, { neb: fade * 0.6, stars: fade, planets: false });
  screen();
  NEB3D.forEach(function (p) {
    var z = p.z - trav;
    if (z < 0.25) return;
    glow(160 + p.x / z, 90 + p.y / z, p.r / z, p.c, p.a * fade * clamp01((z - 0.25) * 1.5));
  });
  var speed = clamp01((u - 1.4) / 1.5) * (1 - ramp(u, 3.6, 4.2));
  WARP.forEach(function (p) {
    var z = 6 - ((p.z + trav * 1.4) % 6) + 0.15;
    var z2 = z + 0.08 + 0.6 * speed;
    var x1 = 160 + p.x / z, y1 = 90 + p.y / z, x2 = 160 + p.x / z2, y2 = 90 + p.y / z2;
    if (fade < hash1(p.x)) return;
    line(x2, y2, x1, y1, z < 1 ? 1.4 : 0.8, p.c);
  });
  // the arena, far away, first a silhouette, then lit by the lightning
  var ar = ramp(u, 3.0, 4.6), lit = ramp(u, 4.2, 4.4);
  if (u > 3.0) {
    var R = 18 + 92 * ar, cy = 100 + 12 * ar;
    if (lit < 1) {
      ell(160, cy, R, R * 0.22, 0, C.space1);
      poly([[160 - R, cy], [160 + R, cy], [160, cy + R * 0.7]], C.space1);
    }
    if (lit > 0) alpha(lit, function () { arena(160, cy, R, { glowL: 0.5, glowR: 0.5 }); });
  }
  if (u > 4.15 && u < 4.55) lightning(40, -10, 150, 100 + 12 * ar - 20, 7, t, 1.8, { branches: 4 });
  if (u > 4.55) { lighter(); glow(60, 28, 70, C.gold, 0.6 * ramp(u, 4.55, 4.9)); glow(60, 28, 20, C.goldW, 0.8 * ramp(u, 4.55, 4.9)); normalBlend(); }
  vignette(0.35, "rgba(10,0,30,");
};
FLASH.push([4.18, 4.6, "#ffffff", 0.75]);

// ------------------------------------------------------------------ 02 · Zeus descends
SHOTS[1] = function (u, t) {
  var cam = camAt([[0, 160, 10, 1.15], [2.4, 160, 70, 1.05], [3.2, 160, 96, 1.1], [5, 165, 96, 1.25]], u);
  shake(cam, u, 3.05, 9, 0.6);
  goldSky(cam, t, { flash: pulse(u, 0.3, 0.7) + pulse(u, 1.6, 2.0) + pulse(u, 3.0, 3.5) });
  setCam(cam, 1);
  // storm tearing open: bright rift with clouds parting
  var open = ramp(u, 0, 1.4);
  lighter(); glow(160, -40, 60 + 50 * open, C.goldW, 0.8 * open); glow(160, -40, 120, C.eBlue, 0.3 * open); normalBlend();
  rays(160, -40, t, 14, C.goldW, 0.18 * open, 260);
  clouds(30 - 50 * open, -90, 110, 40, 211, GOLD_COLS, t, 0, 18);
  clouds(180 + 50 * open, -90, 110, 40, 212, GOLD_COLS, t, 0, 18);
  // platform
  arena(160, 150, 130, { glowL: 0.8, glowR: 0.1, crack: ramp(u, 3.05, 3.4) * 0.35 });
  // descent
  var k = ramp(u, 0.3, 3.05);
  var y = lerp(-70, 150, k);
  var p = u < 3.05 ? pose(ZPOSE, "hover", { wind: 1, lean: 0, legs: "stand", aF: 2.4, bF: 0.4, bolt: 2.8, charge: 0.6, eyeGlow: 0.6 }) :
    poseMix(ZPOSE, "brace", "stand", ramp(u, 3.3, 4.2));
  if (u >= 3.05) { p.wind = 0.8 - 0.4 * ramp(u, 3.3, 4.5); p.legs = u < 3.5 ? "crouch" : p.legs; }
  if (u < 3.05) {
    lightning(160 + Math.sin(t * 3) * 6, -90, 158, y - 50, 31, t, 1.2, { branches: 2 });
    crackle(160, y - 30, 22, 3, 33, t, C.eBlue);
  }
  zeus(160, y, 1.25, 1, p, t);
  // landing burst: marble chips + gold pixels + ring
  var lk = u - 3.05;
  shockRing(160, 152, lk / 0.8, 120, C.goldL, 3, 0.22);
  burst(160, 148, lk, 40, 221, 90, [C.marbleW, C.marble, C.gold, C.goldL], 120, 1.3);
  if (lk > 0 && lk < 0.4) lightning(160, -60, 160, 120, 34, t, 2.4, { branches: 5 });
  vignette(0.3, "rgba(30,10,0,");
};
FLASH.push([8.05, 8.45, "#fff8c8", 0.8]);

// ------------------------------------------------------------------ 03 · Shiva awakens
SHOTS[2] = function (u, t) {
  var cam = camAt([[0, 160, 92, 1.05], [5, 162, 88, 1.75]], u);
  himalaya(cam, t, { px: 160, py: 122 });
  setCam(cam, 1);
  var aura = ramp(u, 2.8, 4.6);
  // aura expanding through the clouds
  if (aura > 0) {
    lighter();
    glow(160, 85, 30 + 160 * aura, C.violet, 0.35 * aura);
    glow(160, 85, 20 + 80 * aura, C.cyan, 0.4 * aura);
    normalBlend();
    for (var i = 0; i < 3; i++) shockRing(160, 88, ((u - 2.8 - i * 0.5) / 2.2), 200, i % 2 ? C.violetL : C.cyanL, 2);
  }
  var sit = 1 - ramp(u, 2.0, 3.0);
  var p = pose(SPOSE, "stand", {
    sit: sit, eyes: u < 1.4 ? "closed" : u < 3.2 ? "calm" : "glow",
    triGlow: ramp(u, 2.4, 3.4), aura: aura, aF: lerp(0.5, 0.9, 1 - sit), bF: lerp(1.6, 1.4, 1 - sit), aB: lerp(0.5, -0.2, 1 - sit), bB: lerp(1.4, 0.3, 1 - sit),
  });
  shiva(160, 123, 0.95, -1, p, t);
  // drifting snow motes
  motes(301, 50, 0, -20, 330, 220, t, [C.white, C.paleBlue], 8, 14, 1);
  vignette(0.3, "rgba(10,10,40,");
};

// ------------------------------------------------------------------ 04 · The challenge
SHOTS[3] = function (u, t) {
  if (u < 1.7) {
    var cam = camAt([[-0.2, 160, 98, 2.2], [1.8, 168, 96, 2.5]], u);
    goldSky(cam, t, {});
    setCam(cam, 1);
    arena(160, 150, 130, { glowL: 0.8 });
    var turn = u > 0.75 ? 1 : -1;
    zeus(160, 150, 1.25, turn, pose(ZPOSE, "stand", { wind: 0.6, eyeGlow: ramp(u, 0.8, 1.3) }), t);
    lighter(); glow(330, 60, 80, C.cyan, 0.3 * ramp(u, 0.6, 1.4)); normalBlend();
  } else if (u < 3.3) {
    var cam2 = camAt([[1.7, 160, 92, 1.6], [3.3, 158, 88, 1.8]], u);
    himalaya(cam2, t, { px: 160, py: 122 });
    setCam(cam2, 1);
    var lift = ramp(u, 1.9, 2.8);
    lighter(); glow(-20, 60, 90, C.gold, 0.35 * ramp(u, 2.2, 3.0)); normalBlend();
    var sh = shiva(160, 123, 0.95, -1, withP(poseMix(SPOSE, "stand", "raise", lift), { triGlow: lift, aura: 0.4 * lift, eyes: "calm" }), t);
  } else {
    var cam3 = camAt([[3.3, 160, 80, 1.15], [5.2, 160, 84, 0.95]], u);
    splitSky(cam3, t, 1);
    setCam(cam3, 1);
    arena(160, GY, 120, { glowL: 1, glowR: 1 });
    // where the two skies meet: a seam of sparks
    burst(160, 40, (u - 3.3) % 0.8, 20, 401 + Math.floor((u - 3.3) / 0.8), 50, [C.goldL, C.cyanL, C.white], 0, 0.8);
    lighter(); glow(160, 40, 30, C.white, 0.5); normalBlend();
  }
  vignette(0.3, "rgba(10,0,30,");
};
FLASH.push([16.62, 16.85, "#ffffff", 0.6], [18.22, 18.45, "#ffffff", 0.6]);

// ------------------------------------------------------------------ 05 · Face to face
SHOTS[4] = function (u, t) {
  var cam = camAt([[0, 128, 84, 1.25], [5, 192, 84, 1.12]], u);
  arenaWorld(cam, u, t, { crack: 0.35 });
  var zy = GY - 8 + bob(t, 0, 1.6), sy = GY - 8 + bob(t, 2, 1.2);
  // energy hums: two tinted halos
  lighter(); glow(ZX, zy - 30, 36, C.gold, 0.4); glow(SX, sy - 30, 36, C.cyan, 0.4); normalBlend();
  zeus(ZX, zy, 1.05, 1, pose(ZPOSE, "ready", { lean: 0.18, charge: 0.4, wind: 0.6, eyeGlow: 0.5 }), t);
  crackle(ZX + 10, zy - 40, 20, 3, 501, t);
  shiva(SX, sy, 1.05, -1, pose(SPOSE, "stand", { triGlow: 0.5, aura: 0.4 }), t);
  motes(502, 30, -40, -20, 400, 220, t, [C.goldL, C.cyanL], 4, -6, 1);
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 06 · Zeus launches the thunderbolt
SHOTS[5] = function (u, t) {
  var cam = camAt([[0, 100, 84, 2.1], [2.9, 104, 84, 2.3], [3.5, 170, 86, 1.45], [5.2, 310, 86, 1.4]], u);
  shake(cam, u, 3.0, 6, 0.4);
  arenaWorld(cam, u, t, { crack: 0.4 });
  var ch = ramp(u, 0.9, 2.8);
  var p = u < 0.8 ? pose(ZPOSE, "ready", { wind: 0.5 }) :
    u < 2.85 ? poseMix(ZPOSE, "brace", "windup", ramp(u, 0.8, 1.6)) : poseMix(ZPOSE, "windup", "throw", ramp(u, 2.85, 3.05));
  p.charge = u < 2.95 ? ch : 0; p.wind = 0.4 + 0.6 * ch; p.eyeGlow = ch;
  p.boltOn = u < 3.0 ? 1 : 0;
  var z = zeus(ZX, GY, 1.05, 1, p, t);
  if (u > 1.0 && u < 3.0) {
    // electricity gathering, compressing into a bright spear
    crackle(z.hand[0], z.hand[1], 18 - 10 * ch, 2 + Math.round(5 * ch), 601, t, C.eBlue);
    lighter(); glow(z.hand[0], z.hand[1], 8 + 14 * ch, C.white, 0.5 * ch); normalBlend();
  }
  shiva(SX, GY, 1.05, -1, pose(SPOSE, "stand", { triGlow: 0.4, eyes: "calm" }), t);
  var k = (u - 3.0) / 2.2;
  spear(ZX + 22, GY - 46, 470, GY - 52, k, 602, t, 1.6, 0.25);
};

// ------------------------------------------------------------------ 07 · Shiva's defense
SHOTS[6] = function (u, t) {
  var cam = camAt([[0, 196, 86, 1.6], [1.7, 200, 86, 1.7], [2.0, 206, 86, 2.4], [3.2, 212, 88, 1.85], [5, 214, 88, 1.75]], u);
  shake(cam, u, 1.8, 12, 0.7);
  arenaWorld(cam, u, t, { crack: 0.45 });
  var p = poseMix(SPOSE, "stand", "across", ramp(u, 0.2, 0.8));
  p.triGlow = ramp(u, 0.6, 1.2); p.eyes = "glow"; p.aura = 0.3;
  shiva(SX, GY, 1.05, -1, p, t);
  var sk = u < 1.8 ? ramp(u, 0.8, 1.5) : 1 - 0.75 * ramp(u, 2.2, 5);
  shield(SX - 18, GY - 34, 22 + 3 * ramp(u, 1.8, 2.4), sk, t);
  // fading rings after the hit
  for (var i = 0; i < 3; i++) shockRing(SX - 18, GY - 34, (u - 1.85 - i * 0.6) / 1.4, 44, C.cyanL, 1.4);
  if (u < 1.85) spear(-60, GY - 52, SX - 40, GY - 38, ramp(u, 0.6, 1.8) * 1.0 + 0.0001, 701, t, 1.6, 0.3);
  var bk = u - 1.8;
  burst(SX - 40, GY - 36, bk, 70, 702, 110, [C.gold, C.goldL, C.eBlue, C.eBlueL, C.white], 20, 1.4);
  if (bk > 0 && bk < 0.25) { lighter(); glow(SX - 40, GY - 36, 60, C.white, 1 - bk * 4); normalBlend(); }
  vignette(0.3, "rgba(10,0,30,");
};
FLASH.push([31.78, 32.25, "#ffffff", 0.85]);

// ------------------------------------------------------------------ 08 · The shockwave
var ROCKS = (function () {
  var r = rng(801), a = [];
  for (var i = 0; i < 22; i++) a.push({ a: r() * 6.28, v: 40 + r() * 90, s: 2 + r() * 6, rot: r() * 6, spin: (r() - 0.5) * 6 });
  return a;
})();
SHOTS[7] = function (u, t) {
  var cam = camAt([[0, 190, 86, 1.75], [1.2, 160, 88, 0.85], [5, 160, 88, 0.78]], u);
  shake(cam, u, 0, 10, 0.9);
  arenaWorld(cam, u, t, { crack: 0.45 + 0.5 * ramp(u, 0.2, 1.6), cloudsTop: true, cloudSplit: ramp(u, 0.4, 2.5) });
  var cx = SX - 40, cy = GY - 36;
  for (var i = 0; i < 3; i++) shockRing(cx, cy, (u - i * 0.35) / 2.2, 330, i === 1 ? C.goldL : C.cyanL, 4);
  ROCKS.forEach(function (r) {
    var k = u + 0.3, x = cx + Math.cos(r.a) * r.v * k, y = cy + Math.sin(r.a) * r.v * k * 0.7;
    g.save(); g.translate(x, y); g.rotate(r.rot + r.spin * k);
    rect(-r.s / 2, -r.s / 2, r.s, r.s * 0.7, C.rock); rect(-r.s / 2, -r.s / 2, r.s, r.s * 0.25, C.marble);
    g.restore();
  });
  // marble slabs crack loose and drift
  slab(60 - 14 * u, GY + 20 + 4 * u, 34, -0.2 - 0.05 * u, 811);
  slab(270 + 12 * u, GY + 24 + 3 * u, 28, 0.2 + 0.04 * u, 812);
  var air = ramp(u, 1.6, 3.8);
  var zp = air < 0.05 ? pose(ZPOSE, "brace", { wind: 1, lean: -0.25 }) : poseMix(ZPOSE, "brace", "hover", air);
  zp.wind = 1;
  zeus(ZX - 10 * ramp(u, 0, 1) - 10 * air, GY - 60 * air + bob(t, 0, air * 1.5), 1.05, 1, zp, t);
  if (air > 0) crackle(ZX - 20, GY - 60 * air - 20, 24, 3, 821, t);
  shiva(SX, GY, 1.05, -1, pose(SPOSE, "guard", { triGlow: 0.6, aura: 0.3, eyes: "calm" }), t);
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 09 · Zeus's lightning barrage
SHOTS[8] = function (u, t) {
  var cam = camAt([[0, 120, 66, 1.3], [1.0, 196, 96, 1.5], [1.35, 112, 58, 1.4], [2.4, 238, 100, 1.5], [2.9, 160, 76, 1.0], [5, 190, 84, 1.12]], u);
  arenaWorld(cam, u, t, { crack: 0.9, cloudsTop: true, cloudSplit: 1 });
  var zx = 80, zy = 58 + bob(t, 0, 2);
  var thr = [0.45, 1.6, 3.1];
  var phase = 0;
  thr.forEach(function (tt) { if (u > tt - 0.35) phase = tt; });
  var w = u - phase;
  var zp = w < 0 ? pose(ZPOSE, "hover", { wind: 0.8 }) : w < 0.15 ? poseMix(ZPOSE, "windup", "throw", w / 0.15) : poseMix(ZPOSE, "throw", "hover", ramp(w, 0.2, 0.9));
  zp.legs = "fly"; zp.wind = 0.8; zp.charge = 0.7; zp.eyeGlow = 0.8;
  zeus(zx, zy, 1.0, 1, zp, t);
  shiva(SX, GY, 1.05, -1, pose(SPOSE, "guard", { triGlow: 0.8, aura: 0.4, eyes: "glow" }), t);
  var targets = [[SX - 30, GY - 2], [SX + 30, GY - 4], [SX - 14, GY - 46]];
  thr.forEach(function (tt, i) {
    var dur = i === 2 ? 2.4 : 0.55;
    var k = (u - tt) / dur;
    var start = [zx + 20, zy - 40];
    if (i === 2) start = [zx - 10, zy - 70];
    if (k > 0 && k < 1.3) spear(start[0], start[1], targets[i][0], targets[i][1], Math.min(k, 1), 900 + i, t, 1.5, 0.45);
    if (i < 2) {
      var ik = u - tt - dur;
      burst(targets[i][0], targets[i][1], ik, 45, 910 + i, 80, [C.gold, C.eBlueL, C.white, C.marble], 60, 1.2);
      if (ik > 0 && ik < 0.3) { lighter(); glow(targets[i][0], targets[i][1], 40, C.eBlueL, 1 - ik / 0.3); normalBlend(); }
      shockRing(targets[i][0], targets[i][1], ik / 0.7, 50, C.eBlueL, 2, 0.3);
    }
  });
  vignette(0.3, "rgba(10,0,30,");
};
FLASH.push([41.0, 41.3, "#cfe8ff", 0.5], [42.15, 42.45, "#cfe8ff", 0.5]);

// ------------------------------------------------------------------ 10 · Shiva redirects the storm
SHOTS[9] = function (u, t) {
  var cam = camAt([[0, 196, 82, 1.7], [2.5, 214, 76, 1.55], [5, 236, 70, 1.35]], u);
  arenaWorld(cam, u, t, { crack: 0.9, cloudsTop: true, cloudSplit: 1 });
  var spin = ramp(u, 0.2, 4.5);
  var tri = 3.14 + Math.sin(u * 2.4) * 0.9;
  var p = pose(SPOSE, "up", { tri: tri, aF: 2.2 + Math.sin(u * 2.4) * 0.5, triGlow: 1, aura: 0.6, eyes: "glow" });
  var vx = SX - 26, vy = GY - 74;
  // the vortex
  lighter(); glow(vx, vy, 34 * spin + 4, C.cyan, 0.5 * spin); normalBlend();
  for (var arm_ = 0; arm_ < 4; arm_++) {
    for (var j = 0; j < 22; j++) {
      var k = j / 22, a = -t * 5 + arm_ * 1.57 + k * 5;
      var r = 4 + 30 * k * spin;
      rect(vx + Math.cos(a) * r, vy + Math.sin(a) * r * 0.75, 1.6, 1.6, j % 3 ? C.cyanL : C.white);
    }
  }
  shiva(SX, GY, 1.05, -1, p, t);
  // incoming bolts get caught...
  [0.3, 1.1, 1.9].forEach(function (tt, i) {
    var k = (u - tt) / 0.5;
    if (k > 0 && k < 1) spear(-40, 10 + i * 20, vx, vy, k, 1001 + i, t, 1.3, 0.5);
    // ...and sent upward into a web across the clouds
    var k2 = (u - tt - 0.5) / 0.8;
    if (k2 > 0) {
      var tx = 120 + i * 90, ty = -40;
      var hk = Math.min(1, k2);
      lightning(vx, vy, lerp(vx, tx, hk), lerp(vy, ty, hk), 1010 + i, t, 1.1, { body: C.cyan, mid: C.cyanL, glowCol: C.cyan });
    }
  });
  // luminous web
  var web = ramp(u, 2.6, 4.2);
  if (web > 0) {
    var nodes = [[60, -30], [120, -40], [180, -20], [240, -42], [300, -26], [360, -38]];
    for (var n = 0; n < nodes.length - 1; n++) {
      if (n / 5 > web) break;
      lightning(nodes[n][0], nodes[n][1], nodes[n + 1][0], nodes[n + 1][1], 1020 + n, t, 0.9, { body: C.cyan, mid: C.cyanL, glowCol: C.violet, glowA: 0.3 });
      lightning(nodes[n][0], nodes[n][1], vx + (n - 2) * 20, vy - 30, 1030 + n, t, 0.6, { body: C.violet, mid: C.violetL, glowCol: C.violet, glowA: 0.2 });
    }
  }
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 11 · Zeus changes angle
SHOTS[10] = function (u, t) {
  var zpos = function (uu) {
    if (uu < 1.8) { var k = ramp(uu, 0, 1.8); return [lerp(30, 150, k), lerp(46, 28, k) + Math.sin(k * 9) * 3]; }
    if (uu < 2.2) return [150, 28];
    var k2 = ramp(uu, 2.2, 4.3); return [lerp(150, SX - 44, k2), lerp(28, GY - 2, k2 * k2)];
  };
  var zp0 = zpos(u);
  var cam = camAt([[0, 50, 52, 1.7], [1.8, 140, 44, 1.55], [2.6, 160, 62, 1.45], [5, 200, 92, 1.65]], u);
  arenaWorld(cam, u, t, { crack: 0.9, cloudsTop: true, cloudSplit: 1 });
  // jagged blue trail of past positions
  var pts = [];
  for (var s = 0; s < 14; s++) { var q = zpos(Math.max(0, u - s * 0.07)); pts.push([q[0] + (hash1(s + Math.floor(t * 15)) - 0.5) * 5, q[1] - 26 + (hash1(s * 3 + Math.floor(t * 15)) - 0.5) * 5]); }
  strokePts(pts, 3.4, C.eBlue); strokePts(pts, 1.4, C.eBlueL); strokePts(pts, 0.6, C.white);
  var diving = u > 2.2;
  var zp = diving ? pose(ZPOSE, "dive", { wind: 1, eyeGlow: 1, charge: 0.8, lean: 0.75 - 0.6 * ramp(u, 3.8, 4.4), legs: u > 4.2 ? "brace" : "fly" }) : pose(ZPOSE, "fly", { wind: 1, eyeGlow: 0.7, lean: 1.1 });
  zeus(zp0[0], zp0[1], 1.05, 1, zp, t);
  shiva(SX, GY, 1.05, -1, pose(SPOSE, "guard", { triGlow: 0.8, aura: 0.3, eyes: "glow", lean: -0.05 }), t);
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 12 · Trident against thunderbolt
SHOTS[11] = function (u, t) {
  var cam = camAt([[0, 214, 80, 2.4], [2.75, 216, 82, 2.8], [3.4, 185, 86, 1.1], [5, 185, 86, 1.05]], u);
  if (u > 0.8 && u < 2.8) { cam.x += (hash1(frameNo(t)) - 0.5) * 1.6 / cam.z * 2; cam.y += (hash1(frameNo(t) + 3) - 0.5) * 1.6 / cam.z * 2; }
  shake(cam, u, 2.8, 14, 0.6);
  arenaWorld(cam, u, t, { crack: 0.95, cloudsTop: true, cloudSplit: 1 });
  var apart = ramp(u, 2.85, 3.9);
  var push = Math.sin(t * 20) * 0.6 * (u > 0.8 && u < 2.8 ? 1 : 0);
  var sx = lerp(250, 276, apart) - push;
  var sp0 = pose(SPOSE, "block", {});
  var zt = zeusTip(0, GY, 1.05, 1, ZPOSE.swing, 21);
  // the point on the shaft level with the bolt tip
  var target = shivaGrip(250, GY, 1.05, -1, sp0, 0), best = 1e9;
  for (var al = -28; al <= 40; al += 1) { var q = shivaGrip(250, GY, 1.05, -1, sp0, al); if (Math.abs(q[1] - zt.tip[1]) < best) { best = Math.abs(q[1] - zt.tip[1]); target = q; } }
  var zx = lerp(target[0] - zt.tip[0] - 1, 108, apart) + push;
  var zp = u < 0.35 ? pose(ZPOSE, "raise", { wind: 0.9 }) : poseMix(ZPOSE, "raise", "swing", ramp(u, 0.35, 0.8));
  if (apart > 0) zp = poseMix(ZPOSE, "swing", "ready", apart);
  zp.charge = 0.9; zp.eyeGlow = 1; zp.wind = 1;
  var sp = pose(SPOSE, "block", { triGlow: 1, aura: 0.4, eyes: "glow" });
  if (apart > 0) sp = poseMix(SPOSE, "block", "guard", apart);
  sp.triGlow = 1; sp.eyes = "glow";
  shiva(sx, GY, 1.05, -1, sp, t);
  var z = zeus(zx, GY, 1.05, 1, zp, t);
  var cp = target;
  if (u > 0.8 && u < 2.85) {
    lighter(); glow(cp[0], cp[1], 14 + 4 * Math.sin(t * 30), C.white, 0.8); glow(cp[0], cp[1], 30, C.gold, 0.35); glow(cp[0] + 6, cp[1], 26, C.cyan, 0.35); normalBlend();
    burst(cp[0], cp[1], (u - 0.8) % 0.45, 26, 1201 + Math.floor((u - 0.8) / 0.45), 60, [C.goldL, C.white, C.cyanL, C.eBlueL], 30, 0.45);
    crackle(cp[0], cp[1], 12, 3, 1210, t, C.eBlue);
  }
  shockRing(cp[0], cp[1], (u - 2.8) / 0.8, 120, C.white, 4);
  vignette(0.3, "rgba(10,0,30,");
};
FLASH.push([55.75, 56.0, "#ffffff", 0.5], [57.7, 58.15, "#ffffff", 0.95]);

// ------------------------------------------------------------------ 13 · The arena breaks (high overhead)
var WEDGES = (function () {
  var r = rng(1301), a = [], n = 7, a0 = 0;
  for (var i = 0; i < n; i++) { var w = 6.2832 / n * (0.75 + r() * 0.5); a.push({ a0: a0, a1: Math.min(6.2832, a0 + w), dr: 0.5 + r() * 0.8, spin: (r() - 0.5) * 0.25, seed: i }); a0 += w; }
  a[n - 1].a1 = 6.2832;
  return a;
})();
function wedge(cx, cy, R, sq, w, k) {
  var mid = (w.a0 + w.a1) / 2;
  var ox = Math.cos(mid) * (R * 0.5 * k * w.dr), oy = Math.sin(mid) * (R * 0.5 * k * w.dr) * sq;
  var pts = [[0, 0]];
  for (var i = 0; i <= 8; i++) { var a = w.a0 + (w.a1 - w.a0) * i / 8; pts.push([Math.cos(a) * R, Math.sin(a) * R * sq]); }
  var rot = w.spin * k;
  var tp = pts.map(function (p) { var c = Math.cos(rot), s = Math.sin(rot); return [cx + ox + p[0] * c - p[1] * s, cy + oy + p[0] * s + p[1] * c]; });
  poly(tp.map(function (p) { return [p[0], p[1] + 10]; }), C.rockD);
  poly(tp.map(function (p) { return [p[0], p[1] + 4]; }), C.marbleD);
  poly(tp, C.marble);
  var inner = tp.slice(1).map(function (p) { return [lerp(tp[0][0], p[0], 0.62), lerp(tp[0][1], p[1], 0.62)]; });
  g.strokeStyle = C.gold; g.lineWidth = 1; g.beginPath(); inner.forEach(function (p, i) { if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); }); g.stroke();
  // glowing broken edges
  if (k > 0) { strokePts([tp[0], tp[1]], 1, C.goldL); strokePts([tp[0], tp[tp.length - 1]], 1, C.goldL); }
  return [cx + ox, cy + oy];
}
SHOTS[12] = function (u, t) {
  var cam = camAt([[0, 160, 92, 1.0], [5, 160, 96, 0.82]], u);
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.mountainD });
  setCam(cam, 1);
  var k = ramp(u, 0.1, 4.8);
  var cs = WEDGES.map(function (w) { return wedge(160, 100, 110, 0.55, w, k); });
  // fracture light flash at the start
  if (u < 0.6) { lighter(); glow(160, 100, 120, C.goldW, 0.6 * (1 - u / 0.6)); normalBlend(); }
  motes(1310, 40, 40, 20, 240, 160, t, [C.marble, C.rock, C.goldL], 0, -10, 1.6);
  // Zeus lands on a drifting slab (left), Shiva descends lightly (right)
  var zc = cs[3], sc = cs[0];
  var zl = ramp(u, 1.0, 2.6), sl = ramp(u, 1.8, 4.0);
  var zx = lerp(zc[0] - 10, zc[0] - 60 + 40, 1) - 20, zy = lerp(20, zc[1] + 8, zl);
  zeus(zc[0] - 30, lerp(10, zc[1] + 4, zl), 0.62, 1, u < 2.6 ? pose(ZPOSE, "hover", { wind: 1 }) : pose(ZPOSE, u < 3.0 ? "brace" : "ready", { legs: u < 3.0 ? "crouch" : "wide" }), t);
  shockRing(zc[0] - 30, zc[1] + 4, (u - 2.6) / 0.6, 30, C.goldL, 2, 0.4);
  shiva(sc[0] + 20, lerp(0, sc[1] + 4, sl), 0.62, -1, pose(SPOSE, sl < 1 ? "glide" : "stand", { aura: 0.5 * (1 - sl) + 0.2, triGlow: 0.6 }), t);
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 14 · Aerial pursuit (side-scroller)
var ZHOPS = [[150, 100], [228, 90], [306, 102], [384, 88], [462, 98], [540, 92]];
var SHOPS = [[70, 130], [148, 124], [226, 130], [304, 122], [382, 128], [460, 124]];
var FIELD = (function () {
  var r = rng(1401), a = [];
  for (var i = 0; i < 26; i++) a.push({ x: -100 + i * 32 + r() * 20, y: 30 + r() * 140, w: 12 + r() * 20, rot: (r() - 0.5) * 0.4, seed: 1410 + i, depth: 0.4 + r() * 0.4 });
  return a;
})();
function pursuitBg(cam, t) {
  spaceBg(cam, t, { neb: 0.8, top: C.void, mid: C.space2, low: C.oceanD });
  setCam(cam, 0.35);
  lighter(); glow(160, 200, 220, C.ocean, 0.5); normalBlend();
  FIELD.forEach(function (f) { setCam(cam, f.depth); slab(f.x, f.y + Math.sin(t + f.seed) * 2, f.w * f.depth, f.rot, f.seed); });
  setCam(cam, 1);
  ZHOPS.forEach(function (p, i) { slab(p[0], p[1] + 2 + Math.sin(t * 1.3 + i) * 1.2, 30, 0.05 * (i % 2 ? 1 : -1), 1450 + i); });
  SHOPS.forEach(function (p, i) { slab(p[0], p[1] + 2 + Math.sin(t * 1.1 + i) * 1.2, 26, 0.05 * (i % 2 ? -1 : 1), 1460 + i); });
}
function hopPos(H_, u, per, arc) {
  var i = Math.min(H_.length - 2, Math.floor(u / per)), k = clamp01((u - i * per) / per);
  var a = H_[i], b = H_[i + 1];
  return [lerp(a[0], b[0], k), lerp(a[1], b[1], k) - Math.sin(k * Math.PI) * arc, k];
}
SHOTS[13] = function (u, t) {
  var uu = clamp01(u / 5) * 5;
  var zp = hopPos(ZHOPS, uu, 1.0, 26);
  var sp = hopPos(SHOPS, uu, 1.0, 10);
  var cam = { x: lerp(150, 474, uu / 5) - 10, y: 82, z: 1.2 };
  pursuitBg(cam, t);
  // electric streak behind Zeus
  var tr = [];
  for (var s = 0; s < 10; s++) { var q = hopPos(ZHOPS, Math.max(0, uu - s * 0.06), 1.0, 26); tr.push([q[0] - 2, q[1] - 22 + (hash1(s + frameNo(t)) - 0.5) * 4]); }
  strokePts(tr, 2.6, C.eBlue); strokePts(tr, 0.8, C.white);
  // Shiva's glide trail (cyan, smooth)
  var st = [];
  for (var s2 = 0; s2 < 10; s2++) { var q2 = hopPos(SHOPS, Math.max(0, uu - s2 * 0.06), 1.0, 10); st.push([q2[0] - 2, q2[1] - 26]); }
  alpha(0.6, function () { strokePts(st, 2, C.cyan); });
  var airZ = zp[2] > 0.08 && zp[2] < 0.92;
  zeus(zp[0], zp[1], 0.95, 1, airZ ? pose(ZPOSE, "fly", { lean: 0.5, wind: 1, eyeGlow: 0.7 }) : pose(ZPOSE, "brace", { legs: "crouch", wind: 1 }), t);
  shiva(sp[0], sp[1], 0.95, 1, pose(SPOSE, "glide", { tri: 1.4 + Math.sin(u * 5) * 0.25, triGlow: 0.6, eyes: "calm", aura: 0.25 }), t);
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 15 · Shiva's precise counter
SHOTS[14] = function (u, t) {
  var cam = camAt([[0, 500, 86, 1.35], [1.2, 488, 92, 1.4], [2.2, 500, 88, 1.2], [3.6, 530, 80, 1.05], [5, 552, 80, 1.0]], u);
  pursuitBg(cam, t);
  var zx = 540, zyBase = 92;
  var jump = ramp(u, 2.6, 3.3) * (1 - ramp(u, 3.6, 4.6) * 0.5);
  var zy = zyBase - 34 * jump;
  var zturn = u < 3.2 ? -1 : 1;
  var zpz = u < 0.4 ? pose(ZPOSE, "ready", { wind: 0.8 }) : u < 1.0 ? poseMix(ZPOSE, "windup", "throw", ramp(u, 0.45, 0.65)) : pose(ZPOSE, jump > 0.1 ? "hover" : "ready", { wind: 1 });
  zpz.eyeGlow = 0.8;
  // Shiva on his slab
  var sx = 460, sy = 124;
  var lean = -0.35 * pulse(u, 0.5, 1.5);
  var spz = u < 1.6 ? pose(SPOSE, "guard", { lean: lean, eyes: "glow", triGlow: 0.6 }) : poseMix(SPOSE, "plant", "guard", ramp(u, 2.4, 3.4));
  spz.triGlow = 0.8; spz.eyes = "glow";
  // cyan wave rising behind Zeus
  var wk = ramp(u, 2.0, 3.8);
  if (wk > 0) {
    lighter(); glow(600, 110, 70 * wk, C.cyan, 0.5 * wk); normalBlend();
    waveWall(612 + 30 * ramp(u, 3.8, 5), 150, 130, 115 * wk, t, 1501, 1, -1);
  }
  shiva(sx, sy, 0.95, 1, spz, t);
  zeus(zx, zy, 0.95, zturn, zpz, t);
  // horizontal lightning slash passing over Shiva's leaning shoulder
  var sk = (u - 0.62) / 0.55;
  if (sk > 0 && sk < 1.3) spear(zx - 16, sy - 54, 380, sy - 56, Math.min(1, sk), 1510, t, 1.6, 0.6);
  // trident tap on the slab
  var tk = u - 2.0;
  shockRing(sx + 10, sy, tk / 0.7, 40, C.cyanL, 2, 0.3);
  if (tk > 0 && tk < 0.3) { lighter(); glow(sx + 10, sy, 20, C.cyanW, 1 - tk / 0.3); normalBlend(); }
  vignette(0.3, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 16 · The arena becomes an ocean
SHOTS[15] = function (u, t) {
  var cam = camAt([[0, 160, -70, 1.05], [3.4, 160, 66, 1.0], [5, 160, 74, 0.95]], u);
  ocean(cam, t, { hy: 122 });
  setCam(cam, 1);
  // fragments descending toward the sea
  for (var i = 0; i < 7; i++) {
    var fx = 20 + i * 46, fy = lerp(-160 + i * 12, 128 + (i % 3) * 3, ramp(u, 0, 3.6 + i * 0.15));
    slab(fx, fy, 22 + (i % 3) * 6, (i - 3) * 0.08, 1601 + i);
    spray(fx, 124, u - 3.4 - i * 0.12, 14, 1610 + i, 30);
  }
  // waves rising like walls
  [[20, 0.9, 1], [110, 0.55, -1], [300, 0.8, -1]].forEach(function (w, i) { waveWall(w[0], 130, 80, 55 * w[1] * ramp(u, 1.5 + i * 0.3, 4.2), t, 1620 + i, 1, w[2]); });
  // Shiva's disc of cyan energy
  var sx = 236, sy = 116;
  lighter(); glow(sx, sy + 2, 30, C.cyan, 0.6); normalBlend();
  ell(sx, sy + 2, 18, 4, 0, C.cyan); ell(sx, sy + 1.5, 14, 2.6, 0, C.cyanW);
  shiva(sx, sy, 0.95, -1, pose(SPOSE, "stand", { triGlow: 0.6, aura: 0.3, eyes: "calm" }), t);
  zeus(86, 66 + bob(t, 0, 2), 0.95, 1, pose(ZPOSE, "hover", { wind: 0.9, legs: "stand", eyeGlow: 0.5 }), t);
  spray(86, 126, (u % 1.2), 20, 1630 + Math.floor(u / 1.2), 40);
  // the towering wave between the gods
  waveWall(162, 134, 110, 115 * ramp(u, 3.0, 5.0), t, 1640, 1, 1);
  vignette(0.3, "rgba(0,10,40,");
};
