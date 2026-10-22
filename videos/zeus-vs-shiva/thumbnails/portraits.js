// Close-up pixel portraits of Zeus and Shiva for the YouTube thumbnails (480x270 world, 4x upscale).
// Busts are drawn front-on in local units around the face centre (head ~80 units tall), for a figure
// standing on the LEFT of frame: +x is the "inner" side that faces the opponent and takes the rim light.
// Mirror with dir = -1 for a figure on the right.

C.zSkinL = "#ffd2a8"; C.zSkinDD = "#7a3a28"; C.zHairD = "#7a7e9a"; C.mouth = "#4a0a18";
C.sSkinDD = "#10286a"; C.neel = "#22248a"; C.snakeL = "#8ae89a"; C.beadsL = "#c87a3a"; C.flame = "#ff8a2a"; C.jataH = "#86569a";

// ------------------------------------------------------------------ sprite with a crisp 1px dark outline
var SPR = document.createElement("canvas"); SPR.width = W; SPR.height = H;
var sprCtx = SPR.getContext("2d", { willReadFrequently: true });
var TNT = document.createElement("canvas"); TNT.width = W; TNT.height = H;
var tntCtx = TNT.getContext("2d");
function sprite(fn, outline) { renderSprite(fn, outline); blitSprite(); }
function renderSprite(fn, outline) {
  var main = g;
  g = sprCtx;
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = "source-over"; g.globalAlpha = 1;
  g.clearRect(0, 0, W, H);
  fn();
  g.setTransform(1, 0, 0, 1, 0, 0);
  g = main;
  var img = sprCtx.getImageData(0, 0, W, H), d = img.data;
  for (var i = 3; i < d.length; i += 4) d[i] = d[i] > 90 ? 255 : 0; // hard pixel edges
  sprCtx.putImageData(img, 0, 0);
  tntCtx.setTransform(1, 0, 0, 1, 0, 0); tntCtx.globalCompositeOperation = "source-over";
  tntCtx.clearRect(0, 0, W, H);
  tntCtx.drawImage(SPR, 0, 0);
  tntCtx.globalCompositeOperation = "source-in"; tntCtx.fillStyle = outline || C.ink; tntCtx.fillRect(0, 0, W, H);
  tntCtx.globalCompositeOperation = "source-over";
}
function blitSprite() {
  var main = g;
  main.save(); main.setTransform(1, 0, 0, 1, 0, 0); main.globalAlpha = 1; main.globalCompositeOperation = "source-over";
  [[-1, 0], [1, 0], [0, -1], [0, 1]].forEach(function (o) { main.drawImage(TNT, o[0], o[1]); });
  main.drawImage(SPR, 0, 0);
  main.restore();
}
// local -> world for a bust placed at (x,y), scale s, mirror dir
function bustPt(x, y, s, dir, lx, ly) { return [x + lx * s * dir, y + ly * s]; }

