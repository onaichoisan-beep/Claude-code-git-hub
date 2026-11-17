import numpy as np, wave, sys
SR=44100; DUR=78.0; BPM=104; beat=60/BPM; s16=beat/4
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig)); 
    if i>=N: return
    s=sig[:j-i]*g; L[i:j]+=s*(1-pan)*0.5*2**0.5; R[i:j]+=s*(1+pan)*0.5*2**0.5
def env(n,a,d):
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))*np.exp(-t/d); return e
def dhol_low(): n=int(.5*SR); t=np.arange(n)/SR; f=55+60*np.exp(-t*25); ph=2*np.pi*np.cumsum(f)/SR; return (np.sin(ph)+0.3*np.sin(2*ph))*env(n,.002,.16)+0.15*rng.standard_normal(n)*env(n,.001,.01)
def dhol_hi(): n=int(.25*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); x=np.convolve(x,np.ones(6)/6,'same'); return (0.5*np.sin(2*np.pi*330*t)+x*0.6)*env(n,.001,.04)
def tabla_na(f=520): n=int(.4*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.01*t)+.25*np.sin(2*np.pi*f*3.03*t))*env(n,.001,.12)
def shaker(): n=int(.08*SR); x=rng.standard_normal(n); x=np.diff(x,prepend=0); return x*env(n,.004,.02)
def ks(freq,dur=1.6,bright=0.5):
    n=int(dur*SR); p=int(SR/freq); buf=rng.uniform(-1,1,p); out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%p]; buf[i%p]=0.996*(bright*buf[i%p]+(1-bright)*buf[(i+1)%p]) if True else 0
    return out*env(n,.002,dur*0.5)
def shehnai(freq,dur):
    n=int(dur*SR); t=np.arange(n)/SR; vib=1+0.006*np.sin(2*np.pi*5.5*t)*np.minimum(1,t/0.25)
    ph=2*np.pi*np.cumsum(freq*vib)/SR; x=sum((1/k**0.9)*np.sin(k*ph) for k in range(1,9))
    e=np.minimum(1,t/0.04)*np.minimum(1,(dur-t)/0.08).clip(0); return np.tanh(1.4*x)*e*0.5
# notes: C major / Bilawal, Sa=C4
Sa=261.63; sw={'S':0,'R':2,'G':4,'m':5,'P':7,'D':9,'N':11}
def hz(n,o=0): return Sa*2**((sw[n]+12*o)/12)
# drone (tanpura-like) whole track
t=np.arange(N)/SR
dr=np.zeros(N)
for f,a in [(Sa/2,1),(hz('P',-1),.7),(Sa,.6),(Sa/4,.5)]:
    dr+=a*sum((1/k)*np.sin(2*np.pi*f*k*t+0.3*np.sin(2*np.pi*0.13*k*t)) for k in range(1,7))
dr*=0.05*(0.8+0.2*np.sin(2*np.pi*t/beat/4))
fade=np.minimum(1,t/2.0); L+=dr*fade; R+=dr*fade
bars=int(DUR/(beat*4))+1
# groove pattern 16 steps (kaharwa-ish / bhangra-lite)
low=[0,6,10]; hi=[4,12,14]; na=[2,3,7,8,11,15]
for b in range(bars):
    bt=b*4*beat
    intro = bt<3.0
    for s in range(16):
        tt=bt+s*s16
        if tt>DUR-0.5: break
        sw_=0.012 if s%2 else 0
        if not intro:
            if s in low: add(dhol_low(),tt+sw_,0,0.55)
            if s in hi: add(dhol_hi(),tt+sw_,0.1,0.35)
            if s in na: add(tabla_na(520 if s%4 else 700),tt+sw_,-0.3,0.12)
        add(shaker(),tt+sw_,0.4,0.10 if s%2 else 0.16)
# sitar-ish pluck riff (2-bar phrase)
riff=[('S',1),('G',1),('P',1),('N',2),('D',1),('P',1),('G',1),('R',1),('S',1),('G',1),('P',1),('D',1),('P',2),('G',1)]
# melody arcs; winter section (36-54) slightly different register
pos=0.0
while pos<DUR-2:
    for n,l in riff:
        if pos>DUR-2: break
        o=1 if (36<pos<54) else 0
        add(ks(hz(n,o),1.2,0.55),pos,0.25,0.22)
        pos+=l*s16*2
# shehnai phrases at intervals (sparse, under VO)
phr=[('S',.5),('R',.5),('G',1),('P',1.5),('G',.5),('R',.5),('S',2)]
for st in [1.0,20.0,40.0,59.0,72.0]:
    p=st
    for n,l in phr:
        add(shehnai(hz(n,1),l*beat),p,-0.2,0.10); p+=l*beat
# final hit
add(dhol_low()*1.5,DUR-1.4,0,0.8); add(ks(hz('S',1),2.0,0.6),DUR-1.4,0,0.3)
m=np.stack([L,R],1)
out=t[:,None]
m*=np.minimum(1,(DUR-t)/1.0).clip(0)[:,None]
m/=np.abs(m).max()*1.12
with wave.open(sys.argv[1],'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m*32767).astype('<i2').tobytes())
