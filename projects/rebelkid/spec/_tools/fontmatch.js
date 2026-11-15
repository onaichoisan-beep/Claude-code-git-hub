const {chromium}=require('playwright');const fs=require('fs');
const [,,text,fontsCsv,out,weightsCsv]=process.argv;
const fonts=fontsCsv.split(',');const weights=(weightsCsv||'400').split(',');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:300}});
 let css=fonts.map((f,i)=>`@font-face{font-family:F${i};src:url(file://${process.cwd()}/web/fonts/cand/${f});}`).join('\n');
 for(let i=0;i<fonts.length;i++){for(const w of weights){for(const ls of [-0.08,-0.05,-0.03,0,0.03]){
  fs.writeFileSync(out+'.html',`<style>${css}body{margin:0;background:#000}div{font-family:F${i};font-weight:${w};font-size:160px;color:#fff;letter-spacing:${ls}em;padding:40px;white-space:nowrap;display:inline-block}</style><div>${text}</div>`);await p.goto('file://'+out+'.html');
  await p.evaluate(()=>document.fonts.ready);
  await p.locator('div').screenshot({path:`${out}/${fonts[i]}__${w}__${ls}.png`});}}}
 await b.close();})();
