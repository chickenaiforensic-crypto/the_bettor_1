#!/usr/bin/env python3
# RPL full-span pack gate: recompute 5 season tables from pack league rows and
# compare profile-exact vs RSSSF rus{2022..2026} printed final tables; plus
# playoff-leg existence + exact score/date check vs RSSSF prorel sections.
import re, unicodedata, sys, json

PACK = '/home/user/AUDIT-OVERRIDE-2026-08-04/RPL-2021-2026.txt'
RSS = {s: f'/home/user/rsssf-ref/rus{y}.txt' for s, y in
       [('2021-22', 2022), ('2022-23', 2023), ('2023-24', 2024), ('2024-25', 2025), ('2025-26', 2026)]}
SPAN = {'2021-22': ('2021-07-01', '2022-06-30'), '2022-23': ('2022-07-01', '2023-06-30'),
        '2023-24': ('2023-07-01', '2024-06-30'), '2024-25': ('2024-07-01', '2025-06-30'),
        '2025-26': ('2025-07-01', '2026-06-30')}

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

# ---- parse pack ----
league = {s: [] for s in RSS}; playoffs = {s: [] for s in RSS}
with open(PACK, encoding='utf-8') as f:
    for ln in f:
        if not ln.startswith('MATCH|'): continue
        p = ln.rstrip('\n').split('|')
        date, comp, ctype, home, hg, ag, away = p[1], p[2], p[3], p[4], int(p[5]), int(p[6]), p[7]
        for s, (a, b) in SPAN.items():
            if a <= date <= b:
                if comp == 'Russian Premier League': league[s].append((date, home, hg, ag, away))
                elif comp == 'Russian Relegation Playoffs': playoffs[s].append((date, home, hg, ag, away))
                break

errs = []
for s in RSS:
    if len(league[s]) != 240: errs.append(f'{s}: league rows {len(league[s])} != 240')
    if len(playoffs[s]) != 4: errs.append(f'{s}: playoff rows {len(playoffs[s])} != 4')
print('row counts per season (league/playoff):', {s: f"{len(league[s])}+{len(playoffs[s])}" for s in RSS})

def build_table(rows):
    T = {}
    for _, h, hg, ag, a in rows:
        for t in (h, a):
            T.setdefault(t, [0, 0, 0, 0, 0, 0])  # Pld W D L GF GA
        T[h][0] += 1; T[a][0] += 1
        T[h][4] += hg; T[h][5] += ag; T[a][4] += ag; T[a][5] += hg
        if hg > ag: T[h][1] += 1; T[a][3] += 1
        elif hg < ag: T[a][1] += 1; T[h][3] += 1
        else: T[h][2] += 1; T[a][2] += 1
    return T

# ---- parse RSSSF final table: FIRST run of 16 sequentially-numbered Pld-30 rows ----
tab_re = re.compile(r'^\s*(\d+)\.\s*(.+?)\s+30\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)')

# explicit alias map: normalised RSSSF print-name -> pack roster name (audited, printed below)
ALIAS = {
 'zenit sankt peterburg': 'Zenit St Petersburg',
 'dinamo moskva': 'Dynamo Moscow', 'dinamo moscow': 'Dynamo Moscow',
 'cska moskva': 'CSKA Moscow',
 'lokomotiv moskva': 'Lokomotiv Moscow',
 'spartak moskva': 'Spartak Moscow',
 'torpedo moskva': 'Torpedo Moscow',
 'ahmat grozny': 'Akhmat Grozny', 'ahmat groznyj': 'Akhmat Grozny',
 'pari nn nizh novgorod': 'Pari Nizhny Novgorod',
 'dinamo mahackala': 'Dynamo Makhachkala',
 'fakel voronez': 'Fakel Voronezh', 'fc soci': 'PFC Sochi',
 'krylya sovetov samara': 'Krylia Sovetov Samara', 'krylja sovetov samara': 'Krylia Sovetov Samara',
 'fc nizhniy novgorod': 'Pari Nizhny Novgorod', 'nizhniy novgorod': 'Pari Nizhny Novgorod',
 'pari nizhniy novgorod': 'Pari Nizhny Novgorod', 'pari nizhny novgorod': 'Pari Nizhny Novgorod',
 'pari nn nizn novgorod': 'Pari Nizhny Novgorod',
 'akron togliatti': 'Akron Tolyatti',
 'dinamo mahachkala': 'Dynamo Makhachkala',
 'fc sochi': 'PFC Sochi',
 'fakel voronezh': 'Fakel Voronezh',
 'ural yekaterinburg': 'Ural Yekaterinburg', 'ural jekaterinburg': 'Ural Yekaterinburg',
 'fc himki': 'FC Khimki', 'himki': 'FC Khimki',
 'fc ufa': 'FC Ufa', 'ufa': 'FC Ufa',
 'baltika kaliningrad': 'Baltika Kaliningrad',
 'orenburg': 'FC Orenburg', 'fc orenburg': 'FC Orenburg',
 'arsenal tula': 'Arsenal Tula', 'rubin kazan': 'Rubin Kazan',
 'fc rostov': 'FC Rostov', 'rostov': 'FC Rostov', 'fc krasnodar': 'FC Krasnodar', 'krasnodar': 'FC Krasnodar',
}
gate_total = 0
for s, path in RSS.items():
    txt = open(path, encoding='utf-8', errors='replace').read().splitlines()
    blocks = []
    for ln in txt:
        m = tab_re.match(ln)
        if m: blocks.append(m)
    # first maximal run with positions 1..16 sequential = the final table
    off = {}
    run = []
    expect = 1
    for m in blocks:
        pos = int(m.group(1))
        if pos == expect:
            run.append(m); expect += 1
            if expect == 17: break
        else:
            run = [m] if pos == 1 else []
            expect = 2 if pos == 1 else 1
    if expect != 17:
        errs.append(f'{s}: could not isolate 1..16 final-table run (found run to {expect-1})'); continue
    for m in run:
        name = re.sub(r'\s*\[.*?\]\s*', ' ', m.group(2))
        name = re.sub(r'<[^>]+>', ' ', name).strip()
        off[name] = [int(m.group(i)) for i in range(3, 9)]  # W D L GF GA Pts
    mine = build_table(league[s])
    if len(mine) != 16: errs.append(f'{s}: pack table teams {len(mine)} != 16')
    ok = 0
    for oname, o in sorted(off.items(), key=lambda kv: -kv[1][-1]):
        n = norm(oname)
        cand = ALIAS.get(n) or {norm(k): k for k in mine}.get(n)
        if not cand:
            errs.append(f'{s}: no pack team for RSSSF "{oname}" (norm "{n}")'); continue
        t = mine[cand]
        pts = t[1] * 3 + t[2]
        prof = [t[1], t[2], t[3], t[4], t[5], pts]
        if prof == o: ok += 1
        else: errs.append(f'{s}: TABLE MISMATCH {oname} rsssf={o} pack={prof}')
    gate_total += ok
    print(f'{s}: table {ok}/16 profile-exact')
print('PLAYOFF brackets:')
for s in RSS:
    print(' ', s, sorted(playoffs[s]))
print('=== TABLE GATE TOTAL:', gate_total, '/ 80 ===')
print('ERRORS:' if errs else 'NO ERRORS', *errs, sep='\n  ')
sys.exit(1 if errs else 0)
