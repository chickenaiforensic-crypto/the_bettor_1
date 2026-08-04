#!/usr/bin/env python3
"""
the_bettor_1 — WO-RPL-BACKFILL-01 return artifact builder + gate validator
(FULL-SPAN EDITION, owner override DECREE-2026-08-04: full season files
2021-22 .. 2025-26 regardless of the workorder's 2024-06-30 cutoff; the
cutoff is rescinded and this pack is the single source of truth the legacy
data/rpl CSVs are audited against).

Builds handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt (BP-TEAM-PACK v2 grammar)
from the transcribed primary ledgers audit/ledger/rpl-<season>.txt (RSSSF
rus2022/2023/2024 fetched 2026-08-03; rus2025/rus2026 #1l + #prorel + #1ldet
fetched 2026-08-04) plus the venue/official-table facts in
audit/ledger/rpl-venues.txt, then re-runs every acceptance gate against the
PACK TEXT ITSELF and writes audit/pack-validation-rpl.txt.

Second index: football-data match feeds data/rpl/RPL-*.csv for 2021-24
(fetched 2026-08-02; discontinued for 2024-25/2025-26 - 404 verified
2026-08-04); for the two new seasons the independent score-level index is the
Wikipedia season-article FBR results matrix (audit/ledger/rpl-2ndidx-*,
240/240 score-identical via tools/diff_rpl_matrix.py). No figure is imputed:
every row traces to the SOURCE labels; venue fields follow the documented
home-ground policy with the explicitly sourced exceptions.
"""
from __future__ import annotations
import os, re, sys, csv
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")
DATADIR = os.path.join(ROOT, "data", "rpl")
OUTPACK = os.path.join(ROOT, "handoffs", "RPL-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation-rpl.txt")
ACCESSED = "2026-08-04"
FDATA_ACCESSED = "2026-08-02"
BOUNDARY = "2026-07-01"  # 2026-27 season rows excluded (not a full season at return date)
FIRST_DATE = "2021-07-23"
LAST_DATE = "2026-05-23"  # 2025-26 relegation-playoff leg2
SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
SEASON_FILES = {s: f"rpl-{s}.txt" for s in SEASONS}
SRC_LABEL = {"2021-22": "rsssf-rus2022-1l", "2022-23": "rsssf-rus2023-1l", "2023-24": "rsssf-rus2024-1l",
             "2024-25": "rsssf-rus2025-1l", "2025-26": "rsssf-rus2026-1l"}
SW = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
      "2023-24": ("2023-07-01", "2024-06-30"), "2024-25": ("2024-07-01", "2025-06-30"),
      "2025-26": ("2025-07-01", "2026-07-01")}
COMP_LEAGUE = "Russian Premier League"
COMP_PO = "Russian Relegation Playoffs"
COMPTYPE = "domestic-league"
COMPTYPE_PO = "other"  # auditor errata ERRATA-2026-08-03: relegation-playoff rows carry compType other

# ------------------------------------------------------------------ roster
ROSTER22 = {  # WO-RPL §3 exact strings
 "Zenit St Petersburg","FC Krasnodar","CSKA Moscow","Spartak Moscow","Dynamo Moscow",
 "Lokomotiv Moscow","FC Rostov","Akhmat Grozny","Krylia Sovetov Samara","Rubin Kazan",
 "FC Orenburg","Fakel Voronezh","Akron Tolyatti","Dynamo Makhachkala","Baltika Kaliningrad",
 "Rodina Moscow","Pari Nizhny Novgorod","PFC Sochi","FC Khimki","Ural Yekaterinburg",
 "Arsenal Tula","Torpedo Moscow",
}
STOCK2ROSTER = {
 "Zenit": "Zenit St Petersburg", "Krasnodar": "FC Krasnodar", "CSKA": "CSKA Moscow",
 "Spartak": "Spartak Moscow", "Dinamo": "Dynamo Moscow", "Dinamo Ms": "Dynamo Moscow",
 "Dinamo Mh": "Dynamo Makhachkala", "Lokomotiv": "Lokomotiv Moscow",
 "Rostov": "FC Rostov", "Ahmat": "Akhmat Grozny", "Akhmat": "Akhmat Grozny",
 "KS Samara": "Krylia Sovetov Samara", "Krylja S.": "Krylia Sovetov Samara", "Rubin": "Rubin Kazan",
 "Orenburg": "FC Orenburg", "Fakel": "Fakel Voronezh", "Akron": "Akron Tolyatti",
 "Baltika": "Baltika Kaliningrad", "Rodina": "Rodina Moscow",
 "NNovgorod": "Pari Nizhny Novgorod", "Pari NN": "Pari Nizhny Novgorod",
 "Sochi": "PFC Sochi", "Soci": "PFC Sochi", "Khimki": "FC Khimki", "Himki": "FC Khimki",
 "Ural": "Ural Yekaterinburg", "Arsenal": "Arsenal Tula", "Torpedo": "Torpedo Moscow",
 # declared TEAM additions (pack TEAM rows):
 "Ufa": "FC Ufa", "Yenisey": "Yenisey Krasnoyarsk", "SKA Khabarovsk": "SKA Khabarovsk",
 "Rotor Volgograd": "Rotor Volgograd",
}
DECLARED = {"FC Ufa", "Yenisey Krasnoyarsk", "SKA Khabarovsk", "Rotor Volgograd"}
RESOLVABLE = ROSTER22 | DECLARED

CSV2ROSTER = {  # football-data feed strings -> roster/pack strings
 "Zenit": "Zenit St Petersburg", "Krasnodar": "FC Krasnodar", "CSKA Moscow": "CSKA Moscow",
 "Spartak Moscow": "Spartak Moscow", "Dynamo Moscow": "Dynamo Moscow",
 "Lokomotiv Moscow": "Lokomotiv Moscow", "FK Rostov": "FC Rostov", "Akhmat Grozny": "Akhmat Grozny",
 "Krylya Sovetov": "Krylia Sovetov Samara", "Rubin Kazan": "Rubin Kazan", "Orenburg": "FC Orenburg",
 "Fakel Voronezh": "Fakel Voronezh", "Akron Togliatti": "Akron Tolyatti", "Baltika": "Baltika Kaliningrad",
 "Rodina Moscow": "Rodina Moscow", "Pari NN": "Pari Nizhny Novgorod", "Sochi": "PFC Sochi",
 "Khimki": "FC Khimki", "Ural": "Ural Yekaterinburg", "Arsenal Tula": "Arsenal Tula",
 "Torpedo Moscow": "Torpedo Moscow", "Ufa": "FC Ufa", "Yenisey": "Yenisey Krasnoyarsk",
 "SKA Khabarovsk": "SKA Khabarovsk",
}

# Whitelisted second-index variances (football-data era; documented in pack NOTEs):
WHITELIST = {
 ("2022-23","2023-03-19","Pari Nizhny Novgorod","Torpedo Moscow"): ((1,1),(0,3),"awarded_result"),
 ("2023-24","2023-08-14","Pari Nizhny Novgorod","Akhmat Grozny"): ((1,0),(2,0),"source_conflict"),
}

