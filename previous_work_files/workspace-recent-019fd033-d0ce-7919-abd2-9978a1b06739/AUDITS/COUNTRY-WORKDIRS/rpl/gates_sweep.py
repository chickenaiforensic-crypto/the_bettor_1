#!/usr/bin/env python3
# CALIBRATION-11 sweep: NO PLAY threshold candidates (demote-only raises).
# kept = actionable zone AND passes banner gates. Objective: kept actW+pair > baseline in BOTH halves.
import json
games = json.load(open("/home/user/rpl/draw_replay.json"))
games.sort(key=lambda g: g["date"])
n = len(games); half = n // 2
A, B = games[:half], games[half:]

def lead(g): return "H" if g["side"] == "TA" else "A"
def won(g): return g["actual"] == lead(g)
def pair(g): return g["actual"] in (lead(g), "D")
def actionable(g): return g["zone"] in ("strong", "win", "windraw")

def kept_stats(gs, eff_min, agree_min, w_min):
    k = [g for g in gs if actionable(g) and g["eff"] >= eff_min and g["agree"] >= agree_min and abs(g["weighted"]) >= w_min]
    if not k: return None
    return len(k), 100 * sum(map(won, k)) / len(k), 100 * sum(map(pair, k)) / len(k)

def fired_dir(gs, eff_min, agree_min, w_min):
    f = [g for g in gs if actionable(g) and not (g["eff"] >= eff_min and g["agree"] >= agree_min and abs(g["weighted"]) >= w_min)]
    if not f: return None
    return len(f), 100 * sum(map(won, f)) / len(f), 100 * sum(map(pair, f)) / len(f)

print("baseline (2 / 0.60 / 0.35):")
for nm, gg in [("A", A), ("B", B), ("ALL", games)]:
    k = kept_stats(gg, 2, 0.60, 0.35); f = fired_dir(gg, 2, 0.60, 0.35)
    print(f"  {nm:3} kept n={k[0]:>3} actW {k[1]:5.1f} pair {k[2]:5.1f}  |  fired n={f[0]:>3} actW {f[1]:5.1f} pair {f[2]:5.1f}")

print("\n== agree threshold sweep (eff=2, w=0.35 fixed) ==")
for ag in [0.55, 0.60, 0.65, 0.70, 0.75]:
    row = f"  agree>={ag:.2f}: "
    for nm, gg in [("A", A), ("B", B)]:
        k = kept_stats(gg, 2, ag, 0.35); f = fired_dir(gg, 2, ag, 0.35)
        row += f" {nm} kept {k[0]:>3} {k[1]:5.1f}/{k[2]:5.1f} fired {f[0]:>3} {f[1]:5.1f}/{f[2]:5.1f} |"
    print(row)

print("\n== |weighted| threshold sweep (eff=2, agree=0.60 fixed) ==")
for wm in [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]:
    row = f"  |w|>={wm:.2f}: "
    for nm, gg in [("A", A), ("B", B)]:
        k = kept_stats(gg, 2, 0.60, wm); f = fired_dir(gg, 2, 0.60, wm)
        row += f" {nm} kept {k[0]:>3} {k[1]:5.1f}/{k[2]:5.1f} fired {f[0]:>3} {f[1]:5.1f}/{f[2]:5.1f} |"
    print(row)

print("\n== eff threshold sweep (agree=0.60, w=0.35 fixed) ==")
for em in [2, 3, 4]:
    row = f"  eff>={em}: "
    for nm, gg in [("A", A), ("B", B)]:
        k = kept_stats(gg, em, 0.60, 0.35); f = fired_dir(gg, em, 0.60, 0.35)
        row += f" {nm} kept {k[0]:>3} {k[1]:5.1f}/{k[2]:5.1f} fired {f[0]:>3} {f[1]:5.1f}/{f[2]:5.1f} |"
    print(row)

print("\n== joint champion probe: agree 0.65 x w combos ==")
for ag in [0.65, 0.70]:
    for wm in [0.35, 0.5, 0.7]:
        row = f"  a={ag:.2f} w={wm:.2f}: "
        for nm, gg in [("A", A), ("B", B)]:
            k = kept_stats(gg, 2, ag, wm)
            row += f" {nm} kept {k[0]:>3} {k[1]:5.1f}/{k[2]:5.1f} |"
        print(row)
