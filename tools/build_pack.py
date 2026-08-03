#!/usr/bin/env python3
"""
the_bettor_1 — WO-RUSCUP-BACKFILL-03 return artifact builder + gate validator.

Builds handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt (BP-TEAM-PACK v2 grammar)
from the dual-verified match ledger in .work/cup-*.txt (RSSSF #kubok/#cupdet
primary, Wikipedia/RFS second index, match-for-match cross-checked), then
re-runs every workorder §5 acceptance gate against the PACK TEXT ITSELF and
writes audit/pack-validation.txt.

90-minute doctrine: MATCH rows carry 90-minute scores only; penalty shootouts
live in NOTE|info|advancement (knockout) and NOTE|info|group_pens (group
bonus-point shootouts) and are re-parsed from those NOTEs by the validator.

No figure in the pack is imputed: every row traces to the SOURCE labels.
"""
from __future__ import annotations
import re, sys, os
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = (os.path.join(ROOT, ".work") if os.path.isdir(os.path.join(ROOT, ".work"))
        else os.path.join(ROOT, "audit", "ledger"))  # committed ledger copy
OUTPACK = os.path.join(ROOT, "handoffs", "RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation.txt")
ACCESSED = "2026-08-03"
CUTOFF = "2024-06-30"

# ---------------------------------------------------------------- identities
ROSTER22 = {  # WO-RPL §3 exact strings
 "Zenit St Petersburg","FC Krasnodar","CSKA Moscow","Spartak Moscow","Dynamo Moscow",
 "Lokomotiv Moscow","FC Rostov","Akhmat Grozny","Krylia Sovetov Samara","Rubin Kazan",
 "FC Orenburg","Fakel Voronezh","Akron Tolyatti","Dynamo Makhachkala","Baltika Kaliningrad",
 "Rodina Moscow","Pari Nizhny Novgorod","PFC Sochi","FC Khimki","Ural Yekaterinburg",
 "Arsenal Tula","Torpedo Moscow",
}
# WO-sanctioned additions / cup-roster already held client-side (RUSCUP WO §3):
ROSTER_EXTRA = {"KAMAZ Naberezhnye Chelny"}  # exact-form KAMAZ per auditor errata 2026-08-03;
# FC Ufa declared as a TEAM row per the auditor's standing cup-audit instruction (no longer roster-extra).
ROSTER = ROSTER22 | ROSTER_EXTRA

NAME_MAP = {  # source string -> roster/pack string
    "Akron Togliatti": "Akron Tolyatti",
    "Torpedo Moskva": "Torpedo Moscow",  # spelling in #OUT ledger comments
}
def nm(s): return NAME_MAP.get(s, s)

# Non-roster opponents -> TEAM rows.
# fields: leagueName, leagueCode, aliases, stadium, city, first-season
TEAMS = OrderedDict([
 ("Leningradets St-Peterburg",   ("Russian Second League","2D","Leningradets St Petersburg;Leningradets","Kirovets Stadium","St Petersburg","2021-22")),
 ("Dinamo Bryansk",              ("Russian Second League","2D","Dynamo Bryansk","Dynamo Stadium","Bryansk","2021-22")),
 ("Dinamo Barnaul",              ("Russian Second League","2D","Dynamo Barnaul","Dynamo Stadium","Barnaul","2021-22")),
 ("Chaika Peschanokopskoe",      ("Russian Second League","2D","Chayka Peschanokopskoye;FC Chaika","Rostov Arena","Peschanokopskoe","2021-22")),
 ("Legion-Dinamo Makhachkala",   ("Russian Second League","2D","Legion Dynamo Makhachkala","Dynamo Stadium","Makhachkala","2021-22")),
 ("Qayrat Moskva",               ("Russian Second League","2D","FC Kairat Moscow;Kairat Moskva","Central Stadium (Odintsovo)","Moscow","2021-22")),
 ("FC Saransk",                  ("Russian Second League","2D","Saransk","Mordovia Arena","Saransk","2021-22")),
 ("Znamya Noginsk",              ("Russian Second League","2D","Znamya","Istomkino Stadium","Noginsk","2021-22")),
 ("Dinamo Stavropol",            ("Russian Second League","2D","Dynamo Stavropol","Dynamo Stadium","Stavropol","2021-22")),
 ("Torpedo Vladimir",            ("Russian Second League","2D","Torpedo","Torpedo Stadium","Vladimir","2021-22")),
 ("Zenit Izhevsk",               ("Russian Second League","2D","Zenit-Izhevsk","Central Republican Stadium","Izhevsk","2021-22")),
 ("Metallurg Lipetsk",           ("Russian First League","FNL","Metallurg","Metallurg Stadium","Lipetsk","2021-22")),
 ("Kuban Krasnodar",             ("Russian First League","FNL","Kuban","Kuban Stadium","Krasnodar","2021-22")),
 ("Veles Moskva",                ("Russian First League","FNL","Veles Moscow","Avangard Stadium","Moscow","2021-22")),
 ("Rotor Volgograd",             ("Russian First League","FNL","Rotor","Volgograd Arena","Volgograd","2021-22")),
 ("Alania Vladikavkaz",          ("Russian First League","FNL","Alania;Spartak Vladikavkaz","Sultan Bilimkhanov Stadium (Grozny)","Vladikavkaz","2021-22")),
 ("Yenisey Krasnoyarsk",         ("Russian First League","FNL","Yenisey","Central Stadium","Krasnoyarsk","2021-22")),
 ("Volga Ulyanovsk",             ("Russian First League","FNL","Volga","Trud Stadium","Ulyanovsk","2022-23")),
 ("Zvezda Sankt-Peterburg",      ("Russian Second League","2D","Zvezda St Petersburg;Zvezda SPb","Kirovets Stadium","St Petersburg","2022-23")),
 ("SKA Khabarovsk",              ("Russian First League","FNL","SKA-Khabarovsk","Kirovets Stadium (St Petersburg)","Khabarovsk","2023-24")),
 ("Volgar Astrakhan",            ("Russian First League","FNL","Volgar","Central Stadium","Astrakhan","2023-24")),
 ("FC Ufa",                      ("Russian Premier League","RPL","Ufa;Ufa FC;Bashinformsvyaz-Dinamo Ufa","BetBoom Arena","Ufa","2021-22")),
])

# ------------------------------------------------------- season RPL-16 rosters
RPL16 = {
 "2021-22": {"Zenit St Petersburg","Spartak Moscow","Lokomotiv Moscow","Rubin Kazan","PFC Sochi",
             "FC Krasnodar","Arsenal Tula","Pari Nizhny Novgorod","FC Rostov","FC Ufa",
             "Akhmat Grozny","FC Khimki","Krylia Sovetov Samara","Dynamo Moscow","Ural Yekaterinburg","CSKA Moscow"},
 "2022-23": {"FC Krasnodar","Lokomotiv Moscow","Pari Nizhny Novgorod","FC Khimki",
             "Spartak Moscow","Krylia Sovetov Samara","Zenit St Petersburg","Fakel Voronezh",
             "Dynamo Moscow","FC Rostov","Akhmat Grozny","FC Orenburg",
             "Ural Yekaterinburg","CSKA Moscow","Torpedo Moscow","PFC Sochi"},
 "2023-24": {"CSKA Moscow","FC Orenburg","PFC Sochi","Fakel Voronezh",
             "Lokomotiv Moscow","FC Rostov","Ural Yekaterinburg","Rubin Kazan",
             "Zenit St Petersburg","Baltika Kaliningrad","Akhmat Grozny","Krylia Sovetov Samara",
             "Spartak Moscow","Dynamo Moscow","FC Krasnodar","Pari Nizhny Novgorod"},
}
EXEMPT2122 = {"Zenit St Petersburg","Spartak Moscow","Lokomotiv Moscow","Rubin Kazan","PFC Sochi"}

