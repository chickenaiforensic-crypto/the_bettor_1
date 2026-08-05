"""
DIAGNOSIS SAID: top flight has the LARGEST same-star draw lift (+3.41%) but the
WIDEST within-star ability spread (sd 0.109-0.161 vs 0.082-0.099 lower down).
=> one star covers ~60-70% more real ability in a top flight.
HYPOTHESIS: top flights need FINER buckets. Test bucket count per tier.
Everything chosen on TRAIN, verified on TEST.
"""
import pickle, math, random
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},
      **{l:3 for l in ['E2','E3']}}
TN={1:'top flight',2:'second tier',3:'third/fourth'}
MIN=5; SHRINK=6

def build(nbuckets_by_tier):
    rec=defaultdict(lambda:{'p':0,'w':0,'d':0})
    pool=defaultdict(dict); lgm=defaultdict(lambda:[0.0,0]); out=[]
    for m in rows:
        lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
        key=(lg,se); NB=nbuckets_by_tier[TIER.get(lg,1)]
        lm=lgm[key][0]/lgm[key][1] if lgm[key][1]>0 else 1.35
        vals=sorted(pool[key].values())
        def st(team):
            d=rec[(lg,se,team)]
            if d['p']<MIN or len(vals)<8: return None
            raw=(3*d['w']+d['d'])/d['p']
            v=(raw*d['p']+lm*SHRINK)/(d['p']+SHRINK)
            pct=sum(1 for x in vals if x<v)/len(vals)
            return min(NB,max(1,int(pct*NB)+1))
        sh,sa=st(h),st(a)
        if sh and sa: out.append((m,sh,sa,NB))
        for t,is_h in ((h,True),(a,False)):
            d=rec[(lg,se,t)]
            won=(m['res']=='H' and is_h) or (m['res']=='A' and not is_h)
            d['p']+=1
            if won: d['w']+=1
            elif m['res']=='D': d['d']+=1
            if d['p']>=MIN: pool[key][t]=(3*d['w']+d['d'])/d['p']
        lgm[key][0]+=3 if m['res']!='D' else 2; lgm[key][1]+=2
    return out

def evaluate(dat):
    dat=sorted([(m,s,a,n) for m,s,a,n in dat if K(m) in dc],key=lambda x:x[0]['date'])
    c=int(len(dat)*0.70); TR,TE=dat[:c],dat[c:]
    tt=defaultdict(lambda:[0,0]); base={}
    for m,sh,sa,nb in TR:
        t=TIER.get(m['lg'],1); x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
    for t in (1,2,3):
        v=[m for m,_,_,_ in TR if TIER.get(m['lg'],1)==t]
        base[t]=sum(1 for m in v if m['res']=='D')/len(v) if v else 0.27
    def tab(t,k):
        x=tt.get((t,k)); return x[1]/x[0] if x and x[0]>=150 else base[t]
    W={}
    for t in (1,2,3):
        sub=[(m,sh,sa) for m,sh,sa,_ in TR if TIER.get(m['lg'],1)==t]
        best=(9,0)
        for w in [0,.05,.1,.15,.2,.25,.3,.35,.4,.5]:
            e=sum((((1-w)*dc[K(m)][1]+w*tab(t,sh-sa))-(m['res']=='D'))**2 for m,sh,sa in sub)/len(sub)
            if e<best[0]: best=(e,w)
        W[t]=best[1]
    d=[]
    for m,sh,sa,_ in TE:
        t=TIER.get(m['lg'],1); y=1.0 if m['res']=='D' else 0.0
        p=dc[K(m)][1]; b=(1-W[t])*p+W[t]*tab(t,sh-sa)
        d.append(((p-y)**2-(b-y)**2, t))
    return d,W

def boot(vals,seed=3):
    random.seed(seed); N=len(vals); bs=[]
    for _ in range(15000):
        s=0.0
        for _ in range(300): s+=vals[random.randrange(N)]
        bs.append(s/300)
    bs.sort(); return bs[375],bs[14625]

print("="*84)
print("BUCKET COUNT PER TIER — finer grain where teams are more stratified")
print("="*84)
configs=[({1:5,2:5,3:5},"5/5/5 baseline"),
         ({1:8,2:5,3:5},"8/5/5 finer top flight"),
         ({1:10,2:6,3:5},"10/6/5 graded"),
         ({1:12,2:8,3:6},"12/8/6 fine")]
res={}
for cfg,label in configs:
    dat=build(cfg); d,W=evaluate(dat)
    tot=sum(x for x,_ in d)/len(d)
    per={t:sum(x for x,tt2 in d if tt2==t)/max(1,sum(1 for _,tt2 in d if tt2==t)) for t in (1,2,3)}
    res[label]=(tot,per,d,W)
    print(f"\n  {label}   weights {W}")
    print(f"    overall gain {tot:+.7f}")
    for t in (1,2,3):
        print(f"      {TN[t]:14s} {per[t]:+.7f}")

print("\n"+"="*84); print("BEST CONFIG — significance test"); print("="*84)
bl=max(res,key=lambda k:res[k][0])
tot,per,d,W=res[bl]
print(f"  best on overall gain: {bl}")
vals=[x for x,_ in d]
lo,hi=boot(vals)
dcb=0.19158
print(f"    gain   : {tot:+.7f} ({tot/dcb*100:+.3f}%)")
print(f"    95% CI : [{lo:+.7f}, {hi:+.7f}]  -> {'ROBUST' if lo>0 else 'not significant'}")
for t in (1,2,3):
    v=[x for x,tt2 in d if tt2==t]
    l2,h2=boot(v,seed=t+10)
    print(f"    {TN[t]:14s} n={len(v):6,} gain {sum(v)/len(v):+.7f} CI [{l2:+.7f},{h2:+.7f}] {'SIG' if l2>0 else ''}")
