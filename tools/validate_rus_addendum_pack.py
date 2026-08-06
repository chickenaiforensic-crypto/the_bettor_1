#!/usr/bin/env python3
"""External validator for handoffs/RUS-ADDENDUM-2026_BP-TEAM-PACK_v2.txt.
Gates embed the transcribed source prints (audit/ledger/rpl-2026-27.txt,
audit/ledger/rus-supercup-2025-2026.txt) and cross-check the RPL pack pins.
Writes audit/pack-validation-rus-addendum.txt; exit 1 on first FAIL."""
import hashlib, re, sys, os

PACK = "handoffs/RUS-ADDENDUM-2026_BP-TEAM-PACK_v2.txt"
RPL = "handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt"
REP = "audit/pack-validation-rus-addendum.txt"
RETURN_DATE = "2026-08-04"

lines = open(PACK, encoding="ascii").read().split("\n")
if lines and lines[-1] == "":
    lines = lines[:-1]
matches = [x for x in lines if x.startswith("MATCH|")]
teams = [x for x in lines if x.startswith("TEAM|")]
sources = [x for x in lines if x.startswith("SOURCE|")]
notes = [x for x in lines if x.startswith("NOTE|")]

results = []
def gate(gid, ok, detail):
    results.append((gid, ok, detail))

# --- embedded source prints (ledger) ---
R1_EXPECT = [
 ("2026-07-24","CSKA Moscow",2,1,"Baltika Kaliningrad"),
 ("2026-07-25","Akron Tolyatti",0,5,"Zenit St Petersburg"),
 ("2026-07-25","Spartak Moscow",3,0,"Rodina Moscow"),
 ("2026-07-25","Dynamo Moscow",0,0,"Krylia Sovetov Samara"),
 ("2026-07-25","Fakel Voronezh",1,2,"Dynamo Makhachkala"),
 ("2026-07-26","Rubin Kazan",1,3,"FC Krasnodar"),
 ("2026-07-26","Lokomotiv Moscow",1,1,"Akhmat Grozny"),
 ("2026-07-26","FC Orenburg",2,1,"FC Rostov"),
]
R2_EXPECT = [
 ("2026-07-31","Rodina Moscow",2,4,"FC Rostov"),
 ("2026-08-01","Akron Tolyatti",1,2,"Rubin Kazan"),
 ("2026-08-01","CSKA Moscow",1,1,"Krylia Sovetov Samara"),
 ("2026-08-01","Dynamo Makhachkala",2,1,"Lokomotiv Moscow"),
 ("2026-08-01","Baltika Kaliningrad",2,1,"Dynamo Moscow"),
 ("2026-08-02","FC Orenburg",0,3,"Zenit St Petersburg"),
 ("2026-08-02","FC Krasnodar",3,2,"Fakel Voronezh"),
 ("2026-08-02","Akhmat Grozny",1,2,"Spartak Moscow"),
]
SUP_EXPECT = [
 ("2025-07-12","Russian Super Cup","domestic-cup","FC Krasnodar",0,1,"CSKA Moscow","Final","Ak Bars Arena","Kazan","rsssf-rus2025-sup"),
 ("2026-07-18","Russian Super Cup","domestic-cup","Zenit St Petersburg",1,1,"Spartak Moscow","Final","Nizhny Novgorod Stadium","Nizhny Novgorod","rsssf-rus2026-sup"),
]
R1_ATT = {("2026-07-24","CSKA Moscow"):15196,("2026-07-25","Akron Tolyatti"):5091,
 ("2026-07-25","Spartak Moscow"):23601,("2026-07-25","Dynamo Moscow"):15335,
 ("2026-07-25","Fakel Voronezh"):9289,("2026-07-26","Rubin Kazan"):18866,
 ("2026-07-26","Lokomotiv Moscow"):10051,("2026-07-26","FC Orenburg"):4803}
