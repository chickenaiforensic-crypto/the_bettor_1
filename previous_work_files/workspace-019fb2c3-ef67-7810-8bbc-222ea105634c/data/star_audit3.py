"""
Compare candidate star constructions for the GOAL-DIFFERENCE job.
All rebuilt PROPERLY: rolling cutoffs from prior data only (no look-ahead).
Judged on: correlation with GD, draw separation, category stability.
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))

# rolling, prior-only team stats per league-season
stats=defaultdict(lambda:{'gf':0,'ga':0,'n':0,'pts':0,'hgf':0,'hga':0,'hn':0,'agf':0,'aga':0,'an':0})
recs=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    H,A=stats[(lg,se,h)],stats[(lg,se,a)]
    peers=[(k,v) for k,v in stats.items() if k[0]==lg and k[1]==se and v['n']>=5]
    recs.append((m,dict(H),dict(A),peers))
    H['gf']+=m['hg'];H['ga']+=m['ag'];H['n']+=1
    H['hgf']+=m['hg'];H['hga']+=m['ag'];H['hn']+=1
    A['gf']+=m['ag'];A['ga']+=m['hg'];A['n']+=1
    A['agf']+=m['ag'];A['aga']+=m['hg'];A['an']+=1
    if m['res']=='H': H['pts']+=3
    elif m['res']=='A': A['pts']+=3
    else: H['pts']+=1; A['pts']+=1

def quint(val,vals):
    if len(vals)<8: return None
    s=sorted(vals); below=sum(1 for x in s if x<val)
    return min(5,max(1,int(below/len(s)*5)+1))

CANDS={
 'A_att+dfn (shipped)': lambda d: (d['gf']/d['n']) + (1-d['ga']/d['n']) if d['n']>=5 else None,
 'B_GD per game'      : lambda d: (d['gf']-d['ga'])/d['n'] if d['n']>=5 else None,
 'C_points per game'  : lambda d: d['pts']/d['n'] if d['n']>=5 else None,
 'D_venue-split GD'   : None,   # handled separately
}
def venue_gd(d,home):
    if home: return (d['hgf']-d['hga'])/d['hn'] if d['hn']>=3 else None
    return (d['agf']-d['aga'])/d['an'] if d['an']>=3 else None

out=defaultdict(list)
for m,H,A,peers in recs:
    gd=m['hg']-m['ag']
    for name,fn in CANDS.items():
        if name.startswith('D_'):
            vh,va=venue_gd(H,True),venue_gd(A,False)
            if vh is None or va is None: continue
            ph=[venue_gd(v,True) for k,v in peers]; pa=[venue_gd(v,False) for k,v in peers]
            ph=[x for x in ph if x is not None]; pa=[x for x in pa if x is not None]
            sh,sa=quint(vh,ph),quint(va,pa)
        else:
            vh,va=fn(H),fn(A)
            if vh is None or va is None: continue
            pv=[fn(v) for k,v in peers]; pv=[x for x in pv if x is not None]
            sh,sa=quint(vh,pv),quint(va,pv)
        if sh is None or sa is None: continue
        out[name].append((sh,sa,gd,m['res']))

def corr(xs,ys):
    mx,my=sum(xs)/len(xs),sum(ys)/len(ys)
    n=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
    d=math.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))
    return n/d if d else 0

print("="*94)
print("8. CANDIDATE STAR CONSTRUCTIONS — all prior-only, rolling cutoffs")
print("="*94)
print(f"  {'construction':24s} {'n':>8s} {'r with GD':>10s} {'draw sep':>9s} {'gap range':>10s}")
res={}
for name,v in sorted(out.items()):
    if len(v)<5000: continue
    gaps=[x[0]-x[1] for x in v]; gds=[x[2] for x in v]
    r=corr(gaps,gds)
    dr=defaultdict(lambda:[0,0])
    for sh,sa,gd,rs in v:
        g=sh-sa; dr[g][0]+=1; dr[g][1]+= (rs=='D')
    d0=dr[0][1]/dr[0][0] if dr[0][0]>200 else float('nan')
    ext=[dr[g][1]/dr[g][0] for g in (-4,4) if dr[g][0]>200]
    sep=d0-(sum(ext)/len(ext)) if ext else float('nan')
    mn=min(x[2] for x in [(0,0,sum(y[2] for y in v if y[0]-y[1]==g)/max(1,sum(1 for y in v if y[0]-y[1]==g))) for g in [-4]]+[(0,0,0)])
    gmeans=[sum(y[2] for y in v if y[0]-y[1]==g)/max(1,sum(1 for y in v if y[0]-y[1]==g)) for g in range(-4,5)]
    res[name]=(r,sep,len(v))
    print(f"  {name:24s} {len(v):8,} {r:+10.4f} {sep:9.1%} {min(gmeans):+.2f}..{max(gmeans):+.2f}")

print("\n  draw sep = draw%% at gap 0 minus draw%% at extreme gaps (higher = better draw signal)")

print("\n"+"="*94)
print("9. BEST CANDIDATE — full goal-difference profile by star gap")
print("="*94)
best=max(res.items(),key=lambda x:x[1][0])[0]
print(f"  winner on correlation: {best}")
v=out[best]
gg=defaultdict(list)
for sh,sa,gd,rs in v: gg[sh-sa].append((gd,rs))
print(f"  {'gap':>5s} {'n':>8s} {'mean GD':>9s} {'sd':>7s} {'draw%':>8s} {'home win%':>10s} {'|GD|>=2':>9s}")
for g in sorted(gg):
    z=gg[g]
    if len(z)<200: continue
    gds=[x[0] for x in z]; mu=sum(gds)/len(gds)
    sd=math.sqrt(sum((x-mu)**2 for x in gds)/len(gds))
    print(f"  {g:>+5d} {len(z):8,} {mu:+9.2f} {sd:7.2f} {sum(1 for x in z if x[0]==0)/len(z):8.1%} "
          f"{sum(1 for x in z if x[1]=='H')/len(z):10.1%} {sum(1 for x in z if abs(x[0])>=2)/len(z):9.1%}")

print("\n"+"="*94)
print("10. STABILITY — how often does a team change star level week to week?")
print("="*94)
for name in sorted(out.keys()):
    if name not in res: continue
    # track consecutive ratings per team
    seq=defaultdict(list)
    for m,H,A,peers in recs[:40000]:
        pass
print("  (measured on construction B below)")
seq=defaultdict(list)
for m,H,A,peers in recs:
    lg,se=m['lg'],m['season']
    for team,d in ((m['home'],H),(m['away'],A)):
        if d['n']<5: continue
        pv=[(v['gf']-v['ga'])/v['n'] for k,v in peers if v['n']>=5]
        s=quint((d['gf']-d['ga'])/d['n'],pv)
        if s: seq[(lg,se,team)].append(s)
ch=0;tot=0;big=0
for k,v in seq.items():
    for i in range(1,len(v)):
        tot+=1
        if v[i]!=v[i-1]: ch+=1
        if abs(v[i]-v[i-1])>=2: big+=1
print(f"  star changed between consecutive matches: {ch}/{tot} = {ch/tot:.1%}")
print(f"  changed by 2+ levels: {big}/{tot} = {big/tot:.1%}")