# ------------------------------------------------------------ group layouts
GROUPS2122 = {
 "Group-1": ["Leningradets St-Peterburg","Kuban Krasnodar","FC Krasnodar"],
 "Group-2": ["Torpedo Vladimir","KAMAZ Naberezhnye Chelny","Ural Yekaterinburg"],
 "Group-3": ["Dinamo Bryansk","Veles Moskva","Arsenal Tula"],
 "Group-4": ["Dinamo Barnaul","Fakel Voronezh","Pari Nizhny Novgorod"],
 "Group-5": ["Chaika Peschanokopskoe","Torpedo Moscow","FC Rostov"],
 "Group-6": ["Legion-Dinamo Makhachkala","Alania Vladikavkaz","FC Ufa"],
 "Group-7": ["Qayrat Moskva","Rotor Volgograd","Akhmat Grozny"],
 "Group-8": ["FC Saransk","Baltika Kaliningrad","FC Khimki"],
 "Group-9": ["Znamya Noginsk","Yenisey Krasnoyarsk","Krylia Sovetov Samara"],
 "Group-10": ["Zenit Izhevsk","Metallurg Lipetsk","CSKA Moscow"],
 "Group-11": ["Dinamo Stavropol","FC Orenburg","Dynamo Moscow"],
}
GROUPS2223 = {
 "Group-A": ["FC Krasnodar","Lokomotiv Moscow","Pari Nizhny Novgorod","FC Khimki"],
 "Group-B": ["Spartak Moscow","Krylia Sovetov Samara","Zenit St Petersburg","Fakel Voronezh"],
 "Group-C": ["Dynamo Moscow","FC Rostov","Akhmat Grozny","FC Orenburg"],
 "Group-D": ["Ural Yekaterinburg","CSKA Moscow","Torpedo Moscow","PFC Sochi"],
}
GROUPS2324 = {
 "Group-A": ["CSKA Moscow","FC Orenburg","PFC Sochi","Fakel Voronezh"],
 "Group-B": ["Lokomotiv Moscow","FC Rostov","Ural Yekaterinburg","Rubin Kazan"],
 "Group-C": ["Zenit St Petersburg","Baltika Kaliningrad","Akhmat Grozny","Krylia Sovetov Samara"],
 "Group-D": ["Spartak Moscow","Dynamo Moscow","FC Krasnodar","Pari Nizhny Novgorod"],
}

# Official group tables as transcribed from RSSSF #kubok chapters (expected side
# of the recompute gate). club order = official finish order.
# tuple fields: W,WP(pens win),LP(pens loss),L,GF,GA,pts  (pts may be None where
# the source comment did not record GF/GA separately for that edition; see files)
T2122 = {
 "Group-1": [("Kuban Krasnodar",1,0,0,1,3,1,3),("FC Krasnodar",1,0,0,1,2,3,3),("Leningradets St-Peterburg",1,0,0,1,1,2,3)],
 "Group-2": [("KAMAZ Naberezhnye Chelny",2,0,0,0,2,0,6),("Ural Yekaterinburg",1,0,0,1,2,1,3),("Torpedo Vladimir",0,0,0,2,0,3,0)],
 "Group-3": [("Arsenal Tula",1,1,0,0,7,2,5),("Veles Moskva",1,0,1,0,4,1,4),("Dinamo Bryansk",0,0,0,2,1,9,0)],
 "Group-4": [("Pari Nizhny Novgorod",2,0,0,0,2,0,6),("Fakel Voronezh",1,0,0,1,2,1,3),("Dinamo Barnaul",0,0,0,2,0,3,0)],
 "Group-5": [("Chaika Peschanokopskoe",2,0,0,0,2,0,6),("Torpedo Moscow",1,0,0,1,2,1,3),("FC Rostov",0,0,0,2,0,3,0)],
 "Group-6": [("Alania Vladikavkaz",2,0,0,0,5,2,6),("FC Ufa",0,1,0,1,1,3,2),("Legion-Dinamo Makhachkala",0,0,1,1,3,4,1)],
 "Group-7": [("Rotor Volgograd",1,1,0,0,4,1,5),("Akhmat Grozny",1,0,1,0,4,1,4),("Qayrat Moskva",0,0,0,2,0,6,0)],
 "Group-8": [("Baltika Kaliningrad",1,0,1,0,2,1,4),("FC Khimki",0,1,1,0,1,1,3),("FC Saransk",0,1,0,1,2,3,2)],
 "Group-9": [("Yenisey Krasnoyarsk",2,0,0,0,5,0,6),("Krylia Sovetov Samara",1,0,0,1,10,1,3),("Znamya Noginsk",0,0,0,2,0,14,0)],
 "Group-10": [("CSKA Moscow",2,0,0,0,6,0,6),("Metallurg Lipetsk",1,0,0,1,2,3,3),("Zenit Izhevsk",0,0,0,2,1,6,0)],
 "Group-11": [("Dynamo Moscow",2,0,0,0,9,0,6),("FC Orenburg",1,0,0,1,3,4,3),("Dinamo Stavropol",0,0,0,2,1,9,0)],
}
T2223 = {  # GF/GA not captured for this edition; pts authoritative
 "Group-A": [("FC Krasnodar",4,0,1,1,None,None,13),("Lokomotiv Moscow",3,1,0,2,None,None,11),("Pari Nizhny Novgorod",2,2,0,2,None,None,10),("FC Khimki",0,0,2,4,None,None,2)],
 "Group-B": [("Spartak Moscow",4,0,1,1,None,None,13),("Krylia Sovetov Samara",4,0,0,2,None,None,12),("Zenit St Petersburg",3,1,0,2,None,None,11),("Fakel Voronezh",0,0,0,6,None,None,0)],
 "Group-C": [("Dynamo Moscow",3,0,1,2,None,None,10),("FC Rostov",3,0,0,3,None,None,9),("Akhmat Grozny",3,0,0,3,None,None,9),("FC Orenburg",2,1,0,3,None,None,8)],
 "Group-D": [("Ural Yekaterinburg",4,1,0,1,None,None,14),("CSKA Moscow",4,0,1,1,None,None,13),("Torpedo Moscow",2,0,1,3,None,None,7),("PFC Sochi",0,1,0,5,None,None,2)],
}
T2324 = {
 "Group-A": [("CSKA Moscow",2,2,1,1,11,5,11),("FC Orenburg",3,1,0,2,6,10,11),("PFC Sochi",2,0,2,2,7,6,8),("Fakel Voronezh",1,1,1,3,4,7,6)],
 "Group-B": [("Lokomotiv Moscow",4,0,1,1,10,4,13),("FC Rostov",3,1,0,2,7,7,11),("Ural Yekaterinburg",2,1,0,3,6,6,8),("Rubin Kazan",1,0,1,4,3,9,4)],
 "Group-C": [("Zenit St Petersburg",4,1,0,1,9,5,14),("Baltika Kaliningrad",4,0,0,2,12,7,12),("Akhmat Grozny",2,0,1,3,10,12,7),("Krylia Sovetov Samara",1,0,0,5,5,12,3)],
 "Group-D": [("Spartak Moscow",4,0,0,2,16,12,12),("Dynamo Moscow",3,0,2,1,12,10,11),("FC Krasnodar",3,1,0,2,12,9,11),("Pari Nizhny Novgorod",0,1,0,5,6,15,2)],
}

