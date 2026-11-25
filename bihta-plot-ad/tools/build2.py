import json, numpy as np, soundfile as sf, subprocess
P="/home/user/Claude-code-git-hub/bihta-plot-ad"; SR=44100
vo=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",P+"/assets/audio/vo_original.mp3","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32)
sy=json.load(open("sync.json")); W=json.load(open("w.json")); vow=W[[k for k in W if k.endswith('.mp3')][0]]
CLEN={"c1":10.03,"c2":10.03,"c3":8.04,"c4":10.03,"c5":8.04,"c6":8.04,"c7":8.04,"c8":10.03,"c9":10.03}
def fade(y):
    f=min(80,len(y)//4); y=y.copy(); y[:f]*=np.linspace(0,1,f); y[-f:]*=np.linspace(1,0,f); return y
# shot = (clip, media_in, rate, mirror, zoom) ; "GFX:name" for full-screen graphic
LINES=[
 ("L1",None,[("B",None,None,[("c6",0.2,1,0,1.22)])],0.31,(0.00,3.35)),
 ("L2","c7",[("F",0,4,None),("B",4,6,[("c4",0.0,1,0,1.0)]),("F",6,8,None)],0.42,None),
 ("L3","c5",[("F",0,2,None),("B",2,9,[("c1",5.3,1,0,1.0),("c2",7.0,1,1,1.1)])],0.27,None),
 ("L4","c3",[("F",0,3,None),("B",3,6,[("c1",8.1,0.77,1,1.15)]),("F",6,8,None)],0.36,None),
 ("L5",None,[("B",None,None,[("c2",1.5,1,0,1.0)])],0.34,(23.34,28.28)),
 ("L6","c8",[("B",0,2,["GFX:baat"]),("F",2,4,None),("B",4,7,[("c6",0.4,1,1,1.3)])],0.38,None),
 ("L7",None,[("B",None,None,[("c1",0.6,1,0,1.08),("c6",4.2,1,0,1.0)])],0.34,(33.99,41.81)),
 ("L8",None,[("B",None,None,[("c4",2.2,1,0,1.15)])],0.38,(42.15,45.92)),
 ("L9","c9",[("B",0,3,[("c2",0.0,0.85,1,1.12)]),("F",3,6,None),("B",6,7,["GFX:invest"]),("F",7,8,None)],0.29,None),
 ("L10",None,[("E",None,None,None)],0.0,(52.48,56.45)),
]
L7SPLIT=38.62  # raw VO time where c1 -> c6 inside L7
out=np.zeros(int(62*SR),np.float32); A=0.0
secs=[]; wordmap=[]   # (vo_time_start, vo_time_end, out_start, out_end) linear pieces
for name,clip,plan,pause,rng in LINES:
    if clip is None:
        v0,v1=rng; y=fade(vo[int(v0*SR):int(v1*SR)]); out[int(A*SR):int(A*SR)+len(y)]+=y
        secs.append(dict(line=name,kind=plan[0][0],A=A,alen=len(y)/SR,shots=plan[0][3],raw=(v0,v1)))
        wordmap.append((v0,v1,A,A+len(y)/SR)); A+=len(y)/SR+pause; continue
    d=sy[name]; v0=d['vo'][0]; anc=d['anc']; tgt=d['tgt']; cs=d['clip_speech'][0]
    syn,_=sf.read(f"sync_{name}.wav")
    for kind,i,j,shots in plan:
        if kind=="F":
            y=fade(syn[int(round(tgt[i]*SR)):int(round(tgt[j]*SR))])
            for k in range(i,j): wordmap.append((v0+anc[k],v0+anc[k+1],A+tgt[k]-tgt[i],A+tgt[k+1]-tgt[i]))
            secs.append(dict(line=name,kind="F",A=A,alen=len(y)/SR,clip=clip,clip_t=cs+tgt[i]))
        else:
            a,b=v0+anc[i],v0+anc[j]; y=fade(vo[int(a*SR):int(b*SR)])
            wordmap.append((a,b,A,A+len(y)/SR))
            secs.append(dict(line=name,kind="B",A=A,alen=len(y)/SR,shots=shots,raw=(a,b)))
        out[int(A*SR):int(A*SR)+len(y)]+=y; A+=len(y)/SR
    A+=pause
TOTAL=round(A+0.9,2); out=out[:int((TOTAL+0.05)*SR)]
sf.write(P+"/assets/audio/vo_synced.wav",out,SR)
def o(t):
    for a,b,x,y in wordmap:
        if a-0.01<=t<=b+0.01: return round(x+(t-a)*(y-x)/(b-a),3)
    return None
# video cut times
for k,s in enumerate(secs):
    if k==0: s['vs']=0.0; continue
    prev=secs[k-1]; gap = s['A']-(prev['A']+prev['alen'])
    if s['kind']=="F": s['vs']=s['A']-0.12
    elif gap>0.05: s['vs']=s['A']-0.06
    else: s['vs']=s['A']-0.03
for k,s in enumerate(secs): s['ve']=secs[k+1]['vs'] if k+1<len(secs) else TOTAL
shots=[]
for s in secs:
    dur=s['ve']-s['vs']
    if s['kind']=="F":
        mi=s['clip_t']-(s['A']-s['vs']); shots.append(dict(type="video",clip=s['clip'],start=s['vs'],dur=dur,mi=mi,rate=1,mirror=0,zoom=1.0,face=1,line=s['line']))
    elif s['kind']=="E":
        pass
    else:
        sh=s['shots']
        if s['line']=="L7":
            cut=o(L7SPLIT)-0.05; parts=[(s['vs'],cut-s['vs']),(cut,s['ve']-cut)]
        elif len(sh)==2: parts=[(s['vs'],dur/2),(s['vs']+dur/2,dur/2)]
        else: parts=[(s['vs'],dur)]
        for (st,du),x in zip(parts,sh):
            if isinstance(x,str): shots.append(dict(type="gfx",name=x[4:],start=st,dur=du,line=s['line']))
            else:
                c,mi,r,m,z=x; shots.append(dict(type="video",clip=c,start=st,dur=du,mi=mi,rate=r,mirror=m,zoom=z,face=0,line=s['line']))
# L9's last face section runs on under the start of the end card; end card c4 from (L10 A - ...) 
e=[s for s in secs if s['kind']=="E"][0]
last=[x for x in shots if x['line']=="L9"][-1]
endStart=e['A']+1.15
last['dur']=endStart+0.45-last['start']
shots.append(dict(type="video",clip="c4",start=endStart,dur=TOTAL-endStart,mi=6.2,rate=1,mirror=0,zoom=1.0,face=0,line="END",fadein=1))
for x in shots:
    x['start']=round(x['start'],3); x['dur']=round(x['dur'],3)
    if x['type']=="video":
        x['mi']=round(x['mi'],3); end=x['mi']+x['dur']*x['rate']
        assert x['mi']>=0 and end<=CLEN[x['clip']]+0.01,(x,end)
    print(x)
cues={}
def cue(key,word,line_hint=None,nth=0):
    hits=[s for w,s,e in vow if word in w and (line_hint is None or line_hint[0]<=s<line_hint[1])]
    cues[key]=o(hits[nth])
sec={s['line']:s for s in secs}
cue('peace','पीस्फल'); cue('strong','स्ट्रोंग'); cue('to','तो',(7,9))
cue('iit','IIT'); cue('nsm','NSMCH'); cue('rail','Railway'); cue('air','भेहता',(19,23)); cue('aiims','आमस'); cue('nit','NIT')
cue('kampa','कंपा',(29,33)); cue('m200','200'); cue('nh','NH'); cue('sh','SH'); cue('bk','भेहता',(36,38)); cue('patna','पतना'); cue('aur','औरंगाबाद'); cue('excel','एकसलिंट')
cue('khaas','सबसे',(42,43)); cue('plot8','प्लोट',(43,44)); cue('six8','6',(44,45)); cue('aaj','आज',(46,47)); cue('kal','कल',(47.5,49)); cue('smart','समाद'); cue('call','कोल')
cue('ph1','प्लस'); cue('ph2','एट',(53,54)); cue('ph3','एट',(54.5,55.5))
for n in ['L2','L3','L4','L5','L6','L7','L8','L9','L10']:
    first=[s for s in secs if s['line']==n]; cues[n]=round(first[0]['A'],3); cues[n+'v']=round(first[0]['vs'],3)
    last=first[-1]; cues[n+'e']=round(last['A']+last['alen'],3)
cues['end']=round(endStart,3); cues['total']=TOTAL
gf=[x for x in shots if x['type']=="gfx"]; 
for x in gf: cues['gfx_'+x['name']]=x['start']; cues['gfx_'+x['name']+'_e']=round(x['start']+x['dur'],3)
print(json.dumps(cues,ensure_ascii=False)); print("TOTAL",TOTAL)
json.dump(dict(total=TOTAL,shots=shots,cues=cues),open(P+"/timeline.json","w"),ensure_ascii=False,indent=1)
