"""Does adding the home-v-home lens improve the model? Fit TRAIN, test HELD-OUT."""
import pickle, math, random
from collections import defaultdict
out,lenses=pickle.load(open("lenses.pkl","rb"))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
idx=[(i,m) for i,(m,_,_,_,_) in enumerate(out) if K(m) in dc]
idx.sort(key=lambda x:x[1]['date'])
c=int(len(idx)*0.70); TR,TE=idx[:c],idx[c:]
print(f"train {len(TR):,}  test {len(TE):,}  (test from {TE[0][1]['date'].date()})")

hvh=lenses['GD HOME-v-HOME']; ava=lenses['GD AWAY-v-AWAY']; std=lenses['GD STANDARD']

def mktab(TR,vec,key,nb=7):
    t=defaultdict(lambda:[0,0.0,0.0])
    for i,m in TR:
        b=max(-3,min(3,int(round(vec[i]))))
        x=t[b]; x[0]+=1
        x[1]+=(1.0 if m['res']=='H' else 0.0)-dc[K(m)][0]
        x[2]+=(1.0 if m['res']=='D' else 0.0)-dc[K(m)][1]
    return {b:(v[1]/v[0],v[2]/v[0]) for b,v in t.items() if v[0]>=300}

TB_h=mktab(TR,hvh,'h'); TB_a=mktab(TR,ava,'a')
print("\nhome-v-home residual corrections (TRAIN):")
for b in sorted(TB_h): print(f"  gap {b:+d}: dH {TB_h[b][0]:+.4f}  dD {TB_h[b][1]:+.4f}")

def score(S,w_h,w_a):
    d=[]
    for i,m in S:
        y=(1.0 if m['res']=='H' else 0.0,1.0 if m['res']=='D' else 0.0,1.0 if m['res']=='A' else 0.0)
        H,D,A=dc[K(m)]
        bh=max(-3,min(3,int(round(hvh[i])))); ba=max(-3,min(3,int(round(ava[i]))))
        ch=TB_h.get(bh,(0,0)); ca=TB_a.get(ba,(0,0))
        H2=H+w_h*ch[0]+w_a*ca[0]; D2=D+w_h*ch[1]+w_a*ca[1]
        H2=max(1e-4,H2); D2=max(1e-4,D2); A2=max(1e-4,1-H2-D2)
        s=H2+D2+A2; H2/=s;D2/=s;A2/=s
        e0=(H-y[0])**2+(D-y[1])**2+(A-y[2])**2
        e1=(H2-y[0])**2+(D2-y[1])**2+(A2-y[2])**2
        d.append(e0-e1)
    return d

print("\n"+"="*72); print("WEIGHT SEARCH ON TRAIN"); print("="*72)
best=(-9,0,0)
for wh in [0,.25,.5,.75,1.0]:
    for wa in [0,.25,.5,.75,1.0]:
        g=sum(score(TR,wh,wa))/len(TR)
        if g>best[0]: best=(g,wh,wa)
print(f"  best on TRAIN: w_homeVhome={best[1]}, w_awayVaway={best[2]}  gain {best[0]:+.7f}")

def boot(d,seed=4):
    random.seed(seed); N=len(d); bs=[]
    for _ in range(20000):
        s=0.0
        for _ in range(300): s+=d[random.randrange(N)]
        bs.append(s/300)
    bs.sort(); return bs[500],bs[19500],sum(1 for x in bs if x<=0)/len(bs)

print("\n"+"="*72); print("HELD-OUT TEST"); print("="*72)
dcb=sum(sum((dc[K(m)][j]-(1.0 if m['res']=='HDA'[j] else 0.0))**2 for j in range(3)) for i,m in TE)/len(TE)
for lbl,wh,wa in [("home-v-home only",best[1],0),("away-v-away only",0,best[2]),
                  ("both lenses",best[1],best[2])]:
    d=score(TE,wh,wa); g=sum(d)/len(d); lo,hi,pn=boot(d)
    print(f"\n  {lbl}  (w={wh},{wa})")
    print(f"    gain {g:+.7f}  ({g/dcb*100:+.3f}%)")
    print(f"    95% CI [{lo:+.7f},{hi:+.7f}]  P(<=0)={pn:.3f}  -> {'ROBUST' if lo>0 else 'not significant'}")
