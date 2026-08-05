"""
v2 rebuild improved STRUCTURE but not prediction. However both v1 and v2 show
the same pattern: lower divisions positive, top divisions negative.
Test that split HONESTLY — decide the rule on TRAIN, verify on TEST.
"""
import pickle, math, random
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
dat=sorted([(m,s,t) for m,s,t in v2 if K(m) in dc],key=lambda x:x[0]['date'])
c=int(len(dat)*0.70); TR,TE=dat[:c],dat[c:]

t=defaultdict(lambda:[0,0])
for m,sh,sa in TR:
    x=t[sh-sa]; x[0]+=1; x[1]+=(m['res']=='D')
G=sum(1 for m,_,_ in TR if m['res']=='D')/len(TR)
sd=lambda k:(t[k][1]/t[k][0]) if t.get(k) and t[k][0]>=200 else G
W=0.25

def delta_of(S):
    out=[]
    for m,sh,sa in S:
        y=1.0 if m['res']=='D' else 0.0
        p=dc[K(m)][1]; b=(1-W)*p+W*sd(sh-sa)
        out.append((p-y)**2-(b-y)**2)
    return out

print("="*78)
print("STEP 1 — WHICH LEAGUES HELP? decided on TRAIN ONLY")
print("="*78)
trl=defaultdict(list)
for d,(m,_,_) in zip(delta_of(TR),TR): trl[m['lg']].append(d)
good=[]
print(f"  {'lg':5s} {'n(train)':>9s} {'train gain':>13s} {'use?':>6s}")
for lg in sorted(trl,key=lambda k:-len(trl[k])):
    g=sum(trl[lg])/len(trl[lg])
    use = g>0 and len(trl[lg])>=2000
    if use: good.append(lg)
    print(f"  {lg:5s} {len(trl[lg]):9,} {g:+13.7f} {'YES' if use else '':>6s}")
print(f"\n  selected on TRAIN: {sorted(good)}")

print("\n"+"="*78)
print("STEP 2 — APPLY THAT SELECTION TO TEST (never used in the choice)")
print("="*78)
sub=[(m,sh,sa) for m,sh,sa in TE if m['lg'] in good]
d=delta_of(sub); N=len(d); gain=sum(d)/N
dcb=sum((dc[K(m)][1]-(1.0 if m['res']=='D' else 0.0))**2 for m,_,_ in sub)/N
random.seed(9)
bs=[]
for _ in range(20000):
    s=0.0
    for _ in range(300): s+=d[random.randrange(N)]
    bs.append(s/300)
bs.sort(); lo,hi=bs[500],bs[19500]
print(f"  test n                : {N:,}")
print(f"  DC draw Brier         : {dcb:.5f}")
print(f"  blended               : {dcb-gain:.5f}")
print(f"  gain                  : {gain:+.7f}  ({gain/dcb*100:+.3f}%)")
print(f"  bootstrap 95% CI      : [{lo:+.7f}, {hi:+.7f}]")
print(f"  P(gain<=0)            : {sum(1 for x in bs if x<=0)/len(bs):.3f}")
print(f"  -> {'ROBUST' if lo>0 else 'STILL NOT SIGNIFICANT'}")

print("\n  per-league on TEST:")
tel=defaultdict(list)
for x,(m,_,_) in zip(d,sub): tel[m['lg']].append(x)
p=n=0
for lg in sorted(tel,key=lambda k:-len(tel[k])):
    g=sum(tel[lg])/len(tel[lg]); n+=1; p+=(g>0)
    print(f"    {lg:5s} n={len(tel[lg]):6,} {g:+.7f} {'+' if g>0 else '-'}")
print(f"    {p}/{n} held up out of sample")

print("\n"+"="*78)
print("STEP 3 — HOW BIG IS THIS IN PRACTICE?")
print("="*78)
print(f"  A {gain/dcb*100:+.3f}% Brier change on draw prediction means, over 1,000 matches,")
print(f"  the draw probability is on average {abs(gain)**0.5*100:.2f}pt closer to reality.")
print("  That is real but small. It will not change a tier or flip a call.")
