import soundfile as sf,numpy as np,json
from scipy.signal import stft
a,sr=sf.read('audio/sep/htdemucs/ref/no_vocals.wav');a=a.mean(1)
v,_=sf.read('audio/sep/htdemucs/ref/vocals.wav');v=v.mean(1)
hop=256;f,t,Z=stft(a,sr,nperseg=1024,noverlap=1024-hop);S=np.abs(Z)
e=20*np.log10(np.sqrt((S**2).sum(0))+1e-9)
# rolling 30 frames RMS envelope (dB) of the non-vocal stem
fr=int(sr/hop/30)  # stft frames per video frame
E=np.array([e[i:i+fr].max() for i in range(0,len(e)-fr,fr)])
V=np.array([20*np.log10(np.sqrt((v[int(i*fr*hop):int((i+1)*fr*hop)]**2).mean())+1e-9) for i in range(len(E))])
floor=np.percentile(E,30)
ev=[];i=0
while i<len(E):
    if E[i]>floor+14 and E[i]-E[max(0,i-3)]>6:
        j=i
        while j<len(E)-1 and E[j]>floor+8: j+=1
        seg=S[:,i*fr:(j+1)*fr];spec=seg.sum(1);cen=(f*spec).sum()/spec.sum()
        lowr=spec[f<300].sum()/spec.sum();hir=spec[f>4000].sum()/spec.sum()
        T=i*fr*hop/sr;ev.append(dict(frame=int(T*30)+1,t=round(T,2),dur_f=round((j-i+1)*fr*hop/sr*30),peak_db=round(float(E[i:j+1].max()),1),rel_voice_db=round(float(E[i:j+1].max()-np.median(V[V>-60])),1),centroid=int(cen),low=round(float(lowr),2),hi=round(float(hir),2)))
        i=j+1
    else: i+=1
json.dump(ev,open('audio/ref_sfx.json','w'),indent=0)
print('floor %.1f dB, events %d'%(floor,len(ev)))
for x in ev: print(x)
