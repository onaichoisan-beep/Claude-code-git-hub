import cv2,glob,numpy as np,json,sys
fs=sorted(glob.glob(sys.argv[1]+'/*.jpg'))
prev=None;R=[]
for i,f in enumerate(fs):
    im=cv2.resize(cv2.imread(f),(180,320)); g=im.astype(np.float32)
    h=cv2.calcHist([cv2.cvtColor(im,cv2.COLOR_BGR2HSV)],[0,1],None,[30,32],[0,180,0,256]); cv2.normalize(h,h)
    lum=float(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).mean())
    if prev is not None:
        d=np.abs(g-prev[0]).mean(); c=cv2.compareHist(h,prev[1],cv2.HISTCMP_CORREL)
        dt=np.abs(g[:160]-prev[0][:160]).mean(); db=np.abs(g[160:]-prev[0][160:]).mean()
        R.append((i+1,round(float(d),1),round(float(c),3),round(float(dt),1),round(float(db),1),round(lum,1)))
    prev=(g,h)
json.dump(R,open(sys.argv[2],'w'))
ds=np.array([r[1] for r in R])
for k,r in enumerate(R):
    loc=np.median(ds[max(0,k-5):k+6])
    if r[1]>max(12,3*loc) or r[2]<0.6: print('CUT?',r,'loc',round(loc,1))