# Official knockout advancement on penalties (90-min draws) — from sources.
ADV = [
 # season, date, home, away, pens winner, pW-pL, extra
 ("2021-22","2022-04-19","Baltika Kaliningrad","Dynamo Moscow","Dynamo Moscow","5-4",""),
 ("2021-22","2022-04-20","Alania Vladikavkaz","Zenit St Petersburg","Alania Vladikavkaz","6-5",""),
 ("2022-23","2023-03-14","Akron Tolyatti","Lokomotiv Moscow","Akron Tolyatti","7-6",""),
 ("2022-23","2023-03-15","Zenit St Petersburg","Dynamo Moscow","Dynamo Moscow","5-4",""),
 ("2022-23","2023-04-04","Dynamo Moscow","Akron Tolyatti","Akron Tolyatti","4-1",""),
 ("2022-23","2023-04-06","FC Krasnodar","FC Rostov","FC Krasnodar","5-3",""),
 ("2022-23","2023-04-19","FC Krasnodar","Krylia Sovetov Samara","FC Krasnodar","3-0",""),
 ("2022-23","2023-05-03","FC Krasnodar","Akron Tolyatti","FC Krasnodar","4-2",""),
 ("2022-23","2023-06-11","CSKA Moscow","FC Krasnodar","CSKA Moscow","6-5","CSKA Moscow are the 2022-23 cup champions"),
 ("2023-24","2024-03-13","Rodina Moscow","Ural Yekaterinburg","Ural Yekaterinburg","4-1",""),
 ("2023-24","2024-03-14","Lokomotiv Moscow","Baltika Kaliningrad","Baltika Kaliningrad","7-6","aggregate 3-3"),
 ("2023-24","2024-03-14","PFC Sochi","SKA Khabarovsk","SKA Khabarovsk","4-2",""),
 ("2023-24","2024-04-02","FC Khimki","FC Rostov","FC Rostov","7-6",""),
 ("2023-24","2024-05-15","Zenit St Petersburg","CSKA Moscow","Zenit St Petersburg","5-4","aggregate 1-1"),
]

# Official two-legged aggregate results (source record, for gate comparison).
OFFICIAL_AGG = {
 ("2022-23","QF-up","Lokomotiv Moscow","Spartak Moscow"): ("Spartak Moscow","5-2"),
 ("2022-23","QF-up","FC Rostov","Ural Yekaterinburg"): ("Ural Yekaterinburg","3-2"),
 ("2022-23","QF-up","CSKA Moscow","FC Krasnodar"): ("CSKA Moscow","3-1"),
 ("2022-23","QF-up","Krylia Sovetov Samara","Dynamo Moscow"): ("Krylia Sovetov Samara","3-2"),
 ("2022-23","SF-up","Spartak Moscow","Ural Yekaterinburg"): ("Ural Yekaterinburg","3-2"),
 ("2022-23","SF-up","Krylia Sovetov Samara","CSKA Moscow"): ("CSKA Moscow","3-2"),
 ("2022-23","Finals-up","CSKA Moscow","Ural Yekaterinburg"): ("CSKA Moscow","3-2"),
 ("2023-24","QF-Major","Baltika Kaliningrad","Lokomotiv Moscow"): ("Baltika Kaliningrad","3-3 (pens 7-6)"),
 ("2023-24","QF-Major","FC Rostov","CSKA Moscow"): ("CSKA Moscow","3-1"),
 ("2023-24","QF-Major","Dynamo Moscow","Zenit St Petersburg"): ("Zenit St Petersburg","2-1"),
 ("2023-24","QF-Major","FC Orenburg","Spartak Moscow"): ("Spartak Moscow","3-2"),
 ("2023-24","SF-Major","Baltika Kaliningrad","CSKA Moscow"): ("CSKA Moscow","3-0"),
 ("2023-24","SF-Major","Spartak Moscow","Zenit St Petersburg"): ("Zenit St Petersburg","2-1"),
 ("2023-24","Finals-Major","CSKA Moscow","Zenit St Petersburg"): ("Zenit St Petersburg","1-1 (pens 5-4)"),
}

# Official knockout checkpoints (bracket reproduction gate).
OFFICIAL = {
 "2021-22": {
   "SF": [{"Dynamo Moscow","Alania Vladikavkaz"},{"Spartak Moscow","Yenisey Krasnoyarsk"}],
   "Final": [{"Spartak Moscow","Dynamo Moscow"}],
   "champion": "Spartak Moscow",
 },
 "2022-23": {
   "SF-up": [{"Spartak Moscow","Ural Yekaterinburg"},{"Krylia Sovetov Samara","CSKA Moscow"}],
   "SF-low P1": [{"Dynamo Moscow","Akron Tolyatti"},{"FC Krasnodar","FC Rostov"}],
   "SF-low P2": [{"Akron Tolyatti","Spartak Moscow"},{"FC Krasnodar","Krylia Sovetov Samara"}],
   "Final": [{"CSKA Moscow","FC Krasnodar"}],
   "champion": "CSKA Moscow",
 },
 "2023-24": {
   "SF-Major": [{"Baltika Kaliningrad","CSKA Moscow"},{"Spartak Moscow","Zenit St Petersburg"}],
   "SF-Minor P1": [{"FC Orenburg","Dynamo Moscow"},{"Ural Yekaterinburg","FC Rostov"}],
   "SF-Minor P2": [{"Dynamo Moscow","Spartak Moscow"},{"FC Rostov","Baltika Kaliningrad"}],
   "Final": [{"Baltika Kaliningrad","Zenit St Petersburg"}],
   "champion": "Zenit St Petersburg",
 },
}

# Official round-by-round in-scope row counts (RSSSF-derived; stated in NOTEs).
OFFICIAL_COUNTS = {
 "2021-22": [("Group",22),("R16",7),("QF",4),("SF",2),("Final",1)],
 "2022-23": [("Group",48),("QF-up",8),("QF-low",8),("SF-up",4),("SF-low",4),
             ("Finals-up",2),("Finals-low",2),("Final",1)],
 "2023-24": [("Group",48),("QF-Major",8),("QF-Minor",8),("SF-Major",4),("SF-Minor",4),
             ("Finals-Major",2),("Finals-Minor",1),("Final",1)],
}

SOURCES = [
 ("rsssf-rus2022-cup","https://www.rsssf.org/tablesr/rus2022.html","primary-archive",
  "2021-22 Russian Cup chapter (Kubok Rossii): every round's dates+scores, elite-group tables and bracket; D2/D3 group-draw tier slots"),
 ("rsssf-rus2023-cup","https://www.rsssf.org/tablesr/rus2023.html","primary-archive",
  "2022-23 Russian Cup chapters (compact + cupdet): dates, scores, venues, RPL-path group tables, full upper/lower bracket"),
 ("rsssf-rus2024-cup","https://www.rsssf.org/tablesr/rus2024.html","primary-archive",
  "2023-24 Russian Cup chapters (compact + cupdet): dates, scores, venues, RPL-path group tables, full Major/Minor bracket"),
 ("wiki-ruscup-2122","https://en.wikipedia.org/wiki/2021%E2%80%9322_Russian_Cup","second-index",
  "independent cross-index for 2021-22: match-for-match dates/scores confirmed; venues (incl. staged-away grounds); links RFS match sheets"),
 ("wiki-ruscup-2223","https://en.wikipedia.org/wiki/2022%E2%80%9323_Russian_Cup","second-index",
  "independent cross-index for 2022-23: match-for-match dates/scores/venues confirmed; RFS match sheets linked"),
 ("wiki-ruscup-2324","https://en.wikipedia.org/wiki/2023%E2%80%9324_Russian_Cup","second-index",
  "independent cross-index for 2023-24: match-for-match dates/scores/venues confirmed; RFS match sheets linked"),
 ("wiki-fc-volga-ulyanovsk","https://en.wikipedia.org/wiki/FC_Volga_Ulyanovsk","web-index",
  "Volga Ulyanovsk tier evidence: promoted 2022-06 to First League for 2022-23 (18th, relegated)"),
 ("wiki-fc-ufa","https://en.wikipedia.org/wiki/FC_Ufa","web-index",
  "FC Ufa context: 2021-22 RPL participant, May-2022 playoff relegation vs FC Orenburg, 2022 sponsor exit/near-collapse, Bashkortostan ministry step-in 2022-10-19, club continued"),
 ("wiki-fc-zvezda-spb","https://en.wikipedia.org/wiki/FC_Zvezda_Saint_Petersburg","web-index",
  "Zvezda SPb tier evidence: Second League (third tier) in 2022-23"),
 ("wiki-fnl-2324","https://en.wikipedia.org/wiki/2023%E2%80%9324_Russian_First_League","web-index",
  "SKA-Khabarovsk and Volgar Astrakhan listed as 2023-24 First League clubs"),
]
SRC_LABEL = {"2021-22":"rsssf-rus2022-cup","2022-23":"rsssf-rus2023-cup","2023-24":"rsssf-rus2024-cup"}

