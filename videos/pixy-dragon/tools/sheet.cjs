// Renders the dragon Pixy character sheet (turnaround, emotions, poses) to renders/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { pixy, hood, EXPR, POSES } = require('./dragon_pixy.cjs');
const OUT = path.join(__dirname, '..', 'renders');
fs.mkdirSync(OUT, { recursive: true });

const full = (o, w) => `<svg viewBox="30 40 540 900" width="${w}" height="${(w * 900) / 540}">${pixy(o)}</svg>`;
const head = (e, w) => `<svg viewBox="110 50 380 380" width="${w}" height="${w}">${hood(e)}</svg>`;
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Bagel+Fat+One&family=Inter:wght@500;800&display=block" rel="stylesheet">`;
const cap = (t) => `<div style="font:800 20px Inter;color:#432f2e;letter-spacing:.08em;text-transform:uppercase;margin-top:6px">${t}</div>`;

const html = `<html><head>${FONTS}</head><body style="margin:0;width:1600px;background:#feefb8;font-family:Inter;color:#432f2e">
  <div style="padding:50px 70px 0;display:flex;gap:40px;align-items:flex-end">
    <div style="font:900 120px/0.9 'Playfair Display'">PIXY</div>
    <div><div style="font:400 44px 'Bagel Fat One'">Dr. Dragon</div><div style="font:500 22px Inter;max-width:820px;margin-top:6px">A tiny doctor in a dragon hood. Scrolls too much, scores even more. Explains medicine like gossip and roars when something is NEET-important.</div></div>
  </div>
  <div style="margin:30px 70px 0;padding:20px 0 10px;border-top:3px solid #432f2e;display:flex;justify-content:space-around;align-items:flex-end;
    background:repeating-linear-gradient(#feefb8 0 58px, #e9d58f 58px 60px)">
    <div style="text-align:center">${full({ expr: 'friendly' }, 300)}${cap('front')}</div>
    <div style="text-align:center">${full({ expr: 'sly', pose: 'hips' }, 300)}${cap('attitude')}</div>
    <div style="text-align:center">${full({ back: true }, 300)}${cap('back')}</div>
    <div style="text-align:center">${full({ expr: 'joy', pose: 'walk' }, 300)}${cap('walk')}</div>
  </div>
  <div style="margin:40px 70px 0;font:400 40px 'Bagel Fat One'">Emotions</div>
  <div style="margin:10px 70px 0;display:grid;grid-template-columns:repeat(9,1fr);gap:8px;text-align:center">
    ${Object.keys(EXPR).map((e) => `<div>${head(e, 150)}${cap(e)}</div>`).join('')}
  </div>
  <div style="margin:40px 70px 0;font:400 40px 'Bagel Fat One'">Poses</div>
  <div style="margin:10px 70px 60px;display:flex;justify-content:space-between;text-align:center">
    ${[['wave', 'friendly'], ['point', 'watching'], ['think', 'confusion'], ['celebrate', 'joy'], ['shrug', 'upset'], ['facepalm', 'gusto'], ['hips', 'angry']]
      .map(([p, e]) => `<div>${full({ pose: p, expr: e }, 190)}${cap(p)}</div>`).join('')}
  </div></body></html>`;
fs.writeFileSync(path.join(OUT, 'sheet.html'), html);
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.setViewportSize({ width: 1600, height: 1800 });
  await pg.goto('file://' + path.join(OUT, 'sheet.html'));
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(600);
  await pg.screenshot({ path: path.join(OUT, 'pixy-dragon-sheet.png'), fullPage: true });
  await b.close(); console.log('sheet written');
})();
