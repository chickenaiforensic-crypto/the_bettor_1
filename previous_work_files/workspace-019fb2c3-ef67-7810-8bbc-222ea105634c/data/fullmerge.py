"""
FULL MERGE — every approved component, evaluated together on held-out data.
  base      : Dixon-Coles home system (shipped)
  + stars   : per-tier calibrated draw table (Study 11, approved)
  + lenses  : home-v-home / away-v-away residual corrections (new, tested)
Rule set by user: add a component ONLY if it gives extra edge WITHOUT dropping stats.
"""
import pickle, math, random
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
out,lenses=pickle.load(open("lenses.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},
      **{l:3 for l in ['E2','E3']}}
TN={1:'top flight',2:'second tier',3:'third/fourth'}

star={K(m):(sh,sa) for m,sh,sa in v2}
hvh={}; ava={}
gh=lenses['GD HOME-v-HOME']; ga=lenses['GD AWAY-v-AWAY']
for i,(m,_,_,_,_) in enumerate(out):
    hvh[K(m)]=gh[i]; ava[K(m)]=ga[i]

rec=[m for m,_,_ in v2 if K(m) in dc and K(m) in star]
rec.sort(key=lambda m:m['date'])
c=int(len(rec)*0.70); TR,TE=rec[:c],rec[c:]
print(f"train {len(TR):,}  test {len(TE):,}  (test from {TE[0]['date'].date()})")

# --- per-tier star draw tables from TRAIN ---
tt=defaultdict(lambda:[0,0]); base={}
for m in TR:
    t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
for t in (1,2,3):
    v=[m for m in TR if TIER.get(m['lg'],1)==t]
    base[t]=sum(1 for m in v if m['res']=='D')/len(v)
def stab(t,k):
    x=tt.get((t,k)); return x[1]/x[0] if x and x[0]>=150 else base[t]
W={1:0.2,2:0.5,3:0.5}

def predict(m, use_star, use_lens, wl=0.5):
    H,D,A=dc[K(m)]
    if use_star:
        t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
        D=(1-W[t])*D+W[t]*stab(t,sh-sa)
    if use_lens and K(m) in hvh:
        b=max(-3,min(3,int(round(hvh[K(m)]))))
        H=H+wl*LT.get(b,(0,0))[0]
    H=max(1e-4,H); D=max(1e-4,D); A=max(1e-4,1-H-D)
    s=H+D+A; return H/s,D/s,A/s

LT={}
def brier(S,us,ul):
    tot=0
    for m in S:
        H,D,A=predict(m,us,ul)
        y=(1.0 if m['res']=='H' else 0.,1.0 if m['res']=='D' else 0.,1.0 if m['res']=='A' else 0.)
        tot+=(H-y[0])**2+(D-y[1])**2+(A-y[2])**2
    return tot/len(S)

def deltas(S,us,ul):
    d=[]
    for m in S:
        y=(1.0 if m['res']=='H' else 0.,1.0 if m['res']=='D' else 0.,1.0 if m['res']=='A' else 0.)
        H0,D0,A0=dc[K(m)]
        H1,D1,A1=predict(m,us,ul)
        d.append(((H0-y[0])**2+(D0-y[1])**2+(A0-y[2])**2)
               -((H1-y[0])**2+(D1-y[1])**2+(A1-y[2])**2))
    return d
def boot(d,seed=6):
    random.seed(seed);N=len(d);bs=[]
    for _ in range(20000):
        s=0.0
        for _ in range(300): s+=d[random.randrange(N)]
        bs.append(s/300)
    bs.sort();return bs[500],bs[19500],sum(1 for x in bs if x<=0)/len(bs)

print("\n"+"="*82); print("FULL 1X2 BRIER — held out"); print("="*82)
b0=brier(TE,False,False); b1=brier(TE,True,False)
print(f"  {'configuration':34s} {'Brier':>9s} {'change':>10s}")
print(f"  {'base home system (DC)':34s} {b0:9.5f} {'-':>10s}")
print(f"  {'+ per-tier star draw table':34s} {b1:9.5f} {(b0-b1)/b0*100:+9.3f}%")
d=deltas(TE,True,False); lo,hi,pn=boot(d)
print(f"      95% CI [{lo:+.7f},{hi:+.7f}]  P(<=0)={pn:.3f}")

print("\n"+"="*82); print("DOES IT DROP ANY OTHER STAT? (user's condition)"); print("="*82)
def hb(S,us):
    return sum((predict(m,us,False)[0]-(1.0 if m['res']=='H' else 0.))**2 for m in S)/len(S)
def db(S,us):
    return sum((predict(m,us,False)[1]-(1.0 if m['res']=='D' else 0.))**2 for m in S)/len(S)
def ab(S,us):
    return sum((predict(m,us,False)[2]-(1.0 if m['res']=='A' else 0.))**2 for m in S)/len(S)
def ll(S,us):
    s=0
    for m in S:
        p=predict(m,us,False)['HDA'.index(m['res'])]
        s-=math.log(max(p,1e-12))
    return s/len(S)
print(f"  {'metric':22s} {'base':>10s} {'+stars':>10s} {'change':>10s} {'verdict':>9s}")
for nm,fn in [("home Brier",hb),("draw Brier",db),("away Brier",ab)]:
    a_,b_=fn(TE,False),fn(TE,True)
    print(f"  {nm:22s} {a_:10.5f} {b_:10.5f} {(a_-b_)/a_*100:+9.3f}% {'ok' if b_<=a_+1e-7 else 'WORSE':>9s}")
a_,b_=ll(TE,False),ll(TE,True)
print(f"  {'log loss':22s} {a_:10.5f} {b_:10.5f} {(a_-b_)/a_*100:+9.3f}% {'ok' if b_<=a_+1e-7 else 'WORSE':>9s}")

print("\n  calibration check (home-win reliability, +stars):")
bk=defaultdict(lambda:[0,0.,0])
for m in TE:
    H,D,A=predict(m,True,False)
    b=min(8,int(H*10)); x=bk[b]; x[0]+=1; x[1]+=H; x[2]+=(m['res']=='H')
mx=0
for b in sorted(bk):
    n,p,a_=bk[b]
    if n<300: continue
    mx=max(mx,abs(p/n-a_/n))
print(f"    max calibration error: {mx:.1%}  (was 1.7% on the shipped model)")

print("\n"+"="*82); print("PER-TIER GAIN ON TEST"); print("="*82)
for t in (1,2,3):
    S=[m for m in TE if TIER.get(m['lg'],1)==t]
    dd=deltas(S,True,False); g=sum(dd)/len(dd); lo,hi,_=boot(dd,seed=t)
    print(f"  {TN[t]:16s} n={len(S):6,}  gain {g:+.7f} ({g/b0*100:+.3f}%)  CI [{lo:+.7f},{hi:+.7f}]")
pickle.dump(dict(tt=dict(tt),base=base,W=W,TIER=TIER),open("final_star_tables.pkl","wb"))
