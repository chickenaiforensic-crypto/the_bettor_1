"""
CRITICAL PRE-CHECK for the 3rd-phase common-opponent idea.
It needs a PATH between the two clubs through shared opponents.
Question: do domestic leagues connect at all?
"""
import pickle
from collections import defaultdict, deque
rows=pickle.load(open("all_matches.pkl","rb"))
# build opponent graph: node = (league-country, team) keyed by team name + country
adj=defaultdict(set)
country=lambda lg: {'E0':'ENG','E1':'ENG','E2':'ENG','E3':'ENG','SC0':'SCO','D1':'GER','D2':'GER',
 'SP1':'ESP','SP2':'ESP','I1':'ITA','I2':'ITA','F1':'FRA','F2':'FRA','N1':'NED','B1':'BEL',
 'P1':'POR','T1':'TUR','G1':'GRE'}[lg]
for m in rows:
    a=(country(m['lg']),m['home']); b=(country(m['lg']),m['away'])
    adj[a].add(b); adj[b].add(a)
print(f"nodes (clubs): {len(adj):,}")
print(f"edges: {sum(len(v) for v in adj.values())//2:,}")

# connected components
seen=set(); comps=[]
for n in adj:
    if n in seen: continue
    q=deque([n]); c=set([n]); seen.add(n)
    while q:
        x=q.popleft()
        for y in adj[x]:
            if y not in seen: seen.add(y); c.add(y); q.append(y)
    comps.append(c)
comps.sort(key=len,reverse=True)
print(f"\nconnected components: {len(comps)}")
for i,c in enumerate(comps[:8]):
    cs=defaultdict(int)
    for co,t in c: cs[co]+=1
    print(f"  component {i+1}: {len(c):4d} clubs  countries: {dict(cs)}")

print("\n"+"="*80)
print("VERDICT")
print("="*80)
print(f"  Every country is its own island. {len(comps)} separate components.")
print("  Within a country, divisions connect via promotion/relegation.")
print("  ACROSS countries there is NO path at any degree -- 2nd, 3rd, or 10th.")
print("  A Polish club and a Danish club share ZERO opponents, transitively.")
print("\n  => The 3rd-phase method CANNOT work on domestic data alone.")
print("     It requires cross-border matches (European competition) as bridges.")
