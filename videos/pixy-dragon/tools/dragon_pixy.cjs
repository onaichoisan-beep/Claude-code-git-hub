// Dragon-hood Pixy: Chi-style noodle-limb proportions, flame-style expressions, doctor outfit,
// in the Blue / Butter / Chocopie palette. Exports SVG builders reused by the reels.
const K = '#432f2e', SKIN = '#FFD8BE', BLUSH = '#FF9AAE', HOOD = '#c4dae8', HOOD_D = '#9fc0d6', BUTTER = '#feefb8',
  ORANGE = '#e8743b', COAT = '#FFFCF2', PANTS = '#6b4f4c', MOUTH = '#7A3A34', TONGUE = '#FF8FA3';
const SW = 7;
const st = (w = SW) => `stroke="${K}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
let uid = 0;

// ---------- face expressions (flame-style eyes: white disc + black pupil, lids, tiny mouths) ----------
const EYE = { L: [259, 290], R: [341, 290] };
function eye(side, o = {}) {
  const [cx, cy] = EYE[side];
  const r = o.r || 27, pr = o.pr || 15, px = o.px || 0, py = o.py || 0;
  const id = `lid${uid++}`;
  let s = `<clipPath id="${id}"><circle cx="${cx}" cy="${cy}" r="${r + 4}"/></clipPath>`;
  s += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff" ${st(5)}/>`;
  s += `<circle cx="${cx + px}" cy="${cy + py}" r="${pr}" fill="${K}"/>`;
  if (o.lid != null) {
    // lid: covers the eye above a line through (cx, cy+lid) tilted by o.tilt (deg, + = outer side lower)
    const t = ((o.tilt || 0) * (side === 'L' ? -1 : 1) * Math.PI) / 180, y = cy + o.lid, d = 50;
    const x1 = cx - d, x2 = cx + d, y1 = y - Math.tan(t) * d, y2 = y + Math.tan(t) * d;
    s += `<g clip-path="url(#${id})"><path d="M ${x1} ${y1} L ${x2} ${y2} L ${x2} ${cy - 60} L ${x1} ${cy - 60} Z" fill="${SKIN}"/></g>`;
    s += `<path d="M ${cx - r * 1.05} ${y1 + (y2 - y1) * ((d - r * 1.05) / (2 * d))} L ${cx + r * 1.05} ${y1 + (y2 - y1) * ((d + r * 1.05) / (2 * d))}" ${st(6)}/>`;
  }
  return s;
}
const MOUTHS = {
  smile: `<path d="M 284 334 Q 300 350 316 334" fill="none" ${st(6)}/>`,
  dot: `<ellipse cx="300" cy="338" rx="6" ry="5" fill="${K}"/>`,
  cat: `<path d="M 284 334 Q 292 344 300 334 Q 308 344 316 334" fill="none" ${st(5)}/>`,
  frown: `<path d="M 284 344 Q 300 328 316 344" fill="none" ${st(6)}/>`,
  slant: `<path d="M 280 330 L 320 344" fill="none" ${st(6)}/>`,
  joy: `<path d="M 274 326 C 272 360 330 366 326 328 C 314 318 288 316 274 326 Z" fill="${K}"/><path d="M 288 350 Q 300 340 312 350 Q 300 360 288 350 Z" fill="${TONGUE}"/>`,
  oh: `<ellipse cx="300" cy="342" rx="13" ry="17" fill="${K}"/>`,
  angry: `<path d="M 280 350 C 280 326 320 326 320 350 Z" fill="${K}"/><path d="M 290 348 L 300 340 L 310 348 Z" fill="#fff"/>`,
  grin: `<path d="M 278 328 Q 300 356 322 328 Z" fill="#fff" ${st(5)}/>`,
  closed: `<path d="M 288 338 L 312 338" ${st(6)}/>`,
  open: `<path d="M 276 326 Q 300 368 324 326 Z" fill="${MOUTH}" ${st(5)}/><path d="M 287 346 Q 300 337 313 346 Q 300 356 287 346 Z" fill="${TONGUE}"/>`,
  mid: `<path d="M 283 330 Q 300 354 317 330 Z" fill="${MOUTH}" ${st(5)}/>`,
};
const EXPR = {
  friendly: { L: {}, R: {}, m: 'smile' },
  joy: { L: { r: 29 }, R: { r: 29 }, m: 'joy' },
  sly: { L: { lid: -4, tilt: -12, px: 8, py: 6 }, R: { lid: -4, tilt: -12, px: 8, py: 6 }, m: 'smile' },
  gusto: { L: { lid: 2, py: 9 }, R: { lid: 2, py: 9 }, m: 'cat' },
  confusion: { L: { r: 30, px: -4 }, R: { r: 21, pr: 11, px: 4, py: -4 }, m: 'slant' },
  watching: { L: { r: 28, pr: 16 }, R: { r: 28, pr: 16 }, m: 'dot' },
  upset: { L: { lid: -8, tilt: 16, py: 6 }, R: { lid: -8, tilt: 16, py: 6 }, m: 'frown' },
  angry: { L: { lid: -6, tilt: -24, py: 3 }, R: { lid: -6, tilt: -24, py: 3 }, m: 'angry' },
  shock: { L: { r: 31, pr: 9 }, R: { r: 31, pr: 9 }, m: 'oh' },
};
function face(expr = 'friendly', mouthOverride) {
  const e = EXPR[expr];
  return `<ellipse cx="300" cy="300" rx="106" ry="98" fill="${SKIN}"/>
    <ellipse cx="226" cy="328" rx="16" ry="10" fill="${BLUSH}" opacity="0.85"/><ellipse cx="374" cy="328" rx="16" ry="10" fill="${BLUSH}" opacity="0.85"/>
    ${eye('L', e.L)}${eye('R', e.R)}${MOUTHS[mouthOverride || e.m]}`;
}

