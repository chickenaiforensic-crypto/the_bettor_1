#!/usr/bin/env python3
"""Parse an SPA RSSSF raw transcription (data/raw/rsssf-span<YYYY>-1sa.txt) into
SPA ledger machine rows on stdout:

  TABLE|<season>|<pos>|<pin>|<P>|<W>|<D>|<L>|<GF>|<GA>|<Pts>|<flags>   La Liga final table (20)
  TABLE2|<season>|<pos>|<name-as-printed>|<P>|<W>|<D>|<L>|<GF>|<GA>|<Pts>|<flags>  Segunda table (22, context)
  R<n>|<dateISO>|<homePin>|<hg>|<ag>|<awayPin>                      league rounds (380)
  ABD|<season>|R<n>|<dateISO>|<homePrint>|<awayPrint>|<note>        abandoned fixture (context; 2023-24 only)
  PO_PLAYOFF|<season>|<leg>|<dateISO>|<homePrint>|<hg>|<ag>|<awayPrint>|<extra>|<flag>
      leg L2-P-SF1/SF2/F1/F2 = Segunda promotion-playoff lines -> NOT-COMMISSIONED-L2-internal
      (lower-tier internal playoffs stay context, ITA Serie B precedent; years 1-3 only)

Skips: header comments, Halfway Table (2022-23/2023-24), duplicate table reprint,
Segunda rounds, RFEF blocks, NB/footer prose. Roster: RSSSF round-print short names
mapped to the WO-pinned 26 strings (Madrid->Real Madrid [wf prints Real Madrid CF],
Atletico->Ath Madrid NEVER Atletico, Athletic->Ath Bilbao NEVER Athletic, Rayo
Vallecano->Vallecano NEVER Rayo, Espanyol->Espanol, Cadiz/Alaves/Almeria/Leganes
ASCII-folded, Sociedad/Betis short).

ABD wrap recovery (2023-24 R16 Granada abd Athletic): the source wraps the bracket note
INTO the next line which opens with an embedded fixture ('Cadiz 1-1 Osasuna   fan due to
cardiac arrest]'). Recovered: fixture ships as its R row; note tail completes the ABD note.
The resumed completion 'Granada 1-1 Athletic [remaining 73'']' (Dec 11) ships as the R16
fixture (annotated context in ABD row + NOTE at pack build).

Gates: 380 R rows, 38 rounds x 10, 20 clubs x 38 apps, date span == season anchors,
GF total == gate anchor (951/955/1005/995), 20 TABLE rows pos 1..20, W*3+D==Pts per row.
"""
import sys
import re

MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

SHORT = {  # RSSSF La Liga round-print short names -> pin (24 round stocks)
    "Madrid": "Real Madrid", "Atlético": "Ath Madrid", "Athletic": "Ath Bilbao",
    "Barcelona": "Barcelona", "Betis": "Betis", "Celta": "Celta", "Cádiz": "Cadiz",
    "Elche": "Elche", "Espanyol": "Espanol", "Getafe": "Getafe", "Girona": "Girona",
    "Granada": "Granada", "Las Palmas": "Las Palmas", "Leganés": "Leganes",
    "Levante": "Levante", "Mallorca": "Mallorca", "Osasuna": "Osasuna",
    "Rayo Vallecano": "Vallecano", "Alavés": "Alaves", "Almería": "Almeria",
    "Oviedo": "Oviedo", "Sociedad": "Sociedad", "Sevilla": "Sevilla",
    "Valencia": "Valencia", "Valladolid": "Valladolid", "Villarreal": "Villarreal",
}

