#!/usr/bin/env python3
"""
LEAGUE PIVOT FIT FULL — using entire UEFA FULL 3200 matches (not just connector 1390)
For owner: entire UCL/UEL/UECL data so live computations always accurate real world.

Uses expanded store 10209 domestic (5082 + ITA/GER/FRA) + UEFA FULL 3200 (or connector 1390)
Fits s[L] per-league pivot X points above/below via bias loop.

Same method as league_pivot_fit.py but with FULL dataset.
"""
import json, math
from collections import defaultdict, Counter

STORE = "audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json"
UEFA_FULL = "handoffs/UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt"

LEAGUE_MAP_SHORT = {
    "England Premier League": "ENG",
    "Czech First League": "CZE",
    "Russian Premier League": "RUS",
    "Italy Serie A": "ITA",
    "Germany Bundesliga": "GER",
    "France Ligue 1": "FRA",
}

print(f"Loading store {STORE}")
with open(STORE) as f:
    j=json.load(f)
    store=j['store'] if 'store' in j else j

LR, DECAY, HFA_LR = 0.055, 0.0022, 0.010
MU0, HFA0 = 0.45, 0.25
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8

att=defaultdict(float); deff=defaultdict(float); hextra=defaultdict(float); seen=defaultdict(int); mu=MU0
hfa_per_league=defaultdict(lambda: HFA0)

def predict_domestic(h,a,league):
    hfa=hfa_per_league[league]
    lh=max(0.05,min(6.0, math.exp(mu+att[h]-deff[a]+hfa+hextra[h])))
    la=max(0.05,min(6.0, math.exp(mu+att[a]-deff[h])))
    return lh,la

def update_domestic(m):
    global mu
    league=m['competitionName']
    h=m['homeName']; a=m['awayName']
    lh,la=predict_domestic(h,a,league)
    eh=m['homeGoals']-lh; ea=m['awayGoals']-la
    kh=LR*(NEW_TEAM_MULT if seen[h]<NEW_TEAM_N else 1.0)
    ka=LR*(NEW_TEAM_MULT if seen[a]<NEW_TEAM_N else 1.0)
    att[h]+=kh*eh*0.5; deff[a]-=ka*eh*0.5
    att[a]+=ka*ea*0.5; deff[h]-=kh*ea*0.5
    hfa_per_league[league]+=HFA_LR*(eh-ea)*0.02
    hextra[h]+=HFA_LR*(eh-ea)*0.010; hextra[h]*=0.999; mu+=0.004*(eh+ea)/2
    hfa_per_league[league]=max(0.05,min(0.55,hfa_per_league[league]))
    hextra[h]=max(-0.25,min(0.25,hextra[h]))
    for t in (h,a):
        att[t]*=(1-DECAY); deff[t]*=(1-DECAY)
    seen[h]+=1; seen[a]+=1

domestic_rows=sorted(store['matches'], key=lambda m: m['dateISO'])
for m in domestic_rows:
    update_domestic(m)

print(f"Domestic fit {len(att)} teams")

import sys
sys.path.insert(0, 'audit_work')
from pack_parse import parse_pack

uefa_full=parse_pack(UEFA_FULL)
print(f"UEFA FULL raw {len(uefa_full['matches'])} teams {len(uefa_full['teams'])}")

# Deduplicate
fps={}
unique=[]
dups=0
for m in uefa_full['matches']:
    fp=(m['dateISO'], m['homeName'], m['awayName'], m['competitionName'])
    if fp in fps:
        dups+=1
        continue
    fps[fp]=m
    unique.append(m)
print(f"UEFA FULL after dedup {len(unique)} removed {dups}")

# Team -> league map from domestic
team_comp=defaultdict(Counter)
for m in domestic_rows:
    team_comp[m['homeName']][m['competitionName']]+=1
    team_comp[m['awayName']][m['competitionName']]+=1
team_league={}
for team,counter in team_comp.items():
    team_league[team]=counter.most_common(1)[0][0]

programme={"England Premier League","Czech First League","Russian Premier League","Italy Serie A","Germany Bundesliga","France Ligue 1","Spain La Liga"}

# For FULL, we want entire competitions, not just connector, so we include ALL UEFA matches, not filtered by programme
# But for pivot fitting, we need at least one team with known domestic rating to compute bias
filtered=[]
for m in unique:
    lh=team_league.get(m['homeName'])
    la=team_league.get(m['awayName'])
    # include if at least one team has known domestic league (so we can compute att/def)
    if lh in programme or la in programme or m['homeName'] in team_league or m['awayName'] in team_league:
        filtered.append(m)

