const {chromium}=require('playwright');const fs=require('fs');
const [a,b]=[+process.argv[2],+process.argv[3]];const PICK=JSON.parse(process.argv[4]);
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1200,height:2000}});const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('http://localhost:8765/render.html');await pg.waitForTimeout(3000);
await pg.evaluate(P=>{$('sw').style.width='1080px';$('sw').style.borderRadius='0';fit();ST=defState();P.forEach((k,i)=>ST.beats[i].d=k);built.key=''},PICK);
fs.mkdirSync('vid/full',{recursive:true});const st=await pg.$('#stage');
const end=Math.min(b,await pg.evaluate(()=>NF));
for(let f=a;f<end;f++){
  await pg.evaluate(f=>new Promise(r=>{let done=false;const fin=()=>{if(!done){done=true;setTimeout(r,40)}};vid.addEventListener('seeked',fin,{once:true});setTimeout(fin,600);vid.currentTime=(f+0.5)/30}),f);
  await pg.evaluate(f=>{lastRK='';render(f)},f);
  await st.screenshot({path:`vid/full/f_${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:94});
}
if(a===0){const ev=await pg.evaluate(()=>{const out=[];for(let i=0;i<BEATS.length;i++){built.key='';buildBeat(i);out.push(...built.ev)}return out});fs.writeFileSync('vid/full/events.json',JSON.stringify(ev))}
console.log('done',a,end,'errs',JSON.stringify(errs));await br.close()})();
