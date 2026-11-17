# Builds a black "fx" track (screen-blended over the edit): white flashes + film burns.
import numpy as np, subprocess, sys
out=sys.argv[1]; FPS=30; DUR=77.0; w,h=270,480
FLASH=[10.00,14.40,36.00,68.60]          # section changes: reveal, wedding, winter, CTA
BURN=[2.00,19.10,31.30,46.80,54.40,62.80]
N=int(DUR*FPS); rng=np.random.default_rng(3)
yy,xx=np.mgrid[0:h,0:w]/np.array([h,w])[:,None,None].astype(float) if False else (np.mgrid[0:h,0:w][0]/h, np.mgrid[0:h,0:w][1]/w)
burns=[]
for c in BURN:
    side=rng.choice([-1,1]); blobs=[(rng.uniform(.0,.4) if side<0 else rng.uniform(.6,1), rng.uniform(.1,.9), rng.uniform(.25,.5), rng.uniform(-.6,.6), rng.uniform(-.3,.3)) for _ in range(4)]
    burns.append((c,side,blobs))
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(FPS),'-i','-',
                    '-c:v','libx264','-crf','12','-pix_fmt','yuv444p',out],stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS; img=np.zeros((h,w,3))
    for c in FLASH:
        d=t-c
        if -0.10<=d<=0.25:
            e=(d+0.10)/0.10 if d<0 else max(0,1-d/0.25)**1.6
            img+=e*0.95
    for c,side,blobs in burns:
        d=t-c+0.35
        if 0<=d<=0.8:
            u=d/0.8; env=np.sin(np.pi*u)**1.3
            m=np.zeros((h,w))
            for bx,by,r,vx,vy in blobs:
                cx=bx+vx*u*side*-1; cy=by+vy*u
                m+=np.exp(-(((xx-cx)/r)**2+((yy-cy)/(r*1.6))**2)*2.2)
            edge=np.clip((xx if side>0 else 1-xx)*1.4-0.2,0,1)**1.5
            m=np.clip(m*0.7+edge*0.6,0,1.6)*env*(0.9+0.2*rng.random())
            col=np.stack([np.clip(m*1.15,0,1),np.clip(m**1.6*0.75,0,1),np.clip(m**3*0.35,0,1)],-1)
            img=1-(1-img)*(1-col)
    p.stdin.write((np.clip(img,0,1)*255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
