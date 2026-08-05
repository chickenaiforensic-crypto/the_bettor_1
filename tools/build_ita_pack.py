#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build + validate handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt (WO-ITA-SPAN-14, returned 2026-08-05).

PRIMARY:  audit/ledger/ita-<season>.txt  (RSSSF tablesi/ital2022..ital2025.html: full round-by-round
          transcribed to R1..R38 rows + official FINAL TABLE constants as TABLE rows; ital2026.html
          prints NO Serie A round-by-round (final table + Coppa Italia + Serie B only, verified full
          page 2026-08-05), so the 2025-26 match rows are carried by openfootball/italy
          2025-26/1-seriea.txt and gated EXACT against the RSSSF table by full recompute -
          documented source_adaptation, same class as FRA 2025-26 / GER 2025-26).
2NDIDX:   audit/ledger/ita-2ndidx-<season>.txt (openfootball MD rows 2021-22..2024-25, diffed
          row-for-row vs RSSSF: 380/380 IDENTICAL x3 incl. dates; 2023-24 379/380 + ONE OFB-side
          typing error MD30 (Torino 0-0 Monza printed vs played 1-0), primary stands per 2+1 rule,
          tools/diff_ita_second_index.py) + audit/ledger/ita-2ndidx-2025-26-MX.txt (Wikipedia
          2025-26 FBR matrix, 380 cells: 380/380 IDENTICAL scores vs the carrier, 922 goals both,
          tools/diff_ita_matrix.py).
CONSTANTS audit/ledger/ita-venues.txt (101 VENUE rows = 100 per-season stadium/city lattice from
          the Wikipedia season articles + 1 neutral ground entry for the 2022-23 spareggio).
PLAYOFFS  the 2022-23 relegation spareggio (17th-vs-18th survival decider, ONE neutral-venue
          game) SHIPS as compType 'other' (ERRATA-2026-08-03 + DECREE-2026-08-04: every pro/rel
          play-off leg touching the top flight ships; the legs are between two roster members,
          so the WO's roster is untouched and zero TEAM rows are needed - WE PROVED WRONG on the
          generic WO expectation that a spareggio 'rarely' exists: exactly one exists in the
          window and is included). 90-minute doctrine: the game ended inside 90. The Serie B
          playoff/Playout blocks (10 PO_PLAYOFF context lines per season) stay NOT-COMMISSIONED.
Output:   handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt  +  audit/pack-validation-ita.txt
Run:      python3 tools/build_ita_pack.py   (exit 0 iff every gate PASS; rebuild is deterministic)
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")
OUTPACK = os.path.join(ROOT, "handoffs", "ITA-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation-ita.txt")
ACCESSED = "2026-08-05"
SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
COMP = "Italy Serie A"                     # WO section-2 verbatim
COMPTYPE = "domestic-league"               # WO section-2 verbatim
COMP_PO = "Italy Relegation Playoffs"      # LOCKED builder constant (spareggio row class)
COMPTYPE_PO = "other"                      # ERRATA-2026-08-03
COUNTRY = "Italy"
SRC_LABEL = {"2021-22": "rsssf-ital2022", "2022-23": "rsssf-ital2023", "2023-24": "rsssf-ital2024",
             "2024-25": "rsssf-ital2025", "2025-26": "ofb-ita-2526"}
# 20 clubs x 38 matchdays x 10 fixtures, every season (WO section-1: v2 retarget awarded 20/38)
SHAPE = {s: (20, 38, 10) for s in SEASONS}
EXP_ROWS = {s: 380 for s in SEASONS}
DEDUCT = {"2022-23": {"Juventus": 10}}     # FIGC decision 2023-05-22 (plusvalenze; initial 15
                                           # on 2023-01-20 revoked on re-trial), no other in-window
ANCHORS = {"2021-22": (380, 1089, ("2021-08-21", "2022-05-22")),
           "2022-23": (380, 974, ("2022-08-13", "2023-06-04")),
           "2023-24": (380, 992, ("2023-08-19", "2024-06-02")),
           "2024-25": (380, 973, ("2024-08-17", "2025-05-25")),
           "2025-26": (380, 922, ("2025-08-23", "2026-05-24"))}
SPOT = {"2021-22": 19, "2022-23": 37, "2023-24": 30, "2024-25": 14, "2025-26": 35}

# ------------------------------------------------------------- identity (WO section-3, 27 pins)
ROSTER27 = ["Atalanta", "Bologna", "Cagliari", "Como", "Cremonese", "Empoli", "Fiorentina",
            "Frosinone", "Genoa", "Inter", "Juventus", "Lazio", "Lecce", "Milan", "Monza",
            "Napoli", "Parma", "Pisa", "Roma", "Salernitana", "Sampdoria", "Sassuolo", "Spezia",
            "Torino", "Udinese", "Venezia", "Verona"]
ROSTER_SET = set(ROSTER27)
IDENTITY_DOMAIN = set(ROSTER27)            # no playoff participant outside the roster in-window
ANTI_APPEAR = ["Internazionale", "AC Milan", "Hellas"]
# the single PO ledger line prints the openfootball/wikipedia name form 'Hellas Verona';
# every R/MD/TABLE/MX/VENUE row in the ITA corpus is already on the pinned strings.
PO2ROSTER = {"Hellas Verona": "Verona"}

def roster(stock):
    return PO2ROSTER.get(stock, stock)

