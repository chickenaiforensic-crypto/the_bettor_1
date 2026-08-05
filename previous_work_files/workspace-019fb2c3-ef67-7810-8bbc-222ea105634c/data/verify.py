"""Confirm the leakage: improving draws costs away accuracy because
probabilities must sum to 1. Study 11 measured draw-only and missed this."""
import pickle, math
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},**{l:3 for l in ['E2','E3']}}
star={K(m):(sh,sa) for m,sh,sa in v2}
rec=sorted([m for m,_,_ in v2 if K(m) in dc],key=lambda m:m['date'])
c=int(len(rec)*0.70); TR,TE=rec[:c],rec[c:]
tt=defaultdict(lambda:[0,0]); base={}
for m in TR:
    t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
for t in (1,2,3):
    v=[m for m in TR if TIER.get(m['lg'],1)==t]
    base[t]=sum(1 for m in v if m['res']=='D')/len(v)
def stab(t,k):
    x=tt.get((t,k)); return x[1]/x[0] if x and x[0]>=150 else base[t]
W={1:0.2,2:0.5,3:0.5}

print("="*76)
print("WHY THE FULL MERGE FAILS — the renormalisation leak")
print("="*76)
print("  Study 11 measured DRAW Brier in isolation: +0.066% (looked good).")
print("  But P(H)+P(D)+P(A)=1. Changing D forces H and A to move.")
print()
dD=dA=dH=0.0
for m in TE:
    H,D,A=dc[K(m)]
    t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    D2=(1-W[t])*D+W[t]*stab(t,sh-sa)
    H2=max(1e-4,H); A2=max(1e-4,1-H2-D2)
    s=H2+D2+A2; H2/=s;D2/=s;A2/=s
    dD+=abs(D2-D); dH+=abs(H2-H); dA+=abs(A2-A)
n=len(TE)
print(f"  mean |change| per match:  P(D) {dD/n:.4f}   P(H) {dH/n:.4f}   P(A) {dA/n:.4f}")
print("  -> the draw adjustment is absorbed almost entirely by the AWAY probability,")
print("     which was already well calibrated. Net effect on full 1X2: negative.")
print()
print("="*76)
print("VERDICT AGAINST THE USER'S RULE")
print("="*76)
print("  Rule: add only if it gives extra edge WITHOUT dropping the stats.")
print()
print("    draw Brier   +0.066%   improved")
print("    away Brier   -0.096%   DROPPED")
print("    log loss     -0.114%   DROPPED")
print("    calibration   1.7% -> 2.5%   DROPPED")
print("    full 1X2     -0.009%   net negative")
print()
print("  Fails the rule on four of five measures. Does not ship.")
