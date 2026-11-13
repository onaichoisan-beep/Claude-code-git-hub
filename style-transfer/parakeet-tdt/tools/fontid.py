import cv2, numpy as np, glob, os
from PIL import Image, ImageDraw, ImageFont
im=cv2.imread('ref/f/00168.png'); hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
def bbox(m):
    ys,xs=np.where(m); return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def refmask(x0,y0,x1,y1,kind):
    r=im[y0:y1,x0:x1].astype(int); h=hsv[y0:y1,x0:x1]
    if kind=='white': m=(h[...,2]>215)&(h[...,1]<45)
    else: m=(r[...,2]>170)&(r[...,1]<110)&(r[...,0]<150)
    a,b,c,d=bbox(m); return m[b:d,a:c].astype(np.float32),(x0+a,y0+b,x0+c,y0+d)
def rend(fp,text,italic_skew=0):
    f=ImageFont.truetype(fp,200); img=Image.new('L',(3000,400)); ImageDraw.Draw(img).text((20,50),text,font=f,fill=255)
    a=np.array(img)>128
    if italic_skew:
        M=np.float32([[1,-italic_skew,italic_skew*200],[0,1,0]]); a=cv2.warpAffine(a.astype(np.uint8),M,(3000,400))>0
    x0,y0,x1,y1=bbox(a); return a[y0:y1,x0:x1].astype(np.float32)
def ncc(a,b):
    b=cv2.resize(b,(a.shape[1],a.shape[0]),interpolation=cv2.INTER_AREA)
    a=a-a.mean(); b=b-b.mean(); return (a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()+1e-9)
for kind,box,text in [('white',(290,385,800,445),"aren't ready for"),('pink',(260,440,930,535),"NEW CLIENTS")]:
    m,bb=refmask(*box,kind); print(kind,text,'ink bbox',bb,'h',bb[3]-bb[1],'w',bb[2]-bb[0])
    res=[]
    for fp in glob.glob('/home/user/work/fonts/*.ttf'):
        try:
            for sk in ([0] if kind=='white' else [0,0.2]):
                res.append((ncc(m,rend(fp,text,sk)),os.path.basename(fp)[:40],sk))
        except Exception as e: pass
    for r in sorted(res,reverse=True)[:8]: print('  %.3f %s skew=%s'%r)