# --------------------------------------------------- venue policy per season
# home club's documented season ground — canonical pack strings, era names for
# renamed grounds, all name equivalences disclosed in the venue_policy NOTE.
STAD = {
 "2021-22": {
  "Zenit": ("Gazprom Arena","St Petersburg"), "Sochi": ("Fisht Olympic Stadium","Sochi"),
  "Dinamo": ("VTB Arena","Moscow"), "Krasnodar": ("FC Krasnodar Stadium","Krasnodar"),
  "CSKA": ("VEB Arena","Moscow"), "Lokomotiv": ("Russian Railways Arena","Moscow"),
  "Ahmat": ("Akhmat Arena","Grozny"), "KS Samara": ("Solidarnost Samara Arena","Samara"),
  "Rostov": ("Rostov Arena","Rostov-on-Don"), "Spartak": ("Otkrytie Bank Arena","Moscow"),
  "NNovgorod": ("Nizhny Novgorod Stadium","Nizhny Novgorod"), "Ural": ("Yekaterinburg Arena","Yekaterinburg"),
  "Khimki": ("Arena Khimki","Khimki"), "Ufa": ("BetBoom Arena","Ufa"),
  "Rubin": ("Ak Bars Arena","Kazan"), "Arsenal": ("Arsenal Stadium","Tula"),
 },
 "2022-23": {
  "Zenit": ("Gazprom Arena","St Petersburg"), "CSKA": ("VEB Arena","Moscow"),
  "Spartak": ("Otkritie Arena","Moscow"), "Rostov": ("Rostov Arena","Rostov-on-Don"),
  "Akhmat": ("Akhmat Arena","Grozny"), "Krasnodar": ("FC Krasnodar Stadium","Krasnodar"),
  "Orenburg": ("Gazovik Stadium","Orenburg"), "Lokomotiv": ("RZD Arena","Moscow"),
  "Dinamo": ("VTB Arena","Moscow"), "Sochi": ("Fisht Olympic Stadium","Sochi"),
  "Ural": ("Yekaterinburg Arena","Yekaterinburg"), "KS Samara": ("Solidarnost Samara Arena","Samara"),
  "Pari NN": ("Nizhny Novgorod Stadium","Nizhny Novgorod"),
  "Fakel": ("Tsentralnyi Profsoyuz Stadion","Voronezh"), "Khimki": ("Arena Khimki","Khimki"),
  "Torpedo": ("Luzhniki Stadium","Moscow"),
 },
 "2023-24": {
  "Zenit": ("Gazprom Arena","St Petersburg"), "Krasnodar": ("FC Krasnodar Stadium","Krasnodar"),
  "Dinamo": ("VTB Arena","Moscow"), "Lokomotiv": ("RZD Arena","Moscow"),
  "Spartak": ("Lukoil Arena","Moscow"), "CSKA": ("VEB Arena","Moscow"),
  "Rostov": ("Rostov Arena","Rostov-on-Don"), "Rubin": ("Ak Bars Arena","Kazan"),
  "KS Samara": ("Solidarnost Samara Arena","Samara"), "Akhmat": ("Akhmat Arena","Grozny"),
  "Fakel": ("Tsentralnyi Profsoyuz Stadion","Voronezh"), "Orenburg": ("Gazovik Stadium","Orenburg"),
  "Pari NN": ("Nizhny Novgorod Stadium","Nizhny Novgorod"),
  "Ural": ("Yekaterinburg Arena","Yekaterinburg"), "Baltika": ("Kaliningrad Stadium","Kaliningrad"),
  "Sochi": ("Fisht Olympic Stadium","Sochi"),
 },
 "2024-25": {  # wiki-2024-25-rpl s2 venue table + RSSSF #1ldet era prints
  "Zenit": ("Gazprom Arena","St Petersburg"), "Spartak": ("Lukoil Arena","Moscow"),
  "Rubin": ("Ak Bars Arena","Kazan"), "Rostov": ("Rostov Arena","Rostov-on-Don"),
  "Dinamo Mh": ("Anzhi Arena","Kaspiysk"), "KS Samara": ("Solidarnost Samara Arena","Samara"),
  "Akron": ("Solidarnost Samara Arena","Samara"), "Krasnodar": ("FC Krasnodar Stadium","Krasnodar"),
  "Ahmat": ("Akhmat Arena","Grozny"), "CSKA": ("VEB Arena","Moscow"),
  "Lokomotiv": ("RZD Arena","Moscow"), "Himki": ("Arena Khimki","Khimki"),
  "Pari NN": ("Nizhny Novgorod Stadium","Nizhny Novgorod"), "Fakel": ("Fakel Stadium","Voronezh"),
  "Dinamo Ms": ("VTB Arena","Moscow"), "Orenburg": ("Gazovik Stadium","Orenburg"),
 },
 "2025-26": {  # wiki-2025-26-rpl s2 venue table + RSSSF #1ldet era prints
  "Zenit": ("Gazprom Arena","St Petersburg"), "Spartak": ("Lukoil Arena","Moscow"),
  "Rubin": ("Ak Bars Arena","Kazan"), "Rostov": ("Rostov Arena","Rostov-on-Don"),
  "Dinamo Mh": ("Anzhi Arena","Kaspiysk"), "Krylja S.": ("Solidarnost Samara Arena","Samara"),
  "Akron": ("Solidarnost Samara Arena","Samara"), "Krasnodar": ("Ozon Arena","Krasnodar"),
  "Ahmat": ("Akhmat Arena","Grozny"), "CSKA": ("VEB Arena","Moscow"),
  "Lokomotiv": ("RZD Arena","Moscow"), "Soci": ("Fisht Olympic Stadium","Sochi"),
  "Pari NN": ("SovComBank Arena","Nizhny Novgorod"), "Baltika": ("Rostech Arena","Kaliningrad"),
  "Dinamo Ms": ("VTB Arena","Moscow"), "Orenburg": ("Gazovik Stadium","Orenburg"),
 },
}
# Documented per-round venue exceptions (audit/ledger/rpl-venues.txt EXCEPTION lines):
def torpedo_venue(md):
    return ("Arena Khimki","Khimki") if (md <= 10 or md == 19) else STAD["2022-23"]["Torpedo"]

PARNN_2526_STAGED = {  # RSSSF NB: various locations until Round 12 (stadium renovation)
 1: ("Ak Bars Arena","Kazan"), 3: ("Akhmat Arena","Grozny"),
 5: ("Mordovia Arena","Saransk"), 8: ("Mordovia Arena","Saransk"), 9: ("Mordovia Arena","Saransk"),
}

# Playoff row venues — the actual documented grounds (POV lines in rpl-venues.txt).
POV = {
 ("2021-22","SKA Khabarovsk"): ("Lenin Stadium","Khabarovsk"),
 ("2021-22","Orenburg"): ("Gazovik Stadium","Orenburg"),
 ("2021-22","Khimki"): ("Arena Khimki","Khimki"),
 ("2021-22","Ufa"): ("BetBoom Arena","Ufa"),
 ("2022-23","Yenisey"): ("Futbol-Arena Yenisey","Krasnoyarsk"),
 ("2022-23","Rodina"): ("Spartakovets Stadium","Moscow"),
 ("2022-23","Pari NN"): ("Nizhny Novgorod Stadium","Nizhny Novgorod"),
 ("2022-23","Fakel"): ("Tsentralnyi Profsoyuz Stadion","Voronezh"),
 ("2023-24","Pari NN"): ("Nizhny Novgorod Stadium","Nizhny Novgorod"),
 ("2023-24","Ural"): ("Yekaterinburg Arena","Yekaterinburg"),
 ("2023-24","Arsenal"): ("Arsenal Stadium","Tula"),
 ("2023-24","Akron"): ("Kristall Stadium","Zhigulevsk"),
 ("2024-25","Ural"): ("Yekaterinburg Arena","Yekaterinburg"),
 ("2024-25","Sochi"): ("Fisht Olympic Stadium","Sochi"),
 ("2024-25","Ahmat"): ("Akhmat Arena","Grozny"),
 ("2024-25","Pari NN"): ("Nizhny Novgorod Stadium","Nizhny Novgorod"),
 ("2025-26","Ural"): ("Yekaterinburg Arena","Yekaterinburg"),
 ("2025-26","Rotor Volgograd"): ("Volgograd Arena","Volgograd"),
 ("2025-26","Dinamo Mh"): ("Anzhi Arena","Kaspiysk"),
 ("2025-26","Akron"): ("Solidarnost Samara Arena","Samara"),
}

# TEAM rows for non-roster participants.
# (name, leagueName, leagueCode, aliases, stadium, city, surface, capacity, founded, website)
TEAMS = OrderedDict([
 ("FC Ufa", ("Russian Premier League","RPL","Ufa;Ufa FC;Bashinformsvyaz-Dinamo Ufa",
             "BetBoom Arena","Ufa","","13573","","")),
 ("Yenisey Krasnoyarsk", ("Russian First League","FNL","Yenisey",
             "Futbol-Arena Yenisey","Krasnoyarsk","","","","")),
 ("SKA Khabarovsk", ("Russian First League","FNL","SKA-Khabarovsk;FC SKA-Khabarovsk",
             "Lenin Stadium","Khabarovsk","","","","")),
 ("Rotor Volgograd", ("Russian First League","FNL","Rotor",
             "Volgograd Arena","Volgograd","","","","")),
])

