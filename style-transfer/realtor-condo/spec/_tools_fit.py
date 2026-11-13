import numpy as np,sys,math
from scipy.optimize import least_squares
def bo(s): return lambda t:1+(s+1)*(t-1)**3+s*(t-1)**2
E={'power2.out':lambda t:1-(1-t)**2,'power3.out':lambda t:1-(1-t)**3,'power4.out':lambda t:1-(1-t)**5,
'expo.out':lambda t:1-2**(-10*t),'circ.out':lambda t:np.sqrt(1-(t-1)**2),'sine.out':lambda t:np.sin(t*np.pi/2),
'power2.inOut':lambda t:np.where(t<.5,2*t*t,1-(-2*t+2)**2/2),'power3.inOut':lambda t:np.where(t<.5,4*t**3,1-(-2*t+2)**3/2),
'expo.inOut':lambda t:np.where(t<.5,2**(20*t-10)/2,(2-2**(-20*t+10))/2),'back.out(1.7)':bo(1.7),'back.out(2.5)':bo(2.5),'back.out(1.2)':bo(1.2)}
def fit(fr,v):
    fr=np.array(fr,float);v=np.array(v,float);R=[]
    for n,e in E.items():
        def r(p):
            t0,d,a,b=p; t=np.clip((fr-t0)/max(d,1),0,1); return a+(b-a)*e(t)-v
        best=None
        for d0 in (6,10,16,24,34):
            s=least_squares(r,[fr[0]-1,d0,v[0],v[-1]])
            if best is None or s.cost<best.cost: best=s
        R.append((math.sqrt(2*best.cost/len(v)),n,[round(x,1) for x in best.x]))
    R.sort(); return R[:3]
if __name__=='__main__':
    d=[l.split() for l in open(sys.argv[1])]
    print(fit([float(x[0]) for x in d],[float(x[1]) for x in d]))
