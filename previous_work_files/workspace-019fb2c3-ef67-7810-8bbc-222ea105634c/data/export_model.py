"""Export current team ratings to a portable JSON the app can consume. No odds."""
import pickle, math, json
st=pickle.load(open("model_state.pkl","rb"))
rows=pickle.load(open("all_matches.pkl","rb"))
# only keep teams active in the last two seasons
active=set()
for m in rows:
    if m['season'] in ('2425','2526'): active.add((m['lg'],m['home'])); active.add((m['lg'],m['away']))
teams={}
for lg,t in sorted(active):
    if t not in st['att']: continue
    teams.setdefault(lg,{})[t]=dict(att=round(st['att'][t],4),dfn=round(st['dfn'][t],4),
                                     home_extra=round(st['thfa'].get(t,0.0),4))
out=dict(
  version="pitch-rating-v1",
  built="2026-07-29",
  source="match results only (153,058 matches, 18 leagues, 2003-2026). NO bookmaker data.",
  formula="lambda_home=exp(mu[lg]+att[H]-dfn[A]+hfa[lg]+home_extra[H]); lambda_away=exp(mu[lg]+att[A]-dfn[H])",
  dixon_coles_rho=-0.06,
  leagues={lg:dict(mu=round(st['mu'][lg],4),hfa=round(st['hfa'][lg],4)) for lg in st['hfa']},
  teams=teams,
  tiers=[dict(name="A+ Fortress",min=0.70,measured_win=0.785,measured_draw=0.141,n=7718),
         dict(name="A Strong",min=0.60,measured_win=0.642,measured_draw=0.216,n=11799),
         dict(name="B Lean",min=0.52,measured_win=0.547,measured_draw=0.260,n=20335),
         dict(name="C Marginal",min=0.45,measured_win=0.475,measured_draw=0.283,n=28246),
         dict(name="D Coin-flip",min=0.35,measured_win=0.408,measured_draw=0.299,n=44718),
         dict(name="E Avoid",min=0.00,measured_win=0.282,measured_draw=0.268,n=37544)],
  calibration=dict(max_error_pct=1.7,brier=0.6112,brier_baseline=0.6476,improvement_pct=5.6),
)
json.dump(out,open("/home/user/pitch_ratings_v1.json","w"),indent=1)
nteams=sum(len(v) for v in teams.values())
print(f"exported {nteams} teams across {len(teams)} leagues -> /home/user/pitch_ratings_v1.json")
import os; print(f"size {os.path.getsize('/home/user/pitch_ratings_v1.json'):,} bytes")
