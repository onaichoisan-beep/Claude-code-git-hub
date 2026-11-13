const {chromium}=require('playwright');
const fams=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:200}});
for(const f of fams){const [fam,w]=f.split(':');
 await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=${fam.replace(/ /g,'+')}:wght@${w}&display=block" rel="stylesheet"></head><body style="margin:0;background:#000"><div id=t style="font-family:'${fam}';font-weight:${w};font-size:120px;color:#fff;letter-spacing:-0.03em;padding:20px;white-space:nowrap;display:inline-block">Aur best part</div></body></html>`);
 await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
 await (await p.$('#t')).screenshot({path:`an/font/${fam.replace(/ /g,'_')}_${w}.png`});}
await b.close();})();
