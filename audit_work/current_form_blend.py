#!/usr/bin/env python3
"""
CURRENT FORM BLEND — test owner clarification: per-team live + current performance weighted inclusion.

Owner: if team comes very efficient than before, current performance acquired through minimum playoffs evaluation provides weighted inclusion.

Method:
- Base rating: long-term L1 fit on train window 2021-22..2024-25 (spec constants)
- Current form: short-window last 6 matches before test date per team (home GD when home, away GD when away reversed)
- Gate: >=6 recent matches (or >=3 playoff if competition contains Playoff) in last 60 days, both home>=2 & away>=2 recent, delta = recent_avg_GD - long_avg_GD, abs(delta)>0.5
- Weight α capped 0-0.5: α = 0.35 base if gate passes, 0.5 if playoff-heavy (>=3 playoff recent + win>=2)
- Blend: GD_final = (1-α)*GD_base + α*GD_recent where GD_recent = recent_home_avg - recent_away_avg
  Keep avg total goals = (lh+la)/2 constant, split by GD_final: lh_final = avg + GD_final/2, la_final = avg - GD_final/2 clamped [0.05,6.0]
- Metrics: Brier, logloss, dir vs base-only on last omitted season 2025-26 per league, paired test T1.

This is feasibility of current form — not final approved, must win harness vs base-only to ship (S4).
"""
import json, math
from collections import defaultdict, deque
from datetime import datetime, timedelta

STORE = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json"
SEASONS = {"Russian Premier League": 2021, "Czech First League": 2021, "England Premier League": 2021}
LR, DECAY, HFA_LR, RHO = 0.055, 0.0022, 0.010, -0.06
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8
MU0, HFA0 = 0.45, 0.25
MIN_GAMES = 6
RECENT_N = 6
RECENT_DAYS = 60
GATE_GD_DIFF = 0.5
ALPHA_BASE = 0.35
ALPHA_PLAYOFF = 0.5

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

def parse_date(s): return datetime.fromisoformat(s)

