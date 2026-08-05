"""
AUDIT OF THE SHIPPED STAR CATEGORISATION — structure, not outcomes.
What exactly did I build? Is the category system defensible?
"""
import pickle, json, math
from collections import defaultdict
st=pickle.load(open("model_state.pkl","rb"))
cut=json.load(open("star_cutoffs.json"))
rows=pickle.load(open("all_matches.pkl","rb"))

active=set()
for m in rows:
    if m['season'] in ('2425','2526'):
        active.add((m['lg'],m['home'])); active.add((m['lg'],m['away']))

print("="*90)
print("1. WHAT THE SHIPPED SYSTEM ACTUALLY IS")
print("="*90)
print("""  starsFor(lg,team):
      v = att[team] + dfn[team]          <-- EQUAL-WEIGHTED composite
      stars = 1 + count(cutoffs[lg] <= v)  where cutoffs = per-league quintiles
  Cutoffs frozen at build time from teams active in 2024/25-2025/26.""")

print("\n"+"="*90)
print("2. FLAW #1 — att+dfn COLLAPSES TWO DIMENSIONS INTO ONE")
print("="*90)
print("  Goal difference depends on the INTERACTION (home att vs away dfn),")
print("  not on a team's own att+dfn total. Same star, very different profile:")
byl=defaultdict(list)
for lg,t in active:
    if t in st['att']: byl[lg].append((t,st['att'][t],st['dfn'][t]))
def stars(lg,a,d):
    v=a+d; c=cut.get(lg)
    return 1+sum(1 for x in c if v>=x)
ex=[]
for t,a,d in byl['E0']:
    ex.append((stars('E0',a,d),t,a,d,a-d))
ex.sort()
print(f"  {'star':>5s} {'team':22s} {'att':>7s} {'dfn':>7s} {'att-dfn':>8s} {'sum':>7s}")
for s,t,a,d,sp in ex:
    print(f"  {s:>5d} {t:22s} {a:7.3f} {d:7.3f} {sp:+8.3f} {a+d:7.3f}")

print("\n  SAME-STAR PAIRS WITH OPPOSITE PROFILES (all leagues):")
worst=[]
grp=defaultdict(list)
for lg,v in byl.items():
    for t,a,d in v: grp[(lg,stars(lg,a,d))].append((t,a,d))
for (lg,s),v in grp.items():
    if len(v)<2: continue
    v2=sorted(v,key=lambda x:x[1]-x[2])
    lo,hi=v2[0],v2[-1]
    spread=(hi[1]-hi[2])-(lo[1]-lo[2])
    worst.append((spread,lg,s,lo,hi))
worst.sort(reverse=True)
print(f"  {'lg':4s} {'star':>4s} {'attack-heavy team':22s} {'att-dfn':>8s}  {'defence-heavy team':22s} {'att-dfn':>8s}")
for spread,lg,s,lo,hi in worst[:6]:
    print(f"  {lg:4s} {s:>4d} {hi[0]:22s} {hi[1]-hi[2]:+8.3f}  {lo[0]:22s} {lo[1]-lo[2]:+8.3f}")
print("  -> two teams share a star yet differ by >1.0 in attack/defence balance.")
print("     For a GOAL-DIFFERENCE system this is the central defect.")

print("\n"+"="*90)
print("3. FLAW #2 — CUTOFFS ARE FROZEN AND WERE SET FROM FINAL RATINGS")
print("="*90)
print("  Cutoffs were computed once, from ratings at the END of the dataset.")
print("  Consequences:")
print("   (a) any backtest using them is contaminated (look-ahead).")
print("   (b) as sync updates ratings, teams drift across FIXED boundaries, so the")
print("       1/5 distribution will skew over time instead of staying quintiles.")
print(f"\n  {'league':22s} {'cutoffs (q20,q40,q60,q80)':>44s}")
for lg in ['E0','SP1','D1','G1','E3']:
    print(f"  {lg:22s} {str([round(x,3) for x in cut[lg]]):>44s}")
sp=[max(cut[lg])-min(cut[lg]) for lg in cut]
print(f"\n  cutoff spread varies by league: {min(sp):.3f} to {max(sp):.3f}")
print("  -> a 5-star in one league is NOT a 5-star in another. Ranks are")
print("     league-relative only. Fine within a fixture; meaningless across.")

print("\n"+"="*90)
print("4. FLAW #3 — BOUNDARY FRAGILITY")
print("="*90)
near=0; tot=0
for lg,v in byl.items():
    c=cut[lg]
    for t,a,d in v:
        tot+=1
        val=a+d
        if min(abs(val-x) for x in c)<0.05: near+=1
print(f"  teams within 0.05 of a cutoff: {near}/{tot} = {near/tot:.1%}")
print("  A single match can move att+dfn by ~0.05, so that share of teams can")
print("  flip category week to week. Categories are not stable at the edges.")
