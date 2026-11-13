import cv2,glob,json,numpy as np
det=cv2.FaceDetectorYN.create('_tools/yunet.onnx','',(720,1280),0.6)
fs=sorted(glob.glob('aroll/f/a_*.jpg')); F=[]
for f in fs:
    im=cv2.imread(f); _,d=det.detect(im)
    d=None if d is None else [r for r in d[:,:4] if r[3]<1.5*r[2]]
    if d: x,y,w,h=max(d,key=lambda r:r[2]*r[3]); F.append([y,y+h*1.05,x,x+w])
    else: F.append(None)
# fill gaps
last=None
for i in range(len(F)):
    if F[i] is None: F[i]=last
    else: last=F[i]
nxt=None
for i in range(len(F)-1,-1,-1):
    if F[i] is None: F[i]=nxt
    else: nxt=F[i]
from scipy.ndimage import median_filter
A=median_filter(np.array(F,float),size=(11,1),mode="nearest")*1.5
out=[]
for i in range(len(A)):
    w=A[max(0,i-3):i+4]; out.append([int(w[:,0].min()),int(w[:,1].max()),int(w[:,2].min()),int(w[:,3].max())])
open('web/faces.js','w').write('window.FACES='+json.dumps(out)+';')
print(len(out),out[0],out[200],out[500],out[750],out[850])
# QC
idx=list(range(0,len(fs),45)); ims=[]
for i in idx:
    im=cv2.imread(fs[i]); t,c,x0,x1=[v/1.5 for v in out[i]]
    cv2.rectangle(im,(int(x0),int(t)),(int(x1),int(c)),(0,255,0),2); cv2.line(im,(0,int(c)),(720,int(c)),(0,0,255),3)
    ims.append(cv2.resize(im,(180,320)))
rows=[np.hstack(ims[k:k+10]+[np.zeros((320,180,3),np.uint8)]*(10-len(ims[k:k+10]))) for k in range(0,len(ims),10)]
cv2.imwrite('an/faces_qc.jpg',np.vstack(rows))
