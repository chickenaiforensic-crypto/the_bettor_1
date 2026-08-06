#!/usr/bin/env python3
"""Row-level diff: EPL primary ledger (RSSSF R-rows) vs second index (openfootball MD rows).

Key = ordered (homeStock, awayStock) pair (unique per season: single round-robin twice,
once home once away, so each ordered pair appears exactly once). Compares round banner,
played date and score. Prints per-season totals and every divergence.

Usage: python3 tools/diff_epl_second_index.py audit/ledger/epl-2021-22.txt audit/ledger/epl-2ndidx-2021-22.txt
"""
import sys
import re

def load(path, tag):
    rows = {}
    order = []
    rx = re.compile(r"^(?:R|MD)(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = rx.match(line.strip())
            if not m:
                continue
            rnd, date, h, hg, ag, a = int(m.group(1)), m.group(2), m.group(3).strip(), int(m.group(4)), int(m.group(5)), m.group(6).strip()
            key = (h, a)
            if key in rows:
                print(f"WARN duplicate key {key} in {path}")
            rows[key] = (rnd, date, hg, ag)
            order.append(key)
    return rows, order

def main():
    p1, p2 = sys.argv[1], sys.argv[2]
    r1, o1 = load(p1, "R")
    r2, o2 = load(p2, "MD")
    missing1 = [k for k in r2 if k not in r1]
    missing2 = [k for k in r1 if k not in r2]
    diffs = []
    same = 0
    for k in r1:
        if k not in r2:
            continue
        a, b = r1[k], r2[k]
        marks = []
        if a[0] != b[0]:
            marks.append(f"round R{a[0]} vs MD{b[0]}")
        if a[1] != b[1]:
            marks.append(f"date {a[1]} vs {b[1]}")
        if a[2] != b[2] or a[3] != b[3]:
            marks.append(f"score {a[2]}-{a[3]} vs {b[2]}-{b[3]}")
        if marks:
            diffs.append((k, a, b, "; ".join(marks)))
        else:
            same += 1
    print(f"{p1.split('/')[-1]} vs {p2.split('/')[-1]}: pairings primary={len(r1)} second={len(r2)}")
    print(f"  identical (round+date+score): {same}")
    print(f"  pairings only in primary: {len(missing2)} {missing2[:5]}")
    print(f"  pairings only in second : {len(missing1)} {missing1[:5]}")
    for k, a, b, why in diffs:
        print(f"  DIFF {k[0]} vs {k[1]}: primary R{a[0]} {a[1]} {a[2]}-{a[3]} | second MD{b[0]} {b[1]} {b[2]}-{b[3]} || {why}")
    print(f"  divergences total: {len(diffs)}")

if __name__ == "__main__":
    main()
