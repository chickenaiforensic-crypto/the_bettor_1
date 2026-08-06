#!/usr/bin/env python3
"""
LADDER RUN 16193 — corrected store without fabricated ClubA/B rows
"""
import json, math
from collections import defaultdict

STORE = "audit_work/pitch-rating-full-16193-corrected-2026-08-06.json"
SEASONS = {
    "Russian Premier League": 2021,
    "Czech First League": 2021,
    "England Premier League": 2021,
    "Italy Serie A": 2021,
    "Germany Bundesliga": 2021,
    "France Ligue 1": 2021,
    "Spain La Liga": 2021,
    "Scottish Premiership": 2021,
    "Kosovo Superliga": 2021,
}
HOLDOUTS = [1,2,3,5,8,10,15,20,25,30,"FULL"]

LR, DECAY, HFA_LR, RHO = 0.055, 0.0022, 0.010, -0.06
NEW_TEAM_MULT, NEW_TEAM_N = 1.6, 8
MU0, HFA0 = 0.45, 0.25
MIN_GAMES = 6

def pmf(k, lam): return math.exp(-lam) * lam**k / math.factorial(k)
def grid(lam_h, lam_a):
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
def logloss(probs,y): return -math.log(max(probs[y],1e-9))
def y_of(m): return 0 if m['homeGoals']>m['awayGoals'] else (1 if m['homeGoals']==m['awayGoals'] else 2)
def outcome(probs): return max(range(3), key=lambda i: probs[i])

