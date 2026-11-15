import cv2,numpy as np,sys
cap=cv2.VideoCapture('src/ref.mp4');fs=[]
for i in range(0,2400,60):
    cap.set(1,i);ok,f=cap.read()
    if ok: fs.append(f)
f=np.array(fs).astype(np.float32)
# panel = where frames vary over time
v=f.std(0).mean(2)
cols=(v>12).mean(0);rows=(v>12).mean(1)
print('cols>0.5',np.where(cols>0.3)[0][[0,-1]]);print('rows',np.where(rows>0.3)[0][[0,-1]])
for x in range(295,312):print(x,round(cols[x],2),end=' | ')
print()
for y in range(320,340):print(y,round(rows[y],2),end=' | ')
print()
for y in range(940,956):print(y,round(rows[y],2),end=' | ')
