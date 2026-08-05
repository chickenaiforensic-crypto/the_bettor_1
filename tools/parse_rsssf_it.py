#!/usr/bin/env python3
"""Parse an ITA RSSSF raw transcription (data/raw/rsssf-ital<YYYY>-1sa.txt) into
ITA ledger machine rows on stdout:

  TABLE|<season>|<pos>|<stock>|<P>|<W>|<D>|<L>|<GF>|<GA>|<Pts>|<flags>   Serie A final table (20)
  TABLE2|<season>|<pos>|<name-as-printed>|<P>|<W>|<D>|<L>|<GF>|<GA>|<Pts>|<flags>  Serie B table (20)
  R<n>|<dateISO>|<homeStock>|<hg>|<ag>|<awayStock>                      league rounds (380; none for 2025-26)
  ABD|<season>|R<n>|<dateISO>|<home>|<away>|<note>                      abandoned-then-RESUMED fixture (context)
  PO_PLAYOFF|<season>|<leg>|<dateISO>|<home>|<hg>|<ag>|<away>|<extra>|<flag>[|<NB>]
      leg Retro-1  = Serie A spareggio retrocessione decider -> SHIP-as-other (ERRATA)
      leg L2-P...  = Serie B promotion playoff lines        -> NOT-COMMISSIONED-L2-internal
      leg L2-R...  = Serie B relegation playoff lines       -> NOT-COMMISSIONED-L2-internal

Skips: header comments, the "Halfway Table" context blocks (2022-23 / 2023-24 prints),
Coppa Italia, NB prose, the mid-round standings/cap-leader prose fragments that some
prints carry. Round section absent (ital2026) -> zero R rows.

Bracket/H2H notes in the table print: trailing "[...]" groups are kept in flags; the
"[...]  Relegated" tail is normalised. The "[-10]" deduction print for Juventus 2022-23
stays in flags; the builder subtracts it in the reproduction gate.
"""
import sys
import re

MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

SHORT = {  # RSSSF Serie A round-print short names -> stock (27 league stocks)
    "Milan": "Milan", "Inter": "Inter", "Napoli": "Napoli", "Juventus": "Juventus",
    "Lazio": "Lazio", "Roma": "Roma", "Fiorentina": "Fiorentina", "Atalanta": "Atalanta",
    "Hellas Verona": "Verona", "Verona": "Verona", "Torino": "Torino",
    "Sassuolo": "Sassuolo", "Udinese": "Udinese", "Bologna": "Bologna",
    "Empoli": "Empoli", "Sampdoria": "Sampdoria", "Spezia": "Spezia",
    "Salernitana": "Salernitana", "Cagliari": "Cagliari", "Genoa": "Genoa",
    "Venezia": "Venezia", "Monza": "Monza", "Cremonese": "Cremonese",
    "Lecce": "Lecce", "Frosinone": "Frosinone", "Parma": "Parma", "Como": "Como",
    "Pisa": "Pisa",
}

TABLE_NAME = {  # RSSSF Serie A final-table official print -> stock
    "Milan AC": "Milan", "AC Milan": "Milan", "Milan": "Milan",
    "FC Internazionale": "Inter", "Inter Milan": "Inter", "Inter": "Inter",
    "SSC Napoli": "Napoli", "Napoli": "Napoli",
    "Juventus FC": "Juventus", "Juventus": "Juventus",
    "SS Lazio": "Lazio", "Lazio": "Lazio",
    "AS Roma": "Roma", "Roma": "Roma",
    "AC Fiorentina": "Fiorentina", "ACF Fiorentina": "Fiorentina", "Fiorentina": "Fiorentina",
    "Atalanta BC": "Atalanta", "Atalanta": "Atalanta",
    "Hellas Verona FC": "Verona", "Hellas Verona": "Verona", "Verona": "Verona",
    "Torino FC": "Torino", "Torino": "Torino",
    "US Sassuolo": "Sassuolo", "US Sassuolo Calcio": "Sassuolo", "Sassuolo": "Sassuolo",
    "Udinese Calcio": "Udinese", "Udinese": "Udinese",
    "Bologna FC": "Bologna", "Bologna FC 1909": "Bologna", "Bologna": "Bologna",
    "Empoli FC": "Empoli", "Empoli": "Empoli",
    "UC Sampdoria": "Sampdoria", "Sampdoria": "Sampdoria",
    "Spezia Calcio": "Spezia", "Spezia": "Spezia",
    "US Salernitana 1919": "Salernitana", "US Salernitana": "Salernitana",
    "Salernitana": "Salernitana",
    "Cagliari Calcio": "Cagliari", "Cagliari": "Cagliari",
    "Genoa CFC": "Genoa", "Genoa": "Genoa",
    "Venezia FC": "Venezia", "Venezia": "Venezia",
    "AC Monza": "Monza", "Monza": "Monza",
    "US Cremonese": "Cremonese", "Cremonese": "Cremonese",
    "US Lecce": "Lecce", "Lecce": "Lecce",
    "Frosinone Calcio": "Frosinone", "Frosinone": "Frosinone",
    "Parma Calcio": "Parma", "Parma": "Parma",
    "Como 1907": "Como", "Como": "Como",
    "AC Pisa": "Pisa", "Pisa": "Pisa",
}