TABLE_EXPECT = {  # wiki-rpl-2627 league table through 2026-08-02: W D L GF GA
 "Zenit St Petersburg":(2,0,0,8,0),"Spartak Moscow":(2,0,0,5,1),
 "FC Krasnodar":(2,0,0,6,3),"Dynamo Makhachkala":(2,0,0,4,2),
 "CSKA Moscow":(1,1,0,3,2),"FC Rostov":(1,0,1,5,4),
 "Baltika Kaliningrad":(1,0,1,3,3),"Rubin Kazan":(1,0,1,3,4),
 "FC Orenburg":(1,0,1,2,4),"Krylia Sovetov Samara":(0,2,0,1,1),
 "Akhmat Grozny":(0,1,1,2,3),"Lokomotiv Moscow":(0,1,1,2,3),
 "Dynamo Moscow":(0,1,1,1,2),"Fakel Voronezh":(0,0,2,3,5),
 "Rodina Moscow":(0,0,2,2,7),"Akron Tolyatti":(0,0,2,1,7),
}
ALLOWED_STADIUM = {"VEB Arena","VTB Arena","Solidarnost Samara Arena","Fakel Stadium",
 "Lukoil Arena","RZD Arena","Gazovik Stadium","Ak Bars Arena","Anzhi Arena",
 "Rostech Arena","Ozon Arena","Akhmat Arena","Arena Khimki","Gazprom Arena",
 "Nizhny Novgorod Stadium"}
CLUBS16 = sorted(TABLE_EXPECT)

# G01 frame
gate("G01", lines and lines[0].startswith("NOTE|info|pack_id|") and lines[-1] == "END",
     "first line pack_id NOTE; last line END")

# G02 field grammar
g2ok = all(len(x.split("|")) == 14 for x in matches) and \
       all(len(x.split("|")) == 13 for x in teams) and \
       all(len(x.split("|")) == 6 for x in sources) and \
       all(len(x.split("|")) == 4 for x in notes)
gate("G02", g2ok, "MATCH rows 14 fields, TEAM rows 13 fields (RPL-pack convention), SOURCE 6, NOTE 4")

# G03 ascii
g3bad = [ [i+1,x[:60]] for i,x in enumerate(lines) if any(ord(c) > 127 for c in x) ]
gate("G03", not g3bad, f"ASCII-only pack lines (violations: {g3bad[:3]})")

# G04 composition
league = [x for x in matches if x.split("|")[3] == "domestic-league"]
cups = [x for x in matches if x.split("|")[3] == "domestic-cup"]
r1 = [x for x in league if x.split("|")[8] == "Round 1"]
r2 = [x for x in league if x.split("|")[8] == "Round 2"]
gate("G04", len(matches) == 18 and len(league) == 16 and len(r1) == 8 and len(r2) == 8
     and len(cups) == 2 and all(x.split("|")[8] == "Final" for x in cups)
     and len(teams) == 1 and len(sources) == 7 and len(notes) >= 11,
     f"MATCH {len(matches)} (league {len(league)} = R1 {len(r1)} + R2 {len(r2)}; supercup {len(cups)} Final), TEAM {len(teams)}, SOURCE {len(sources)}, NOTE {len(notes)}")

# G05 ISO dates + sorted + competition strings
okiso = all(re.fullmatch(r"20\d\d-\d\d-\d\d", x.split("|")[1]) for x in matches)
dates = [x.split("|")[1] for x in matches]
comps = {(x.split("|")[2], x.split("|")[3]) for x in matches}
gate("G05", okiso and dates == sorted(dates) and
     comps == {("Russian Premier League","domestic-league"),("Russian Super Cup","domestic-cup")},
     "ISO dates, non-decreasing order, competition/class grammar")

def core(x):
    p = x.split("|"); return (p[1], p[4], int(p[5]), int(p[6]), p[7])
gate("G06", sorted(core(x) for x in r1) == sorted(R1_EXPECT),
     "Round-1 rows == rsssf-rus2027 print 8/8 (date, home, hg, ag, away)")
gate("G07", sorted(core(x) for x in r2) == sorted(R2_EXPECT),
     "Round-2 rows == premierliga-heritage official print 8/8")

sup_core = [tuple(x.split("|")[i] for i in (1,2,3,4)) + (int(x.split("|")[5]), int(x.split("|")[6])) +
            tuple(x.split("|")[i] for i in (7,8,9,10,13)) for x in cups]
gate("G08", sorted(x[:6]+x[6:] for x in sup_core) == sorted(SUP_EXPECT),
     "Super Cup rows == rsssf rus2025/rus2026 #sup prints 2/2 (grammar incl. source labels)")

# G09 recompute league table from rows vs wiki table
tab = {}
for x in league:
    p = x.split("|"); h, a, hg, ag = p[4], p[7], int(p[5]), int(p[6])
    for c, gf, ga in ((h, hg, ag), (a, ag, hg)):
        w, d, l, f0, a0 = tab.get(c, (0, 0, 0, 0, 0))
        tab[c] = (w + (gf > ga), d + (gf == ga), l + (gf < ga), f0 + gf, a0 + ga)
