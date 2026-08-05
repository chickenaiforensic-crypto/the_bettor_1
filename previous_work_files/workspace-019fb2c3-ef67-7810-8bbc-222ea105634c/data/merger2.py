"""The real question: does MERGING the star system with the existing home
system beat the home system alone? Blend weight fitted on TRAIN, tested on TEST."""
import pickle, math
from collections import defaultdict
data=pickle.load(open("stardata.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dcmap={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
data.sort(key=lambda x:x[0]['date'])
cut=int(len(data)*0.70); TR,TE=data[:cut],data[cut:]

_f=[math.factorial(i) for i in range(11)]
def dcp(lh,la,rho=-0.06):
    ph=[math.exp(-lh)*lh**i/_f[i] for i in range(11)]
    pa=[math.exp(-la)*la**j/_f[j] for j in range(11)]
    H=D=A=0.
    for i in range(11):
        for j in range(11):
            t=1.
            if i==0 and j==0:t=1-lh*la*rho
            elif i==0 and j==1:t=1+lh*rho
            elif i==1 and j==0:t=1+la*rho
            elif i==1 and j==1:t=1-rho
            p=ph[i]*pa[j]*t
            if i>j:H+=p
            elif i==j:D+=p
            else:A+=p
    s=H+D+A;return H/s,D/s,A/s

cellL=defaultdict(lambda:[0,0.,0.])
for m,sh,sa in TR:
    c=cellL[(sh,sa)];c[0]+=1;c[1]+=m['hg'];c[2]+=m['ag']
gh=sum(m['hg'] for m,_,_ in TR)/len(TR); ga=sum(m['ag'] for m,_,_ in TR)/len(TR)
def star_p(sh,sa):
    c=cellL.get((sh,sa))
    lh,la=(c[1]/c[0],c[2]/c[0]) if c and c[0]>=60 else (gh,ga)
    return dcp(max(.05,lh),max(.05,la))

def score(S,wt):
    s=0;n=0
    for m,sh,sa in S:
        k=K(m)
        if k not in dcmap: continue
        d=dcmap[k]; st=star_p(sh,sa)
        H=(1-wt)*d[0]+wt*st[0]; D=(1-wt)*d[1]+wt*st[1]; A=(1-wt)*d[2]+wt*st[2]
        t=H+D+A; H/=t;D/=t;A/=t
        s+=(H-(m['res']=='H'))**2+(D-(m['res']=='D'))**2+(A-(m['res']=='A'))**2;n+=1
    return s/n

print("="*72); print("MERGER TEST — blend star cells into the home (DC) system"); print("="*72)
print(f"  {'blend weight':>14s} {'TRAIN Brier':>13s} {'TEST Brier':>12s}")
best=(9,0)
for wt in [0,.05,.1,.15,.2,.3,.4,.5,.7,1.0]:
    tr=score(TR,wt); te=score(TE,wt)
    if tr<best[0]: best=(tr,wt)
    mark="  <- best on TRAIN" if wt==best[1] else ""
    print(f"  {wt:14.2f} {tr:13.5f} {te:12.5f}{mark}")
w=best[1]
print(f"\n  weight chosen on TRAIN: {w}")
print(f"  TEST Brier at that weight: {score(TE,w):.5f}")
print(f"  TEST Brier home-system alone: {score(TE,0):.5f}")
d=score(TE,0)-score(TE,w)
print(f"  merger gain: {d/score(TE,0)*100:+.3f}%  ->", "MERGER HELPS" if d>0 else "no gain; DC already contains it")
