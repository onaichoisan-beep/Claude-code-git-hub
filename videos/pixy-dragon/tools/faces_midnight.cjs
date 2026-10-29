// Large 3x3 emotion close-up of the dragon-hood face.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const { hood, EXPR } = require('./dragon_pixy_midnight.cjs');
const OUT = path.join(__dirname, '..', 'renders');
const cell = (e) => `<div style="text-align:center"><svg viewBox="110 40 380 390" width="330" height="338">${hood(e)}</svg>
  <div style="font:800 28px Inter;color:#132441;letter-spacing:.06em">${e}</div></div>`;
const html = `<html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@800&display=block" rel="stylesheet"></head>
<body style="margin:0;width:1200px;background:#87BBD7"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px 0;padding:50px 30px">
${Object.keys(EXPR).map(cell).join('')}</div></body></html>`;
fs.writeFileSync(path.join(OUT, 'faces-midnight.html'), html);
(async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.setViewportSize({ width: 1200, height: 1300 });
  await p.goto('file://' + path.join(OUT, 'faces-midnight.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(OUT, 'pixy-dragon-emotions-midnight.png'), fullPage: true }); await b.close(); console.log('ok'); })();
