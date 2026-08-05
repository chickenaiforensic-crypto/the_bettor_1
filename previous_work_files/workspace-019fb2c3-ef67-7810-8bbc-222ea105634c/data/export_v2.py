"""Export everything the app needs for star v2 + the tactical consensus layer."""
import pickle, json, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
st=pickle.load(open("model_state.pkl","rb"))
gc=pickle.load(open("goals_calib.pkl","rb"))

TIER={**{l:1 for l in ['E0','SC0','D1','SP1','I1','F1','N1','B1','P1','T1','G1']},
      **{l:2 for l in ['E1','D2','SP2','I2','F2']},**{l:3 for l in ['E2','E3']}}
MIN=5; SHRINK=6

# ---- rebuild star assignments over full history to fit the draw tables ----
rec=defaultdict(lambda:{'p':0,'w':0,'d':0})
pool=defaultdict(dict); lgm=defaultdict(lambda:[0.0,0]); prev={}
BOUND=[0.2,0.4,0.6,0.8]; HYST=0.05
star_of={}
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    key=(lg,se)
    lm=lgm[key][0]/lgm[key][1] if lgm[key][1]>0 else 1.35
    vals=sorted(pool[key].values())
    def st_(team):
        d=rec[(lg,se,team)]
        if d['p']<MIN or len(vals)<8: return None
        raw=(3*d['w']+d['d'])/d['p']
        v=(raw*d['p']+lm*SHRINK)/(d['p']+SHRINK)
        pct=sum(1 for x in vals if x<v)/len(vals)
        s=min(5,max(1,int(pct*5)+1))
        p=prev.get((lg,se,team))
        if p is not None and s!=p:
            if s>p:
                b=BOUND[p-1] if 1<=p<=4 else None
                if b is not None and pct<b+HYST: s=p
            else:
                b=BOUND[s-1] if 1<=s<=4 else None
                if b is not None and pct>b-HYST: s=p
        return s
    sh,sa=st_(h),st_(a)
    if sh: prev[(lg,se,h)]=sh
    if sa: prev[(lg,se,a)]=sa
    if sh and sa: star_of[(lg,se,m['date'],h,a)]=(sh,sa)
    for t,is_h in ((h,True),(a,False)):
        d=rec[(lg,se,t)]
        won=(m['res']=='H' and is_h) or (m['res']=='A' and not is_h)
        d['p']+=1
        if won: d['w']+=1
        elif m['res']=='D': d['d']+=1
        if d['p']>=MIN: pool[key][t]=(3*d['w']+d['d'])/d['p']
    lgm[key][0]+=3 if m['res']!='D' else 2; lgm[key][1]+=2

# ---- fit per-tier draw tables on ALL history ----
tt=defaultdict(lambda:[0,0]); tbase={}
for m in rows:
    k=(m['lg'],m['season'],m['date'],m['home'],m['away'])
    if k not in star_of: continue
    t=TIER.get(m['lg'],1); sh,sa=star_of[k]
    x=tt[(t,sh-sa)]; x[0]+=1; x[1]+=(m['res']=='D')
for t in (1,2,3):
    v=[m for m in rows if TIER.get(m['lg'],1)==t and (m['lg'],m['season'],m['date'],m['home'],m['away']) in star_of]
    tbase[t]=sum(1 for m in v if m['res']=='D')/len(v)
draw_tab={f"{t}|{g}": round(v[1]/v[0],5) for (t,g),v in tt.items() if v[0]>=150}
print(f"draw table cells: {len(draw_tab)}")

# ---- current team records for the LATEST season, for stars + consensus ----
latest={}
for m in rows:
    latest[m['lg']]=max(latest.get(m['lg'],''),m['season'])
