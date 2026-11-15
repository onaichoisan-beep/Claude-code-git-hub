import cv2,numpy as np,sys
a,b,step,cols,out=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
W=int(sys.argv[6]) if len(sys.argv)>6 else 135
H=W*16//9;tiles=[]
for i in range(a,b+1,step):
    im=cv2.imread('ref/f/%05d.jpg'%i)
    if im is None: break
    im=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
    cv2.rectangle(im,(0,0),(62,16),(0,0,0),-1);cv2.putText(im,'%d %.1f'%(i,(i-1)/30),(1,12),0,0.35,(0,255,255),1)
    tiles.append(im)
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
