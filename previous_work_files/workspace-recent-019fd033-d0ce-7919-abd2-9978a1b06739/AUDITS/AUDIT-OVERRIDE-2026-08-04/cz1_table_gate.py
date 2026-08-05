#!/usr/bin/env python3
# CZ1 full-span pack gate: recompute the 16-club final table from pack league rows
# (regular + Titul/Zachranu/Evropu split games; pro/rel 'other' rows excluded) and
# profile-compare vs RSSSF tsje{2022..2026} printed final tables (Pld 35 x 16).
import re, unicodedata, sys

PACK = '/home/user/AUDIT-OVERRIDE-2026-08-04/CZ1-2021-2026.txt'
RSS = {s: f'/home/user/rsssf-ref/tsje{y}.txt' for s, y in
       [('2021-22', 2022), ('2022-23', 2023), ('2023-24', 2024), ('2024-25', 2025), ('2025-26', 2026)]}
SPAN = {'2021-22': ('2021-07-01', '2022-06-30'), '2022-23': ('2022-07-01', '2023-06-30'),
        '2023-24': ('2023-07-01', '2024-06-30'), '2024-25': ('2024-07-01', '2025-06-30'),
        '2025-26': ('2025-07-01', '2026-06-30')}
def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

PREFIX = re.compile(r'^(sk|ac|fc|fk|mfk|tj|sc|1 fc|1 fk)\s+', re.I)
def stripname(s):
    s = re.sub(r'&#(\d+);', lambda q: chr(int(q.group(1))), s).strip()
    s = PREFIX.sub('', s); s = PREFIX.sub('', s)          # legal prefixes (up to 2, e.g. '1. FC')
    s = re.sub(r'\s+\d+$', '', s)                          # founding-year suffix (Jablonec 97)
    return s.strip()

# normalised-short -> pack canonical (keyed after stripname+norm on both key and lookup)
AL = {}
def _a(k, v): AL[norm(k)] = v
for k, v in [('Plzeň','Viktoria Plzen'),('Viktoria Plzen','Viktoria Plzen'),('Viktoria Plzeň','Viktoria Plzen'),
 ('Slovácko','Slovacko'),('Slovacko','Slovacko'),('Olomouc','Sigma Olomouc'),('Sigma Olomouc','Sigma Olomouc'),
 ('Sparta','Sparta Prague'),('Sparta Praha','Sparta Prague'),('Sparta Prague','Sparta Prague'),
 ('Slavia','Slavia Prague'),('Slavia Praha','Slavia Prague'),('Slavia Prague','Slavia Prague'),
 ('Bohemians','Bohemians 1905'),('Bohemians 1905','Bohemians 1905'),('Bohemians 1905 Praha','Bohemians 1905'),
 ('Liberec','Slovan Liberec'),('Slovan Liberec','Slovan Liberec'),
 ('Hradec Králové','Hradec Kralove'),('Hradec Kralove','Hradec Kralove'),
 ('Mladá Boleslav','Mlada Boleslav'),('Mlada Boleslav','Mlada Boleslav'),
 ('České Budějovice','Ceske Budejovice'),('Ceske Budejovice','Ceske Budejovice'),
 ('Dynamo České Budějovice','Ceske Budejovice'),('Dynamo Ceske Budejovice','Ceske Budejovice'),
 ('Jablonec','Jablonec'),('Baumit Jablonec','Jablonec'),('Baník Ostrava','Banik Ostrava'),
 ('Ostrava','Banik Ostrava'),('Banik Ostrava','Banik Ostrava'),
 ('Teplice','Teplice'),('Zbrojovka Brno','Zbrojovka Brno'),('Brno','Zbrojovka Brno'),
 ('Pardubice','Pardubice'),('Zlín','Zlin'),('Zlin','Zlin'),('Trinity Zlín','Zlin'),('Fastav Zlín','Zlin'),
 ('Karviná','Karvina'),('Karvina','Karvina'),('OKD Karviná','Karvina'),
 ('Dukla','Dukla Prague'),('Dukla Praha','Dukla Prague'),('Dukla Prague','Dukla Prague')]:
    _a(k, v)

