"""
TEST: do leagues differ in strength, and does ignoring that distort chains?
Method: measure each league's clubs in EUROPEAN matches only (the common arena).
Results only. No coefficients from any external table.
"""
import pickle, math
from collections import defaultdict
import chain as C

# club -> home country (from domestic edges)
ctry={}
for d,comp,ch,h,ca,a,hg,ag in C.EDGES:
    if comp.startswith('DOM:'):
        ctry.setdefault(C.CANON[C.norm(h)],ch)
        ctry.setdefault(C.CANON[C.norm(a)],ca)
# fill from european edges where domestic missing
for d,comp,ch,h,ca,a,hg,ag in C.EDGES:
    if comp.startswith('EUR'):
        ctry.setdefault(C.CANON[C.norm(h)],ch)
        ctry.setdefault(C.CANON[C.norm(a)],ca)

# european performance per country
perf=defaultdict(lambda:[0,0,0])   # played, gf, ga
for d,comp,ch,h,ca,a,hg,ag in C.EDGES:
    if not comp.startswith('EUR'): continue
    H,A=C.CANON[C.norm(h)],C.CANON[C.norm(a)]
    cH,cA=ctry.get(H),ctry.get(A)
    if cH: p=perf[cH]; p[0]+=1; p[1]+=hg; p[2]+=ag
    if cA: p=perf[cA]; p[0]+=1; p[1]+=ag; p[2]+=hg

rows=[(k,v[0],(v[1]-v[2])/v[0]) for k,v in perf.items() if v[0]>=40]
rows.sort(key=lambda r:-r[2])
print("="*74)
print("LEAGUE STRENGTH — measured from EUROPEAN matches only")
print("="*74)
print(f"  {'country':8s} {'euro matches':>13s} {'GD per match':>14s}")
for k,n,gd in rows:
    print(f"  {k:8s} {n:13d} {gd:+14.2f}")
strength={k:gd for k,n,gd in rows}
pickle.dump((strength,ctry),open('league_strength.pkl','wb'))

print()
print("="*74)
print("SPREAD CHECK — is the difference big enough to matter?")
print("="*74)
vals=[r[2] for r in rows]
print(f"  strongest {rows[0][0]} {rows[0][2]:+.2f}  |  weakest {rows[-1][0]} {rows[-1][2]:+.2f}")
print(f"  range {max(vals)-min(vals):.2f} goals per match across leagues")
print(f"  sd {(sum((v-sum(vals)/len(vals))**2 for v in vals)/len(vals))**0.5:.2f}")
