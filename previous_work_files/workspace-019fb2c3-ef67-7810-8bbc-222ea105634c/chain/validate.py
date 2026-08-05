"""
CHAIN SYSTEM — FOUNDATION STEP 3
Validate against outcomes only. No odds anywhere.

Method: take real cross-border European ties, build chains from data BEFORE
the tie, compare the chain estimate to what actually happened.
"""
import pickle, re, glob, os, math
from collections import defaultdict
import chain as C

line_re = re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)')
ties = []
for f in sorted(glob.glob("/tmp/ucl/champions-league-master/*/*.txt")):
    season = f.split('/')[-2]
    yr = int(season[:4])
    if yr < 2021:
        continue
    for ln in open(f, encoding='utf-8', errors='replace'):
        m = line_re.match(ln.strip('\r\n'))
        if m and m.group(2) != m.group(4):          # cross-border only
            ties.append((yr, m.group(1).strip(), m.group(3).strip(),
                         int(m.group(5)), int(m.group(6))))
print(f"cross-border European matches 2021+: {len(ties):,}")

rows = []
for yr, h, a, hg, ag in ties:
    since = f"{yr-4}-01-01"
    cutoff = f"{yr}-06-29"                          # strictly before the tie
    r = C.find_chains(h, a, since=since)
    if "error" in r:
        continue
    for key, ph in (("phase2", 2), ("phase3", 3)):
        cs = [c for c in r[key] if c["y1"] <= str(yr - 1)]   # prior links only
        if len(cs) < 3:
            continue
        v = [c["est"] for c in cs]
        mean = sum(v) / len(v)
        sd = (sum((x - mean) ** 2 for x in v) / len(v)) ** 0.5
        rows.append((ph, mean, sd, max(v) - min(v), len(cs), hg - ag, hg, ag))

print(f"scoreable chain estimates: {len(rows):,}")


def corr(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    a = sum((p - mx) * (q - my) for p, q in zip(x, y))
    b = math.sqrt(sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y))
    return a / b if b else 0


print("\n" + "=" * 84)
print("DOES THE CHAIN ESTIMATE TRACK THE ACTUAL RESULT?")
print("=" * 84)
for ph in (2, 3):
    s = [r for r in rows if r[0] == ph]
    if len(s) < 20:
        print(f"  phase {ph}: only {len(s)} cases")
        continue
    est = [r[1] for r in s]
    act = [r[5] for r in s]
    hit = sum(1 for r in s if (r[1] > 0) == (r[5] > 0) and r[5] != 0)
    dec = sum(1 for r in s if r[5] != 0)
    print(f"  phase {ph}: n={len(s):4d}  r={corr(est, act):+.4f}  "
          f"direction correct {hit}/{dec} = {hit/dec:.1%}" if dec else "")

print("\n" + "=" * 84)
print("DOES LOW SPREAD MEAN A BETTER ESTIMATE?  (the usability rule)")
print("=" * 84)
print(f"  {'spread band':16s} {'n':>6s} {'r with actual':>14s} {'direction %':>13s}")
for lo, hi in [(0, 1.5), (1.5, 3), (3, 5), (5, 99)]:
    s = [r for r in rows if lo <= r[3] < hi]
    if len(s) < 20:
        continue
    est = [r[1] for r in s]
    act = [r[5] for r in s]
    dec = sum(1 for r in s if r[5] != 0)
    hit = sum(1 for r in s if (r[1] > 0) == (r[5] > 0) and r[5] != 0)
    print(f"  {f'{lo}-{hi}':16s} {len(s):6d} {corr(est, act):+14.4f} "
          f"{hit/dec:12.1%}" if dec else "")

print("\n" + "=" * 84)
print("BASELINE — how good is 'always predict a level game'?")
print("=" * 84)
act = [r[5] for r in rows]
print(f"  actual GD mean {sum(act)/len(act):+.2f}, "
      f"home wins {sum(1 for a in act if a>0)/len(act):.1%}, "
      f"draws {sum(1 for a in act if a==0)/len(act):.1%}")
pickle.dump(rows, open("/home/user/chain/val_rows.pkl", "wb"))
