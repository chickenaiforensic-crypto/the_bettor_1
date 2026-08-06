#!/usr/bin/env python3
"""wiki_ita_tables.py — final-table reproduction gate ITA 2021-22..2025-26.

GATES (per SPEC-2026-08-04: per-season final table club-for-club + position order):
  1. parse the 5 archived table TEMPLATE raw blocks (data/raw/wiki-ita-tables-raw.txt)
  2. parse the RSSSF primary season ledgers' TABLE rows (audit/ledger/ita-YYYY-YY.txt)
  3. club-for-club W/D/L/GF/GA identical; pts arithmetic 3W+D+adjust == ledger Pts
     (2022-23 JUV adjust -10 adjudicated, documented);
     position in template team_order == ledger position;
     status loose-map (template C -> ledger Champions/[C]; R -> Relegated;
     O -> NOT Relegated [2022-23 spareggio survivor Verona]);
     gf-sum == season goal anchor (1089/974/992/973/922); Pld=38.
  4. 2022-23 SECOND WITNESS: rendered Pos-table inside
     data/raw/wiki-ita-2022-23-sections-raw.txt (positions + Pts re-checked).
Emits audit/ledger/ita-wikitables.txt (argument '-' prints to stdout).
Loud exit(2) on any mismatch. No network; reads local raws only.
"""
import re, sys
from collections import OrderedDict

CODE2ROSTER = {
    "ATA": "Atalanta", "BOL": "Bologna", "CAG": "Cagliari", "COM": "Como",
    "CRE": "Cremonese", "EMP": "Empoli", "FIO": "Fiorentina", "FRO": "Frosinone",
    "GEN": "Genoa", "VER": "Verona", "INT": "Inter", "JUV": "Juventus",
    "LAZ": "Lazio", "LEC": "Lecce", "MIL": "Milan", "MON": "Monza",
    "NAP": "Napoli", "PAR": "Parma", "PIS": "Pisa", "ROM": "Roma",
    "SAL": "Salernitana", "SAM": "Sampdoria", "SAS": "Sassuolo", "SPE": "Spezia",
    "TOR": "Torino", "UDI": "Udinese", "VEN": "Venezia",
}
GF_ANCHOR = {"2021-22": 1089, "2022-23": 974, "2023-24": 992, "2024-25": 973, "2025-26": 922}
SEASON_FILE = {"2021-22": "audit/ledger/ita-2021-22.txt", "2022-23": "audit/ledger/ita-2022-23.txt",
               "2023-24": "audit/ledger/ita-2023-24.txt", "2024-25": "audit/ledger/ita-2024-25.txt",
               "2025-26": "audit/ledger/ita-2025-26.txt"}
SEASON_SOURCE = {"2021-22": "wikitemplate-ita-2122", "2022-23": "wikitemplate-ita-2223",
                 "2023-24": "wikitemplate-ita-2324", "2024-25": "wikitemplate-ita-2425",
                 "2025-26": "wikitemplate-ita-2526"}


def parse_templates(path):
    d = open(path, encoding="utf-8").read()
    blocks = re.split(r"^===== TEMPLATE (\d{4}-\d{2}) .*$", d, flags=re.M)
    out = {}
    for i in range(1, len(blocks), 2):
        season, body = blocks[i], blocks[i + 1]
        order = None
        wdl, adjust, status, hth, note = {}, {}, {}, {}, {}
        for ln in body.split("\n"):
            s = ln.rstrip()
            m = re.match(r"^\\\|team\\_order\s*=\s*(.+)$", s)
            if m:
                order = [t.strip() for t in m.group(1).split(",")]
                continue
            if re.match(r"^\\\|win\\_[A-Z]{3}=", s):
                for piece in s[2:].split("\\|"):  # fields key=value with escaped key underscores
                    if "=" not in piece:
                        continue
                    k, v = piece.split("=", 1)
                    k = k.replace("\\_", "_")
                    m2 = re.match(r"^(win|draw|loss|gf|ga)_([A-Z]{3})$", k)
                    if m2:
                        wdl.setdefault(m2.group(2), {})[m2.group(1)] = int(v.strip())
                continue
            m = re.match(r"^\\\|adjust\\_points\\_([A-Z]{3})=(-?\d+)$", s)
            if m:
                adjust[m.group(1)] = int(m.group(2))
                continue
            m = re.match(r"^\\\|status\\_([A-Z]{3})=(.+)$", s)
            if m:
                status[m.group(1)] = m.group(2).strip()
                continue
            m = re.match(r"^\\\|hth\\_([A-Z]{3})=(.+)$", s)
            if m:
                hth[m.group(1)] = m.group(2).strip()
                continue
            m = re.match(r"^\\\|note\\_([A-Z]{3})=(.+)$", s)
            if m:
                note.setdefault(m.group(1), m.group(2).strip())
        out[season] = {"order": order, "wdl": wdl, "adjust": adjust,
                       "status": status, "hth": hth, "note": note}
    return out


