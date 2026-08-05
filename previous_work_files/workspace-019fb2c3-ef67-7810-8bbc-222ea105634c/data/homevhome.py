"""
USER'S NEW IDEA: instead of comparing home-team-at-home vs away-team-away,
compare BOTH teams on their HOME record. Like-for-like strength comparison
with venue asymmetry stripped out.

Build all three lenses, prior-only:
  STANDARD  : H's home record  vs  A's away record   (what everyone does)
  HOME-v-HOME: H's home record vs  A's HOME record   (user's idea)
  AWAY-v-AWAY: H's away record vs  A's away record
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
MIN=3

# rolling venue-split records
H_rec=defaultdict(lambda:{'p':0,'pts':0,'gf':0,'ga':0})   # team's HOME record
A_rec=defaultdict(lambda:{'p':0,'pts':0,'gf':0,'ga':0})   # team's AWAY record
out=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    hh,ha=H_rec[(lg,se,h)],A_rec[(lg,se,h)]
    ah,aa=H_rec[(lg,se,a)],A_rec[(lg,se,a)]
    if hh['p']>=MIN and aa['p']>=MIN and ah['p']>=MIN and ha['p']>=MIN:
        f=lambda d:(d['pts']/d['p'], (d['gf']-d['ga'])/d['p'])
        out.append((m,
            f(hh),   # home team's HOME record
            f(aa),   # away team's AWAY record   -> standard
            f(ah),   # away team's HOME record   -> user's idea
            f(ha)))  # home team's AWAY record
    hp=3 if m['res']=='H' else (1 if m['res']=='D' else 0)
    ap=3 if m['res']=='A' else (1 if m['res']=='D' else 0)
    d=H_rec[(lg,se,h)]; d['p']+=1; d['pts']+=hp; d['gf']+=m['hg']; d['ga']+=m['ag']
    d=A_rec[(lg,se,a)]; d['p']+=1; d['pts']+=ap; d['gf']+=m['ag']; d['ga']+=m['hg']
print(f"fixtures with all four venue records: {len(out):,}")

def corr(xs,ys):
    mx,my=sum(xs)/len(xs),sum(ys)/len(ys)
    n=sum((p-mx)*(q-my) for p,q in zip(xs,ys))
    d=math.sqrt(sum((p-mx)**2 for p in xs)*sum((q-my)**2 for q in ys))
    return n/d if d else 0

gd=[m['hg']-m['ag'] for m,_,_,_,_ in out]
res=[m['res'] for m,_,_,_,_ in out]
hw=[1.0 if r=='H' else 0.0 for r in res]
dw=[1.0 if r=='D' else 0.0 for r in res]

lenses={
 'STANDARD  H_home - A_away' : [hh[0]-aa[0] for _,hh,aa,ah,ha in out],
 'HOME-v-HOME H_home - A_home': [hh[0]-ah[0] for _,hh,aa,ah,ha in out],
 'AWAY-v-AWAY H_away - A_away': [ha[0]-aa[0] for _,hh,aa,ah,ha in out],
 'GD STANDARD'               : [hh[1]-aa[1] for _,hh,aa,ah,ha in out],
 'GD HOME-v-HOME'            : [hh[1]-ah[1] for _,hh,aa,ah,ha in out],
 'GD AWAY-v-AWAY'            : [ha[1]-aa[1] for _,hh,aa,ah,ha in out],
}
print("\n"+"="*84)
print("WHICH LENS PREDICTS BEST? (correlation, n=%s)"%f"{len(out):,}")
print("="*84)
print(f"  {'lens':30s} {'r w/ goal diff':>15s} {'r w/ home win':>15s} {'r w/ draw':>11s}")
for k,v in lenses.items():
    print(f"  {k:30s} {corr(v,gd):+15.4f} {corr(v,hw):+15.4f} {corr(v,dw):+11.4f}")

print("\n"+"="*84)
print("KEY TEST — is HOME-v-HOME independent of STANDARD?")
print("="*84)
s=lenses['STANDARD  H_home - A_away']; hvh=lenses['HOME-v-HOME H_home - A_home']
ava=lenses['AWAY-v-AWAY H_away - A_away']
print(f"  corr(STANDARD, HOME-v-HOME) = {corr(s,hvh):+.4f}")
print(f"  corr(STANDARD, AWAY-v-AWAY) = {corr(s,ava):+.4f}")
print(f"  corr(HOME-v-HOME, AWAY-v-AWAY) = {corr(hvh,ava):+.4f}")
print("  -> lower correlation = more independent information to add")

print("\n"+"="*84)
print("DOES HOME-v-HOME EXPLAIN WHAT THE MODEL MISSES? (residual test)")
print("="*84)
have=[(i,m) for i,(m,_,_,_,_) in enumerate(out) if K(m) in dc]
print(f"  matched to model predictions: {len(have):,}")
buckets=defaultdict(lambda:[0,0.0,0,0.0,0])
for i,m in have:
    v=hvh[i]
    b=max(-3,min(3,int(round(v))))
    x=buckets[b]; x[0]+=1; x[1]+=dc[K(m)][0]; x[2]+=(m['res']=='H'); x[3]+=dc[K(m)][1]; x[4]+=(m['res']=='D')
print(f"  {'H-v-H gap':>10s} {'n':>7s} {'model P(H)':>11s} {'actual H':>9s} {'err':>7s} {'model P(D)':>11s} {'actual D':>9s} {'err':>7s}")
for b in sorted(buckets):
    n,mp,ac,mpd,acd=buckets[b]
    if n<400: continue
    print(f"  {b:>+10d} {n:7,} {mp/n:11.1%} {ac/n:9.1%} {ac/n-mp/n:+7.1%} {mpd/n:11.1%} {acd/n:9.1%} {acd/n-mpd/n:+7.1%}")
pickle.dump((out,dict(lenses)),open("lenses.pkl","wb"))
