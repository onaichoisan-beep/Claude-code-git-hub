# Place each cue's Roman words on real speech: speech intervals = whisper(hi) words inside the cue window.
import json,re
W=json.load(open('aroll/whisper_hi_words.json'))
src=open('site/data.js').read()
cues=json.loads(re.search(r'window.CUES=(\[.*?\]);',src).group(1))
words=json.loads(re.search(r'window.WORDS=(\[.*?\]);',src).group(1))
out=[];moved=[]
for ci,q in enumerate(cues):
    ws=[w for w in words if w['c']==ci]
    sp=[(max(s,q['s']-0.08),min(e,q['e'])) for s,e,_ in W if s<q['e']-0.02 and e>q['s']-0.08 and (s+e)/2>=q['s']-0.08]
    sp=[(s,e) for s,e in sp if e>s]
    total=sum(e-s for s,e in sp)
    if not sp or total<0.45*(q['e']-q['s']): out+=ws;continue
    wt=[len(w['w'])+1.0 for w in ws];T=sum(wt);acc=0
    def at(frac):
        x=frac*total
        for s,e in sp:
            if x<=e-s: return s+x
            x-=e-s
        return sp[-1][1]
    for w,k in zip(ws,wt):
        s=at(acc/T);acc+=k;e=at(acc/T)
        if ws.index(w)==0: s=max(sp[0][0],q['s']-0.08)
        moved.append(s-w['s']);out.append(dict(w=w['w'],s=round(s,3),e=round(e,3),c=ci))
src=re.sub(r'window.WORDS=\[.*?\];','window.WORDS='+json.dumps(out,ensure_ascii=False)+';',src,flags=re.S)
open('site/data.js','w').write(src)
import numpy as np;m=np.abs(moved);print('words',len(out),'mean shift %.3fs, max %.3fs'%(m.mean(),m.max()))
