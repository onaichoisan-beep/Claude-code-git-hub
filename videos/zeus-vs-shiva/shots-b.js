// Shots 17–32 (1:20–2:40): Zeus splits the wave → the cosmic arena appears.

// camera with a roll around the screen centre (for the spiralling storm)
function setCamR(cam, rot) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.translate(W / 2, H / 2); g.rotate(rot || 0); g.scale(cam.z, cam.z); g.translate(-cam.x, -cam.y);
}
function cyanDisc(x, y, t) {
  lighter(); glow(x, y + 2, 30, C.cyan, 0.6); normalBlend();
  ell(x, y + 2, 18, 4, 0, C.cyan); ell(x, y + 1.5, 14, 2.6, 0, C.cyanW);
  for (var i = 0; i < 3; i++) arcS(x, y + 2, 10 + i * 4, t * 2 + i, t * 2 + i + 1.2, 0.6, C.white, 0.6);
}
function steam(x, y, k, seed) {
  burst(x, y, k, 50, seed, 70, [C.white, C.foam, C.cyanL, C.eBlueL], -30, 1.8);
}
// a column of water shooting skyward
function waterColumn(x, by, h, w, t) {
  if (h < 1) return;
  poly([[x - w, by], [x - w * 0.6, by - h], [x + w * 0.6, by - h], [x + w, by]], C.ocean);
  poly([[x - w * 0.6, by], [x - w * 0.3, by - h], [x + w * 0.2, by - h], [x + w * 0.4, by]], C.oceanL);
  for (var i = 0; i < 10; i++) {
    var yy = by - ((i * 13 + t * 90) % h), xx = x + (hash1(i) - 0.5) * w;
    line(xx, yy, xx, yy - 6, 1, C.foam);
  }
  disc(x, by - h, w * 0.9, C.foam);
  burst(x, by - h, (t * 2) % 1, 20, 1900 + Math.floor(t * 2), 30, [C.foam, C.white, C.cyanL], 40, 1);
}

// ------------------------------------------------------------------ 17 · Zeus splits the wave
SHOTS[16] = function (u, t) {
  var cam = camAt([[0, 112, 88, 1.3], [5, 152, 86, 1.6]], u);
  ocean(cam, t, { hy: 122 });
  setCam(cam, 1);
  var split = ramp(u, 1.1, 2.4) * (1 - 0.35 * ramp(u, 3.8, 5));
  // Shiva on his cyan disc, seen through the opening
  cyanDisc(186, 116, t);
  shiva(186, 116, 0.6, -1, pose(SPOSE, "guard", { triGlow: 0.7, aura: 0.3, eyes: "glow" }), t);
  if (split < 0.02) waveWall(178, 134, 120, 118, t, 1640, 1, 1);
  else {
    waveWall(178 - 34 - 26 * split, 134, 80, 118 * (1 - 0.1 * split), t, 1701, 1, -1);
    waveWall(178 + 34 + 26 * split, 134, 80, 118 * (1 - 0.1 * split), t, 1702, 1, 1);
    // glitter on the split faces
    motes(1703, 40, 178 - 40 * split - 10, 30, 80 * split + 20, 100, t, [C.cyanW, C.white, C.eBlueL], 0, -20, 1.2);
  }
  var hk = u - 1.1;
  steam(178, 70, hk, 1710);
  steam(178, 100, hk - 0.2, 1711);
  if (hk > -0.4 && hk < 0.6) {
    lightning(70, 40, 160, 60, 1720, t, 2.0, { branches: 3 });
    lightning(70, 40, 190, 90, 1721, t, 1.6, { branches: 3 });
    lightning(70, 40, 175, 30, 1722, t, 1.4, { branches: 2 });
  }
  // Zeus seen from behind his shoulder, big in the foreground
  var p = poseMix(ZPOSE, "ready", "arms", ramp(u, 0.2, 0.9));
  p.wind = 1; p.charge = 1; p.eyeGlow = 1; p.legs = "wide";
  zeus(58, 210, 2.2, 1, p, t);
  vignette(0.3, "rgba(0,10,40,");
};
FLASH.push([80.95, 81.4, "#cfe8ff", 0.65]);

