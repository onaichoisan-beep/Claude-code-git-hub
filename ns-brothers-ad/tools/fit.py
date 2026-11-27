import json, numpy as np, subprocess
M=json.load(open('/tmp/claude-0/-home-user-Claude-code-git-hub/27087e4f-92b6-5274-8677-945e8539474f/scratchpad/ns/mouth.json'))
SR=16000; FPS=25
vo=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","/home/user/Claude-code-git-hub/ns-brothers-ad/assets/audio/vo.mp3","-af","highpass=f=200,lowpass=f=3500","-ac","1","-ar",str(SR),"-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
hop=SR//FPS
env=np.array([np.sqrt(np.mean(vo[i:i+hop*2]**2)) for i in range(0,len(vo)-hop*2,hop)])
env=np.log(env+1e-4)
def mouth(clip,face):
    a=np.array([np.nan if x is None else x for x in M[clip][face]],float)
    idx=np.arange(len(a)); ok=~np.isnan(a); a=np.interp(idx,idx[ok],a[ok]); return a
JOBS=[("a3.mp4","360",8.58,9.50,2.6,4.2),("a4.mp4","1080",9.50,10.45,2.95,4.12),("a3.mp4","360",30.25,33.95,4.0,8.68),("a5.mp4","360",65.75,69.05,0,4.56)]
for clip,face,v0,v1,lo,hi in JOBS:
    m=mouth(clip,face); L=len(m)/FPS
    t=np.arange(v0,v1,1/FPS); e=env[(t*FPS).astype(int)]
    best=None
    for r in np.arange(0.85,1.201,0.01):
        for s in np.arange(lo,hi-r*(v1-v0)+0.001,0.02):
            vt=s+r*(t-v0); mm=np.interp(vt*FPS,np.arange(len(m)),m)
            c=np.corrcoef(e,mm)[0,1]
            if best is None or c>best[0]: best=(c,round(r,2),round(s,2))
    c,r,s=best
    print(f"{clip} VO {v0}-{v1}: best corr {c:.2f} rate {r} in-point {s:.2f} (clip end {s+r*(v1-v0):.2f}/{L:.2f})")