TABLE_NAME = {  # RSSSF La Liga final-table official print -> pin
    "Real Madrid CF": "Real Madrid", "FC Barcelona": "Barcelona",
    "Atlético de Madrid": "Ath Madrid", "Athletic de Bilbao": "Ath Bilbao",
    "Athletic Club (Bilbao)": "Ath Bilbao", "Sevilla FC": "Sevilla",
    "Real Betis Balompié (Sevilla)": "Betis", "Real Betis Balompié": "Betis",
    "Real Sociedad (San Sebastián)": "Sociedad", "Real Sociedad": "Sociedad",
    "Villarreal CF": "Villarreal", "Valencia CF": "Valencia",
    "CA Osasuna (Pamplona)": "Osasuna", "CA Osasuna": "Osasuna",
    "RC Celta (Vigo)": "Celta", "RC Celta de Vigo": "Celta", "RC Celta": "Celta",
    "Rayo Vallecano": "Vallecano", "Elche CF": "Elche",
    "RCD Espanyol (Barcelona)": "Espanol", "RCD Espanyol": "Espanol",
    "Getafe CF": "Getafe", "RCD Mallorca (Palma de M.)": "Mallorca",
    "RCD Mallorca": "Mallorca", "Cádiz CF": "Cadiz", "Granada CF": "Granada",
    "Levante UD (Valencia)": "Levante", "Deportivo Alavés (Vitoria)": "Alaves",
    "UD Almería": "Almeria", "Real Valladolid": "Valladolid", "Girona FC": "Girona",
    "UD Las Palmas": "Las Palmas", "CD Leganés": "Leganes", "Real Oviedo": "Oviedo",
}

RE_ROUND = re.compile(r"^Round (\d+)(?:\s+\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([\d,-]+)\])?\s*$")
RE_DATE = re.compile(r"^\s*\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\]\s*$")
RE_SCORE = re.compile(r"^\s*(.+?) (\d+)-(\d+) (.+?)\s*$")
RE_ABD = re.compile(r"^\s*(.+?) abd (.+?)(?:\s{2,}\[(.*))?$")
RE_ANN = re.compile(r"\s+\[.*$")
RE_TABROW = re.compile(
    r"^\s*(\d+)\.\s*(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)\s*(.*)$")
RE_LEGD = re.compile(
    r"^(First|Second) Legs?(?:\s+\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})\])?\s*$")


def clean_tail(tail):
    t = tail.strip()
    t = re.sub(r"\s+", " ", t)
    t = t.replace("- - - - - - - - - - - - - - - - - - - - - - - - - - - -", "").strip()
    t = re.sub(r"^(-\s*)+", "", t).strip()
    return t


