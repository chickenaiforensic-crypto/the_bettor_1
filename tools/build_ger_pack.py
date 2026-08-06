#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build + validate handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt (WO-GER-SPAN-15, returned 2026-08-05).

PRIMARY:  audit/ledger/ger-<season>.txt  (RSSSF tablesd/duit2022..duit2025.html: full round-by-round
          transcribed to R1..R34 rows + official FINAL TABLE constants as TABLE rows; duit2026.html
          prints NO 1.Bundesliga round-by-round (final table + playoffs + cups only, verified full
          page 2026-08-05), so the 2025-26 match rows are carried by openfootball/deutschland
          2025-26/1-bundesliga.txt and gated EXACT against the RSSSF table by full recompute -
          documented source_adaptation, same class as FRA 2025-26).
2NDIDX:   audit/ledger/ger-2ndidx-<season>.txt (openfootball MD rows 2021-22..2024-25, diffed
          row-for-row vs RSSSF: 306/306 IDENTICAL x4, tools/diff_ger_second_index.py) +
          audit/ledger/ger-2ndidx-2025-26-MX.txt (Wikipedia 2025-26 FBR matrix, 306 cells:
          306/306 IDENTICAL scores vs the carrier, 990 goals both, tools/diff_ger_matrix.py).
CONSTANTS audit/ledger/ger-venues.txt (96 VENUE rows = 90 per-season stadium/city lattice from the
          Wikipedia season articles + 5 playoff-year PO fallbacks + the Freiburg 2021-22
          Dreisamstadion/Europa-Park split-season footnote).
PLAYOFFS  PO_PLAYOFF lines in the five ledgers: the 1./2. Final legs SHIP as compType 'other'
          (ERRATA-2026-08-03 + DECREE-2026-08-04 owner override; the WO text 'Relegation playoff
          exists but is OUT of this order' is superseded - documented tension NOTE; mirrors
          RPL/CZ1/MOLCUP/FRA). The 2./3. legs stay NOT-COMMISSIONED context. 90-minute doctrine:
          aet/ET legs ship the 90-min score (goal-minute verified in the wiki playoff boxes),
          advancement in pack NOTEs.
Output:   handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt  +  audit/pack-validation-ger.txt
Run:      python3 tools/build_ger_pack.py   (exit 0 iff every gate PASS; rebuild is deterministic)
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")
OUTPACK = os.path.join(ROOT, "handoffs", "GER-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation-ger.txt")
ACCESSED = "2026-08-05"
SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
COMP = "Germany Bundesliga"                # WO section-2 verbatim
COMPTYPE = "domestic-league"               # WO section-2 verbatim
COMP_PO = "Germany Relegation Playoffs"    # mirrors CZ1's "Czech Relegation Playoffs"
COMPTYPE_PO = "other"                      # ERRATA-2026-08-03
COUNTRY = "Germany"
SRC_LABEL = {"2021-22": "rsssf-duit2022", "2022-23": "rsssf-duit2023", "2023-24": "rsssf-duit2024",
             "2024-25": "rsssf-duit2025", "2025-26": "ofb-ger-2526"}
PO_LABEL = {"2025-26": "rsssf-duit2026"}   # all other PO seasons label like their season
# 18 clubs x 34 matchdays x 9 fixtures, every season (WO section-1: NOT 20/38)
SHAPE = {s: (18, 34, 9) for s in SEASONS}
EXP_ROWS = {s: 306 for s in SEASONS}
DEDUCT = {}                                # no point deductions anywhere in the window
ANCHORS = {"2021-22": (306, 954, ("2021-08-13", "2022-05-14")),
           "2022-23": (306, 971, ("2022-08-05", "2023-05-27")),
           "2023-24": (306, 985, ("2023-08-18", "2024-05-18")),
           "2024-25": (306, 959, ("2024-08-23", "2025-05-17")),
           "2025-26": (306, 990, ("2025-08-22", "2026-05-16"))}
SPOT = {"2021-22": 27, "2022-23": 34, "2023-24": 13, "2024-25": 14, "2025-26": 17}
FREIBURG_SPLIT = {"2021-22": {2, 4, 6}}    # first three home matches at Dreisamstadion

# ------------------------------------------------------------- identity (WO section-3)
ROSTER25 = ["Augsburg", "Bayern Munich", "Bielefeld", "Bochum", "Darmstadt", "Dortmund",
            "Ein Frankfurt", "FC Koln", "Freiburg", "Greuther Furth", "Hamburg", "Heidenheim",
            "Hertha", "Hoffenheim", "Holstein Kiel", "Leverkusen", "M'gladbach", "Mainz",
            "RB Leipzig", "Schalke 04", "St Pauli", "Stuttgart", "Union Berlin", "Werder Bremen",
            "Wolfsburg"]
ROSTER_SET = set(ROSTER25)
# ERRATA-shipped playoff legs introduce three 2.-Bundesliga participants outside the section-3
# pins; their packs-side identities are registered with TEAM rows (ASCII-canonical forms; the
# umlaut print kept as alias, mirroring the venue ledger's ASCII-fold convention).
PO_TEAMS = [  # name, league-desc, code, otherNames (ASCII aliases only), stadium, city
    ("Fortuna Dusseldorf", "2. Bundesliga", "GER2", "Fortuna Duesseldorf;Fortuna Dusseldorf",
     "Merkur Spiel-Arena", "Dusseldorf"),
    ("SC Paderborn", "2. Bundesliga", "GER2", "SC Paderborn 07;SC Paderborn",
     "Home Deluxe Arena", "Paderborn"),
    ("SV Elversberg", "2. Bundesliga", "GER2", "SV 07 Elversberg;SV Elversberg",
     "Waldstadion an der Kaiserlinde", "Spiesen-Elversberg"),
]
PO_TEAM_SET = {t[0] for t in PO_TEAMS}
IDENTITY_DOMAIN = ROSTER_SET | PO_TEAM_SET
ANTI_APPEAR = ["Eintracht Frankfurt", "FC Köln", "FC Koeln", "Borussia", "Mönchengladbach",
               "Moenchengladbach", "St. Pauli", "Hertha BSC", "Bayern München"]
STOCK2ROSTER = {"Bayern": "Bayern Munich", "Frankfurt": "Ein Frankfurt", "FCKoln": "FC Koln",
                "GreutherFurth": "Greuther Furth", "HolsteinKiel": "Holstein Kiel",
                "Mgladbach": "M'gladbach", "RBLeipzig": "RB Leipzig", "Schalke04": "Schalke 04",
                "StPauli": "St Pauli", "UnionBerlin": "Union Berlin", "WerderBremen": "Werder Bremen",
                "FortunaDusseldorf": "Fortuna Dusseldorf", "Elversberg": "SV Elversberg",
                "SCPaderborn": "SC Paderborn"}
# league stocks (ledger TABLE/R club ids) -> roster strings; the three PO stocks are not league data
LEAGUE_STOCKS = {"Augsburg", "Bayern", "Bielefeld", "Bochum", "Darmstadt", "Dortmund", "FCKoln",
                 "Frankfurt", "Freiburg", "GreutherFurth", "Hamburg", "Heidenheim", "Hertha",
                 "Hoffenheim", "HolsteinKiel", "Leverkusen", "Mainz", "Mgladbach", "RBLeipzig",
                 "Schalke04", "StPauli", "Stuttgart", "UnionBerlin", "WerderBremen", "Wolfsburg"}

def roster(stock):
    return STOCK2ROSTER.get(stock, stock)

