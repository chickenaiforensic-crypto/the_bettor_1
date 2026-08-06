#!/usr/bin/env python3
"""Parse RSSSF MLS raw text -> BP-TEAM-PACK v2 MATCH rows + table verification."""
import re, sys, collections

MAP = {
    "Montreal CF": "CF Montréal", "Montréal CF": "CF Montréal", "Montreal": "CF Montréal",
    "Chicago Fire": "Chicago Fire FC",
    "DC United": "D.C. United",
    "Houston Dynamo": "Houston Dynamo FC",
    "Inter Miami": "Inter Miami CF",
    "LA Galaxy": "LA Galaxy", "Los Angeles Galaxy": "LA Galaxy",
    "Los Angeles FC": "Los Angeles FC", "LAFC": "Los Angeles FC",
    "Minnesota United": "Minnesota United FC",
    "New York City": "New York City FC", "NYCFC": "New York City FC",
    "Seattle Sounders": "Seattle Sounders FC",
    "Sporting Kansas City": "Sporting Kansas City",
    "Vancouver Whitecaps": "Vancouver Whitecaps FC",
    "Real Salt Lake": "Real Salt Lake",
    "Portland Timbers": "Portland Timbers",
    "San Jose Earthquakes": "San Jose Earthquakes",
    "FC Dallas": "FC Dallas",
    "Colorado Rapids": "Colorado Rapids",
    "Austin FC": "Austin FC",
    "Atlanta United": "Atlanta United FC",
    "Orlando City": "Orlando City SC",
    "Columbus Crew": "Columbus Crew",
    "Philadelphia Union": "Philadelphia Union",
    "New York Red Bulls": "New York Red Bulls",
    "Toronto FC": "Toronto FC",
    "FC Cincinnati": "FC Cincinnati",
    "Nashville SC": "Nashville SC",
    "New England Revolution": "New England Revolution",
    "Saint Louis City": "St. Louis City SC",
    "Saint Louis City SC": "St. Louis City SC",
    "St. Louis City SC": "St. Louis City SC",
    "Charlotte FC": "Charlotte FC",
    "San Diego FC": "San Diego FC",
}
CANON = set(MAP.values())

def canon(name):
    if name in CANON:
        return name
    return MAP.get(name, name)

MONTHS = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

def date_line_to_iso(s, year):
    d = re.search(r"\[(\d{1,2})/(\d{1,2})\]", s)
    if d:
        return f"{year}-{int(d.group(1)):02d}-{int(d.group(2)):02d}"
    m4 = re.search(r"\[(20\d\d-\d\d-\d\d)\]", s)
    if m4:
        return m4.group(1)
    md = re.search(r"\[([A-Za-z]{3}) (\d{1,2})\]", s)
    if md:
        return f"{year}-{MONTHS[md.group(1)]:02d}-{int(md.group(2)):02d}"
    return None

def parse_rounds(text, year):
    rows = []
    cur_date = None
    cur_round = None
    for raw in text.splitlines():
        s = raw.rstrip().strip()
        if not s:
            continue
        if s.startswith("Round") or s.startswith("Moved") or s.startswith("Final Tables"):
            m = re.match(r"Round\s+(\d+)", s)
            cur_round = "RS R" + m.group(1) if m else None
            continue
        if s.startswith("["):
            cur_date = date_line_to_iso(s, year)
            continue
        if s.lower().endswith(" bye"):
            continue
        # strip trailing bracket annotations like [aet], [3-1 pen], [abandoned...]
        m = re.match(r"^(.+?)\s+(\d+)-(\d+)\s+(.+)$", s)
        if not m:
            continue
        home = m.group(1).strip(); hg=int(m.group(2)); ag=int(m.group(3))
        away_part = m.group(4).strip()
        # away_part may include annotation in brackets
        away = re.split(r"\s+\[", away_part)[0].strip()
        # skip abandoned matches (no score recorded / abd)
        if "abd" in home.lower() or home.lower().endswith("abd"):
            continue
        if "abd" in away.lower():
            continue
        if hg is None or ag is None:
            continue
        home_c = canon(home); away_c = canon(away)
        if cur_date is None:
            print("WARN no date:", s, file=sys.stderr)
            continue
        rows.append((cur_round or "RS", cur_date, home_c, hg, ag, away_c))
    return rows

def compute_table(rows):
    tbl = collections.defaultdict(lambda: [0,0,0,0,0,0,0])
    for _, d, home, hg, ag, away in rows:
        h=tbl[home]; a=tbl[away]
        h[3]+=hg; h[4]+=ag; a[3]+=ag; a[4]+=hg
        h[5]+=hg-ag; a[5]+=ag-hg
        if hg>ag: h[0]+=1; a[2]+=1; h[6]+=3
        elif hg<ag: a[0]+=1; h[2]+=1; a[6]+=3
        else: h[1]+=1; a[1]+=1; h[6]+=1; a[6]+=1
    return tbl

if __name__ == "__main__":
    for y in ["2021","2022","2023","2024"]:
        rows = parse_rounds(open(f"audit_work/.mls_raw/usa{y}.txt",encoding="utf-8").read(), y)
        print(y, "MATCH rows:", len(rows))
        tbl = compute_table(rows)
        for t in sorted(tbl, key=lambda t:(-tbl[t][6], -tbl[t][5], -tbl[t][3])):
            w,d,l,gf,ga,gd,pts = tbl[t]
            print(f"  {t:24s} {w:2d} {d:2d} {l:2d} {gf}-{ga} {pts:3d}")
        print()