// ------------------------------------------------------------------ 18 · Shiva commands the current
SHOTS[17] = function (u, t) {
  var cam = camAt([[0, 166, 82, 1.8], [3, 152, 82, 1.45], [5, 128, 84, 1.0]], u);
  ocean(cam, t, { hy: 122 });
  setCam(cam, 1);
  var form = ramp(u, 1.2, 3.6);
  var cx = 160, cy = 84;
  // water walls pause, then become streams spiralling around him
  if (form < 1) {
    alpha(1 - form, function () {
      waveWall(100 + 30 * form, 134, 80, 104, u < 0.8 ? t : 0.8 + (t - u), 1701, 1, -1);
      waveWall(220 - 30 * form, 134, 80, 104, u < 0.8 ? t : 0.8 + (t - u), 1702, 1, 1);
    });
  }
  for (var s = 0; s < 7; s++) {
    var a0 = -t * 2.4 + s * 0.9, r = lerp(70, 34, form) + s * 2;
    var len = 0.9 + form;
    arcS(cx, cy, r, a0, a0 + len, 3.4, C.ocean, form);
    arcS(cx, cy, r, a0, a0 + len, 1.6, s % 2 ? C.oceanL : C.cyanL, form);
    var tip = [cx + Math.cos(a0 + len) * r, cy + Math.sin(a0 + len) * r];
    if (form > 0.2) rect(tip[0] - 1, tip[1] - 1, 2.4, 2.4, C.foam);
  }
  cyanDisc(cx, 118, t);
  var tri = 1.2 + Math.sin(u * 1.8) * 0.5;
  shiva(cx, 118, 1.15, -1, pose(SPOSE, "sweep", { tri: tri, aF: 1.5 + Math.sin(u * 1.8) * 0.3, triGlow: 1, aura: 0.5, eyes: "glow" }), t);
  // the rotating water shield, facing Zeus, with a clear opening
  var sh = ramp(u, 3.0, 4.4);
  if (sh > 0) {
    var rx = 12, ry = 36, sx = 112, sy = 80;
    for (var i = 0; i < 16; i++) {
      var a = i / 16 * 6.2832 + t * 3;
      var px = sx + Math.cos(a) * rx * sh, py = sy + Math.sin(a) * ry * sh;
      disc(px, py, 4, C.ocean); disc(px - 1, py - 1, 2.4, C.oceanL);
      if (i % 3 === 0) rect(px, py - 2, 1.5, 1.5, C.foam);
    }
    ellS(sx, sy, rx * sh, ry * sh, 0, 1, C.cyanL, sh);
  }
  if (u > 3.4) zeus(28, 82 + bob(t, 0, 2), 0.7, 1, pose(ZPOSE, "hover", { wind: 0.8, eyeGlow: 0.6 }), t);
  vignette(0.3, "rgba(0,10,40,");
};

// ------------------------------------------------------------------ 19 · Zeus pierces the shield
SHOTS[18] = function (u, t) {
  var cam = camAt([[0, 52, 82, 1.7], [1.5, 60, 82, 1.6], [2.7, 214, 86, 1.25], [5, 205, 76, 1.0]], u);
  ocean(cam, t, { hy: 122 });
  setCam(cam, 1);
  // the shield ring
  var sx = 112, sy = 80;
  for (var i = 0; i < 16; i++) {
    var a = i / 16 * 6.2832 + t * 3, px = sx + Math.cos(a) * 12, py = sy + Math.sin(a) * 36;
    disc(px, py, 4, C.ocean); disc(px - 1, py - 1, 2.4, C.oceanL);
  }
  ellS(sx, sy, 12, 36, 0, 1, C.cyanL, 1);
  // column of water behind Shiva after the explosion
  var ek = u - 2.65;
  waterColumn(262, 124, 140 * easeOut(clamp01(ek / 1.2)), 12, t);
  cyanDisc(160, 118, t);
  shiva(160, 118, 1.0, -1, pose(SPOSE, "guard", { triGlow: 0.8, aura: 0.3, eyes: "glow", lean: -0.12 * pulse(u, 1.9, 2.6) }), t);
  var ch = ramp(u, 0.2, 1.5);
  var zp = u < 1.55 ? pose(ZPOSE, "windup", { charge: ch, legs: "fly", lean: 0, wind: 0.8, eyeGlow: 1 }) : poseMix(ZPOSE, "windup", "throw", ramp(u, 1.55, 1.7));
  zp.legs = "fly"; zp.wind = 0.8; zp.boltOn = u < 1.65 ? 1 : 0; zp.eyeGlow = 1;
  var z = zeus(32, 92 + bob(t, 0, 1.5), 1.0, 1, zp, t);
  if (u < 1.6) { crackle(z.hand[0], z.hand[1], 14 - 8 * ch, 4, 1801, t); lighter(); glow(z.hand[0], z.hand[1], 6 + 6 * ch, C.white, ch); normalBlend(); }
  // the narrow lance: through the opening, past Shiva's shoulder, into the sea
  var lk = (u - 1.6) / 1.05;
  if (lk > 0 && lk < 1.2) {
    var pts = [[50, 76], [112, 80], [158, 76], [262, 124]];
    var seg = Math.min(2.999, lk * 3), si = Math.floor(seg), f = seg - si;
    var hx = lerp(pts[si][0], pts[si + 1][0], f), hy = lerp(pts[si][1], pts[si + 1][1], f);
    var tailK = Math.max(0, seg - 0.8), ti = Math.floor(tailK), tf = tailK - ti;
    var tx = lerp(pts[ti][0], pts[ti + 1][0], tf), ty = lerp(pts[ti][1], pts[ti + 1][1], tf);
    if (lk < 1) { lightning(tx, ty, hx, hy, 1810, t, 1.0, { rough: 0.08 }); lighter(); glow(hx, hy, 8, C.white, 1); normalBlend(); }
  }
  spray(262, 120, ek, 60, 1820, 80);
  if (ek > 0 && ek < 0.3) { lighter(); glow(262, 120, 50, C.eBlueL, 1 - ek / 0.3); normalBlend(); }
  vignette(0.3, "rgba(0,10,40,");
};
FLASH.push([92.62, 92.95, "#cfe8ff", 0.5]);

