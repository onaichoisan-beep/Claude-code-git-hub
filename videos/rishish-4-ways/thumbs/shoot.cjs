const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 4000 } });
  await p.goto('file://' + __dirname + '/thumbs.html'); await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  for (let i = 1; i <= 6; i++) await (await p.$('#t' + i)).screenshot({ path: `thumbnail_${i}.png` });
  await b.close();
})();
