"""Is the +0.041% draw gain real or noise? Bootstrap, per-era, per-league."""
import pickle, math, random
from collections import defaultdict
data=pickle.load(open("user_stars.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
data.sort(key=lambda x:x[0]['date'])
cut=int(len(data)*0.70)
TR=[(m,s,t) for m,s,t in data[:cut] if K(m) in dc]
TE=[(m,s,t) for m,s,t in data[cut:] if K(m) in dc]
tab=defaultdict(lambda:[0,0])
for m,sh,sa in TR:
    t=tab[sh-sa]; t[0]+=1; t[1]+=(m['res']=='D')
glob=sum(1 for m,_,_ in TR if m['res']=='D')/len(TR)
sd=lambda g:(tab[g][1]/tab[g][0]) if tab.get(g) and tab[g][0]>=200 else glob
W=0.2
def diff(S):
    a=sum((dc[K(m)][1]-(m['res']=='D'))**2 for m,_,_ in S)/len(S)
    b=sum((((1-W)*dc[K(m)][1]+W*sd(sh-sa))-(m['res']=='D'))**2 for m,sh,sa in S)/len(S)
    return a-b

print("="*74); print("IS THE DRAW GAIN ROBUST?"); print("="*74)
base=diff(TE)
print(f"  overall test gain: {base:+.7f} Brier ({base/0.19163*100:+.3f}%)")
random.seed(11)
bs=[]
for _ in range(4000):
    S=[random.choice(TE) for _ in range(len(TE))]
    bs.append(diff(S))
bs.sort()
lo,hi=bs[100],bs[3900]
print(f"  bootstrap 95% CI: [{lo:+.7f}, {hi:+.7f}]")
print(f"  P(gain <= 0) = {sum(1 for x in bs if x<=0)/len(bs):.3f}")
print(f"  -> {'ROBUST' if lo>0 else 'NOT DISTINGUISHABLE FROM ZERO'}")

print("\n  by season:")
sea=defaultdict(list)
for r in TE: sea[r[0]['season']].append(r)
pos=0;tot=0
for s in sorted(sea):
    if len(sea[s])<1500: continue
    d=diff(sea[s]); tot+=1; pos+=(d>0)
    print(f"    {s}  n={len(sea[s]):6,}  gain {d:+.7f}")
print(f"    {pos}/{tot} seasons positive")

print("\n  by league (top 8 by volume):")
lgs=defaultdict(list)
for r in TE: lgs[r[0]['lg']].append(r)
p2=0;t2=0
for lg in sorted(lgs,key=lambda k:-len(lgs[k]))[:8]:
    if len(lgs[lg])<1200: continue
    d=diff(lgs[lg]); t2+=1; p2+=(d>0)
    print(f"    {lg:4s} n={len(lgs[lg]):6,}  gain {d:+.7f}")
print(f"    {p2}/{t2} leagues positive")

print("\n"+"="*74); print("PRACTICAL SIZE"); print("="*74)
print(f"  Brier improvement: {base/0.19163*100:+.3f}%")
print(f"  For comparison, the model beats a constant draw rate by "
      f"{(0.19336-0.19163)/0.19336*100:.2f}%")
print(f"  So stars recover roughly {base/(0.19336-0.19163)*100:.0f}% as much again on top.")