// ------------------------------------------------------------------ 20 · Shiva closes the distance
SHOTS[19] = function (u, t) {
  var sx = lerp(214, 118, ramp(u, 0, 4.2));
  var cam = camAt([[0, 200, 84, 1.45], [3.6, 120, 84, 1.45], [4.3, 82, 78, 1.6], [5, 70, 74, 2.1]], u);
  ocean(cam, t, { hy: 122 });
  setCam(cam, 1);
  waterColumn(262, 124, 140 * (1 - 0.6 * ramp(u, 0, 5)), 12, t);
  // suspended spray
  motes(2001, 90, -40, 30, 360, 90, 0, [C.foam, C.cyanL, C.white], 0, 0, 1.4);
  var dk = (u - 2.1) / 0.6;
  var defl = u > 2.7;
  var sp = defl ? poseMix(SPOSE, "low", "up", ramp(u, 2.6, 2.85)) : pose(SPOSE, "low", {});
  sp.legs = "glide"; sp.triGlow = 1; sp.eyes = "glow"; sp.aura = 0.35;
  cyanDisc(sx, 118, t);
  shiva(sx, 118, 1.0, -1, sp, t);
  var zp = u < 2.1 ? pose(ZPOSE, "windup", { charge: 0.8 }) : poseMix(ZPOSE, "windup", "throw", ramp(u, 2.1, 2.25));
  zp.legs = "fly"; zp.wind = 0.8; zp.boltOn = u < 2.2 ? 1 : 0;
  zp.eyeGlow = u > 4.1 ? 1 : 0.6;
  if (u > 2.6) { zp = pose(ZPOSE, "ready", { legs: "fly", wind: 0.8, eyeGlow: u > 4.1 ? 1 : 0.6, lean: -0.1 }); }
  zeus(40, 90 + bob(t, 0, 1.5), 1.0, 1, zp, t);
  if (dk > 0 && dk < 1) spear(58, 46, sx - 20, 76, dk, 2010, t, 1.4, 0.4);
  // deflected upward into the sky
  var uk = (u - 2.7) / 0.7;
  if (uk > 0 && uk < 1.4) spear(sx - 20, 76, sx + 60, -80, Math.min(uk, 1), 2011, t, 1.4, 0.5);
  if (uk > 0 && uk < 0.3) { lighter(); glow(sx - 20, 76, 26, C.cyanW, 1 - uk / 0.3); normalBlend(); burst(sx - 20, 76, uk, 30, 2012, 60, [C.cyanL, C.white, C.eBlueL], 0, 0.5); }
  vignette(0.3, "rgba(0,10,40,");
};

// ------------------------------------------------------------------ 21 · Zeus summons the hurricane
SHOTS[20] = function (u, t) {
  if (u < 2.2) {
    var cam = camAt([[-0.2, 60, 76, 1.5], [2.2, 70, 64, 1.25]], u);
    ocean(cam, t, { hy: 122 });
    setCam(cam, 1);
    var sw = ramp(u, 0.2, 2.0);
    for (var i = 0; i < 26; i++) {
      var a = -t * 2.2 + i * 0.5, r = 30 + i * 4;
      var x = 70 + Math.cos(a) * r, y = 10 + Math.sin(a) * r * 0.25;
      alpha(sw, function () { disc(x, y, 8 + i * 0.4, C.stormD); disc(x, y - 2, 6 + i * 0.3, C.storm); });
    }
    lightning(20, 8, 120, 14, 2101, t, 1.0);
    var p = poseMix(ZPOSE, "ready", "arms", ramp(u, 0, 0.6));
    p.wind = 1; p.charge = 1; p.eyeGlow = 1; p.legs = "wide";
    zeus(70, 100 + bob(t, 0, 1.5), 1.1, 1, p, t);
    shiva(250, 118, 0.9, -1, pose(SPOSE, "guard", { triGlow: 0.6, eyes: "glow" }), t);
    cyanDisc(250, 118, t);
  } else {
    // high overhead: the storm dwarfs both figures
    var cam2 = camAt([[2.2, 160, 90, 1.7], [5, 160, 90, 0.85]], u);
    fillAll(C.oceanD);
    setCam(cam2, 1);
    for (var row = 0; row < 40; row++) for (var col = 0; col < 30; col++) {
      var wx = -200 + col * 24 + (row % 2) * 12 + Math.sin(t + row) * 3, wy = -160 + row * 12;
      line(wx, wy, wx + 6, wy, 0.8, row % 3 ? C.ocean : C.oceanL);
    }
    disc(150, 92, 3, C.gold); disc(172, 90, 3, C.cyan);
    lighter(); glow(150, 92, 8, C.gold, 0.8); glow(172, 90, 8, C.cyan, 0.8); normalBlend();
    hurricane(160, 90, 150, t * 0.7, t, {});
  }
  vignette(0.35, "rgba(0,10,40,");
};
FLASH.push([102.1, 102.4, "#ffffff", 0.7]);