SOURCES = [
 ("rsssf-duit2022", "https://www.rsssf.org/tablesd/duit2022.html", "primary-archive",
  "2021-22: all 34 rounds dates+scores (round-27 Bochum 0-2 M'gladbach abandoned 70' with the "
  "RESULT STANDING = awarded 0-2, RSSSF in-line annotation kept verbatim in the raw; the "
  "round-23 '[Feb 21]' three-fixture misprint cluster documented under source_conflict), official "
  "final table, pro/rel playoff block; transcribed in audit/ledger/ger-2021-22.txt; anchors 306 "
  "rows / 954 goals / span 2021-08-13..2022-05-14"),
 ("rsssf-duit2023", "https://www.rsssf.org/tablesd/duit2023.html", "primary-archive",
  "2022-23: all 34 rounds dates+scores + official final table (16th Stuttgart survived the "
  "playoff; Hertha/Schalke relegated direct), pro/rel playoff block; the page's Halfway Table "
  "context block is skipped by the parser; audit/ledger/ger-2022-23.txt; anchors 306 / 971 / "
  "2022-08-05..2023-05-27"),
 ("rsssf-duit2024", "https://www.rsssf.org/tablesd/duit2024.html", "primary-archive",
  "2023-24: all 34 rounds dates+scores (the round-1 '[Aug 21]' two-fixture misprint cluster "
  "documented under source_conflict), official final table (Leverkusen's first title, unbeaten "
  "28-6-0), pro/rel playoff block; a transcription seam-drop (round-19 '[Feb 3] "
  "Augsburg 1-0 Leverkusen') was repaired in the raw on fetch day and is documented in the "
  "ledger header - raw now round-complete; audit/ledger/ger-2023-24.txt; anchors 306 / 985 / "
  "2023-08-18..2024-05-18"),
 ("rsssf-duit2025", "https://www.rsssf.org/tablesd/duit2025.html", "primary-archive",
  "2024-25: all 34 rounds dates+scores (round-14 Union AWD Bochum: originally 1-1, awarded 0-2 "
  "- keeper Patrick Drewes hit by a lighter; openfootball prints '0-2 [awarded]'), official "
  "final table, pro/rel playoff block; audit/ledger/ger-2024-25.txt; anchors 306 / 959 / "
  "2024-08-23..2025-05-17"),
 ("rsssf-duit2026", "https://www.rsssf.org/tablesd/duit2026.html", "primary-archive",
  "2025-26: OFFICIAL FINAL TABLE + pro/rel playoff + 2. Bundesliga table and cups - but NO "
  "1.Bundesliga round-by-round (verified full page 2026-08-05; an interim GARBLED revision was "
  "briefly served on first fetch, self-healed on re-fetch, quarantined as a disclosed anomaly - "
  "never a data source); final-table authority for the season: the recompute of the pack's 306 "
  "rows reproduces it club-for-club and in position order EXACT; constants transcribed in "
  "audit/ledger/ger-2025-26.txt; also the playoff-leg source for 2025-26 (the aet print whose "
  "90-minute split was verified against the wiki match box)"),
 ("rsssf-duit2027", "https://www.rsssf.org/tablesd/duit2027.html", "primary-archive",
  "404 Not Found on 2026-08-05 - boundary evidence that no 2026-27 season page (and no played "
  "2026-27 fixture) existed on the return date"),
 ("ofb-ger-2526", "https://raw.githubusercontent.com/openfootball/deutschland/master/2025-26/1-bundesliga.txt",
  "match-carrier",
  "2025-26 match rows (306 fixtures: format B 'Regular Season - n' banners mapped to MD1..MD34, "
  "duplicate-banner makeup blocks RS16 (Werder 0-2 Hoffenheim + St Pauli 1-1 RB Leipzig Tue "
  "2026-01-27) and RS17 (Hamburger SV 0-1 Bayer Leverkusen Wed 2026-03-04) summed under their "
  "banner numbers; scorer lines skipped by the parser; header '# Matches 306', dates Fri Aug 22 "
  "2025 - Sat May 16 2026, fetched 2026-08-05) - the season's date/score carrier under the "
  "documented source_adaptation; label carried on all 2025-26 league MATCH rows"),
 ("ofb-ger-2122", "https://raw.githubusercontent.com/openfootball/deutschland/master/2021-22/1-bundesliga.txt",
  "second-index", "306 matchday-grouped rows diffed vs the RSSSF rows: 306/306 IDENTICAL on "
  "round + date + score after adjudicating the RSSSF round-23 '[Feb 21]' misprint cluster "
  "(three Sunday fixtures 2022-02-20, two independents agree - see source_conflict NOTEs); "
  "includes the MD25 makeup Mainz 0-1 Dortmund Wed 2022-03-16 and MD26 "
  "makeup Augsburg 2-1 Mainz Wed 2022-04-06 summed under their banner numbers); "
  "audit/ledger/ger-2ndidx-2021-22.txt, tools/diff_ger_second_index.py"),
 ("ofb-ger-2223", "https://raw.githubusercontent.com/openfootball/deutschland/master/2022-23/1-bundesliga.txt",
  "second-index", "306 rows diffed: 306/306 IDENTICAL round + date + score "
  "(audit/ledger/ger-2ndidx-2022-23.txt)"),
 ("ofb-ger-2324", "https://raw.githubusercontent.com/openfootball/deutschland/master/2023-24/1-bundesliga.txt",
  "second-index", "306 rows diffed: 306/306 IDENTICAL round + date + score after adjudicating "
  "the RSSSF round-1 '[Aug 21]' misprint cluster (two Sunday fixtures 2023-08-20, two "
  "independents agree - see source_conflict NOTEs); includes the MD13 "
  "makeup Bayern 1-0 Union Wed 2024-01-24 and MD18 makeup Mainz 1-1 Union Wed 2024-02-07; "
  "audit/ledger/ger-2ndidx-2023-24.txt"),
 ("ofb-ger-2425", "https://raw.githubusercontent.com/openfootball/deutschland/master/2024-25/1-bundesliga.txt",
  "second-index", "306 rows diffed: 306/306 IDENTICAL round + date + score; this file prints the "
  "MD14 Union-Bochum fixture '0-2 [awarded]' corroborating the RSSSF awarded print; "
  "audit/ledger/ger-2ndidx-2024-25.txt"),
 ("wikimatrix-ger-2526", "https://en.wikipedia.org/wiki/2025%E2%80%9326_Bundesliga", "second-index",
  "Results FBR matrix (306 cells, source line: Bundesliga/bundesliga.com; article chunks 5-6 "
  "transcription) diffed vs the 2025-26 carrier rows: 306/306 IDENTICAL scores, goals 990 both "
  "(tools/diff_ger_matrix.py); the article's league table matches the RSSSF table club-for-club "
  "and its playoff boxes fixed the 90-minute split of the 2025-26 leg-2 (90-min = 1-1: "
  "Pejcinovic 3' + Bilbija 38', ET winner Curda 100') (audit/ledger/ger-2ndidx-2025-26-MX.txt)"),
 ("wiki-ger-venues", "https://en.wikipedia.org/wiki/2021%E2%80%9322_Bundesliga", "second-index",
  "stadium/location tables of the five season articles 2021-22..2025-26 (sibling pages "
  "...%E2%80%9322 through ...%E2%80%9326_Bundesliga; fetched 2026-08-05): 96 venue rows = the "
  "stadium/city constants in audit/ledger/ger-venues.txt (90-season lattice + Freiburg's 2021-22 "
  "split-season footnote 'first three home matches at the Dreisamstadion' + 5 playoff fallback "
  "grounds); each article's league table matches the RSSSF table club-for-club 18/18; playoff "
  "boxes verified all five ties' 90-minute splits (2023-24 ET goalless Hofmann 18'/66' Stoeger "
  "70'(p) -> leg2 ships 0-3; 2024-25 winner Scienza 90+5' still regulation -> leg2 ships 1-2; "
  "2025-26 Curda 100' -> leg2 ships 1-1); tie-break rule print 'points, goal difference, goals "
  "scored, head-to-head results, head-to-head away goals, away goals, play-off'"),
 ("wiki-ger-2627", "https://en.wikipedia.org/wiki/2026%E2%80%9327_Bundesliga", "second-index",
  "span-end boundary: 2026-27 season dates 28 August 2026 - 22 May 2027, 18 teams; promoted "
  "Schalke 04 (return after three years), SV Elversberg (Bundesliga debut, 59th club in the "
  "division) and SC Paderborn (playoff winners, return after six years); relegated VfL "
  "Wolfsburg (via the playoff), 1. FC Heidenheim and FC St. Pauli - exactly this pack's 2025-26 "
  "relegation places; the season had NOT started on the return date 2026-08-05"),
 ("wf-ger-2122-md27", "https://www.worldfootball.net/schedule/bundesliga-2021-2022-spieltag/27/",
  "second-index", "2021-22 matchday-27 spot-audit page: dates and scores match the pack rows "
  "one-for-one incl. Bochum 0:2 Borussia M'gladbach marked 'dec.' (decided/awarded)"),
 ("wf-ger-2122-md23", "https://www.worldfootball.net/schedule/bundesliga-2021-2022-spieltag/23/",
  "second-index", "2021-22 matchday-23 adjudication page: prints Bayern 4:1 Greuther Fuerth "
  "20.02.2022 15:30, Dortmund 6:0 M'gladbach 20.02.2022 17:30 and Hertha 1:6 RB Leipzig "
  "20.02.2022 19:30 - one of the two independent indexes adjudicating the RSSSF '[Feb 21]' "
  "misprint cluster (20.02.2022 was the Sunday; 21.02 a fixtureless Monday)"),
 ("wf-ger-2223-md34", "https://www.worldfootball.net/schedule/bundesliga-2022-2023-spieltag/34/",
  "second-index", "2022-23 matchday-34 spot-audit page (simultaneous final round 2023-05-27): "
  "dates and scores match the pack rows one-for-one"),
 ("wf-ger-2324-md1", "https://www.worldfootball.net/schedule/bundesliga-2023-2024-spieltag/1/",
  "second-index", "2023-24 matchday-1 adjudication page: prints Union Berlin 4:1 Mainz "
  "20.08.2023 15:30 and Eintracht Frankfurt 1:0 Darmstadt 20.08.2023 17:30 - one of the two "
  "independent indexes adjudicating the RSSSF '[Aug 21]' misprint cluster (20.08.2023 was the "
  "Sunday; 21.08 a fixtureless Monday)"),
 ("wf-ger-2324-md13", "https://www.worldfootball.net/schedule/bundesliga-2023-2024-spieltag/13/",
  "second-index", "2023-24 matchday-13 spot-audit page: eight fixtures dated 2023-12-01..03 "
  "plus the postponed Bayern 1:0 Union Berlin dated 24.01.2024 20:30 - matches the pack rows "
  "one-for-one"),
 ("wf-ger-2425-md14", "https://www.worldfootball.net/schedule/bundesliga-2024-2025-spieltag/14/",
  "second-index", "2024-25 matchday-14 spot-audit page: dates and scores match the pack rows "
  "one-for-one incl. Union 0:2 Bochum marked 'dec.' (awarded)"),
 ("wf-ger-2526-md17", "https://www.worldfootball.net/schedule/bundesliga-2025-2026-spieltag/17/",
  "second-index", "2025-26 matchday-17 spot-audit page: eight fixtures dated 2026-01-13..15 (a mid-week "
  "round) plus the Hamburger SV fixture dated 04.03.2026 - corroborates the carrier's RS17 banner-"
  "stray mapping one-for-one"),
]

