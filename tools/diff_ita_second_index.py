#!/usr/bin/env python3
"""diff_ita_second_index.py - cross-check an ITA ledger season against its second index.

Usage: python3 tools/diff_ger_second_index.py <season-ledger> <2ndidx-file>
Gate: as multisets over (home, away) fixtures, carrier R rows and index MD rows must
cover each other exactly with identical scores. Direction matters (home/away as printed).
Prints matched totals and any divergence lines; exit code 1 on any mismatch.
"""
import sys
import collections


def load_ledger(path):
    rows = collections.Counter()
    dates = {}
    rnd_of = {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("R") and line[1].isdigit():
            p = line.strip().split("|")
            rnd, date, h, hg, ag, a = p[0], p[1], p[2], int(p[3]), int(p[4]), p[5]
            rows[(h, a, hg, ag)] += 1
            dates[(h, a)] = date
            rnd_of[(h, a)] = rnd
    return rows, dates, rnd_of


def load_md(path, pfx):
    rows = collections.Counter()
    dates = {}
    rnd_of = {}
    for line in open(path, encoding="utf-8"):
        if line.startswith(pfx):
            p = line.strip().split("|")
            rnd, date, h, hg, ag, a = p[0], p[1], p[2], int(p[3]), int(p[4]), p[5]
            rows[(h, a, hg, ag)] += 1
            dates[(h, a)] = date
            rnd_of[(h, a)] = rnd
    return rows, dates, rnd_of


def main(carrier, index, pfx="MD"):
    C, Cd, Cr = load_ledger(carrier)
    I, Id, Ir = load_md(index, pfx)
    ok = True
    both = C & I
    n_both = sum(both.values())
    only_c = C - I
    only_i = I - C
    print(f"# matched (direction+score): {n_both}  carrier-only: {sum(only_c.values())}  index-only: {sum(only_i.values())}")
    for (h, a, hg, ag), c in sorted(only_c.items()):
        print(f"DIVERGENT carrier-only {Cr.get((h,a),'')} {Cd.get((h,a),'')} {h} {hg}-{ag} {a}")
        ok = False
    for (h, a, hg, ag), c in sorted(only_i.items()):
        print(f"DIVERGENT index-only   {Ir.get((h,a),'')} {Id.get((h,a),'')} {h} {hg}-{ag} {a}")
        ok = False
    if ok:
        print("# GATE PASS: carrier == index as fixture multiset (ITA)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "MD")
