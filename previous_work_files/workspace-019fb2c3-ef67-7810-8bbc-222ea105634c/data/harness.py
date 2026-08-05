"""
CORRECTED MEASUREMENT HARNESS — fixes 1-6 from Study 13.
  1. paired tests as standard
  2. minimum detectable effect reported alongside every result
  3. covid window flagged/excluded
  4. rolling-origin validation (multiple splits, not one)
  5. full 1X2 always measured
  6. renormalisation handled explicitly
"""
import math, pickle
from collections import defaultdict

COVID_START, COVID_END = "2020-03-01", "2021-06-30"

def is_covid(m):
    return COVID_START <= str(m['date'].date()) <= COVID_END

def paired_test(d):
    """d = list of per-match (base_error - variant_error). positive = variant better."""
    N=len(d)
    if N<2: return dict(n=N,mean=0,t=0,p=1,lo=0,hi=0,mde=0)
    mean=sum(d)/N
    sd=math.sqrt(sum((x-mean)**2 for x in d)/(N-1))
    se=sd/math.sqrt(N) if N else 0
    t=mean/se if se else 0
    p=2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2)))) if se else 1
    mde=2.8*sd/math.sqrt(N)          # 80% power, alpha .05, two-sided
    return dict(n=N,mean=mean,sd=sd,se=se,t=t,p=p,
                lo=mean-1.96*se,hi=mean+1.96*se,mde=mde)

def report(label,d,base_brier=None):
    r=paired_test(d)
    v = "BETTER" if (r['p']<0.05 and r['mean']>0) else ("WORSE" if (r['p']<0.05 and r['mean']<0) else "neutral")
    pct = f"{r['mean']/base_brier*100:+.4f}%" if base_brier else ""
    print(f"  {label:32s} n={r['n']:6,} {r['mean']:+.8f} {pct:>10s} t={r['t']:+6.2f} p={r['p']:.4f} "
          f"MDE={r['mde']:.8f} {v}")
    return r

def renorm(H,D,A):
    H=max(1e-6,H); D=max(1e-6,D); A=max(1e-6,A)
    s=H+D+A; return H/s,D/s,A/s

def err1x2(H,D,A,res):
    y=(1.0 if res=='H' else 0.,1.0 if res=='D' else 0.,1.0 if res=='A' else 0.)
    return (H-y[0])**2+(D-y[1])**2+(A-y[2])**2

def rolling_splits(items, keyfn, n_splits=4, train_frac=0.55):
    """rolling-origin: expanding train window, successive test blocks"""
    items=sorted(items,key=keyfn)
    N=len(items); start=int(N*train_frac); block=(N-start)//n_splits
    out=[]
    for i in range(n_splits):
        a=start+i*block
        b=start+(i+1)*block if i<n_splits-1 else N
        out.append((items[:a], items[a:b]))
    return out
