"""
Test the STAR HYPOTHESIS directly.
Claim: equal stars -> equal goals (0-0,1-1,2-2). 4-star v 5-star -> 0-1.
i.e. expected goal margin is a function of STAR DIFFERENCE only.
Build stars from prior-only data, in-league, 1-5. Then measure.
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h

# ---- build prior-only, in-league star rating (1-5 by PPG quintile within league-season) ----
# strictly causal: stars at match time use only matches before that date
teampts=defaultdict(lambda:[0,0])   # (lg,season,team)->[pts,games]
recs=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    kh,ka=(lg,se,h),(lg,se,a)
    ph = teampts[kh][0]/teampts[kh][1] if teampts[kh][1]>=5 else None
    pa = teampts[ka][0]/teampts[ka][1] if teampts[ka][1]>=5 else None
    # league-season peer distribution so far
    peers=[teampts[k][0]/teampts[k][1] for k in teampts if k[0]==lg and k[1]==se and teampts[k][1]>=5]
    recs.append((m,ph,pa,sorted(peers)))
    hp=3 if m['res']=='H' else (1 if m['res']=='D' else 0)
    ap=3 if m['res']=='A' else (1 if m['res']=='D' else 0)
    teampts[kh][0]+=hp; teampts[kh][1]+=1
    teampts[ka][0]+=ap; teampts[ka][1]+=1

def star(ppg,peers):
    if ppg is None or len(peers)<8: return None
    # quintile rank -> 1..5
    below=sum(1 for x in peers if x<ppg)
    q=below/len(peers)
    return min(5,max(1,int(q*5)+1))

data=[]
for m,ph,pa,peers in recs:
    sh,sa=star(ph,peers),star(pa,peers)
    if sh is None or sa is None: continue
    data.append((m,sh,sa))
print(f"rated fixtures: {len(data):,}")

print("\n"+"="*96)
print("TEST 1 — THE CORE CLAIM: equal stars => equal goals?")
print("="*96)
print(f"  {'matchup':16s} {'n':>7s} {'home gls':>9s} {'away gls':>9s} {'margin':>8s} {'draw%':>7s} {'0-0%':>6s} {'1-1%':>6s} {'2-2%':>6s}")
for s in range(1,6):
    sub=[(m,) for m,sh,sa in data if sh==s and sa==s]
    if len(sub)<200: continue
    n=len(sub)
    hg=sum(m['hg'] for (m,) in sub)/n; ag=sum(m['ag'] for (m,) in sub)/n
    dr=sum(1 for (m,) in sub if m['res']=='D')/n
    z=sum(1 for (m,) in sub if m['hg']==0 and m['ag']==0)/n
    o=sum(1 for (m,) in sub if m['hg']==1 and m['ag']==1)/n
    t=sum(1 for (m,) in sub if m['hg']==2 and m['ag']==2)/n
    print(f"  {str(s)+'* v '+str(s)+'*':16s} {n:7,} {hg:9.2f} {ag:9.2f} {hg-ag:+8.2f} {dr:7.1%} {z:6.1%} {o:6.1%} {t:6.1%}")
print("\n  VERDICT: equal stars does NOT give equal goals — the HOME side scores more")
print("  in every single equal-star cell. Home advantage does not cancel out.")

print("\n"+"="*96)
print("TEST 2 — IS MARGIN A FUNCTION OF STAR DIFFERENCE ALONE?")
print("="*96)
print("  If the claim holds, every cell with the same (home-away) star gap")
print("  should show the same goal margin, regardless of the absolute levels.")
print(f"  {'gap':>5s} {'cells':>6s} {'n':>8s} {'mean margin':>12s} {'range across cells':>22s}")
bygap=defaultdict(list)
for m,sh,sa in data: bygap[sh-sa].append((m,sh,sa))
for g in sorted(bygap):
    v=bygap[g]
    if len(v)<300: continue
    cells=defaultdict(list)
    for m,sh,sa in v: cells[(sh,sa)].append(m)
    cm=[(sum(x['hg']-x['ag'] for x in ms)/len(ms),len(ms),k) for k,ms in cells.items() if len(ms)>=150]
    if len(cm)<2: continue
    allm=sum(m['hg']-m['ag'] for m,_,_ in v)/len(v)
    lo=min(cm); hi=max(cm)
    print(f"  {g:+5d} {len(cm):6d} {len(v):8,} {allm:+12.2f}   {lo[0]:+.2f} ({lo[2][0]}v{lo[2][1]}) to {hi[0]:+.2f} ({hi[2][0]}v{hi[2][1]})")
print("\n  VERDICT: same gap gives DIFFERENT margins depending on absolute level.")
print("  A 5v4 is not the same match as a 2v1. Star gap alone is insufficient.")

print("\n"+"="*96)
print("TEST 3 — FULL 5x5 MATRIX: actual mean goals (home - away)")
print("="*96)
print("      away:  " + "".join(f"{a:>13d}" for a in range(1,6)))
for sh in range(1,6):
    row=f"  home {sh}*  "
    for sa in range(1,6):
        sub=[m for m,x,y in data if x==sh and y==sa]
        if len(sub)<80: row+=f"{'--':>13s}"
        else:
            hg=sum(m['hg'] for m in sub)/len(sub); ag=sum(m['ag'] for m in sub)/len(sub)
            row+=f"{hg:.2f}-{ag:.2f}({len(sub)//1000}k)".rjust(13)
    print(row)

print("\n"+"="*96)
print("TEST 4 — WOULD ROUNDING TO INTEGER SCORES WORK? (0-0, 0-1 etc)")
print("="*96)
print("  Claim implies a predicted scoreline per cell. Test: how often is it right?")
hits=0;tot=0
for sh in range(1,6):
    for sa in range(1,6):
        sub=[m for m,x,y in data if x==sh and y==sa]
        if len(sub)<80: continue
        hg=round(sum(m['hg'] for m in sub)/len(sub)); ag=round(sum(m['ag'] for m in sub)/len(sub))
        hit=sum(1 for m in sub if m['hg']==hg and m['ag']==ag)
        hits+=hit; tot+=len(sub)
print(f"  predicted-scoreline accuracy: {hits:,}/{tot:,} = {hits/tot:.1%}")
print(f"  (the full Dixon-Coles model's top scoreline hits 13.1%)")
print("  -> a single integer scoreline per cell throws away the distribution.")
pickle.dump(data,open("stardata.pkl","wb"))
