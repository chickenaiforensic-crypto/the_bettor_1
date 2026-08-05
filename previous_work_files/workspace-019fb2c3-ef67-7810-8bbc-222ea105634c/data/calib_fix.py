"""Home calibration degraded 1.73->2.60%. Diagnose and fix."""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},**{l:3 for l in ['E2','E3']}}
v2=pickle.load(open("stars_v2.pkl","rb"))
star={K(m):(sh,sa) for m,sh,sa in v2}
rec=sorted([m for m,_,_ in v2 if K(m) in dc],key=lambda m:m['date'])
def fit(TR):
    tt=defaultdict(lambda:[0,0]); base={}
    for m in TR:
        t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
    for t in (1,2,3):
        v=[m for m in TR if TIER.get(m['lg'],1)==t]
        base[t]=sum(1 for m in v if m['res']=='D')/len(v) if v else .27
    return lambda t,k:(tt[(t,k)][1]/tt[(t,k)][0]) if tt.get((t,k)) and tt[(t,k)][0]>=150 else base[t]

def run(W,cap=None):
    rows=[]
    for TR,TE in rolling_splits(rec,lambda m:m['date'],4):
        tab=fit(TR)
        for m in TE:
            H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
            D2=(1-W[t])*D+W[t]*tab(t,sh-sa)
            if cap is not None: D2=max(D-cap,min(D+cap,D2))   # limit the move
            rem=1-D2; tot=H+A
            H2,D2n,A2=renorm(rem*(H/tot),D2,rem*(A/tot))
            rows.append((m,H,D,A,H2,D2n,A2))
    return rows

def calib(rows,idx,which):
    bk=defaultdict(lambda:[0,0.0,0])
    for r in rows:
        m=r[0]; p=r[idx]
        b=min(8,int(p*10)); x=bk[b]; x[0]+=1; x[1]+=p; x[2]+=(m['res']==which)
    return max(abs(v[1]/v[0]-v[2]/v[0]) for v in bk.values() if v[0]>=300)

print("="*94)
print("DIAGNOSIS — where does home calibration break?")
print("="*94)
rows=run({1:0.2,2:0.5,3:0.5})
bk=defaultdict(lambda:[0,0.0,0,0.0])
for m,H,D,A,H2,D2,A2 in rows:
    b=min(8,int(H2*10)); x=bk[b]; x[0]+=1; x[1]+=H2; x[2]+=(m['res']=='H'); x[3]+=H
print(f"  {'band':10s} {'n':>7s} {'base pred':>10s} {'new pred':>10s} {'actual':>8s} {'new err':>9s}")
for b in sorted(bk):
    n,p,a,pb=bk[b]
    if n<300: continue
    print(f"  {b/10:.1f}-{(b+1)/10:.1f}   {n:7,} {pb/n:10.1%} {p/n:10.1%} {a/n:8.1%} {a/n-p/n:+9.1%}")

print("\n"+"="*94)
print("FIX — cap how far the draw estimate may move, and lower tier weights")
print("="*94)
print(f"  {'config':34s} {'homeCal':>9s} {'drawCal':>9s} {'1X2 gain':>11s} {'p':>8s}")
base_rows=[(m,H,D,A,H,D,A) for m,H,D,A,_,_,_ in rows]
for lbl,W,cap in [("current W=.2/.5/.5 no cap",{1:0.2,2:0.5,3:0.5},None),
                  ("cap 0.03",{1:0.2,2:0.5,3:0.5},0.03),
                  ("cap 0.02",{1:0.2,2:0.5,3:0.5},0.02),
                  ("W=.1/.3/.3 cap 0.02",{1:0.1,2:0.3,3:0.3},0.02),
                  ("W=0/.3/.3 cap 0.02",{1:0.0,2:0.3,3:0.3},0.02),
                  ("W=0/.25/.25 cap 0.015",{1:0.0,2:0.25,3:0.25},0.015)]:
    r=run(W,cap)
    hc=calib(r,4,'H'); dcal=calib(r,5,'D')
    d=[err1x2(H,D,A,m['res'])-err1x2(H2,D2,A2,m['res']) for m,H,D,A,H2,D2,A2 in r]
    st=paired_test(d)
    print(f"  {lbl:34s} {hc:9.2%} {dcal:9.2%} {st['mean']/0.608*100:+10.4f}% {st['p']:8.4f}")
print(f"\n  BASELINE (no stars)                {calib(base_rows,4,'H'):9.2%} {calib(base_rows,5,'D'):9.2%}")
