# Removes the A-roll's burned-in captions (white text + drop shadow, band y 140-215 of 720x1280)
# using a per-shot temporal plate of the static background.
import cv2,numpy as np,json,subprocess
Y0,Y1=128,226
cap=cv2.VideoCapture('src/aroll.mp4');frames=[]
while True:
    ok,f=cap.read()
    if not ok:break
    frames.append(f)
n=len(frames);print('frames',n)
small=[cv2.resize(f,(72,128)).astype(np.float32) for f in frames]
cuts=[0]+[i for i in range(1,n) if np.abs(small[i]-small[i-1]).mean()>18]+[n]
print('shots',len(cuts)-1,[round(c/30,2) for c in cuts])
k=np.ones((5,5),np.uint8)
def mask(b):
    w=((b.min(2)>205)).astype(np.uint8);w[:150-Y0]=0;w[203-Y0:]=0
    w=cv2.dilate(w,k);o=w.copy()
    for d in range(2,9,2):
        sh=np.zeros_like(w);sh[d:,d:]=w[:-d,:-d];o|=sh
    return cv2.dilate(o,np.ones((7,7),np.uint8))>0
bands=np.array([f[Y0:Y1] for f in frames]);M=np.array([mask(b) for b in bands])
skip=set(range(int(55.25*30),int(58.85*30)))  # original editor's comment-screenshot graphics: leave untouched
gsub=np.array([i for i in range(0,n,7) if not (55.2*30<=i<=64.2*30)])
st=bands[gsub].astype(np.float32);st[M[gsub]]=np.nan
GP=np.nanmedian(st,0);gh=np.isnan(GP).any(2);GP=np.nan_to_num(GP).astype(np.uint8)
print('global holes',gh.sum())
if gh.any(): GP=cv2.inpaint(GP,gh.astype(np.uint8)*255,5,cv2.INPAINT_TELEA)
del st
for a,b in zip(cuts[:-1],cuts[1:]):
    idx=np.arange(a,b);sub=idx[::max(1,len(idx)//60)]
    st=bands[sub].astype(np.float32);st[M[sub]]=np.nan
    plate=np.nanmedian(st,0);hole=np.isnan(plate).any(2)
    plate=np.nan_to_num(plate).astype(np.uint8)
    um=~M[sub].any(0)
    err=np.abs(bands[sub].astype(np.float32).mean(0)-GP.astype(np.float32)).mean(2)[um].mean() if um.any() else 99
    print('shot %.2f err %.1f holes %d'%(a/30,err,hole.sum()))
    if err<9: plate=np.where(hole[...,None],GP,plate)
    elif hole.any(): plate=cv2.inpaint(plate,hole.astype(np.uint8)*255,7,cv2.INPAINT_TELEA)
    for i in idx:
        if i in skip: continue
        m=cv2.GaussianBlur(M[i].astype(np.float32),(9,9),0)[...,None]
        ring=(cv2.dilate(M[i].astype(np.uint8),np.ones((15,15),np.uint8))>0)&~M[i]
        g=(bands[i][ring].astype(np.float32).mean(0)+1)/(plate[ring].astype(np.float32).mean(0)+1) if ring.any() else 1
        pl=np.clip(plate*g,0,255)
        frames[i][Y0:Y1]=(bands[i]*(1-m)+pl*m).astype(np.uint8)
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','720x1280','-r','30','-i','-','-i','src/aroll.mp4','-map','0:v','-map','1:a','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','aroll/clean.mp4'],stdin=subprocess.PIPE)
for f in frames:p.stdin.write(f.tobytes())
p.stdin.close();p.wait()
json.dump(cuts,open('aroll/shots.json','w'))