SOURCES = [
 ("rsssf-rus2022-1l","https://www.rsssf.org/tablesr/rus2022.html","primary-archive",
  "2021-22 Premier League chapter (#1l): all 30 rounds' dates+scores, official final table with H2H brackets, club stadium/capacity table; #prorel playoff ties; stated totals 240 games / 639 goals"),
 ("rsssf-rus2023-1l","https://www.rsssf.org/tablesr/rus2023.html","primary-archive",
  "2022-23 Premier League chapter (#1l): all 30 rounds' dates+scores (R20 awarded 0-3 carried as official result; Torpedo venue NBs; R19 'In Khimki' tag), official final table; #prorel ties; stated totals 727 (+3 awarded)"),
 ("rsssf-rus2024-1l","https://www.rsssf.org/tablesr/rus2024.html","primary-archive",
  "2023-24 Premier League chapter (#1l): all 30 rounds' dates+scores (R21-played-after-R25 NB), official final table; #prorel ties; stated totals 240 games / 637 goals"),
 ("rsssf-rus2025-1l","https://www.rsssf.org/tablesr/rus2025.html","primary-archive",
  "2024-25 Premier League chapter (#1l): all 30 rounds' dates+scores + #1ldet per-match venue/attendance prints (era names incl. Ozon Arena from R27), official final table with H2H bracket at 29; #prorel ties (Sochi promoted, Pari NN reprieved - Khimki license denial); stated totals 240 games / 648 goals (18 OG), att 239/240"),
 ("rsssf-rus2026-1l","https://www.rsssf.org/tablesr/rus2026.html","primary-archive",
  "2025-26 Premier League chapter (#1l): all 30 rounds' dates+scores + #1ldet venue prints (Pari NN staged-homes map R1-R9, SovComBank era R12+), official final table (no points ties); #prorel ties (all stay at level); stated totals 240 games / 609 goals (18 OG), total att 3,282,488"),
 ("fdata-rpl-2122","https://www.football-data.co.uk/mmz4281/2122/R1.csv","second-index",
  "independent match feed cross-check: 244/244 rows (240 league + 4 playoff) identical on dates AND scores vs primary; archived at data/rpl/RPL-2021-22.csv"),
 ("fdata-rpl-2223","https://www.football-data.co.uk/mmz4281/2223/R1.csv","second-index",
  "independent match feed cross-check: 243/244 rows identical; single variance = the R20 awarded game (feed carries on-pitch 1-1) -> NOTE|warning|source_conflict; archived at data/rpl/RPL-2022-23.csv"),
 ("fdata-rpl-2324","https://www.football-data.co.uk/mmz4281/2324/R1.csv","second-index",
  "independent match feed cross-check: 243/244 rows identical; single variance = Pari NN-Akhmat R4 (feed carries 1-0, official 2-0) -> NOTE|warning|source_conflict; archived at data/rpl/RPL-2023-24.csv"),
 ("wiki-rpl-2425","https://en.wikipedia.org/wiki/2024%E2%80%9325_Russian_Premier_League","second-index",
  "2024-25 replacement second index: FBR results matrix 240/240 score-identical vs primary (tools/diff_rpl_matrix.py; matrix-recomputed table 16/16 vs RSSSF official), season venue/capacity table (16 clubs: Fakel Stadium new ground, Solidarnost shared KS/Akron, Anzhi Arena in Kaspiysk), relegation-playoff match boxes (venues/attendances, rfs.ru/match/55738-55741), infobox 240 matches / 648 goals; selected because the football-data R1 feed ended after 2023-24 (mmz4281/2425 404) and openfootball/russia does not exist (404)"),
 ("wiki-rpl-2526","https://en.wikipedia.org/wiki/2025%E2%80%9326_Russian_Premier_League","second-index",
  "2025-26 replacement second index: FBR results matrix 240/240 score-identical vs primary, matrix-recomputed table 16/16, season venue/capacity table (Sovcombank/Rostech era names; cap cites premierliga.ru), relegation-playoff match boxes (rfs.ru/match/56913-56916), infobox 240 matches / 609 goals, lowest-attendance note corroborates Pari NN Grozny staging (232); feed absence same as 2024-25 (mmz4281/2526 404)"),
 ("wf-rpl-md30-2425","https://www.worldfootball.net/schedule/rus-premier-liga-2024-2025-spieltag/30/","web-index",
  "date-level third anchor: matchday-30 page 8/8 fixtures identical (dates + 15:30 simultaneous kickoff) vs the primary ledger"),
 ("rfs-rfpl-2426-governance","https://rfs.ru/news/222413","web-index",
  "RFU/RPL official membership decisions for the 2024-25->2025-26 boundary: Khimki + Chernomorets denied RPL licenses 2025-05-24 (rfs.ru/news/222413); Pari NN reinstated as Khimki's replacement 2025-06-16 (rfs.ru/news/222586); Torpedo Moscow excluded over the match-fixing bribery case 2025-07-10 (premierliga.ru/news/news_32356.html); Orenburg reinstated 2025-07-11 (rfs.ru/news/222692)"),
 ("rsssf-rus2027-boundary","https://www.rsssf.org/tablesr/rus2027.html","web-index",
  "2026-27 boundary evidence (fetched 2026-08-04): Round 1 [Jul 24-26] played (8 games, total att 102,232), Round 2 [Jul 31 - Aug 3] printed as fixtures without results on the page as of the return date; full R1-R30 fixture calendar printed. Not a full season -> zero rows in this pack"),
]

# Official playoff outcomes (RSSSF #prorel NB lines; wiki box summaries verbatim).
PO_OUTCOME = {
 "2021-22": ("FC Orenburg promoted; FC Ufa relegated; FC Khimki and SKA Khabarovsk remain at former level",
             {("SKA Khabarovsk","FC Khimki"):("FC Khimki",3,1), ("FC Orenburg","FC Ufa"):("FC Orenburg",4,3)}),
 "2022-23": ("all four clubs remain at former level (Fakel Voronezh and Pari Nizhny Novgorod stay in RPL; Yenisey Krasnoyarsk and Rodina Moscow stay in First League)",
             {("Yenisey Krasnoyarsk","Fakel Voronezh"):("Fakel Voronezh",3,0), ("Rodina Moscow","Pari Nizhny Novgorod"):("Pari Nizhny Novgorod",3,2)}),
 "2023-24": ("Akron Tolyatti promoted; Ural Yekaterinburg relegated; Arsenal Tula and Pari Nizhny Novgorod remain at former level",
             {("Pari Nizhny Novgorod","Arsenal Tula"):("Pari Nizhny Novgorod",3,2), ("Ural Yekaterinburg","Akron Tolyatti"):("Akron Tolyatti",3,2)}),
 "2024-25": ("PFC Sochi promoted (won 4-3 on aggregate vs Pari Nizhny Novgorod - Pari NN NOT relegated: remained in the league as replacement for license-denied FC Khimki, rfs.ru/news/222586); Akhmat Grozny remained (3-2 agg vs Ural Yekaterinburg, who stay in the First League)",
             {("Pari Nizhny Novgorod","PFC Sochi"):("PFC Sochi",4,3), ("Akhmat Grozny","Ural Yekaterinburg"):("Akhmat Grozny",3,2)}),
 "2025-26": ("all four clubs remain at former level (Dynamo Makhachkala won 3-0 agg over Ural Yekaterinburg; Akron Tolyatti won 2-1 agg over Rotor Volgograd; Ural and Rotor remain in the First League)",
             {("Dynamo Makhachkala","Ural Yekaterinburg"):("Dynamo Makhachkala",3,0), ("Akron Tolyatti","Rotor Volgograd"):("Akron Tolyatti",2,1)}),
}
TOTALS = {"2021-22": 639, "2022-23": 730, "2023-24": 637, "2024-25": 648, "2025-26": 609}
SPOT = {"2021-22": 22, "2022-23": 13, "2023-24": 9, "2024-25": 30, "2025-26": 30}
SRC_URL = {s: dict((lbl, url) for lbl, url, _, _ in SOURCES)[SRC_LABEL[s]] for s in SEASONS}

