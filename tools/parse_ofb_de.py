#!/usr/bin/env python3
"""Parse GER openfootball raw transcriptions (data/raw/ofb-de-<season>.txt) into
second-index MD rows on stdout:

  MD<n>|<dateISO>|<homeStock>|<hg>|<ag>|<awayStock>

Formats handled (all transcriptions have renderer escapes already stripped):
  A (2021-22..2023-24): banners '▪ Matchday n' (duplicate banner numbers = postponed
      makeup blocks; rows are summed under the printed n), day headers 'Fri Aug 13'
      (no year), match lines 'Home hg-ag (ht) Away' (optional kickoff time / HT).
  V (2024-25): banners '▪ Matchday n', day headers ' Fri Aug 23 2024' (year optional),
      match lines 'Home v Away hg-ag (ht)' (time optional), one '[awarded]' marker.
  B (2025-26): banners '▪ Regular Season - n' (duplicates = makeups), day headers
      'Fri Aug 22 2025' (year on first banner, then bare), match lines 'Home hg-ag
      (ht) Away', parenthesized scorer lines skipped (any line whose first non-space
      character is '(').
Year roll: explicit year sets it; bare headers inherit; any month-number drop (12 -> 1, or
11 -> 1 across the World Cup winter of the 2022-23 file) bumps the year.
Diagnostics (stderr): parsed vs header match count, per-round histogram, unknowns.
"""
import sys
import re

MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

NAME = {
    "Borussia Mönchengladbach": "Mgladbach", "Borussia M'gladbach": "Mgladbach",
    "FC Bayern München": "Bayern", "VfL Wolfsburg": "Wolfsburg",
    "VfL Bochum 1848": "Bochum", "1. FC Union Berlin": "UnionBerlin",
    "Bayer 04 Leverkusen": "Leverkusen", "VfB Stuttgart": "Stuttgart",
    "SpVgg Greuther Fürth 1903": "GreutherFurth", "FC Augsburg": "Augsburg",
    "TSG 1899 Hoffenheim": "Hoffenheim", "Arminia Bielefeld": "Bielefeld",
    "Borussia Dortmund": "Dortmund", "Eintracht Frankfurt": "Frankfurt",
    "1. FSV Mainz 05": "Mainz", "RB Leipzig": "RBLeipzig",
    "1. FC Köln": "FCKoln", "Hertha BSC": "Hertha", "SC Freiburg": "Freiburg",
    "SV Werder Bremen": "WerderBremen", "FC Schalke 04": "Schalke04",
    "1. FC Heidenheim 1846": "Heidenheim", "SV Darmstadt 98": "Darmstadt",
    "FC St. Pauli 1910": "StPauli", "Holstein Kiel": "HolsteinKiel",
    "Hamburger SV": "Hamburg",
    # 2025-26 short print
    "Heidenheim": "Heidenheim", "Werder Bremen": "WerderBremen",
    "Union Berlin": "UnionBerlin", "Bayer Leverkusen": "Leverkusen",
    "St. Pauli": "StPauli", "Wolfsburg": "Wolfsburg",
}

RE_BANNER = re.compile(r"^▪ (?:Matchday|Regular Season -) (\d+)")
RE_DAY = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})(?: (\d{4}))?\s*$")
RE_INF = re.compile(r"^\s*(?:\d{1,2}:\d{2} )?(.+?) (\d+)-(\d+)(?: \(\d+-\d+\))? (.+?)\s*$")
RE_VST = re.compile(r"^\s*(?:\d{1,2}:\d{2} )?(.+?) v (.+?) (\d+)-(\d+)(?: \(\d+-\d+\))?(?: \[awarded\])?\s*$")
RE_HDR = re.compile(r"^# Matches (\d+)")


def main(path):
    fn = path.split("/")[-1]
    s0 = fn.replace("ofb-de-", "").replace(".txt", "")
    y1 = int(s0[:4])
    year = y1
    prev_month = None
    rnd = None
    day = None
    rows = []
    hdr = None
    unknown = set()
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = RE_HDR.match(line)
        if m:
            hdr = int(m.group(1))
            continue
        m = RE_BANNER.match(line)
        if m:
            rnd = int(m.group(1))
            continue
        m = RE_DAY.match(line)
        if m:
            mon = MON[m.group(1)]
            dd = int(m.group(2))
            yy = m.group(3)
            if yy:
                year = int(yy)
            elif prev_month is not None and mon < prev_month:
                # calendar-year roll inside a season file: Dec->Jan, or Nov->Jan across the
                # 2022 World Cup winter break (2022-23 file has no December headers)
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
                continue
            h, hg, ag, a = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        hs, as_ = NAME.get(h), NAME.get(a)
        if hs is None:
            unknown.add(h)
            continue
        if as_ is None:
            unknown.add(a)
            continue
        rows.append(f"MD{rnd}|{day}|{hs}|{hg}|{ag}|{as_}")
    for r in rows:
        print(r)
    counts = {}
    for r in rows:
        k = int(r.split("|")[0][2:])
        counts[k] = counts.get(k, 0) + 1
    print(f"# parsed {len(rows)} rows; header says {hdr}; rounds histogram {sorted(counts.items())}",
          file=sys.stderr)
    for u in sorted(unknown):
        print(f"# UNKNOWN NAME: {u!r}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
