// Zeus vs Shiva — backdrops and set pieces (space, arena, storm, Himalaya, cosmic ocean, hurricane, sphere, portal).

// ------------------------------------------------------------------ space
var STARS = (function () {
  var r = rng(5), a = [];
  for (var i = 0; i < 360; i++) a.push({ x: -520 + r() * 1360, y: -420 + r() * 1020, s: r() < 0.12 ? 2 : 1, c: r() < 0.2 ? C.cyanL : r() < 0.3 ? C.goldW : C.white, ph: r() * 6.28, sp: 1 + r() * 3 });
  return a;
})();
var NEB = (function () {
  var r = rng(17), a = [], cols = [C.nebula, C.nebula2, C.nebPink, C.violet, C.cyanDeep, C.nebula];
  for (var i = 0; i < 26; i++) a.push({ x: -420 + r() * 1160, y: -300 + r() * 780, r: 40 + r() * 110, c: cols[i % cols.length], a: 0.18 + r() * 0.25 });
  return a;
})();
var PLANETS = [
  { x: 40, y: 34, r: 16, c: C.violet, d: C.violetD, ring: true },
  { x: 290, y: 30, r: 7, c: C.cyan, d: C.cyanDeep },
  { x: 250, y: 150, r: 4, c: C.goldL, d: C.amber },
  { x: -120, y: 120, r: 22, c: C.nebPink, d: C.nebula },
  { x: 470, y: 60, r: 12, c: C.oceanL, d: C.ocean },
];
// o: {top, mid, low, neb (0..1), stars (0..1), pull: {x,y,k} distort stars toward a point, planets}
function spaceBg(cam, t, o) {
  o = o || {};
  screen();
  g.fillStyle = vgrad(0, H, [[0, o.top || C.void], [0.55, o.mid || C.space1], [1, o.low || C.space2]]);
  g.fillRect(0, 0, W, H);
  var nebA = o.neb === undefined ? 1 : o.neb;
  if (nebA > 0) {
    setCam(cam, 0.15);
    NEB.forEach(function (b) { glow(b.x, b.y, b.r, b.c, b.a * nebA); });
  }
  var sa = o.stars === undefined ? 1 : o.stars;
  if (sa > 0) {
    setCam(cam, 0.3);
    var pl = o.pull;
    STARS.forEach(function (s, i) {
      var tw = 0.55 + 0.45 * Math.sin(t * s.sp + s.ph);
      if (tw < 0.3 || hash1(i) > sa) return;
      var x = s.x, y = s.y;
      if (pl && pl.k > 0) {
        var dx = pl.x - x, dy = pl.y - y, d = Math.sqrt(dx * dx + dy * dy) + 1;
        var f = pl.k * Math.min(1, 60 / d) * 0.8;
        x += dx * f; y += dy * f;
        if (pl.k > 0.2) line(s.x + (x - s.x) * 0.5, s.y + (y - s.y) * 0.5, x, y, 0.6, C.violetL);
      }
      rect(x, y, s.s, s.s, s.c);
    });
  }
  if (o.planets !== false) {
    setCam(cam, 0.22);
    PLANETS.forEach(function (p) {
      disc(p.x, p.y, p.r, p.d);
      disc(p.x - p.r * 0.25, p.y - p.r * 0.25, p.r * 0.8, p.c);
      if (p.ring) ellS(p.x, p.y, p.r * 1.8, p.r * 0.45, -0.25, 1.6, C.violetL, 0.8);
    });
  }
  setCam(cam, 1);
}

