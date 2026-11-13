import cv2,glob,numpy as np
im=cv2.imread('ref/f/00565.jpg')[640:712,140:580]; hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
ink=((hsv[...,2]>185)&(hsv[...,1]<70)).astype(np.uint8)*255
ys,xs=np.nonzero(ink); ref=ink[ys.min():ys.max()+1,xs.min():xs.max()+1]; cv2.imwrite('an/font/_ref.png',ref)
def norm(a,h=80):
    ys,xs=np.nonzero(a>128); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    return cv2.resize(a,(int(a.shape[1]*h/a.shape[0]),h),interpolation=cv2.INTER_AREA).astype(np.float32)
R=norm(ref);res=[]
for f in glob.glob('an/font/*_*.png'):
    if '_ref' in f: continue
    g=cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY); C=norm(g)
    ar=C.shape[1]/R.shape[1]; C2=cv2.resize(C,(R.shape[1],R.shape[0]))
    a=(R-R.mean());b=(C2-C2.mean()); ncc=(a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum())
    res.append((round(float(ncc),3),round(ar,3),f.split('/')[-1]))
for r in sorted(res,reverse=True): print(r)
