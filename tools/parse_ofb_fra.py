#!/usr/bin/env python3
"""Parse openfootball/europe france <season>_fr1.txt -> MD rows for the FRA second index.

Output rows (stdout): MD<n>|<dateISO>|<homeStock>|<hg>|<ag>|<awayStock>
Diagnostics on stderr: parsed vs header match count, per-round counts, unknown names.

Formats handled:
  A (2021-22..2024-25): banners '▪ Matchday n', day headers ' Sat Aug 7 [2021]',
      match lines ' 21:00 Home v Away FT (HT)' (time optional; FT may be missing HT part).
  B (2025-26): banners '▪ Regular Season - n' (duplicated banner numbers reused for
      postponed strays - assigned to their printed round), day headers 'Sat Aug 16',
      match lines ' 20:45 Home FT (HT) Away' followed by a scorers line in parens.
Year roll: explicit year on some banners; bare banners inherit; a bare month drop
      12 -> 1 bumps the year (all season boundary banners here carry explicit years).
"""
import sys
import re

MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

NAME = {
    "AS Monaco": "Monaco", "AS Monaco FC": "Monaco",
    "FC Nantes": "Nantes",
    "Olympique Lyonnais": "Lyon",
    "Stade Brestois 29": "Brest", "Stade Brestois": "Brest",
    "ESTAC Troyes": "Troyes",
    "Paris Saint-Germain": "ParisSG", "Paris Saint-Germain FC": "ParisSG",
    "Stade Rennais": "Rennes", "Stade Rennais FC 1901": "Rennes", "Rennes": "Rennes",
    "RC Lens": "Lens", "Racing Club de Lens": "Lens", "Lens": "Lens",
    "AS Saint-Étienne": "SaintEtienne",
    "FC Lorient": "Lorient",
    "Girondins Bordeaux": "Bordeaux",
    "Clermont Foot 63": "Clermont",
    "OGC Nice": "Nice",
    "Stade de Reims": "Reims",
    "RC Strasbourg": "Strasbourg", "RC Strasbourg Alsace": "Strasbourg",
    "Angers SCO": "Angers",
    "FC Metz": "Metz",
    "Lille OSC": "Lille", "Lille": "Lille",
    "Montpellier HSC": "Montpellier",
    "Olympique Marseille": "Marseille", "Olympique de Marseille": "Marseille",
    "AC Ajaccio": "Ajaccio",
    "AJ Auxerre": "Auxerre", "Auxerre": "Auxerre",
    "Toulouse FC": "Toulouse",
    "Le Havre AC": "LeHavre", "Le Havre": "LeHavre",
    "Paris FC": "ParisFC",
}

RE_BANNER_A = re.compile(r"^▪ Matchday (\d+)\s*$")
RE_BANNER_B = re.compile(r"^▪ Regular Season - (\d+)\s*$")
RE_DAY = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})(?: (\d{4}))?\s*$")
RE_MATCH_A = re.compile(r"^\s*(?:\d{1,2}:\d{2} )?(.+?) v (.+?) (\d+)-(\d+)(?: \(\d+-\d+\))?(?: \\\[awarded\\\])?\s*$")
RE_MATCH_B = re.compile(r"^\s*\d{1,2}:\d{2} (.+?) (\d+)-(\d+) \(\d+-\d+\) (.+?)\s*$")
RE_MATCH_B_NOHT = re.compile(r"^\s*\d{1,2}:\d{2} (.+?) (\d+)-(\d+) (.+?)\s*$")
RE_HEADER_MATCHES = re.compile(r"^\\# Matches (\d+)")


def main(path):
    year = None
    prev_month = None
    rnd = None
    day = None
    rows = []
    hdr = None
    unknown = set()
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = RE_HEADER_MATCHES.match(line)
        if m:
            hdr = int(m.group(1))
            continue
        m = RE_BANNER_A.match(line) or RE_BANNER_B.match(line)
        if m:
            rnd = int(m.group(1))
            continue
        m = RE_DAY.match(line)
        if m:
            mon = MONTHS[m.group(1)]
            dd = int(m.group(2))
            yy = m.group(3)
            if yy:
                year = int(yy)
            elif prev_month and mon < prev_month and prev_month == 12 and mon == 1:
                year += 1
            prev_month = mon
            day = f"{year:04d}-{mon:02d}-{dd:02d}"
            continue
        if rnd is None or day is None:
            continue
        if " v " in line:
            m = RE_MATCH_A.match(line)
            if not m:
                continue
            h, a, hg, ag = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        else:
            m = RE_MATCH_B.match(line)
            if m:
                h, hg, ag, a = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            else:
                m = RE_MATCH_B_NOHT.match(line)
                if not m:
                    continue
                h, hg, ag, a = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        hs = NAME.get(h)
        as_ = NAME.get(a)
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
    print(f"# parsed {len(rows)} rows; header says {hdr}; rounds {sorted(counts.items())}", file=sys.stderr)
    for u in sorted(unknown):
        print(f"# UNKNOWN NAME: {u!r}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