// ------------------------------------------------------------------ floating marble arena
var CRACK_LINES = (function () {
  var r = rng(23), a = [];
  for (var i = 0; i < 16; i++) {
    var ang = r() * 6.2832, x = Math.cos(ang) * 0.15, y = Math.sin(ang) * 0.15, pts = [[x, y]];
    for (var k = 0; k < 6; k++) { ang += (r() - 0.5) * 0.9; x += Math.cos(ang) * 0.07; y += Math.sin(ang) * 0.07; pts.push([x, y]); }
    a.push({ pts: pts, at: r() * 0.8 });
  }
  return a;
})();
function rockUnder(cx, cy, R, seed, depth) {
  var r = rng(seed), pts = [[cx - R, cy]];
  var n = 9;
  for (var i = 1; i < n; i++) {
    var k = i / n, x = cx - R + 2 * R * k;
    var d = Math.sin(k * Math.PI) * R * (depth || 0.75) * (0.75 + r() * 0.4);
    pts.push([x, cy + d]);
  }
  pts.push([cx + R, cy]);
  poly(pts, C.rockD);
  poly(pts.map(function (p, i) { return [cx + (p[0] - cx) * 0.8 - R * 0.1, cy + (p[1] - cy) * 0.75]; }), C.rock);
  // dangling roots of rock
  for (var j = 0; j < 4; j++) {
    var x0 = cx - R * 0.5 + r() * R, y0 = cy + Math.sin((x0 - cx + R) / (2 * R) * Math.PI) * R * 0.5;
    poly([[x0 - 3, y0], [x0 + 3, y0], [x0, y0 + 8 + r() * 10]], C.rockD);
  }
}
// o: {crack 0..1, crackCol, glowL (gold), glowR (cyan), cols: false to hide columns, seed}
function arena(cx, cy, R, o) {
  o = o || {};
  var ry = R * 0.22;
  rockUnder(cx, cy + ry * 0.4, R * 0.98, o.seed || 3, 0.8);
  ell(cx, cy + ry * 0.35, R, ry, 0, C.marbleD);
  ell(cx, cy, R, ry, 0, C.marble);
  ellS(cx, cy, R * 0.86, ry * 0.86, 0, 0.8, C.marbleM);
  ellS(cx, cy, R * 0.62, ry * 0.62, 0, 1.2, C.gold);
  ellS(cx, cy, R * 0.4, ry * 0.4, 0, 0.8, C.marbleM);
  for (var k = 0; k < 12; k++) {
    var a = k / 12 * 6.2832;
    line(cx + Math.cos(a) * R * 0.4, cy + Math.sin(a) * ry * 0.4, cx + Math.cos(a) * R * 0.86, cy + Math.sin(a) * ry * 0.86, 0.6, C.marbleM);
  }
  ell(cx, cy - ry * 0.3, R * 0.7, ry * 0.4, 0, C.marbleW);
  ell(cx, cy, R, ry, 0, "rgba(0,0,0,0)");
  if (o.glowL) { lighter(); glow(cx - R * 0.5, cy, R * 0.7, C.gold, 0.35 * o.glowL); normalBlend(); }
  if (o.glowR) { lighter(); glow(cx + R * 0.5, cy, R * 0.7, C.cyan, 0.35 * o.glowR); normalBlend(); }
  if (o.cols !== false) {
    [3.5, 4.0, 4.6, 5.2, 5.8].forEach(function (a, i) {
      var x = cx + Math.cos(a) * R * 0.92, y = cy + Math.sin(a) * ry * 0.92, h = R * (i % 2 ? 0.22 : 0.34), w = R * 0.07;
      rect(x - w / 2, y - h, w, h, C.marble); rect(x - w / 2, y - h, w * 0.35, h, C.marbleW); rect(x + w * 0.2, y - h, w * 0.3, h, C.marbleM);
      rect(x - w * 0.7, y - h - 2, w * 1.4, 2.4, C.marbleW);
      if (i % 2) poly([[x - w / 2, y - h - 2], [x + w / 2, y - h - 2], [x + w * 0.2, y - h - 5]], C.marble);
    });
  }
  if (o.crack > 0) {
    g.save(); g.beginPath(); g.ellipse(cx, cy, R * 0.97, ry * 0.95, 0, 0, 6.2832); g.clip();
    CRACK_LINES.forEach(function (c) {
      if (c.at > o.crack) return;
      var pts = c.pts.map(function (p) { return [cx + p[0] * R * 0.9, cy + p[1] * ry * 0.9]; });
      strokePts(pts, 1.2, C.marbleD); strokePts(pts, 0.5, o.crackCol || C.goldL);
    });
    g.restore();
  }
}
// a broken fragment / slab of marble floating
function slab(x, y, w, rot, seed, o) {
  o = o || {};
  var r = rng(seed);
  g.save(); g.translate(x, y); g.rotate(rot || 0);
  var h = w * 0.22;
  var pts = [[-w / 2, 0]];
  for (var i = 1; i < 6; i++) pts.push([-w / 2 + w * i / 6, h * (0.5 + r() * 0.9) + w * 0.15 * Math.sin(i / 6 * Math.PI)]);
  pts.push([w / 2, 0]);
  poly(pts, C.rockD);
  poly([[-w / 2, 0], [w / 2, 0], [w / 2 - 1, h * 0.35], [-w / 2 + 1, h * 0.35]], C.marbleD);
  poly([[-w / 2, 0], [-w / 2 + w * 0.08, -h * 0.5], [w / 2 - w * 0.06, -h * 0.55], [w / 2, 0]], C.marble);
  line(-w / 2 + 2, -h * 0.3, w / 2 - 3, -h * 0.34, 0.8, C.marbleW);
  if (o.glow) { lighter(); glow(0, 0, w * 0.6, o.glowCol || C.cyan, 0.35 * o.glow); normalBlend(); }
  g.restore();
}

