import cv2,sys,numpy as np
d,out=sys.argv[1],sys.argv[2]; fr=[int(x) for x in sys.argv[3].split(',')]
y0,y1=[int(v) for v in sys.argv[4].split(':')]; cols=int(sys.argv[5]) if len(sys.argv)>5 else 2
ims=[]
for i in fr:
    im=cv2.imread(f'{d}/{i:05d}.jpg')[y0:y1]; im=im.copy(); cv2.putText(im,str(i),(4,24),0,0.8,(0,255,255),2); ims.append(im)
h,w=ims[0].shape[:2]; rows=(len(ims)+cols-1)//cols
S=np.zeros((rows*h,cols*w,3),np.uint8)
for k,im in enumerate(ims): S[(k//cols)*h:(k//cols+1)*h,(k%cols)*w:(k%cols+1)*w]=im
cv2.imwrite(out,S)
