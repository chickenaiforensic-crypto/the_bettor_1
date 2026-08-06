#!/usr/bin/env python3
"""
League pivot refined — 16193 corrected store (without fabricated ClubA/B)
"""
import json, math, re
from collections import defaultdict, Counter

STORE = "audit_work/pitch-rating-full-16193-corrected-2026-08-06.json"
CUTOFF = "2024-07-01"
STEP = 0.05
TOL = 0.02
MAX_ITER = 100
RHO = -0.06

def canon(s):
    s=str(s).lower()
    s=re.sub(r'[^a-z0-9]+',' ',s).strip()
    s=re.sub(r'\s+',' ',s)
    return s

print(f"Loading store {STORE}")
with open(STORE) as f:
    j=json.load(f)
    wrapper=j['store'] if 'store' in j else j
    matches=wrapper.get('matches',[])
    if not matches and 'store' in wrapper:
        matches=wrapper['store'].get('matches',[]) if isinstance(wrapper['store'],dict) else []
    print(f"matches {len(matches)} from wrapper")

domestic=[m for m in matches if 'UEFA' not in m['competitionName']]
uefa=[m for m in matches if 'UEFA' in m['competitionName']]
print(f"Domestic {len(domestic)} UEFA {len(uefa)}")

team_comp_counter=defaultdict(Counter)
for m in domestic:
    team_comp_counter[canon(m['homeName'])][m['competitionName']]+=1
    team_comp_counter[canon(m['awayName'])][m['competitionName']]+=1

team_league_canon={}
for c_team, counter in team_comp_counter.items():
    team_league_canon[c_team]=counter.most_common(1)[0][0]

programme_leagues={
    "England Premier League",
    "Czech First League",
    "Russian Premier League",
    "Italy Serie A",
    "Germany Bundesliga",
    "France Ligue 1",
    "Spain La Liga",
    "Scottish Premiership",
    "Kosovo Superliga",
}

LR, DECAY, HFA_LR = 0.055, 0.0022, 0.010
MU0, HFA0 = 0.45, 0.25
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8

att_c=defaultdict(float)
deff_c=defaultdict(float)
hextra_c=defaultdict(float)
seen_c=defaultdict(int)
mu=MU0
hfa_per_league=defaultdict(lambda: HFA0)

def predict_domestic_params_canon(home_c, away_c, home_league):
    hfa=hfa_per_league[home_league] if home_league in hfa_per_league else HFA0
    lh_raw=mu + att_c[home_c] - deff_c[away_c] + hfa + hextra_c[home_c]
    la_raw=mu + att_c[away_c] - deff_c[home_c]
    lh=max(0.05, min(6.0, math.exp(lh_raw)))
    la=max(0.05, min(6.0, math.exp(la_raw)))
    return lh, la

def update_domestic(m):
    global mu
    league=m['competitionName']
    hc=canon(m['homeName']); ac=canon(m['awayName'])
    lh, la = predict_domestic_params_canon(hc, ac, league)
    eh=m['homeGoals']-lh
    ea=m['awayGoals']-la
    kh=LR*(NEW_TEAM_MULT if seen_c[hc]<NEW_TEAM_N else 1.0)
    ka=LR*(NEW_TEAM_MULT if seen_c[ac]<NEW_TEAM_N else 1.0)
    att_c[hc]+=kh*eh*0.5
    deff_c[ac]-=ka*eh*0.5
    att_c[ac]+=ka*ea*0.5
    deff_c[hc]-=kh*ea*0.5
    hfa_per_league[league]+=HFA_LR*(eh-ea)*0.02
    hextra_c[hc]+=HFA_LR*(eh-ea)*0.010
    hextra_c[hc]*=0.999
    mu+=0.004*(eh+ea)/2
    hfa_per_league[league]=max(0.05,min(0.55,hfa_per_league[league]))
    hextra_c[hc]=max(-0.25,min(0.25,hextra_c[hc]))
    for t_c in (hc,ac):
        att_c[t_c]*=(1-DECAY)
        deff_c[t_c]*=(1-DECAY)
    seen_c[hc]+=1
    seen_c[ac]+=1

domestic_sorted=sorted(domestic, key=lambda m: m['dateISO'])
domestic_train=[m for m in domestic_sorted if m['dateISO']<CUTOFF]
print(f"Domestic train {len(domestic_train)}")
for m in domestic_train:
    update_domestic(m)
