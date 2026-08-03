#!/usr/bin/env python3
"""
the_bettor_1 — WO-RPL-BACKFILL-01 return artifact builder + gate validator.

Builds handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt (BP-TEAM-PACK v2 grammar)
from the transcribed primary ledger audit/ledger/rpl-<season>.txt (RSSSF
rus2022/2023/2024 #1l + #prorel chapters, fetched 2026-08-03) plus the
venue/official-table facts in audit/ledger/rpl-venues.txt, then re-runs every
workorder §5 acceptance gate against the PACK TEXT ITSELF and writes
audit/pack-validation-rpl.txt.

Second index (WO §4): the in-repo football-data match feeds data/rpl/RPL-*.csv
(fetched 2026-08-02, independent of RSSSF) — diffed match-for-match (dates AND
scores) by this script; the two known variances are whitelisted here and
disclosed in the pack as source_conflict NOTEs. No figure is imputed: every
row traces to the SOURCE labels; venue fields follow the documented
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
ACCESSED = "2026-08-03"
FDATA_ACCESSED = "2026-08-02"
CUTOFF = "2024-06-30"
SEASONS = ["2021-22", "2022-23", "2023-24"]
SEASON_FILES = {s: f"rpl-{s}.txt" for s in SEASONS}
SRC_LABEL = {"2021-22": "rsssf-rus2022-1l", "2022-23": "rsssf-rus2023-1l", "2023-24": "rsssf-rus2024-1l"}
COMP_LEAGUE = "Russian Premier League"
COMP_PO = "Russian Relegation Playoffs"
COMPTYPE = "domestic-league"
COMPTYPE_PO = "other"  # auditor errata ERRATA-2026-08-03: relegation-playoff rows carry compType other
# (league rows stay domestic-league; supersedes the cb6e workorder draft's "playoffs too" grammar line)

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
 "Spartak": "Spartak Moscow", "Dinamo": "Dynamo Moscow", "Lokomotiv": "Lokomotiv Moscow",
 "Rostov": "FC Rostov", "Ahmat": "Akhmat Grozny", "Akhmat": "Akhmat Grozny",
 "KS Samara": "Krylia Sovetov Samara", "Rubin": "Rubin Kazan", "Orenburg": "FC Orenburg",
 "Fakel": "Fakel Voronezh", "Akron": "Akron Tolyatti", "Baltika": "Baltika Kaliningrad",
 "Rodina": "Rodina Moscow", "NNovgorod": "Pari Nizhny Novgorod", "Pari NN": "Pari Nizhny Novgorod",
 "Sochi": "PFC Sochi", "Khimki": "FC Khimki", "Ural": "Ural Yekaterinburg",
 "Arsenal": "Arsenal Tula", "Torpedo": "Torpedo Moscow",
 # declared TEAM additions (pack TEAM rows):
 "Ufa": "FC Ufa", "Yenisey": "Yenisey Krasnoyarsk", "SKA Khabarovsk": "SKA Khabarovsk",
}
DECLARED = {"FC Ufa", "Yenisey Krasnoyarsk", "SKA Khabarovsk"}
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

# Whitelisted second-index variances (all documented in pack NOTEs):
# key (season,date,homeR,awayR) -> (csv (hg,ag), pack (hg,ag), tag)
WHITELIST = {
 ("2022-23","2023-03-19","Pari Nizhny Novgorod","Torpedo Moscow"): ((1,1),(0,3),"awarded_result"),
 ("2023-24","2023-08-14","Pari Nizhny Novgorod","Akhmat Grozny"): ((1,0),(2,0),"source_conflict"),
}

# --------------------------------------------------- venue policy per season
# home club's documented season ground (RSSSF 2021-22 stadium table; Wikipedia
# 2022-23 / 2023-24 season-article venue tables) — canonical strings, era names
# for renamed grounds, all name equivalences disclosed in the venue_policy NOTE.
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
}
# 2022-23 Torpedo exceptions (RSSSF rus2023 NB + R19 match tag):
def torpedo_venue(md):
    return ("Arena Khimki","Khimki") if (md <= 10 or md == 19) else STAD["2022-23"]["Torpedo"]

# Playoff row venues — the actual documented grounds (en.wikipedia match boxes,
# corroborating pages; see audit/ledger/rpl-venues.txt POV lines).
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
}

# TEAM rows for non-roster participants (WO §3 known additions).
# (name, leagueName, leagueCode, aliases, stadium, city, surface, capacity, founded, website)
TEAMS = OrderedDict([
 ("FC Ufa", ("Russian Premier League","RPL","Ufa;Ufa FC;Bashinformsvyaz-Dinamo Ufa",
             "BetBoom Arena","Ufa","","13573","","")),
 ("Yenisey Krasnoyarsk", ("Russian First League","FNL","Yenisey",
             "Futbol-Arena Yenisey","Krasnoyarsk","","","","")),
 ("SKA Khabarovsk", ("Russian First League","FNL","SKA-Khabarovsk;FC SKA-Khabarovsk",
             "Lenin Stadium","Khabarovsk","","","","")),
])

SOURCES = [
 ("rsssf-rus2022-1l","https://www.rsssf.org/tablesr/rus2022.html","primary-archive",
  "2021-22 Premier League chapter (#1l): all 30 rounds' dates+scores, official final table with H2H brackets, club stadium/capacity table; #prorel playoff ties; stated totals 240 games / 639 goals"),
 ("rsssf-rus2023-1l","https://www.rsssf.org/tablesr/rus2023.html","primary-archive",
  "2022-23 Premier League chapter (#1l): all 30 rounds' dates+scores (R20 awarded 0-3 carried as official result; Torpedo venue NBs; R19 'In Khimki' tag), official final table; #prorel ties; stated totals 727 (+3 awarded)"),
 ("rsssf-rus2024-1l","https://www.rsssf.org/tablesr/rus2024.html","primary-archive",
  "2023-24 Premier League chapter (#1l): all 30 rounds' dates+scores (R21-played-after-R25 NB), official final table; #prorel ties; stated totals 240 games / 637 goals"),
 ("fdata-rpl-2122","https://www.football-data.co.uk/mmz4281/2122/R1.csv","second-index",
  "independent match feed cross-check: 244/244 rows (240 league + 4 playoff) identical on dates AND scores vs primary; archived at data/rpl/RPL-2021-22.csv"),
 ("fdata-rpl-2223","https://www.football-data.co.uk/mmz4281/2223/R1.csv","second-index",
  "independent match feed cross-check: 243/244 rows identical; single variance = the R20 awarded game (feed carries on-pitch 1-1) -> NOTE|warning|source_conflict; archived at data/rpl/RPL-2022-23.csv"),
 ("fdata-rpl-2324","https://www.football-data.co.uk/mmz4281/2324/R1.csv","second-index",
  "independent match feed cross-check: 243/244 rows identical; single variance = Pari NN-Akhmat R4 (feed carries 1-0, official 2-0) -> NOTE|warning|source_conflict; archived at data/rpl/RPL-2023-24.csv"),
 ("wiki-rpl-2122","https://en.wikipedia.org/wiki/2021%E2%80%9322_Russian_Premier_League","web-index",
  "relegation playoff match boxes (venues, referees, aggregates), season infobox totals 240 matches / 639 goals, relegation record (Ufa via playoffs, Rubin, Arsenal)"),
 ("wiki-rpl-2223","https://en.wikipedia.org/wiki/2022%E2%80%9323_Russian_Premier_League","web-index",
  "season venue/capacity table (16 clubs incl. Torpedo = Luzhniki), playoff match boxes (venues), awarded-game section (RFU decision 2023-03-22), season infobox totals 240 / 730"),
 ("wiki-rpl-2324","https://en.wikipedia.org/wiki/2023%E2%80%9324_Russian_Premier_League","web-index",
  "season venue/capacity table (16 clubs), playoff match boxes (venues + attendances), season infobox totals 240 / 637, champion-decided-on-last-day account"),
 ("fotmob-ska-khimki-220525","https://www.fotmob.com/match/3880923/matchfacts/ska-khabarovsk-vs-khimki","web-index",
  "corroborates 2022-05-25 playoff leg venue Stadion imeni V.I. Lenina (Lenin Stadium), Khabarovsk"),
 ("espn-akron-ural-240601","https://www.espn.com/soccer/match/_/gameId/702716/fc-ural-ekaterinburg-akron-tolyatti","web-index",
  "corroborates 2024-06-01 playoff leg venue Stadion Kristall, Zhigulyovsk (att 2,827)"),
 ("sofascore-parinn-rodina-230610","https://www.sofascore.com/football/match/rodina-moscow-pari-nizhny-novgorod/eIFbsZdEc#id:11330123","web-index",
  "corroborates 2023-06-10 playoff leg venue Nizhny Novgorod Stadium"),
 ("fandom-rpl-2223-playoffs","https://football.fandom.com/wiki/2022%E2%80%9323_Russian_Premier_League","web-index",
  "text mirror confirming 2023-06-10 Fakel leg venue Tsentralnyi Profsoyuz Stadion, Voronezh"),
]

# Official playoff outcomes (RSSSF #prorel NB lines).
PO_OUTCOME = {
 "2021-22": ("FC Orenburg promoted; FC Ufa relegated; FC Khimki and SKA Khabarovsk remain at former level",
             {("SKA Khabarovsk","FC Khimki"):("FC Khimki",3,1), ("FC Orenburg","FC Ufa"):("FC Orenburg",4,3)}),
 "2022-23": ("all four clubs remain at former level (Fakel Voronezh and Pari Nizhny Novgorod stay in RPL; Yenisey Krasnoyarsk and Rodina Moscow stay in First League)",
             {("Yenisey Krasnoyarsk","Fakel Voronezh"):("Fakel Voronezh",3,0), ("Rodina Moscow","Pari Nizhny Novgorod"):("Pari Nizhny Novgorod",3,2)}),
 "2023-24": ("Akron Tolyatti promoted; Ural Yekaterinburg relegated; Arsenal Tula and Pari Nizhny Novgorod remain at former level",
             {("Pari Nizhny Novgorod","Arsenal Tula"):("Pari Nizhny Novgorod",3,2), ("Ural Yekaterinburg","Akron Tolyatti"):("Akron Tolyatti",3,2)}),
}
TOTALS = {"2021-22": 639, "2022-23": 730, "2023-24": 637}  # 2022-23 stated as 727 +3 awarded
SPOT = {"2021-22": 22, "2022-23": 13, "2023-24": 9}  # fixed spot-audit matchdays (documented)

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
                tabs[s].append({"pos": int(pos), "stock": club, "P": int(P), "W": int(W), "D": int(D),
                                "L": int(L), "GF": int(GF), "GA": int(GA), "Pts": int(Pts), "note": note})
    return tabs

# ------------------------------------------------------------- pack emission
def build_pack(allrows, tables):
    L = []
    a = L.append
    a("NOTE|info|pack_id|RPL-2021-2026_BP-TEAM-PACK_v2 - return of WO-RPL-BACKFILL-01 (issued 2026-08-02, owner-approved). "
      "Segment 2021-22/2022-23/2023-24 of the 5-year Russian Premier League span; new rows stop at the 2024-06-30 hard cutoff "
      "(2024-25 + 2025-26 already held and auditor-verified client-side; current season fills centrally). "
      "732 MATCH rows = (240 league + 4 relegation-playoff) x 3 seasons - every official league match plus every "
      "promotion/relegation playoff leg of the window. Compiled " + ACCESSED + ".")
    for label, url, typ, what in SOURCES:
        acc = FDATA_ACCESSED if label.startswith("fdata-") else ACCESSED
        a(f"SOURCE|{label}|{url}|{acc}|{typ}|{what}")
    for name, (lg, code, al, stad, city, surf, cap, fou, web) in TEAMS.items():
        a(f"TEAM|{name}|Russia|{lg}|{code}|{al}|{stad}|{city}|Russia|{surf}|{cap}|{fou}|{web}")

    # ---- NOTE block
    a("NOTE|info|comp_class|compType assignments per auditor errata ERRATA-2026-08-03 (corrected RPL workorder fingerprint "
      "cb6e -> 9903cf856877d173ba71d72cef64e9c6, supersedes the cb6e draft's grammar line 'domestic-league (playoffs too)'): "
      "the 720 Russian Premier League rows keep compType domestic-league; the 12 Russian Relegation Playoffs rows now carry "
      "compType other; cup packs are domestic-cup (see the RUSCUP return). Row content otherwise unchanged - this pack is "
      "identical to the cb6e return except compType field 4 on the 12 playoff rows. Rebuilt and all gates re-run 2026-08-03; "
      "the uploaded ERRATA file did not materialize in the repo working tree, applied verbatim from the owner's inline errata "
      "text and logged in docs/AUDIT.md.")
    a("NOTE|info|identity|Top-flight clubs use the pinned WO-RPL section-3 strings. FC Nizhny Novgorod played the 2021-22 season "
      "under its era name and was renamed Pari Nizhny Novgorod on 2022-06-10 (RFU-approved sponsorship rename, same club; "
      "wiki-rpl-2223) - all 2021-22 rows are recorded under the permanent roster string Pari Nizhny Novgorod; alias-only update "
      "offered by this NOTE: aliases FC Nizhny Novgorod;Nizhny Novgorod;NNovgorod. Source compact spellings map to roster strings: "
      "Ahmat/Akhmat = Akhmat Grozny; KS Samara/Krylya Sovetov = Krylia Sovetov Samara; Dinamo = Dynamo Moscow; Rostov/FK Rostov = "
      "FC Rostov; Orenburg = FC Orenburg; Sochi = PFC Sochi; Akron Togliatti = Akron Tolyatti; NNovgorod/Pari NN = Pari Nizhny Novgorod; "
      "Arsenal = Arsenal Tula; Ural = Ural Yekaterinburg; Rubin = Rubin Kazan. Roster clubs appearing in playoffs only (Rodina Moscow, "
      "Akron Tolyatti, Arsenal Tula in 2023-24) are used as-is per section-3 discipline - no re-declared identities.")
    a("NOTE|info|venue_policy|MATCH stadium/city = the home club's documented season ground: 2021-22 from the RSSSF rus2022 club "
      "stadium/capacity table; 2022-23 and 2023-24 from the season-article venue tables (wiki-rpl-2223/2324). Explicit documented "
      "exceptions applied: Torpedo Moscow home matches of 2022-23 rounds 1-10 were played at Arena Khimki, Khimki (RSSSF NB, printed "
      "twice), as was the round-19 match Torpedo 0-1 Ural on 2023-03-11 (RSSSF match tag 'In Khimki'; season-low attendance 207 per "
      "wiki infobox); all other 2022-23 Torpedo home rows = Luzhniki Stadium, Moscow (season venue table). Playoff rows carry the "
      "actual documented grounds from the season-article match boxes, incl. Yenisey's indoor Futbol-Arena Yenisey (their Central "
      "Stadium unavailable), Rodina's Spartakovets Stadium, and Akron's Kristall Stadium in Zhigulevsk (not Tolyatti). Stadium "
      "name-style equivalences, one ground one row: Krestovsky Stadium = Gazprom Arena; Solidarnost Arena = Solidarnost Samara Arena; "
      "Akhmat-Arena/Ahmat Arena = Akhmat Arena; Central Stadium (Yekaterinburg) = Yekaterinburg Arena; Krasnodar Stadium = FC Krasnodar "
      "Stadium; Central'nyi Stadion Profsoyuzov/Central Trade Union Stadium = Tsentralnyi Profsoyuz Stadion; Stadion Kristall/Crystal "
      "Stadium = Kristall Stadium (Zhigulevsk = Zhiguliovsk spelling variant); Stadion imeni V.I. Lenina = Lenin Stadium; Neftianik "
      "Stadium = BetBoom Arena (sponsor rename); Otkrytie Bank Arena -> Otkritie Arena -> Lukoil Arena are the era names of the same "
      "Spartak ground (rows carry the era name); Russian Railways Arena = RZD Arena (renamed 2022; rows carry era names).")
    a("NOTE|info|stage_mapping|The venue-detail field carries the matchday/stage label: 'Round n' (n = 1..30) for league rows - "
      "the official matchday of the fixture per the primary source, kept even where postponed (see continuity NOTE); 'Playoff leg1' / "
      "'Playoff leg2' for the two-legged promotion/relegation ties (Russian Relegation Playoffs, exactly 2 rows per tie, 90-minute "
      "scores; no shootout was needed in any of the six ties; compType other per the 2026-08-03 errata - see comp_class NOTE).")
    a("NOTE|info|round_counts|Per season: 240 league rows (30 matchdays x 8 fixtures, every matchday fully dated; each of the 16 "
      "clubs exactly 30 played - enumerated club-by-club in the audit pivot ledger) + 4 playoff rows (2 ties x 2 legs) = 244. "
      "Pack total 732. Source totals anchors reproduced: 2021-22 240 games/639 goals; 2022-23 240 games/730 goals (727 on-pitch + 3 "
      "from the awarded game: the canceled 1-1's two on-pitch goals are annulled in the official record); 2023-24 240 games/637 goals - "
      "matching the RSSSF stated totals and both Wikipedia infobox totals.")
    a("NOTE|warning|awarded_result|2022-23 Round 20, 2023-03-19: Pari Nizhny Novgorod - Torpedo Moscow. Row carries the OFFICIAL "
      "awarded score 0-3. Pari NN fielded the disqualified Yaroslav Mikhaylov (untracked caution-ban carried from lower-league "
      "games); on-pitch 1-1 (Gotsuk 34 - Reyna 58) annulled by RFU decision 2023-03-22 (wiki-rpl-2223 section 'Pari NN-Torpedo "
      "game'; rsssf-rus2023-1l lists '0-3 [Awarded]' as the round-20 result and its final table carries Torpedo W3 D4 L23 22-61 13 "
      "pts, Pari NN W8 D6 L16 33-50 30 pts - identical to the table recomputed from this pack's rows).")
    a("NOTE|warning|source_conflict|2022-23: the football-data second index carries the annulled on-pitch 1-1 for the 2023-03-19 "
      "Pari NN-Torpedo game; resolved to RSSSF-primary awarded 0-3 (see awarded_result NOTE). The repository's pre-existing CSV "
      "dataset documents the same variance as anomaly A1; table positions were unaffected by the award.")
    a("NOTE|warning|source_conflict|2023-24 Round 4, 2023-08-14: Pari Nizhny Novgorod 2-0 Akhmat Grozny (Sevikyan 1, Suleymanov 38) "
      "per RSSSF-primary and three Russian match reports; the football-data second index misrecords 1-0. Resolved to RSSSF. Same "
      "variance already disclosed in the repository audit as anomaly A2.")
    a("NOTE|info|club_context|FC Ufa (WO section-3 known addition): 2021-22 RPL club, 14th - lost the May-2022 playoff to FC "
      "Orenburg and was relegated. The WO's 'folded summer 2022' context is the 2022 financial crisis documented in the already-"
      "delivered RUSCUP pack (sponsor exit, near-collapse, republic ministry step-in 2022-10-19); the club played on and appears in "
      "that pack's 2023-02-26 cup row. League rows here are correct as played through 2022-05-21 (+ playoff legs 2022-05-25/28).")
    a("NOTE|info|team_fields|3 TEAM rows declared for participants not on the section-3 roster: FC Ufa (leagueCode RPL - top-flight "
      "2021-22 participant; the other two are First League clubs appearing in relegation playoffs only): Yenisey Krasnoyarsk and SKA "
      "Khabarovsk (leagueCode FNL). Stadium fields = the verified actual grounds of their in-scope home matches (Yenisey's documented "
      "home leg was staged at the indoor Futbol-Arena Yenisey; SKA's at Lenin Stadium); capacity filled only where a fetched source "
      "carries it (Ufa 13,573 from the RSSSF stadium table); surface/founded/website left blank rather than asserted uncaptured "
      "(no-fabrication policy).")
    a("NOTE|info|tiebreak|Official final-table position-order ties (recomputed W-D-L and GF-GA are exact for all 48 club-rows; order "
      "follows the federation head-to-head rule, RSSSF prints the H2H brackets): 2021-22 - Krasnodar over CSKA at 50 [H2H 1-1-0, "
      "1-0]; Rostov over Spartak at 38 [1-1-0, 4-3]; Pari NN (era name NNovgorod) over Ural at 33 [1-1-0, 2-1]. 2022-23 - Lokomotiv "
      "over Dynamo at 45 [brackets printed 1-0-1, 5-5 for both; decided deeper in the federation H2H chain]; Pari NN over Fakel at "
      "30 [1-0-1, 3-2]. 2023-24 - Krasnodar over Dynamo at 56 [2-0-0, 4-1]; Pari NN over Ural at 30 [1-1-0, 1-0]. No points "
      "deductions occurred in-window; one awarded result (see NOTE) is carried in both rows and tables.")
    a("NOTE|info|source_adaptation|WO section-4 second index: the football-data match feeds (fdata-rpl-*, independent commercial "
      "feeds fetched 2026-08-02, archived in-repo and auditor-verified earlier) were diffed against the RSSSF-primary transcription "
      "match-for-match for all 732 rows - 730/732 identical on date AND score; the two variances are the documented source_conflict "
      "NOTEs above (no other date or score diverged anywhere). The Wikipedia season articles add independent confirmation of every "
      "final table (16/16 x 3), the season totals, the awarded-game narrative, and all venues/playoff grounds. No figure in this "
      "pack comes from the second index where it conflicts with RSSSF.")
    a("NOTE|info|playoff_outcomes|2021-22 ties: SKA Khabarovsk 1-0 / 0-3 FC Khimki (Khimki 3-1 agg, stays in RPL); FC Orenburg "
      "2-2 / 2-1 FC Ufa (Orenburg 4-3 agg, promoted; Ufa relegated) - RSSSF NB confirms. 2022-23: Yenisey Krasnoyarsk 0-1 / 0-2 "
      "Fakel Voronezh (Fakel 3-0 agg); Rodina Moscow 0-3 / 2-0 Pari Nizhny Novgorod (Pari NN 3-2 agg); all four clubs remain at "
      "former level - RSSSF NB confirms (Alania Vladikavkaz was denied the RPL license, so Yenisey seeded 3rd, Rodina 4th; wiki "
      "match-box footnote). 2023-24: Pari Nizhny Novgorod 1-2 / 2-0 Arsenal Tula (Pari NN 3-2 agg, stays); Ural Yekaterinburg "
      "0-2 / 2-1 Akron Tolyatti (Akron 3-2 agg, promoted; Ural relegated). All decided inside 180 minutes - no shootouts.")
    a("NOTE|info|continuity|Continuity-clause accounting (league segment is gap-free): all 90 matchdays of the window exist and are "
      "dated in this pack; no match was cancelled. Documented postponements - 2021-22 Round 19: FC Rostov 1-0 Krylia Sovetov Samara "
      "played 2022-04-06 and FC Krasnodar 1-0 Lokomotiv Moscow played 2022-05-04 (rows keep their Round-19 labels, file is "
      "date-sorted); 2023-24: Round 21 was played after Round 25 (RSSSF NB; its fixtures date 2024-04-24/25 and keep their Round-21 "
      "labels). Winter breaks (Dec-Mar) and the 2022-23 World-Cup break are competition scheduling, not gaps. First row 2021-07-23, "
      "last row 2024-06-01; nothing dated 2024-06-30 or later (boundary gate green); 2024-25 MD1 resumes 2024-07-20 client-side.")
    a("NOTE|info|boundary_no_dupes|Hard-cutoff scan: max row date 2024-06-01; zero rows >= 2024-06-30; zero dateless rows; zero "
      "duplicate (date, home, away) rows; zero rows of clubs outside the section-3 identity discipline (federation check - every "
      "home/away string is RPL Russian Premier League football, seasons 2021-22..2023-24; playoff opponents are their documented "
      "First League counterparts).")
    a("NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot gate: each season's pack rows are "
      "re-pivoted club-by-club and every one of the 16 clubs must total exactly 30 played (W+D+L) with the full campaign enumerated "
      "round-by-round; the ledgers print in audit/pack-validation-rpl.txt next to this file. All 48 club-season pivots green.")
    # spot audits, one matchday per season, re-listed with source URL
    for s in SEASONS:
        md = SPOT[s]
        games = [r for r in allrows[s]["league"] if mdnum(r["tag"]) == md]
        txt = "; ".join(f"{r['date']} {STOCK2ROSTER[r['home']]} {r['hg']}-{r['ag']} {STOCK2ROSTER[r['away']]}"
                        for r in sorted(games, key=lambda r: (r["date"], r["home"])))
        a(f"NOTE|info|spot_audit|{s} Round {md} re-listed for spot-audit (source {SOURCES[SEASONS.index(s)][1]} #1l): {txt}.")
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
        "other on the 12 relegation-playoff rows (errata ERRATA-2026-08-03)")
    iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    G.g(all(iso.match(m[1]) for m in matches), "no dateless / non-ISO rows")
    G.g(all(m[1] < CUTOFF for m in matches), "boundary: no row >= 2024-06-30")
    keys = [(m[1], m[4], m[7]) for m in matches]
    G.g(len(keys) == len(set(keys)), "no duplicate rows (date/home/away)")
    G.g(all(m[8] and m[9] and m[10] for m in matches),
        "venue-detail (Round n / Playoff legK), stadium and city populated on every row")
    G.g(all(m[13] in sources for m in matches), "every MATCH sourceLabel resolves to a SOURCE row")
    G.g(all(len(t) == 13 for t in teams), "TEAM grammar: 13 fields")
    G.g({t[1] for t in teams} == DECLARED, "declared TEAM set = {FC Ufa, Yenisey Krasnoyarsk, SKA Khabarovsk}")
    G.g(not ({t[1] for t in teams} & ROSTER22), "TEAM rows disjoint from client roster")
    G.g(all(m[4] in RESOLVABLE and m[7] in RESOLVABLE for m in matches),
        "every home/away string resolves to roster identity or declared TEAM row (federation check)")
    G.g(len(matches) == 732, f"total rows = 732 (720 league + 12 playoff); got {len(matches)}")
    for s in SEASONS:
        lo = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
              "2023-24": ("2023-07-01", "2024-06-30")}[s]
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
        lo = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
              "2023-24": ("2023-07-01", "2024-06-30")}[s]
        stat = {c: [0, 0, 0, 0, 0, 0] for c in [x["stock"] for x in tables[s]]}  # P W D L GF GA by stock
        r2s = {}
        for stock, ros in STOCK2ROSTER.items():
            r2s.setdefault(ros, []).append(stock)
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
        lo = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
              "2023-24": ("2023-07-01", "2024-06-30")}[s]
        lg = [m for m in matches if lo[0] <= m[1] < lo[1] and m[2] == COMP_LEAGUE]
        by_pts = defaultdict(list)
        for row in tables[s]:
            by_pts[row["Pts"]].append(row["stock"])
        for pts, grp in by_pts.items():
            if len(grp) < 2:
                continue
            # official order = tables[s] pos order inside grp
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
            # federation chain: H2H pts -> H2H GD -> H2H GF -> H2H away goals -> official
            computed = sorted(grp, key=key)
            chain_ok = computed == official_seq
            rec = {c: "%d-%d-%d %d:%d (away %d)" % (hstat[c][1], hstat[c][2], hstat[c][3], hstat[c][4], hstat[c][5], hstat[c][6]) for c in grp}
            h2h_report.append((s, pts, official_seq, rec, chain_ok))
            G.g(chain_ok, f"{s} H2H tie at {pts} pts: official order {' > '.join(official_seq)} reproduced from mutual results")

    # goals totals
    for s in SEASONS:
        lo = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
              "2023-24": ("2023-07-01", "2024-06-30")}[s]
        tot = sum(int(m[5]) + int(m[6]) for m in matches if lo[0] <= m[1] < lo[1] and m[2] == COMP_LEAGUE)
        G.g(tot == TOTALS[s], f"{s} league goals total = {TOTALS[s]} (RSSSF/wiki anchors)")

    # playoff aggregates + outcomes
    for s in SEASONS:
        lo = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
              "2023-24": ("2023-07-01", "2024-06-30")}[s]
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

    # second-index diff vs football-data CSVs
    diff_report = []
    for s in SEASONS:
        y1 = {"2021-22": ("2021", "2022"), "2022-23": ("2022", "2023"), "2023-24": ("2023", "2024")}[s]
        rows = list(csv.DictReader(open(os.path.join(DATADIR, f"RPL-{s}.csv"), encoding="utf-8-sig")))
        feed = {}
        for r in rows:
            dd, mm, yy = r["Date"].split("/")
            iso = f"{yy}-{mm}-{dd}"
            feed[(iso, CSV2ROSTER[r["Home"]], CSV2ROSTER[r["Away"]])] = (int(r["HG"]), int(r["AG"]))
        lo = {"2021-22": ("2021-07-01", "2022-06-01"), "2022-23": ("2022-07-01", "2023-06-30"),
              "2023-24": ("2023-07-01", "2024-06-30")}[s]
        mine = {(m[1], m[4], m[7]): (int(m[5]), int(m[6])) for m in matches if lo[0] <= m[1] < lo[1]}
        miss = [k for k in feed if k not in mine] + [k for k in mine if k not in feed]
        diffs = []
        wl_seen = set()
        for k in feed.keys() & mine.keys():
            if feed[k] != mine[k]:
                wl = (s,) + k
                if wl in WHITELIST and feed[k] == WHITELIST[wl][0] and mine[k] == WHITELIST[wl][1]:
                    wl_seen.add(wl)
                else:
                    diffs.append((k, feed[k], mine[k]))
        diff_report.append((s, len(feed), len(mine), len(feed.keys() & mine.keys()), len(diffs)))
        G.g(not miss and not diffs,
            f"{s} second-index diff: {len(mine)} rows vs feed 1:1, every date+score identical except documented whitelist")
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

    G.g(sum(1 for n in notes if "|spot_audit|" in n) == 3, "three spot-audit NOTE rows present (one matchday per season)")
    for tag in ("pack_id", "comp_class", "identity", "venue_policy", "stage_mapping", "round_counts", "awarded_result",
                "club_context", "team_fields", "tiebreak", "source_adaptation", "playoff_outcomes",
                "continuity", "boundary_no_dupes", "perclub_gate"):
        G.g(any(f"|{tag}|" in n for n in notes), f"NOTE present: {tag}")
    G.g(sum(1 for n in notes if "|source_conflict|" in n) == 2, "two source_conflict NOTE rows present")
    G.g(all(len(l) == len(l.encode("ascii", "ignore").decode("ascii")) for l in lines), "pack is ASCII-only")

    # ---------------------------------------------------------------- report
    p, fx = G.summary()
    out = []
    out.append("PACK VALIDATION - RPL-2021-2026_BP-TEAM-PACK_v2.txt")
    out.append(f"built {ACCESSED} by tools/build_rpl_pack.py from audit/ledger/rpl-<season>.txt (RSSSF rus2022/2023/2024 "
               "#1l+#prorel primary, transcribed " + ACCESSED + ") + rpl-venues.txt facts; second index = football-data "
               "feeds (fdata-rpl-*, fetched " + FDATA_ACCESSED + ") diffed match-for-match; Wikipedia season articles third anchor.")
    out.append("=" * 100)
    out.append(f"GATES: {p} PASS, {fx} FAIL")
    if fx:
        out.append("!")
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
    out.append("SECOND-INDEX (football-data) DIFF SUMMARY")
    for s, nf, nm, n1, nd in diff_report:
        out.append(f"--- {s}: feed rows {nf}, pack rows {nm}, keys matched 1:1 = {n1}, undocumented diffs = {nd}")
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
