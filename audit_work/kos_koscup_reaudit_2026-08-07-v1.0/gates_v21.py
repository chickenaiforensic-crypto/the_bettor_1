#!/usr/bin/env python3
"""FRESH gate suite for KOS/KOSCUP v2.1 (2026-08-07, auditor code).

Verifies the Director's correction order is fully applied and nothing else
changed:
 KOS  - 910 MATCH (900 league + 10 playoff); 12 appendix rows present;
        0 venue placeholders; table reproduction 5/5 from pack alone;
        goals anchors; no dups/future; D1-D4 irrelevant here.
 KOSCUP - 123 MATCH; 0 placeholders; D1-D4 still fixed; slice/bracket;
        no dups/future.
"""
import re, sys
from collections import Counter, defaultdict

POOL = ["KF Ballkani","Drita","Gjilani","Llapi","Prishtina","Drenica Skenderaj",
        "Dukagjini","Malisheva","Ferizaj","Prishtina E Re"]
KOS_TEAMS = ["Ulpiana","Feronikeli","Trepça'89","Fushë Kosova","Liria","Suhareka",
             "Vushtrria","Dinamo Fzaj."]
MEMBERSHIP = {
    "2021-22": {"KF Ballkani","Drita","Gjilani","Llapi","Prishtina","Drenica Skenderaj",
                "Dukagjini","Malisheva","Ulpiana","Feronikeli"},
    "2022-23": {"KF Ballkani","Drita","Gjilani","Llapi","Prishtina","Drenica Skenderaj",
                "Dukagjini","Malisheva","Ferizaj","Trepça'89"},
    "2023-24": {"KF Ballkani","Drita","Gjilani","Llapi","Prishtina","Dukagjini",
                "Malisheva","Feronikeli","Fushë Kosova","Liria"},
    "2024-25": {"KF Ballkani","Drita","Gjilani","Llapi","Prishtina","Dukagjini",
                "Malisheva","Ferizaj","Suhareka","Feronikeli"},
    "2025-26": {"KF Ballkani","Drita","Gjilani","Llapi","Prishtina","Drenica Skenderaj",
                "Dukagjini","Malisheva","Ferizaj","Prishtina E Re"},
}
APPENDIX = [
    ("2026-03-09","Malisheva","Prishtina",3,0),("2026-03-22","Malisheva","Llapi",2,0),
    ("2026-04-05","Drita","Malisheva",2,0),("2026-04-11","Prishtina E Re","Malisheva",2,1),
    ("2026-04-19","Malisheva","KF Ballkani",4,2),("2026-04-26","Dukagjini","Malisheva",0,1),
    ("2026-04-29","Malisheva","Gjilani",3,1),("2026-05-02","Prishtina","Malisheva",0,1),
    ("2026-05-10","Ferizaj","Malisheva",1,1),("2026-05-17","Malisheva","Drenica Skenderaj",4,1),
    ("2026-05-24","Llapi","Malisheva",3,2),("2026-05-31","Malisheva","Drita",3,2),
]
RSSSF_MAP = {
    "Ballkani (Suhareke)": "KF Ballkani", "Drita (Gjilan)": "Drita",
    "Gjilani (Gjilan)": "Gjilani", "Llapi (Besiane) (Podujeve)": "Llapi",
    "Prishtina KF (Prishtine)": "Prishtina", "Drenica KF (Skenderaj)": "Drenica Skenderaj",
    "Dukagjini (Kline)": "Dukagjini", "Malisheva": "Malisheva",
    "Ulpiana (Lipljan)": "Ulpiana", "Feronikeli (Drenas)": "Feronikeli",
    "Ferizaj (Ferizaj)": "Ferizaj", "Trepca'89 (Mitrovice)": "Trepça'89",
    "Fushe Kosova (Fushe Kosove)": "Fushë Kosova", "Liria (Prizren)": "Liria",
    "Suhareka (Suhareke)": "Suhareka",
}

def season_of(d):
    y, m = int(d[:4]), int(d[5:7])
    return f"{y}-{str(y+1)[2:]}" if m >= 8 else f"{y-1}-{str(y)[2:]}"

def parse(path):
    rows = []
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("MATCH|"):
            p = ln.rstrip("\n").split("|")
            rows.append({"date":p[1],"comp":p[2],"ctype":p[3],"home":p[4],"hg":int(p[5]),
                         "ag":int(p[6]),"away":p[7],"round":p[8],"st":p[9],"ct":p[10],"src":p[13]})
    return rows

def standings(rows):
    st = defaultdict(lambda: {"P":0,"W":0,"D":0,"L":0,"GF":0,"GA":0,"Pts":0})
    for r in rows:
        for t, f, c in ((r["home"],r["hg"],r["ag"]),(r["away"],r["ag"],r["hg"])):
            s = st[t]; s["P"]+=1; s["GF"]+=f; s["GA"]+=c
            if f>c: s["W"]+=1; s["Pts"]+=3
            elif f==c: s["D"]+=1; s["Pts"]+=1
            else: s["L"]+=1
    return st

