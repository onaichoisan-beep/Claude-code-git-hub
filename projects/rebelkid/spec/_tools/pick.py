import cv2,numpy as np,sys
ids=[int(x) for x in sys.argv[2].split(',')];W=int(sys.argv[3]);cols=int(sys.argv[4]);H=W*16//9;t=[]
for i in ids:
    im=cv2.resize(cv2.imread('ref/f/%05d.jpg'%i),(W,H),interpolation=cv2.INTER_AREA)
    cv2.rectangle(im,(0,0),(70,18),(0,0,0),-1);cv2.putText(im,str(i),(2,14),0,0.5,(0,255,255),1);t.append(im)
while len(t)%cols:t.append(np.zeros_like(t[0]))
cv2.imwrite(sys.argv[1],np.vstack([np.hstack(t[i:i+cols]) for i in range(0,len(t),cols)]),[cv2.IMWRITE_JPEG_QUALITY,88])
