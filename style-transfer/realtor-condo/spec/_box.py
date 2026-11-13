import cv2,numpy as np,sys
for a in sys.argv[1:]:
    n,f,y0,y1,x0,x1=a.split(','); f,y0,y1,x0,x1=int(f),int(y0),int(y1),int(x0),int(x1)
    im=cv2.imread(f'ref/f/{f:05d}.jpg'); r=im[y0:y1,x0:x1]; h=cv2.cvtColor(r,cv2.COLOR_BGR2HSV)
    m=((h[...,2]>200)&(h[...,1]<45)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    ys,xs=np.nonzero(m)
    if len(xs)<20: print(n,'none');continue
    rows=m.sum(1); band=np.nonzero(rows>rows.max()*0.5)[0]
    print(f'{n:14s} f{f} box x{int((x0+np.percentile(xs,1))*1.5)}-{int((x0+np.percentile(xs,99))*1.5)} y{int((y0+ys.min())*1.5)}-{int((y0+ys.max())*1.5)} core-band h={int((band.max()-band.min())*1.5)}px(x-height-ish)')
