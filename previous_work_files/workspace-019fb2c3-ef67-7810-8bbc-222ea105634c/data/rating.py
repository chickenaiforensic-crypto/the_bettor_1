"""
PITCH RATING SYSTEM v1 — built ONLY from match results. No odds, no market data.
Dixon-Coles style attack/defence ratings + per-team home advantage,
fitted online with time decay, producing calibrated 1X2 + scoreline probabilities.
Validated on held-out seasons by Brier score / log loss against base-rate benchmarks.
"""
import pickle, math, json
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home'],r['away']))
print(f"matches {len(rows):,}")

LEAGUE_MU=defaultdict(lambda:[0.0,0]) # league -> mean goals

class Model:
    """Online-updated attack/defence ratings. Gradient step per match on Poisson log-lik."""
    def __init__(self, lr=0.055, decay=0.0022, hfa_lr=0.010):
        self.att=defaultdict(float); self.dfn=defaultdict(float)
        self.hfa=defaultdict(lambda:0.26)      # per-league home advantage (log scale)
        self.thfa=defaultdict(float)           # per-team extra home advantage
        self.mu=defaultdict(lambda:0.30)       # per-league log base goals
        self.lr=lr; self.decay=decay; self.hfa_lr=hfa_lr
        self.seen=defaultdict(int)
    def lam(self,lg,h,a):
        lh=math.exp(self.mu[lg]+self.att[h]-self.dfn[a]+self.hfa[lg]+self.thfa[h])
        la=math.exp(self.mu[lg]+self.att[a]-self.dfn[h])
        return max(0.05,min(6.0,lh)), max(0.05,min(6.0,la))
    def update(self,m):
        lg,h,a,hg,ag=m['lg'],m['home'],m['away'],m['hg'],m['ag']
        lh,la=self.lam(lg,h,a)
        eh,ea=hg-lh, ag-la
        # reliability: new teams move faster
        kh=self.lr*(1.6 if self.seen[h]<8 else 1.0)
        ka=self.lr*(1.6 if self.seen[a]<8 else 1.0)
        self.att[h]+=kh*eh*0.5; self.dfn[a]-=ka*eh*0.5
        self.att[a]+=ka*ea*0.5; self.dfn[h]-=kh*ea*0.5
        self.hfa[lg]+=self.hfa_lr*(eh-ea)*0.02
        self.thfa[h]+=self.hfa_lr*(eh-ea)*0.010
        self.thfa[h]*=0.999
        self.mu[lg]+=0.004*((eh+ea)/2)
        # shrink toward zero (time decay / regression to mean)
        for t in (h,a):
            self.att[t]*=(1-self.decay); self.dfn[t]*=(1-self.decay)
        self.seen[h]+=1; self.seen[a]+=1
        self.hfa[lg]=max(0.05,min(0.55,self.hfa[lg]))
        self.thfa[h]=max(-0.25,min(0.25,self.thfa[h]))

def dc_tau(i,j,lh,la,rho=-0.06):
    if i==0 and j==0: return 1-lh*la*rho
    if i==0 and j==1: return 1+lh*rho
    if i==1 and j==0: return 1+la*rho
    if i==1 and j==1: return 1-rho
    return 1.0
_fact=[math.factorial(i) for i in range(11)]
def probs(lh,la,rho=-0.06,K=11):
    ph=[math.exp(-lh)*lh**i/_fact[i] for i in range(K)]
    pa=[math.exp(-la)*la**j/_fact[j] for j in range(K)]
    H=D=A=0.0; grid={}
    for i in range(K):
        for j in range(K):
            p=ph[i]*pa[j]*dc_tau(i,j,lh,la,rho)
            grid[(i,j)]=p
            if i>j: H+=p
            elif i==j: D+=p
            else: A+=p
    t=H+D+A
    return H/t, D/t, A/t, grid, t

# ---------- walk-forward: train on everything prior, predict next ----------
model=Model()
preds=[]
for m in rows:
    if model.seen[m['home']]>=6 and model.seen[m['away']]>=6:
        lh,la=model.lam(m['lg'],m['home'],m['away'])
        H,D,A,_,_=probs(lh,la)
        preds.append((m,H,D,A,lh,la))
    model.update(m)

print(f"predictions made (both teams >=6 games): {len(preds):,}")

def brier(ps):
    s=0.0
    for m,H,D,A,_,_ in ps:
        y=(1 if m['res']=='H' else 0, 1 if m['res']=='D' else 0, 1 if m['res']=='A' else 0)
        s+=(H-y[0])**2+(D-y[1])**2+(A-y[2])**2
    return s/len(ps)
def logloss(ps):
    s=0.0
    for m,H,D,A,_,_ in ps:
        p={'H':H,'D':D,'A':A}[m['res']]
        s-=math.log(max(p,1e-12))
    return s/len(ps)

# benchmark: fixed base rate
base=(0.446,0.268,0.286)
bb=sum((base[0]-(m['res']=='H'))**2+(base[1]-(m['res']=='D'))**2+(base[2]-(m['res']=='A'))**2 for m,_,_,_,_,_ in preds)/len(preds)
bl=-sum(math.log({'H':base[0],'D':base[1],'A':base[2]}[m['res']]) for m,_,_,_,_,_ in preds)/len(preds)
print("\n"+"="*80); print("MODEL QUALITY (no odds used anywhere)"); print("="*80)
print(f"  {'':22s} {'Brier':>10s} {'LogLoss':>10s}")
print(f"  {'base rate (44.6/26.8/28.6)':22s} {bb:10.4f} {bl:10.4f}")
print(f"  {'rating model':22s} {brier(preds):10.4f} {logloss(preds):10.4f}")
print(f"  improvement: Brier {(bb-brier(preds))/bb:+.1%}  LogLoss {(bl-logloss(preds))/bl:+.1%}")

# recent-era only
rec=[p for p in preds if p[0]['season']>='1819']
bbr=sum((base[0]-(m['res']=='H'))**2+(base[1]-(m['res']=='D'))**2+(base[2]-(m['res']=='A'))**2 for m,_,_,_,_,_ in rec)/len(rec)
print(f"\n  2018/19->now only (n={len(rec):,}): model Brier {brier(rec):.4f} vs base {bbr:.4f}  ({(bbr-brier(rec))/bbr:+.1%})")

pickle.dump(preds,open("preds.pkl","wb"))
pickle.dump(dict(att=dict(model.att),dfn=dict(model.dfn),hfa=dict(model.hfa),
                 thfa=dict(model.thfa),mu=dict(model.mu)),open("model_state.pkl","wb"))
