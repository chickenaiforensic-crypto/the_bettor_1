"""
Chain estimates are a weaker signal than Layer-1 ratings.
So DERIVE tier rates for chain predictions from outcomes, not borrow domestic ones.
Uses the 2,778 cross-border European matches from Study 19.
"""
import pickle, re, glob, math
from collections import defaultdict
import chain as C

line_re=re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)')
ties=[]
for f in sorted(glob.glob("/home/user/chain/ucl/champions-league-master/*/*.txt")):
    yr=int(f.split('/')[-2][:4])
    if yr<2021: continue
    for ln in open(f,encoding='utf-8',errors='replace'):
        m=line_re.match(ln.strip('\r\n'))
        if m and m.group(2)!=m.group(4):
            ties.append((yr,m.group(1).strip(),m.group(3).strip(),int(m.group(5)),int(m.group(6))))
print(f"cross-border matches 2021+: {len(ties):,}")

rows=[]
for yr,h,a,hg,ag in ties:
    r=C.find_chains(h,a,since=f"{yr-4}-01-01")
    if "error" in r: continue
    p2=[c for c in r['phase2'] if c['y1']<=str(yr-1)]
    p3=[c for c in r['phase3'] if c['y1']<=str(yr-1)]
    if not p2 and not p3: continue
    vals=[c['est'] for c in p2]*2+[c['est'] for c in p3]
    allv=[c['est'] for c in p2]+[c['est'] for c in p3]
    m=sum(vals)/len(vals)
    sd=(sum((x-m)**2 for x in allv)/len(allv))**0.5 if len(allv)>1 else None
    contra = bool(p2 and p3 and (min(c['est'] for c in p2)>0)!=(min(c['est'] for c in p3)>0))
    rows.append(dict(est=m,sd=sd,n=len(p2)+len(p3),n2=len(p2),n3=len(p3),
                     contra=contra,res='H' if hg>ag else ('D' if hg==ag else 'A'),gd=hg-ag))
print(f"scoreable: {len(rows):,}")
pickle.dump(rows,open('chain_calib.pkl','wb'))

def wil(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h

print("\n"+"="*92)
print("CHAIN TIER TABLE — measured, not borrowed")
print("="*92)
print(f"  {'chain est band':18s} {'n':>6s} {'HOME':>8s} {'DRAW':>8s} {'AWAY':>8s} {'95% CI home':>18s}")
BANDS=[(-99,-1.0),(-1.0,-0.35),(-0.35,0.35),(0.35,1.0),(1.0,2.0),(2.0,99)]
for lo,hi in BANDS:
    s=[r for r in rows if lo<=r['est']<hi]
    if len(s)<25: continue
    n=len(s); H=sum(1 for r in s if r['res']=='H'); D=sum(1 for r in s if r['res']=='D')
    l,u=wil(H,n)
    print(f"  [{lo:6.2f},{hi:6.2f})   {n:6d} {H/n:8.1%} {D/n:8.1%} {(n-H-D)/n:8.1%}  [{l:.1%},{u:.1%}]")

print("\n"+"="*92)
print("EVIDENCE GRADE — does path count / agreement / contradiction matter?")
print("="*92)
print(f"  {'grade':34s} {'n':>6s} {'direction correct':>18s} {'95% CI':>18s}")
def dircorrect(s):
    dec=[r for r in s if r['res']!='D']
    if not dec: return None,0
    hit=sum(1 for r in dec if (r['est']>0)==(r['res']=='H'))
    return hit/len(dec), len(dec)
for lbl,f in [("all",lambda r:True),
              ("contradiction flagged",lambda r:r['contra']),
              ("no contradiction",lambda r:not r['contra']),
              ("1 path only",lambda r:r['n']==1),
              ("2 paths",lambda r:r['n']==2),
              ("3-5 paths",lambda r:3<=r['n']<=5),
              ("6+ paths",lambda r:r['n']>=6),
              ("has 2nd-phase evidence",lambda r:r['n2']>0),
              ("3rd-phase only",lambda r:r['n2']==0)]:
    s=[r for r in rows if f(r)]
    if len(s)<25: continue
    d,dn=dircorrect(s)
    if d is None: continue
    l,u=wil(int(d*dn),dn)
    print(f"  {lbl:34s} {len(s):6d} {d:18.1%}  [{l:.1%},{u:.1%}]")
