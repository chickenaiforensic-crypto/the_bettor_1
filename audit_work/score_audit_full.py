#!/usr/bin/env python3
"""
SCORE AUDIT FULL — expanded 10,209-row store (5082 + ITA 1900 + GER 1530 + FRA 1678 + playoffs)
Runs backtest harness per league: train 2021-22..2024-25, test 2025-26 last omitted season
Metrics: Brier DC vs base, logloss, dir, paired T1, MDE80 T2, full T4 per-side, O2.5/BTTS I3
Claims to verify: Average Gain +8.70% across 6 leagues, ITA +9.0% n=374 p<0.01, GER +11.7% n=300 p<0.001, FRA +6.9% n=300 p<0.05
"""
import json, math
from collections import defaultdict

STORE = "audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json"
SEASONS = {
    "Russian Premier League": 2021,
    "Czech First League": 2021,
    "England Premier League": 2021,
    "Italy Serie A": 2021,
    "Germany Bundesliga": 2021,
    "France Ligue 1": 2021,
}
LR, DECAY, HFA_LR, RHO = 0.055, 0.0022, 0.010, -0.06
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8
MU0, HFA0 = 0.45, 0.25
MIN_GAMES = 6

def pmf(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)
def grid(lh, la):
    n=10
    p=[[0.0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        for j in range(n+1):
            t=1.0
            if i==0 and j==0: t=1-lh*la*RHO
            elif i==0 and j==1: t=1+lh*RHO
            elif i==1 and j==0: t=1+la*RHO
            elif i==1 and j==1: t=1-RHO
            p[i][j]=pmf(i,lh)*pmf(j,la)*t
    s=sum(sum(r) for r in p)
    ph=sum(p[i][j] for i in range(n+1) for j in range(n+1) if i>j)/s
    pd=sum(p[i][i] for i in range(n+1))/s
    return ph, pd, 1-ph-pd

def brier(probs,y): return sum((pr-(1.0 if i==y else 0.0))**2 for i,pr in enumerate(probs))
def logloss(probs,y): return -math.log(max(probs[y],1e-9))
def y_of(m): return 0 if m['homeGoals']>m['awayGoals'] else (1 if m['homeGoals']==m['awayGoals'] else 2)

def run_league(league):
    with open(STORE) as f:
        j=json.load(f)
        store=j['store'] if 'store' in j else j
    rows=[m for m in store['matches'] if m['competitionName']==league]
    rows.sort(key=lambda m: m['dateISO'])
    cutoff=f"{SEASONS[league]+4}-07-01"
    train=[m for m in rows if m['dateISO']<cutoff]
    test=[m for m in rows if m['dateISO']>=cutoff]

    att=defaultdict(float); deff=defaultdict(float); hextra=defaultdict(float); seen=defaultdict(int); mu=MU0; hfa=HFA0
    def predict(h,a):
        lh=max(0.05,min(6.0, math.exp(mu+att[h]-deff[a]+hfa+hextra[h])))
        la=max(0.05,min(6.0, math.exp(mu+att[a]-deff[h])))
        return lh,la
    def update(m):
        nonlocal mu,hfa
        lh,la=predict(m['homeName'], m['awayName'])
        eh=m['homeGoals']-lh; ea=m['awayGoals']-la
        kh=LR*(NEW_TEAM_MULT if seen[m['homeName']]<NEW_TEAM_N else 1.0)
        ka=LR*(NEW_TEAM_MULT if seen[m['awayName']]<NEW_TEAM_N else 1.0)
        att[m['homeName']]+=kh*eh*0.5; deff[m['awayName']]-=ka*eh*0.5
        att[m['awayName']]+=ka*ea*0.5; deff[m['homeName']]-=kh*ea*0.5
        hfa+=HFA_LR*(eh-ea)*0.02; hextra[m['homeName']]+=HFA_LR*(eh-ea)*0.010; hextra[m['homeName']]*=0.999; mu+=0.004*(eh+ea)/2
        hfa_clamped=max(0.05,min(0.55,hfa)); hfa=hfa_clamped
        hextra[m['homeName']]=max(-0.25,min(0.25,hextra[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att[t]*=(1-DECAY); deff[t]*=(1-DECAY)
        seen[m['homeName']]+=1; seen[m['awayName']]+=1

    for m in train: update(m)

    b=bl=hits=n=0
    diffs=[]
    refusals=0
    marg=[0.0]*3
    for m in test:
        y=y_of(m); marg[y]+=1
        if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
            refusals+=1; update(m); continue
        lh,la=predict(m['homeName'], m['awayName'])
        probs=list(grid(lh,la))
        b+=brier(probs,y); bl+=logloss(probs,y)
        if max(range(3), key=lambda i: probs[i])==y: hits+=1
        # base = marginals of test window
        n+=1
        update(m)

    tot=len(test)
    base=[c/tot for c in marg]
    # compute base brier: for each test match, brier of base marginals
    b_base=sum(brier(base, y_of(m)) for m in test)/tot if tot else 0
    # paired per-match deltas for T1 (base - DC) positive = DC better
    # need per-match diffs: we already have b per match? Recompute for diffs
    # redo quickly for diffs
    # reset state for diff calc? Simpler compute diffs from earlier loop: we need per-match base brier vs DC brier
    # We'll recompute second pass for paired
    # For brevity, we will do second pass training again
    att=defaultdict(float); deff=defaultdict(float); hextra=defaultdict(float); seen=defaultdict(int); mu=MU0; hfa=HFA0
    for m in train: update(m)  # update uses outer att etc — need to redo with fresh defs, so we will redo full second pass below

    # Actually redo full second pass to get diffs
    att=defaultdict(float); deff=defaultdict(float); hextra=defaultdict(float); seen=defaultdict(int); mu=MU0; hfa=HFA0
    def predict2(h,a):
        lh=max(0.05,min(6.0, math.exp(mu+att[h]-deff[a]+hfa+hextra[h])))
        la=max(0.05,min(6.0, math.exp(mu+att[a]-deff[h])))
        return lh,la
    def update2(m):
        nonlocal mu,hfa
        lh,la=predict2(m['homeName'], m['awayName'])
        eh=m['homeGoals']-lh; ea=m['awayGoals']-la
        kh=LR*(NEW_TEAM_MULT if seen[m['homeName']]<NEW_TEAM_N else 1.0)
        ka=LR*(NEW_TEAM_MULT if seen[m['awayName']]<NEW_TEAM_N else 1.0)
        att[m['homeName']]+=kh*eh*0.5; deff[m['awayName']]-=ka*eh*0.5
        att[m['awayName']]+=ka*ea*0.5; deff[m['homeName']]-=kh*ea*0.5
        hfa+=HFA_LR*(eh-ea)*0.02; hextra[m['homeName']]+=HFA_LR*(eh-ea)*0.010; hextra[m['homeName']]*=0.999; mu+=0.004*(eh+ea)/2
        hfa_clamped=max(0.05,min(0.55,hfa)); hfa=hfa_clamped
        hextra[m['homeName']]=max(-0.25,min(0.25,hextra[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att[t]*=(1-DECAY); deff[t]*=(1-DECAY)
        seen[m['homeName']]+=1; seen[m['awayName']]+=1

    for m in train: update2(m)
    diffs=[]
    for m in test:
        y=y_of(m)
        if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
            update2(m); continue
        lh,la=predict2(m['homeName'], m['awayName'])
        probs=list(grid(lh,la))
        b_dc=brier(probs,y)
        b_bs=brier(base,y)
        diffs.append(b_bs-b_dc)  # positive = DC better
        update2(m)

    mean=sum(diffs)/len(diffs) if diffs else 0
    sd=math.sqrt(sum((x-mean)**2 for x in diffs)/(len(diffs)-1)) if len(diffs)>1 else 0
    se=sd/math.sqrt(len(diffs)) if diffs else 0
    t=mean/se if se else 0
    # two-sided p approx via erf (for large n, t~normal)
    p=2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2)))) if se else 1
    mde=2.8*sd/math.sqrt(len(diffs)) if diffs else 0
    gain = (b_base - b/n)/b_base*100 if b_base and n else 0

    print(f"== {league} == train {len(train)} test {len(test)} scored {n} refused {refusals}")
    print(f"  Brier DC {b/n:.4f} base {b_base:.4f} gain {gain:+.1f}% logloss {bl/n:.4f} dir {hits/n*100:.1f}%")
    print(f"  Paired meanDelta {mean:+.5f} sd {sd:.4f} se {se:.4f} t {t:+.2f} p {p:.4g} MDE80 {mde:.5f} {'BETTER' if mean>0 and p<0.05 else ''}")
    return {
        'league': league,
        'train': len(train),
        'test': len(test),
        'scored': n,
        'refused': refusals,
        'brier_dc': b/n if n else 0,
        'brier_base': b_base,
        'gain_pct': gain,
        'logloss': bl/n if n else 0,
        'dir_acc': hits/n*100 if n else 0,
        'paired_mean': mean,
        'paired_sd': sd,
        'paired_se': se,
        't': t,
        'p': p,
        'mde80': mde,
    }

if __name__=="__main__":
    results=[]
    for lg in ("Russian Premier League","Czech First League","England Premier League","Italy Serie A","Germany Bundesliga","France Ligue 1"):
        r=run_league(lg)
        if r:
            results.append(r)
    if results:
        avg_gain=sum(r['gain_pct'] for r in results)/len(results)
        print(f"\n=== SUMMARY ===")
        print(f"Average gain across {len(results)} leagues: {avg_gain:+.2f}%")
        for r in results:
            print(f"{r['league']}: gain {r['gain_pct']:+.1f}% n={r['scored']} p={r['p']:.4g} {'SIGNIFICANT' if r['p']<0.05 else ''}")
