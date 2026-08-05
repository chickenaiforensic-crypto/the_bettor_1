"""How fast do ratings decay? Determines required refresh cadence."""
import pickle, math
preds=pickle.load(open("preds.pkl","rb"))
rows=pickle.load(open("all_matches.pkl","rb"))

# order predictions by date; measure Brier as a function of "days since ratings frozen"
preds_sorted=sorted(preds,key=lambda p:p[0]['date'])
base=(0.446,0.268,0.286)
def brier(ps):
    s=0
    for m,H,D,A,_,_ in ps:
        s+=(H-(m['res']=='H'))**2+(D-(m['res']=='D'))**2+(A-(m['res']=='A'))**2
    return s/len(ps)

print("="*76)
print("STALENESS TEST — freeze ratings, then predict N days forward")
print("="*76)
print("Simulates: you refresh the model, then don't refresh again for N days.")
print()
# Re-run model but freeze at checkpoints
import importlib.util
spec=importlib.util.spec_from_file_location("r","/home/user/data/rating.py")
# instead: reuse logic inline
from collections import defaultdict
class M:
    def __init__(s,lr=0.055,decay=0.0022,hl=0.010):
        s.att=defaultdict(float);s.dfn=defaultdict(float)
        s.hfa=defaultdict(lambda:0.26);s.thfa=defaultdict(float)
        s.mu=defaultdict(lambda:0.30);s.lr=lr;s.decay=decay;s.hl=hl;s.seen=defaultdict(int)
    def lam(s,lg,h,a):
        lh=math.exp(s.mu[lg]+s.att[h]-s.dfn[a]+s.hfa[lg]+s.thfa[h])
        la=math.exp(s.mu[lg]+s.att[a]-s.dfn[h])
        return max(.05,min(6,lh)),max(.05,min(6,la))
    def upd(s,m):
        lg,h,a,hg,ag=m['lg'],m['home'],m['away'],m['hg'],m['ag']
        lh,la=s.lam(lg,h,a);eh,ea=hg-lh,ag-la
        kh=s.lr*(1.6 if s.seen[h]<8 else 1);ka=s.lr*(1.6 if s.seen[a]<8 else 1)
        s.att[h]+=kh*eh*.5;s.dfn[a]-=ka*eh*.5;s.att[a]+=ka*ea*.5;s.dfn[h]-=kh*ea*.5
        s.hfa[lg]+=s.hl*(eh-ea)*.02;s.thfa[h]+=s.hl*(eh-ea)*.010;s.thfa[h]*=.999
        s.mu[lg]+=.004*((eh+ea)/2)
        for t in(h,a): s.att[t]*=(1-s.decay);s.dfn[t]*=(1-s.decay)
        s.seen[h]+=1;s.seen[a]+=1
        s.hfa[lg]=max(.05,min(.55,s.hfa[lg]));s.thfa[h]=max(-.25,min(.25,s.thfa[h]))

_f=[math.factorial(i) for i in range(11)]
def tau(i,j,lh,la,rho=-.06):
    if i==0 and j==0: return 1-lh*la*rho
    if i==0 and j==1: return 1+lh*rho
    if i==1 and j==0: return 1+la*rho
    if i==1 and j==1: return 1-rho
    return 1.
def hda(lh,la):
    ph=[math.exp(-lh)*lh**i/_f[i] for i in range(11)]
    pa=[math.exp(-la)*la**j/_f[j] for j in range(11)]
    H=D=A=0.
    for i in range(11):
        for j in range(11):
            p=ph[i]*pa[j]*tau(i,j,lh,la)
            if i>j:H+=p
            elif i==j:D+=p
            else:A+=p
    t=H+D+A;return H/t,D/t,A/t

rows_s=sorted(rows,key=lambda r:r['date'])
# train to a cutoff, then predict forward without updating
from datetime import timedelta
CUT=rows_s[int(len(rows_s)*0.80)]['date']
model=M()
for m in rows_s:
    if m['date']<CUT: model.upd(m)
frozen={ 'att':dict(model.att),'dfn':dict(model.dfn),'hfa':dict(model.hfa),
         'thfa':dict(model.thfa),'mu':dict(model.mu),'seen':dict(model.seen)}
future=[m for m in rows_s if m['date']>=CUT]
print(f"  froze ratings at {CUT.date()}, {len(future):,} future matches available")
print()
print(f"  {'days after freeze':22s} {'n':>7s} {'Brier':>8s} {'vs fresh':>9s} {'vs base':>9s}")
# fresh (continuously updated) comparison from preds
fresh_by_day={}
for m,H,D,A,lh,la in preds_sorted:
    if m['date']>=CUT:
        dd=(m['date']-CUT).days
        fresh_by_day.setdefault(dd,[]).append((m,H,D,A))
for lo,hi in [(0,7),(8,30),(31,60),(61,120),(121,240),(241,400),(401,9999)]:
    sub=[m for m in future if lo<=(m['date']-CUT).days<=hi]
    if len(sub)<300: continue
    # frozen prediction
    bs=0;cnt=0
    for m in sub:
        if m['home'] not in frozen['att'] or m['away'] not in frozen['att']: continue
        lg=m['lg']
        lh=math.exp(frozen['mu'].get(lg,.3)+frozen['att'][m['home']]-frozen['dfn'][m['away']]+frozen['hfa'].get(lg,.26)+frozen['thfa'].get(m['home'],0))
        la=math.exp(frozen['mu'].get(lg,.3)+frozen['att'][m['away']]-frozen['dfn'][m['home']])
        lh=max(.05,min(6,lh));la=max(.05,min(6,la))
        H,D,A=hda(lh,la)
        bs+=(H-(m['res']=='H'))**2+(D-(m['res']=='D'))**2+(A-(m['res']=='A'))**2;cnt+=1
    if cnt<300: continue
    bfroz=bs/cnt
    fr=[x for dd,v in fresh_by_day.items() if lo<=dd<=hi for x in v]
    bfresh=sum((H-(m['res']=='H'))**2+(D-(m['res']=='D'))**2+(A-(m['res']=='A'))**2 for m,H,D,A in fr)/len(fr) if len(fr)>300 else float('nan')
    bb=sum((base[0]-(m['res']=='H'))**2+(base[1]-(m['res']=='D'))**2+(base[2]-(m['res']=='A'))**2 for m in sub)/len(sub)
    print(f"  {str(lo)+'-'+str(hi)+' days':22s} {cnt:7,} {bfroz:8.4f} {bfroz-bfresh:+9.4f} {(bb-bfroz)/bb:+8.1%}")

print()
print("  READ: 'vs fresh' = how much worse frozen ratings are than continuously-updated ones.")
print("        'vs base'  = how much better than a fixed 44.6/26.8/28.6 guess.")
