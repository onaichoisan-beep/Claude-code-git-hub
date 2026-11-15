import cv2,numpy as np,sys
ref,x0,y0,x1,y1,mode,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6],sys.argv[7];cands=sys.argv[8:]
im=cv2.imread(f'ref/n/{ref}.png')[y0-3:y1+4,x0-3:x1+4]
H=90;r=cv2.resize(im,(int(im.shape[1]*H/im.shape[0]),H),interpolation=cv2.INTER_CUBIC)
rows=[r]
for c in cands:
    g=cv2.imread(c);ys,xs=np.where(g.max(2)>128);g=g[ys.min():ys.max()+1,xs.min():xs.max()+1]
    g=cv2.resize(g,(int(g.shape[1]*(H-8)/g.shape[0]),H-8));g=cv2.copyMakeBorder(g,4,4,4,4,0)
    cv2.putText(g,c.split('/')[-1][:22],(2,12),0,0.4,(0,255,255),1);rows.append(g)
W=max(x.shape[1] for x in rows);cv2.imwrite(out,np.vstack([np.pad(x,((2,2),(0,W-x.shape[1]),(0,0))) for x in rows]))
