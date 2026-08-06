#!/usr/bin/env python3
"""
LEAGUE PIVOT FIT — implements owner clarification: per-league rating that pivots one league X points above another
so live computations always accurate / real world.

Owner: cross leagues we use standard evaluation per team-league then per results obtain we bump it up/calibrate it to create per-league rating that pivots one league X points above another league.

Formalisation (Masterplan §6 fit-to-results loop):
- Each team has att/def fitted within its own league (L1).
- League pivot s[L] init 0.
- Common-scale strength: S[t] = att[t] - def[t] + s[league(t)]
- For cross-league Euro match home A (league LA) away B (league LB):
  predicted GD = (att[A] - def[A] + s[LA]) - (att[B] - def[B] + s[LB]) + hfa? Simplified: GD_pred = (att_home - def_away + sLA - sLB) - (att_away - def_home + sLB - sLA)? Use att-def difference + s diff.
  Actually simplest per owner: bump league up until predictions match real results.
  Implementation: GD_pred = (att_home - def_away) - (att_away - def_home) + (s[LA] - s[LB]) + hfa
  Where att/def from domestic long-term fit.
- Bias(L) = mean(GD_pred - GD_actual) over Euro ties involving L
- Update: s[L] ← s[L] - step * bias(L)  step 0.05-0.1, iterate 20-50 until bias<0.02
- Validate weighted vs frozen 1.00 baseline (s[L]=0) on last Euro omitted window — adopt only if wins.

This script is feasibility on current data:
- Store 10209 expanded (5082 + ITA/GER/FRA) for domestic ratings
- UEFA connector 1390 (with 1 dup, we deduplicate by taking first occurrence)
- It fits s[L] on Euro ties up to cutoff 2024-07-01, tests on 2024-25..2025-26 Euro ties last omitted window
- Outputs s[L] pivot points, bias convergence, and validation Brier/RMSE vs frozen baseline.

Per owner: app alive when takes results + current performance weighted inclusion via playoffs — league pivot makes cross-league real-world.
"""
import json, math
from collections import defaultdict, Counter

STORE = "audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json"
UEFA = "handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt"

# Map leagues from pack names to our store competition names and to short pivot keys
LEAGUE_MAP = {
    "England Premier League": "ENG",
    "Czech First League": "CZE",
    "Russian Premier League": "RUS",
    "Italy Serie A": "ITA",
    "Germany Bundesliga": "GER",
    "France Ligue 1": "FRA",
    "Spain La Liga": "SPA",  # not yet in store
    "Scottish Premiership": "SCO",
}

# Load store
print("Loading store", STORE)
with open(STORE) as f:
    j=json.load(f)
    store=j['store'] if 'store' in j else j

# Build per-team att/def via simple online fit on domestic data (same constants as harness)
LR, DECAY, HFA_LR = 0.055, 0.0022, 0.010
MU0, HFA0 = 0.45, 0.25
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8

att=defaultdict(float)
deff=defaultdict(float)
hextra=defaultdict(float)
seen=defaultdict(int)
mu=MU0
hfa_per_league=defaultdict(lambda: HFA0)  # per league hfa

def predict_domestic(home, away, league):
    # league-specific hfa
    hfa = hfa_per_league[league]
    lh = max(0.05, min(6.0, math.exp(mu + att[home] - deff[away] + hfa + hextra[home])))
    la = max(0.05, min(6.0, math.exp(mu + att[away] - deff[home])))
    return lh, la