// ------------------------------------------------------------------ clouds
// billowing cloud mass; cols = [dark, mid, light]
function clouds(x, y, w, h, seed, cols, t, drift, n) {
  var r = rng(seed);
  n = n || Math.round(w / 9);
  var pts = [];
  for (var i = 0; i < n; i++) {
    var px = x + r() * w + (drift || 0) * t * (0.5 + r() * 0.5), py = y + r() * h, rr = 9 + r() * 15;
    pts.push([px, py, rr]);
  }
  pts.forEach(function (p) { disc(p[0], p[1] + 3, p[2], cols[0]); });
  pts.forEach(function (p) { disc(p[0], p[1], p[2] * 0.9, cols[1]); });
  pts.forEach(function (p) { disc(p[0] - p[2] * 0.25, p[1] - p[2] * 0.3, p[2] * 0.5, cols[2]); });
}
var STORM_COLS = [C.stormD, C.storm, C.stormL];
var GOLD_COLS = [C.amber, C.cloudGold, C.goldL];
// storm sky backdrop; o: {gold 0..1 (left warm), cyan 0..1 (right cool), flash, seed, top, low}
function stormSky(cam, t, o) {
  o = o || {};
  screen();
  g.fillStyle = vgrad(0, H, [[0, o.top || C.void], [0.5, C.stormD], [1, o.low || C.storm]]);
  g.fillRect(0, 0, W, H);
  setCam(cam, 0.3);
  clouds(-200, -60, 720, 50, (o.seed || 1) + 1, STORM_COLS, t, 3, 70);
  setCam(cam, 0.55);
  clouds(-220, 120, 760, 60, (o.seed || 1) + 2, STORM_COLS, t, -4, 80);
  if (o.flash > 0) { screen(); g.globalAlpha = clamp01(o.flash) * 0.5; g.fillStyle = C.eBlueL; g.fillRect(0, 0, W, H); g.globalAlpha = 1; }
  setCam(cam, 1);
}
// golden storm (Zeus's sky)
function goldSky(cam, t, o) {
  o = o || {};
  screen();
  g.fillStyle = vgrad(0, H, [[0, C.space2], [0.45, C.nebula], [0.8, C.amber], [1, C.cloudGold]]);
  g.fillRect(0, 0, W, H);
  setCam(cam, 0.25);
  clouds(-200, -70, 720, 60, 31, GOLD_COLS, t, 4, 80);
  setCam(cam, 0.5);
  clouds(-220, 130, 760, 50, 32, [C.nebula, C.amber, C.cloudGold], t, -5, 70);
  if (o.flash > 0) { screen(); g.globalAlpha = clamp01(o.flash) * 0.55; g.fillStyle = C.goldW; g.fillRect(0, 0, W, H); g.globalAlpha = 1; }
  setCam(cam, 1);
}

