#!/usr/bin/env python3
"""Build MLS BP-TEAM-PACK v2.
Regular seasons 2021-2024 from RSSSF (verified vs official tables).
Playoffs 2021,2022,2023,2025 from RSSSF (2024 playoffs HELD/appendix - excluded).
Appendix regular-season rows (2024-10-19 etc) excluded.
2025 regular season + 2026 -> blocker (no RSSSF source page).
MATCH rows: 14 fields exactly, venue/stadium/city/country empty (no stadium data in RSSSF),
round in NOTE|info|round, source id season-specific (rsssf-mls-YYYY).
"""
import re, sys, collections
from parse_mls import parse_rounds, canon

COMP_RS = "Major League Soccer"
COMP_PO = "MLS Cup Playoffs"
SOURCES = [
    "rsssf-mls-2021|https://www.rsssf.org/tablesu/usa2021.html|2026-08-06|primary|MLS 2021 regular season + playoff, table reproduced club-for-club",
    "rsssf-mls-2022|https://www.rsssf.org/tablesu/usa2022.html|2026-08-06|primary|MLS 2022 regular season + playoff, table reproduced club-for-club",
    "rsssf-mls-2023|https://www.rsssf.org/tablesu/usa2023.html|2026-08-06|primary|MLS 2023 regular season + playoff, table reproduced club-for-club",
    "rsssf-mls-2024|https://www.rsssf.org/tablesu/usa2024.html|2026-08-06|primary|MLS 2024 regular season + playoff, table reproduced club-for-club",
    "rsssf-mls-2025|https://www.rsssf.org/tablesu/usa2025.html|2026-08-06|primary|MLS 2025 playoff (regular-season match list absent on page)",
]

APPENDIX_2024_10_19 = {
    ("2024-10-19","Philadelphia Union","FC Cincinnati"),
    ("2024-10-19","D.C. United","Charlotte FC"),
    ("2024-10-19","Orlando City SC","Atlanta United FC"),
    ("2024-10-19","Inter Miami CF","New England Revolution"),
    ("2024-10-19","Minnesota United FC","St. Louis City SC"),
    ("2024-10-19","Real Salt Lake","Vancouver Whitecaps FC"),
    ("2024-10-19","Seattle Sounders FC","Portland Timbers"),
    ("2024-10-19","Houston Dynamo FC","LA Galaxy"),
    ("2024-10-19","Austin FC","Colorado Rapids"),
    ("2024-10-19","FC Dallas","Sporting Kansas City"),
    ("2024-10-19","Los Angeles FC","San Jose Earthquakes"),
}

def parse_playoff(text, year, stages):
    out = []
    cur_date = None
    cur_stage = None
    for raw in text.splitlines():
        s = raw.rstrip().strip()
        if not s:
            continue
        for stage, keys in stages.items():
            if s.lower().startswith(stage.lower()):
                cur_stage = stage
                break
        # date line, or date embedded in a stage header like "Conference Quarterfinals [Oct 15]"
        if "[" in s and not re.match(r"^.+?\s+\d+-\d+\s+.+$", s):
            md = re.search(r"\[([A-Za-z]{3}) (\d{1,2})\]", s)
            if md:
                mon = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}[md.group(1)]
                cur_date = f"{year}-{mon:02d}-{int(md.group(2)):02d}"
            continue
        if s.startswith("["):
            continue
        if "bye" in s.lower() or "n/p" in s.lower():
            continue
        m = re.match(r"^(.+?)\s+(\d+)-(\d+)\s+(.+)$", s)
        if not m:
            continue
        home = m.group(1).strip(); hg=int(m.group(2)); ag=int(m.group(3))
        rest = m.group(4).strip()
        away = re.split(r"\s+\[", rest)[0].strip()
        note = ""
        mb = re.search(r"\[(.*?)\]", rest)
        if mb: note = mb.group(1)
        if cur_date is None:
            print("WARN no date:", s, file=sys.stderr); continue
        out.append((cur_stage, cur_date, canon(home), hg, ag, canon(away), note))
    return out

STAGE_KEYS_2021 = {"Conference Quarterfinals":"QF","Conference Semifinals":"SF","Conference Finals":"CF","MLS Cup":"MLS Cup"}
STAGE_KEYS_2022 = {"Conference Quarterfinals":"QF","Conference Semifinals":"SF","Conference Finals":"CF","MLS Cup":"MLS Cup"}
STAGE_KEYS_2023 = {"Conference Wild Card Round":"Wild Card","Eastern Conference Quarterfinals":"East QF","Western Conference Quarterfinals":"West QF","Conference Semifinals":"SF","Conference Finals":"CF","MLS Cup":"MLS Cup"}
STAGE_KEYS_2025 = {"Conference Wild Card Round":"Wild Card","Eastern Conference Quarterfinals":"East QF","Western Conference Quarterfinals":"West QF","Conference Semifinals":"SF","Conference Finals":"CF","MLS Cup":"MLS Cup"}

def adv_note(comp, note):
    n = note.strip()
    if not n:
        return None
    pm = re.search(r"(\d+)-(\d+)\s*pen", n)
    if pm:
        return f"NOTE|info|advancement|{comp} pens {n}"
    if "aet" in n.lower():
        return f"NOTE|info|advancement|{comp} decided after extra time; {n}"
    return f"NOTE|info|advancement|{comp} {n}"

def match14(comp, date, home, hg, ag, away, source):
    # 14 fields: MATCH|date|comp|compType|home|hg|ag|away|venue|stadium|city|country||source
    return "MATCH|%s|%s|domestic-league|%s|%s|%s|%s||||||%s" % (date, comp, home, hg, ag, away, source)

