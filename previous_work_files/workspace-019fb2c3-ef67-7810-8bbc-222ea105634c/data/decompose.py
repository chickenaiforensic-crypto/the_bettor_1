"""
The matrix shows two AXES, not one:
  CONSENSUS    = (HvH + AvA)/2    -> how much better is the home side overall
  DISAGREEMENT = |HvH - AvA|      -> do the two lenses agree? (uncertainty signal)
Key cells: both strong 74.2% home / 16.5% draw.  Both level 42.4% / 30.0% draw.
Disagree  ~50% home / 27-28% draw.
Test whether DISAGREEMENT carries draw information the MODEL lacks.
"""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
data=pickle.load(open("hvh_ava.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
rec=[(m,(h+a)/2,abs(h-a)) for m,h,a in data if K(m) in dc]
rec.sort(key=lambda x:x[0]['date'])
print(f"matched: {len(rec):,}")

def wil(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    hh=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-hh,c+hh

print("\n"+"="*100)
print("AXIS 1 — CONSENSUS (both lenses averaged): pure strength")
print("="*100)
print(f"  {'band':16s} {'n':>8s} {'home W':>8s} {'draw':>8s} {'model P(H)':>11s} {'residual':>10s}")
for lo,hi in [(-99,-1),(-1,-0.5),(-0.5,0),(0,0.5),(0.5,1),(1,1.5),(1.5,99)]:
    v=[(m,c,d) for m,c,d in rec if lo<=c<hi]
    if len(v)<400: continue
    n=len(v); w=sum(1 for m,_,_ in v if m['res']=='H'); dr=sum(1 for m,_,_ in v if m['res']=='D')
    mp=sum(dc[K(m)][0] for m,_,_ in v)/n
    print(f"  [{lo:5.1f},{hi:5.1f})   {n:8,} {w/n:8.1%} {dr/n:8.1%} {mp:11.1%} {w/n-mp:+10.1%}")

print("\n"+"="*100)
print("AXIS 2 — DISAGREEMENT |HvH-AvA|: the uncertainty signal")
print("="*100)
print("  Held at CONSTANT consensus, does disagreement change the draw rate?")
print(f"  {'consensus':16s} {'disagree':12s} {'n':>7s} {'home W':>8s} {'draw':>8s} {'model D':>9s} {'resid':>8s}")
for clo,chi,cl in [(-0.3,0.3,"level"),(0.3,1.0,"home better"),(1.0,99,"home much better")]:
    for dlo,dhi,dl in [(0,0.5,"agree"),(0.5,1.2,"mild"),(1.2,99,"conflict")]:
        v=[(m,c,d) for m,c,d in rec if clo<=c<chi and dlo<=d<dhi]
        if len(v)<300: continue
        n=len(v); w=sum(1 for m,_,_ in v if m['res']=='H'); dr=sum(1 for m,_,_ in v if m['res']=='D')
        md=sum(dc[K(m)][1] for m,_,_ in v)/n
        lo_,hi_=wil(dr,n)
        flag=" <<<" if not (lo_<=md<=hi_) else ""
        print(f"  {cl:16s} {dl:12s} {n:7,} {w/n:8.1%} {dr/n:8.1%} {md:9.1%} {dr/n-md:+8.1%}{flag}")
print("  '<<<' = model draw prediction outside actual 95% CI -> unexplained signal")

print("\n"+"="*100)
print("IS DISAGREEMENT INDEPENDENT OF WHAT THE MODEL KNOWS?")
print("="*100)
def corr(x,y):
    mx,my=sum(x)/len(x),sum(y)/len(y)
    n=sum((a-mx)*(b-my) for a,b in zip(x,y))
    d=math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return n/d if d else 0
cons=[c for _,c,_ in rec]; dis=[d for _,_,d in rec]
mph=[dc[K(m)][0] for m,_,_ in rec]; mpd=[dc[K(m)][1] for m,_,_ in rec]
print(f"  corr(consensus, model P(home)) = {corr(cons,mph):+.4f}   <- model already knows this")
print(f"  corr(disagreement, model P(draw)) = {corr(dis,mpd):+.4f}   <- weak = potentially NEW")
print(f"  corr(disagreement, |model P(H)-P(A)|) = {corr(dis,[abs(dc[K(m)][0]-dc[K(m)][2]) for m,_,_ in rec]):+.4f}")

print("\n"+"="*100)
print("DRAW RATE BY DISAGREEMENT ALONE")
print("="*100)
print(f"  {'disagreement':16s} {'n':>8s} {'draw':>8s} {'95% CI':>16s} {'model D':>9s} {'resid':>8s}")
for lo,hi in [(0,0.3),(0.3,0.6),(0.6,1.0),(1.0,1.5),(1.5,2.5),(2.5,99)]:
    v=[(m,c,d) for m,c,d in rec if lo<=d<hi]
    if len(v)<400: continue
    n=len(v); dr=sum(1 for m,_,_ in v if m['res']=='D')
    md=sum(dc[K(m)][1] for m,_,_ in v)/n
    l,h=wil(dr,n)
    print(f"  [{lo:4.1f},{hi:5.1f})     {n:8,} {dr/n:8.1%} [{l:.1%},{h:.1%}] {md:9.1%} {dr/n-md:+8.1%}")
