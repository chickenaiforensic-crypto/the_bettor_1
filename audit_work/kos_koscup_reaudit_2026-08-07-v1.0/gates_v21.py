#!/usr/bin/env python3
"""FRESH GATES for the corrected KOS/KOSCUP v2.1 packs (2026-08-07).
Independent of the builder: parses the shipped .txt files only.
Checks: completeness (910 rows), no placeholder venues, table reproduction
(50 club-seasons), per-club counts, duplicates, names, slice, identity, brackets.
"""
import datetime, re
from collections import Counter

FAIL = []
def check(cond, label, detail=''):
    print(('  PASS  ' if cond else '  FAIL  ') + label + ((' | ' + detail) if detail else ''))
    if not cond:
        FAIL.append(label)

ROSTER = {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini',
          'Malisheva','Ferizaj','Prishtina E Re','Ulpiana','Feronikeli',"Trepça'89",
          'Fushë Kosova','Liria','Suhareka'}

def season_of(date):
    d = datetime.date.fromisoformat(date)
    y0 = d.year if d.month >= 8 else d.year - 1
    return f'{y0}-{str(y0+1)[2:]}'

def parse(path):
    rows, notes, teams = [], [], []
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('MATCH|'):
            f = ln.split('|')
            assert len(f) == 14, f'field count {len(f)}: {ln[:80]}'
            rows.append(f)
        elif ln.startswith('NOTE|'):
            notes.append(ln)
        elif ln.startswith('TEAM|'):
            teams.append(ln.split('|'))
    return rows, notes, teams

def standings(rows):
    st = {}
    for x in rows:
        for side in ('h', 'a'):
            st.setdefault(x[4] if side == 'h' else x[7], {'W':0,'D':0,'L':0,'GF':0,'GA':0,'Pts':0})
        h, a = st[x[4]], st[x[7]]
        hg, ag = int(x[5]), int(x[6])
        h['GF'] += hg; h['GA'] += ag; a['GF'] += ag; a['GA'] += hg
        if hg > ag: h['W'] += 1; a['L'] += 1; h['Pts'] += 3
        elif hg < ag: a['W'] += 1; h['L'] += 1; a['Pts'] += 3
        else: h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
    return st

print('=' * 26, 'KOS v2.1', '=' * 26)
rows, notes, teams = parse('handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt')
league = [x for x in rows if x[2] == 'Kosovo Superliga']
po = [x for x in rows if x[2] == 'Kosovo Relegation Playoffs']
check(len(rows) == 910, f'910 MATCH rows (got {len(rows)})')
check(len(league) == 900 and len(po) == 10, f'900 league + 10 playoff (got {len(league)}/{len(po)})')
check(len(rows) == len({(x[1], x[4], x[7]) for x in rows}), 'no duplicates')
check(all(datetime.date.fromisoformat(x[1]) <= datetime.date(2026, 8, 7) for x in rows), 'no future-dated')
check(all(x[5].isdigit() and x[6].isdigit() for x in rows), 'integer scores')
# venue placeholders
ph = [x for x in rows if x[9].strip() == '' or x[9].lower() in ('unknown', 'stadium', 'city', 'n/a')
      or x[10].strip() == '' or x[10].lower() in ('unknown', 'stadium', 'city', 'n/a')]
check(len(ph) == 0, f'no placeholder venues in MATCH rows (got {len(ph)})')
for x in ph[:5]:
    print('    ', x[1], x[4], x[7], x[9], x[10])
# names
extra = ({x[4] for x in league} | {x[7] for x in league}) - ROSTER
check(not extra, f'league names all in 16-pool (extra {sorted(extra) or "none"})')
po_extra = ({x[4] for x in po} | {x[7] for x in po}) - ROSTER
check(po_extra <= {'Vushtrria', 'Dinamo Fzaj.', 'Liria', 'Ulpiana', 'Prishtina E Re', 'Feronikeli'},
      f'playoff outsiders are declared (got {sorted(po_extra)})')