// ------------------------------------------------------------------ Himalaya
function himalaya(cam, t, o) {
  o = o || {};
  screen();
  g.fillStyle = vgrad(0, H, [[0, C.void], [0.5, C.skyN], [1, C.violetD]]);
  g.fillRect(0, 0, W, H);
  setCam(cam, 0.15);
  NEB.slice(0, 8).forEach(function (b) { glow(b.x * 0.5 + 100, b.y * 0.4, b.r, b.c, b.a * 0.6); });
  setCam(cam, 0.25);
  STARS.forEach(function (s, i) { if (Math.sin(t * s.sp + s.ph) > -0.4 && s.y < 200) rect(s.x * 0.6 + 80, s.y * 0.5 + 10, s.s, s.s, s.c); });
  // far range
  setCam(cam, 0.45);
  poly([[-200, 200], [-140, 120], [-90, 150], [-30, 100], [30, 140], [80, 96], [130, 140], [190, 90], [250, 135], [310, 100], [380, 140], [460, 110], [540, 200]], C.mountainD);
  // mid range with snow caps
  setCam(cam, 0.7);
  var mid = [[-160, 230], [-100, 140], [-50, 170], [10, 120], [60, 160], [240, 150], [290, 115], [350, 160], [420, 130], [500, 230]];
  poly(mid, C.mountain);
  [[-100, 140], [10, 120], [290, 115], [420, 130]].forEach(function (p) { poly([[p[0] - 12, p[1] + 12], [p[0], p[1]], [p[0] + 12, p[1] + 12], [p[0] + 4, p[1] + 9], [p[0] - 3, p[1] + 13]], C.snowShade); });
  // the peak (Shiva's seat) in world space
  setCam(cam, 1);
  var px = o.px || 160, py = o.py || 120;
  poly([[px - 120, py + 160], [px - 40, py + 30], [px - 14, py + 4], [px, py], [px + 16, py + 6], [px + 50, py + 40], [px + 130, py + 160]], C.snowShade);
  poly([[px - 100, py + 160], [px - 36, py + 34], [px - 12, py + 6], [px, py + 2], [px + 10, py + 8], [px + 20, py + 30], [px - 4, py + 60], [px - 30, py + 160]], C.snow);
  poly([[px + 20, py + 30], [px + 50, py + 40], [px + 40, py + 80], [px + 10, py + 70]], C.mountain);
  // drifting cloud band
  clouds(px - 260, py + 40, 520, 20, 41, [C.snowShade, C.paleBlue, C.white], t, 6, 50);
}

