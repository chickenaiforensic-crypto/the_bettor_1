"""
User asks: am I forcing the stats with a lean expectation?
Test my own claim symmetrically. If 3rd phase is genuinely weak, it must be
weak in BOTH directions and weak on FRESH data too - not just where I said so.
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
def corr(x,y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    a=sum((p-mx)*(q-my) for p,q in zip(x,y))
    b=math.sqrt(sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))
    return a/b if b else 0

hist=defaultdict(lambda: defaultdict(list))
out=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    H=hist[(lg,se,h)]; A=hist[(lg,se,a)]
    if len(H)>=5 and len(A)>=5:
        shared=(set(H)&set(A))-{h,a}
        p2=None
        if shared:
            p2=(sum(sum(H[o])/len(H[o]) for o in shared)/len(shared)
               -sum(sum(A[o])/len(A[o]) for o in shared)/len(shared))
        oppH=set(H)-shared; oppA=set(A)-shared
        secH=defaultdict(list); secA=defaultdict(list)
        for o in oppH:
            for o2,v in hist[(lg,se,o)].items():
                if o2 in (h,a) or o2 in oppH: continue
                secH[o2].append(sum(H[o])/len(H[o])+sum(v)/len(v))
        for o in oppA:
            for o2,v in hist[(lg,se,o)].items():
                if o2 in (h,a) or o2 in oppA: continue
                secA[o2].append(sum(A[o])/len(A[o])+sum(v)/len(v))
        c2=set(secH)&set(secA)
        p3=None
        if c2:
            p3=(sum(sum(secH[o])/len(secH[o]) for o in c2)/len(c2)
               -sum(sum(secA[o])/len(secA[o]) for o in c2)/len(c2))
        out.append((m,p2,p3,len(shared),len(c2)))
    gd=m['hg']-m['ag']
    hist[(lg,se,h)][a].append(gd); hist[(lg,se,a)][h].append(-gd)

gd=[m['hg']-m['ag'] for m,_,_,_,_ in out]
print("="*86)
print("SYMMETRY TEST — is the 3rd phase weak in BOTH directions?")
print("="*86)
for lbl,f in [("all fixtures",lambda o:True),
              ("home side favoured by 3rd",lambda o:o[2] is not None and o[2]>0),
              ("away side favoured by 3rd",lambda o:o[2] is not None and o[2]<0)]:
    v=[(o[2],g) for o,g in zip(out,gd) if o[2] is not None and f(o)]
    if len(v)<500: continue
    print(f"  {lbl:30s} n={len(v):7,}  r={corr([x for x,_ in v],[y for _,y in v]):+.4f}")

print("\n"+"="*86)
print("DOES MORE DATA RESCUE IT? (r by number of connectors)")
print("="*86)
print(f"  {'connectors':>14s} {'n':>8s} {'2nd phase r':>13s} {'3rd phase r':>13s}")
for lo,hi in [(1,4),(5,9),(10,14),(15,19),(20,99)]:
    v3=[(o[2],g) for o,g in zip(out,gd) if o[2] is not None and lo<=o[4]<=hi]
    v2=[(o[1],g) for o,g in zip(out,gd) if o[1] is not None and lo<=o[3]<=hi]
    if len(v3)<500: continue
    r3=corr([x for x,_ in v3],[y for _,y in v3])
    r2=corr([x for x,_ in v2],[y for _,y in v2]) if len(v2)>500 else float('nan')
    print(f"  {str(lo)+'-'+str(hi):>14s} {len(v3):8,} {r2:+13.4f} {r3:+13.4f}")
print("  -> if 3rd phase improved with more connectors, it would be a sample-size issue.")

print("\n"+"="*86)
print("BEST CASE FOR THE 3RD PHASE — where it should be strongest")
print("="*86)
v=[(o[2],g) for o,g in zip(out,gd) if o[2] is not None and o[1] is None]
if len(v)>200:
    print(f"  when NO direct common opponents exist: n={len(v):,} r={corr([x for x,_ in v],[y for _,y in v]):+.4f}")
else:
    print(f"  when NO direct common opponents exist: only n={len(v)} cases in league play")
    print("  (in a league everyone shares opponents - the 3rd phase is never NEEDED)")
