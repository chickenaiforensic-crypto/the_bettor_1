#!/usr/bin/env python3
"""BACKTEST HARNESS — feasibility run on the real store (2026-08-05).

Owner doctrine (2026-08-05): approval = a measured test run. Every system is
bulk-backtested on all data up to a cutoff, scored on the LAST OMITTED WINDOW,
then calibrated from the results. This script is the harness's first live run.

Design:
  train = seasons 2021-22 .. 2024-25 (online Dixon-Coles fit, spec B3 constants)
  test  = season 2025-26 (the last omitted window)
  metrics: Brier (full 1X2 + per side), log loss, direction accuracy,
           base-rate comparison, min-6-matches refusal gate (P3)
This is a FEASIBILITY run of the instrument, not the approved engine
calibration (no star correction / no evidence ensemble / naive init).
"""
import json, math, sys
from collections import defaultdict

STORE = "Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json"
SEASONS = {"Russian Premier League": 2021, "Czech First League": 2021, "England Premier League": 2021}

LR, DECAY, HFA_LR, RHO = 0.055, 0.0022, 0.010, -0.06
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8
MU0, HFA0 = 0.45, 0.25
MIN_GAMES = 6

def poisson_pmf(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)

def grid_prob(lam_h, lam_a):
    """Poisson x Poisson with DC tau (rho=-0.06), normalised."""
    n = 10
    p = [[0.0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        for j in range(n+1):
            t = 1.0
            if i == 0 and j == 0: t = 1 - lam_h*lam_a*RHO
            elif i == 0 and j == 1: t = 1 + lam_h*RHO
            elif i == 1 and j == 0: t = 1 + lam_a*RHO
            elif i == 1 and j == 1: t = 1 - RHO
            p[i][j] = poisson_pmf(i, lam_h) * poisson_pmf(j, lam_a) * t
    s = sum(sum(r) for r in p)
    ph = sum(p[i][j] for i in range(n+1) for j in range(n+1) if i > j) / s
    pd = sum(p[i][i] for i in range(n+1)) / s
    pa = 1 - ph - pd
    return ph, pd, pa

def outcome(ph, pd, pa):
    m = max(ph, pd, pa)
    return 0 if m == ph else (1 if m == pd else 2)

def brier(probs, y):
    return sum((p - (1.0 if i == y else 0.0))**2 for i, p in enumerate(probs))

def logloss(probs, y):
    return -math.log(max(probs[y], 1e-9))

def run(league):
    with open(STORE) as f:
        store = json.load(f)['store']
    rows = [m for m in store['matches'] if m['competitionName'] == league]
    rows.sort(key=lambda m: m['dateISO'])
    if not rows:
        print(f"{league}: no rows"); return
    # split by season (Jul start year)
    train = [m for m in rows if m['dateISO'] < f"{SEASONS[league]+4}-07-01"]
    test  = [m for m in rows if m['dateISO'] >= f"{SEASONS[league]+4}-07-01"]
    # state
    att, deff, hextra, seen = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(int)
    mu, hfa = MU0, HFA0
    def predict(h, a):
        lh = math.exp(mu + att[h] - deff[a] + hfa + hextra[h])
        la = math.exp(mu + att[a] - deff[h])
        lh = max(0.05, min(6.0, lh)); la = max(0.05, min(6.0, la))
        return lh, la
    def update(m):
        nonlocal mu, hfa
        lh, la = predict(m['homeName'], m['awayName'])
        eh = m['homeGoals'] - lh; ea = m['awayGoals'] - la
        kh = LR * (NEW_TEAM_MULT if seen[m['homeName']] < NEW_TEAM_N else 1.0)
        ka = LR * (NEW_TEAM_MULT if seen[m['awayName']] < NEW_TEAM_N else 1.0)
        att[m['homeName']] += kh * eh * 0.5
        deff[m['awayName']] -= ka * eh * 0.5
        att[m['awayName']] += ka * ea * 0.5
        deff[m['homeName']] -= kh * ea * 0.5
        hfa += HFA_LR * (eh - ea) * 0.02
        hextra[m['homeName']] += HFA_LR * (eh - ea) * 0.010
        hextra[m['homeName']] *= 0.999
        mu += 0.004 * (eh + ea) / 2
        hfa = max(0.05, min(0.55, hfa))
        hextra[m['homeName']] = max(-0.25, min(0.25, hextra[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att[t] *= (1 - DECAY); deff[t] *= (1 - DECAY)
        seen[m['homeName']] += 1; seen[m['awayName']] += 1
    for m in train:
        update(m)
    # test: predict, then update (online causality)
    b, bl, hits, n = 0.0, 0.0, 0, 0
    refusals = 0
    marg = [0.0, 0.0, 0.0]
    for m in test:
        y = 0 if m['homeGoals'] > m['awayGoals'] else (1 if m['homeGoals'] == m['awayGoals'] else 2)
        marg[y] += 1
        if seen[m['homeName']] < MIN_GAMES or seen[m['awayName']] < MIN_GAMES:
            refusals += 1
            update(m); continue
        lh, la = predict(m['homeName'], m['awayName'])
        ph, pd, pa = grid_prob(lh, la)
        probs = [ph, pd, pa]
        b += brier(probs, y); bl += logloss(probs, y)
        if outcome(*probs) == y: hits += 1
        n += 1
        update(m)
    tot = len(test)
    base = [c / tot for c in marg]
    b_base = sum(brier(base, 0 if m['homeGoals'] > m['awayGoals'] else (1 if m['homeGoals'] == m['awayGoals'] else 2)) for m in test) / tot
    print(f"== {league} ==")
    print(f"  train {len(train)} rows -> test {n} scored (+{refusals} refused: <{MIN_GAMES} games, P3)")
    print(f"  Brier DC      : {b/n:.4f}   (n={n})")
    print(f"  Brier base    : {b_base:.4f}   (test-window marginals {[round(x,3) for x in base]})")
    print(f"  log loss DC   : {bl/n:.4f}")
    print(f"  direction acc : {hits/n*100:.1f}%")

if __name__ == "__main__":
    for lg in ("Russian Premier League", "Czech First League", "England Premier League"):
        run(lg)
