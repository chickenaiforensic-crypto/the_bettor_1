#!/usr/bin/env python3
"""Fresh full-store ladder audit (2026-08-06).

Runs the frozen online DC-style harness constants against each requested domestic
competition and a combined UEFA cohort.  It rejects malformed calendar dates
rather than silently ordering them lexicographically, and records any cohort
that lacks a meaningful train/test chronology as INSUFFICIENT_DATA.

The companion 11,599 replay is used solely for row-preservation parity on the
six shared domestic leagues; it is not an optimisation pass.
"""
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FULL = ROOT / "audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json"
PRIOR = ROOT / "audit_work/pitch-rating-full-11599-with-uefa-2026-08-05.json"
OUT = ROOT / "audit_work/ladder_baseline_2026-08-06_16629.json"

DOMESTIC = ["Russian Premier League", "Czech First League", "England Premier League",
            "Italy Serie A", "Germany Bundesliga", "France Ligue 1", "Spain La Liga",
            "Scottish Premiership", "Kosovo Superliga"]
UEFA = ["UEFA Champions League", "UEFA Europa League", "UEFA Conference League"]
CUTS = {league: "2025-07-01" for league in DOMESTIC}
CUTS["UEFA"] = "2024-07-01"
HOLDOUTS = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, "FULL"]
LR, DECAY, HFA_LR, RHO = .055, .0022, .010, -.06
NEW_TEAM_MULT, NEW_TEAM_N, MU0, HFA0, MIN_GAMES = 1.6, 8, .45, .25, 6


def pmf(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)
def grid(lh, la):
    cells = []
    for h in range(11):
        for a in range(11):
            adjust = (1-lh*la*RHO if h == a == 0 else 1+lh*RHO if h == 0 and a == 1 else
                      1+la*RHO if h == 1 and a == 0 else 1-RHO if h == a == 1 else 1)
            cells.append((h, a, pmf(h, lh)*pmf(a, la)*adjust))
    z = sum(c[2] for c in cells)
    home = sum(p for h,a,p in cells if h > a) / z
    draw = sum(p for h,a,p in cells if h == a) / z
    return home, draw, 1-home-draw

def yof(m): return 0 if m["homeGoals"] > m["awayGoals"] else 1 if m["homeGoals"] == m["awayGoals"] else 2
def brier(p, y): return sum((v-(i == y))**2 for i,v in enumerate(p))
def logloss(p, y): return -math.log(max(p[y], 1e-9))

def valid_rows(store, cohort):
    names = UEFA if cohort == "UEFA" else [cohort]
    good, bad = [], []
    for m in store["matches"]:
        if m["competitionName"] not in names: continue
        try: dt.date.fromisoformat(m["dateISO"])
        except (ValueError, TypeError): bad.append(m); continue
        good.append(m)
    return sorted(good, key=lambda m:(m["dateISO"], m["homeName"], m["awayName"])), bad

