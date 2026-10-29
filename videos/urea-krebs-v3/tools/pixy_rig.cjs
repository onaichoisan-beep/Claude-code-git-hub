// Pixy #1 (Classic Spiky) as an animatable rig: every moving part is its own <g> with a known pivot.
// Coordinates are the original 600x790 chibi space (head centre 300,290; feet ~780).
const K = '#432f2e', SKIN = '#FFD3B0', SKIN_S = '#EBAF8C', HAIR = '#2c1f1e', BLUE = '#c4dae8', BLUE_D = '#9DBFD6',
  COAT = '#FFFCF2', MOUTH = '#7A3A34', BLUSH = '#FF9AAE', IRIS = '#5A3A22';
const S = (w = 7) => `stroke="${K}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

const PIVOTS = {
  root: '300 780', body: '300 700', head: '300 430', hair: '300 200',
  armL: '214 494', armR: '386 494', legL: '266 690', legR: '334 690',
  eyeL: '250 302', eyeR: '350 302', browL: '250 246', browR: '350 246', mouth: '300 362',
};

function arm(side) {
  const m = x => (side === 'L' ? x : 600 - x);
  const hx = m(197);
  return `<g id="px-arm${side}">
    <path d="M ${m(212)} 492 C ${m(182)} 520 ${m(170)} 600 ${m(176)} 650 L ${m(218)} 655 C ${m(218)} 610 ${m(222)} 560 ${m(236)} 522 Z" fill="${COAT}" ${S()}/>
    <rect id="px-finger${side}" x="${hx - 8}" y="676" width="16" height="40" rx="8" fill="${SKIN}" ${S(5)} opacity="0"/>
    <circle cx="${hx}" cy="670" r="25" fill="${SKIN}" ${S()}/>
  </g>`;
}
function leg(side) {
  const x = side === 'L' ? 240 : 308, sx = side === 'L' ? 220 : 300;
  return `<g id="px-leg${side}"><rect x="${x}" y="680" width="52" height="66" fill="${K}" ${S()}/>
    <rect x="${sx}" y="738" width="80" height="36" rx="18" fill="#fff" ${S()}/>
    <path d="M ${sx + 18} 752 Q ${sx + 42} 762 ${sx + 64} 750" fill="none" stroke="${BLUE}" stroke-width="5" stroke-linecap="round"/></g>`;
}
const eyeNorm = x => `<g><ellipse cx="${x}" cy="302" rx="20" ry="26" fill="${K}"/>
  <g class="px-pupil"><ellipse cx="${x}" cy="308" rx="13" ry="15" fill="${IRIS}"/><ellipse cx="${x}" cy="309" rx="7" ry="9" fill="${K}"/>
  <circle cx="${x + 7}" cy="292" r="7" fill="#fff"/><circle cx="${x - 7}" cy="314" r="3" fill="#fff"/></g></g>`;
const eyeShock = x => `<ellipse cx="${x}" cy="300" rx="26" ry="31" fill="#fff" ${S(6)}/><circle cx="${x}" cy="302" r="10" fill="${K}"/><circle cx="${x + 3}" cy="298" r="3" fill="#fff"/>`;
const eyeClosed = x => `<path d="M ${x - 20} 306 Q ${x} 288 ${x + 20} 306" fill="none" stroke="${K}" stroke-width="8" stroke-linecap="round"/>`;
const eyeHappy = x => `<path d="M ${x - 20} 310 Q ${x} 284 ${x + 20} 310" fill="none" stroke="${K}" stroke-width="9" stroke-linecap="round"/>`;

const MOUTHS = {
  closed: `<path d="M 278 358 Q 300 374 322 358" fill="none" stroke="${K}" stroke-width="7" stroke-linecap="round"/>`,
  smile: `<path d="M 272 352 Q 300 384 328 352 Z" fill="${MOUTH}" ${S(6)}/>`,
  mid: `<path d="M 276 352 Q 300 382 324 352 Z" fill="${MOUTH}" ${S(6)}/><path d="M 290 368 Q 300 362 310 368 Q 300 374 290 368 Z" fill="${BLUSH}"/>`,
  open: `<path d="M 264 346 Q 300 404 336 346 Z" fill="${MOUTH}" ${S(6)}/><path d="M 282 374 Q 300 360 318 374 Q 300 390 282 374 Z" fill="${BLUSH}"/>`,
  oh: `<ellipse cx="300" cy="368" rx="19" ry="24" fill="${MOUTH}" ${S(6)}/>`,
  ee: `<path d="M 270 352 Q 300 358 330 352 Q 326 376 300 378 Q 274 376 270 352 Z" fill="#fff" ${S(6)}/><path d="M 274 362 Q 300 366 326 362" stroke="#e8dcc8" stroke-width="3" fill="none"/>`,
};

function rig() {
  const hair = `<g transform="translate(300 290) scale(140 132)"><path d="M -1.03 0.05 C -1.1 -0.5 -0.95 -0.85 -0.7 -1.0 L -0.85 -1.35 L -0.4 -1.12 L -0.3 -1.55 L 0.05 -1.15 L 0.35 -1.6 L 0.45 -1.12 L 0.9 -1.35 L 0.82 -0.95 L 1.2 -0.85 L 1.0 -0.55 C 1.08 -0.35 1.06 -0.15 1.03 0.05 C 0.96 -0.25 0.88 -0.4 0.76 -0.5 C 0.45 -0.32 0.0 -0.32 -0.35 -0.5 C -0.6 -0.38 -0.85 -0.2 -1.03 0.05 Z" fill="${HAIR}" stroke="${K}" stroke-width="7" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
    <path d="M 0.05 -1.15 L 0.35 -1.6 L 0.45 -1.12 C 0.35 -0.9 0.2 -0.85 0.0 -0.8 Z" fill="${BLUE}"/></g>`;
  const brow = (id, d) => `<path id="${id}" d="${d}" fill="none" stroke="${HAIR}" stroke-width="12" stroke-linecap="round"/>`;
  return `<g id="px-root">
  <ellipse id="px-shadow" cx="300" cy="782" rx="150" ry="18" fill="#000" opacity="0.15"/>
  ${leg('L')}${leg('R')}
  <g id="px-body">
    <rect x="276" y="410" width="48" height="66" fill="${SKIN}" ${S()}/>
    <path d="M 205 485 C 240 458 360 458 395 485 L 418 702 C 340 720 260 720 182 702 Z" fill="${COAT}" ${S()}/>
    <path d="M 372 470 C 384 475 392 480 395 485 L 418 702 C 404 706 392 708 380 710 Z" fill="${BLUE}"/>
    <path d="M 300 560 L 300 714" fill="none" ${S()}/>
    <path d="M 260 466 L 300 560 L 340 466 Z" fill="${BLUE}" ${S()}/>
    <path d="M 262 466 L 300 560 L 264 542 L 244 478 Z" fill="${COAT}" ${S()}/>
    <path d="M 338 466 L 300 560 L 336 542 L 356 478 Z" fill="${COAT}" ${S()}/>
    <path d="M 258 476 C 246 520 236 560 252 598" fill="none" stroke="${K}" stroke-width="10" stroke-linecap="round"/>
    <path d="M 342 476 C 352 510 350 535 336 556" fill="none" stroke="${K}" stroke-width="10" stroke-linecap="round"/>
    <circle cx="252" cy="612" r="17" fill="${BLUE}" ${S(6)}/><circle cx="252" cy="612" r="6" fill="#fff"/>
    <g transform="translate(308 582)"><rect width="66" height="42" rx="6" fill="#fff" ${S(5)}/><rect x="3" y="3" width="60" height="12" fill="${BLUE}"/>
      <text x="33" y="35" text-anchor="middle" font-family="Inter" font-weight="800" font-size="16" fill="${K}">PIXY</text></g>
    ${arm('L')}${arm('R')}
    <g id="px-head">
      <circle cx="162" cy="306" r="26" fill="${SKIN}" ${S()}/><circle cx="438" cy="306" r="26" fill="${SKIN}" ${S()}/>
      <ellipse cx="300" cy="290" rx="140" ry="132" fill="${SKIN}" ${S()}/>
      <g id="px-hair">${hair}</g>
      ${brow('px-browL', 'M 224 250 Q 250 238 276 246')}${brow('px-browR', 'M 324 246 Q 350 238 376 250')}
      <g id="px-eyes-norm"><g id="px-eyeL">${eyeNorm(250)}</g><g id="px-eyeR">${eyeNorm(350)}</g></g>
      <g id="px-eyes-shock" opacity="0">${eyeShock(250)}${eyeShock(350)}</g>
      <g id="px-eyes-happy" opacity="0">${eyeHappy(250)}${eyeHappy(350)}</g>
      <g id="px-eyes-wink" opacity="0">${eyeNorm(250)}${eyeClosed(350)}</g>
      <ellipse cx="214" cy="344" rx="18" ry="9" fill="${BLUSH}" opacity="0.75"/><ellipse cx="386" cy="344" rx="18" ry="9" fill="${BLUSH}" opacity="0.75"/>
      <path d="M 300 318 Q 308 332 297 337" fill="none" stroke="${SKIN_S}" stroke-width="5" stroke-linecap="round"/>
      <g id="px-chinhand" opacity="0"><rect x="338" y="378" width="16" height="36" rx="8" fill="${SKIN}" ${S(5)}/><circle cx="350" cy="428" r="25" fill="${SKIN}" ${S()}/><path d="M 338 420 Q 350 414 362 420" fill="none" stroke="${SKIN_S}" stroke-width="4" stroke-linecap="round"/></g>
      <g id="px-mouth">${Object.entries(MOUTHS).map(([k, v]) => `<g id="px-m-${k}" opacity="${k === 'smile' ? 1 : 0}">${v}</g>`).join('')}</g>
    </g>
  </g>
</g>`;
}
module.exports = { rig, PIVOTS, MOUTHS: Object.keys(MOUTHS) };