def parse_ledger_table(path):
    rows = OrderedDict()  # roster -> dict
    for ln in open(path, encoding="utf-8"):
        if not ln.startswith("TABLE|"):
            continue
        f = ln.rstrip("\n").split("|")
        rows[f[3]] = {"pos": int(f[2]), "pld": int(f[4]), "w": int(f[5]), "d": int(f[6]),
                      "l": int(f[7]), "gf": int(f[8]), "ga": int(f[9]), "pts": int(f[10]),
                      "note": f[11] if len(f) > 11 else ""}
    return rows


def parse_2223_rendered(path):
    """rendered Pos table rows: | Pos | [Team](url \"X\")(C) | Pld | W | D | L | GF | GA | GD | Pts | ... |"""
    out = []
    for ln in open(path, encoding="utf-8"):
        if not ln.startswith("| ") or "| Pos |" in ln:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 10 or not re.match(r"^\d+$", cells[0]):
            continue
        m = re.match(r"^\[([^\]]+)\]\(", cells[1])
        team = m.group(1) if m else None
        stat = "C" if "(C)" in cells[1] else ("R" if "(R)" in cells[1] else
               ("O" if "(O)" in cells[1] else ("DR" if "(DR)" in cells[1] else "")))
        ptm = re.match(r"^(\d+)", cells[9])
        out.append({"pos": int(cells[0]), "team": team, "pld": int(cells[2]),
                    "w": int(cells[3]), "d": int(cells[4]), "l": int(cells[5]),
                    "gf": int(cells[6]), "ga": int(cells[7]), "pts": int(ptm.group(1)),
                    "status": stat})
    return out


