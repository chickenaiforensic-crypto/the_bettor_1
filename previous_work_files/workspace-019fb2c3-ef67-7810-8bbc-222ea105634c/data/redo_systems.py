"""Re-test every rejected system with paired tests + rolling origin + covid handling."""
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
print(f"star-rated fixtures: {len(rec):,}")

def fit_tables(TR):
    tt=defaultdict(lambda:[0,0]); base={}
    for m in TR:
        t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
    for t in (1,2,3):
        v=[m for m in TR if TIER.get(m['lg'],1)==t]
        base[t]=sum(1 for m in v if m['res']=='D')/len(v) if v else 0.27
    def tab(t,k):
        x=tt.get((t,k)); return x[1]/x[0] if x and x[0]>=150 else base[t]
    return tab

W={1:0.2,2:0.5,3:0.5}

print("\n"+"="*100)
print("RE-TEST A — STAR DRAW TABLE, rolling origin, DRAW probability only")
print("="*100)
for i,(TR,TE) in enumerate(rolling_splits(rec,lambda m:m['date'],4),1):
    tab=fit_tables(TR)
    d=[]
    for m in TE:
        H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        D2=(1-W[t])*D+W[t]*tab(t,sh-sa); y=1.0 if m['res']=='D' else 0.0
        d.append((D-y)**2-(D2-y)**2)
    bb=sum((dc[K(m)][1]-(1.0 if m['res']=='D' else 0.0))**2 for m in TE)/len(TE)
    report(f"split {i} ({TE[0]['date'].date()})",d,bb)

print("\n"+"="*100)
print("RE-TEST B — SAME, but FULL 1X2 (the renormalisation cost)")
print("="*100)
for i,(TR,TE) in enumerate(rolling_splits(rec,lambda m:m['date'],4),1):
    tab=fit_tables(TR)
    d=[]
    for m in TE:
        H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        D2=(1-W[t])*D+W[t]*tab(t,sh-sa)
        H2,D2n,A2=renorm(H,D2,1-H-D2)
        d.append(err1x2(H,D,A,m['res'])-err1x2(H2,D2n,A2,m['res']))
    bb=sum(err1x2(*dc[K(m)],m['res']) for m in TE)/len(TE)
    report(f"split {i} ({TE[0]['date'].date()})",d,bb)

print("\n"+"="*100)
print("RE-TEST C — FIX THE LEAK: take the draw adjustment from BOTH H and A proportionally")
print("="*100)
print("  old: D changes, A absorbs all of it.  new: H and A each give up their share.")
for i,(TR,TE) in enumerate(rolling_splits(rec,lambda m:m['date'],4),1):
    tab=fit_tables(TR)
    d=[]
    for m in TE:
        H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        D2=(1-W[t])*D+W[t]*tab(t,sh-sa)
        rem=1-D2; tot=H+A
        H2=rem*(H/tot); A2=rem*(A/tot)          # proportional split
        H2,D2n,A2=renorm(H2,D2,A2)
        d.append(err1x2(H,D,A,m['res'])-err1x2(H2,D2n,A2,m['res']))
    bb=sum(err1x2(*dc[K(m)],m['res']) for m in TE)/len(TE)
    report(f"split {i} ({TE[0]['date'].date()})",d,bb)

print("\n"+"="*100)
print("RE-TEST D — POOLED over all splits, leak fixed, by tier and covid status")
print("="*100)
allsp=rolling_splits(rec,lambda m:m['date'],4)
pool=defaultdict(list)
for TR,TE in allsp:
    tab=fit_tables(TR)
    for m in TE:
        H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        D2=(1-W[t])*D+W[t]*tab(t,sh-sa)
        rem=1-D2; tot=H+A
        H2,D2n,A2=renorm(rem*(H/tot),D2,rem*(A/tot))
        delta=err1x2(H,D,A,m['res'])-err1x2(H2,D2n,A2,m['res'])
        pool['all'].append(delta); pool[f'tier{t}'].append(delta)
        pool['covid' if is_covid(m) else 'nocovid'].append(delta)
bb=0.608
for k in ['all','nocovid','covid','tier1','tier2','tier3']:
    if pool[k]: report(k,pool[k],bb)
