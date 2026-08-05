"""Is the 0.7-0.8 calibration 'failure' real, or a thin-band artefact?"""
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
W={1:0.2,2:0.5,3:0.5}; CAP=0.02
rows=[]
for TR,TE in rolling_splits(rec,lambda m:m['date'],4):
    tab=fit(TR)
    for m in TE:
        H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        D2=(1-W[t])*D+W[t]*tab(t,sh-sa); D2=max(D-CAP,min(D+CAP,D2))
        rem=1-D2; tot=H+A
        H2,D2n,A2=renorm(rem*(H/tot),D2,rem*(A/tot))
        rows.append((m,H,D,A,H2,D2n,A2))

def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h

print("="*98)
print("HOME-WIN CALIBRATION WITH CIs — is any band's error outside sampling noise?")
print("="*98)
print(f"  {'band':10s} {'n':>7s} {'base':>8s} {'stars':>8s} {'actual':>8s} {'95% CI actual':>18s} {'base in CI':>11s} {'stars in CI':>12s}")
bk=defaultdict(lambda:[0,0.0,0,0.0])
for m,H,D,A,H2,D2,A2 in rows:
    b=min(8,int(H2*10)); x=bk[b]; x[0]+=1; x[1]+=H2; x[2]+=(m['res']=='H'); x[3]+=H
for b in sorted(bk):
    n,ps,a,pb=bk[b]
    if n<300: continue
    lo,hi=wilson(a,n)
    inb = lo<=pb/n<=hi; ins = lo<=ps/n<=hi
    print(f"  {b/10:.1f}-{(b+1)/10:.1f}   {n:7,} {pb/n:8.1%} {ps/n:8.1%} {a/n:8.1%} [{lo:6.1%},{hi:6.1%}] "
          f"{'yes' if inb else 'NO':>11s} {'yes' if ins else 'NO':>12s}")
print("\n  -> if both sit inside the CI, the 'error' is sampling noise, not miscalibration")

print("\n"+"="*98)
print("FINAL CONFIG: W=.2/.5/.5, cap 0.02, proportional split")
print("="*98)
for nm,f in [("home Brier",lambda m,H,D,A:(H-(1.0 if m['res']=='H' else 0.))**2),
             ("draw Brier",lambda m,H,D,A:(D-(1.0 if m['res']=='D' else 0.))**2),
             ("away Brier",lambda m,H,D,A:(A-(1.0 if m['res']=='A' else 0.))**2),
             ("full 1X2",lambda m,H,D,A:err1x2(H,D,A,m['res'])),
             ("log loss",lambda m,H,D,A:-math.log(max({'H':H,'D':D,'A':A}[m['res']],1e-12)))]:
    d=[f(m,H,D,A)-f(m,H2,D2,A2) for m,H,D,A,H2,D2,A2 in rows]
    b=sum(f(m,H,D,A) for m,H,D,A,_,_,_ in rows)/len(rows)
    report(nm,d,b)
pool=defaultdict(list)
for m,H,D,A,H2,D2,A2 in rows:
    t=TIER.get(m['lg'],1)
    pool[f'tier{t}'].append(err1x2(H,D,A,m['res'])-err1x2(H2,D2,A2,m['res']))
print()
for k in ['tier1','tier2','tier3']: report(k,pool[k],0.608)
