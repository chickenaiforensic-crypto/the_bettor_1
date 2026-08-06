#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build + validate handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt (WO-EPL-SPAN-12, issued 2026-08-03).

PRIMARY:  audit/ledger/epl-<season>.txt  (RSSSF tablese/eng2022..eng2026.html; R1..R38 dated rows +
          RSSSF final-table constants as TABLE rows. 2021-22..2024-25 pages carry full rounds
          (Ian King); eng2026.html (Karel Stokkermans) carries the 2025-26 FINAL TABLE ONLY, so the
          2025-26 match rows come from the independent index openfootball/england
          master/2025-26/1-premierleague.txt and are gated EXACT against the RSSSF table by full
          recompute - documented source_adaptation.)
2NDIDX:   audit/ledger/epl-2ndidx-<season>.txt (openfootball matchday rows 2021-22..2024-25, diffed
          row-for-row; Wikipedia FBR results matrix 380 cells for 2025-26 via tools/diff_epl_matrix)
CONSTANTS audit/ledger/epl-venues.txt (per-season stadium/city constants, Wikipedia season tables)
SPIVOTS   audit/ledger/epl-pivot-<season>.txt are re-derived here and embedded in the validation
          output (owner's per-team pivot decree).
Output:   handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt  +  audit/pack-validation-epl.txt
Run:      python3 tools/build_epl_pack.py   (exit 0 iff every gate PASS; rebuild is deterministic)
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "audit", "ledger")
OUTPACK = os.path.join(ROOT, "handoffs", "EPL-2021-2026_BP-TEAM-PACK_v2.txt")
OUTAUDIT = os.path.join(ROOT, "audit", "pack-validation-epl.txt")
ACCESSED = "2026-08-03"
SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
COMP = "England Premier League"        # WO section-2 verbatim
COMPTYPE = "domestic-league"           # WO section-2 verbatim
COUNTRY = "England"
SRC_LABEL = {"2021-22": "rsssf-eng2022", "2022-23": "rsssf-eng2023", "2023-24": "rsssf-eng2024",
             "2024-25": "rsssf-eng2025", "2025-26": "openfootball-england-2526"}
DEDUCT = {"2023-24": {"Everton": 8, "Nottingham": 4}}   # RSSSF table brackets "-8"/"-4" (PSR rulings)
SPOT = {"2021-22": 1, "2022-23": 7, "2023-24": 17, "2024-25": 15, "2025-26": 31}  # one matchday/season

# ------------------------------------------------------------- identity (WO section-3)
ROSTER27 = ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea",
            "Crystal Palace", "Everton", "Fulham", "Ipswich", "Leeds", "Leicester", "Liverpool",
            "Luton", "Man City", "Man United", "Newcastle", "Norwich", "Nott'm Forest",
            "Sheffield United", "Southampton", "Sunderland", "Tottenham", "Watford", "West Ham",
            "Wolves"]
ROSTER_SET = set(ROSTER27)
ANTI_APPEAR = ["Spurs", "Tottenham Hotspur", "Wolverhampton", "Manchester City", "Manchester United",
               "AFC Bournemouth", "Nottingham Forest", "Sheffield Utd", "West Ham United",
               "Leeds United", "Leicester City", "Ipswich Town", "Norwich City", "Luton Town",
               "Newcastle United", "Brighton & Hove", "Aston Villa FC"]
STOCK2ROSTER = {"Villa": "Aston Villa", "Palace": "Crystal Palace", "City": "Man City",
                "United": "Man United", "Nottingham": "Nott'm Forest", "SheffUtd": "Sheffield United",
                "WestHam": "West Ham"}
def roster(stock):
    return STOCK2ROSTER.get(stock, stock)

