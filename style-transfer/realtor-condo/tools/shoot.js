const {chromium}=require('playwright');
const frames=process.argv[2].split(',').map(Number), out=process.argv[3], picks=process.argv[4]||'';
(async()=>{const b=await chromium.launch({args:['--autoplay-policy=no-user-gesture-required']});const p=await b.newPage({viewport:{width:1300,height:1000}});
const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(String(e)));
await p.goto('http://localhost:8765/test.html');

await p.waitForFunction(()=>document.getElementById('loading').hidden,null,{timeout:30000});
if(picks){await p.evaluate(k=>window.__dbg.pickAll(+k),picks);}
let i=0;for(const f of frames){await p.evaluate(f=>{window.__dbg.seekF(f)},f);await p.waitForTimeout(350);const el=await p.$('#stageBox');await el.screenshot({path:`${out}_${String(i).padStart(2,'0')}.png`});i++;}
await p.screenshot({path:out+'_full.png'});
console.log('errors:',errs.slice(0,5));await b.close();})();
