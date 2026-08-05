"""
Does att+dfn actually rank teams correctly? And does it predict GOAL DIFFERENCE,
which is what the star system is now specified to do?
"""
import pickle, json, math
from collections import defaultdict
st=pickle.load(open("model_state.pkl","rb"))
cut=json.load(open("star_cutoffs.json"))
rows=pickle.load(open("all_matches.pkl","rb"))

print("="*92)
print("5. SANITY CHECK — does att+dfn rank teams the way reality does?")
print("="*92)
# actual 2025/26 league table
tbl=defaultdict(lambda:[0,0,0,0])  # team -> [pts, gf, ga, games]
for m in rows:
    if m['season']!='2526' or m['lg']!='E0': continue
    h,a=m['home'],m['away']
    tbl[h][1]+=m['hg']; tbl[h][2]+=m['ag']; tbl[h][3]+=1
    tbl[a][1]+=m['ag']; tbl[a][2]+=m['hg']; tbl[a][3]+=1
    if m['res']=='H': tbl[h][0]+=3
    elif m['res']=='A': tbl[a][0]+=3
    else: tbl[h][0]+=1; tbl[a][0]+=1
def stars(lg,t):
    v=st['att'].get(t,0)+st['dfn'].get(t,0); c=cut[lg]
    return 1+sum(1 for x in c if v>=x)
real=sorted(tbl.items(), key=lambda x:(-x[1][0], -(x[1][1]-x[1][2])))
print(f"  {'#':>3s} {'team':20s} {'pts':>4s} {'GD':>5s} {'games':>6s} {'STARS':>6s} {'flag':>6s}")
bad=0
for i,(t,v) in enumerate(real,1):
    s=stars('E0',t)
    exp = 5 if i<=4 else 4 if i<=8 else 3 if i<=12 else 2 if i<=16 else 1
    flag='' if abs(s-exp)<=1 else 'WRONG'
    if flag: bad+=1
    print(f"  {i:>3d} {t:20s} {v[0]:>4d} {v[1]-v[2]:>+5d} {v[3]:>6d} {s:>6d} {flag:>6s}")
print(f"\n  teams misplaced by 2+ star levels: {bad}/{len(real)}")

print("\n"+"="*92)
print("6. THE ROOT CAUSE — dfn SIGN CONVENTION")
print("="*92)
print("  In the model, lambda_away = exp(mu + att[away] - dfn[home]).")
print("  HIGHER dfn => FEWER goals conceded => BETTER defence.")
print("  So att+dfn is directionally fine. But the SCALES differ:")
A=[st['att'][t] for lg,t in [( 'E0',x) for x in tbl] if t in st['att']]
D=[st['dfn'][t] for lg,t in [( 'E0',x) for x in tbl] if t in st['dfn']]
import statistics as S
print(f"    att: mean {S.mean(A):+.3f}  sd {S.pstdev(A):.3f}  range {min(A):+.3f}..{max(A):+.3f}")
print(f"    dfn: mean {S.mean(D):+.3f}  sd {S.pstdev(D):.3f}  range {min(D):+.3f}..{max(D):+.3f}")
print(f"    sd ratio dfn/att = {S.pstdev(D)/S.pstdev(A):.2f}")
print("  -> an equal-weighted SUM lets whichever component has more spread dominate.")
print("     Arsenal's dfn=0.888 (huge) drags it to 5*; Tottenham's balanced")
print("     profile scores low. The composite is not a strength measure.")

print("\n"+"="*92)
print("7. DOES THE CURRENT STAR GAP PREDICT GOAL DIFFERENCE? (its new job)")
print("="*92)
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
recent=[(m,H,D,A,lh,la) for m,H,D,A,lh,la in preds if m['season'] in ('2425','2526')]
g=defaultdict(list)
for m,H,D,A,lh,la in recent:
    if m['home'] not in st['att'] or m['away'] not in st['att']: continue
    sh,sa=stars(m['lg'],m['home']),stars(m['lg'],m['away'])
    g[sh-sa].append((m['hg']-m['ag'], lh-la))
print(f"  {'star gap':>9s} {'n':>7s} {'actual GD':>11s} {'model xGD':>11s} {'draw%':>8s}")
for k in sorted(g):
    v=g[k]
    if len(v)<150: continue
    print(f"  {k:>+9d} {len(v):7,} {sum(x[0] for x in v)/len(v):+11.2f} {sum(x[1] for x in v)/len(v):+11.2f} "
          f"{sum(1 for x in v if x[0]==0)/len(v):8.1%}")
# correlation
import math as M
xs=[k for k in g for _ in g[k]]; ys=[x[0] for k in g for x in g[k]]
mx,my=sum(xs)/len(xs),sum(ys)/len(ys)
num=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
den=M.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))
zs=[x[1] for k in g for x in g[k]]
mz=sum(zs)/len(zs)
num2=sum((a-mz)*(b-my) for a,b in zip(zs,ys))
den2=M.sqrt(sum((a-mz)**2 for a in zs)*sum((b-my)**2 for b in ys))
print(f"\n  correlation with actual goal difference:")
print(f"    star gap  r = {num/den:+.4f}")
print(f"    model xGD r = {num2/den2:+.4f}   <-- continuous version, same underlying data")
print(f"  -> discretising into 5 buckets costs {(1-(num/den)/(num2/den2))*100:.0f}% of the correlation.")