// ------------------------------------------------------------------ 22 · The storm lifts them
var UPDRAFT = (function () {
  var r = rng(2201), a = [];
  for (var i = 0; i < 70; i++) a.push({ x: -60 + r() * 440, y: r() * 400, v: 60 + r() * 120, s: 1 + r() * 3, c: r() < 0.5 ? C.foam : r() < 0.7 ? C.rock : C.oceanL, sw: r() * 6 });
  return a;
})();
SHOTS[21] = function (u, t) {
  var rise = u * 22;
  var cam = { x: 160, y: 84 - rise, z: 1.15 };
  var rot = Math.sin(u * 0.6) * 0.12;
  fillAll(C.stormD);
  setCamR(cam, rot);
  g.fillStyle = vgrad(-200, 200, [[0, C.violetD], [0.5, C.storm], [1, C.stormL]]); g.fillRect(-200, -260, 720, 520);
  lighter(); glow(160, 40 - rise, 160, C.eBlue, 0.25); normalBlend();
  // vortex walls on both sides
  for (var i = 0; i < 18; i++) {
    var yy = 160 - i * 20, ph = t * 4 + i * 0.7;
    var lx = 10 + Math.sin(ph) * 10, rx = 310 + Math.sin(ph + 1) * 10;
    disc(lx, yy, 28, C.storm); disc(lx + 6, yy - 4, 16, C.stormL);
    disc(rx, yy, 28, C.storm); disc(rx - 6, yy - 4, 16, C.stormL);
  }
  UPDRAFT.forEach(function (d, i) {
    var y = 200 - ((d.y + d.v * u) % 400) + 0, x = d.x + Math.sin(u * 3 + d.sw) * 10;
    rect(x, y - rise * 0.3, d.s, d.s * 1.6, d.c);
  });
  // Shiva's calm cyan field
  var sx = 220, sy = 120 - rise * 1.0 + bob(t, 1, 2);
  lighter(); glow(sx, sy - 30, 40, C.cyan, 0.5); normalBlend();
  ringS(sx, sy - 30, 34, 1, C.cyanL, 0.7);
  shiva(sx, sy, 0.95, -1, pose(SPOSE, "stand", { triGlow: 0.6, eyes: "calm", aura: 0.3 }), t);
  var zx = 100 + Math.sin(u * 2) * 8, zy = 120 - rise * 1.05;
  zeus(zx, zy, 0.95, 1, pose(ZPOSE, "arms", { legs: "fly", lean: 0.1, wind: 1, eyeGlow: 0.8, charge: 0.5 }), t);
  // dark clouds closing above, lightning flashes reveal them
  var dk = ramp(u, 3.0, 4.6);
  screen();
  alpha(dk * 0.5, function () { fillAll(C.stormD); });
  [3.4, 4.0, 4.6].forEach(function (ft, i) {
    var f = pulse(u, ft, ft + 0.3);
    if (f > 0) { setCamR(cam, rot); lightning(40 + i * 110, zy - 120, 60 + i * 100, zy - 20, 2210 + i, t, 1.2, { branches: 3 }); screen(); alpha(f * 0.5, function () { fillAll(C.eBlueL); }); }
  });
  if (dk > 0.4) {
    setCamR(cam, rot);
    lighter(); glow(zx, zy - 30, 20, C.gold, 0.5 * dk); glow(sx, sy - 30, 20, C.cyan, 0.5 * dk); normalBlend();
  }
  vignette(0.4, "rgba(0,0,20,");
};

// ------------------------------------------------------------------ 23 · Zeus gains the advantage
SHOTS[22] = function (u, t) {
  var cam = camAt([[0, 150, -10, 1.5], [1.8, 158, 70, 1.4], [2.05, 164, 74, 1.7], [5, 196, 80, 1.1]], u);
  shake(cam, u, 1.8, 14, 0.6);
  stormSky(cam, t, { seed: 5, flash: pulse(u, 1.75, 2.1) });
  setCam(cam, 1);
  // dark cloud bank on the right
  clouds(250, 30, 160, 110, 2301, [C.void, C.stormD, C.storm], t, 0, 40);
  var hit = u > 1.8;
  var drive = ramp(u, 1.8, 4.4);
  var sx = lerp(170, 292, drive), sy = lerp(112, 104, drive);
  var flick = hit ? (Math.sin(t * 40) > 0 ? 1 : 0.4) * (1 - 0.5 * drive) : 1;
  shield(sx - 14, sy - 34, 26, flick, t);
  shiva(sx, sy, 1.0, -1, pose(SPOSE, hit ? "across" : "guard", { triGlow: 0.8, eyes: "glow", legs: "glide", lean: hit ? -0.2 : 0 }), t);
  var zk = ramp(u, 0, 1.8);
  var zx = lerp(120, 130, zk), zy = lerp(-90, 100, zk);
  if (hit) { zx = 130 + 6 * Math.sin(t * 2); zy = 100 + bob(t, 0, 1.5); }
  var zp = hit ? poseMix(ZPOSE, "thrust", "hover", ramp(u, 2.0, 3.0)) : pose(ZPOSE, "dive", { lean: 0.4, wind: 1, eyeGlow: 1, charge: 1 });
  zp.wind = 1; zp.eyeGlow = 1;
  var tr = [];
  for (var s = 0; s < 10 && !hit; s++) tr.push([zx - 4 + (hash1(s + frameNo(t)) - 0.5) * 4, zy - 40 - s * 8]);
  if (tr.length > 1) { strokePts(tr, 3, C.eBlue); strokePts(tr, 1, C.white); }
  zeus(zx, zy, 1.15, 1, zp, t);
  var bk = u - 1.8;
  burst(160, 76, bk, 60, 2310, 100, [C.gold, C.goldL, C.cyanL, C.white], 20, 1.2);
  if (bk > 0 && bk < 0.25) { lighter(); glow(160, 76, 70, C.white, 1 - bk * 4); normalBlend(); }
  vignette(0.35, "rgba(0,0,20,");
};
FLASH.push([111.78, 112.2, "#ffffff", 0.9]);