# table reproduction 50/50 (full seasons, incl. former appendix rows)
OFF = {
 '2021-22': {'KF Ballkani':(23,7,6,61,26,76),'Drita':(18,10,8,56,25,64),'Gjilani':(16,14,6,57,36,62),
  'Llapi':(15,9,12,57,44,54),'Prishtina':(14,9,13,49,37,51),'Drenica Skenderaj':(14,8,14,51,48,50),
  'Dukagjini':(12,14,10,37,34,50),'Malisheva':(13,9,14,45,43,48),'Ulpiana':(6,9,21,34,72,27),
  'Feronikeli':(3,3,30,16,98,12)},
 '2022-23': {'KF Ballkani':(20,13,3,62,32,73),'Drita':(20,10,6,63,31,70),'Gjilani':(13,15,8,34,34,54),
  'Dukagjini':(14,8,14,41,37,50),'Prishtina':(12,12,12,46,36,48),'Malisheva':(12,10,14,52,52,46),
  'Llapi':(11,10,15,44,50,43),'Ferizaj':(10,11,15,31,50,41),'Trepça\'89':(10,10,16,46,62,40),
  'Drenica Skenderaj':(6,5,25,27,62,23)},
 '2023-24': {'KF Ballkani':(23,9,4,62,26,78),'Llapi':(21,8,7,56,27,71),'Drita':(19,10,7,49,27,67),
  'Malisheva':(17,6,13,58,45,57),'Prishtina':(11,16,9,41,32,49),'Gjilani':(11,12,13,43,38,45),
  'Dukagjini':(10,15,11,38,48,45),'Feronikeli':(12,8,16,39,47,44),'Fushë Kosova':(4,8,24,20,64,20),
  'Liria':(2,8,26,26,78,14)},
 '2024-25': {'Drita':(22,8,6,59,26,74),'KF Ballkani':(17,11,8,61,39,62),'Malisheva':(14,11,11,44,39,53),
  'Gjilani':(13,12,11,48,47,51),'Ferizaj':(14,8,14,42,47,50),'Prishtina':(11,15,10,42,36,48),
  'Dukagjini':(13,9,14,35,45,48),'Llapi':(12,11,13,42,41,47),'Suhareka':(12,7,17,49,62,43),
  'Feronikeli':(3,6,27,24,64,15)},
 '2025-26': {'Drita':(20,6,10,50,35,66),'Malisheva':(18,5,13,58,50,59),'KF Ballkani':(17,7,12,61,41,58),
  'Dukagjini':(13,12,11,42,36,51),'Gjilani':(14,9,13,47,48,51),'Drenica Skenderaj':(15,5,16,46,55,50),
  'Prishtina':(13,10,13,52,51,49),'Llapi':(13,10,13,46,50,49),'Ferizaj':(9,9,18,40,55,36),
  'Prishtina E Re':(8,7,21,39,60,31)},
}
by_season = {}
for x in league:
    by_season.setdefault(season_of(x[1]), []).append(x)
check(set(by_season) == set(OFF), 'five seasons present', str(sorted(by_season)))
allok = True
for tag, rs in by_season.items():
    st = standings(rs)
    for club, (W, D, L, GF, GA, Pts) in OFF[tag].items():
        s = st[club]
        if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, Pts):
            print('    TABLE mismatch', tag, club, s)
            allok = False
    per = Counter()
    for x in rs:
        per[x[4]] += 1; per[x[7]] += 1
    if not all(v == 36 for v in per.values()):
        print('    club-count mismatch', tag, {c: n for c, n in per.items() if n != 36})
        allok = False
    g = sum(int(x[5]) + int(x[6]) for x in rs)
    print(f'  {tag}: rows={len(rs)} goals={g}')
check(allok, 'table reproduction 50/50 club-seasons + per-club 36')
# labels
labels = Counter(x[-1] for x in league)
check(labels.get('wf-kos-2526', 0) == 180 and 'rsssf-kosovo2026' not in labels,
      f'2025-26 league labels wf-kos-2526 x180 (got {dict(labels)})')
plabels = Counter(x[-1] for x in po)
check(dict(plabels) == {'rsssf-kosovo2022':2,'rsssf-kosovo2023':2,'rsssf-kosovo2024':2,'rsssf-kosovo2025':2,'rsssf-kosovo2026':2},
      f'playoff labels per-season x2 (got {dict(plabels)})')
# former appendix rows present with correct data
APP = {('2026-03-09','Malisheva','Prishtina'), ('2026-03-22','Malisheva','Llapi'),
 ('2026-04-05','Drita','Malisheva'), ('2026-04-11','Prishtina E Re','Malisheva'),
 ('2026-04-19','Malisheva','KF Ballkani'), ('2026-04-26','Dukagjini','Malisheva'),
 ('2026-04-29','Malisheva','Gjilani'), ('2026-05-02','Prishtina','Malisheva'),
 ('2026-05-10','Ferizaj','Malisheva'), ('2026-05-17','Malisheva','Drenica Skenderaj'),
 ('2026-05-24','Llapi','Malisheva'), ('2026-05-31','Malisheva','Drita')}
pk = {(x[1], x[4], x[7]) for x in league}
check(APP <= pk, f'former appendix rows all included ({len(APP & pk)}/12)')

print('=' * 26, 'KOSCUP v2.1', '=' * 26)
rows2, notes2, teams2 = parse('handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt')
check(len(rows2) == 123, f'123 slice ties (got {len(rows2)})')
check(len(rows2) == len({(x[1], x[4], x[7], x[8]) for x in rows2}), 'no duplicates')
check(all(datetime.date.fromisoformat(x[1]) <= datetime.date(2026, 8, 7) for x in rows2), 'no future-dated')
check(all(x[3] == 'domestic-cup' for x in rows2), 'compType domestic-cup')
ph2 = [x for x in rows2 if x[9].strip() == '' or x[9].lower() in ('unknown', 'stadium', 'city', 'n/a')
       or x[10].strip() == '' or x[10].lower() in ('unknown', 'stadium', 'city', 'n/a')]