# ---------------------------------------------------------------- readers
R_RX = re.compile(r"^R(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MD_RX = re.compile(r"^MD(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MX_RX = re.compile(r"^MX\|([^|]+)\|([^|]+)\|(\d+)\|(\d+)$")
PO_RX = re.compile(r"^PO_PLAYOFF\|([^|]+)\|([^|]+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)\|([^|]*)\|(.*)$")

def read_season(season):
    """League rows + official table + playoff context, from the five primary ledgers.
    2025-26 is the source_adaptation season: duit2026 prints no 1.BL rounds, so the
    306 carrier rows are read from the openfootball second-index ledger (MD rows)."""
    rows, table, po = [], [], []
    with open(os.path.join(LEDGER, f"ger-{season}.txt"), encoding="utf-8") as fh:
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
    if season == "2025-26":
        with open(os.path.join(LEDGER, "ger-2ndidx-2025-26.txt"), encoding="utf-8") as fh:
            for ln in fh:
                m = MD_RX.match(ln.strip())
                if m:
                    rows.append({"rnd": int(m.group(1)), "date": m.group(2), "home": m.group(3).strip(),
                                 "hg": int(m.group(4)), "ag": int(m.group(5)), "away": m.group(6).strip()})
    return rows, table, po

def read_venues():
    """(season, stock) -> (stadium, city); the Freiburg 2021-22 SPLIT footnote line is held
    separately so the lattice entry stays the Europa-Park base."""
    ven, split = {}, {}
    nlines = 0
    with open(os.path.join(LEDGER, "ger-venues.txt"), encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("VENUE|"):
                nlines += 1
                p = ln.rstrip("\n").split("|")
                if p[6].startswith("SPLIT"):
                    split[(p[1], p[2])] = (p[3], p[4])
                else:
                    ven[(p[1], p[2])] = (p[3], p[4])
    return ven, split, nlines

def read_2ndidx_md(season):
    out = {}
    with open(os.path.join(LEDGER, f"ger-2ndidx-{season}.txt"), encoding="utf-8") as fh:
        for ln in fh:
            m = MD_RX.match(ln.strip())
            if m:
                out[(m.group(3).strip(), m.group(6).strip())] = (int(m.group(1)), m.group(2),
                                                                 int(m.group(4)), int(m.group(5)))
    return out

def read_2ndidx_mx():
    out = {}
    with open(os.path.join(LEDGER, "ger-2ndidx-2025-26-MX.txt"), encoding="utf-8") as fh:
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

def emit_match(season, r, ven, split):
    h, a = roster(r["home"]), roster(r["away"])
    key = (season, r["home"])
    if season in FREIBURG_SPLIT and r["home"] == "Freiburg" and r["rnd"] in FREIBURG_SPLIT[season]:
        stadium, city = split[key]
    else:
        stadium, city = ven[key]
    return (f"MATCH|{r['date']}|{COMP}|{COMPTYPE}|{h}|{r['hg']}|{r['ag']}|{a}|MD{r['rnd']}|"
            f"{stadium}|{city}|{COUNTRY}||{SRC_LABEL[season]}")

# SHIP-as-other playoff legs, 90-minute doctrine applied (verified against the wiki playoff boxes'
# goal minutes 2026-08-05 + RSSSF playoff blocks). Tuple:
# (season, date, home, hg90, ag90, away, venueDetail, stadium, city, sourceLabel, aetFinal-or-None)
PO_SHIP = [
 ("2021-22", "2022-05-19", "Hertha", 0, 1, "Hamburg", "Playoff leg1",
  "Olympiastadion", "Berlin", "rsssf-duit2022", None),
 ("2021-22", "2022-05-23", "Hamburg", 0, 2, "Hertha", "Playoff leg2",
  "Volksparkstadion", "Hamburg", "rsssf-duit2022", None),
 ("2022-23", "2023-06-01", "Stuttgart", 3, 0, "Hamburg", "Playoff leg1",
  "Mercedes-Benz Arena", "Stuttgart", "rsssf-duit2023", None),
 ("2022-23", "2023-06-05", "Hamburg", 1, 3, "Stuttgart", "Playoff leg2",
  "Volksparkstadion", "Hamburg", "rsssf-duit2023", None),
 ("2023-24", "2024-05-23", "Bochum", 0, 3, "FortunaDusseldorf", "Playoff leg1",
  "Vonovia Ruhrstadion", "Bochum", "rsssf-duit2024", None),
 ("2023-24", "2024-05-27", "FortunaDusseldorf", 0, 3, "Bochum", "Playoff leg2",
  "Merkur Spiel-Arena", "Dusseldorf", "rsssf-duit2024", (3, 3)),
 ("2024-25", "2025-05-22", "Heidenheim", 2, 2, "Elversberg", "Playoff leg1",
  "Voith-Arena", "Heidenheim", "rsssf-duit2025", None),
 ("2024-25", "2025-05-26", "Elversberg", 1, 2, "Heidenheim", "Playoff leg2",
  "Waldstadion an der Kaiserlinde", "Spiesen-Elversberg", "rsssf-duit2025", None),
 ("2025-26", "2026-05-21", "Wolfsburg", 0, 0, "SCPaderborn", "Playoff leg1",
  "Volkswagen Arena", "Wolfsburg", "rsssf-duit2026", None),
 ("2025-26", "2026-05-25", "SCPaderborn", 1, 1, "Wolfsburg", "Playoff leg2",
  "Home Deluxe Arena", "Paderborn", "rsssf-duit2026", (2, 1)),
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
    ven, ven_split, ven_lines = read_venues()
    data = {}
    for s in SEASONS:
        data[s] = read_season(s)

    G = Gates()
    pack_rows = []
    season_blocks = []   # (season, [league lines])

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
        h2h_gd = defaultdict(int)
        h2h_gf = defaultdict(int)
        for r in rows:
            if r["hg"] > r["ag"]:
                h2h_pts[(r["home"], r["away"])] += 3
            elif r["hg"] < r["ag"]:
                h2h_pts[(r["away"], r["home"])] += 3
            else:
                h2h_pts[(r["home"], r["away"])] += 1; h2h_pts[(r["away"], r["home"])] += 1
            h2h_gd[(r["home"], r["away"])] += r["hg"] - r["ag"]
            h2h_gd[(r["away"], r["home"])] += r["ag"] - r["hg"]
            h2h_gf[(r["home"], r["away"])] += r["hg"]
            h2h_gf[(r["away"], r["home"])] += r["ag"]
        for t in table:
            c = st[t["club"]]
            pts = c[1] * 3 + c[2] - ded.get(t["club"], 0)
            if [c[0], c[1], c[2], c[3], c[4], c[5], pts] != [t["P"], t["W"], t["D"], t["L"], t["GF"], t["GA"], t["Pts"]]:
                bad.append(t["club"])
            order.append((t["club"], pts, c[4] - c[5], c[4], t["pos"]))
        G.g(not bad, f"{s}: table reproduction club-for-club {nclubs}/{nclubs} (P/W/D/L/GF/GA/Pts"
                     + (f", deductions {ded}" if ded else ", no deductions in-window") + f") fails={bad or '-'}")
        # position order, Bundesliga rule depth (wiki print): 1 points, 2 overall GD, 3 goals
        # scored, 4 head-to-head points, 5 head-to-head away goals, 6 overall away goals,
        # 7 play-off. H2H steps apply only between clubs whose mutual meetings are complete;
        # the printed official position is accepted whenever the computed keys are level
        # (the sources' official prints are the authority at every such spot).
        h2h_away = defaultdict(int)
        for r in rows:
            h2h_away[(r["away"], r["home"])] += r["ag"]  # club's goals scored away in the pairing
        inv = []
        for i in range(len(order) - 1):
            (c1, p1, gd1, gf1, pos1), (c2, p2, gd2, gf2, pos2) = order[i], order[i + 1]
            if (p1, gd1, gf1) > (p2, gd2, gf2):
                continue  # steps 1-3 decide
            if (p1, gd1, gf1) == (p2, gd2, gf2):
                h1 = (h2h_pts.get((c1, c2), 0), h2h_away.get((c1, c2), 0))
                h2 = (h2h_pts.get((c2, c1), 0), h2h_away.get((c2, c1), 0))
                away1 = sum(r["ag"] for r in rows if r["away"] == c1)
                away2 = sum(r["ag"] for r in rows if r["away"] == c2)
                if (h1, away1) >= (h2, away2):
                    continue
            inv.append((c1, c2))
        G.g(not inv, f"{s}: final-table position order consistent (pts -> GD -> GF -> H2H pts -> "
                     f"H2H away goals -> overall away goals; printed order kept where computed keys "
                     f"are level) inversions={inv or '-'}")
        members = {t["club"] for t in table}
        G.g(len(members) == nclubs and members <= LEAGUE_STOCKS
            and all(roster(c) in ROSTER_SET for c in members),
            f"{s}: {nclubs} member clubs, every roster string in WO section-3 domain")
        goals = sum(r["hg"] + r["ag"] for r in rows)
        span = (min(r["date"] for r in rows), max(r["date"] for r in rows))
        want = ANCHORS[s]
        G.g((len(rows), goals, span) == (want[0], want[1], want[2]),
            f"{s}: anchors {want[0]} rows / {want[1]} goals / span {want[2][0]}..{want[2][1]} "
            f"(got {len(rows)}/{goals}/{span[0]}..{span[1]})")
        block = []
        for r in sorted(rows, key=lambda r: (r["date"], r["rnd"], r["home"], r["away"])):
            block.append(emit_match(s, r, ven, ven_split))
        season_blocks.append((s, block))
        pack_rows.extend(block)

    # ---- Freiburg split-season self-check: the wiki footnote says the first three 2021-22
    # home matches were at the Dreisamstadion; the pack data's first three Freiburg home
    # rounds must be exactly MD2/MD4/MD6 (gated) so the keyed split is the footnote's.
    frb_home = sorted(r["rnd"] for r in data["2021-22"][0] if r["home"] == "Freiburg")
    G.g(sorted(FREIBURG_SPLIT["2021-22"]) == frb_home[:3],
        f"2021-22 Freiburg split: first three home rounds from the pack rows = "
        f"{frb_home[:3]} == keyed Dreisamstadion rounds {sorted(FREIBURG_SPLIT['2021-22'])}")

    # ---- season-to-season membership boundary gates (GFP = Greuther Furth ASCII-fold)
    EXP = {"2021-22": {"out": {"Bielefeld", "GreutherFurth"}, "in": {"Schalke04", "WerderBremen"}, "nswap": 4, "nout": 2},
           "2022-23": {"out": {"Schalke04", "Hertha"}, "in": {"Heidenheim", "Darmstadt"}, "nswap": 4, "nout": 2},
           "2023-24": {"out": {"FCKoln", "Darmstadt"}, "in": {"StPauli", "HolsteinKiel"}, "nswap": 4, "nout": 2},
           "2024-25": {"out": {"HolsteinKiel", "Bochum"}, "in": {"FCKoln", "Hamburg"}, "nswap": 4, "nout": 2}}
    PO_OPP = {"2021-22": "Hamburg", "2022-23": "Hamburg", "2023-24": "FortunaDusseldorf",
              "2024-25": "Elversberg"}
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
        po16 = {t["club"] for t in data[s1][1] if t["pos"] == len(m1) - nrel}
        legs = [p for p in data[s1][2] if p["stage"].startswith("Final")]
        leg_stocks = set()
        for p in legs:
            leg_stocks.add(p["home"]); leg_stocks.add(p["away"])
        G.g(po16 <= leg_stocks and PO_OPP[s1] in leg_stocks and len(legs) == 2,
            f"boundary {s1}: 16th-place {sorted(po16)} and 2.BL side {PO_OPP[s1]} meet in the "
            f"two SHIP playoff legs; survivor stays in {s2} membership ({sorted(po16 & m2)} = "
            f"the playoff winner)")
    # 2025-16th lost the playoff: Wolfsburg exits the top flight (first playoff relegation in
    # the window) - internal consistency of the final table + playoff NB (boundary NOTE owns
    # the 2026-27 promoted set).
    w16 = [t for t in data["2025-26"][1] if t["pos"] == 16]
    po25 = [p for p in data["2025-26"][2] if p["stage"].startswith("Final")]
    G.g(len(w16) == 1 and w16[0]["club"] == "Wolfsburg" and len(po25) == 2
        and {po25[0]["home"], po25[0]["away"]} == {"Wolfsburg", "SCPaderborn"}
        and "Paderborn promoted" in po25[1]["flags"],
        "boundary 2025-26: 16th Wolfsburg lost the playoff to SC Paderborn (NB in ledger) - "
        "Wolfsburg/Heidenheim/St Pauli are the relegated set of the span-end season")

    # ---- playoff ('other') rows: curated 90-min ships cross-verified against ledger PO lines
    po_all = [p for s in SEASONS for p in data[s][2]]
    ships = [p for p in po_all if "SHIP-as-other" in p["flags"]]
    notcom = [p for p in po_all if "NOT-COMMISSIONED" in p["flags"]]
    G.g(len(ships) == 10 and len(notcom) == 10,
        f"playoffs: 10 SHIP-as-other legs (2 each season x 5 ties; the 1./2. Final touches the "
        f"top flight every year) + 10 NOT-COMMISSIONED 2./3. lines (got {len(ships)}/{len(notcom)})")
    po_lines = []
    ok_po = True
    for (s, date, home, hg90, ag90, away, vd, stadium, city, label, aet) in PO_SHIP:
        matches = [p for p in ships if p["season"] == s and p["date"] == date
                   and p["home"] == home and p["away"] == away]
        if not matches:
            ok_po = False
            continue
        p = matches[0]
        if s == "2023-24" and p["stage"] == "Final-2":
            # ledger prints the aet FINAL 0-3; after 90 it was 0-3 already (all goals 18'/66'/70')
            # and the ET was goalless: the shipped 90-min row equals every print; aet tuple here
            # carries the full-time-after-ET aggregate context (3-3) for the gate text
            ok_po &= (p["hg"], p["ag"]) == (hg90, ag90) and "aet" in p["extra"]
        elif s == "2025-26" and p["stage"] == "Final-2":
            # ledger row was corrected to the 90-min 1-1 with 'aet; FT final 2-1 after ET (Curda
            # 100)' in extra: the shipped row equals the ledger row; the aet final lives in extra
            ok_po &= (p["hg"], p["ag"]) == (hg90, ag90) and p["extra"].startswith("aet")
        else:
            ok_po &= (p["hg"], p["ag"]) == (hg90, ag90)
        po_lines.append((s, f"MATCH|{date}|{COMP_PO}|{COMPTYPE_PO}|{roster(home)}|{hg90}|{ag90}|"
                            f"{roster(away)}|{vd}|{stadium}|{city}|{COUNTRY}||{label}"))
    G.g(ok_po, "playoffs: every SHIP leg's ledger print matches the curated row (90-minute "
               "doctrine: 2023-24 leg2 ships the 0-3 played inside 90 with a goalless ET; "
               "2024-25 leg2 ships its regulation 1-2 (winner 90+5'); 2025-26 leg2 ships the "
               "90-min 1-1, Curda's 100' ET winner excluded)")
    # append PO rows after the five league blocks (mirrors the FRA pack layout)
    for s, lines in po_lines:
        pack_rows.append(lines)

    # ---- TEAM rows for the ERRATA-shipped 2.Bundesliga participants (3, alphabetical)
    team_lines = []
    for (name, ldesc, code, aliases, stadium, city) in PO_TEAMS:
        team_lines.append(f"TEAM|{name}|{COUNTRY}|{ldesc}|{code}|{aliases}|{stadium}|{city}|"
                          f"{COUNTRY}||||")

    # ---- global gates
    G.g(len(pack_rows) == 1530 + 10,
        f"pack: 1,540 MATCH rows total = 1,530 league + 10 playoff (got {len(pack_rows)})")
    keys = ["|".join((f[1], f[4], f[7])) for f in (line.split("|") for line in pack_rows)]
    G.g(len(set(keys)) == len(keys), "pack: zero duplicate (date,home,away) rows")
    clubs_union = set()
    for s in SEASONS:
        clubs_union |= {roster(t["club"]) for t in data[s][1]}
    G.g(clubs_union == ROSTER_SET,
        f"pack: union of league clubs across the 5 seasons = exactly the 25 WO section-3 strings "
        f"(no club pinned-but-unused, none outside; got {len(clubs_union)})")
    bad_names = [c for line in pack_rows for c in (line.split("|")[4], line.split("|")[7])
                 if c not in IDENTITY_DOMAIN]
    G.g(not bad_names, f"pack: every home/away string in the identity domain (25 roster pins + 3 "
                       f"registered PO participants; bad={bad_names[:4] or '-'})")
    anti = [line for line in pack_rows
            if any(a in line.split("|")[4] or a in line.split("|")[7] for a in ANTI_APPEAR)]
    G.g(not anti, "pack: anti-appear traps absent from home/away identity fields (Eintracht "
                  "Frankfurt, umlaut-print Koeln/Koeln-without variants, any Borussia or "
                  "full-form Moenchengladbach, dot-print St. Pauli, the Hertha BSC suffix, "
                  "Bayern Muenchen; city/prose fields are sourced venue "
                  "data, not identities) hits=" + str(len(anti)))

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
    G.g(same == 306 and miss == 0 and not diffs and g_idx == 990,
        f"2ndidx 2025-26: Wikipedia FBR matrix 306 cells - ALL IDENTICAL scores vs the carrier "
        f"(matrix goals {g_idx} = carrier 990 = season anchor; same={same} miss={miss} "
        f"divergent={len(diffs)})")

    # ---- anomaly gates
    r21 = data["2021-22"][0]
    G.g(any(r["rnd"] == 27 and r["home"] == "Bochum" and r["away"] == "Mgladbach"
            and r["date"] == "2022-03-18" and (r["hg"], r["ag"]) == (0, 2) for r in r21),
        "anomaly 2021-22 R27: Bochum 0-2 M'gladbach ships 2022-03-18 - abandoned 70' (assistant "
        "referee hit by a beverage cup), awarded 0-2 on 2022-03-24, the result STOOD (wf 'dec.' "
        "+ wiki efn corroborate)")
    G.g(all(any(r["rnd"] == 23 and r["home"] == h and r["away"] == a and r["date"] == "2022-02-20"
                and (r["hg"], r["ag"]) == s for r in r21)
            for (h, a, s) in [("Bayern", "GreutherFurth", (4, 1)), ("Dortmund", "Mgladbach", (6, 0)),
                              ("Hertha", "RBLeipzig", (1, 6))]),
        "anomaly 2021-22 R23: three Sunday fixtures dated 2022-02-20 (RSSSF '[Feb 21]' misprint "
        "cluster overridden on two independent indexes - OFB + wf-md23)")
    r24 = data["2024-25"][0]
    G.g(any(r["rnd"] == 14 and r["home"] == "UnionBerlin" and r["away"] == "Bochum"
            and r["date"] == "2024-12-14" and (r["hg"], r["ag"]) == (0, 2) for r in r24),
        "anomaly 2024-25 R14: Union AWD Bochum ships 0-2 on 2024-12-14 - originally 1-1, "
        "awarded to Bochum (keeper Patrick Drewes hit by a lighter; openfootball '[awarded]', "
        "wf 'dec.', wiki note)")
    r23 = data["2023-24"][0]
    G.g(all(any(r["rnd"] == 1 and r["home"] == h and r["away"] == a and r["date"] == "2023-08-20"
                and (r["hg"], r["ag"]) == s for r in r23)
            for (h, a, s) in [("UnionBerlin", "Mainz", (4, 1)), ("Frankfurt", "Darmstadt", (1, 0))]),
        "anomaly 2023-24 R1: two Sunday fixtures dated 2023-08-20 (RSSSF '[Aug 21]' misprint "
        "cluster overridden on two independent indexes - OFB + wf-md1)")
    md13 = [r for r in r23 if r["rnd"] == 13]
    md18 = [r for r in r23 if r["rnd"] == 18]
    G.g(len(md13) == 9 and any(r["home"] == "Bayern" and r["away"] == "UnionBerlin"
            and r["date"] == "2024-01-24" and (r["hg"], r["ag"]) == (1, 0) for r in md13)
        and sum(1 for r in md13 if "2023-12-01" <= r["date"] <= "2023-12-03") == 8,
        "anomaly 2023-24 MD13: 9 rows = 8 main-window (2023-12-01..03) + Bayern 1-0 Union "
        "postponed to 2024-01-24 (snow; wf-md13 corroborated)")
    G.g(len(md18) == 9 and any(r["home"] == "Mainz" and r["away"] == "UnionBerlin"
            and r["date"] == "2024-02-07" and (r["hg"], r["ag"]) == (1, 1) for r in md18)
        and sum(1 for r in md18 if "2024-01-19" <= r["date"] <= "2024-01-21") == 8,
        "anomaly 2023-24 MD18: 9 rows = 8 main-window (2024-01-19..21) + Mainz 1-1 Union "
        "postponed to 2024-02-07")
    r22 = data["2022-23"][0]
    G.g(len({r["date"] for r in r22 if r["rnd"] == 34}) == 1
        and all(r["date"] == "2023-05-27" for r in r22 if r["rnd"] == 34)
        and len([r for r in r22 if r["rnd"] == 34]) == 9,
        "anomaly 2022-23 MD34: nine simultaneous final-round fixtures all dated 2023-05-27")
    r26 = data["2025-26"][0]
    md16 = [r for r in r26 if r["rnd"] == 16]
    md17 = [r for r in r26 if r["rnd"] == 17]
    G.g(len(md16) == 9
        and any(r["home"] == "WerderBremen" and r["away"] == "Hoffenheim" and r["date"] == "2026-01-27"
                and (r["hg"], r["ag"]) == (0, 2) for r in md16)
        and any(r["home"] == "StPauli" and r["away"] == "RBLeipzig" and r["date"] == "2026-01-27"
                and (r["hg"], r["ag"]) == (1, 1) for r in md16),
        "anomaly 2025-26 RS16: 9 rows incl. the duplicate-banner makeups Werder 0-2 Hoffenheim "
        "and St Pauli 1-1 RB Leipzig, both 2026-01-27")
    G.g(len(md17) == 9
        and any(r["home"] == "Hamburg" and r["away"] == "Leverkusen" and r["date"] == "2026-03-04"
                and (r["hg"], r["ag"]) == (0, 1) for r in md17)
        and sum(1 for r in md17 if "2026-01-13" <= r["date"] <= "2026-01-15") == 8,
        "anomaly 2025-26 RS17: 9 rows = 8 mid-week main-window (2026-01-13..15, wf-md17 corroborated) + "
        "Hamburger SV 0-1 Bayer Leverkusen postponed to 2026-03-04 (Kofane 73')")
    md1 = [r for r in r26 if r["rnd"] == 1]
    G.g(len(md1) == 9 and any(r["home"] == "Bayern" and r["away"] == "RBLeipzig"
            and r["date"] == "2025-08-22" and (r["hg"], r["ag"]) == (6, 0) for r in md1),
        "anomaly 2025-26 carrier cross-check: RS1 opener Bayern 6-0 RB Leipzig 2025-08-22 sits "
        "in the openfootball carrier exactly as the season record prints it")

    # ---- venue gate
    bad_ven = []
    for line in pack_rows:
        f = line.split("|")
        if not f[9] or not f[10]:
            bad_ven.append(line)
    G.g(not bad_ven and ven_lines == 96 and len(ven) == 95 and len(ven_split) == 1,
        f"venues: all 1,540 rows carry stadium/city constants (ger-venues.txt = 96 VENUE rows: "
        f"90 per-season lattice + 5 playoff fallbacks + 1 Freiburg 2021-22 SPLIT footnote entry; "
        f"dict keys {len(ven)}+{len(ven_split)}; empties={len(bad_ven)})")
    dreisam = sum(1 for line in pack_rows if "Dreisamstadion" in line)
    europa = sum(1 for line in pack_rows if "Europa-Park Stadion" in line)
    G.g(dreisam == 3 and europa == 14 + 17 * 4,
        f"venues Freiburg: exactly 3 Dreisamstadion rows (2021-22 MD2/MD4/MD6 home) + 82 "
        f"Europa-Park rows = 14 in 2021-22 + 17 in each of the four later seasons "
        f"(got {dreisam}/{europa})")

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
                         f"34 games in round order; summary gated vs the season TABLE constants)")
        pivot_out.extend(lines)
    G.g(all_ok, f"pivots: {green}/{total} club-season full-campaign pivots reproduce the "
                "final-table lines (34 games = 17 home + 17 away each)")

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
                 "'Germany Bundesliga'/'domestic-league'; playoff legs: 'Germany Relegation "
                 "Playoffs'/'other'; country Germany everywhere)")
    labels = {s[0] for s in SOURCES}
    G.g(all(line.split("|")[13] in labels for line in pack_rows),
        "grammar: every row's sourceLabel resolves to a declared SOURCE")
    try:
        for line in team_lines + pack_rows:
            line.encode("ascii")
        asc = True
    except UnicodeEncodeError:
        asc = False
    G.g(asc, "grammar: ASCII-only TEAM+MATCH rows (venue/team strings NFKD-folded - Forsterei, "
             "Furth, Monchengladbach, Schuco-Arena, Bollenfalltor, Dusseldorf; apostrophes "
             "typewriter; TEAM aliases carry the ASCII 'ue'-transliteration convention; the "
             "umlaut verbatim prints live in the ledgers' verbatim fields, never in pack rows)")

    # ---------------------------------------------------------------- NOTE texts
    notes = []
    notes.append(
        f"NOTE|info|pack_id|GER-2021-2026_BP-TEAM-PACK_v2 - return of WO-GER-SPAN-15 (queue "
        f"position 15), FULL SPAN under OWNER OVERRIDE DECREE-2026-08-04 ('I require you to "
        f"deliver full season files regardless of what the workorder said ... my authority "
        f"overrides everything ... I want one source of truth'). 1,540 MATCH rows = 1,530 "
        f"Germany Bundesliga rows (306 per season x 5 - 18 clubs x 34 matchdays every season, "
        f"the WO's explicit 'NOT 20/38' shape) + 10 Germany Relegation Playoffs pro/rel legs "
        f"compType 'other' (every 1./2. tie in the window - one per season, two legs each - "
        f"ships per ERRATA-2026-08-03 + DECREE-2026-08-04; the WO line 'Relegation playoff "
        f"exists but is OUT of this order' is superseded by the owner override, same handling "
        f"as RPL/CZ1/MOLCUP/FRA - tension disclosed under errata_playoffs). Then the 2026-27 "
        f"boundary: the new season starts 2026-08-28, AFTER the {ACCESSED} return date, so zero "
        f"2026-27 rows exist (sourced boundary NOTE below). The file name 'GER-2021-2026' "
        f"carries no cutoff - the span is certified gap-free through today. Compiled {ACCESSED}.")
    for lbl, url, typ, what in SOURCES:
        notes.append(f"SOURCE|{lbl}|{url}|{ACCESSED}|{typ}|{what}")
    notes.append(
        "NOTE|info|federation_check|Section-0 scan on the finished pack: all 1,540 rows are "
        "Germany rows. The 1,530 league rows are populated exclusively by the 25 pinned "
        "section-3 roster strings (all 25 appear in-window; none is pinned-but-unused). "
        "Per-season compositions: 2021-22 Augsburg, Bayern Munich, Bielefeld, Bochum, Dortmund, "
        "Ein Frankfurt, FC Koln, Freiburg, Greuther Furth, Hertha, Hoffenheim, Leverkusen, "
        "M'gladbach, Mainz, RB Leipzig, Stuttgart, Union Berlin, Wolfsburg; 2022-23 minus "
        "Bielefeld/Greuther Furth plus Schalke 04, Werder Bremen; 2023-24 minus "
        "Hertha/Schalke 04 plus Darmstadt, Heidenheim; 2024-25 minus Darmstadt/FC Koln plus "
        "Holstein Kiel, St Pauli; 2025-26 minus Bochum/Holstein Kiel plus FC Koln, Hamburg. "
        "The 10 playoff rows add exactly three participants outside the section-3 pins - all "
        "2. Bundesliga clubs, registered with TEAM rows (Fortuna Dusseldorf 2023-24, SV "
        "Elversberg 2024-25, SC Paderborn 2025-26; the other three ties' entrants Hamburg "
        "2021-22/2022-23 are section-3 members already). Not England, not France; the DFB-Pokal "
        "and 2. Bundesliga stay OUT per WO section-1 (the 2.BL table lives only as ledger "
        "context and the playoff adversaries' registration data). Anti-appear list (Eintracht "
        "Frankfurt, the umlaut print 1. FC Koeln or the Koeln variant, any Borussia or "
        "full-form Moenchengladbach, dot-print St. Pauli, the Hertha BSC suffix, Bayern "
        "Muenchen) is empty on row identity fields. No standings tables "
        "carried - rows only.")
    notes.append(
        "NOTE|info|catalog|1,540 MATCH rows = 1,530 'Germany Bundesliga' 'domestic-league' rows "
        "(306 x 5) + 10 'Germany Relegation Playoffs' 'other' rows (2 legs x 5 ties, one tie per "
        "season; competition strings declared once here, per WO section-2) + 3 TEAM rows "
        "(registration of the playoff participants missing from the section-3 roster - see "
        "team_registration). Venue-detail field carries MD1..MD34 round labels per WO; playoff "
        "legs carry 'Playoff leg1'/'Playoff leg2'. Rows only, no tables; file ends with END. "
        "90-minute doctrine: league rows are full-time scores throughout; two playoff legs went "
        "past 90 minutes and ship the 90-minute score with advancement NOTEs (2023-24 leg2 "
        "0-3 with a goalless ET then 5-6 on penalties; 2025-26 leg2 1-1 then Curda's 100' ET "
        "winner made it 2-1); the 2024-25 leg2 winner came at 90+5' = still regulation, the "
        "row ships 1-2 as played.")
    notes.append(
        "NOTE|info|identity|The 25 pinned section-3 strings are used verbatim in home/away for "
        "every league row. Rename/spelling traps mapped silently, each once here: Borussia "
        "Borussia Moenchengladbach (official print with umlaut-o) -> always M'gladbach (this "
        "exact abbreviated form, typewriter "
        "apostrophe); Eintracht Frankfurt -> always Ein Frankfurt (never Eintracht); 1. FC "
        "Koeln (official print with umlaut-o and the dots) -> always FC Koln (the WO's exact "
        "string drops the dots and the umlaut); FC St. "
        "Pauli -> always St Pauli (no dot); SpVgg Greuther Fuerth (official print with "
        "umlaut-u) -> Greuther Furth (ASCII fold); the rest of the abbreviations are already "
        "the canonical roster forms: "
        "Augsburg, Bielefeld, Bochum, Darmstadt, Heidenheim, Hertha, Hoffenheim, Leverkusen, "
        "Mainz, Stuttgart, Wolfsburg, Hamburg, plus stock-to-roster maps Bayern->Bayern Munich, "
        "Leipzig->RB Leipzig, Schalke->Schalke 04, Union->Union Berlin, Bremen->Werder "
        "Bremen, Kiel->Holstein Kiel. No club changed identity in-window (no renames or "
        "mergers 2021-26). ASCII discipline: pack rows and prose are ASCII-only; official "
        "umlaut prints are transliterated ue/oe in NOTE prose and folded in identity fields, "
        "with the verbatim prints preserved in the ledgers. The three playoff-only participants "
        "are registered ASCII-canonical "
        "Fortuna Dusseldorf (official print with umlaut-u), SV Elversberg, SC Paderborn "
        "(official print SC Paderborn 07) - aliases on their TEAM rows.")
    notes.append(
        "NOTE|info|venue_policy|MATCH stadium/city = the home club's documented ground for that "
        "season per the Wikipedia season articles' stadium/location tables (second index; RSSSF "
        "carries no venues), transcribed to audit/ledger/ger-venues.txt (96 entries = 90-season "
        "lattice 18x5 + 1 split + 5 playoff fallbacks) and ASCII-folded. Stadium strings follow "
        "the articles' printed display text per season - sponsor epochs are era data, not "
        "errors: Stuttgart 'Mercedes-Benz Arena' 2021-22/2022-23 -> 'MHPArena' from 2023-24; "
        "Werder Bremen 'Wohninvest Weserstadion' 2022-23/2023-24 -> plain 'Weserstadion' from "
        "2024-25; Mainz 'Mewa Arena' -> uppercase print 'MEWA Arena' 2025-26; capacity prints "
        "shift some seasons (Frankfurt 51,500/58,000/59,500; Koln 49,698/50,000) - carried per "
        "season. Split season: Freiburg 2021-22 'played their first three home matches at the "
        "Dreisamstadion before permanently moving to the Europa-Park Stadion' (wiki footnote) "
        "=> MD2/MD4/MD6 home rows carry Dreisamstadion (24,000), the other 14 home rounds "
        "Europa-Park Stadion (34,700); the keyed rounds are self-gated against the pack rows. "
        "Playoff legs use the home club's ground: 2.BL hosts read their documented home grounds "
        "(Hamburg Volksparkstadion in both 2021-22 and 2022-23, Fortuna Dusseldorf Merkur "
        "Spiel-Arena, SV Elversberg Waldstadion an der Kaiserlinde Spiesen-Elversberg, SC "
        "Paderborn Home Deluxe Arena) - the five fallback entries in the ledger, corroborated "
        "by the wiki playoff boxes (attendances 57,000 / 55,500 / 51,500 / 9,105 / 15,000). No "
        "groundshares and no neutral-venue fixtures anywhere in the window.")
    notes.append(
        "NOTE|info|round_counts|Season row/goal/span anchors, each recomputed from the pack rows "
        "and matching the official record: 2021-22 = 306 rows, 954 goals, 2021-08-13.."
        "2022-05-14 (opener M'gladbach 1-1 Bayern Munich; champions Bayern Munich 77); 2022-23 "
        "= 306, 971, 2022-08-05..2023-05-27 (nine simultaneous final-round fixtures 2023-05-27; "
        "champions Bayern Munich 71, decided on goal difference over Dortmund on the last day); "
        "2023-24 = 306, 985, 2023-08-18..2024-05-18 (champions Leverkusen 90 - first title, "
        "UNBEATEN 28-6-0, clinched 2024-04-14); 2024-25 = 306, 959, 2024-08-23..2025-05-17 "
        "(champions Bayern Munich 82); 2025-26 = 306, 990, 2025-08-22..2026-05-16 (opener "
        "Bayern Munich 6-0 RB Leipzig; champions Bayern Munich 89 with a league-record 122 "
        "goals - 34th title, clinched 2026-04-19 at Stuttgart 4-2 per the season article). "
        "Every season is one full double round-robin: 34 matchdays x 9 fixtures, zero "
        "double-rounds, zero cancellations.")
    notes.append(
        "NOTE|info|continuity|Continuity-clause accounting (gap-free league span 2021-08-13 -> "
        "2026-05-16): every matchday of all five seasons exists and is dated; no fixture was "
        "cancelled; no point deductions anywhere in the window. Documented disruptions, rows "
        "always keep their original MD labels while the file stays date-sorted. "
        "Abandonment/award cases, two in the window, both with the result STANDING (rows ship "
        "normally, never an abandoned-score row and never a VOID): 2021-22 R27 Bochum 0-2 "
        "M'gladbach abandoned 70' (assistant referee hit by a beverage cup), awarded 0-2 on "
        "2022-03-24 - the scoreline was already 0-2 when play stopped; 2024-25 R14 Union AWD "
        "Bochum originally 1-1 (keeper Drewes hit by a lighter), awarded 0-2 - openfootball "
        "prints '0-2 [awarded]', worldfootball 'dec.' on both. Postponements with stray dates "
        "into later windows: 2021-22 MD25 Mainz 0-1 Dortmund played 2022-03-16, MD26 Augsburg "
        "2-1 Mainz played 2022-04-06; 2022-23 none; 2023-24 MD13 Bayern 1-0 Union played "
        "2024-01-24 (snow) and MD18 Mainz 1-1 Union played 2024-02-07 - the same club Union on "
        "both makeup trips, wf-md13 corroborates; 2024-25 none; 2025-26 RS16 Werder 0-2 "
        "Hoffenheim + St Pauli 1-1 RB Leipzig both 2026-01-27 (duplicate-banner blocks summed "
        "under the banner), RS17 Hamburger SV 0-1 Bayer Leverkusen 2026-03-04 (wf-md17 "
        "corroborates). Winter breaks (incl. the 2022 World Cup winter) are scheduling, not "
        "gaps. Season spans as listed under round_counts; every official match sits exactly "
        "once in the pack.")
    notes.append(
        "NOTE|info|boundary|Span-end state per WO section-1 row 2: the last completed round of "
        "the span is 2025-26 MD34, all nine fixtures played 2026-05-16 (final table inside the "
        "gates; Bayern Munich champions 89 pts, league-record 122 goals, 34th title clinched "
        "2026-04-19). The playoff tail of the same season runs 2026-05-21/25 (10 'other' rows "
        "total across the window, included - and this is the tie that changed a level: SC "
        "Paderborn PROMOTED, Wolfsburg RELEGATED, the first playoff exchange of the window; the "
        "four earlier ties all kept both clubs at their levels). The 2026-27 season had NOT "
        "started on the return date 2026-08-05: rsssf.org/tablesd/duit2027.html answers 404, "
        "and the 2026-27 season article fixes the dates '28 August 2026 - 22 May 2027' with 18 "
        "teams - promoted Schalke 04 (return after three years), SV Elversberg (Bundesliga "
        "debut, 59th club in the division) and SC Paderborn (the playoff winners; return after "
        "six years); relegated VfL Wolfsburg (via the playoff), 1. FC Heidenheim and FC St. "
        "Pauli - exactly this pack's 2025-26 play-off place plus bottom two. Zero 2026-27 rows "
        "are emitted; this is a boundary statement, not a blocker. No dateless rows, no "
        "duplicate (date,home,away) rows anywhere in the pack (gate-verified).")
    notes.append(
        "NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot "
        "gate: the pack's own rows are re-pivoted club-by-club - each club of each season shows "
        "its full campaign (17 home + 17 away = 34 games) enumerated in round order with dates, "
        "and every TEAMPIVOT summary line reproduces the club's official final-table line "
        "(P/W/D/L/GF/GA/Pts; no deductions in-window). All 90 club-season pivots (18 clubs x 5 "
        "seasons) are printed in audit/pack-validation-ger.txt next to this file. 90/90 green.")
    notes.append(
        "NOTE|info|source_adaptation|WO section-4 design: RSSSF tablesd/duit<YEAR>.html pages = "
        "primary for dates AND scores (German archive uses 'duit'); duit2022..duit2025 carry "
        "full round-by-round sections transcribed to audit/ledger/ger-<season>.txt on fetch day "
        "2026-08-05. ADAPTATION for 2025-26: duit2026.html (Karel Stokkermans, updated 18 Jun "
        "2026) carries the 1.Bundesliga final table, the playoff block and the cups but NO "
        "league round-by-round - the 2025-26 match rows therefore come from the independent "
        "index openfootball/deutschland 2025-26/1-bundesliga.txt and are labelled ofb-ger-2526 "
        "(format-B banner groups mapped to MD incl. the RS16/RS17 makeup blocks; parser "
        "tools/parse_ofb_de.py, verbatim raw saved in data/raw/); the RSSSF final table remains "
        "the table authority and the recompute of those 306 rows reproduces it club-for-club "
        "and in position order EXACT (gate above). Second-index coverage: openfootball season "
        "files diffed row-for-row vs RSSSF for 2021-22..2024-25 (306/306 IDENTICAL round + date "
        "+ score x4, tools/diff_ger_second_index.py); the Wikipedia 2025-26 FBR results matrix "
        "diffed cell-for-cell against the carrier (306/306 IDENTICAL, 990 goals both, "
        "tools/diff_ger_matrix.py); worldfootball matchday pages corroborate one full round per "
        "season (spot_audit) including both awarded fixtures and the 2025-26 RS17 stray; "
        "Wikipedia playoff boxes verified the three past-90' 90-minute splits (2023-24 18'/66'/"
        "70'(p) all regulation + goalless ET; 2024-25 Scienza 90+5' still regulation; 2025-26 "
        "Bilbija 38' regulation + Curda 100' ET). Conflicts were resolved per section-4(3) - "
        "RSSSF stands unless two independent indexes agree against it - and exactly TWO conflicts "
        "arose in the whole order, both the same species: an RSSSF date misprint cluster "
        "(three Sunday fixtures of round 23 2021-22 printed under '[Feb 21]', two Sunday "
        "fixtures of round 1 2023-24 printed under '[Aug 21]'), each disproved by TWO "
        "independent indexes agreeing on the Sunday dates (openfootball AND the worldfootball "
        "matchday page), resolved to the independent dates with the two source_conflict NOTEs "
        "below; the RSSSF prints stay verbatim in the raws and in the ledger addenda. Nothing "
        "else diverges anywhere in the five seasons, and nothing is imputed. The only other "
        "blemish was the RSSSF site's own garbled interim 2025-26 revision, quarantined in the "
        "quarantine NOTE below.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF duit2022.html prints round 23 'Bayern 4-1 Greuther "
        "Fuerth', 'Dortmund 6-0 M'gladbach' and 'Hertha 1-6 RB Leipzig' under '[Feb 21]' - a "
        "fixtureless Monday (the round ran Fri 2022-02-18 to Sun 2022-02-20; the DFB schedule "
        "carries no Monday game that week). TWO independent indexes agree against it: the "
        "openfootball season file and the worldfootball MD23 page (20.02.2022 15:30 / 17:30 / "
        "19:30 respectively). Per section-4, the pack rows carry 2022-02-20; the RSSSF print is "
        "preserved verbatim in data/raw/rsssf-duit2022-1bl.txt with the addendum in "
        "audit/ledger/ger-2021-22.txt. All scores were always identical across every source; "
        "the final table is unaffected either way.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF duit2024.html prints round 1 'Union 4-1 Mainz' and "
        "'Frankfurt 1-0 Darmstadt' under '[Aug 21]' - a fixtureless Monday (the round ran Fri "
        "2023-08-18 to Sun 2023-08-20). TWO independent indexes agree against it: the "
        "openfootball season file and the worldfootball MD1 page (20.08.2023 15:30 / 17:30 "
        "respectively). Per section-4, the pack rows carry 2023-08-20; the RSSSF print is "
        "preserved verbatim in data/raw/rsssf-duit2024-1bl.txt with the addendum in "
        "audit/ledger/ger-2023-24.txt. All scores were always identical across every source; "
        "the final table is unaffected either way.")
    notes.append(
        "NOTE|warning|quarantine|First fetch of RSSSF duit2026.html on 2026-08-05 served a "
        "garbled interim revision of the 1.Bundesliga playoff/table section (stale placement); "
        "it was quarantined immediately, never transcribed into any ledger and never produced a "
        "pack row. The corrected revision was served on re-fetch the same day and is the gated "
        "truth - it agrees 18/18 with the Wikipedia 2025-26 league table, and the FBR matrix "
        "(306/306) plus the season anchors (306 matches / 990 goals) close around it. Disclosed "
        "here as an anomaly of the primary's serving pipeline; NOT a source_conflict (no second "
        "source ever carried the garble).")
    notes.append(
        "NOTE|warning|errata_playoffs|Tension disclosure: WO-GER-SPAN-15 section-1 says "
        "'Relegation playoff exists but is OUT of this order'. ERRATA-2026-08-03 (registered in "
        "the supervisor decree pack) plus OWNER OVERRIDE DECREE-2026-08-04 supersede: every "
        "pro/rel play-off leg touching the top flight SHIPS as compType 'other', same handling "
        "already staged-forced in the RPL, CZ1, MOLCUP and FRA returns ('I want one source of "
        "truth'). The ten legs are therefore in this file: 2021-22 Hertha-Hamburg 0-1 + "
        "Hamburg-Hertha 0-2 (both remain), 2022-23 Stuttgart-Hamburg 3-0 + Hamburg-Stuttgart "
        "1-3 (both remain), 2023-24 Bochum-Fortuna Dusseldorf 0-3 + Fortuna Dusseldorf-Bochum "
        "0-3 aet 5-6 pen (both remain), 2024-25 Heidenheim-SV Elversberg 2-2 + Elversberg-"
        "Heidenheim 1-2 (both remain), 2025-26 Wolfsburg-SC Paderborn 0-0 + Paderborn-Wolfsburg "
        "1-1 after 90 / 2-1 aet (Paderborn PROMOTED, Wolfsburg relegated). The 2./3. playoffs "
        "of the ledger (Kaiserslautern-Dresden, Wehen Wiesbaden-Bielefeld, Regensburg-Wehen, "
        "Saarbruecken-Braunschweig, RW Essen-Greuther Fuerth) stay NOT-COMMISSIONED context per "
        "WO section-1 (2. Bundesliga out).")
    notes.append(
        "NOTE|warning|team_registration|WO section-2 says TEAM rows are 'NOT expected: every "
        "club of the 2021-26 window is already on our roster'. True for all 1,530 league rows "
        "(all 25 pins used, none invented). The ERRATA-shipped playoff legs, however, introduce "
        "three participants the section-3 roster never lists - Fortuna Dusseldorf (official "
        "print with umlaut-u, transliterated Fortuna Duesseldorf in the TEAM aliases; "
        "2023-24 tie), SV Elversberg (2024-25) and SC Paderborn "
        "(official print SC Paderborn 07; 2025-26), all 2. Bundesliga clubs in their tie "
        "seasons. Rather than leaving unregistered identities in home/away (and instead of the "
        "WO's fallback 'NOTE|warning|blocker; do NOT invent an identity' - nothing is invented "
        "here, every attribute is fetched: grounds from the season/PO documentation, identities "
        "from the primary playoff blocks), the three clubs are registered with the three TEAM "
        "rows at the top of this file, following the MOLCUP/RUS-ADDENDUM registration shape; "
        "ASCII-canonical name forms are the match-row identities, the umlaut/official prints "
        "ride as aliases. SV Elversberg becomes a section-3-worthy identity from 2026-27 "
        "(promoted; boundary NOTE) but stays registered here as a 2.BL participant for 2024-25.")
    notes.append(
        "NOTE|info|advancement|2021-22 pro/rel Final: Hertha 0-1 Hamburg (2022-05-19, "
        "Olympiastadion 75,500) and Hamburg 0-2 Hertha (2022-05-23, Volksparkstadion 57,000) - "
        "no extra time either leg; HERTHA WON 2-1 ON AGGREGATE and both clubs remained at "
        "their levels (Hertha stays Bundesliga, Hamburg stays 2. Bundesliga; run to a "
        "third-straight failed 2.BL playoff for Hamburg). L2-internal 2./3. tie "
        "(Kaiserslautern 0-0 Dynamo Dresden; Dresden 0-2 Kaiserslautern) is outside the "
        "commissioned slice - ledger context lines only.")
    notes.append(
        "NOTE|info|advancement|2022-23 pro/rel Final: Stuttgart 3-0 Hamburg (2023-06-01, "
        "Mercedes-Benz Arena 47,500) and Hamburg 1-3 Stuttgart (2023-06-05, Volksparkstadion "
        "55,500) - no extra time either leg; STUTTGART WON 6-1 ON AGGREGATE and both clubs "
        "remained at their levels (Stuttgart stays Bundesliga; Hamburg's second-straight "
        "failed playoff). L2-internal 2./3. tie (Wehen Wiesbaden-Bielefeld) is outside the "
        "commissioned slice - ledger context lines only.")
    notes.append(
        "NOTE|info|advancement|2023-24 pro/rel Final: Bochum 0-3 Fortuna Dusseldorf "
        "(2024-05-23, Vonovia Ruhrstadion 26,000) and Fortuna Dusseldorf 0-3 Bochum "
        "(2024-05-27, Merkur Spiel-Arena 51,500) - the second leg's three Bochum goals all "
        "came inside 90 minutes (Hofmann 18', 66'; Stoeger 70' pen), the extra time was "
        "GOALLESS, so the shipped row is the 90-minute 0-3 exactly as printed everywhere; "
        "3-3 aggregate, BOCHUM WON 6-5 ON PENALTIES (the '5-6 pen' of the ledger) and both "
        "clubs remained at their levels - the preservation-of-the-season salvage of the "
        "window. L2-internal 2./3. tie (Regensburg-Wehen) is outside the commissioned slice - "
        "ledger context lines only.")
    notes.append(
        "NOTE|info|advancement|2024-25 pro/rel Final: Heidenheim 2-2 SV Elversberg (2025-05-22, "
        "Voith-Arena 15,000) and SV Elversberg 1-2 Heidenheim (2025-05-26, Waldstadion an der "
        "Kaiserlinde, Spiesen-Elversberg 9,105) - the leg-2 winner (Scienza 90+5', after "
        "Honsak 9' and Fellhauer 31') landed in STOPPAGE TIME = regulation, so NO extra time "
        "was played and the shipped row is the full-time 1-2 as printed; HEIDENHEIM WON 4-3 ON "
        "AGGREGATE and both clubs remained at their levels. L2-internal 2./3. tie "
        "(Saarbruecken-Braunschweig, leg2 after ET) is outside the commissioned slice - ledger "
        "context lines only.")
    notes.append(
        "NOTE|info|advancement|2025-26 pro/rel Final: Wolfsburg 0-0 SC Paderborn (2026-05-21, "
        "Volkswagen Arena 27,800) and SC Paderborn 1-1 Wolfsburg after 90 minutes (2026-05-25, "
        "Home Deluxe Arena) - regulation goals Pejcinovic 3' (WOB) and Bilbija 38' (PAD); the "
        "tie went to EXTRA TIME where Curda scored at 100' to make it 2-1, so the shipped row "
        "is the 90-minute 1-1 per doctrine and this NOTE carries the outcome: 2-1 AFTER EXTRA "
        "TIME, SC PADERBORN PROMOTED to the 2026-27 Bundesliga (return after six years) and "
        "VfL Wolfsburg RELEGATED - the first promotion/relegation exchange via the playoff in "
        "the window. L2-internal 2./3. tie (RW Essen-Greuther Fuerth) is outside the "
        "commissioned slice - ledger context lines only.")
    notes.append(
        "NOTE|info|spot_audit|2021-22 matchday 27 re-listed for spot-audit - the abandoned-and-"
        "awarded round (sources https://www.rsssf.org/tablesd/duit2022.html, ofb-ger-2122 - diff "
        "306/306 IDENTICAL - and the worldfootball matchday page wf-ger-2122-md27 which marks "
        "Bochum 0:2 M'gladbach 'dec.'): "
        + spot_listing("2021-22", SPOT["2021-22"], data["2021-22"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2022-23 matchday 34 re-listed for spot-audit - the simultaneous "
        "final round, all nine fixtures 2023-05-27 (sources https://www.rsssf.org/tablesd/"
        "duit2023.html, ofb-ger-2223 AND wf-ger-2223-md34; title decided on goal difference): "
        + spot_listing("2022-23", SPOT["2022-23"], data["2022-23"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2023-24 matchday 13 re-listed for spot-audit - the snow-"
        "postponement round with its January makeup (sources https://www.rsssf.org/tablesd/"
        "duit2024.html, ofb-ger-2324 AND wf-ger-2324-md13, which prints the makeup Bayern 1:0 "
        "Union on 24.01.2024 20:30 exactly like the carrier): "
        + spot_listing("2023-24", SPOT["2023-24"], data["2023-24"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2024-25 matchday 14 re-listed for spot-audit - the awarded-"
        "fixture round (sources https://www.rsssf.org/tablesd/duit2025.html, ofb-ger-2425 "
        "printing '0-2 [awarded]', AND wf-ger-2425-md14 marking Union 0:2 Bochum 'dec.'): "
        + spot_listing("2024-25", SPOT["2024-25"], data["2024-25"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2025-26 matchday 17 re-listed for spot-audit - the round with "
        "the RS17 banner-stray (sources ofb-ger-2526 = the season's labelled carrier, "
        "wikimatrix-ger-2526 AND wf-ger-2526-md17, which prints eight fixtures 2026-01-09..11 "
        "plus the Hamburger SV fixture dated 04.03.2026 exactly like the carrier): "
        + spot_listing("2025-26", SPOT["2025-26"], data["2025-26"][0]) + ".")

    # ---------------------------------------------------------------- final pack integrity gates
    pack = "\n".join(notes + team_lines + pack_rows + ["END"]) + "\n"
    G.g(pack.rstrip().endswith("END"), "file ends with END")
    G.g(len(pack.splitlines()) == len(notes) + len(team_lines) + 1540 + 1,
        f"pack line accounting: {len(notes)} header rows (NOTE+SOURCE) + {len(team_lines)} TEAM + "
        f"1,540 MATCH + END")
    block_ok = True
    for s, block in season_blocks:
        dates = [l.split("|")[1] for l in block]
        labels = {l.split("|")[13] for l in block}
        if dates != sorted(dates) or labels != {SRC_LABEL[s]}:
            block_ok = False
    po_dates = [l.split("|")[1] for l in pack_rows if l.split("|")[3] == COMPTYPE_PO]
    G.g(block_ok and all(l.split("|")[8].startswith("Playoff leg") for l in pack_rows if l.split("|")[3] == COMPTYPE_PO),
        "pack ordering: five season blocks in order, each league block date-sorted and carrying "
        "only its season's source label; the 10 playoff legs follow the league blocks in tie "
        "order (Playoff leg1/leg2 venue-details)")
    team_ok = (len(team_lines) == 3
               and all(len(l.split("|")) == 13 for l in team_lines)
               and [l.split("|")[1] for l in team_lines] == sorted(l.split("|")[1] for l in team_lines))
    G.g(team_ok, "TEAM rows: 3, alphabetical, 13 pipe-fields in the "
                 "TEAM|name|country|league|code|aliases|stadium|city|country|...|founded| shape "
                 "(founded left empty - no imputation)")

    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="ascii", newline="\n") as fh:
        fh.write(pack)

    # ---------------------------------------------------------------- validation output
    head = [
        "GER PACK VALIDATION - handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt",
        f"builder tools/build_ger_pack.py, run {ACCESSED}; gates PASS {G.n_pass} FAIL {G.n_fail}",
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
