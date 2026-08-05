#!/usr/bin/env python3
# CZ1 gate v2 — phase-correct:
#  A) REGULAR stage: pack 'Round n' rows -> table vs tsje regular Final Table (Pld 30, 16 rows)
#  B) Titul + Zachranu groups: pack regular+group rows for the 6 clubs -> vs tsje group
#     Final Tables (Pld 35, two 6-row runs)  [Evropu legs + pro/rel handled separately]
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
PREFIX = re.compile(r'^(?:1\.\s*)?(sk|ac|fc|fk|mfk|tj|sc)\.\s\s*|^(?:1\.\s*)?(sk|ac|fc|fk|mfk|tj|sc)\s+', re.I)
def stripname(s):
    s = re.sub(r'&#(\d+);', lambda q: chr(int(q.group(1))), s).strip()
    s = PREFIX.sub('', s); s = PREFIX.sub('', s)
    s = re.sub(r'\s+\d+$', '', s)
    return s.strip()

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
def parse_tables(path):
    """Return parsed numbered-table runs: [(startpos, pld, [(name,[W D L GF GA Pts]),...]), ...].
       Runs may start at 1 (regular/titul) or 11 (zachranu keeps league numbering)."""
    runs, cur = [], []
    for ln in open(path, encoding='utf-8', errors='replace'):
        m = tab_re.match(ln)
        if not m: continue
        pos, pld = int(m.group(1)), int(m.group(3))
        if cur and pos == cur[-1][0] + 1 and pld == cur[0][1]:
            cur.append((pos, pld, m)); continue
        if cur: runs.append(cur); cur = []
        if pos in (1, 11): cur.append((pos, pld, m))
    if cur: runs.append(cur)
    out = []
    for run in runs:
        if len(run) < 4: continue
        start, pld = run[0][0], run[0][1]
        rows_out = []
        for _, _, m in run:
            nm = re.sub(r'<[^>]+>', ' ', m.group(2))
            nm = re.sub(r'&#(\d+);', lambda q: chr(int(q.group(1))), nm)
            nm = re.sub(r'\s*\[.*?\]\s*', ' ', nm).strip()
            rows_out.append((nm, [int(m.group(i)) for i in (4, 5, 6, 7, 8, 9)]))
        out.append((start, pld, rows_out))
    return out

def cmp_table(season, label, mine, off, errors):
    ok = 0
    for oname, o in off:
        cand = AL.get(norm(stripname(oname)))
        if not cand: cand = AL.get(norm(oname))
        if not cand or cand not in mine:
            # containment fallback
            n = norm(stripname(oname))
            hits = [k for k in mine if n in norm(k) or norm(k) in n]
            cand = hits[0] if len(hits) == 1 else cand
        if not cand or cand not in mine:
            errors.append(f'{season} {label}: no pack team for "{oname}"'); continue
        t = mine[cand]
        prof = [t[1], t[2], t[3], t[4], t[5], t[1] * 3 + t[2]]
        if prof == o: ok += 1
        else: errors.append(f'{season} {label}: MISMATCH {oname} rsssf={o} pack={prof} Pld={t[0]}')
    return ok

total, need = 0, 0
errors = []
for s, (a, b) in SPAN.items():
    sea = [r for r in rows if r[2] == 'Czech First League' and a <= r[1] <= b]
    reg = [(r[4], int(r[5]), int(r[6]), r[7]) for r in sea if r[8].startswith('Round ')]
    tit = [(r[4], int(r[5]), int(r[6]), r[7]) for r in sea if r[8].startswith('Round ') or r[8].startswith('Titul ')]
    zac = [(r[4], int(r[5]), int(r[6]), r[7]) for r in sea if r[8].startswith('Round ') or r[8].startswith('Zachranu ')]
    tables = parse_tables(RSS[s])
    reg_off = [rs for st, pld, rs in tables if st == 1 and pld == 30 and len(rs) == 16]
    tit_off = [rs for st, pld, rs in tables if st == 1 and pld == 35 and len(rs) == 6]
    zac_off = [rs for st, pld, rs in tables if st == 11 and pld == 35 and len(rs) == 6]
    if len(reg_off) < 1: errors.append(f'{s}: no 16-row Pld-30 regular table parsed'); continue
    ok = cmp_table(s, 'REG', build(reg), reg_off[0], errors)
    total += ok; need += 16
    print(f'{s}: REGULAR {ok}/16 profile-exact   (runs: {[(st, p, len(r)) for st, p, r in tables][:7]})')
    if tit_off:
        ok = cmp_table(s, 'TITUL', build(tit), tit_off[0], errors)
        total += ok; need += 6
        print(f'{s}: TITUL {ok}/6 profile-exact')
    else: errors.append(f'{s}: no TITUL (1..6 Pld-35) run parsed')
    if zac_off:
        ok = cmp_table(s, 'ZACHRANU', build(zac), zac_off[0], errors)
        total += ok; need += 6
        print(f'{s}: ZACHRANU {ok}/6 profile-exact')
    else: errors.append(f'{s}: no ZACHRANU (11..16 Pld-35) run parsed')
print('=== CZ1 PHASE GATE TOTAL:', total, '/', need, '===')
print('NO ERRORS' if not errors else 'ERRORS:')
for e in errors[:40]: print('  ', e)
sys.exit(1 if errors else 0)