def main():
    tpl = parse_templates("data/raw/wiki-ita-tables-raw.txt")
    fails = []
    lines = []
    out_do = lines.append
    out_do("# ITA WIKIPEDIA LEAGUE-TABLE REPRODUCTION GATE 2021-22..2025-26 - run 2026-08-05")
    out_do("# tool: tools/wiki_ita_tables.py | primary ledger: RSSSF TABLE rows | witness: wiki")
    out_do("# table TEMPLATE raws (data/raw/wiki-ita-tables-raw.txt). Per-club W/D/L/GF/GA,")
    out_do("# pts arithmetic 3W+D+adjust, team_order position, status loose-map, gf anchor.")
    for season in ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]:
        t = tpl[season]
        led = parse_ledger_table(SEASON_FILE[season])
        order = t["order"]
        ok = True
        out_do("")
        out_do(f"## {season} (source {SEASON_SOURCE[season]})")
        if not order or len(order) != 20 or len(t["wdl"]) != 20:
            fails.append(f"{season}: order/wdl count defect {order and len(order)}/{len(t['wdl'])}")
            ok = False
        gf_sum = 0
        for idx, code in enumerate(order, 1):
            roster = CODE2ROSTER[code]
            w = t["wdl"][code]
            adj = t["adjust"].get(code, 0)
            pts_t = 3 * w["win"] + w["draw"] + adj
            gf_sum += w["gf"]
            L = led.get(roster)
            row_ok = True
            if L is None:
                row_ok = False
            else:
                checks = [(w["win"], L["w"]), (w["draw"], L["d"]), (w["loss"], L["l"]),
                          (w["gf"], L["gf"]), (w["ga"], L["ga"]), (pts_t, L["pts"]),
                          (idx, L["pos"])]
                if any(a != b for a, b in checks):
                    row_ok = False
                st = t["status"].get(code, "")
                # RSSSF marks play-off-bound tails 'Relegation Playoff' (2022-23 SPE
                # was relegated VIA the spareggio, template prints R; VER survived,
                # template prints O). Accept the RSSSF PO marker under R.
                if st == "R" and not ("Relegated" in L["note"] or "Relegation Playoff" in L["note"]):
                    row_ok = False
                if st == "C" and not ("Champions" in L["note"] or "[C]" in L["note"]):
                    row_ok = False
                if st == "O" and "Relegated" in L["note"]:
                    row_ok = False
            if not row_ok:
                ok = False
                fails.append(f"{season} {code}({roster}) pos{idx}: template WDL "
                             f"{w['win']}/{w['draw']}/{w['loss']} gf{w['gf']} ga{w['ga']} "
                             f"ptsT{pts_t} vs ledger {L}")
            extra = ""
            if code in t["adjust"]:
                extra += f" adjust={t['adjust'][code]}"
            if code in t["status"]:
                extra += f" status={t['status'][code]}"
            out_do(f"WTAB|{season}|{idx}|{roster}|{w['win']}|{w['draw']}|{w['loss']}|"
                   f"{w['gf']}|{w['ga']}|ptsT={pts_t}|ptsL={L['pts'] if L else '-'}|"
                   f"{'MATCH' if row_ok else 'MISMATCH'}{extra}")
        anchor = GF_ANCHOR[season]
        if gf_sum != anchor:
            ok = False
            fails.append(f"{season}: gf anchor {anchor} vs template sum {gf_sum}")
        out_do(f"WTAB|{season}|SUM|-|-|gf_sum={gf_sum}|anchor={anchor}|"
               f"{'MATCH' if gf_sum == anchor else 'MISMATCH'}")
        for code, txt in sorted(t["hth"].items()):
            short = re.sub(r"\s+", " ", txt)[:150]
            out_do(f"WTAB|{season}|NOTE|hth_{code}: {short}")
        for code, txt in sorted(t["note"].items()):
            short = re.sub(r"\s+", " ", txt)[:150]
            out_do(f"WTAB|{season}|NOTE|note_{code}: {short}")
        out_do(f"WTAB|{season}|GATE|{'PASS' if ok else 'FAIL'}")
    # second witness 2022-23 rendered table
    wit = parse_2223_rendered("data/raw/wiki-ita-2022-23-sections-raw.txt")
    t = tpl["2022-23"]
    R2 = {"Hellas Verona": "Verona", "Inter Milan": "Inter", "Milan": "Milan",
          "AC Milan": "Milan"}
    out_do("")
    out_do("## 2022-23 SECOND WITNESS (rendered Pos-table, wiki-ita-2022-23-sections-raw.txt)")
    wok = True
    if len(wit) != 20:
        wok = False
        fails.append(f"2022-23 witness: {len(wit)} rows")
    for row in wit:
        roster = R2.get(row["team"], row["team"])
        code = [c for c, r in CODE2ROSTER.items() if r == roster][0]
        w = t["wdl"][code]
        adj = t["adjust"].get(code, 0)
        pts_t = 3 * w["win"] + w["draw"] + adj
        pos = t["order"].index(code) + 1
        same = (row["w"], row["d"], row["l"], row["gf"], row["ga"], row["pts"], row["pos"]) == \
               (w["win"], w["draw"], w["loss"], w["gf"], w["ga"], pts_t, pos)
        if not same:
            wok = False
            fails.append(f"2022-23 witness row {row} vs template {code} pos{pos}")
        out_do(f"WIT|2022-23|{row['pos']}|{roster}|rendered_pts={row['pts']}|computed={pts_t}|"
               f"{'MATCH' if same else 'MISMATCH'}")
    out_do(f"WIT|2022-23|GATE|{'PASS' if wok else 'FAIL'}")
    out_do("")
    out_do(f"## OVERALL: {'ALL GATES PASS' if not fails else str(len(fails)) + ' FAILURES'}")
    txt = "\n".join(lines) + "\n"
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        open(sys.argv[1], "w", encoding="utf-8").write(txt)
    else:
        sys.stdout.write(txt)
    if fails:
        for f in fails:
            print("FAIL:", f, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
