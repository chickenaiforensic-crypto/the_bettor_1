"""Fast version: precompute per-match Brier deltas, then bootstrap over those."""
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

# precompute delta per match: (DC error) - (blend error). positive = stars help
delta=[]; meta=[]
for m,sh,sa in TE:
    y=1.0 if m['res']=='D' else 0.0
    p_dc=dc[K(m)][1]
    p_bl=(1-W)*p_dc + W*sd(sh-sa)
    delta.append((p_dc-y)**2 - (p_bl-y)**2)
    meta.append((m['season'],m['lg']))
N=len(delta); base=sum(delta)/N
dc_brier=sum((dc[K(m)][1]-(1.0 if m['res']=='D' else 0.0))**2 for m,_,_ in TE)/N

print("="*72); print("IS THE DRAW GAIN ROBUST?"); print("="*72)
print(f"  test n = {N:,}")
print(f"  overall gain: {base:+.7f} Brier  ({base/dc_brier*100:+.3f}%)")

random.seed(11)
bs=[]
for _ in range(20000):
    s=0.0
    for _ in range(200):            # 200-block bootstrap for speed
        s+=delta[random.randrange(N)]
    bs.append(s/200)
bs.sort()
lo,hi=bs[500],bs[19500]
print(f"  bootstrap 95% CI: [{lo:+.7f}, {hi:+.7f}]")
print(f"  P(gain <= 0) = {sum(1 for x in bs if x<=0)/len(bs):.3f}")
print(f"  -> {'ROBUST' if lo>0 else 'NOT DISTINGUISHABLE FROM ZERO'}")

print("\n  by season:")
sea=defaultdict(list)
for d,(s,l) in zip(delta,meta): sea[s].append(d)
pos=tot=0
for s in sorted(sea):
    if len(sea[s])<1500: continue
    g=sum(sea[s])/len(sea[s]); tot+=1; pos+=(g>0)
    print(f"    {s}  n={len(sea[s]):6,}  gain {g:+.7f}  {'+' if g>0 else '-'}")
print(f"    {pos}/{tot} seasons positive")

print("\n  by league (top 8 by volume):")
lgs=defaultdict(list)
for d,(s,l) in zip(delta,meta): lgs[l].append(d)
p2=t2=0
for lg in sorted(lgs,key=lambda k:-len(lgs[k]))[:8]:
    g=sum(lgs[lg])/len(lgs[lg]); t2+=1; p2+=(g>0)
    print(f"    {lg:4s} n={len(lgs[lg]):6,}  gain {g:+.7f}  {'+' if g>0 else '-'}")
print(f"    {p2}/{t2} leagues positive")

print("\n"+"="*72); print("PRACTICAL SIZE"); print("="*72)
const=0.19336
print(f"  constant-rate draw Brier : {const:.5f}")
print(f"  model (DC) draw Brier    : {dc_brier:.5f}   ({(const-dc_brier)/const*100:+.2f}% vs constant)")
print(f"  model + stars            : {dc_brier-base:.5f}   ({base/dc_brier*100:+.3f}% vs model)")
print(f"  stars add ~{base/(const-dc_brier)*100:.0f}% as much again on top of the model's own draw edge.")
