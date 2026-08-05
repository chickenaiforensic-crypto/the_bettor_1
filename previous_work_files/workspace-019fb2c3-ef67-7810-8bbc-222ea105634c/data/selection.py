"""Consensus selection hit 81.8% at 2% coverage. Is that better than the MODEL's
own top picks, or is the model still better? This decides the tactical use."""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
data=pickle.load(open("hvh_ava.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
rec=[(m,(h+a)/2,abs(h-a),h,a) for m,h,a in data if K(m) in dc]
print(f"n = {len(rec):,}")
def wil(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    hh=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-hh,c+hh

print("\n"+"="*100)
print("SELECTION SHOOT-OUT — who picks the best home wins?")
print("="*100)
print(f"  {'cov':>5s} {'n':>6s} | {'MODEL P(H)':>22s} | {'consensus':>22s} | {'HvH only':>22s}")
print(f"  {'':5s} {'':6s} | {'win%':>10s} {'draw%':>10s} | {'win%':>10s} {'draw%':>10s} | {'win%':>10s} {'draw%':>10s}")
for cov in [0.10,0.05,0.03,0.02,0.01]:
    k=int(len(rec)*cov)
    out=[]
    for keyf in [lambda x:-dc[K(x[0])][0], lambda x:-x[1], lambda x:-x[3]]:
        s=sorted(rec,key=keyf)[:k]
        w=sum(1 for r in s if r[0]['res']=='H')/k
        d=sum(1 for r in s if r[0]['res']=='D')/k
        out.append((w,d))
    print(f"  {cov:5.0%} {k:6,} | {out[0][0]:10.1%} {out[0][1]:10.1%} | {out[1][0]:10.1%} {out[1][1]:10.1%} | {out[2][0]:10.1%} {out[2][1]:10.1%}")

print("\n"+"="*100)
print("COMBINED FILTER — model's top picks, further filtered by the lenses")
print("="*100)
k=int(len(rec)*0.10)
top=sorted(rec,key=lambda x:-dc[K(x[0])][0])[:k]
w0=sum(1 for r in top if r[0]['res']=='H')/len(top)
lo0,hi0=wil(sum(1 for r in top if r[0]['res']=='H'),len(top))
print(f"  model top 10%:                  n={len(top):6,} home {w0:6.1%} [{lo0:.1%},{hi0:.1%}]")
for lbl,f in [("+ consensus > 1.0",lambda r: r[1]>1.0),
              ("+ consensus > 1.5",lambda r: r[1]>1.5),
              ("+ lenses agree (disagree<0.6)",lambda r: r[2]<0.6),
              ("+ BOTH lenses positive",lambda r: r[3]>0 and r[4]>0),
              ("+ consensus>1.0 AND agree<0.8",lambda r: r[1]>1.0 and r[2]<0.8)]:
    v=[r for r in top if f(r)]
    if len(v)<150: print(f"  {lbl:32s} n={len(v)} too few"); continue
    w=sum(1 for r in v if r[0]['res']=='H'); n=len(v)
    lo,hi=wil(w,n)
    sig=" SIG" if lo>w0 else ""
    print(f"  {lbl:32s} n={n:6,} home {w/n:6.1%} [{lo:.1%},{hi:.1%}] {w/n-w0:+6.1%}{sig}")

print("\n"+"="*100)
print("DRAW SELECTION — model's flattest games, filtered by the lenses")
print("="*100)
flat=sorted(rec,key=lambda x:-dc[K(x[0])][1])[:int(len(rec)*0.10)]
d0=sum(1 for r in flat if r[0]['res']=='D')/len(flat)
lo0,hi0=wil(sum(1 for r in flat if r[0]['res']=='D'),len(flat))
print(f"  model top-10% draw picks:       n={len(flat):6,} draw {d0:6.1%} [{lo0:.1%},{hi0:.1%}]")
for lbl,f in [("+ |consensus| < 0.2",lambda r: abs(r[1])<0.2),
              ("+ lenses agree (disagree<0.5)",lambda r: r[2]<0.5),
              ("+ |cons|<0.2 AND agree<0.5",lambda r: abs(r[1])<0.2 and r[2]<0.5),
              ("+ disagreement > 1.2",lambda r: r[2]>1.2)]:
    v=[r for r in flat if f(r)]
    if len(v)<150: print(f"  {lbl:32s} n={len(v)} too few"); continue
    d=sum(1 for r in v if r[0]['res']=='D'); n=len(v)
    lo,hi=wil(d,n)
    sig=" SIG" if lo>d0 else ""
    print(f"  {lbl:32s} n={n:6,} draw {d/n:6.1%} [{lo:.1%},{hi:.1%}] {d/n-d0:+6.1%}{sig}")
