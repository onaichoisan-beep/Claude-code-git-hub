# track an element: template from frame REF, region box (540x960 coords) -> per-frame dx,dy,scale,score
import cv2,numpy as np,sys
a,b,ref=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]);x0,y0,x1,y1=map(int,sys.argv[4].split(','))
g=lambda i:cv2.cvtColor(cv2.imread('ref/f/%05d.jpg'%i),cv2.COLOR_BGR2GRAY).astype(np.float32)
T=g(ref)[y0:y1,x0:x1];k=1080/540
for i in range(a,b+1):
    I=g(i);best=(-2,)
    for s in np.arange(0.80,1.21,0.02):
        t=cv2.resize(T,None,fx=s,fy=s)
        r=cv2.matchTemplate(I,t,cv2.TM_CCOEFF_NORMED);_,v,_,p=cv2.minMaxLoc(r)
        if v>best[0]: best=(v,s,p[0]+t.shape[1]/2,p[1]+t.shape[0]/2)
    v,s,cx,cy=best;print(i,'score %.2f scale %.2f cx %.1f cy %.1f'%(v,s,cx*k,cy*k))
