"""Does the user's star system improve DRAW prediction over the current model?
Fit on TRAIN, judge on held-out TEST. Draw-specific metrics."""
import pickle, math
from collections import defaultdict
data=pickle.load(open("user_stars.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
data.sort(key=lambda x:x[0]['date'])
cut=int(len(data)*0.70); TR,TE=data[:cut],data[cut:]
TRk=[(m,s,t) for m,s,t in TR if K(m) in dc]
TEk=[(m,s,t) for m,s,t in TE if K(m) in dc]
print(f"train {len(TRk):,}  test {len(TEk):,}  (test from {TEk[0][0]['date'].date()})")

# star-only draw rate table, fitted on TRAIN
tab=defaultdict(lambda:[0,0])
for m,sh,sa in TRk:
    t=tab[sh-sa]; t[0]+=1; t[1]+=(m['res']=='D')
glob=sum(1 for m,_,_ in TRk if m['res']=='D')/len(TRk)
def star_draw(g):
    t=tab.get(g)
    return t[1]/t[0] if t and t[0]>=200 else glob

def draw_brier(S,fn):
    return sum((fn(m,sh,sa)-(m['res']=='D'))**2 for m,sh,sa in S)/len(S)
def logloss(S,fn):
    s=0
    for m,sh,sa in S:
        p=min(max(fn(m,sh,sa),1e-9),1-1e-9)
        s-= math.log(p) if m['res']=='D' else math.log(1-p)
    return s/len(S)

f_const=lambda m,sh,sa: glob
f_star =lambda m,sh,sa: star_draw(sh-sa)
f_dc   =lambda m,sh,sa: dc[K(m)][1]

print("\n"+"="*80); print("DRAW PREDICTION — held-out test"); print("="*80)
print(f"  {'system':34s} {'Brier(draw)':>12s} {'LogLoss':>10s}")
for n,f in [("constant "+f"{glob:.1%}",f_const),("stars only (user spec)",f_star),
            ("current model (DC)",f_dc)]:
    print(f"  {n:34s} {draw_brier(TEk,f):12.5f} {logloss(TEk,f):10.5f}")

# blended
print("\n  blends of DC and stars (weight chosen on TRAIN):")
best=(9,0)
for w in [0,.1,.2,.3,.4,.5,.7,1.0]:
    f=lambda m,sh,sa,w=w:(1-w)*dc[K(m)][1]+w*star_draw(sh-sa)
    tr=draw_brier(TRk,f); te=draw_brier(TEk,f)
    if tr<best[0]: best=(tr,w)
    print(f"    w={w:.1f}  TRAIN {tr:.5f}  TEST {te:.5f}"+("  <- best on TRAIN" if w==best[1] else ""))
w=best[1]
fb=lambda m,sh,sa:(1-w)*dc[K(m)][1]+w*star_draw(sh-sa)
d=draw_brier(TEk,f_dc)-draw_brier(TEk,fb)
print(f"\n  chosen w={w}: TEST Brier {draw_brier(TEk,fb):.5f} vs DC {draw_brier(TEk,f_dc):.5f}")
print(f"  gain: {d/draw_brier(TEk,f_dc)*100:+.3f}%  ->", "STARS ADD" if d>1e-6 else "no independent gain")

print("\n"+"="*80); print("IS THE STAR DRAW SIGNAL ALREADY IN THE MODEL?"); print("="*80)
print(f"  {'gap':>5s} {'n':>7s} {'stars say':>10s} {'model says':>11s} {'actual':>8s} {'model err':>10s}")
agg=defaultdict(lambda:[0,0.0,0])
for m,sh,sa in TEk:
    a=agg[sh-sa]; a[0]+=1; a[1]+=dc[K(m)][1]; a[2]+=(m['res']=='D')
for g in sorted(agg):
    n,sp,ac=agg[g]
    if n<200: continue
    print(f"  {g:>+5d} {n:7,} {star_draw(g):10.1%} {sp/n:11.1%} {ac/n:8.1%} {sp/n-ac/n:+10.1%}")
print("\n  if 'model says' already tracks 'actual', the star table is redundant.")
