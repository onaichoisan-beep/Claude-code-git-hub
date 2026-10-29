// Exports the official Dr. Dragon Pixy asset pack: every emotion (head) and pose (full body) as SVG + transparent PNG.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const { pixy, hood, EXPR, POSES } = require('./dragon_pixy.cjs');
const OUT = path.join(__dirname, '..', 'final');
const fontFace = `<defs><style>@font-face{font-family:"Bagel Fat One";src:url("https://fonts.gstatic.com/s/bagelfatone/v2/hYkPPucsQOr5dy02WmQr5Zkd0B4.ttf")}</style></defs>`;
const files = [];
for (const e of Object.keys(EXPR)) files.push([`emotions/${e}`, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="110 40 380 390" width="760" height="780">${hood(e)}</svg>`, 760, 780]);
for (const p of Object.keys(POSES)) {
  const expr = { wave: 'friendly', point: 'watching', think: 'confusion', celebrate: 'joy', shrug: 'upset', facepalm: 'gusto', hips: 'sly', walk: 'joy', stand: 'friendly' }[p];
  files.push([`poses/${p}`, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="30 40 540 900" width="1080" height="1800">${fontFace}${pixy({ pose: p, expr })}</svg>`, 1080, 1800]);
}
files.push([`poses/back`, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="30 40 540 900" width="1080" height="1800">${pixy({ back: true })}</svg>`, 1080, 1800]);
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  for (const [name, svg, w, h] of files) {
    fs.mkdirSync(path.join(OUT, path.dirname(name)), { recursive: true });
    fs.writeFileSync(path.join(OUT, name + '.svg'), svg);
    await pg.setViewportSize({ width: w, height: h });
    await pg.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(150);
    await pg.locator('svg').screenshot({ path: path.join(OUT, name + '.png'), omitBackground: true });
  }
  await b.close(); console.log(files.length, 'assets exported');
})();