// ------------------------------------------------------------------ cosmic ocean
function ocean(cam, t, o) {
  o = o || {};
  var hy = o.hy === undefined ? 100 : o.hy;
  spaceBg(cam, t, { neb: 0.8, planets: o.planets });
  setCam(cam, 1);
  g.fillStyle = vgrad(hy, hy + 260, [[0, C.oceanL], [0.15, C.ocean], [0.6, C.oceanD], [1, C.void]]);
  g.fillRect(-600, hy, 1600, 600);
  line(-600, hy, 1000, hy, 1.2, C.cyanL);
  // wave rows with perspective spacing
  for (var row = 0; row < 14; row++) {
    var y = hy + 2 + row * row * 1.6 + row * 2;
    var amp = 0.6 + row * 0.35, len = 14 + row * 5, sp = 10 + row * 2;
    g.strokeStyle = row % 3 === 0 ? C.foam : C.oceanL; g.lineWidth = 0.6 + row * 0.12;
    g.beginPath();
    for (var x = -600; x <= 1000; x += 4) {
      var yy = y + Math.sin((x + t * sp) / len * 6.28 + row) * amp;
      if (x === -600) g.moveTo(x, yy); else g.lineTo(x, yy);
    }
    g.stroke();
  }
  // star reflections
  for (var i = 0; i < 40; i++) {
    var sx = -200 + hash1(i * 3.3) * 720, sy = hy + 4 + hash1(i * 7.1) * 60;
    if (Math.sin(t * 4 + i) > 0.2) rect(sx, sy, 2, 1, C.cyanW);
  }
}
// tall rising wave wall / curl; k = height 0..1
function waveWall(x, by, w, h, t, seed, foamK, curl) {
  if (h <= 1) return;
  var r = rng(seed);
  curl = curl === undefined ? 1 : curl;
  w = Math.max(w, h * 0.9);
  var pts = [[x - w / 2, by]];
  for (var i = 0; i <= 12; i++) {
    var k = i / 12, kk = curl > 0 ? Math.pow(k, 0.75) : 1 - Math.pow(1 - k, 0.75), px = x - w / 2 + w * k;
    var top = by - h * Math.pow(Math.sin(kk * Math.PI), 0.8) * (0.92 + 0.08 * Math.sin(t * 3 + i + r()));
    pts.push([px, top]);
  }
  pts.push([x + w / 2, by]);
  // curling lip at the crest
  var ci = curl > 0 ? 9 : 3, cp = pts[ci + 1];
  var lip = [[cp[0] - 6 * curl, cp[1] + 1], [cp[0] + 10 * curl, cp[1] - 2], [cp[0] + 16 * curl, cp[1] + 8], [cp[0] + 6 * curl, cp[1] + 4]];
  poly(pts, C.oceanD);
  poly(pts.map(function (p) { return [x + (p[0] - x) * 0.85, by + (p[1] - by) * 0.94]; }), C.ocean);
  poly(pts.map(function (p) { return [x + (p[0] - x) * 0.55 - w * 0.08, by + (p[1] - by) * 0.85]; }), C.oceanL);
  for (var sb = 1; sb <= 3; sb++) {
    var band_ = pts.slice(1, -1).map(function (p) { return [x + (p[0] - x) * (1 - sb * 0.18), by + (p[1] - by) * (1 - sb * 0.2)]; });
    alpha(0.7, function () { strokePts(band_, 1, sb % 2 ? C.oceanL : C.cyanL); });
  }
  strokePts(pts.slice(2, -2), 2.4, C.foam);
  poly(lip, C.oceanL); poly(lip.map(function (p) { return [p[0], p[1] - 1.5]; }).slice(0, 3), C.foam);
  // foam crest
  for (var j = 1; j < pts.length - 1; j++) {
    rect(pts[j][0] - 2, pts[j][1] - 1, 5, 2.2, C.foam);
    if ((foamK || 1) > 0.5 && hash1(j + Math.floor(t * 8)) > 0.4) rect(pts[j][0] + (hash1(j * 3 + Math.floor(t * 8)) - 0.5) * 8, pts[j][1] - 3 - hash1(j) * 4, 1.4, 1.4, C.white);
  }
  // streaks
  for (var s = 0; s < 6; s++) {
    var sx = x - w * 0.35 + w * 0.7 * (s / 5), sy = by - h * (0.2 + 0.5 * hash1(s + seed));
    line(sx, sy, sx + 2, sy + 10, 0.8, C.cyanL);
  }
}
function spray(x, y, k, n, seed, spread) {
  burst(x, y, k, n, seed, spread || 50, [C.foam, C.cyanL, C.white, C.oceanL], 40, 1.6);
}