def run_ladder(league):
    with open(STORE) as f:
        data=json.load(f)
        store=data['store'] if 'store' in data else data
        # wrapper['matches'] is corrected list
        matches=store['matches'] if 'matches' in store else []
        # if store itself is wrapper, matches is at store['matches']
        # but we need to handle structure: data['store'] is wrapper containing matches
        if 'matches' not in store and 'store' in data:
            # maybe data['store']['matches']?
            wrapper=data['store']
            matches=wrapper.get('matches',[])
    rows=[m for m in matches if m['competitionName']==league]
    rows.sort(key=lambda m: m['dateISO'])
    if not rows:
        return {"refused":"no rows"}
    cutoff=f"{SEASONS[league]+4}-07-01"
    train_all=[m for m in rows if m['dateISO']<cutoff]
    test_season=[m for m in rows if m['dateISO']>=cutoff]
    if not test_season:
        return {"refused":f"no test season after {cutoff}"}
    res={}
    for h in HOLDOUTS:
        nhold=len(test_season) if h=="FULL" else h
        if nhold>len(test_season):
            res[str(h)]={"n":0,"scored":0,"holdout":nhold,"insufficient":True,"reason":f"holdout {nhold} > test {len(test_season)}"}
            continue
        train=train_all + test_season[:-nhold] if nhold < len(test_season) else train_all
        test=test_season[-nhold:]
        att, deff, hextra, seen=defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(int)
        mu, hfa=MU0, HFA0
        def predict(home, away):
            lh=max(0.05,min(6.0, math.exp(mu+att[home]-deff[away]+hfa+hextra[home])))
            la=max(0.05,min(6.0, math.exp(mu+att[away]-deff[home])))
            return lh, la
        def update(m):
            nonlocal mu, hfa
            lh, la=predict(m['homeName'], m['awayName'])
            eh, ea=m['homeGoals']-lh, m['awayGoals']-la
            kh=LR*(NEW_TEAM_MULT if seen[m['homeName']]<NEW_TEAM_N else 1.0)
            ka=LR*(NEW_TEAM_MULT if seen[m['awayName']]<NEW_TEAM_N else 1.0)
            att[m['homeName']]+=kh*eh*0.5; deff[m['awayName']]-=ka*eh*0.5
            att[m['awayName']]+=ka*ea*0.5; deff[m['homeName']]-=kh*ea*0.5
            hfa+=HFA_LR*(eh-ea)*0.02
            hextra[m['homeName']]+=HFA_LR*(eh-ea)*0.010
            hextra[m['homeName']]*=0.999
            mu+=0.004*(eh+ea)/2
            hfa=max(0.05,min(0.55,hfa))
            hextra[m['homeName']]=max(-0.25,min(0.25,hextra[m['homeName']]))
            for t in (m['homeName'], m['awayName']):
                att[t]*=(1-DECAY); deff[t]*=(1-DECAY)
            seen[m['homeName']]+=1; seen[m['awayName']]+=1
        for m in train: update(m)
        b=bl=hits=n=0.0
        marg=[0.0]*3
        for m in test:
            y=y_of(m); marg[y]+=1
            if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
                update(m); continue
            lh, la=predict(m['homeName'], m['awayName'])
            probs=list(grid(lh, la))
            b+=brier(probs,y); bl+=logloss(probs,y)
            if outcome(probs)==y: hits+=1
            n+=1
            update(m)
        tot=len(test)
        base=[c/tot for c in marg]
        b_base=sum(brier(base, y_of(m)) for m in test)/tot if tot else 0
        # second pass for paired
        att=defaultdict(float); deff=defaultdict(float); hextra=defaultdict(float); seen=defaultdict(int); mu=MU0; hfa=HFA0
        def predict2(h,a):
            lh=max(0.05,min(6.0, math.exp(mu+att[h]-deff[a]+hfa+hextra[h])))
            la=max(0.05,min(6.0, math.exp(mu+att[a]-deff[h])))
            return lh, la
        def update2(m):
            nonlocal mu, hfa
            lh, la=predict2(m['homeName'], m['awayName'])
            eh, ea=m['homeGoals']-lh, m['awayGoals']-la
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
        for m in train: update2(m)
        diffs=[]
        per_side_dc_home=[]; per_side_dc_draw=[]; per_side_dc_away=[]
        per_side_base_home=[]; per_side_base_draw=[]; per_side_base_away=[]
        for m in test:
            y=y_of(m)
            if seen[m['homeName']]<MIN_GAMES or seen[m['awayName']]<MIN_GAMES:
                update2(m); continue
            lh, la=predict2(m['homeName'], m['awayName'])
            probs=list(grid(lh, la))
            b_dc=brier(probs,y)
            b_bs=brier(base,y)
            diffs.append(b_bs-b_dc)
            per_side_dc_home.append((probs[0]-(1 if y==0 else 0))**2)
            per_side_dc_draw.append((probs[1]-(1 if y==1 else 0))**2)
            per_side_dc_away.append((probs[2]-(1 if y==2 else 0))**2)
            per_side_base_home.append((base[0]-(1 if y==0 else 0))**2)
            per_side_base_draw.append((base[1]-(1 if y==1 else 0))**2)
            per_side_base_away.append((base[2]-(1 if y==2 else 0))**2)
            update2(m)
        import math as mymath
        mean=sum(diffs)/len(diffs) if diffs else 0
        sd=mymath.sqrt(sum((x-mean)**2 for x in diffs)/(len(diffs)-1)) if len(diffs)>1 else 0
        se=sd/mymath.sqrt(len(diffs)) if diffs else 0
        t=mean/se if se else 0
        p=2*(1-0.5*(1+mymath.erf(abs(t)/mymath.sqrt(2)))) if se else 1
        mde=2.8*sd/mymath.sqrt(len(diffs)) if diffs else 0
        gain=(b_base - (b/n if n else 0))/b_base*100 if b_base else 0
        res[str(h)]={
            "n": int(n),
            "scored": int(n),
            "refused": int(tot-n),
            "holdout": nhold,
            "brier": round(b/n,4) if n else 0,
            "brier_base": round(b_base,4),
            "logloss": round(bl/n,4) if n else 0,
            "dir_acc": round(hits/n*100,1) if n else 0,
            "gain_pct": round(gain,2),
            "brier_side_dc": {
                "home": round(sum(per_side_dc_home)/len(per_side_dc_home),4) if per_side_dc_home else 0,
                "draw": round(sum(per_side_dc_draw)/len(per_side_dc_draw),4) if per_side_dc_draw else 0,
                "away": round(sum(per_side_dc_away)/len(per_side_dc_away),4) if per_side_dc_away else 0,
            },
            "brier_side_base": {
                "home": round(sum(per_side_base_home)/len(per_side_base_home),4) if per_side_base_home else 0,
                "draw": round(sum(per_side_base_draw)/len(per_side_base_draw),4) if per_side_base_draw else 0,
                "away": round(sum(per_side_base_away)/len(per_side_base_away),4) if per_side_base_away else 0,
            },
            "paired": {
                "n": len(diffs),
                "meanDelta": round(mean,5),
                "sd": round(sd,5),
                "se": round(se,5),
                "t": round(t,2),
                "df": len(diffs)-1,
                "pTwo": round(p,6),
                "mde80": round(mde,5),
            },
            "trainWindow": [train[0]['dateISO'] if train else None, train[-1]['dateISO'] if train else None],
            "trainRows": len(train),
            "lastSeasonWindow": [test_season[0]['dateISO'], test_season[-1]['dateISO']],
            "lastSeasonRows": len(test_season),
        }
    return res

if __name__=="__main__":
    out={}
    for lg in SEASONS.keys():
        print(f"== {lg} ==")
        r=run_ladder(lg)
        out[lg]=r
        if "FULL" in r and "brier" in r["FULL"]:
            print(f"  FULL: Brier {r['FULL']['brier']} base {r['FULL']['brier_base']} gain {r['FULL']['gain_pct']}% p {r['FULL']['paired']['pTwo']}")
    with open("audit_work/ladder_baseline_2026-08-06_16193.json","w") as f:
        import json
        json.dump({"date":"2026-08-06","store":STORE,"engine":"DC online, spec B3 constants, naive init, 9 leagues, corrected 16193 without fabricated ClubA/B","results":out}, f, indent=2)
    print("\nartifact: audit_work/ladder_baseline_2026-08-06_16193.json")
    gains=[]
    for lg, data in out.items():
        if "FULL" in data and "gain_pct" in data["FULL"]:
            gains.append(data["FULL"]["gain_pct"])
    if gains:
        print(f"Average gain FULL across {len(gains)} leagues: {sum(gains)/len(gains):.2f}%")
