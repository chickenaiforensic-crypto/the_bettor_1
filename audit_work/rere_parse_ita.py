#!/usr/bin/env python3
import re, html, unicodedata, datetime, collections, sys, os
import json

REF = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/REFERENCE/rsssf-ref"
MONTHS = {m: i+1 for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

ITA_ALIASES = {
    "ac milan": "Milan", "milan ac": "Milan", "milan": "Milan",
    "fc internazionale": "Inter", "internazionale": "Inter", "inter": "Inter",
    "ssc napoli": "Napoli", "napoli": "Napoli",
    "juventus fc": "Juventus", "juventus": "Juventus",
    "ss lazio": "Lazio", "lazio": "Lazio",
    "as roma": "Roma", "roma": "Roma",
    "ac fiorentina": "Fiorentina", "fiorentina": "Fiorentina",
    "atalanta bc": "Atalanta", "atalanta": "Atalanta",
    "hellas verona fc": "Verona", "hellas verona": "Verona", "verona": "Verona",
    "torino fc": "Torino", "torino": "Torino",
    "us sassuolo": "Sassuolo", "sassuolo": "Sassuolo",
    "udinese calcio": "Udinese", "udinese": "Udinese",
    "bologna fc": "Bologna", "bologna": "Bologna",
    "empoli fc": "Empoli", "empoli": "Empoli",
    "uc sampdoria": "Sampdoria", "sampdoria": "Sampdoria",
    "spezia calcio": "Spezia", "spezia": "Spezia",
    "us salernitana": "Salernitana", "salernitana": "Salernitana",
    "cagliari calcio": "Cagliari", "cagliari": "Cagliari",
    "genoa cfc": "Genoa", "genoa": "Genoa",
    "venezia fc": "Venezia", "venezia": "Venezia",
    "ac monza": "Monza", "monza": "Monza",
    "us lecce": "Lecce", "lecce": "Lecce",
    "us cremonese": "Cremonese", "cremonese": "Cremonese",
    "frosinone calcio": "Frosinone", "frosinone": "Frosinone",
    "como 1907": "Como", "como": "Como",
    "parma calcio 1913": "Parma", "parma": "Parma",
}

RESOLVER = {norm(k): v for k, v in ITA_ALIASES.items()}

def resolve(name):
    n = norm(name)
    if n in RESOLVER: return RESOLVER[n]
    # strip FC, AC, etc
    n2 = re.sub(r'^(fc|ac|ss|as|us|uc)\s*', '', n)
    if n2 in RESOLVER: return RESOLVER[n2]
    return None

DATE_RE = re.compile(r'\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2})')
MATCH_RE = re.compile(r'^\s*(.*?)\s+(\d{1,2})\s*-\s*(\d{1,2})\s+(.*?)\s*$')

def parse_ita_file(fname, y1):
    y2 = y1 + 1
    path = f"{REF}/{fname}"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return []
    with open(path, encoding='utf-8-sig', errors='replace') as f:
        text = html.unescape(f.read())
    lines = text.splitlines()
    out = []
    section = 'other'
    cur_date = None
    
    def resolve_date(mon, day):
        return datetime.date(y2 if mon <= 6 else y1, mon, day)

    for line in lines:
        line = line.strip()
        low = line.lower()
        if 'name="seriea"' in low:
            section = 'league'
            continue
        if '</pre>' in low and section == 'league':
            section = 'other'
            continue
        
        if section == 'league':
            mr = re.match(r'^round\s+(\d{1,2})', low)
            if mr:
                m = DATE_RE.search(line)
                if m:
                    cur_date = resolve_date(MONTHS[m.group(1)], int(m.group(2)))
                continue
            
            m = DATE_RE.search(line)
            if m and line.startswith('['):
                cur_date = resolve_date(MONTHS[m.group(1)], int(m.group(2)))
                continue
            
            mm = MATCH_RE.match(line)
            if mm:
                h = resolve(mm.group(1).strip())
                a = resolve(mm.group(4).strip())
                if h and a and cur_date:
                    out.append({
                        "date": cur_date.isoformat(),
                        "home": h,
                        "away": a,
                        "hg": int(mm.group(2)),
                        "ag": int(mm.group(3)),
                        "comp": "Italy Serie A"
                    })
    return out

def load_pack_matches(path):
    sys.path.insert(0, 'audit_work')
    from pack_parse import parse_pack
    p = parse_pack(path)
    return p['matches']

def main():
    pack_path = "handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt"
    pack_matches = load_pack_matches(pack_path)
    
    seasons = [(2021, "ital2022.txt"), (2022, "ital2023.txt"), (2023, "ital2024.txt"), (2024, "ital2025.txt"), (2025, "ital2026.txt")]
    
    all_rsssf = []
    for y1, fn in seasons:
        s_matches = parse_ita_file(fn, y1)
        print(f"RSSSF {y1}-{y1+1}: {len(s_matches)} matches parsed")
        all_rsssf.extend(s_matches)
    
    # Comparison
    rsssf_map = collections.defaultdict(list)
    for m in all_rsssf:
        rsssf_map[(m['date'], m['home'], m['away'])].append((m['hg'], m['ag']))
    
    exact = 0
    mismatch = []
    missing = []
    
    # Filter pack matches for Serie A only for this check
    ita_pack = [m for m in pack_matches if m['competitionName'] == "Italy Serie A"]
    
    for m in ita_pack:
        k = (m['dateISO'], m['homeName'], m['awayName'])
        if k in rsssf_map:
            if any(hg == m['homeGoals'] and ag == m['awayGoals'] for hg, ag in rsssf_map[k]):
                exact += 1
            else:
                mismatch.append((m, rsssf_map[k]))
        else:
            missing.append(m)
            
    print(f"\nITA Audit Results:")
    print(f"  Pack matches (Serie A): {len(ita_pack)}")
    print(f"  RSSSF matches parsed: {len(all_rsssf)}")
    print(f"  EXACT: {exact}")
    print(f"  MISMATCH: {len(mismatch)}")
    print(f"  MISSING in RSSSF: {len(missing)}")
    
    if mismatch:
        print("\nMismatches (first 5):")
        for p, r in mismatch[:5]:
            print(f"  {p['dateISO']} {p['homeName']} {p['homeGoals']}-{p['awayGoals']} {p['awayName']} vs RSSSF {r}")
            
    if missing:
        print("\nMissing in RSSSF (first 5):")
        for p in missing[:5]:
            print(f"  {p['dateISO']} {p['homeName']} vs {p['awayName']}")

    # Table reproduction check for last season
    print("\nTable Reproduction ITA 2025-26:")
    last_season_matches = [m for m in ita_pack if "2025-07-01" <= m['dateISO'] <= "2026-06-30"]
    pts = collections.defaultdict(int)
    gd = collections.defaultdict(int)
    for m in last_season_matches:
        h, a = m['homeName'], m['awayName']
        hg, ag = m['homeGoals'], m['awayGoals']
        if hg > ag: pts[h]+=3
        elif hg == ag: pts[h]+=1; pts[a]+=1
        else: pts[a]+=3
        gd[h]+=hg-ag; gd[a]+=ag-hg
    sorted_table = sorted(pts.items(), key=lambda x: (-x[1], -gd[x[0]], x[0]))
    for i, (team, p) in enumerate(sorted_table, 1):
        print(f"  {i:2}. {team:20} {p:2} GD {gd[team]:2}")

if __name__ == "__main__":
    main()