// ------------------------------------------------------------------ hurricane (overhead)
function hurricane(cx, cy, R, rot, t, o) {
  o = o || {};
  var layers = [[C.stormD, 1.0, 2], [C.storm, 0.75, 0], [C.stormL, 0.38, -2], [C.paleBlue, 0.12, -3]];
  layers.forEach(function (L) {
    for (var arm = 0; arm < 4; arm++) {
      g.strokeStyle = L[0]; g.lineCap = "round";
      for (var j = 60; j > 3; j--) {
        var k = j / 60, k2 = (j - 1) / 60, a = rot + arm * 1.5708 + k * 4.2, a2 = rot + arm * 1.5708 + k2 * 4.2;
        g.lineWidth = (8 + 34 * k) * L[1];
        g.beginPath();
        g.moveTo(cx + Math.cos(a) * R * k, cy + Math.sin(a) * R * k * (o.squash || 1) + L[2]);
        g.lineTo(cx + Math.cos(a2) * R * k2, cy + Math.sin(a2) * R * k2 * (o.squash || 1) + L[2]);
        g.stroke();
      }
    }
  });
  // eye wall lightning ring
  if (o.eye !== false) {
    disc(cx, cy, R * 0.12, C.oceanD);
    for (var b = 0; b < 3; b++) {
      var a0 = rot * 2 + b * 2.1 + t * 3, a1 = a0 + 0.9;
      lightning(cx + Math.cos(a0) * R * 0.16, cy + Math.sin(a0) * R * 0.16 * (o.squash || 1), cx + Math.cos(a1) * R * 0.16, cy + Math.sin(a1) * R * 0.16 * (o.squash || 1), 300 + b, t, 0.9);
    }
  }
}

// ------------------------------------------------------------------ cosmic arena (final stage)
var ARCHES = [[-60, 120, 46], [60, 60, 30], [250, 50, 34], [380, 110, 50], [140, 20, 22]];
var FISSURES = (function () {
  var r = rng(61), a = [];
  for (var i = 0; i < 7; i++) {
    var x = -150 + r() * 620, y = -60 + r() * 220, pts = [[x, y]], ang = r() * 6.28;
    for (var k = 0; k < 7; k++) { ang += (r() - 0.5) * 1.2; x += Math.cos(ang) * 10; y += Math.sin(ang) * 10; pts.push([x, y]); }
    a.push(pts);
  }
  return a;
})();
function cosmicArena(cam, t, o) {
  o = o || {};
  spaceBg(cam, t, { neb: 1, pull: o.pull, top: C.void, mid: C.space2, low: C.nebula });
  setCam(cam, 0.35);
  FISSURES.forEach(function (pts, i) {
    lighter(); glow(pts[3][0], pts[3][1], 26, C.violet, 0.3); normalBlend();
    strokePts(pts, 2.4, C.violet); strokePts(pts, 1, C.violetL);
  });
  setCam(cam, 0.55);
  ARCHES.forEach(function (a, i) {
    var x = a[0], y = a[1], r = a[2];
    g.strokeStyle = C.marbleD; g.lineWidth = r * 0.28; g.beginPath(); g.arc(x, y, r, Math.PI, 0); g.stroke();
    g.strokeStyle = C.marbleM; g.lineWidth = r * 0.16; g.beginPath(); g.arc(x, y - 1, r, Math.PI, 0); g.stroke();
    rect(x - r - r * 0.14, y, r * 0.28, r * 0.6, C.marbleD); rect(x + r - r * 0.14, y, r * 0.28, r * 0.4, C.marbleD);
    rockUnder(x, y + r * 0.6, r * 1.2, 70 + i, 0.5);
  });
  setCam(cam, 1);
}
// final platform (long, flat) at world (cx,cy)
function finalPlatform(cx, cy, R, o) {
  arena(cx, cy, R, { cols: false, glowL: (o && o.glowL) || 0, glowR: (o && o.glowR) || 0, crack: (o && o.crack) || 0, crackCol: C.violetL, seed: 9 });
}

