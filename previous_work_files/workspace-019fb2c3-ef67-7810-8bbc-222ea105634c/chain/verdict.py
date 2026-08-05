"""
CHAIN TIER + VERDICT SYSTEM — rates measured on 1,302 cross-border outcomes.
Mirrors ENGINE_SPEC Part E/F structure but with chain-specific, evidence-based rates.
"""
import math, pickle
import chain as C

# measured bands (calib_chain.py, n=1302)
TIERS=[("CH-A  Strong home",  2.00,  99, .657,.199,.145,166),
       ("CH-B  Clear home",   1.00, 2.00,.625,.167,.208,192),
       ("CH-C  Slight home",  0.35, 1.00,.551,.200,.249,185),
       ("CH-D  Level",       -0.35, 0.35,.502,.213,.284,211),
       ("CH-E  Slight away", -1.00,-0.35,.397,.248,.355,214),
       ("CH-F  Clear away",    -99,-1.00,.327,.205,.467,336)]
def tier_of(est):
    for name,lo,hi,h,d,a,n in TIERS:
        if lo<=est<hi: return dict(name=name,H=h,D=d,A=a,n=n)
    return dict(name="CH-D  Level",H=.49,D=.212,A=.298,n=208)

def grade(n2,n3,sd,contra):
    """Evidence grade from what was MEASURED to matter: path count and 2nd-phase presence."""
    n=n2+n3
    if n==0: return "NONE"
    if n>=6 and n2>0: return "B+"          # 64.2% dir / 64.0% dir
    if n>=6 or (n>=3 and n2>0): return "B"
    if n>=3: return "C"
    if n==2: return "C-"                   # 58.9% measured
    return "D"                             # single path, 61.9% but n=1

def verdict(tier,grade_,est,sd,contra):
    """What the system actually recommends. Domain = where it is allowed to speak."""
    if grade_ in ("NONE",): return "NO CALL","no path — outside domain"
    if grade_=="D": return "NO CALL","single path — insufficient evidence"
    if grade_=="C-" and abs(est)>1.5:
        return "NO CALL",f"extreme estimate ({est:+.2f}) from only 2 paths — magnitude not supported"
    strong = tier['name'].startswith(("CH-A","CH-B"))
    away   = tier['name'].startswith(("CH-E","CH-F"))
    if strong and grade_ in ("B","B+"): return "HOME LEAN","tier+evidence agree"
    if strong: return "WEAK HOME LEAN","tier says home, evidence thin"
    if away and grade_ in ("B","B+"): return "AVOID HOME","away-leaning"
    if away: return "AVOID HOME","away-leaning, thin"
    return "NO EDGE","level band — no home edge"

_f=[math.factorial(i) for i in range(9)]
def grid(gd,tot=2.65,hfa=1.10,rho=-0.06):
    lh=(tot+gd)/2*math.sqrt(hfa); la=(tot-gd)/2/math.sqrt(hfa)
    lh=max(0.15,min(4.5,lh)); la=max(0.15,min(4.5,la))
    ph=[math.exp(-lh)*lh**i/_f[i] for i in range(9)]
    pa=[math.exp(-la)*la**j/_f[j] for j in range(9)]
    g={}; s=0
    for i in range(9):
        for j in range(9):
            t=1.
            if i==0 and j==0:t=1-lh*la*rho
            elif i==0 and j==1:t=1+lh*rho
            elif i==1 and j==0:t=1+la*rho
            elif i==1 and j==1:t=1-rho
            p=ph[i]*pa[j]*t; g[(i,j)]=p; s+=p
    return {k:v/s for k,v in g.items()},lh,la

def phase4(A,B,since,cap=40):
    """4-hop fallback. Validated 60.4% direction (n=96, CI 50.4-69.6). Grade D4."""
    def rec(t):
        return {o:v for o,v in C.RES[t].items() if [e for e in v if e[0]>=since]}
    oA,oB=rec(A),rec(B)
    if not oA or not oB: return []
    sh=set(oA)&set(oB)
    av=lambda l: sum(g for _,g,_ in l)/len(l)
    out=[]
    for w in list(oA)[:cap]:
        if w in sh or w==B: continue
        oW=rec(w)
        for x in list(oW)[:cap]:
            if x in (A,B,w) or x in sh: continue
            oX=rec(x)
            for y in oX:
                if y in (A,B,w,x) or y in sh or y not in oB: continue
                out.append(av(oA[w])+av(oW[x])+av(oX[y])-av(oB[y]))
    return out

