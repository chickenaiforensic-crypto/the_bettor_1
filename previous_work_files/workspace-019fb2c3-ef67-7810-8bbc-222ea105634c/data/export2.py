import pickle, json, math
st=pickle.load(open("model_state.pkl","rb"))
gc=pickle.load(open("goals_calib.pkl","rb"))
rows=pickle.load(open("all_matches.pkl","rb"))
active=set()
for m in rows:
    if m['season'] in ('2425','2526'):
        active.add((m['lg'],m['home'])); active.add((m['lg'],m['away']))
# also record which grounds each team has hosted at (flip detection)
hosted=set()
for m in rows: hosted.add((m['lg'],m['home']))
teams={}
for lg,t in sorted(active):
    if t not in st['att']: continue
    teams.setdefault(lg,{})[t]=[round(st['att'][t],4),round(st['dfn'][t],4),round(st['thfa'].get(t,0.0),4)]
NAMES={'E0':'England Premier League','E1':'England Championship','E2':'England League One','E3':'England League Two',
'SC0':'Scotland Premiership','D1':'Germany Bundesliga','D2':'Germany 2. Bundesliga','SP1':'Spain La Liga',
'SP2':'Spain Segunda','I1':'Italy Serie A','I2':'Italy Serie B','F1':'France Ligue 1','F2':'France Ligue 2',
'N1':'Netherlands Eredivisie','B1':'Belgium Pro League','P1':'Portugal Primeira Liga','T1':'Turkey Super Lig',
'G1':'Greece Super League'}
out=dict(
 version="pitch-rating-v1.1", built="2026-07-29",
 source="153,058 match results, 18 leagues, 2003-2026. NO bookmaker data.",
 note="teams[lg][name] = [att, dfn, home_extra]",
 rho=-0.06, goals_shrink=gc['k'], goals_mu=round(gc['mu'],4),
 leagues={lg:{"name":NAMES.get(lg,lg),"mu":round(st['mu'][lg],4),"hfa":round(st['hfa'][lg],4)} for lg in sorted(st['hfa'])},
 teams=teams,
 hosted={lg:sorted(set(t for l,t in hosted if l==lg)) for lg in sorted(set(l for l,_ in hosted))},
 tiers=[["A+ Fortress",0.70,0.785,0.141,0.074,7718],["A Strong",0.60,0.642,0.216,0.142,11799],
        ["B Lean",0.52,0.547,0.260,0.193,20335],["C Marginal",0.45,0.475,0.283,0.242,28246],
        ["D Coin-flip",0.35,0.408,0.299,0.293,44718],["E Avoid",0.0,0.282,0.268,0.450,37544]],
 markets={"1X2":1.7,"DC":1.6,"DNB":1.9,"O15":1.8,"O25":2.7,"H-1":3.0,"O35":3.3,"BTTS":6.0},
 ship=["1X2","DC","DNB","O15","O25"], caution=["H-1","O35"], blocked=["BTTS"],
 calibration={"max_error_pct":1.7,"brier":0.6112,"brier_base":0.6476,"n":150360},
)
json.dump(out,open("/home/user/pitch_ratings_v1.json","w"),separators=(",",":"))
import os
print(f"teams {sum(len(v) for v in teams.values())}  leagues {len(teams)}  size {os.path.getsize('/home/user/pitch_ratings_v1.json'):,}B")