SEASON_FILES = {"2021-22":"cup-2021-22.txt","2022-23":"cup-2022-23.txt","2023-24":"cup-2023-24.txt"}

# ---------------------------------------------------------------- read ledger
def read_rows():
    rows, out_rows = [], []
    ann = re.compile(r"\s*[\[#].*$")
    for season, fn in SEASON_FILES.items():
        with open(os.path.join(WORK, fn), encoding="utf-8") as f:
            for ln in f:
                ln = ln.rstrip("\n")
                if not ln.strip(): continue
                if ln.startswith("#OUT"):
                    body = ln[4:].strip()
                    p = body.split("|")
                    if len(p) >= 6:
                        out_rows.append({"season":season,"date":p[0].strip(),"stage":p[1].strip(),
                            "home":nm(p[2].strip()),"hg":int(p[3]),"ag":int(p[4]),
                            "away":nm(ann.sub("",p[5]).strip()),"pens":None,
                            "stadium":"","city":""})
                    continue
                if ln.startswith("#"): continue
                p = ln.split("|")
                pens = None
                if len(p) > 6 and p[6].strip() != "":
                    pens = (int(p[6]), int(p[7]))
                rows.append({"season":season,"date":p[0],"stage":p[1],"home":nm(p[2]),
                             "hg":int(p[3]),"ag":int(p[4]),"away":nm(p[5]),"pens":pens,
                             "stadium":p[8] if len(p)>8 else "", "city":p[9] if len(p)>9 else ""})
    rows.sort(key=lambda r: (r["season"], r["date"], r["stage"], r["home"]))
    return rows, out_rows

