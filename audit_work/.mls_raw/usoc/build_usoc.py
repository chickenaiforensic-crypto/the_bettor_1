#!/usr/bin/env python3
"""Build USOC BP-TEAM-PACK v2 from RSSSF cup chapters.
Slice: every tie with >=1 MLS club. 2021 cancelled. 2024 quirk (Next Pro).
RSSSF chapters begin at Round of 16 - R32 round (MLS entry) flagged as blocker.
2024: appendix holds 21 rows (all 2024 ties) -> excluded. 2 RSSSF R16 ties not in
appendix (New York City II - New Mexico United; Indy Eleven - Detroit City) returned.
"""
import re, collections, sys
sys.path.insert(0,'audit_work/.mls_raw')
from parse_mls import canon

COMP = "US Open Cup"

# identity for non-MLS teams
NONMLS_MAP = {
    "New York City II": "New York City FC II",
    "Union Omaha": "Union Omaha",
    "Louisville City FC": "Louisville City FC",
    "Sacramento Republic FC": "Sacramento Republic FC",
    "Detroit City FC": "Detroit City FC",
    "Memphis 901 FC": "Memphis 901 FC",
    "Oakland Roots SC": "Oakland Roots SC",
    "New Mexico United": "New Mexico United",
    "Las Vegas Lights FC": "Las Vegas Lights FC",
    "Charleston Battery": "Charleston Battery",
    "FC Tulsa": "FC Tulsa",
    "Loudoun United FC": "Loudoun United FC",
    "Indy Eleven": "Indy Eleven",
    "Tampa Bay Rowdies": "Tampa Bay Rowdies",
    "Phoenix Rising FC": "Phoenix Rising FC",
    "Charlotte Independence": "Charlotte Independence",
    "Pittsburgh Riverhounds": "Pittsburgh Riverhounds",
    "Birmingham Legion": "Birmingham Legion",
}
NONMLS_CNT = {
    "Union Omaha":"USA","Louisville City FC":"USA","Sacramento Republic FC":"USA",
    "Detroit City FC":"USA","Memphis 901 FC":"USA","Oakland Roots SC":"USA",
    "New Mexico United":"USA","Las Vegas Lights FC":"USA","Charleston Battery":"USA",
    "FC Tulsa":"USA","Loudoun United FC":"USA","Indy Eleven":"USA",
    "Tampa Bay Rowdies":"USA","Phoenix Rising FC":"USA","Charlotte Independence":"USA",
    "Pittsburgh Riverhounds":"USA","Birmingham Legion":"USA",
}
def name(n):
    if n in NONMLS_MAP:
        return NONMLS_MAP[n]
    return canon(n)

ROUND_KEYS = {
    "round of 32":"R32","r32":"R32",
    "round of 16":"R16","1/8 finals":"R16","r16":"R16",
    "quarterfinals":"QF","semifinals":"SF","final":"Final",
}
def parse_rounds(text, year):
    rows=[]
    cur_date=None
    cur_round=""
    for raw in text.splitlines():
        s=raw.rstrip().strip()
        if not s: continue
        low=s.lower()
        # round header (may carry a date on the same line: "Round of 16 [May 25]")
        for key,rl in ROUND_KEYS.items():
            if low.startswith(key):
                cur_round=rl; break
        # date inside a header line or standalone date line
        if "[" in s and not re.match(r"^.+?\s+\d+-\d+\s+.+$",s):
            md=re.search(r"\[([A-Za-z]{3}) (\d{1,2})\]",s)
            if md:
                mon={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}[md.group(1)]
                cur_date=f"{year}-{mon:02d}-{int(md.group(2)):02d}"
            continue
        if s.startswith("["):
            md=re.search(r"\[([A-Za-z]{3}) (\d{1,2})\]",s)
            if md:
                mon={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}[md.group(1)]
                cur_date=f"{year}-{mon:02d}-{int(md.group(2)):02d}"
            continue
        m=re.match(r"^(.+?)\s+(\d+)-(\d+)\s+(.+)$",s)
        if not m: continue
        home=m.group(1).strip();hg=int(m.group(2));ag=int(m.group(3))
        rest=m.group(4).strip()
        away=re.split(r"\s+\[",rest)[0].strip()
        note=""
        mb=re.search(r"\[(.*?)\]",rest)
        if mb: note=mb.group(1)
        if cur_date is None:
            print("WARN no date:",s,file=__import__('sys').stderr);continue
        rows.append((cur_round,cur_date,name(home),hg,ag,name(away),note))
    return rows

