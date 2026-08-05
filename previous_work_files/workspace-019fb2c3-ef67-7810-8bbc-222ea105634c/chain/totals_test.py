"""
TEST 1 (one at a time, as instructed):
Does the chain carry TOTAL GOALS information, or only goal DIFFERENCE?
Current code hardcodes tot=2.65 for every fixture. Test whether that is defensible.
"""
import re, glob, math
from collections import defaultdict
import chain as C

# rebuild results carrying full scoreline
RESW=defaultdict(lambda: defaultdict(list))
for dt,comp,ch,h,ca,a,hg,ag in C.EDGES:
    H,A=C.CANON[C.norm(h)],C.CANON[C.norm(a)]
    RESW[H][A].append((dt,hg,ag)); RESW[A][H].append((dt,ag,hg))

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
    for k,v in RESW[t].items():
        f=[x for x in v if since<=x[0]<=cut]
        if f: o[k]=f
    return o

rows=[]
for yr,h,a,hg,ag in ties:
    A,B=C.resolve(h),C.resolve(a)
    if not A or not B: continue
    since,cut=f"{yr-5}-01-01",f"{yr}-06-29"
    oA,oB=links(A,since,cut),links(B,since,cut)
    if not oA or not oB: continue
    # club-level scoring rates from ALL their matches in window
    aG=[g for v in oA.values() for _,g,_ in v]; aC=[c for v in oA.values() for _,_,c in v]
    bG=[g for v in oB.values() for _,g,_ in v]; bC=[c for v in oB.values() for _,_,c in v]
    if len(aG)<8 or len(bG)<8: continue
    # expected total = home attack + away attack, blended with defences
    exp_tot=(sum(aG)/len(aG)+sum(bC)/len(bC))/2 + (sum(bG)/len(bG)+sum(aC)/len(aC))/2
    rows.append((exp_tot, hg+ag))

print(f"fixtures scored: {len(rows):,}")
def corr(x,y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    a=sum((p-mx)*(q-my) for p,q in zip(x,y))
    b=math.sqrt(sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))
    return a/b if b else 0
est=[r[0] for r in rows]; act=[r[1] for r in rows]
print(f"\n  mean predicted total : {sum(est)/len(est):.2f}")
print(f"  mean ACTUAL total    : {sum(act)/len(act):.2f}")
print(f"  hardcoded constant   : 2.65")
print(f"\n  correlation(predicted total, actual total) r = {corr(est,act):+.4f}")

print("\n  calibration by predicted band:")
print(f"    {'band':14s} {'n':>5s} {'pred':>7s} {'actual':>7s} {'O2.5 rate':>10s}")
for lo,hi in [(0,2.2),(2.2,2.5),(2.5,2.8),(2.8,3.1),(3.1,99)]:
    s=[r for r in rows if lo<=r[0]<hi]
    if len(s)<25: continue
    o25=sum(1 for r in s if r[1]>2.5)/len(s)
    print(f"    [{lo:.1f},{hi:4.1f})    {len(s):5d} {sum(r[0] for r in s)/len(s):7.2f} "
          f"{sum(r[1] for r in s)/len(s):7.2f} {o25:10.1%}")
base=sum(1 for r in rows if r[1]>2.5)/len(rows)
print(f"\n  overall O2.5 rate: {base:.1%}")