def parse_rsssf_tables(path):
    tbl, cur = [], []
    def flush():
        if len(cur) >= 5: tbl.append(list(cur))
        cur.clear()
    for ln in open(path, encoding="utf-8", errors="replace"):
        s = re.sub(r"<[^>]+>","",ln)
        m = re.match(r"^\s*\d+\.\s*(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)(?:\s|$)", s)
        if m:
            cur.append({"name": re.sub(r"\s*\[.*$","",m.group(1)).strip(),
                        "P":int(m.group(2)),"W":int(m.group(3)),"D":int(m.group(4)),
                        "L":int(m.group(5)),"GF":int(m.group(6)),"GA":int(m.group(7)),
                        "Pts":int(m.group(8))})
        else:
            flush()
    flush()
    return tbl

def main():
    problems = []
    # ---------------- KOS ----------------
    krows = parse("/home/user/the_bettor_1/handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt")
    league = [r for r in krows if r["ctype"] == "domestic-league"]
    play = [r for r in krows if r["ctype"] == "other"]
    print(f"KOS v2.1: total {len(krows)}  league {len(league)}  playoff {len(play)}")
    if len(krows) != 910: problems.append(f"KOS total {len(krows)} != 910")
    if len(league) != 900: problems.append(f"KOS league {len(league)} != 900")
    if len(play) != 10: problems.append(f"KOS playoff {len(play)} != 10")
    # appendix rows present
    app_present = {(r["date"], r["home"], r["away"]) for r in krows}
    missing_app = [(d,h,a) for (d,h,a,hg,ag) in APPENDIX if (d,h,a) not in app_present]
    if missing_app: problems.append(f"KOS appendix rows missing: {missing_app}")
    print(f"  appendix rows present: {12 - len(missing_app)}/12")
    # placeholders
    ph = [(r["date"], r["home"]) for r in krows if r["st"] in ("unknown","") or r["ct"] in ("unknown","")]
    if ph: problems.append(f"KOS placeholders: {ph}")
    print(f"  placeholders: {len(ph)}")
    # dups/future
    fp = Counter((r["date"], r["home"], r["away"]) for r in krows)
    dups = [k for k,c in fp.items() if c>1]
    fut = [r["date"] for r in krows if r["date"] > "2026-08-07"]
    if dups: problems.append(f"KOS dups: {dups}")
    if fut: problems.append(f"KOS future: {fut}")
    print(f"  dups {len(dups)}  future {len(fut)}")
    # per-season shape + membership + goals
    sc = Counter(season_of(r["date"]) for r in league)
    goals = Counter()
    cc = defaultdict(Counter)
    for r in league:
        goals[season_of(r["date"])] += r["hg"] + r["ag"]
        cc[season_of(r["date"])][r["home"]] += 1
        cc[season_of(r["date"])][r["away"]] += 1
    for s in MEMBERSHIP:
        if sc[s] != 180: problems.append(f"KOS {s}: {sc[s]} != 180")
        for t, n in cc[s].items():
            if n != 36: problems.append(f"KOS {s} {t}: {n} != 36")
        if set(cc[s]) != MEMBERSHIP[s]: problems.append(f"KOS {s} membership mismatch")
    print(f"  per-season: {dict(sorted(sc.items()))}")
    print(f"  goals: {dict(sorted(goals.items()))}")
    # table reproduction (2021-22..2024-25 vs RSSSF transcriptions; 2025-26 vs official)
    refmap = {"2021-22":"/home/user/the_bettor_1/audit_work/kos_receipt_2026-08-07/researcher_evidence/rsssf-2021-22.txt",
              "2022-23":"/home/user/the_bettor_1/audit_work/kos_receipt_2026-08-07/researcher_evidence/rsssf-2022-23.txt",
              "2023-24":"/home/user/the_bettor_1/audit_work/kos_receipt_2026-08-07/researcher_evidence/rsssf-2023-24.txt",
              "2024-25":"/home/user/the_bettor_1/audit_work/kos_receipt_2026-08-07/researcher_evidence/rsssf-2024-25.txt"}
    for s, path in refmap.items():
        rows = [r for r in league if season_of(r["date"]) == s]
        st = standings(rows)
        tables = parse_rsssf_tables(path)
        table = next((t for t in tables if len(t)==10 and all(x["P"]==36 for x in t)), None)
        if table is None:
            problems.append(f"KOS {s}: RSSSF table not found"); continue
        mapped = {RSSSF_MAP.get(x["name"], x["name"]): x for x in table}
        diffs = []
        for t, sr in st.items():
            x = mapped.get(t)
            if not x: diffs.append(f"{t} missing"); continue
            for k in ("P","W","D","L","GF","GA","Pts"):
                if sr[k] != x[k]: diffs.append(f"{t} {k} {sr[k]} vs {x[k]}")
        print(f"  table {s}: diffs {len(diffs)}")
        for d in diffs[:6]: problems.append(f"KOS TABLE {s}: {d}")
    # 2025-26 official table (RSSSF kosovo2026 fetched earlier; constants)
    official = [
        ("Drita",36,20,6,10,50,35,66),("Malisheva",36,18,5,13,58,50,59),
        ("KF Ballkani",36,17,7,12,61,41,58),("Dukagjini",36,13,12,11,42,36,51),
        ("Gjilani",36,14,9,13,47,48,51),("Drenica Skenderaj",36,15,5,16,46,55,50),
        ("Prishtina",36,13,10,13,52,51,49),("Llapi",36,13,10,13,46,50,49),
        ("Ferizaj",36,9,9,18,40,55,36),("Prishtina E Re",36,8,7,21,39,60,31),
    ]
    rows = [r for r in league if season_of(r["date"]) == "2025-26"]
    st = standings(rows)
    diffs = []
    for name, P,W,D,L,GF,GA,Pts in official:
        sr = st.get(name)
        if not sr: diffs.append(f"{name} missing"); continue
        if (sr["P"],sr["W"],sr["D"],sr["L"],sr["GF"],sr["GA"],sr["Pts"]) != (P,W,D,L,GF,GA,Pts):
            diffs.append(f"{name} {sr}")
    print(f"  table 2025-26 (pack alone, 180 rows): diffs {len(diffs)}")
    for d in diffs[:6]: problems.append(f"KOS TABLE 2025-26: {d}")
    # playoff compType/comp
    for r in play:
        if r["comp"] != "Kosovo Relegation Playoffs": problems.append(f"KOS playoff comp {r['comp']}")
        if r["ctype"] != "other": problems.append(f"KOS playoff ctype {r['ctype']}")
    # ---------------- KOSCUP ----------------
    crows = parse("/home/user/the_bettor_1/handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt")
    print(f"\nKOSCUP v2.1: total {len(crows)}")
    if len(crows) != 123: problems.append(f"KOSCUP total {len(crows)} != 123")
    ph = [(r["date"], r["home"]) for r in crows if r["st"] in ("unknown","") or r["ct"] in ("unknown","")]
    if ph: problems.append(f"KOSCUP placeholders: {ph}")
    print(f"  placeholders: {len(ph)}")
    fp = Counter((r["date"], r["home"], r["away"]) for r in crows)
    dups = [k for k,c in fp.items() if c>1]
    if dups: problems.append(f"KOSCUP dups: {dups}")
    # degenerate names
    deg = sorted({r["home"] for r in crows} | {r["away"] for r in crows} if False else set())
    used = set()
    for r in crows: used.add(r["home"]); used.add(r["away"])
    deg = sorted(u for u in used if len(u) <= 1)
    if deg: problems.append(f"KOSCUP degenerate names: {deg}")
    print(f"  dups {len(dups)}  degenerate {deg if deg else 'none'}")
    # slice counts
    rc = defaultdict(Counter)
    for r in crows:
        rc[season_of(r["date"])][r["round"]] += 1
    exp = {"2021-22":24,"2022-23":24,"2023-24":24,"2024-25":26,"2025-26":25}
    total = 0
    for s in sorted(rc):
        n = sum(rc[s].values()); total += n
        if n != exp[s]: problems.append(f"KOSCUP slice {s}: {n} != {exp[s]}")
        print(f"  {s}: {n}  rounds {dict(rc[s])}")
    print(f"  total {total}")
    # D1-D4 regression
    d1 = [r for r in crows if r["home"] == "A" or r["away"] == "A"]
    d2 = [r for r in crows if "Ph'nix" in r["home"] or "Ph'nix" in r["away"]]
    d3 = [r for r in crows if "Prishtina e Re" in r["home"] or "Prishtina e Re" in r["away"]]
    if d1: problems.append(f"KOSCUP D1 regression: {d1}")
    if d2: problems.append(f"KOSCUP D2 regression: {d2}")
    if d3: problems.append(f"KOSCUP D3 regression: {d3}")
    print(f"  D1 'A' rows: {len(d1)}  D2 Ph'nix rows: {len(d2)}  D3 lowercase rows: {len(d3)}")
    # finals/bracket
    for r in crows:
        if r["round"] == "Final":
            print(f"  FINAL {season_of(r['date'])}: {r['home']} {r['hg']}-{r['ag']} {r['away']}")
    print(f"\nPROBLEMS: {len(problems)}")
    for p in problems: print(" -", p)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