def analyse(h,a,since="2021-01-01"):
    r=C.find_chains(h,a,since=since)
    if "error" in r: return dict(fixture=f"{h} v {a}",domain="OUT",reason=r['error'])
    p2,p3=r['phase2'],r['phase3']
    n2,n3=len(p2),len(p3)
    if n2+n3==0:
        v4=phase4(r['A'],r['B'],since)
        if len(v4)>=3:
            est=sum(v4)/len(v4)
            sd=(sum((x-est)**2 for x in v4)/len(v4))**0.5
            t=tier_of(est)
            g,lh,la=grid(est)
            H=sum(p for (i,j),p in g.items() if i>j); D=sum(p for (i,j),p in g.items() if i==j)
            Aw=sum(p for (i,j),p in g.items() if i<j)
            strong=t['name'].startswith(("CH-A","CH-B")); away=t['name'].startswith(("CH-E","CH-F"))
            v = "WEAK HOME LEAN" if strong else ("AVOID HOME" if away else "NO EDGE")
            return dict(fixture=f"{r['A']} v {r['B']}",domain="IN",est=est,sd=sd,
                        n2=0,n3=0,n4=len(v4),contra=False,tier=t,grade="D4",
                        verdict=v,why="4-hop fallback only (60.4% direction)",
                        H=H,D=D,A=Aw,lh=lh,la=la,g=g,
                        ceiling=t['H'], extrapolated=(H > t['H']+0.02),
                        o25=None, o25_status="WITHHELD: Phase 7 not validated",
                        hm1=sum(p for (i,j),p in g.items() if i-j>1),
                        hm1_status="derived from Phase 6 (validated)",
                        top=sorted(g.items(),key=lambda kv:-kv[1])[:3])
        return dict(fixture=f"{r['A']} v {r['B']}",domain="OUT",
                    reason="no path within 3 hops since "+since,n2=0,n3=0)
    vals=[c['est'] for c in p2]*2+[c['est'] for c in p3]
    allv=[c['est'] for c in p2]+[c['est'] for c in p3]
    est=sum(vals)/len(vals)
    sd=(sum((x-est)**2 for x in allv)/len(allv))**0.5 if len(allv)>1 else None
    contra=bool(p2 and p3 and (min(c['est'] for c in p2)>0)!=(min(c['est'] for c in p3)>0))
    t=tier_of(est); gr=grade(n2,n3,sd,contra); v,why=verdict(t,gr,est,sd,contra)
    g,lh,la=grid(est)
    H=sum(p for (i,j),p in g.items() if i>j); D=sum(p for (i,j),p in g.items() if i==j)
    A=sum(p for (i,j),p in g.items() if i<j)
    # PHASE 6 AUDIT (P6): the modelled probability may exceed the measured tier
    # ceiling. Report BOTH and flag, so the extrapolation is never quoted bare.
    ceiling = t['H']
    extrapolated = H > ceiling + 0.02
    # PHASE 7 (P4): totals are UNVALIDATED -> over/under is withheld entirely.
    return dict(fixture=f"{r['A']} v {r['B']}",domain="IN",est=est,sd=sd,n2=n2,n3=n3,
                contra=contra,tier=t,grade=gr,verdict=v,why=why,
                H=H,D=D,A=A,lh=lh,la=la,g=g,
                ceiling=ceiling, extrapolated=extrapolated,
                o25=None, o25_status="WITHHELD: Phase 7 not validated",
                hm1=sum(p for (i,j),p in g.items() if i-j>1),
                hm1_status="derived from Phase 6 (validated)",
                top=sorted(g.items(),key=lambda kv:-kv[1])[:3])
