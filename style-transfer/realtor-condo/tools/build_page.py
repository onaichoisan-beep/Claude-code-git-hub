import json
s=open('web/builder.tpl.html').read()
s=s.replace("""  o.box={l:L,t:y,r:L+wd,b:y+ht,w:wd,h:ht};
  return o.box;""","""  o.box={l:L,t:y,r:L+wd,b:y+ht,w:wd,h:ht};
  o.i.querySelectorAll('.ch.gt').forEach(c=>{c.style.backgroundSize=wd+'px 100%';c.style.backgroundPosition=(-c.offsetLeft)+'px 0';});
  return o.box;""") if "backgroundSize=wd" not in s else s
s=s.replace("""  lk.style.opacity=op;[...lk.children]""","""  lk.style.opacity=op;const pk=t<B-3?0:t<B?(t-B+3)/3:t<B+2?1:1-clamp((t-B-2)/4);lk.style.background=`rgba(255,255,255,${pk})`;[...lk.children]""") if "const pk=" not in s else s
open('web/builder.tpl.html','w').write(s)
W=json.load(open('aroll/words.json'));W=[{'w':w['w'],'s':w['s'],'e':w['e']} for w in W]
F=open('web/faces.js').read().strip()[len('window.FACES='):-1]
page=s.replace('/*__DATA__*/','const WORDS='+json.dumps(W,separators=(',',':'))+';\nconst FACES='+F+';')
open('web/index.html','w').write(page)
open('web/test.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><style>[hidden]{display:none!important}body{margin:0}</style></head><body>'+page+'</body></html>')
print('built',len(page))
