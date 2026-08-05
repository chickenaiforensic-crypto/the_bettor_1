"""
HvH x AvA JOINT ANALYSIS.
  HvH = home team's HOME record  -  away team's HOME record   ("who is better at home")
  AvA = home team's AWAY record  -  away team's AWAY record   ("who is better away")
Both computed prior-only. Then: what does the PAIR tell us that neither tells alone?
"""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
MIN=4
H_rec=defaultdict(lambda:{'p':0,'pts':0,'gf':0,'ga':0})
A_rec=defaultdict(lambda:{'p':0,'pts':0,'gf':0,'ga':0})
data=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    hh,ah = H_rec[(lg,se,h)], H_rec[(lg,se,a)]   # both teams AT HOME
    ha,aa = A_rec[(lg,se,h)], A_rec[(lg,se,a)]   # both teams AWAY
    if min(hh['p'],ah['p'],ha['p'],aa['p'])>=MIN:
        gd=lambda d:(d['gf']-d['ga'])/d['p']
        data.append((m, gd(hh)-gd(ah), gd(ha)-gd(aa)))   # (match, HvH, AvA)
    hp=3 if m['res']=='H' else (1 if m['res']=='D' else 0)
    ap=3 if m['res']=='A' else (1 if m['res']=='D' else 0)
    d=H_rec[(lg,se,h)]; d['p']+=1; d['pts']+=hp; d['gf']+=m['hg']; d['ga']+=m['ag']
    d=A_rec[(lg,se,a)]; d['p']+=1; d['pts']+=ap; d['gf']+=m['ag']; d['ga']+=m['hg']
print(f"fixtures with >= {MIN} home AND away games for both teams: {len(data):,}")
pickle.dump(data,open("hvh_ava.pkl","wb"))

def wil(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    hh=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-hh,c+hh

print("\n"+"="*104)
print("THE JOINT MATRIX — home win % by (HvH band, AvA band)")
print("="*104)
B=[(-99,-0.5),(-0.5,0.0),(0.0,0.5),(0.5,1.0),(1.0,99)]
BL=["<-0.5","-0.5..0","0..0.5","0.5..1.0",">1.0"]
def bi(v):
    for i,(lo,hi) in enumerate(B):
        if lo<=v<hi: return i
    return 4
print(f"  {'':12s}" + "".join(f"{('AvA '+BL[j]):>17s}" for j in range(5)))
cells={}
for i in range(5):
    row=f"  HvH {BL[i]:7s}"
    for j in range(5):
        v=[m for m,h,a in data if bi(h)==i and bi(a)==j]
        cells[(i,j)]=v
        if len(v)<150: row+=f"{'--':>17s}"
        else:
            n=len(v); w=sum(1 for m in v if m['res']=='H')/n
            row+=f"{w:8.1%}({n//1000}k){'':4s}"
    print(row)

print("\n" + "="*104)
print("DRAW % by the same matrix")
print("="*104)
print(f"  {'':12s}" + "".join(f"{('AvA '+BL[j]):>17s}" for j in range(5)))
for i in range(5):
    row=f"  HvH {BL[i]:7s}"
    for j in range(5):
        v=cells[(i,j)]
        if len(v)<150: row+=f"{'--':>17s}"
        else:
            n=len(v); d=sum(1 for m in v if m['res']=='D')/n
            row+=f"{d:8.1%}({n//1000}k){'':4s}"
    print(row)

print("\n"+"="*104)
print("WHAT THE PAIR TELLS YOU — key diagnostic cells")
print("="*104)
def rep(lbl,v):
    if len(v)<150: print(f"  {lbl:44s} n={len(v)} too few"); return
    n=len(v); w=sum(1 for m in v if m['res']=='H'); d=sum(1 for m in v if m['res']=='D')
    lo,hi=wil(w,n)
    print(f"  {lbl:44s} n={n:6,} home {w/n:6.1%} [{lo:.1%},{hi:.1%}] draw {d/n:6.1%} away {(n-w-d)/n:6.1%}")
rep("BOTH strong (HvH>1, AvA>1)",       [m for m,h,a in data if h>1 and a>1])
rep("BOTH weak  (HvH<-0.5, AvA<-0.5)",  [m for m,h,a in data if h<-0.5 and a<-0.5])
rep("HvH strong, AvA weak (>1 / <0)",   [m for m,h,a in data if h>1 and a<0])
rep("HvH weak, AvA strong (<0 / >1)",   [m for m,h,a in data if h<0 and a>1])
rep("BOTH level (|HvH|<0.25,|AvA|<0.25)",[m for m,h,a in data if abs(h)<0.25 and abs(a)<0.25])
