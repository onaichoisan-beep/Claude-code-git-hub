import cv2,numpy as np,glob,sys,os
ref,x0,y0,x1,y1,mode,cand=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6],sys.argv[7]
im=cv2.imread(f'ref/n/{ref}.png')[y0:y1+1,x0:x1+1].astype(np.float32)
if mode=='dark': g=255-im.mean(2)
elif mode=='red': g=np.clip(im[...,2]-im[...,1],0,255)
elif mode=='yellow': g=np.clip((im[...,2]+im[...,1])/2-im[...,0],0,255)
else: g=im.min(2)
g=(g-g.min())/(g.max()-g.min()+1e-6)
ys,xs=np.where(g>0.5);g=g[ys.min():ys.max()+1,xs.min():xs.max()+1];H,W=g.shape
up=cv2.resize(g,(W*4,H*4),interpolation=cv2.INTER_CUBIC)
res=[]
for f in glob.glob(cand+'/*.png'):
    c=cv2.imread(f,0).astype(np.float32)/255;ys,xs=np.where(c>0.5)
    if len(xs)==0: continue
    c=c[ys.min():ys.max()+1,xs.min():xs.max()+1]
    ar=(c.shape[1]/c.shape[0])/(W/H)
    cr=cv2.resize(c,(W,H),interpolation=cv2.INTER_AREA);cr=cv2.resize(cr,(W*4,H*4),interpolation=cv2.INTER_CUBIC)
    a=up-up.mean();b=cr-cr.mean();ncc=(a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum())
    res.append((ncc-abs(np.log(ar))*0.5,ncc,ar,os.path.basename(f)))
for r in sorted(res,reverse=True)[:6]: print('score %.3f ncc %.3f aspect %.2f %s'%r)
