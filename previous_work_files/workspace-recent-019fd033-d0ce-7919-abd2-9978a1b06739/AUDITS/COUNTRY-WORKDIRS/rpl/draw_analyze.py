#!/usr/bin/env python3
# CALIBRATION-9 dissection, step A: does the displayed draw mass (balD = neuW/totalW)
# track realized draw rate? Where is the miscalibration?
import json
games = json.load(open("/home/user/rpl/draw_replay.json"))
n = len(games)
def rate(vals): return 100*sum(vals)/len(vals) if vals else float("nan")

# 1) Draw calibration curve: bucket by displayed Draw%
print("== Draw-mass calibration curve (displayed Draw% bucket vs realized) ==")
edges = [0,10,15,20,25,30,35,40,100]
for lo,hi in zip(edges, edges[1:]):
    b = [g for g in games if lo <= g["balD"] < hi]
    if not b: continue
    print(f"  Draw% {lo:>3}-{hi:<3} n={len(b):>3}  mean displayed {sum(g['balD'] for g in b)/len(b):5.1f}%  realized draw {rate([g['actual']=='D' for g in b]):5.1f}%")

# 2) Three-way: for each bucket also realized H/A
print("\n== Full 3-way per Draw% bucket ==")
for lo,hi in zip(edges, edges[1:]):
    b = [g for g in games if lo <= g["balD"] < hi]
    if not b: continue
    print(f"  D {lo:>3}-{hi:<3} n={len(b):>3}  realized H {rate([g['actual']=='H' for g in b]):5.1f}  D {rate([g['actual']=='D' for g in b]):5.1f}  A {rate([g['actual']=='A' for g in b]):5.1f}   displayed-mean {sum(g['balH'] for g in b)/len(b):5.1f}/{sum(g['balD'] for g in b)/len(b):5.1f}/{sum(g['balA'] for g in b)/len(b):5.1f}")

# 3) Leader-side calibration: leader share S vs realized leader-win (zone machine uses raw shares)
print("\n== Leader share S_ (pre-gate raw) vs realized leader-win ==")
for lo,hi in [(0,45),(45,50),(50,55),(55,60),(60,65),(65,70),(70,75),(75,80),(80,85),(85,101)]:
    b = [g for g in games if lo <= g["S"] < hi]
    if not b: continue
    lead = [(g["actual"]==("H" if g["side"]=="TA" else "A")) for g in b]
    print(f"  S {lo:>3}-{hi:<3} n={len(b):>3}  mean S {sum(g['S'] for g in b)/len(b):5.1f}%  leader-win {rate(lead):5.1f}%  realized-draw {rate([g['actual']=='D' for g in b]):5.1f}%")

# 4) 2.2-2.5 expected-goals draw band check on this replay snapshot (CALIBRATION-6 finding)
print("\n== EVG2 expected-goals draw band ==")
bb = [g for g in games if g["est"] is not None]
for lo,hi in [(0,2.0),(2.0,2.2),(2.2,2.5),(2.5,2.8),(2.8,9)]:
    b = [g for g in bb if lo <= g["est"] < hi]
    if not b: continue
    print(f"  est {lo:.1f}-{hi:<.1f} n={len(b):>3}  realized draw {rate([g['actual']=='D' for g in b]):5.1f}%   displayed Draw-mean {sum(g['balD'] for g in b)/len(b):5.1f}%")

# 5) Baseline 3-way log-loss of displayed balance vs actual (probability model read)
import math
base = [0.0,0.0,0.0]
for g in games: base["HDA".index(g["actual"])] += 1
base = [x/n for x in base]
def ll(dist, g):
    p = max(dist["HDA".index(g["actual"])], 1e-9)
    return -math.log(p)
ll_disp = sum(ll([g["balH"]/100, g["balD"]/100, g["balA"]/100], g) for g in games)/n
ll_base = sum(-math.log(base["HDA".index(g["actual"])]) for g in games)/n
print(f"\n== Baseline accuracy of displayed 3-way balance ==")
print(f"  displayed-balance log-loss {ll_disp:.4f}")
print(f"  flat base-rate     log-loss {ll_base:.4f}   (base {base[0]*100:.1f}/{base[1]*100:.1f}/{base[2]*100:.1f})")