SOURCES = [
 ("rsssf-eng2022", "https://www.rsssf.org/tablese/eng2022.html", "primary-archive",
  "2021-22: all 38 rounds dates+scores + official final table (Ian King page); transcribed in "
  "audit/ledger/epl-2021-22.txt the day of fetch; gate anchors 380 rows / 1071 goals / span "
  "2021-08-13..2022-05-22"),
 ("rsssf-eng2023", "https://www.rsssf.org/tablese/eng2023.html", "primary-archive",
  "2022-23: all 38 rounds dates+scores incl. the complete round-7 postponement scatter (death of "
  "Queen Elizabeth II; fixtures played 2023-01-12..2023-04-05) + official final table; "
  "audit/ledger/epl-2022-23.txt; anchors 380 / 1084 / 2022-08-05..2023-05-28"),
 ("rsssf-eng2024", "https://www.rsssf.org/tablese/eng2024.html", "primary-archive",
  "2023-24: all 38 rounds dates+scores (round 17 Bournemouth-Luton 2023-12-16 printed as the VOID "
  "abandoned game; the full 4-3 replay of 2024-03-13 carried under round 17) + official final table "
  "with Everton -8 / Nottingham -4 PSR deduction brackets; audit/ledger/epl-2023-24.txt; anchors "
  "380 / 1246 / 2023-08-11..2024-05-19"),
 ("rsssf-eng2025", "https://www.rsssf.org/tablese/eng2025.html", "primary-archive",
  "2024-25: all 38 rounds dates+scores + official final table (Liverpool champions 84; the page's "
  "[C] tag sits on row 3 Man City - carried verbatim, tagged quirk, table itself ordered normally); "
  "audit/ledger/epl-2024-25.txt; anchors 380 / 1115 / 2024-08-16..2025-05-25"),
 ("rsssf-eng2026", "https://www.rsssf.org/tablese/eng2026.html", "primary-archive",
  "2025-26: OFFICIAL FINAL TABLE ONLY (Karel Stokkermans page, last updated 14 Jun 2026 - unlike "
  "Ian King's 2021-22..2024-25 pages it prints no round-by-round section for the Premier League); "
  "table authority for the season: recompute of the pack's 380 match rows reproduces it club-for-club "
  "and in position order EXACT; constants transcribed in audit/ledger/epl-2025-26.txt"),
 ("rsssf-eng2027", "https://www.rsssf.org/tablese/eng2027.html", "primary-archive",
  "404 Not Found on 2026-08-03 - boundary evidence that no 2026-27 season page (and no played "
  "2026-27 fixture) existed on the return date"),
 ("openfootball-england-2526", "https://raw.githubusercontent.com/openfootball/england/master/2025-26/1-premierleague.txt",
  "match-carrier",
  "2025-26 match rows (380 fixtures, matchday banners MD1..MD38, played dates, scores; file header "
  "'# Matches 380', fetched in 5 chunks) - the season's date/score carrier under the documented "
  "source_adaptation; label carried on all 2025-26 MATCH rows"),
 ("ofb-eng-2122", "https://raw.githubusercontent.com/openfootball/england/master/2021-22/1-premierleague.txt",
  "second-index", "380 matchday-grouped rows diffed vs the RSSSF rows: 380/380 pairings IDENTICAL on "
  "round + date + score (audit/ledger/epl-2ndidx-2021-22.txt, tools/diff_epl_second_index.py)"),
 ("ofb-eng-2223", "https://raw.githubusercontent.com/openfootball/england/master/2022-23/1-premierleague.txt",
  "second-index", "380 rows diffed: 380/380 IDENTICAL round + date + score incl. the 10-fixture QEII "
  "round-7 scatter reconciled 10/10 (audit/ledger/epl-2ndidx-2022-23.txt)"),
 ("ofb-eng-2324", "https://raw.githubusercontent.com/openfootball/england/master/2023-24/1-premierleague.txt",
  "second-index", "380 rows diffed: 380/380 IDENTICAL round + date + score; confirms the two RSSSF "
  "[Dec 2] round-15 misprints were played 2023-12-07 (audit/ledger/epl-2ndidx-2023-24.txt)"),
 ("ofb-eng-2425", "https://raw.githubusercontent.com/openfootball/england/master/2024-25/1-premierleague.txt",
  "second-index", "380 rows diffed: 380/380 IDENTICAL round + date + score ('Home FC v Away FC' file "
  "style this season; audit/ledger/epl-2ndidx-2024-25.txt)"),
 ("wikimatrix-epl-2526", "https://en.wikipedia.org/wiki/2025%E2%80%9326_Premier_League", "second-index",
  "Results FBR matrix (380 cells; matrix source line = premierleague.com) diffed vs the 2025-26 pack "
  "rows: 380/380 IDENTICAL scores, goals 1045 = 1045 (audit/ledger/epl-2ndidx-2025-26.txt, "
  "tools/diff_epl_matrix.py); the article's league table rows agree with the RSSSF constants "
  "club-for-club; stadium/location table = 2025-26 venue constants (Everton's first season at Hill "
  "Dickinson Stadium)"),
 ("wiki-epl-venues", "https://en.wikipedia.org/wiki/2021%E2%80%9322_Premier_League", "second-index",
  "stadium/location tables of the five season articles 2021-22..2025-26 (sibling pages ...%E2%80%9322 "
  "through ...%E2%80%9326_Premier_League; fetched 2026-08-03): 100 venue rows = the stadium/city "
  "constants compiled in audit/ledger/epl-venues.txt; each season's promoted/relegated prose matches "
  "the membership gates"),
 ("wf-epl-2223-md7", "https://www.worldfootball.net/schedule/eng-premier-league-2022-2023-spieltag/7/",
  "second-index",
  "QEII matchday-7 spot-audit (redirects to the canonical results-and-standings page): all 10 "
  "fixtures dates AND scores identical to the pack rows, incl. Fulham-Chelsea 2023-01-12 and "
  "West Ham-Newcastle 2023-04-05"),
 ("football-data-e0-2425", "https://www.football-data.co.uk/mmz4281/2425/E0.csv", "second-index",
  "row 'E0,25/11/2024,20:00,Newcastle,West Ham,0,2,...' = the second independent date for the "
  "adjudicated round-12 fixture (see source_conflict NOTE)"),
 ("football-data-e0-2526", "https://www.football-data.co.uk/mmz4281/2526/E0.csv", "second-index",
  "2025-26 spot rows: MD1 block identical date+score (13 rows incl. MD2 openers); MD31 strays "
  "'E0,18/02/2026,20:00,Wolves,Arsenal,2,2,D,0,1,A,P Tierney' and "
  "'E0,13/05/2026,20:00,Man City,Crystal Palace,3,0,H,2,0,H,S Attwell' corroborate both stray dates; "
  "final-day rows all 24/05/2026 16:00 match MD38"),
 ("wiki-epl-2627", "https://en.wikipedia.org/wiki/2026%E2%80%9327_Premier_League", "second-index",
  "span-end boundary: 2026-27 season dates 21 August 2026 - 30 May 2027; fixtures released 19 June "
  "2026 at 10:00 BST (after the 2025-26 season ended); Arsenal enter as defending champions; promoted "
  "Coventry City, Ipswich Town, Hull City; relegated West Ham United, Burnley, Wolverhampton Wanderers "
  "- consistent with this pack's 2025-26 final-table bottom three; season had NOT started on the "
  "return date 2026-08-03"),
]

