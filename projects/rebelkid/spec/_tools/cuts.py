import cv2,numpy as np,glob,json
fs=sorted(glob.glob('ref/f/*.jpg'))
prev=None;rows=[]
for i,p in enumerate(fs):
    g=cv2.imread(p);s=cv2.resize(g,(135,240)).astype(np.float32)
    if prev is not None:
        d=np.abs(s-prev).mean()
        h1=cv2.calcHist([g],[0,1,2],None,[8,8,8],[0,256]*3);h2=cv2.calcHist([pg],[0,1,2],None,[8,8,8],[0,256]*3)
        hc=cv2.compareHist(h1,h2,cv2.HISTCMP_CORREL)
        dt=np.abs(s[:120]-prev[:120]).mean();db=np.abs(s[120:]-prev[120:]).mean()
        rows.append((i+1,round(float(d),2),round(float(hc),3),round(float(dt),2),round(float(db),2)))
    prev=s;pg=g
json.dump(rows,open('an/diff.json','w'))
ds=np.array([r[1] for r in rows])
med=np.median(ds)
cand=[r for r in rows if r[1]>max(12,4*med) or r[2]<0.85]
print('median',med,len(cand))
for r in cand:print(r, '%.2fs'%((r[0]-1)/30))
