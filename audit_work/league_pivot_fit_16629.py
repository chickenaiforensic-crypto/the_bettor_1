#!/usr/bin/env python3
"""Fresh P1-safe cross-league pivot re-fit on the 16,629-row store (2026-08-06).

Owner-required changes: >=100 UEFA test rows (614 valid dated rows from 2024-07-01),
full Poisson lambda model, domestic fitted per-league HFA, H/D/A Brier validation,
100 deterministic iterations with step .05, and nine-domestic-league re-filtering.
No market data is read or used.
"""
import datetime as dt
import json, math
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
STORE=ROOT/'audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json'
OUT=ROOT/'audit_work/league_pivot_16629_artifact.json'
CUTOFF='2024-07-01'; STEP=.05; ITERATIONS=100
DOMESTIC={'Russian Premier League':'RUS','Czech First League':'CZE','England Premier League':'ENG','Italy Serie A':'ITA','Germany Bundesliga':'GER','France Ligue 1':'FRA','Spain La Liga':'SPA','Scottish Premiership':'SCO','Kosovo Superliga':'KOS'}
UEFA={'UEFA Champions League','UEFA Europa League','UEFA Conference League'}
LR,DECAY,HFA_LR,MU0,HFA0,RHO=.055,.0022,.010,.45,.25,-.06
NEW_MULT,NEW_N=1.6,8

def canon(x): return ''.join(c for c in x.lower() if c.isalnum())
def pmf(k,l): return math.exp(-l)*l**k/math.factorial(k)
def probs(lh,la):
    q=[]
    for h in range(11):
      for a in range(11):
        corr=1-lh*la*RHO if h==a==0 else 1+lh*RHO if h==0 and a==1 else 1+la*RHO if h==1 and a==0 else 1-RHO if h==a==1 else 1
        q.append((h,a,pmf(h,lh)*pmf(a,la)*corr))
    z=sum(v for _,_,v in q)
    return (sum(v for h,a,v in q if h>a)/z,sum(v for h,a,v in q if h==a)/z,sum(v for h,a,v in q if h<a)/z)
def outcome(m): return 0 if m['homeGoals']>m['awayGoals'] else 1 if m['homeGoals']==m['awayGoals'] else 2
def brier(p,y): return sum((p[i]-(i==y))**2 for i in range(3))
def valid(m):
    try: dt.date.fromisoformat(m['dateISO']); return True
    except (TypeError,ValueError): return False

