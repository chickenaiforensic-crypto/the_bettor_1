#!/usr/bin/env python3
"""Score-level diff: EPL primary ledger (R-rows) vs a second-index FBR matrix (MX-rows).

Key = ordered (homeStock, awayStock) pair (unique per season in a double round-robin).
Compares scores only — matrices carry no dates/rounds. Prints totals and every divergence.

Usage: python3 tools/diff_epl_matrix.py audit/ledger/epl-2025-26.txt audit/ledger/epl-2ndidx-2025-26.txt
"""
import sys
import re

R_RX = re.compile(r"^R(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MX_RX = re.compile(r"^MX\|([^|]+)\|([^|]+)\|(\d+)\|(\d+)$")


def main():
    primary_path, matrix_path = sys.argv[1], sys.argv[2]
    primary = {}
    goals_primary = 0
    with open(primary_path, encoding="utf-8") as fh:
        for line in fh:
            m = R_RX.match(line.strip())
            if not m:
                continue
            h, a = m.group(3).strip(), m.group(6).strip()
            key = (h, a)
            if key in primary:
                print(f"WARN duplicate key {key} in {primary_path}")
            primary[key] = (int(m.group(4)), int(m.group(5)))
            goals_primary += int(m.group(4)) + int(m.group(5))

    matrix = {}
    goals_matrix = 0
    with open(matrix_path, encoding="utf-8") as fh:
        for line in fh:
            m = MX_RX.match(line.strip())
            if not m:
                continue
            key = (m.group(1).strip(), m.group(2).strip())
            if key in matrix:
                print(f"WARN duplicate key {key} in {matrix_path}")
            matrix[key] = (int(m.group(3)), int(m.group(4)))
            goals_matrix += int(m.group(3)) + int(m.group(4))

    missing_in_matrix = sorted(k for k in primary if k not in matrix)
    missing_in_primary = sorted(k for k in matrix if k not in primary)
    divergent = []
    identical = 0
    for key in primary:
        if key not in matrix:
            continue
        if primary[key] == matrix[key]:
            identical += 1
        else:
            divergent.append((key, primary[key], matrix[key]))

    print(f"primary rows: {len(primary)} ({primary_path}) goals={goals_primary}")
    print(f"matrix cells: {len(matrix)} ({matrix_path}) goals={goals_matrix}")
    print(f"identical scores: {identical}/{len(primary)}")
    if missing_in_matrix:
        print(f"MISSING in matrix ({len(missing_in_matrix)}): {missing_in_matrix}")
    if missing_in_primary:
        print(f"MISSING in primary ({len(missing_in_primary)}): {missing_in_primary}")
    for key, ps, ms in divergent:
        print(f"DIVERGENT {key}: primary {ps[0]}-{ps[1]} vs matrix {ms[0]}-{ms[1]}")
    if not divergent and not missing_in_matrix and not missing_in_primary:
        print("RESULT: ALL CELLS IDENTICAL")


if __name__ == "__main__":
    main()
