import cv2,numpy as np,json
casc=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture('aroll/clean.mp4');res=[];i=0;K=1080/720
while True:
    ok,f=cap.read()
    if not ok:break
    if i%3==0:
        g=cv2.equalizeHist(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY))
        fs=casc.detectMultiScale(g,1.1,6,minSize=(120,120))
        if len(fs): x,y,w,h=max(fs,key=lambda r:r[2]*r[3]);res.append((i,[y*K,(y+h*1.05)*K,x*K,(x+w)*K]))
        else: res.append((i,None))
    i+=1
n=i;idx=[r[0] for r in res if r[1]];val=np.array([r[1] for r in res if r[1]])
F=np.array([[np.interp(j,idx,val[:,c]) for c in range(4)] for j in range(n)])
# chin = max over +-3 frames
ch=np.array([F[max(0,j-3):j+4,1].max() for j in range(n)]);F[:,1]=ch
json.dump([[round(v) for v in r] for r in F],open('web/faces.json','w'))
print('frames',n,'detected',len(idx),'/',len(res));print('chin y range',F[:,1].min(),np.median(F[:,1]),F[:,1].max());print('top',np.median(F[:,0]),'x',np.median(F[:,2]),np.median(F[:,3]))