// ------------------------------------------------------------------ 24 · The midpoint reversal (inside the cloud bank)
var RAIN = (function () {
  var r = rng(2401), a = [];
  for (var i = 0; i < 140; i++) a.push({ x: r() * 420 - 50, y: r() * 300 - 60, v: 120 + r() * 80, l: 3 + r() * 4 });
  return a;
})();
function rainAt(tt, x0, y0, frozen) {
  RAIN.forEach(function (d) {
    var y = y0 + ((d.y + d.v * tt) % 300 + 300) % 300 - 60, x = x0 + d.x - (y - y0) * 0.15;
    if (frozen) { rect(x, y, 1, 1.4, C.cyanW); }
    else line(x, y, x - d.l * 0.15, y - d.l, 0.6, C.stormL);
  });
}
SHOTS[23] = function (u, t) {
  var cam = camAt([[0, 156, 48, 2.0], [2.3, 155, 40, 3.2], [3.0, 155, 42, 2.8], [5, 160, 70, 1.0]], u);
  var freezeT = 115 + 2.4;
  var tt = Math.min(t, freezeT);
  fillAll(C.storm);
  setCam(cam, 0.5);
  clouds(-120, -40, 560, 220, 2402, [C.stormD, C.storm, C.stormL], tt, 3, 90);
  setCam(cam, 1);
  var bloom = ramp(u, 2.4, 4.6);
  if (bloom > 0) {
    lighter();
    glow(156, 40, 40 + 220 * bloom, C.violet, 0.45 * bloom);
    glow(156, 40, 30 + 140 * bloom, C.cyan, 0.5 * bloom);
    normalBlend();
    for (var i = 0; i < 4; i++) shockRing(156, 40, (u - 2.4 - i * 0.45) / 2.0, 260, i % 2 ? C.violetL : C.cyanL, 2);
  }
  rainAt(tt, 0, 0, u > 2.4);
  var eyes = u < 0.9 ? "calm" : u < 2.3 ? "closed" : "glow";
  shiva(160, 150, 2.2, -1, pose(SPOSE, "stand", { eyes: eyes, triGlow: bloom, aura: 0.2 + 0.8 * bloom, lean: -0.05 * (1 - ramp(u, 0, 1.2)) }), t);
  vignette(0.45, "rgba(0,0,20,");
};

// ------------------------------------------------------------------ 25 · The storm falls still
var GALAXIES = [[40, 30, 1], [200, 10, -1], [330, 50, 1], [-40, 70, -1]];
function galaxy(x, y, s, dir, t, a) {
  for (var arm_ = 0; arm_ < 2; arm_++) for (var j = 0; j < 18; j++) {
    var k = j / 18, an = dir * (t * 0.4 + arm_ * 3.14 + k * 4), r = 2 + k * 16 * s;
    alpha(a * (1 - k * 0.6), function () { rect(x + Math.cos(an) * r, y + Math.sin(an) * r * 0.45, 1.6, 1.6, j % 3 ? C.violetL : C.portal); });
  }
  lighter(); glow(x, y, 8 * s, C.violet, 0.6 * a); normalBlend();
}
SHOTS[24] = function (u, t) {
  var cam = camAt([[0, 230, 80, 1.5], [3.0, 180, 76, 1.3], [5, 96, 80, 1.15]], u);
  var tt = 117.4;
  fillAll(C.stormD);
  setCam(cam, 0.5);
  clouds(-120, -40, 560, 220, 2402, [C.void, C.stormD, C.storm], tt, 3, 90);
  setCam(cam, 0.6);
  GALAXIES.forEach(function (gx, i) { galaxy(gx[0] + u * 14 * gx[2], gx[1], 1.2, gx[2], t, 0.9); });
  setCam(cam, 1);
  lighter(); glow(230, 80, 120, C.violet, 0.35); glow(230, 80, 70, C.cyan, 0.35); normalBlend();
  rainAt(tt, 0, 0, true);
  // frozen fragments
  for (var i = 0; i < 12; i++) { var fx = 40 + hash1(i * 3.1) * 260, fy = 20 + hash1(i * 7.7) * 130; g.save(); g.translate(fx, fy); g.rotate(i); rect(-2, -1.5, 4, 3, C.rock); rect(-2, -1.5, 4, 1, C.marble); g.restore(); }
  shiva(230, 120, 1.2, -1, pose(SPOSE, "stand", { eyes: "glow", triGlow: 1, aura: 0.9 }), t);
  // Zeus beyond the clouds, framed by lightning frozen in place
  var zr = ramp(u, 2.6, 4.4);
  setCam(cam, 1);
  if (zr > 0) {
    lightning(30, 10, 46, 60, 2501, 120.0, 1.2, { branches: 2 });
    lightning(80, 20, 64, 80, 2502, 120.0, 1.0, { branches: 2 });
    zeus(54, 100, 0.8, 1, pose(ZPOSE, "hover", { wind: 0.3, eyeGlow: 0.6 }), t);
    alpha(1 - zr, function () { clouds(0, 30, 120, 90, 2503, [C.stormD, C.storm, C.stormL], tt, 0, 30); });
  }
  vignette(0.4, "rgba(0,0,20,");
};

