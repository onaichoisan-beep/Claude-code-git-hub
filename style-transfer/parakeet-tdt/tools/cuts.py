import cv2, glob, numpy as np
fs=sorted(glob.glob('ref/f/*.png')); prev=None
for i,f in enumerate(fs):
    im=cv2.resize(cv2.imread(f),(270,480)).astype(np.float32)
    if prev is not None:
        d=np.abs(im-prev).mean(); dt=np.abs(im[:240]-prev[:240]).mean(); db=np.abs(im[240:]-prev[240:]).mean()
        h1=cv2.calcHist([im.astype(np.uint8)],[0,1,2],None,[8,8,8],[0,256]*3); h0=cv2.calcHist([prev.astype(np.uint8)],[0,1,2],None,[8,8,8],[0,256]*3)
        c=cv2.compareHist(h0,h1,cv2.HISTCMP_CORREL)
        if d>9 or c<0.9: print(f"{i+1:4d} t={i/30:6.2f} mad={d:5.1f} top={dt:5.1f} bot={db:5.1f} hc={c:.3f}")
    prev=im
