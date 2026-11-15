# bbox of white ink inside region per frame (540x960 coords in, 1080 coords out)
import cv2,numpy as np,sys
a,b=int(sys.argv[1]),int(sys.argv[2]);x0,y0,x1,y1=map(int,sys.argv[3].split(','));mode=sys.argv[4] if len(sys.argv)>4 else 'white'
for i in range(a,b+1):
    im=cv2.imread('ref/f/%05d.jpg'%i)[y0:y1,x0:x1].astype(int)
    if mode=='white': m=im.min(2)>215
    elif mode=='dark': m=im.sum(2)<330
    elif mode=='yellow': m=(im[...,2]>170)&(im[...,1]>170)&(im[...,0]<130)
    ys,xs=np.where(m)
    if len(xs)<15: print(i,'-');continue
    print(i,'n=%d bbox x %d-%d y %d-%d  w %d h %d mean_px %d'%(len(xs),2*(xs.min()+x0),2*(xs.max()+x0),2*(ys.min()+y0),2*(ys.max()+y0),2*(xs.max()-xs.min()),2*(ys.max()-ys.min()),int(im[m].mean())))