# ------------------------------------------------------------- pack emission
def build_pack(rows):
    L = []
    a = L.append
    a("NOTE|info|pack_id|RUSCUP-2021-2026_BP-TEAM-PACK_v2 - return of WO-RUSCUP-BACKFILL-03 (issued 2026-08-02). "
      "Segment 2021-22/2022-23/2023-24 of the 5-year Russian Cup span; new rows stop at the 2024-06-30 hard cutoff "
      "(2024-25 + 2025-26 already held and auditor-verified client-side; current season fills centrally). "
      "189 rows = 36+77+76 - every official Russian Cup match with at least one participant among that season's "
      "16 Premier League clubs (auditor-proven slice, same rule as the 152 held 2024-26 rows). Compiled " + ACCESSED + ".")
    for label, url, typ, what in SOURCES:
        a(f"SOURCE|{label}|{url}|{ACCESSED}|{typ}|{what}")
    CAPACITY = {"FC Ufa": "13573"}  # RSSSF rus2022.html #1l stadium table (same page as the 2021-22 cup chapter)
    for name,(lg,code,al,stad,city,first) in TEAMS.items():
        a(f"TEAM|{name}|Russia|{lg}|{code}|{al}|{stad}|{city}|Russia||{CAPACITY.get(name, '')}||")
    notes = {
 "identity": "NOTE|info|identity|Top-flight clubs use the pinned WO-RPL 2021-2026 5YSPAN section-3 strings; era names only here. "
   "FC Nizhny Novgorod appeared 2021-22 under its era name before the 2022 sponsorship rename - all rows (2021-22: group R2/R3, R16) "
   "are recorded under the permanent roster string Pari Nizhny Novgorod; old name added to alias list by this NOTE. "
   "Source spelling Akron Togliatti (RSSSF/Wikipedia) maps to roster string Akron Tolyatti (2022-23 lower-bracket rows). "
   "Lower-league cup participants already on the client roster are used as-is, not re-declared (WO section-3 directive): "
   "Arsenal Tula, Ural Yekaterinburg, Torpedo Moscow, Baltika Kaliningrad, Fakel Voronezh, FC Orenburg, "
   "KAMAZ Naberezhnye Chelny, Rodina Moscow, FC Khimki. FC Ufa moved OUT of the roster-as-is list into the declared "
   "TEAM rows per the auditor's standing cup-audit instruction (errata 2026-08-03 - see team_fields); KAMAZ written "
   "per the auditor's exact-form correction (the cb6e workorder draft used mixed case for the acronym).",
 "ufa": "NOTE|info|club_context|FC Ufa (WO-RPL section-3 known addition): 2021-22 RPL club - played this cup's elite groups "
   "(Group-6, 2 rows + regions-path continuation). Relegated after the May-2022 playoff vs FC Orenburg; summer-2022 sponsor exit "
   "caused a near-collapse (layoff plans reported 2022-10; republic ministry step-in 2022-10-19) and the club played on - it appears "
   "in this pack in the 2022-23 Regions-path QF (2023-02-26 home vs Akhmat Grozny). The workorder's folded summer 2022 context = "
   "that 2022 financial crisis; per the cited public record the club did not fold (wiki-fc-ufa).",
 "compclass": "NOTE|info|comp_class|compType assignments per auditor errata ERRATA-2026-08-03 (supersedes the cb6e workorder "
   "grammar drafts 'domestic-league' everywhere): CUP packs = domestic-cup (all 189 rows here); league packs keep "
   "domestic-league on league rows; promotion/relegation-playoff rows carry compType other (see the RPL return's 12 rows). "
   "The corrected workorder fingerprints were announced by the owner; the uploaded ERRATA file itself did not materialize "
   "in the repo working tree at rebuild time - applied verbatim from the owner's inline errata text and logged in docs/AUDIT.md.",
 "teams": "NOTE|info|team_fields|22 TEAM rows declared for non-roster opponents: the 21 lower-league challengers listed below "
   "plus FC Ufa, added per the auditor's standing cup-audit instruction (errata 2026-08-03). FC Ufa is anchored to its "
   "2021-22 RPL elite-slot identity (leagueCode RPL, BetBoom Arena Ufa, capacity 13,573 per the RSSSF rus2022.html #1l "
   "stadium table - the same page as this pack's cited 2021-22 cup chapter) for byte-level consistency with the RPL "
   "return's declaration; in this pack it appears via 2021-22 Group-6 and the 2022-23 Regions-path QF. "
   "Tier evidence: 2021-22 D2/D3 slot per club is "
   "structural from the RSSSF elite-group draw itself (each group = 1 RPL + 1 First League + 1 Second League club); Volga Ulyanovsk "
   "2022-23 = First League (wiki-fc-volga-ulyanovsk), Zvezda Sankt-Peterburg 2022-23 = Second League (wiki-fc-zvezda-spb), "
   "SKA Khabarovsk + Volgar Astrakhan 2023-24 = First League (wiki-fnl-2324); Qayrat Moskva = amateur entrant occupying a "
   "Second League slot (aliased to FC Kairat Moscow). Stadium/city fields = the verified grounds where each club staged its "
   "in-scope home tie(s); surface/capacity/founded/website left blank rather than asserted without a captured source (no-fabrication policy).",
 "format": "NOTE|info|format_reading|WO section-1 lists 2021-22 as old straight-knockout, no group stage - correction per sources: "
   "2021-22 ran an Elite Group Stage (11 groups x 3 clubs = 1 RPL + 1 First League + 1 Second League, single round-robin over "
   "rounds 1-3). Group round 1 paired the non-RPL clubs (0 RPL on pitch = outside the slice); rounds 2-3 each carry exactly one "
   "RPL club per fixture = 22 in-scope rows. Group winners (11) + 5 European-exempt RPL clubs (Zenit St Petersburg, Spartak Moscow, "
   "Lokomotiv Moscow, Rubin Kazan, PFC Sochi) formed the Round of 16. Verified on RSSSF rus2022 and the wiki second index. "
   "2022-23/2023-24 new format as WO states (RPL-path group stage 4x4, 6 rounds + double-elimination bracket).",
 "rc2122": "NOTE|info|round_counts|2021-22 = 36 rows: 22 elite-group (rounds 2-3; 11 groups, one RPL club per fixture) + 7 R16 + 4 QF + 2 SF + 1 Final. "
   "Group round 1 (11 fixtures, 2021-08-25/26) and qualifying rounds R1-R3 (Jul-Aug 2021): no RPL club on the pitch - outside the "
   "auditor-proven slice, not returned (gap-free span NOTE-explained). R16 tie Baltika Kaliningrad 3-0 Chaika Peschanokopskoe "
   "(2022-03-03) likewise excluded - neither club was then top-flight. Source: rsssf-rus2022-cup.",
 "rc2223": "NOTE|info|round_counts|2022-23 = 77 rows: 48 RPL-path group (4 groups x 4 clubs, 6 rounds) + 29 bracket "
   "(QF-up 8 = 4 ties x 2 legs; QF-low 8 = P1 4 + P2 4; SF-up 4; SF-low 4; Finals-up 2; Finals-low 2; Super Final 1). "
   "Regions-path rounds 1-6 structurally carried 0 RPL clubs (survivors Akron Tolyatti, FC Ufa, Volga Ulyanovsk, Zvezda "
   "Sankt-Peterburg entered at QF-low P1) - outside slice. Source: rsssf-rus2023-cup.",
 "rc2324": "NOTE|info|round_counts|2023-24 = 76 rows: 48 group + 28 bracket (QF-Major 8, QF-Minor 8, SF-Major 4, SF-Minor 4, "
   "Finals-Major 2, Finals-Minor 1, Super Final 1) - matches the WO section-1 proven 2024-25 calibration (76 = 48 + 28). "
   "Regions-path rounds structurally RPL-free (survivors Rodina Moscow, FC Khimki, SKA Khabarovsk, Volgar Astrakhan entered at "
   "QF-Minor P1). Source: rsssf-rus2024-cup.",
 "stages": "NOTE|info|stage_mapping|Venue-detail stage labels: Group-N Rn = 2021-22 elite groups 1-11, rounds 2-3; Group-A..D Rn = "
   "2022-23/2023-24 RPL-path groups, rounds 1-6; R16 = Round of 16 (2021-22 single legs); QF-up/SF-up/Finals-up = 2022-23 upper "
   "(RPL-path) bracket, QF-low/SF-low/Finals-low = 2022-23 lower (Regions-path) bracket; QF-Major/SF-Major/Finals-Major and "
   "QF-Minor/SF-Minor/Finals-Minor = the same two tracks renamed by the federation for 2023-24; leg1/leg2 = two-legged ties "
   "(exactly 2 rows each); P1/P2 = single-match stages of the lower/Minor track; Final = season Super Final.",
 "adapt": "NOTE|info|source_adaptation|WO section-4 cross-index: soccerway is match-level only and worldfootball's rus-cup season "
   "slugs 404 - the Wikipedia season pages (wiki-ruscup-2122/2223/2324, embedding RFS rfs.ru match-sheet links) were used as the "
   "required independent second index. Every round, every date and every scoreline cross-checked match-for-match (189/189); venues "
   "transcribed from RSSSF cupdet chapters with the second index confirming. Name-style equivalents kept as RSSSF-primary strings: "
   "Russian Railways Arena = RZD Arena; Fisht Stadium(s) = Fisht Olympic Stadium; RosTech Arena = Rostec Arena; Crystal Stadium = "
   "Kristall (Zhiguliovsk); FC Krasnodar Stadium = Krasnodar Stadium; Trud Stadium = RSSSF 'Labour Stadium'.",
 "conflict": "NOTE|warning|source_conflict|3 date conflicts 2022-23, all resolved to RSSSF-primary detailed date (cupdet chapter) "
   "corroborated by the wiki/RFS second index - the RSSSF compact chapter's bracket headers run +1 day: Ural Yekaterinburg 2-1 "
   "Spartak Moscow (SF-up leg2) = 2023-04-04 not 04-05; CSKA Moscow 1-0 Krylia Sovetov Samara (SF-up leg2) = 2023-04-05 not 04-06; "
   "FC Krasnodar 0-0 Akron Tolyatti (Finals-low P1) = 2023-05-03 not 05-04. Rows carry the resolved dates.",
 "venue": "NOTE|info|venue_note|Staged/relocated home ties (rows carry the actual match venue, TEAM rows document it): "
   "Alania Vladikavkaz staged all three 2021-22 home ties in Grozny (Sultan Bilimkhanov Stadium - Republican Spartak rebuild). "
   "Chaika Peschanokopskoe staged its 2021-09-22 home tie at Rostov Arena, Rostov-on-Don. Qayrat Moskva staged its 2021-09-22 home "
   "tie at Central Stadium, Odintsovo. Torpedo Moscow home ties 2021-23 at the Luzhniki complex (Sportivnyy Gorodok Luzhniki / "
   "Luzhniki Stadium) during their ground rebuild. SKA Khabarovsk's designated-home QF-Minor tie 2024-04-02 was staged at Kirovets "
   "Stadium, St Petersburg (RSSSF cupdet: In Sankt-Peterburg). Rodina Moscow home 2024-03-13 = Sapsan Arena, Moscow (second index).",
 "cont": "NOTE|info|continuity|Continuity-clause accounting for the full span: every other official Russian Cup match 2021-07 onward "
   "falls outside the auditor-proven section-1 slice and is NOTE-explained here - 2021-22 qualifying rounds (Jul-Aug 2021, lower-league "
   "clubs only), 2021-22 elite-group round 1 (2021-08-25/26), 2021-22 R16 tie Baltika-Chaika, and the complete 2022-23/2023-24 "
   "Regions-path rounds 1-6 (0 RPL participants, verified structurally on RSSSF; consistent with the 152 held 2024-26 rows carrying "
   "0 such rows). No postponed or cancelled ties occurred in-window. No date gaps remain unexplained.",
 "gate": "NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot gate: for each season the full "
   "campaign of every one of the 16 RPL clubs is enumerated club-by-club (2021-22: 11 group entrants x 2 group dates + 5 "
   "European-exempt entering at R16; 2022-23 + 2023-24: each club exactly 6 group dates; then bracket rows until elimination or "
   "the title). RPL-club appearance totals: 40 (2021-22 - every group row carries exactly one RPL club by draw design; 14 later "
   "rounds bring both-RPL fixtures), 146 + 146 (2022-23/2023-24 - group rows are all-RPL x2, Regions-path survivors fill one slot "
   "in lower/Minor ties). Per-club ledgers and all gate recomputes ship in audit/pack-validation.txt.",
 "boundary": "NOTE|info|boundary|First row 2021-09-22, last row 2024-06-02 (Super Final, Luzhniki Stadium). No row dated 2024-06-30 "
   "or later; no dateless rows; no duplicates; two-legged ties appear as exactly two rows. 2024-25 and 2025-26 intentionally absent "
   "(held client-side).",
 "queue": "NOTE|info|queue_override|WO-RUSCUP-BACKFILL-03 was staged queue position 3 behind RPL and CZ1; owner superseded live "
   "in-session and commissioned this cup segment first; league packs follow in queue order.",
 "spot2122": "NOTE|info|spot_audit|2021-22 R16 re-listed one round for spot-audit (source https://www.rsssf.org/tablesr/rus2022.html "
   "Kubok Rossii chapter): 2022-03-01 Dynamo Moscow 3-0 Pari Nizhny Novgorod; 2022-03-02 Spartak Moscow 6-1 Kuban Krasnodar; "
   "2022-03-02 Alania Vladikavkaz 1-0 Arsenal Tula; 2022-03-02 PFC Sochi 1-2 CSKA Moscow; 2022-03-03 Lokomotiv Moscow 0-4 Yenisey "
   "Krasnoyarsk; 2022-03-03 Zenit St Petersburg 6-0 KAMAZ Naberezhnye Chelny; 2022-03-03 Rubin Kazan 2-1 Rotor Volgograd. "
   "(8th tie Baltika Kaliningrad 3-0 Chaika Peschanokopskoe excluded - outside slice, see round_counts note.)",
 "spot2223": "NOTE|info|spot_audit|2022-23 QF-up leg1 re-listed (source https://www.rsssf.org/tablesr/rus2023.html): 2023-02-22 "
   "Lokomotiv Moscow 0-1 Spartak Moscow; 2023-02-22 FC Rostov 1-1 Ural Yekaterinburg; 2023-02-23 CSKA Moscow 3-0 FC Krasnodar; "
   "2023-02-23 Krylia Sovetov Samara 2-1 Dynamo Moscow.",
 "spot2324": "NOTE|info|spot_audit|2023-24 SF-Major (both legs) re-listed (source https://www.rsssf.org/tablesr/rus2024.html): "
   "2024-04-03 Baltika Kaliningrad 0-1 CSKA Moscow; 2024-04-03 Spartak Moscow 1-2 Zenit St Petersburg; 2024-04-16 CSKA Moscow 2-0 "
   "Baltika Kaliningrad; 2024-04-17 Zenit St Petersburg 0-0 Spartak Moscow (aggregates CSKA 3-0, Zenit 2-1).",
    }
    order = ["identity","compclass","ufa","teams","format","rc2122","rc2223","rc2324","stages","adapt","conflict",
             "venue","cont","gate","boundary","queue","spot2122","spot2223","spot2324"]
    for k in order:
        a(notes[k])

    # group-pens notes (generated from verified pen columns in the ledger)
    for r in rows:
        if r["pens"] and r["stage"].startswith("Group"):
            w = r["home"] if r["pens"][0] > r["pens"][1] else r["away"]
            pw, pl = max(r["pens"]), min(r["pens"])
            a(f"NOTE|info|group_pens|{r['season']} {r['stage']} {r['date']}: {r['home']} {r['hg']}-{r['ag']} {r['away']} - "
              f"bonus-point shootout won by {w} {pw}-{pl}; the 90-minute draw stands as the row score")
    # aggregate notes (computed from row pairs; cross-checked vs OFFICIAL_AGG in validate)
    adv0 = {(date, frozenset((h, t))): (w, pens) for season, date, h, t, w, pens, _ in ADV}
    adv0_map = {k: v[0] for k, v in adv0.items()}
    for (season, prefix, h, t_, winner, aggtxt) in compute_aggregates_pack(rows, adv0_map):
        a(f"NOTE|info|aggregate|{season} {prefix}: {winner} won the tie {aggtxt} ({h} vs {t_}, two legs)")
    # advancement notes
    for season, date, h, t_, w, pens, extra in ADV:
        ex = f"; {extra}" if extra else ""
        a(f"NOTE|info|advancement|{season} {date} {h} vs {t_}: {w} advanced (pens {pens} after the recorded 90-minute draw){ex}")

    for r in rows:
        a(f"MATCH|{r['date']}|Russian Cup|domestic-cup|{r['home']}|{r['hg']}|{r['ag']}|{r['away']}|"
          f"{r['stage']}|{r['stadium']}|{r['city']}|Russia||{SRC_LABEL[r['season']]}")
    a("END")
    return L

