# Cut dead space + the repeated "स्कूल शॉपिंग की" from a8, then warp the picture so its speech lines up with VO 0-4.15s.
import numpy as np, subprocess, librosa, json, os
A8="assets/ai/a8.mp4"; VO="assets/audio/vo.mp3"
KEEP=[(3.72,5.54),(6.34,8.56)]           # clip ranges kept (the first "स्कूल शॉपिंग की" 5.54-6.34 is dropped)
V0,V1=0.0,4.15                            # VO range of the line
SR=16000; HOP=160
def load(f,ss=None,to=None):
    a=["ffmpeg","-v","error"]+(["-ss",str(ss),"-to",str(to)] if ss is not None else [])+["-i",f,"-af","highpass=f=200,lowpass=f=4000","-ac","1","-ar",str(SR),"-f","s16le","-"]
    return np.frombuffer(subprocess.run(a,capture_output=True).stdout,np.int16).astype(np.float32)/32768
def feat(a):
    m=librosa.feature.mfcc(y=a,sr=SR,n_mfcc=13,hop_length=HOP,n_fft=512)[1:]; m=(m-m.mean(1,keepdims=True))/(m.std(1,keepdims=True)+1e-6)
    e=np.log(librosa.feature.rms(y=a,frame_length=400,hop_length=HOP)+1e-4); e=(e-e.mean())/(e.std()+1e-6)
    d=np.diff(e,prepend=e[:,:1],axis=1); d=d/(d.std()+1e-6); return np.vstack([0.5*m,2*e,1.5*d])
clip=np.concatenate([load(A8,a,b) for a,b in KEEP])
# edited-clip time -> source time
def src(t):
    for a,b in KEEP:
        if t<=b-a+1e-6: return a+t
        t-=b-a
    return KEEP[-1][1]
vo=load(VO,V0,V1)
D,wp=librosa.sequence.dtw(X=feat(vo),Y=feat(clip),metric='euclidean',global_constraints=True,band_rad=0.15); wp=wp[::-1]
fq=wp[:,0]*HOP/SR; fr=wp[:,1]*HOP/SR
def m(t): return float(np.interp(t,fq,fr))
L=sum(b-a for a,b in KEEP)
anchors=[0.0]+[t for t in np.arange(0.5,V1-V0-0.3,0.5)]+[V1-V0]
tgt=[0.0]+[m(t) for t in anchors[1:-1]]+[L]
for i in range(1,len(tgt)):   # clamp speeds to 0.75-1.3
    d=anchors[i]-anchors[i-1]; tgt[i]=tgt[i-1]+min(max(tgt[i]-tgt[i-1],0.75*d),1.3*d)
tgt=[t*L/tgt[-1] for t in tgt]
print("speeds:",[round((tgt[i+1]-tgt[i])/(anchors[i+1]-anchors[i]),2) for i in range(len(anchors)-1)])
# build pieces: each VO piece [anchors[i],anchors[i+1]] shows edited-clip [tgt[i],tgt[i+1]]
os.makedirs("/tmp/a8p",exist_ok=True); parts=[]
for i in range(len(anchors)-1):
    c0,c1=tgt[i],tgt[i+1]; out_d=anchors[i+1]-anchors[i]
    # a piece may straddle the dropped section -> split it
    segs=[]; t=c0
    while t<c1-1e-4:
        # locate the kept range holding edited time t (left-closed, right-open)
        acc=0.0
        for a,b in KEEP:
            if t < acc+(b-a)-1e-6: s0=a+(t-acc); break
            acc+=b-a
        rem=c1-t
        take=min(rem,b-s0)
        if take<1e-4: break
        segs.append((s0,s0+take)); t+=take
    for (s0,s1) in segs:
        frac=(s1-s0)/(c1-c0); d=out_d*frac; f=f"/tmp/a8p/p{len(parts):02d}.mp4"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{s0:.3f}","-t",f"{s1-s0:.3f}","-i",A8,"-vf",f"setpts=(PTS-STARTPTS)*{d/(s1-s0):.4f},fps=30","-an","-c:v","libx264","-crf","14","-pix_fmt","yuv420p","-t",f"{d:.3f}",f],check=True)
        parts.append(f)
open("/tmp/a8p/list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","/tmp/a8p/list.txt","-c:v","libx264","-crf","14","-pix_fmt","yuv420p","assets/ai/a8_opener_synced.mp4"],check=True)
print(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","assets/ai/a8_opener_synced.mp4"],capture_output=True,text=True).stdout)