def update_domestic(m):
    global mu
    league=m['competitionName']
    h=m['homeName']; a=m['awayName']
    lh,la=predict_domestic(h,a,league)
    eh=m['homeGoals']-lh
    ea=m['awayGoals']-la
    kh=LR*(NEW_TEAM_MULT if seen[h]<NEW_TEAM_N else 1.0)
    ka=LR*(NEW_TEAM_MULT if seen[a]<NEW_TEAM_N else 1.0)
    att[h]+=kh*eh*0.5
    deff[a]-=ka*eh*0.5
    att[a]+=ka*ea*0.5
    deff[h]-=kh*ea*0.5
    hfa_per_league[league]+=HFA_LR*(eh-ea)*0.02
    hextra[h]+=HFA_LR*(eh-ea)*0.010
    hextra[h]*=0.999
    mu+=0.004*(eh+ea)/2
    hfa_per_league[league]=max(0.05,min(0.55,hfa_per_league[league]))
    hextra[h]=max(-0.25,min(0.25,hextra[h]))
    for t in (h,a):
        att[t]*=(1-DECAY)
        deff[t]*=(1-DECAY)
    seen[h]+=1
    seen[a]+=1

# Sort domestic matches by date
domestic_rows=sorted(store['matches'], key=lambda m: m['dateISO'])
for m in domestic_rows:
    update_domestic(m)

print(f"Domestic fit done: {len(att)} teams, example att Arsenal {att.get('Arsenal',0):.3f} def {deff.get('Arsenal',0):.3f}")

# Load UEFA connector, deduplicate fingerprint
import sys
sys.path.insert(0, 'audit_work')
from pack_parse import parse_pack

uefa_pack=parse_pack(UEFA)
print(f"UEFA raw {len(uefa_pack['matches'])} matches, {len(uefa_pack['teams'])} teams")

# Deduplicate by fingerprint (date, home, away, competition) keeping first
fps={}
dups=0
unique=[]
for m in uefa_pack['matches']:
    fp=(m['dateISO'], m['homeName'], m['awayName'], m['competitionName'])
    if fp in fps:
        dups+=1
        # keep first occurrence
        continue
    fps[fp]=m
    unique.append(m)

print(f"UEFA after dedup {len(unique)} matches (removed {dups} dup) — defect Real Madrid-Chelsea duplicate removed")

# Map each team in UEFA to its domestic league if known, else unknown
# For simplicity, we use country field in pack? pack's country is home side's country — but we need league mapping
# We'll infer league from team name if team appears in domestic store? Or use competitionName of domestic? For foreign opponents (e.g., PSG) league = FRA? Actually PSG is in FRA domestic now, so we can map.

# Build team -> league from domestic store: for each team, most frequent competitionName? Or we have country? Simplify: use a mapping from team name to league based on which domestic competition they appear in most.

team_league=Counter()
# Actually need per team league: find for each team which competition they appear most in domestic
team_comp_counter=defaultdict(Counter)
for m in domestic_rows:
    team_comp_counter[m['homeName']][m['competitionName']]+=1
    team_comp_counter[m['awayName']][m['competitionName']]+=1

team_league_map={}
for team, counter in team_comp_counter.items():
    most=counter.most_common(1)[0][0]
    team_league_map[team]=most

# For UEFA teams not in domestic store, try to infer from country field or use name heuristics
# For foreign opponents (e.g., Real Madrid), league = Spain La Liga (not in store yet) — we will treat as "Other" with s=0 initially but still fit?
# For this feasibility, we will only fit s[L] for leagues that are in domestic store: ENG, CZE, RUS, ITA, GER, FRA
# For other leagues (SPA, etc.), s=0 fixed.

# Filter UEFA matches where at least one team has league in our 6 leagues and is programme-league club (ENG/RUS/CZE/SPA/ITA/GER/FRA)
# Per workorder, in-scope = every tie with at least one club from programme leagues
# Programme leagues list
programme_leagues={"England Premier League","Czech First League","Russian Premier League","Italy Serie A","Germany Bundesliga","France Ligue 1","Spain La Liga"}

# For UEFA matches, we need to know league of each team
def get_league(team):
    return team_league_map.get(team, None)