// ---------- dragon hood (front) ----------
const teeth = (pts, down) => pts.map(([x, y]) => `<path d="M ${x - 14} ${y} Q ${x} ${y + (down ? 34 : -34)} ${x + 14} ${y} Z" fill="#fff" ${st(5)}/>`).join('');
function hoodBack() {
  // crest spikes + horns behind the hood
  return `${[[300, 70, 0], [236, 90, -26], [364, 90, 26]].map(([x, y, r]) => `<path transform="rotate(${r} ${x} ${y + 40})" d="M ${x - 26} ${y + 40} L ${x} ${y - 18} L ${x + 26} ${y + 40} Z" fill="${ORANGE}" ${st(6)}/>`).join('')}
    <path d="M 176 152 C 150 132 132 100 146 66 C 160 92 184 112 206 124 Z" fill="#f2c94c" ${st(6)}/>
    <path d="M 424 152 C 450 132 468 100 454 66 C 440 92 416 112 394 124 Z" fill="#f2c94c" ${st(6)}/>`;
}
function hood(expr = 'friendly', mouth) {
  return `${hoodBack()}
  <ellipse cx="300" cy="256" rx="168" ry="162" fill="${HOOD}" ${st()}/>
  <path d="M 162 300 Q 172 316 182 300 M 166 336 Q 176 352 186 336 M 418 300 Q 428 316 438 300 M 414 336 Q 424 352 434 336" fill="none" stroke="${HOOD_D}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="300" cy="300" rx="120" ry="110" fill="${MOUTH}" ${st()}/>
  ${face(expr, mouth)}
  ${teeth([[234, 212], [300, 193], [366, 212]], true)}
  ${teeth([[252, 394], [348, 394]], false)}
  <g id="hood-eyes">
    <path d="M 222 150 Q 246 112 276 146 Z" fill="#fff" ${st(6)}/><path d="M 378 150 Q 354 112 324 146 Z" fill="#fff" ${st(6)}/>
    <circle cx="256" cy="138" r="9" fill="${K}"/><circle cx="344" cy="138" r="9" fill="${K}"/>
    <path d="M 214 112 Q 240 112 280 128 M 386 112 Q 360 112 320 128" fill="none" ${st(8)}/>
  </g>
  <ellipse cx="287" cy="172" rx="6" ry="4" fill="${K}"/><ellipse cx="313" cy="172" rx="6" ry="4" fill="${K}"/>`;
}
function hoodBackView() {
  return `${hoodBack()}<ellipse cx="300" cy="256" rx="168" ry="162" fill="${HOOD}" ${st()}/>
    ${[[300, 150], [300, 215], [300, 280], [300, 345]].map(([x, y]) => `<path d="M ${x - 20} ${y} L ${x} ${y - 30} L ${x + 20} ${y} Z" fill="${ORANGE}" ${st(5)}/>`).join('')}
    <path d="M 196 260 Q 210 276 224 260 M 376 260 Q 390 276 404 260 M 206 300 Q 220 316 234 300 M 366 300 Q 380 316 394 300" fill="none" stroke="${HOOD_D}" stroke-width="6" stroke-linecap="round"/>`;
}

