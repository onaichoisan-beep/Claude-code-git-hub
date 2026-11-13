import cv2,numpy as np,json,os,sys
a,b=int(sys.argv[1]),int(sys.argv[2]); os.makedirs('vid',exist_ok=True)
cam=json.load(open('render/cam.json'))
def rgba(p):
    im=cv2.imread(p,cv2.IMREAD_UNCHANGED)
    if im is None: return None
    if im.ndim==2: im=cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)
    a=im[...,3:4].astype(np.float32)/255. if im.shape[2]==4 else np.ones(im.shape[:2]+(1,),np.float32)
    return (im[...,:3].astype(np.float32),a)
for f in range(a,b):
    o=f'vid/f_{f:04d}.jpg'
    if os.path.exists(o): continue
    sc,px,py=cam[f]
    M=np.float32([[sc,0,px*(1-sc)],[0,sc,py*(1-sc)]])
    fr=cv2.resize(cv2.imread(f'aroll/f/a_{f+1:04d}.jpg'),(1080,1920),interpolation=cv2.INTER_LANCZOS4)
    fr=cv2.warpAffine(fr,M,(1080,1920),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    m=cv2.imread(f'aroll/m/a_{f+1:04d}.png',0); m=cv2.resize(m,(1080,1920),interpolation=cv2.INTER_CUBIC)
    m=cv2.warpAffine(m,M,(1080,1920),flags=cv2.INTER_LINEAR).astype(np.float32)[...,None]/255.
    out=fr.copy()
    B=rgba(f'render/back_{f:04d}.png')
    if B: out=B[0]*B[1]+out*(1-B[1])
    out=fr*m+out*(1-m)                     # subject in front of the back layer
    F=rgba(f'render/front_{f:04d}.png')
    if F: out=F[0]*F[1]+out*(1-F[1])
    L=rgba(f'render/leak_{f:04d}.png')
    if L: l=L[0]*L[1]/255.; out=255*(1-(1-out/255.)*(1-l))   # screen blend
    cv2.imwrite(o,np.clip(out,0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,95])
print('done',a,b)
