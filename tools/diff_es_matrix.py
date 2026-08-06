#!/usr/bin/env python3
"""Score-level diff: SPA 2025-26 league carrier (MD rows, openfootball under
source_adaptation) vs the independent second-index FBR matrix (MX rows, Wikipedia
2025-26 La Liga results matrix). Mirrors tools/diff_ita_matrix.py.

Key = ordered (homePin, awayPin) pair (unique per season in a double round-robin).
Compares scores only - matrices carry no dates/rounds.

Usage: python3 tools/diff_es_matrix.py <carrier.md> <matrix.mx>
"""
import sys
import re

R_RX = re.compile(r"^(?:R|MD)(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MX_RX = re.compile(r"^MX\|([^|]+)\|([^|]+)\|(\d+)\|(\d+)$")


def load_carrier(path):
    data, goals = {}, 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = R_RX.match(line.strip())
            if not m:
                continue
            key = (m.group(3).strip(), m.group(6).strip())
            if key in data:
                print(f"WARN duplicate key {key} in {path}")
            data[key] = (int(m.group(4)), int(m.group(5)))
            goals += int(m.group(4)) + int(m.group(5))
    return data, goals


def load_matrix(path):
    data, goals = {}, 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = MX_RX.match(line.strip())
            if not m:
                continue
            key = (m.group(1).strip(), m.group(2).strip())
            if key in data:
                print(f"WARN duplicate key {key} in {path}")
            data[key] = (int(m.group(3)), int(m.group(4)))
            goals += int(m.group(3)) + int(m.group(4))
    return data, goals


def main():
    primary, matrix = sys.argv[1], sys.argv[2]
    p, gp = load_carrier(primary)
    x, gx = load_matrix(matrix)
    missing_in_matrix = sorted(k for k in p if k not in x)
    missing_in_primary = sorted(k for k in x if k not in p)
    divergent = [(k, p[k], x[k]) for k in p if k in x and p[k] != x[k]]
    identical = sum(1 for k in p if k in x and p[k] == x[k])
    print(f"carrier rows: {len(p)} ({primary}) goals={gp}")
    print(f"matrix cells: {len(x)} ({matrix}) goals={gx}")
    print(f"identical scores: {identical}/{len(p)}")
    if missing_in_matrix:
        print(f"MISSING in matrix ({len(missing_in_matrix)}): {missing_in_matrix}")
    if missing_in_primary:
        print(f"MISSING in carrier ({len(missing_in_primary)}): {missing_in_primary}")
    for key, ps, ms in divergent:
        print(f"DIVERGENT {key}: carrier {ps[0]}-{ps[1]} vs matrix {ms[0]}-{ms[1]}")
    if not divergent and not missing_in_matrix and not missing_in_primary:
        print("RESULT: ALL CELLS IDENTICAL")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