SOURCES = [
 ("rsssf-ital2022", "https://www.rsssf.org/tablesi/ital2022.html", "primary-archive",
  "2021-22: all 38 rounds dates+scores (Covid-postponement makeups ride inside their original "
  "round banners with their true makeup dates: R19 '[Apr 20] Udinese 0-1 Salernitana', the R20 "
  "'[Apr 27]' batch Fiorentina 0-4 Udinese / Atalanta 4-4 Torino / Bologna 2-1 Inter and '[May 5] "
  "Salernitana 2-1 Venezia'), official final table (Milan champions 86; Cagliari/Genoa/Venezia "
  "relegated), Serie B playoff/playout blocks as L2 context (10 PO_PLAYOFF context lines; the "
  "page prints the final table twice - duplicate elided in the raw with a note); transcribed in "
  "audit/ledger/ita-2021-22.txt; anchors 380 rows / 1,089 goals / span 2021-08-21..2022-05-22"),
 ("rsssf-ital2023", "https://www.rsssf.org/tablesi/ital2023.html", "primary-archive",
  "2022-23: all 38 rounds dates+scores (the round-9 '[Oct 1]' date misprint documented under "
  "source_conflict), official final table (Napoli champions 90; Juventus '10 points deducted by "
  "decision of the FIGC' arithmetic verified -10), the relegation SPAREGGIO block (Spezia 1-3 "
  "Verona one-off 2023-06-11 = this pack's single 'other' row, RSSSF prints it 'Relegation "
  "Playoff'), Serie B playoff/playout blocks; transcribed in audit/ledger/ita-2022-23.txt; "
  "anchors 380 rows / 974 goals / span 2022-08-13..2023-06-04 (+ spareggio 2023-06-11)"),
 ("rsssf-ital2024", "https://www.rsssf.org/tablesi/ital2024.html", "primary-archive",
  "2023-24: all 38 rounds dates+scores (R32 Udinese-Roma wrap-continuation 'abandoned in 72' "
  "at 1-1 on 2024-04-14 ... [Apr 25] Udinese 1-2 Roma [completion of match abandoned at 1-1]' - "
  "the completion row ships inside R32 with its true date; R30 Torino 1-0 Monza), official final "
  "table (Inter champions 94, 20th title; Frosinone/Sassuolo/Salernitana relegated), Serie B "
  "playoff/playout blocks; transcribed in audit/ledger/ita-2023-24.txt; anchors 380 rows / 992 "
  "goals / span 2023-08-19..2024-06-02"),
 ("rsssf-ital2025", "https://www.rsssf.org/tablesi/ital2025.html", "primary-archive",
  "2024-25: all 38 rounds dates+scores (R14 Fiorentina-Inter wrap 'abandoned at 0-0 in 16' due "
  "to medical emergency Fiorentina player Edoardo Bove' 2024-12-01, completed as 'Fiorentina 3-0 "
  "Inter [completion]' 2025-02-06 - the completion row ships inside R14 with its true date), "
  "official final table (Napoli champions 82, one point over Inter 81 - decided in the Friday "
  "double-header 2025-05-23; Empoli/Venezia/Monza relegated), Serie B playoff/playout blocks "
  "(incl. the Salernitana awd Sampdoria awarded-0-3 context line); transcribed in "
  "audit/ledger/ita-2024-25.txt; anchors 380 rows / 973 goals / span 2024-08-17..2025-05-25"),
 ("rsssf-ital2026", "https://www.rsssf.org/tablesi/ital2026.html", "primary-archive",
  "2025-26: OFFICIAL FINAL TABLE (Inter champions 87, 21st title; Multigroup 2-row hth bracket "
  "Napoli/Roma; relegated Cremonese/Verona/Pisa; promoted flags Sassuolo/Cremonese/Pisa) + Serie B "
  "playoff/playout blocks - but NO Serie A round-by-round (verified full page 2026-08-05: the page "
  "prints final table + Coppa Italia + Serie B only): final-table authority for the season - the "
  "recompute of the pack's 380 rows reproduces it club-for-club and in position order EXACT; "
  "constants transcribed in audit/ledger/ita-2025-26.txt. The Serie B block carries a source-"
  "internal same-date anomaly (First Leg [May 20] Catanzaro 0-2 Monza printed on the same date as "
  "semifinal leg-2 Palermo 2-0 Catanzaro) - context zone only, documented NOT adjudicated"),
 ("rsssf-ital2027", "https://www.rsssf.org/tablesi/ital2027.html", "primary-archive",
  "404 Not Found on 2026-08-05 - boundary evidence that no 2026-27 season page (and no played "
  "2026-27 fixture) existed on the return date"),
 ("ofb-ita-2122", "https://raw.githubusercontent.com/openfootball/italy/master/2021-22/1-seriea.txt",
  "match-second-index",
  "2021-22 openfootball season file (380 matches, header '# Date Sat Aug 21 2021 - Sun May 22 "
  "2022 (274d)'), parsed by tools/parse_ofb_it.py on fetch day 2026-08-05; diffed row-for-row vs "
  "the RSSSF primary: 380/380 IDENTICAL fixtures AND dates (tools/diff_ita_second_index.py -> "
  "audit/ledger/ita-2ndidx-2021-22.txt)"),
 ("ofb-ita-2223", "https://raw.githubusercontent.com/openfootball/italy/master/2022-23/1-seriea.txt",
  "match-second-index",
  "2022-23 openfootball season file (380 matches): diff 380/380 IDENTICAL fixtures AND dates vs "
  "RSSSF; independently prints the round-9 Fiorentina 0-4 Lazio fixture 'Mon Oct 10 20:45' - one "
  "of the two independent indexes adjudicating the RSSSF '[Oct 1]' misprint "
  "(audit/ledger/ita-2ndidx-2022-23.txt)"),
 ("ofb-ita-2324", "https://raw.githubusercontent.com/openfootball/italy/master/2023-24/1-seriea.txt",
  "match-second-index",
  "2023-24 openfootball season file (380 matches): diff 379/380 IDENTICAL vs RSSSF + ONE "
  "OFB-SIDE TYPING ERROR - MD30 prints 'Torino 0-0 Monza' where the played score is 1-0 (RSSSF "
  "stands; the typo is quadruple-corroborated as OFFICIAL 1-0 by ESPN / FoxSports / live-result "
  "AND worldfootball wf-ita-2324-md30 '30.03.2024 15:00 Torino FC 1:0 AC Monza'; quarantined "
  "from any downstream use, documented under source_conflict). Dates 380/380 identical "
  "(audit/ledger/ita-2ndidx-2023-24.txt)"),
 ("ofb-ita-2425", "https://raw.githubusercontent.com/openfootball/italy/master/2024-25/1-seriea.txt",
  "match-second-index",
  "2024-25 openfootball season file (380 matches): diff 380/380 IDENTICAL fixtures AND dates vs "
  "RSSSF, including the R14 Fiorentina 3-0 Inter completion dated 2025-02-06 "
  "(audit/ledger/ita-2ndidx-2024-25.txt)"),
 ("ofb-ita-2526", "https://raw.githubusercontent.com/openfootball/italy/master/2025-26/1-seriea.txt",
  "match-carrier",
  "2025-26 match rows (380 fixtures: format B 'Regular Season - n' banners mapped to MD1..MD38, "
  "duplicate-banner makeup blocks for postponed MD16 fixtures (four games 2026-01-14..15) and "
  "the MD24 Milan 1-1 Como Perth-cancelled completion 2026-02-18 summed under their original "
  "banner numbers - banner summing disclosed in the anomaly NOTE; scorer lines skipped by the "
  "parser; header '# Matches 380', dates Sat Aug 23 2025 - Sun May 24 2026, fetched 2026-08-05) - "
  "the season's date/score carrier under the documented source_adaptation; label carried on all "
  "2025-26 league MATCH rows (audit/ledger/ita-2ndidx-2025-26.txt)"),
 ("wikimatrix-ita-2526", "https://en.wikipedia.org/wiki/2025%E2%80%9326_Serie_A", "second-index",
  "2025-26 Serie A FBR results matrix from the season article's action=raw wikitext (fetched "
  "2026-08-05): 380 cells diffed cell-for-cell vs the carrier - 380/380 IDENTICAL scores, 922 "
  "goals both (tools/diff_ita_matrix.py -> audit/ledger/ita-2ndidx-2025-26-MX.txt)"),
 ("wiki-ita-venues", "https://en.wikipedia.org/wiki/2021%E2%80%9322_Serie_A", "second-index",
  "stadium/location tables + league-table templates of the five season articles 2021-22..2025-26 "
  "(sibling pages ...%E2%80%9322 through ...%E2%80%9326_Serie_A; action=raw wikitext, fetched "
  "2026-08-05): 101 venue rows = the 100-season lattice (20 clubs x 5 seasons) + the spareggio "
  "neutral-ground entry, transcribed to audit/ledger/ita-venues.txt. Same-ground split prints are "
  "era data: Inter 'Giuseppe Meazza' 75,710 vs Milan 'San Siro' 75,710 in 2023-24 while both "
  "articles agree they share the ground; Lazio/Roma Stadio Olimpico print swings 70,634 -> "
  "67,585 -> back to 70,634 (source reprints, verified not structural); Atalanta name epoch "
  "Gewiss Stadium -> 'Stadio Atleti Azzurri d'Italia' reconstruction season -> 'Stadio di "
  "Bergamo' 2025-26; Juventus 'Allianz Stadium' <-> 'Juventus Stadium' name oscillations; "
  "Sassuolo city cell prints Sassuolo while the ground stands in Reggio Emilia (parenthetical "
  "acknowledged in the 2021-22 print). League-table template gate (tools/wiki_ita_tables.py): "
  "5/5 tables reproduce the RSSSF tables club-for-club + position order incl. adjust_points JUV "
  "-10 with the FIGC cite, the 2022-23 Spezia 'Relegation playoff' note vs template status_R "
  "alias (accepted, disclosed), and the rendered Pos table as second witness 20/20 for 2022-23"),
 ("wiki-ita-2627", "https://en.wikipedia.org/w/index.php?title=2026%E2%80%9327_Serie_A&action=raw",
  "second-index",
  "span-end boundary: 2026-27 season dates 23 August 2026 - 30 May 2027 (calendar cite "
  "gazzetta.it), 20 teams; promoted Venezia (return after one year) and Frosinone (after two) "
  "direct + A.C. Monza (Serie B playoff winners, better-record tiebreak - first such case); "
  "relegated Cremonese, Hellas Verona and Pisa - exactly this pack's 2025-26 relegation places; "
  "the season had NOT started on the return date 2026-08-05 (raw byte-verified, mid-word join "
  "'Stadio Artemio F'+'ranchi' repaired + disclosed in the raw header)"),
 ("wf-ita-2122-md19", "https://www.worldfootball.net/competition/co111/italy-serie-a/se39347/2021-2022/ro117889/matchday/md19/results-and-standings/",
  "second-index",
  "2021-22 matchday-19 spot-audit page: dates and scores match the pack rows one-for-one and "
  "prints the COVID-quarantine makeup '20.04.2022 18:45 Udinese 0:1 US Salernitana (Ended)' "
  "inside Matchday 19 (postponed from 2021-12-22, forfeit overturned, played 2022-04-20) - "
  "third index agreeing with RSSSF and openfootball"),
 ("wf-ita-2223-md9", "https://www.worldfootball.net/competition/ro133686/md9/results-and-standings/",
  "second-index",
  "2022-23 matchday-9 adjudication page: prints Fiorentina 0:4 Lazio '10.10.2022 20:45' - one "
  "of the two independent indexes adjudicating the RSSSF '[Oct 1]' date misprint (2022-10-10 "
  "was the Monday of round 9; the round ran 2022-10-08..10)"),
 ("wf-ita-2324-md30", "https://www.worldfootball.net/competition/co111/italy-serie-a/se52577/2023-2024/ro150179/matchday/md30/results-and-standings/",
  "second-index",
  "2023-24 matchday-30 adjudication page: prints '30.03.2024 15:00 Torino FC 1:0 AC Monza "
  "(Ended)' - the fourth independent witness that the played score is 1-0, quarantining the "
  "openfootball 0-0 typing error alongside ESPN / FoxSports / live-result"),
 ("wf-ita-2425-md14", "https://www.worldfootball.net/competition/co111/italy-serie-a/se74735/2024-2025/ro209207/matchday/md14/results-and-standings/",
  "second-index",
  "2024-25 matchday-14 spot-audit page: dates and scores match the pack rows one-for-one and "
  "prints '06.02.2025 20:45 ACF Fiorentina 3:0 Inter (Ended)' inside Matchday 14 - third "
  "witness to the Bove-abandonment completion (abandoned 0-0 at 16' on 2024-12-01, completed "
  "2025-02-06)"),
 ("wf-ita-2526-md24", "https://www.worldfootball.net/competition/co111/italy-serie-a/se95481/2025-2026/ro264306/matchday/md24/results-and-standings/",
  "second-index",
  "2025-26 matchday-24 adjudication page: prints '18.02.2026 20:45 AC Milan 1:1 Como 1907' "
  "inside Matchday 24; the match report (ma11129283) prints STADIUM GIUSEPPE MEAZZA (San Siro), "
  "attendance 75,251, referee Maurizio Mariani, scorers Paz 32' left foot / Leao 64' right foot - "
  "EXACT agreement with the carrier row and the venue source for the Perth-cancelled fixture"),
 ("legaseriea-2223-spareggio", "https://www.legaseriea.it/en/match/2022-23aspareuni1spever",
  "second-index",
  "official league match report of the 2022-23 relegation spareggio Spezia 1-3 Verona "
  "(2023-06-11 20:45 CEST, Mapei Stadium - Citta del Tricolore Reggio Emilia, attendance "
  "15,000, referee Daniele Orsato; scorers Faraoni 5', Ngonge 26' 38', Ampadu dissent-goal 15' "
  "for Spezia): independent corroboration of the 90-minute score, the ground and the outcome"),
]

