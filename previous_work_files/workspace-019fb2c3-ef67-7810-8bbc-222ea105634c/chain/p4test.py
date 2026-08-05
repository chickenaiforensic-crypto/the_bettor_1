"""Do 4-hop chains carry signal? Blueprint T8: validate before gating on it."""
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

def avg(l): return sum(g for _,g,_ in l)/len(l)

def p4(A,B,cut,since):
    """4-hop: A-w, w-x, x-y, y-B  -> too many; use A-w, w-x, x-B (3 intermediate hops = phase4)"""
    def rec(t):
        return {o:[e for e in v if since<=e[0]<=cut] for o,v in C.RES[t].items()
                if [e for e in v if since<=e[0]<=cut]}
    oA,oB=rec(A),rec(B)
    if not oA or not oB: return []
    sh=set(oA)&set(oB)
    out=[]
    for w in list(oA)[:40]:
        if w in sh or w==B: continue
        oW=rec(w)
        for x in list(oW)[:40]:
            if x in (A,B,w) or x in sh: continue
            oX=rec(x)
            for y in oX:
                if y in (A,B,w,x) or y in sh or y not in oB: continue
                out.append(avg(oA[w])+avg(oW[x])+avg(oX[y])-avg(oB[y]))
    return out

rows=[]
for yr,h,a,hg,ag in ties[:900]:
    A,B=C.resolve(h),C.resolve(a)
    if not A or not B: continue
    cut=f"{yr-1}-12-31"; since=f"{yr-5}-01-01"
    r=C.find_chains(h,a,since=since)
    if "error" in r: continue
    p2=[c for c in r['phase2'] if c['y1']<=str(yr-1)]
    p3=[c for c in r['phase3'] if c['y1']<=str(yr-1)]
    if p2 or p3: continue                      # only test where 2/3 FAIL
    v4=p4(A,B,cut,since)
    if len(v4)<2: continue
    m=sum(v4)/len(v4)
    rows.append((m,len(v4),'H' if hg>ag else ('D' if hg==ag else 'A')))
print(f"fixtures where p2/p3 failed but p4 found paths: {len(rows)}")
if len(rows)>=25:
    dec=[r for r in rows if r[2]!='D']
    hit=sum(1 for r in dec if (r[0]>0)==(r[2]=='H'))
    def wil(k,n,z=1.96):
        p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
        h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h
    lo,up=wil(hit,len(dec))
    print(f"  direction correct: {hit}/{len(dec)} = {hit/len(dec):.1%}  CI [{lo:.1%},{up:.1%}]")
    print(f"  -> {'USABLE' if lo>0.5 else 'NOT USABLE — CI includes coin-flip'}")
else:
    print("  too few cases to validate 4th phase")
