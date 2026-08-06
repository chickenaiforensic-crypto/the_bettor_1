#!/usr/bin/env python3
"""Parse ITA openfootball raw transcriptions (data/raw/ofb-it-<season>.txt) into
second-index MD rows on stdout:

  MD<n>|<dateISO>|<homeStock>|<hg>|<ag>|<awayStock>

Formats handled (transcriptions have renderer escapes stripped):
  A (2021-22..2024-25): banners '▪ Matchday n' (a duplicate banner number = a postponed
      makeup block; rows are summed under the printed n), day headers 'Sat Aug 13 2022'
      (year on first banner, then optional/bare), match lines 'Home hg-ag (ht) Away'
      optional kickoff time / HT; some seasons print 'Home v Away hg-ag'.
  B (2025-26): banners '▪ Regular Season - n' (duplicates = makeups), day headers
      'Sat Aug 23 2025' style, scorer lines skipped (any line whose first non-space
      character is '('), HT lines '(1-0)' tolerated after the score.
Year roll: explicit year sets it; bare headers inherit; any month-number drop bumps the year.
Diagnostics (stderr): parsed vs header match count, per-round histogram, unknowns.
"""
import sys
import re

MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

NAME = {
    "AC Milan": "Milan", "Milan": "Milan",
    "FC Internazionale Milano": "Inter", "Inter": "Inter", "Inter Milan": "Inter",
    "SSC Napoli": "Napoli", "Napoli": "Napoli",
    "Juventus FC": "Juventus", "Juventus": "Juventus",
    "SS Lazio": "Lazio", "Lazio": "Lazio",
    "AS Roma": "Roma", "Roma": "Roma",
    "ACF Fiorentina": "Fiorentina", "AC Fiorentina": "Fiorentina", "Fiorentina": "Fiorentina",
    "Atalanta BC": "Atalanta", "Atalanta": "Atalanta",
    "Hellas Verona FC": "Verona", "Hellas Verona": "Verona", "Verona": "Verona",
    "Torino FC": "Torino", "Torino": "Torino",
    "US Sassuolo Calcio": "Sassuolo", "US Sassuolo": "Sassuolo", "Sassuolo": "Sassuolo",
    "Udinese Calcio": "Udinese", "Udinese": "Udinese",
    "Bologna FC 1909": "Bologna", "Bologna FC": "Bologna", "Bologna": "Bologna",
    "Empoli FC": "Empoli", "Empoli": "Empoli",
    "UC Sampdoria": "Sampdoria", "Sampdoria": "Sampdoria",
    "Spezia Calcio": "Spezia", "Spezia": "Spezia",
    "US Salernitana 1919": "Salernitana", "Salernitana": "Salernitana",
    "Cagliari Calcio": "Cagliari", "Cagliari": "Cagliari",
    "Genoa CFC": "Genoa", "Genoa": "Genoa",
    "Venezia FC": "Venezia", "Venezia": "Venezia",
    "AC Monza": "Monza", "Monza": "Monza",
    "US Cremonese": "Cremonese", "Cremonese": "Cremonese",
    "US Lecce": "Lecce", "Lecce": "Lecce",
    "Frosinone Calcio": "Frosinone", "Frosinone": "Frosinone",
    "Parma Calcio 1913": "Parma", "Parma Calcio": "Parma", "Parma": "Parma",
    "Como 1907": "Como", "Como": "Como",
    "AC Pisa": "Pisa", "Pisa": "Pisa", "Pisa SC": "Pisa",
}

RE_BANNER = re.compile(r"^▪ (?:Matchday|Regular Season -) (\d+)")
RE_DAY = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})(?: (\d{4}))?\s*$")
RE_INF = re.compile(r"^\s*(?:\d{1,2}:\d{2}\s+)?(.+?) (\d+)-(\d+)(?: \(\d+-\d+\))? (.+?)\s*$")
RE_VST = re.compile(r"^\s*(?:\d{1,2}:\d{2}\s+)?(.+?) v (.+?) (\d+)-(\d+)(?: \(\d+-\d+\))?(?: \[[^\]]*\])?\s*$")
RE_HDR = re.compile(r"^# Matches\s+(\d+)")


def parse(path):
    fn = path.split("/")[-1]
    s0 = fn.replace("ofb-it-", "").replace(".txt", "")
    y1 = int(s0[:4])
    year = y1
    prev_month = None
    rnd = None
    day = None
    rows = []
    hdr = None
    unknown = set()
    dup_banner = {}
    defects = []
    for nln, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        m = RE_HDR.match(line)
        if m:
            hdr = int(m.group(1))
            continue
        m = RE_BANNER.match(line)
        if m:
            rnd = int(m.group(1))
            dup_banner[rnd] = dup_banner.get(rnd, 0) + 1
            continue
        m = RE_DAY.match(line)
        if m:
            mon = MON[m.group(1)]
            dd = int(m.group(2))
            yy = m.group(3)
            if yy:
                year = int(yy)
            elif prev_month is not None and mon < prev_month:
                year += 1
            prev_month = mon
            day = f"{year:04d}-{mon:02d}-{dd:02d}"
            continue
        s = line.lstrip()
        if not s or s.startswith("(") or s.startswith("#") or s.startswith("="):
            continue
        if rnd is None or day is None:
            continue
        m = RE_VST.match(line)
        if m:
            h, a, hg, ag = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        else:
            m = RE_INF.match(line)
            if not m:
                if re.search(r"(?:[A-Z][A-Za-z]+\s+)*[A-Z][A-Za-z]+\s+\d{1,2}:\d{2}\s+", line) or \
                   (re.search(r"\S", line) and re.search(r"[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ ", line)
                    and "\n" not in line and re.search(r"\d+-\d+", line) is None and len(line) > 40):
                    defects.append((nln, line))
                continue
            h, hg, ag, a = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        h = re.sub(r"\s+", " ", h.strip())
        a = re.sub(r"\s+", " ", a.strip())
        hs, as_ = NAME.get(h), NAME.get(a)
        if hs is None:
            unknown.add(h)
            continue
        if as_ is None:
            unknown.add(a)
            continue
        rows.append(f"MD{rnd}|{day}|{hs}|{hg}|{ag}|{as_}")
    return rows, hdr, counts_histogram(rows), sorted(k for k, v in dup_banner.items() if v > 1), defects, sorted(unknown)


def counts_histogram(rows):
    counts = {}
    for r in rows:
        k = int(r.split("|")[0][2:])
        counts[k] = counts.get(k, 0) + 1
    return sorted(counts.items())


def main(path):
    rows, hdr, hist, dups, defects, unknown = parse(path)
    for r in rows:
        print(r)
    print(f"# parsed {len(rows)} rows; header says {hdr}; rounds histogram {hist}",
          file=sys.stderr)
    if hdr is not None and hdr != len(rows):
        print(f"# HEADER-COUNT MISMATCH: parsed {len(rows)} != header {hdr}", file=sys.stderr)
    for ln, txt in defects:
        print(f"# DEFECT-SUSPECT line {ln}: {txt[:90]!r}", file=sys.stderr)
    if dups:
        print(f"# duplicate banners (makeup blocks summed under banner): {dups}", file=sys.stderr)
    for u in unknown:
        print(f"# UNKNOWN NAME: {u!r}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