def compute_aggregates_pack(rows, adv_map):
    """Pair leg1/leg2 rows of the same stage-prefix + club pair; derive aggregates.
    Returns list of (season, prefix, leg1home, other, winner, aggtxt)."""
    pairs = defaultdict(dict)
    for r in rows:
        m = re.match(r"(.+) leg([12])$", r["stage"])
        if m:
            pairs[(r["season"], m.group(1), frozenset((r["home"], r["away"])))][m.group(2)] = r
    out = []
    for (season, prefix, pair), d in sorted(pairs.items(), key=lambda kv: kv[1]["1"]["date"]):
        if set(d) != {"1", "2"}:
            continue
        h = d["1"]["home"]
        t = [c for c in pair if c != h][0]
        tot = defaultdict(int)
        for rr in d.values():
            tot[rr["home"]] += rr["hg"]
            tot[rr["away"]] += rr["ag"]
        ta, tb = tot[h], tot[t]
        if ta == tb:
            pens_txt = ""
            for (seasonA, date, hh, tt, w, pensS, extra) in ADV:
                if seasonA == season and date == d["2"]["date"] and {hh, tt} == {h, t}:
                    pens_txt = f" (pens {pensS})"
            out.append((season, prefix, h, t, adv_map.get((d["2"]["date"], frozenset((h, t)))),
                        f"{ta}-{tb}{pens_txt}"))
        elif ta > tb:
            out.append((season, prefix, h, t, h, f"{ta}-{tb}"))
        else:
            out.append((season, prefix, h, t, t, f"{tb}-{ta}"))
    return out

# ------------------------------------------------------------------ parsing
def parse_pack_lines(lines):
    matches, notes, teams, sources = [], [], [], []
    for ln in lines:
        if ln.startswith("MATCH|"): matches.append(ln.split("|"))
        elif ln.startswith("NOTE|"): notes.append(ln)
        elif ln.startswith("TEAM|"): teams.append(ln.split("|"))
        elif ln.startswith("SOURCE|"): sources.append(ln.split("|"))
    return matches, notes, teams, sources

# ---------------------------------------------------------------- validators
class Gate:
    def __init__(self): self.fails, self.passes, self.lines = 0, 0, []
    def ok(self, cond, name, detail=""):
        tag = "PASS" if cond else "FAIL"
        if cond: self.passes += 1
        else: self.fails += 1
        self.lines.append(f"[{tag}] {name}" + (f" :: {detail}" if detail and not cond else ""))
        return cond

def recompute_table(games, members, pens_winners):
    st = {c: dict(W=0,WP=0,LP=0,L=0,GF=0,GA=0,pts=0) for c in members}
    for g in games:
        h, a = g["home"], g["away"]
        st[h]["GF"] += g["hg"]; st[h]["GA"] += g["ag"]
        st[a]["GF"] += g["ag"]; st[a]["GA"] += g["hg"]
        if g["hg"] > g["ag"]:
            st[h]["W"] += 1; st[h]["pts"] += 3; st[a]["L"] += 1
        elif g["hg"] < g["ag"]:
            st[a]["W"] += 1; st[a]["pts"] += 3; st[h]["L"] += 1
        else:
            key = (g["date"], frozenset((h, a)))
            w = pens_winners.get(key)
            if w is None: return None  # undecided draw - data error
            l = a if w == h else h
            st[w]["WP"] += 1; st[w]["pts"] += 2
            st[l]["LP"] += 1; st[l]["pts"] += 1
    return st

