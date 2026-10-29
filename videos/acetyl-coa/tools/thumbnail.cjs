// YouTube thumbnails for reel #2: vertical 1080x1920 (Shorts) and 1280x720 (feed / search).
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const { hood } = require('./dragon_pixy.cjs');
const OUT = path.join(__dirname, '..', 'renders');
const font = (f) => 'file://' + path.join(__dirname, '..', 'assets', 'fonts', f);
const CSS = `@font-face{font-family:"Playfair Display";font-weight:900;src:url("${font('playfair-900.ttf')}")}
  @font-face{font-family:"Bagel Fat One";src:url("${font('bagel.ttf')}")}
  @font-face{font-family:"Inter";font-weight:800;src:url("${font('inter-800.ttf')}")}
  *{margin:0;padding:0;box-sizing:border-box} body{background:#feefb8;color:#432f2e;overflow:hidden}
  .bg{position:absolute;inset:0;background:radial-gradient(circle,rgba(159,192,214,.5) 4px,transparent 5px) 0 0/56px 56px,#feefb8}
  .burst{position:absolute;border-radius:50%;background:repeating-conic-gradient(#f6d365 0 10deg,#feefb8 10deg 20deg);opacity:.9}
  .stamp{position:absolute;background:#e8743b;color:#fffcf2;border:10px solid #432f2e;border-radius:28px;font-family:"Bagel Fat One";text-align:center;transform:rotate(-6deg)}
  .q{position:absolute;font-family:"Playfair Display";font-weight:900;text-align:center;line-height:1.02}
  .q span{color:#b2461a}
  .pill{position:absolute;background:#432f2e;color:#feefb8;font-family:"Bagel Fat One";border-radius:999px;text-align:center}
  .opt{position:absolute;display:flex;gap:16px}
  .opt div{background:#fffcf2;border:7px solid #432f2e;border-radius:26px;font-family:"Inter";font-weight:800;text-align:center}
  .bang{position:absolute;background:#f6d365;border:9px solid #432f2e;border-radius:50%;font-family:"Bagel Fat One";text-align:center}`;
const face = (w) => `<svg viewBox="110 40 380 390" width="${w}" height="${w * 390 / 380}">${hood('shock')}</svg>`;

const vertical = `<html><head><style>${CSS}</style></head><body style="width:1080px;height:1920px;position:relative">
  <div class="bg"></div>
  <div class="stamp" style="left:250px;top:150px;width:580px;height:150px;font-size:100px;line-height:126px">NEET 2013</div>
  <div class="q" style="left:40px;top:370px;width:1000px;font-size:118px">Fats, Carbs<br>&amp; Proteins ka<br><span>COMMON</span> dost?</div>
  <div class="opt" style="left:70px;top:890px;width:940px;justify-content:center">
    ${['A', 'B', 'C', 'D'].map((k) => `<div style="width:210px;height:150px;font-size:96px;line-height:136px">${k}</div>`).join('')}</div>
  <div class="burst" style="left:190px;top:1080px;width:700px;height:700px"></div>
  <div style="position:absolute;left:215px;top:1100px">${face(650)}</div>
  <div class="bang" style="left:800px;top:1110px;width:190px;height:190px;font-size:150px;line-height:190px;transform:rotate(12deg)">!</div>
  <div class="pill" style="left:160px;top:1760px;width:760px;height:120px;font-size:64px;line-height:120px">99% galat karte hain 😳</div>
</body></html>`;

const landscape = `<html><head><style>${CSS}</style></head><body style="width:1280px;height:720px;position:relative">
  <div class="bg"></div>
  <div class="burst" style="left:770px;top:90px;width:560px;height:560px"></div>
  <div style="position:absolute;left:800px;top:110px">${face(500)}</div>
  <div class="bang" style="left:1110px;top:60px;width:140px;height:140px;font-size:110px;line-height:140px;transform:rotate(12deg)">!</div>
  <div class="stamp" style="left:50px;top:40px;width:420px;height:110px;font-size:72px;line-height:90px">NEET 2013</div>
  <div class="q" style="left:40px;top:190px;width:760px;font-size:96px;text-align:left">Fats, Carbs &amp;<br>Proteins ka<br><span>COMMON</span> dost?</div>
  <div class="pill" style="left:50px;top:580px;width:620px;height:96px;font-size:52px;line-height:96px">99% galat karte hain 😳</div>
</body></html>`;

(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [name, html, w, h] of [['thumb-shorts-1080x1920.png', vertical, 1080, 1920], ['thumb-youtube-1280x720.png', landscape, 1280, 720]]) {
    await p.setViewportSize({ width: w, height: h });
    const f = path.join(OUT, name + '.html'); fs.writeFileSync(f, html); await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400); fs.unlinkSync(f);
    await p.screenshot({ path: path.join(OUT, name) });
  }
  await b.close(); console.log('thumbnails written');
})();
