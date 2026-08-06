#!/usr/bin/env python3
"""
the_bettor_1 - RPL 2024-25 / 2025-26 second-index tool (owner override DECREE-2026-08-04).

The football-data R1.csv second index used for 2021-24 is discontinued (mmz4281/2425
and /2526 both 404 as of 2026-08-04; openfootball has no russia repo (404)), so the
independent score-level index for the two new seasons is the Wikipedia season-article
"Results" FBR matrix, transcribed 2026-08-04 (MediaWiki API, section 14).

This script:
  1. regenerates audit/ledger/rpl-2ndidx-<season>.txt deterministically from the
     matrix transcription embedded below (single source of the transcription);
  2. diffs matrix vs the primary RSSSF ledger score-for-score (expect 240/240);
  3. recomputes the full league table from the matrix and compares club-for-club
     against the official constants in audit/ledger/rpl-venues.txt TABLE lines;
  4. cross-checks the season goals total (648 / 609, RSSSF + wiki infobox anchors).

Exit 0 iff everything is exact.
"""
import os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")

# Column order = the verbatim wiki matrix header codes (home row's own column omitted).
COLS = {
 "2024-25": ["AKH","AKR","CSK","DMH","DMO","FAK","KHI","KRA","KRY","LOK","ORE","PNN","ROS","RUB","SPA","ZEN"],
 "2025-26": ["AKH","AKR","BAL","CSK","DMH","DMO","KRA","KRY","LOK","ORE","PNN","ROS","RUB","SOC","SPA","ZEN"],
}
CODE2STOCK = {
 "2024-25": {"AKH":"Ahmat","AKR":"Akron","CSK":"CSKA","DMH":"Dinamo Mh","DMO":"Dinamo Ms","FAK":"Fakel",
             "KHI":"Himki","KRA":"Krasnodar","KRY":"KS Samara","LOK":"Lokomotiv","ORE":"Orenburg",
             "PNN":"Pari NN","ROS":"Rostov","RUB":"Rubin","SPA":"Spartak","ZEN":"Zenit"},
 "2025-26": {"AKH":"Ahmat","AKR":"Akron","BAL":"Baltika","CSK":"CSKA","DMH":"Dinamo Mh","DMO":"Dinamo Ms",
             "KRA":"Krasnodar","KRY":"Krylja S.","LOK":"Lokomotiv","ORE":"Orenburg","PNN":"Pari NN",
             "ROS":"Rostov","RUB":"Rubin","SOC":"Soci","SPA":"Spartak","ZEN":"Zenit"},
}
# FBR matrix home rows: 15 cells each, in full column order minus the home club's own column.
ROWS = {
"2024-25": [
 ("AKH","0-0 1-1 1-1 1-1 2-3 3-3 1-1 1-1 0-5 1-0 0-2 2-1 2-1 0-0 1-2"),
 ("AKR","3-2 1-2 1-0 0-2 1-0 3-0 2-5 2-0 1-4 1-0 2-2 2-3 1-2 2-3 0-5"),
 ("CSK","3-0 4-0 2-0 3-1 0-0 1-0 1-0 1-1 0-1 5-1 2-0 1-2 2-2 0-2 0-1"),
 ("DMH","1-0 1-1 0-1 0-1 0-0 4-1 2-3 4-0 1-1 2-1 0-1 1-1 2-3 1-1 0-1"),
 ("DMO","4-2 2-1 1-2 4-0 3-1 4-1 0-1 1-0 3-1 5-1 3-1 1-1 3-1 2-0 1-1"),
 ("FAK","0-0 0-2 0-1 1-1 1-1 1-1 0-0 1-1 0-1 1-0 0-0 0-2 0-0 0-0 0-2"),
 ("KHI","1-1 2-2 0-2 1-1 3-4 1-0 2-2 1-3 2-0 0-0 2-0 1-1 3-2 1-3 1-1"),
 ("KRA","3-1 1-0 2-1 0-0 3-0 5-0 4-0 1-1 0-0 4-0 2-1 2-0 2-1 0-3 2-0"),
 ("KRY","2-1 0-2 1-2 0-1 1-3 2-0 0-0 1-2 5-1 2-0 3-1 1-3 1-1 0-2 0-4"),
 ("LOK","1-1 3-2 2-2 2-0 2-1 2-1 1-3 0-3 1-0 1-1 3-0 3-2 1-0 3-1 1-1"),
 ("ORE","0-0 2-2 0-2 2-1 2-2 1-0 1-1 1-2 2-2 2-4 1-2 1-2 1-2 2-0 0-1"),
 ("PNN","1-0 2-1 0-3 0-0 1-1 1-1 1-0 0-3 5-2 1-3 1-2 1-1 2-4 0-2 0-3"),
 ("ROS","2-3 0-2 0-0 0-0 1-1 4-1 3-1 0-1 3-1 1-1 3-2 4-0 1-1 0-3 0-1"),
 ("RUB","2-0 3-0 1-1 2-0 0-4 2-1 2-3 1-1 0-2 1-0 4-2 1-0 1-0 2-1 0-4"),
 ("SPA","0-0 4-0 1-2 1-2 2-2 3-0 5-0 0-3 3-0 5-2 2-0 3-0 3-0 1-0 2-1"),
 ("ZEN","3-0 1-2 0-0 2-1 1-0 3-1 1-0 4-1 2-3 1-1 1-0 2-1 5-0 4-0 0-0"),
],
"2025-26": [
 ("AKH","3-0 1-1 1-0 1-1 2-1 0-1 3-1 1-1 1-0 2-0 1-0 0-2 2-4 1-2 1-0"),
 ("AKR","1-1 0-2 1-2 1-1 2-3 0-1 1-1 1-1 1-2 1-2 1-3 2-2 3-2 1-1 1-1"),
 ("BAL","2-0 0-1 1-0 2-0 1-2 1-1 2-0 1-1 3-2 2-2 0-0 0-1 4-0 1-0 0-0"),
 ("CSK","2-1 3-1 1-0 3-1 1-4 1-1 1-0 3-1 2-0 2-0 1-1 5-1 0-1 3-2 1-3"),
 ("DMH","1-0 1-1 2-2 0-1 1-0 0-2 2-0 1-1 1-0 0-1 1-2 2-1 0-0 0-0 0-1"),
 ("DMO","2-2 1-2 1-1 1-3 3-0 2-1 4-0 3-5 3-3 3-0 1-0 0-1 2-0 2-2 1-3"),
 ("KRA","2-0 2-1 2-2 3-2 2-1 1-0 5-0 1-2 3-0 5-0 2-1 1-0 5-1 2-1 0-2"),
 ("KRY","2-2 4-1 1-1 1-1 2-0 2-3 0-6 2-0 1-1 2-0 2-0 0-0 2-0 2-1 1-1"),
 ("LOK","2-2 5-1 1-0 3-0 1-1 1-1 1-1 2-2 1-0 2-1 3-3 1-0 3-0 4-2 0-0"),
 ("ORE","2-2 2-0 0-0 0-0 1-1 1-3 0-1 1-0 0-1 2-1 0-1 2-2 3-1 0-2 2-1"),
 ("PNN","1-2 0-1 0-0 1-2 2-0 1-1 0-3 3-0 2-3 3-1 0-1 0-0 2-1 1-2 0-2"),
 ("ROS","1-1 0-1 1-1 1-0 1-1 0-1 0-0 1-4 1-3 0-1 1-0 2-0 0-1 1-1 0-1"),
 ("RUB","1-0 1-1 0-3 0-0 1-0 0-0 2-1 2-0 3-0 0-0 2-2 1-0 2-1 0-2 2-2"),
 ("SOC","1-1 0-4 0-2 1-3 0-0 1-1 1-2 2-1 2-4 3-1 2-1 0-1 0-1 2-3 0-3"),
 ("SPA","3-1 4-3 0-3 1-0 1-0 1-1 1-2 2-1 2-1 1-0 3-0 1-1 2-1 2-1 2-2"),
 ("ZEN","2-0 2-0 1-0 1-1 4-0 2-1 1-1 2-1 2-0 5-2 2-0 2-1 1-0 2-1 2-0"),
],
}
URL = {"2024-25": "https://en.wikipedia.org/wiki/2024%E2%80%9325_Russian_Premier_League",
       "2025-26": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Russian_Premier_League"}
GOALS = {"2024-25": 648, "2025-26": 609}

def matrix_cells(season):
    """-> list of (stockHome, stockAway, hg, ag) in matrix row order."""
    cols = COLS[season]; m2s = CODE2STOCK[season]; out = []
    for home_code, cellstr in ROWS[season]:
        cells = cellstr.split()
        away_cols = [c for c in cols if c != home_code]
        assert len(cells) == 15 and len(away_cols) == 15, (season, home_code, len(cells))
        for ac, cell in zip(away_cols, cells):
            hg, ag = cell.split("-")
            out.append((m2s[home_code], m2s[ac], int(hg), int(ag)))
    return out

def write_ledger(season):
    cells = matrix_cells(season)
    L = []
    L.append(f"# RPL {season} - SECOND-INDEX LEDGER (score-level; Wikipedia FBR results matrix)")
    L.append(f"# Source: {URL[season]} - section \"Results\" (full-season 16x16 FBR matrix). Fetched")
    L.append("# 2026-08-04 via MediaWiki API (action=parse, section 14, prop=wikitext). Matrix carries")
    L.append("# SCORES ONLY (no dates/rounds); date-level second-index coverage for these seasons: the")
    L.append("# football-data R1.csv feed is discontinued (mmz4281/2425 + /2526 404, verified 2026-08-04);")
    L.append("# openfootball/russia absent (404). worldfootball.net per-round pages confirmed as the")
    L.append("# spot-audit third anchor (MD30 2024-25 = 8/8 exact). League-table rows printed adjacent")
    L.append("# to the matrix agree with the RSSSF final-table constants club-for-club (both seasons);")
    L.append("# infobox anchors: 2024-25 240 matches / 648 goals; 2025-26 240 / 609.")
    L.append("# Row format: MX|<HomeStock>|<AwayStock>|<hg>|<ag>; stock strings = the RSSSF compact")
    L.append("# strings of the primary ledger so the diff is literal. Wiki code -> stock map in COLS.")
    L.append("COLS|" + "|".join(COLS[season]))
    for h, a, hg, ag in cells:
        L.append(f"MX|{h}|{a}|{hg}|{ag}")
    p = os.path.join(LEDGER, f"rpl-2ndidx-{season}.txt")
    with open(p, "w", encoding="ascii") as f:
        f.write("\n".join(L) + "\n")
    return p, cells

def primary_scores(season):
    d = {}
    with open(os.path.join(LEDGER, f"rpl-{season}.txt"), encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip():
                continue
            t = ln.split("|")
            if not t[0].startswith("R"):
                continue
            d[(t[2].strip(), t[5].strip())] = (int(t[3]), int(t[4]))
    return d

def official_table(season):
    rows = []
    rx = re.compile(r"^TABLE\|([^|]+)\|(\d+)\|([^|]+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|?(.*)$")
    with open(os.path.join(LEDGER, "rpl-venues.txt"), encoding="utf-8") as f:
        for ln in f:
            m = rx.match(ln.strip())
            if m and m.group(1) == season:
                rows.append({"pos": int(m.group(2)), "stock": m.group(3), "P": int(m.group(4)),
                             "W": int(m.group(5)), "D": int(m.group(6)), "L": int(m.group(7)),
                             "GF": int(m.group(8)), "GA": int(m.group(9)), "Pts": int(m.group(10)),
                             "note": m.group(11)})
    return rows

def season_window(season):
    return {"2024-25": ("2024-07-01", "2025-06-30"), "2025-26": ("2025-07-01", "2026-07-24")}[season]

def main():
    ok_all = True
    for season in ("2024-25", "2025-26"):
        p, cells = write_ledger(season)
        mx = {(h, a): (hg, ag) for h, a, hg, ag in cells}
        prim = primary_scores(season)
        # 1) score-for-score diff
        missing_in_mx = [k for k in prim if k not in mx]
        missing_in_pr = [k for k in mx if k not in prim]
        diffs = [(k, mx[k], prim[k]) for k in mx.keys() & prim.keys() if mx[k] != prim[k]]
        n_ident = sum(1 for k in mx.keys() & prim.keys() if mx[k] == prim[k])
        print(f"[{season}] matrix cells {len(mx)}; primary league rows {len(prim)}; missing mx {len(missing_in_mx)},"
              f" missing prim {len(missing_in_pr)}, score diffs {len(diffs)}, IDENTICAL {n_ident}/240")
        for k in missing_in_mx[:5]: print("   only-primary:", k, prim[k])
        for k in missing_in_pr[:5]: print("   only-matrix :", k, mx[k])
        for k, a, b in diffs[:10]: print("   DIFF:", k, "matrix", a, "primary", b)
        good = (len(mx) == 240 and len(prim) == 240 and not missing_in_mx and not missing_in_pr and not diffs)
        print(f"[{season}] score diff gate: {'PASS' if good else 'FAIL'}")
        ok_all &= good
        # 2) table recompute from matrix vs official constants
        stat = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
        for (h, a), (hg, ag) in mx.items():
            stat[h][0] += 1; stat[a][0] += 1
            stat[h][4] += hg; stat[h][5] += ag; stat[a][4] += ag; stat[a][5] += hg
            if hg > ag: stat[h][1] += 1; stat[a][3] += 1
            elif hg < ag: stat[a][1] += 1; stat[h][3] += 1
            else: stat[h][2] += 1; stat[a][2] += 1
        tab_ok = True
        for row in official_table(season):
            st = row["stock"]; P, W, D, Ld, GF, GA = stat[st]
            pts = 3 * W + D
            good_row = (P, W, D, Ld, GF, GA, pts) == (row["P"], row["W"], row["D"], row["L"], row["GF"], row["GA"], row["Pts"])
            if not good_row:
                print(f"   TABLE MISMATCH {st}: matrix {P} {W}-{D}-{Ld} {GF}-{GA} {pts} vs official "
                      f"{row['P']} {row['W']}-{row['D']}-{row['L']} {row['GF']}-{row['GA']} {row['Pts']}")
            tab_ok &= good_row
        tot = sum(hg + ag for hg, ag in mx.values())
        print(f"[{season}] matrix-recomputed table vs RSSSF official: {'16/16 PASS' if tab_ok else 'FAIL'};"
              f" goals {tot} (anchor {GOALS[season]}) {'PASS' if tot == GOALS[season] else 'FAIL'}")
        ok_all &= tab_ok and tot == GOALS[season]
    return 0 if ok_all else 1

if __name__ == "__main__":
    sys.exit(main())
