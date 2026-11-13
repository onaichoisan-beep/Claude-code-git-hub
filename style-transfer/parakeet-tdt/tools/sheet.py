import cv2, sys, glob, numpy as np
d, step, out, cols = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]) if len(sys.argv)>4 else 10
a = int(sys.argv[5]) if len(sys.argv)>5 else 1; b = int(sys.argv[6]) if len(sys.argv)>6 else 99999
fs = sorted(glob.glob(d+'/*'))
tiles=[]
for i in range(a-1, min(b,len(fs)), step):
    im = cv2.imread(fs[i]); im = cv2.resize(im,(216,384))
    cv2.rectangle(im,(0,0),(70,24),(0,0,0),-1); cv2.putText(im,str(i+1),(3,18),0,0.6,(0,255,255),2)
    tiles.append(im)
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[r*cols:(r+1)*cols]) for r in range(len(tiles)//cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
