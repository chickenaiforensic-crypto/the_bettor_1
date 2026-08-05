"""
The decisive test the doc could not run: same spec, unchanged threshold,
every available season 2012-2026 across the three leagues.
n goes from 36 to several hundred. No tuning. Pure out-of-sample.
"""
import csv, math
from datetime import datetime
from scipy import stats

LEAGUES = {"SWE":"Allsvenskan","NOR":"Eliteserien","FIN":"Veikkausliiga"}
MINPRIOR, THRESH = 3, 1.0

def load_all(code):
    out=[]
    with open(f"/home/user/gate1/{code}.csv",encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not r["HG"] or not r["AG"]: continue
            try: d=datetime.strptime(r["Date"],"%d/%m/%Y")
            except: continue
            def fl(k):
                try: return float(r.get(k,"") or "")
                except: return None
            out.append(dict(season=r["Season"],date=d,home=r["Home"].strip(),
                away=r["Away"].strip(),hg=int(r["HG"]),ag=int(r["AG"]),res=r["Res"],
                ch=fl("PSCH") or fl("AvgCH") or fl("B365CH"),
                cd=fl("PSCD") or fl("AvgCD") or fl("B365CD"),
                ca=fl("PSCA") or fl("AvgCA") or fl("B365CA")))
    return out

def run(code):
    rows=load_all(code)
    byseason={}
    for r in rows: byseason.setdefault(r["season"],[]).append(r)
    fired=[]; graded=[]
    for s,ms in byseason.items():
        ms.sort(key=lambda x:x["date"])
        for i,fx in enumerate(ms):
            prior=[m for m in ms if m["date"]<fx["date"]]
            hh=[m for m in prior if m["home"]==fx["home"]]
            aa=[m for m in prior if m["away"]==fx["away"]]
            if len(hh)<MINPRIOR or len(aa)<MINPRIOR: continue
            S6=0.5*(sum(m["hg"] for m in hh)/len(hh))+0.5*(sum(m["hg"] for m in aa)/len(aa))
            S7=0.5*(sum(m["ag"] for m in aa)/len(aa))+0.5*(sum(m["ag"] for m in hh)/len(hh))
            xm=S6-S7
            rec=dict(lg=code,**fx,xm=xm)
            graded.append(rec)
            if xm>=THRESH: fired.append(rec)
    return fired,graded

AF,AG=[],[]
print("="*86)
print("MULTI-SEASON TEST — spec unchanged, threshold unchanged, all seasons")
print("="*86)
print(f"{'League':14s} {'seasons':>8} {'graded':>7} {'fired':>6} {'W':>4} {'D':>4} {'L':>4} {'hit':>7} {'draw%':>7}")
for c,n in LEAGUES.items():
    f,g=run(c); AF+=f; AG+=g
    W=sum(1 for x in f if x["res"]=="H");D=sum(1 for x in f if x["res"]=="D");L=sum(1 for x in f if x["res"]=="A")
    ns=len(set(x["season"] for x in g))
    print(f"{n:14s} {ns:8d} {len(g):7d} {len(f):6d} {W:4d} {D:4d} {L:4d} {W/len(f):7.1%} {D/len(f):7.1%}")

W=sum(1 for x in AF if x["res"]=="H");D=sum(1 for x in AF if x["res"]=="D");L=sum(1 for x in AF if x["res"]=="A");N=len(AF)
print("-"*86)
print(f"{'COMBINED':14s} {'':8s} {len(AG):7d} {N:6d} {W:4d} {D:4d} {L:4d} {W/N:7.1%} {D/N:7.1%}")

def wilson(k,n,z=1.96):
    p=k/n;d=1+z*z/n
    c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h,c+h
lo,hi=wilson(W,N)
print(f"\nHIT RATE {W}/{N} = {W/N:.1%}   95% CI [{lo:.1%}, {hi:.1%}]   (n was 36, now {N})")
print(f"DRAW RATE among fired: {D}/{N} = {D/N:.1%}")

print("\n" + "="*86)
print("THE 2026-ONLY vs ALL-SEASONS COMPARISON")
print("="*86)
f26=[x for x in AF if x["season"]=="2026"]
W26=sum(1 for x in f26 if x["res"]=="H");D26=sum(1 for x in f26 if x["res"]=="D")
print(f"  2026 only (the doc's sample): {W26}/{len(f26)} = {W26/len(f26):.1%}, draw rate {D26/len(f26):.1%}")
oth=[x for x in AF if x["season"]!="2026"]
Wo=sum(1 for x in oth if x["res"]=="H");Do=sum(1 for x in oth if x["res"]=="D")
lo2,hi2=wilson(Wo,len(oth))
print(f"  All OTHER seasons          : {Wo}/{len(oth)} = {Wo/len(oth):.1%} CI [{lo2:.1%},{hi2:.1%}], draw rate {Do/len(oth):.1%}")
odr,p=stats.fisher_exact([[W26,len(f26)-W26],[Wo,len(oth)-Wo]])
print(f"  Fisher exact 2026 vs rest: p={p:.4f}")
pv=stats.binom.cdf(D26,len(f26),Do/len(oth))
print(f"  P(<={D26} draws in {len(f26)} | true draw rate {Do/len(oth):.1%}) = {pv:.4f}")

print("\n" + "="*86)
print("SEASON-BY-SEASON (is 2026 an outlier?)")
print("="*86)
seas={}
for x in AF: seas.setdefault(x["season"],[]).append(x)
print(f"{'season':8s} {'n':>4} {'W':>4} {'D':>4} {'L':>4} {'hit':>8} {'draw%':>8}")
for s in sorted(seas):
    v=seas[s];w=sum(1 for x in v if x["res"]=="H");d=sum(1 for x in v if x["res"]=="D")
    print(f"{s:8s} {len(v):4d} {w:4d} {d:4d} {len(v)-w-d:4d} {w/len(v):8.1%} {d/len(v):8.1%}")

print("\n" + "="*86)
print("BAND TABLE — all seasons, all leagues (is the relationship smooth?)")
print("="*86)
bands=[(-9,-0.3),(-0.3,0),(0,0.3),(0.3,0.6),(0.6,0.8),(0.8,1.0),(1.0,1.2),(1.2,1.5),(1.5,9)]
print(f"{'band':14s} {'n':>5} {'home%':>8} {'draw%':>8} {'away%':>8}")
for lo_,hi_ in bands:
    v=[x for x in AG if lo_<=x["xm"]<hi_]
    if not v: continue
    w=sum(1 for x in v if x["res"]=="H");d=sum(1 for x in v if x["res"]=="D")
    print(f"[{lo_:5.1f},{hi_:5.1f}) {len(v):5d} {w/len(v):8.1%} {d/len(v):8.1%} {(len(v)-w-d)/len(v):8.1%}")

print("\n" + "="*86)
print("THRESHOLD SENSITIVITY — all seasons (does 1.0 still look special?)")
print("="*86)
print(f"{'cut':>6} {'n':>6} {'hit':>8} {'draw%':>8}")
for cut in [0.4,0.6,0.8,1.0,1.2,1.4,1.6,2.0]:
    v=[x for x in AG if x["xm"]>=cut]
    if len(v)<5: continue
    w=sum(1 for x in v if x["res"]=="H");d=sum(1 for x in v if x["res"]=="D")
    print(f"{cut:6.1f} {len(v):6d} {w/len(v):8.1%} {d/len(v):8.1%}")

import pickle; pickle.dump((AF,AG),open("/home/user/gate1/multi.pkl","wb"))
