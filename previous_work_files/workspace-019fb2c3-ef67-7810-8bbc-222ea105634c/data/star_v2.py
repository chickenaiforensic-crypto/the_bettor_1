"""
STAR SYSTEM v2 — user specification + Study 08 robustness fixes.

USER SPEC (unchanged):
  metric  = (3*won + drawn) / played        <- ranked by games played & won/drawn
  qualify = played >= 5
  stars   = 1..5, ranked within league

STUDY 08 FIXES:
  (1) rolling cutoffs   — recomputed at every fixture from PRIOR matches only
  (2) shrinkage         — regress metric toward league mean by games played,
                          so a 5-game record isn't treated as firmly as a 30-game one
  (3) hysteresis        — must clear a boundary by a margin to change star level

All hyperparameters chosen on TRAIN only. TEST never touched until the end.
"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
MIN=5
BOUND=[0.2,0.4,0.6,0.8]

def build(shrink_k, hyst):
    """shrink_k = prior weight in games; hyst = percentile buffer at boundaries"""
    rec=defaultdict(lambda:{'p':0,'w':0,'d':0})
    pool=defaultdict(dict)          # (lg,se) -> team -> raw metric   (indexed: fast)
    prev=defaultdict(lambda:None)   # (lg,se,team) -> last star
    lgmean=defaultdict(lambda:[0.0,0])
    out=[]
    for m in rows:
        lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
        key=(lg,se)
        lm = lgmean[key][0]/lgmean[key][1] if lgmean[key][1]>0 else 1.35
        vals=sorted(pool[key].values())

        def star_of(team):
            d=rec[(lg,se,team)]
            if d['p']<MIN: return None
            raw=(3*d['w']+d['d'])/d['p']
            v=(raw*d['p'] + lm*shrink_k)/(d['p']+shrink_k)   # shrinkage
            if len(vals)<8: return None
            below=sum(1 for x in vals if x<v)
            pct=below/len(vals)
            s=min(5,max(1,int(pct*5)+1))
            p=prev[(lg,se,team)]
            if p is not None and s!=p and hyst>0:            # hysteresis
                # boundary between level L and L+1 sits at BOUND[L-1] (L=1..4)
                if s>p:
                    b=BOUND[p-1] if 1<=p<=4 else None        # crossing upward out of p
                    if b is not None and pct < b+hyst: s=p
                elif s<p:
                    b=BOUND[s-1] if 1<=s<=4 else None        # crossing downward into s
                    if b is not None and pct > b-hyst: s=p
            return s

        sh,sa=star_of(h),star_of(a)
        if sh is not None: prev[(lg,se,h)]=sh
        if sa is not None: prev[(lg,se,a)]=sa
        if sh is not None and sa is not None:
            out.append((m,sh,sa))

        for t,res in ((h,m['res']),(a,m['res'])):
            d=rec[(lg,se,t)]
            won = (res=='H' and t==h) or (res=='A' and t==a)
            drew= res=='D'
            d['p']+=1
            if won: d['w']+=1
            elif drew: d['d']+=1
            if d['p']>=MIN:
                pool[key][t]=(3*d['w']+d['d'])/d['p']
        pts_h=3 if m['res']=='H' else (1 if m['res']=='D' else 0)
        pts_a=3 if m['res']=='A' else (1 if m['res']=='D' else 0)
        lgmean[key][0]+=pts_h+pts_a; lgmean[key][1]+=2
    return out

def churn(dat):
    seq=defaultdict(list)
    for m,sh,sa in dat:
        seq[(m['lg'],m['season'],m['home'])].append(sh)
        seq[(m['lg'],m['season'],m['away'])].append(sa)
    ch=tot=0
    for v in seq.values():
        for i in range(1,len(v)):
            tot+=1; ch+= (v[i]!=v[i-1])
    return ch/tot if tot else 0

def drawsep(dat):
    s=[m for m,x,y in dat if x==y]; d=[m for m,x,y in dat if x!=y]
    if not s or not d: return 0
    return (sum(1 for m in s if m['res']=='D')/len(s)
          - sum(1 for m in d if m['res']=='D')/len(d))

print("="*84)
print("TUNING ON TRAIN ONLY (first 70% by date)")
print("="*84)
print(f"  {'shrink':>7s} {'hyst':>6s} {'n':>9s} {'churn':>8s} {'draw sep':>9s}")
best=None
for sk in [0,3,6]:
    for hy in [0.0,0.05,0.10]:
        dat=build(sk,hy)
        dat.sort(key=lambda x:x[0]['date'])
        cut=int(len(dat)*0.70); tr=dat[:cut]
        c=churn(tr); ds=drawsep(tr)
        score=ds-0.02*c            # reward draw separation, penalise churn
        if best is None or score>best[0]: best=(score,sk,hy)
        print(f"  {sk:>7d} {hy:>6.2f} {len(dat):9,} {c:8.1%} {ds:9.2%}")
_,SK,HY=best
print(f"\n  chosen on TRAIN: shrink={SK}, hysteresis={HY}")

dat=build(SK,HY)
dat.sort(key=lambda x:x[0]['date'])
pickle.dump(dat,open("stars_v2.pkl","wb"))
print(f"  built {len(dat):,} rated fixtures -> stars_v2.pkl")

print("\n"+"="*84)
print("v1 vs v2 — structural quality")
print("="*84)
v1=pickle.load(open("user_stars.pkl","rb"))
print(f"  {'version':28s} {'n':>9s} {'churn':>8s} {'draw sep':>9s}")
print(f"  {'v1 (your spec, no fixes)':28s} {len(v1):9,} {churn(v1):8.1%} {drawsep(v1):9.2%}")
print(f"  {'v2 (+rolling+shrink+hyst)':28s} {len(dat):9,} {churn(dat):8.1%} {drawsep(dat):9.2%}")
