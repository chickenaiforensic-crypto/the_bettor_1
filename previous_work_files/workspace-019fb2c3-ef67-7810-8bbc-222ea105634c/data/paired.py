"""
THE REAL ERROR: I bootstrapped the ABSOLUTE Brier difference, which carries the
full match-to-match variance. The correct test for two models on the SAME matches
is a PAIRED test on per-match differences - variance mostly cancels.
Redo Study 11's star result properly.
"""
import pickle, math, random
from collections import defaultdict
v2=pickle.load(open("stars_v2.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},**{l:3 for l in ['E2','E3']}}
star={K(m):(sh,sa) for m,sh,sa in v2}
rec=sorted([m for m,_,_ in v2 if K(m) in dc],key=lambda m:m['date'])
c=int(len(rec)*0.70); TR,TE=rec[:c],rec[c:]
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

# paired per-match DRAW brier differences
d=[]
for m in TE:
    H,D,A=dc[K(m)]
    t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    D2=(1-W[t])*D+W[t]*stab(t,sh-sa)
    y=1.0 if m['res']=='D' else 0.0
    d.append((D-y)**2-(D2-y)**2)
N=len(d); mean=sum(d)/N
sd=math.sqrt(sum((x-mean)**2 for x in d)/(N-1))
se=sd/math.sqrt(N)
t_stat=mean/se
print("="*78)
print("PAIRED TEST — draw probability, star table vs base (same matches)")
print("="*78)
print(f"  n = {N:,}")
print(f"  mean per-match improvement : {mean:+.8f}")
print(f"  sd of the DIFFERENCE       : {sd:.6f}   <- tiny, because it's paired")
print(f"  standard error             : {se:.8f}")
print(f"  t statistic                : {t_stat:+.3f}")
p=2*(1-0.5*(1+math.erf(abs(t_stat)/math.sqrt(2))))
print(f"  two-sided p-value          : {p:.6f}")
print(f"  95% CI                     : [{mean-1.96*se:+.8f}, {mean+1.96*se:+.8f}]")
print(f"  -> {'SIGNIFICANT' if p<0.05 else 'not significant'}")
print()
print("  COMPARE: my earlier unpaired bootstrap gave CI [-0.00124,+0.00157]")
print(f"           the paired CI is {((1.96*se)/0.00124):.3f}x as wide  -> {(0.00124/(1.96*se)):.0f}x MORE PRECISE")

# now the full 1X2 paired
d2=[]
for m in TE:
    H,D,A=dc[K(m)]
    t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    D2=(1-W[t])*D+W[t]*stab(t,sh-sa)
    H2=max(1e-4,H); A2=max(1e-4,1-H2-D2); s=H2+D2+A2; H2/=s;D2/=s;A2/=s
    y=(1.0 if m['res']=='H' else 0.,1.0 if m['res']=='D' else 0.,1.0 if m['res']=='A' else 0.)
    e0=(H-y[0])**2+(D-y[1])**2+(A-y[2])**2
    e1=(H2-y[0])**2+(D2-y[1])**2+(A2-y[2])**2
    d2.append(e0-e1)
N2=len(d2); m2=sum(d2)/N2
sd2=math.sqrt(sum((x-m2)**2 for x in d2)/(N2-1)); se2=sd2/math.sqrt(N2)
t2=m2/se2
p2=2*(1-0.5*(1+math.erf(abs(t2)/math.sqrt(2))))
print("\n"+"="*78)
print("PAIRED TEST — FULL 1X2")
print("="*78)
print(f"  mean per-match change : {m2:+.8f}")
print(f"  t = {t2:+.3f}   p = {p2:.6f}")
print(f"  95% CI [{m2-1.96*se2:+.8f}, {m2+1.96*se2:+.8f}]")
print(f"  -> {'SIGNIFICANTLY WORSE' if (p2<0.05 and m2<0) else ('SIGNIFICANTLY BETTER' if p2<0.05 else 'not significant')}")