RE_ROUND = re.compile(r"^Round (\d+)(?:\s+\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([\d,-]+)\])?\s*$")
RE_DATE = re.compile(r"^\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\]\s*$")
RE_SCORE = re.compile(r"^\s*(.+?) (\d+)-(\d+) (.+?)\s*$")
RE_ABD = re.compile(r"^\s*(.+?) abd (.+?)\s*(?:\[(.*)\])?\s*$")
RE_ANN = re.compile(r"\s+\[.*$")
RE_TABROW = re.compile(
    r"^\s*(\d+)\.\s*(.+?)\s{2,}(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)\s*(.*)$")
RE_LEG = re.compile(
    r"^(First|Second) Leg(?:\s+\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\])?\s*$")


def clean_tail(tail):
    t = tail.strip()
    t = re.sub(r"\s+", " ", t)
    t = t.replace("- - - - - - - - - - - - - - - - - - - - - - - - - - - -", "").strip()
    t = re.sub(r"^(-\s*)+", "", t).strip()
    return t


def main(path):
    m = re.search(r"ital(\d{4})", path)
    y2 = int(m.group(1))
    y1 = y2 - 1
    season = f"{y1}-{str(y2)[2:]}"

    def iso(mon_name, dd):
        mo = MON[mon_name]
        yy = y1 if mo >= 7 else y2
        return f"{yy:04d}-{mo:02d}-{int(dd):02d}"

    mode = None
    rnd = None
    cur_date = None
    rows, abd, tab, tab2, po = [], [], [], [], []
    unknown = set()
    seen_first_table = False
    in_serieb = False
    po_zone = None      # None | 'retro' | 'l2promo' | 'l2rel'
    pending_po_date = None
    pending_leg = None

    def emit_po(leg, date_iso, line):
        m2 = RE_SCORE.match(line)
        if not m2:
            return
        extra = ""
        away_tok = m2.group(4)
        an = re.search(r"\s{2,}\[(.*?)\]\s*$", away_tok)
        if an:
            extra = an.group(1)
            away_tok = away_tok[: an.start()].strip()
        away_tok = RE_ANN.sub("", away_tok).strip()
        fl = "SHIP-as-other" if leg.startswith("Retro") else "NOT-COMMISSIONED-L2-internal"
        po.append(f"PO_PLAYOFF|{season}|{leg}|{date_iso}|{m2.group(1).strip()}|{m2.group(2)}|"
                  f"{m2.group(3)}|{away_tok}|{extra}|{fl}")

    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        s = line.strip()
        if not s:
            continue
        if not seen_first_table:
            if s in ("Final Table:", "Serie A Final Table:"):
                seen_first_table = True
                mode = "table"
            continue
        if s.startswith("Halfway Table"):
            mode = "halftime"
            continue
        if s in ("Final Table:", "Serie A Final Table:") and mode != "table" and not tab:
            mode = "table"
            continue
        if s.startswith("Serie B") or s.startswith("#### Serie B") or s == "Serie B Final Table:":
            in_serieb = True
            if s == "Serie B Final Table:":
                mode = "table2"
            else:
                mode = "serieb-prose"
            continue
        if in_serieb and s.endswith("Final Table:"):
            mode = "table2"
            continue
        if s.startswith("Promotion Playoff") and in_serieb:
            mode = "po"
            po_zone = "l2promo"
            pending_leg = "L2-P"
            continue
        if s.startswith("Relegation Playoff") and (in_serieb or po_zone == "l2promo"):
            mode = "po"
            po_zone = "l2rel"
            pending_leg = "L2-R"
            continue
        if s.startswith("Spareggio"):
            mode = "po"
            po_zone = "retro"
            pending_leg = "Retro-1"
            continue
        if s.startswith("Semifinals") and mode == "po":
            continue
        if s.startswith("Final") and mode == "po" and not RE_TABROW.match(s):
            continue
        if s.startswith("Round") and mode == "po":
            pending_po_date = None
            pending_leg = None
            continue
        if s.startswith("Coppa Italia") or s.startswith("#### Coppa"):
            mode = "coppa"
            continue
        m2 = RE_ROUND.match(s)
        if m2 and not in_serieb and mode != "coppa":
            if mode in ("table", "halftime", None, "rounds"):
                mode = "rounds"
                if mode != "halftime":
                    rnd = int(m2.group(1))
                    if m2.group(2):
                        cur_date = iso(m2.group(2), m2.group(3).split(",")[0])
            continue
        if mode in ("halftime", "coppa", "serieb-prose"):
            continue
        if s.startswith("NB:") or s.startswith("- ") or s.startswith("---"):
            continue
        if s.startswith("Verified:"):
            continue
        if mode in ("table", "table2"):
            m2 = RE_TABROW.match(line)
            if m2:
                pos, name = int(m2.group(1)), m2.group(2).strip()
                p, w, d, l = (int(m2.group(i)) for i in (3, 4, 5, 6))
                gf, ga, pts = int(m2.group(7)), int(m2.group(8)), int(m2.group(9))
                flags = clean_tail(m2.group(10))
                if not name or name.startswith("-"):
                    continue
                if mode == "table":
                    st = TABLE_NAME.get(name)
                    if st is None:
                        unknown.add("TABLE:" + name)
                        continue
                    tab.append(f"TABLE|{season}|{pos}|{st}|{p}|{w}|{d}|{l}|{gf}|{ga}|{pts}|{flags}")
                else:
                    tab2.append(f"TABLE2|{season}|{pos}|{name}|{p}|{w}|{d}|{l}|{gf}|{ga}|{pts}|{flags}")
            continue
        if mode == "po":
            md = RE_DATE.match(s)
            if md:
                pending_po_date = iso(md.group(1), md.group(2))
                continue
            one = re.match(r"^(.+?)\s+\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})(?:,\s*([^\]]+))?\]\s*$", s)
            if one and po_zone == "retro":
                city = (one.group(4) or "").strip()
                emit_po("Retro-1" + (f"({city})" if city else ""), iso(one.group(2), one.group(3)), one.group(1))
                pending_po_date = None
                continue
            ml = RE_LEG.match(s)
            if ml:
                if ml.group(2):
                    pending_po_date = iso(ml.group(2), ml.group(3))
                pending_leg = ("Retro-1" if ml.group(1) == "First" else "Retro-2") if po_zone == "retro" \
                    else ({"l2promo": "L2-P", "l2rel": "L2-R"}.get(po_zone, "L2-?"))
                continue
            if pending_po_date:
                eff = pending_leg if isinstance(pending_leg, str) else \
                    {"l2promo": "L2-P", "l2rel": "L2-R", "retro": "Retro-1"}.get(po_zone, "L2-?")
                if eff.startswith("Retro") and "-" in eff:
                    emit_po(eff, pending_po_date, line)
                else:
                    n = sum(1 for p in po if p.split("|")[2].startswith(eff))
                    emit_po(f"{eff}{n + 1}", pending_po_date, line)
            continue
        if mode == "rounds" and rnd:
            md = RE_DATE.match(s)
            if md:
                cur_date = iso(md.group(1), md.group(2))
                continue
            ma = RE_ABD.match(line)
            if ma:
                note = (ma.group(3) or "").strip()
                abd.append(f"ABD|{season}|R{rnd}|{cur_date}|{ma.group(1).strip()}|"
                           f"{ma.group(2).strip()}|{note}")
                continue
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

    out = []
    out.extend(tab)
    out.extend(rows)
    if abd:
        out.append("")
        out.append("## ABD (abandoned-then-RESUMED fixtures; the completion rows ship inside the round,")
        out.append("#  the original-date lines are context only; 90-minute/standing doctrine)")
        out.extend(abd)
    out.append("")
    out.append("## PO_PLAYOFF (spareggio retrocessione SHIP as compType other per ERRATA-2026-08-03;")
    out.append("#  Serie B promotion/relegation playoffs = tier-internal context, NOT commissioned)")
    out.extend(po)
    out.append("")
    out.append("## TABLE2 (Serie B final table context; promotion/relegation boundary gate input)")
    out.extend(tab2)
    for r in out:
        print(r)
    counts = {}
    for r in rows:
        k = int(r.split("|")[0][1:])
        counts[k] = counts.get(k, 0) + 1
    print(f"# season {season}: TABLE {len(tab)}, R {len(rows)}, ABD {len(abd)}, PO {len(po)},"
          f" TABLE2 {len(tab2)}; rounds histogram {sorted(counts.items())}", file=sys.stderr)
    for u in sorted(unknown):
        print(f"# UNKNOWN NAME: {u!r}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
