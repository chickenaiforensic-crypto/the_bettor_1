#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build + validate handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt (WO-CZ1-BACKFILL-02, full-span override).

DECREE-2026-08-04 (OWNER OVERRIDE, supervisor/DECREE-2026-08-04-full-span-override.md): every pack is
the FULL span 2021-22..today; the 2024-06-30 hard cutoffs are rescinded; packs = single source of truth.
CZ1 therefore carries all five completed seasons 2021-22..2025-26; 2026-27 (R1 scheduled 2026-08-07..09,
after return date) is NOT a full season -> zero rows, boundary NOTE.

PRIMARY:  audit/ledger/cz1-<season>.txt  (RSSSF tablest/tsje2022|2023|2024|2025|2026.html;
          240 regular rows R1..R30 + Titul T31..T35 + Zachranu Z31..Z35 + Evropu ESF/EF legs + CLP 2023-24,
          with H2H brackets, group tables, pro/rel ties as comment records / RT-TT-ZT constant records.
          2025-26: tsje2026 is PAGE-FORM (tables + playoff legs only, no round listings) -> the 270
          league-stage rows were rebuilt from the BBC dated month lattice (audit/ledger/cz1-dates-bbc-
          2025-2026.txt) + wiki FBR matrices under the tools/build_cz1_2526_ledger.py V1..V6 gates,
          recompute == RSSSF constants EXACT; same adaptation class as the EPL 2025-26 return.)
2NDIDX:   audit/ledger/cz1-2ndidx-<season>.txt (Wikipedia season articles: FBR results matrices, group
          matrices, Evropu brackets, pro/rel TwoLeg boxes; worldfootball.net matchday spot-audits
          R10/R20/R25 for 2021-22..2023-24 - worldfootball dropped Czech coverage from 2024-25, 404s
          documented, spot-audit gate n/a for the two new seasons)
