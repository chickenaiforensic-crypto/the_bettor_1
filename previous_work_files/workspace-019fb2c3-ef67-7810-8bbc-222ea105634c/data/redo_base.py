"""Re-validate the BASE model itself with the corrected harness."""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict

preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
P=sorted(preds,key=lambda x:x[0]['date'])
BASE=(0.446,0.268,0.286)

print("="*100)
print("RE-VALIDATION 1 — BASE MODEL vs FIXED BASE RATE (paired, was never paired before)")
print("="*100)
d=[err1x2(*BASE,m['res'])-err1x2(H,D,A,m['res']) for m,H,D,A,lh,la in P]
b0=sum(err1x2(*BASE,m['res']) for m,_,_,_,_,_ in P)/len(P)
report("model vs base rate (ALL)",d,b0)

nc=[(m,H,D,A) for m,H,D,A,lh,la in P if not is_covid(m)]
cv=[(m,H,D,A) for m,H,D,A,lh,la in P if is_covid(m)]
print(f"\n  covid window: {len(cv):,} matches ({len(cv)/len(P):.1%})")
for lbl,S in [("excluding covid",nc),("covid window only",cv)]:
    dd=[err1x2(*BASE,m['res'])-err1x2(H,D,A,m['res']) for m,H,D,A in S]
    bb=sum(err1x2(*BASE,m['res']) for m,_,_,_ in S)/len(S)
    report(lbl,dd,bb)

print("\n"+"="*100)
print("RE-VALIDATION 2 — ROLLING-ORIGIN (4 splits, not one arbitrary date)")
print("="*100)
splits=rolling_splits(P,lambda x:x[0]['date'],n_splits=4)
for i,(tr,te) in enumerate(splits,1):
    dd=[err1x2(*BASE,m['res'])-err1x2(H,D,A,m['res']) for m,H,D,A,lh,la in te]
    bb=sum(err1x2(*BASE,m['res']) for m,_,_,_,_,_ in te)/len(te)
    a=te[0][0]['date'].date(); b=te[-1][0]['date'].date()
    report(f"split {i} ({a}..{b})",dd,bb)

print("\n"+"="*100)
print("RE-VALIDATION 3 — CALIBRATION, covid-excluded")
print("="*100)
bk=defaultdict(lambda:[0,0.0,0])
for m,H,D,A in nc:
    b=min(8,int(H*10)); x=bk[b]; x[0]+=1; x[1]+=H; x[2]+=(m['res']=='H')
mx=0
print(f"  {'band':10s} {'n':>8s} {'pred':>8s} {'actual':>8s} {'err':>8s}")
for b in sorted(bk):
    n,p,a=bk[b]
    if n<300: continue
    e=abs(p/n-a/n); mx=max(mx,e)
    print(f"  {b/10:.1f}-{(b+1)/10:.1f}   {n:8,} {p/n:8.1%} {a/n:8.1%} {a/n-p/n:+8.1%}")
print(f"  max calibration error (covid excluded): {mx:.2%}")
