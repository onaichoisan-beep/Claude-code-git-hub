import cv2,numpy as np,sys
a,b,x0,y0,x1,y1,out=int(sys.argv[1]),int(sys.argv[2]),*map(int,sys.argv[3:7]),sys.argv[7]
cols=int(sys.argv[8]) if len(sys.argv)>8 else 4
t=[]
for i in range(a,b+1):
    im=cv2.imread(f'ref/f/{i:05d}.png')[y0:y1,x0:x1].copy(); cv2.putText(im,str(i),(5,30),0,1,(0,255,255),2); t.append(im)
while len(t)%cols: t.append(np.zeros_like(t[0]))
cv2.imwrite(out,np.vstack([np.hstack(t[r*cols:(r+1)*cols]) for r in range(len(t)//cols)]),[cv2.IMWRITE_JPEG_QUALITY,80])