// ---------- body (Chi proportions: small torso, long noodle limbs, big round feet) ----------
const SH = { L: [228, 430], R: [372, 430] };   // shoulders
const HIP = { L: [268, 636], R: [332, 636] };
const UPPER = 128, LOWER = 118, THIGH = 124, SHIN = 112;
const dir = (side, a) => { const s = side === 'L' ? -1 : 1, r = (a * Math.PI) / 180; return [Math.sin(r) * s, Math.cos(r)]; };
function limb(pts, fill, w) {
  const d = 'M ' + pts.map((p) => p.map((v) => v.toFixed(1)).join(' ')).join(' L ');
  return `<path d="${d}" fill="none" stroke="${K}" stroke-width="${w + SW * 2}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" fill="none" stroke="${fill}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
}
function ik(side, [tx, ty]) {
  const [sx, sy] = SH[side];
  let dx = tx - sx, dy = ty - sy, d = Math.hypot(dx, dy);
  d = Math.min(d, UPPER + LOWER - 1);
  const base = Math.atan2(dy, dx), cosA = (UPPER * UPPER + d * d - LOWER * LOWER) / (2 * UPPER * d);
  const bend = side === 'L' ? 1 : -1;  // elbow swings outward/down
  const a = base + bend * Math.acos(Math.max(-1, Math.min(1, cosA)));
  const ex = sx + Math.cos(a) * UPPER, ey = sy + Math.sin(a) * UPPER;
  const hx = sx + Math.cos(base) * d, hy = sy + Math.sin(base) * d;
  return [ex, ey, hx, hy];
}
function arm(side, spec = [8, 4], hand = 'mitt') {
  const [sx, sy] = SH[side];
  let ex, ey, hx, hy;
  if (spec.ik) [ex, ey, hx, hy] = ik(side, spec.ik);
  else { const [d1x, d1y] = dir(side, spec[0]), [d2x, d2y] = dir(side, spec[1]); ex = sx + d1x * UPPER; ey = sy + d1y * UPPER; hx = ex + d2x * LOWER; hy = ey + d2y * LOWER; }
  const fl = Math.hypot(hx - ex, hy - ey), d2x = (hx - ex) / fl, d2y = (hy - ey) / fl;
  const cuffx = ex + d2x * (fl - 30), cuffy = ey + d2y * (fl - 30);
  let s = limb([[sx, sy], [ex, ey], [cuffx, cuffy]], COAT, 44);
  s += limb([[cuffx, cuffy], [hx, hy]], SKIN, 34);
  // mitten hand with a thumb
  const ang = (Math.atan2(d2y, d2x) * 180) / Math.PI - 90;
  s += `<g transform="translate(${hx.toFixed(1)} ${hy.toFixed(1)}) rotate(${ang.toFixed(1)})">
    <ellipse cx="${side === 'L' ? 14 : -14}" cy="2" rx="9" ry="14" transform="rotate(${side === 'L' ? -30 : 30} ${side === 'L' ? 14 : -14} 2)" fill="${SKIN}" ${st(5)}/>
    <ellipse cx="0" cy="12" rx="22" ry="24" fill="${SKIN}" ${st(6)}/>
    ${hand === 'point' ? `<rect x="-7" y="22" width="14" height="34" rx="7" fill="${SKIN}" ${st(5)}/>` : ''}
  </g>`;
  return s;
}
function leg(side, [a1, a2] = [0, 0]) {
  const [hx, hy] = HIP[side], [d1x, d1y] = dir(side, a1), [d2x, d2y] = dir(side, a2);
  const kx = hx + d1x * THIGH, ky = hy + d1y * THIGH, fx = kx + d2x * SHIN, fy = ky + d2y * SHIN;
  const out = side === 'L' ? -1 : 1;
  return limb([[hx, hy], [kx, ky], [fx, fy]], PANTS, 50) +
    `<path d="M ${fx - 46 + out * 18} ${fy + 34} C ${fx - 54 + out * 18} ${fy - 20} ${fx + 50 + out * 18} ${fy - 24} ${fx + 50 + out * 18} ${fy + 34} Z" fill="${HOOD}" ${st()}/>
     <path d="M ${fx - 30 + out * 18} ${fy + 16} L ${fx + 34 + out * 18} ${fy + 16}" stroke="${HOOD_D}" stroke-width="6" stroke-linecap="round"/>`;
}
function torso(back = false) {
  let s = `<path d="M 222 420 Q 300 386 378 420 L 392 650 Q 300 680 208 650 Z" fill="${COAT}" ${st()}/>`;
  if (!back) {
    s += `<path d="M 270 402 L 300 470 L 330 402 Z" fill="${HOOD}" ${st(6)}/>
      <path d="M 268 402 L 300 470 L 272 466 L 252 412 Z M 332 402 L 300 470 L 328 466 L 348 412 Z" fill="${COAT}" ${st(6)}/>
      <path d="M 300 470 L 300 664" ${st(6)}/>
      <path d="M 262 412 C 248 452 246 500 262 528" fill="none" ${st(9)}/><path d="M 338 412 C 350 440 350 466 338 488" fill="none" ${st(9)}/>
      <circle cx="262" cy="542" r="15" fill="${HOOD}" ${st(6)}/><circle cx="262" cy="542" r="5" fill="#fff"/>
      <g transform="translate(316 520)"><rect width="58" height="38" rx="6" fill="#fff" ${st(5)}/><rect x="3" y="3" width="52" height="10" fill="${ORANGE}"/>
        <text x="29" y="32" text-anchor="middle" font-family="Bagel Fat One" font-size="15" fill="${K}">PIXY</text></g>
      <path d="M 232 590 L 276 590 M 324 590 L 368 590" stroke="${K}" stroke-width="5" stroke-linecap="round"/>`;
  } else s += `<path d="M 300 430 L 300 664" ${st(6)}/><path d="M 236 600 Q 300 620 364 600" fill="none" ${st(5)}/>`;
  return s;
}

const POSES = {
  stand: { L: [8, 4], R: [8, 4] },
  wave: { L: [8, 4], R: [130, 170] },
  point: { L: [8, 4], R: [88, 92], hand: 'point' },
  celebrate: { L: [150, 168], R: [150, 168] },
  think: { L: [8, 4], R: { ik: [330, 392] }, hand: 'point', front: 'R' },
  shrug: { L: [62, 150], R: [62, 150] },
  hips: { L: [50, -40], R: [50, -40] },
  facepalm: { L: [8, 4], R: { ik: [300, 268] }, front: 'R' },
  walk: { L: [-18, -10], R: [20, 30], legs: { L: [16, 6], R: [-14, -4] } },
};
function body(pose = 'stand', back = false) {
  const p = POSES[pose];
  const legs = p.legs || { L: [0, 0], R: [0, 0] };
  // arms that cross in front of the body are drawn after the torso
  return `${leg('L', legs.L)}${leg('R', legs.R)}${torso(back)}${p.front === 'L' ? '' : arm('L', p.L)}${p.front === 'R' ? '' : arm('R', p.R, p.hand || 'mitt')}`;
}
function frontArm(pose) { const p = POSES[pose]; return p.front ? arm(p.front, p[p.front], p.hand || 'mitt') : ''; }
function pixy({ expr = 'friendly', pose = 'stand', back = false, mouth } = {}) {
  return `<ellipse cx="300" cy="910" rx="160" ry="16" fill="${K}" opacity="0.12"/>${body(pose, back)}${back ? hoodBackView() : hood(expr, mouth)}${back ? '' : frontArm(pose)}`;
}
module.exports = { pixy, hood, face, EXPR, POSES, MOUTHS: Object.keys(MOUTHS), palette: { K, HOOD, BUTTER, ORANGE, COAT } };