print(f"Filtered FULL in-scope with ≥1 known domestic team: {len(filtered)} (from {len(unique)})")

appearing=set()
for m in filtered:
    lh=team_league.get(m['homeName'])
    la=team_league.get(m['awayName'])
    if lh: appearing.add(lh)
    if la: appearing.add(la)
print(f"Leagues appearing: {appearing}")

# Fit s[L]
s_pivot=defaultdict(float)
step=0.08; tol=0.02; max_iter=100

# Split train/test: cutoff 2024-07-01 for last omitted window
cutoff="2024-07-01"
train=[m for m in filtered if m['dateISO']<cutoff]
test=[m for m in filtered if m['dateISO']>=cutoff]
print(f"Train {len(train)} test {len(test)} cutoff {cutoff}")

def pred_gd(m, s_piv):
    lh_l=team_league.get(m['homeName'])
    la_l=team_league.get(m['awayName'])
    s_h=s_piv.get(lh_l,0.0)
    s_a=s_piv.get(la_l,0.0)
    home_strength=att.get(m['homeName'],0)-deff.get(m['homeName'],0)
    away_strength=att.get(m['awayName'],0)-deff.get(m['awayName'],0)
    hfa=0.25
    return (home_strength - away_strength) + (s_h - s_a) + hfa

def actual_gd(m): return m['homeGoals']-m['awayGoals']

for it in range(max_iter):
    bias_sum=defaultdict(float); bias_cnt=defaultdict(int)
    for m in train:
        gd_pred=pred_gd(m, s_pivot)
        gd_actual=actual_gd(m)
        err=gd_pred - gd_actual
        lh=team_league.get(m['homeName']); la=team_league.get(m['awayName'])
        if lh:
            bias_sum[lh]+=err; bias_cnt[lh]+=1
        if la:
            bias_sum[la]+= -err; bias_cnt[la]+=1
    max_bias=0
    for lg in bias_sum:
        if bias_cnt[lg]==0: continue
        bias=bias_sum[lg]/bias_cnt[lg]
        max_bias=max(max_bias, abs(bias))
        s_pivot[lg]-=step*bias
    # print
    if (it+1)%10==0 or it<5:
        print(f"Iter {it+1:3d} max_bias {max_bias:+.4f} " + ", ".join(f"{LEAGUE_MAP_SHORT.get(l,l)[:3]}={s_pivot[l]:+.3f}" for l in sorted(s_pivot)))
    if max_bias<tol:
        print(f"Converged iter {it+1} max_bias {max_bias:.4f} < tol {tol}")
        break

print("\nFinal pivots s[L]:")
for l in sorted(s_pivot):
    print(f"  {l} ({LEAGUE_MAP_SHORT.get(l,l)}): {s_pivot[l]:+.4f} log-goals ~{math.exp(s_pivot[l]):.3f}x")

# Validation MSE
def mse_eval(test_set, s_piv):
    s=0
    for m in test_set:
        gd_pred=pred_gd(m, s_piv)
        gd_actual=actual_gd(m)
        s+=(gd_pred-gd_actual)**2
    return s/len(test_set) if test_set else 0

mse_frozen=mse_eval(test, defaultdict(float))
mse_weighted=mse_eval(test, s_pivot)
imp=(mse_frozen-mse_weighted)/mse_frozen*100 if mse_frozen else 0
print(f"\nValidation last omitted window {cutoff} onwards test {len(test)}:")
print(f"  MSE frozen 0: {mse_frozen:.4f}")
print(f"  MSE weighted: {mse_weighted:.4f}")
print(f"  Improvement: {imp:+.2f}% {'BETTER' if mse_weighted<mse_frozen else 'WORSE'}")

artifact={
    "store": STORE,
    "uefa_full": UEFA_FULL,
    "train": len(train),
    "test": len(test),
    "s_pivot": dict(s_pivot),
    "mse_frozen": mse_frozen,
    "mse_weighted": mse_weighted,
    "improvement_pct": imp,
    "method": "full 3200 entire UCL/UEL/UECL + qualifiers, bias loop s[L]←s[L]-step*bias step 0.08 tol 0.02 max_iter 100, pred GD = (att-def + sLA) - (att-def + sLB) + hfa 0.25",
    "note": "Entire UEFA data for real-world cross-league accuracy per owner directive gather entire UFA champions league data europa etc"
}
with open("audit_work/league_pivot_full_artifact.json","w") as f:
    json.dump(artifact,f,indent=2)
print("\nArtifact saved audit_work/league_pivot_full_artifact.json")