// ------------------------------------------------------------------ 26 · Shiva releases the field
var CLOUDWALL = (function () {
  var r = rng(2601), a = [];
  for (var i = 0; i < 70; i++) a.push({ x: -200 + r() * 520, y: -40 + r() * 220, r: 12 + r() * 16 });
  return a;
})();
SHOTS[25] = function (u, t) {
  var cam = camAt([[0, 214, 84, 1.3], [2.0, 136, 84, 1.0], [5, 28, 84, 1.25]], u);
  var ringR = 360 * ramp(u, 0.9, 4.4);
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.violetD });
  setCam(cam, 1);
  var cx = 230, cy = 84;
  CLOUDWALL.forEach(function (c) {
    var dx = c.x - cx, dy = c.y - cy, d = Math.sqrt(dx * dx + dy * dy) + 0.1;
    var push = Math.max(0, ringR - d + 40) * 1.2;
    var x = c.x + dx / d * push, y = c.y + dy / d * push * 0.6;
    disc(x, y + 3, c.r, C.stormD); disc(x, y, c.r * 0.9, C.storm); disc(x - c.r * 0.25, y - c.r * 0.3, c.r * 0.45, C.stormL);
  });
  if (ringR > 0) {
    ellS(cx, cy, ringR, ringR * 0.55, 0, 6, C.violet, 0.8);
    ellS(cx, cy, ringR, ringR * 0.55, 0, 2.4, C.cyanL, 1);
    lighter(); glow(cx + ringR, cy, 26, C.cyanW, 0.5); normalBlend();
  }
  var low = ramp(u, 0.2, 0.9);
  shiva(cx, 120, 1.05, -1, withP(poseMix(SPOSE, "stand", "low", low), { triGlow: 1, eyes: "glow", aura: 0.6 }), t);
  var hitZ = u > 3.9;
  zeus(4, 96 + bob(t, 0, 1.5), 0.95, 1, pose(ZPOSE, hitZ ? "brace" : "hover", { wind: hitZ ? 1 : 0.4, legs: "fly", lean: hitZ ? -0.25 * (1 - ramp(u, 4.2, 5)) : 0, eyeGlow: 0.7 }), t);
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 27 · Zeus adapts (hand close-up, tilt to face)
SHOTS[26] = function (u, t) {
  var cam = camAt([[0, 198, 80, 3.0], [2.4, 196, 76, 2.9], [3.8, 166, 56, 2.5], [5, 164, 52, 2.7]], u);
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.violetD });
  setCam(cam, 0.6);
  clouds(-60, 120, 400, 60, 2701, [C.stormD, C.storm, C.stormL], t, 2, 30);
  setCam(cam, 1);
  var gather = ramp(u, 0.3, 3.4);
  var p = pose(ZPOSE, "low", { aF: 1.2, bF: 0.6, bolt: 1.9, charge: 0.3 + 0.7 * gather, wind: 0.5, eyeGlow: ramp(u, 3.6, 4.4), legs: "wide" });
  // arcs drawn inward from the air toward the arm
  var hx = 200.8, hy = 74.7;
  for (var i = 0; i < 5; i++) {
    var a = i * 1.26 + t * 0.7, r0 = 60 * (1 - gather) + 12;
    if (gather < 0.98) lightning(hx + Math.cos(a) * r0, hy + Math.sin(a) * r0, hx + Math.cos(a) * 6, hy + Math.sin(a) * 6, 2710 + i, t, 0.7);
  }
  zeus(150, 175, 2.4, 1, p, t);
  lighter();
  glow(hx - 10, hy + 2, 14 + 6 * gather, C.gold, 0.5 * gather);
  glow(hx - 10, hy + 2, 10 + 4 * gather, C.eBlue, 0.5 * gather);
  normalBlend();
  ringS(hx - 6, hy, 6 + 2 * Math.sin(t * 10), 0.8, C.goldL, gather);
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 28 · A focused thunder spear
var DEBRIS28 = [[160, 60, 16], [262, 46, 20], [330, 118, 18], [250, 136, 12], [90, 130, 14]];
var PATH28 = [[46, 70], [150, 30], [216, 86], [312, 76], [372, 116], [290, 124], [236, 116]];
function pathAt(P, k) {
  var L = [], tot = 0;
  for (var i = 0; i < P.length - 1; i++) { var d = Math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]); L.push(d); tot += d; }
  var s = clamp01(k) * tot;
  for (var j = 0; j < L.length; j++) { if (s <= L[j]) { var f = s / L[j]; return [lerp(P[j][0], P[j + 1][0], f), lerp(P[j][1], P[j + 1][1], f)]; } s -= L[j]; }
  return P[P.length - 1].slice();
}
SHOTS[27] = function (u, t) {
  var hk = ramp(u, 0.6, 5.2) * 0.93;
  var head = pathAt(PATH28, hk);
  var cam = { x: lerp(110, head[0], ramp(u, 0.4, 1.2)), y: lerp(78, head[1] * 0.4 + 52, ramp(u, 0.4, 1.2)), z: 1.35 };
  if (u > 3.8) { var e = ramp(u, 3.8, 5); cam.x = lerp(cam.x, 262, e); cam.y = lerp(cam.y, 100, e); cam.z = lerp(1.35, 1.2, e); }
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.violetD });
  setCam(cam, 1);
  DEBRIS28.forEach(function (d, i) { slab(d[0], d[1] + Math.sin(t + i) * 2, d[2], i * 0.3, 2801 + i); });
  shiva(236, 128, 0.95, -1, pose(SPOSE, "guard", { triGlow: 0.6, eyes: "glow", aura: 0.3 }), t);
  var zp = u < 0.6 ? pose(ZPOSE, "windup", { charge: 1, legs: "fly" }) : poseMix(ZPOSE, "windup", "thrust", ramp(u, 0.6, 0.75));
  zp.legs = "fly"; zp.wind = 0.6; zp.eyeGlow = 1; zp.boltOn = u < 0.7 ? 1 : 0;
  zeus(28, 104 + bob(t, 0, 1.5), 0.95, 1, zp, t);
  if (u > 0.6) {
    var tail = [];
    for (var s = 0; s <= 12; s++) tail.push(pathAt(PATH28, Math.max(0, hk - s * 0.012)));
    tail = tail.map(function (p, i) { return [p[0] + (hash1(i + frameNo(t)) - 0.5) * 2, p[1] + (hash1(i * 5 + frameNo(t)) - 0.5) * 2]; });
    strokePts(tail, 3.2, C.eBlue); strokePts(tail, 1.4, C.goldL); strokePts(tail, 0.6, C.white);
    lighter(); glow(head[0], head[1], 10, C.goldL, 0.8); glow(head[0], head[1], 4, C.white, 1); normalBlend();
  }
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 29 · Shiva slips past
SHOTS[28] = function (u, t) {
  var sk = ramp(u, 0, 3.2);
  var sx = lerp(236, 120, sk), sy = lerp(128, 110, Math.sin(sk * Math.PI) * 0.6 + sk * 0.4);
  var cam = { x: sx + 10, y: 92, z: 1.5 - 0.15 * ramp(u, 3, 5) };
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.violetD });
  // distant rock that gets split (parallax)
  setCam(cam, 0.6);
  var rk = u - 2.4;
  if (rk < 0) slab(40, 70, 26, 0.3, 2901);
  else {
    for (var i = 0; i < 2; i++) slab(40 + (i ? 1 : -1) * 18 * easeOut(clamp01(rk)), 70 + (i ? 6 : -6) * rk, 14, 0.3 + (i ? 1 : -1) * rk, 2902 + i);
    burst(40, 70, rk, 60, 2905, 60, [C.goldL, C.eBlueL, C.white, C.gold], 20, 1.6);
    if (rk < 0.3) { lighter(); glow(40, 70, 40, C.goldW, 1 - rk / 0.3); normalBlend(); }
  }
  setCam(cam, 1);
  // the two fragments forming the gap
  slab(172, 70 + Math.sin(t) * 1.5, 48, 0.25, 2910);
  slab(170, 146 + Math.sin(t + 1) * 1.5, 50, -0.2, 2911);
  // spear passes just behind him
  var pk = (u - 1.1) / 1.3;
  if (pk > 0 && pk < 1.3) spear(380, 108, 40, 70, Math.min(1, pk), 2920, t, 1.2, 0.35);
  var sp = u < 3.2 ? pose(SPOSE, "glide", { lean: -0.05, tri: 1.3 }) : poseMix(SPOSE, "glide", "thrust", ramp(u, 3.2, 3.8));
  sp.triGlow = 0.8; sp.eyes = "glow"; sp.aura = 0.3;
  if (u > 3.8) sp.legs = "wide";
  // turned sideways: a narrower silhouette while passing through the gap
  var side = 1 - 0.35 * pulse(u, 0.6, 2.8);
  shiva(sx, sy, 1.2, -side, sp, t);
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 30 · Trident arc
SHOTS[29] = function (u, t) {
  var cam = camAt([[0, 214, 86, 1.6], [2.0, 170, 80, 1.2], [5, 104, 72, 1.5]], u);
  spaceBg(cam, t, { neb: 1, top: C.void, mid: C.space2, low: C.violetD });
  setCam(cam, 1);
  slab(80, 104, 40, 0.1, 3001);
  slab(232, 130, 44, -0.1, 3002);
  var sp = poseMix(SPOSE, "low", "up", ramp(u, 0.3, 0.9));
  sp.triGlow = 1; sp.eyes = "glow"; sp.aura = 0.5;
  var s = shiva(232, 126, 1.05, -1, sp, t);
  var zx = 80, zy = 100 + bob(t, 0, 1.2);
  zeus(zx, zy, 1.0, 1, pose(ZPOSE, "ready", { legs: "wide", wind: 0.6, eyeGlow: 0.8, charge: 0.5 }), t);
  var cx = zx, cy = zy - 30;
  for (var i = 0; i < 3; i++) {
    var k = ramp(u, 0.8 + i * 0.15, 3.2 + i * 0.15);
    if (k <= 0) continue;
    // each arc travels from the trident tip and wraps around Zeus, leaving the top open
    var r = lerp(140, 30 + i * 9, k);
    var mx = lerp(s.tip[0], cx, Math.min(1, k * 1.4)), my = lerp(s.tip[1], cy, Math.min(1, k * 1.4));
    var spin = t * (1.4 + i * 0.3) * (i % 2 ? -1 : 1);
    var gap = 0.5 + 0.3 * k;
    var a0 = -1.5708 + gap + spin * (1 - k), a1 = -1.5708 + 6.2832 - gap + spin * (1 - k);
    arcS(mx, my, r, a0, a1, 3.2, C.cyan, 0.9);
    arcS(mx, my, r, a0, a1, 1.2, C.cyanW, 1);
  }
  vignette(0.35, "rgba(10,0,30,");
};

