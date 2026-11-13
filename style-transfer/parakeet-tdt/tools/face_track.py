import cv2,glob,json,numpy as np
cc=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
fs=sorted(glob.glob('aroll/f/*.jpg')); out=[]; last=None
for i,f in enumerate(fs):
    g=cv2.imread(f,0); s=cv2.resize(g,(540,960)); d=cc.detectMultiScale(s,1.1,5,minSize=(80,80))
    if len(d): x,y,w,h=max(d,key=lambda r:r[2]*r[3])*2; last=[int(y),int(y+h+0.05*h),int(x),int(x+w)]
    out.append(last)
for i in range(len(out)):
    if out[i] is None: out[i]=next(o for o in out if o)
chin=[max(o[1] for o in out[max(0,i-3):i+4]) for i in range(len(out))]
print('top min/max',min(o[0] for o in out),max(o[0] for o in out),'chin min/max',min(chin),max(chin),'x',min(o[2] for o in out),max(o[3] for o in out))
json.dump({'faces':out,'chin':chin},open('aroll/faces.json','w'))
im=cv2.imread(fs[400]); cv2.line(im,(0,max(chin)),(1080,max(chin)),(0,0,255),4); o=out[400]; cv2.rectangle(im,(o[2],o[0]),(o[3],o[1]),(0,255,0),3); cv2.imwrite('an/faces_qc.jpg',cv2.resize(im,(540,960)))
