import json,sys
picks=json.load(open('src/picks_v1.json'))['picks']
s=open('site/index.html').read()
head='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080">
<script>window.RENDER=true;</script>
<style>header,.tbar,.tl,.hint,.beats,.toast{display:none!important} body{padding:0!important;margin:0!important;background:#000!important}
main{display:block!important;padding:0!important} .stagecol{position:static!important}
.phone{max-width:none!important;width:1080px!important;border-radius:0!important;box-shadow:none!important}
#av{display:none} #fr{position:absolute;left:0;top:0;width:1080px;height:1920px}</style></head><body>'''
tail='''<script>
const PK=%s;for(const k in PK)picks[k]=PK[k].design;
const fr=document.createElement('img');fr.id='fr';spk.appendChild(fr);
let curB=null;
window.renderAt=async function(f){const t=(f-1)/30+0.0001;const b=beatAt(t);
  if(curB!==b){build(b);curB=b}
  fr.src='../aroll/f/a_'+String(f).padStart(4,'0')+'.jpg';await fr.decode();
  update(t);return true};
window.events=function(){const out=[];for(const b of BEATS){build(b);
  for(const o of ELS){const el=o.el;let k='word';
    if(el.classList.contains('card'))k='card';else if(el.querySelector('.tb'))k='type';else if(el.querySelector('.ch'))k='accent';
    else if(el.classList.contains('cap'))k='cap';else if(el.querySelector('svg'))k='art';
    out.push({b:b.id,t:o.on,k,txt:el.textContent.slice(0,30)});
    if(k==='word'||k==='cap'){}
  }}curB=null;return out};
window.ready=document.fonts.ready.then(()=>true);
</script></body></html>'''%json.dumps(picks)
open('site/render.html','w').write(head+s+tail)
