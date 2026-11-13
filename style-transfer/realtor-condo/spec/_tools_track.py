# colour-mask bbox tracker. coords reported in 1080x1920 space (x1.5)
import cv2,numpy as np,sys,json
name,f0,f1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
hlo,hhi,smin,vmin=[int(v) for v in sys.argv[4].split(',')]
y0,y1=[int(v) for v in sys.argv[5].split(':')]
out=[]
for i in range(f0,f1+1):
    im=cv2.imread(f'ref/f/{i:05d}.jpg'); hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    m=((hsv[...,0]>=hlo)&(hsv[...,0]<=hhi)&(hsv[...,1]>=smin)&(hsv[...,2]>=vmin)).astype(np.uint8)
    m[:y0]=0;m[y1:]=0
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    ys,xs=np.nonzero(m); n=len(xs)
    if n<80: out.append((i,n)); continue
    x0,x1=np.percentile(xs,[1,99]); yy0,yy1=np.percentile(ys,[1,99])
    col=cv2.mean(im,mask=m)[:3]
    out.append((i,n,int(x0*1.5),int(yy0*1.5),int(x1*1.5),int(yy1*1.5),'#%02x%02x%02x'%(int(col[2]),int(col[1]),int(col[0]))))
for o in out: print(name,*o)