// ------------------------------------------------------------------ 31 · Zeus breaks the ring
SHOTS[30] = function (u, t) {
  var zk = ramp(u, 0.5, 4.6);
  var zy = lerp(100, -150, zk), zx = 80;
  var cam = { x: 84, y: Math.min(76, zy - 10 + 30), z: 1.35 };
  stormSky(cam, t, { seed: 9, flash: pulse(u, 0.5, 0.9) });
  setCam(cam, 1);
  // rings closing beneath him and dissolving into sparkles
  var close = ramp(u, 0.6, 1.8);
  for (var i = 0; i < 3; i++) {
    var r = (30 + i * 9) * (1 - 0.85 * close);
    if (close < 1) { arcS(80, 70, r, 0, 6.2832, 2.6, C.cyan, 1 - close); arcS(80, 70, r, 0, 6.2832, 1, C.cyanW, 1 - close); }
  }
  motes(3101, 40, 50, 40, 60, 60, t, [C.cyanW, C.cyanL, C.white], 0, 18, 1.2);
  // spinning ascent with lightning bursting from the shoulders
  var spin = Math.cos(ramp(u, 0.6, 1.8) * 6.2832);
  var p = pose(ZPOSE, "raise", { legs: "fly", lean: 0, wind: 1, eyeGlow: 1, charge: 1 });
  var trail = [];
  for (var s = 0; s < 10; s++) trail.push([zx + (hash1(s + frameNo(t)) - 0.5) * 6, zy + 10 + s * 10]);
  strokePts(trail, 3, C.eBlue); strokePts(trail, 1, C.white);
  zeus(zx, zy, 1.15, spin >= 0 ? Math.max(0.2, spin) : Math.min(-0.2, spin), p, t);
  if (u > 0.7 && u < 2.4) for (var b = 0; b < 4; b++) {
    var ang = b * 1.57 + t * 2;
    lightning(zx, zy - 48, zx + Math.cos(ang) * 50, zy - 48 + Math.sin(ang) * 30, 3110 + b, t, 1.0);
  }
  // the sky fractures into cosmic light
  var fr = ramp(u, 3.6, 5.0);
  if (fr > 0) {
    var top = cam.y - 90 / cam.z;
    for (var c = 0; c < 7; c++) {
      var a = 0.3 + c * 0.42;
      var pts = boltPts(zx, top - 6, zx + Math.cos(a + 3.14) * 160 * fr, top - 6 + Math.sin(a) * 50 * fr + 40 * fr, 3120 + c, 0.3, 0);
      strokePts(pts, 3, C.violet); strokePts(pts, 1.2, C.portal);
    }
    lighter(); glow(zx, top, 80 * fr, C.portal, 0.6 * fr); normalBlend();
  }
  vignette(0.35, "rgba(0,0,20,");
};

