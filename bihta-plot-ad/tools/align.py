import numpy as np, subprocess, json, librosa, soundfile as sf, os
VO=[f for f in os.listdir('/root/.claude/uploads/27087e4f-92b6-5274-8677-945e8539474f') if f.endswith('.mp3')][0]
VO='/root/.claude/uploads/27087e4f-92b6-5274-8677-945e8539474f/'+VO
SR=44100
def load(f):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
def bp(f):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-af","highpass=f=200,lowpass=f=4000","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
vo=load(VO); vo16=bp(VO)
words=json.load(open('w.json'))
vow=[(w,s,e) for w,s,e in words[[k for k in words if k.endswith('.mp3')][0]]]
HOP=160
def feat(a):
    m=librosa.feature.mfcc(y=a,sr=16000,n_mfcc=13,hop_length=HOP,n_fft=512)[1:]
    m=(m-m.mean(1,keepdims=True))/(m.std(1,keepdims=True)+1e-6)
    e=librosa.feature.rms(y=a,frame_length=400,hop_length=HOP)
    e=np.log(e+1e-4); e=(e-e.mean())/(e.std()+1e-6)
    d=np.diff(e,prepend=e[:,:1],axis=1); d=d/(d.std()+1e-6)
    return np.vstack([0.5*m,2*e,1.5*d])
def stretch(x, ratio):
    # ratio = out_len/in_len ; rubberband tempo = in/out
    p=subprocess.run(["ffmpeg","-v","error","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af",f"rubberband=tempo={1/ratio:.5f}:pitchq=quality:formant=preserved:window=short","-f","f32le","-"],input=x.astype(np.float32).tobytes(),capture_output=True)
    return np.frombuffer(p.stdout,np.float32)
# line: name, vo_start, vo_end, clip, clip_search_from, clip_search_to
LINES=[("L2",3.66,9.81,"c7",1.45,7.62),("L3",10.23,17.02,"c5",2.12,7.74),("L4",17.29,22.98,"c3",1.40,7.22),
       ("L6",28.62,33.61,"c8",1.30,6.97),("L9",46.30,52.19,"c9",2.0,8.06)]
out={}
for name,v0,v1,clip,c0,c1 in LINES:
    q=feat(vo16[int(v0*16000):int(v1*16000)])
    cl=bp(f"clips/{clip}.mp4")
    r=feat(cl[int(c0*16000):int(c1*16000)])
    D,wp=librosa.sequence.dtw(X=q,Y=r,metric='euclidean',global_constraints=True,band_rad=0.12)
    wp=wp[::-1]
    fq=wp[:,0]*HOP/16000; fr=wp[:,1]*HOP/16000+c0
    def m(t):  # vo-relative t -> clip time
        idx=np.where(np.abs(fq-t)<0.006)[0]
        return float(np.mean(fr[idx])) if len(idx) else float(np.interp(t,fq,fr))
    cs,ce=m(0.0),m(v1-v0)
    # anchors at VO word starts inside line, spaced >=0.5s
    anc=[0.0]
    for w,s,e in vow:
        t=s-v0
        if 0.4<t<(v1-v0)-0.4 and t-anc[-1]>=0.5: anc.append(t)
    anc.append(v1-v0)
    tgt=[m(t)-cs for t in anc]
    # monotonic + clamp ratios
    for i in range(1,len(tgt)):
        d=anc[i]-anc[i-1]; tgt[i]=tgt[i-1]+min(max(tgt[i]-tgt[i-1],0.65*d),1.5*d)
    total=ce-cs; scale=total/tgt[-1]; tgt=[t*scale for t in tgt]
    pieces=[]
    for i in range(len(anc)-1):
        a=vo[int((v0+anc[i])*SR):int((v0+anc[i+1])*SR)]
        n=int(round(tgt[i+1]*SR))-int(round(tgt[i]*SR))
        y=stretch(a,n/len(a))
        y=np.pad(y,(0,max(0,n-len(y))))[:n]
        f=min(64,len(y)//4); y[:f]*=np.linspace(0,1,f); y[-f:]*=np.linspace(1,0,f)
        pieces.append(y)
    y=np.concatenate(pieces)
    sf.write(f"sync_{name}.wav",y,SR)
    ratios=[round((tgt[i+1]-tgt[i])/(anc[i+1]-anc[i]),2) for i in range(len(anc)-1)]
    out[name]=dict(clip=clip,vo=[v0,v1],clip_speech=[round(cs,3),round(ce,3)],ratios=ratios)
    print(name,clip,f"clip speech {cs:.2f}-{ce:.2f} ({ce-cs:.2f}s) vs VO {v1-v0:.2f}s",ratios)
json.dump(out,open("sync.json","w"),indent=1)
