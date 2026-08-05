#!/usr/bin/env python3
"""Parse a GER RSSSF raw transcription (data/raw/rsssf-duit<YYYY>-1bl.txt) into
GER ledger machine rows on stdout:

  TABLE|<season>|<pos>|<stock>|<P>|<W>|<D>|<L>|<GF>|<GA>|<Pts>|<flags>     1.BL final table (18)
  TABLE2|<season>|<pos>|<name-as-printed>|<P>|<W>|<D>|<L>|<GF>|<GA>|<Pts>|<flags>  2.BL final table (18)
  R<n>|<dateISO>|<homeStock>|<hg>|<ag>|<awayStock>                        league rounds (306; none for 2025-26)
  PO_PLAYOFF|<season>|<leg>|<dateISO>|<homeStock>|<hg>|<ag>|<awayStock>|<extra>|<flag>[|<NB>]
      leg Final-1/Final-2 = 1./2. playoff -> SHIP-as-other
      leg L2-1/L2-2       = 2./3. playoff -> NOT-COMMISSIONED-L2-internal

Skips: header comments, the "Halfway Table" context block (2022-23 / 2024-25 raw),
NB prose, and the 2./3.-tier context NBs. Round section absent (duit2026) -> zero R rows.
"""
import sys
import re

MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

SHORT = {  # RSSSF round-print short names -> stock
    "Frankfurt": "Frankfurt", "Bayern": "Bayern", "Union": "UnionBerlin",
    "Hertha": "Hertha", "Mönchengladbach": "Mgladbach", "Hoffenheim": "Hoffenheim",
    "Augsburg": "Augsburg", "Freiburg": "Freiburg", "Bochum": "Bochum",
    "Mainz": "Mainz", "Wolfsburg": "Wolfsburg", "Bremen": "WerderBremen",
    "Dortmund": "Dortmund", "Leverkusen": "Leverkusen", "Stuttgart": "Stuttgart",
    "Leipzig": "RBLeipzig", "Köln": "FCKoln", "Schalke": "Schalke04",
    "Bielefeld": "Bielefeld", "Greuther Fürth": "GreutherFurth",
    "Heidenheim": "Heidenheim", "Darmstadt": "Darmstadt",
    "Sankt Pauli": "StPauli", "Kiel": "HolsteinKiel", "Hamburg": "Hamburg",
    "Düsseldorf": "FortunaDusseldorf", "Elversberg": "Elversberg",
    "Paderborn": "SCPaderborn",
    # 2./3. context names (ledger NOT-COMMISSIONED lines keep printed names)
    "Wehen Wiesbaden": "WehenWiesbaden", "Dresden": "DynamoDresden",
    "Kaiserslautern": "FCKaiserslautern", "Regensburg": "JahnRegensburg",
    "Saarbrücken": "FCSaarbrucken", "Braunschweig": "EintrBraunschweig",
    "RW Essen": "RWEssen",
}

TABLE_NAME = {  # RSSSF 1.BL final-table official print -> stock
    "FC Bayern München": "Bayern", "Borussia Dortmund": "Dortmund",
    "Bayer 04 Leverkusen": "Leverkusen", "RB Leipzig": "RBLeipzig",
    "1.FC Union Berlin": "UnionBerlin", "SC Freiburg": "Freiburg",
    "1.FC Köln": "FCKoln", "1.FSV Mainz 05": "Mainz",
    "TSG 1899 Hoffenheim": "Hoffenheim", "Borussia Mönchengladbach": "Mgladbach",
    "Eintracht Frankfurt": "Frankfurt", "VfL Wolfsburg": "Wolfsburg",
    "VfL Bochum": "Bochum", "FC Augsburg": "Augsburg",
    "VfB Stuttgart": "Stuttgart", "Hertha BSC Berlin": "Hertha",
    "DSC Arminia Bielefeld": "Bielefeld", "SpVgg Greuther Fürth": "GreutherFurth",
    "FC Schalke 04 Gelsenkirchen": "Schalke04", "SV Werder Bremen": "WerderBremen",
    "1.FC Heidenheim": "Heidenheim", "SV Darmstadt 98": "Darmstadt",
    "FC Sankt Pauli": "StPauli", "Holstein Kiel": "HolsteinKiel",
    "Hamburger SV": "Hamburg",
}

RE_ROUND = re.compile(r"^Round (\d+)(?:\s+\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\])?\s*$")
RE_DATE = re.compile(r"^\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\]\s*$")
RE_SCORE = re.compile(r"^\s*(.+?) (\d+)-(\d+) (.+?)\s*$")
RE_ANN = re.compile(r"\s+\[.*$")
RE_TABROW = re.compile(r"^\s*(\d+)\.\s*(.+?)\s{2,}(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)\s*(.*)$")
RE_LEG = re.compile(r"^(First|Second) Leg \[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\]\s*$")


def flag_norm(tail):
    tail = tail.strip()
    if not tail:
        return ""
    return re.sub(r"\s+", " ", tail)


