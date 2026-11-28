# Sanity check: for words both transcripts share, where does the warped clip put them vs the VO?
import json, numpy as np, librosa, subprocess, sys
sys.argv=['x']; exec(open('tools/sync_lines.py').read().split('report = {}')[0])
W=json.load(open(sys_path)) if False else json.load(open('/tmp/claude-0/-home-user-Claude-code-git-hub/27087e4f-92b6-5274-8677-945e8539474f/scratchpad/ab/w_med.json'))
vow=W['vo.mp3']
for name, clip, v0, v1, keep in LINES:
    cw=W[clip+'.mp4']
    ca=np.concatenate([load(f"assets/ai/{clip}.mp4",a,b) for a,b in keep]); va=load(VO,v0,v1)
    D,wp=librosa.sequence.dtw(X=feat(va),Y=feat(ca),metric="euclidean",global_constraints=True,band_rad=0.2); wp=wp[::-1]
    fq=wp[:,0]*HOP/SR; fr=wp[:,1]*HOP/SR
    def e2s(t):  # edited clip time -> source
        acc=0
        for a,b in keep:
            if t<acc+(b-a): return a+t-acc
            acc+=b-a
        return keep[-1][1]
    errs=[]
    vw=[(w,s) for w,s,e in vow if v0<=s<v1]
    for w,s in vw:
        src_t=e2s(float(np.interp(s-v0,fq,fr)))
        m=[cs for cwd,cs,ce in cw if cwd[:2]==w[:2] and abs(cs-src_t)<1.0]
        if m: errs.append(round(min(m,key=lambda x:abs(x-src_t))-src_t,2))
    print(name, 'matched',len(errs),'of',len(vw),'median |err|',np.median(np.abs(errs)) if errs else None, errs[:12])