check(len(ph2) == 0, f'no placeholder venues in MATCH rows (got {len(ph2)})')
for x in ph2[:5]:
    print('    ', x[1], x[4], x[7], x[9], x[10])
MEM = {
 '2021-22': {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini','Malisheva','Ulpiana','Feronikeli'},
 '2022-23': {'KF Ballkani','Drita','Gjilani','Dukagjini','Prishtina','Malisheva','Llapi','Ferizaj',"Trepça'89",'Drenica Skenderaj'},
 '2023-24': {'KF Ballkani','Llapi','Drita','Malisheva','Prishtina','Gjilani','Dukagjini','Feronikeli','Fushë Kosova','Liria'},
 '2024-25': {'Drita','KF Ballkani','Malisheva','Gjilani','Ferizaj','Prishtina','Dukagjini','Llapi','Suhareka','Feronikeli'},
 '2025-26': {'Drita','Malisheva','KF Ballkani','Dukagjini','Gjilani','Drenica Skenderaj','Prishtina','Llapi','Ferizaj','Prishtina E Re'},
}
bad = [x for x in rows2 if not (x[4] in MEM[season_of(x[1])] or x[7] in MEM[season_of(x[1])])]
check(not bad, f'slice membership (0 bad; got {len(bad)})')
# identity invariant
teamed = {t[1] for t in teams2}
allnames = {x[4] for x in rows2} | {x[7] for x in rows2}
viol = []
for n in sorted(allnames):
    if n in ROSTER:
        if n in teamed: viol.append(f'{n}: pool but TEAM row')
    else:
        c = sum(1 for t in teams2 if t[1] == n)
        if c != 1: viol.append(f'{n}: {c} TEAM rows')
    if len(n) < 2 or not re.search(r'[A-Za-z]', n): viol.append(f'{n}: degenerate')
check(not viol, f'identity invariant (violations {viol or "none"})')
# per-edition counts
sc = Counter((season_of(x[1]), x[8].split(' ')[0]) for x in rows2)
exp = {('2021-22','R1'):10, ('2021-22','R8'):6, ('2021-22','QF'):3, ('2021-22','SF'):4, ('2021-22','Final'):1,
       ('2022-23','R1'):10, ('2022-23','R8'):6, ('2022-23','QF'):3, ('2022-23','SF'):4, ('2022-23','Final'):1,
       ('2023-24','R1'):10, ('2023-24','R8'):6, ('2023-24','QF'):3, ('2023-24','SF'):4, ('2023-24','Final'):1,
       ('2024-25','R16'):10, ('2024-25','R8'):7, ('2024-25','QF'):4, ('2024-25','SF'):4, ('2024-25','Final'):1,
       ('2025-26','R16'):10, ('2025-26','R8'):6, ('2025-26','QF'):4, ('2025-26','SF'):4, ('2025-26','Final'):1}
check(dict(sc) == exp, 'per-edition stage counts', str(dict(sc)))
finals = {season_of(x[1]): (x[4], int(x[5]), int(x[6]), x[7]) for x in rows2 if x[8] == 'Final'}
exp_f = {'2021-22': ('Llapi', 2, 1, 'Drita'), '2022-23': ('Prishtina', 2, 0, 'Gjilani'),
         '2023-24': ('KF Ballkani', 2, 2, 'Prishtina'), '2024-25': ('Prishtina', 1, 0, 'Llapi'),
         '2025-26': ('Ferizaj', 1, 2, 'Dukagjini')}
check(finals == exp_f, 'finals vs official record', str(finals))
# spot venues
for needle in [('2023-02-04', 'KF Ballkani', 'A&N Prizren'), ('2022-11-24', 'Phoenix-Banje', 'KF Ballkani'),
               ('2026-02-11', 'Dukagjini', 'Prishtina E Re'), ('2024-12-03', 'Rilindja 74', 'KF Ballkani'),
               ('2025-12-03', 'Prishtina E Re', 'Lepenci')]:
    hit = [x for x in rows2 if x[1] == needle[0] and x[4] == needle[1] and x[7] == needle[2]]
    check(len(hit) == 1 and hit[0][9] != 'unknown' and hit[0][10] != 'unknown',
          f'venue spot {needle[0]} {needle[1]}-{needle[2]}', hit[0][9] + ', ' + hit[0][10] if hit else 'MISSING')

print('=' * 26, 'SUMMARY', '=' * 26)
if FAIL:
    print(f'{len(FAIL)} FAILURES:')
    for f in FAIL:
        print('  -', f)
else:
    print('ALL GATES PASSED — both v2.1 packs are complete, placeholder-free, and consistent with the official records.')
