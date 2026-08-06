import json
import math
from collections import defaultdict

STORE = "audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json"
LEAGUES = [
    "Russian Premier League",
    "Czech First League",
    "England Premier League",
    "Italy Serie A",
    "Germany Bundesliga",
    "France Ligue 1"
]
SEASONS = {l: 2021 for l in LEAGUES}

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
        hfa=max(0.05,min(0.55,hfa))
        hextra[m['homeName']]=max(-0.25,min(0.25,hextra[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att[t]*=(1-DECAY); deff[t]*=(1-DECAY)
        seen[m['homeName']]+=1; seen[m['awayName']]+=1

    for m in train: update(m)
    
    baseline = []
    for m in test:
        y=y_of(m)
        if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
            update(m); continue
        lh,la=predict(m['homeName'], m['awayName'])
        probs=list(grid(lh,la))
        baseline.append({
            "id": m['id'],
            "date": m['dateISO'],
            "home": m['homeName'],
            "away": m['awayName'],
            "prob": [round(x,4) for x in probs],
            "y": y
        })
        update(m)
    return baseline

def main():
    full_baseline = {}
    for lg in LEAGUES:
        full_baseline[lg] = run_league(lg)
    
    with open("audit_work/ladder_baseline_2026-08-05_full.json", "w") as f:
        json.dump({"baseline": full_baseline, "constants": {"LR":LR, "DECAY":DECAY, "HFA_LR":HFA_LR, "RHO":RHO}}, f, indent=2)
    print("Baseline artifact produced.")

if __name__=="__main__":
    main()
