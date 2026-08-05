"""
1) Is HOME-v-HOME a better discriminator than the STANDARD lens?
2) Does it add anything the model does not already have?
Judged as a THRESHOLD system, the way the user framed it.
"""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
data=pickle.load(open("hvh_data.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}

print("="*102)
print("1. HEAD-TO-HEAD: home-v-home  vs  standard (home@home vs away@away)")
print("="*102)
print("  Both scaled to the same coverage. Which threshold picks better home wins?")
hvh=[(m,hh['gd']-ah['gd']) for m,hh,ah,aa,ha in data]
std=[(m,hh['gd']-aa['gd']) for m,hh,ah,aa,ha in data]
print(f"  {'coverage':>9s} | {'HOME-v-HOME':>26s} | {'STANDARD':>26s}")
print(f"  {'':9s} | {'thresh':>7s} {'win%':>7s} {'draw%':>7s} | {'thresh':>7s} {'win%':>7s} {'draw%':>7s}")
for cov in [0.30,0.20,0.15,0.10,0.05,0.03]:
    k=int(len(data)*cov)
    for name,arr in [('h',hvh),('s',std)]:
        s=sorted(arr,key=lambda x:-x[1])[:k]
        w=sum(1 for m,_ in s if m['res']=='H')/k; d=sum(1 for m,_ in s if m['res']=='D')/k
        th=s[-1][1]
        if name=='h': hw,hd,hth=w,d,th
        else: sw,sd,sth=w,d,th
    star=" <<<" if hw>sw else ""
    print(f"  {cov:9.0%} | {hth:7.2f} {hw:7.1%} {hd:7.1%} | {sth:7.2f} {sw:7.1%} {sd:7.1%}{star}")

print("\n"+"="*102)
print("2. DO THEY DISAGREE USEFULLY? cases where the two lenses conflict")
print("="*102)
both=[(m,h,s) for (m,h),(m2,s) in zip(hvh,std)]
agree_hi=[(m,h,s) for m,h,s in both if h>=1.0 and s>=1.0]
only_h  =[(m,h,s) for m,h,s in both if h>=1.0 and s<0.5]
only_s  =[(m,h,s) for m,h,s in both if s>=1.0 and h<0.5]
for lbl,v in [("both lenses say strong",agree_hi),("ONLY home-v-home says strong",only_h),
              ("ONLY standard says strong",only_s)]:
    if len(v)<100: print(f"  {lbl:32s} n={len(v)} too few"); continue
    n=len(v); w=sum(1 for m,_,_ in v if m['res']=='H'); d=sum(1 for m,_,_ in v if m['res']=='D')
    print(f"  {lbl:32s} n={n:6,}  home {w/n:6.1%}  draw {d/n:6.1%}  away {(n-w-d)/n:6.1%}")

print("\n"+"="*102)
print("3. THE DECIDING TEST — does home-v-home add over the MODEL? (paired)")
print("="*102)
have=[(m,h) for m,h in hvh if K(m) in dc]
have.sort(key=lambda x:x[0]['date'])
print(f"  matched: {len(have):,}")
print(f"  {'hvh band':16s} {'n':>7s} {'model P(H)':>11s} {'actual':>8s} {'residual':>10s} {'sig?':>6s}")
def wil(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    hh=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-hh,c+hh
for lo,hi in [(-9,-1.0),(-1.0,-0.5),(-0.5,0),(0,0.5),(0.5,1.0),(1.0,1.5),(1.5,9)]:
    v=[(m,h) for m,h in have if lo<=h<hi]
    if len(v)<400: continue
    n=len(v); mp=sum(dc[K(m)][0] for m,_ in v)/n
    aw=sum(1 for m,_ in v if m['res']=='H'); ac=aw/n
    l,u=wil(aw,n)
    sig = "yes" if not (l<=mp<=u) else ""
    print(f"  [{lo:5.1f},{hi:5.1f})   {n:7,} {mp:11.1%} {ac:8.1%} {ac-mp:+10.1%} {sig:>6s}")
print("  'sig' = model prediction lies OUTSIDE the actual 95% CI -> real unexplained signal")
