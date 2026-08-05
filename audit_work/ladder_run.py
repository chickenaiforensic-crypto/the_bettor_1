#!/usr/bin/env python3
"""LADDER RUN — owner's test-run protocol on the 5,082 store (2026-08-05).

L-1: hold out the NEWEST 1 game of the last full season; train on all before; score.
L-2: hold out the newest 2; retrain; score.
L-n: expanding holdout (3,5,8,10,15,20,25,30) ...
FULL: hold out the entire last season.
Artifact written: audit_work/ladder_baseline_2026-08-05.json
"""
import json, math, sys
from collections import defaultdict

STORE = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json"
SEASONS = {"Russian Premier League": 2021, "Czech First League": 2021, "England Premier League": 2021}
HOLDOUTS = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, "FULL"]

LR, DECAY, HFA_LR, RHO = 0.055, 0.0022, 0.010, -0.06
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8
MU0, HFA0 = 0.45, 0.25
MIN_GAMES = 6

def pmf(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)

def grid(lam_h, lam_a):
    n = 10
    p = [[0.0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        for j in range(n+1):
            t = 1.0
            if i == 0 and j == 0: t = 1 - lam_h*lam_a*RHO
            elif i == 0 and j == 1: t = 1 + lam_h*RHO
            elif i == 1 and j == 0: t = 1 + lam_a*RHO
            elif i == 1 and j == 1: t = 1 - RHO
            p[i][j] = pmf(i, lam_h)*pmf(j, lam_a)*t
    s = sum(sum(r) for r in p)
    ph = sum(p[i][j] for i in range(n+1) for j in range(n+1) if i > j)/s
    pd = sum(p[i][i] for i in range(n+1))/s
    return ph, pd, 1-ph-pd

def outcome(probs):
    return max(range(3), key=lambda i: probs[i])

def brier(probs, y): return sum((p-(1.0 if i==y else 0.0))**2 for i,p in enumerate(probs))
def logloss(probs, y): return -math.log(max(probs[y], 1e-9))

def y_of(m):
    return 0 if m['homeGoals'] > m['awayGoals'] else (1 if m['homeGoals'] == m['awayGoals'] else 2)

def run_ladder(league):
    with open(STORE) as f:
        store = json.load(f)['store']
    rows = [m for m in store['matches'] if m['competitionName'] == league]
    rows.sort(key=lambda m: m['dateISO'])
    cutoff = f"{SEASONS[league]+4}-07-01"
    train_all = [m for m in rows if m['dateISO'] < cutoff]
    test_season = [m for m in rows if m['dateISO'] >= cutoff]
    res = {}
    for h in HOLDOUTS:
        nhold = len(test_season) if h == "FULL" else h
        train = train_all + test_season[:-nhold]
        test = test_season[-nhold:]
        att, deff, hextra, seen = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(int)
        mu, hfa = MU0, HFA0
        def predict(home, away):
            lh = max(0.05, min(6.0, math.exp(mu + att[home] - deff[away] + hfa + hextra[home])))
            la = max(0.05, min(6.0, math.exp(mu + att[away] - deff[home])))
            return lh, la
        def update(m):
            nonlocal mu, hfa
            lh, la = predict(m['homeName'], m['awayName'])
            eh, ea = m['homeGoals'] - lh, m['awayGoals'] - la
            kh = LR*(NEW_TEAM_MULT if seen[m['homeName']] < NEW_TEAM_N else 1.0)
            ka = LR*(NEW_TEAM_MULT if seen[m['awayName']] < NEW_TEAM_N else 1.0)
            att[m['homeName']] += kh*eh*0.5; deff[m['awayName']] -= ka*eh*0.5
            att[m['awayName']] += ka*ea*0.5; deff[m['homeName']] -= kh*ea*0.5
            hfa += HFA_LR*(eh-ea)*0.02
            hextra[m['homeName']] += HFA_LR*(eh-ea)*0.010
            hextra[m['homeName']] *= 0.999
            mu += 0.004*(eh+ea)/2
            hfa = max(0.05, min(0.55, hfa))
            hextra[m['homeName']] = max(-0.25, min(0.25, hextra[m['homeName']]))
            for t in (m['homeName'], m['awayName']):
                att[t] *= (1-DECAY); deff[t] *= (1-DECAY)
            seen[m['homeName']] += 1; seen[m['awayName']] += 1
        for m in train: update(m)
        b = bl = hits = n = 0.0
        marg = [0.0]*3
        for m in test:
            y = y_of(m); marg[y] += 1
            if seen[m['homeName']] < MIN_GAMES or seen[m['awayName']] < MIN_GAMES:
                update(m); continue
            lh, la = predict(m['homeName'], m['awayName'])
            probs = list(grid(lh, la))
            b += brier(probs, y); bl += logloss(probs, y)
            if outcome(probs) == y: hits += 1
            n += 1
            update(m)
        tot = len(test)
        base = [c/tot for c in marg]
        b_base = sum(brier(base, y_of(m)) for m in test)/tot
        res[str(h)] = {"n": int(n), "scored": int(n), "holdout": nhold,
                       "brier": round(b/n,4), "brier_base": round(b_base,4),
                       "logloss": round(bl/n,4), "dir_acc": round(hits/n*100,1)}
    return res

if __name__ == "__main__":
    out = {}
    for lg in ("Russian Premier League", "Czech First League", "England Premier League"):
        print(f"== {lg} ==")
        out[lg] = run_ladder(lg)
        for h in HOLDOUTS:
            r = out[lg][str(h)]
            print(f"  holdout {str(h):>4}: n={r['n']:>3}  Brier {r['brier']:.4f} (base {r['brier_base']:.4f})  "
                  f"ll {r['logloss']:.4f}  dir {r['dir_acc']}%")
    with open("audit_work/ladder_baseline_2026-08-05.json","w") as f:
        json.dump({"date":"2026-08-05","store":STORE,"engine":"DC online, spec B3 constants, naive init",
                   "results":out}, f, indent=1)
    print("\nartifact: audit_work/ladder_baseline_2026-08-05.json")
