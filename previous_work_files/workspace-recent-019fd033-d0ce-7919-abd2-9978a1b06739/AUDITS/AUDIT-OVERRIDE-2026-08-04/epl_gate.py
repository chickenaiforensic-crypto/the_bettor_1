#!/usr/bin/env python3
# EPL full-span pack gate:
#  A) seasons 2021-22..2024-25: row-exact multiset diff vs auditor baselines (sha-pinned)
#  B) season 2025-26: table recompute vs RSSSF eng2026 printed final table (20/20)
#  C) boundary: zero 2026-27 league rows + MD venue detail intact + internal dupes 0
import json, re, sys, unicodedata
from collections import Counter

PACK = '/home/user/AUDIT-OVERRIDE-2026-08-04/EPL-2021-2026.txt'
BASE = {s: f'/home/user/audit-baseline/epl-{s}.json'
        for s in ['2021-22', '2022-23', '2023-24', '2024-25']}
SPAN = {'2021-22': ('2021-07-01', '2022-06-30'), '2022-23': ('2022-07-01', '2023-06-30'),
        '2023-24': ('2023-07-01', '2024-06-30'), '2024-25': ('2024-07-01', '2025-06-30'),
        '2025-26': ('2025-07-01', '2026-06-30')}
rows = [l.rstrip('\n').split('|') for l in open(PACK, encoding='utf-8') if l.startswith('MATCH|')]
print('pack MATCH rows:', len(rows), '| comps:', Counter(r[2] + '|' + r[3] for r in rows))
print('venue-detail sample:', rows[0][8] if len(rows[0]) > 8 else '(none)')

by_season = {s: [] for s in SPAN}
for r in rows:
    d = r[1]
    for s, (a, b) in SPAN.items():
        if a <= d <= b: by_season[s].append(r); break

errs = []
for s in SPAN:
    n = len(by_season[s])
    if n != 380: errs.append(f'{s}: {n} rows != 380')
    else: print(f'{s}: 380 rows OK')

# RSSSF-long -> pack-short canonical map (both directions audited against both rosters)
SHORT = {'AFC Bournemouth': 'Bournemouth', 'Arsenal': 'Arsenal', 'Aston Villa': 'Aston Villa',
 'Brentford': 'Brentford', 'Brighton & Hove Albion': 'Brighton', 'Burnley': 'Burnley',
 'Chelsea': 'Chelsea', 'Crystal Palace': 'Crystal Palace', 'Everton': 'Everton', 'Fulham': 'Fulham',
 'Ipswich Town': 'Ipswich', 'Leeds United': 'Leeds', 'Leicester City': 'Leicester',
 'Liverpool': 'Liverpool', 'Luton Town': 'Luton', 'Manchester City': 'Man City',
 'Manchester United': 'Man United', 'Newcastle United': 'Newcastle', 'Norwich City': 'Norwich',
 'Nottingham Forest': "Nott'm Forest", 'Sheffield United': 'Sheffield United',
 'Southampton': 'Southampton', 'Sunderland': 'Sunderland', 'Tottenham Hotspur': 'Tottenham',
 'Watford': 'Watford', 'West Ham United': 'West Ham', 'Wolverhampton Wanderers': 'Wolves'}

# A) row-exact vs baselines (baseline long names canonicalised to pack short set)
for s, bp in BASE.items():
    B = json.load(open(bp))
    pk = Counter((r[1], r[4], r[5], r[6], r[7]) for r in by_season[s])
    bl = Counter((m['date'], SHORT.get(m['home'], m['home']), str(m['hg']), str(m['ag']),
                  SHORT.get(m['away'], m['away'])) for m in B['matches'])
    only_pk = pk - bl; only_bl = bl - pk
    if only_pk or only_bl:
        errs.append(f'{s}: ROW DIFF pack-only={sum(only_pk.values())} baseline-only={sum(only_bl.values())}')
        for k in list(only_pk)[:5]: errs.append(f'   pack-only: {k}')
        for k in list(only_bl)[:5]: errs.append(f'   base-only: {k}')
    else:
        print(f'{s}: ROW-EXACT 380/380 vs pinned baseline')