// ------------------------------------------------------------------ limbs, hands, weapons
function seg(x1, y1, x2, y2, w1, w2, col) {
  var dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) + 1e-3, nx = -dy / L, ny = dx / L;
  poly([[x1 + nx * w1 / 2, y1 + ny * w1 / 2], [x2 + nx * w2 / 2, y2 + ny * w2 / 2], [x2 - nx * w2 / 2, y2 - ny * w2 / 2], [x1 - nx * w1 / 2, y1 - ny * w1 / 2]], col);
  disc(x1, y1, w1 / 2, col); disc(x2, y2, w2 / 2, col);
}
// tapered, muscled two-segment arm from shoulder (sx,sy) to hand (hx,hy); lit strip on the +x side
function arm(sx, sy, hx, hy, bend, wU, wF, col, colD, colL) {
  var mx = (sx + hx) / 2, my = (sy + hy) / 2, dx = hx - sx, dy = hy - sy, L = Math.hypot(dx, dy) + 0.01;
  var ex = mx - dy / L * bend, ey = my + dx / L * bend;
  seg(sx, sy, ex, ey, wU + 5, wU * 0.8 + 4, colD);
  seg(ex, ey, hx, hy, wF + 4, wF * 0.7 + 4, colD);
  seg(sx, sy, ex, ey, wU, wU * 0.8, col);
  seg(ex, ey, hx, hy, wF, wF * 0.7, col);
  var ua = Math.atan2(ey - sy, ex - sx), fa = Math.atan2(hy - ey, hx - ex);
  ell(sx + (ex - sx) * 0.45, sy + (ey - sy) * 0.45, Math.hypot(ex - sx, ey - sy) * 0.32, wU * 0.56, ua, col);
  ell(ex + (hx - ex) * 0.3, ey + (hy - ey) * 0.3, Math.hypot(hx - ex, hy - ey) * 0.28, wF * 0.54, fa, col);
  if (colL) {
    [[sx, sy, ex, ey, wU], [ex, ey, hx, hy, wF * 0.85]].forEach(function (q) {
      var ddx = q[2] - q[0], ddy = q[3] - q[1], LL = Math.hypot(ddx, ddy) + 1e-3, nx = -ddy / LL, ny = ddx / LL;
      if (nx < 0) { nx = -nx; ny = -ny; }
      var o = q[4] * 0.26;
      line(q[0] + nx * o, q[1] + ny * o, q[2] + nx * o, q[3] + ny * o, q[4] * 0.26, colL);
    });
  }
  return [ex, ey];
}
function fist(x, y, ang, r, col, colD, colL) {
  g.save(); g.translate(x, y); g.rotate(ang);
  rrect(-r - 1.2, -r * 0.9 - 1.2, r * 2 + 2.4, r * 1.8 + 2.4, r * 0.55, colD);
  rrect(-r, -r * 0.9, r * 2, r * 1.8, r * 0.5, col);
  for (var k = -1; k <= 1; k++) line(r * 0.1, k * r * 0.5, r * 0.9, k * r * 0.5, 0.9, colD);
  ell(-r * 0.35, r * 0.6, r * 0.6, r * 0.34, -0.25, colL || col);
  g.restore();
}
function bracer(el, hand) {
  var a0 = [lerp(el[0], hand[0], 0.32), lerp(el[1], hand[1], 0.32)], a1 = [lerp(el[0], hand[0], 0.74), lerp(el[1], hand[1], 0.74)];
  line(a0[0], a0[1], a1[0], a1[1], 15, C.goldD); line(a0[0], a0[1], a1[0], a1[1], 12, C.gold);
  line(a0[0] + 3, a0[1], a1[0] + 3, a1[1], 3, C.goldL);
}
// Zeus's thunderbolt as a bold double-ended zigzag (rot 0 = upright), gripped at its centre
var ZAP = [[6, -50], [-12, -2], [2, -6], [-6, 50], [12, 2], [-2, 6]];
function boltIcon(x, y, rot, sc, grip) {
  grip = grip || 0;
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(sc, sc); g.translate(0, -grip);
  g.beginPath(); ZAP.forEach(function (p, i) { if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); }); g.closePath();
  g.lineJoin = "miter"; g.miterLimit = 6; g.strokeStyle = C.goldD; g.lineWidth = 4; g.stroke();
  g.fillStyle = C.gold; g.fill();
  strokePts([[5, -46], [-6, -3], [6, 3], [-5, 46]], 3, C.goldL);
  strokePts([[5, -44], [-5, -3], [5, 3], [-4, 44]], 1.2, C.white);
  g.restore();
  function R(p) { var c = Math.cos(rot), s = Math.sin(rot), py = p[1] - grip; return [x + (p[0] * c - py * s) * sc, y + (p[0] * s + py * c) * sc]; }
  return { top: R([6, -50]), bottom: R([-6, 50]), mid: R([0, 0]) };
}
// Shiva's trishul (solid part only); shaft along angle a (A() convention) through the grip point (x,y)
function trishulShape(x, y, a, sc, below, above) {
  var d = A(a), nx = d[1], ny = -d[0];
  function P(u_, v) { return [x + (d[0] * u_ + nx * v) * sc, y + (d[1] * u_ + ny * v) * sc]; }
  var b0 = P(-below, 0), top = P(above, 0);
  line(b0[0], b0[1], top[0], top[1], 4 * sc, C.goldD);
  line(b0[0], b0[1], top[0], top[1], 2 * sc, C.gold);
  var dm = P(above - 9, 0);
  poly([P(above - 15, -6), P(above - 15, 6), dm], C.beads); poly([P(above - 3, -6), P(above - 3, 6), dm], C.beads);
  poly([P(above - 14, -5), P(above - 14, 1), dm], C.beadsL);
  var r1 = P(above - 10, 8), r2 = P(above - 19, 13);
  line(dm[0], dm[1], r1[0], r1[1], 1.6 * sc, C.tilak); line(r1[0], r1[1], r2[0], r2[1], 1.6 * sc, C.tilak);
  var c1 = P(above, -12), c2 = P(above, 12);
  line(c1[0], c1[1], c2[0], c2[1], 3.4 * sc, C.cyanL);
  poly([P(above, -2.6), P(above, 2.6), P(above + 26, 0)], C.cyanW);
  poly([P(above, -12), P(above, -7.5), P(above + 11, -9.5), P(above + 22, -15), P(above + 14, -15.5)], C.cyanW);
  poly([P(above, 12), P(above, 7.5), P(above + 11, 9.5), P(above + 22, 15), P(above + 14, 15.5)], C.cyanW);
  line(P(above, 0)[0], P(above, 0)[1], P(above + 22, 0)[0], P(above + 22, 0)[1], 0.9 * sc, C.cyanL);
  return { tip: P(above + 26, 0), head: P(above + 8, 0) };
}
// curved gold shoulder plate
function pauldron(cx, cy, sd, lit) {
  var cm = lit ? C.gold : C.amber, cl = lit ? C.goldL : C.gold;
  function P(p) { return [cx + p[0] * sd, cy + p[1]]; }
  var shape = [[-24, -2], [-16, -15], [-2, -21], [14, -18], [25, -7], [30, 8], [27, 22], [14, 21], [-2, 14], [-15, 8]];
  poly(shape.map(P), C.goldD);
  poly(shape.map(function (p) { return P([p[0] * 0.86 + 1, p[1] * 0.84 - 1]); }), cm);
  var ox = cx - sd * 8, oy = cy + 18, a0 = sd > 0 ? -2.45 : -Math.PI + 0.35, a1 = sd > 0 ? -0.35 : -Math.PI + 2.45;
  arcS(ox, oy, 31, a0, a1, 1.8, C.goldD, 1);
  arcS(ox, oy, 23, a0 + 0.15 * sd, a1 - 0.1 * sd, 1.6, C.goldD, 1);
  arcS(ox, oy, 34, sd > 0 ? -2.0 : -Math.PI + 0.6, sd > 0 ? -0.6 : -Math.PI + 2.0, 1.4, cl, 1);
  disc(cx + sd * 4, cy - 1, 5.5, C.goldD); disc(cx + sd * 4, cy - 1, 4, cl); disc(cx + sd * 4 + 1, cy - 2, 1.4, C.goldW);
}