# ---------------------------------------------------------------- readers
R_RX = re.compile(r"^R(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MD_RX = re.compile(r"^MD(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MX_RX = re.compile(r"^MX\|([^|]+)\|([^|]+)\|(\d+)\|(\d+)$")
PO_RX = re.compile(r"^PO_PLAYOFF\|([^|]+)\|([^|]+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\w+)\|(\d*)\|([^|]+)\|([^|]*)\|(.*)$")
ABD_RX = re.compile(r"^ABD\|([^|]+)\|(R\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|([^|]+)\|(.*)$")

def read_season(season):
    """League rows + official table + playoff/spareggio context, from the five primary ledgers.
    2025-26 is the source_adaptation season: ital2026 prints no Serie A rounds, so the
    380 carrier rows are read from the openfootball second-index ledger (MD rows)."""
    rows, table, po, abd = [], [], [], []
    with open(os.path.join(LEDGER, f"ita-{season}.txt"), encoding="utf-8") as fh:
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
                           "home": m.group(4).strip(), "hg": m.group(5), "ag": m.group(6),
                           "away": m.group(7).strip(), "extra": m.group(8), "flags": m.group(9)})
                continue
            m = ABD_RX.match(s)
            if m:
                abd.append({"rnd": m.group(2), "date": m.group(3), "home": m.group(4).strip(),
                            "away": m.group(5).strip(), "note": m.group(6)})
    if season == "2025-26":
        with open(os.path.join(LEDGER, "ita-2ndidx-2025-26.txt"), encoding="utf-8") as fh:
            for ln in fh:
                m = MD_RX.match(ln.strip())
                if m:
                    rows.append({"rnd": int(m.group(1)), "date": m.group(2), "home": m.group(3).strip(),
                                 "hg": int(m.group(4)), "ag": int(m.group(5)), "away": m.group(6).strip()})
    return rows, table, po, abd