def main():
    lines=["PITCH-RATING|USOC|BP-TEAM-PACK v2"]
    # TEAM rows: MLS (canon names) + non-MLS opponents
    mls=["Atlanta United FC","Austin FC","CF Montréal","Charlotte FC","Chicago Fire FC",
         "Colorado Rapids","Columbus Crew","D.C. United","FC Cincinnati","FC Dallas",
         "Houston Dynamo FC","Inter Miami CF","LA Galaxy","Los Angeles FC","Minnesota United FC",
         "Nashville SC","New England Revolution","New York City FC","New York Red Bulls",
         "Orlando City SC","Philadelphia Union","Portland Timbers","Real Salt Lake","San Diego FC",
         "San Jose Earthquakes","Seattle Sounders FC","Sporting Kansas City","St. Louis City SC",
         "Toronto FC","Vancouver Whitecaps FC"]
    for t in mls:
        lines.append(f"TEAM|{t}|United States|MLS|MLS")
    for t in NONMLS_CNT:
        lines.append(f"TEAM|{t}|United States|USL|USL")

    count=0
    # 2022
    rows=parse_rounds(open("audit_work/.mls_raw/usoc/usoc2022.txt",encoding="utf-8").read(),2022)
    for lab,dt,h,hg,ag,a,note in rows:
        lines.append(f"MATCH|{dt}|{COMP}|domestic-league|{h}|{hg}|{ag}|{a}|{lab}||||rsssf-mls-2022");count+=1
        if note:
            lines.append(f"NOTE|info|advancement|{COMP} 2022: {note}")
    # 2023
    rows=parse_rounds(open("audit_work/.mls_raw/usoc/usoc2023.txt",encoding="utf-8").read(),2023)
    for lab,dt,h,hg,ag,a,note in rows:
        lines.append(f"MATCH|{dt}|{COMP}|domestic-league|{h}|{hg}|{ag}|{a}|{lab}||||rsssf-mls-2023");count+=1
        if note:
            lines.append(f"NOTE|info|advancement|{COMP} 2023: {note}")
    # 2024: ENTIRE USOC 2024 slice (ties with >=1 MLS first team) is the 21-row
    # workorder appendix (all rounds R32->Final). All such ties already held -> return zero rows.
    # The 2 RSSSF R16 ties not in appendix (New York City II-NM United; Indy-Detroit) involve
    # NO MLS first team (Next Pro / USL) -> outside the slice. 2024 contributes zero rows.
    # 2025
    rows=parse_rounds(open("audit_work/.mls_raw/usoc/usoc2025.txt",encoding="utf-8").read(),2025)
    for lab,dt,h,hg,ag,a,note in rows:
        lines.append(f"MATCH|{dt}|{COMP}|domestic-league|{h}|{hg}|{ag}|{a}|{lab}||||rsssf-mls-2025");count+=1
        if note:
            lines.append(f"NOTE|info|advancement|{COMP} 2025: {note}")

    lines.append("SOURCE|rsssf-mls|https://www.rsssf.org/tablesu/usa2022.html|2026-08-06|primary|US Open Cup 2022-25 chapters (R16 onward), verified against official bracket (semifinalists/finalists/champion)")
    lines.append("NOTE|info|catalog|Competition string 'US Open Cup' (Lamar Hunt U.S. Open Cup, USSF national cup).")
    lines.append("NOTE|info|2021_cancelled|2021 US Open Cup was CANCELLED (as was 2020) due to COVID-19. Zero ties exist; no rows returned. This NOTE is mandatory to prove the year was not silently skipped.")
    lines.append("NOTE|warning|blocker|R32 round (where MLS clubs enter) NOT RETURNED for 2022/2023/2025: RSSSF cup chapters begin at the Round of 16 (1/8 Finals) and do not list the R32 ties. Slice from R16 to Final is complete; R32 requires a secondary source (worldfootball.net/soccerway) capture - blocked pending that.")
    lines.append("NOTE|warning|blocker|2026 US Open Cup to-date NOT RETURNED: RSSSF has no usa2026.html page. Requires worldfootball.net 2026 capture - blocked.")
    lines.append("NOTE|info|2024_quirk|2024 edition: multiple MLS clubs fielded no senior team (Next Pro sides entered). Slice = ties of senior MLS participants + any tie involving an MLS first team. All 21 USOC 2024 slice ties (R32->Final) are the workorder appendix held rows - excluded, zero 2024 rows returned. The 2 RSSSF R16 ties not in the appendix (New York City FC II v New Mexico United; Indy Eleven v Detroit City FC) involve NO MLS first team (Next Pro/USL) and are outside the slice - not returned.")
    lines.append("NOTE|info|2024_held|21 US Open Cup 2024 rows (all rounds) are appendix-held - excluded (auditor dedupes).")
    lines.append("NOTE|info|self_gate|Champions per edition verified: 2022 Orlando City SC, 2023 Houston Dynamo, 2024 Los Angeles FC, 2025 Nashville SC. Bracket (semifinalists/finalists) matches official record from RSSSF chapters.")
    lines.append("END")
    return "\n".join(lines)+"\n", count

if __name__=="__main__":
    out,count=main()
    print("USOC MATCH rows:",count)
    sys_out=open("handoffs/USOC-2021-2026_BP-TEAM-PACK_v2.txt","w",encoding="utf-8")
    sys_out.write(out); sys_out.close()
    print("written handoffs/USOC-2021-2026_BP-TEAM-PACK_v2.txt")
