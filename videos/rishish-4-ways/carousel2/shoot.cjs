const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  await p.goto('file://' + __dirname + '/carousel.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  for (let i = 1; i <= 8; i++) await (await p.$('#s' + i)).screenshot({ path: `slide_${i}.png` });
  await b.close();
})();
