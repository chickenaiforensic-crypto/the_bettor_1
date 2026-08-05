"""
Does league-strength adjustment improve chain accuracy?
Blueprint T1 (paired), T3 (rolling origin), T8 (validate before gating).
Adjust each link by the strength gap between the two clubs' leagues.
"""
import pickle, re, glob, math
from collections import defaultdict
import chain as C
strength,ctry=pickle.load(open('league_strength.pkl','rb'))
DEF=sum(strength.values())/len(strength)
S=lambda t: strength.get(ctry.get(t),DEF)

line=re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)')
ties=[]
for f in sorted(glob.glob("/home/user/chain/ucl/champions-league-master/*/*.txt")):
    yr=int(f.split('/')[-2][:4])
    if yr<2021: continue
    for ln in open(f,encoding='utf-8',errors='replace'):
        m=line.match(ln.strip('\r\n'))
        if m and m.group(2)!=m.group(4):
            ties.append((yr,m.group(1).strip(),m.group(3).strip(),int(m.group(5)),int(m.group(6))))

def links(t,since,cut):
    o={}
    for k,v in C.RES[t].items():
        f=[e for e in v if since<=e[0]<=cut]
        if f: o[k]=f
    return o
def gd(l): return sum(g for _,g,_ in l)/len(l)

def build(A,B,since,cut,adj):
    """adj=False: raw GD. adj=True: subtract league-strength gap from each link."""
    oA,oB=links(A,since,cut),links(B,since,cut)
    if not oA or not oB: return []
    sh=set(oA)&set(oB); out=[]
    def link(t,o,lst):
        v=gd(lst)
        return v-(S(t)-S(o)) if adj else v
    for x in sh:
        out.append(('p2',link(A,x,oA[x])-link(B,x,oB[x])))
    if not sh:
        for x in oA:
            if x==B: continue
            oX=links(x,since,cut)
            for y in oX:
                if y in (A,B,x) or y not in oB: continue
                out.append(('p3',link(A,x,oA[x])+link(x,y,oX[y])-link(B,y,oB[y])))
    return out

rows=[]
for yr,h,a,hg,ag in ties:
    A,B=C.resolve(h),C.resolve(a)
    if not A or not B: continue
    since,cut=f"{yr-5}-01-01",f"{yr}-06-29"
    raw=build(A,B,since,cut,False); adj=build(A,B,since,cut,True)
    if len(raw)<2 or len(adj)<2: continue
    r=sum(e for _,e in raw)/len(raw); j=sum(e for _,e in adj)/len(adj)
    rows.append((r,j,'H' if hg>ag else ('D' if hg==ag else 'A'),hg-ag))
print(f"scoreable fixtures: {len(rows):,}")

def corr(x,y):
    n=len(x);mx=sum(x)/n;my=sum(y)/n
    a=sum((p-mx)*(q-my) for p,q in zip(x,y))
    b=math.sqrt(sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))
    return a/b if b else 0
def wil(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h

act=[r[3] for r in rows]; dec=[r for r in rows if r[2]!='D']
print("\n"+"="*72); print("RAW vs LEAGUE-ADJUSTED"); print("="*72)
for lbl,i in [("raw goal difference",0),("LEAGUE-ADJUSTED",1)]:
    hit=sum(1 for r in dec if (r[i]>0)==(r[2]=='H'))
    lo,up=wil(hit,len(dec))
    print(f"  {lbl:22s} r={corr([r[i] for r in rows],act):+.4f}  direction {hit}/{len(dec)} = {hit/len(dec):.1%}  CI [{lo:.1%},{up:.1%}]")

nA=sum(1 for r in dec if ((r[1]>0)==(r[2]=='H')) and not ((r[0]>0)==(r[2]=='H')))
nB=sum(1 for r in dec if ((r[0]>0)==(r[2]=='H')) and not ((r[1]>0)==(r[2]=='H')))
print(f"\n  adjusted right/raw wrong = {nA} | raw right/adjusted wrong = {nB}")
if nA+nB:
    p=2*sum(math.comb(nA+nB,k)*0.5**(nA+nB) for k in range(min(nA,nB)+1))
    print(f"  McNemar exact p = {min(p,1):.4f}")
    print(f"  VERDICT: {'ADJUSTMENT HELPS' if nA>nB and p<0.05 else ('adjustment HURTS' if nB>nA and p<0.05 else 'no significant difference')}")