# Keep only UEFA matches where at least one team league in programme
filtered=[]
for m in unique:
    lh=get_league(m['homeName'])
    la=get_league(m['awayName'])
    # if either team league in programme OR team name appears as programme team? For foreign opponents not in domestic map, we may still have them as programme if they are from programme leagues but not in domestic store? Actually all programme league teams should be in domestic store now for 6 leagues, so get_league should work for them.
    # For foreign opponents (e.g., Real Madrid) league = Spain La Liga which is programme but not in our domestic map yet (since SPA not in store), so get_league returns None — we need to check if team name is Spanish and treat as SPA
    # Simple heuristic: if country == Spain, league = Spain La Liga etc — but country field is home side's country only, not away
    # For simplicity, we will include matches where at least one team is in team_league_map (i.e., domestic team)
    if lh in programme_leagues or la in programme_leagues:
        filtered.append(m)
    elif m['homeName'] in team_league_map or m['awayName'] in team_league_map:
        filtered.append(m)

print(f"Filtered UEFA in-scope with ≥1 programme-league club: {len(filtered)} (from {len(unique)})")

# Now fit s[L] league pivots
# Initialize s[L]=0 for all leagues in programme
s_pivot=defaultdict(float)
leagues_to_fit=list(programme_leagues)  # include SPA even if not in store, s=0 fixed? We'll fit only those in domestic
leagues_to_fit=[l for l in leagues_to_fit if l in team_league_map or l in ["England Premier League","Czech First League","Russian Premier League","Italy Serie A","Germany Bundesliga","France Ligue 1"]]

# Actually iterate over all programme leagues that appear in filtered matches
appearing_leagues=set()
for m in filtered:
    lh=get_league(m['homeName'])
    la=get_league(m['awayName'])
    if lh: appearing_leagues.add(lh)
    if la: appearing_leagues.add(la)

print(f"Leagues appearing in filtered UEFA: {appearing_leagues}")

# Fit loop
step=0.08
tol=0.02
max_iter=50

# For validation, split UEFA into train (up to 2024-07-01) and test (2024-07-01 onwards last omitted window)
cutoff_train="2024-07-01"
train_uefa=[m for m in filtered if m['dateISO']<cutoff_train]
test_uefa=[m for m in filtered if m['dateISO']>=cutoff_train]

print(f"Train UEFA {len(train_uefa)} test {len(test_uefa)} cutoff {cutoff_train}")

def predicted_gd(m, s_pivot):
    # Predicted GD = (att_home - def_away + s[LA] ) - (att_away - def_home + s[LB]) + hfa? Simplified: att_home - def_home? Let's use:
    # att and def are per-team, s is per-league pivot
    # GD_pred = (att[home] - deff[home]) - (att[away] - deff[away]) + (s[LA]-s[LB]) + hfa_avg
    # For simplicity, use att-def difference
    lh_league=get_league(m['homeName'])
    la_league=get_league(m['awayName'])
    # if league not in s_pivot, s=0
    s_home=s_pivot.get(lh_league,0.0)
    s_away=s_pivot.get(la_league,0.0)
    # att/def difference
    home_strength=att.get(m['homeName'],0)-deff.get(m['homeName'],0)
    away_strength=att.get(m['awayName'],0)-deff.get(m['awayName'],0)
    # hfa average from domestic per league? Use 0.25
    hfa=0.25
    gd_pred=(home_strength - away_strength) + (s_home - s_away) + hfa
    return gd_pred

def actual_gd(m):
    return m['homeGoals']-m['awayGoals']

