import cv2,sys,glob,numpy as np
d,out,step,start,end=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
fs=sorted(glob.glob(d+'/*.jpg'))
idx=list(range(start,min(end,len(fs)),step))
W=180;H=320;cols=10
rows=(len(idx)+cols-1)//cols
S=np.zeros((rows*H,cols*W,3),np.uint8)
for k,i in enumerate(idx):
    im=cv2.resize(cv2.imread(fs[i]),(W,H))
    cv2.putText(im,str(i+1),(4,18),0,0.55,(0,255,255),2)
    S[(k//cols)*H:(k//cols+1)*H,(k%cols)*W:(k%cols+1)*W]=im
cv2.imwrite(out,S,[cv2.IMWRITE_JPEG_QUALITY,80])