// ------------------------------------------------------------------ 32 · The cosmic arena appears
SHOTS[31] = function (u, t) {
  var cam = camAt([[0, 116, 82, 1.15], [5, 206, 86, 0.98]], u);
  cosmicArena(cam, t, {});
  setCam(cam, 1);
  finalPlatform(160, 122, 150, { glowL: 0.6, glowR: 0.6 });
  zeus(40, 106 + bob(t, 0, 1.5), 0.95, 1, pose(ZPOSE, "hover", { wind: 0.5, eyeGlow: 0.5 }), t);
  shiva(282, 108 + bob(t, 2, 1.2), 0.95, -1, pose(SPOSE, "stand", { triGlow: 0.6, eyes: "calm", aura: 0.3 }), t);
  // storm clouds peeling away to the edges
  var peel = ramp(u, 0, 3.4);
  if (peel < 1) {
    setCam(cam, 0.8);
    clouds(-140 - 200 * peel, -40, 220, 220, 3201, STORM_COLS, t, 0, 60);
    clouds(260 + 200 * peel, -40, 220, 220, 3202, STORM_COLS, t, 0, 60);
    clouds(-40, -140 - 120 * peel, 400, 80, 3203, STORM_COLS, t, 0, 60);
  }
  vignette(0.3, "rgba(10,0,30,");
};