def main(path):
    m = re.search(r"(?:span|rsssf-es-)(\d{4})", path)
    y2 = int(m.group(1))
    y1 = y2 - 1
    season = f"{y1}-{str(y2)[2:]}"

    def iso(mon_name, dd):
        mo = MON[mon_name]
        yy = y1 if mo >= 7 else y2
        return f"{yy:04d}-{mo:02d}-{int(dd):02d}"

    mode = None           # None | table | table2 | rounds | po | skip
    rnd = None
    cur_date = None
    rows, abd, tab, tab2, po, notes = [], [], [], [], [], []
    unknown = set()
    seen_first_table = False
    in_segunda = False
    po_phase = None       # 'SF' | 'F'
    pending_leg = None
    pending_leg_date = None
    pending_abd = None    # [rnd, date, home, away, note]

    def close_abd():
        nonlocal pending_abd
        if pending_abd:
            r0, d0, h0, a0, n0 = pending_abd
            abd.append(f"ABD|{season}|R{r0}|{d0}|{h0}|{a0}|{n0.strip()}")
            pending_abd = None

    def note_restored(hp, ap):
        note = (f"RESTORED-TRANSCRIPTION line shipped as its R{rnd} fixture "
                f"(source line carries my same-day RESTORED disclosure tag verbatim in the raw)")
        notes.append(f"NOTE|{season}|R{rnd}|{hp}|{ap}|{note}")

    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        s = line.strip()
        if not s or (s.startswith("#") and not s.startswith("####")):
            continue  # archive comments skipped; '#### <zone>' markdown headings are content
        if (s.startswith("Primera RFEF") or s.startswith("#### Primera RFEF")
                or s.startswith("#### Primera Federación")):
            in_segunda = False      # RFEF zone: entirely context-only — must NOT emit
            mode = "rfef"
            continue
        if mode == "rfef":
            continue
        if not seen_first_table:
            if s == "Final Table:":
                seen_first_table = True
                mode = "table"
            continue
        if s.startswith("Halfway Table"):
            mode = "halftime"
            continue
        if s.startswith("Segunda División") or s.startswith("#### Segunda"):
            close_abd()
            in_segunda = True
            mode = "seg-prose"
            continue
        if in_segunda and s.endswith("Final Table:"):
            mode = "table2"
            continue
        if mode == "po" and (s == "```" or s.startswith("####")):
            mode = "skip"           # Segunda playoff section closed (fence/zone heading)
            continue
        if s == "Final Table:" and mode != "table" and tab:
            mode = "skipdup"
            continue
        if s.startswith("Promotion Playoff") and in_segunda:
            mode = "po"
            po_phase = None
            continue
        if mode == "po":
            if s in ("Semifinals", "Semifinals:"):
                po_phase = "SF"
                continue
            if s in ("Final", "Final:"):
                po_phase = "F"
                continue
            ml = RE_LEGD.match(s)
            if ml:
                pending_leg = f"L2-P-{po_phase}{1 if ml.group(1) == 'First' else 2}"
                pending_leg_date = None
                if ml.group(2):
                    pending_leg_date = iso(ml.group(2), ml.group(3))
                continue
            md0 = RE_DATE.match(s)
            if md0:
                pending_leg_date = iso(md0.group(1), md0.group(2))
                continue
            msc = RE_SCORE.match(s)
            if msc and pending_leg:
                home, hg, ag, away_t = msc.group(1).strip(), msc.group(2), msc.group(3), msc.group(4)
                extra = ""
                an = re.search(r"\s{2,}\[(.*?)\]\s*$", away_t)
                if an:
                    extra = an.group(1)
                    away_t = away_t[: an.start()].strip()
                away_t = RE_ANN.sub("", away_t).strip()
                po.append(f"PO_PLAYOFF|{season}|{pending_leg}|{pending_leg_date}|{home}|{hg}|{ag}|"
                          f"{away_t}|{extra}|NOT-COMMISSIONED-L2-internal")
                continue
            if s == "```":
                mode = "skip"
                continue
        m2 = RE_ROUND.match(s)
        if m2 and not in_segunda:
            mode = "rounds"
            rnd = int(m2.group(1))
            if m2.group(2):
                cur_date = iso(m2.group(2), m2.group(3).split(",")[0])
            continue
        if mode == "table":
            m2 = RE_TABROW.match(line)
            if m2:
                pos, name = int(m2.group(1)), m2.group(2).strip()
                p, w, d, l = (int(m2.group(i)) for i in (3, 4, 5, 6))
                gf, ga, pts = int(m2.group(7)), int(m2.group(8)), int(m2.group(9))
                flags = clean_tail(m2.group(10))
                if name.startswith("-"):
                    continue
                st = TABLE_NAME.get(name)
                if st is None:
                    unknown.add("TABLE:" + name)
                    continue
                tab.append((pos, st, p, w, d, l, gf, ga, pts, flags))
                continue
        if mode == "table2":
            m2 = RE_TABROW.match(line)
            if m2:
                pos, name = int(m2.group(1)), m2.group(2).strip()
                p, w, d, l = (int(m2.group(i)) for i in (3, 4, 5, 6))
                gf, ga, pts = int(m2.group(7)), int(m2.group(8)), int(m2.group(9))
                flags = clean_tail(m2.group(10))
                if name.startswith("-"):
                    continue
                tab2.append((pos, name, p, w, d, l, gf, ga, pts, flags))
                continue
            if tab2 and len(tab2) >= 22:
                mode = "skip"
                continue
        if mode != "rounds":
            continue
        md = RE_DATE.match(s)
        if md:
            cur_date = iso(md.group(1), md.group(2))
            continue
        # ABD wrap: an open abd note gets its tail from this line (embedded fixture or not)
        if pending_abd:
            emb = RE_SCORE.match(s)
            tail_used = None
            if emb and emb.group(4):
                # split away token: first known SHORT name, remainder = abd note tail
                toks = emb.group(4)
                for cand in sorted(SHORT, key=len, reverse=True):
                    if toks == cand or toks.startswith(cand + " "):
                        tail_used = toks[len(cand):].strip()
                        break
            if tail_used:
                if pending_abd[4].endswith("\\"):
                    pending_abd[4] = pending_abd[4][:-1]  # archive line-wrap marker, not content
                pending_abd[4] += " " + tail_used
                close_abd()
                hpin, apin = SHORT.get(emb.group(1)), SHORT.get(emb.group(4).split("  ")[0].split(" [")[0])
                # fixture ships below through the normal R-row path
                line = f"{emb.group(1)} {emb.group(2)}-{emb.group(3)} {toks[:len(toks) - len(' ' + tail_used) if tail_used else len(toks)]}"
                s = line.strip()
            else:
                pending_abd[4] += " " + s
                if "]" in s:
                    close_abd()
                continue
        mab = RE_ABD.match(s)
        # home token must be a known SHORT name — a scored fixture whose trailing
        # bracketed disclosure note merely CONTAINS the word "abd" is not an abandonment
        if mab and mab.group(1).strip() in SHORT and " abd " in f" {s} ":
            home, away = mab.group(1).strip(), mab.group(2).strip()
            note = (mab.group(3) or "").strip()
            full = f"[{note}" if note else "["
            if note.endswith("]"):
                abd.append(f"ABD|{season}|R{rnd}|{cur_date}|{home}|{away}|{note}")
            else:
                pending_abd = [rnd, cur_date, home, away, full]
            continue
        m2 = RE_SCORE.match(line)
        if not m2:
            continue
        home, hg, ag = m2.group(1).strip(), m2.group(2), m2.group(3)
        restored = "RESTORED" in m2.group(4)
        away_t = RE_ANN.sub("", m2.group(4)).strip()
        hpin, apin = SHORT.get(home), SHORT.get(away_t)
        if hpin is None:
            unknown.add("H:" + home)
            continue
        if apin is None:
            unknown.add("A:" + away_t)
            continue
        rows.append((rnd, cur_date, hpin, int(hg), int(ag), apin))
        if restored:
            note_restored(hpin, apin)
    close_abd()

    # gates
    from collections import Counter
    cnt = Counter(r[0] for r in rows)
    apps = Counter()
    goals = 0
    for _, _, h, hg, ag, a in rows:
        apps[h] += 1
        apps[a] += 1
        goals += hg + ag
    dates = [r[1] for r in rows]
    GATE = {2022: ("2021-08-13", "2022-05-22", 951), 2023: ("2022-08-12", "2023-06-04", 955),
            2024: ("2023-08-11", "2024-05-26", 1005), 2025: ("2024-08-15", "2025-05-25", 995)}
    d0, d1, gf_gate = GATE[y2]
    errs = []
    if len(rows) != 380:
        errs.append(f"rows={len(rows)}")
    if len(cnt) != 38 or any(v != 10 for v in cnt.values()):
        errs.append("histogram")
    if len(apps) != 20 or any(v != 38 for v in apps.values()):
        errs.append(f"apps={ {k: v for k, v in apps.items() if v != 38} }")
    if min(dates) != d0 or max(dates) != d1:
        errs.append(f"span={min(dates)}..{max(dates)}")
    if goals != gf_gate:
        errs.append(f"GF={goals}")
    if len(tab) != 20 or [t[0] for t in tab] != list(range(1, 21)):
        errs.append(f"table={len(tab)}")
    for t in tab:
        if t[3] * 3 + t[4] != t[8]:
            errs.append(f"ptsrow {t[1]}")
    if unknown:
        errs.append(f"unknown={sorted(unknown)[:8]}")
    print(f"# season {season}: R rows {len(rows)}, rounds {len(cnt)}, TABLE {len(tab)}, "
          f"TABLE2 {len(tab2)}, ABD {len(abd)}, PO {len(po)}, GF {goals}, "
          f"span {min(dates) if dates else '-'}..{max(dates) if dates else '-'}", file=sys.stderr)
    if errs:
        print("# GATE FAIL: " + "; ".join(errs), file=sys.stderr)
        sys.exit(1)
    for t in tab:
        print(f"TABLE|{season}|{t[0]}|{t[1]}|{t[2]}|{t[3]}|{t[4]}|{t[5]}|{t[6]}|{t[7]}|{t[8]}|{t[9]}")
    for t in tab2:
        print(f"TABLE2|{season}|{t[0]}|{t[1]}|{t[2]}|{t[3]}|{t[4]}|{t[5]}|{t[6]}|{t[7]}|{t[8]}|{t[9]}")
    for r in rows:
        print(f"R{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}|{r[5]}")
    for row in abd:
        print(row)
    for row in po:
        print(row)
    for row in notes:
        print(row)


if __name__ == "__main__":
    main(sys.argv[1])
