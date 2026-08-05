"""
The residuals showed systematic patterns. Test properly:
fit a correction on TRAIN, measure Brier on HELD-OUT TEST. No peeking.
"""
import pickle, math
from collections import defaultdict
preds=pickle.load(open("preds.pkl","rb"))
data=pickle.load(open("stardata.pkl","rb"))
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))

K=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
smap={K(m):(sh,sa) for m,sh,sa in data}
# familiarity
visits=defaultdict(int); fmap={}
for m in rows:
    v=visits[(m['home'],m['away'])]
    fmap[K(m)]=1 if v==0 else 2 if v<=2 else 3 if v<=5 else 4 if v<=10 else 5
    visits[(m['home'],m['away'])]+=1

P=[(m,H,D,A) for m,H,D,A,lh,la in preds]
P.sort(key=lambda x:x[0]['date'])
cut=int(len(P)*0.70)
TR,TE=P[:cut],P[cut:]
print(f"train {len(TR):,}  test {len(TE):,}  (test starts {TE[0][0]['date'].date()})")

def brier(S,adj=None):
    s=0
    for m,H,D,A in S:
        if adj: H,D,A=adj(m,H,D,A)
        s+=(H-(m['res']=='H'))**2+(D-(m['res']=='D'))**2+(A-(m['res']=='A'))**2
    return s/len(S)

base_te=brier(TE)
print(f"\nbaseline model Brier on TEST: {base_te:.5f}")

# ---- fit star-gap correction on TRAIN ----
sg=defaultdict(lambda:[0,0.0,0])
for m,H,D,A in TR:
    s=smap.get(K(m))
    if not s: continue
    g=max(-4,min(4,s[0]-s[1]))
    sg[g][0]+=1; sg[g][1]+=H; sg[g][2]+= (1 if m['res']=='H' else 0)
starcorr={g:(v[2]/v[0]-v[1]/v[0]) for g,v in sg.items() if v[0]>=400}
print("\nstar-gap correction fitted on TRAIN (actual - predicted):")
for g in sorted(starcorr): print(f"  gap {g:+d}: {starcorr[g]:+.4f}  (n={sg[g][0]:,})")

# ---- fit familiarity correction on TRAIN ----
fg=defaultdict(lambda:[0,0.0,0])
for m,H,D,A in TR:
    f=fmap.get(K(m))
    if not f: continue
    fg[f][0]+=1; fg[f][1]+=A; fg[f][2]+=(1 if m['res']=='A' else 0)
famcorr={f:(v[2]/v[0]-v[1]/v[0]) for f,v in fg.items() if v[0]>=400}
print("\nfamiliarity correction fitted on TRAIN (actual - predicted, away win):")
for f in sorted(famcorr): print(f"  fam {f}: {famcorr[f]:+.4f}  (n={fg[f][0]:,})")

def renorm(H,D,A):
    H=max(1e-4,H);D=max(1e-4,D);A=max(1e-4,A);t=H+D+A
    return H/t,D/t,A/t

def adj_star(m,H,D,A):
    s=smap.get(K(m))
    if not s: return H,D,A
    c=starcorr.get(max(-4,min(4,s[0]-s[1])),0.0)
    return renorm(H+c,D,A-c*0.5)
def adj_fam(m,H,D,A):
    f=fmap.get(K(m))
    if not f: return H,D,A
    c=famcorr.get(f,0.0)
    return renorm(H-c*0.5,D,A+c)
def adj_both(m,H,D,A):
    H,D,A=adj_star(m,H,D,A); return adj_fam(m,H,D,A)

print("\n"+"="*80)
print("HELD-OUT TEST — does any correction actually improve Brier?")
print("="*80)
for name,f in [("baseline (no correction)",None),("+ star-gap correction",adj_star),
               ("+ familiarity correction",adj_fam),("+ both",adj_both)]:
    b=brier(TE,f)
    print(f"  {name:28s} Brier {b:.5f}  {'':4s}{(base_te-b)/base_te*100:+.3f}%")

print("\n"+"="*80)
print("SANITY: is the star-gap residual stable, or noise?")
print("="*80)
sg2=defaultdict(lambda:[0,0.0,0])
for m,H,D,A in TE:
    s=smap.get(K(m))
    if not s: continue
    g=max(-4,min(4,s[0]-s[1]))
    sg2[g][0]+=1; sg2[g][1]+=H; sg2[g][2]+=(1 if m['res']=='H' else 0)
print(f"  {'gap':>5s} {'TRAIN resid':>12s} {'TEST resid':>12s} {'same sign?':>11s}")
agree=0;tot=0
for g in sorted(starcorr):
    if g not in sg2 or sg2[g][0]<200: continue
    tr=starcorr[g]; te=sg2[g][2]/sg2[g][0]-sg2[g][1]/sg2[g][0]
    same = (tr>0)==(te>0); agree+=same; tot+=1
    print(f"  {g:>+5d} {tr:+12.4f} {te:+12.4f} {'yes' if same else 'NO':>11s}")
print(f"  -> {agree}/{tot} bands keep their sign out of sample")