// ------------------------------------------------------------------ the energy sphere
// bal: -1 all gold .. 0 even .. 1 all cyan; k: intensity 0..1
function energySphere(x, y, r, t, bal, k, o) {
  o = o || {};
  lighter();
  glow(x, y, r * 3.2, C.goldW, 0.3 * k);
  glow(x - r * 0.6, y, r * 2.2, C.gold, 0.35 * k * (1 - bal) * 0.6);
  glow(x + r * 0.6, y, r * 2.2, C.cyan, 0.35 * k * (1 + bal) * 0.6);
  normalBlend();
  var split = x + bal * r * 0.9 + Math.sin(t * 23) * r * 0.06;
  g.save(); g.beginPath(); g.rect(x - r * 2, y - r * 2, split - (x - r * 2), r * 4); g.clip();
  disc(x, y, r, o.flick === 1 ? C.eBlue : C.gold); disc(x, y, r * 0.75, C.goldL);
  g.restore();
  g.save(); g.beginPath(); g.rect(split, y - r * 2, r * 4, r * 4); g.clip();
  disc(x, y, r, o.flick === 2 ? C.violet : C.cyan); disc(x, y, r * 0.75, C.cyanL);
  g.restore();
  disc(x, y, r * 0.42, C.white);
  // swirling surface bands
  for (var i = 0; i < 3; i++) arcS(x, y, r * (0.55 + i * 0.15), t * (3 + i) + i * 2, t * (3 + i) + i * 2 + 1.6, 1, i === 1 ? C.violetL : C.white, 0.7);
  if (o.seam > 0) { line(x - r * 1.1, y, x + r * 1.1, y, 1.2 * o.seam, C.white); lighter(); glow(x, y, r * 1.4, C.white, 0.6 * o.seam); normalBlend(); }
}

// ------------------------------------------------------------------ the fissure / portal and the unknown shadow
function fissureShape(x, y, h, wdt, t) {
  var pts = [];
  var n = 10;
  for (var i = 0; i <= n; i++) { var k = i / n; pts.push([x - wdt * Math.sin(k * Math.PI) * (0.7 + 0.3 * hash1(i * 5.1)) + (hash1(i) - 0.5) * 3, y - h / 2 + h * k]); }
  for (var j = n; j >= 0; j--) { var k2 = j / n; pts.push([x + wdt * Math.sin(k2 * Math.PI) * (0.7 + 0.3 * hash1(j * 2.7)) + (hash1(j) - 0.5) * 3, y - h / 2 + h * k2]); }
  return pts;
}
function fissure(x, y, h, wdt, t, k, inner) {
  lighter();
  glow(x, y, h * 0.7, C.portalV, 0.35 * k);
  glow(x, y, h * 0.35, C.portal, 0.4 * k);
  normalBlend();
  var pts = fissureShape(x, y, h, Math.max(wdt, 0.6), t);
  poly(pts, C.portalV);
  poly(fissureShape(x, y, h * 0.92, Math.max(wdt * 0.7, 0.4), t), C.portal);
  if (wdt > 3) poly(fissureShape(x, y, h * 0.8, wdt * 0.45, t), C.white);
  if (inner) { g.save(); g.beginPath(); pts.forEach(function (p, i) { if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); }); g.closePath(); g.clip(); inner(); g.restore(); }
}
// abstract silhouette (no identity) — a towering dark mass with shifting tendrils
function shadowMass(x, y, sc, t, a) {
  g.globalAlpha = clamp01(a);
  ell(x, y, 26 * sc, 34 * sc, 0, C.shadow);
  ell(x, y - 30 * sc, 16 * sc, 14 * sc, 0, C.shadow);
  ell(x - 26 * sc, y - 8 * sc, 20 * sc, 12 * sc, 0.5, C.shadow);
  ell(x + 26 * sc, y - 8 * sc, 20 * sc, 12 * sc, -0.5, C.shadow);
  for (var i = 0; i < 7; i++) {
    var a0 = -2.6 + i * 0.85 + Math.sin(t * 1.5 + i) * 0.2;
    line(x, y - 10 * sc, x + Math.cos(a0) * 50 * sc, y - 10 * sc + Math.sin(a0) * 46 * sc, (5 - Math.abs(i - 3)) * sc + 1, C.shadow);
  }
  g.globalAlpha = 1;
}
function rays(cx, cy, t, n, col, a, len) {
  g.globalAlpha = clamp01(a);
  for (var i = 0; i < n; i++) {
    var an = i * 6.2832 / n + t * 0.3;
    poly([[cx, cy], [cx + Math.cos(an) * (len || 400), cy + Math.sin(an) * (len || 400)], [cx + Math.cos(an + 0.1) * (len || 400), cy + Math.sin(an + 0.1) * (len || 400)]], col);
  }
  g.globalAlpha = 1;
}