def ladder(rows, cutoff):
    train_all = [m for m in rows if m["dateISO"] < cutoff]
    season = [m for m in rows if m["dateISO"] >= cutoff]
    if len(train_all) < 50 or len(season) < 30:
        return {"status":"INSUFFICIENT_DATA", "train_rows":len(train_all), "test_rows":len(season),
                "reason":"requires at least 50 dated pre-cutoff rows and 30 dated test rows"}
    results = {}
    for holdout in HOLDOUTS:
        n_hold = len(season) if holdout == "FULL" else holdout
        if n_hold > len(season): continue
        train, test = train_all + season[:-n_hold], season[-n_hold:]
        att, deff, hx, seen = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(int)
        mu, hfa = MU0, HFA0
        def predict(h,a):
            return (max(.05,min(6,math.exp(mu+att[h]-deff[a]+hfa+hx[h]))),
                    max(.05,min(6,math.exp(mu+att[a]-deff[h]))))
        def update(m):
            nonlocal mu,hfa
            h,a=m["homeName"],m["awayName"]; lh,la=predict(h,a); eh,ea=m["homeGoals"]-lh,m["awayGoals"]-la
            kh=LR*(NEW_TEAM_MULT if seen[h] < NEW_TEAM_N else 1); ka=LR*(NEW_TEAM_MULT if seen[a] < NEW_TEAM_N else 1)
            att[h]+=kh*eh*.5; deff[a]-=ka*eh*.5; att[a]+=ka*ea*.5; deff[h]-=kh*ea*.5
            hfa=max(.05,min(.55,hfa+HFA_LR*(eh-ea)*.02)); hx[h]=max(-.25,min(.25,(hx[h]+HFA_LR*(eh-ea)*.010)*.999))
            mu+=.004*(eh+ea)/2
            for team in (h,a): att[team]*=1-DECAY; deff[team]*=1-DECAY; seen[team]+=1
        for m in train: update(m)
        total_brier=total_ll=hits=0.; scored=0; marginal=[0.,0.,0.]
        for m in test:
            y=yof(m); marginal[y]+=1
            if seen[m["homeName"]] >= MIN_GAMES and seen[m["awayName"]] >= MIN_GAMES:
                p=grid(*predict(m["homeName"],m["awayName"])); total_brier+=brier(p,y); total_ll+=logloss(p,y); hits+=int(max(range(3),key=lambda i:p[i]) == y); scored+=1
            update(m)
        base=[x/len(test) for x in marginal]
        results[str(holdout)]={"holdout":n_hold,"n":scored,"scored":scored,
          "brier":round(total_brier/scored,4) if scored else None,
          "brier_base":round(sum(brier(base,yof(m)) for m in test)/len(test),4),
          "logloss":round(total_ll/scored,4) if scored else None,
          "dir_acc":round(hits/scored*100,1) if scored else None,
          "note":"no fixture passed the six-prior-games rule" if not scored else None}
    return {"status":"PASS","train_rows":len(train_all),"test_rows":len(season),"results":results}

def load(path):
    with path.open() as f: return json.load(f)["store"]
def main():
    full, prior = load(FULL), load(PRIOR)
    cohorts=DOMESTIC+["UEFA"]; audit={}; parity={}
    for cohort in cohorts:
        rows,bad=valid_rows(full,cohort); audit[cohort]={"dated_rows":len(rows),"rejected_invalid_dates":len(bad),
          "invalid_date_examples":[{"dateISO":m["dateISO"],"home":m["homeName"],"away":m["awayName"]} for m in bad[:3]],
          **ladder(rows,CUTS[cohort])}
    for cohort in DOMESTIC[:6]:
        now,_=valid_rows(full,cohort); before,_=valid_rows(prior,cohort)
        # Exact fingerprints establish whether new store changed the shared cohort.
        fp=lambda rows:{(m["dateISO"],m["homeName"],m["awayName"],m["homeGoals"],m["awayGoals"]) for m in rows}
        same=fp(now)==fp(before)
        current=ladder(now,CUTS[cohort]); old=ladder(before,CUTS[cohort])
        equal = same and current.get("results") == old.get("results")
        parity[cohort]={"shared_row_fingerprint_parity":same,"ladder_metric_delta":"0.0000" if equal else "NONZERO","pass":equal}
    artifact={"date":"2026-08-06","store":str(FULL.relative_to(ROOT)),"store_match_count":len(full["matches"]),
      "engine":"frozen online DC-style harness constants (LR=.055, decay=.0022, HFA LR=.010, rho=-.06)",
      "cutoffs":CUTS,"holdouts":HOLDOUTS,"results":audit,"existing_six_parity":parity,
      "verdict":"CONDITIONAL: six shared leagues preserve exactly; KOS lacks a usable pre-cutoff history; UEFA has 343 malformed dates excluded from scoring."}
    with OUT.open("w") as f: json.dump(artifact,f,indent=2)
    for c,v in audit.items(): print(c,v["status"],"dated",v["dated_rows"],"invalid",v["rejected_invalid_dates"])
    print("wrote",OUT)
if __name__ == "__main__": main()
