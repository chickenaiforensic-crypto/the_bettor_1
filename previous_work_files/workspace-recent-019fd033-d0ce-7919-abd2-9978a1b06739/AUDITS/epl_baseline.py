#!/usr/bin/env python3
"""epl_baseline.py - auditor baseline builder for EPL seasons from local RSSSF pages.
Parses rsssf-ref/eng<Y>.txt (#premier section) -> audit-baseline/epl-<season>.json
Gate per season: 380 matches, 0 date+pair dupes, printed Final Table reproduced 20/20
on W-D-L-GF-GA from round listings (point deductions reported separately, never merged).
PASS history (2026-08-03): eng2022/2023/2024/2025 = 4x PASS (incl. 2023-24 abandoned
Bournemouth-Luton [2023-12-16, cardiac arrest Tom Lockyer] excluded, replay counted;
Everton -8 / Nottingham Forest -4 deductions reported, not table-blocking).
Gotchas encoded: 'Wolverhampton' overflows the 12-char name column (single-space before
score); top/bottom printed tables are excluded by the leading-date guard on round parse
and the [A-Za-z] start guard on team tokens; abandoned games recorded as 'abd'; replay
suffix lines '[replay]' (etc.) accepted as valid results; date headers [Mon D] with
Jul-Dec -> season start year, Jan-Jun -> next year.
"""
import re, json, sys, os

MONTHS = {m: i+1 for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])}
ALIAS = {'Manchester C':'Manchester City','Manchester U':'Manchester United','Crystal P':'Crystal Palace',
'Sheffield U':'Sheffield United','Luton':'Luton Town','Ipswich':'Ipswich Town','Nottingham':'Nottingham Forest',
'Wolverhampton':'Wolverhampton Wanderers','West Ham':'West Ham United','Newcastle':'Newcastle United',
'Leeds':'Leeds United','Leicester':'Leicester City','Norwich':'Norwich City','Brighton':'Brighton & Hove Albion',
'Tottenham':'Tottenham Hotspur','Bournemouth':'AFC Bournemouth','Fulham':'Fulham','Arsenal':'Arsenal',
'Aston Villa':'Aston Villa','Everton':'Everton','Liverpool':'Liverpool','Chelsea':'Chelsea','Burnley':'Burnley',
'Brentford':'Brentford','Watford':'Watford','Southampton':'Southampton'}
SEASONS = {'eng2022': 2021, 'eng2023': 2022, 'eng2024': 2023, 'eng2025': 2024}

def section(path):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    a = b = 0
    for i, l in enumerate(lines):
        if 'name="premier"' in l: a = i
        elif a and 'name="cups"' in l: b = i; break
    return [l.rstrip('\r') for l in lines[a:b]]

def build(fn, y0):
    sec = section(f'rsssf-ref/{fn}.txt')
    matches, cur, rnd, anomalies = [], None, None, []
    for l in sec:
        m = re.match(r'^Round (\d+)', l)
        if m: rnd = int(m.group(1)); continue
        m = re.match(r'^\[([A-Z][a-z]{2}) (\d{1,2})\]$', l.strip())
        if m and m.group(1) in MONTHS:
            mo = MONTHS[m.group(1)]; yr = y0 if mo >= 7 else y0+1
            cur = f"{yr}-{mo:02d}-{int(m.group(2)):02d}"; continue
        if re.search(r'\sabd\s', l) and cur:
            note = re.search(r'\[([^\]]*)\]', l)
            anomalies.append(('ABANDONED', rnd, cur, note.group(1)[:100] if note else '')); continue
        m = re.match(r"^([A-Za-z][A-Za-z .&']*?)\s+(\d+)-(\d+)\s+([A-Za-z][A-Za-z .&']*?)(?:\s+\[[^\]]*\])?\s*$", l)
        if m and cur and rnd:
            h, hg, ag, a = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4).strip()
            if h not in ALIAS or a not in ALIAS: anomalies.append(('UNKNOWN', h, a)); continue
            matches.append(dict(round=rnd, date=cur, home=ALIAS[h], hg=hg, ag=ag, away=ALIAS[a]))
    tbl = {}
    for l in sec:
        m = re.match(r"^\s*(\d+)\.([A-Za-z][A-Za-z .&']*?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-\s*(\d+)\s+(-?\d+)", l)
        if m: tbl.setdefault(m.group(2).strip(), dict(p=int(m.group(3)), w=int(m.group(4)), d=int(m.group(5)),
                                                       l=int(m.group(6)), gf=int(m.group(7)), ga=int(m.group(8)), pts=int(m.group(9))))
    der = {}
    for mt in matches:
        for t, gf, ga in ((mt['home'], mt['hg'], mt['ag']), (mt['away'], mt['ag'], mt['hg'])):
            s = der.setdefault(t, dict(p=0, w=0, d=0, l=0, gf=0, ga=0))
            s['p'] += 1; s['gf'] += gf; s['ga'] += ga
            s['w' if gf > ga else 'd' if gf == ga else 'l'] += 1
    exact = sum(1 for t, r in tbl.items() if t in der and
                tuple(der[t][k] for k in ('p','w','d','l','gf','ga')) == tuple(r[k] for k in ('p','w','d','l','gf','ga')))
    ded = {t: tbl[t]['pts'] - (der[t]['w']*3 + der[t]['d']) for t in tbl if t in der and tbl[t]['pts'] != der[t]['w']*3 + der[t]['d']}
    seen, dups = set(), 0
    for mt in matches:
        k = (mt['date'], mt['home'], mt['away'])
        if k in seen: dups += 1
        seen.add(k)
    status = 'PASS' if len(matches) == 380 and exact == 20 and dups == 0 else 'CHECK'
    return status, matches, tbl, ded, anomalies, exact, dups

if __name__ == '__main__':
    os.makedirs('audit-baseline', exist_ok=True)
    allok = True
    for fn, y0 in SEASONS.items():
        status, matches, tbl, ded, anomalies, exact, dups = build(fn, y0)
        if status != 'PASS': allok = False
        print(f"{fn} ({y0}-{str(y0+1)[2:]}): matches={len(matches)} table-exact={exact}/20 dups={dups} pts-adj={ded} anomalies={len(anomalies)} -> {status}")
        for an in anomalies: print('   ', an)
        if status == 'PASS':
            out = dict(season=f'{y0}-{str(y0+1)[2:]}', source=f'rsssf-{fn}-premier',
                       note='380 matches; printed table reproduced 20/20 W-D-L-GF-GA from round listings; deductions separate',
                       deductions=ded, anomalies=anomalies, matches=matches)
            json.dump(out, open(f'audit-baseline/epl-{y0}-{str(y0+1)[2:]}.json', 'w'), indent=1)
    print('ALL LOCKED' if allok else 'NOT ALL LOCKED')
    sys.exit(0 if allok else 1)