CONSTANTS audit/ledger/cz1-venues.txt (venues + official regular/Titul/Zachranu table constants, wiki)
Output:   handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt  +  audit/pack-validation-cz1.txt
Run:      python3 tools/build_cz1_pack.py   (exit 0 iff every gate PASS)
"""
import os, re, sys
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")
OUTPACK = os.path.join(ROOT, "handoffs", "CZ1-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation-cz1.txt")
ACCESSED = "2026-08-04"
RETURN_DATE = "2026-08-04"   # DECREE-2026-08-04 boundary (the 2024-06-30 hard cutoff is rescinded)
SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
SEASON_FILES = {s: f"cz1-{s}.txt" for s in SEASONS}
COMP = "Czech First League"
COMPTYPE = "domestic-league"   # WO-CZ1 section-2 verbatim (regular AND all three playoff-stage groups)
COUNTRY = "Czech Republic"
SRC_LABEL = {"2021-22": "rsssf-tsje2022", "2022-23": "rsssf-tsje2023", "2023-24": "rsssf-tsje2024",
             "2024-25": "rsssf-tsje2025", "2025-26": "rsssf-tsje2026"}
SPOT = {"2021-22": 10, "2022-23": 20, "2023-24": 25}     # worldfootball spot-audit matchdays (fixed,
             # documented; wf dropped Czech coverage 2024-25 on -> gate documented n/a for new seasons)

# ---------------- pro/rel playoff block (WO section-1 last row, owner sanction 2026-08-03) ----------------
PROCOMP = "Czech Relegation Playoffs"   # WO section-2 verbatim competition string for the pro/rel ties
PROTYPE = "other"                       # ERRATA-2026-08-03 class rule for pro/rel rows; supersedes the WO
                                        # section-2 single-class line, which predates the ties' re-entry
FNL5 = {"Vlasim", "Opava", "Pribram", "Vyskov", "Taborsko"}  # FNL (CZ2) pro/rel opponents 2021-24, reused
                                        # client-roster strings (no TEAM rows; tiers in the ledgers)
FNL7 = FNL5 | {"Chrudim", "Artis Brno"}  # full-span override additions: MFK Chrudim (2024-25 tie),
                                        # SK Artis Brno ex-SK Lisen (2025-26 tie; wiki SK Artis Brno article)
PROREL_VENUE = {  # (season, home stock/FNL club) -> (stadium, city); evidence in venue_policy NOTE + cz1-venues.txt
 ("2021-22", "Teplice"):   ("Na Stinadlech", "Teplice"),
 ("2021-22", "Opava"):     ("Stadion v Mestskych sadech", "Opava"),
 ("2021-22", "Bohemians"): ("Dolicek", "Prague"),
 ("2021-22", "Vlasim"):    ("Stadion Kollarova ulice", "Vlasim"),
 ("2022-23", "Pribram"):   ("Na Litavce", "Pribram"),
 ("2022-23", "Pardubice"): ("CFIG Arena", "Pardubice"),
 ("2022-23", "Zlin"):      ("Letna Stadion", "Zlin"),
 ("2022-23", "Vyskov"):    ("Sportovni areal Drnovice", "Vyskov"),
 ("2023-24", "Vyskov"):    ("Sportovni areal Drnovice", "Vyskov"),
 ("2023-24", "CBudejovice"): ("Stadion Strelecky ostrov", "Ceske Budejovice"),
 ("2023-24", "Karvina"):   ("Mestsky stadion (Karvina)", "Karvina"),
 ("2023-24", "Taborsko"):  ("Stadion v Kvapilove ulici", "Tabor"),
 ("2024-25", "Vyskov"):    ("Sportovni areal Drnovice", "Vyskov"),
 ("2024-25", "Dukla"):     ("Stadion Juliska", "Prague"),
 ("2024-25", "Pardubice"): ("CFIG Arena", "Pardubice"),
 ("2024-25", "Chrudim"):   ("Za Vodojemem", "Chrudim"),           # en.wiki MFK Chrudim infobox ground 1500
 ("2025-26", "Ostrava"):   ("Mestsky stadion (Ostrava)", "Ostrava"),
 ("2025-26", "Taborsko"):  ("Stadion v Kvapilove ulici", "Tabor"),
 ("2025-26", "Slovacko"):  ("Mestsky fotbalovy stadion Miroslava Valenty", "Uherske Hradiste"),
 ("2025-26", "Artis Brno"): ("Mestsky fotbalovy stadion Srbska", "Brno"),  # en.wiki SK Artis Brno
                                        # infobox ground 10200 (club moved to Srbska for 2025-26, shared
                                        # with Zbrojovka Brno; renamed from SK Lisen after 2024-25)
}
# Official tie aggregates + winners (RSSSF playoff sections = primary; wiki TwoLegResults identical),
# 4th element = decider when the aggregate was level (None otherwise). In ALL five seasons every tie
# was won by the First-League side ON THE FIELD - no club changed division via the playoffs
# (2024-25 Dukla survived on penalties 4-2 after 1-1 agg/aet; the 2025-26 close-season Karvina
# administrative demotion + Artis Brno repromotion is documented in karvina_incident, not a playoff).
PROREL_TIES = {
 "2021-22": [(("Teplice", "Vlasim"), "Teplice", "5-2", None), (("Opava", "Bohemians"), "Bohemians", "3-0", None)],
 "2022-23": [(("Pribram", "Pardubice"), "Pardubice", "2-0", None), (("Zlin", "Vyskov"), "Zlin", "1-0", None)],
 "2023-24": [(("Vyskov", "Karvina"), "Karvina", "2-0", None), (("CBudejovice", "Taborsko"), "CBudejovice", "3-2", None)],
 "2024-25": [(("Vyskov", "Dukla"), "Dukla", "1-1", "pens 4-2"), (("Pardubice", "Chrudim"), "Pardubice", "2-1", None)],
 "2025-26": [(("Ostrava", "Taborsko"), "Ostrava", "8-0", None), (("Artis Brno", "Slovacko"), "Slovacko", "7-1", None)],
}

# ------------------------------------------------------------------ identity (WO-CZ1 section-3)
ROSTER17 = {
 "Banik Ostrava","Bohemians 1905","Ceske Budejovice","Hradec Kralove","Jablonec","Karvina",
 "Mlada Boleslav","Pardubice","Sigma Olomouc","Slavia Prague","Slovacko","Slovan Liberec",
 "Sparta Prague","Teplice","Viktoria Plzen","Zbrojovka Brno","Zlin",
}
DUKLA_SEASONS = {"2024-25", "2025-26"}   # Dukla Prague (promoted 2024, relegated 2026) league
                                        # membership - replaces the retired anti-appear treatment per
                                        # DECREE-2026-08-04 (full span overrides the old 3-season window)
ERA_FRAGMENTS = ("Fastav", "Trinity", "Baumit", "OKD", "MFK", "1. FC")  # NOTEs only, never row fields
STOCK2ROSTER = {
 "Bohemians": "Bohemians 1905", "Brno": "Zbrojovka Brno", "CBudejovice": "Ceske Budejovice",
 "Dukla": "Dukla Prague",
 "Hradec": "Hradec Kralove", "Jablonec": "Jablonec", "Karvina": "Karvina", "Liberec": "Slovan Liberec",
 "MlBoleslav": "Mlada Boleslav", "Olomouc": "Sigma Olomouc", "Ostrava": "Banik Ostrava",
 "Pardubice": "Pardubice", "Plzen": "Viktoria Plzen", "Slavia": "Slavia Prague",
 "Slovacko": "Slovacko", "Sparta": "Sparta Prague", "Teplice": "Teplice", "Zlin": "Zlin",
}
LEAGUE_NAMES = ROSTER17 | {"Dukla Prague"}   # names admitted on league rows (Dukla gated by season below)
# WO-pinned per-season composition (section-3; 2024-25/2025-26 per the override's full-span sources)
SEASON_CLUBS = {
 "2021-22": {"Slavia","Plzen","Sparta","Slovacko","Ostrava","Hradec","MlBoleslav","Liberec",
             "Olomouc","CBudejovice","Zlin","Teplice","Jablonec","Bohemians","Pardubice","Karvina"},
 "2022-23": {"Slavia","Plzen","Sparta","Slovacko","Ostrava","Hradec","MlBoleslav","Liberec",
             "Olomouc","CBudejovice","Zlin","Teplice","Jablonec","Bohemians","Pardubice","Brno"},
 "2023-24": {"Slavia","Plzen","Sparta","Slovacko","Ostrava","Hradec","MlBoleslav","Liberec",
             "Olomouc","CBudejovice","Zlin","Teplice","Jablonec","Bohemians","Pardubice","Karvina"},
 "2024-25": {"Slavia","Plzen","Sparta","Slovacko","Ostrava","Hradec","MlBoleslav","Liberec",
             "Olomouc","CBudejovice","Teplice","Jablonec","Bohemians","Pardubice","Karvina","Dukla"},
 "2025-26": {"Slavia","Plzen","Sparta","Slovacko","Ostrava","Hradec","MlBoleslav","Liberec",
             "Olomouc","Zlin","Teplice","Jablonec","Bohemians","Pardubice","Karvina","Dukla"},
}
SEASON_GROUPS = {  # regular-table positions -> playoff-stage assignment (from official constants)
 "2021-22": {"T": {"Slavia","Plzen","Sparta","Slovacko","Ostrava","Hradec"},
             "E": {"MlBoleslav","Liberec","Olomouc","CBudejovice"},
             "Z": {"Zlin","Teplice","Jablonec","Bohemians","Pardubice","Karvina"}},
 "2022-23": {"T": {"Sparta","Slavia","Plzen","Bohemians","Slovacko","Olomouc"},
             "E": {"Liberec","Hradec","MlBoleslav","CBudejovice"},
             "Z": {"Jablonec","Ostrava","Teplice","Brno","Pardubice","Zlin"}},
 "2023-24": {"T": {"Sparta","Slavia","Plzen","Ostrava","MlBoleslav","Slovacko"},
             "E": {"Liberec","Olomouc","Hradec","Teplice"},
             "Z": {"Bohemians","Jablonec","Pardubice","Karvina","Zlin","CBudejovice"}},
 "2024-25": {"T": {"Slavia","Plzen","Ostrava","Sparta","Jablonec","Olomouc"},
             "E": {"Liberec","Karvina","Hradec","Bohemians"},
             "Z": {"Slovacko","Dukla","Pardubice","CBudejovice","Teplice","MlBoleslav"}},
 "2025-26": {"T": {"Slavia","Sparta","Plzen","Jablonec","Hradec","Liberec"},
             "E": {"Olomouc","Pardubice","Karvina","Bohemians"},
             "Z": {"MlBoleslav","Zlin","Teplice","Dukla","Slovacko","Ostrava"}},
}
# Official Evropu outcomes (RSSSF playoff NB lines + wiki brackets; aggregates recomputed in gates)
EVROPU = {
 "2021-22": {"sf": [("CBudejovice","MlBoleslav",4,2), ("Olomouc","Liberec",3,0)],
             "f":  ("Olomouc","MlBoleslav","MlBoleslav",4,3), "winner": "MlBoleslav", "clp": None},
 "2022-23": {"sf": [("MlBoleslav","Hradec",2,0), ("CBudejovice","Liberec",6,3)],
             "f":  ("Hradec","Liberec","Liberec",6,3), "winner": "Liberec", "clp": None},
 "2023-24": {"sf": [("Teplice","Liberec",4,1), ("Hradec","Olomouc",6,2)],
             "f":  ("Teplice","Hradec","Hradec",3,0), "winner": "Hradec",
             "clp": ("MlBoleslav","Hradec",3,1)},
 "2024-25": {"sf": [("Hradec","Karvina",5,0), ("Bohemians","Liberec",4,2)],
             "f":  ("Bohemians","Hradec","Hradec",2,1), "winner": "Hradec", "clp": None},
 "2025-26": {"sf": [("Karvina","Pardubice",4,3), ("Olomouc","Bohemians",4,3)],
             "f":  ("Karvina","Olomouc","Olomouc",7,1), "winner": "Olomouc", "clp": None},
}
# Whitelisted second-index errors, each resolved to RSSSF-primary after re-fetching the cited
# tsje pages 2026-08-03 and proven by the articles' OWN official tables (gate evidence below):
# (season,(home,away)) -> (wiki FBR-cell score, pack/RSSSF score)
WIKI_WRONG_CELLS = {
 ("2022-23",("Liberec","Zlin")):    ((1,0),(2,1)),  # R26 2023-04-08, RSSSF: 2-1; wiki cell 1-0 breaks its own table (ZLN GA 55, LIB GF 39)
 ("2022-23",("Plzen","Zlin")):      ((3,0),(4,0)),  # R28 2023-04-23, RSSSF: 4-0; wiki cell 3-0 breaks its own table (ZLN GA 55, PLZ GF 55)
 ("2023-24",("Pardubice","Jablonec")): ((0,3),(0,0)),  # R2 2023-07-29, RSSSF: 0-0; wiki cell 0-3 breaks its own table (PCE GA 42, JAB GF 35)
}
# worldfootball matchday listing-date nuance: wf-cz1-2324-r25 lists Teplice-Slovacko under
# 2024-03-16 18:00; RSSSF Round 25 bracket dates it [Mar 17]. Score identical; RSSSF date kept.
WF_DATE_NUANCE = {("2023-24", 25, "Teplice", "Slovacko"): ("2024-03-16", "2024-03-17")}
# Season totals anchors = matches/goals recomputed from the fully cross-checked official record
# (RSSSF rows == wiki tables agreement). The wiki INFOBOX scalar disagrees with its own article
# for 2021-22 (763 vs derived 770) and 2023-24 (804 vs derived 792) - documented source_conflict,
# not propagated. 2022-23 infobox (276/819) is consistent.
# 2024-25/2025-26 anchors = 276 matches / goals recomputed (reg 627 + Titul 54 + Zachranu 40 + Evropu 13
# = 734; reg 623 + Titul 43 + Zachranu 36 + Evropu 22 = 724) - verified by the INFOBOX gate below.
INFOBOX = {"2021-22": (276, 770), "2022-23": (276, 819), "2023-24": (277, 792),
           "2024-25": (276, 734), "2025-26": (276, 724)}
SHAPE = {"2021-22": {35: 12, 34: 2, 32: 2}, "2022-23": {35: 12, 34: 2, 32: 2},
         "2023-24": {36: 1, 35: 12, 34: 1, 32: 2},  # 2023-24 deviation documented in NOTE (CLP Final)
         "2024-25": {35: 12, 34: 2, 32: 2}, "2025-26": {35: 12, 34: 2, 32: 2}}

SOURCES = [
 ("rsssf-tsje2022","https://www.rsssf.org/tablest/tsje2022.html","primary-archive",
  "2021-22: all 30 regular rounds dates+scores, Titul and Zachranu rounds 31-35, Evropu semifinal/final legs, "
  "official regular table with H2H brackets, group tables, pro/rel ties + NB; transcribed in audit/ledger/cz1-2021-22.txt"),
 ("rsssf-tsje2023","https://www.rsssf.org/tablest/tsje2023.html","primary-archive",
  "2022-23: all 30 regular rounds dates+scores, both group stages, Evropu legs, official regular table with H2H "
  "brackets, the regular-points tie-break NB (Sparta champion), Zlin rename note [*], pro/rel ties; audit/ledger/cz1-2022-23.txt"),
 ("rsssf-tsje2024","https://www.rsssf.org/tablest/tsje2024.html","primary-archive",
  "2023-24: all 30 regular rounds dates+scores, both group stages, Evropu legs + the extra Conference League "
  "playoff Final (2024-05-31), official regular table, group tables, pro/rel ties; audit/ledger/cz1-2023-24.txt"),
 ("rsssf-tsje2025","https://www.rsssf.org/tablest/tsje2025.html","primary-archive",
  "2024-25: all 30 regular rounds dates+scores, both group stages, Evropu legs, official regular table with "
  "the three-way H2H bracket at 34 (Bohemians over MlBoleslav over Teplice), the Titul regular-points NB "
  "(Sparta 62 over Jablonec 51 at 63), pro/rel ties (Dukla pens 4-2 after 1-1 agg aet; Pardubice 2-1; NB "
  "all remain at former level); audit/ledger/cz1-2024-25.txt (transcribed 2026-08-04)"),
 ("rsssf-tsje2026","https://www.rsssf.org/tablest/tsje2026.html","primary-archive",
  "2025-26: PAGE-FORM printing - official regular/Titul/Zachranu tables + Evropu and pro/rel leg lines only, "
  "no round listings (same adaptation class as the EPL 2025-26 return); the 270 league-stage rows were "
  "rebuilt in audit/ledger/cz1-2025-26.txt from the BBC dated month lattice + wiki FBR matrices under "
  "gates V1..V6 (two independent indexes cell-identical; recompute == these RSSSF constants EXACT "
  "16/16 regular + 6/6 Titul + 6/6 Zachranu; 623 regular goals). Zachranu position prints 13/13/15/14 "
  "= documented misprint (see print_error NOTE); Karvia relegated 'after accusations of match fixing' "
  "NB line; T32 derby official 0-3 award; pro/rel ties (Ostrava 8-0, Slovacko 7-1; NB all remain)"),
 ("wiki-cz1-2425","https://en.wikipedia.org/wiki/2024%E2%80%9325_Czech_First_League","second-index",
  "240-cell FBR regular matrix + Titul/Zachranu group matrices, 16-row regular table with hth_BOH "
  "three-way note, 6+6 group tables, venues + capacities (s5), Evropu bracket (leg2 Bohemians-Liberec 1-0 "
  "re-verified after MX transcription gate catch), pro/rel TwoLeg boxes (Vyskov-Dukla 0-0/1-1 aet pens 4-2; "
  "Pardubice-Chrudim 2-0/0-1); audit/ledger/cz1-2ndidx-2024-25.txt - diff gate 280/280 vs ledger"),
 ("wiki-cz1-2526","https://en.wikipedia.org/wiki/2025%E2%80%9326_Czech_First_League","second-index",
  "240-cell FBR regular matrix + group matrices (s8/s9/s11), regular table with hth_DUK note (Dukla 6-0 "
  "over Slovacko at 23) and note_KAR (Karvina demoted for match-fixing accusations; Artis Brno "
  "administratively promoted in its place; Karvina waived the Europa League play-off spot), championship-"
  "group walkover footnote (T32 Slavia-Sparta abandoned 3-2, LFA awarded 0-3 on 2026-05-12 - row carries "
  "the official 0-3), three unicode-minus corrupted Z-group cells adjudicated 2-0/0-3/2-0 via BBC + "
  "arithmetic closure (see print_error NOTE), venues + 2025-26 capacity reprints (s4), playoff TwoLeg "
  "boxes; audit/ledger/cz1-2ndidx-2025-26.txt - diff gate 280/280 vs ledger"),
 ("bbc-cz1-2526","https://www.bbc.com/sport/football/czech-first-league/scores-fixtures/2025-07","second-index",
  "BBC 'Czech Liga' server-rendered scores-fixtures month lattice 2025-07..2026-05 (12 month pages, same "
  "URL root): 276 dated fixtures incl. stage labels (championship/relegation groups, play-offs = Evropu), "
  "postponement dates and the T32 'Match awarded' print; transcribed to audit/ledger/cz1-dates-bbc-"
  "2025-2026.txt (276 D-rows) - BBC/wikipedia cell bijection 270/270 for the league-stage rows under gate "
  "V1 of tools/build_cz1_2526_ledger.py"),
 ("wiki-chrudim","https://en.wikipedia.org/wiki/MFK_Chrudim","second-index",
  "MFK Chrudim (FNL 2024-25, pro/rel opponent) ground = Za Vodojemem, Chrudim, capacity 1,500 "
  "(infobox Ground) - venue evidence for the 2025-06-01 pro/rel leg-2 row Chrudim 1-0 Pardubice"),
 ("wiki-artis-brno","https://en.wikipedia.org/wiki/SK_Artis_Brno","second-index",
  "SK Artis Brno (until 2025 SK Lisen; FNL 2025-26, pro/rel opponent) ground = Mestsky fotbalovy stadion "
  "Srbska, Brno, capacity 10,200 (infobox Ground + history: moved to Srbska for 2025-26, groundshare with "
  "Zbrojovka Brno) - venue evidence for the 2026-05-27 pro/rel leg-1 row Artis Brno 1-4 Slovacko; the same "
  "article documents the administrative promotion to the 2026-27 First League after Karvina's demotion"),
 ("wiki-cz1-2122","https://en.wikipedia.org/wiki/2021%E2%80%9322_Czech_First_League","second-index",
  "240-cell FBR results matrix, 16-row regular table, 6+6 group tables, Evropu bracket, venues + efn venue moves "
  "(Hradec in Mlada Boleslav, Pardubice at Dolicek), infobox 276 matches/763 goals, pro/rel TwoLeg aggregates"),
 ("wiki-cz1-2223","https://en.wikipedia.org/wiki/2022%E2%80%9323_Czech_First_League","second-index",
  "240-cell FBR matrix, regular + Titul/Zachranu tables, Evropu bracket, venues (Pardubice autumn at Dolicek, "
  "spring CFIG Arena; Slavia Fortuna Arena, Sparta epet ARENA), infobox 276/819, pro/rel match boxes with dates/venues"),
 ("wiki-cz1-2324","https://en.wikipedia.org/wiki/2023%E2%80%9324_Czech_First_League","second-index",
  "240-cell FBR matrix, regular + group tables, Conference League play-off structure text + brackets + the Final "
  "match box (2024-05-31, MlBoleslav 3-1 Hradec, Lokotrans Arena, att 4173), venues (Hradec Malsovicka Arena "
  "opened 2023-08-05), infobox 277 matches/804 goals, pro/rel TwoLeg aggregates (legs identical all 4)"),
 ("wf-cz1-2122-r10","https://www.worldfootball.net/schedule/cze-1-fotbalova-liga-2021-2022-spieltag/10/","second-index",
  "matchday-10 spot-audit: 8 fixtures, dates AND scores identical to the pack rows (results-and-standings matchday page)"),
 ("wf-cz1-2223-r20","https://www.worldfootball.net/schedule/cze-1-fotbalova-liga-2022-2023-spieltag/20/","second-index",
  "matchday-20 spot-audit: 8 fixtures, dates AND scores identical to the pack rows"),
 ("wf-cz1-2324-r25","https://www.worldfootball.net/schedule/cze-1-fotbalova-liga-2023-2024-spieltag/25/","second-index",
  "matchday-25 spot-audit: 8 fixtures, dates AND scores identical to the pack rows"),
 ("isport-baraz-2024","https://isport.blesk.cz/clanek/fotbal-chance-liga-rocnik-2023-24/448139/vyskov-karvina-0-1-hoste-jsou-bliz-zachrane-v-lize-rozhodl-cavos.html","web-index",
  "2024-05-30 evening report on pro/rel leg 1 Vyskov 0-1 Karvina (Cavos) - confirms the played date vs the pre-season announced 29 May"),
 ("ctsport-baraz-2024","https://sport.ceskatelevize.cz/clanek/fotbal/1-liga/zive-ceske-budejovice-taborsko-0-0-a-vyskov-karvina-0-0/665885f861d8d47534fa048b","web-index",
  "CT sport same-evening coverage 2024-05-30: both pro/rel leg-1 ties played that date (CBudejovice 2-1 Taborsko, Vyskov 0-1 Karvina)"),
 ("sportcz-karvina-vyskov-2024","https://www.sport.cz/clanek/fotbal-ceska-1-liga-vyskov-barazove-prokleti-nezlomil-karvina-je-stale-prvoligova-5029534","web-index",
  "2024-06-02 return-leg report: Karvina 1-0 Vyskov (Mikus 54), Karvina stays in the top flight"),
 ("wf-molcup-stadiums","https://www.worldfootball.net/competition/co88/se55490/stadiums/","third-index",
  "FNL home grounds of the pro/rel legs, from the season cup-stadium indexes se39724/se46910/se55490: Opava Stadion v "
  "Mestskych sadech 7758, Vlasim Stadion Kollarova ulice 6000, Pribram Na Litavce 7120, Vyskov listed as Stadion FK "
  "Drnovice 6400 (row string Sportovni areal Drnovice per the wiki 2023-06-04 playoff match box); full listings in "
  "audit/ledger/molcup-venues-teams.txt section A"),
 ("wiki-taborsko","https://en.wikipedia.org/wiki/FC_Silon_T%C3%A1borsko","second-index",
  "FC Silon Taborsko (CNFL/2nd tier in-window) ground = Stadion v Kvapilove ulici, Tabor - venue evidence for pro/rel "
  "leg-2 2024-06-02 Taborsko 1-1 CBudejovice (infobox Ground + lead prose)"),
]

# ------------------------------------------------------------------ readers
def read_season_rows(season):
    rows, pro = [], []
    with open(os.path.join(LEDGER, SEASON_FILES[season]), encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"):
                continue
            p = ln.split("|")
            if p[0].strip() in ("RT", "TT", "ZT"):
                continue   # official table constants carried inline in the new-season ledgers
                           # (authoritative copies gated from cz1-venues.txt; constants, not match rows)
            tag, d, h, hg, ag, a = p[0].strip(), p[1].strip(), p[2].strip(), int(p[3]), int(p[4]), p[5].strip()
            tgt = pro if tag == "PRO" else rows
            tgt.append({"season": season, "tag": tag, "date": d, "home": h, "hg": hg, "ag": ag, "away": a})
    # leg numbers inside each pro/rel tie, chronological
    ties = defaultdict(list)
    for r in pro:
        ties[frozenset((r["home"], r["away"]))].append(r)
    for legs in ties.values():
        legs.sort(key=lambda r: r["date"])
        for i, r in enumerate(legs, 1):
            r["leg"] = i
    return rows, pro

def stage_of(tag):
    if tag.startswith("T"): return "Titul"
    if tag.startswith("Z"): return "Zachranu"
    if tag == "CLP": return "Evropu-CLP"
    if tag in ("ESF1", "ESF2"): return "Evropu-SF"
    if tag in ("EF1", "EF2"): return "Evropu-F"
    return "Round"

def vdetail_of(tag):
    if tag.startswith("T") or tag.startswith("Z"):
        return f"{stage_of(tag)} R{tag[1:]}"
    if tag in ("ESF1", "ESF2"): return f"Evropu-SF L{tag[-1]}"
    if tag in ("EF1", "EF2"): return f"Evropu-F L{tag[-1]}"
    if tag == "CLP": return "Evropu-CLP"
    return f"Round {int(tag[1:])}"

def weight_of(tag):
    return {"R": 0, "T": 1, "Z": 2}.get(tag[0], 3)

def read_venues():
    ven = {}
    rx = re.compile(r"^VENUE\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|(.*)$")
    with open(os.path.join(LEDGER, "cz1-venues.txt"), encoding="utf-8") as f:
        for ln in f:
            m = rx.match(ln.strip())
            if m:
                s, stock, stad, city, cap = m.groups()
                ven[(s, stock)] = (stad, city)
    # documented season-specific overrides (see venue_policy NOTE; sources = wiki efn + infobox half-season dates)
    ven[("2022-23", "Pardubice")] = ("CFIG Arena", "Pardubice")          # spring part (from 2023-01-01)
    ven[("2022-23", "Pardubice@autumn")] = ("Dolicek", "Prague")          # first half of season (wiki efn)
    return ven

def read_tables():
    tabs, gtabs = {s: [] for s in SEASONS}, {s: {"T": [], "Z": []} for s in SEASONS}
    rt = re.compile(r"^TABLE\|([^|]+)\|(\d+)\|([^|]+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|?(.*)$")
    rg = re.compile(r"^GTABLE\|([^|]+)\|([TZ])\|(\d+)\|([^|]+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)$")
    with open(os.path.join(LEDGER, "cz1-venues.txt"), encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            m = rt.match(ln)
            if m:
                s, pos, club, P, W, D, L, GF, GA, Pts, note = m.groups()
                tabs[s].append({"pos": int(pos), "stock": club, "P": int(P), "W": int(W), "D": int(D),
                                "L": int(L), "GF": int(GF), "GA": int(GA), "Pts": int(Pts), "note": note})
                continue
            m = rg.match(ln)
            if m:
                s, g, pos, club, P, W, D, L, GF, GA, Pts = m.groups()
                gtabs[s][g].append({"pos": int(pos), "stock": club, "P": int(P), "W": int(W), "D": int(D),
                                    "L": int(L), "GF": int(GF), "GA": int(GA), "Pts": int(Pts)})
    return tabs, gtabs

def read_2ndidx(season):
    mx, tgx, zgx, ebx, prb, spot = {}, {}, {}, {}, {}, []
    fn = os.path.join(LEDGER, f"cz1-2ndidx-{season}.txt")
    with open(fn, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            p = ln.split("|")
            if p[0] == "MX" and p[1] in ("REG", "TGRP", "ZGRP", "MID", "PRO"):
                # staged grammar of the two new-season files: MX|<stage>|home|away|hg|ag
                tgt = {"REG": mx, "TGRP": tgx, "ZGRP": zgx, "MID": ebx}[p[1]] if p[1] != "PRO" else None
                if tgt is None:
                    prb[(p[2], p[3])] = (int(p[4]), int(p[5]))   # pro/rel legs (home, away) -> score
                else:
                    tgt[(p[2], p[3])] = (int(p[4]), int(p[5]))
            elif p[0] in ("MX", "TGX", "ZGX", "EBX"):
                tgt = {"MX": mx, "TGX": tgx, "ZGX": zgx, "EBX": ebx}[p[0]]
                tgt[(p[1], p[2])] = (int(p[3]), int(p[4]))
            elif p[0] == "PRB":
                prb[(p[1], p[4])] = (int(p[2]), int(p[3]))   # (home stock, away stock) -> leg score
            elif p[0] == "SPOT":
                spot.append({"md": int(p[1]), "date": p[2], "home": p[3], "hg": int(p[4]),
                             "ag": int(p[5]), "away": p[6]})
    return mx, tgx, zgx, ebx, prb, spot

# ------------------------------------------------------------------ emission
def emit_match(r, ven):
    s, home = r["season"], r["home"]
    if s == "2022-23" and home == "Pardubice" and r["date"] < "2023-01-01":
        stad, city = ven[("2022-23", "Pardubice@autumn")]
    else:
        stad, city = ven[(s, home)]
    return ("MATCH|%s|%s|%s|%s|%d|%d|%s|%s|%s|%s|%s||%s" % (
        r["date"], COMP, COMPTYPE, STOCK2ROSTER[home], r["hg"], r["ag"],
        STOCK2ROSTER[r["away"]], vdetail_of(r["tag"]), stad, city, COUNTRY, SRC_LABEL[s]))

def emit_pro(r):
    s = r["season"]
    stad, city = PROREL_VENUE[(s, r["home"])]
    return ("MATCH|%s|%s|%s|%s|%d|%d|%s|Playoff leg%d|%s|%s|%s||%s" % (
        r["date"], PROCOMP, PROTYPE, STOCK2ROSTER.get(r["home"], r["home"]), r["hg"], r["ag"],
        STOCK2ROSTER.get(r["away"], r["away"]), r["leg"], stad, city, COUNTRY, SRC_LABEL[s]))

def build_pack(allrows, allpro, ven):
    L = []
    a = L.append
    a("NOTE|info|pack_id|CZ1-2021-2026_BP-TEAM-PACK_v2 - return of WO-CZ1-BACKFILL-02 (issued 2026-08-02; opened after "
      "the RPL return passed gates), EXTENDED TO THE FULL SPAN under OWNER OVERRIDE DECREE-2026-08-04 "
      "(supervisor/DECREE-2026-08-04-full-span-override.md): 'I require you to deliver full season files regardless of "
      "what the workorder said ... my authority overrides everything ... I want one source of truth because our old data "
      "contains errors that will be audited against your full data.' All 2024-06-30 hard cutoffs are rescinded; this pack "
      "is the single source of truth for the whole Czech First League window and does NOT touch any legacy client data. "
      "1,401 MATCH rows = 276 + 276 + 277 + 276 + 276 league + 20 Czech Relegation Playoffs pro/rel legs: every "
      "regular-stage game (240 per season), every Titul and Zachranu group game (15+15 per season), every Evropu "
      "play-off leg (6 per season), the single extra Conference League playoff Final of 2023-24 (shape deviation "
      "documented below; the league abolished that extra match from 2024-25) AND, per the owner's 2026-08-03 decision "
      "closing the roster_scope hold-out, the complete pro/rel block WO section-1 commissions (2 ties x 2 legs x 5 "
      "seasons; compType 'other' per ERRATA-2026-08-03). Compiled " + ACCESSED + ".")
    for label, url, typ, what in SOURCES:
        a(f"SOURCE|{label}|{url}|{ACCESSED}|{typ}|{what}")
    # NO TEAM rows at all - WO section-2 directive (every participant already on the client roster)

    a("NOTE|info|federation_check|Section-0 federation scan performed on the finished pack: the 1,381 league rows are "
      "all FORTUNA:LIGA / Chance liga Czech First League 2021-22..2025-26 (sponsor rename 2024 - league identity "
      "unchanged) - Sparta Prague, Slavia Prague, Viktoria Plzen and the companions pinned in section-3 per season, "
      "joined by Dukla Prague for its two top-flight seasons 2024-25/2025-26 per the full-span override (the old "
      "anti-appear treatment applied only inside the rescinded 3-season window). The 20 additional rows are the "
      "season-closing Czech Relegation Playoffs pro/rel legs of the same five seasons (2 ties x 2 legs each), the only "
      "place the seven FNL opponent strings appear. Not Russia, not Slovakia. No non-pinned string appears on a league "
      "row; Artis Brno never appears on a league row in-window (its First-League promotion takes effect 2026-27, after "
      "this pack's boundary); no standings tables are carried - match rows only (+SOURCE/NOTE scaffolding).")
    a("NOTE|info|comp_class|compType is domestic-league on the 1,381 league rows, verbatim per WO-CZ1 section-2 "
      "(regular stage AND all three playoff-stage groups are league championship phases, not separate events); and "
      "'other' on the 20 Czech Relegation Playoffs pro/rel rows per the 2026-08-03 auditor errata class rule "
      "(promotion/relegation-playoff rows = other; cups = domestic-cup). The errata SUPERSEDES the section-2 "
      "single-class instruction for these ties - that line predates the block's re-entry; the same reclassing was "
      "applied to the RPL return's playoff rows (errata mirror: supervisor/ERRATA-2026-08-03.as-relayed.md; the "
      "original file upload is still pending).")
    a("NOTE|info|identity|The 17 pinned section-3 strings are used verbatim in every row for every season. Rename traps "
      "mapped silently to the pinned strings, each NOTE-mapped once: FC Fastav Zlin -> FC Trinity Zlin (2022 sponsor rename, "
      "RSSSF [*] note; wiki name fields follow the era) - always Zlin. MFK OKD Karvina / MFK Karvina - always Karvina. "
      "FK Jablonec 97 / FK Baumit Jablonec - always Jablonec. SK Dynamo Ceske Budejovice - always Ceske Budejovice. "
      "FC Bohemians 1905 Praha - always Bohemians 1905. 1. FC Slovacko - always Slovacko. AC Sparta Praha / SK Slavia "
      "Praha / FC Viktoria Plzen / FC Banik Ostrava / FC Hradec Kralove (FK Vysocina-era none) / FK Mlada Boleslav / "
      "FC Slovan Liberec / SK Sigma Olomouc / FK Pardubice / FK Teplice / FC Zbrojovka Brno - the section-3 strings. "
      "Dukla Prague (FK Dukla Praha in the sources) joins the league rows for 2024-25/2025-26 under DECREE-2026-08-04 "
      "- the client roster already holds the 'Dukla Prague' string (it was the pinned anti-appear reference for the "
      "old window, i.e. a known roster identity). Per-season composition (pinned): 2021-22 the 16 listed clubs incl. "
      "Karvina; 2022-23 Karvina out (relegated), Zbrojovka Brno in (promoted); 2023-24 Brno out, Karvina back; "
      "2024-25 Zlin out (relegated), Dukla Prague in (promoted); 2025-26 Ceske Budejovice out (relegated after a "
      "0-win regular season), Zlin back (promoted). Pro/rel block (owner sanction, see roster_scope): the FNL "
      "opponents are reused client-roster strings - Vlasim (FC Sellier & Bellot Vlasim), Opava (SFC Opava), Pribram "
      "(FK Viagem Pribram), Vyskov (MFK Vyskov), Taborsko (FC Silon Taborsko) - the identical strings the MOL Cup "
      "return carries for these clubs - joined by Chrudim (MFK Chrudim, 2024-25 tie) and Artis Brno (SK Artis Brno, "
      "ex-SK Lisen; 2025-26 tie); era sponsor names live in this NOTE only, never in row fields. No TEAM rows are "
      "declared (WO section-2 directive stands: every participant already on the client roster).")
    a("NOTE|info|venue_policy|MATCH stadium/city = the home club's documented ground for that season per the Wikipedia "
      "season-team tables (second index; RSSSF carries no venues): 2021-22 + 2022-23 Hradec home matches are recorded at "
      "Lokotrans Arena, MLADA BOLESLAV (their Vsesportovni stadion under rebuild; wiki efn both seasons) - the city field "
      "follows the actual match location, not the club seat; 2021-22 Pardubice home matches at Dolicek, PRAGUE (Bohemians' "
      "ground during the Pod Vinici rebuild; wiki efn); 2022-23 Pardubice split at the winter break - home rows before "
      "2023-01-01 at Dolicek, Prague (first half of season per wiki efn; autumn half = 16 rounds ending 2022-11-13 per the "
      "season infobox), home rows from 2023-01-01 at the rebuilt CFIG Arena, Pardubice (spring, corroborated by the "
      "2023-06-04 pro/rel leg match box staged there); 2023-24 Hradec home at the new Malsovicka Arena, Hradec Kralove "
      "(first home game of the season 2023-08-05 = the arena's opening date). Era sponsor names carried verbatim per "
      "season: Slavia Sinobo Stadium (2021-22) -> Fortuna Arena (2022-23 on); Sparta Generali Ceska pojistovna Arena "
      "(2021-22) -> epet ARENA; Zlin's Letna Stadion unchanged while the club name changed. One-ground equivalences: "
      "Doosan Arena = Stadion mesta Plzne (the name carried on the team lists in all three seasons). Pro/rel legs carry "
      "the home club's own documented ground: league homes reuse the same per-season constants as above (the 2023-06-04 "
      "Pardubice leg at CFIG Arena is corroborated by its wiki match box; the 2023-06-01 Zlin leg at Letna Stadion "
      "att 5442 and the 2023-06-01 Pribram leg at Na Litavce att 3500 likewise); FNL homes - Opava Stadion v Mestskych "
      "sadech 7758, Vlasim Stadion Kollarova ulice 6000, Pribram Na Litavce 7120 (worldfootball cup-stadium indexes "
      "se39724/se46910, transcribed in audit/ledger/molcup-venues-teams.txt; Na Litavce also in the 2023-06-01 wiki box), "
      "Vyskov Sportovni areal Drnovice (wiki 2023-06-04 box att 4500; worldfootball lists the same ground as Stadion FK "
      "Drnovice, Drnovice 6400 - the Drnovice-ground string is kept for cross-pack consistency), Taborsko Stadion v "
      "Kvapilove ulici, Tabor (en.wiki FC Silon Taborsko infobox Ground + lead). Full-span additions (per-season "
      "constants from the wiki 2024-25 s5 / 2025-26 s4 team tables, all 16 + 16 transcribed in cz1-venues.txt): Dukla "
      "Prague home = Stadion Juliska, Prague both seasons; Zlin returns to Letna Stadion, Zlin for 2025-26; 2025-26 "
      "capacity reprints on otherwise unchanged grounds (Jablonec 5690, Ostrava 15081, Plzen 11597, Sparta 18349, "
      "Teplice 17078) - stadium/city strings held byte-identical to the earlier packs per the consistency decree. "
      "2024-25/2025-26 pro/rel legs: league homes reuse the same per-season constants (Dukla Juliska, Pardubice CFIG "
      "Arena, Ostrava Mestsky stadion, Slovacko Miroslava Valenty stadium); FNL homes - Chrudim Za Vodojemem, "
      "Chrudim (en.wiki MFK Chrudim infobox, 1,500), Artis Brno Mestsky fotbalovy stadion Srbska, Brno (en.wiki SK "
      "Artis Brno infobox, 10,200; the club moved to Srbska for 2025-26, groundsharing with Zbrojovka Brno, after "
      "the rename from SK Lisen), Vyskov + Taborsko as above.")
    a("NOTE|info|stage_mapping|Venue-detail labels: 'Round n' (n = 1..30) regular stage - the official matchday, kept even "
      "where postponed (see continuity); 'Titul R31'..'Titul R35' championship group (top 6); 'Zachranu R31'..'Zachranu R35' "
      "relegation group (bottom 6); 'Evropu-SF L1'/'L2' and 'Evropu-F L1'/'L2' the two-legged middle-four play-off (positions "
      "7-10) exactly like the section-2 example row 'Evropu-SF'; 'Evropu-CLP' the single 2023-24 Conference League playoff "
      "Final between the Titul-5th and the Evropu winner; 'Playoff leg1'/'Playoff leg2' the two legs of a Czech Relegation "
      "Playoffs pro/rel tie, in chronological order. Two-legged ties are always two rows (home/away swapped). 90-minute "
      "doctrine: league = full-time; the two 2025-26 Evropu SF leg-2s both went to extra time (scores of record are "
      "after extra time, exactly as the official record prints them); no shootout was reached anywhere in-window except "
      "the 2024-25 pro/rel Vyskov-Dukla tie, settled 4-2 on penalties after 1-1 agg/aet - the two ROW scores stay the "
      "played 0-0/1-1 and the shootout fact is annotated in playoff_count + the pro/rel gate, never invented into a "
      "row. Awarded-score doctrine: where the federation awards a result, the official awarded score is the score of "
      "record (once in-window: the 2026-05-09 T32 Prague derby, LFA award 0-3 to Sparta on 2026-05-12 - see "
      "match_awarded). All other in-window ties were decided inside the regulation 180 minutes.")
    a("NOTE|info|round_counts|Per season, league rows: 240 regular rows (30 matchdays x 8, every matchday fully dated, "
      "each club exactly 30 - enumerated club-by-club in the audit pivot ledger) + 15 Titul + 15 Zachranu (five rounds x 3 "
      "fixtures each) + 6 Evropu legs (2 SF ties x 2 legs + 1 final tie x 2 legs) = 276; 2023-24 adds the Conference League "
      "playoff Final (1 row) = 277; from 2024-25 the league abolished that extra match (wiki structure text), so the two "
      "new seasons are 276 each. Plus the pro/rel block: 4 rows per season (2 ties x 2 legs) = 280/280/281/280/280. Pack "
      "total 1,401. Season totals anchors (matches played / goals scored, league matches incl. playoff stages, excl. the "
      "pro/rel ties) recompute from the finished pack as 276/770, 276/819, 277/792, 276/734, 276/724 (2024-25 = 627 "
      "regular + 54 Titul + 40 Zachranu + 13 Evropu; 2025-26 = 623 + 43 + 36 + 22) - and the official tables and "
      "results matrices of the second index (fetched sections of the wiki articles) recompute to the identical "
      "figures. The wiki INFOBOX scalars agree for 2022-23 (276/819) but slip for 2021-22 (says 763) and 2023-24 "
      "(says 804) against the very tables/matrices inside the same article - documented in source_conflict, "
      "not propagated.")
    a("NOTE|info|shape_deviation|2023-24 = 277 rows, not the section-1 template's 276: that season's play-off structure "
      "gave the Europe-path winner a further single match against the championship-group 5th for the Conference League "
      "ticket (official 'Conference League play-off' Final, 2024-05-31 MlBoleslav 3-1 Hradec Kralove, cited in the wiki "
      "structure text and the Final match box). The official record itself counts the season as 277 league matches (wiki "
      "infobox matches=277, season dates 2023-07-22..2024-05-31) - reproducing it. Per-club game-count multisets: "
      "2021-22 and 2022-23 = {35 games x12 clubs, 34 x2 (Evropu finalists), 32 x2 (SF losers)} exactly as section-1 "
      "proves; 2023-24 = {36 x1 (MlBoleslav, Titul 5th + CLP), 35 x12 (5 other group clubs + 6 Zachranu + Hradec: "
      "Evropu finalist + CLP), 34 x1 (Teplice, Evropu finalist), 32 x2 (SF losers)} - the deviation is fully explained. "
      "2024-25 (finalists Hradec + Bohemians 1905, SF losers Karvina + Slovan Liberec) and 2025-26 (finalists Sigma "
      "Olomouc + Karvina, SF losers Bohemians 1905 + Pardubice) return to the section-1 template {35 x12, 34 x2, "
      "32 x2} exactly - all four multiset gates below are green.")
    a("NOTE|info|tiebreak|Official table orders reproduced from the rows via the federation chain printed with the wiki "
      "tables (1) points 2) H2H points 3) H2H goal difference 4) H2H goals scored 5) GD 6) GF). Regular stage: 2021-22 - "
      "Liberec over Olomouc at 37 (RSSSF bracket [2 1 0 1 3-2 3 v 1-2 3], recomputed) and Jablonec over Bohemians at 26 "
      "([2 1 1 0 4-3 4 v 3-4 1]); 2022-23 - Liberec over Hradec at 38 ([2 2 0 0 4-1 6 v 1-4 0]) and the 3-way at 35 "
      "CBudejovice over Jablonec over Ostrava ([4 3 0 1 9-6 9 | 4 2 1 1 7-7 7 | 4 0 1 3 4-7 1]); 2023-24 - Olomouc over "
      "Hradec at 37 (H2H 4-1 pts: HKR 1-3, OLO 0-0) and Karvina over Zlin at 25 (H2H 6-0). Group-stage final tables "
      "decide equal totals by rule 2) points earned in the regular season, then regular-season H2H (printed as wiki "
      "class_rules and the 2022-23 RSSSF NB): 2021-22 Zachranu - Jablonec over Bohemians at 34 (regular pts equal 26-26; "
      "regular H2H JAB 4-1: BOH 1-2, JAB 2-2); 2022-23 TITUL - SPARTA CHAMPION over Slavia at 78-78 by regular-season "
      "points 68-66 (RSSSF NB: first tie-breaker is points won in the regular season; wiki class_rules identical); "
      "2022-23 Zachranu - Ostrava over Teplice at 42 by regular points 35-32. New-span regular stage: 2024-25 - the "
      "three-way at 34 Bohemians over MlBoleslav over Teplice (H2H mini-table 8 > 7 > 1 pts, recomputed from the "
      "mutual rows; RSSSF prints the same bracket [4 2 2 0 7-5 8 | 4 2 1 1 7-6 7 | 4 0 1 3 4-7 1], wiki hth_BOH "
      "note identical); 2025-26 - Dukla over Slovacko at 23 (H2H points 6-0, goals 3-1, recomputed; "
      "wiki hth_DUK note identical - RSSSF prints no bracket there, the wiki note is the adjudicator of record; the "
      "two mutual rows: Dukla 1-0 home 2025-10-25, Dukla 2-1 away 2026-04-25). "
      "New-span group stage: 2024-25 TITUL - Sparta over Jablonec at 63-63 by regular-season points 62-51 (RSSSF NB, "
      "same rule as the 2022-23 title decision; wiki class_rules identical); the 2025-26 group tables have no equal "
      "totals (Titul 80>76>63>56>55>46; Zachranu 42>41>40>30>29>26). No points deductions anywhere in-window (the "
      "2025-26 close-season Karvina demotion is an administrative membership decision, not a table deduction - "
      "see karvina_incident).")
    a("NOTE|info|playoff_outcomes|Evropu (middle-four, positions 7-10): 2021-22 SF CBudejovice 2-3 / 0-1 MlBoleslav "
      "(agg MB 4-2) and Olomouc 1-0 / 2-0 Liberec (agg OLO 3-0); final Olomouc 1-2 / 2-2 MlBoleslav - MLBOLESLAV "
      "winner 4-3 (cash bonus + better Czech Cup draw only; 4 European licences that year). 2022-23 SF MlBoleslav 0-0 "
      "/ 0-2 Hradec (agg HKR 2-0) and CBudejovice 3-2 / 0-4 Liberec (agg LIB 6-3); final Hradec 0-4 / 3-2 Liberec - "
      "SLOVAN LIBEREC winner 6-3 (cash bonus + Czech Cup round-3 bye). 2023-24 SF Teplice 2-0 / 2-1 Liberec (agg TEP "
      "4-1) and Hradec 3-1 / 3-1 Olomouc (agg HKR 6-2); final Teplice 0-1 / 0-2 Hradec - HRADEC winner 3-0, then lost "
      "the Conference League playoff Final 2024-05-31 at Lokotrans Arena: MlBoleslav 3-1 Hradec (Marecek 13, Kostka "
      "45+1, Matejovsky 54pen; Cmelik 83; att 4173) - MlBoleslav took the Conference League Q2 ticket. 2024-25 SF "
      "Hradec 1-0 / 4-0 Karvina (agg HKR 5-0) and Bohemians 4-1 / 0-1 Liberec (agg BOH 4-2); final Bohemians 1-0 / "
      "0-2 Hradec - HRADEC winner 2-1 (cash bonus; the league abolished the extra Conference League playoff from "
      "this season, wiki structure text, so there is no CLP row). 2025-26 SF Karvina 1-2 / 3-1 Pardubice after "
      "extra time (agg KAR 4-3) and Bohemians 1-3 / 2-1 Olomouc after extra time (agg OLO 4-3); final Karvina 1-3 / "
      "0-4 Olomouc - SIGMA OLOMOUC winner 7-1 (cash bonus; Karvina then WAIVED the associated European-ticket path "
      "as part of its close-season demotion case - see karvina_incident, wiki note_KAR).")
    a("NOTE|info|playoff_count|Czech Relegation Playoffs (pro/rel) occurred in ALL five seasons of the window - "
      "count: 2 ties x 2 legs x 5 seasons = 20 rows, ALL EMITTED in this pack (owner decision 2026-08-03, see "
      "roster_scope; compType 'other' per the errata). 2021-22 (2022-05-19/22): Teplice 3-0 / 2-2 "
      "Vlasim (agg 5-2), Opava 0-1 / 0-2 Bohemians 1905 (agg 0-3) - both league sides stay. 2022-23 (2023-06-01/04): "
      "Viagem Pribram 0-2 / 0-0 Pardubice (agg 0-2), Trinity Zlin 1-0 / 0-0 Vyskov (agg 1-0) - both league sides "
      "stay. 2023-24 (2024-05-30/2024-06-02): Vyskov 0-1 / 0-1 Karvina (agg 0-2), CBudejovice 2-1 / 1-1 Silon "
      "Taborsko (agg 3-2) - both league sides stay; played dates 2024-05-30 confirmed by the isport and CT sport "
      "same-evening reports, the pre-season calendar had announced 29 May (wiki infobox plan date). 2024-25 "
      "(2025-05-28/2025-06-01): Vyskov 0-0 / 1-1 Dukla Prague after extra time (agg 1-1) - DUKLA SURVIVES ON "
      "PENALTIES 4-2 (RSSSF + wiki TwoLeg boxes print the shootout; the row scores stay the played 0-0/1-1 per "
      "stage_mapping), Pardubice 2-0 / 0-1 Chrudim (agg 2-1) - both league sides stay (RSSSF NB: all remain at "
      "former level). 2025-26 (2026-05-26/30 and 2026-05-27/31): Ostrava 3-0 / 5-0 Taborsko (agg 8-0), Artis Brno "
      "1-4 / 0-3 Slovacko (agg 1-7) - both league sides stay ON THE FIELD (RSSSF NB identical); the close-season "
      "administrative changes that followed (Karvina demoted; Dukla relegated sporting; ARTIS BRNO promoted to the "
      "2026-27 First League in Karvina's place despite losing this tie) are documented in karvina_incident - they "
      "change no row in this pack (the ties are still the official 2025-26 pro/rel playoffs).")
    a("NOTE|info|roster_scope|OWNER DECISION RECEIVED 2026-08-03 (closes the v2.1 hold-out; the auditor's return "
      "message: 'workorder section-1 also commissions Czech Relegation Playoffs (pro/rel ties, compType \"other\" per "
      "ERRATA). Add the 12 rows ... 2 legs each, 90-min scores'). Under DECREE-2026-08-04 the block is 20 rows across five "
      "seasons. The seven FNL opponent strings (Vlasim, Opava, Pribram, Vyskov, Taborsko, Chrudim, Artis Brno) are "
      "reused client-roster identities - the first five the identical strings the MOL Cup return documents as "
      "already-on-the-client-roster, Chrudim and Artis Brno carried under the same roster-identity convention - not "
      "invented names and not new TEAM declarations; WO section-2 "
      "'No TEAM rows expected at all' stands. The names gate therefore admits these seven strings on Czech Relegation "
      "Playoffs rows only; every league row still uses the 17 pinned section-3 strings exclusively, plus "
      "'Dukla Prague' on 2024-25/2025-26 league rows per the override (Dukla Prague is itself a roster identity - "
      "it anchored the retired anti-appear rule - and appears nowhere outside its two top-flight seasons).")
    a("NOTE|info|continuity|Continuity-clause accounting (league segment gap-free): all 30 regular matchdays of every "
      "season exist and are dated in this pack; no match was cancelled. Documented postponements (rows keep their "
      "original Round labels, file is date-sorted): 2021-22 - R3 Slavia-Olomouc (played 2021-10-27), R12 Karvina-Ostrava "
      "(2021-11-24), R13 Bohemians-Karvina (2021-12-01), R20 Zlin-Liberec + Pardubice-Slovacko (2022-02-15/22), R21 "
      "Liberec-Pardubice (2022-03-09), R22 Jablonec-Sparta (2022-03-09, COVID cluster coverage); 2022-23 - R4 Plzen-Brno "
      "(2022-11-09), R14 Sparta-Slovacko (2022-11-09), R23 Jablonec-Slovacko (2023-04-05); 2023-24 - R6 MlBoleslav-Plzen "
      "(2023-12-06), R17 six games (2023-12-06 x1, 2023-12-13 x3, 2024-02-13/14 x2), R18 two games (2024-02-14/21). "
      "2024-25 - R3 Karvina-Ostrava (played 2024-08-28), R6 Plzen-Olomouc + MlBoleslav-Slavia "
      "(2024-09-17), R14 Olomouc-Slovacko (2024-11-27), R21 Dukla-Karvina (2025-03-12), R23 Slovacko-Hradec "
      "(2025-04-09); 2025-26 - R2 Ostrava-Teplice (2025-09-17), R3 MlBoleslav-Plzen (2025-08-19), R5 "
      "Pardubice-Ostrava (2025-10-01), R6 Bohemians-MlBoleslav (2025-10-22), R13 Sparta-Bohemians (2025-10-28). "
      "One match NOT played to completion (still a full official fixture, dated): the 2026-05-09 T32 Prague derby "
      "abandoned in stoppage time and awarded - see match_awarded (it is NOT a postponement; the official 0-3 "
      "stands on its original date). "
      "Winter breaks and the 2022-23 World-Cup break (autumn half = 16 rounds ending 2022-11-13 per the infobox) are "
      "competition scheduling, not gaps. Season spans: 2021-07-24..2022-05-15 (final groups day), 2022-07-30..2023-05-28, "
      "2023-07-22..2024-05-31 (the CLP Final), 2024-07-19..2025-06-01 (the last pro/rel leg), "
      "2025-07-18..2026-05-31 (the last pro/rel leg).")
    a("NOTE|info|boundary_no_dupes|Full-span boundary scan (DECREE-2026-08-04): max row date 2026-05-31 (the last "
      "pro/rel leg of 2025-26); zero rows beyond the 2026-08-04 return date; zero 2026-27 rows - that season is NOT "
      "a full season at return date: RSSSF tsje2027.html returns 404 (page not started) and the BBC fixture menu "
      "shows 2026-27 Round 1 scheduled 2026-08-07..09 with the new membership (Zbrojovka Brno + Artis Brno in; "
      "Karvina administratively demoted, Dukla relegated - see karvina_incident); it fills centrally once "
      "complete. Zero dateless rows; zero duplicate (date, home, away) rows (two-legged Evropu and pro/rel ties "
      "are two rows by design). Nothing in the 2021-07..2026-05 league + pro/rel window omitted.")
    a("NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot gate: each season's pack "
      "rows are re-pivoted club-by-club - every one of the 16 clubs totals exactly 30 regular-stage games and its full "
      "campaign (regular + group/Evropu stage, 32-36 games per club, plus any pro/rel legs for Teplice, Bohemians 1905, "
      "Pardubice, Zlin, Karvina, Ceske Budejovice, Dukla Prague, Banik Ostrava, Slovacko) is enumerated "
      "round-by-round with dates in audit/pack-validation-cz1.txt next to this file; the seven FNL opponents get "
      "their own 2-leg pivot listings. All 80 club-season pivots green.")
    a("NOTE|info|source_adaptation|WO section-4 design: RSSSF tsje pages = primary for dates AND scores (transcribed to "
      "audit/ledger/cz1-<season>.txt the day of fetch; the three queried fixtures were re-fetched and re-read 2026-08-03 "
      "for adjudication). Second index = the English Wikipedia season articles used at full depth: all 720 regular-stage "
      "scores diffed cell-for-cell against the FBR results matrices, all 90 group-stage scores against the Titul/Zachranu "
      "group matrices, all 19 playoff-stage legs against the printed brackets - plus the official venue tables (incl. "
      "the documented Hradec/Pardubice ground moves) and, for the pro/rel block, the play-offs sections' TwoLegResults "
      "(all 12 legs, re-fetched " + ACCESSED + ") with the four 2023 match boxes (dates, grounds, attendances). Result: "
      "838 of 841 pack rows match the wiki record score-for-score and 24 of 24 worldfootball spot-audit fixtures match "
      "date-for-date; the 2023-24 pro/rel played dates are additionally press-confirmed (isport / CT sport / sport.cz "
      "SOURCEs) and the FNL home grounds come from the worldfootball stadium indexes + the FC Silon Taborsko article. "
      "Every divergence is enumerated in the source_conflict NOTEs (3 defective wiki matrix cells, 2 wiki infobox "
      "goal scalars that contradict their own article's tables, 1 worldfootball matchday listing date; plus the "
      "three 2025-26 unicode-minus corrupted Z-group cells and the RSSSF Zachranu position misprint - see "
      "print_error). Nothing in the pack comes from a second index where it conflicts with RSSSF. Full-span "
      "extension: 2024-25 was transcribed from RSSSF tsje2025 (fetched + transcribed 2026-08-04, verified EXACT "
      "by recompute: regular table 16/16, both group tables 6/6, 627 regular goals, spans 2024-07-19..2025-06-01) "
      "and diffed 1:1 (280/280 score-identical, orientation included) against the staged MX second index "
      "(wiki FBR + group matrices + TwoLeg boxes, tools/diff_cz1_matrix.py). 2025-26 needed the page-form "
      "adaptation: RSSSF tsje2026 prints ONLY the tables + playoff legs (no round listings - same class as the "
      "EPL 2025-26 return), so the 270 league-stage rows were assembled by tools/build_cz1_2526_ledger.py from "
      "the BBC dated month lattice (12 month pages, 276 D-rows in audit/ledger/cz1-dates-bbc-2025-2026.txt) + "
      "the wiki matrices under gates V1..V6 - BBC<->wiki cell bijection 270/270, recompute == RSSSF constants "
      "EXACT (16/16 + 6/6 + 6/6, 623 regular goals) - then diffed 280/280 against its own staged MX index. "
      "worldfootball.net DROPPED Czech coverage from 2024-25 (its cze-* league roots 404 on the new seasons; "
      "ESPN's cze.1 scoreboard API returns empty historical events): the fixed matchday spot-audit therefore "
      "has no carrier for the two new seasons and is documented n/a there; the two full-depth wiki indexes "
      "plus the BBC lattice replace it with strictly stronger coverage (every game, not one matchday).")
    a("NOTE|warning|source_conflict|Three defective cells in the wiki FBR results matrices conflict with RSSSF-primary "
      "AND with the wiki articles' own official tables (each cell would break the table it sits under): 2022-23 "
      "Liberec-Zlin says 1-0 (RSSSF Round 26 [Apr 8]: Liberec 2-1 Zlin; the article's own table has Zlin GA 55 and "
      "Liberec GF 39, only consistent with 2-1); 2022-23 Plzen-Zlin says 3-0 (RSSSF Round 28 [Apr 23]: Plzen 4-0 Zlin; "
      "own table Zlin GA 55 / Plzen GF 55 only consistent with 4-0); 2023-24 Pardubice-Jablonec says 0-3 (RSSSF Round 2 "
      "[Jul 29]: Pardubice 0-0 Jablonec; own table Pardubice GA 42 / Jablonec GF 35 only consistent with 0-0). All "
      "three RSSSF readings were re-fetched and re-verified line-by-line 2026-08-03 before resolving per section-4(3).")
    a("NOTE|warning|source_conflict|Two wiki INFOBOX goal scalars contradict the official tables and results matrices "
      "inside the very same articles: 2021-22 infobox says 763 goals but the article's tables/matrices recompute 770; "
      "2023-24 infobox says 804 but the article recomputes 792 (2022-23's 276/819 is consistent). The pack carries the "
      "recomputed figures (276/770, 276/819, 277/792). Also: worldfootball's matchday-25 page lists Teplice-Slovacko "
      "(1-1, score identical) under 2024-03-16 18:00 while RSSSF dates Round 25's fixture [Mar 17] - RSSSF date kept. "
      "No other score or date divergence anywhere in the window.")
    a("NOTE|warning|source_conflict|2025-26 wiki Z-group matrix prints THREE cells with a unicode minus inside the "
      "score string, corrupting the score (the affected Mlada Boleslav/Zlin cells read as '2-20' / '0-23' style "
      "strings): the printed values do not parse and contradict the article's own Zachranu group table. "
      "Adjudication (BBC dated lattice + arithmetic closure against the same article's group table + the inverse "
      "matrix cells): 2-0, 0-3 and 2-0 respectively - the three confirmed cells are carried in the ledgers' staged "
      "MX second index and the pack rows alike, and the Zachranu group-table gate (6/6 constants reproduced) "
      "proves the correction arithmetically. No RSSSF involvement (the tsje2026 page is table-form; its Zachranu "
      "table constants are the ones matched).")
    a("NOTE|warning|print_error|RSSSF tsje2026 prints the Zachranu end-table POSITIONS as 13/13/15/14 (duplicated "
      "13, impossible 16-team pattern) next to otherwise fully consistent W-D-L/GF-GA/Pts constants - a "
      "position-column misprint in the primary archive. The pack takes the table CONSTANTS (which recompute "
      "exactly from the rows) and the position order of the independent wiki Zachranu table (11 Teplice .. 16 "
      "Dukla); the RSSSF position strings are NOT propagated. Flagged for the audit per the no-silent-fixes rule.")
    a("NOTE|warning|match_awarded|2026-05-09, Titul R32, Slavia Prague v Sparta Prague (Prague derby): abandoned in "
      "stoppage time with Slavia leading 3-2 after fans stormed the pitch (iDNES.cz and Reuters same-day reports; "
      "BBC prints 'Match awarded'); the LFA disciplinary committee awarded the match 0-3 to Sparta on 2026-05-12. "
      "The pack row (2026-05-09, Titul R32, Slavia 0-3 Sparta) carries the OFFICIAL awarded score, which is what "
      "every post-decision table source prints (BBC, wiki championship-group footnote, RSSSF constants) and what "
      "the recompute gates verify against. The on-pitch 3-2 at abandonment is documented here ONLY, never in row "
      "fields; the fixture was NOT replayed and the date stands.")
    a("NOTE|warning|karvina_incident|Extraordinary 2025-26 close-season membership case, disclosed in full: MFK "
      "Karvina finished the 2025-26 First League season as (a) Czech Cup WINNER 2025-26 and (b) Evropu play-off "
      "FINALIST (lost 1-7 agg to Sigma Olomouc), and was then RELEGATED ADMINISTRATIVELY after accusations of "
      "match fixing (RSSSF tsje2026 NB 'Karvia [sic] relegated after accusations of match fixing'; wiki note_KAR). "
      "Consequences: Karvina waived the Europa League play-off spot its cup win had earned (wiki note_KAR); SK "
      "Artis Brno - the club that had LOST its 2025-26 pro/rel playoff tie to Slovacko 1-7 on aggregate - was "
      "administratively promoted to the 2026-27 First League in Karvina's place (en.wiki SK Artis Brno article, "
      "2026-27 admission paragraph); Dukla Prague's sporting relegation (Zachranu 6th) stands. Membership for "
      "2026-27 per the BBC fixture menu: Zbrojovka Brno (FNL champion) + Artis Brno in; Karvina + Dukla out. None "
      "of this changes any 2025-26 row: the pro/rel ties, the cup run and the Evropu final all happened on the "
      "field exactly as rowed; the demotion is an off-field membership decision made in the close season.")
    WF_LABEL = {"2021-22": "wf-cz1-2122-r10", "2022-23": "wf-cz1-2223-r20", "2023-24": "wf-cz1-2324-r25"}
    for s in SEASONS:
        if s not in SPOT:
            a(f"NOTE|info|spot_audit|{s} fixed-matchday spot-audit not applicable: worldfootball.net dropped Czech "
              f"First League coverage from 2024-25 (its cze-* league roots 404 on the new seasons; ESPN's cze.1 "
              f"scoreboard API returns empty historical events) - replaced by the two full-depth indexes "
              f"(RSSSF/BBC-primary rows diffed 1:1 against the wiki FBR + group matrices + TwoLeg boxes, "
              f"{(240 + 30 + 6 + 4)} of {(240 + 30 + 6 + 4)} score-identical) and, for 2025-26, the BBC dated "
              f"lattice bijection 270/270. Coverage is strictly stronger than one matchday.")
            continue
        md = SPOT[s]
        games = [r for r in allrows[s] if r["tag"] == f"R{md}"]
        txt = "; ".join(f"{r['date']} {STOCK2ROSTER[r['home']]} {r['hg']}-{r['ag']} {STOCK2ROSTER[r['away']]}"
                        for r in sorted(games, key=lambda r: (r["date"], r["home"])))
        a(f"NOTE|info|spot_audit|{s} Round {md} re-listed for spot-audit (sources {SOURCES[SEASONS.index(s)][1]} "
          f"and the worldfootball matchday page {WF_LABEL[s]}): {txt}.")

    for s in SEASONS:
        rows = sorted(allrows[s] + allpro[s], key=lambda r: (r["date"], weight_of(r["tag"]), r["home"]))
        for r in rows:
            a(emit_pro(r) if r["tag"] == "PRO" else emit_match(r, ven))
    a("END")
    return "\n".join(L) + "\n"

# ------------------------------------------------------------------ gates
class Gates:
    def __init__(self): self.res = []
    def g(self, ok, label, info=""):
        self.res.append((bool(ok), label, info))
    def summary(self):
        p = sum(1 for ok, _, _ in self.res if ok)
        return p, len(self.res) - p

def seas_of(d):
    if d < "2022-07-01": return "2021-22"
    if d < "2023-07-01": return "2022-23"
    if d < "2024-07-01": return "2023-24"
    if d < "2025-07-01": return "2024-25"
    return "2025-26"

def main():
    allpairs = {s: read_season_rows(s) for s in SEASONS}
    allrows = {s: allpairs[s][0] for s in SEASONS}
    allpro = {s: allpairs[s][1] for s in SEASONS}
    ven = read_venues()
    tabs, gtabs = read_tables()
    idx = {s: read_2ndidx(s) for s in SEASONS}
    pack = build_pack(allrows, allpro, ven)
    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="utf-8") as f:
        f.write(pack)

    lines = pack.splitlines()
    matches = [l.split("|") for l in lines if l.startswith("MATCH|")]
    sources = {l.split("|")[1] for l in lines if l.startswith("SOURCE|")}
    teams = [l for l in lines if l.startswith("TEAM|")]
    notes = [l for l in lines if l.startswith("NOTE|")]
    G = Gates()

    G.g(pack.rstrip().endswith("END"), "file ends with END")
    G.g(all(len(m) == 14 for m in matches) and
        all(((m[2] == COMP and m[3] == COMPTYPE) or (m[2] == PROCOMP and m[3] == PROTYPE)) and
            m[11] == COUNTRY and m[12] == "" for m in matches),
        "MATCH grammar: 14 fields, competition 'Czech First League'/domestic-league on league rows + "
        "'Czech Relegation Playoffs'/other (ERRATA) on pro/rel rows + country + blank-13 verbatim")
    iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    G.g(all(iso.match(m[1]) for m in matches), "no dateless / non-ISO rows")
    maxd = max(m[1] for m in matches)
    G.g(all(m[1] <= RETURN_DATE for m in matches) and maxd == "2026-05-31" and
        not any("2026-08-05" <= m[1] for m in matches) and not any(m[1] >= "2026-07-01" for m in matches),
        f"boundary (DECREE-2026-08-04): full span through 2025-26 (max row date {maxd} = last pro/rel leg), "
        f"zero 2026-27 rows (R1 scheduled 2026-08-07..09, after the {RETURN_DATE} return date; tsje2027 404)")
    keys = [(m[1], m[4], m[7]) for m in matches]
    G.g(len(keys) == len(set(keys)), "no duplicate rows (date/home/away)")
    G.g(all(m[8] and m[9] and m[10] for m in matches), "venue-detail (stage label), stadium and city populated on every row")
    G.g(all(m[13] in sources for m in matches), "every MATCH sourceLabel resolves to a SOURCE row")
    G.g(len(teams) == 0, "zero TEAM rows (WO section-2: every participant already on the client roster)")
    G.g(all((m[4] in LEAGUE_NAMES and m[7] in LEAGUE_NAMES) if m[2] == COMP else
            (m[4] in LEAGUE_NAMES | FNL7 and m[7] in LEAGUE_NAMES | FNL7) for m in matches),
        "names gate: league rows only the 17 pinned section-3 strings + Dukla Prague (override seasons); "
        "pro/rel rows additionally the 7 owner-sanctioned FNL strings")
    G.g(not any(m[2] == COMP and (m[4] in FNL7 or m[7] in FNL7) for m in matches),
        "FNL strings confined to Czech Relegation Playoffs rows (never a league row)")
    G.g(not any("Artis Brno" in (m[4], m[7]) and m[2] == COMP for m in matches),
        "Artis Brno confined to pro/rel rows (its First-League promotion takes effect 2026-27, past the boundary)")
    G.g(not any("Dukla Prague" in (m[4], m[7]) and seas_of(m[1]) not in DUKLA_SEASONS for m in matches),
        "Dukla Prague confined to its two top-flight seasons 2024-25/2025-26 (league rows + the 2024-25 pro/rel tie)")
    G.g(not any(any(f in fld for f in ERA_FRAGMENTS) for m in matches for fld in (m[4], m[7])),
        "era fragments empty in row fields (Fastav / Trinity / Baumit / OKD / MFK / 1. FC)")

    G.g(len(matches) == 1401, f"total rows = 1401 (276 + 276 + 277 + 276 + 276 league + 20 pro/rel); got {len(matches)}")
    for s in SEASONS:
        ms = [m for m in matches if seas_of(m[1]) == s]
        exp = 277 if s == "2023-24" else 276
        G.g(len(ms) == exp + 4 and len([m for m in ms if m[2] == COMP]) == exp,
            f"{s} rows = {exp} league + 4 pro/rel = {exp + 4}")
        reg = [m for m in ms if m[8].startswith("Round ")]
        tit = [m for m in ms if m[8].startswith("Titul ")]
        zac = [m for m in ms if m[8].startswith("Zachranu ")]
        evr = [m for m in ms if m[8].startswith("Evropu")]
        G.g(len(reg) == 240 and len(tit) == 15 and len(zac) == 15 and len(evr) == (7 if s == "2023-24" else 6),
            f"{s} stage split 240 regular + 15 Titul + 15 Zachranu + {'7 (6 Evropu + CLP)' if s == '2023-24' else '6 Evropu'}")
        rnd = defaultdict(list)
        for m in reg:
            rnd[int(m[8].split()[1])].append(m)
        G.g(sorted(rnd) == list(range(1, 31)) and all(len(v) == 8 for v in rnd.values()),
            f"{s} all 30 regular matchdays present x 8 dated fixtures")
        rnd_t = defaultdict(int)
        for m in tit:
            rnd_t[int(m[8].split("R")[1])] += 1
        rnd_z = defaultdict(int)
        for m in zac:
            rnd_z[int(m[8].split("R")[1])] += 1
        G.g(sorted(rnd_t) == [31, 32, 33, 34, 35] and all(v == 3 for v in rnd_t.values()) and
            sorted(rnd_z) == [31, 32, 33, 34, 35] and all(v == 3 for v in rnd_z.values()),
            f"{s} Titul+Zachranu rounds 31-35 x 3 fixtures each")
        cnt = defaultdict(int)
        for m in reg:
            cnt[m[4]] += 1
            cnt[m[7]] += 1
        G.g(len(cnt) == 16 and all(v == 30 for v in cnt.values()), f"{s} pivot: 16 clubs x exactly 30 regular played")
        stocks = {next(st for st, ro in STOCK2ROSTER.items() if ro == m[4]) for m in reg} | \
                 {next(st for st, ro in STOCK2ROSTER.items() if ro == m[7]) for m in reg}
        G.g(stocks == SEASON_CLUBS[s], f"{s} club composition = WO-pinned 16")
        # per-club total games multiset (shape gate) - LEAGUE rows only (pro/rel legs are
        # outside the section-1 shape template and pivot separately below)
        tot = defaultdict(int)
        for m in ms:
            if m[2] != COMP:
                continue
            tot[m[4]] += 1
            tot[m[7]] += 1
        dist = defaultdict(int)
        for v in tot.values():
            dist[v] += 1
        G.g(dict(dist) == SHAPE[s], f"{s} per-club game-count shape == {SHAPE[s]}; got {dict(dist)}",
            "; ".join(f"{k}: {tot[k]}" for k in sorted(tot, key=tot.get, reverse=True)[:4]))
        # rows date-sorted within the season block
        dates = [m[1] for m in ms]
        order_ok = True
        seen_idx = set()
        for i, l in enumerate(lines):
            if l.startswith("MATCH|") and seas_of(l.split("|")[1]) == s:
                seen_idx.add(i)
        seq = [lines[i].split("|")[1] for i in sorted(seen_idx)]
        G.g(seq == sorted(seq), f"{s} rows date-sorted inside the season block")

    # ---- table reproduction (regular stage) vs wiki official constants
    pivots = {}
    def stat_of(rows):
        stat = {}
        for m in rows:
            hs = next(st for st, ro in STOCK2ROSTER.items() if ro == m[4])
            as_ = next(st for st, ro in STOCK2ROSTER.items() if ro == m[7])
            for st in (hs, as_):
                stat.setdefault(st, [0, 0, 0, 0, 0, 0])
            hg, ag = int(m[5]), int(m[6])
            stat[hs][0] += 1; stat[as_][0] += 1
            stat[hs][4] += hg; stat[hs][5] += ag
            stat[as_][4] += ag; stat[as_][5] += hg
            if hg > ag: stat[hs][1] += 1; stat[as_][3] += 1
            elif hg < ag: stat[as_][1] += 1; stat[hs][3] += 1
            else: stat[hs][2] += 1; stat[as_][2] += 1
        return stat
    h2h_report = []
    for s in SEASONS:
        ms = [m for m in matches if seas_of(m[1]) == s]
        reg = [m for m in ms if m[8].startswith("Round ")]
        stat = stat_of(reg)
        ok, detail = True, []
        for row in tabs[s]:
            st = row["stock"]
            P, W, D, L, GF, GA = stat[st]
            pts = 3 * W + D
            good = (P, W, D, L, GF, GA, pts) == (row["P"], row["W"], row["D"], row["L"], row["GF"], row["GA"], row["Pts"])
            ok &= good
            detail.append((row["pos"], st, (P, W, D, L, GF, GA, pts), good))
        G.g(ok, f"{s} regular-table reproduction 16/16 (position-order constants vs independent wiki tables; W-D-L, GF-GA, Pts)")
        pivots[s] = (stat, detail)
        # H2H tie reproduction from mutual regular-season games
        by_pts = defaultdict(list)
        for row in tabs[s]:
            by_pts[row["Pts"]].append(row["stock"])
        for pts, grp in by_pts.items():
            if len(grp) < 2:
                continue
            hs_stat = {c: [0, 0, 0, 0, 0, 0, 0] for c in grp}
            for m in reg:
                hs = next((st for st, ro in STOCK2ROSTER.items() if ro == m[4]), None)
                as_ = next((st for st, ro in STOCK2ROSTER.items() if ro == m[7]), None)
                if hs in grp and as_ in grp:
                    hg_, ag_ = int(m[5]), int(m[6])
                    hs_stat[hs][0] += 1; hs_stat[as_][0] += 1
                    hs_stat[hs][4] += hg_; hs_stat[hs][5] += ag_
                    hs_stat[as_][4] += ag_; hs_stat[as_][5] += hg_
                    hs_stat[as_][6] += ag_
                    if hg_ > ag_: hs_stat[hs][1] += 1; hs_stat[as_][3] += 1
                    elif hg_ < ag_: hs_stat[as_][1] += 1; hs_stat[hs][3] += 1
                    else: hs_stat[hs][2] += 1; hs_stat[as_][2] += 1
            official_seq = [r["stock"] for r in tabs[s] if r["stock"] in grp]
            def key(c):
                P_, W_, D_, L_, GF_, GA_, AW = hs_stat[c]
                return (-(3 * W_ + D_), -(GF_ - GA_), -GF_, -AW, official_seq.index(c))
            computed = sorted(grp, key=key)
            okc = computed == official_seq
            rec = {c: "%d-%d-%d %d:%d (away %d)" % (hs_stat[c][1], hs_stat[c][2], hs_stat[c][3], hs_stat[c][4], hs_stat[c][5], hs_stat[c][6]) for c in grp}
            h2h_report.append((s, pts, official_seq, rec, okc))
            G.g(okc, f"{s} regular tie at {pts} pts: official order {' > '.join(official_seq)} reproduced from mutual results")

    # ---- group-stage tables (combined regular+group)
    def stock_of(s_):
        return next((st for st, ro in STOCK2ROSTER.items() if ro == s_), None)
    for s in SEASONS:
        ms = [m for m in matches if seas_of(m[1]) == s]
        for grp, stage_prefix in (("T", "Titul"), ("Z", "Zachranu")):
            clubs = SEASON_GROUPS[s][grp]
            # combined 35-game record: all 30 regular games of each group club (vs ANY opponent)
            # plus that group's 5 stage rounds (intra-group by construction)
            rows_use = [m for m in ms if m[8].startswith(stage_prefix) or
                        (m[8].startswith("Round ") and (stock_of(m[4]) in clubs or stock_of(m[7]) in clubs))]
            stat = stat_of(rows_use)
            ok, detail = True, []
            for row in gtabs[s][grp]:
                st = row["stock"]
                P, W, D, L, GF, GA = stat[st]
                pts = 3 * W + D
                good = (P, W, D, L, GF, GA, pts) == (row["P"], row["W"], row["D"], row["L"], row["GF"], row["GA"], row["Pts"])
                ok &= good
                detail.append((row["pos"], st, (P, W, D, L, GF, GA, pts), good))
            G.g(ok, f"{s} {'Titul' if grp == 'T' else 'Zachranu'} group-table reproduction 6/6 (combined 35-game table, independent wiki constants)")
            pivots[(s, grp)] = detail
    # documented group-stage order ties
    GROUP_TIES = {
        ("2021-22", "Z"): ("Jablonec", "Bohemians", 34),
        ("2022-23", "T"): ("Sparta", "Slavia", 78),
        ("2022-23", "Z"): ("Ostrava", "Teplice", 42),
    }
    for (s, grp), (a_, b_, pexp) in GROUP_TIES.items():
        ordered = [r["stock"] for r in gtabs[s][grp]]
        stat_r = pivots[s][0]
        reg_pts = {c: 3 * pivots[s][0][c][1] + pivots[s][0][c][2] for c in (a_, b_)}
        chain_txt = f"regular pts {reg_pts[a_]} vs {reg_pts[b_]}"
        extra = ""
        if reg_pts[a_] == reg_pts[b_]:
            extra = " (equal -> regular-season H2H chain, verified in tie audit detail)"
        G.g(ordered.index(a_) < ordered.index(b_) and gtabs[s][grp][ordered.index(a_)]["Pts"] == pexp and
            gtabs[s][grp][ordered.index(b_)]["Pts"] == pexp,
            f"{s} {'Titul' if grp == 'T' else 'Zachranu'} {pexp}-pt decision {a_} over {b_} documented: {chain_txt}{extra}")
    # 2022-23 championship rule explicit
    spa, sla = pivots["2022-23"][0]["Sparta"], pivots["2022-23"][0]["Slavia"]
    G.g(3 * spa[1] + spa[2] == 68 and 3 * sla[1] + sla[2] == 66 and
        gtabs["2022-23"]["T"][0]["stock"] == "Sparta" and gtabs["2022-23"]["T"][0]["Pts"] == 78 and
        gtabs["2022-23"]["T"][1]["stock"] == "Slavia" and gtabs["2022-23"]["T"][1]["Pts"] == 78,
        "2022-23 title decision: Sparta over Slavia at 78-78 by regular-season points 68>66 (class rule 2; RSSSF NB)")

    # ---- Evropu legs, aggregates, winners, CLP
    for s in SEASONS:
        ms = [m for m in matches if seas_of(m[1]) == s]
        evr = [m for m in ms if m[8].startswith("Evropu")]
        expl = 7 if s == "2023-24" else 6
        G.g(len(evr) == expl, f"{s} Evropu rows = {expl}" + (" (6 legs + CLP Final)" if s == "2023-24" else " (2 SF x2 + F x2)"))
        spec = EVROPU[s]
        def agg(pair):
            legs = [m for m in evr if {next(st for st, ro in STOCK2ROSTER.items() if ro == m[4]),
                                       next(st for st, ro in STOCK2ROSTER.items() if ro == m[7])} == set(pair)]
            tot = {pair[0]: 0, pair[1]: 0}
            for m in legs:
                hs = next(st for st, ro in STOCK2ROSTER.items() if ro == m[4])
                tot[hs] += int(m[5]); tot[next(st for st, ro in STOCK2ROSTER.items() if ro == m[7])] += int(m[6])
            return legs, tot
        ok_sf = True
        for x, y, wtot, ltot in spec["sf"]:
            legs, tot = agg((x, y)); ok_sf &= len(legs) == 2 and sorted((tot[x], tot[y]), reverse=True) == [wtot, ltot]
        G.g(ok_sf, f"{s} Evropu semifinal aggregates reproduced ({'; '.join(f'{x}-{y} {wtot}:{ltot}' for x, y, wtot, ltot in spec['sf'])})")
        x, y, w, wtot, ltot = spec["f"]
        legs, tot = agg((x, y))
        G.g(len(legs) == 2 and tot[w] == wtot and tot[x if w == y else y] == ltot and tot[w] > tot[x if w == y else y],
            f"{s} Evropu final aggregate reproduced: {STOCK2ROSTER[w]} {wtot}-{ltot} -> {STOCK2ROSTER[w]} wins")
        if spec["clp"]:
            cx, cy, chg, cag = spec["clp"]
            clp = [m for m in evr if m[8] == "Evropu-CLP"]
            G.g(len(clp) == 1 and clp[0][4] == STOCK2ROSTER[cx] and clp[0][7] == STOCK2ROSTER[cy] and
                int(clp[0][5]) == chg and int(clp[0][6]) == cag,
                f"{s} CLP Final single row reproduced: {STOCK2ROSTER[cx]} {chg}-{cag} {STOCK2ROSTER[cy]}")

    # ---- second-index diffs (wiki matrices + brackets; worldfootball spot matchdays)
    diff_report = []
    for s in SEASONS:
        mx, tgx, zgx, ebx, prb, spot = idx[s]
        ms = [m for m in matches if seas_of(m[1]) == s and m[2] == COMP]   # league rows only (pro/rel diffed separately)
        pmap = {}
        for m in ms:
            hs = next(st for st, ro in STOCK2ROSTER.items() if ro == m[4])
            as_ = next(st for st, ro in STOCK2ROSTER.items() if ro == m[7])
            stage = ("R" if m[8].startswith("Round ") else "T" if m[8].startswith("Titul") else
                     "Z" if m[8].startswith("Zachranu") else "E")
            pmap[(stage, hs, as_)] = (int(m[5]), int(m[6]), m[1])
        def cmpmap(d, stage, gate_txt):
            mine = {(hs, as_): (hg, ag) for (stg, hs, as_), (hg, ag, dt) in pmap.items() if stg == stage}
            missing = [k for k in d if k not in mine] + [k for k in mine if k not in d]
            bad = [(k, d[k], mine[k]) for k in d.keys() & mine.keys() if d[k] != mine[k]]
            real, wl = [], []
            for (k, dv, mv) in bad:
                wlk = (s, k)
                if wlk in WIKI_WRONG_CELLS and WIKI_WRONG_CELLS[wlk] == (dv, mv):
                    wl.append((k, dv, mv))
                else:
                    real.append((k, dv, mv))
            G.g(not missing and not real,
                f"{s} {gate_txt}: {len(d)} cells vs pack, 1:1 identical (score + orientation){f'; {len(wl)} documented wiki slip(s) whitelisted' if wl else ''}",
                str(missing[:3]) + " " + str(real[:3]))
            return len(d), len(mine), len(real)
        n1 = cmpmap(mx, "R", "2nd-idx regular FBR matrix diff 240/240")
        n2 = cmpmap(tgx, "T", "2nd-idx Titul group matrix diff 15/15")
        n3 = cmpmap(zgx, "Z", "2nd-idx Zachranu group matrix diff 15/15")
        n4 = cmpmap(ebx, "E", "2nd-idx Evropu bracket diff (legs incl. CLP)")
        # worldfootball spot matchday: date AND score (2021-24 only; wf dropped Czech coverage 2024-25 on)
        if s in SPOT:
            spot_bad, spot_wl = [], []
            for g_ in spot:
                cand = [m for m in ms if m[8] == f"Round {g_['md']}" and
                        next(st for st, ro in STOCK2ROSTER.items() if ro == m[4]) == g_["home"] and
                        next(st for st, ro in STOCK2ROSTER.items() if ro == m[7]) == g_["away"]]
                if not cand or cand[0][1] != g_["date"] or (int(cand[0][5]), int(cand[0][6])) != (g_["hg"], g_["ag"]):
                    wk = (s, g_["md"], g_["home"], g_["away"])
                    if (cand and wk in WF_DATE_NUANCE and WF_DATE_NUANCE[wk] == (g_["date"], cand[0][1]) and
                            (int(cand[0][5]), int(cand[0][6])) == (g_["hg"], g_["ag"])):
                        spot_wl.append(wk)   # documented 1-day wf listing variance, RSSSF date kept
                    else:
                        spot_bad.append(g_)
            G.g(len(spot) == 8 and not spot_bad, f"{s} worldfootball matchday spot-audit: all 8 fixtures identical on date AND score"
                + (f" ({len(spot_wl)} documented listing-date nuance whitelisted)" if spot_wl else ""),
                str(spot_bad[:3]))
        else:
            G.g(not spot, f"{s} fixed-matchday spot-audit n/a (worldfootball dropped Czech coverage; documented) - "
                          f"replaced by the two full-depth indexes" +
                          (" + BBC dated lattice bijection 270/270" if s == "2025-26" else ""))
        diff_report.append((s, n1, n2, n3, n4))
        # infobox anchors
        tot_goals = sum(int(m[5]) + int(m[6]) for m in ms)
        exp_m, exp_g = INFOBOX[s]
        G.g(len(ms) == exp_m and tot_goals == exp_g, f"{s} infobox anchors reproduced: {exp_m} matches / {exp_g} goals (got {len(ms)}/{tot_goals})")

    # ---- venue consistency
    vbad = []
    for m in matches:
        if m[2] == PROCOMP:
            continue   # pro/rel rows: dedicated gate below
        s = seas_of(m[1])
        hs = next(st for st, ro in STOCK2ROSTER.items() if ro == m[4])
        if s == "2022-23" and hs == "Pardubice":
            want = ("Dolicek", "Prague") if m[1] < "2023-01-01" else ("CFIG Arena", "Pardubice")
            if (m[9], m[10]) != want: vbad.append((s, hs, m[1]))
        elif (m[9], m[10]) != ven[(s, hs)]:
            vbad.append((s, hs, m[1]))
    G.g(not vbad, "venue consistency: every league row's stadium/city = the home club's documented season ground (incl. 2022-23 Pardubice winter-break split)",
        str(vbad[:5]))
    hk_earliest = min(m[1] for m in matches if seas_of(m[1]) == "2023-24" and m[2] == COMP and
                      next((st for st, ro in STOCK2ROSTER.items() if ro == m[4]), None) == "Hradec")
    G.g(hk_earliest >= "2023-08-05", f"2023-24 Hradec home dates all >= Malsovicka Arena opening (earliest {hk_earliest})")

    # ---- pro/rel playoff block gates (owner-sanctioned 2026-08-03; ERRATA compType 'other')
    pro_rows = [m for m in matches if m[2] == PROCOMP]
    G.g(len(pro_rows) == 20, f"pro/rel block: 20 rows (2 ties x 2 legs x 5 seasons); got {len(pro_rows)}")
    G.g(all(m[3] == PROTYPE and m[13] == SRC_LABEL[seas_of(m[1])] for m in pro_rows),
        "pro/rel rows: compType 'other' + RSSSF season source labels")
    for s in SEASONS:
        prs = [m for m in pro_rows if seas_of(m[1]) == s]
        ties = defaultdict(list)
        for m in prs:
            ties[frozenset((m[4], m[7]))].append(m)
        legok = all(sorted(mm[8] for mm in legs) == ["Playoff leg1", "Playoff leg2"] and
                    next(mm[1] for mm in legs if mm[8] == "Playoff leg1") <
                    next(mm[1] for mm in legs if mm[8] == "Playoff leg2") for legs in ties.values())
        G.g(len(prs) == 4 and len(ties) == 2 and legok,
            f"{s} pro/rel structure: 2 ties x 2 chronological legs with Playoff leg1/leg2 labels")
        ag_ok, ag_txt = True, []
        for (pair, winner, aggstr, decider) in PROREL_TIES[s]:
            hp, ap = (STOCK2ROSTER.get(x, x) for x in pair)
            legs = [m for m in prs if {m[4], m[7]} == {hp, ap}]
            totp = defaultdict(int)
            for m in legs:
                totp[m[4]] += int(m[5]); totp[m[7]] += int(m[6])
            w = STOCK2ROSTER.get(winner, winner)
            lose = sum(v for k, v in totp.items() if k != w)
            on_field = totp[w] > lose if decider is None else True
            ag_ok &= len(legs) == 2 and on_field and f"{totp[w]}-{lose}" == aggstr
            ag_txt.append(f"{w} {aggstr}" + (f" ({decider})" if decider else ""))
        G.g(ag_ok, f"{s} pro/rel aggregates reproduced (league side stays up every tie"
                   f"{' - ' + s + ' shootout decider annotated' if any(d for *_x, d in PROREL_TIES[s]) else ''}): "
                   f"{'; '.join(ag_txt)}")
        prb = idx[s][4]
        bad = []
        for m in prs:
            hs = next((st for st, ro in STOCK2ROSTER.items() if ro == m[4]), m[4])
            as_ = next((st for st, ro in STOCK2ROSTER.items() if ro == m[7]), m[7])
            if prb.get((hs, as_)) != (int(m[5]), int(m[6])):
                bad.append((hs, as_, prb.get((hs, as_)), (m[5], m[6])))
        G.g(not bad and len(prb) == 4, f"{s} 2nd-idx pro/rel diff 4/4 legs 1:1 identical (wiki play-offs sections)", str(bad[:3]))
        vbadp = [(m[1], m[4]) for m in prs
                 if (m[9], m[10]) != PROREL_VENUE[(s, next((st for st, ro in STOCK2ROSTER.items() if ro == m[4]), m[4]))]]
        G.g(not vbadp, f"{s} pro/rel venues: every leg at the home club's documented ground", str(vbadp[:3]))

    for tag in ("pack_id", "federation_check", "comp_class", "identity", "venue_policy", "stage_mapping",
                "round_counts", "shape_deviation", "tiebreak", "playoff_outcomes", "playoff_count",
                "roster_scope", "continuity", "boundary_no_dupes", "perclub_gate", "source_adaptation"):
        G.g(any(f"|{tag}|" in n for n in notes), f"NOTE present: {tag}")
    G.g(sum(1 for n in notes if "|spot_audit|" in n) == 5, "five spot-audit NOTE rows (three fixed matchdays 2021-24 + two documented n/a lines where worldfootball dropped Czech coverage)")
    G.g(sum(1 for n in notes if "|source_conflict|" in n) == 3, "three source_conflict NOTEs (wiki matrix cells; infobox scalars + wf date; 2025-26 corrupted Z cells)")
    G.g(sum(1 for n in notes if "|print_error|" in n) == 1, "one print_error NOTE (RSSSF 2025-26 Zachranu position misprint)")
    G.g(sum(1 for n in notes if "|match_awarded|" in n) == 1, "one match_awarded NOTE (2026-05-09 derby abandoned 3-2, LFA award 0-3)")
    G.g(sum(1 for n in notes if "|karvina_incident|" in n) == 1, "one karvina_incident NOTE (match-fixing demotion + Artis Brno repromotion)")
    G.g(sum(1 for n in notes if n.startswith("NOTE|warning|")) == 6,
        "six warning NOTEs (source_conflict x3, print_error, match_awarded, karvina_incident - all disclosed, nothing silently fixed)")
    G.g(all(len(l) == len(l.encode("ascii", "ignore").decode("ascii")) for l in lines), "pack is ASCII-only")
    G.g(not any("|TABLE|" in l or l.startswith("STANDING") for l in lines), "no standings tables in the pack (rows only)")

    # ---------------------------------------------------------------- report
    p, fx = G.summary()
    out = []
    out.append("PACK VALIDATION - CZ1-2021-2026_BP-TEAM-PACK_v2.txt  (FULL SPAN 2021-22..2025-26 per DECREE-2026-08-04)")
    out.append(f"built {ACCESSED} by tools/build_cz1_pack.py from audit/ledger/cz1-<season>.txt (RSSSF tsje2022..2026 "
               "primary, transcribed 2026-08-03/2026-08-04; 2025-26 rows assembled from the BBC dated lattice + wiki "
               "matrices under tools/build_cz1_2526_ledger.py V1..V6, recompute == RSSSF table constants EXACT); "
               "second index = Wikipedia season articles (FBR matrices, group matrices, official table + group-table "
               "constants, venue tables, brackets + CLP box, TwoLeg boxes) + worldfootball matchday spot-audits "
               "R10/R20/R25 for 2021-24 (wf dropped Czech coverage 2024-25 on; n/a documented). Constants in "
               "audit/ledger/cz1-venues.txt and cz1-2ndidx-<season>.txt.")
    out.append("=" * 100)
    out.append(f"GATES: {p} PASS, {fx} FAIL")
    for ok, label, info in G.res:
        out.append(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  <<{info}>>" if (not ok and info) else ""))
    out.append("")
    out.append("REGULAR-TABLE REPRODUCTION DETAIL (official constants = wiki 'League table' sections, position order)")
    for s in SEASONS:
        stat, detail = pivots[s]
        out.append(f"--- {s} (pos | club | recomputed P W-D-L GF-GA Pts | match)")
        for pos, st, vals, good in detail:
            P, W, D, L, GF, GA, pts = vals
            out.append(f"  {pos:>2}. {st:<14} {P:>2} {W:>2}-{D:>2}-{L:>2} {GF:>2}-{GA:<2} {pts:>2}  {'OK' if good else 'MISMATCH'}")
    out.append("")
    out.append("HEAD-TO-HEAD TIE DETAIL (mutual regular-season records recomputed from pack rows)")
    for s, pts, seq, rec, okc in h2h_report:
        out.append(f"--- {s} tie at {pts} pts, official order: {' > '.join(seq)} | mutual records: " +
                   "; ".join(f"{c}: {rec[c]}" for c in seq) +
                   f" | chain reproduces official: {'YES' if okc else 'NO -> FAIL above'}")
    out.append("")
    out.append("GROUP-STAGE REPRODUCTION DETAIL (combined 35-game tables vs wiki Championship/Relegation group sections)")
    for s in SEASONS:
        for grp in ("T", "Z"):
            out.append(f"--- {s} {'TITUL' if grp == 'T' else 'ZACHRANU'} final group table")
            for pos, st, vals, good in pivots[(s, grp)]:
                P, W, D, L, GF, GA, pts = vals
                out.append(f"  {pos}. {st:<14} {P:>2} {W:>2}-{D:>2}-{L:>2} {GF:>2}-{GA:<2} {pts:>2}  {'OK' if good else 'MISMATCH'}")
    out.append("")
    out.append("SECOND-INDEX DIFF SUMMARY")
    for s, n1, n2, n3, n4 in diff_report:
        out.append(f"--- {s}: regular matrix {n1[2]}/{n1[0]} diffs | Titul matrix {n2[2]}/{n2[0]} | Zachranu matrix "
                   f"{n3[2]}/{n3[0]} | Evropu bracket {n4[2]}/{n4[0]} (0 diffs = gates green)")
    out.append("")
    out.append("PER-CLUB PIVOT LEDGERS (owner technique: every club's full in-window campaign, round by round)")
    for s in SEASONS:
        out.append(f"")
        out.append(f"### {s}")
        ms = [l.split("|") for l in lines if l.startswith("MATCH|") and seas_of(l.split("|")[1]) == s]
        for st in sorted(SEASON_CLUBS[s]):
            ros = STOCK2ROSTER[st]
            games = [m for m in ms if m[4] == ros or m[7] == ros]
            rec = [0, 0, 0, 0, 0]  # W D L GF GA
            lines_out = []
            for m in games:
                home = m[4] == ros
                gf, ga = (int(m[5]), int(m[6])) if home else (int(m[6]), int(m[5]))
                rec[3] += gf; rec[4] += ga
                if gf > ga: rec[0] += 1; res = "W"
                elif gf < ga: rec[1] += 0; rec[2] += 1; res = "L"
                else: rec[1] += 1; res = "D"
                opp = m[7] if home else m[4]
                lines_out.append(f"    {m[8]:<13} {m[1]} {'H' if home else 'A'} {res} {gf}-{ga} v {opp}")
            stg = {"T": "Titul", "E": "Evropu", "Z": "Zachranu"}
            gs = next((g for g in ("T", "E", "Z") if st in SEASON_GROUPS[s][g]), "?")
            out.append(f"  {ros:<16} [{stg[gs]}] {len(games)} games  W{rec[0]:>2} D{rec[1]:>2} L{rec[2]:>2} "
                       f"GF{rec[3]:>3} GA{rec[4]:>3}")
            out.extend(lines_out)
    out.append("")
    out.append("### FNL PRO/REL OPPONENTS (owner-sanctioned Czech Relegation Playoffs block; 2 legs each; CZ2/FNL tier in-window)")
    allm = [l.split("|") for l in lines if l.startswith("MATCH|")]
    for club in sorted(FNL7):
        games = sorted([m for m in allm if m[4] == club or m[7] == club], key=lambda x: x[1])
        out.append(f"  {club:<10} {len(games)} games")
        for m in games:
            home = m[4] == club
            gf, ga = (m[5], m[6]) if home else (m[6], m[5])
            res = "W" if gf > ga else "L" if gf < ga else "D"
            out.append(f"    {m[8]:<13} {m[1]} {'H' if home else 'A'} {res} {gf}-{ga} v {m[7] if home else m[4]}")
    with open(OUTAUDIT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"pack rows={len(matches)} gates: {p} PASS {fx} FAIL -> {OUTPACK}")
    print(f"audit -> {OUTAUDIT}")
    return 0 if fx == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
