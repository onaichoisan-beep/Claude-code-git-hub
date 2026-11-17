import sys, numpy as np
from edl import BURN, LEAK
w,h,FPS,DUR=270,480,30,75.0
yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
rng=np.random.default_rng(3)
def blobs(n,seed):
    r=np.random.default_rng(seed)
    return [(r.uniform(-.3,1.3),r.uniform(-.2,1.2),r.uniform(-.9,.9),r.uniform(-.9,.9),r.uniform(.25,.6)) for _ in range(n)]
def leakblobs(seed):
    r=np.random.default_rng(seed); side=-.15 if seed%2 else 1.15; d=1 if seed%2 else -1
    return [(side,r.uniform(.15,.45),d*.35,.1,.55),(side,r.uniform(.55,.85),d*.25,-.1,.45)]
events=[(t,'burn',blobs(5,i)) for i,t in enumerate(BURN)]+[(t,'leak',leakblobs(100+i)) for i,t in enumerate(LEAK)]
# colour ramp for film burn: dark red -> orange -> yellow -> white
def ramp(v):
    v=np.clip(v,0,1.4)
    r=np.clip(v*2.2,0,1); g=np.clip((v-.25)*1.6,0,1); b=np.clip((v-.75)*2.0,0,1)
    return np.stack([r,g,b],-1)
out=sys.stdout.buffer
blank=np.zeros((h,w,3),np.uint8).tobytes()
for n in range(int(DUR*FPS)):
    t=n/FPS; acc=np.zeros((h,w,3),np.float32); any_=False
    for (tc,kind,bl) in events:
        dur=0.8 if kind=='burn' else 1.1
        u=(t-(tc-dur*0.45))/dur
        if not 0<=u<=1: continue
        any_=True
        envl=np.sin(np.pi*u)**(1.2 if kind=='burn' else 2)
        field=np.zeros((h,w),np.float32)
        for (x0,y0,vx,vy,rad) in bl:
            cx=(x0+vx*u)*w; cy=(y0+vy*u)*h; R=rad*w*(0.8+0.6*u)
            field+=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*R*R))
        if kind=='burn':
            flick=0.85+0.3*np.sin(n*2.3)
            acc+=ramp(field*1.05*envl*flick)
        else:
            col=np.array([1.0,.55,.25],np.float32) if bl[0][2]>0 else np.array([1.0,.35,.55],np.float32)
            acc+=(np.clip(field,0,1)*envl*.85)[...,None]*col
    out.write((np.clip(acc,0,1)*255).astype(np.uint8).tobytes() if any_ else blank)
