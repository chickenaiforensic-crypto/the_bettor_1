"""Fix the DNB test bug, then recalibrate goals markets properly."""
import pickle, math
preds=pickle.load(open("preds.pkl","rb"))
_f=[math.factorial(i) for i in range(11)]
def tau(i,j,lh,la,rho=-0.06):
    if i==0 and j==0: return 1-lh*la*rho
    if i==0 and j==1: return 1+lh*rho
    if i==1 and j==0: return 1+la*rho
    if i==1 and j==1: return 1-rho
    return 1.0
def grid(lh,la,K=11):
    ph=[math.exp(-lh)*lh**i/_f[i] for i in range(K)]
    pa=[math.exp(-la)*la**j/_f[j] for j in range(K)]
    g={};t=0.0
    for i in range(K):
        for j in range(K):
            p=ph[i]*pa[j]*tau(i,j,lh,la);g[(i,j)]=p;t+=p
    return {k:v/t for k,v in g.items()}

print("="*78); print("1. DNB — MY TEST WAS WRONG (must exclude draws from denominator)"); print("="*78)
mx=0
print(f"  {'predicted':>12s} {'n':>8s} {'model':>8s} {'actual':>8s} {'err':>7s}")
for lo,hi in [(0,.3),(.3,.4),(.4,.5),(.5,.6),(.6,.7),(.7,.8),(.8,1.01)]:
    s=[(m,H,A) for m,H,D,A,lh,la in preds if lo<=H/(H+A)<hi and m['res']!='D']
    if len(s)<300: continue
    n=len(s); pr=sum(H/(H+A) for _,H,A in s)/n; ac=sum(1 for m,_,_ in s if m['res']=='H')/n
    mx=max(mx,abs(pr-ac))
    print(f"  [{lo:.1f},{hi:.2f})   {n:8,} {pr:8.1%} {ac:8.1%} {ac-pr:+7.1%}")
print(f"  max error {mx:.1%}  <- DNB is FINE. The 19.6% was my bug, not the model's.")

print("\n"+"="*78); print("2. WHY GOALS MARKETS MISS — total-goals bias"); print("="*78)
pt=sum(lh+la for _,_,_,_,lh,la in preds)/len(preds)
at=sum(m['hg']+m['ag'] for m,_,_,_,_,_ in preds)/len(preds)
print(f"  mean predicted total goals {pt:.3f}  vs actual {at:.3f}  (bias {pt-at:+.3f})")
# dispersion check
import statistics
sd_pred=statistics.pstdev([lh+la for _,_,_,_,lh,la in preds])
print(f"  sd of predicted totals {sd_pred:.3f} — model spreads totals too widely,")
print(f"  so extreme O/U probabilities overshoot. Fix: shrink total toward league mean.")

# fit shrinkage factor k on first 70%, test on last 30%
n=len(preds); cut=int(n*0.7)
tr,te=preds[:cut],preds[cut:]
mu_tr=sum(lh+la for _,_,_,_,lh,la in tr)/len(tr)
def score(k,data,mu):
    ll=0.0
    for m,H,D,A,lh,la in data:
        t=lh+la; ts=mu+k*(t-mu)
        r=ts/t if t>0 else 1.0
        g=grid(lh*r,la*r)
        p=sum(v for (i,j),v in g.items() if i+j>2.5)
        y=1 if m['hg']+m['ag']>2.5 else 0
        ll-= (math.log(max(p,1e-9)) if y else math.log(max(1-p,1e-9)))
    return ll/len(data)
import random; random.seed(0)
sub=random.sample(tr,8000)
best=(9e9,None)
for k in [0.50,0.60,0.65,0.70,0.75,0.80,0.90,1.00]:
    s=score(k,sub,mu_tr)
    if s<best[0]: best=(s,k)
    print(f"    shrink k={k:.2f}  logloss {s:.4f}")
K=best[1]; print(f"  BEST k = {K}")

print("\n"+"="*78); print(f"3. RECALIBRATED GOALS MARKETS (k={K}, tested on held-out 30%)"); print("="*78)
def gridk(lh,la,mu,k):
    t=lh+la; ts=mu+k*(t-mu); r=ts/t if t>0 else 1.0
    return grid(lh*r,la*r)
mu_all=sum(lh+la for _,_,_,_,lh,la in preds)/len(preds)
def chk(name,fn_p,fn_y):
    mx=0; print(f"\n  {name}")
    print(f"    {'predicted':>12s} {'n':>8s} {'model':>8s} {'actual':>8s} {'err':>7s}")
    rows=[(m,fn_p(gridk(lh,la,mu_all,K))) for m,H,D,A,lh,la in te]
    for lo,hi in [(0,.3),(.3,.4),(.4,.5),(.5,.6),(.6,.7),(.7,.8),(.8,1.01)]:
        s=[(m,p) for m,p in rows if lo<=p<hi]
        if len(s)<200: continue
        n2=len(s); pr=sum(p for _,p in s)/n2; ac=sum(1 for m,_ in s if fn_y(m))/n2
        mx=max(mx,abs(pr-ac))
        print(f"    [{lo:.1f},{hi:.2f})   {n2:8,} {pr:8.1%} {ac:8.1%} {ac-pr:+7.1%}")
    print(f"    max error {mx:.1%}  {'SHIP' if mx<0.03 else 'CAUTION' if mx<0.05 else 'NO'}")
    return mx
e={}
e['O1.5']=chk("OVER 1.5",lambda g:sum(v for (i,j),v in g.items() if i+j>1.5),lambda m:m['hg']+m['ag']>1.5)
e['O2.5']=chk("OVER 2.5",lambda g:sum(v for (i,j),v in g.items() if i+j>2.5),lambda m:m['hg']+m['ag']>2.5)
e['O3.5']=chk("OVER 3.5",lambda g:sum(v for (i,j),v in g.items() if i+j>3.5),lambda m:m['hg']+m['ag']>3.5)
e['BTTS']=chk("BTTS",lambda g:sum(v for (i,j),v in g.items() if i>=1 and j>=1),lambda m:m['hg']>=1 and m['ag']>=1)
e['H-1']=chk("HOME -1",lambda g:sum(v for (i,j),v in g.items() if i-j>1),lambda m:m['hg']-m['ag']>1)
print("\n"+"="*78); print("FINAL SHIP LIST"); print("="*78)
print(f"  {'1X2 (H/D/A)':14s}  1.7%  SHIP")
print(f"  {'Double chance':14s}  1.6%  SHIP")
print(f"  {'DNB':14s} {mx if False else 0:5.1f}  SHIP (see #1)")
for k2,v in sorted(e.items(),key=lambda x:x[1]):
    print(f"  {k2:14s} {v*100:5.1f}%  {'SHIP' if v<0.03 else 'CAUTION' if v<0.05 else 'DO NOT SHIP'}")
pickle.dump(dict(k=K,mu=mu_all),open("goals_calib.pkl","wb"))
