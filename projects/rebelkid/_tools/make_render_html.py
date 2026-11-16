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
    const cs=el.style;let n=0;
    if(el.classList.contains('card'))k='card';else if(el.querySelector('.tb')){k='type';n=el.querySelector('.tb span:last-child').textContent.length}
    else if(el.querySelector('.ch'))k=(cs.color||'').includes('243, 248')||cs.fontFamily.includes('Familjen')?'lime':'script';
    else if(el.classList.contains('cap'))k='cap';else if(el.querySelector('textPath'))k='arc';
    else if(el.querySelector('svg'))k=el.innerHTML.includes('evenodd')?'camera':(el.innerHTML.includes('pg')?'pink':'art');
    else if(cs.fontFamily.includes('Bodoni')&&parseInt(cs.fontSize)>=100)k='serif';
    else if(cs.color&&cs.color.includes('237, 235'))k='note';
    else if(cs.color&&(cs.color.includes('95, 1, 0')))k='cardtext';
    out.push({b:b.id,t:o.on,k,n,txt:el.textContent.slice(0,30)});
    if(k==='word'||k==='cap'){}
  }}curB=null;return out};
window.ready=Promise.all([document.fonts.ready,...['assets/gingham.jpg','assets/camera.png'].map(u=>{const i=new Image();i.src=u;return i.decode()})]).then(()=>true);
</script></body></html>'''%json.dumps(picks)
open('site/render.html','w').write(head+s+tail)
