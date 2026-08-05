"""Stress-test the only positive cell: short-priced home favourites.
Gate-1 discipline: split by league, by era, walk-forward, and bootstrap."""
import pickle, math, random
from collections import defaultdict
elig=pickle.load(open("elig.pkl","rb"))
random.seed(7)
def devig(oh,od,oa):
    t=1/oh+1/od+1/oa; return (1/oh)/t,(1/od)/t,(1/oa)/t
def stats_(sub):
    n=len(sub); w=sum(1 for m,_,_ in sub if m['res']=='H')
    act=w/n; mk=sum(devig(m['oh'],m['od'],m['oa'])[0] for m,_,_ in sub)/n
    roi=sum((m['oh']-1) if m['res']=='H' else -1 for m,_,_ in sub)/n
    return n,act,mk,act-mk,roi
def boot(sub,B=20000):
    r=[]
    for _ in range(B):
        s=[random.choice(sub) for _ in sub]
        r.append(sum((m['oh']-1) if m['res']=='H' else -1 for m,_,_ in s)/len(s))
    r.sort(); return r[int(.025*B)],r[int(.975*B)]

fav=[x for x in elig if x[0]['oh']<1.5]
print("="*96); print("SHORT-PRICED HOME FAVOURITES (odds < 1.50) — full stress test"); print("="*96)
n,act,mk,edge,roi=stats_(fav)
lo,hi=boot(fav)
print(f"  ALL: n={n:,}  actual {act:.1%}  market {mk:.1%}  edge {edge:+.1%}  ROI {roi:+.2%}  boot95 [{lo:+.2%},{hi:+.2%}]")

print("\n  BY LEAGUE (must be consistent, not driven by one):")
byl=defaultdict(list)
for x in fav: byl[x[0]['lg']].append(x)
pos=0;tot=0
for lg in sorted(byl,key=lambda k:-len(byl[k])):
    s=byl[lg]
    if len(s)<400: continue
    n,act,mk,edge,roi=stats_(s); tot+=1; pos+= (roi>0)
    print(f"    {lg:4s} n={n:6,} act {act:6.1%} mkt {mk:6.1%} edge {edge:+6.1%} ROI {roi:+6.2%}")
print(f"    -> {pos}/{tot} leagues positive ROI")

print("\n  BY ERA (is it decaying as markets sharpen?):")
for a,b in [('0304','0910'),('1011','1516'),('1617','2021'),('2122','2526')]:
    s=[x for x in fav if a<=x[0]['season']<=b]
    if len(s)<500: continue
    n,act,mk,edge,roi=stats_(s)
    print(f"    {a}-{b}: n={n:6,} act {act:6.1%} mkt {mk:6.1%} edge {edge:+6.1%} ROI {roi:+6.2%}")

print("\n  BY PRICE (where exactly?):")
for lo_,hi_ in [(1.0,1.15),(1.15,1.25),(1.25,1.35),(1.35,1.5)]:
    s=[x for x in elig if lo_<=x[0]['oh']<hi_]
    if len(s)<300: continue
    n,act,mk,edge,roi=stats_(s)
    print(f"    [{lo_:.2f},{hi_:.2f}) n={n:6,} act {act:6.1%} mkt {mk:6.1%} edge {edge:+6.1%} ROI {roi:+6.2%}")

print("\n  Does 'won both H&A' ADD anything on top of just being a short favourite?")
for lbl,s in [("fav & home BOTH",[x for x in fav if x[1]['wh'] and x[1]['wa']]),
              ("fav & home NOT both",[x for x in fav if not(x[1]['wh'] and x[1]['wa'])])]:
    if len(s)<200: print(f"    {lbl}: n={len(s)} too small"); continue
    n,act,mk,edge,roi=stats_(s)
    print(f"    {lbl:22s} n={n:6,} edge {edge:+6.1%} ROI {roi:+6.2%}")

print("\n  WALK-FORWARD (bet fav<1.5 in season t only if profitable in all prior seasons):")
seasons=sorted(set(x[0]['season'] for x in elig))
tn=0;tp=0.0
for i in range(6,len(seasons)):
    tr=[x for x in fav if x[0]['season']<seasons[i]]
    te=[x for x in fav if x[0]['season']==seasons[i]]
    if len(tr)<1000 or not te: continue
    trroi=sum((m['oh']-1) if m['res']=='H' else -1 for m,_,_ in tr)/len(tr)
    if trroi<=0: continue
    p=sum((m['oh']-1) if m['res']=='H' else -1 for m,_,_ in te)
    tn+=len(te); tp+=p
if tn: print(f"    n={tn:,} bets  ROI {tp/tn:+.2%}")

print("\n"+"="*96); print("CONTEXT: favourite-longshot bias across the WHOLE price curve"); print("="*96)
print("  (this is a known, documented market bias — not a new discovery)")
print(f"  {'home price':16s} {'n':>8s} {'actual':>8s} {'market':>8s} {'edge':>8s} {'ROI':>8s}")
for lo_,hi_ in [(1.0,1.3),(1.3,1.5),(1.5,2.0),(2.0,3.0),(3.0,5.0),(5.0,10),(10,100)]:
    s=[x for x in elig if lo_<=x[0]['oh']<hi_]
    if len(s)<200: continue
    n,act,mk,edge,roi=stats_(s)
    print(f"  [{lo_:5.1f},{hi_:5.1f})  {n:8,} {act:8.1%} {mk:8.1%} {edge:+8.1%} {roi:+8.2%}")
