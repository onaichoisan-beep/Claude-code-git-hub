import numpy as np, soundfile as sf
SR=44100; T=83.4; out=np.zeros(int((T+0.5)*SR),np.float32); rng=np.random.default_rng(3)
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
for c in [7.6,24.75,35.0,56.0]: place(W,c-0.28,0.2)
for p in [12.48,16.86,36.2,36.84,37.4,39.1,40.32,42.14,42.92,43.58,44.16,44.96,47.34,48.58,51.62,52.84,54.06,65.55,69.77,72.04,73.6,74.68,76.43]: place(pop(),p,0.22)
for d in [7.75,20.92,79.07]: place(boom(),d,0.35); place(ding(),d+0.02,0.35)
sf.write("assets/audio/sfx.wav",out,SR); print(np.abs(out).max())