rows = [l.rstrip('\n').split('|') for l in open(PACK, encoding='utf-8') if l.startswith('MATCH|')]
league = {s: [] for s in RSS}
for r in rows:
    d, comp = r[1], r[2]
    if comp != 'Czech First League': continue
    for s, (a, b) in SPAN.items():
        if a <= d <= b: league[s].append((r[4], int(r[5]), int(r[6]), r[7])); break

print('league rows/season:', {s: len(league[s]) for s in RSS})
errors = []
if any('Artis' in t for s in RSS for row in league[s] for t in (row[0], row[3])):
    errors.append('Artis Brno appears on a league row (must not in-window)')

def build(rows):
    T = {}
    for h, hg, ag, a in rows:
        for t in (h, a): T.setdefault(t, [0, 0, 0, 0, 0, 0])
        T[h][0] += 1; T[a][0] += 1; T[h][4] += hg; T[h][5] += ag; T[a][4] += ag; T[a][5] += hg
        if hg > ag: T[h][1] += 1; T[a][3] += 1
        elif hg < ag: T[a][1] += 1; T[h][3] += 1
        else: T[h][2] += 1; T[a][2] += 1
    return T

tab_re = re.compile(r'^\s*(\d+)\.\s*(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)')
tot = 0
for s, path in RSS.items():
    T = build(league[s])
    txt = open(path, encoding='utf-8', errors='replace').read().splitlines()
    # find the 1..16 run of numbered rows (Pld column = games played, 33..35 accepted)
    off = []
    for ln in txt:
        m = tab_re.match(ln)
        if m:
            pos = int(m.group(1)); pld = int(m.group(3))
            if pos == len(off) + 1 and pld >= 30:
                nm = re.sub(r'<[^>]+>', ' ', m.group(2))
                nm = re.sub(r'&#(\d+);', lambda q: chr(int(q.group(1))), nm)
                nm = re.sub(r'\s*\[.*?\]\s*', ' ', nm).strip()
                off.append((nm, [int(m.group(i)) for i in (4, 5, 6, 7, 8, 9)]))
            elif pos == 1 and pld >= 30:
                nm = re.sub(r'<[^>]+>', ' ', m.group(2))
                nm = re.sub(r'&#(\d+);', lambda q: chr(int(q.group(1))), nm)
                nm = re.sub(r'\s*\[.*?\]\s*', ' ', nm).strip()
                off = [(nm, [int(m.group(i)) for i in (4, 5, 6, 7, 8, 9)])]
        if len(off) == 16: break
    if len(off) != 16: errors.append(f'{s}: final-table run parsed {len(off)} != 16'); continue
    ok = 0
    for oname, o in off:
        cand = AL.get(norm(stripname(oname)))
        if not cand:
            for pk in T:
                if norm(pk) == norm(stripname(oname)): cand = pk; break
        if not cand:
            errors.append(f'{s}: no pack team for "{oname}" (norm {norm(stripname(oname))})'); continue
        t = T[cand]
        prof = [t[1], t[2], t[3], t[4], t[5], t[1] * 3 + t[2]]
        if prof == o: ok += 1
        else: errors.append(f'{s}: TABLE MISMATCH {oname} rsssf={o} pack={prof} (Pld {t[0]})')
    tot += ok
    print(f'{s}: table {ok}/16 profile-exact')
artis_league = sum(1 for s in RSS for r0 in league[s] if 'Artis' in r0[0] or 'Artis' in r0[3])
print('Artis Brno on league rows (expect 0):', artis_league)
print('=== CZ1 TABLE GATE TOTAL:', tot, '/ 80 ===')
print('NO ERRORS' if not errors else 'ERRORS:')
for e in errors[:30]: print('  ', e)
sys.exit(1 if errors else 0)