# B) 2025-26 table recompute vs eng2026
def norm(x): return re.sub(r'[^a-z0-9]+', ' ', unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode().lower()).strip()
ALIAS = {'wolverhampton wanderers': 'Wolves', 'wolves': 'Wolves',
         'manchester utd': 'Man United', 'manchester united': 'Man United',
         'manchester city': 'Man City', 'man city': 'Man City',
         'newcastle utd': 'Newcastle', 'newcastle united': 'Newcastle',
         'tottenham hotspur': 'Tottenham', 'spurs': 'Tottenham',
         'brighton hove albion': 'Brighton', 'west ham utd': 'West Ham', 'west ham united': 'West Ham',
         'nottingham forest': "Nott'm Forest", 'leeds utd': 'Leeds', 'leeds united': 'Leeds',
         'leicester city': 'Leicester', 'sunderland': 'Sunderland',
         'ipswich town': 'Ipswich', 'luton town': 'Luton', 'norwich city': 'Norwich',
         'afc bournemouth': 'Bournemouth'}
T = {}
for r in by_season['2025-26']:
    h, a = r[4], r[7]; hg, ag = int(r[5]), int(r[6])
    for t in (h, a): T.setdefault(t, [0, 0, 0, 0, 0, 0])
    T[h][0] += 1; T[a][0] += 1; T[h][4] += hg; T[h][5] += ag; T[a][4] += ag; T[a][5] += hg
    if hg > ag: T[h][1] += 1; T[a][3] += 1
    elif hg < ag: T[a][1] += 1; T[h][3] += 1
    else: T[h][2] += 1; T[a][2] += 1
tab_re = re.compile(r'^\s*(\d+)\.\s*(.+?)\s+38\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)')
off = {}
for ln in open('/home/user/rsssf-ref/eng2026.txt', encoding='utf-8', errors='replace'):
    m = tab_re.match(ln)
    if m:
        nm = re.sub(r'\s*\[.*?\]\s*', ' ', m.group(2)); nm = re.sub(r'<[^>]+>', ' ', nm).strip()
        off[nm] = [int(m.group(i)) for i in range(3, 9)]
print(f'2025-26: RSSSF eng2026 table rows parsed: {len(off)} (expect 20)')
nmap = {norm(k): k for k in T}
ok = 0
for oname, o in off.items():
    n = norm(oname); cand = nmap.get(n) or ALIAS.get(n) or nmap.get(norm(ALIAS.get(n, oname)))
    if not cand: errs.append(f'2025-26: no pack team for "{oname}" (norm {n})'); continue
    t = T[cand]; prof = [t[1], t[2], t[3], t[4], t[5], t[1] * 3 + t[2]]
    if prof == o: ok += 1
    else: errs.append(f'2025-26 TABLE MISMATCH {oname} rsssf={o} pack={prof}')
print(f'2025-26: table {ok}/20 profile-exact')

# C) boundary + dupes + MD detail
f26 = [r[1] for r in rows if r[1].startswith('2026-0') and r[1] > '2026-06-30']
print('2026-27 EPL rows (expect 0):', len(f26))
fp = Counter((r[1], r[4], r[7], r[2]) for r in rows)
dups = [k for k, v in fp.items() if v > 1]
print('internal duplicate fingerprints:', len(dups))
md = sum(1 for r in rows if len(r) > 8 and r[8].startswith('MD'))
print('MD venue-detail rows:', md, '/ 1900')
note26 = [l for l in open(PACK, encoding='utf-8') if l.startswith('NOTE|') and '2026-27' in l]
print('2026-27 boundary NOTE present:', len(note26) > 0)
if f26 or dups: errs.append(f'boundary/dupes: {len(f26)}/{len(dups)}')
print('=== ERRORS ===' if errs else '=== EPL GATE: NO ERRORS ===', *errs, sep='\n  ')
sys.exit(1 if errs else 0)
