"""
WHY does the star system work in lower divisions and fail in top flights?
Diagnose the mechanism before calibrating. No fixes yet.
"""
import pickle, math, statistics as S
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
rows=pickle.load(open("all_matches.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}

TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},
      **{l:3 for l in ['E2','E3']}}
TN={1:'top flight',2:'second tier',3:'third/fourth'}

print("="*88)
print("HYPOTHESIS 1 — top divisions are more STRATIFIED, so a star bucket")
print("               hides a much wider range of real ability")
print("="*88)
# within-league spread of end-of-season PPG
sp=defaultdict(list)
tbl=defaultdict(lambda:[0,0])
for m in rows:
    for t,pts in ((m['home'],3 if m['res']=='H' else 1 if m['res']=='D' else 0),
                  (m['away'],3 if m['res']=='A' else 1 if m['res']=='D' else 0)):
        k=(m['lg'],m['season'],t); tbl[k][0]+=pts; tbl[k][1]+=1
byls=defaultdict(list)
for (lg,se,t),(p,n) in tbl.items():
    if n>=20: byls[(lg,se)].append(p/n)
for (lg,se),v in byls.items():
    if len(v)>=10: sp[TIER.get(lg,1)].append(S.pstdev(v))
print(f"  {'tier':16s} {'league-seasons':>15s} {'mean sd of PPG':>16s}")
for t in (1,2,3):
    print(f"  {TN[t]:16s} {len(sp[t]):15,} {sum(sp[t])/len(sp[t]):16.3f}")
print("  -> higher sd = more stratified = one star covers more real ability")

print("\n"+"="*88)
print("HYPOTHESIS 2 — within-star ability spread, by tier")
print("="*88)
ws=defaultdict(list)
for m,sh,sa in v2:
    k=K(m)
    if k not in dc: continue
    t=TIER.get(m['lg'],1)
    ws[(t,sh)].append(dc[k][0])       # model P(home) as an ability proxy
print(f"  {'tier':16s} {'star':>5s} {'n':>8s} {'sd of model P(home)':>21s}")
for t in (1,2,3):
    for s in range(1,6):
        v=ws.get((t,s),[])
        if len(v)<300: continue
        print(f"  {TN[t]:16s} {s:>5d} {len(v):8,} {S.pstdev(v):21.4f}")
print("  -> if top-flight sd is larger, the star label is a coarser summary there")

print("\n"+"="*88)
print("HYPOTHESIS 3 — where exactly does the draw table go wrong, by tier?")
print("="*88)
dat=sorted([(m,s,a) for m,s,a in v2 if K(m) in dc],key=lambda x:x[0]['date'])
c=int(len(dat)*0.70); TR,TE=dat[:c],dat[c:]
tab=defaultdict(lambda:[0,0])
for m,sh,sa in TR:
    x=tab[sh-sa]; x[0]+=1; x[1]+=(m['res']=='D')
G=sum(1 for m,_,_ in TR if m['res']=='D')/len(TR)
sd_=lambda k:(tab[k][1]/tab[k][0]) if tab.get(k) and tab[k][0]>=200 else G
print(f"  {'tier':16s} {'gap':>5s} {'n':>7s} {'global tbl':>11s} {'actual':>8s} {'error':>8s}")
for t in (1,2,3):
    for g in (-2,-1,0,1,2):
        v=[m for m,sh,sa in TE if TIER.get(m['lg'],1)==t and sh-sa==g]
        if len(v)<300: continue
        act=sum(1 for m in v if m['res']=='D')/len(v)
        print(f"  {TN[t]:16s} {g:>+5d} {len(v):7,} {sd_(g):11.1%} {act:8.1%} {sd_(g)-act:+8.1%}")
print("  -> a single global table mis-states the draw rate differently in each tier")

print("\n"+"="*88)
print("HYPOTHESIS 4 — base draw rates simply differ by tier")
print("="*88)
print(f"  {'tier':16s} {'n':>9s} {'draw rate':>11s} {'same-star draw':>16s} {'lift':>7s}")
for t in (1,2,3):
    v=[(m,sh,sa) for m,sh,sa in v2 if TIER.get(m['lg'],1)==t]
    n=len(v); dr=sum(1 for m,_,_ in v if m['res']=='D')/n
    ss=[m for m,sh,sa in v if sh==sa]
    ds=sum(1 for m in ss if m['res']=='D')/len(ss)
    df=[m for m,sh,sa in v if sh!=sa]
    dd=sum(1 for m in df if m['res']=='D')/len(df)
    print(f"  {TN[t]:16s} {n:9,} {dr:11.1%} {ds:16.1%} {ds-dd:+7.2%}")
print("  -> the same-star LIFT is real in every tier; the base rate it sits on differs")