// ------------------------------------------------------------------ ZEUS bust
// o: weapon 'raise' (bolt raised on the outer side) | 'thrust' (bolt driven at o.target) | 'none'
//    look (-1..1 iris shift toward the inner side), mouth (0 closed .. 1 battle cry), dirv (thrust direction)
function zeusBust(x, y, s, dir, o) {
  o = o || {};
  var look = o.look === undefined ? 0.6 : o.look, mouth = o.mouth === undefined ? 0.7 : o.mouth;
  var info = {};
  function W2(lx, ly) { return bustPt(x, y, s, dir, lx, ly); }
  g.save(); g.translate(x, y); g.scale(dir * s, s);
  // cape behind the shoulders
  poly([[-56, 42], [56, 42], [118, 220], [-118, 220]], C.capeD);
  poly([[-20, 42], [56, 42], [118, 220], [10, 220]], C.cape);
  // mane: a wavy cloud of white hair, blown toward the outer side
  var hp = [];
  for (var i = 0; i < 60; i++) {
    var a = i / 60 * 6.2832, r = 1 + 0.07 * Math.sin(a * 9) + 0.04 * Math.sin(a * 5 + 1);
    var bx = Math.cos(a) * 46 * r - 5 - (Math.cos(a) < 0 ? 8 * Math.max(0, -Math.cos(a)) : 0);
    hp.push([bx, -8 + Math.sin(a) * 54 * r]);
  }
  poly(hp, C.zHairD);
  poly(hp.map(function (p) { return [p[0] * 0.92 + 3, p[1] * 0.94 - 1]; }), C.zHairShade);
  poly(hp.map(function (p) { return [p[0] * 0.84 + 6, p[1] * 0.88 - 4]; }), C.zHair);
  [[-40, -34, -76, -46, -60, -26], [-46, -8, -84, -10, -64, 6], [-42, 18, -76, 30, -54, 30]].forEach(function (q) {
    poly([[q[0], q[1] - 7], [q[2], q[3]], [q[4], q[5]], [q[0], q[1] + 7]], C.zHairShade);
    line(q[0] + 2, q[1], q[2] + 6, q[3] + 2, 1, C.zHairD);
  });
  for (var st = 0; st < 7; st++) { var sa = 3.5 + st * 0.32; arcS(-4, -8, 40, sa, sa + 0.22, 1, C.zHairD, 1); }
  // weapon arm on the outer side, raised high (behind the torso so the shoulder hides the joint)
  if (o.weapon === "raise") {
    var hand = [-88, -34];
    var b = boltIcon(hand[0], hand[1], 0.32, 0.95, 20);
    info.tip = W2(b.top[0], b.top[1]); info.mid = W2(b.mid[0], b.mid[1]); info.tail = W2(b.bottom[0], b.bottom[1]);
    var el = arm(-64, 66, hand[0], hand[1] + 4, -14, 19, 15, C.zSkin, C.zSkinDD, C.zSkinL);
    bracer(el, hand);
    fist(hand[0], hand[1], -1.4, 8, C.zSkin, C.zSkinDD, C.zSkinL);
  }
  // neck
  poly([[-17, 14], [17, 14], [22, 50], [-22, 50]], C.zSkinD);
  poly([[-3, 14], [17, 14], [22, 50], [2, 50]], C.zSkin);
  // torso
  poly([[-24, 40], [24, 40], [62, 52], [86, 72], [96, 110], [100, 220], [-100, 220], [-96, 110], [-86, 72], [-62, 52]], C.zSkinD);
  poly([[0, 40], [24, 40], [62, 52], [86, 72], [96, 110], [100, 220], [0, 220]], C.zSkin);
  poly([[34, 70], [72, 76], [86, 104], [52, 108]], C.zSkinL);
  line(-44, 110, -8, 118, 1.6, C.zSkinDD); line(8, 118, 44, 110, 1.6, C.zSkinDD);
  line(0, 120, 0, 160, 1.2, C.zSkinDD);
  // toga sash over the outer shoulder
  poly([[-74, 50], [-42, 42], [72, 220], [28, 220]], C.ivoryShade);
  poly([[-64, 50], [-44, 45], [66, 220], [40, 220]], C.ivory);
  for (var k = 0; k < 4; k++) line(-58 + k * 6, 58, 30 + k * 8, 216, 0.9, C.ivoryShade);
  // weapon arm driving the bolt at a target (in front of the torso, under the shoulder guard)
  if (o.weapon === "thrust") {
    var tg = o.target || [118, -10], dv = o.dirv || [0.62, -0.78], bs = 1.0, gr = 22;
    var hand2 = [tg[0] - dv[0] * (50 + gr) * bs, tg[1] - dv[1] * (50 + gr) * bs];
    var el2 = arm(64, 66, hand2[0], hand2[1], 16, 19, 15, C.zSkin, C.zSkinDD, C.zSkinL);
    bracer(el2, hand2);
    var b2 = boltIcon(hand2[0], hand2[1], Math.atan2(dv[0], -dv[1]), bs, gr);
    info.tip = W2(b2.top[0], b2.top[1]); info.mid = W2(b2.mid[0], b2.mid[1]); info.tail = W2(b2.bottom[0], b2.bottom[1]);
    fist(hand2[0], hand2[1], Math.atan2(dv[1], dv[0]), 8, C.zSkin, C.zSkinDD, C.zSkinL);
  }
  // gold pauldrons + brooch
  pauldron(-76, 72, -1, false);
  pauldron(76, 72, 1, true);
  disc(-48, 52, 8, C.goldD); disc(-48, 52, 6, C.gold); disc(-48, 52, 3, C.tilak); rect(-49, 50, 1.4, 1.4, C.white);
  // face, with sockets, lit cheek and an inner rim light
  ell(0, -6, 25, 31, 0, C.zSkinD);
  ell(3, -7, 22, 28, 0, C.zSkin);
  ell(13, -1, 7, 10, 0, C.zSkinL);
  ell(-12, -4, 9, 4.8, 0, C.zSkinD); ell(12, -4, 8.5, 4.6, 0, C.zSkinD);
  arcS(3, -7, 21.5, -1.25, 0.95, 1.6, C.zSkinL, 1);
  // beard
  var bd = [[-27, -2], [-32, 16], [-29, 36], [-23, 54], [-13, 68], [-5, 80], [2, 86], [9, 78], [17, 66], [25, 50], [31, 30], [32, 10], [27, -2]];
  poly(bd, C.zHairD);
  poly(bd.map(function (p) { return [p[0] * 0.9 + 2, p[1] * 0.95]; }), C.zHairShade);
  poly(bd.map(function (p) { return [p[0] * 0.78 + 6, p[1] * 0.92]; }), C.zHair);
  for (var sk = -3; sk <= 3; sk++) {
    g.strokeStyle = sk < 0 ? C.zHairD : C.zHairShade; g.lineWidth = 1;
    g.beginPath(); g.moveTo(sk * 7, 24); g.quadraticCurveTo(sk * 8 + 3, 50, sk * 4 + 2, 74 - Math.abs(sk) * 5); g.stroke();
  }
  // mouth: battle cry
  if (mouth > 0.05) {
    var mh = 2 + 6 * mouth;
    ell(1, 17 + mh * 0.45, 8.5, mh * 0.6 + 1, 0, C.mouth);
    rect(-6, 15.6, 13, 2, C.white);
    if (mouth > 0.5) rect(-4, 17 + mh * 0.9 - 1, 10, 1.4, C.ivoryShade);
  }
  // moustache
  poly([[0, 11], [-6, 12], [-15, 16], [-24, 25], [-19, 26], [-10, 20], [-2, 16]], C.zHairShade);
  poly([[0, 11], [6, 12], [15, 16], [24, 25], [19, 26], [10, 20], [2, 16]], C.zHair);
  // nose
  poly([[-1, -8], [-4, 4], [-6, 9], [-2, 11], [0, 8]], C.zSkinD);
  line(2.5, -8, 4, 5, 1.3, C.zSkinL);
  poly([[-6, 9], [6, 9], [4, 12], [-4, 12]], C.zSkinD);
  rect(-4, 10, 2, 1.4, C.zSkinDD); rect(2.5, 10, 2, 1.4, C.zSkinDD);
  // hair over the forehead
  poly([[-27, -18], [-23, -34], [-12, -41], [0, -43], [12, -41], [23, -34], [27, -18], [21, -27], [10, -31], [0, -30], [-10, -31], [-21, -27]], C.zHair);
  line(-20, -28, -8, -33, 1, C.zHairShade); line(20, -28, 8, -33, 1, C.zHairShade);
  // forehead lines + frown
  line(-10, -23, 10, -23, 0.9, C.zSkinD); line(-6, -26, 6, -26, 0.9, C.zSkinD);
  line(-2, -14, -1, -8, 1, C.zSkinDD); line(2, -14, 1, -8, 1, C.zSkinDD);
  // brows: thick, white, angled down to the centre
  poly([[-26, -15], [-19, -20], [-5, -13], [-3, -8], [-10, -10], [-25, -11]], C.zHair);
  poly([[26, -15], [19, -20], [5, -13], [3, -8], [10, -10], [25, -11]], C.zHair);
  line(-23, -10, -5, -6.5, 1.2, C.zSkinDD); line(23, -10, 5, -6.5, 1.2, C.zSkinDD);
  // eyes: crackling electric blue
  [-1, 1].forEach(function (sd) {
    var ex = sd * 12, ey = -3, n = -sd;
    poly([[ex + n * 7, ey + 0.8], [ex + n * 2, ey - 2.2], [ex - n * 4, ey - 2.6], [ex - n * 7.5, ey - 0.6], [ex - n * 3, ey + 2.6], [ex + n * 4, ey + 2.6]], C.eBlueL);
    disc(ex + look * 2.2, ey + 0.2, 2.5, C.cyanW); disc(ex + look * 2.2, ey + 0.2, 1.2, C.white);
    line(ex - 6, ey + 3.6, ex + 6, ey + 3.6, 0.9, C.zSkinD);
  });
  // laurel wreath
  for (var lf = 0; lf < 11; lf++) {
    var la = Math.PI * 1.1 + lf * (Math.PI * 0.8 / 10), lx = Math.cos(la) * 30, ly = -9 + Math.sin(la) * 32;
    ell(lx, ly, 5.4, 2.6, la + Math.PI / 2 + 0.6, C.goldD); ell(lx, ly - 0.5, 4.2, 1.8, la + Math.PI / 2 + 0.6, lf % 2 ? C.gold : C.goldL);
  }
  disc(0, -41.5, 3.4, C.goldD); disc(0, -41.5, 2.2, C.cyanL);
  g.restore();
  info.eyes = [W2(-12, -3), W2(12, -3)];
  info.head = W2(0, -6);
  return info;
}

