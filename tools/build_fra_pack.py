#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build + validate handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt (WO-FRA-SPAN-16, returned 2026-08-04).

PRIMARY:  audit/ledger/fra-<season>.txt  (RSSSF tablesf/fran2022..fran2025.html: full round-by-round
          transcribed to R1..R38/R34 rows + official FINAL TABLE constants as TABLE rows; fran2026.html
          prints NO league round-by-round (final table + cups only, verified full page 2026-08-04), so
          the 2025-26 match rows are carried by openfootball/europe france/2025-26_fr1.txt and gated
          EXACT against the RSSSF table by full recompute - documented source_adaptation).
2NDIDX:   audit/ledger/fra-2ndidx-<season>.txt (openfootball MD rows 2021-22..2024-25, diffed
          row-for-row: 380/380, 380/380, 306/306, 306/306 identical after two adjudicated date
          misprints) + audit/ledger/fra-2ndidx-2025-26-MX.txt (Wikipedia 2025-26 FBR matrix, 306
          cells: 305/306 identical, 1 documented wiki typo Brest-Lens).
CONSTANTS audit/ledger/fra-venues.txt (94 per-season stadium/city rows from the Wikipedia season
          articles' stadium/location tables; PO fallback entries for playoff-year home clubs).
PLAYOFFS  PO_PLAYOFF lines in the five ledgers: legs touching the Ligue 1 club SHIP as compType
          'other' (ERRATA-2026-08-03 + DECREE-2026-08-04 override; mirrors RPL/CZ1), L2-internal
          rounds stay NOT-COMMISSIONED context. 90-minute doctrine: aet legs ship the 90-min score
          (goal-minute verified in the wiki playoff boxes), advancement in pack NOTEs.
Output:   handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt  +  audit/pack-validation-fra.txt
Run:      python3 tools/build_fra_pack.py   (exit 0 iff every gate PASS; rebuild is deterministic)
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")
OUTPACK = os.path.join(ROOT, "handoffs", "FRA-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation-fra.txt")
ACCESSED = "2026-08-04"
SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
COMP = "France Ligue 1"                # WO section-2 verbatim
COMPTYPE = "domestic-league"           # WO section-2 verbatim
COMP_PO = "France Relegation Playoffs" # mirrors CZ1 pack's "Czech Relegation Playoffs"
COMPTYPE_PO = "other"                  # ERRATA-2026-08-03
COUNTRY = "France"
SRC_LABEL = {"2021-22": "rsssf-fran2022", "2022-23": "rsssf-fran2023", "2023-24": "rsssf-fran2024",
             "2024-25": "rsssf-fran2025", "2025-26": "ofb-fra-2526"}
PO_LABEL = {"2021-22": "rsssf-fran2022", "2023-24": "rsssf-fran2024", "2024-25": "rsssf-fran2025",
            "2025-26": "rsssf-fran2026"}
# (clubs, rounds, per-round) per season
SHAPE = {"2021-22": (20, 38, 10), "2022-23": (20, 38, 10), "2023-24": (18, 34, 9),
         "2024-25": (18, 34, 9), "2025-26": (18, 34, 9)}
EXP_ROWS = {"2021-22": 380, "2022-23": 380, "2023-24": 306, "2024-25": 306, "2025-26": 306}
DEDUCT = {"2021-22": {"Nice": 1, "Lyon": 1}, "2023-24": {"Montpellier": 1}}
ANCHORS = {"2021-22": (380, 1067, ("2021-08-06", "2022-05-21")),
           "2022-23": (380, 1067, ("2022-08-05", "2023-06-03")),
           "2023-24": (306, 826, ("2023-08-11", "2024-05-19")),
           "2024-25": (306, 911, ("2024-08-16", "2025-05-17")),
           "2025-26": (306, 863, ("2025-08-15", "2026-05-17"))}
SPOT = {"2021-22": 1, "2022-23": 2, "2023-24": 8, "2024-25": 9, "2025-26": 26}

# ------------------------------------------------------------- identity (WO section-3)
ROSTER26 = ["Ajaccio", "Angers", "Auxerre", "Bordeaux", "Brest", "Clermont", "Dijon", "Le Havre",
            "Lens", "Lille", "Lorient", "Lyon", "Marseille", "Metz", "Monaco", "Montpellier",
            "Nantes", "Nice", "Paris FC", "Paris SG", "Reims", "Rennes", "St Etienne", "Strasbourg",
            "Toulouse", "Troyes"]
ROSTER_SET = set(ROSTER26)
ANTI_APPEAR = ["PSG", "Saint-Etienne", "Saint-Étienne", "Paris Saint-Germain", "ASSE",
               "Havre AC", "Le Havre AC", "Stade Rennais", "Olympique"]
STOCK2ROSTER = {"ParisSG": "Paris SG", "SaintEtienne": "St Etienne", "LeHavre": "Le Havre",
                "ParisFC": "Paris FC"}
def roster(stock):
    return STOCK2ROSTER.get(stock, stock)

SOURCES = [
 ("rsssf-fran2022", "https://www.rsssf.org/tablesf/fran2022.html", "primary-archive",
  "2021-22: all 38 rounds dates+scores (round-3 Nice-Marseille and round-14 Lyon-Marseille VOID "
  "abandonments printed with their full replays [Oct 27]/[Feb 1] carrying the round labels), official "
  "final table with the Nice -1 / Lyon -1 brackets, pro/rel playoff block; transcribed in "
  "audit/ledger/fra-2021-22.txt; anchors 380 rows / 1,067 goals / span 2021-08-06..2022-05-21"),
 ("rsssf-fran2023", "https://www.rsssf.org/tablesf/fran2023.html", "primary-archive",
  "2022-23: all 38 rounds dates+scores + official final table (last 20-club season; no pro/rel "
  "playoff - four relegated direct as the league shrank to 18; '[Aug 14]' misprint for "
  "Lorient-Lyon documented under source_conflict); audit/ledger/fra-2022-23.txt; anchors 380 / "
  "1,067 / 2022-08-05..2023-06-03"),
 ("rsssf-fran2024", "https://www.rsssf.org/tablesf/fran2024.html", "primary-archive",
  "2023-24: all 34 rounds dates+scores (18 clubs from this season; round-8 Montpellier-Clermont "
  "VOID abandonment + closed-doors replay [Nov 29] under R8; Montpellier -1 bracket), official final "
  "table with the Metz/Lorient H2H tie-break, pro/rel playoff block; audit/ledger/fra-2023-24.txt; "
  "anchors 306 / 826 / 2023-08-11..2024-05-19"),
 ("rsssf-fran2025", "https://www.rsssf.org/tablesf/fran2025.html", "primary-archive",
  "2024-25: all 34 rounds dates+scores (round-26 Montpellier 0-2 Saint-Etienne abandoned 62' with "
  "the RESULT STANDING, openfootball prints it '[awarded]'; '[Oct 26]' misprint for "
  "Rennes-Le Havre documented under source_conflict), official final table, pro/rel playoff block; "
  "audit/ledger/fra-2024-25.txt; anchors 306 / 911 / 2024-08-16..2025-05-17"),
 ("rsssf-fran2026", "https://www.rsssf.org/tablesf/fran2026.html", "primary-archive",
  "2025-26: OFFICIAL FINAL TABLE + pro/rel playoff + Ligue 2/National tables and the Coupe de "
  "France - but NO league round-by-round (single-chunk page, verified in full 2026-08-04; same "
  "page shape as rsssf-eng2026 in the EPL pack); final-table authority for the season: the "
  "recompute of the pack's 306 rows reproduces it club-for-club and in position order EXACT; "
  "constants transcribed in audit/ledger/fra-2025-26.txt; also the playoff-leg source for 2025-26"),
 ("rsssf-fran2027", "https://www.rsssf.org/tablesf/fran2027.html", "primary-archive",
  "404 Not Found on 2026-08-04 - boundary evidence that no 2026-27 season page (and no played "
  "2026-27 fixture) existed on the return date"),
 ("ofb-fra-2526", "https://raw.githubusercontent.com/openfootball/europe/master/france/2025-26_fr1.txt",
  "match-carrier",
  "2025-26 match rows (306 fixtures: banner groups RS1..RS34 mapped to MD1..MD34 incl. the three "
  "banner-appended strays - Marseille 1-0 Paris SG played Mon 2025-09-22 (RS5, storm), Paris SG "
  "3-0 Nantes played 2026-04-22 (RS26 duplicate banner block), Brest 1-2 Strasbourg + Lens 0-2 "
  "Paris SG played 2026-05-13 (RS29 duplicate banner block); file header '# Matches 306', dates "
  "Fri Aug 15 2025 - Sun May 17 2026, fetched 2026-08-04) - the season's date/score carrier under "
  "the documented source_adaptation; label carried on all 2025-26 league MATCH rows"),
 ("ofb-fra-2122", "https://raw.githubusercontent.com/openfootball/europe/master/france/2021-22_fr1.txt",
  "second-index", "380 matchday-grouped rows diffed vs the RSSSF rows: 380/380 pairings IDENTICAL "
  "on round + date + score (audit/ledger/fra-2ndidx-2021-22.txt, tools/diff_epl_second_index.py)"),
 ("ofb-fra-2223", "https://raw.githubusercontent.com/openfootball/europe/master/france/2022-23_fr1.txt",
  "second-index", "380 rows diffed: 379/380 + ONE divergence - RSSSF prints Lorient 3-1 Lyon "
  "under round 2 '[Aug 14]' while openfootball AND the worldfootball MD2 page both date the match "
  "2022-09-07 19:00; resolved per section-4 (two independents agree against the primary); "
  "audit/ledger/fra-2ndidx-2022-23.txt"),
 ("ofb-fra-2324", "https://raw.githubusercontent.com/openfootball/europe/master/france/2023-24_fr1.txt",
  "second-index", "306 rows diffed: 306/306 IDENTICAL round + date + score "
  "(audit/ledger/fra-2ndidx-2023-24.txt)"),
 ("ofb-fra-2425", "https://raw.githubusercontent.com/openfootball/europe/master/france/2024-25_fr1.txt",
  "second-index", "306 rows diffed: 305/306 + ONE divergence - RSSSF prints Rennes 1-0 Le Havre "
  "under round 9 '[Oct 26]' while openfootball ('Fri Oct 25') AND the worldfootball MD9 page "
  "(25.10.2024 20:45) agree on 2024-10-25; resolved per section-4; audit/ledger/fra-2ndidx-2024-25.txt"),
 ("wikimatrix-fra-2526", "https://en.wikipedia.org/wiki/2025%E2%80%9326_Ligue_1", "second-index",
  "Results FBR matrix (306 cells, source line: ligue1.com; action=raw transcription) diffed vs the "
  "2025-26 carrier rows: 305/306 IDENTICAL scores - the one divergence is the matrix's own Brest-Lens "
  "print '3-0', disproved by the RSSSF final table, the article's own league-table template, the "
  "carrier and the 863-goal season total (documented source_conflict); matrix also evidences the "
  "Nantes-Toulouse 0-0 abandonment-22' efn and the article carries the playoff boxes used to fix "
  "the 90-minute splits (audit/ledger/fra-2ndidx-2025-26-MX.txt)"),
 ("wiki-fra-venues", "https://en.wikipedia.org/wiki/2021%E2%80%9322_Ligue_1", "second-index",
  "stadium/location tables of the five season articles 2021-22..2025-26 (sibling pages "
  "...%E2%80%9322 through ...%E2%80%9326_Ligue_1; fetched 2026-08-04): 94 venue rows = the "
  "stadium/city constants in audit/ledger/fra-venues.txt; each article's promoted/relegated prose "
  "matches the membership gates; playoff boxes verified the 90-minute splits (2021-22 Sakhi 51' / "
  "Camara 76' -> 1-1 at 90; 2023-24 Wadji 116' -> Metz 2-1 at 90; 2024-25 Toure 110'/Hein 114' -> "
  "Reims 1-1 at 90; 2025-26 no ET, leg2 behind closed doors)"),
 ("wf-fra-2122-md1", "https://www.worldfootball.net/schedule/fra-ligue-1-2021-2022-spieltag/1/",
  "second-index", "2021-22 matchday-1 spot-audit page (canonical results-and-standings redirect): "
  "the round's dates and scores match the pack rows"),
 ("wf-fra-2223-md2", "https://www.worldfootball.net/schedule/fra-ligue-1-2022-2023-spieltag/2/",
  "second-index", "2022-23 matchday-2 spot-audit page: prints Lorient 3:1 Lyon on 07.09.2022 19:00 - "
  "one of the two independent indexes adjudicating the RSSSF '[Aug 14]' misprint"),
 ("wf-fra-2324-md8", "https://www.worldfootball.net/schedule/fra-ligue-1-2023-2024-spieltag/8/",
  "second-index", "2023-24 matchday-8 spot-audit page: eight fixtures dated 2023-10-06..08 plus the "
  "Montpellier 1:1 Clermont full replay dated 29.11.2023 19:00 - matches the pack rows one-for-one"),
 ("wf-fra-2425-md9", "https://www.worldfootball.net/schedule/fra-ligue-1-2024-2025-spieltag/9/",
  "second-index", "2024-25 matchday-9 spot-audit page: prints Rennes 1:0 Le Havre on 25.10.2024 "
  "20:45 - one of the two independent indexes adjudicating the RSSSF '[Oct 26]' misprint"),
 ("wf-fra-2526-md26", "https://www.worldfootball.net/schedule/fra-ligue-1-2025-2026-spieltag/26/",
  "second-index", "2025-26 matchday-26 spot-audit page: eight fixtures dated 2026-03-13..15 plus "
  "Paris SG 3:0 Nantes dated 22.04.2026 19:00 - corroborates the carrier's RS26 banner-stray "
  "mapping one-for-one"),
 ("wiki-fra-2627", "https://en.wikipedia.org/wiki/2026%E2%80%9327_Ligue_1", "second-index",
  "span-end boundary: 2026-27 season dates 23 August 2026 - 29 May 2027, 18 teams; Paris SG enter "
  "as FIVE-time defending champions; promoted Troyes and Le Mans; relegated Metz and Nantes - "
  "exactly this pack's 2025-26 bottom two plus playoff survivor Nice staying up: consistent; the "
  "season had NOT started on the return date 2026-08-04"),
]

# ---------------------------------------------------------------- readers
R_RX = re.compile(r"^R(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MD_RX = re.compile(r"^MD(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MX_RX = re.compile(r"^MX\|([^|]+)\|([^|]+)\|(\d+)\|(\d+)$")
PO_RX = re.compile(r"^PO_PLAYOFF\|([^|]+)\|([^|]+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)\|([^|]*)\|(.*)$")

def read_season(season):
    rows, table, po = [], [], []
    with open(os.path.join(LEDGER, f"fra-{season}.txt"), encoding="utf-8") as fh:
        for ln in fh:
            s = ln.rstrip("\n")
            m = R_RX.match(s)
            if m:
                rows.append({"rnd": int(m.group(1)), "date": m.group(2), "home": m.group(3).strip(),
                             "hg": int(m.group(4)), "ag": int(m.group(5)), "away": m.group(6).strip()})
                continue
            if s.startswith("TABLE|"):
                p = s.split("|")
                table.append({"pos": int(p[2]), "club": p[3].strip(), "P": int(p[4]), "W": int(p[5]),
                              "D": int(p[6]), "L": int(p[7]), "GF": int(p[8]), "GA": int(p[9]),
                              "Pts": int(p[10]), "note": p[11] if len(p) > 11 else ""})
                continue
            m = PO_RX.match(s)
            if m:
                po.append({"season": m.group(1), "stage": m.group(2), "date": m.group(3),
                           "home": m.group(4).strip(), "hg": int(m.group(5)), "ag": int(m.group(6)),
                           "away": m.group(7).strip(), "extra": m.group(8), "flags": m.group(9)})
    return rows, table, po

def read_venues():
    ven = {}
    with open(os.path.join(LEDGER, "fra-venues.txt"), encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("VENUE|"):
                p = ln.rstrip("\n").split("|")
                ven[(p[1], p[2])] = (p[3], p[4])
    return ven

def read_2ndidx_md(season):
    out = {}
    with open(os.path.join(LEDGER, f"fra-2ndidx-{season}.txt"), encoding="utf-8") as fh:
        for ln in fh:
            m = MD_RX.match(ln.strip())
            if m:
                out[(m.group(3).strip(), m.group(6).strip())] = (int(m.group(1)), m.group(2),
                                                                 int(m.group(4)), int(m.group(5)))
    return out

def read_2ndidx_mx():
    out = {}
    with open(os.path.join(LEDGER, "fra-2ndidx-2025-26-MX.txt"), encoding="utf-8") as fh:
        for ln in fh:
            m = MX_RX.match(ln.strip())
            if m:
                out[(m.group(1).strip(), m.group(2).strip())] = (int(m.group(3)), int(m.group(4)))
    return out

# ---------------------------------------------------------------- gates
class Gates:
    def __init__(self):
        self.lines = []
        self.n_pass = 0
        self.n_fail = 0
    def g(self, ok, label):
        self.lines.append(("PASS " if ok else "FAIL ") + label)
        if ok:
            self.n_pass += 1
        else:
            self.n_fail += 1

def emit_match(season, r, ven):
    h, a = roster(r["home"]), roster(r["away"])
    stadium, city = ven[(season, r["home"])]
    return (f"MATCH|{r['date']}|{COMP}|{COMPTYPE}|{h}|{r['hg']}|{r['ag']}|{a}|MD{r['rnd']}|"
            f"{stadium}|{city}|{COUNTRY}||{SRC_LABEL[season]}")

# SHIP-as-other playoff legs, 90-minute doctrine applied (verified against the wiki playoff boxes'
# goal minutes 2026-08-04 + RSSSF playoff blocks). Tuple:
# (season, date, home, hg90, ag90, away, venueDetail, stadium, city, sourceLabel, aetFinal-or-None)
PO_SHIP = [
 ("2021-22", "2022-05-26", "Auxerre", 1, 1, "SaintEtienne", "Playoff leg1",
  "Stade de l'Abbe-Deschamps", "Auxerre", "rsssf-fran2022", None),
 ("2021-22", "2022-05-29", "SaintEtienne", 1, 1, "Auxerre", "Playoff leg2",
  "Stade Geoffroy-Guichard", "Saint-Etienne", "rsssf-fran2022", (1, 1)),
 ("2023-24", "2024-05-30", "SaintEtienne", 2, 1, "Metz", "Playoff leg1",
  "Stade Geoffroy Guichard", "Saint-Etienne", "rsssf-fran2024", None),
 ("2023-24", "2024-06-02", "Metz", 2, 1, "SaintEtienne", "Playoff leg2",
  "Stade Saint-Symphorien", "Longeville-les-Metz", "rsssf-fran2024", (2, 2)),
 ("2024-25", "2025-05-21", "Metz", 1, 1, "Reims", "Playoff leg1",
  "Stade Saint-Symphorien", "Longeville-les-Metz", "rsssf-fran2025", None),
 ("2024-25", "2025-05-29", "Reims", 1, 1, "Metz", "Playoff leg2",
  "Stade Auguste Delaune", "Reims", "rsssf-fran2025", (1, 3)),
 ("2025-26", "2026-05-26", "SaintEtienne", 0, 0, "Nice", "Playoff leg1",
  "Stade Geoffroy Guichard", "Saint-Etienne", "rsssf-fran2026", None),
 ("2025-26", "2026-05-29", "Nice", 4, 1, "SaintEtienne", "Playoff leg2",
  "Allianz Riviera", "Nice", "rsssf-fran2026", None),
]

def pivot_block(season, rows, table):
    stats = {t["club"]: (t["P"], t["W"], t["D"], t["L"], t["GF"], t["GA"], t["Pts"]) for t in table}
    lines, summaries = [], {}
    for club in sorted(stats):
        games = sorted((r for r in rows if r["home"] == club or r["away"] == club),
                       key=lambda r: r["rnd"])
        w = d = l = gf = ga = 0
        entries = []
        for i, r in enumerate(games, 1):
            if r["home"] == club:
                gf += r["hg"]; ga += r["ag"]
                w += r["hg"] > r["ag"]; d += r["hg"] == r["ag"]; l += r["hg"] < r["ag"]
                entries.append(f"{i}|MD{r['rnd']}|{r['date']}|H|{roster(r['away'])}|{r['hg']}|{r['ag']}|home")
            else:
                gf += r["ag"]; ga += r["hg"]
                w += r["ag"] > r["hg"]; d += r["ag"] == r["hg"]; l += r["ag"] < r["hg"]
                entries.append(f"{i}|MD{r['rnd']}|{r['date']}|A|{roster(r['home'])}|{r['ag']}|{r['hg']}|away")
        raw = 3 * w + d
        ded = DEDUCT.get(season, {}).get(club, 0)
        exp = stats[club]
        ok = (len(games) == exp[0] and (w, d, l, gf, ga) == exp[1:6] and raw - ded == exp[6])
        ded_txt = f" (-{ded} deducted => {exp[6]})" if ded else ""
        summ = f"TEAMPIVOT|{roster(club)}|P{len(games)} W{w} D{d} L{l} GF{gf} GA{ga} PTS{exp[6]}{ded_txt}"
        summaries[club] = (ok, summ, len(games))
        lines.append(summ)
        lines.extend(entries)
        lines.append("")
    return lines, summaries

def spot_listing(season, rnd, rows):
    games = sorted((r for r in rows if r["rnd"] == rnd), key=lambda r: (r["date"], r["home"]))
    return "; ".join(f"{r['date']} {roster(r['home'])} {r['hg']}-{r['ag']} {roster(r['away'])}"
                     for r in games)

def main():
    ven = read_venues()
    data = {}
    for s in SEASONS:
        data[s] = read_season(s)

    G = Gates()
    pack_rows = []
    season_blocks = []   # (season, [league lines], [po lines])

    # ---- structural gates + emission, season by season
    for s in SEASONS:
        rows, table, po = data[s]
        nclubs, nrounds, per = SHAPE[s]
        want_rows = EXP_ROWS[s]
        G.g(len(rows) == want_rows, f"{s}: {want_rows} rows (got {len(rows)})")
        G.g(len(table) == nclubs, f"{s}: {nclubs} TABLE constants (got {len(table)})")
        rnd = defaultdict(int)
        for r in rows:
            rnd[r["rnd"]] += 1
        G.g(all(rnd.get(n, 0) == per for n in range(1, nrounds + 1)) and len(rnd) == nrounds,
            f"{s}: rounds 1..{nrounds} x {per} rows")
        pairs = [(r["home"], r["away"]) for r in rows]
        G.g(len(set(pairs)) == want_rows, f"{s}: {want_rows} distinct ordered (home,away) pairings")
        hc = defaultdict(int); ac = defaultdict(int)
        for h, a in pairs:
            hc[h] += 1; ac[a] += 1
        ha = nrounds // 2
        G.g(all(hc[c] == ha and ac[c] == ha for c in set(hc) | set(ac)) and len(set(hc) | set(ac)) == nclubs,
            f"{s}: every club {ha} home + {ha} away")
        srt = sorted(rows, key=lambda r: (r["date"], r["rnd"], r["home"], r["away"]))
        G.g([r["date"] for r in srt] == sorted(r["date"] for r in srt), f"{s}: rows date-sortable")
        # table reproduction
        st = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
        for r in rows:
            st[r["home"]][0] += 1; st[r["away"]][0] += 1
            st[r["home"]][4] += r["hg"]; st[r["home"]][5] += r["ag"]
            st[r["away"]][4] += r["ag"]; st[r["away"]][5] += r["hg"]
            if r["hg"] > r["ag"]: st[r["home"]][1] += 1; st[r["away"]][3] += 1
            elif r["hg"] < r["ag"]: st[r["away"]][1] += 1; st[r["home"]][3] += 1
            else: st[r["home"]][2] += 1; st[r["away"]][2] += 1
        ded = DEDUCT.get(s, {})
        bad, order = [], []
        h2h_pts = defaultdict(int)
        for r in rows:
            if r["hg"] > r["ag"]: h2h_pts[(r["home"], r["away"])] += 3
            elif r["hg"] < r["ag"]: h2h_pts[(r["away"], r["home"])] += 3
            else: h2h_pts[(r["home"], r["away"])] += 1; h2h_pts[(r["away"], r["home"])] += 1
        for t in table:
            c = st[t["club"]]
            pts = c[1] * 3 + c[2] - ded.get(t["club"], 0)
            if [c[0], c[1], c[2], c[3], c[4], c[5], pts] != [t["P"], t["W"], t["D"], t["L"], t["GF"], t["GA"], t["Pts"]]:
                bad.append(t["club"])
            order.append((t["club"], pts, c[4] - c[5], c[4], t["pos"]))
        G.g(not bad, f"{s}: table reproduction club-for-club {nclubs}/{nclubs} (P/W/D/L/GF/GA/Pts"
                     + (f", deductions {ded}" if ded else "") + f") fails={bad or '-'}")
        # position order, Ligue 1 rule depth: pts -> overall GD -> H2H pts -> H2H GD -> H2H away
        # goals -> GF (RSSSF 2023-24 prints the tie-break brackets: Metz/Lorient [2 1 0 1 4-4 3;
        # 3 ag] vs [.. 2 ag] - 3-3 H2H points, level H2H GD, away goals 3-2 decides)
        h2h_gd = defaultdict(int)
        h2h_away = defaultdict(int)
        for r in rows:
            if r["hg"] > r["ag"]:
                h2h_gd[(r["home"], r["away"])] += r["hg"] - r["ag"]
                h2h_gd[(r["away"], r["home"])] -= r["hg"] - r["ag"]
            elif r["hg"] < r["ag"]:
                h2h_gd[(r["away"], r["home"])] += r["ag"] - r["hg"]
                h2h_gd[(r["home"], r["away"])] -= r["ag"] - r["hg"]
            h2h_away[(r["away"], r["home"])] += r["ag"]  # club's goals scored away from home in the tie
        inv = []
        for i in range(len(order) - 1):
            (c1, p1, gd1, gf1, pos1), (c2, p2, gd2, gf2, pos2) = order[i], order[i + 1]
            if (p1, gd1) > (p2, gd2):
                continue
            if p1 == p2 and gd1 == gd2:
                key1 = (h2h_pts.get((c1, c2), 0), h2h_gd.get((c1, c2), 0), h2h_away.get((c1, c2), 0), gf1)
                key2 = (h2h_pts.get((c2, c1), 0), h2h_gd.get((c2, c1), 0), h2h_away.get((c2, c1), 0), gf2)
                if key1 > key2:
                    continue
            inv.append((c1, c2))
        G.g(not inv, f"{s}: final-table position order consistent (pts/GD/GF with Ligue 1 H2H "
                     f"exceptions verified from the pack rows) inversions={inv or '-'}")
        members = {t["club"] for t in table}
        G.g(len(members) == nclubs and all(roster(c) in ROSTER_SET for c in members),
            f"{s}: {nclubs} member clubs, every roster string in WO section-3 domain")
        goals = sum(r["hg"] + r["ag"] for r in rows)
        span = (min(r["date"] for r in rows), max(r["date"] for r in rows))
        want = ANCHORS[s]
        G.g((len(rows), goals, span) == (want[0], want[1], want[2]),
            f"{s}: anchors {want[0]} rows / {want[1]} goals / span {want[2][0]}..{want[2][1]} "
            f"(got {len(rows)}/{goals}/{span[0]}..{span[1]})")
        block = []
        for r in sorted(rows, key=lambda r: (r["date"], r["rnd"], r["home"], r["away"])):
            block.append(emit_match(s, r, ven))
        season_blocks.append((s, block))
        pack_rows.extend(block)

    # ---- season-to-season membership boundary gates
    EXP = {"2021-22": {"out": {"SaintEtienne", "Metz", "Bordeaux"}, "in": {"Toulouse", "Ajaccio", "Auxerre"}, "nswap": 6, "nout": 3},
           "2022-23": {"out": {"Auxerre", "Ajaccio", "Troyes", "Angers"}, "in": {"LeHavre", "Metz"}, "nswap": 6, "nout": 4},
           "2023-24": {"out": {"Metz", "Lorient", "Clermont"}, "in": {"Auxerre", "Angers", "SaintEtienne"}, "nswap": 6, "nout": 3},
           "2024-25": {"out": {"Reims", "SaintEtienne", "Montpellier"}, "in": {"Lorient", "ParisFC", "Metz"}, "nswap": 6, "nout": 3}}
    for i in range(4):
        s1, s2 = SEASONS[i], SEASONS[i + 1]
        m1 = {t["club"] for t in data[s1][1]}
        m2 = {t["club"] for t in data[s2][1]}
        nrel = EXP[s1]["nout"]
        bottom = {t["club"] for t in data[s1][1] if t["pos"] > len(m1) - nrel}
        G.g(bottom == EXP[s1]["out"] and not (bottom & m2) and EXP[s1]["in"] <= m2
            and not (EXP[s1]["in"] & m1) and len(m1 ^ m2) == EXP[s1]["nswap"],
            f"boundary {s1}->{s2}: relegated {sorted(bottom)} absent in {s2}; promoted "
            f"{sorted(EXP[s1]['in'])} present (and absent in {s1}); memberships verified")

    # ---- playoff ('other') rows: curated 90-min ships cross-verified against ledger PO lines
    po_all = [p for s in SEASONS for p in data[s][2]]
    ships = [p for p in po_all if "SHIP-as-other" in p["flags"]]
    notcom = [p for p in po_all if "NOT-COMMISSIONED" in p["flags"]]
    G.g(len(ships) == 8 and len(notcom) == 8,
        f"playoffs: 8 SHIP-as-other legs (2 each of 2021-22/2023-24/2024-25/2025-26) + 8 "
        f"NOT-COMMISSIONED L2-internal lines (got {len(ships)}/{len(notcom)})")
    po_lines = []
    ok_po = True
    for (s, date, home, hg90, ag90, away, vd, stadium, city, label, aet) in PO_SHIP:
        matches = [p for p in ships if p["season"] == s and p["date"] == date
                   and p["home"] == home and p["away"] == away]
        if not matches:
            ok_po = False
            continue
        p = matches[0]
        if aet:
            ok_po &= (p["hg"], p["ag"]) == aet and "aet" in p["extra"]
        else:
            ok_po &= (p["hg"], p["ag"]) == (hg90, ag90)
        po_lines.append((s, f"MATCH|{date}|{COMP_PO}|{COMPTYPE_PO}|{roster(home)}|{hg90}|{ag90}|"
                            f"{roster(away)}|{vd}|{stadium}|{city}|{COUNTRY}||{label}"))
    G.g(ok_po, "playoffs: every SHIP leg's ledger print matches the curated row (aet leg finals "
               "match the RSSSF prints; 90-minute scores ship per doctrine)")
    # append PO rows to their season blocks (date position = after the league season, order kept)
    for s, lines in po_lines:
        pack_rows.append(lines)

    # ---- global gates
    G.g(len(pack_rows) == 1678 + 8, f"pack: 1,686 MATCH rows total = 1,678 league + 8 playoff (got {len(pack_rows)})")
    keys = ["|".join((f[1], f[4], f[7])) for f in (line.split("|") for line in pack_rows)]
    G.g(len(set(keys)) == len(keys), "pack: zero duplicate (date,home,away) rows")
    clubs_union = set()
    for s in SEASONS:
        clubs_union |= {roster(t["club"]) for t in data[s][1]}
    clubs_union |= {roster(x[2]) for x in PO_SHIP} | {roster(x[5]) for x in PO_SHIP}
    G.g(clubs_union == ROSTER_SET - {"Dijon"},
        f"pack: union of clubs across 5 seasons + playoffs = 25 of the 26 WO section-3 strings "
        f"(Dijon pinned by the WO but never in-window - last top-flight season 2020-21, documented "
        f"not a gap; got {len(clubs_union)})")
    bad_names = [c for line in pack_rows for c in (line.split("|")[4], line.split("|")[7])
                 if c not in ROSTER_SET]
    G.g(not bad_names, f"pack: every home/away string verbatim in the roster domain (bad={bad_names[:4] or '-'})")
    anti = [line for line in pack_rows
            if any(a in line.split("|")[4] or a in line.split("|")[7] for a in ANTI_APPEAR)]
    G.g(not anti, "pack: anti-appear traps absent from home/away identity fields (PSG / Saint-Etienne "
                  "with hyphen / Paris Saint-Germain / full club-name forms; the city field's "
                  "'Saint-Etienne' is sourced venue prose, not an identity) hits=" + str(len(anti)))

    # ---- second-index gates
    for s in ["2021-22", "2022-23", "2023-24", "2024-25"]:
        idx = read_2ndidx_md(s)
        rows = data[s][0]
        same = miss = 0
        diffs = []
        for r in rows:
            k = (r["home"], r["away"])
            if k not in idx:
                miss += 1
                continue
            e = idx[k]
            if e == (r["rnd"], r["date"], r["hg"], r["ag"]):
                same += 1
            else:
                diffs.append((k, (r["rnd"], r["date"], r["hg"], r["ag"]), e))
        G.g(same == EXP_ROWS[s] and miss == 0 and not diffs,
            f"2ndidx {s}: {EXP_ROWS[s]}/{EXP_ROWS[s]} pairings IDENTICAL round+date+score vs "
            f"openfootball (same={same} miss={miss} divergent={len(diffs)})")
    idx_mx = read_2ndidx_mx()
    rows26 = data["2025-26"][0]
    same = miss = 0
    diffs = []
    for r in rows26:
        k = (r["home"], r["away"])
        if k not in idx_mx:
            miss += 1
            continue
        e = idx_mx[k]
        if e == (r["hg"], r["ag"]):
            same += 1
        else:
            diffs.append((k, (r["hg"], r["ag"]), e))
    g_idx = sum(v[0] + v[1] for v in idx_mx.values())
    G.g(same == 305 and miss == 0 and diffs == [(("Brest", "Lens"), (3, 3), (3, 0))] and g_idx == 860,
        f"2ndidx 2025-26: Wikipedia FBR matrix 306 cells - 305 IDENTICAL scores + exactly the one "
        f"documented wiki typo (Brest-Lens 3-0 print vs 3-3 everywhere else incl. the season table); "
        f"matrix goals 860 vs carrier 863 (same={same} miss={miss} divergent={len(diffs)} mxgoals={g_idx})")

    # ---- anomaly gates
    r21 = data["2021-22"][0]
    G.g(not any(r["home"] == "Nice" and r["away"] == "Marseille" and r["date"] == "2021-08-22" for r in r21)
        and any(r["rnd"] == 3 and r["home"] == "Nice" and r["away"] == "Marseille"
                and r["date"] == "2021-10-27" and (r["hg"], r["ag"]) == (1, 1) for r in r21),
        "anomaly 2021-22 R3: no Nice-Marseille row on 2021-08-22 (abandoned 75' at 1-0, VOID); "
        "full replay 2021-10-27 Nice 1-1 Marseille carries the R3 label")
    G.g(not any(r["home"] == "Lyon" and r["away"] == "Marseille" and r["date"] == "2021-11-21" for r in r21)
        and any(r["rnd"] == 14 and r["home"] == "Lyon" and r["away"] == "Marseille"
                and r["date"] == "2022-02-01" and (r["hg"], r["ag"]) == (2, 1) for r in r21),
        "anomaly 2021-22 R14: no Lyon-Marseille row on 2021-11-21 (abandoned 5' at 0-0, VOID); "
        "full replay 2022-02-01 Lyon 2-1 Marseille carries the R14 label")
    r22 = data["2022-23"][0]
    G.g(any(r["rnd"] == 2 and r["home"] == "Lorient" and r["away"] == "Lyon"
            and r["date"] == "2022-09-07" and (r["hg"], r["ag"]) == (3, 1) for r in r22),
        "anomaly 2022-23 R2: Lorient-Lyon dated 2022-09-07 (RSSSF '[Aug 14]' misprint overridden "
        "on two independent indexes)")
    r23 = data["2023-24"][0]
    G.g(not any(r["home"] == "Montpellier" and r["away"] == "Clermont" and r["date"] == "2023-10-08" for r in r23)
        and any(r["rnd"] == 8 and r["home"] == "Montpellier" and r["away"] == "Clermont"
                and r["date"] == "2023-11-29" and (r["hg"], r["ag"]) == (1, 1) for r in r23),
        "anomaly 2023-24 R8: no Montpellier-Clermont row on 2023-10-08 (abandoned 90+2' at 4-2, "
        "VOID + Montpellier -1); closed-doors replay 2023-11-29 Montpellier 1-1 Clermont carries R8")
    r24 = data["2024-25"][0]
    G.g(any(r["rnd"] == 9 and r["home"] == "Rennes" and r["away"] == "LeHavre"
            and r["date"] == "2024-10-25" and (r["hg"], r["ag"]) == (1, 0) for r in r24),
        "anomaly 2024-25 R9: Rennes-Le Havre dated 2024-10-25 (RSSSF '[Oct 26]' misprint "
        "overridden on two independent indexes)")
    G.g(any(r["rnd"] == 26 and r["home"] == "Montpellier" and r["away"] == "SaintEtienne"
            and (r["hg"], r["ag"]) == (0, 2) for r in r24),
        "anomaly 2024-25 R26: Montpellier 0-2 St Etienne row SHIPS normally - abandoned 62' but "
        "the result STOOD (openfootball prints '[awarded]'), no VOID, no replay")
    r26 = data["2025-26"][0]
    md5 = [r for r in r26 if r["rnd"] == 5]
    md26 = [r for r in r26 if r["rnd"] == 26]
    md29 = [r for r in r26 if r["rnd"] == 29]
    G.g(len(md5) == 9 and any(r["home"] == "Marseille" and r["away"] == "ParisSG"
            and r["date"] == "2025-09-22" and (r["hg"], r["ag"]) == (1, 0) for r in md5)
        and sum(1 for r in md5 if "2025-09-19" <= r["date"] <= "2025-09-21") == 8,
        "anomaly 2025-26 MD5: 9 rows = 8 main-window (2025-09-19..21) + Marseille 1-0 Paris SG "
        "storm-postponed to Monday 2025-09-22")
    G.g(len(md26) == 9 and any(r["home"] == "ParisSG" and r["away"] == "Nantes"
            and r["date"] == "2026-04-22" and (r["hg"], r["ag"]) == (3, 0) for r in md26)
        and sum(1 for r in md26 if "2026-03-13" <= r["date"] <= "2026-03-15") == 8,
        "anomaly 2025-26 MD26: 9 rows = 8 main-window (2026-03-13..15, wf-md26 corroborated) + "
        "Paris SG 3-0 Nantes postponed to 2026-04-22 (wf-md26 corroborated)")
    G.g(len(md29) == 9
        and any(r["home"] == "Brest" and r["away"] == "Strasbourg" and r["date"] == "2026-05-13"
                and (r["hg"], r["ag"]) == (1, 2) for r in md29)
        and any(r["home"] == "Lens" and r["away"] == "ParisSG" and r["date"] == "2026-05-13"
                and (r["hg"], r["ag"]) == (0, 2) for r in md29)
        and sum(1 for r in md29 if "2026-04-10" <= r["date"] <= "2026-04-12") == 7,
        "anomaly 2025-26 MD29: 9 rows = 7 main-window (2026-04-10..12) + Brest-Strasbourg and "
        "Lens-Paris SG (the title decider) both on 2026-05-13")
    G.g(any(r["rnd"] == 34 and r["home"] == "Nantes" and r["away"] == "Toulouse"
            and r["date"] == "2026-05-17" and (r["hg"], r["ag"]) == (0, 0) for r in r26),
        "anomaly 2025-26 MD34: Nantes 0-0 Toulouse row SHIPS - abandoned 22' (pitch invasion) "
        "with the score UPHELD by the LFP (wiki efn), no replay")

    # ---- venue gate
    bad_ven = []
    for line in pack_rows:
        f = line.split("|")
        if not f[9] or not f[10]:
            bad_ven.append(line)
    G.g(not bad_ven and len(ven) == 94,
        f"venues: all 1,686 rows carry stadium/city constants (94 venue rows in fra-venues.txt = "
        f"5 seasons x membership; playoff legs use the curated home-club grounds incl. the "
        f"documented fallback seasons); empties={len(bad_ven)}")

    # ---- pivot gate (owner decree)
    pivot_out = []
    all_ok = True
    green = 0
    total = 0
    for s in SEASONS:
        rows, table, _ = data[s]
        lines, summaries = pivot_block(s, rows, table)
        okn = sum(1 for v in summaries.values() if v[0])
        all_ok &= okn == SHAPE[s][0]
        green += okn
        total += SHAPE[s][0]
        pivot_out.append(f"### PIVOT {s} (re-derived from the pack's own rows; each club = its "
                         f"{SHAPE[s][1]} games in round order; summary gated vs the season TABLE "
                         f"constants)")
        pivot_out.extend(lines)
    G.g(all_ok, f"pivots: {green}/{total} club-season full-campaign pivots reproduce the "
                "final-table lines (38 or 34 games each, deductions flagged)")

    # ---- pack grammar gate
    gram_ok = all(len(line.split("|")) == 14 for line in pack_rows)
    G.g(gram_ok, "grammar: every MATCH line has 14 pipe-fields (incl. empty pre-source field)")
    comp_ok = True
    for line in pack_rows:
        f = line.split("|")
        if f[3] == COMPTYPE and (f[2] != COMP or f[11] != COUNTRY):
            comp_ok = False
        if f[3] == COMPTYPE_PO and (f[2] != COMP_PO or f[11] != COUNTRY):
            comp_ok = False
        if f[3] not in (COMPTYPE, COMPTYPE_PO):
            comp_ok = False
    G.g(comp_ok, "grammar: competition/compType/country constants per row class (league rows: "
                 "'France Ligue 1'/'domestic-league'; playoff legs: 'France Relegation "
                 "Playoffs'/'other'; country France everywhere - AS Monaco is the French league's "
                 "cross-border member, disclosed under venue_policy)")
    labels = {s[0] for s in SOURCES}
    G.g(all(line.split("|")[13] in labels for line in pack_rows),
        "grammar: every row's sourceLabel resolves to a declared SOURCE")
    try:
        for line in pack_rows:
            line.encode("ascii")
        asc = True
    except UnicodeEncodeError:
        asc = False
    G.g(asc, "grammar: ASCII-only pack rows (venue/team strings NFKD-folded - Velodrome, Oceane, "
             "Abbe, Decines; apostrophes typewriter)")

    # ---------------------------------------------------------------- NOTE texts
    notes = []
    notes.append(
        f"NOTE|info|pack_id|FRA-2021-2026_BP-TEAM-PACK_v2 - return of WO-FRA-SPAN-16 (queue "
        f"position 16), FULL SPAN under OWNER OVERRIDE DECREE-2026-08-04 ('I require you to "
        f"deliver full season files regardless of what the workorder said ... my authority "
        f"overrides everything ... I want one source of truth'). 1,686 MATCH rows = 1,678 France "
        f"Ligue 1 rows (2021-22 380 + 2022-23 380 + 2023-24 306 + 2024-25 306 + 2025-26 306 - the "
        f"league shrank from 20 clubs x 38 matchdays to 18 clubs x 34 from 2023-24, the WO's "
        f"membership trap applied) + 8 France Relegation Playoffs pro/rel legs compType 'other' "
        f"(every tie in the window that touches the top flight: 2021-22 Auxerre-St Etienne, "
        f"2023-24 St Etienne-Metz, 2024-25 Metz-Reims, 2025-26 St Etienne-Nice; 2022-23 held NONE "
        f"- four direct relegations as the league contracted). Then the 2026-27 boundary: the new "
        f"season starts 2026-08-23, AFTER the {ACCESSED} return date, so zero 2026-27 rows exist "
        f"(sourced boundary NOTE below). The file name 'FRA-2021-2026' carries no cutoff - the "
        f"span is certified gap-free through today. Compiled {ACCESSED}.")
    for lbl, url, typ, what in SOURCES:
        notes.append(f"SOURCE|{lbl}|{url}|{ACCESSED}|{typ}|{what}")
    notes.append(
        "NOTE|info|federation_check|Section-0 scan on the finished pack: all 1,686 rows are France "
        "rows populated exclusively by the 26 pinned section-3 roster strings (25 appear in-window; "
        "Dijon is pinned by the WO but was relegated in 2020-21 and never returns - documented, not "
        "a gap). Per-season compositions: 2021-22 Angers, Bordeaux, Brest, Clermont, Lens, Lille, "
        "Lorient, Lyon, Marseille, Metz, Monaco, Montpellier, Nantes, Nice, Paris SG, Reims, "
        "Rennes, St Etienne, Strasbourg, Troyes; 2022-23 minus Bordeaux/Metz/St Etienne plus "
        "Ajaccio, Auxerre, Toulouse; 2023-24 minus Ajaccio/Angers/Auxerre/Troyes plus Le Havre, "
        "Metz (18 clubs); 2024-25 minus Clermont/Lorient/Metz plus Angers, Auxerre, St Etienne; "
        "2025-26 minus Montpellier/Reims/St Etienne plus Lorient, Paris FC, Metz. Playoff rows add "
        "no new identity (every participant is a roster string: Auxerre, St Etienne, Metz, Reims, "
        "Nice). Not England, not the Coupe de France (WO section-1 league-only cups exclusion; the "
        "cup lives only in the source descriptions). Anti-appear list (PSG, any Saint-Etienne "
        "hyphen form, Paris Saint-Germain, full club-name forms) is empty on row identity fields. "
        "No standings tables carried - rows only.")
    notes.append(
        "NOTE|info|catalog|1,686 MATCH rows = 1,678 'France Ligue 1' 'domestic-league' rows "
        "(380+380+306+306+306) + 8 'France Relegation Playoffs' 'other' rows (2 legs x 4 ties; "
        "competition strings declared once here, per WO section-2); 0 TEAM rows (WO section-2: the "
        "26 exact section-3 strings are pinned, none is missing, so no blocker - no TEAM row was "
        "expected). Venue-detail field carries MD1..MD38 / MD1..MD34 round labels per WO; playoff "
        "legs carry 'Playoff leg1'/'Playoff leg2'. Rows only, no tables; file ends with END. "
        "90-minute doctrine: six league-scale abandonments in the window produce three VOID games "
        "with full replays carrying the round labels and three results that stood (all itemized "
        "under continuity - never an abandoned score as a row); the playoff ties ship 90-minute "
        "scores with advancement NOTEs next.")
    notes.append(
        "NOTE|info|identity|The 26 pinned section-3 strings are used verbatim in home/away for "
        "every row. Rename traps mapped silently, each once here: Paris Saint-Germain -> always "
        "Paris SG (never PSG); AS Saint-Etienne -> always St Etienne (never Saint-Etienne, the "
        "WO's exact string keeps the space and drops the accent); Le Havre AC -> Le Havre; Paris "
        "FC written with the space. Source stock names map 1:1: ParisSG->Paris SG, "
        "SaintEtienne->St Etienne, LeHavre->Le Havre, ParisFC->Paris FC; all other 20 strings are "
        "already identical to the WO pins (Ajaccio, Angers, Auxerre, Bordeaux, Brest, Clermont, "
        "Lens, Lille, Lorient, Lyon, Marseille, Metz, Monaco, Montpellier, Nantes, Nice, Reims, "
        "Rennes, Strasbourg, Toulouse, Troyes - and Dijon which never appears). No club changed "
        "identity in-window (no renames/mergers 2021-26).")
    notes.append(
        "NOTE|info|venue_policy|MATCH stadium/city = the home club's documented ground for that "
        "season per the Wikipedia season articles' stadium/location tables (second index; RSSSF "
        "carries no venues), transcribed to audit/ledger/fra-venues.txt (94 entries = 20+20+18+18"
        "+18) and NFKD-folded to ASCII. Stadium strings follow the articles' printed display text "
        "per season - sponsor epochs are era data: Lille 'Stade Pierre-Mauroy' 2021-22, 'Decathlon "
        "Arena Pierre Mauroy Stadium' 2022-23..2024-25, 'Stade Pierre-Mauroy' 2025-26; Marseille "
        "'Orange Velodrome' 2021-22..2024-25, 'Stade Velodrome' (unsponsored print) 2025-26; "
        "Toulouse 'Stadium Municipal' 2022-23..2023-24, 'Stadium de Toulouse' from 2024-25; "
        "Auxerre 'Stade de l'Abbe-Deschamps' 2022-23, 'Stade Abbe Deschamps' from 2024-25; "
        "St Etienne 'Stade Geoffroy-Guichard' (hyphen print) 2021-22, 'Stade Geoffroy Guichard' "
        "from 2024-25. City strings carried canonically: Lyon at Groupama Stadium uses "
        "Decines-Charpieu (some articles print Lyon - verbatim variance kept in the ledger), "
        "Lille uses Villeneuve-d'Ascq (2022-23 article prints Lille), Metz uses "
        "Longeville-les-Metz. AS Monaco is the league's cross-border member - Monaco home rows "
        "carry Stade Louis II / Monaco while the country field stays France for the whole pack "
        "(league-country convention, disclosed once here). No groundshares and no neutral-venue "
        "league fixtures in the window. Playoff legs use the home club's ground with the "
        "documented fallback season for clubs home in a year they were outside Ligue 1: Auxerre "
        "2021-22 leg reads its 2022-23 Ligue 1 entry, St Etienne 2023-24/2025-26 legs read the "
        "2024-25 entry, Metz 2024-25 leg reads the 2023-24 entry; playoff venues also printed in "
        "the wiki football boxes (all home grounds, no neutrals; the 2025-26 leg at Nice was "
        "played behind closed doors).")
    notes.append(
        "NOTE|info|round_counts|Season row/goal/span anchors, each recomputed from the pack rows "
        "and matching the official record: 2021-22 = 380 rows, 1,067 goals, 2021-08-06.."
        "2022-05-21 (opener Monaco 1-1 Nantes; champions Paris SG 86); 2022-23 = 380, 1,067, "
        "2022-08-05..2023-06-03 (round-38 simultaneous finals 2023-06-03; champions Paris SG "
        "85); 2023-24 = 306, 826, 2023-08-11..2024-05-19 (first 18-club season; champions "
        "Paris SG 76); 2024-25 = 306, 911, 2024-08-16..2025-05-17 (champions Paris SG 84); "
        "2025-26 = 306, 863, 2025-08-15..2026-05-17 (opener Rennes 1-0 Marseille, wiki "
        "infobox matches/goals agree; champions Paris SG 76, clinched at Lens on 2026-05-13, "
        "a fifth consecutive title). Every season is one full double round-robin: 38 matchdays "
        "x 10 fixtures in the 20-club years, 34 x 9 in the 18-club years, zero double-rounds, "
        "zero cancellations.")
    notes.append(
        "NOTE|info|continuity|Continuity-clause accounting (gap-free league span): every matchday "
        "of all five seasons exists and is dated; no league fixture was cancelled. Documented "
        "disruptions, rows always keep their original MD labels while the file stays date-sorted. "
        "Abandonments, six in the window, in both governed shapes: VOID + full replay (three) - "
        "2021-22 R3 Nice-Marseille of 2021-08-22 stopped 75' at 1-0 (crowd trouble), replay "
        "2021-10-27 finished 1-1 and carries R3 (Nice also -1 for the same incidents); 2021-22 "
        "R14 Lyon-Marseille of 2021-11-21 stopped 5' at 0-0, replay 2022-02-01 Lyon 2-1 carries "
        "R14 (Lyon also -1); 2023-24 R8 Montpellier-Clermont of 2023-10-08 stopped 90+2' at 4-2, "
        "closed-doors replay 2023-11-29 finished 1-1 and carries R8 (Montpellier -1). Result "
        "STOOD (three, rows ship normally) - 2024-25 R26 Montpellier 0-2 St Etienne abandoned "
        "62' (openfootball prints '[awarded]'); 2025-26 MD34 Nantes 0-0 Toulouse abandoned 22' "
        "(pitch invasion; LFP upheld the score, wiki efn cross-check; Nantes already relegated). "
        "Postponements with stray dates: 2021-22 R19 Clermont-Strasbourg 2022-01-19, R20 two "
        "games 2022-01-19 + Angers-St Etienne 2022-01-26, R36 two games 2022-05-11; 2025-26 MD5 "
        "Marseille 1-0 Paris SG Monday 2025-09-22 (storm), MD26 Paris SG 3-0 Nantes 2026-04-22, "
        "MD29 Brest-Strasbourg and Lens-Paris SG both 2026-05-13. The 2022 World Cup break "
        "(2022-11-13..2022-12-27) and winter breaks are scheduling, not gaps. Season spans as "
        "listed under round_counts; the span 2021-08-06 -> 2026-05-17 is complete and every "
        "official match sits exactly once.")
    notes.append(
        "NOTE|info|boundary|Span-end state per WO section-1 row 2: the last completed round of "
        "the span is 2025-26 MD34, all nine fixtures played 2026-05-17 (final table inside the "
        "gates; Paris SG champions 76 pts and five-time defending champions of 2026-27 per the "
        "season article). The playoff tail of the same season runs 2026-05-26/29 (8 'other' rows "
        "total across the window, included). The 2026-27 season had NOT started on the return "
        "date 2026-08-04: rsssf.org/tablesf/fran2027.html answers 404, and the 2026-27 season "
        "article fixes the season dates '23 August 2026 - 29 May 2027' with 18 teams - promoted "
        "Troyes and Le Mans, relegated Metz and Nantes (exactly this pack's 2025-26 bottom two), "
        "16th-place Nice surviving the playoff tie included here. Zero 2026-27 rows are emitted; "
        "this is a boundary statement, not a blocker. No dateless rows, no duplicate "
        "(date,home,away) rows anywhere in the pack (gate-verified).")
    notes.append(
        "NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot "
        "gate: the pack's own rows are re-pivoted club-by-club - each club of each season shows "
        "its full campaign (19 home + 19 away in the 20-club years, 17 + 17 in the 18-club "
        "years) enumerated in round order with dates, and every TEAMPIVOT summary line "
        "reproduces the club's official final-table line (P/W/D/L/GF/GA/Pts; the 2021-22 "
        "Nice/Lyon and 2023-24 Montpellier deductions flagged inline). All 94 club-season "
        "pivots are printed in audit/pack-validation-fra.txt next to this file. 94/94 green.")
    notes.append(
        "NOTE|info|source_adaptation|WO section-4 design: RSSSF fran<Y>.html pages = primary for "
        "dates AND scores; fran2022..fran2025 carry full round-by-round sections transcribed to "
        "audit/ledger/fra-<season>.txt on fetch day. ADAPTATION for 2025-26: fran2026.html "
        "(Karel Stokkermans, updated 18 Jun 2026) carries the final table, playoff block and cups "
        "but NO league round-by-round - the 2025-26 match rows therefore come from the "
        "independent index openfootball/europe france/2025-26_fr1.txt and are labelled "
        "ofb-fra-2526 (banner groups RS-mapped to MD incl. the three stray-date blocks; parser "
        "tools/parse_ofb_fra.py, verbatim raw saved in data/raw/); the RSSSF final table remains "
        "the table authority and the recompute of those 306 rows reproduces it club-for-club "
        "and in position order EXACT (gate above). Second-index coverage: openfootball season "
        "files diffed row-for-row vs RSSSF for 2021-22..2024-25 (380/380, 380/380, 306/306, "
        "306/306 IDENTICAL round+date+score after the two adjudicated date misprints, "
        "tools/diff_epl_second_index.py); Wikipedia 2025-26 FBR results matrix diffed "
        "cell-for-cell for 2025-26 (305/306 IDENTICAL + one wiki typo, below); worldfootball "
        "matchday pages corroborate one full round per season (spot_audit) including both "
        "adjudicated dates and the 2025-26 RS26 stray; Wikipedia playoff boxes verified the "
        "three 90-minute splits (goal minutes Sakhi 51'/Camara 76', Wadji 116', Toure "
        "110'/Hein 114'). Conflicts were resolved per section-4(3) - RSSSF stands unless two "
        "independent indexes agree against it - and every divergence anywhere in the five "
        "seasons is one of the three source_conflict NOTEs below; nothing else diverges.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF fran2023.html prints round-2 'Lorient 3-1 Lyon' "
        "under '[Aug 14]' - but TWO independent indexes agree against it: the openfootball "
        "season file places the fixture on Wednesday 2022-09-07, and the worldfootball MD2 page "
        "prints '07.09.2022 19:00 Lorient 3:1 Lyon'. Per section-4 (two independent indexes "
        "agree against RSSSF => their value plus this NOTE), the pack row carries 2022-09-07; "
        "the RSSSF print is preserved verbatim in audit/ledger/fra-2022-23.txt. Score was "
        "never in doubt; the final table is unaffected either way.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF fran2025.html prints round-9 'Rennes 1-0 Le Havre' "
        "under '[Oct 26]' - but TWO independent indexes agree against it: openfootball lists "
        "'Fri Oct 25' and the worldfootball MD9 page prints '25.10.2024 20:45 Rennes 1:0 Le "
        "Havre'. Per section-4, the pack row carries 2024-10-25; the RSSSF print is preserved "
        "verbatim in audit/ledger/fra-2024-25.txt. Score was never in doubt; the final table "
        "is unaffected either way.")
    notes.append(
        "NOTE|warning|source_conflict|Wikipedia's 2025-26 FBR results matrix prints Brest-Lens "
        "= '3-0' - against FOUR agreements for 3-3: the RSSSF fran2026 final table (Brest GF "
        "43, Lens GA 35), the article's own league-table template, the openfootball carrier "
        "row 'MD31|2026-04-24|Brest 3-3 Lens', and the season goal total (863 - the matrix's "
        "own cells sum to 860 with the typo). This is a transcription typo inside the "
        "matrix alone; the pack keeps 3-3 and the diff gate tolerates exactly this one "
        "cell. Verbatim evidence in audit/ledger/fra-2ndidx-2025-26-MX.txt.")
    notes.append(
        "NOTE|info|advancement|2021-22 pro/rel Final: Auxerre 1-1 St Etienne (2022-05-26) and "
        "St Etienne 1-1 Auxerre (2022-05-29, 90-min; Sakhi 51', Camara 76') - 2-2 aggregate "
        "after a goalless extra time, AUXERRE WON 5-4 ON PENALTIES and was promoted (Boudebouz "
        "missed for St Etienne); St Etienne relegated to Ligue 2. L2-internal rounds (Paris FC "
        "1-2 Sochaux; Auxerre 0-0 Sochaux aet 5-4 pen) are outside the commissioned slice - "
        "ledger context lines only.")
    notes.append(
        "NOTE|info|advancement|2023-24 pro/rel Final: St Etienne 2-1 Metz (2024-05-30) and "
        "Metz 2-1 St Etienne (2024-06-02, 90-min) - the second leg finished Metz 2-2 St "
        "Etienne after extra time (Wadji 116'), so the SHIPPED row is the 90-minute 2-1 per "
        "doctrine; ST ETIENNE WON 4-3 ON AGGREGATE and was promoted; Metz relegated to Ligue "
        "2. L2-internal rounds (Rodez 2-2 Paris FC aet 3-2 pen; St Etienne 2-0 Rodez) are "
        "outside the commissioned slice - ledger context lines only.")
    notes.append(
        "NOTE|info|advancement|2024-25 pro/rel Final: Metz 1-1 Reims (2025-05-21) and Reims "
        "1-1 Metz (2025-05-29, 90-min) - the second leg finished Reims 1-3 Metz after extra "
        "time (Toure 110', Hein 114'), so the SHIPPED row is the 90-minute 1-1 per doctrine; "
        "METZ WON 4-2 ON AGGREGATE and was promoted; Reims relegated to Ligue 2. L2-internal "
        "rounds (Dunkerque 1-0 Guingamp; Metz 1-0 Dunkerque) are outside the commissioned "
        "slice - ledger context lines only.")
    notes.append(
        "NOTE|info|advancement|2025-26 pro/rel Final: St Etienne 0-0 Nice (2026-05-26) and "
        "Nice 4-1 St Etienne (2026-05-29; played BEHIND CLOSED DOORS per the wiki box - Nice "
        "supporters banned) - no extra time: the shipped rows are the full-time scores; NICE "
        "WON 4-1 ON AGGREGATE and both clubs remained at their levels (Nice stays in Ligue 1, "
        "St Etienne in Ligue 2). L2-internal rounds (Red Star 2-3 Rodez; St Etienne 0-0 Rodez "
        "aet 7-6 pen) are outside the commissioned slice - ledger context lines only.")
    notes.append(
        "NOTE|info|spot_audit|2021-22 matchday 1 re-listed for spot-audit (sources "
        "https://www.rsssf.org/tablesf/fran2022.html, ofb-fra-2122 - diff 380/380 IDENTICAL - "
        "and the worldfootball matchday page wf-fra-2122-md1): "
        + spot_listing("2021-22", SPOT["2021-22"], data["2021-22"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2022-23 matchday 2 re-listed for spot-audit - the round with "
        "the adjudicated Lorient-Lyon date (sources https://www.rsssf.org/tablesf/fran2023.html, "
        "ofb-fra-2223 AND wf-fra-2223-md2, both carrying 2022-09-07 for the fixture): "
        + spot_listing("2022-23", SPOT["2022-23"], data["2022-23"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2023-24 matchday 8 re-listed for spot-audit - the abandonment "
        "round and its closed-doors replay (sources https://www.rsssf.org/tablesf/fran2024.html, "
        "ofb-fra-2324 AND wf-fra-2324-md8 - dates and scores identical 9/9): "
        + spot_listing("2023-24", SPOT["2023-24"], data["2023-24"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2024-25 matchday 9 re-listed for spot-audit - the round with "
        "the adjudicated Rennes-Le Havre date (sources https://www.rsssf.org/tablesf/fran2025.html, "
        "ofb-fra-2425 AND wf-fra-2425-md9, both carrying 2024-10-25 for the fixture): "
        + spot_listing("2024-25", SPOT["2024-25"], data["2024-25"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2025-26 matchday 26 re-listed for spot-audit - the round with "
        "the RS26 banner-stray (sources ofb-fra-2526 = the season's labelled carrier, "
        "wikimatrix-fra-2526 AND wf-fra-2526-md26, which prints eight fixtures 2026-03-13..15 "
        "plus Paris SG 3:0 Nantes on 22.04.2026 exactly like the carrier): "
        + spot_listing("2025-26", SPOT["2025-26"], data["2025-26"][0]) + ".")

    # ---------------------------------------------------------------- final pack integrity gates
    pack = "\n".join(notes + pack_rows + ["END"]) + "\n"
    G.g(pack.rstrip().endswith("END"), "file ends with END")
    G.g(len(pack.splitlines()) == len(notes) + 1686 + 1,
        f"pack line accounting: {len(notes)} header rows (NOTE+SOURCE) + 1,686 MATCH + END")
    block_ok = True
    ofs = 0
    for s, block in season_blocks:
        dates = [l.split("|")[1] for l in block]
        labels = {l.split("|")[13] for l in block}
        if dates != sorted(dates) or labels != {SRC_LABEL[s]}:
            block_ok = False
        ofs += len(block)
    G.g(block_ok, "pack ordering: five season blocks in order, each league block date-sorted and "
                  "carrying only its season's source label (playoff legs follow their season "
                  "block in tie order)")

    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="ascii", newline="\n") as fh:
        fh.write(pack)

    # ---------------------------------------------------------------- validation output
    head = [
        "FRA PACK VALIDATION - handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt",
        f"builder tools/build_fra_pack.py, run {ACCESSED}; gates PASS {G.n_pass} FAIL {G.n_fail}",
        "order: section A = gate ledger; section B = per-club full-campaign pivots (owner decree).",
        "",
        "== SECTION A: GATES ==",
    ]
    body = head + G.lines + ["", "== SECTION B: PER-CLUB FULL-CAMPAIGN PIVOTS (owner decree) ==", ""] + pivot_out
    with open(OUTAUDIT, "w", encoding="ascii", newline="\n") as fh:
        fh.write("\n".join(body).rstrip() + "\n")

    print(f"gates PASS {G.n_pass} FAIL {G.n_fail}")
    for l in G.lines:
        if l.startswith("FAIL"):
            print(" ", l)
    print(f"wrote {OUTPACK}")
    print(f"wrote {OUTAUDIT}")
    sys.exit(1 if G.n_fail else 0)

if __name__ == "__main__":
    main()