print(f"Fit done mu {mu:.3f} teams {len(att_c)}")
for lg in sorted(programme_leagues):
    print(f"  HFA {lg}: {hfa_per_league[lg]:.4f}")

uefa_sorted=sorted(uefa, key=lambda m: m['dateISO'])
uefa_train=[m for m in uefa_sorted if m['dateISO']<CUTOFF]
uefa_test=[m for m in uefa_sorted if m['dateISO']>=CUTOFF]
print(f"UEFA train {len(uefa_train)} test {len(uefa_test)}")

def get_league_canon(team_name):
    return team_league_canon.get(canon(team_name))

appearing=set()
for m in uefa_train+uefa_test:
    lh=get_league_canon(m['homeName'])
    la=get_league_canon(m['awayName'])
    if lh: appearing.add(lh)
    if la: appearing.add(la)
print(f"Appearing leagues: {appearing}")

filtered_train=[m for m in uefa_train if (get_league_canon(m['homeName']) in programme_leagues) or (get_league_canon(m['awayName']) in programme_leagues)]
filtered_test=[m for m in uefa_test if (get_league_canon(m['homeName']) in programme_leagues) or (get_league_canon(m['awayName']) in programme_leagues)]
print(f"Filtered train {len(filtered_train)} test {len(filtered_test)}")

if len(filtered_test)<100:
    print(f"Filtered test {len(filtered_test)} <100, using expanded seen-based")
    filtered_train2=[m for m in uefa_train if (canon(m['homeName']) in seen_c) or (canon(m['awayName']) in seen_c)]
    filtered_test2=[m for m in uefa_test if (canon(m['homeName']) in seen_c) or (canon(m['awayName']) in seen_c)]
    print(f"  seen-based train {len(filtered_train2)} test {len(filtered_test2)}")
    if len(filtered_test2)>=100:
        filtered_train, filtered_test = filtered_train2, filtered_test2

if len(filtered_test)<100:
    print(f"Still <100, fallback to all UEFA")
    filtered_train, filtered_test = uefa_train, uefa_test

print(f"Final using train {len(filtered_train)} test {len(filtered_test)}")

def pmf(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)
def grid_prob(lam_h, lam_a):
    n=10
    p=[[0.0]*(n+1) for _ in range(n+1)]
    for i in range(n+1):
        for j in range(n+1):
            t=1.0
            if i==0 and j==0: t=1 - lam_h*lam_a*RHO
            elif i==0 and j==1: t=1 + lam_h*RHO
            elif i==1 and j==0: t=1 + lam_a*RHO
            elif i==1 and j==1: t=1 - RHO
            p[i][j]=pmf(i, lam_h)*pmf(j, lam_a)*t
    s=sum(sum(r) for r in p)
    ph=sum(p[i][j] for i in range(n+1) for j in range(n+1) if i>j)/s
    pd=sum(p[i][i] for i in range(n+1))/s
    return ph, pd, 1-ph-pd
def brier(probs,y): return sum((p-(1.0 if i==y else 0.0))**2 for i,p in enumerate(probs))
def y_of(m): return 0 if m['homeGoals']>m['awayGoals'] else (1 if m['homeGoals']==m['awayGoals'] else 2)
def actual_gd(m): return m['homeGoals']-m['awayGoals']

s_pivot=defaultdict(float)

def pred_lambdas(m, s_dict):
    hc=canon(m['homeName']); ac=canon(m['awayName'])
    lh_league=get_league_canon(m['homeName'])
    la_league=get_league_canon(m['awayName'])
    s_h=s_dict.get(lh_league,0.0) if lh_league else 0.0
    s_a=s_dict.get(la_league,0.0) if la_league else 0.0
    hfa=hfa_per_league[lh_league] if lh_league in hfa_per_league else HFA0
    att_h=att_c.get(hc,0.0)
    att_a=att_c.get(ac,0.0)
    def_h=deff_c.get(hc,0.0)
    def_a=deff_c.get(ac,0.0)
    hextra_h=hextra_c.get(hc,0.0)
    lh_raw=mu + att_h - def_a + hfa + hextra_h + (s_h - s_a)
    la_raw=mu + att_a - def_h + (s_a - s_h)
    lh=max(0.05,min(6.0,math.exp(lh_raw)))
    la=max(0.05,min(6.0,math.exp(la_raw)))
    return lh, la, lh-la

