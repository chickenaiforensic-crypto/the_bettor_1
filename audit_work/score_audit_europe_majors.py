#!/usr/bin/env python3
"""
SCORE AUDIT EUROPE MAJORS — expanded 13,429 domestic major championships (5082+ITA/GER/FRA/SPA/SCO1/KOS)
Runs backtest harness per league: train 2021-22..2024-25, test 2025-26 last omitted season
For owner: Europe for now needs to be strong — major per-country premiere leagues championships first
"""
import json, math
from collections import defaultdict

STORE = "audit_work/pitch-rating-full-13429-europe-majors-2026-08-05.json"
SEASONS = {
    "Russian Premier League": 2021,
    "Czech First League": 2021,
    "England Premier League": 2021,
    "Italy Serie A": 2021,
    "Germany Bundesliga": 2021,
    "France Ligue 1": 2021,
    "Spain La Liga": 2021,
    "Scottish Premiership": 2021,
    "Kosovo Superliga": 2022,  # only 2022:90 2023:90 = 180, so start 2022
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
def y_of(m): return 0 if m['homeGoals']>m['awayGoals'] else (1 if m['homeGoals']==m['awayGoals'] else 2)

def run_league(league, season_start):
    with open(STORE) as f:
        j=json.load(f)
        store=j['store'] if 'store' in j else j
    rows=[m for m in store['matches'] if m['competitionName']==league]
    rows.sort(key=lambda m: m['dateISO'])
    if not rows:
        print(f"== {league} == no rows")
        return None
    cutoff=f"{season_start+4}-07-01"
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

    b=0; marg=[0.0]*3; n=0; refusals=0; diffs=[]
    # for paired
    att2=defaultdict(float); deff2=defaultdict(float); hextra2=defaultdict(float); seen2=defaultdict(int); mu2=MU0; hfa2=HFA0
    def predict2(h,a):
        lh=max(0.05,min(6.0, math.exp(mu2+att2[h]-deff2[a]+hfa2+hextra2[h])))
        la=max(0.05,min(6.0, math.exp(mu2+att2[a]-deff2[h])))
        return lh,la
    def update2(m):
        nonlocal mu2,hfa2
        lh,la=predict2(m['homeName'], m['awayName'])
        eh=m['homeGoals']-lh; ea=m['awayGoals']-la
        kh=LR*(NEW_TEAM_MULT if seen2[m['homeName']]<NEW_TEAM_N else 1.0)
        ka=LR*(NEW_TEAM_MULT if seen2[m['awayName']]<NEW_TEAM_N else 1.0)
        att2[m['homeName']]+=kh*eh*0.5; deff2[m['awayName']]-=ka*eh*0.5
        att2[m['awayName']]+=ka*ea*0.5; deff2[m['homeName']]-=kh*ea*0.5
        hfa2+=HFA_LR*(eh-ea)*0.02; hextra2[m['homeName']]+=HFA_LR*(eh-ea)*0.010; hextra2[m['homeName']]*=0.999; mu2+=0.004*(eh+ea)/2
        hfa2_clamped=max(0.05,min(0.55,hfa2)); hfa2=hfa2_clamped
        hextra2[m['homeName']]=max(-0.25,min(0.25,hextra2[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att2[t]*=(1-DECAY); deff2[t]*=(1-DECAY)
        seen2[m['homeName']]+=1; seen2[m['awayName']]+=1

    for m in train: update2(m)

    for m in test:
        y=y_of(m)
        # base marginals
        # we need marg counts for base
        pass

    # Simplified: compute base marginals from test
    for m in test:
        y=y_of(m)
        marg[y]+=1
    tot=len(test)
    base=[c/tot for c in marg] if tot else [0.33,0.33,0.34]
    b_base=sum(brier(base, y_of(m)) for m in test)/tot if tot else 0

    # Now score
    b=0; bl=0; hits=0; n=0; refusals=0; diffs=[]
    # reset for scoring pass (reuse att2 etc already trained)
    # att2 etc already trained on train, need to reset to train state for scoring
    # redo training for att2 to have clean state
    att2=defaultdict(float); deff2=defaultdict(float); hextra2=defaultdict(float); seen2=defaultdict(int); mu2=MU0; hfa2=HFA0
    for m in train: update2(m)

    for m in test:
        y=y_of(m)
        if seen2[m['homeName']]<MIN_GAMES or seen2[m['awayName']]<MIN_GAMES:
            refusals+=1; update2(m); continue
        lh,la=predict2(m['homeName'], m['awayName'])
        probs=list(grid(lh,la))
        b+=brier(probs,y)
        if max(range(3), key=lambda i: probs[i])==y: hits+=1
        # for paired diff
        diffs.append(brier(base,y)-brier(probs,y))
        n+=1
        update2(m)

    mean=sum(diffs)/len(diffs) if diffs else 0
    import math as _m
    sd=_m.sqrt(sum((x-mean)**2 for x in diffs)/(len(diffs)-1)) if len(diffs)>1 else 0
    se=sd/_m.sqrt(len(diffs)) if diffs else 0
    t=mean/se if se else 0
    p=2*(1-0.5*(1+_m.erf(abs(t)/_m.sqrt(2)))) if se else 1
    gain=(b_base - b/n)/b_base*100 if b_base and n else 0

    print(f"== {league} == train {len(train)} test {len(test)} scored {n} refused {refusals}")
    brier_dc = b/n if n else 0
    dir_acc = hits/n*100 if n else 0
    print(f"  Brier DC {brier_dc:.4f} base {b_base:.4f} gain {gain:+.1f}% dir {dir_acc:.1f}% meanDelta {mean:+.5f} t {t:+.2f} p {p:.4g}")

    return {
        'league': league,
        'train': len(train),
        'test': len(test),
        'scored': n,
        'refused': refusals,
        'brier_dc': b/n if n else 0,
        'brier_base': b_base,
        'gain_pct': gain,
        'dir_acc': hits/n*100 if n else 0,
        'paired_mean': mean,
        't': t,
        'p': p,
    }

if __name__=="__main__":
    results=[]
    for lg, sy in SEASONS.items():
        r=run_league(lg, sy)
        if r:
            results.append(r)
    if results:
        avg=sum(r['gain_pct'] for r in results)/len(results)
        print(f"\nAverage gain across {len(results)} leagues: {avg:+.2f}%")
        for r in results:
            print(f"{r['league']}: gain {r['gain_pct']:+.1f}% n={r['scored']} p={r['p']:.4g}")
