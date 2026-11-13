const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.setContent(`<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,800&display=block" rel="stylesheet"><canvas id=c width=600 height=300></canvas>`);
await p.evaluate(()=>document.fonts.load("800 100px 'Bricolage Grotesque'"));await p.evaluate(()=>document.fonts.load("300 100px 'Bricolage Grotesque'"));await p.waitForTimeout(500);
const r=await p.evaluate(()=>{const c=document.getElementById('c').getContext('2d');const o={};for(const w of [300,800]){c.font=w+" 100px 'Bricolage Grotesque'";const x=c.measureText('x'),H=c.measureText('H');o[w]={xh:x.actualBoundingBoxAscent,cap:H.actualBoundingBoxAscent,wAur:c.measureText('Aur best part').width}}return o});
console.log(JSON.stringify(r));await b.close();})();
