const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1300,height:1000}});
 const errs=[]; pg.on('pageerror',e=>errs.push(e.message)); pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await pg.goto('http://localhost:8765/test.html'); await pg.waitForTimeout(2500); console.log(await pg.evaluate(()=>[vid.readyState, vid.duration, document.fonts.check('italic 900 92px Saira'), vid.currentSrc]));
 const shots=JSON.parse(process.argv[2]);
 for(const [name,setup,f] of shots){
   await pg.evaluate(setup); await pg.evaluate(f=>{seekF(f)},f);
   await pg.evaluate(()=>new Promise(r=>{if(!vid.seeking)return r();vid.addEventListener('seeked',r,{once:true})}));
   await pg.waitForTimeout(150); await pg.evaluate(f=>render(f),f);
   const st=await pg.$('#stage');
   await pg.evaluate(()=>{const s=document.getElementById('stage');s.dataset.t=s.style.transform;s.style.transform="scale(1)";document.getElementById("sw").style.width="1080px";});
   await (await pg.$('#sw')).screenshot({path:`/home/user/work/proj/an/b_${name}.png`});
   await pg.evaluate(()=>{const s=document.getElementById('stage');document.getElementById('sw').style.width='';fit()});
 }
 await pg.screenshot({path:'/home/user/work/proj/an/b_page.png'});
 console.log('errors:',JSON.stringify(errs)); await b.close();
})();
