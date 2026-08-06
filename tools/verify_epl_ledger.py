#!/usr/bin/env python3
"""Self-check for WO-EPL-SPAN-12 primary ledgers (audit/ledger/epl-<season>.txt).

Recomputes played/W/D/L/GF/GA/Pts from the R-rows and compares every club
against the TABLE constants transcribed from the RSSSF page (position order
inclusive). Also asserts 38 rounds x 10 rows and prints goals total + span.

Usage: python3 tools/verify_epl_ledger.py audit/ledger/epl-2024-25.txt [deduct:Stock=8,Stock=4]
Exit 0 only when every check passes.
"""
import sys
import re
from collections import defaultdict

def main():
    path = sys.argv[1]
    deduct = {}
    if len(sys.argv) > 2:
        for part in sys.argv[2].split(","):
            k, v = part.split("=")
            deduct[k.strip()] = int(v)
    rows, table = [], []
    season = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("R"):
                m = re.match(r"^R(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$", line)
                if m:
                    rows.append((int(m.group(1)), m.group(2), m.group(3).strip(),
                                 int(m.group(4)), int(m.group(5)), m.group(6).strip()))
            elif line.startswith("TABLE|"):
                p = line.split("|")
                season = p[1]
                table.append((int(p[2]), p[3], int(p[4]), int(p[5]), int(p[6]),
                              int(p[7]), int(p[8]), int(p[9]), int(p[10]), p[11] if len(p) > 11 else ""))
    fails = []
    # rounds x 10
    rnd = defaultdict(int)
    for r in rows:
        rnd[r[0]] += 1
    for n in range(1, 39):
        if rnd.get(n, 0) != 10:
            fails.append(f"round R{n} has {rnd.get(n, 0)} rows (want 10)")
    if len(rows) != 380:
        fails.append(f"row count {len(rows)} (want 380)")
    # recompute
    st = defaultdict(lambda: [0, 0, 0, 0, 0, 0])  # P W D L GF GA
    dates = []
    goals = 0
    for _, d, h, hg, ag, a in rows:
        dates.append(d)
        goals += hg + ag
        st[h][0] += 1; st[a][0] += 1
        st[h][4] += hg; st[h][5] += ag
        st[a][4] += ag; st[a][5] += hg
        if hg > ag:
            st[h][1] += 1; st[a][3] += 1
        elif hg < ag:
            st[a][1] += 1; st[h][3] += 1
        else:
            st[h][2] += 1; st[a][2] += 1
    # compare club-for-club + position order
    if len(table) != 20:
        fails.append(f"TABLE constants {len(table)} rows (want 20)")
    recomputed_order = []
    for pos, club, P, W, D, L, GF, GA, Pts, note in table:
        c = st.get(club)
        if c is None:
            fails.append(f"pos {pos} {club}: no match rows"); continue
        pts = c[1] * 3 + c[2] - deduct.get(club, 0)
        got = [c[0], c[1], c[2], c[3], c[4], c[5], pts]
        want = [P, W, D, L, GF, GA, Pts]
        if got != want:
            fails.append(f"pos {pos} {club}: recompute P/W/D/L/GF/GA/Pts {got} != table {want}")
        recomputed_order.append((club, pts, GF - GA, GF, pos))
    extra = set(st) - {t[1] for t in table}
    if extra:
        fails.append(f"clubs in rows but not in TABLE: {sorted(extra)}")
    # verify ordering rule: position order must equal sort by pts, GD, GF
    sorted_order = sorted(recomputed_order, key=lambda x: (-x[1], -x[2], -x[3]))
    if [x[4] for x in sorted_order] != [x[4] for x in recomputed_order]:
        # EPL tie-break = GD then GF then head-to-head (latter rare); report ordering anomalies
        fails.append("position order does not follow pts/GD/GF sort (check H2H case) -> " +
                     ", ".join(f"{c}@{p}" for c, _, _, _, p in sorted_order))
    print(f"{path.split('/')[-1]} season={season} rows={len(rows)} goals={goals} "
          f"span={min(dates)}..{max(dates)} deductions={deduct or 'none'}")
    if fails:
        for f in fails:
            print("  FAIL:", f)
        sys.exit(1)
    print("  OK: 38x10 rounds, table 20/20 club-for-club + position order EXACT")

if __name__ == "__main__":
    main()
