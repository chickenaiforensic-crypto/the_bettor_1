"""Re-test v2 against the model on HELD-OUT data. Blend weight from TRAIN only."""
import pickle, math, random
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
v1=pickle.load(open("user_stars.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}

def prep(dat):
    dat=sorted(dat,key=lambda x:x[0]['date'])
    dat=[(m,s,t) for m,s,t in dat if K(m) in dc]
    c=int(len(dat)*0.70); return dat[:c],dat[c:]
TR1,TE1=prep(v1); TR2,TE2=prep(v2)
print(f"v2: train {len(TR2):,}  test {len(TE2):,}  (test from {TE2[0][0]['date'].date()})")

def table(TR):
    t=defaultdict(lambda:[0,0])
    for m,sh,sa in TR:
        c=t[sh-sa]; c[0]+=1; c[1]+=(m['res']=='D')
    g=sum(1 for m,_,_ in TR if m['res']=='D')/len(TR)
    return t,g

def evaluate(TR,TE,label):
    t,g=table(TR)
    sd=lambda k:(t[k][1]/t[k][0]) if t.get(k) and t[k][0]>=200 else g
    dcb=sum((dc[K(m)][1]-(m['res']=='D'))**2 for m,_,_ in TE)/len(TE)
    # choose weight on TRAIN
    best=(9,0)
    for w in [0,.05,.1,.15,.2,.25,.3,.4,.5]:
        tr=sum((((1-w)*dc[K(m)][1]+w*sd(sh-sa))-(m['res']=='D'))**2 for m,sh,sa in TR)/len(TR)
        if tr<best[0]: best=(tr,w)
    w=best[1]
    delta=[]
    for m,sh,sa in TE:
        y=1.0 if m['res']=='D' else 0.0
        p=dc[K(m)][1]; b=(1-w)*p+w*sd(sh-sa)
        delta.append((p-y)**2-(b-y)**2)
    N=len(delta); gain=sum(delta)/N
    random.seed(5)
    bs=[]
    for _ in range(20000):
        s=0.0
        for _ in range(300): s+=delta[random.randrange(N)]
        bs.append(s/300)
    bs.sort()
    lo,hi=bs[500],bs[19500]
    pneg=sum(1 for x in bs if x<=0)/len(bs)
    print(f"\n  {label}")
    print(f"    weight chosen on TRAIN : {w}")
    print(f"    DC draw Brier          : {dcb:.5f}")
    print(f"    blended                : {dcb-gain:.5f}")
    print(f"    gain                   : {gain:+.7f}  ({gain/dcb*100:+.3f}%)")
    print(f"    bootstrap 95% CI       : [{lo:+.7f}, {hi:+.7f}]")
    print(f"    P(gain<=0)             : {pneg:.3f}   -> {'ROBUST' if lo>0 else 'not significant'}")
    return delta,w,gain,lo

print("="*80); print("HELD-OUT RE-TEST"); print("="*80)
d1,w1,g1,l1=evaluate(TR1,TE1,"v1 (your spec, original)")
d2,w2,g2,l2=evaluate(TR2,TE2,"v2 (rebuilt: rolling + shrink + hysteresis)")
print("\n"+"="*80)
print(f"  improvement v1 -> v2: {(g2-g1):+.7f} Brier  ({(g2/g1-1)*100 if g1 else 0:+.0f}% larger gain)")

# consistency
print("\n"+"="*80); print("v2 CONSISTENCY"); print("="*80)
sea=defaultdict(list); lgs=defaultdict(list)
for d,(m,sh,sa) in zip(d2,TE2):
    sea[m['season']].append(d); lgs[m['lg']].append(d)
p=t=0
for s in sorted(sea):
    if len(sea[s])<1500: continue
    gg=sum(sea[s])/len(sea[s]); t+=1; p+=(gg>0)
    print(f"    {s}  n={len(sea[s]):6,}  {gg:+.7f}  {'+' if gg>0 else '-'}")
print(f"    {p}/{t} seasons positive")
p2=t2=0
print()
for lg in sorted(lgs,key=lambda k:-len(lgs[k]))[:10]:
    gg=sum(lgs[lg])/len(lgs[lg]); t2+=1; p2+=(gg>0)
    print(f"    {lg:4s} n={len(lgs[lg]):6,}  {gg:+.7f}  {'+' if gg>0 else '-'}")
print(f"    {p2}/{t2} leagues positive")
pickle.dump(dict(weight=w2),open("star_weight.pkl","wb"))
