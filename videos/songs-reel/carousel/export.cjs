// Export each carousel page as a 1080x1350 PNG. Run from videos/songs-reel.
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1400 }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.resolve("carousel/carousel.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState("networkidle");
  for (let i = 1; i <= 6; i++) {
    await page.locator("#s" + i).screenshot({ path: `carousel/page-${i}.png` });
  }
  await browser.close();
  console.log("exported 6 pages");
})();
