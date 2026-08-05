"""
Residuals are POSITIVE at high home-v-home (model under-rates strong home sides).
Test a proper monotone correction, rolling-origin, paired, full 1X2.
This is the test I should have run the first time.
"""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
data=pickle.load(open("hvh_data.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
recs=sorted([(m,hh['gd']-ah['gd']) for m,hh,ah,aa,ha in data if K(m) in dc],
            key=lambda x:x[0]['date'])
print(f"n = {len(recs):,}")

BANDS=[(-99,-1.0),(-1.0,-0.5),(-0.5,0.0),(0.0,0.5),(0.5,1.0),(1.0,1.5),(1.5,99)]
def bidx(v):
    for i,(lo,hi) in enumerate(BANDS):
        if lo<=v<hi: return i
    return len(BANDS)-1

def fit(TR,shrink=200):
    t=defaultdict(lambda:[0,0.0,0.0])
    for m,v in TR:
        i=bidx(v); x=t[i]; x[0]+=1
        x[1]+=(1.0 if m['res']=='H' else 0.0)-dc[K(m)][0]
        x[2]+=(1.0 if m['res']=='D' else 0.0)-dc[K(m)][1]
    # shrink toward zero by sample size -> avoids fitting noise
    return {i:(v[1]/(v[0]+shrink), v[2]/(v[0]+shrink)) for i,v in t.items() if v[0]>=300}

print("\n"+"="*94)
print("ROLLING-ORIGIN, PAIRED, FULL 1X2 — proper correction")
print("="*94)
for W in [0.5,1.0]:
    print(f"\n  weight {W}:")
    pool=[]
    for TR,TE in rolling_splits(recs,lambda x:x[0]['date'],4):
        tab=fit(TR)
        d=[]
        for m,v in TE:
            H,D,A=dc[K(m)]
            ch,cd=tab.get(bidx(v),(0.0,0.0))
            H2=H+W*ch; D2=D+W*cd
            H2,D2,A2=renorm(H2,D2,1-H2-D2)
            d.append(err1x2(H,D,A,m['res'])-err1x2(H2,D2,A2,m['res']))
        pool+=d
        report(f"    split {TE[0][0]['date'].date()}",d,0.608)
    report(f"    POOLED w={W}",pool,0.608)

print("\n"+"="*94)
print("BEST CONFIG — every metric, user's rule")
print("="*94)
W=1.0
rows=[]
for TR,TE in rolling_splits(recs,lambda x:x[0]['date'],4):
    tab=fit(TR)
    for m,v in TE:
        H,D,A=dc[K(m)]
        ch,cd=tab.get(bidx(v),(0.0,0.0))
        H2,D2,A2=renorm(H+W*ch,D+W*cd,1-(H+W*ch)-(D+W*cd))
        rows.append((m,H,D,A,H2,D2,A2))
for nm,f in [("home Brier",lambda m,H,D,A:(H-(1.0 if m['res']=='H' else 0.))**2),
             ("draw Brier",lambda m,H,D,A:(D-(1.0 if m['res']=='D' else 0.))**2),
             ("away Brier",lambda m,H,D,A:(A-(1.0 if m['res']=='A' else 0.))**2),
             ("full 1X2",lambda m,H,D,A:err1x2(H,D,A,m['res'])),
             ("log loss",lambda m,H,D,A:-math.log(max({'H':H,'D':D,'A':A}[m['res']],1e-12)))]:
    d=[f(m,H,D,A)-f(m,H2,D2,A2) for m,H,D,A,H2,D2,A2 in rows]
    b=sum(f(m,H,D,A) for m,H,D,A,_,_,_ in rows)/len(rows)
    report(nm,d,b)
def cal(idx,which):
    bk=defaultdict(lambda:[0,0.0,0])
    for r in rows:
        m=r[0]; p=r[idx]; b=min(8,int(p*10)); x=bk[b]; x[0]+=1; x[1]+=p; x[2]+=(m['res']==which)
    return max(abs(v[1]/v[0]-v[2]/v[0]) for v in bk.values() if v[0]>=300)
print(f"\n  home calibration: base {cal(1,'H'):.2%} -> with hvh {cal(4,'H'):.2%}")
print(f"  draw calibration: base {cal(2,'D'):.2%} -> with hvh {cal(5,'D'):.2%}")
