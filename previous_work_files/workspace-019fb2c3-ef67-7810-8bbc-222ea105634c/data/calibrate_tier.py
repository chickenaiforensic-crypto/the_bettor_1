"""
THE USER'S METHOD: don't discard where it fails - calibrate per segment.
Diagnosis showed:
  - same-star LIFT is LARGEST in top flight (+3.41%) - the signal is strongest there
  - but the GLOBAL table is miscalibrated for it (over-predicts draws by 1.5-3.5pt)
  - base draw rates differ by tier: 25.1% / 29.2% / 26.8%
So: fit a SEPARATE draw table per tier, on TRAIN only. Test held-out.
"""
import pickle, math, random
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},
      **{l:3 for l in ['E2','E3']}}
TN={1:'top flight',2:'second tier',3:'third/fourth'}

dat=sorted([(m,s,a) for m,s,a in v2 if K(m) in dc],key=lambda x:x[0]['date'])
c=int(len(dat)*0.70); TR,TE=dat[:c],dat[c:]
print(f"train {len(TR):,}  test {len(TE):,}  (test from {TE[0][0]['date'].date()})")

# ---------- GLOBAL table (what we had) ----------
gt=defaultdict(lambda:[0,0])
for m,sh,sa in TR:
    x=gt[sh-sa]; x[0]+=1; x[1]+=(m['res']=='D')
GG=sum(1 for m,_,_ in TR if m['res']=='D')/len(TR)
def g_tab(k): return gt[k][1]/gt[k][0] if gt.get(k) and gt[k][0]>=200 else GG

# ---------- PER-TIER tables ----------
tt=defaultdict(lambda:[0,0]); tbase={}
for m,sh,sa in TR:
    t=TIER.get(m['lg'],1)
    x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
for t in (1,2,3):
    v=[m for m,_,_ in TR if TIER.get(m['lg'],1)==t]
    tbase[t]=sum(1 for m in v if m['res']=='D')/len(v)
def t_tab(t,k):
    x=tt.get((t,k))
    return x[1]/x[0] if x and x[0]>=150 else tbase[t]

print("\n"+"="*86)
print("PER-TIER DRAW TABLES (fitted on TRAIN) vs the single global table")
print("="*86)
print(f"  {'gap':>5s} {'GLOBAL':>9s} {'top flight':>12s} {'second tier':>13s} {'third/fourth':>14s}")
for k in range(-4,5):
    print(f"  {k:>+5d} {g_tab(k):9.1%} {t_tab(1,k):12.1%} {t_tab(2,k):13.1%} {t_tab(3,k):14.1%}")
print("  -> the tiers genuinely need different tables. Top flight draws less at every gap.")

# ---------- weights, chosen per tier on TRAIN ----------
def fit_w(t):
    best=(9,0)
    sub=[(m,sh,sa) for m,sh,sa in TR if TIER.get(m['lg'],1)==t]
    for w in [0,.05,.1,.15,.2,.25,.3,.35,.4,.5]:
        e=sum((((1-w)*dc[K(m)][1]+w*t_tab(t,sh-sa))-(m['res']=='D'))**2 for m,sh,sa in sub)/len(sub)
        if e<best[0]: best=(e,w)
    return best[1]
W={t:fit_w(t) for t in (1,2,3)}
print(f"\n  blend weights chosen on TRAIN: " + ", ".join(f"{TN[t]}={W[t]}" for t in (1,2,3)))

# ---------- evaluate on TEST ----------
def deltas(S, mode):
    out=[]
    for m,sh,sa in S:
        t=TIER.get(m['lg'],1)
        y=1.0 if m['res']=='D' else 0.0
        p=dc[K(m)][1]
        if mode=='global': b=(1-0.25)*p+0.25*g_tab(sh-sa)
        else:              b=(1-W[t])*p+W[t]*t_tab(t,sh-sa)
        out.append((p-y)**2-(b-y)**2)
    return out

def boot(d,seed=7):
    random.seed(seed); N=len(d); bs=[]
    for _ in range(20000):
        s=0.0
        for _ in range(300): s+=d[random.randrange(N)]
        bs.append(s/300)
    bs.sort(); return bs[500],bs[19500],sum(1 for x in bs if x<=0)/len(bs)

dcb=sum((dc[K(m)][1]-(1.0 if m['res']=='D' else 0.0))**2 for m,_,_ in TE)/len(TE)
print("\n"+"="*86); print("HELD-OUT RESULT"); print("="*86)
for mode,label in [('global','single global table (Study 10)'),('tier','PER-TIER calibrated tables')]:
    d=deltas(TE,mode); g=sum(d)/len(d); lo,hi,pn=boot(d)
    print(f"\n  {label}")
    print(f"    gain      : {g:+.7f}  ({g/dcb*100:+.3f}%)")
    print(f"    95% CI    : [{lo:+.7f}, {hi:+.7f}]")
    print(f"    P(gain<=0): {pn:.3f}  -> {'ROBUST' if lo>0 else 'not significant'}")

print("\n"+"="*86); print("PER-TIER BREAKDOWN ON TEST (calibrated version)"); print("="*86)
d=deltas(TE,'tier')
bt=defaultdict(list)
for x,(m,_,_) in zip(d,TE): bt[TIER.get(m['lg'],1)].append(x)
print(f"  {'tier':16s} {'n':>8s} {'gain':>13s} {'95% CI':>28s} {'sig':>5s}")
for t in (1,2,3):
    v=bt[t]; g=sum(v)/len(v); lo,hi,pn=boot(v,seed=t)
    print(f"  {TN[t]:16s} {len(v):8,} {g:+13.7f}  [{lo:+.7f},{hi:+.7f}] {'YES' if lo>0 else 'no':>5s}")
pickle.dump(dict(tier=dict(tt),base=tbase,W=W,TIER=TIER),open("tier_tables.pkl","wb"))
