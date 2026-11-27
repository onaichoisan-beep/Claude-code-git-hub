import numpy as np, soundfile as sf
SR=44100; T=72.0; out=np.zeros(int((T+0.5)*SR),np.float32); rng=np.random.default_rng(3)
def env(n,a=0.01,r=None):
    t=np.arange(n)/SR; e=np.minimum(1,t/a); 
    return e*np.exp(-t/(r or 0.1))
def whoosh(d=0.42):
    n=int(d*SR); x=rng.standard_normal(n).astype(np.float32)
    # moving bandpass via simple one-pole sweeps
    y=np.zeros(n,np.float32); lp=0; hp=0
    for i in range(n):
        f=300+3000*np.sin(np.pi*i/n); a=min(.99,2*np.pi*f/SR)
        lp+=a*(x[i]-lp); y[i]=lp
    w=np.sin(np.pi*np.arange(n)/n)**2
    return y*w*0.9
def pop():
    n=int(0.12*SR); t=np.arange(n)/SR; f=900*np.exp(-t*18)+500
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.002,0.03)).astype(np.float32)*0.5
def ding():
    n=int(1.2*SR); t=np.arange(n)/SR
    y=sum(np.sin(2*np.pi*f*t)*g for f,g in [(1568,1),(2349,.5),(3136,.3),(4186,.15)])
    return (y*env(n,0.003,0.35)).astype(np.float32)*0.28
def boom():
    n=int(0.6*SR); t=np.arange(n)/SR; f=110*np.exp(-t*6)+40
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.004,0.18)).astype(np.float32)*0.7
def place(x,t,g=1.0):
    i=int(t*SR); out[i:i+len(x)]+=x[:len(out)-i]*g
W=whoosh(); 
for c in [8.58,30.2,47.1,65.6]: place(W,c-0.28,0.2)
for p in [15.18,16.38,17.66,18.52,26.78,27.6,28.86,34.74,36.0,37.76,39.56,40.95,42.02,42.7,43.4,44.16,57.66,59.72,61.2,63.74,66.86,67.64,68.5]: place(pop(),p,0.22)
for d in [8.96,69.3]: place(boom(),d,0.35); place(ding(),d+0.02,0.35)
sf.write("assets/audio/sfx.wav",out,SR); print(np.abs(out).max())
