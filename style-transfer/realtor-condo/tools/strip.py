import cv2,sys,numpy as np
d,out=sys.argv[1],sys.argv[2]; fr=[int(x) for x in sys.argv[3].split(',')]
W=int(sys.argv[4]) if len(sys.argv)>4 else 240; H=W*16//9
ims=[]
for i in fr:
    im=cv2.resize(cv2.imread(f'{d}/{i:05d}.jpg'),(W,H)); cv2.putText(im,str(i),(4,20),0,0.6,(0,255,255),2); ims.append(im)
cols=min(8,len(ims)); rows=(len(ims)+cols-1)//cols
S=np.zeros((rows*H,cols*W,3),np.uint8)
for k,im in enumerate(ims): S[(k//cols)*H:(k//cols+1)*H,(k%cols)*W:(k%cols+1)*W]=im
cv2.imwrite(out,S)
