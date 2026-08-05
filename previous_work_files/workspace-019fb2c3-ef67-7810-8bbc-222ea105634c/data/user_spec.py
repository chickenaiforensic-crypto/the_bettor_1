"""
USER SPECIFICATION — build and test exactly as instructed.
  - Rank teams by games played and games won/drawn (our own metric, no external ranking)
  - Minimum 5 games to enter the ranking
  - Stars = goal-determining categorisation
  - Same star plain => expected equality => raised draw odds
Everything computed from match results only, strictly prior to each fixture.
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
MIN_GAMES=5

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h

# rolling record: played / won / drawn / lost — prior only
rec=defaultdict(lambda:{'p':0,'w':0,'d':0,'l':0})
fixtures=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    H,A=rec[(lg,se,h)],rec[(lg,se,a)]
    # peer pool: everyone in this league-season with >= MIN_GAMES so far
    peers=[v for k,v in rec.items() if k[0]==lg and k[1]==se and v['p']>=MIN_GAMES]
    fixtures.append((m,dict(H),dict(A),[dict(x) for x in peers]))
    hp = 'w' if m['res']=='H' else ('d' if m['res']=='D' else 'l')
    ap = 'w' if m['res']=='A' else ('d' if m['res']=='D' else 'l')
    H['p']+=1; H[hp]+=1
    A['p']+=1; A[ap]+=1

def ppg(d):
    """user's metric: games won/drawn measured against games played"""
    if d['p']<MIN_GAMES: return None
    return (3*d['w'] + d['d'])/d['p']

def star(v,peers):
    pv=[ppg(x) for x in peers]; pv=[x for x in pv if x is not None]
    if v is None or len(pv)<8: return None
    below=sum(1 for x in pv if x<v)
    return min(5,max(1,int(below/len(pv)*5)+1))

data=[]
for m,H,A,peers in fixtures:
    sh,sa=star(ppg(H),peers),star(ppg(A),peers)
    if sh is None or sa is None: continue
    data.append((m,sh,sa))
print(f"rated fixtures (both teams >= {MIN_GAMES} games): {len(data):,}")

print("\n"+"="*92)
print("THE CORE CLAIM — same star plain => equality => higher draw odds")
print("="*92)
print(f"  {'matchup':14s} {'n':>8s} {'draw%':>8s} {'95% CI':>16s} {'mean |GD|':>10s} {'GD':>7s}")
same=[]
for s in range(1,6):
    v=[m for m,x,y in data if x==s and y==s]
    if len(v)<200: continue
    n=len(v); dr=sum(1 for m in v if m['res']=='D')/n
    lo,hi=wilson(sum(1 for m in v if m['res']=='D'),n)
    agd=sum(abs(m['hg']-m['ag']) for m in v)/n
    gd=sum(m['hg']-m['ag'] for m in v)/n
    same+= v
    print(f"  {str(s)+'* v '+str(s)+'*':14s} {n:8,} {dr:8.1%} [{lo:.1%},{hi:.1%}]  {agd:10.2f} {gd:+7.2f}")
n=len(same); dr_same=sum(1 for m in same if m['res']=='D')/n
diff=[m for m,x,y in data if x!=y]
dr_diff=sum(1 for m in diff if m['res']=='D')/len(diff)
lo1,hi1=wilson(sum(1 for m in same if m['res']=='D'),n)
lo2,hi2=wilson(sum(1 for m in diff if m['res']=='D'),len(diff))
print(f"\n  ALL same-star : {n:,} matches, draw {dr_same:.1%}  CI [{lo1:.1%},{hi1:.1%}]")
print(f"  ALL diff-star : {len(diff):,} matches, draw {dr_diff:.1%}  CI [{lo2:.1%},{hi2:.1%}]")
print(f"  LIFT: {(dr_same-dr_diff)*100:+.2f} percentage points")

print("\n"+"="*92)
print("DRAW RATE BY STAR GAP — does it fall away as the gap widens?")
print("="*92)
print(f"  {'gap':>5s} {'n':>8s} {'draw%':>8s} {'95% CI':>16s} {'mean GD':>9s} {'home W':>8s}")
g=defaultdict(list)
for m,sh,sa in data: g[sh-sa].append(m)
for k in sorted(g):
    v=g[k]
    if len(v)<200: continue
    n2=len(v); dw=sum(1 for m in v if m['res']=='D')
    lo,hi=wilson(dw,n2)
    print(f"  {k:>+5d} {n2:8,} {dw/n2:8.1%} [{lo:.1%},{hi:.1%}]  "
          f"{sum(m['hg']-m['ag'] for m in v)/n2:+9.2f} {sum(1 for m in v if m['res']=='H')/n2:8.1%}")
print("\n  |gap| grouped:")
for ag in range(0,5):
    v=[m for k,ms in g.items() if abs(k)==ag for m in ms]
    if len(v)<200: continue
    dw=sum(1 for m in v if m['res']=='D'); lo,hi=wilson(dw,len(v))
    print(f"    |gap|={ag}  n={len(v):7,}  draw {dw/len(v):6.1%}  CI [{lo:.1%},{hi:.1%}]")
pickle.dump(data,open("user_stars.pkl","wb"))