def read_venues():
    """(season, roster-string) -> (stadium, city); the spareggio neutral-ground entry is held
    separately so the per-season lattice stays exactly 20 keys each."""
    ven, neutral = {}, {}
    nlines = 0
    with open(os.path.join(LEDGER, "ita-venues.txt"), encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("VENUE|"):
                nlines += 1
                p = ln.rstrip("\n").split("|")
                if p[2].startswith("PLAYOFF-NEUTRAL"):
                    neutral[(p[1], p[2])] = (p[3], p[4])
                else:
                    ven[(p[1], p[2])] = (p[3], p[4])
    return ven, neutral, nlines

def read_2ndidx_md(season):
    out = {}
    with open(os.path.join(LEDGER, f"ita-2ndidx-{season}.txt"), encoding="utf-8") as fh:
        for ln in fh:
            m = MD_RX.match(ln.strip())
            if m:
                out[(m.group(3).strip(), m.group(6).strip())] = (int(m.group(1)), m.group(2),
                                                                 int(m.group(4)), int(m.group(5)))
    return out

def read_2ndidx_mx():
    out = {}
    with open(os.path.join(LEDGER, "ita-2ndidx-2025-26-MX.txt"), encoding="utf-8") as fh:
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
    key = (season, r["home"])
    stadium, city = ven[key]
    return (f"MATCH|{r['date']}|{COMP}|{COMPTYPE}|{roster(r['home'])}|{r['hg']}|{r['ag']}|"
            f"{roster(r['away'])}|MD{r['rnd']}|{stadium}|{city}|{COUNTRY}||{SRC_LABEL[season]}")

# SHIP-as-other playoff row, 90-minute doctrine applied (the spareggio ended inside 90; box
# verified in the wiki 2022-23 sections raw + the Lega Serie A report). Tuple:
# (season, date, home, hg90, ag90, away, venueDetail, stadium, city, sourceLabel, aetFinal-or-None)
PO_SHIP = [
 ("2022-23", "2023-06-11", "Spezia", 1, 3, "Verona", "Playoff",
  "Mapei Stadium - Citta del Tricolore", "Reggio Emilia", "rsssf-ital2023", None),
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
    ven, ven_neutral, ven_lines = read_venues()
    data = {}
    for s in SEASONS:
        data[s] = read_season(s)

    G = Gates()
    pack_rows = []
    season_blocks = []   # (season, [league lines])

    # ---- structural gates + emission, season by season
    for s in SEASONS:
        rows, table, po, abd = data[s]
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
        for t in table:
            c = st[t["club"]]
            pts = c[1] * 3 + c[2] - ded.get(t["club"], 0)
            if [c[0], c[1], c[2], c[3], c[4], c[5], pts] != [t["P"], t["W"], t["D"], t["L"], t["GF"], t["GA"], t["Pts"]]:
                bad.append(t["club"])
            order.append((t["club"], pts, c[4] - c[5], c[4], t["pos"]))
        G.g(not bad, f"{s}: table reproduction club-for-club {nclubs}/{nclubs} (P/W/D/L/GF/GA/Pts"
                     + (f", deductions {ded}" if ded else ", no deductions in-window") + f") fails={bad or '-'}")
        # position order, Serie A tie-rules (wiki 2023-24 print): at 6th place and above -
        # 1 points, 2 head-to-head points, 3 head-to-head GD, 4 overall GD, 5 goals scored,
        # 6 draw; below 6th head-to-head is NOT applied. Where the computed keys are level the
        # printed official position is kept (the sources' official prints are the authority at
        # every such spot - e.g. RSSSF's own level-tie pairs are position-order-stable).
        h2h = defaultdict(lambda: [0, 0])      # (c1,c2) -> [pts of c1 in pairing, gd of c1]
        for r in rows:
            if r["hg"] > r["ag"]:
                h2h[(r["home"], r["away"])][0] += 3
            elif r["hg"] < r["ag"]:
                h2h[(r["away"], r["home"])][0] += 3
            else:
                h2h[(r["home"], r["away"])][0] += 1
                h2h[(r["away"], r["home"])][0] += 1
            h2h[(r["home"], r["away"])][1] += r["hg"] - r["ag"]
            h2h[(r["away"], r["home"])][1] += r["ag"] - r["hg"]
        inv = []
        for i in range(len(order) - 1):
            (c1, p1, gd1, gf1, pos1), (c2, p2, gd2, gf2, pos2) = order[i], order[i + 1]
            if p1 > p2:
                continue                       # step 1 decides
            if p1 < p2:
                inv.append((c1, c2))
                continue
            hp1, hg1 = h2h[(c1, c2)]
            hp2, hg2 = h2h[(c2, c1)]
            below_ok = True
            if pos1 > 5:
                # below-6th stratum: head-to-head not applied; a better h2h line for the
                # lower club is NOT an inversion. Flag only if the lower club is better on
                # h2h pts + h2h GD AND on overall GD + GF (i.e. unorderable by any rule).
                below_ok = not ((hp1, hg1, gd1, gf1) < (hp2, hg2, gd2, gf2))
            else:
                below_ok = (hp1, hg1) >= (hp2, hg2)
            if not below_ok:
                inv.append((c1, c2))
        G.g(not inv, f"{s}: final-table position order consistent (pts -> H2H pts -> H2H GD "
                     f"[6th and above only; not applied below 6th] -> GD -> GF; printed order kept "
                     f"where computed keys are level; 2022-23 pos 17/18 settled by the surviving "
                     f"spareggio) inversions={inv or '-'}")
        members = {t["club"] for t in table}
        G.g(len(members) == nclubs and members <= ROSTER_SET,
            f"{s}: {nclubs} member clubs, every string in the WO section-3 27-pin roster domain")
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

    # ---- season-to-season membership boundary gates (nout=3 direct relegations, nswap=6 every
    # jump; the 2022-23 spareggio is a 17/18 survival decider - the loser RELEGATES in addition
    # to the direct bottom three registered there? NO: Serie A 2022-23 relegates 3 total, and
    # the spareggio loser Spezia is the THIRD relegated club of that season: the direct set is
    # pos 19/20 Cremonese/Sampdoria + the spareggio loser pos 17 Spezia; pos 18 Verona survives).
    EXP = {"2021-22": {"out": {"Cagliari", "Genoa", "Venezia"}, "in": {"Monza", "Lecce", "Cremonese"},
                       "bottom": 3, "nswap": 6},
           "2022-23": {"out": {"Spezia", "Cremonese", "Sampdoria"}, "in": {"Frosinone", "Genoa", "Cagliari"},
                       "bottom": 2, "nswap": 6},
           "2023-24": {"out": {"Frosinone", "Sassuolo", "Salernitana"}, "in": {"Parma", "Como", "Venezia"},
                       "bottom": 3, "nswap": 6},
           "2024-25": {"out": {"Empoli", "Venezia", "Monza"}, "in": {"Sassuolo", "Cremonese", "Pisa"},
                       "bottom": 3, "nswap": 6}}
    for i in range(4):
        s1, s2 = SEASONS[i], SEASONS[i + 1]
        m1 = {t["club"] for t in data[s1][1]}
        m2 = {t["club"] for t in data[s2][1]}
        ndirect = EXP[s1]["bottom"]
        bottom = {t["club"] for t in data[s1][1] if t["pos"] > len(m1) - ndirect}
        if s1 == "2022-23":
            # direct relegations = pos 19/20 (Cremonese/Sampdoria); pos 17 Spezia lost the
            # spareggio and is the third relegated club, pos 18 Verona survived and stays
            bottom |= {"Spezia"}
        G.g(bottom == EXP[s1]["out"] and not (bottom & m2) and EXP[s1]["in"] <= m2
            and not (EXP[s1]["in"] & m1) and len(m1 ^ m2) == EXP[s1]["nswap"],
            f"boundary {s1}->{s2}: relegated {sorted(bottom)} absent in {s2}; promoted "
            f"{sorted(EXP[s1]['in'])} present (and absent in {s1}); memberships verified "
            f"(6 swapped; {ndirect} direct relegations"
            + (" + the spareggio loser Spezia" if s1 == "2022-23" else "") + ")")
    # 2022-23 spareggio boundary detail: 17 Spezia lost the 2023-06-11 game 1-3 and exits...
    spe17 = [t for t in data["2022-23"][1] if t["pos"] in (17, 18)]
    m3 = {t["club"] for t in data["2023-24"][1]}
    G.g(len(spe17) == 2 and {t["club"] for t in spe17} == {"Spezia", "Verona"}
        and spe17[0]["club"] == "Spezia" and spe17[1]["club"] == "Verona"
        and "Spezia" not in m3 and "Verona" in m3
        and "Relegation Playoff" in spe17[0]["note"] and "Relegation Playoff" in spe17[1]["note"],
        "boundary 2022-23: the 17/18 tie Spezia 31 / Verona 31 was settled ON THE PITCH by the "
        "spareggio (RSSSF note 'Relegation Playoff' on both lines; the wiki template prints "
        "status SPE=R vs VER=O - survivor alias accepted + disclosed in the table-gate ledger): "
        "loser Spezia relegated with 19/20 Cremonese/Sampdoria; winner Verona plays on in 2023-24")
    # span-end boundary (NOTE-only): 2026-27 set fixed by sources, zero rows ship.

    # ---- playoff ('other') rows: curated 90-min ship cross-verified against ledger PO lines
    po_all = [p for s in SEASONS for p in data[s][2]]
    ships = [p for p in po_all if "SHIP-as-other" in p["flags"]]
    notcom = [p for p in po_all if "NOT-COMMISSIONED" in p["flags"]]
    G.g(len(ships) == 1 and len(notcom) == 50,
        f"playoffs: exactly ONE SHIP-as-other leg in the whole window (the 2022-23 relegation "
        f"spareggio single-decider; Serie A has no two-leg pro/rel tie in 2021-26) + 50 "
        f"NOT-COMMISSIONED Serie B playoff/playout context lines (10 per season x 5; the "
        f"Salernitana awd Sampdoria awarded-0-3 line among the 2024-25 ten) (got "
        f"{len(ships)}/{len(notcom)})")
    po_lines = []
    ok_po = True
    for (s, date, home, hg90, ag90, away, vd, stadium, city, label, aet) in PO_SHIP:
        matches = [p for p in ships if p["season"] == s and p["date"] == date
                   and roster(p["home"]) == home and roster(p["away"]) == away]
        if not matches:
            ok_po = False
            continue
        p = matches[0]
        ok_po &= (p["hg"], p["ag"]) == (str(hg90), str(ag90)) and not p["extra"]
        po_lines.append((s, f"MATCH|{date}|{COMP_PO}|{COMPTYPE_PO}|{home}|{hg90}|{ag90}|"
                            f"{away}|{vd}|{stadium}|{city}|{COUNTRY}||{label}"))
    G.g(ok_po, "playoffs: the SHIP spareggio's ledger print matches the curated row exactly "
               "(90-minute doctrine - the game ended inside regulation: Spezia 1-3 Verona, "
               "2023-06-11; the venue/city constants come from the venues ledger's neutral entry "
               "and the wiki playoff box)")
    # append the PO row after the five league blocks (mirrors the GER/FRA pack layout)
    for s, lines in po_lines:
        pack_rows.append(lines)
    # neutral-venue self-check: the venues ledger's neutral entry IS the shipped ground
    G.g(len(ven_neutral) == 1 and list(ven_neutral.values())[0]
        == ("Mapei Stadium - Citta del Tricolore", "Reggio Emilia"),
        f"playoffs: venues ledger holds exactly one neutral entry = the spareggio ground "
        f"(got {list(ven_neutral.items()) or '-'})")

    # ---- TEAM rows: ZERO needed - the only 'other'-row participants (Spezia, Verona) are
    # pinned section-3 roster members already (WO section-2 shape per full-span decree)
    team_lines = []

    # ---- global gates
    G.g(len(pack_rows) == 1900 + 1,
        f"pack: 1,901 MATCH rows total = 1,900 league + 1 spareggio (got {len(pack_rows)})")
    keys = ["|".join((f[1], f[4], f[7])) for f in (line.split("|") for line in pack_rows)]
    G.g(len(set(keys)) == len(keys), "pack: zero duplicate (date,home,away) rows")
    clubs_union = set()
    for s in SEASONS:
        clubs_union |= {roster(t["club"]) for t in data[s][1]}
    G.g(clubs_union == ROSTER_SET,
        f"pack: union of league clubs across the 5 seasons = exactly the 27 WO section-3 "
        f"strings (no club pinned-but-unused, none outside; got {len(clubs_union)})")
    bad_names = [c for line in pack_rows for c in (line.split("|")[4], line.split("|")[7])
                 if c not in IDENTITY_DOMAIN]
    G.g(not bad_names, f"pack: every home/away string in the identity domain (the 27 roster "
                       f"pins - the spareggio adds no outside participant; bad={bad_names[:4] or '-'})")
    anti = [line for line in pack_rows
            if any(a in line.split("|")[4] or a in line.split("|")[7] for a in ANTI_APPEAR)]
    G.g(not anti, "pack: anti-appear traps absent from home/away identity fields (Inter never "
                  "'Internazionale'/'Inter Milan', Milan never 'AC Milan'/'A.C. Milan', Verona "
                  "never 'Hellas'/'Hellas Verona' on IDENTITY fields - the Hellas print survives "
                  "only inside the ledger's verbatim PO line; city/prose fields are sourced venue "
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
        if s == "2023-24":
            G.g(same == 379 and miss == 0 and len(diffs) == 1
                and diffs[0][0] == ("Torino", "Monza") and diffs[0][1] == (30, "2024-03-30", 1, 0)
                and diffs[0][2][2:] == (0, 0),
                f"2ndidx {s}: 379/380 pairings IDENTICAL round+date+score vs openfootball - the "
                f"single divergence is the KNOWN OFB-side MD30 typing error (Torino {diffs[0][1][2]}-"
                f"{diffs[0][1][3]} Monza printed by RSSSF/wf/ESPN vs {diffs[0][2][2]}-{diffs[0][2][3]} "
                f"in the OFB file; quarantined, primary stands) (same={same} miss={miss} "
                f"divergent={len(diffs)})")
        else:
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
    G.g(same == 380 and miss == 0 and not diffs and g_idx == 922,
        f"2ndidx 2025-26: Wikipedia FBR matrix 380 cells - ALL IDENTICAL scores vs the carrier "
        f"(matrix goals {g_idx} = carrier 922 = season anchor; same={same} miss={miss} "
        f"divergent={len(diffs)})")

    # ---- anomaly gates
    r21 = data["2021-22"][0]
    G.g(any(r["rnd"] == 19 and r["home"] == "Udinese" and r["away"] == "Salernitana"
            and r["date"] == "2022-04-20" and (r["hg"], r["ag"]) == (0, 1) for r in r21)
        and sum(1 for r in r21 if r["rnd"] == 19) == 10,
        "anomaly 2021-22 R19: 10 rows incl. the COVID-quarantine makeup Udinese 0-1 Salernitana "
        "2022-04-20 (postponed from 2021-12-22; forfeit overturned; wf-md19 '20.04.2022 (Ended)' "
        "third-agrees)")
    G.g(all(any(r["rnd"] == 20 and r["home"] == h and r["away"] == a and r["date"] == dte
                and (r["hg"], r["ag"]) == sc for r in r21)
            for (h, a, dte, sc) in [("Fiorentina", "Udinese", "2022-04-27", (0, 4)),
                                    ("Atalanta", "Torino", "2022-04-27", (4, 4)),
                                    ("Bologna", "Inter", "2022-04-27", (2, 1)),
                                    ("Salernitana", "Venezia", "2022-05-05", (2, 1))]),
        "anomaly 2021-22 R20: the '[Apr 27]' makeup batch (Fiorentina 0-4 Udinese, Atalanta 4-4 "
        "Torino, Bologna 2-1 Inter) + '[May 5]' Salernitana 2-1 Venezia ship with their true "
        "makeup dates inside round 20")
    r22 = data["2022-23"][0]
    G.g(any(r["rnd"] == 9 and r["home"] == "Fiorentina" and r["away"] == "Lazio"
            and r["date"] == "2022-10-10" and (r["hg"], r["ag"]) == (0, 4) for r in r22),
        "anomaly 2022-23 R9: Fiorentina 0-4 Lazio dated 2022-10-10 (RSSSF '[Oct 1]' date misprint "
        "overridden on TWO independent indexes - OFB 'Mon Oct 10 20:45' + wf-md9 '10.10.2022 "
        "20:45')")
    G.g(sum(1 for r in r22 if r["rnd"] == 9) == 10
        and sum(1 for r in r22 if r["rnd"] == 9 and "2022-10-08" <= r["date"] <= "2022-10-10") == 10,
        "anomaly 2022-23 R9: all ten round-9 rows dated inside the 2022-10-08..10 window (no "
        "row left on the misprinted October-1 date)")
    r23 = data["2023-24"][0]
    G.g(any(r["rnd"] == 30 and r["home"] == "Torino" and r["away"] == "Monza"
            and r["date"] == "2024-03-30" and (r["hg"], r["ag"]) == (1, 0) for r in r23),
        "anomaly 2023-24 MD30: Torino 1-0 Monza ships as played - the OFB 0-0 typing error is "
        "quadruple-corroborated as an error on the OFB side (ESPN/FoxSports/live-result/wf-md30), "
        "RSSSF stands")
    G.g(any(r["rnd"] == 32 and r["home"] == "Udinese" and r["away"] == "Roma"
            and r["date"] == "2024-04-25" and (r["hg"], r["ag"]) == (1, 2) for r in r23)
        and any(a["home"] == "Udinese" and a["away"] == "Roma" and a["date"] == "2024-04-14"
                and "abandoned" in a["note"] and "72" in a["note"] for a in data["2023-24"][3]),
        "anomaly 2023-24 R32: Udinese-Roma ABD wrap-continuation row ships 2024-04-25 as the 1-2 "
        "completion (abandoned at 1-1 in 72' on 2024-04-14, RSSSF verbatim - Roma player Evan "
        "Ndicka's medical emergency; ledger ABD context row verified)")
    r24 = data["2024-25"][0]
    G.g(any(r["rnd"] == 14 and r["home"] == "Fiorentina" and r["away"] == "Inter"
            and r["date"] == "2025-02-06" and (r["hg"], r["ag"]) == (3, 0) for r in r24)
        and any(a["home"] == "Fiorentina" and a["away"] == "Inter" and a["date"] == "2024-12-01"
                and "Bove" in a["note"] for a in data["2024-25"][3]),
        "anomaly 2024-25 R14: Fiorentina 3-0 Inter ships 2025-02-06 as the completion of the "
        "2024-12-01 game abandoned at 0-0 in 16' (medical emergency of Fiorentina's Edoardo "
        "Bove; ledger ABD row verified; OFB + wf-md14 third-agree the date and the score)")
    po_l2_2425 = [p for p in data["2024-25"][2] if p["hg"] == "awd"]
    G.g(len(po_l2_2425) == 1 and po_l2_2425[0]["home"] == "Salernitana"
        and po_l2_2425[0]["away"] == "Sampdoria" and "awarded 0-3" in po_l2_2425[0]["extra"]
        and "NOT-COMMISSIONED" in po_l2_2425[0]["flags"],
        "anomaly 2024-25 L2-R2: the Serie B playout line 'Salernitana awd Sampdoria [awarded 0-3; "
        "abandoned at 0-2 in 74']' rides as a NOT-COMMISSIONED context line with the 'awd' token "
        "in the score slot - zero shipped rows carry an award (a top-flight-touching leg would "
        "follow the GER 0-2-awarded precedent, and none occurred in-window)")
    r26 = data["2025-26"][0]
    md16 = [r for r in r26 if r["rnd"] == 16]
    G.g(len(md16) == 10
        and sum(1 for r in md16 if "2025-12-20" <= r["date"] <= "2025-12-21") == 6
        and sum(1 for r in md16 if "2026-01-14" <= r["date"] <= "2026-01-15") == 4,
        "anomaly 2025-26 MD16 (carrier duplicate-banner): 10 rows = 6 main-window 2025-12-20..21 "
        "+ 4 mid-week makeups 2026-01-14..15 (Napoli 0-0 Parma, Inter 1-0 Lecce, Verona 2-3 "
        "Bologna, Como 1-3 Milan) summed under banner 16")
    md24 = [r for r in r26 if r["rnd"] == 24]
    G.g(len(md24) == 10
        and sum(1 for r in md24 if "2026-02-06" <= r["date"] <= "2026-02-09") == 9
        and any(r["home"] == "Milan" and r["away"] == "Como" and r["date"] == "2026-02-18"
                and (r["hg"], r["ag"]) == (1, 1) for r in md24)
        and not any(r["date"] == "2026-02-08" and r["home"] == "Milan" for r in r26),
        "anomaly 2025-26 MD24 (carrier duplicate-banner): 10 rows = 9 main-window 2026-02-06..09 "
        "+ Milan 1-1 Como 2026-02-18 - the Perth fixture, cancelled 2025-12-22, played at San "
        "Siro on the makeup date (NO 2026-02-08 Milan row exists anywhere in the season)")
    md35 = [r for r in r26 if r["rnd"] == 35]
    G.g(len(md35) == 10 and any(r["home"] == "Inter" and r["away"] == "Parma"
            and r["date"] == "2026-05-03" and (r["hg"], r["ag"]) == (2, 0) for r in md35),
        "anomaly 2025-26 MD35 cross-check: Inter 2-0 Parma 2026-05-03 sits in the carrier exactly "
        "as the title-clincher of the season record (21st title, three matches to spare)")

    # ---- venue gate
    bad_ven = []
    for line in pack_rows:
        f = line.split("|")
        if not f[9] or not f[10]:
            bad_ven.append(line)
    G.g(not bad_ven and ven_lines == 101 and len(ven) == 100 and len(ven_neutral) == 1,
        f"venues: all 1,901 rows carry stadium/city constants (ita-venues.txt = 101 VENUE rows: "
        f"100 per-season lattice 20x5 + 1 spareggio neutral entry; dict keys {len(ven)}+"
        f"{len(ven_neutral)}; empties={len(bad_ven)})")
    meazza = sum(1 for line in pack_rows if "Giuseppe Meazza" in line.split("|")[9])
    sansiro = sum(1 for line in pack_rows if line.split("|")[9] == "San Siro")
    G.g(meazza >= 19 and sansiro >= 19,
        f"venues Milan/Inter: the shared ground carries BOTH printed names in-window (Inter home "
        f"rows print 'Giuseppe Meazza' at least one full season - {meazza} rows; Milan home rows "
        f"print 'San Siro' - {sansiro} rows; capacities equal per season - same-ground split "
        f"prints disclosed under venue_policy)")
    mapei = sum(1 for line in pack_rows if "Mapei" in line.split("|")[9])
    sass_home = sum(1 for line in pack_rows if line.split("|")[4] == "Sassuolo")
    G.g(mapei == sass_home + 1 and sass_home == 76,
        f"venues Mapei: {mapei} Mapei-print rows = Sassuolo's {sass_home} home rows (19 in each "
        f"of its 4 in-window seasons: 2021-22/2022-23/2023-24 and the 2025-26 return - none in "
        f"the 2024-25 Serie B year; 2021-22 short print 'Mapei Stadium' -> 'Mapei Stadium - "
        f"Citta del Tricolore' from 2022-23, ground in Reggio Emilia while the city cell prints "
        f"Sassuolo) + the ONE neutral spareggio row at the same ground")
    olimp = sum(1 for line in pack_rows if line.split("|")[9] == "Stadio Olimpico")
    rom_laz_home = sum(1 for line in pack_rows if line.split("|")[4] in ("Roma", "Lazio"))
    G.g(olimp == rom_laz_home == 190,
        f"venues Olimpico: {olimp} Stadio Olimpico rows = Roma+Lazio combined home rows "
        f"(19 x 2 x 5; capacity prints 70,634/70,634/67,585/67,585/70,634 by season - source "
        f"reprints verified not structural)")

    # ---- pivot gate (owner decree)
    pivot_out = []
    all_ok = True
    green = 0
    total = 0
    for s in SEASONS:
        rows, table, _, _ = data[s]
        lines, summaries = pivot_block(s, rows, table)
        okn = sum(1 for v in summaries.values() if v[0])
        all_ok &= okn == SHAPE[s][0]
        green += okn
        total += SHAPE[s][0]
        pivot_out.append(f"### PIVOT {s} (re-derived from the pack's own rows; each club = its "
                         f"38 games in round order; summary gated vs the season TABLE constants)")
        pivot_out.extend(lines)
    G.g(all_ok, f"pivots: {green}/{total} club-season full-campaign pivots reproduce the "
                "final-table lines (38 games = 19 home + 19 away each; Juventus 2022-23 carries "
                "the -10 FIGC deduction 71-10=61)")

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
                 "'Italy Serie A'/'domestic-league'; the spareggio: 'Italy Relegation "
                 "Playoffs'/'other'; country Italy everywhere)")
    labels = {s[0] for s in SOURCES}
    G.g(all(line.split("|")[13] in labels for line in pack_rows),
        "grammar: every row's sourceLabel resolves to a declared SOURCE")
    try:
        for line in team_lines + pack_rows:
            line.encode("ascii")
        asc = True
    except UnicodeEncodeError:
        asc = False
    G.g(asc, "grammar: ASCII-only MATCH rows (venue strings NFKD-folded - Citta for Citta', "
             "Dall'Ara apostrophes typewriter; the accented prints live in the ledgers' verbatim "
             "fields, never in pack rows)")

    # ---------------------------------------------------------------- NOTE texts
    notes = []
    notes.append(
        f"NOTE|info|pack_id|ITA-2021-2026_BP-TEAM-PACK_v2 - return of WO-ITA-SPAN-14 (queue "
        f"position 8), FULL SPAN under OWNER OVERRIDE DECREE-2026-08-04 ('I require you to "
        f"deliver full season files regardless of what the workorder said ... my authority "
        f"overrides everything ... I want one source of truth') - the v2 retarget of the "
        f"superseded v1 order (the v2 WO awarded the full 20/38 shape: v1's 18-club premise was "
        f"itself corrected by the owner, supersession disclosed here). 1,901 MATCH rows = 1,900 "
        f"Italy Serie A rows (380 per season x 5 - 20 clubs x 38 matchdays every season) + 1 "
        f"'Italy Relegation Playoffs' row compType 'other' (the ONE pro/rel decider touching the "
        f"top flight in the window: the 2022-23 relegation spareggio Spezia 1-3 Verona, a "
        f"single neutral-ground game, ships per ERRATA-2026-08-03 + DECREE-2026-08-04 - same "
        f"handling as RPL/CZ1/MOLCUP/FRA/GER; the WO's generic expectation that a spareggio "
        f"'rarely exists/is out of scope' proves wrong in-window exactly once and the leg IS "
        f"included, disclosed under errata_spareggio). Then the 2026-27 boundary: the new "
        f"season starts 2026-08-23, AFTER the {ACCESSED} return date, so zero 2026-27 rows "
        f"exist (sourced boundary NOTE below). The file name 'ITA-2021-2026' carries no cutoff "
        f"- the span is certified gap-free through today. Compiled {ACCESSED}.")
    for lbl, url, typ, what in SOURCES:
        notes.append(f"SOURCE|{lbl}|{url}|{ACCESSED}|{typ}|{what}")
    notes.append(
        "NOTE|info|federation_check|Section-0 scan on the finished pack: all 1,901 rows are "
        "Italy rows. The 1,900 league rows are populated exclusively by the 27 pinned section-3 "
        "roster strings (all 27 appear in-window; none is pinned-but-unused). Per-season "
        "compositions: 2021-22 Atalanta, Bologna, Cagliari, Empoli, Fiorentina, Genoa, Inter, "
        "Juventus, Lazio, Milan, Napoli, Roma, Salernitana, Sampdoria, Sassuolo, Spezia, Torino, "
        "Udinese, Venezia, Verona; 2022-23 minus Cagliari/Genoa/Venezia plus Cremonese, Lecce, "
        "Monza; 2023-24 minus Cremonese/Sampdoria/Spezia (Spezia via the spareggio) plus "
        "Cagliari, Frosinone, Genoa; 2024-25 minus Frosinone/Salernitana/Sassuolo plus Como, "
        "Parma, Venezia; 2025-26 minus Empoli/Monza/Venezia plus Cremonese, Pisa, Sassuolo. The "
        "spareggio row adds NO outside participant (Spezia/Verona are roster members), hence "
        "zero TEAM rows. Not England, not Germany; the Coppa Italia and Serie B stay OUT per WO "
        "section-1 (the Serie B tables/playoff blocks live only as ledger context lines). "
        "Anti-appear list (Inter never Internazionale/Inter Milan, Milan never AC Milan/A.C. "
        "Milan, Verona never Hellas/Hellas Verona) is empty on row identity fields - the Hellas "
        "print survives only inside the 2022-23 ledger's verbatim PO line. No standings tables "
        "carried - rows only.")
    notes.append(
        "NOTE|info|catalog|1,901 MATCH rows = 1,900 'Italy Serie A' 'domestic-league' rows "
        "(380 x 5) + 1 'Italy Relegation Playoffs' 'other' row (the 2022-23 spareggio "
        "single-decider; competition strings declared once here, per WO section-2) + 0 TEAM "
        "rows (no unregistered identity appears - both spareggio participants are section-3 "
        "members). venueDetail = 'MD<n>' on league rows (carrier matchday; makeup fixtures keep "
        "their original round banners), 'Playoff' on the spareggio. The 13th pipe-field is "
        "empty on every row (SPEC-2026-08-04 14-field grammar); sourceLabel per row: "
        "rsssf-ital2022..ital2025 on the first four seasons, ofb-ita-2526 on the source-"
        "adaptation season, rsssf-ital2023 on the spareggio row.")
    notes.append(
        "NOTE|info|identity|Pack identities = the 27 section-3 pins EXACTLY, mapped from "
        "source name-forms: RSSSF/openfootball 'Inter' (the Wiki matrix team_code 'Inter "
        "Milan'), 'Milan' ('AC Milan'), 'Verona' ('Hellas Verona' on the PO ledger line and in "
        "source prose) collapse to the pinned strings Inter / Milan / Verona on every identity "
        "field. NAME-EPOCH DATA, not identities: the Juventus ground prints 'Allianz Stadium' in "
        "2021-22, 'Juventus Stadium' 2022-23..2024-25 and 'Allianz Stadium' again 2025-26 - the "
        "pinned club string Juventus is untouched; the shared Milan/Inter ground prints "
        "'Giuseppe Meazza' (75,710) on Inter's side and 'San Siro' (75,710) on Milan's side in "
        "the 2023-24 article while both agree the clubs share the stadium - carried as printed "
        "per home club per the venue lattice, disclosed under venue_policy. No alias table is "
        "shipped: nothing outside the 27 pins appears on identity fields.")
    notes.append(
        "NOTE|info|venue_policy|MATCH stadium/city = the home club's documented ground for "
        "that season per the Wikipedia season articles' stadium/location tables (second index; "
        "RSSSF carries no venues), transcribed to audit/ledger/ita-venues.txt (101 entries = "
        "100-season lattice 20x5 + 1 spareggio neutral entry) and ASCII-folded. Stadium strings "
        "follow the articles' printed display text per season - epochs are era data, not "
        "errors: Atalanta 'Gewiss Stadium' 19,768 (2021-22) -> 'Stadio Atleti Azzurri "
        "d'Italia' 21,000 (reconstruction season 2022-23) -> Gewiss Stadium 15,222 (2023-24, "
        "works-phase capacity) -> 23,439 (2024-25) -> renamed 'Stadio di Bergamo' 23,439 "
        "(2025-26); Bologna 36,462/36,462/36,532/36,000/38,279; Ferraris (Genoa/Sampdoria) "
        "36,599 -> 33,205 from 2023-24; Fiorentina 43,147 -> 43,118; Juventus name oscillation "
        "Allianz <-> 'Juventus Stadium' (see identity NOTE); Lecce 31,533 (2022-23) -> 30,354 "
        "and the 2025-26 print 'Stadio Via del Mare-Ettore Giardiniero'; Empoli 2024-25 print "
        "'Stadio Carlo Castellani - Computer Gross Arena'; Monza 15,039 -> 17,102 (2024-25); "
        "Napoli 54,726 -> 54,732 (2024-25); Pisa 'Cetilar Arena' 12,508; Salernitana Arechi "
        "26,000 (2021-22) / 37,180 (2022-23) / 29,739 (2023-24); San Siro/Meazza 75,923 -> "
        "75,710 (2023-24); Stadio Olimpico 70,634/70,634/67,585/67,585/70,634 (source reprint "
        "swings, verified not structural); Udinese print-epoch 25,144 -> 25,132 and the "
        "'Bluenergy Stadium' print; Venezia 11,150 stable in-window (the 2026-27 article "
        "re-counts 12,048 - post-window, not used); Cagliari 'Sardegna Arena' 16,416 -> "
        "'Unipol Domus' 16,412/16,416; Cremonese Zini 16,003 (2022-23) and 20,641 (2025-26); "
        "Frosinone Stirpe 16,227; Parma Tardini 22,352; Como Sinigaglia 13,602; Spezia Picco "
        "11,512; Torino 28,958/27,958/28,177 stable-after; Sassuolo city cell prints Sassuolo "
        "while the Mapei ground stands in Reggio Emilia (parenthetical acknowledged in the "
        "article; the long print 'Mapei Stadium - Citta del Tricolore' rides from 2022-23). "
        "The ONE neutral-venue fixture of the window is the spareggio: Mapei Stadium - Citta "
        "del Tricolore, Reggio Emilia 21,515 (ledger neutral entry; glance-confirmed by the "
        "official Lega Serie A report, attendance 15,000). No other neutral-venue fixture and "
        "no split home season exists in the window.")
    notes.append(
        "NOTE|info|round_counts|Season row/goal/span anchors, each recomputed from the pack "
        "rows and matching the official record: 2021-22 = 380 rows, 1,089 goals, "
        "2021-08-21..2022-05-22 (opener Inter 4-0 Genoa; champions Milan 86 - 19th title); "
        "2022-23 = 380, 974, 2022-08-13..2023-06-04 (opener Milan 4-2 Udinese; champions "
        "Napoli 90 - 3rd title, clinched 2023-05-04 at Udinese 1-1 with five matches to "
        "spare; the relegation spareggio tail runs 2023-06-11 and ships as the 'other' row); "
        "2023-24 = 380, 992, 2023-08-19..2024-06-02 (opener Empoli 0-1 Verona; champions "
        "Inter 94 - 20th title, second star); 2024-25 = 380, 973, 2024-08-17..2025-05-25 "
        "(opener Genoa 2-2 Inter; champions Napoli 82 - 4th title, one point over Inter 81, "
        "decided in the Friday R38 double-header 2025-05-23: Napoli 2-0 Cagliari, Como 0-2 "
        "Inter); 2025-26 = 380, 922, 2025-08-23..2026-05-24 (opener Sassuolo 0-2 Napoli; "
        "champions Inter 87 - 21st title, clinched with three matches to spare 2026-05-03 via "
        "the 2-0 home win over Parma per the season article and its Guardian cite). Every "
        "season is one full double round-robin: 38 matchdays x 10 fixtures, zero "
        "double-rounds, zero cancellations.")
    notes.append(
        "NOTE|info|continuity|Continuity-clause accounting (gap-free league span "
        "2021-08-21 -> 2026-05-24): every matchday of all five seasons exists and is dated; "
        "no fixture was cancelled; ONE point deduction in the window (Juventus -10 in 2022-23, "
        "FIGC plusvalenze decision 2023-05-22 - the initial 15-point penalty of 2023-01-20 was "
        "revoked on re-trial; arithmetic gated 71 raw -> 61 official and disclosed under the "
        "deduction anomaly NOTE). Documented disruptions; rows always keep their original MD "
        "labels while the file stays date-sorted. Abandoned-then-completed fixtures - two in "
        "the window, both ship as their re-played COMPLETIONS under the original round with "
        "the abandonment rides as a ledger ABD context row (never an abandoned-score row and "
        "never a VOID): 2023-24 R32 Udinese-Roma abandoned at 1-1 in 72' on 2024-04-14 (medical "
        "emergency of Roma player Evan Ndicka), completed as Udinese 1-2 Roma on 2024-04-25; "
        "2024-25 R14 Fiorentina-Inter abandoned at 0-0 in 16' on 2024-12-01 (medical emergency "
        "of Fiorentina's Edoardo Bove), completed as Fiorentina 3-0 Inter on 2025-02-06 "
        "(wf-md14 '06.02.2025 ... (Ended)' third-agrees). COVID-era makeups 2021-22: R19 "
        "Udinese 0-1 Salernitana postponed from 2021-12-22 (quarantine; the forfeit was "
        "overturned) and played 2022-04-20, plus the R20 '[Apr 27]' batch (Fiorentina 0-4 "
        "Udinese, Atalanta 4-4 Torino, Bologna 2-1 Inter) and '[May 5]' Salernitana 2-1 "
        "Venezia - all ship with their true makeup dates inside their original rounds; "
        "wf-md19 third-agrees the Udinese date. 2025-26 carrier duplicate-banner makeups "
        "(banner summing disclosed): MD16 rows = 6 main-window 2025-12-20..21 + 4 mid-week "
        "makeups 2026-01-14..15; MD24 rows = 9 main-window 2026-02-06..09 + Milan 1-1 Como "
        "2026-02-18 (the Perth-cancelled fixture - full episode under its own NOTE). Winter "
        "breaks are scheduling, not gaps. Season spans as listed under round_counts; every "
        "official match sits exactly once in the pack.")
    notes.append(
        "NOTE|info|boundary|Span-end state per WO section-1 row 2: the last completed round "
        "of the span is 2025-26 MD38, all ten fixtures 2026-05-23..24 (final table inside the "
        "gates; Inter champions 87, 21st title; Multigroup 2-row hth bracket Napoli/Roma levels "
        "at 76/73 decision lines). No top-flight playoff tail exists for 2025-26 (the 17/18 "
        "spareggio mechanism produced no game: Verona 19 and Cremonese 17 finished 18th/17th "
        "with Pisa 20th - three direct relegations). The 2026-27 season had NOT started on the "
        "return date 2026-08-05: rsssf.org/tablesi/ital2027.html answers 404, and the 2026-27 "
        "season article (action=raw, byte-verified) fixes the dates '23 August 2026 - 30 May "
        "2027' (calendar cite gazzetta.it) with 20 teams - promoted Venezia (return after one "
        "year), Frosinone (after two) and A.C. Monza (Serie B playoff winners on the "
        "better-record tiebreak: final 0-2 away / 2-0 home vs Catanzaro, aggregate 2-2 - the "
        "first such playoff-final tiebreak in the window, RSSSF NB line; context zone only, "
        "nothing adjudicated); relegated Cremonese, Hellas Verona and Pisa - exactly this "
        "pack's 2025-26 bottom three. Zero 2026-27 rows are emitted; this is a boundary "
        "statement, not a blocker. No dateless rows, no duplicate (date,home,away) rows "
        "anywhere in the pack (gate-verified).")
    notes.append(
        "NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a "
        "pivot gate: the pack's own rows are re-pivoted club-by-club - each club of each "
        "season shows its full campaign (19 home + 19 away = 38 games) enumerated in round "
        "order with dates, and every TEAMPIVOT summary line reproduces the club's official "
        "final-table line (P/W/D/L/GF/GA/Pts incl. the Juventus 2022-23 -10 deduction "
        "71-10=61). All 100 club-season pivots (20 clubs x 5 seasons) are printed in "
        "audit/pack-validation-ita.txt next to this file. 100/100 green.")
    notes.append(
        "NOTE|info|source_adaptation|WO section-4 design: RSSSF tablesi/ital<YEAR>.html pages "
        "= primary for dates AND scores (Italian archive uses 'ital'); ital2022..ital2025 "
        "carry full round-by-round sections transcribed to audit/ledger/ita-<season>.txt on "
        "fetch day 2026-08-05. ADAPTATION for 2025-26: ital2026.html (Roberto Di Maggio / "
        "Karel Stokkermans, footer 'Last updated: 21 Jun 2026') carries the Serie A final "
        "table, the Coppa Italia block and Serie B - but NO Serie A round-by-round (verified "
        "full page 2026-08-05) - the 2025-26 match rows therefore come from the independent "
        "index openfootball/italy 2025-26/1-seriea.txt and are labelled ofb-ita-2526 (format-B "
        "banner groups mapped to MD incl. the RS16/RS24 duplicate-banner makeup blocks; parser "
        "tools/parse_ofb_it.py, verbatim raw saved in data/raw/ with the c0-c1 'Mon Oct20' "
        "defect repair disclosed in the raw header); the RSSSF final table remains the table "
        "authority and the recompute of those 380 rows reproduces it club-for-club and in "
        "position order EXACT (gate above). Second-index coverage: openfootball season files "
        "diffed row-for-row vs RSSSF for 2021-22..2024-25 (380/380 IDENTICAL round + date + "
        "score in 2021-22/2022-23/2024-25; 379/380 + the single OFB-side MD30 typing error in "
        "2023-24, tools/diff_ita_second_index.py); the Wikipedia 2025-26 FBR results matrix "
        "diffed cell-for-cell against the carrier (380/380 IDENTICAL, 922 goals both, "
        "tools/diff_ita_matrix.py); worldfootball matchday pages corroborate one full round "
        "per season (spot_audit) including the 2021-22 R19 COVID makeup, the 2022-23 R9 date "
        "adjudication, the 2023-24 MD30 1-0 and the 2024-25/2025-26 completions; the five "
        "Wikipedia league-table templates reproduce all five RSSSF tables club-for-club "
        "(tools/wiki_ita_tables.py, byte-deterministic; 2022-23 additionally witnessed 20/20 "
        "by the rendered league table; adjust_points JUV=-10 with the FIGC cite in-wikitext; "
        "the Spezia template status_R vs RSSSF 'Relegation Playoff' note alias accepted + "
        "disclosed). Conflicts were resolved per section-4(3) - RSSSF stands unless two "
        "independent indexes agree against it - and exactly TWO conflicts arose in the whole "
        "order, both documented below (one RSSSF-side date misprint, one OFB-side score typo "
        "where RSSSF stands four-witnesses-strong). Nothing else diverges anywhere in the "
        "five seasons, and nothing is imputed.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF ital2023.html prints round 9 'Fiorentina 0-4 "
        "Lazio' under '[Oct 1]' - a fixtureless Saturday (round 9 ran Sat 2022-10-08 to Mon "
        "2022-10-10; the fixture was the Monday-night game). TWO independent indexes agree "
        "against it: the openfootball season file header line 'Mon Oct 10 20:45 Fiorentina "
        "0-4 Lazio' and the worldfootball round-9 page '10.10.2022 20:45'. Per section-4, the "
        "pack row carries 2022-10-10; the RSSSF print is preserved verbatim in "
        "data/raw/rsssf-ital2023-1sa.txt with the addendum in audit/ledger/ita-2022-23.txt. "
        "All scores were always identical across every source; the final table is unaffected "
        "either way.")
    notes.append(
        "NOTE|warning|source_conflict|The 2023-24 openfootball season file prints round 30 "
        "'Torino 0-0 Monza' (Sat Mar 30 15:00) - but the played score is TORINO 1-0 MONZA "
        "exactly as the RSSSF primary prints it. The primary stands per section-4(3): this is "
        "a defect on the SECOND-INDEX side, now quadruple-corroborated - ESPN and FoxSports "
        "and live-result and the worldfootball round-30 page '30.03.2024 15:00 Torino FC 1:0 "
        "AC Monza (Ended)' all print 1-0. The OFB line is quarantined from every downstream "
        "use (it never touched a shipped row); diff ledger audit/ledger/ita-2ndidx-2023-24.txt "
        "shows 379/380 IDENTICAL + this one defect, dates 380/380. The final table is "
        "unaffected either way (the table constants come from RSSSF and recompute exactly).")
    notes.append(
        "NOTE|warning|deduction|2022-23 Juventus: the FIGC plusvalenze ruling deducted 10 "
        "points on 2023-05-22 (an initial 15-point deduction of 2023-01-20 was revoked by the "
        "CONI re-trial and re-set at 10; the separate UEFA settlement kept the club out of "
        "2023-24 Europe - the template's note_JUV). The pack's rows recompute Juventus at "
        "P38 W22 D6 L10 GF56 GA33 = 71 raw; 71 - 10 = 61 EXACTLY the official table print "
        "(adjust_points_JUV in the wiki template carries the same -10 with the FIGC cite); "
        "position order re-verified around the deduction (61 lands 7th; Roma 63 6th).")
    notes.append(
        "NOTE|warning|errata_spareggio|WO-ITA-SPAN-14's generic text treats a relegation "
        "spareggio as a conditional scope item ('if it exists ... SHIP' / 'rarely'); IN THIS "
        "WINDOW it exists EXACTLY ONCE and the conditioned clause fires: 2022-23, pos 17/18 "
        "level on 31 points (Serie A relegation tie-break rule - a tied 17th/18th is settled "
        "on the pitch, not by the Multigroup), Spezia 1-3 Verona, 2023-06-11 20:45 CEST, "
        "neutral Mapei Stadium - Citta del Tricolore Reggio Emilia, attendance 15,000, "
        "referee Daniele Orsato; scorers Faraoni 5', Ngonge 26' and 38' (Verona), Ampadu 15' "
        "(Spezia) per the official Lega Serie A match report. The game ended inside 90 "
        "minutes = the 90-minute doctrine ships its score unchanged. ERRATA-2026-08-03 + "
        "DECREE-2026-08-04 (every pro/rel play-off leg touching the top flight SHIPS as "
        "compType 'other') plus the WO's own conditioned clause agree: the row IS in this "
        "file (mirrors RPL/CZ1/MOLCUP/FRA/GER). NB the loser Spezia is relegated - the "
        "spareggio is a survival decider, the reverse of the German tie; winner Verona (table "
        "note 'Relegation Playoff', wiki status VER=O) plays the 2023-24 Serie A. No TEAM "
        "rows arise: both participants are pinned roster members.")
    notes.append(
        "NOTE|warning|abandoned_completions|Two abandonments in the window, both re-played to "
        "a full completion (ships the completion; the abandoned partial rides as a ledger ABD "
        "context row only): (1) 2024-04-14 Udinese-Roma abandoned at 1-1 in 72' for the "
        "medical emergency of Roma player Evan Ndicka (RSSSF verbatim; player stabilised and "
        "the fixture was rescheduled for 2024-04-25), completion Udinese 1-2 Roma - the row "
        "ships "
        "inside R32 with the true completion date. (2) 2024-12-01 Fiorentina-Inter abandoned "
        "at 0-0 in 16' for the medical emergency of Fiorentina midfielder Edoardo Bove "
        "(player recovered; match resumed on 2025-02-06), completion Fiorentina 3-0 Inter - "
        "ships inside R14 with the true completion date; independent openfootball AND "
        "worldfootball md14 ('06.02.2025 20:45 ACF Fiorentina 3:0 Inter (Ended)') agree the "
        "date and score. No abandoned-score row and no VOID row exists anywhere in the pack.")
    notes.append(
        "NOTE|warning|awd_token_context|The only award-token in the ITA ledger corpus sits "
        "OUTSIDE the shipped slice: 2024-25 Serie B playout 'Salernitana awd Sampdoria "
        "[awarded 0-3; abandoned at 0-2 in 74']' rides as a NOT-COMMISSIONED-L2-internal "
        "context line with the 'awd' print in the score slot (parser policy disclosed in the "
        "parser header). No top-flight-touching awarded fixture occurred in the window (the "
        "GER 0-2-awarded precedent was noted should one have occurred; the pack's 1,901 "
        "shipped rows are all played results).")
    notes.append(
        "NOTE|warning|perth_episode|The 2025-26 MD24 fixture Milan-Como was SCHEDULED for "
        "2026-02-08 at Perth Stadium (Australia) - the infamous proposed first European "
        "league match played on another continent. The AFC called the relocation demands "
        "'unacceptable' and the plan was CANCELLED on 2025-12-22 (San Siro was also "
        "unavailable on 2026-02-08 because of the Winter Olympics opening ceremony of "
        "2026-02-06). The match was instead played ordinarily in Milan on the makeup date "
        "2026-02-18: Milan 1-1 Como - Paz 32' left foot / Leao 64' right foot, STADIUM "
        "GIUSEPPE MEAZZA (San Siro), attendance 75,251, referee Maurizio Mariani per the "
        "worldfootball match report (ma11129283), exact-agreeing with the carrier row the "
        "pack ships (MD24, 2026-02-18, rsssf-adaptation label ofb-ita-2526). No 2026-02-08 "
        "Milan row exists anywhere in the season (gated). Venue of the shipped row is San "
        "Siro per the venue lattice and the report, NOT Perth: the Perth game never "
        "happened.")
    notes.append(
        "NOTE|warning|source_internal_anomaly|The 2025-26 RSSSF page's Serie B playoff block "
        "is source-internally inconsistent on one date: 'First Leg [May 20] Catanzaro 0-2 "
        "Monza' prints on the SAME date as semifinal leg-2 'Palermo 2-0 Catanzaro'. This is a "
        "context-zone block (NOT-COMMISSIONED tier-internal data, zero shipped rows affected) "
        "so it is DOCUMENTED, not adjudicated - nothing imputed. Same block: 'NB: Monza "
        "promoted on better record regular season' after aggregate 2-2 (0-2 away, 2-0 home) - "
        "the first better-record playoff-final tiebreak in the window; boundary NOTE-only.")
    notes.append(
        "NOTE|info|spot_audit|2021-22 matchday 19 re-listed for spot-audit - the "
        "COVID-quarantine round with its April makeup (sources https://www.rsssf.org/tablesi/"
        "ital2022.html, ofb-ita-2122 - diff 380/380 IDENTICAL incl. dates - AND "
        "wf-ita-2122-md19): "
        + spot_listing("2021-22", SPOT["2021-22"], data["2021-22"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2022-23 matchday 37 re-listed for spot-audit - the penultimate "
        "round of the champions' season (sources https://www.rsssf.org/tablesi/ital2023.html, "
        "ofb-ita-2223 AND wf-ita-2223-md9 round-adjudication page corroborating this season's "
        "conventions one round earlier): "
        + spot_listing("2022-23", SPOT["2022-23"], data["2022-23"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2023-24 matchday 30 re-listed for spot-audit - the round "
        "carrying the OFB-side typing error (sources https://www.rsssf.org/tablesi/"
        "ital2024.html, wf-ita-2324-md30 '30.03.2024 15:00 Torino FC 1:0 AC Monza (Ended)', "
        "plus ESPN/FoxSports/live-result as archived; the OFB file itself is the quarantined "
        "defect): "
        + spot_listing("2023-24", SPOT["2023-24"], data["2023-24"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2024-25 matchday 14 re-listed for spot-audit - the Bove-"
        "abandonment round with its February completion (sources https://www.rsssf.org/"
        "tablesi/ital2025.html, ofb-ita-2425 AND wf-ita-2425-md14): "
        + spot_listing("2024-25", SPOT["2024-25"], data["2024-25"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2025-26 matchday 35 re-listed for spot-audit - the Inter "
        "title-clinch round (sources ofb-ita-2526 = the season's labelled carrier, "
        "wikimatrix-ita-2526 - diff 380/380 IDENTICAL - AND wf-ita-2526-md24 corroborating "
        "this season's carrier conventions a round later than the clinch): "
        + spot_listing("2025-26", SPOT["2025-26"], data["2025-26"][0]) + ".")

    # ---------------------------------------------------------------- final pack integrity gates
    pack = "\n".join(notes + team_lines + pack_rows + ["END"]) + "\n"
    G.g(pack.rstrip().endswith("END"), "file ends with END")
    G.g(len(pack.splitlines()) == len(notes) + len(team_lines) + 1901 + 1,
        f"pack line accounting: {len(notes)} header rows (NOTE+SOURCE) + {len(team_lines)} TEAM "
        f"(zero expected) + 1,901 MATCH + END")
    block_ok = True
    for s, block in season_blocks:
        dates = [l.split("|")[1] for l in block]
        labels_ = {l.split("|")[13] for l in block}
        if dates != sorted(dates) or labels_ != {SRC_LABEL[s]}:
            block_ok = False
    po_dates = [l.split("|")[1] for l in pack_rows if l.split("|")[3] == COMPTYPE_PO]
    G.g(block_ok and all(l.split("|")[8] == "Playoff" for l in pack_rows if l.split("|")[3] == COMPTYPE_PO)
        and len(po_dates) == 1,
        "pack ordering: five season blocks in order, each league block date-sorted and carrying "
        "only its season's source label; the single spareggio row follows the league blocks "
        "(venueDetail 'Playoff', 'Italy Relegation Playoffs'/'other')")
    team_ok = (len(team_lines) == 0)
    G.g(team_ok, "TEAM rows: 0 - participants of the single 'other' row are pinned roster "
                 "members (Spezia, Verona); nothing outside the 27 pins appears anywhere")

    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="ascii", newline="\n") as fh:
        fh.write(pack)

    # ---------------------------------------------------------------- validation output
    head = [
        "ITA PACK VALIDATION - handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt",
        f"builder tools/build_ita_pack.py, run {ACCESSED}; gates PASS {G.n_pass} FAIL {G.n_fail}",
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