for it in range(MAX_ITER):
    bias_sum=defaultdict(float)
    bias_cnt=defaultdict(int)
    for m in filtered_train:
        lh, la, gd_pred = pred_lambdas(m, s_pivot)
        gd_actual=actual_gd(m)
        err=gd_pred - gd_actual
        lh_league=get_league_canon(m['homeName'])
        la_league=get_league_canon(m['awayName'])
        if lh_league in programme_leagues:
            bias_sum[lh_league]+=err
            bias_cnt[lh_league]+=1
        if la_league in programme_leagues:
            bias_sum[la_league]+= -err
            bias_cnt[la_league]+=1
    max_bias=0
    for lg in bias_sum:
        if bias_cnt[lg]==0: continue
        bias=bias_sum[lg]/bias_cnt[lg]
        max_bias=max(max_bias, abs(bias))
        s_pivot[lg]-=STEP*bias
    if (it+1)%10==0 or it<5:
        print(f"Iter {it+1:3d} max_bias {max_bias:+.5f} "+" ".join(f"{lg[:3]}={s_pivot[lg]:+.4f}" for lg in sorted(s_pivot)))
    if max_bias<TOL:
        print(f"Converged iter {it+1} max_bias {max_bias:.5f}")
        break

print("\nFinal s[L]:")
for lg in sorted(s_pivot):
    print(f"  {lg}: {s_pivot[lg]:+.5f}")

def evaluate(test_set, s_dict):
    mse=0; brier_sum=0; base_sum=0; n=0
    marg=[0,0,0]
    for m in test_set:
        marg[y_of(m)]+=1
    tot=len(test_set)
    base_probs=[c/tot for c in marg] if tot else [1/3]*3
    for m in test_set:
        lh, la, gd_pred = pred_lambdas(m, s_dict)
        gd_actual=actual_gd(m)
        mse+=(gd_pred-gd_actual)**2
        ph,pd,pa=grid_prob(lh, la)
        probs=[ph,pd,pa]
        y=y_of(m)
        brier_sum+=brier(probs,y)
        base_sum+=brier(base_probs,y)
        n+=1
    return (mse/n if n else 0, brier_sum/n if n else 0, base_sum/n if n else 0, n, base_probs)

mse_f, br_f, base_f, n_f, base_probs = evaluate(filtered_test, defaultdict(float))
mse_w, br_w, base_w, n_w, _ = evaluate(filtered_test, s_pivot)
print(f"\nValidation test n={n_w}")
print(f"  MSE frozen {mse_f:.4f} weighted {mse_w:.4f} imp {(mse_f-mse_w)/mse_f*100:+.2f}%")
print(f"  Brier frozen {br_f:.4f} weighted {br_w:.4f} base {base_f:.4f} imp vs frozen {(br_f-br_w)/br_f*100:+.2f}% vs base {(base_f-br_w)/base_f*100:+.2f}%")
print(f"  Base probs {base_probs}")

artifact={
    "store": STORE,
    "cutoff": CUTOFF,
    "train_filtered": len(filtered_train),
    "test_filtered": len(filtered_test),
    "s_pivot": dict(s_pivot),
    "hfa_per_league": {lg: hfa_per_league[lg] for lg in programme_leagues},
    "mu": mu,
    "mse_frozen": mse_f,
    "mse_weighted": mse_w,
    "improvement_pct_mse": (mse_f-mse_w)/mse_f*100 if mse_f else 0,
    "brier_frozen": br_f,
    "brier_weighted": br_w,
    "brier_base": base_f,
    "improvement_pct_brier_vs_frozen": (br_f-br_w)/br_f*100 if br_f else 0,
    "gain_vs_base_pct": (base_f-br_w)/base_f*100 if base_f else 0,
    "method": f"16193 corrected without fabricated ClubA/B, canon matching, full λ model, per-league HFA, bias loop step {STEP} tol {TOL} iter {MAX_ITER}, Poisson RHO {RHO} Brier, cutoff {CUTOFF}",
    "note": "Corrected store 16193 without 436 fabricated ClubA/B UCL rows, ≥100 samples, full λ, per-league HFA, Brier"
}
import json as js
with open("audit_work/league_pivot_16193_refined.json","w") as f:
    js.dump(artifact,f,indent=2)
with open("audit_work/dc-fitted-league-pivot-16193.json","w") as f:
    js.dump({"kind":"dc-fitted-league-pivot","version":"v3.11.0-league-pivot-16193","generatedAt":"2026-08-06T00:00:00Z","data":artifact,"note":"Corrected 16193"},f,indent=2)
print("Saved refined 16193")
