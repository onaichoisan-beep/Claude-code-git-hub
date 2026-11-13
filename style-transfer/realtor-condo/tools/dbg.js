const {chromium}=require('playwright');
(async()=>{const br=await chromium.launch();const p=await br.newPage({viewport:{width:1080,height:1920}});
await p.goto('http://localhost:8765/test.html');await p.waitForFunction(()=>window.__render&&document.getElementById('loading').hidden);
await p.evaluate(()=>window.__render.on());
const r=await p.evaluate(()=>{window.__render.layer(550,'back');return window.__dbg.ITEMS.filter(it=>it.o&&it.o.box&&it.page.b.f0===499).map(it=>{const rc=it.o.i.getBoundingClientRect();return {txt:it.o.i.textContent.slice(0,30),box:it.o.box,fs:it.o.i.style.fontSize,real:[rc.left,rc.right],ow:it.o.i.offsetWidth,fonts:document.fonts.check("800 100px 'Bricolage Grotesque'")}})});
console.log(JSON.stringify(r,null,0));await br.close();})();