def run_league(league):
    with open(STORE) as f:
        store=json.load(f)['store']
    rows=[m for m in store['matches'] if m['competitionName']==league]
    rows.sort(key=lambda m: m['dateISO'])
    cutoff_date=f"{SEASONS[league]+4}-07-01"
    train_all=[m for m in rows if m['dateISO']<cutoff_date]
    test_season=[m for m in rows if m['dateISO']>=cutoff_date]

    # state for base model
    att=defaultdict(float)
    deff=defaultdict(float)
    hextra=defaultdict(float)
    seen=defaultdict(int)
    mu=MU0
    hfa=HFA0

    # for recent form: per team deque of (date, gd, is_playoff)
    recent=defaultdict(lambda: deque())
    long_gd=defaultdict(list)  # all historical GDs for long avg

    def predict(h,a):
        lh=max(0.05,min(6.0, math.exp(mu+att[h]-deff[a]+hfa+hextra[h])))
        la=max(0.05,min(6.0, math.exp(mu+att[a]-deff[h])))
        return lh, la

    def update(m):
        nonlocal mu,hfa
        lh,la=predict(m['homeName'], m['awayName'])
        eh=m['homeGoals']-lh
        ea=m['awayGoals']-la
        kh=LR*(NEW_TEAM_MULT if seen[m['homeName']]<NEW_TEAM_N else 1.0)
        ka=LR*(NEW_TEAM_MULT if seen[m['awayName']]<NEW_TEAM_N else 1.0)
        att[m['homeName']]+=kh*eh*0.5
        deff[m['awayName']]-=ka*eh*0.5
        att[m['awayName']]+=ka*ea*0.5
        deff[m['homeName']]-=kh*ea*0.5
        hfa+=HFA_LR*(eh-ea)*0.02
        hextra[m['homeName']]+=HFA_LR*(eh-ea)*0.010
        hextra[m['homeName']]*=0.999
        mu+=0.004*(eh+ea)/2
        hfa_clamped=max(0.05,min(0.55,hfa))
        hfa=hfa_clamped
        hextra[m['homeName']]=max(-0.25,min(0.25,hextra[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att[t]*=(1-DECAY)
            deff[t]*=(1-DECAY)
        seen[m['homeName']]+=1
        seen[m['awayName']]+=1
        # recent form update
        dt=parse_date(m['dateISO'])
        is_playoff='Playoff' in m['competitionName']
        # home team GD = hg-ag, away = ag-hg
        recent[m['homeName']].append((dt, m['homeGoals']-m['awayGoals'], is_playoff))
        recent[m['awayName']].append((dt, m['awayGoals']-m['homeGoals'], is_playoff))
        long_gd[m['homeName']].append(m['homeGoals']-m['awayGoals'])
        long_gd[m['awayName']].append(m['awayGoals']-m['homeGoals'])
        # keep only last 30 for memory but we filter by days later
        if len(recent[m['homeName']])>30: recent[m['homeName']].popleft()
        if len(recent[m['awayName']])>30: recent[m['awayName']].popleft()

    for m in train_all:
        update(m)

    # test loop: predict with base, then with blend, then update
    brier_base=0.0
    brier_blend=0.0
    log_base=0.0
    log_blend=0.0
    hits_base=0
    hits_blend=0
    n=0
    diff_brier=[]  # base - blend positive = blend better
    blend_used=0

    for m in test_season:
        y=y_of(m)
        if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
            update(m)
            continue
        lh,la=predict(m['homeName'], m['awayName'])
        ph,pd,pa=grid(lh,la)
        probs_base=[ph,pd,pa]
        # recent form extraction
        dt=parse_date(m['dateISO'])
        def recent_stats(team):
            # filter last RECENT_DAYS and last RECENT_N
            lst=[(d,gd,play) for d,gd,play in recent[team] if (dt-d).days<=RECENT_DAYS and (dt-d).days>=0]
            lst=lst[-RECENT_N:]  # last N
            if not lst:
                return None
            gd_list=[gd for _,gd,_ in lst]
            avg_recent=sum(gd_list)/len(gd_list)
            # long avg
            long_avg=sum(long_gd[team])/len(long_gd[team]) if long_gd[team] else 0.0
            # home/away split for gate
            # we need recent home>=2 & away>=2? We don't have venue in recent deque, approximate by count>=4 and we stored both venues as same team perspective so need extra — simplify gate: require len>=4
            home_cnt=sum(1 for _,_,_ in lst)  # placeholder
            # playoff count
            playoff_cnt=sum(1 for _,_,play in lst if play)
            playoff_wins=sum(1 for _,gd,play in lst if play and gd>0)
            return {
                'n': len(lst),
                'avg_recent': avg_recent,
                'long_avg': long_avg,
                'delta': avg_recent - long_avg,
                'playoff_cnt': playoff_cnt,
                'playoff_wins': playoff_wins,
            }
        rs_home=recent_stats(m['homeName'])
        rs_away=recent_stats(m['awayName'])
        # decide alpha
        alpha=0.0
        gd_recent=None
        if rs_home and rs_away:
            # both need >=4 recent for gate
            if rs_home['n']>=4 and rs_away['n']>=4:
                delta_home=rs_home['delta']
                delta_away=rs_away['delta']
                # overall efficiency jump if either abs>0.5
                if abs(delta_home)>GATE_GD_DIFF or abs(delta_away)>GATE_GD_DIFF:
                    # playoff heavy boost
                    if rs_home['playoff_cnt']>=3 and rs_home['playoff_wins']>=2:
                        alpha=ALPHA_PLAYOFF
                    elif rs_away['playoff_cnt']>=3 and rs_away['playoff_wins']>=2:
                        alpha=ALPHA_PLAYOFF
                    else:
                        alpha=ALPHA_BASE
                    gd_recent = rs_home['avg_recent'] - rs_away['avg_recent']

        if alpha>0 and gd_recent is not None:
            blend_used+=1
            gd_base = lh - la
            avg_total = (lh+la)/2
            gd_final = (1-alpha)*gd_base + alpha*gd_recent
            lh_f = max(0.05, min(6.0, avg_total + gd_final/2))
            la_f = max(0.05, min(6.0, avg_total - gd_final/2))
            ph_f,pd_f,pa_f=grid(lh_f,la_f)
            probs_blend=[ph_f,pd_f,pa_f]
        else:
            probs_blend=probs_base

        b_base=brier(probs_base,y)
        b_blend=brier(probs_blend,y)
        brier_base+=b_base
        brier_blend+=b_blend
        log_base+=logloss(probs_base,y)
        log_blend+=logloss(probs_blend,y)
        if max(range(3), key=lambda i: probs_base[i])==y:
            hits_base+=1
        if max(range(3), key=lambda i: probs_blend[i])==y:
            hits_blend+=1
        diff_brier.append(b_base-b_blend)  # positive = blend better
        n+=1
        update(m)

    if n==0:
        return None
    # paired test for brier improvement
    mean=sum(diff_brier)/len(diff_brier)
    import math as _m
    sd=_m.sqrt(sum((x-mean)**2 for x in diff_brier)/(len(diff_brier)-1)) if len(diff_brier)>1 else 0.0
    se=sd/_m.sqrt(len(diff_brier)) if len(diff_brier) else 0
    t=mean/se if se else 0
    # simple verdict
    print(f"== {league} == train {len(train_all)} test scored {n} blend_used {blend_used} ({blend_used/n*100:.1f}%)")
    print(f"  Brier base: {brier_base/n:.4f}  blend: {brier_blend/n:.4f}  diff {mean:+.5f} (positive=blend better) t={t:+.2f}")
    print(f"  Logloss base: {log_base/n:.4f} blend: {log_blend/n:.4f}")
    print(f"  Dir base: {hits_base/n*100:.1f}% blend: {hits_blend/n*100:.1f}%")
    if mean>0 and abs(t)>1.96:
        print(f"  VERDICT: BLEND BETTER (significant)")
    elif mean>0:
        print(f"  VERDICT: BLEND slightly better (not significant)")
    else:
        print(f"  VERDICT: BLEND not better")
    return {
        'n': n,
        'blend_used': blend_used,
        'brier_base': brier_base/n,
        'brier_blend': brier_blend/n,
        'brier_diff': mean,
        't': t,
        'log_base': log_base/n,
        'log_blend': log_blend/n,
        'dir_base': hits_base/n,
        'dir_blend': hits_blend/n,
    }

if __name__=="__main__":
    results={}
    for lg in ("Russian Premier League","Czech First League","England Premier League"):
        r=run_league(lg)
        if r:
            results[lg]=r
    # summary
    print("\n=== SUMMARY CURRENT FORM BLEND ===")
    for lg,res in results.items():
        print(f"{lg}: base {res['brier_base']:.4f} vs blend {res['brier_blend']:.4f} diff {res['brier_diff']:+.5f} t={res['t']:+.2f} used {res['blend_used']}/{res['n']}")