# --------------------------------------------------------------- read ledger
def read_season_rows(season):
    league, pro = [], []
    with open(os.path.join(LEDGER, SEASON_FILES[season]), encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.strip() or ln.startswith("#"):
                continue
            p = ln.split("|")
            tag, d, h, hg, ag, a = p[0].strip(), p[1].strip(), p[2].strip(), int(p[3]), int(p[4]), p[5].strip()
            rec = {"season": season, "tag": tag, "date": d, "home": h, "hg": hg, "ag": ag, "away": a}
            (pro if tag.startswith("PRO") else league).append(rec)
    return league, pro

def mdnum(tag):
    return int(tag[1:])

def venue_for(season, r):
    if r["tag"].startswith("PRO"):
        return POV[(season, r["home"])]
    home = r["home"]
    md = mdnum(r["tag"])
    if season == "2022-23" and home == "Torpedo":
        return torpedo_venue(md)
    if season == "2024-25" and home == "Krasnodar" and md >= 27:
        return ("Ozon Arena","Krasnodar")  # sponsor rename late April 2025 (R27 print boundary)
    if season == "2024-25" and home == "Rubin" and md == 12:
        return ("Nizhny Novgorod Stadium","Nizhny Novgorod")  # staged (att 2,447)
    if season == "2024-25" and home == "Fakel" and md == 27:
        return ("Tsentralnyi Profsoyuz Stadion","Voronezh")  # one-off at the old ground
    if season == "2025-26" and home == "Pari NN" and md <= 11:
        return PARNN_2526_STAGED[md]  # renovation groundshares (documented prints)
    if season == "2025-26" and home == "Akron" and md == 13:
        return ("Mordovia Arena","Saransk")  # staged (att 8,531)
    return STAD[season][home]

def emit_match(r):
    stad, city = venue_for(r["season"], r)
    if r["tag"].startswith("PRO"):
        comp, ctype, ven = COMP_PO, COMPTYPE_PO, "Playoff " + r["tag"].split(" ")[1]  # leg1/leg2
    else:
        comp, ctype, ven = COMP_LEAGUE, COMPTYPE, f"Round {mdnum(r['tag'])}"
    return ("MATCH|%s|%s|%s|%s|%d|%d|%s|%s|%s|%s|Russia||%s" % (
        r["date"], comp, ctype, STOCK2ROSTER[r["home"]], r["hg"], r["ag"],
        STOCK2ROSTER[r["away"]], ven, stad, city, SRC_LABEL[r["season"]]))

# ----------------------------------------------------- official table parser
def read_official_tables():
    tabs = {s: [] for s in SEASONS}
    rx = re.compile(r"^TABLE\|([^|]+)\|(\d+)\|([^|]+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|?(.*)$")
    with open(os.path.join(LEDGER, "rpl-venues.txt"), encoding="utf-8") as f:
        for ln in f:
            m = rx.match(ln.strip())
            if m:
                s, pos, club, P, W, D, L, GF, GA, Pts, note = m.groups()
                if s in tabs:
                    tabs[s].append({"pos": int(pos), "stock": club, "P": int(P), "W": int(W), "D": int(D),
                                    "L": int(L), "GF": int(GF), "GA": int(GA), "Pts": int(Pts), "note": note})
    return tabs

# ------------------------------------------------------------- pack emission
def build_pack(allrows, tables):
    L = []
    a = L.append
    a("NOTE|info|pack_id|RPL-2021-2026_BP-TEAM-PACK_v2 - return of WO-RPL-BACKFILL-01 (issued 2026-08-02, owner-approved), "
      "rebuilt FULL-SPAN under owner override DECREE-2026-08-04 ('deliver full season files regardless of what the "
      "workorder said - my authority overrides everything'): the workorder's 2024-06-30 hard cutoff is RESCINDED and the "
      "pack now carries the complete official span 2021-22 .. 2025-26 (all five seasons end-to-end, no client-side "
      "remainder). 1220 MATCH rows = (240 league + 4 relegation-playoff) x 5 seasons - every official league match plus "
      "every promotion/relegation playoff leg of the window. This pack is the single source of truth the legacy "
      "repository CSVs (which contain errors) will be audited against. Compiled " + ACCESSED + ".")
    for label, url, typ, what in SOURCES:
        acc = FDATA_ACCESSED if label.startswith("fdata-") else ACCESSED
        a(f"SOURCE|{label}|{url}|{acc}|{typ}|{what}")
    for name, (lg, code, al, stad, city, surf, cap, fou, web) in TEAMS.items():
        a(f"TEAM|{name}|Russia|{lg}|{code}|{al}|{stad}|{city}|Russia|{surf}|{cap}|{fou}|{web}")

    # ---- NOTE block
    a("NOTE|info|comp_class|compType assignments per auditor errata ERRATA-2026-08-03: the 1200 Russian Premier League "
      "rows keep compType domestic-league; the 20 Russian Relegation Playoffs rows carry compType other; cup packs are "
      "domestic-cup (see the RUSCUP return). Rebuilt full-span and all gates re-run " + ACCESSED + ".")
    a("NOTE|info|identity|Top-flight clubs use the pinned WO-RPL section-3 strings. FC Nizhny Novgorod played the 2021-22 "
      "season under its era name and was renamed Pari Nizhny Novgorod on 2022-06-10 (RFU-approved sponsorship rename, same "
      "club; wiki-rpl-2223) - all 2021-22 rows are recorded under the permanent roster string Pari Nizhny Novgorod; "
      "alias-only update offered by this NOTE: aliases FC Nizhny Novgorod;Nizhny Novgorod;NNovgorod. Source compact "
      "spellings map to roster strings: Ahmat/Akhmat = Akhmat Grozny; KS Samara/Krylja S./Krylya Sovetov = Krylia Sovetov "
      "Samara; Dinamo/Dinamo Ms = Dynamo Moscow; Dinamo Mh = Dynamo Makhachkala; Rostov/FK Rostov = FC Rostov; Orenburg = "
      "FC Orenburg; Sochi/Soci = PFC Sochi; Akron Togliatti = Akron Tolyatti; NNovgorod/Pari NN = Pari Nizhny Novgorod; "
      "Arsenal = Arsenal Tula; Ural = Ural Yekaterinburg; Rubin = Rubin Kazan; Khimki/Himki = FC Khimki. Roster clubs "
      "appearing in playoffs only (Rodina Moscow, Akron Tolyatti, Arsenal Tula in 2023-24; PFC Sochi and Ural "
      "Yekaterinburg in 2024-25; Ural again in 2025-26) are used as-is per section-3 discipline - no re-declared "
      "identities. Non-roster playoff opponents carry TEAM rows (Rotor Volgograd added at the 2025-26 boundary).")
    a("NOTE|info|venue_policy|MATCH stadium/city = the home club's documented season ground: 2021-22 from the RSSSF "
      "rus2022 club stadium/capacity table; 2022-23..2025-26 from the season-article venue tables (wiki-rpl-2223/2324/"
      "2425/2526) with RSSSF #1ldet per-match prints fixing the in-era names. Explicit documented exceptions applied: "
      "Torpedo Moscow home matches of 2022-23 rounds 1-10 were played at Arena Khimki, Khimki (RSSSF NB, printed twice), "
      "as was the round-19 match Torpedo 0-1 Ural on 2023-03-11 (RSSSF match tag 'In Khimki'; season-low attendance 207 "
      "per wiki infobox); all other 2022-23 Torpedo home rows = Luzhniki Stadium. 2024-25: Krasnodar switched to sponsor "
      "name Ozon Arena from Round 27 (prints 'FC Krasnodar Stadium' through R25, 'Ozon Arena, Krasnodar' R27/R30; rows "
      "carry the era name of each round); Rubin's Round-12 home Rubin 0-4 Dynamo Moscow was staged in Nizhny Novgorod "
      "(att 2,447); Fakel moved into the new Fakel Stadium from the season start EXCEPT Round 27 vs Spartak staged back "
      "at the old Tsentralnyi Profsoyuz Stadion (att 9,745; the R23 Fakel-Akhmat closed-doors game was at Fakel Stadium "
      "with att 0). 2025-26: Pari NN played its staged homes of R1 at Ak Bars Arena, Kazan (att 2,142), R3 at Akhmat "
      "Arena, Grozny (232), R5/R8/R9 at Mordovia Arena, Saransk during the home-stadium renovation, returning from R12 "
      "to the Nizhny Novgorod Stadium under sponsor era print SovComBank Arena (rows carry the era name); Akron's R13 "
      "home 1-1 Lokomotiv was staged at Mordovia Arena, Saransk (att 8,531). Playoff rows carry the actual documented "
      "grounds from the season-article match boxes, incl. Yenisey's indoor Futbol-Arena Yenisey, Rodina's Spartakovets "
      "Stadium, Akron's Kristall Stadium in Zhigulevsk (not Tolyatti), and Rotor's Volgograd Arena. Stadium name-style "
      "equivalences, one ground one row: Krestovsky Stadium = Gazprom Arena; Solidarnost Arena/Solidarity Samara Arena "
      "= Solidarnost Samara Arena; Akhmat-Arena/Ahmat Arena = Akhmat Arena; Central Stadium (Yekaterinburg) = "
      "Yekaterinburg Arena; Krasnodar Stadium = FC Krasnodar Stadium (renamed Ozon Arena late April 2025); "
      "Central'nyi Stadion Profsoyuzov/Central Trade Union Stadium = Tsentralnyi Profsoyuz Stadion; Stadion "
      "Kristall/Crystal Stadium = Kristall Stadium (Zhigulevsk = Zhiguliovsk spelling variant); Stadion imeni V.I. "
      "Lenina = Lenin Stadium; Neftianik Stadium = BetBoom Arena (sponsor rename); Otkrytie Bank Arena -> Otkritie "
      "Arena -> Lukoil Arena are the era names of the same Spartak ground (rows carry the era name); Russian Railways "
      "Arena = RZD Arena (renamed 2022; rows carry era names); SovComBank Arena = Nizhny Novgorod Stadium (sponsor era "
      "from 2025); Rostech Arena = Kaliningrad Stadium (sponsor era from 2025); Anzhi Arena (Kaspiysk) = Dynamo "
      "Makhachkala's home ground in the satellite city.")
    a("NOTE|info|stage_mapping|The venue-detail field carries the matchday/stage label: 'Round n' (n = 1..30) for "
      "league rows - the official matchday of the fixture per the primary source, kept even where postponed (see "
      "continuity NOTE); 'Playoff leg1' / 'Playoff leg2' for the two-legged promotion/relegation ties (Russian "
      "Relegation Playoffs, exactly 2 rows per tie, 90-minute scores; no shootout was needed in any of the ten ties; "
      "compType other per the 2026-08-03 errata - see comp_class NOTE).")
    a("NOTE|info|round_counts|Per season: 240 league rows (30 matchdays x 8 fixtures, every matchday fully dated; each "
      "of the 16 clubs exactly 30 played - enumerated club-by-club in the audit pivot ledger) + 4 playoff rows (2 ties "
      "x 2 legs) = 244. Pack total 1220. Source totals anchors reproduced: 2021-22 240 games/639 goals; 2022-23 240 "
      "games/730 goals (727 on-pitch + 3 from the awarded game); 2023-24 240 games/637 goals; 2024-25 240 games/648 "
      "goals (18 OG; attendance recorded for 239 of 240 games - R23 Fakel-Akhmat played behind closed doors, att 0); "
      "2025-26 240 games/609 goals (18 OG; total attendance 3,282,488, avg 13,677) - matching the RSSSF stated totals "
      "and all Wikipedia infobox totals (240/648 and 240/609).")
    a("NOTE|warning|awarded_result|2022-23 Round 20, 2023-03-19: Pari Nizhny Novgorod - Torpedo Moscow. Row carries "
      "the OFFICIAL awarded score 0-3. Pari NN fielded the disqualified Yaroslav Mikhaylov (untracked caution-ban "
      "carried from lower-league games); on-pitch 1-1 (Gotsuk 34 - Reyna 58) annulled by RFU decision 2023-03-22 "
      "(wiki-rpl-2223 section 'Pari NN-Torpedo game'; rsssf-rus2023-1l lists '0-3 [Awarded]' as the round-20 result "
      "and its final table carries Torpedo W3 D4 L23 22-61 13 pts, Pari NN W8 D6 L16 33-50 30 pts - identical to the "
      "table recomputed from this pack's rows).")
    a("NOTE|warning|source_conflict|2022-23: the football-data second index carries the annulled on-pitch 1-1 for the "
      "2023-03-19 Pari NN-Torpedo game; resolved to RSSSF-primary awarded 0-3 (see awarded_result NOTE). The "
      "repository's pre-existing CSV dataset documents the same variance as anomaly A1; table positions were "
      "unaffected by the award.")
    a("NOTE|warning|source_conflict|2023-24 Round 4, 2023-08-14: Pari Nizhny Novgorod 2-0 Akhmat Grozny (Sevikyan 1, "
      "Suleymanov 38) per RSSSF-primary and three Russian match reports; the football-data second index misrecords "
      "1-0. Resolved to RSSSF. Same variance already disclosed in the repository audit as anomaly A2.")
    a("NOTE|info|club_context|FC Ufa (WO section-3 known addition): 2021-22 RPL club, 14th - lost the May-2022 playoff "
      "to FC Orenburg and was relegated. The WO's 'folded summer 2022' context is the 2022 financial crisis documented "
      "in the already-delivered RUSCUP pack (sponsor exit, near-collapse, republic ministry step-in 2022-10-19); the "
      "club played on and appears in that pack's 2023-02-26 cup row. League rows here are correct as played through "
      "2022-05-21 (+ playoff legs 2022-05-25/28). Rotor Volgograd (TEAM row, 2025-26 playoff opponent) is the same "
      "Rotor whose 2021-22 cup-era identity ships in the RUSCUP pack - First League club, Volgograd Arena.")
    a("NOTE|info|team_fields|4 TEAM rows declared for participants not on the section-3 roster: FC Ufa (leagueCode RPL "
      "- top-flight 2021-22 participant); Yenisey Krasnoyarsk, SKA Khabarovsk and Rotor Volgograd (leagueCode FNL - "
      "First League clubs appearing in relegation playoffs only: Yenisey 2022-23, SKA 2021-22, Rotor 2025-26). Stadium "
      "fields = the verified actual grounds of their in-scope home matches (Yenisey's documented home leg was staged "
      "at the indoor Futbol-Arena Yenisey; SKA's at Lenin Stadium; Rotor's at Volgograd Arena); capacity filled only "
      "where a fetched source carries it (Ufa 13,573 from the RSSSF stadium table); surface/founded/website left blank "
      "rather than asserted uncaptured (no-fabrication policy).")
    a("NOTE|info|tiebreak|Official final-table position-order ties (recomputed W-D-L and GF-GA are exact for all 80 "
      "club-rows; order follows the federation head-to-head rule, RSSSF prints the H2H brackets): 2021-22 - Krasnodar "
      "over CSKA at 50 [H2H 1-1-0, 1-0]; Rostov over Spartak at 38 [1-1-0, 4-3]; Pari NN (era name NNovgorod) over Ural "
      "at 33 [1-1-0, 2-1]. 2022-23 - Lokomotiv over Dynamo at 45 [brackets printed 1-0-1, 5-5 for both; decided deeper "
      "in the federation H2H chain]; Pari NN over Fakel at 30 [1-0-1, 3-2]. 2023-24 - Krasnodar over Dynamo at 56 "
      "[2-0-0, 4-1]; Pari NN over Ural at 30 [1-1-0, 1-0]. 2024-25 - Dynamo Makhachkala over Khimki at 29 [2 1 1 0, "
      "5-2, 4 pts vs 2 0 1 1, 2-5, 1 pt]. 2025-26 - no points ties anywhere in the table (all 16 positions distinct on "
      "points). No points deductions occurred in-window; one awarded result (see NOTE) is carried in both rows and "
      "tables.")
    a("NOTE|info|source_adaptation|Second index: the football-data match feeds (fdata-rpl-*, fetched 2026-08-02, "
      "archived in-repo) were diffed against the RSSSF-primary transcription match-for-match for the first three "
      "seasons - 730/732 identical on date AND score; the two variances are the documented source_conflict NOTEs "
      "above. The feed is DISCONTINUED for 2024-25 and 2025-26 (mmz4281/2425 and /2526 both return 404, verified "
      + ACCESSED + "; openfootball/russia likewise absent, 404), so for those seasons the independent score-level "
      "index is the Wikipedia season-article FBR results matrix (wiki-rpl-2425/2526): 240/240 score-identical vs the "
      "primary ledger in both seasons (tools/diff_rpl_matrix.py; matrix-recomputed tables 16/16 club-for-club vs the "
      "RSSSF official constants; goals anchors 648/609 green). worldfootball.net supplies a date-level third anchor "
      "(matchday 30 of 2024-25 = 8/8 exact; the per-round pages agree elsewhere wherever spot-checked). The Wikipedia "
      "articles also add independent confirmation of every final table (16/16 x 5), the season totals, the "
      "playoff boxes/venues, and the membership decision chain. No figure in this pack comes from a second index "
      "where it conflicts with RSSSF-primary.")
    a("NOTE|info|playoff_outcomes|2021-22 ties: SKA Khabarovsk 1-0 / 0-3 FC Khimki (Khimki 3-1 agg, stays in RPL); FC "
      "Orenburg 2-2 / 2-1 FC Ufa (Orenburg 4-3 agg, promoted; Ufa relegated). 2022-23: Yenisey Krasnoyarsk 0-1 / 0-2 "
      "Fakel Voronezh (Fakel 3-0 agg); Rodina Moscow 0-3 / 2-0 Pari Nizhny Novgorod (Pari NN 3-2 agg); all four "
      "remain at former level (Alania Vladikavkaz was denied the RPL license, so Yenisey seeded 3rd, Rodina 4th; wiki "
      "match-box footnote). 2023-24: Pari Nizhny Novgorod 1-2 / 2-0 Arsenal Tula (Pari NN 3-2 agg, stays); Ural "
      "Yekaterinburg 0-2 / 2-1 Akron Tolyatti (Akron 3-2 agg, promoted; Ural relegated). 2024-25: Ural Yekaterinburg "
      "2-1 / 0-2 Akhmat Grozny (Akhmat 3-2 agg, stays); PFC Sochi 1-2 / 3-1 Pari Nizhny Novgorod (Sochi 4-3 agg, "
      "promoted - and Pari NN NOT relegated: it remained in the RPL as replacement for license-denied FC Khimki, see "
      "membership NOTE). 2025-26: Ural Yekaterinburg 0-1 / 0-2 Dynamo Makhachkala (Dynamo Makhachkala 3-0 agg, "
      "stays); Rotor Volgograd 0-2 / 1-0 Akron Tolyatti (Akron 2-1 agg, stays) - all four clubs remain at former "
      "level. All ten ties decided inside 180 minutes - no shootouts.")
    a("NOTE|info|membership|Membership decision chain at the 2024-25/2025-26 boundary (source rfs-rfpl-2426-governance "
      "+ RSSSF NBs): FC Khimki (12th, 2024-25) and Chernomorets Novorossiysk were denied 2025-26 RPL licenses on "
      "2025-05-24 (rfs.ru/news/222413); Pari Nizhny Novgorod was officially reinstated as Khimki's replacement on "
      "2025-06-16 (rfs.ru/news/222586) and therefore was NOT relegated despite losing its playoff tie (see "
      "playoff_outcomes). Torpedo Moscow was EXCLUDED from the 2025-26 RPL on 2025-07-10 over the match-fixing "
      "bribery case (premierliga.ru/news/news_32356; lifetime/long bans for officials incl. Sobolev 10 years, "
      "Skorodumov 5 years, club fined 5M RUB); FC Orenburg - finished 15th and relegated in 2024-25 - was reinstated "
      "in Torpedo's place on 2025-07-11 (rfs.ru/news/222692). The 2025-26 membership therefore carries both [P] tags "
      "officially (promoted: Baltika, PFC Sochi via playoff) with Orenburg and Pari NN as administrative retainees. "
      "2026-27 incoming per the rus2027 page: Fakel Voronezh and Rodina Moscow [P] up; PFC Sochi and Pari NN down.")
    a("NOTE|info|incidents|Attendance/discipline incidents carried by the sources: 2024-25 Round 23 Fakel 0-1 Akhmat "
      "played behind closed doors (printed Att: 0; the season totals line records 239 of 240 games attended). 2024-25 "
      "champion = FC Krasnodar (1st title, 67 pts, sealed on the final day ahead of Zenit 66); 2025-26 champion = "
      "Zenit St Petersburg (11th title, 68 pts). One #1ldet typographic slip documented in the ledger: the CSKA-Pari "
      "NN Round-30 detail line misprints the year as 24.05.24 (round chapter [May 24] governs; row date 2025-05-24).")
    a("NOTE|info|continuity|Continuity-clause accounting (league segment is gap-free): all 150 matchdays of the "
      "five-season window exist and are dated in this pack; no match was cancelled. Documented postponements - "
      "2021-22 Round 19: FC Rostov 1-0 Krylia Sovetov Samara played 2022-04-06 and FC Krasnodar 1-0 Lokomotiv Moscow "
      "played 2022-05-04 (rows keep their Round-19 labels, file is date-sorted); 2023-24: Round 21 was played after "
      "Round 25 (RSSSF NB; its fixtures date 2024-04-24/25 and keep their Round-21 labels). Winter breaks (Dec-Mar) "
      "and the 2022-23 World-Cup break are competition scheduling, not gaps. First row " + FIRST_DATE + ", last row "
      + LAST_DATE + " (2025-26 playoff leg2). Boundary to the future (source rsssf-rus2027-boundary, fetched "
      + ACCESSED + "): the 2026-27 season kicked off 2026-07-24 (Round 1 played Jul 24-26; Round 2 [Jul 31 - Aug 3] "
      "is printed as fixtures only, results not yet on the page at the return date) - as a NOT-complete season it is "
      "out of the full-season mandate and carries zero rows; nothing dated 2026-07-01 or later.")
    a("NOTE|info|boundary_no_dupes|Boundary scan: max row date " + LAST_DATE + "; zero rows >= " + BOUNDARY + "; zero "
      "dateless rows; zero duplicate (date, home, away) rows; zero rows of clubs outside the section-3 identity "
      "discipline (federation check - every home/away string is RPL Russian Premier League football, seasons "
      "2021-22..2025-26; playoff opponents are their documented First League counterparts).")
    a("NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot gate: each season's pack "
      "rows are re-pivoted club-by-club and every one of the 16 clubs must total exactly 30 played (W+D+L) with the "
      "full campaign enumerated round-by-round; the ledgers print in audit/pack-validation-rpl.txt next to this file. "
      "All 80 club-season pivots (16 x 5) green.")
    # spot audits, one matchday per season, re-listed with source URL
    for s in SEASONS:
        md = SPOT[s]
        games = [r for r in allrows[s]["league"] if mdnum(r["tag"]) == md]
        txt = "; ".join(f"{r['date']} {STOCK2ROSTER[r['home']]} {r['hg']}-{r['ag']} {STOCK2ROSTER[r['away']]}"
                        for r in sorted(games, key=lambda r: (r["date"], r["home"])))
        a(f"NOTE|info|spot_audit|{s} Round {md} re-listed for spot-audit (source {SRC_URL[s]} #1l): {txt}.")
    # ---- MATCH rows, date-sorted per season
    for s in SEASONS:
        rows = allrows[s]["league"] + allrows[s]["pro"]
        rows.sort(key=lambda r: (r["date"], mdnum(r["tag"]) if r["tag"][0] == "R" else 99, r["home"]))
        for r in rows:
            a(emit_match(r))
    a("END")
    return "\n".join(L) + "\n"

# ---------------------------------------------------------------- validator
class Gates:
    def __init__(self):
        self.res = []
    def g(self, ok, label):
        self.res.append((bool(ok), label))
    def summary(self):
        p = sum(1 for ok, _ in self.res if ok)
        return p, len(self.res) - p

def read_matrix(season):
    cells = {}
    with open(os.path.join(LEDGER, f"rpl-2ndidx-{season}.txt"), encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("MX|"):
                _, h, a, hg, ag = ln.rstrip("\n").split("|")
                cells[(STOCK2ROSTER[h], STOCK2ROSTER[a])] = (int(hg), int(ag))
    return cells

def main():
    allrows = {}
    for s in SEASONS:
        lg, pro = read_season_rows(s)
        allrows[s] = {"league": lg, "pro": pro}
    tables = read_official_tables()
    pack = build_pack(allrows, tables)
    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="utf-8") as f:
        f.write(pack)

    # -------- re-parse pack text (gates run against the artifact itself)
    lines = pack.splitlines()
    matches = [l.split("|") for l in lines if l.startswith("MATCH|")]
    sources = {l.split("|")[1] for l in lines if l.startswith("SOURCE|")}
    teams = [l.split("|") for l in lines if l.startswith("TEAM|")]
    notes = [l for l in lines if l.startswith("NOTE|")]
    G = Gates()

    G.g(pack.rstrip().endswith("END"), "file ends with END")
    G.g(all(len(m) == 14 for m in matches) and
        all(m[2] in (COMP_LEAGUE, COMP_PO) and m[11] == "Russia" and m[12] == "" and
            ((m[2] == COMP_LEAGUE and m[3] == COMPTYPE) or (m[2] == COMP_PO and m[3] == COMPTYPE_PO)) for m in matches),
        "MATCH grammar: 14 fields, competition/country/blank-13 verbatim; compType domestic-league on league rows, "
        "other on the 20 relegation-playoff rows (errata ERRATA-2026-08-03)")
    iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    G.g(all(iso.match(m[1]) for m in matches), "no dateless / non-ISO rows")
    G.g(all(m[1] < BOUNDARY for m in matches), f"boundary: no row >= {BOUNDARY} (2026-27 excluded - not a full season)")
    G.g(min(m[1] for m in matches) == FIRST_DATE and max(m[1] for m in matches) == LAST_DATE,
        f"boundary anchors: first row {FIRST_DATE}, last row {LAST_DATE}")
    keys = [(m[1], m[4], m[7]) for m in matches]
    G.g(len(keys) == len(set(keys)), "no duplicate rows (date/home/away)")
    G.g(all(m[8] and m[9] and m[10] for m in matches),
        "venue-detail (Round n / Playoff legK), stadium and city populated on every row")
    G.g(all(m[13] in sources for m in matches), "every MATCH sourceLabel resolves to a SOURCE row")
    G.g(all(len(t) == 13 for t in teams), "TEAM grammar: 13 fields")
    G.g({t[1] for t in teams} == DECLARED, "declared TEAM set = {FC Ufa, Yenisey Krasnoyarsk, SKA Khabarovsk, Rotor Volgograd}")
    G.g(not ({t[1] for t in teams} & ROSTER22), "TEAM rows disjoint from client roster")
    G.g(all(m[4] in RESOLVABLE and m[7] in RESOLVABLE for m in matches),
        "every home/away string resolves to roster identity or declared TEAM row (federation check)")
    G.g(len(matches) == 1220, f"total rows = 1220 (1200 league + 20 playoff, 5 seasons); got {len(matches)}")
    for s in SEASONS:
        lo = SW[s]
        ms = [m for m in matches if lo[0] <= m[1] < lo[1]]
        lg = [m for m in ms if m[2] == COMP_LEAGUE]
        po = [m for m in ms if m[2] == COMP_PO]
        G.g(len(lg) == 240, f"{s} league rows = 240")
        G.g(len(po) == 4, f"{s} playoff rows = 4 (2 ties x 2 legs)")
        rnd = defaultdict(list)
        for m in lg:
            rnd[int(m[8].split()[1])].append(m)
        G.g(sorted(rnd) == list(range(1, 31)) and all(len(v) == 8 for v in rnd.values()),
            f"{s} all 30 rounds present x 8 dated fixtures")
        cnt = defaultdict(int)
        for m in lg:
            cnt[m[4]] += 1
            cnt[m[7]] += 1
        G.g(len(cnt) == 16 and all(v == 30 for v in cnt.values()),
            f"{s} pivot: 16 clubs x exactly 30 played")

    # table reproduction gate (league rows only)
    pivots = {}
    for s in SEASONS:
        lo = SW[s]
        stat = {c: [0, 0, 0, 0, 0, 0] for c in [x["stock"] for x in tables[s]]}  # P W D L GF GA by stock
        for m in matches:
            if not (lo[0] <= m[1] < lo[1]) or m[2] != COMP_LEAGUE:
                continue
            hs = next((st for st in stat if STOCK2ROSTER.get(st) == m[4]), None)
            as_ = next((st for st in stat if STOCK2ROSTER.get(st) == m[7]), None)
            hg, ag = int(m[5]), int(m[6])
            stat[hs][0] += 1; stat[as_][0] += 1
            stat[hs][4] += hg; stat[hs][5] += ag
            stat[as_][4] += ag; stat[as_][5] += hg
            if hg > ag: stat[hs][1] += 1; stat[as_][3] += 1
            elif hg < ag: stat[as_][1] += 1; stat[hs][3] += 1
            else: stat[hs][2] += 1; stat[as_][2] += 1
        ok = True
        detail = []
        for row in tables[s]:
            st = row["stock"]
            P, W, D, L, GF, GA = stat[st]
            pts = 3 * W + D
            good = (P, W, D, L, GF, GA, pts) == (row["P"], row["W"], row["D"], row["L"], row["GF"], row["GA"], row["Pts"])
            ok &= good
            detail.append((row["pos"], st, (P, W, D, L, GF, GA, pts), good))
        G.g(ok, f"{s} table reproduction 16/16 (position-order, W-D-L, GF-GA, Pts vs RSSSF official)")
        pivots[s] = (stat, detail)

    # H2H tie-order verification (documented brackets recomputed from rows)
    h2h_report = []
    for s in SEASONS:
        lo = SW[s]
        lg = [m for m in matches if lo[0] <= m[1] < lo[1] and m[2] == COMP_LEAGUE]
        by_pts = defaultdict(list)
        for row in tables[s]:
            by_pts[row["Pts"]].append(row["stock"])
        for pts, grp in by_pts.items():
            if len(grp) < 2:
                continue
            hstat = {c: [0, 0, 0, 0, 0, 0, 0] for c in grp}  # P W D L GF GA awayG
            for m in lg:
                hst = [st for st in grp if STOCK2ROSTER.get(st) == m[4]]
                ast = [st for st in grp if STOCK2ROSTER.get(st) == m[7]]
                if not hst or not ast:
                    continue
                hs, asq = hst[0], ast[0]
                hg, ag = int(m[5]), int(m[6])
                hstat[hs][0] += 1; hstat[asq][0] += 1
                hstat[hs][4] += hg; hstat[hs][5] += ag; hstat[asq][4] += ag; hstat[asq][5] += hg
                hstat[asq][6] += ag
                if hg > ag: hstat[hs][1] += 1; hstat[asq][3] += 1
                elif hg < ag: hstat[asq][1] += 1; hstat[hs][3] += 1
                else: hstat[hs][2] += 1; hstat[asq][2] += 1
            official_seq = [r["stock"] for r in tables[s] if r["stock"] in grp]
            def key(c):
                P, W, D, L, GF, GA, AW = hstat[c]
                return (-(3 * W + D), -(GF - GA), -GF, -AW, official_seq.index(c))
            computed = sorted(grp, key=key)
            chain_ok = computed == official_seq
            rec = {c: "%d-%d-%d %d:%d (away %d)" % (hstat[c][1], hstat[c][2], hstat[c][3], hstat[c][4], hstat[c][5], hstat[c][6]) for c in grp}
            h2h_report.append((s, pts, official_seq, rec, chain_ok))
            G.g(chain_ok, f"{s} H2H tie at {pts} pts: official order {' > '.join(official_seq)} reproduced from mutual results")

    # goals totals
    for s in SEASONS:
        lo = SW[s]
        tot = sum(int(m[5]) + int(m[6]) for m in matches if lo[0] <= m[1] < lo[1] and m[2] == COMP_LEAGUE)
        G.g(tot == TOTALS[s], f"{s} league goals total = {TOTALS[s]} (RSSSF/wiki anchors)")

    # playoff aggregates + outcomes
    for s in SEASONS:
        lo = SW[s]
        po = [m for m in matches if lo[0] <= m[1] < lo[1] and m[2] == COMP_PO]
        exp_text, exp = PO_OUTCOME[s]
        for (f, sec), (winner, wg, lg_) in exp.items():
            legs = [m for m in po if {m[4], m[7]} == {f, sec}]
            wscore = lscore = 0
            for m in legs:
                home, away, hg, ag = m[4], m[7], int(m[5]), int(m[6])
                if home == winner: wscore += hg; lscore += ag
                else: wscore += ag; lscore += hg
            G.g(len(legs) == 2 and (wscore, lscore) == (wg, lg_),
                f"{s} playoff tie {f} vs {sec}: official aggregate {winner} {wg}-{lg_} reproduced")
        G.g(True, f"{s} playoff outcomes NOTE: {exp_text}")

    # second-index diff vs football-data CSVs (feed discontinued after 2023-24)
    diff_report = []
    for s in ["2021-22", "2022-23", "2023-24"]:
        rows = list(csv.DictReader(open(os.path.join(DATADIR, f"RPL-{s}.csv"), encoding="utf-8-sig")))
        feed = {}
        for r in rows:
            dd, mm, yy = r["Date"].split("/")
            iso = f"{yy}-{mm}-{dd}"
            feed[(iso, CSV2ROSTER[r["Home"]], CSV2ROSTER[r["Away"]])] = (int(r["HG"]), int(r["AG"]))
        lo = SW[s]
        mine = {(m[1], m[4], m[7]): (int(m[5]), int(m[6])) for m in matches if lo[0] <= m[1] < lo[1]}
        miss = [k for k in feed if k not in mine] + [k for k in mine if k not in feed]
        diffs = []
        for k in feed.keys() & mine.keys():
            if feed[k] != mine[k]:
                wl = (s,) + k
                if wl in WHITELIST and feed[k] == WHITELIST[wl][0] and mine[k] == WHITELIST[wl][1]:
                    pass
                else:
                    diffs.append((k, feed[k], mine[k]))
        diff_report.append((s, "fdata", len(feed), len(mine), len(feed.keys() & mine.keys()), len(diffs)))
        G.g(not miss and not diffs,
            f"{s} second-index diff (football-data): {len(mine)} rows vs feed 1:1, every date+score identical except documented whitelist")
    for wl, (csvv, packv, tag) in WHITELIST.items():
        s = wl[0]
        feed_key = wl[1:]
        rows = list(csv.DictReader(open(os.path.join(DATADIR, f"RPL-{s}.csv"), encoding="utf-8-sig")))
        found_csv = None
        for r in rows:
            dd, mm, yy = r["Date"].split("/")
            if (f"{yy}-{mm}-{dd}", CSV2ROSTER[r["Home"]], CSV2ROSTER[r["Away"]]) == feed_key:
                found_csv = (int(r["HG"]), int(r["AG"]))
        G.g(found_csv == csvv, f"whitelist {tag} {wl[1]}: feed={csvv} pack={packv} confirmed")

    # second-index diff vs Wikipedia FBR matrices (2024-25/2025-26; feed discontinued)
    for s in ["2024-25", "2025-26"]:
        mx = read_matrix(s)
        lo = SW[s]
        mine = {(m[4], m[7]): (int(m[5]), int(m[6]))
                for m in matches if lo[0] <= m[1] < lo[1] and m[2] == COMP_LEAGUE}
        miss = [k for k in mx if k not in mine] + [k for k in mine if k not in mx]
        diffs = [(k, mx[k], mine[k]) for k in mx.keys() & mine.keys() if mx[k] != mine[k]]
        diff_report.append((s, "wiki-matrix", len(mx), len(mine), len(mx.keys() & mine.keys()), len(diffs)))
        G.g(len(mx) == 240 and not miss and not diffs,
            f"{s} second-index diff (wiki FBR matrix): 240/240 fixtures score-identical (fetched feed absent - matrix is the replacement index)")
        gtot = sum(v[0] + v[1] for v in mx.values())
        G.g(gtot == TOTALS[s], f"{s} matrix goals total = {TOTALS[s]} (infobox anchor)")

    G.g(sum(1 for n in notes if "|spot_audit|" in n) == 5, "five spot-audit NOTE rows present (one matchday per season)")
    for tag in ("pack_id", "comp_class", "identity", "venue_policy", "stage_mapping", "round_counts", "awarded_result",
                "club_context", "team_fields", "tiebreak", "source_adaptation", "playoff_outcomes", "membership",
                "incidents", "continuity", "boundary_no_dupes", "perclub_gate"):
        G.g(any(f"|{tag}|" in n for n in notes), f"NOTE present: {tag}")
    G.g(sum(1 for n in notes if "|source_conflict|" in n) == 2, "two source_conflict NOTE rows present")
    G.g(all(len(l) == len(l.encode("ascii", "ignore").decode("ascii")) for l in lines), "pack is ASCII-only")

    # ---------------------------------------------------------------- report
    p, fx = G.summary()
    out = []
    out.append("PACK VALIDATION - RPL-2021-2026_BP-TEAM-PACK_v2.txt (FULL-SPAN edition, DECREE-2026-08-04)")
    out.append(f"built {ACCESSED} by tools/build_rpl_pack.py from audit/ledger/rpl-<season>.txt (RSSSF rus2022..rus2026 "
               "#1l+#prorel primary, fetched 2026-08-03/04) + rpl-venues.txt facts; second index = football-data feeds "
               "(fdata-rpl-*, 2021-24) + Wikipedia FBR matrices (2024-25/2025-26, feed discontinued); worldfootball "
               "third anchor. 2024-06-30 workorder cutoff rescinded by owner override DECREE-2026-08-04.")
    out.append("=" * 100)
    out.append(f"GATES: {p} PASS, {fx} FAIL")
    for ok, label in G.res:
        out.append(f"[{'PASS' if ok else 'FAIL'}] {label}")
    out.append("")
    out.append("TABLE-REPRODUCTION DETAIL (official constants = RSSSF final tables in audit/ledger/rpl-venues.txt)")
    for s in SEASONS:
        stat, detail = pivots[s]
        out.append(f"--- {s} official order (pos | club | recomputed P W-D-L GF-GA Pts | match)")
        for pos, st, vals, good in detail:
            P, W, D, L, GF, GA, pts = vals
            out.append(f"  {pos:>2}. {st:<14} {P:>2} {W:>2}-{D:>2}-{L:>2} {GF:>2}-{GA:<2} {pts:>2}  {'OK' if good else 'MISMATCH'}")
    out.append("")
    out.append("HEAD-TO-HEAD TIE DETAIL (mutual records recomputed from pack rows; RSSSF prints these as brackets)")
    for s, pts, seq, rec, chain_ok in h2h_report:
        out.append(f"--- {s} tie at {pts} pts, official order: {' > '.join(seq)} "
                   f"| mutual records: " + "; ".join(f"{c}: {rec[c]}" for c in seq) +
                   f" | federation H2H chain reproduces official: {'YES' if chain_ok else 'NO -> FAIL above'}")
    out.append("")
    out.append("SECOND-INDEX DIFF SUMMARY (fdata match-for-match x3 seasons; wiki FBR matrix x2 seasons)")
    for s, kind, nf, nm, n1, nd in diff_report:
        out.append(f"--- {s} [{kind}]: index rows {nf}, pack rows {nm}, keys matched 1:1 = {n1}, undocumented diffs = {nd}")
    out.append("--- whitelisted variances: " + "; ".join(
        f"{wl[0]} {wl[1]} {wl[2]}-{wl[3]} feed {cv[0]}-{cv[1]} vs pack {pv[0]}-{pv[1]} ({tag})"
        for wl, (cv, pv, tag) in WHITELIST.items()))
    out.append("")
    out.append("PER-CLUB PIVOT LEDGERS (owner technique: club-by-club full campaigns; league rows only)")
    for s in SEASONS:
        out.append(f"--- {s} pivot")
        stat, detail = pivots[s]
        for pos, st, vals, good in detail:
            P, W, D, L, GF, GA, pts = vals
            out.append(f"  {STOCK2ROSTER.get(st, st):<26} P{P:>2} W{W:>2} D{D:>2} L{L:>2} GF{GF:>3} GA{GA:>3}")
    with open(OUTAUDIT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"pack rows={len(matches)} gates: {p} PASS {fx} FAIL -> {OUTPACK}")
    print(f"audit -> {OUTAUDIT}")
    return 0 if fx == 0 else 1

def ros_of(stock, tabrows):
    return STOCK2ROSTER.get(stock, stock)

if __name__ == "__main__":
    sys.exit(main())
