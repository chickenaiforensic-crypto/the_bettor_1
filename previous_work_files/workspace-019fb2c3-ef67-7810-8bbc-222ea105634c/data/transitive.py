"""
DOES TRANSITIVE STRENGTH ACTUALLY PREDICT?
Test inside one league (where we have ground truth and thousands of matches):
  - 2nd phase: direct common opponents
  - 3rd phase: opponents-of-opponents
Compare each against the actual result. If the 3rd phase is weak HERE,
it will be far weaker across a noisy 3-hop European chain.
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

# build per-season opponent results, prior-only
hist=defaultdict(lambda: defaultdict(list))   # (lg,se,team) -> opp -> [gd,...]
out=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    H=hist[(lg,se,h)]; A=hist[(lg,se,a)]
    if len(H)>=5 and len(A)>=5:
        # 2nd phase: direct shared opponents
        shared=set(H)&set(A)
        shared.discard(h); shared.discard(a)
        p2=None
        if shared:
            dh=sum(sum(H[o])/len(H[o]) for o in shared)/len(shared)
            da=sum(sum(A[o])/len(A[o]) for o in shared)/len(shared)
            p2=dh-da
        # 3rd phase: opponents-of-opponents (exclude direct shared)
        oppH=set(H)-shared; oppA=set(A)-shared
        secH=defaultdict(list); secA=defaultdict(list)
        for o in oppH:
            for o2,v in hist[(lg,se,o)].items():
                if o2 in (h,a) or o2 in oppH: continue
                secH[o2].append(sum(H[o])/len(H[o]) + sum(v)/len(v))
        for o in oppA:
            for o2,v in hist[(lg,se,o)].items():
                if o2 in (h,a) or o2 in oppA: continue
                secA[o2].append(sum(A[o])/len(A[o]) + sum(v)/len(v))
        common2=set(secH)&set(secA)
        p3=None
        if common2:
            p3=(sum(sum(secH[o])/len(secH[o]) for o in common2)/len(common2)
              - sum(sum(secA[o])/len(secA[o]) for o in common2)/len(common2))
        # simple direct form for comparison
        fh=sum(sum(v)/len(v) for v in H.values())/len(H)
        fa=sum(sum(v)/len(v) for v in A.values())/len(A)
        out.append((m, p2, p3, fh-fa, len(shared), len(common2)))
    gd=m['hg']-m['ag']
    hist[(lg,se,h)][a].append(gd)
    hist[(lg,se,a)][h].append(-gd)

print(f"fixtures analysed: {len(out):,}")
gd=[m['hg']-m['ag'] for m,_,_,_,_,_ in out]
print(f"\n{'signal':34s} {'n':>8s} {'r with actual GD':>18s}")
for lbl,i in [("direct form (1st phase)",3),("common opponents (2nd phase)",1),
              ("opponents-of-opponents (3rd)",2)]:
    v=[(o[i],g) for o,g in zip(out,gd) if o[i] is not None]
    if len(v)<500: print(f"  {lbl:32s} {len(v):8,} insufficient"); continue
    print(f"  {lbl:32s} {len(v):8,} {corr([x for x,_ in v],[y for _,y in v]):+18.4f}")

print(f"\n  mean direct shared opponents: {sum(o[4] for o in out)/len(out):.1f}")
print(f"  mean 2nd-degree connectors  : {sum(o[5] for o in out)/len(out):.1f}")

# does 3rd phase ADD over 2nd?
both=[(o[1],o[2],g) for o,g in zip(out,gd) if o[1] is not None and o[2] is not None]
print(f"\n  fixtures with BOTH signals: {len(both):,}")
if len(both)>500:
    p2=[x[0] for x in both]; p3=[x[1] for x in both]; y=[x[2] for x in both]
    print(f"  corr(2nd phase, 3rd phase) = {corr(p2,p3):+.4f}  <- overlap")
    print(f"  2nd alone r={corr(p2,y):+.4f} | 3rd alone r={corr(p3,y):+.4f}")
    # residual of 3rd after removing 2nd
    mx=sum(p2)/len(p2); my=sum(p3)/len(p3)
    b=sum((a-mx)*(c-my) for a,c in zip(p2,p3))/sum((a-mx)**2 for a in p2)
    resid=[c-(my+b*(a-mx)) for a,c in zip(p2,p3)]
    print(f"  3rd-phase residual (after 2nd) r with GD = {corr(resid,y):+.4f}")