# Iterative fit
for iteration in range(max_iter):
    # compute bias per league on train set
    bias_sum=defaultdict(float)
    bias_count=defaultdict(int)
    for m in train_uefa:
        gd_pred=predicted_gd(m, s_pivot)
        gd_actual=actual_gd(m)
        err=gd_pred - gd_actual
        # attribute error to both leagues? For league L, bias(L)=mean(predicted - actual) over ties involving L
        # So for each match, we add err to home league and -err? Actually if we predict home too high (err>0), we need to lower home league pivot or raise away league.
        # Simpler: bias for home league = err, for away league = -err? But spec says bias(L)=mean(predicted GD - actual GD) over ties involving L — for away team, predicted GD from away perspective is -GD_pred, so bias for away league should be (-GD_pred) - (-GD_actual) = -(GD_pred - GD_actual) = -err
        lh=get_league(m['homeName'])
        la=get_league(m['awayName'])
        if lh:
            bias_sum[lh]+=err
            bias_count[lh]+=1
        if la:
            bias_sum[la]+= -err
            bias_count[la]+=1

    max_bias=0
    for league in list(bias_sum.keys()):
        if bias_count[league]==0:
            continue
        bias=bias_sum[league]/bias_count[league]
        max_bias=max(max_bias, abs(bias))
        # update s[L] ← s[L] - step*bias
        s_pivot[league] -= step*bias

    print(f"Iter {iteration+1:2d} max_bias {max_bias:+.4f} s_pivot: " + ", ".join(f"{LEAGUE_MAP.get(l,l)[:3]}={s_pivot[l]:+.3f}" for l in sorted(s_pivot.keys())))

    if max_bias < tol:
        print(f"Converged at iteration {iteration+1} max_bias {max_bias:.4f} < tol {tol}")
        break

print("\nFinal league pivots s[L] (log-goals, positive = league stronger than average):")
for l in sorted(s_pivot.keys()):
    print(f"  {l} ({LEAGUE_MAP.get(l,l)}): {s_pivot[l]:+.4f} log-goals (~{math.exp(s_pivot[l]):.3f}x goal multiplier)")

# Validation: weighted vs frozen baseline on test set
def brier_for_gd(gd_pred, gd_actual):
    # Convert GD_pred to prob approximate via logistic? For simplicity, use MSE of GD
    return (gd_pred - gd_actual)**2

def evaluate(test_set, s_pivot_used):
    mse=0
    for m in test_set:
        gd_pred=predicted_gd(m, s_pivot_used)
        gd_actual=actual_gd(m)
        mse+=(gd_pred-gd_actual)**2
    return mse/len(test_set) if test_set else 0

mse_frozen=evaluate(test_uefa, defaultdict(float))
mse_weighted=evaluate(test_uefa, s_pivot)
print(f"\nValidation on last omitted window {cutoff_train} onwards test {len(test_uefa)} matches:")
print(f"  MSE frozen s=0: {mse_frozen:.4f}")
print(f"  MSE weighted s[L] fitted: {mse_weighted:.4f}")
print(f"  Improvement: {(mse_frozen-mse_weighted)/mse_frozen*100:+.2f}% {'BETTER' if mse_weighted<mse_frozen else 'WORSE'}")

# Save artifact
artifact={
    "store": STORE,
    "uefa": UEFA,
    "train_uefa": len(train_uefa),
    "test_uefa": len(test_uefa),
    "s_pivot": dict(s_pivot),
    "final_max_bias": max_bias,
    "mse_frozen": mse_frozen,
    "mse_weighted": mse_weighted,
    "improvement_pct": (mse_frozen-mse_weighted)/mse_frozen*100 if mse_frozen else 0,
    "method": "bias loop s[L]←s[L]-step*bias(L) bias(L)=mean(predicted GD - actual GD) over ties involving L, step 0.08 tol 0.02 max_iter 50, predicted GD = (att_home-def_home + sLA) - (att_away-def_away + sLB) + hfa 0.25",
    "note": "Per owner clarification: standard evaluation per team-league then bump/calibrate to per-league rating that pivots one league X points above another so live computations always accurate real world"
}

with open("audit_work/league_pivot_artifact.json","w") as f:
    json.dump(artifact,f,indent=2)

print("\nArtifact saved to audit_work/league_pivot_artifact.json")
print("Per-league pivot points X above/below ready for S5 cross-border bridge.")
