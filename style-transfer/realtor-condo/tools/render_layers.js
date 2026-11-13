const {chromium}=require('playwright');const fs=require('fs');
const [a,b]=process.argv.slice(2).map(Number);const out='render';
(async()=>{const br=await chromium.launch();const p=await br.newPage({viewport:{width:1080,height:1920}});
await p.goto('http://localhost:8765/test.html');
await p.waitForFunction(()=>window.__render&&document.getElementById('loading').hidden,null,{timeout:60000});
await p.evaluate(()=>window.__render.on());await p.waitForTimeout(300);
if(a===0){fs.writeFileSync(out+'/ev.json',JSON.stringify(await p.evaluate(()=>window.__render.ev())));
 const cams=await p.evaluate(n=>{const r=[];for(let f=0;f<n;f++){const c=window.__render.cam(f);r.push([c.sc,c.px,c.py]);}return r;},885);fs.writeFileSync(out+'/cam.json',JSON.stringify(cams));}
const w=await p.$('#world');
for(let f=a;f<b;f++){
  for(const L of ['back','front','leak']){const r=await p.evaluate(([f,L])=>window.__render.layer(f,L),[f,L]);if(L==='leak'&&!r.leak)continue;
    await w.screenshot({path:`${out}/${L}_${String(f).padStart(4,'0')}.png`,omitBackground:true});}
}
await br.close();})();