def main():
  data=json.load(STORE.open())['store']['matches']
  domestic=[m for m in data if m['competitionName'] in DOMESTIC and valid(m) and m['dateISO']<CUTOFF]
  domestic.sort(key=lambda m:(m['dateISO'],m['competitionName'],m['homeName'],m['awayName']))
  # Canonical domestic team -> single league; ambiguous names are omitted from cross-league mapping.
  membership=defaultdict(Counter)
  for m in domestic:
    membership[canon(m['homeName'])][m['competitionName']]+=1; membership[canon(m['awayName'])][m['competitionName']]+=1
  team_league={k:c.most_common(1)[0][0] for k,c in membership.items() if len(c)==1}
  att=defaultdict(float); deff=defaultdict(float); hx=defaultdict(float); seen=defaultdict(int); hfa=defaultdict(lambda:HFA0); mu=MU0
  def domestic_lam(h,a,lg):
    return max(.05,min(6,math.exp(mu+att[h]-deff[a]+hfa[lg]+hx[h]))),max(.05,min(6,math.exp(mu+att[a]-deff[h])))
  for m in domestic:
    h,a,lg=m['homeName'],m['awayName'],m['competitionName']; lh,la=domestic_lam(h,a,lg); eh,ea=m['homeGoals']-lh,m['awayGoals']-la
    kh=LR*(NEW_MULT if seen[h]<NEW_N else 1);ka=LR*(NEW_MULT if seen[a]<NEW_N else 1)
    att[h]+=kh*eh*.5;deff[a]-=ka*eh*.5;att[a]+=ka*ea*.5;deff[h]-=kh*ea*.5
    hfa[lg]=max(.05,min(.55,hfa[lg]+HFA_LR*(eh-ea)*.02));hx[h]=max(-.25,min(.25,(hx[h]+HFA_LR*(eh-ea)*.010)*.999));mu+=.004*(eh+ea)/2
    for t in (h,a):att[t]*=1-DECAY;deff[t]*=1-DECAY;seen[t]+=1
  # UEFA rows use canonical names to map all nine domestic leagues; retain rows with >=1 mapped programme side.
  invalid=[m for m in data if m['competitionName'] in UEFA and not valid(m)]
  uefa=[m for m in data if m['competitionName'] in UEFA and valid(m)]
  scoped=[]
  for m in uefa:
    m=dict(m);m['hkey']=canon(m['homeName']);m['akey']=canon(m['awayName']);m['hlg']=team_league.get(m['hkey']);m['alg']=team_league.get(m['akey'])
    if m['hlg'] or m['alg']: scoped.append(m)
  scoped.sort(key=lambda m:(m['dateISO'],m['competitionName'],m['homeName'],m['awayName']))
  # Validation population is every valid UEFA result, not only the mapped subset:
  # this is the owner's 614-row post-cutoff population. Unmapped foreign clubs
  # retain the neutral zero-rating prior; they contribute to Brier but cannot
  # create a league-pivot gradient. The mapped subset remains diagnostic coverage.
  all_uefa=sorted((dict(m, hkey=canon(m['homeName']), akey=canon(m['awayName']), hlg=team_league.get(canon(m['homeName'])), alg=team_league.get(canon(m['awayName']))) for m in uefa), key=lambda m:(m['dateISO'],m['competitionName'],m['homeName'],m['awayName']))
  train=[m for m in all_uefa if m['dateISO']<CUTOFF];test=[m for m in all_uefa if m['dateISO']>=CUTOFF]
  # λ model: domestic fitted attack/defence + home league HFA + learned relative pivots.
  piv=defaultdict(float)
  def lambdas(m,p):
    hl,al=m['hlg'],m['alg']; hs=p[hl] if hl else 0.;as_=p[al] if al else 0.
    hh=hfa[hl] if hl else HFA0
    lh=max(.05,min(6,math.exp(mu+att[m['homeName']]-deff[m['awayName']]+hh+hs-as_+hx[m['homeName']])))
    la=max(.05,min(6,math.exp(mu+att[m['awayName']]-deff[m['homeName']]+as_-hs+hx[m['awayName']])))
    return lh,la
  # Poisson score-gradient fit; paired +/- pivot updates preserve the relative-strength anchor.
  history=[]
  for it in range(ITERATIONS):
    grad=defaultdict(float); count=defaultdict(int)
    for m in train:
      lh,la=lambdas(m,piv); errh=m['homeGoals']-lh; erra=m['awayGoals']-la
      if m['hlg']: grad[m['hlg']]+=errh-erra;count[m['hlg']]+=1
      if m['alg']: grad[m['alg']]+=erra-errh;count[m['alg']]+=1
    maxchange=0.
    for lg in DOMESTIC:
      if count[lg]:
        change=STEP*grad[lg]/count[lg];piv[lg]+=change;maxchange=max(maxchange,abs(change))
    # centre fitted pivots so absolute intercept stays fixed.
    active=[lg for lg in DOMESTIC if count[lg]]; centre=sum(piv[lg] for lg in active)/len(active)
    for lg in active:piv[lg]-=centre
    if it in (0,9,24,49,74,99): history.append({'iteration':it+1,'max_step':maxchange,'pivots':{DOMESTIC[k]:round(piv[k],6) for k in active}})
  def score(rows,p):
    vals=[brier(probs(*lambdas(m,p)),outcome(m)) for m in rows]
    return sum(vals)/len(vals)
  frozen=score(test,defaultdict(float)); fitted=score(test,piv); improvement=(frozen-fitted)/frozen*100
  coverage=Counter()
  for m in scoped:
    if m['hlg']:coverage[m['hlg']]+=1
    if m['alg']:coverage[m['alg']]+=1
  artifact={'date':'2026-08-06','store':str(STORE.relative_to(ROOT)),'method':'frozen domestic online ratings through cutoff; full Poisson lambdas; per-league domestic HFA; Poisson H/D/A grid Brier; outcome-only','cutoff':CUTOFF,'iterations':ITERATIONS,'step':STEP,'domestic_fit_rows':len(domestic),'uefa_invalid_dates_excluded':len(invalid),'uefa_valid_rows':len(uefa),'in_scope_rows':len(scoped),'train_rows':len(train),'test_rows':len(test),'test_requirement':'>=100','test_requirement_pass':len(test)>=100,'league_coverage':dict(coverage),'pivots_log_goals':{DOMESTIC[k]:round(piv[k],6) for k in DOMESTIC if coverage[k]},'brier_frozen':round(frozen,6),'brier_weighted':round(fitted,6),'brier_improvement_pct':round(improvement,4),'iteration_checkpoints':history,'p1_market_data_used':False}
  json.dump(artifact,OUT.open('w'),indent=2)
  print(json.dumps(artifact,indent=2));print('wrote',OUT)
if __name__=='__main__':main()
