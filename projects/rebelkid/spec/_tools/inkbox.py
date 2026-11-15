import cv2,numpy as np,sys,json
# usage: inkbox.py frame x0 y0 x1 y1 mode(dark|white|yellow|red)
f,x0,y0,x1,y1,mode=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
im=cv2.imread(f'ref/n/{f}.png')[y0:y1,x0:x1].astype(int);B,G,R=im[...,0],im[...,1],im[...,2]
if mode=='dark': m=(R+G+B)<400
elif mode=='white': m=(B>200)&(G>200)&(R>200)
elif mode=='yellow': m=(R>180)&(G>180)&(B<120)
elif mode=='red': m=(R>120)&(G<90)&(B<90)
ys,xs=np.where(m)
bx=[int(xs.min()+x0),int(ys.min()+y0),int(xs.max()+x0),int(ys.max()+y0)]
col=np.median(im[m],0)[::-1]; core=im[m]; s=core.sum(1); 
pick=core[s<=np.percentile(s,30)] if mode in('dark','red') else core[s>=np.percentile(s,70)]
cc=np.median(pick,0)[::-1]
k=1080/346
print(json.dumps(dict(native=bx,px1080=[round(v*k) for v in bx],h1080=round((bx[3]-bx[1]+1)*k,1),w1080=round((bx[2]-bx[0]+1)*k,1),hex='#%02X%02X%02X'%tuple(int(v) for v in cc))))
cv2.imwrite(f'an/ink_{f}_{x0}_{y0}.png',(m*255).astype(np.uint8))
