#!/usr/bin/env python3
"""
CURRENT FORM BLEND v2 — retuned per 14 experiment FAIL.

Retune per 14 recommendations:
1. Playoff-only current form (not generic recent 6)
2. Lower α 0.15-0.20 max not 0.35-0.5
3. Efficiency relative to expectation: delta = recent_avg_GD - expected_GD_from_base (not recent - long avg)
"""
import json, math
from collections import defaultdict, deque
from datetime import datetime

STORE = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json"
SEASONS = {"Russian Premier League": 2021, "Czech First League": 2021, "England Premier League": 2021}
LR, DECAY, HFA_LR, RHO = 0.055, 0.0022, 0.010, -0.06
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8
MU0, HFA0 = 0.45, 0.25
MIN_GAMES = 6
RECENT_DAYS = 60
ALPHA_PLAYOFF_ONLY = 0.15
GATE_PLAYOFF_MIN = 3
GATE_GD_DIFF = 0.5

def pmf(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)
def grid(lh,la):
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
    return ph,pd,1-ph-pd

def brier(probs,y): return sum((pr-(1.0 if i==y else 0.0))**2 for i,pr in enumerate(probs))
def y_of(m): return 0 if m['homeGoals']>m['awayGoals'] else (1 if m['homeGoals']==m['awayGoals'] else 2)
def parse_date(s): return datetime.fromisoformat(s)

def run_league(league):
    with open(STORE) as f:
        store=json.load(f)['store']
    rows=[m for m in store['matches'] if m['competitionName']==league]
    rows.sort(key=lambda m: m['dateISO'])
    cutoff=f"{SEASONS[league]+4}-07-01"
    train_all=[m for m in rows if m['dateISO']<cutoff]
    test_season=[m for m in rows if m['dateISO']>=cutoff]

    att=defaultdict(float); deff=defaultdict(float); hextra=defaultdict(float); seen=defaultdict(int); mu=MU0; hfa=HFA0
    recent=defaultdict(lambda: deque())  # (date, gd, is_playoff, exp_gd)
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
        hfa=max(0.05,min(0.55,hfa)); hextra[m['homeName']]=max(-0.25,min(0.25,hextra[m['homeName']]))
        for t in (m['homeName'], m['awayName']):
            att[t]*=(1-DECAY); deff[t]*=(1-DECAY)
        seen[m['homeName']]+=1; seen[m['awayName']]+=1
        dt=parse_date(m['dateISO'])
        is_playoff='Playoff' in m['competitionName']
        # expected GD from model at that time (before update? use current lh,la for simplicity after)
        # For efficiency relative to expectation we store expected GD
        exp_gd = lh - la if m['homeName']==m['homeName'] else 0  # placeholder
        # Actually home team expected GD = lh - la, away = la - lh
        recent[m['homeName']].append((dt, m['homeGoals']-m['awayGoals'], is_playoff, lh-la))
        recent[m['awayName']].append((dt, m['awayGoals']-m['homeGoals'], is_playoff, la-lh))
        if len(recent[m['homeName']])>30: recent[m['homeName']].popleft()
        if len(recent[m['awayName']])>30: recent[m['awayName']].popleft()

    for m in train_all: update(m)

    b_base=0; b_blend=0; n=0; diff=[]; used=0
    for m in test_season:
        y=y_of(m)
        if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
            update(m); continue
        lh,la=predict(m['homeName'], m['awayName'])
        ph,pd,pa=grid(lh,la)
        base=[ph,pd,pa]
        dt=parse_date(m['dateISO'])
        def get_playoff_recent(team):
            lst=[(d,gd,play,exp) for d,gd,play,exp in recent[team] if (dt-d).days<=RECENT_DAYS and (dt-d).days>=0 and play]
            # last N playoff
            lst=lst[-6:]
            if len(lst)<GATE_PLAYOFF_MIN:
                return None
            # efficiency relative to expectation: actual GD - expected GD
            eff=[gd-exp for _,gd,_,exp in lst]
            avg_eff=sum(eff)/len(eff)
            avg_gd=sum(gd for _,gd,_,_ in lst)/len(lst)
            wins=sum(1 for _,gd,_,_ in lst if gd>0)
            return {'n':len(lst), 'avg_gd':avg_gd, 'avg_eff':avg_eff, 'wins':wins}
        rh=get_playoff_recent(m['homeName'])
        ra=get_playoff_recent(m['awayName'])
        alpha=0.0
        gd_recent=None
        if rh and ra:
            # both have playoff recent >=3
            # gate: efficiency jump abs>0.5
            if abs(rh['avg_eff'])>GATE_GD_DIFF or abs(ra['avg_eff'])>GATE_GD_DIFF:
                alpha=ALPHA_PLAYOFF_ONLY
                gd_recent=rh['avg_gd']-ra['avg_gd']
        elif rh and not ra:
            # only home has playoff recent
            if abs(rh['avg_eff'])>GATE_GD_DIFF:
                alpha=ALPHA_PLAYOFF_ONLY
                gd_recent=rh['avg_gd'] - 0.0  # away no recent -> 0
        elif ra and not rh:
            if abs(ra['avg_eff'])>GATE_GD_DIFF:
                alpha=ALPHA_PLAYOFF_ONLY
                gd_recent=0.0 - ra['avg_gd']

        if alpha>0 and gd_recent is not None:
            used+=1
            gd_base=lh-la
            avg_total=(lh+la)/2
            gd_final=(1-alpha)*gd_base + alpha*gd_recent
            lh_f=max(0.05,min(6.0, avg_total + gd_final/2))
            la_f=max(0.05,min(6.0, avg_total - gd_final/2))
            ph_f,pd_f,pa_f=grid(lh_f,la_f)
            blend=[ph_f,pd_f,pa_f]
        else:
            blend=base

        b_base+=brier(base,y); b_blend+=brier(blend,y)
        diff.append(brier(base,y)-brier(blend,y))
        n+=1
        update(m)

    if n==0:
        return None
    mean=sum(diff)/len(diff)
    import math as _m
    sd=_m.sqrt(sum((x-mean)**2 for x in diff)/(len(diff)-1)) if len(diff)>1 else 0.0
    se=sd/_m.sqrt(len(diff)) if len(diff) else 0
    t=mean/se if se else 0
    print(f"== {league} v2 playoff-only α={ALPHA_PLAYOFF_ONLY} == train {len(train_all)} test {n} used {used} ({used/n*100:.1f}%)")
    print(f"  Brier base {b_base/n:.4f} blend {b_blend/n:.4f} diff {mean:+.5f} t={t:+.2f} {'BETTER' if mean>0 and abs(t)>1.96 else 'not better'}")
    return {'n':n,'used':used,'base':b_base/n,'blend':b_blend/n,'diff':mean,'t':t}

if __name__=="__main__":
    for lg in ("Russian Premier League","Czech First League","England Premier League"):
        run_league(lg)