// ------------------------------------------------------------------ SHIVA bust
// o: weapon 'hold' (trishul upright on the outer side) | 'thrust' (driven at o.target), look, third (0..1)
function shivaBust(x, y, s, dir, o) {
  o = o || {};
  var look = o.look === undefined ? 0.6 : o.look;
  var info = {};
  function W2(lx, ly) { return bustPt(x, y, s, dir, lx, ly); }
  g.save(); g.translate(x, y); g.scale(dir * s, s);
  // long matted locks falling behind the shoulders
  poly([[-22, -24], [-38, 6], [-48, 50], [-58, 116], [-40, 130], [-30, 70], [-18, 20]], C.jata);
  poly([[22, -24], [38, 6], [48, 50], [56, 116], [40, 130], [30, 70], [18, 20]], C.jata);
  line(-30, 4, -46, 110, 1, C.jataL); line(32, 4, 46, 110, 1, C.jataL);
  // trishul upright on the outer side (shaft behind the shoulder, hand in front)
  var trInfo = null;
  if (o.weapon === "hold") trInfo = trishulShape(-98, 98, Math.PI, 1.0, 140, 146);
  // neck + blue throat
  poly([[-15, 14], [15, 14], [19, 48], [-19, 48]], C.sSkinD);
  poly([[-3, 14], [15, 14], [19, 48], [1, 48]], C.sSkin);
  ell(0, 31, 10, 7, 0, C.neel);
  // torso
  poly([[-22, 40], [22, 40], [58, 50], [82, 70], [92, 108], [96, 220], [-96, 220], [-92, 108], [-82, 70], [-58, 50]], C.sSkinD);
  poly([[0, 40], [22, 40], [58, 50], [82, 70], [92, 108], [96, 220], [0, 220]], C.sSkin);
  poly([[32, 66], [68, 72], [82, 100], [48, 104]], C.sSkinL);
  line(-42, 112, -8, 120, 1.6, C.sSkinDD); line(8, 120, 42, 112, 1.6, C.sSkinDD);
  // sacred ash stripes on the shoulders
  [-1, 1].forEach(function (sd) {
    for (var k = 0; k < 3; k++) arcS(sd * 74, 86 + k * 5, 16, sd > 0 ? -2.6 : -0.9, sd > 0 ? -1.4 : 0.3, 1.6, C.ash, 1);
  });
  // tiger-skin over the outer shoulder
  poly([[-84, 70], [-60, 50], [-20, 150], [-50, 220], [-96, 220]], C.tigerD);
  poly([[-82, 72], [-62, 54], [-24, 150], [-52, 216], [-92, 216]], C.tiger);
  for (var ts = 0; ts < 6; ts++) line(-80 + ts * 6, 80 + ts * 22, -70 + ts * 6, 88 + ts * 22, 2, C.tigerD);
  // rudraksha mala
  for (var bi = 0; bi < 17; bi++) {
    var ba = Math.PI * (0.08 + 0.84 * bi / 16), bx = Math.cos(ba) * 44, by = 44 + Math.sin(ba) * 62;
    disc(bx, by, 3.4, C.beads); disc(bx - 0.8, by - 0.8, 1.5, C.beadsL);
  }
  // the serpent coiled around the neck, hood rising on the inner side
  g.lineCap = "round";
  g.strokeStyle = C.snakeD; g.lineWidth = 9; g.beginPath(); g.moveTo(-30, 42); g.quadraticCurveTo(0, 66, 30, 42); g.stroke();
  g.strokeStyle = C.snake; g.lineWidth = 6; g.stroke();
  for (var sc = 0; sc < 8; sc++) { var sx_ = -24 + sc * 7, sy_ = 42 + 13 * Math.sin((sc + 0.5) / 8 * Math.PI); rect(sx_, sy_ - 1, 2, 1.4, C.snakeD); }
  g.strokeStyle = C.snakeD; g.lineWidth = 8; g.beginPath(); g.moveTo(30, 42); g.quadraticCurveTo(46, 32, 42, 6); g.stroke();
  g.strokeStyle = C.snake; g.lineWidth = 5; g.stroke();
  ell(42, -2, 12, 15, 0, C.snakeD); ell(42, -2, 10, 13, 0, C.snake); ell(42, 1, 4.5, 8, 0, C.snakeL);
  for (var hm = 0; hm < 3; hm++) line(39, -6 + hm * 4, 45, -6 + hm * 4, 0.8, C.snakeD);
  ell(42, -15, 5.5, 4.2, 0, C.snakeD); ell(42, -15.5, 4.5, 3.4, 0, C.snake);
  rect(39.5, -17, 1.4, 1.4, C.tilak); rect(43.6, -17, 1.4, 1.4, C.tilak);
  line(42, -12, 42, -8.5, 0.7, C.tilak);
  // hands
  if (o.weapon === "hold") {
    arm(-64, 64, -98, 106, -12, 17, 13, C.sSkin, C.sSkinDD, C.sSkinL);
    fist(-98, 102, -1.57, 8, C.sSkin, C.sSkinDD, C.sSkinL);
    info.tip = W2(trInfo.tip[0], trInfo.tip[1]); info.head = W2(trInfo.head[0], trInfo.head[1]);
  }
  if (o.weapon === "thrust") {
    var tg = o.target || [118, -20], ang = o.angle === undefined ? 2.21 : o.angle, dv = A(ang);
    var hand2 = [tg[0] - dv[0] * 74, tg[1] - dv[1] * 74];
    var tr = trishulShape(hand2[0], hand2[1], ang, 1.0, 90, 48);
    arm(62, 64, hand2[0], hand2[1], 14, 17, 13, C.sSkin, C.sSkinDD, C.sSkinL);
    fist(hand2[0], hand2[1], Math.atan2(dv[1], dv[0]), 8, C.sSkin, C.sSkinDD, C.sSkinL);
    info.tip = W2(tr.tip[0], tr.tip[1]); info.head = W2(tr.head[0], tr.head[1]);
  }
  // face, with sockets, lit cheek and an inner rim light
  var face = [[-24, -14], [-23, 6], [-17, 20], [-8, 28], [0, 30], [8, 28], [17, 20], [23, 6], [24, -14], [22, -26], [12, -34], [0, -36], [-12, -34], [-22, -26]];
  poly(face, C.sSkinD);
  poly(face.map(function (p) { return [p[0] * 0.86 + 3.5, p[1] * 0.95 - 0.5]; }), C.sSkin);
  ell(13, 3, 6.5, 9, 0, C.sSkinL);
  ell(-11, -4, 8.5, 4.4, 0, C.sSkinD); ell(11, -4, 8, 4.2, 0, C.sSkinD);
  arcS(3.5, -3, 21, -1.3, 1.0, 1.5, C.sSkinL, 1);
  // ears + kundala earrings
  ell(-25, -1, 4, 7, 0, C.sSkinDD); ell(25, -1, 4, 7, 0, C.sSkinD);
  ringS(-26, 13, 5.5, 2.4, C.gold); ringS(26, 13, 5.5, 2.4, C.goldL);
  // hairline
  poly([[-25, -12], [-24, -28], [-14, -38], [0, -41], [14, -38], [24, -28], [25, -12], [20, -24], [8, -30], [0, -29], [-8, -30], [-20, -24]], C.jata);
  // jata crown: a tall bun of coiled locks, wrapped with rudraksha
  for (var row = 0; row < 8; row++) {
    var ry = -38 - row * 8, hw = 22 - row * 2.2, nL = row < 3 ? 4 : row < 6 ? 3 : 2;
    for (var j = 0; j < nL; j++) {
      var lx = nL === 1 ? 0 : -hw + 6 + j * (2 * hw - 12) / (nL - 1) + (row % 2 ? 3 : -3);
      ell(lx, ry, 7.5, 6, (row % 2 ? 0.5 : -0.5), C.jata);
      arcS(lx, ry, 5.5, -2.6, -0.6, 1.4, j * 2 >= nL - 1 ? C.jataH : C.jataL, 1);
    }
  }
  ell(0, -103, 7, 5.5, 0, C.jata); arcS(0, -103, 4.5, -2.8, -0.4, 1.3, C.jataH, 1);
  [-50, -76].forEach(function (by_, j) {
    var hw2 = j ? 17 : 22;
    line(-hw2, by_, hw2, by_, 3.4, C.beads);
    for (var rb = -hw2 + 3; rb <= hw2 - 3; rb += 5) { disc(rb, by_, 2, C.beads); disc(rb - 0.5, by_ - 0.6, 1, C.beadsL); }
  });
  g.strokeStyle = C.jata; g.lineWidth = 3.4; g.lineCap = "round";
  g.beginPath(); g.moveTo(-5, -100); g.quadraticCurveTo(-26, -98, -27, -76); g.stroke();
  g.beginPath(); g.moveTo(5, -100); g.quadraticCurveTo(24, -102, 27, -82); g.stroke();
  arcS(-16, -96, 9, 3.4, 4.6, 1, C.jataH, 1);
  // crescent moon on the inner side of the crown
  g.strokeStyle = C.moon; g.lineWidth = 3.6; g.lineCap = "round";
  g.beginPath(); g.arc(20, -70, 8.5, -1.5, 1.2); g.stroke();
  // tripundra (three ash lines) + third eye
  for (var tk = 0; tk < 3; tk++) { rect(-17, -24.5 + tk * 3.4, 12.5, 1.7, C.ash); rect(4.5, -24.5 + tk * 3.4, 12.5, 1.7, C.ash); }
  ell(0, -20, 3.4, 7.4, 0, C.sSkinDD);
  ell(0, -20, 2.2, 6.2, 0, (o.third || 0) > 0.3 ? C.cyanW : C.tilak);
  if ((o.third || 0) > 0.3) ell(0, -20, 0.9, 4, 0, C.white);
  // brows: calm, slightly arched
  poly([[-21, -11], [-12, -14.5], [-4, -12.5], [-4, -10.5], [-12, -12.5], [-21, -9]], C.jata);
  poly([[21, -11], [12, -14.5], [4, -12.5], [4, -10.5], [12, -12.5], [21, -9]], C.jata);
  // eyes: half-lidded, glowing
  [-1, 1].forEach(function (sd) {
    var ex = sd * 11, ey = -4, n = -sd;
    poly([[ex + n * 7, ey + 0.6], [ex + n * 2, ey - 2.2], [ex - n * 4, ey - 2.4], [ex - n * 7.5, ey - 0.4], [ex - n * 3, ey + 2.4], [ex + n * 4, ey + 2.4]], C.white);
    disc(ex + look * 2, ey + 0.6, 2.4, C.cyan); disc(ex + look * 2, ey + 0.6, 1.2, C.cyanW);
    poly([[ex + n * 7.8, ey + 0.4], [ex + n * 2, ey - 3], [ex - n * 4, ey - 3.2], [ex - n * 8, ey - 0.6], [ex - n * 4, ey - 0.8], [ex + n * 2, ey - 1]], C.sSkinD);
    line(ex + n * 7.6, ey + 0.2, ex - n * 8, ey - 0.6, 1.3, C.jata);
    line(ex - 5, ey + 3.2, ex + 5, ey + 3.2, 0.8, C.sSkinD);
  });
  // nose + calm mouth
  poly([[-1, -6], [-3, 5], [-5, 9], [-1, 11], [0, 8]], C.sSkinD);
  line(2.5, -6, 3.5, 6, 1.1, C.sSkinL);
  rect(-4, 10, 2, 1.2, C.sSkinDD); rect(2.5, 10, 2, 1.2, C.sSkinDD);
  line(-7, 17, 7, 17, 1.5, C.sSkinDD);
  line(-4, 19.6, 5, 19.6, 1.1, C.sSkinL);
  g.restore();
  info.eyes = [W2(-11, -4), W2(11, -4)];
  info.third = W2(0, -20);
  info.moon = W2(22, -70);
  return info;
}

