import numpy as np, wave
SR=44100; BPM=108; beat=60/BPM; bar=4*beat; DUR=75.5
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); 
    if i>=N: return
    s=sig[:N-i]*gain; L[i:i+len(s)]+=s*(1-max(0,pan)); R[i:i+len(s)]+=s*(1+min(0,pan))
def env(n,a,d):
    t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def kick():
    n=int(.45*SR); t=np.arange(n)/SR; f=48+120*np.exp(-t/.04); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t/.16)*1.0 + 0.3*rng.standard_normal(n)*np.exp(-t/.004)
def lp(x,a):  # one-pole
    y=np.empty_like(x); acc=0.
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def snare():
    n=int(.3*SR); t=np.arange(n)/SR; nz=rng.standard_normal(n)
    nz=nz-lp(nz,.15)
    return .55*nz*np.exp(-t/.07)+.4*np.sin(2*np.pi*190*t)*np.exp(-t/.05)
def hat(o=False):
    n=int((.25 if o else .06)*SR); t=np.arange(n)/SR; nz=rng.standard_normal(n); nz=nz-lp(nz,.5)
    return .18*nz*np.exp(-t/(.08 if o else .015))
def dhol():  # low tom-ish hand drum
    n=int(.35*SR); t=np.arange(n)/SR; f=110+60*np.exp(-t/.03)
    return .6*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.12)
def tabla():
    n=int(.25*SR); t=np.arange(n)/SR; f=520+80*np.exp(-t/.02)
    return .25*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.09)
def saw(f,n,det=0):
    t=np.arange(n)/SR; out=0
    for d in ([-det,0,det] if det else [0]):
        ph=(t*f*(1+d))%1; out=out+(2*ph-1)
    return out/(3 if det else 1)
def note(m): return 440*2**((m-69)/12)
K,S_,H,HO,D,T=kick(),snare(),hat(),hat(True),dhol(),tabla()
# progression Am F C G  (roots midi)
prog=[(45,[57,60,64]),(41,[57,60,65]),(48,[55,60,64]),(43,[55,59,62])]
bars=int(DUR/bar)+1
for b in range(bars):
    t0=b*bar; root,ch=prog[b%4]
    drop = 41.0<=t0<43.2   # breathe before the question
    full = t0>=1.0
    # pad
    n=int(bar*SR); pad=sum(saw(note(m),n,.004) for m in ch)/3
    pad=lp(pad,.06)*env(n,.25,6)*.16
    add(pad,t0,1,-.3); add(pad,t0,1,.3)
    if drop: 
        add(HO*2,t0+bar-beat,.5); continue
    for k in range(4):
        tb=t0+k*beat
        if k in (0,2) or (k==3 and b%2==1): add(K,tb, .9)
        if k==3 and b%2==1: add(K,tb+beat/2,.6)
        if k in (1,3): add(S_,tb,.55)
        for e in range(2):
            add(H if e==0 else HO*0.6,tb+e*beat/2,.8, .4)
        # hand drum groove (desi flavour)
        add(D,tb+beat*0.75,.45,-.2); add(T,tb+beat*0.25,.5,.25)
        if k==2: add(T,tb+beat*0.5,.4,.25)
    # bass 8ths
    for e in range(8):
        n=int(beat/2*SR*.9); bs=lp(saw(note(root),n),.08)*env(n,.005,.18)*.55
        add(bs+0.35*np.sin(2*np.pi*note(root)*np.arange(n)/SR)*env(n,.005,.2), t0+e*beat/2)
    # pluck arp 16ths
    arp=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+12]
    for e in range(16):
        n=int(.25*SR); m=arp[e%4]
        pl=lp(saw(note(m),n),.25)*env(n,.002,.07)*.09
        add(pl,t0+e*beat/4,1,.35 if e%2 else -.35)
# risers + impacts at brand moments
def riser(d):
    n=int(d*SR); t=np.arange(n)/SR; nz=rng.standard_normal(n); nz=nz-lp(nz,.3)
    return nz*(t/d)**2*.25
def impact():
    n=int(2.0*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*(40+60*np.exp(-t/.05))*t)*np.exp(-t/.5)*.9 + rng.standard_normal(n)*np.exp(-t/.25)*.25)
from edl import FLASH,BURN,LEAK,PUNCH,GLITCH
def whoosh(d=0.5):
    n=int(d*SR); t=np.arange(n)/SR; nz=rng.standard_normal(n)
    out=np.zeros(n); acc=0.
    a=0.02+0.5*np.sin(np.pi*t/d)**2
    for i in range(n): acc+=a[i]*(nz[i]-acc); out[i]=acc
    return out*np.sin(np.pi*t/d)**1.5*.9
for tt in BURN+LEAK+PUNCH:
    add(whoosh(0.5),tt-0.28,.55,0.3*np.sin(tt))
for tt in GLITCH:
    add(rng.standard_normal(int(.12*SR))*np.exp(-np.arange(int(.12*SR))/SR/.04)*.35,tt,1)
for tt in FLASH:
    add(riser(1.5),tt-1.5,.8); add(impact(),tt,.8)
# fade out
fo=int(3*SR); 
for ch in (L,R): ch[-fo:]*=np.linspace(1,0,fo)
st=np.stack([L,R],1); st/=np.abs(st).max()*1.12
w=wave.open('bgm.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
