const {chromium}=require('playwright');const fs=require('fs');
const beats=JSON.parse(process.argv[2]);
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1200,height:2000}});const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('http://localhost:8765/render.html');await pg.waitForTimeout(3000);
await pg.evaluate(()=>{$('sw').style.width='1080px';$('sw').style.borderRadius='0';fit();});
// stop the live loop from fighting our renders
const st=await pg.$('#stage');
for(const bi of beats){for(const k of ['A','B','C']){
  const dir=`vid/b${String(bi+1).padStart(2,'0')}_${k}`;fs.mkdirSync(dir,{recursive:true});
  const [f0,f1,ev]=await pg.evaluate(([bi,k])=>{ST=defState();ST.beats[bi].d=k;built.key='';buildBeat(bi);return[beatStart(bi),beatEnd(bi),built.ev]},[bi,k]);
  fs.writeFileSync(dir+'/events.json',JSON.stringify({f0,f1,ev}));
  for(let f=f0;f<f1;f++){
    await pg.evaluate(f=>new Promise(r=>{vid.currentTime=(f+0.5)/30;let done=false;const fin=()=>{if(!done){done=true;setTimeout(r,40)}};vid.addEventListener('seeked',fin,{once:true});setTimeout(fin,600)}),f);
    await pg.evaluate(f=>{lastRK='';render(f)},f);
    await st.screenshot({path:`${dir}/f_${String(f-f0).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});
  }
  console.log('done',dir,f1-f0);
}}
console.log('errs',errs);await b.close()})();