def main(path):
    m = re.search(r"duit(\d{4})", path)
    y2 = int(m.group(1))
    y1 = y2 - 1
    season = f"{y1}-{str(y2)[2:]}"

    def iso(mon_name, dd):
        mo = MON[mon_name]
        yy = y1 if mo >= 7 else y2
        return f"{yy:04d}-{mo:02d}-{int(dd):02d}"

    mode = None            # None | table | rounds | po12 | po23 | table2 | halftime-skip
    rnd = None
    cur_date = None
    leg_key = None
    leg_date = None
    po12 = []
    po23 = []
    rows = []
    tab = []
    tab2 = []
    unknown = set()

    seen_table_banner = False
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        s = line.strip()
        if not s:
            continue
        if not seen_table_banner:
            # everything before the first 1.BL final-table banner is transcription header prose
            if s == "Final Table:" or s == "1. Bundesliga Final Table:":
                seen_table_banner = True
                mode = "table"
                continue
            continue
        if s.startswith("Halfway Table"):
            mode = "halftime"
            continue
        if s == "Final Table:" or s == "1. Bundesliga Final Table:":
            if mode != "table" and not tab:
                mode = "table"
                continue
        if s == "2. Bundesliga Final Table:":
            mode = "table2"
            continue
        if s.startswith("Promotion/Relegation Playoff 1./2."):
            mode = "po12"
            continue
        if s.startswith("Promotion/Relegation Playoff 2./3."):
            mode = "po23"
            continue
        m2 = RE_ROUND.match(s)
        if m2:
            if mode in ("table", "halftime", None) and mode != "po12" and mode != "po23" and mode != "table2":
                mode = "rounds"
            if mode == "rounds":
                rnd = int(m2.group(1))
                if m2.group(2):
                    cur_date = iso(m2.group(2), m2.group(3))
            continue
        if mode == "halftime":
            # skip until next Round header (handled above) or PO banner
            continue
        if s.startswith("NB:"):
            continue
        if s.startswith("- ") or s.startswith("---"):
            continue
        m2 = RE_DATE.match(s)
        if m2 and mode == "rounds":
            cur_date = iso(m2.group(1), m2.group(2))
            continue
        m2 = RE_LEG.match(s)
        if m2 and mode in ("po12", "po23"):
            leg_key = ("Final-1" if m2.group(1) == "First" else "Final-2") if mode == "po12" \
                else ("L2-1" if m2.group(1) == "First" else "L2-2")
            leg_date = iso(m2.group(2), m2.group(3))
            continue
        if mode in ("table", "table2"):
            m2 = RE_TABROW.match(line)
            if m2:
                pos, name, p, w, d, l, gf, ga, pts = m2.group(1), m2.group(2).strip(), \
                    int(m2.group(3)), int(m2.group(4)), int(m2.group(5)), int(m2.group(6)), \
                    int(m2.group(7)), int(m2.group(8)), int(m2.group(9))
                flags = flag_norm(m2.group(10))
                if flags == "- - - - - - - - - - - - - - - - - - - - - - - - - - - -":
                    continue
                if mode == "table":
                    st = TABLE_NAME.get(name)
                    if st is None:
                        unknown.add(name)
                        continue
                    tab.append(f"TABLE|{season}|{pos}|{st}|{p}|{w}|{d}|{l}|{gf}|{ga}|{pts}|{flags}")
                else:
                    tab2.append(f"TABLE2|{season}|{pos}|{name}|{p}|{w}|{d}|{l}|{gf}|{ga}|{pts}|{flags}")
            continue
        if mode == "rounds" and cur_date and rnd:
            m2 = RE_SCORE.match(line)
            if m2:
                h = m2.group(1).strip()
                hg, ag = int(m2.group(2)), int(m2.group(3))
                a = RE_ANN.sub("", m2.group(4)).strip()
                hs, as_ = SHORT.get(h), SHORT.get(a)
                if hs is None:
                    unknown.add(h)
                    continue
                if as_ is None:
                    unknown.add(a)
                    continue
                rows.append(f"R{rnd}|{cur_date}|{hs}|{hg}|{ag}|{as_}")
            continue
        if mode in ("po12", "po23") and leg_key and leg_date:
            m2 = RE_SCORE.match(line)
            if m2:
                h = m2.group(1).strip()
                hg, ag = int(m2.group(2)), int(m2.group(3))
                atok = m2.group(4)
                extra = ""
                am = re.search(r"\s{2,}\[(.*?)\]\s*$", atok)
                if am:
                    extra = am.group(1)
                    atok = atok[: am.start()].strip()
                a = RE_ANN.sub("", atok).strip()
                hs, as_ = SHORT.get(h), SHORT.get(a)
                if hs is None:
                    unknown.add(h)
                    continue
                if as_ is None:
                    unknown.add(a)
                    continue
                flag = "SHIP-as-other" if mode == "po12" else "NOT-COMMISSIONED-L2-internal"
                entry = f"PO_PLAYOFF|{season}|{leg_key}|{leg_date}|{hs}|{hg}|{ag}|{as_}|{extra}|{flag}"
                (po12 if mode == "po12" else po23).append(entry)
            continue

    out = []
    out.extend(tab)
    out.extend(rows)
    out.append("")
    out.append("## PO_PLAYOFF (90-minute doctrine; 1./2. legs SHIP as compType other per ERRATA-2026-08-03;")
    out.append("#  2./3. legs = 2nd/3rd tier internal context only, NOT commissioned)")
    out.extend(po12)
    out.extend(po23)
    out.append("")
    out.append("## TABLE2 (2. Bundesliga final table context; promotion/relegation boundary gate input)")
    out.extend(tab2)
    for r in out:
        print(r)
    counts = {}
    for r in rows:
        k = int(r.split("|")[0][1:])
        counts[k] = counts.get(k, 0) + 1
    print(f"# season {season}: TABLE {len(tab)}, R {len(rows)}, PO12 {len(po12)}, PO23 {len(po23)},"
          f" TABLE2 {len(tab2)}; rounds histogram {sorted(counts.items())}", file=sys.stderr)
    for u in sorted(unknown):
        print(f"# UNKNOWN NAME: {u!r}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