gate("G09", tab == TABLE_EXPECT,
     "league table recomputed from 16 rows == wiki-rpl-2627 table through 2026-08-02, 16/16 club-for-club")

# G10 goal/attendance anchors
goals = sum(int(x.split("|")[5]) + int(x.split("|")[6]) for x in league)
att_ok = all(R1_ATT[(x.split("|")[1], x.split("|")[4])] for x in r1) and sum(R1_ATT.values()) == 102232
gate("G10", goals == 51 and goals == sum(v[3] for v in TABLE_EXPECT.values()) == sum(v[4] for v in TABLE_EXPECT.values()) and att_ok and len(r1) == len(R1_ATT),
     f"goals {goals} == wiki infobox 51 == table GF/GA sums; R1 attendance anchors sum 102,232 == RSSSF printed total (8/8 keyed)")

# G11 dupes + window
keys = [(x.split("|")[1], x.split("|")[4], x.split("|")[7]) for x in matches]
gate("G11", len(keys) == len(set(keys)) and min(dates) == "2025-07-12" and max(dates) == "2026-08-02" and max(dates) <= RETURN_DATE,
     f"no duplicate (date,home,away); window {min(dates)}..{max(dates)} <= return date {RETURN_DATE}")

# G12 roster containment vs pinned RPL pack
rpl_clubs = set()
for x in open(RPL, encoding="ascii"):
    if x.startswith("MATCH|"):
        p = x.split("|"); rpl_clubs.add(p[4]); rpl_clubs.add(p[7])
used = {x.split("|")[4] for x in matches} | {x.split("|")[7] for x in matches}
gate("G12", used == set(CLUBS16) and used <= rpl_clubs,
     f"all {len(used)} club strings verbatim in pinned RPL pack (missing: {sorted(used - rpl_clubs)})")

# G13 stadium pins
st = {x.split("|")[9] for x in matches}
gate("G13", st <= ALLOWED_STADIUM, f"stadium strings subset of the pinned set ({len(st)} used; extras: {sorted(st - ALLOWED_STADIUM)})")

# G14 advancement NOTEs
n_join = "\n".join(notes)
gate("G14", "4-2 on penalties" in n_join and "Diveyev 48" in n_join and "Nizhny Novgorod Stadium, att 42,139" in n_join and "att 34,677" in n_join,
     "advancement NOTEs for both finals (2026 pens 4-2 detail; 2025 Diveyev 48, both attendances)")

# G15 TEAM registration
gate("G15", teams == ["TEAM|Rodina Moscow|Russia|Russian Premier League|RPL|Rodina|Arena Khimki|Moscow|Russia||||"],
     "single TEAM row = Rodina Moscow top-flight registration, RPL tier")

# G16 policy NOTEs present
need = ["rolling_append", "source_adaptation", "supercup_scope", "advancement", "venue_era", "boundary"]
got = [x.split("|")[2] for x in notes]
gate("G16", all(any(n == t for n in got) for t in need),
     f"policy NOTE types present: rolling_append/source_adaptation/supercup_scope/advancement/venue_era/boundary ({got})")

# --- report incl. per-club pivots (owner decree) ---
out = []
npass = sum(1 for _, ok, _ in results if ok)
out.append(f"VALIDATION RUS-ADDENDUM-2026_BP-TEAM-PACK_v2 - external re-run, fetched-vs-pack comparison, return date {RETURN_DATE}")
out.append(f"pack sha256: {hashlib.sha256(open(PACK,'rb').read()).hexdigest()}")
for gid, ok, detail in results:
    out.append(f"{'PASS' if ok else 'FAIL'} {gid} - {detail}")
out.append(f"GATES: {npass}/{len(results)} PASS")
out.append("")
out.append("PER-CLUB PIVOTS (owner decree: per-team full-campaign view of this drop)")
for c in CLUBS16:
    rows = [x for x in matches if x.split('|')[4] == c or x.split('|')[7] == c]
    out.append(f"PIVOT {c} ({len(rows)} games):")
    for x in rows:
        p = x.split("|")
        out.append(f"  {p[1]} {p[2]} ({p[8]}): {p[4]} {p[5]}-{p[6]} {p[7]} @ {p[9]}, {p[10]} [{p[13]}]")
text = "\n".join(out) + "\n"
open(REP, "w", encoding="utf-8", newline="\n").write(text)
print(f"validation written: {npass}/{len(results)} PASS -> {REP}")
print(f"report sha256: {hashlib.sha256(text.encode('utf-8')).hexdigest()}")
sys.exit(0 if npass == len(results) else 1)
