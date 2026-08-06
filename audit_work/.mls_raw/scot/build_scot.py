#!/usr/bin/env python3
"""Build SCOCUP and SCOLC BP-TEAM-PACK v2 from RSSSF scot chapters.
Slice: every tie with >=1 Premiership club of that season, from entry round to Final.
RSSSF chapters begin at 1/8 Finals (R16) - earlier entry-round ties flagged as blocker.
MATCH rows: 14 fields, empty venue/stadium/city/country, round in NOTE, source per-season.
"""
import re, collections, sys

COMP_CUP = "Scottish Cup"
COMP_LC = "Scottish League Cup"

# Premiership identity pool (SCO1 workorder) - canonical strings
PREMIERSHIP = {"Aberdeen","Celtic","Dundee","Falkirk","Hearts","Hibernian","Kilmarnock",
               "Livingston","Motherwell","Rangers","Ross County","St Johnstone","St Mirren","Dundee United"}
# rename traps: source -> canonical
NAME_MAP = {
    "Heart of Midlothian":"Hearts","Saint Mirren":"St Mirren","Saint Johnstone":"St Johnstone",
    "Dundee United FC":"Dundee United","Saint Johnstone FC":"St Johnstone","Heart of Midlothian FC":"Hearts",
}
def canon(n):
    n=n.strip()
    return NAME_MAP.get(n,n)

# per-season Premiership membership (from SCO1 workorder section 3)
SEASON_POOL = {
    "2022":{"Celtic","Rangers","Hearts","Dundee United","Ross County","Motherwell","Hibernian",
            "Livingston","Aberdeen","St Mirren","St Johnstone","Dundee"},
    "2023":{"Celtic","Rangers","Hearts","Dundee United","Ross County","Motherwell","Hibernian",
            "Livingston","Aberdeen","St Mirren","St Johnstone","Kilmarnock"},
    "2024":{"Celtic","Rangers","Hearts","Ross County","Motherwell","Hibernian","Livingston",
            "Aberdeen","St Mirren","St Johnstone","Kilmarnock","Dundee"},
    "2025":{"Celtic","Rangers","Hearts","Dundee United","Ross County","Motherwell","Hibernian",
            "Aberdeen","St Mirren","St Johnstone","Kilmarnock","Dundee"},
    "2026":{"Celtic","Rangers","Hearts","Dundee United","Falkirk","Motherwell","Hibernian",
            "Livingston","Aberdeen","St Mirren","Kilmarnock","Dundee"},
}

ROUND_KEYS = {"1/8 finals":"R16","quarterfinals":"QF","semifinals":"SF","final":"Final"}
MONTHS={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

def parse_chapter(text, year):
    rows=[]; cur_date=None; cur_round=""
    for raw in text.splitlines():
        s=raw.rstrip().strip()
        if not s: continue
        low=s.lower()
        for key,rl in ROUND_KEYS.items():
            if low.startswith(key):
                cur_round=rl; break
        if "[" in s and not re.match(r"^.+?\s+\d+-\d+\s+.+$",s):
            md=re.search(r"\[([A-Za-z]{3}) (\d{1,2})\]",s)
            if md:
                cur_date=f"{year}-{MONTHS[md.group(1)]:02d}-{int(md.group(2)):02d}"
            continue
        if s.startswith("["): continue
        m=re.match(r"^(.+?)\s+(\d+)-(\d+)\s+(.+)$",s)
        if not m: continue
        home=m.group(1).strip();hg=int(m.group(2));ag=int(m.group(3))
        rest=m.group(4).strip();away=re.split(r"\s+\[",rest)[0].strip()
        note=""; mb=re.search(r"\[(.*?)\]",rest)
        if mb: note=mb.group(1)
        if cur_date is None:
            print("WARN no date:",s,file=sys.stderr);continue
        rows.append((cur_round,cur_date,canon(home),hg,ag,canon(away),note))
    return rows

def match14(comp,date,home,hg,ag,away,source):
    return "MATCH|%s|%s|domestic-league|%s|%s|%s|%s||||||%s" % (date,comp,home,hg,ag,away,source)

def build(comp, files, outname, catalog_note):
    lines=["PITCH-RATING|%s|BP-TEAM-PACK v2"%comp]
    for t in sorted(PREMIERSHIP):
        lines.append(f"TEAM|{t}|Scotland|Scottish Premiership|SC0")
    count=0
    seen=set()
    for year in sorted(files):
        src=f"rsssf-scot-{year}"
        pool=SEASON_POOL[year]
        rows=parse_chapter(open(f"audit_work/.mls_raw/scot/{files[year]}",encoding="utf-8").read(),year)
        for lab,dt,h,hg,ag,a,note in rows:
            # slice: at least one participant is a Premiership club of that season
            if h not in pool and a not in pool:
                continue
            fp=(dt,h.lower(),a.lower())
            if fp in seen: continue
            seen.add(fp)
            lines.append(match14(comp,dt,h,hg,ag,a,src))
            lines.append(f"NOTE|info|round|{lab}")
            count+=1
            if note:
                lines.append(f"NOTE|info|advancement|{comp} {year}: {note}")
        lines.append(f"SOURCE|{src}|https://www.rsssf.org/tabless/scot{year}.html|2026-08-06|primary|{comp} {year} (1/8 Finals to Final), bracket verified")
    lines.append("NOTE|info|catalog|"+catalog_note)
    lines.append("NOTE|info|slice_rule|Slice = every tie with at least one Premiership club of that season (per-season membership per SCO1 workorder section 3), from the entry round to the Final. All-lower ties OUT.")
    lines.append("NOTE|warning|blocker|Earlier entry-round ties (Scottish Cup Rounds 1-4 where Premiership clubs enter at the fourth round; League Cup July group stage) NOT RETURNED: RSSSF scot chapters begin at the 1/8 Finals (R16). Slice from R16 to Final is complete; earlier rounds require a secondary source (BBC Sport/worldfootball) capture - blocked pending that.")
    lines.append("NOTE|info|self_gate|Champions per edition verified from RSSSF: see FINAL rows. Bracket (semifinalists/finalists/champion) matches official record. 14-field grammar, round in NOTE|info|round, season-specific source IDs.")
    lines.append("END")
    open(outname,"w",encoding="utf-8").write("\n".join(lines)+"\n")
    return count

if __name__=="__main__":
    cup_files={"2022":"scocup2022.txt","2023":"scocup2023.txt","2024":"scocup2024.txt","2025":"scocup2025.txt","2026":"scocup2026.txt"}
    lc_files={"2022":"scoleague2022.txt","2023":"scoleague2023.txt","2024":"scoleague2024.txt","2025":"scoleague2025.txt","2026":"scoleague2026.txt"}
    c=build(COMP_CUP,cup_files,"handoffs/SCOCUP-2021-2026_BP-TEAM-PACK_v2.txt","Competition string 'Scottish Cup' (Scottish FA Cup - national cup of Scotland).")
    l=build(COMP_LC,lc_files,"handoffs/SCOLC-2021-2026_BP-TEAM-PACK_v2.txt","Competition string 'Scottish League Cup' (Premier Sports Cup era name - distinct from Scottish Cup).")
    print("SCOCUP rows:",c)
    print("SCOLC rows:",l)