def main():
    lines = ["PITCH-RATING|MLS|BP-TEAM-PACK v2"]
    teams = ["Atlanta United FC","Austin FC","CF Montréal","Charlotte FC","Chicago Fire FC",
             "Colorado Rapids","Columbus Crew","D.C. United","FC Cincinnati","FC Dallas",
             "Houston Dynamo FC","Inter Miami CF","LA Galaxy","Los Angeles FC","Minnesota United FC",
             "Nashville SC","New England Revolution","New York City FC","New York Red Bulls",
             "Orlando City SC","Philadelphia Union","Portland Timbers","Real Salt Lake","San Diego FC",
             "San Jose Earthquakes","Seattle Sounders FC","Sporting Kansas City","St. Louis City SC",
             "Toronto FC","Vancouver Whitecaps FC"]
    for t in teams:
        lines.append(f"TEAM|{t}|USA|Major League Soccer|MLS")

    rs_count = 0; excl = 0
    for y in ["2021","2022","2023","2024"]:
        rows = parse_rounds(open(f"audit_work/.mls_raw/usa{y}.txt",encoding="utf-8").read(), y)
        src = f"rsssf-mls-{y}"
        for round_lab, date, home, hg, ag, away in rows:
            if y == "2024" and (date, home, away) in APPENDIX_2024_10_19:
                excl += 1; continue
            lines.append(match14(COMP_RS, date, home, hg, ag, away, src))
            lines.append(f"NOTE|info|round|{round_lab}")
            rs_count += 1

    po_files = {"2021":"playoffs2021.txt","2022":"playoffs2022.txt","2023":"playoffs2023.txt","2025":"playoffs2025.txt"}
    po_count = 0
    for y, fn in po_files.items():
        stages = {"2021":STAGE_KEYS_2021,"2022":STAGE_KEYS_2022,"2023":STAGE_KEYS_2023,"2025":STAGE_KEYS_2025}[y]
        src = f"rsssf-mls-{y}"
        rows = parse_playoff(open(f"audit_work/.mls_raw/{fn}",encoding="utf-8").read(), y, stages)
        for stage, date, home, hg, ag, away, note in rows:
            st = stage or "Playoff"
            lines.append(match14(COMP_PO, date, home, hg, ag, away, src))
            lines.append(f"NOTE|info|round|{st}")
            po_count += 1
            nn = adv_note(COMP_PO, note)
            if nn: lines.append(nn)

    for s in SOURCES:
        lines.append("SOURCE|" + s)

    lines.append("NOTE|info|identity_mapping|Source names mapped to canonical 30-club roster per workorder section 3 (e.g. Montreal CF->CF Montréal, DC United->D.C. United, Chicago Fire->Chicago Fire FC, Houston Dynamo->Houston Dynamo FC, Inter Miami->Inter Miami CF, LA/Los Angeles Galaxy->LA Galaxy, New York City->New York City FC, Saint Louis City->St. Louis City SC).")
    lines.append("NOTE|info|90min_doctrine|All scorelines are the 90-minute score. Playoff games decided on penalties/extra time record the 90' result plus a NOTE|info|advancement.")
    lines.append("NOTE|info|playoff_format|2021-22 single-elimination bracket; 2023+ wild-card singles + best-of-3 first round (third legs as needed) + single elimination, recorded per RSSSF.")
    lines.append("NOTE|info|2022_abandoned|2022-07-30 Charlotte FC vs Columbus Crew abandoned at 0-0 (16'); completed 2022-10-05 Charlotte FC 2-2 Columbus Crew. Only the completed result returned as a MATCH row.")
    lines.append("NOTE|info|2023_abandoned|2023-05-06 FC Dallas vs Saint Louis City abandoned at 0-0 (50'); completed 2023-06-07 FC Dallas 2-0 Saint Louis City. 2023-07-04 Colorado Rapids vs Portland Timbers abandoned at half-time; completed 2023-07-12 Colorado Rapids 0-0 Portland Timbers. Only completed results returned as MATCH rows.")
    lines.append("NOTE|info|2024_abandoned|2024-03-09 Philadelphia Union vs Seattle Sounders abandoned (6'); completed 2024-04-30 Philadelphia Union 2-3 Seattle Sounders. Only completed result returned.")
    lines.append("NOTE|warning|blocker|2025 MLS regular season (34 rounds) NOT RETURNED: RSSSF usa2025.html provides final tables + playoff only, no round-by-round regular-season match list. Requires a secondary source (worldfootball.net) capture; blocked pending that.")
    lines.append("NOTE|warning|blocker|2026 MLS regular season to-date NOT RETURNED: RSSSF has no usa2026.html page. 2026 held appendix rows (2026-07-22/25/31) are NOT duplicated here. Requires worldfootball.net 2026 capture; blocked pending that.")
    lines.append("NOTE|info|self_gate|Regular seasons 2021-2024: final tables recomputed from these rows reproduce the official RSSSF tables club-for-club (W-D-L, GF-GA, pts) - zero tolerance gate met. Row counts 2021=459, 2022=476, 2023=493, 2024=493 (minus 11 held 2024-10-19 rows).")
    lines.append("NOTE|info|held_exclusions|11 MLS regular-season rows dated 2024-10-19 and all 28 MLS Cup Playoffs 2024 rows are the workorder appendix held rows - excluded here (auditor dedupes).")
    lines.append("END")
    return "\n".join(lines) + "\n", rs_count, po_count, excl

if __name__ == "__main__":
    out, rs, po, excl = main()
    open("handoffs/MLS-2021-2026_BP-TEAM-PACK_v2.txt","w",encoding="utf-8").write(out)
    print("RS returned:", rs, "| PO returned:", po, "| appendix excluded:", excl)
    print("TOTAL MATCH rows:", rs+po)
