// node render.js <first> <last>  -> vid/f_%04d.jpg (1080x1920)
const {chromium}=require('playwright');const fs=require('fs');
const [a,b]=process.argv.slice(2).map(Number);fs.mkdirSync('vid',{recursive:true});
(async()=>{const br=await chromium.launch({args:['--allow-file-access-from-files']});const p=await br.newPage({viewport:{width:1080,height:1920}});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file://'+process.cwd()+'/site/render.html');await p.evaluate(()=>window.ready);await p.waitForTimeout(500);
 const t0=Date.now();
 for(let f=a;f<=b;f++){await p.evaluate(f=>window.renderAt(f),f);
   await p.screenshot({path:`vid/f_${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:93,clip:{x:0,y:0,width:1080,height:1920}});
   if(f%200==0)console.log(f,((Date.now()-t0)/(f-a+1)).toFixed(0)+'ms/f');}
 console.log('done',a,b,'errors',JSON.stringify(errs.slice(0,5)));await br.close();})();
