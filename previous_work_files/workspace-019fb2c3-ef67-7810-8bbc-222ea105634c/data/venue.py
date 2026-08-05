"""
Q1: when a team wins at home, how often do they win/lose away?
Q2: what is the state of teams that win BOTH home and away?

DESIGN RULES (learned from Gate 1):
 - every conditioning variable uses STRICTLY PRIOR matches only
 - every result reported with n and Wilson CI
 - every result compared to (a) unconditional base rate AND (b) closing market price
 - no single season or league may drive a conclusion
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h,c+h
def fmt(k,n):
    if n==0: return "     n=0"
    lo,hi=wilson(k,n); return f"{k/n:6.1%} [{lo:.1%},{hi:.1%}] n={n:,}"

# ---- build per-team chronological match list within each league-season ----
teamseq=defaultdict(list)   # (lg,season,team) -> list of (date, venue, res_for_team, match)
for m in rows:
    teamseq[(m['lg'],m['season'],m['home'])].append((m['date'],'H','W' if m['res']=='H' else ('D' if m['res']=='D' else 'L'),m))
    teamseq[(m['lg'],m['season'],m['away'])].append((m['date'],'A','W' if m['res']=='A' else ('D' if m['res']=='D' else 'L'),m))
for k in teamseq: teamseq[k].sort(key=lambda x:x[0])

print("="*92)
print("BASELINE — unconditional rates across 153,058 matches")
print("="*92)
H=sum(1 for m in rows if m['res']=='H'); D=sum(1 for m in rows if m['res']=='D'); A=len(rows)-H-D
print(f"  Home win {H/len(rows):.1%} | Draw {D/len(rows):.1%} | Away win {A/len(rows):.1%}")
# per-team-match view
allm=[(v,r) for k in teamseq for (_,v,r,_) in teamseq[k]]
hw=[r for v,r in allm if v=='H']; aw=[r for v,r in allm if v=='A']
print(f"  From team perspective — at HOME: W {hw.count('W')/len(hw):.1%} D {hw.count('D')/len(hw):.1%} L {hw.count('L')/len(hw):.1%}")
print(f"                          AWAY: W {aw.count('W')/len(aw):.1%} D {aw.count('D')/len(aw):.1%} L {aw.count('L')/len(aw):.1%}")

print()
print("="*92)
print("Q1. AFTER A HOME WIN, WHAT HAPPENS IN THE TEAM'S NEXT AWAY MATCH?")
print("="*92)
print("  (next away fixture chronologically after that home result, same season)")
buckets=defaultdict(lambda:[0,0,0])   # prior home result -> [W,D,L] in next away match
for k,seq in teamseq.items():
    for i,(dt,v,res,m) in enumerate(seq):
        if v!='H': continue
        nxt=next(((d2,v2,r2,m2) for (d2,v2,r2,m2) in seq[i+1:] if v2=='A'), None)
        if not nxt: continue
        b=buckets[res]; b[{'W':0,'D':1,'L':2}[nxt[2]]]+=1
print(f"  {'prior HOME result':20s} {'next AWAY: W':>28s} {'D':>28s} {'L':>28s}")
for pr in ['W','D','L']:
    w,d,l=buckets[pr]; n=w+d+l
    print(f"  {('home '+pr):20s} {fmt(w,n):>28s} {fmt(d,n):>28s} {fmt(l,n):>28s}")
tw=sum(buckets[p][0] for p in 'WDL'); tn=sum(sum(buckets[p]) for p in 'WDL')
print(f"  {'ALL':20s} {fmt(tw,tn):>28s}")

print()
print("="*92)
print("Q1b. SAME, BUT CONDITIONING ON A RUN OF PRIOR HOME RESULTS")
print("="*92)
runb=defaultdict(lambda:[0,0,0])
for k,seq in teamseq.items():
    homes=[(i,x) for i,x in enumerate(seq) if x[1]=='H']
    for j in range(len(homes)):
        # last up-to-3 home results ending at homes[j]
        last3=[homes[t][1][2] for t in range(max(0,j-2),j+1)]
        if len(last3)<3: continue
        i=homes[j][0]
        nxt=next(((d2,v2,r2,m2) for (d2,v2,r2,m2) in seq[i+1:] if v2=='A'), None)
        if not nxt: continue
        key='WWW' if last3==['W','W','W'] else ('LLL' if last3==['L','L','L'] else ('2W+' if last3.count('W')>=2 else 'other'))
        runb[key][{'W':0,'D':1,'L':2}[nxt[2]]]+=1
for key in ['WWW','2W+','other','LLL']:
    w,d,l=runb[key]; n=w+d+l
    if n: print(f"  last 3 home = {key:6s} -> next away  W {fmt(w,n)}   L {fmt(l,n)}")

print()
print("="*92)
print("Q2. TEAMS THAT WIN BOTH HOME AND AWAY — how strong, and is it predictive?")
print("="*92)
print("  Definition: using ONLY matches before a cutoff, classify each team by whether it has")
print("  won >=1 home AND >=1 away in its prior matches, then measure its FUTURE results.")
print()
# rolling: at each match, look at team's prior form split by venue
cat_next=defaultdict(lambda:[0,0,0])   # category -> next-match [W,D,L]
cat_ppg=defaultdict(list)
MINP=6
for k,seq in teamseq.items():
    for i in range(len(seq)):
        prior=seq[:i]
        if len(prior)<MINP: continue
        ph=[r for (_,v,r,_) in prior if v=='H']; pa=[r for (_,v,r,_) in prior if v=='A']
        if len(ph)<3 or len(pa)<3: continue
        wh='W' in ph; wa='W' in pa
        cat = 'BOTH (won H & A)' if (wh and wa) else ('HOME ONLY' if wh else ('AWAY ONLY' if wa else 'NEITHER'))
        res=seq[i][2]
        cat_next[cat][{'W':0,'D':1,'L':2}[res]]+=1
        cat_ppg[cat].append(3 if res=='W' else (1 if res=='D' else 0))
print(f"  {'prior-form category':20s} {'NEXT match W':>28s} {'D':>28s} {'L':>28s} {'PPG':>6}")
for c in ['BOTH (won H & A)','HOME ONLY','AWAY ONLY','NEITHER']:
    w,d,l=cat_next[c]; n=w+d+l
    if not n: continue
    print(f"  {c:20s} {fmt(w,n):>28s} {fmt(d,n):>28s} {fmt(l,n):>28s} {sum(cat_ppg[c])/n:6.2f}")
pickle.dump(dict(teamseq),open("teamseq.pkl","wb"))