// halos drawn BEHIND a bust (before blitSprite) so they never wash out the figure's colours
function zeusBack(z, t) {
  lighter();
  if (z.mid) { glow(z.mid[0], z.mid[1], 58, C.eBlue, 0.6); glow(z.mid[0], z.mid[1], 34, C.goldL, 0.45); }
  glow(z.head[0], z.head[1], 70, C.goldW, 0.25);
  normalBlend();
  if (z.mid) crackle(z.mid[0], z.mid[1], 40, 8, 931, t, C.eBlue);
}
function zeusFront(z) {
  lighter();
  z.eyes.forEach(function (e) { glow(e[0], e[1], 6, C.cyan, 0.7); glow(e[0], e[1], 2.5, C.white, 0.8); });
  if (z.tip) { glow(z.tip[0], z.tip[1], 9, C.white, 0.9); glow(z.tail[0], z.tail[1], 7, C.white, 0.6); }
  normalBlend();
}
function shivaBack(sv) {
  lighter();
  if (sv.head) { glow(sv.head[0], sv.head[1], 40, C.cyan, 0.6); glow(sv.head[0], sv.head[1], 20, C.white, 0.4); }
  glow(sv.third[0], sv.third[1] - 30, 60, C.violet, 0.35);
  normalBlend();
}
function shivaFront(sv) {
  lighter();
  sv.eyes.forEach(function (e) { glow(e[0], e[1], 5, C.cyan, 0.55); });
  glow(sv.third[0], sv.third[1], 6, C.cyanW, 0.9); glow(sv.third[0], sv.third[1], 13, C.violet, 0.5);
  glow(sv.moon[0], sv.moon[1], 9, C.moon, 0.45);
  if (sv.tip) glow(sv.tip[0], sv.tip[1], 8, C.white, 0.8);
  normalBlend();
}
// streaky storm-cloud bands (wide, flat ellipses instead of round puffs)
function cloudBand(x0, x1, y, h, seed, cols) {
  var r = rng(seed), pts = [];
  for (var i = 0; i < (x1 - x0) / 7; i++) pts.push([x0 + r() * (x1 - x0), y + r() * h, 16 + r() * 26, 5 + r() * 7]);
  pts.forEach(function (p) { ell(p[0], p[1] + 2, p[2], p[3], 0, cols[0]); });
  pts.forEach(function (p) { ell(p[0], p[1], p[2] * 0.9, p[3] * 0.8, 0, cols[1]); });
  pts.forEach(function (p) { ell(p[0] - p[2] * 0.15, p[1] - p[3] * 0.45, p[2] * 0.5, p[3] * 0.3, 0, cols[2]); });
}
function starField(seed, n, x0, y0, w, h) {
  var r = rng(seed);
  for (var i = 0; i < n; i++) {
    var x = x0 + r() * w, y = y0 + r() * h, big = r() < 0.12;
    rect(x, y, big ? 2 : 1, big ? 2 : 1, r() < 0.25 ? C.cyanL : r() < 0.4 ? C.goldW : C.white);
    if (big && r() < 0.5) { rect(x - 2, y + 0.5, 6, 1, C.paleBlue); rect(x + 0.5, y - 2, 1, 6, C.paleBlue); }
  }
}
// an abstract presence: a vast dark mass rising behind the rift, only its rim lit (no identity)
function looming(x, y, sc) {
  disc(x, y + 60 * sc, 64 * sc, C.shadow);
  disc(x + 6 * sc, y - 4 * sc, 34 * sc, C.shadow);
  ell(x - 30 * sc, y + 24 * sc, 34 * sc, 22 * sc, 0.4, C.shadow);
  ell(x + 34 * sc, y + 26 * sc, 34 * sc, 22 * sc, -0.4, C.shadow);
  arcS(x + 6 * sc, y - 4 * sc, 34 * sc, -2.6, -0.5, 1.6, C.portalV, 1);
  arcS(x - 30 * sc, y + 24 * sc, 34 * sc, -2.9, -1.9, 1.4, C.portalV, 0.8);
  arcS(x + 34 * sc, y + 26 * sc, 34 * sc, -1.2, -0.3, 1.4, C.portalV, 0.8);
}
// pixel title: bold 5x7 glyphs with a thick dark outline, drop shadow and a two-tone bevel (ui canvas)
function glyphs(str, x, y, s, col, bold) {
  u.fillStyle = col;
  for (var i = 0; i < str.length; i++) {
    var gl = FONT[str[i]] || FONT[" "];
    for (var p = 0; p < 35; p++) if (gl[p] === "1") u.fillRect(x + i * 6 * s + (p % 5) * s, y + Math.floor(p / 5) * s, s + bold, s);
  }
}
function title(segs, cy, s, cx, o) {
  o = o || {};
  var bold = o.bold === undefined ? Math.max(1, Math.round(s / 3)) : o.bold, ol = o.outline || 2, sh = o.shadow || 2;
  var full = segs.map(function (q) { return q[0]; }).join("");
  var tw = full.length * 6 * s - s + bold;
  var x0 = Math.round((cx === undefined ? W / 2 : cx) - tw / 2), y0 = Math.round(cy - 3.5 * s);
  var x = x0;
  segs.forEach(function (q) {
    for (var dx = -ol; dx <= ol + sh; dx++) for (var dy = -ol; dy <= ol + sh; dy++) {
      if (dx > ol || dy > ol) glyphs(q[0], x + dx, y0 + dy, s, "#000000", bold);
    }
    for (var dx2 = -ol; dx2 <= ol; dx2++) for (var dy2 = -ol; dy2 <= ol; dy2++) glyphs(q[0], x + dx2, y0 + dy2, s, o.outlineCol || "#05040c", bold);
    x += q[0].length * 6 * s;
  });
  x = x0;
  segs.forEach(function (q) {
    var w = q[0].length * 6 * s;
    glyphs(q[0], x, y0, s, q[1], bold);
    u.save(); u.beginPath(); u.rect(x - 1, y0 + 4 * s, w + 2, 3 * s); u.clip(); glyphs(q[0], x, y0, s, q[2], bold); u.restore();
    u.save(); u.beginPath(); u.rect(x - 1, y0, w + 2, Math.max(1, Math.round(s * 0.5))); u.clip(); glyphs(q[0], x, y0, s, "#ffffff", bold); u.restore();
    x += w;
  });
}
