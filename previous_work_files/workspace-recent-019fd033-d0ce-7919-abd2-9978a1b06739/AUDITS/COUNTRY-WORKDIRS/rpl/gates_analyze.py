#!/usr/bin/env python3
# CALIBRATION-11 (section #7): dissect effective-paths discount + NO PLAY thresholds.
# Input: rpl/draw_replay.json (v2.8.7/8-engine replay: zone, side, eff, agree, weighted, actual).
import json
games = json.load(open("/home/user/rpl/draw_replay.json"))
games.sort(key=lambda g: g["date"])
n = len(games); half = n // 2

def lead(g): return "H" if g["side"] == "TA" else "A"
def won(g): return g["actual"] == lead(g)
def pair(g): return g["actual"] in (lead(g), "D")
def actionable(g): return g["zone"] in ("strong", "win", "windraw")
def stat(gs):
    if not gs: return "-"
    return f"n={len(gs):>3}  W {100*sum(map(won,gs))/len(gs):5.1f}  pair {100*sum(map(pair,gs))/len(gs):5.1f}  action-W { (100*sum(map(won,[g for g in gs if actionable(g)]))/max(1,len([g for g in gs if actionable(g)]))) if any(map(actionable,gs)) else float('nan'):5.1f}"

print("== 1) effective independent paths (discount) vs accuracy ==")
for k in [1, 2, 3, 4, 5, 6]:
    lo, hi = (k, k+1) if k < 6 else (6, 99)
    gs = [g for g in games if lo <= g["eff"] < hi]
    lbl = str(k) if k < 6 else "6+"
    print(f"  eff={lbl:<3} {stat(gs)}")
print()
print("== 2) agree (alignment) buckets vs accuracy ==")
for lo, hi in [(0, .5), (.5, .6), (.6, .7), (.7, .8), (.8, .9), (.9, 1.01)]:
    gs = [g for g in games if lo <= g["agree"] < hi]
    print(f"  {lo:.1f}-{hi if hi<1.01 else 1.0:<4} {stat(gs)}")
print()
print("== 3) |weighted estimate| buckets vs accuracy ==")
for lo, hi in [(0, .2), (.2, .35), (.35, .6), (.6, 1.0), (1.0, 1.5), (1.5, 9)]:
    gs = [g for g in games if lo <= abs(g["weighted"]) < hi]
    print(f"  {lo:.2f}-{hi:<5} {stat(gs)}")
print()
print("== 4) gate-fired cohorts (current classify thresholds) ==")
for name, fn in [
    ("eff<2", lambda g: g["eff"] < 2),
    ("agree<0.60", lambda g: g["agree"] < 0.60),
    ("|weighted|<0.35", lambda g: abs(g["weighted"]) < 0.35),
    ("ANY gate", lambda g: g["eff"] < 2 or g["agree"] < 0.60 or abs(g["weighted"]) < 0.35),
    ("passes all", lambda g: g["eff"] >= 2 and g["agree"] >= 0.60 and abs(g["weighted"]) >= 0.35),
]:
    gs = [g for g in games if fn(g)]
    print(f"  {name:<18} {stat(gs)}")
print()
print("== 5) interplay: gates vs zones (does a fired gate mark bad zones?) ==")
for z in ["strong", "win", "windraw", "lean", "toss"]:
    gs = [g for g in games if g["zone"] == z]
    fired = [g for g in gs if g["eff"] < 2 or g["agree"] < 0.60 or abs(g["weighted"]) < 0.35]
    kept = [g for g in gs if g not in fired]
    fz = f"fired {stat(fired)}" if fired else "fired n=0"
    print(f"  {z:<8} kept {stat(kept)}   |   {fz}")
print()
print("== 6) consecutive splits (both halves agree in every bucket above?) ==")
for label, keyfn, edges in [
    ("eff", lambda g: g["eff"], [(1,2),(2,3),(3,4),(4,99)]),
    ("agree", lambda g: g["agree"], [(0,.6),(.6,.75),(.75,1.01)]),
    ("|weighted|", lambda g: abs(g["weighted"]), [(0,.35),(.35,.7),(.7,9)]),
]:
    print(f"  {label}:")
    for lo, hi in edges:
        for hname, gg in [("A", games[:half]), ("B", games[half:])]:
            gs = [g for g in gg if lo <= keyfn(g) < hi]
            a = [g for g in gs if actionable(g)]
            wr = f"W {100*sum(map(won,gs))/len(gs):5.1f}" if gs else "n=0"
            aw = f"actW {100*sum(map(won,a))/len(a):5.1f}" if a else "act n=0"
            print(f"    {lo}-{hi} half{hname}: n={len(gs):>3} {wr} pair {100*sum(map(pair,gs))/max(1,len(gs)):5.1f} {aw}")
