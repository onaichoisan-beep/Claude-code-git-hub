import soundfile as sf,numpy as np
from scipy.signal import stft
a,sr=sf.read('audio/stems/htdemucs/ref/no_vocals.wav'); a=a.mean(1) if a.ndim>1 else a
hop=int(sr/100); f,t,Z=stft(a,sr,nperseg=2048,noverlap=2048-hop); M=np.abs(Z)
flux=np.maximum(0,np.diff(np.log1p(M*50),axis=1)).sum(0)
rms=np.sqrt(np.convolve(a**2,np.ones(hop)/hop,'same'))[::hop]
med=np.convolve(flux,np.ones(51)/51,'same')
pk=[i for i in range(2,len(flux)-2) if flux[i]==flux[i-2:i+3].max() and flux[i]>2.2*med[i] and flux[i]>np.percentile(flux,80)]
cent=lambda i:(f[:,None]*M[:,i:i+15]).sum(0).mean()/(M[:,i:i+15].sum(0).mean()+1e-9)
for i in pk:
    ts=t[i+1]; seg=rms[i:i+60]; dur=(np.argmax(seg<seg.max()*0.25) if (seg<seg.max()*0.25).any() else 60)*10
    print(f't={ts:6.2f}s f={int(ts*30)+1:4d} flux={flux[i]/med[i]:4.1f} peak_dBFS={20*np.log10(rms[i:i+20].max()+1e-9):6.1f} centroid={cent(i):6.0f}Hz decay~{dur}ms')