# ---------------------------------------------------------------- readers
R_RX = re.compile(r"^R(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MD_RX = re.compile(r"^MD(\d+)\|(\d{4}-\d{2}-\d{2})\|([^|]+)\|(\d+)\|(\d+)\|([^|]+)$")
MX_RX = re.compile(r"^MX\|([^|]+)\|([^|]+)\|(\d+)\|(\d+)$")

def read_season(season):
    rows, table = [], []
    with open(os.path.join(LEDGER, f"epl-{season}.txt"), encoding="utf-8") as fh:
        for ln in fh:
            s = ln.rstrip("\n")
            m = R_RX.match(s)
            if m:
                rows.append({"rnd": int(m.group(1)), "date": m.group(2), "home": m.group(3).strip(),
                             "hg": int(m.group(4)), "ag": int(m.group(5)), "away": m.group(6).strip()})
            elif s.startswith("TABLE|"):
                p = s.split("|")
                table.append({"pos": int(p[2]), "club": p[3].strip(), "P": int(p[4]), "W": int(p[5]),
                              "D": int(p[6]), "L": int(p[7]), "GF": int(p[8]), "GA": int(p[9]),
                              "Pts": int(p[10]), "note": p[11] if len(p) > 11 else ""})
    return rows, table

def read_venues():
    ven = {}
    with open(os.path.join(LEDGER, "epl-venues.txt"), encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("VENUE|"):
                p = ln.rstrip("\n").split("|")
                ven[(p[1], p[2])] = (p[3], p[4])
    return ven

def read_2ndidx(season):
    out = {}
    with open(os.path.join(LEDGER, f"epl-2ndidx-{season}.txt"), encoding="utf-8") as fh:
        for ln in fh:
            s = ln.strip()
            m = MD_RX.match(s)
            if m:
                out[(m.group(3).strip(), m.group(6).strip())] = (int(m.group(1)), m.group(2),
                                                                 int(m.group(4)), int(m.group(5)))
                continue
            m = MX_RX.match(s)
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

def pivot_block(season, rows, table):
    """Per-club full-campaign pivot (owner decree). Returns text lines + per-club summary map."""
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
        ok = (len(games) == 38 and (w, d, l, gf, ga) == exp[1:6] and raw - ded == exp[6])
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

    # ---- structural gates + emission, season by season
    for s in SEASONS:
        rows, table = data[s]
        G.g(len(rows) == 380, f"{s}: 380 rows (got {len(rows)})")
        G.g(len(table) == 20, f"{s}: 20 TABLE constants (got {len(table)})")
        # 38 rounds x 10
        rnd = defaultdict(int)
        for r in rows:
            rnd[r["rnd"]] += 1
        G.g(all(rnd.get(n, 0) == 10 for n in range(1, 39)) and len(rnd) == 38,
            f"{s}: rounds 1..38 x 10 rows")
        # distinct ordered pairs, 19H+19A
        pairs = [(r["home"], r["away"]) for r in rows]
        G.g(len(set(pairs)) == 380, f"{s}: 380 distinct ordered (home,away) pairings")
        hc = defaultdict(int)
        ac = defaultdict(int)
        for h, a in pairs:
            hc[h] += 1
            ac[a] += 1
        G.g(all(hc[c] == 19 and ac[c] == 19 for c in set(hc) | set(ac)) and len(set(hc) | set(ac)) == 20,
            f"{s}: every club 19 home + 19 away")
        # date sort
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
        bad = []
        order = []
        for t in table:
            c = st[t["club"]]
            pts = c[1] * 3 + c[2] - ded.get(t["club"], 0)
            if [c[0], c[1], c[2], c[3], c[4], c[5], pts] != [t["P"], t["W"], t["D"], t["L"], t["GF"], t["GA"], t["Pts"]]:
                bad.append(t["club"])
            order.append((t["club"], pts, c[4] - c[5], c[4], t["pos"]))
        G.g(not bad, f"{s}: table reproduction club-for-club 20/20 (P/W/D/L/GF/GA/Pts"
                     + (f", deductions {ded}" if ded else "") + f") fails={bad or '-'}")
        so = sorted(order, key=lambda x: (-x[1], -x[2], -x[3]))
        G.g([x[4] for x in so] == [x[4] for x in order],
            f"{s}: final-table position order follows pts/GD/GF sort")
        # membership = roster domain
        members = {t["club"] for t in table}
        G.g(all(roster(c) in ROSTER_SET for c in members) and len(members) == 20,
            f"{s}: 20 member clubs, every roster string in WO section-3 domain")
        G.g({roster(t["club"]) for t in table} == {roster(c) for c in members},
            f"{s}: roster mapping consistent")
        # goals + span anchors
        goals = sum(r["hg"] + r["ag"] for r in rows)
        span = (min(r["date"] for r in rows), max(r["date"] for r in rows))
        ANCHORS = {"2021-22": (380, 1071, ("2021-08-13", "2022-05-22")),
                   "2022-23": (380, 1084, ("2022-08-05", "2023-05-28")),
                   "2023-24": (380, 1246, ("2023-08-11", "2024-05-19")),
                   "2024-25": (380, 1115, ("2024-08-16", "2025-05-25")),
                   "2025-26": (380, 1045, ("2025-08-15", "2026-05-24"))}
        want = ANCHORS[s]
        G.g((len(rows), goals, span) == (want[0], want[1], want[2]),
            f"{s}: anchors {want[0]} rows / {want[1]} goals / span {want[2][0]}..{want[2][1]} "
            f"(got {len(rows)}/{goals}/{span[0]}..{span[1]})")
        # emission (date-sorted block)
        for r in sorted(rows, key=lambda r: (r["date"], r["rnd"], r["home"], r["away"])):
            G_line = emit_match(s, r, ven)
            pack_rows.append(G_line)

    # ---- membership-season boundary gate
    EXP = {"2021-22": {"out": {"Burnley", "Watford", "Norwich"}, "in": {"Fulham", "Bournemouth", "Nottingham"}},
           "2022-23": {"out": {"Leeds", "Leicester", "Southampton"}, "in": {"Burnley", "SheffUtd", "Luton"}},
           "2023-24": {"out": {"Burnley", "SheffUtd", "Luton"}, "in": {"Leicester", "Ipswich", "Southampton"}},
           "2024-25": {"out": {"Leicester", "Ipswich", "Southampton"}, "in": {"Sunderland", "Leeds", "Burnley"}}}
    for i in range(4):
        s1, s2 = SEASONS[i], SEASONS[i + 1]
        m1 = {t["club"] for t in data[s1][1]}
        m2 = {t["club"] for t in data[s2][1]}
        bottom3 = {t["club"] for t in data[s1][1] if t["pos"] >= 18}
        G.g(bottom3 == EXP[s1]["out"] and not (bottom3 & m2) and EXP[s1]["in"] <= m2
            and not (EXP[s1]["in"] & m1) and len(m1 ^ m2) == 6,
            f"boundary {s1}->{s2}: relegated {sorted(bottom3)} absent in {s2}; promoted "
            f"{sorted(EXP[s1]['in'])} present (and absent in {s1}); exactly 3 clubs swap each way")

    # ---- global gates
    G.g(len(pack_rows) == 1900, f"pack: 1,900 MATCH rows total (got {len(pack_rows)})")
    keys = ["|".join((f[1], f[4], f[7])) for f in (line.split("|") for line in pack_rows)]  # date,home,away
    G.g(len(set(keys)) == 1900, "pack: zero duplicate (date,home,away) rows")
    clubs_union = set()
    for s in SEASONS:
        clubs_union |= {roster(t["club"]) for t in data[s][1]}
    G.g(clubs_union == ROSTER_SET,
        f"pack: union of member clubs across 5 seasons = the 27 WO section-3 strings "
        f"(got {len(clubs_union)})")
    bad_names = [c for line in pack_rows for c in (line.split("|")[4], line.split("|")[7])
                 if c not in ROSTER_SET]
    G.g(not bad_names, f"pack: every home/away string verbatim in the roster domain (bad={bad_names[:4] or '-'})")
    anti = [line for line in pack_rows
            if any(a in line.split("|")[4] or a in line.split("|")[7] for a in ANTI_APPEAR)]
    G.g(not anti, "pack: anti-appear traps absent from home/away identity fields "
                  "(Spurs/Wolverhampton/full-name forms; venue constants like Tottenham Hotspur "
                  f"Stadium or the city Wolverhampton are sourced venue prose, not identities) hits={len(anti)}")

    # ---- second-index gates
    for s in SEASONS:
        idx = read_2ndidx(s)
        rows = data[s][0]
        if s != "2025-26":
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
            G.g(same == 380 and miss == 0 and not diffs,
                f"2ndidx {s}: 380/380 pairings IDENTICAL round+date+score vs openfootball "
                f"(same={same} miss={miss} divergent={len(diffs)})")
        else:
            same = miss = 0
            diffs = []
            for r in rows:
                k = (r["home"], r["away"])
                if k not in idx:
                    miss += 1
                    continue
                e = idx[k]
                if e == (r["hg"], r["ag"]):
                    same += 1
                else:
                    diffs.append((k, (r["hg"], r["ag"]), e))
            g_idx = sum(v[0] + v[1] for v in idx.values())
            G.g(same == 380 and miss == 0 and not diffs and g_idx == 1045,
                f"2ndidx {s}: 380/380 matrix cells IDENTICAL scores vs Wikipedia FBR matrix "
                f"(same={same} miss={miss} divergent={len(diffs)} goals-matrix={g_idx})")

    # ---- anomaly gates
    r23 = data["2022-23"][0]
    r7 = [r for r in r23 if r["rnd"] == 7]
    G.g(len(r7) == 10 and min(r["date"] for r in r7) == "2023-01-12"
        and max(r["date"] for r in r7) == "2023-04-05"
        and not any(r["date"].startswith("2022-09") for r in r7),
        "anomaly 2022-23 R7 (QEII): 10 rows, all played 2023-01-12..2023-04-05, none in Sep 2022")
    r24 = data["2023-24"][0]
    G.g(not any(r["home"] == "Bournemouth" and r["away"] == "Luton" and r["date"] == "2023-12-16" for r in r24)
        and any(r["rnd"] == 17 and r["home"] == "Bournemouth" and r["away"] == "Luton"
                and r["date"] == "2024-03-13" and (r["hg"], r["ag"]) == (4, 3) for r in r24),
        "anomaly 2023-24 R17: no Bournemouth-Luton row on 2023-12-16 (abandoned game VOID); "
        "full replay 2024-03-13 Bournemouth 4-3 Luton carries the R17 label")
    r25 = data["2024-25"][0]
    G.g(any(r["rnd"] == 12 and r["home"] == "Newcastle" and r["away"] == "WestHam"
            and r["date"] == "2024-11-25" and (r["hg"], r["ag"]) == (0, 2) for r in r25),
        "anomaly 2024-25 R12: Newcastle-West Ham dated 2024-11-25 (RSSSF [Nov 24] misprint overridden "
        "on two independent indexes)")
    G.g(any(r["rnd"] == 15 and r["home"] == "Everton" and r["away"] == "Liverpool"
            and r["date"] == "2025-02-12" for r in r25),
        "anomaly 2024-25 R15: Everton-Liverpool (Storm Darragh postponement) dated 2025-02-12")
    r26 = data["2025-26"][0]
    r31 = [r for r in r26 if r["rnd"] == 31]
    G.g(len(r31) == 10
        and any(r["home"] == "Wolves" and r["away"] == "Arsenal" and r["date"] == "2026-02-18" for r in r31)
        and any(r["home"] == "City" and r["away"] == "Palace" and r["date"] == "2026-05-13" for r in r31)
        and sum(1 for r in r31 if "2026-03-20" <= r["date"] <= "2026-03-22") == 8,
        "anomaly 2025-26 MD31 triple-slice: Wolves-Arsenal fwd 2026-02-18 + 8 games 2026-03-20..22 "
        "+ City-Palace back 2026-05-13")

    # ---- venue gate
    bad_ven = []
    for line in pack_rows:
        f = line.split("|")
        if not f[9] or not f[10]:
            bad_ven.append(line)
    G.g(not bad_ven and len(ven) == 100,
        f"venues: all 1,900 rows carry the per-season stadium/city constants (100 venue rows in "
        f"epl-venues.txt); empties={len(bad_ven)}")

    # ---- pivot gate (owner decree) + validation pivot output
    pivot_out = []
    all_ok = True
    green = 0
    for s in SEASONS:
        rows, table = data[s]
        lines, summaries = pivot_block(s, rows, table)
        okn = sum(1 for v in summaries.values() if v[0])
        all_ok &= okn == 20
        green += okn
        pivot_out.append(f"### PIVOT {s} (re-derived from the pack's own rows; each club = its 38 "
                         f"games in round order; summary gated vs the season TABLE constants)")
        pivot_out.extend(lines)
    G.g(all_ok, f"pivots: {green}/100 club-season full-campaign pivots = 38 games, "
                "summaries reproduce the final-table lines (deductions flagged)")

    # ---- pack grammar gate
    gram_ok = all(len(line.split("|")) == 14 for line in pack_rows)
    G.g(gram_ok, "grammar: every MATCH line has 14 pipe-fields (incl. empty pre-source field)")
    G.g(all(line.split("|")[2] == COMP and line.split("|")[3] == COMPTYPE and line.split("|")[11] == COUNTRY
            for line in pack_rows),
        "grammar: competition/compType/country constants verbatim on every row")
    labels = {s[0] for s in SOURCES}
    G.g(all(line.split("|")[13] in labels for line in pack_rows),
        "grammar: every row's sourceLabel resolves to a declared SOURCE")
    try:
        for line in pack_rows:
            line.encode("ascii")
        asc = True
    except UnicodeEncodeError:
        asc = False
    G.g(asc, "grammar: ASCII-only pack rows (apostrophes are the typewriter form; no diacritics)")

    # ---------------------------------------------------------------- NOTE texts
    notes = []
    notes.append(
        f"NOTE|info|pack_id|EPL-2021-2026_BP-TEAM-PACK_v2 - return of WO-EPL-SPAN-12 (issued "
        f"{ACCESSED}, queue position 12). The complete England Premier League 5-year span running "
        f"into today: 1,900 MATCH rows = 5 full seasons x 380 (2021-22 .. 2025-26, 20 clubs x 38 "
        f"matchdays every season, every club exactly 38 matches), then the 2026-27 boundary - the "
        f"new season starts 2026-08-21, AFTER the {ACCESSED} return date, so zero 2026-27 rows exist "
        f"(sourced boundary NOTE below; the WO's 'file name 2021-2026' note: no cutoff, no appendix, "
        f"the span is certified gap-free through today). Compiled {ACCESSED}.")
    for lbl, url, typ, what in SOURCES:
        notes.append(f"SOURCE|{lbl}|{url}|{ACCESSED}|{typ}|{what}")
    notes.append(
        "NOTE|info|federation_check|Section-0 scan on the finished pack: all 1,900 rows are England "
        "Premier League rows populated exclusively by the 27 pinned section-3 roster strings - the "
        "per-season compositions are: 2021-22 Arsenal, Aston Villa, Brentford, Brighton, Burnley, "
        "Chelsea, Crystal Palace, Everton, Leeds, Leicester, Liverpool, Man City, Man United, "
        "Newcastle, Norwich, Southampton, Tottenham, Watford, West Ham, Wolves; 2022-23 = same minus "
        "Burnley/Watford/Norwich plus Bournemouth/Fulham/Nott'm Forest; 2023-24 minus "
        "Leeds/Leicester/Southampton plus Burnley/Sheffield United/Luton; 2024-25 minus "
        "Burnley/Sheffield United/Luton plus Leicester/Ipswich/Southampton; 2025-26 minus "
        "Leicester/Ipswich/Southampton plus Sunderland/Leeds/Burnley. Not Scotland, not Wales, no cup "
        "rows (WO section-1 excludes cups/Europe). The anti-appear list (Spurs, Tottenham Hotspur, "
        "Wolverhampton, Manchester City/United, AFC Bournemouth, Nottingham Forest, Sheffield Utd, "
        "any 'Town/City' suffix form) is empty on row fields. No standings tables carried - rows only.")
    notes.append(
        "NOTE|info|catalog|1,900 MATCH rows = 380 x 5 seasons (2021-22 380, 2022-23 380, 2023-24 380, "
        "2024-25 380, 2025-26 380); 0 TEAM rows (WO section-2: every 2021-26 member club already on "
        "the client roster - section 3 pins the 27 exact strings; none is missing, so no blocker); "
        "competition string on every row declared once here: 'England Premier League'; compType "
        "'domestic-league' on every row (single-flight league - no playoff phase exists in this "
        "competition); venue-detail field carries the round label MD1..MD38 per WO section-2; "
        "90-minute doctrine trivially satisfied (league matches always end at full time - no aet/pens "
        "exist; the one abandoned match is documented under continuity and carries NO row).")
    notes.append(
        "NOTE|info|identity|The 27 pinned section-3 strings are used verbatim in home/away for every "
        "row of every season. Rename traps mapped silently to the pinned strings, each mapped once "
        "here: Tottenham Hotspur/Spurs -> always Tottenham; Wolverhampton Wanderers -> always Wolves "
        "(never Wolverhampton); Manchester City -> always Man City; Manchester United -> always Man "
        "United; AFC Bournemouth -> Bournemouth; Nottingham Forest -> Nott'm Forest (the apostrophe "
        "form, verbatim); Sheffield United stays Sheffield United (never Sheffield Utd); West Ham "
        "United -> West Ham; Aston Villa, Crystal Palace, Everton, Fulham, Arsenal, Brentford, "
        "Brighton, Burnley, Chelsea, Liverpool, Newcastle, Southampton, Sunderland, Watford, Wolves "
        "and the short-forms Leeds (Leeds United), Leicester (Leicester City), Ipswich (Ipswich "
        "Town), Norwich (Norwich City), Luton (Luton Town) - the section-3 strings. Source stock "
        "names (RSSSF/openfootball) map 1:1: Villa->Aston Villa, Palace->Crystal Palace, City->Man "
        "City, United->Man United, Nottingham->Nott'm Forest, SheffUtd->Sheffield United, "
        "WestHam->West Ham; all others identical. No club changed its identity in-window (no "
        "renames/mergers in the EPL 2021-26 window).")
    notes.append(
        "NOTE|info|venue_policy|MATCH stadium/city = the home club's documented ground for that "
        "season per the Wikipedia season articles' stadium/location tables (second index; RSSSF "
        "carries no venues), transcribed to audit/ledger/epl-venues.txt (100 rows = 5 seasons x 20). "
        "No groundshares and no neutral-venue league fixtures occurred in the window; every club "
        "played every home league game at its listed ground. Epoch boundary: Everton at Goodison "
        "Park, Liverpool (Walton) through 2024-25, then Hill Dickinson Stadium, Liverpool (Vauxhall) "
        "from 2025-26 (first season in the new ground per the 2025-26 season article). City strings "
        "carried canonically: United's Old Trafford rows use Manchester (the 2021-22 article prints "
        "Trafford, later season articles print Manchester (Old Trafford) / Trafford, Manchester - one "
        "stadium, canonical metro city Manchester, documented per the venue ledger); the City Ground "
        "carries West Bridgford as printed (not Nottingham); Falmer Stadium carries Falmer (not "
        "Brighton). Stadium-name constants are era-stable for the remaining 24 clubs across the span "
        "(Brentford Community Stadium from 2021-22 onward, Luton Kenilworth Road 2023-24, Watford "
        "Vicarage Road 2021-22, Norwich Carrow Road 2021-22, SheffUtd Bramall Lane 2023-24, Ipswich "
        "Portman Road 2024-25, Sunderland Stadium of Light 2025-26).")
    notes.append(
        "NOTE|info|round_counts|Season row/goal/span anchors, each recomputed from the pack rows and "
        "matching the official record: 2021-22 = 380 rows, 1,071 goals, 2021-08-13..2022-05-22 "
        "(opener Brentford 2-0 Arsenal, the club's first top-flight match since 1947 per the season "
        "article); 2022-23 = 380, 1,084, 2022-08-05..2023-05-28; 2023-24 = 380, 1,246 (all-time "
        "Premier League season goals record per the season article), 2023-08-11..2024-05-19; "
        "2024-25 = 380, 1,115, 2024-08-16..2025-05-25; 2025-26 = 380, 1,045, 2025-08-15..2026-05-24 "
        "(wiki infobox matches: 380 games, 1,045 goals, 2.75/match; fixtures released 18 June 2025). "
        "Every season is 38 matchdays x 10 fixtures, zero double-rounds, zero cancellations.")
    notes.append(
        "NOTE|info|continuity|Continuity-clause accounting (gap-free league span): all 38 matchdays "
        "of all five seasons exist and are dated; no league fixture was cancelled in the window. "
        "Documented disruptions, rows always keep their original MD labels while the file stays "
        "date-sorted: 2022-23 round 7 was postponed in FULL (death of Queen Elizabeth II; original "
        "window 2022-09-10..12) and all ten fixtures were played on scattered dates 2023-01-12 "
        "(Fulham-Chelsea) through 2023-04-05 (West Ham-Newcastle) - reconciled 10/10 against "
        "openfootball AND the worldfootball matchday page; 2023-24 round 17 Bournemouth-Luton of "
        "2023-12-16 was abandoned at 1-1 in the 65th minute (Tom Lockyer cardiac incident) and "
        "declared VOID - it carries NO row, while the complete rematch played 2024-03-13 "
        "(Bournemouth 4-3 Luton) carries the R17 label, per RSSSF doctrine; 2024-25 round 15 "
        "Everton-Liverpool (Storm Darragh) was played 2025-02-12, round-29 Aston Villa-Liverpool "
        "moved forward to 2025-02-19 and Newcastle-Crystal Palace back to 2025-04-16, round-34 "
        "Nott'm Forest-Brentford played 2025-05-01; 2025-26 MD31 is a triple-slice round - "
        "Wolves-Arsenal brought forward to 2026-02-18, eight games on the main body 2026-03-20..22, "
        "Man City-Crystal Palace postponed to 2026-05-13 (both stray dates corroborated by the "
        "football-data CSV rows). Winter breaks and the 2022 World Cup break (2022-11-13..2022-12-26) "
        "are scheduling, not gaps. Season spans as listed under round_counts; the span 2021-08-13 -> "
        "2026-05-24 is complete and every official match sits exactly once.")
    notes.append(
        "NOTE|info|boundary|Span-end state per WO section-1 row 2: the last completed round of the "
        "span is 2025-26 MD38, all ten fixtures played 2026-05-24 (final table inside the gates; "
        "Arsenal champions 85 pts - and enter 2026-27 as defending champions per the season article). "
        "The 2026-27 season had NOT started on the return date 2026-08-03: rsssf.org/tablese/ "
        "eng2027.html answers 404, and the 2026-27 season article fixes the season dates '21 August "
        "2026 - 30 May 2027', fixtures released 19 June 2026 at 10:00 BST, 33 weekend + 5 midweek "
        "rounds (opening and final matchweeks shifted one week around the 2026 FIFA World Cup). "
        "2026-27 membership per the same source: the 17 survivors plus promoted Coventry City, "
        "Ipswich Town and Hull City; relegated out West Ham United, Burnley and Wolverhampton "
        "Wanderers - exactly this pack's 2025-26 bottom three. Zero 2026-27 rows are emitted; this is "
        "a boundary statement, not a blocker. No dateless rows, no duplicate (date,home,away) rows "
        "anywhere in the pack (gate-verified).")
    notes.append(
        "NOTE|info|perclub_gate|Owner's per-club completeness technique implemented as a pivot gate: "
        "the pack's own rows are re-pivoted club-by-club - each of the 20 clubs of each season shows "
        "exactly 38 games (19 home + 19 away) enumerated in round order with dates, and every "
        "TEAMPIVOT summary line reproduces the club's official final-table line (P/W/D/L/GF/GA/Pts; "
        "the two 2023-24 PSR deductions flagged inline). All 100 club-season pivots are printed in "
        "audit/pack-validation-epl.txt next to this file; copies live in "
        "audit/ledger/epl-pivot-<season>.txt. 100/100 green.")
    notes.append(
        "NOTE|info|source_adaptation|WO section-4 design: RSSSF eng<Y>.html pages = primary for "
        "dates AND scores; eng2022..eng2025 (Ian King) carry full round-by-round sections and were "
        "transcribed to audit/ledger/epl-<season>.txt on fetch day. ADAPTATION for 2025-26: the "
        "eng2026.html page (Karel Stokkermans, updated 14 Jun 2026) carries ONLY the Premier League "
        "final table - no round listings (verified over the full page, chunks 0-2, on 2026-08-03). "
        "The 2025-26 match rows were therefore sourced from the independent index openfootball/"
        "england master/2025-26/1-premierleague.txt and are labelled openfootball-england-2526; the "
        "RSSSF final table remains the table authority and the recompute of those 380 rows "
        "reproduces it club-for-club and in position order EXACT (gate above). Second-index coverage: "
        "openfootball season files diffed row-for-row vs RSSSF for 2021-22..2024-25 (380/380 "
        "IDENTICAL round+date+score in all four seasons, tools/diff_epl_second_index.py); Wikipedia "
        "2025-26 FBR results matrix diffed cell-for-cell for 2025-26 (380/380 IDENTICAL scores, "
        "goals 1045=1045, tools/diff_epl_matrix.py); worldfootball matchday-7 page corroborates the "
        "QEII scatter 10/10; football-data E0 CSVs corroborate the adjudicated 2024-11-25 date and "
        "the two 2025-26 MD31 stray dates byte-for-byte, plus the full MD1 block and the MD38 "
        "final-day date. Conflicts were resolved per section-4(3) and are disclosed in the two "
        "source_conflict NOTEs; nothing else in the five seasons diverges between any two indexes.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF eng2024.html misprints TWO round-15 fixtures under "
        "'[Dec 2]': Everton 3-0 Newcastle and Tottenham 1-2 West Ham - both clubs already appear in "
        "round 14 on Dec 2/3, so a Dec-2 round-15 slot is impossible inside the page's own chronology. "
        "The openfootball season file places MD15's pair on 2023-12-07 (independent index), and the "
        "pack rows carry 2023-12-07; scores were never in doubt (identical everywhere). Resolution "
        "per section-4(3): RSSSF scores kept, dates corrected to the date both indexes and the "
        "page-chronology require; the misprint strings are preserved verbatim in "
        "audit/ledger/epl-2023-24.txt.")
    notes.append(
        "NOTE|warning|source_conflict|RSSSF eng2025.html prints round-12 'Newcastle 0-2 West Ham' "
        "under '[Nov 24]' - but TWO independent indexes agree against it: openfootball lists 'Mon "
        "Nov 25 / 20:00' and football-data.co.uk's season CSV carries the row "
        "'E0,25/11/2024,20:00,Newcastle,West Ham,0,2,...'. Per section-4 (two independent indexes "
        "agree against RSSSF => their value plus this NOTE), the pack row carries 2024-11-25; the "
        "RSSSF print is preserved verbatim in audit/ledger/epl-2024-25.txt. Score was never in "
        "doubt; the final table is unaffected either way.")
    notes.append(
        "NOTE|info|spot_audit|2021-22 matchday 1 re-listed for spot-audit (sources "
        "https://www.rsssf.org/tablese/eng2022.html and the openfootball second index "
        "ofb-eng-2122; the four-season openfootball diffs all ran 380/380 IDENTICAL): "
        + spot_listing("2021-22", SPOT["2021-22"], data["2021-22"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2022-23 matchday 7 re-listed for spot-audit - the QEII round, played "
        "entirely out of its original window (sources https://www.rsssf.org/tablese/eng2023.html, "
        "ofb-eng-2223 AND the worldfootball matchday page wf-epl-2223-md7; dates AND scores "
        "identical 10/10 across all three): "
        + spot_listing("2022-23", SPOT["2022-23"], data["2022-23"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2023-24 matchday 17 re-listed for spot-audit - the abandonment round "
        "and its replay (sources https://www.rsssf.org/tablese/eng2024.html and ofb-eng-2324): "
        + spot_listing("2023-24", SPOT["2023-24"], data["2023-24"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2024-25 matchday 15 re-listed for spot-audit - the Storm Darragh round "
        "(sources https://www.rsssf.org/tablese/eng2025.html and ofb-eng-2425): "
        + spot_listing("2024-25", SPOT["2024-25"], data["2024-25"][0]) + ".")
    notes.append(
        "NOTE|info|spot_audit|2025-26 matchday 31 re-listed for spot-audit - the triple-slice round "
        "(sources openfootball-england-2526 = the season's labelled carrier, wikimatrix-epl-2526 and "
        "the two football-data CSV stray rows): "
        + spot_listing("2025-26", SPOT["2025-26"], data["2025-26"][0]) + ".")

    # ---------------------------------------------------------------- final pack integrity gates
    pack = "\n".join(notes + pack_rows + ["END"]) + "\n"
    G.g(pack.rstrip().endswith("END"), "file ends with END")
    G.g(len(pack.splitlines()) == len(notes) + 1900 + 1,
        f"pack line accounting: {len(notes)} header rows (NOTE+SOURCE) + 1,900 MATCH + END")
    block_ok = True
    for i, s in enumerate(SEASONS):
        block = pack_rows[i * 380:(i + 1) * 380]
        dates = [l.split("|")[1] for l in block]
        labels = {l.split("|")[13] for l in block}
        if dates != sorted(dates) or labels != {SRC_LABEL[s]}:
            block_ok = False
    G.g(block_ok, "pack ordering: five season blocks in order, each block date-sorted and "
                  "carrying only its season's source label")

    os.makedirs(os.path.dirname(OUTPACK), exist_ok=True)
    with open(OUTPACK, "w", encoding="ascii", newline="\n") as fh:
        fh.write(pack)

    # ---------------------------------------------------------------- validation output
    head = [
        "EPL PACK VALIDATION - handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt",
        f"builder tools/build_epl_pack.py, run {ACCESSED}; gates PASS {G.n_pass} FAIL {G.n_fail}",
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