tr=defaultdict(lambda:{'p':0,'w':0,'d':0,'hp':0,'hgf':0,'hga':0,'ap':0,'agf':0,'aga':0})
for m in rows:
    lg,se=m['lg'],m['season']
    if se!=latest.get(lg): continue
    h,a=m['home'],m['away']
    H=tr[(lg,h)]; A=tr[(lg,a)]
    H['p']+=1; A['p']+=1
    H['hp']+=1; H['hgf']+=m['hg']; H['hga']+=m['ag']
    A['ap']+=1; A['agf']+=m['ag']; A['aga']+=m['hg']
    if m['res']=='H': H['w']+=1
    elif m['res']=='A': A['w']+=1
    else: H['d']+=1; A['d']+=1
records={}
for (lg,t),d in tr.items():
    if d['p']<1: continue
    records.setdefault(lg,{})[t]=[d['p'],d['w'],d['d'],d['hp'],d['hgf'],d['hga'],d['ap'],d['agf'],d['aga']]
print(f"team records exported: {sum(len(v) for v in records.values())} across {len(records)} leagues")

NAMES={'E0':'England Premier League','E1':'England Championship','E2':'England League One','E3':'England League Two',
'SC0':'Scotland Premiership','D1':'Germany Bundesliga','D2':'Germany 2. Bundesliga','SP1':'Spain La Liga',
'SP2':'Spain Segunda','I1':'Italy Serie A','I2':'Italy Serie B','F1':'France Ligue 1','F2':'France Ligue 2',
'N1':'Netherlands Eredivisie','B1':'Belgium Pro League','P1':'Portugal Primeira Liga','T1':'Turkey Super Lig',
'G1':'Greece Super League'}
active=set()
for m in rows:
    if m['season'] in ('2425','2526'): active.add((m['lg'],m['home'])); active.add((m['lg'],m['away']))
teams={}
for lg,t in sorted(active):
    if t in st['att']:
        teams.setdefault(lg,{})[t]=[round(st['att'][t],4),round(st['dfn'][t],4),round(st['thfa'].get(t,0.0),4)]
hosted=defaultdict(set)
for m in rows: hosted[m['lg']].add(m['home'])

out=dict(
 version="pitch-rating-v2.0", built="2026-07-30",
 source="153,058 match results, 18 leagues, 2003-2026. NO bookmaker data.",
 rho=-0.06, goals_shrink=gc['k'], goals_mu=round(gc['mu'],4),
 leagues={lg:{"name":NAMES.get(lg,lg),"mu":round(st['mu'][lg],4),"hfa":round(st['hfa'][lg],4),
              "tier":TIER.get(lg,1)} for lg in sorted(st['hfa'])},
 teams=teams,
 hosted={lg:sorted(v) for lg,v in hosted.items()},
 records=records,
 star_min_games=MIN, star_shrink=SHRINK, star_hyst=HYST,
 draw_table=draw_tab, draw_base={str(k):round(v,5) for k,v in tbase.items()},
 star_weight={"1":0.2,"2":0.5,"3":0.5}, star_cap=0.02,
 consensus={"strong":1.5,"confirmed":1.0,"draw_lean":0.2,"min_games":4},
 tiers=[["A+ Fortress",0.70,0.785,0.141,0.074,7718],["A Strong",0.60,0.642,0.216,0.142,11799],
        ["B Lean",0.52,0.547,0.260,0.193,20335],["C Marginal",0.45,0.475,0.283,0.242,28246],
        ["D Coin-flip",0.35,0.408,0.299,0.293,44718],["E Avoid",0.0,0.282,0.268,0.450,37544]],
 markets={"1X2":1.7,"DC":1.6,"DNB":1.9,"O15":1.8,"O25":2.7,"H-1":3.0,"O35":3.3,"BTTS":6.0},
 ship=["1X2","DC","DNB","O15","O25"], caution=["H-1","O35"], blocked=["BTTS"],
 calibration={"max_error_pct":1.7,"brier":0.6112,"brier_base":0.6476,"n":150360},
 validation={"star_gain_pct":0.047,"star_p":0.0000,"consensus_strong_pct":78.6,
             "consensus_confirmed_pct":74.8,"base_top10_pct":73.0},
)
json.dump(out,open("/home/user/pitch_ratings_v2.json","w"),separators=(",",":"))
import os
print(f"size {os.path.getsize('/home/user/pitch_ratings_v2.json'):,} bytes")
