"""Calibration + the home-match tier system. No odds anywhere."""
import pickle, math
from collections import defaultdict
preds=pickle.load(open("preds.pkl","rb"))
def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h

print("="*88)
print("CALIBRATION — does 'model says 70%' actually win 70%?")
print("="*88)
print(f"  {'predicted home win':20s} {'n':>9s} {'predicted':>10s} {'actual':>10s} {'error':>8s}  {'95% CI':>16s}")
bands=[(0,.15),(.15,.25),(.25,.35),(.35,.45),(.45,.55),(.55,.65),(.65,.75),(.75,.85),(.85,1.01)]
mx=0
for lo,hi in bands:
    s=[p for p in preds if lo<=p[1]<hi]
    if len(s)<200: continue
    n=len(s); pr=sum(p[1] for p in s)/n; ac=sum(1 for p in s if p[0]['res']=='H')/n
    l,h_=wilson(sum(1 for p in s if p[0]['res']=='H'),n)
    mx=max(mx,abs(pr-ac))
    print(f"  [{lo:.2f},{hi:.2f})          {n:9,} {pr:10.1%} {ac:10.1%} {ac-pr:+8.1%}  [{l:.1%},{h_:.1%}]")
print(f"  MAX calibration error across all bands: {mx:.1%}")

print("\n  DRAW calibration (the thing the old app could never do):")
print(f"  {'predicted draw':20s} {'n':>9s} {'predicted':>10s} {'actual':>10s} {'error':>8s}")
for lo,hi in [(.15,.22),(.22,.25),(.25,.275),(.275,.30),(.30,.40)]:
    s=[p for p in preds if lo<=p[2]<hi]
    if len(s)<300: continue
    n=len(s); pr=sum(p[2] for p in s)/n; ac=sum(1 for p in s if p[0]['res']=='D')/n
    print(f"  [{lo:.3f},{hi:.3f})        {n:9,} {pr:10.1%} {ac:10.1%} {ac-pr:+8.1%}")

print("\n"+"="*88)
print("HOME-MATCH TIER SYSTEM — points-based, derived from calibrated probability")
print("="*88)
print("  Tier assigned purely from model P(home win). Each tier's REAL rate measured.")
tiers=[("A+  Fortress",0.70,1.01),("A   Strong",0.60,0.70),("B   Lean",0.52,0.60),
       ("C   Marginal",0.45,0.52),("D   Coin-flip",0.35,0.45),("E   Avoid",0.0,0.35)]
print(f"  {'tier':16s} {'n':>9s} {'model P':>9s} {'actual':>9s} {'draw':>8s} {'loss':>8s} {'PPG':>6s}")
for name,lo,hi in tiers:
    s=[p for p in preds if lo<=p[1]<hi]
    if not s: continue
    n=len(s); pr=sum(p[1] for p in s)/n
    w=sum(1 for p in s if p[0]['res']=='H'); d=sum(1 for p in s if p[0]['res']=='D')
    print(f"  {name:16s} {n:9,} {pr:9.1%} {w/n:9.1%} {d/n:8.1%} {(n-w-d)/n:8.1%} {(3*w+d)/n:6.2f}")

print("\n"+"="*88)
print("100-POINT HOME RATING SCALE (what you asked for)")
print("="*88)
print("  score = 100 * P(home win) ; validated in 10-point buckets")
print(f"  {'points':12s} {'n':>9s} {'actual home win':>16s} {'reliability':>12s}")
for lo in range(20,90,10):
    s=[p for p in preds if lo/100<=p[1]<(lo+10)/100]
    if len(s)<200: continue
    n=len(s); ac=sum(1 for p in s if p[0]['res']=='H')/n
    mid=(lo+5)/100
    print(f"  {lo}-{lo+9:<8} {n:9,} {ac:16.1%} {'OK' if abs(ac-mid)<0.04 else 'off':>12s}")

print("\n"+"="*88)
print("PER-LEAGUE HOME ADVANTAGE (measured, not assumed)")
print("="*88)
st=pickle.load(open("model_state.pkl","rb"))
names={'E0':'England PL','E1':'England Champ','E2':'England L1','E3':'England L2','SC0':'Scotland Prem',
 'D1':'Germany Bund','D2':'Germany 2.Bund','SP1':'Spain LaLiga','SP2':'Spain Segunda','I1':'Italy Serie A',
 'I2':'Italy Serie B','F1':'France L1','F2':'France L2','N1':'Netherlands','B1':'Belgium','P1':'Portugal',
 'T1':'Turkey','G1':'Greece'}
hf=sorted(st['hfa'].items(),key=lambda x:-x[1])
for lg,v in hf:
    print(f"  {names.get(lg,lg):18s} log-HFA {v:.3f}  (goal multiplier {math.exp(v):.2f}x)")

print("\n"+"="*88)
print("STRONGEST PER-TEAM HOME EFFECTS (extra beyond league average)")
print("="*88)
tt=sorted(st['thfa'].items(),key=lambda x:-x[1])
print("  Biggest home-field boost:")
for t,v in tt[:8]: print(f"    {t:22s} {v:+.3f}")
print("  Weakest / negative:")
for t,v in tt[-5:]: print(f"    {t:22s} {v:+.3f}")
