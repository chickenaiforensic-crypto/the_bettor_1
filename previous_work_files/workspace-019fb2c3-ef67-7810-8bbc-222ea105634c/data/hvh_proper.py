"""
WHAT I ACTUALLY DID (and why it was not your idea):
  I took GD(home-v-home), rounded to integers -3..3, computed a residual
  correction per bucket, and ADDED it to the model's P(home).
  That tests "does a crude additive nudge help?" - it does NOT test your idea.

YOUR IDEA:
  Compare the home team's HOME stats vs the away team's HOME stats.
  That asks: "if both sides were at their best, who is better?"
  Then find a THRESHOLD - a margin above which home wins confidently,
  and a band within which it is draw/loss.
Test that properly.
"""
import sys, pickle, math
sys.path.insert(0,'/home/user/data')
from harness import *
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
rows.sort(key=lambda r:(r['date'],r['lg'],r['home']))
MIN=4

H_rec=defaultdict(lambda:{'p':0,'pts':0,'gf':0,'ga':0,'w':0,'d':0})
A_rec=defaultdict(lambda:{'p':0,'pts':0,'gf':0,'ga':0,'w':0,'d':0})
data=[]
for m in rows:
    lg,se,h,a=m['lg'],m['season'],m['home'],m['away']
    hh=H_rec[(lg,se,h)]      # home team AT HOME
    ah=H_rec[(lg,se,a)]      # away team AT HOME  <- the key stat
    aa=A_rec[(lg,se,a)]      # away team AWAY
    ha=A_rec[(lg,se,h)]      # home team AWAY
    if hh['p']>=MIN and ah['p']>=MIN and aa['p']>=MIN:
        f=lambda d:dict(ppg=d['pts']/d['p'], gd=(d['gf']-d['ga'])/d['p'],
                        gf=d['gf']/d['p'], ga=d['ga']/d['p'], wr=d['w']/d['p'], n=d['p'])
        data.append((m,f(hh),f(ah),f(aa),f(ha) if ha['p']>=MIN else None))
    hp=3 if m['res']=='H' else (1 if m['res']=='D' else 0)
    ap=3 if m['res']=='A' else (1 if m['res']=='D' else 0)
    d=H_rec[(lg,se,h)]; d['p']+=1; d['pts']+=hp; d['gf']+=m['hg']; d['ga']+=m['ag']
    d['w']+= (m['res']=='H'); d['d']+= (m['res']=='D')
    d=A_rec[(lg,se,a)]; d['p']+=1; d['pts']+=ap; d['gf']+=m['ag']; d['ga']+=m['hg']
    d['w']+= (m['res']=='A'); d['d']+= (m['res']=='D')
print(f"fixtures with >= {MIN} home games for BOTH teams: {len(data):,}")

print("\n"+"="*100)
print("WHAT DOES HOME-vs-HOME ACTUALLY MEASURE? outcome by the raw differential")
print("="*100)
print("  diff = home team's home GD/game  MINUS  away team's home GD/game")
print(f"  {'band':16s} {'n':>8s} {'home W':>8s} {'draw':>8s} {'away W':>8s} {'mean GD':>9s} {'home PPG':>9s}")
bands=[(-9,-1.5),(-1.5,-1.0),(-1.0,-0.5),(-0.5,0),(0,0.5),(0.5,1.0),(1.0,1.5),(1.5,2.0),(2.0,9)]
for lo,hi in bands:
    v=[m for m,hh,ah,aa,ha in data if lo<=hh['gd']-ah['gd']<hi]
    if len(v)<200: continue
    n=len(v); w=sum(1 for m in v if m['res']=='H'); d=sum(1 for m in v if m['res']=='D')
    print(f"  [{lo:5.1f},{hi:5.1f})    {n:8,} {w/n:8.1%} {d/n:8.1%} {(n-w-d)/n:8.1%} "
          f"{sum(m['hg']-m['ag'] for m in v)/n:+9.2f} {(3*w+d)/n:9.2f}")

print("\n"+"="*100)
print("YOUR THRESHOLD QUESTION — where is a CONFIDENT home win?")
print("="*100)
print(f"  {'threshold':>12s} {'n above':>9s} {'home W%':>9s} {'draw%':>8s} {'lose%':>8s} {'coverage':>9s}")
for th in [0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.5]:
    v=[m for m,hh,ah,aa,ha in data if hh['gd']-ah['gd']>=th]
    if len(v)<150: continue
    n=len(v); w=sum(1 for m in v if m['res']=='H'); d=sum(1 for m in v if m['res']=='D')
    print(f"  >= {th:8.2f} {n:9,} {w/n:9.1%} {d/n:8.1%} {(n-w-d)/n:8.1%} {n/len(data):9.1%}")

print("\n  DRAW / LOSS BAND — within what margin is it not safe?")
print(f"  {'band':16s} {'n':>8s} {'home W%':>9s} {'draw%':>8s} {'not-win%':>9s}")
for lo,hi in [(-0.25,0.25),(-0.5,0.5),(-0.75,0.75),(-1.0,1.0)]:
    v=[m for m,hh,ah,aa,ha in data if lo<=hh['gd']-ah['gd']<=hi]
    n=len(v); w=sum(1 for m in v if m['res']=='H'); d=sum(1 for m in v if m['res']=='D')
    print(f"  [{lo:5.2f},{hi:5.2f}]    {n:8,} {w/n:9.1%} {d/n:8.1%} {1-w/n:9.1%}")
pickle.dump(data,open("hvh_data.pkl","wb"))
