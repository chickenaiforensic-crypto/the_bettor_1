"""
Disagreement is nearly independent of the model (r=-0.09) and shows residuals
up to +1.3pt on draws. Test extraction properly: rolling-origin, paired, full 1X2,
with the proportional renormalisation that worked for stars.
"""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
data=pickle.load(open("hvh_ava.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
rec=sorted([(m,(h+a)/2,abs(h-a)) for m,h,a in data if K(m) in dc],key=lambda x:x[0]['date'])

# 2-D cell: consensus band x disagreement band
CB=[(-99,-0.5),(-0.5,0.3),(0.3,1.0),(1.0,99)]
DB=[(0,0.5),(0.5,1.2),(1.2,99)]
def ci(v):
    for i,(lo,hi) in enumerate(CB):
        if lo<=v<hi: return i
    return 3
def di(v):
    for i,(lo,hi) in enumerate(DB):
        if lo<=v<hi: return i
    return 2

def fit(TR,shrink=400):
    t=defaultdict(lambda:[0,0.0])
    for m,c,d in TR:
        k=(ci(c),di(d)); x=t[k]; x[0]+=1
        x[1]+=(1.0 if m['res']=='D' else 0.0)-dc[K(m)][1]
    return {k:v[1]/(v[0]+shrink) for k,v in t.items() if v[0]>=400}

print("="*94)
print("EXTRACTION TEST — draw correction from the (consensus x disagreement) cell")
print("="*94)
for W in [0.5,1.0]:
    pool=[]
    print(f"\n  weight {W}:")
    for TR,TE in rolling_splits(rec,lambda x:x[0]['date'],4):
        tab=fit(TR)
        d=[]
        for m,c,dd in TE:
            H,D,A=dc[K(m)]
            adj=tab.get((ci(c),di(dd)),0.0)*W
            D2=D+adj
            rem=1-D2; tot=H+A
            H2,D2n,A2=renorm(rem*(H/tot),D2,rem*(A/tot))
            d.append(err1x2(H,D,A,m['res'])-err1x2(H2,D2n,A2,m['res']))
        pool+=d
        report(f"    split {TE[0][0]['date'].date()}",d,0.608)
    report(f"    POOLED w={W}",pool,0.608)

print("\n"+"="*94)
print("BEST WEIGHT — all metrics under the user's rule")
print("="*94)
W=0.5
rows=[]
for TR,TE in rolling_splits(rec,lambda x:x[0]['date'],4):
    tab=fit(TR)
    for m,c,dd in TE:
        H,D,A=dc[K(m)]
        D2=D+tab.get((ci(c),di(dd)),0.0)*W
        rem=1-D2; tot=H+A
        H2,D2n,A2=renorm(rem*(H/tot),D2,rem*(A/tot))
        rows.append((m,H,D,A,H2,D2n,A2))
for nm,f in [("home Brier",lambda m,H,D,A:(H-(1.0 if m['res']=='H' else 0.))**2),
             ("draw Brier",lambda m,H,D,A:(D-(1.0 if m['res']=='D' else 0.))**2),
             ("away Brier",lambda m,H,D,A:(A-(1.0 if m['res']=='A' else 0.))**2),
             ("full 1X2",lambda m,H,D,A:err1x2(H,D,A,m['res'])),
             ("log loss",lambda m,H,D,A:-math.log(max({'H':H,'D':D,'A':A}[m['res']],1e-12)))]:
    d=[f(m,H,D,A)-f(m,H2,D2,A2) for m,H,D,A,H2,D2,A2 in rows]
    b=sum(f(m,H,D,A) for m,H,D,A,_,_,_ in rows)/len(rows)
    report(nm,d,b)

print("\n"+"="*94)
print("SELECTION VALUE — the tactical use (no probability change)")
print("="*94)
print("  Best home-win picks using BOTH lenses vs consensus alone:")
print(f"  {'coverage':>9s} {'consensus only':>18s} {'both lenses agree':>20s} {'gain':>7s}")
for cov in [0.10,0.05,0.03,0.02]:
    k=int(len(rec)*cov)
    s1=sorted(rec,key=lambda x:-x[1])[:k]
    w1=sum(1 for m,_,_ in s1 if m['res']=='H')/k
    cand=[(m,c,d) for m,c,d in rec if d<0.6]
    s2=sorted(cand,key=lambda x:-x[1])[:k]
    w2=sum(1 for m,_,_ in s2 if m['res']=='H')/len(s2) if s2 else 0
    print(f"  {cov:9.0%} {w1:18.1%} {w2:20.1%} {w2-w1:+7.1%}")
print("\n  Draw-targeting: lowest consensus + highest disagreement")
print(f"  {'selection':>28s} {'n':>7s} {'draw%':>8s} {'base draw':>10s}")
base=sum(1 for m,_,_ in rec if m['res']=='D')/len(rec)
for lbl,f in [("|cons|<0.2 any",lambda c,d: abs(c)<0.2),
              ("|cons|<0.2 & disagree>1.2",lambda c,d: abs(c)<0.2 and d>1.2),
              ("|cons|<0.15 & disagree>1.5",lambda c,d: abs(c)<0.15 and d>1.5)]:
    v=[m for m,c,d in rec if f(c,d)]
    if len(v)<200: continue
    print(f"  {lbl:>28s} {len(v):7,} {sum(1 for m in v if m['res']=='D')/len(v):8.1%} {base:10.1%}")
