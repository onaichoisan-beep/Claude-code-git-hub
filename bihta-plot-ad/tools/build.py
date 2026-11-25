import json, numpy as np, soundfile as sf, subprocess
P="/home/user/Claude-code-git-hub/bihta-plot-ad"
SR=44100
vo=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",P+"/assets/audio/vo_original.mp3","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32)
sync=json.load(open("sync.json")); words=json.load(open("w.json"))
vow=words[[k for k in words if k.endswith('.mp3')][0]]
CLEN={f"c{i}":l for i,l in zip(range(1,10),[10.03,10.03,8.04,10.03,8.04,8.04,8.04,10.03,10.03])}
# kind, name, clip, vo range (raw), pause after, broll media-in
L=[("B","L1","c6",(0.00,3.35),0.31,0.2),
   ("T","L2","c7",None,0.42,None),
   ("T","L3","c5",None,0.27,None),
   ("T","L4","c3",None,0.36,None),
   ("B","L5","c2",(23.34,28.28),0.34,1.5),
   ("T","L6","c8",None,0.38,None),
   ("B","L7","c1",(33.99,41.81),0.34,0.6),
   ("B","L8","c4",(42.15,45.92),0.38,2.2),
   ("T","L9","c9",None,0.29,None),
   ("E","L10","c4",(52.48,56.45),0.0,None)]
segs=[]; A=0.0
for kind,name,clip,rng,pause,mi in L:
    if kind=="T":
        y,_=sf.read(f"sync_{name}.wav"); cs,ce=sync[name]["clip_speech"]; v0,v1=sync[name]["vo"]
        # word times in output = A + (cw - cs) using clip whisper words
        wt=[(w,round(A+s-cs,2)) for w,s,e in words[clip+".mp4"] if cs-0.15<=s<=ce]
    else:
        v0,v1=rng; y=vo[int(v0*SR):int(v1*SR)]; cs=None
        wt=[(w,round(A+s-v0,2)) for w,s,e in vow if v0-0.15<=s<v1]
    segs.append(dict(kind=kind,name=name,clip=clip,A=round(A,3),alen=round(len(y)/SR,3),cs=cs,mi=mi,words=wt,audio=y))
    A+=len(y)/SR+pause
TOTAL=round(A+0.9,2)
# cuts: start of each segment's video
for i,s in enumerate(segs):
    s["start"]=0.0 if i==0 else round(s["A"]-(0.18 if s["kind"]=="T" else 0.06),3)
for i,s in enumerate(segs):
    s["end"]=segs[i+1]["start"] if i+1<len(segs) else TOTAL
    s["dur"]=round(s["end"]-s["start"],3)
    if s["kind"]=="T": s["mi"]=round(s["cs"]-(s["A"]-s["start"]),3)
out=np.zeros(int((TOTAL+0.1)*SR),np.float32)
for s in segs:
    a=int(s["A"]*SR); out[a:a+len(s["audio"])]+=s["audio"]
sf.write(P+"/assets/audio/vo_synced.wav",out,SR)
# End segment: c9 continues smiling under phone number for ~1.6s, then c4 sunset w/ end card
ed=[]
for s in segs:
    d={k:v for k,v in s.items() if k!="audio"}
    ed.append(d)
    print(f'{s["name"]:4} {s["kind"]} {s["clip"]} out {s["start"]:6.2f}-{s["end"]:6.2f} ({s["dur"]:.2f}s) media_in {s["mi"]} -> media_out {None if s["mi"] is None else round(s["mi"]+s["dur"],2)} / len {CLEN[s["clip"]]}  audio@{s["A"]:.2f}+{s["alen"]:.2f}')
json.dump(dict(total=TOTAL,segs=ed),open(P+"/timeline.json","w"),ensure_ascii=False,indent=1)
print("TOTAL",TOTAL)
