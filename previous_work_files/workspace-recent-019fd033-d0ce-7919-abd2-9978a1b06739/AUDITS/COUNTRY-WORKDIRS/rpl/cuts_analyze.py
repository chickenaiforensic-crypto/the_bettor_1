#!/usr/bin/env python3
# CALIBRATION-12 (section #8): zone cut-point dissection. S_ is raw leader share (engine).
# Gates interact with cuts (C5 fires at zone=='win' etc.) -> full-engine sweep comes after;
# here: realized accuracy along S_ to locate real gradient breaks, per half.
import json
games = json.load(open("/home/user/rpl/draw_replay.json"))
games.sort(key=lambda g: g["date"])
n = len(games); half = n // 2; A, B = games[:half], games[half:]

def lead(g): return "H" if g["side"] == "TA" else "A"
def won(g): return g["actual"] == lead(g)
def pair(g): return g["actual"] in (lead(g), "D")

print("== realized W/pair by 5-pt S_ bins (ALL / A / B) ==")
print(f"{'S bin':<10}{'ALL n':>6}{'W':>7}{'pair':>7} | {'A n':>5}{'W':>7}{'pair':>7} | {'B n':>5}{'W':>7}{'pair':>7}")
import math
lo_edges = sorted(set(int(g["S"] // 5 * 5) for g in games))
for lo in range(35, 100, 5):
    hi = lo + 5
    row = f"  {lo}-{hi:<5}"
    for gg in [games, A, B]:
        gs = [g for g in gg if lo <= g["S"] < hi]
        if gs:
            row += f"{len(gs):>7}{100*sum(map(won,gs))/len(gs):>7.1f}{100*sum(map(pair,gs))/len(gs):>7.1f} | "
        else:
            row += f"{'—':>19} | "
    print(row)

print("\n== cumulative from-top (S >= c): the 'this rung and above' profile ==")
for c in range(50, 100, 5):
    gs = [g for g in games if g["S"] >= c]
    ga = [g for g in A if g["S"] >= c]; gb = [g for g in B if g["S"] >= c]
    print(f"  S>={c}: ALL n={len(gs):>3} W {100*sum(map(won,gs))/len(gs):5.1f} pair {100*sum(map(pair,gs))/len(gs):5.1f}"
          f"  | A {100*sum(map(won,ga))/max(1,len(ga)):5.1f}/{100*sum(map(pair,ga))/max(1,len(ga)):5.1f} (n={len(ga)})"
          f"  | B {100*sum(map(won,gb))/max(1,len(gb)):5.1f}/{100*sum(map(pair,gb))/max(1,len(gb)):5.1f} (n={len(gb)})")