def main():
    rows, out_rows = read_rows()
    lines = build_pack(rows)
    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    G = Gate()
    matches, notes, teams, sources = parse_pack_lines(lines)
    plabels = {s[1] for s in sources}
    rowsP = [{"season": None, "date": m[1], "home": m[4], "hg": int(m[5]), "ag": int(m[6]),
              "away": m[7], "stage": m[8], "stadium": m[9], "city": m[10],
              "source": m[13] if len(m) > 13 else ""} for m in matches]
    season_of = {d.split("|")[1]: None for d in []}
    def season_by_date(d):  # pack rows have no season field; derive
        y = int(d[:4]); m = int(d[5:7])
        return f"{y}-{str(y+1)[2:]}" if m >= 7 else f"{y-1}-{str(y)[2:]}"
    for r in rowsP: r["season"] = season_by_date(r["date"])
    G.ok(all(len(v) == 16 for v in RPL16.values()), "season RPL sets carry exactly 16 clubs each")

    # ---- grammar/structural gates
    G.ok(lines[-1] == "END", "file ends with END")
    G.ok(all(len(m) == 14 and m[2] == "Russian Cup" and m[3] == "domestic-cup" and m[11] == "Russia"
             and m[12] == "" for m in matches), "MATCH grammar: 14 fields, competition/compType (domestic-cup per errata 2026-08-03)/country verbatim")
    G.ok(all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]) for r in rowsP), "no dateless / non-ISO rows")
    G.ok(all(r["date"] < CUTOFF for r in rowsP), "boundary: no row >= 2024-06-30",
       str([r["date"] for r in rowsP if r["date"] >= CUTOFF][:5]))
    seen = set(); dups = []
    for r in rowsP:
        k = (r["date"], r["home"], r["away"])
        (dups.append(k) if k in seen else seen.add(k))
    G.ok(not dups, "no duplicate rows (date/home/away)", str(dups[:5]))
    G.ok(all(r["stage"] and r["stadium"] and r["city"] for r in rowsP), "venue-detail/stadium/city populated on every row")
    G.ok(all(r["source"] in plabels for r in rowsP), "every MATCH sourceLabel resolves to a SOURCE row")
    G.ok(all(len(t) == 13 for t in teams), "TEAM grammar: 13 fields")
    teamed = {t[1] for t in teams}
    G.ok(teamed == set(TEAMS), "declared TEAM set = 22 planned non-roster opponents (21 + FC Ufa per errata 2026-08-03)",
       str(sorted(teamed ^ set(TEAMS))))
    G.ok(not (teamed & ROSTER), "TEAM rows disjoint from client roster")
    G.ok(teamed.isdisjoint({r["home"] for r in rowsP} - teamed - ROSTER) and not ({r["home"] for r in rowsP} | {r["away"] for r in rowsP}) - teamed - ROSTER,
         "every home/away string resolves to roster identity or declared TEAM row",
         str(({r["home"] for r in rowsP} | {r["away"] for r in rowsP}) - teamed - ROSTER))
    used = {x for r in rowsP for x in (r["home"], r["away"])}
    G.ok(all(t in used for t in teamed), "every declared TEAM appears in >=1 row")

    # ---- count gates per season
    for season, spec in OFFICIAL_COUNTS.items():
        got = defaultdict(int)
        for r in rowsP:
            if r["season"] == season:
                key = "Group" if r["stage"].startswith("Group") else next((p for p,_ in spec if r["stage"].startswith(p) and p != "Group"), r["stage"])
                got[key] += 1
        tot = sum(n for _, n in spec)
        G.ok(sum(got.values()) == tot, f"{season} total rows = {tot}", f"got {sum(got.values())}")
        for prefix, n in spec:
            G.ok(got[prefix] == n, f"{season} {prefix} rows = {n}", f"got {got[prefix]}")

    # ---- slice rule: every row has >=1 of that season's RPL-16
    bad = [r for r in rowsP if r["home"] not in RPL16[r["season"]] and r["away"] not in RPL16[r["season"]]]
    G.ok(not bad, "slice rule: every row has >=1 of that season's 16 RPL clubs",
         "; ".join(f"{r['date']} {r['home']} v {r['away']}" for r in bad[:5]))

    # ---- stage whitelist
    WL = {"2021-22": re.compile(r"^(Group-\d+ R[23]|R16|QF|SF|Final)$"),
          "2022-23": re.compile(r"^(Group-[A-D] R[1-6]|QF-up leg[12]|QF-low P[12]|SF-up leg[12]|SF-low P[12]|Finals-up leg[12]|Finals-low P[12]|Final)$"),
          "2023-24": re.compile(r"^(Group-[A-D] R[1-6]|QF-Major leg[12]|QF-Minor P[12]|SF-Major leg[12]|SF-Minor P[12]|Finals-Major leg[12]|Finals-Minor|Final)$")}
    bad = [r for r in rowsP if not WL[r["season"]].match(r["stage"])]
    G.ok(not bad, "stage labels within per-season whitelist", "; ".join(sorted({r["stage"] for r in bad})))

    # ---- pens NOTE parsing (group bonus + knockout advancement)
    pens_winners = {}
    for n in notes:
        m = re.match(r"NOTE\|info\|group_pens\|(\d{4}-\d{2}) (Group-\S+ R\d) (\d{4}-\d{2}-\d{2}): (.*) (\d+)-(\d+) (.*) - bonus-point shootout won by (.*) (\d+)-(\d+)", n)
        if m:
            date = m.group(3); h = m.group(4).strip(); a = m.group(7).strip(); w = m.group(8).strip()
            pens_winners[(date, frozenset((h, a)))] = w
    adv_map, adv_pairs = {}, {}
    for n in notes:
        m = re.match(r"NOTE\|info\|advancement\|(\d{4}-\d{2}) (\d{4}-\d{2}-\d{2}) (.*) vs (.*): (.*) advanced \(pens (\d+)-(\d+)", n)
        if m:
            date = m.group(2); h, a, w = m.group(3).strip(), m.group(4).strip(), m.group(5).strip()
            adv_map[(date, frozenset((h, a)))] = w
            adv_pairs[(date, frozenset((h, a)))] = (h, a)
    # consistency: knockout pens rows are 90-min draws; group pens too
    for (date, pair), w in adv_map.items():
        rr = next((r for r in rowsP if r["date"] == date and frozenset((r["home"], r["away"])) == pair), None)
        G.ok(rr is not None and rr["hg"] == rr["ag"], f"advancement NOTE matches a 90-min draw row ({date} {'/'.join(pair)})")
    G.ok(len(adv_map) == len(ADV), f"advancement NOTEs present: {len(ADV)}", f"got {len(adv_map)}")
    ngp = len([n for n in notes if n.startswith("NOTE|info|group_pens|")])
    G.ok(ngp == 21, "group_pens NOTEs present: 21 (5+7+9)", f"got {ngp}")

    # ---- group membership + table recompute
    for season, groups, T in (("2021-22", GROUPS2122, T2122), ("2022-23", GROUPS2223, T2223), ("2023-24", GROUPS2324, T2324)):
        games = [r for r in rowsP if r["season"] == season and r["stage"].startswith("Group")]
        for gname, members in groups.items():
            gg = [g for g in games if g["stage"].startswith(gname + " ")]
            exp = 3 if season == "2021-22" else 12
            if season == "2021-22": exp = 2  # only rounds 2-3 in scope (2 group games)
            G.ok(len(gg) == exp, f"{season} {gname} in-scope group rows = {exp}", f"got {len(gg)}")
            inb = all(g["home"] in members and g["away"] in members for g in gg)
            G.ok(inb, f"{season} {gname} memberships match official draw")
            if season == "2021-22":
                continue  # full 3-round tables need out-of-scope round 1 (covered by .work cross-gate below)
            st = recompute_table(gg, members, pens_winners)
            G.ok(st is not None, f"{season} {gname} every group draw carries a group_pens NOTE")
            if st:
                club_by_club = True
                detail = []
                for c, w, wp, lp, l, gf, ga, pts in T[gname]:
                    gotc = st[c]
                    for k, v in (("W", w), ("WP", wp), ("LP", lp), ("L", l), ("GF", gf), ("GA", ga), ("pts", pts)):
                        if v is not None and gotc[k] != v:
                            club_by_club = False
                            detail.append(f"{c}.{k}: got {gotc[k]} want {v}")
                G.ok(club_by_club, f"{season} {gname} table reproduces official club-for-club (W/WP/LP/L/GF/GA/pts)", "; ".join(detail))
                # finish order = weakly non-increasing points (official tie-breaks not re-derivable)
                pts_order = [st[c]["pts"] for c, *_ in T[gname]]
                G.ok(all(pts_order[i] >= pts_order[i+1] for i in range(len(pts_order)-1)),
                     f"{season} {gname} official finish order consistent with recomputed points")
                want_first = T[gname][0][0]
                top_pts = max(s["pts"] for s in st.values())
                G.ok(st[want_first]["pts"] == top_pts, f"{season} {gname} group winner {want_first} on top points")

    # ---- 2021-22 internal cross-gate vs full ledger (incl out-of-scope round 1)
    if out_rows:
        games = [dict(r) for r in out_rows if r["stage"].startswith("Group")] + \
                [dict(r, pens=None) for r in rows if r["season"] == "2021-22" and r["stage"].startswith("Group")]
        pw = {}
        for r in rows:
            if r["pens"] and r["stage"].startswith("Group"):
                pw[(r["date"], frozenset((r["home"], r["away"])))] = r["home"] if r["pens"][0] > r["pens"][1] else r["away"]
        for gname, members in GROUPS2122.items():
            gg = [g for g in games if g["stage"].startswith(gname + " ")]
            st = recompute_table(gg, members, pw)
            ok = st is not None
            if ok:
                for c, w, wp, lp, l, gf, ga, pts in T2122[gname]:
                    s = st[c]
                    if (s["W"], s["WP"], s["LP"], s["L"], s["GF"], s["GA"], s["pts"]) != (w, wp, lp, l, gf, ga, pts):
                        ok = False
                        break
            G.ok(ok, f"2021-22 {gname} full 3-team table recomputes from full ledger (incl round 1)")
        winners_official = {g: T2122[g][0][0] for g in GROUPS2122}
        bracket16 = set(winners_official.values()) | EXEMPT2122
        excluded = {x for r in out_rows if r["stage"] == "R16" for x in (r["home"], r["away"])}
        G.ok(excluded and excluded.isdisjoint(RPL16["2021-22"]),
             "2021-22 excluded R16 tie (Baltika-Chaika) has 0 RPL participants (documented slice exclusion)")
        r16_expected = bracket16 - excluded
        r16_got = {x for r in rowsP if r["season"] == "2021-22" and r["stage"] == "R16" for x in (r["home"], r["away"])}
        G.ok(r16_got == r16_expected, "2021-22 R16 lineup (in-scope) = 11 group winners + 5 exempt, minus the RPL-free tie",
             f"missing {sorted(r16_expected - r16_got)} extra {sorted(r16_got - r16_expected)}")

    # ---- bracket reproduction
    win = {}
    for r in rowsP:
        if r["hg"] > r["ag"]: win[(r["date"], frozenset((r["home"], r["away"])))] = r["home"]
        elif r["ag"] > r["hg"]: win[(r["date"], frozenset((r["home"], r["away"])))] = r["away"]
        else: win[(r["date"], frozenset((r["home"], r["away"])))] = adv_map.get((r["date"], frozenset((r["home"], r["away"]))))
    for season, spec in OFFICIAL.items():
        for stage_key, ties in spec.items():
            if stage_key == "champion":
                finals = [r for r in rowsP if r["season"] == season and r["stage"] == "Final"]
                champ = None
                if finals:
                    f = finals[0]
                    champ = f["home"] if f["hg"] > f["ag"] else f["away"] if f["ag"] > f["hg"] else adv_map.get((f["date"], frozenset((f["home"], f["away"]))))
                G.ok(champ == spec["champion"], f"{season} champion = {spec['champion']}", f"derived {champ}")
                continue
            if stage_key in ("Final",):
                sel = [r for r in rowsP if r["season"] == season and r["stage"] == "Final"]
            elif stage_key == "SF":
                sel = [r for r in rowsP if r["season"] == season and r["stage"] == "SF"]
            else:
                sel = [r for r in rowsP if r["season"] == season and r["stage"].startswith(stage_key)]
            ties_got = sorted({tuple(sorted((r["home"], r["away"]))) for r in sel})
            ties_want = sorted({tuple(sorted(s)) for s in ties})
            G.ok(ties_got == ties_want,
                 f"{season} {stage_key} tie-pairs reproduce official record",
                 f"got {ties_got}")

    # ---- aggregates gate
    agg_fail = []
    for (season, prefix, h, t, winner, aggtxt) in compute_aggregates_pack(rowsP, adv_map):
        key = (season, prefix, h, t)
        want = OFFICIAL_AGG.get((season, prefix, h, t)) or OFFICIAL_AGG.get((season, prefix, t, h))
        if want is None or winner != want[0] or aggtxt != want[1]:
            agg_fail.append(f"{season} {prefix} {h} v {t}: got {winner} {aggtxt} want {want}")
    G.ok(not agg_fail, "two-legged aggregates reproduce official record (14 ties)", "; ".join(agg_fail))

    # ---- per-club pivot gate
    pivot_lines = []
    for season in ("2021-22", "2022-23", "2023-24"):
        apps = defaultdict(lambda: [0, 0])
        for r in rowsP:
            if r["season"] != season: continue
            for c in (r["home"], r["away"]):
                if c in RPL16[season]:
                    apps[c][0 if r["stage"].startswith("Group") else 1] += 1
        pivot_lines.append(f"per-club pivot {season} (group apps / bracket apps):")
        for c in sorted(RPL16[season]):
            g, b = apps[c]
            pivot_lines.append(f"  {c:<28} {g} / {b}")
        if season == "2021-22":
            G.ok(all(apps[c][0] == 2 for c in RPL16[season] - EXEMPT2122), "2021-22 pivot: 11 group entrants x 2 group dates")
            G.ok(all(apps[c][0] == 0 and apps[c][1] >= 1 for c in EXEMPT2122), "2021-22 pivot: 5 exempt clubs enter at R16")
        else:
            G.ok(all(apps[c][0] == 6 for c in RPL16[season]), f"{season} pivot: all 16 RPL clubs x 6 group dates",
                 str({c: apps[c][0] for c in RPL16[season] if apps[c][0] != 6}))
        G.ok(all((apps[c][0] + apps[c][1]) >= 1 for c in RPL16[season]), f"{season} pivot: every RPL club appears")
        total_apps = sum(g + b for g, b in apps.values())
        nrows = sum(1 for r in rowsP if r["season"] == season)
        # RPL-club appearances < 2 x rows wherever a non-RPL club is on the pitch
        # (2021-22 group rows carry exactly one RPL club by draw design): expected 40/146/146.
        expect_apps = {"2021-22": 40, "2022-23": 146, "2023-24": 146}[season]
        nonrpl_apps = 2 * nrows - total_apps
        G.ok(total_apps == expect_apps,
             f"{season} RPL-club appearances = {expect_apps} (of 2x{nrows}; {nonrpl_apps} non-RPL opponent slots)",
             f"got {total_apps}")

    # ---------------------------------------------------------------- report
    os.makedirs(os.path.dirname(OUTAUDIT), exist_ok=True)
    with open(OUTAUDIT, "w", encoding="utf-8") as f:
        f.write("PACK VALIDATION - RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt\n")
        f.write(f"built {ACCESSED} by tools/build_pack.py from audit/ledger/cup-*.txt "
                "(RSSSF rus2022/2023/2024 cup chapters primary; Wikipedia/RFS second index x-checked 189/189 rows)\n")
        f.write("=" * 100 + "\n")
        f.write(f"GATES: {G.passes} PASS, {G.fails} FAIL\n\n")
        for ln in G.lines: f.write(ln + "\n")
        f.write("\n" + "=" * 100 + "\nPER-CLUB PIVOT LEDGERS (owner's per-team completeness technique)\n" + "=" * 100 + "\n")
        for ln in pivot_lines: f.write(ln + "\n")
        f.write("\n" + "=" * 100 + "\nBRACKET REPRODUCTION SUMMARY\n" + "=" * 100 + "\n")
        f.write("2021-22: SF Dynamo Moscow-Alania Vladikavkaz, Spartak Moscow-Yenisey Krasnoyarsk - final Spartak Moscow 2-1 Dynamo Moscow (Luzhniki, 2022-05-29) - champion SPARTAK MOSCOW\n")
        f.write("2022-23: up-final CSKA Moscow 3-2 agg Ural Yekaterinburg; low-final FC Krasnodar past Akron Tolyatti (pens 4-2) and Ural (2-1) - Super Final CSKA Moscow 1-1 FC Krasnodar, pens 6-5 (Luzhniki, 2023-06-11) - champion CSKA MOSCOW\n")
        f.write("2023-24: Major-final Zenit St Petersburg past CSKA Moscow (agg 1-1, pens 5-4); Minor-final Baltika Kaliningrad 1-0 Spartak Moscow - Super Final Zenit St Petersburg 2-1 Baltika Kaliningrad (Luzhniki, 2024-06-02) - champion ZENIT ST PETERSBURG\n")
        f.write("\nSOURCE CONFLICTS (resolved, 3): SF-up leg2 Ural-Spartak = 2023-04-04; SF-up leg2 CSKA-Krylia Sovetov = 2023-04-05; Finals-low P1 Krasnodar-Akron = 2023-05-03 - RSSSF compact headers ran +1 day; detailed cupdet dates corroborated by wiki/RFS index.\n")
    print(f"pack -> {OUTPACK} ({len(matches)} MATCH rows, {len(teams)} TEAM, {len(sources)} SOURCE, {len(notes)} NOTE)")
    print(f"validation -> {OUTAUDIT} [{G.passes} PASS / {G.fails} FAIL]")
    return 0 if G.fails == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
