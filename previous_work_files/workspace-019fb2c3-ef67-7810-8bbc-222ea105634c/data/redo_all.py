"""Re-test EVERY system I rejected, using the correct paired test."""
import pickle, math
from collections import defaultdict
def paired(d,label,invert=False):
    N=len(d); m=sum(d)/N
    sd=math.sqrt(sum((x-m)**2 for x in d)/(N-1)); se=sd/math.sqrt(N)
    t=m/se if se else 0
    p=2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2))))
    verdict = "SIGNIF BETTER" if (p<0.05 and m>0) else ("SIGNIF WORSE" if (p<0.05 and m<0) else "not significant")
    print(f"  {label:34s} {m:+.8f}  t={t:+6.2f}  p={p:.4f}  {verdict}")
    return m,p

preds=pickle.load(open("preds.pkl","rb"))
K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
dc={K(m):(H,D,A) for m,H,D,A,lh,la in preds}
TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},**{l:3 for l in ['E2','E3']}}

print("="*88); print("RE-TESTING EVERYTHING WITH THE CORRECT PAIRED TEST"); print("="*88)

# ---------- 1. star draw tables, per tier ----------
v2=pickle.load(open("stars_v2.pkl","rb"))
star={K(m):(sh,sa) for m,sh,sa in v2}
rec=sorted([m for m,_,_ in v2 if K(m) in dc],key=lambda m:m['date'])
c=int(len(rec)*0.70); TR,TE=rec[:c],rec[c:]
tt=defaultdict(lambda:[0,0]); base={}
for m in TR:
    t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
for t in (1,2,3):
    v=[m for m in TR if TIER.get(m['lg'],1)==t]; base[t]=sum(1 for m in v if m['res']=='D')/len(v)
def stab(t,k):
    x=tt.get((t,k)); return x[1]/x[0] if x and x[0]>=150 else base[t]
W={1:0.2,2:0.5,3:0.5}
print("\nSTAR SYSTEM (per-tier calibrated):")
d=[]
for m in TE:
    H,D,A=dc[K(m)]; t=TIER.get(m['lg'],1); sh,sa=star[K(m)]
    D2=(1-W[t])*D+W[t]*stab(t,sh-sa); y=1.0 if m['res']=='D' else 0.0
    d.append((D-y)**2-(D2-y)**2)
paired(d,"draw probability")
for t in (1,2,3):
    dd=[]
    for m in TE:
        if TIER.get(m['lg'],1)!=t: continue
        H,D,A=dc[K(m)]; sh,sa=star[K(m)]
        D2=(1-W[t])*D+W[t]*stab(t,sh-sa); y=1.0 if m['res']=='D' else 0.0
        dd.append((D-y)**2-(D2-y)**2)
    paired(dd,f"  draw, tier {t}")

# ---------- 2. home-v-home lens ----------
out,lenses=pickle.load(open("lenses.pkl","rb"))
gh=lenses['GD HOME-v-HOME']; ga=lenses['GD AWAY-v-AWAY']
hvh={}; ava={}
for i,(m,_,_,_,_) in enumerate(out): hvh[K(m)]=gh[i]; ava[K(m)]=ga[i]
idx=sorted([m for m,_,_,_,_ in out if K(m) in dc],key=lambda m:m['date'])
c2=int(len(idx)*0.70); TR2,TE2=idx[:c2],idx[c2:]
def lens_tab(TR2,vec):
    t=defaultdict(lambda:[0,0.0])
    for m in TR2:
        b=max(-3,min(3,int(round(vec[K(m)]))))
        x=t[b]; x[0]+=1; x[1]+=(1.0 if m['res']=='H' else 0.0)-dc[K(m)][0]
    return {b:v[1]/v[0] for b,v in t.items() if v[0]>=300}
LTh=lens_tab(TR2,hvh); LTa=lens_tab(TR2,ava)
print("\nVENUE LENSES:")
for nm,vec,LT in [("home-v-home",hvh,LTh),("away-v-away",ava,LTa)]:
    for w in [0.25,0.5]:
        d=[]
        for m in TE2:
            H,D,A=dc[K(m)]
            b=max(-3,min(3,int(round(vec[K(m)]))))
            H2=max(1e-4,H+w*LT.get(b,0.0)); A2=max(1e-4,1-H2-D); s=H2+D+A2
            H2/=s; A2/=s; D2=D/s
            y=(1.0 if m['res']=='H' else 0.,1.0 if m['res']=='D' else 0.,1.0 if m['res']=='A' else 0.)
            d.append(((H-y[0])**2+(D-y[1])**2+(A-y[2])**2)-((H2-y[0])**2+(D2-y[1])**2+(A2-y[2])**2))
        paired(d,f"{nm} w={w} (full 1X2)")

print("\n"+"="*88)
print("WHAT CHANGED, AND WHY")
print("="*88)
print("""  Unpaired bootstrap resamples matches, so each resample contains a DIFFERENT
  set of matches. Match-to-match variance (sd 0.289) swamps the model difference.

  Paired test uses the SAME matches for both models and looks only at the
  per-match DIFFERENCE (sd 0.012). That is 23x less noisy.

  Both models get Arsenal-Chelsea right or wrong together; only the small
  disagreement matters. My bootstrap threw that structure away.""")
