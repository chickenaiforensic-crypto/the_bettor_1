"""
Test the user's hypothesis DIRECTLY, using match results only. No odds anywhere.
Q: if a team has played at a given ground N times before, does that change the result?
Two versions:
  (a) AWAY team's prior visits to THIS specific stadium  (familiarity with the venue)
  (b) HOME team's tenure at its own ground (how long it has been in this league/ground)
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h

# ---- build visit counters chronologically (strictly prior) ----
visits=defaultdict(int)      # (venue_home_team, visiting_team) -> prior meetings at that ground
ground=defaultdict(int)      # home team -> total prior home matches (tenure proxy)
recs=[]
for m in rows:
    v=visits[(m['home'],m['away'])]
    g=ground[m['home']]
    recs.append((m,v,g))
    visits[(m['home'],m['away'])]+=1
    ground[m['home']]+=1

print("="*94)
print("A. AWAY TEAM'S PRIOR VISITS TO THIS SPECIFIC GROUND")
print("="*94)
print("  Hypothesis: more visits = more familiarity = better away result")
print(f"  {'prior visits':16s} {'n':>9s} {'home W':>9s} {'draw':>8s} {'away W':>9s} {'away PPG':>9s}")
bands=[(0,0),(1,1),(2,2),(3,4),(5,7),(8,11),(12,17),(18,99)]
for lo,hi in bands:
    s=[(m,v,g) for m,v,g in recs if lo<=v<=hi]
    if len(s)<300: continue
    n=len(s)
    h=sum(1 for m,_,_ in s if m['res']=='H'); d=sum(1 for m,_,_ in s if m['res']=='D'); a=n-h-d
    lbl=f"{lo}" if lo==hi else f"{lo}-{hi}" if hi<99 else f"{lo}+"
    print(f"  {lbl:16s} {n:9,} {h/n:9.1%} {d/n:8.1%} {a/n:9.1%} {(3*a+d)/n:9.2f}")

print("\n  CONFOUND WARNING: visit count correlates with league tenure. Teams that meet")
print("  often are both long-established (=stronger than promoted sides). Control needed.")

print("\n"+"="*94)
print("B. SAME, CONTROLLED FOR TEAM STRENGTH (within prior-PPG bands of the away side)")
print("="*94)
# compute prior season-to-date PPG for away team
teampts=defaultdict(lambda:[0,0])  # (lg,season,team)->[pts,games]
ppg_of=[]
for m in rows:
    k1=(m['lg'],m['season'],m['home']); k2=(m['lg'],m['season'],m['away'])
    ph = teampts[k1][0]/teampts[k1][1] if teampts[k1][1]>=5 else None
    pa = teampts[k2][0]/teampts[k2][1] if teampts[k2][1]>=5 else None
    ppg_of.append((ph,pa))
    hp = 3 if m['res']=='H' else (1 if m['res']=='D' else 0)
    ap = 3 if m['res']=='A' else (1 if m['res']=='D' else 0)
    teampts[k1][0]+=hp; teampts[k1][1]+=1
    teampts[k2][0]+=ap; teampts[k2][1]+=1

print(f"  {'away PPG band':16s} {'visits':>10s} {'n':>8s} {'away W':>9s} {'away PPG':>9s}")
for plo,phi in [(0,1.0),(1.0,1.5),(1.5,3.1)]:
    for vlo,vhi in [(0,1),(2,5),(6,99)]:
        s=[(m,v) for (m,v,g),(ph,pa) in zip(recs,ppg_of)
           if pa is not None and plo<=pa<phi and vlo<=v<=vhi]
        if len(s)<300: continue
        n=len(s); a=sum(1 for m,_ in s if m['res']=='A'); d=sum(1 for m,_ in s if m['res']=='D')
        lo_,hi_=wilson(a,n)
        print(f"  [{plo:.1f},{phi:.1f})        {vlo}-{vhi if vhi<99 else '+':<4} {n:8,} {a/n:9.1%} {(3*a+d)/n:9.2f}   CI[{lo_:.1%},{hi_:.1%}]")

print("\n"+"="*94)
print("C. HOME TEAM'S TENURE AT ITS OWN GROUND (prior home matches in dataset)")
print("="*94)
print(f"  {'prior home games':18s} {'n':>9s} {'home W':>9s} {'home PPG':>9s}")
for lo,hi in [(0,9),(10,29),(30,59),(60,119),(120,199),(200,9999)]:
    s=[(m,v,g) for m,v,g in recs if lo<=g<=hi]
    if len(s)<500: continue
    n=len(s); h=sum(1 for m,_,_ in s if m['res']=='H'); d=sum(1 for m,_,_ in s if m['res']=='D')
    print(f"  {str(lo)+'-'+str(hi):18s} {n:9,} {h/n:9.1%} {(3*h+d)/n:9.2f}")
print("  (this mostly measures survivorship: teams that stay up are better)")

print("\n"+"="*94)
print("D. THE CLEAN TEST — REPEAT MEETINGS, SAME PAIR, DOES AWAY IMPROVE OVER TIME?")
print("="*94)
print("  Within each (home,away) pair, compare the away side's result on visit 1-2")
print("  vs visit 6+. Pair fixed => team quality largely held constant.")
pairres=defaultdict(list)
for m,v,g in recs: pairres[(m['home'],m['away'])].append((v,m['res']))
early=[];late=[]
for k,lst in pairres.items():
    if len(lst)<8: continue
    for v,r in lst:
        (early if v<=1 else (late if v>=6 else [])).append(r)
for lbl,s in [("visits 0-1",early),("visits 6+",late)]:
    n=len(s); a=s.count('A'); d=s.count('D')
    lo_,hi_=wilson(a,n)
    print(f"  {lbl:12s} n={n:7,}  away win {a/n:6.1%} CI[{lo_:.1%},{hi_:.1%}]  away PPG {(3*a+d)/n:.2f}")
print("  -> if familiarity mattered, 'visits 6+' would be clearly higher.")
