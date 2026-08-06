#!/usr/bin/env python3
"""Parse SPA openfootball raw transcriptions (data/raw/ofb-es-<season>.txt) into
second-index MD rows on stdout:

  MD<n>|<dateISO>|<homePin>|<hg>|<ag>|<awayPin>

Mirrors tools/parse_ofb_it.py. Formats handled:
  A (2021-22..2023-24): banners '▪ Matchday n', day headers 'Fri Aug 13' (year on the
      first header of the file only or not at all -> --start-year), match lines
      'HH:MM Home hg-ag (ht) Away' (short names incl. 'Real Madrid C.F.').
  B (2024-25): banners '▪ Matchday n', long-name v-format
      'HH:MM Home v Away hg-ag (ht)'  ('Real Sociedad de Fútbol v Rayo Vallecano de Madrid').
  C (2025-26): banners '▪ Regular Season - n' (non-monotonic block order, documented in
      the raw header: RS-6 before RS-3, RS-19 before RS-15, RS-16 makeup, RS-23 makeup
      fragment, RS-33 before RS-32), day headers 'Fri Aug 15 2025' (year on first),
      short-name inf format.
Duplicate banner number = a postponed/makeup block; rows are summed under the printed n
(ITA 2025-26 precedent). gate: 380 rows, 38 rounds x 10 after summing, 20 clubs x 38 apps.
Bracketed audit tags appended to fixture lines in the raws ([SPLICED...], [SOURCE-TOKEN...],
[TRANSCRIPTION-REPAIR...], [splice marker...]) are stripped before name matching - their
disclosures live in the raw headers and are echoed into the ledger headers by the caller.
Scorer lines (first non-space char '(') skipped. HT parens after the score tolerated.
Unknown-name tolerance 0: every name hit must map to one of the 26 roster pins.

Usage: python3 tools/parse_ofb_es.py <raw> <seasonLabel> <startYear>
"""
import sys
import re
from collections import Counter

MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
       "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

NAME = {
    "Athletic Club": "Ath Bilbao",
    "Atlético de Madrid": "Ath Madrid", "Club Atlético de Madrid": "Ath Madrid",
    "Atlético Madrid": "Ath Madrid",
    "Barcelona": "Barcelona", "FC Barcelona": "Barcelona",
    "CA Osasuna": "Osasuna", "Osasuna": "Osasuna",
    "Cádiz CF": "Cadiz",
    "Deportivo Alavés": "Alaves",
    "Elche CF": "Elche",
    "Getafe CF": "Getafe",
    "Girona FC": "Girona", "Girona CF": "Girona",  # GF->FC upstream token, raw-header disclosed
    "Granada CF": "Granada",
    "Levante UD": "Levante",
    "RC Celta": "Celta", "RC Celta de Vigo": "Celta", "Celta Vigo": "Celta",
    "RCD Espanyol": "Espanol", "RCD Espanyol de Barcelona": "Espanol",
    "RCD Mallorca": "Mallorca",
    "Rayo Vallecano": "Vallecano", "Rayo Vallecano de Madrid": "Vallecano",
    "Real Betis": "Betis", "Real Betis Balompié": "Betis",
    "Real Madrid C.F.": "Real Madrid", "Real Madrid CF": "Real Madrid",
    "Real Oviedo": "Oviedo",
    "Real Sociedad": "Sociedad", "Real Sociedad de Fútbol": "Sociedad",
    "Real Valladolid CF": "Valladolid", "Real Valladolid": "Valladolid",
    "Sevilla": "Sevilla", "Sevilla CF": "Sevilla", "Sevilla FC": "Sevilla",  # CF token, disclosed
    "UD Almería": "Almeria",
    "UD Las Palmas": "Las Palmas",
    "CD Leganés": "Leganes",
    "Valencia CF": "Valencia", "Valencia": "Valencia",
    "Villarreal": "Villarreal", "Villarreal CF": "Villarreal",
}

RE_BANNER = re.compile(r"^▪ (?:Matchday|Regular Season -) (\d+)")
RE_DAY = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2})(?: (\d{4}))?\s*$")
RE_INF = re.compile(r"^\s*(?:\d{1,2}:\d{2}\s+)?(.+?) (\d+)-(\d+)(?: \(\d+-\d+\))? (.+?)\s*$")
RE_VST = re.compile(r"^\s*(?:\d{1,2}:\d{2}\s+)?(.+?) v (.+?) (\d+)-(\d+)(?: \(\d+-\d+\))?\s*$")
RE_TAG = re.compile(r"\s+\[.*$")


def clean(line):
    return RE_TAG.sub("", line.rstrip("\n"))


def pin(name, unknowns, lineno):
    n = " ".join(name.strip().split())
    if n in NAME:
        return NAME[n]
    unknowns.append((lineno, n))
    return None


def main():
    raw, season, start_year = sys.argv[1], sys.argv[2], int(sys.argv[3])
    year, month, dayno = start_year, None, None
    rnd = None
    rows = []
    unknowns = []
    inbody = False
    for lineno, rawline in enumerate(open(raw, encoding="utf-8"), 1):
        line = clean(rawline)
        mb = RE_BANNER.match(line)
        if mb:
            rnd = int(mb.group(1))
            inbody = True
            continue
        md = RE_DAY.match(line)
        if md and inbody:
            m2 = MON[md.group(1)]
            d = int(md.group(2))
            if md.group(3):
                year = int(md.group(3))
            elif month is not None and m2 < month:
                year += 1
            month, dayno = m2, d
            continue
        if line.lstrip().startswith("(") or not line.strip() or line.startswith("#"):
            continue
        if not inbody or rnd is None or month is None:
            continue
        m = RE_VST.match(line)
        if m:
            h = pin(m.group(2).split(" v ")[0] if False else m.group(1), unknowns, lineno)
            a = pin(m.group(2), unknowns, lineno)
            hg, ag = int(m.group(3)), int(m.group(4))
        else:
            m = RE_INF.match(line)
            if not m:
                continue
            h = pin(m.group(1), unknowns, lineno)
            a = pin(m.group(4), unknowns, lineno)
            hg, ag = int(m.group(2)), int(m.group(3))
        if h is None or a is None:
            continue
        rows.append((rnd, f"{year:04d}-{month:02d}-{dayno:02d}", h, hg, ag, a))

    # gates
    cnt = Counter(r[0] for r in rows)
    apps = Counter()
    for _, _, h, _, _, a in rows:
        apps[h] += 1
        apps[a] += 1
    print(f"# parsed rows: {len(rows)} (file {raw}, season {season})", file=sys.stderr)
    hist_bad = {k: v for k, v in sorted(cnt.items()) if v != 10}
    print(f"# rounds present: {len(cnt)}; rounds != 10 after summing: {hist_bad}", file=sys.stderr)
    app_bad = {k: v for k, v in apps.items() if v != 38}
    print(f"# clubs: {len(apps)}; clubs != 38 apps: {app_bad}", file=sys.stderr)
    print(f"# unknown names: {len(unknowns)}: {unknowns[:12]}", file=sys.stderr)
    dates = [r[1] for r in rows]
    print(f"# date span: {min(dates)} .. {max(dates)}", file=sys.stderr)
    if len(rows) != 380 or hist_bad or app_bad or unknowns or len(cnt) != 38:
        print("# GATE FAIL", file=sys.stderr)
        sys.exit(1)
    for r in rows:
        print(f"MD{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}|{r[5]}")


if __name__ == "__main__":
    main()
