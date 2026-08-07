#!/usr/bin/env python3
"""Final acceptance gates on the KOS + KOSCUP pack files (fresh code, mirrors workorder section 5)."""
import re, datetime
from collections import Counter

ROSTER = {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini',
          'Malisheva','Ferizaj','Prishtina E Re','Ulpiana','Feronikeli',"Trepça'89",
          'Fushë Kosova','Liria','Suhareka'}

OFFICIAL = {
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
APPENDIX = {('2026-03-09','Malisheva','Prishtina'), ('2026-03-22','Malisheva','Llapi'),
 ('2026-04-05','Drita','Malisheva'), ('2026-04-11','Prishtina E Re','Malisheva'),
 ('2026-04-19','Malisheva','KF Ballkani'), ('2026-04-26','Dukagjini','Malisheva'),
 ('2026-04-29','Malisheva','Gjilani'), ('2026-05-02','Prishtina','Malisheva'),
 ('2026-05-10','Ferizaj','Malisheva'), ('2026-05-17','Malisheva','Drenica Skenderaj'),
 ('2026-05-24','Llapi','Malisheva'), ('2026-05-31','Malisheva','Drita')}

def season_of(date):
    d = datetime.date.fromisoformat(date)
    y0 = d.year if d.month >= 8 else d.year - 1
    return f'{y0}-{str(y0+1)[2:]}'

print('=' * 20, 'KOS pack', '=' * 20)
rows, notes, teams = [], [], []
for ln in open('handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.txt', encoding='utf-8'):
    ln = ln.rstrip('\n')
    if ln.startswith('MATCH|'):
        f = ln.split('|')
        assert len(f) == 14, f'field count {len(f)}: {ln[:80]}'
        rows.append(f)
    elif ln.startswith('NOTE|'):
        notes.append(ln)
    elif ln.startswith('TEAM|'):
        teams.append(ln)
print(f'MATCH rows: {len(rows)} (expect 898 = 888 league + 10 playoff) | TEAM rows: {len(teams)} (expect 6) | END: {open("handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.txt").read().rstrip().endswith("END")}')
by_comp = Counter(r[2] for r in rows)
print(f'competitions: {dict(by_comp)} | compTypes: {dict(Counter(r[3] for r in rows))}')
# names
names = {r[4] for r in rows} | {r[7] for r in rows}
bad = names - ROSTER
print(f'non-roster names: {sorted(bad) if bad else "none"}')
# dupes + future
dups = len(rows) - len({(r[1], r[4], r[7]) for r in rows})
fut = [r for r in rows if datetime.date.fromisoformat(r[1]) > datetime.date(2026, 8, 7)]
print(f'duplicates: {dups} | future-dated: {len(fut)}')
# league structure per season
league = [r for r in rows if r[2] == 'Kosovo Superliga']
po = [r for r in rows if r[2] == 'Kosovo Relegation Playoffs']
print(f'league rows: {len(league)} (expect 888) | playoff rows: {len(po)} (expect 10)')
by_season = {}
for r in league:
    by_season.setdefault(season_of(r[1]), []).append(r)
for tag, rs in sorted(by_season.items()):
    rc = Counter(x[8] for x in rs)
    print(f'  {tag}: rows={len(rs)} rounds={len(rc)} goals={sum(int(x[5])+int(x[6]) for x in rs)} span={min(x[1] for x in rs)}..{max(x[1] for x in rs)}')
# per-club counts (league only)
cnt = Counter()
for r in league:
    cnt[r[4]] += 1
    cnt[r[7]] += 1
badc = {c: n for c, n in cnt.items() if n != 36}
print(f'per-club 36-gate (whole span): {"PASS" if not badc else badc} (clubs {len(cnt)})')
# table reproduction: pack rows + appendix for 2025-26
def standings(rs):
    st = {}
    for x in rs:
        for s in ('h', 'a'):
            st.setdefault(x[4] if s == 'h' else x[7], {'W':0,'D':0,'L':0,'GF':0,'GA':0,'Pts':0})
        h, a = st[x[4]], st[x[7]]
        hg, ag = int(x[5]), int(x[6])
        h['GF'] += hg; h['GA'] += ag; a['GF'] += ag; a['GA'] += hg
        if hg > ag: h['W'] += 1; a['L'] += 1; h['Pts'] += 3
        elif hg < ag: a['W'] += 1; h['L'] += 1; a['Pts'] += 3
        else: h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
    return st
ok_all = True
for tag in ['2021-22','2022-23','2023-24','2024-25']:
    st = standings(by_season[tag])
    off = OFFICIAL[tag]
    for club, (W, D, L, GF, GA, Pts) in off.items():
        s = st[club]
        if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, Pts):
            print(f'  TABLE MISMATCH {tag} {club}: {s}'); ok_all = False
# 2025-26: pack + appendix
rs26 = list(by_season['2025-26'])
added = 0
for r in league:
    pass
with open('team_workspace/researcher_handoffs/kos_ledgers/kos-2025-26-league.json') as f:
    import json
    full = json.load(f)
app = [r for r in full if (r['date'], r['home'], r['away']) in APPENDIX]
# pack 2025-26 should equal full minus app
pk = {(x[1], x[4], x[7]) for x in rs26}
fullset = {(x['date'], x['home'], x['away']) for x in full}
print(f'2025-26 pack rows = full - appendix: {pk == fullset - APPENDIX}')
st = standings(rs26 + [[None, a['date'], 'Kosovo Superliga', 'domestic-league', a['home'], str(a['hg']), str(a['ag']), a['away'], 'RS'] for a in app])
off = OFFICIAL['2025-26']
for club, (W, D, L, GF, GA, Pts) in off.items():
    s = st[club]
    if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, Pts):
        print(f'  TABLE MISMATCH 2025-26 {club}: {s}'); ok_all = False
print(f'table reproduction all 5 seasons (50 club-seasons): {"PASS" if ok_all else "FAIL"}')
# appendix exclusion check
inter = pk & APPENDIX
print(f'appendix rows leaked into pack: {inter or "none"}')

print('=' * 20, 'KOSCUP pack', '=' * 20)
rows2, notes2, teams2 = [], [], []
for ln in open('handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt', encoding='utf-8'):
    ln = ln.rstrip('\n')
    if ln.startswith('MATCH|'):
        rows2.append(ln.split('|'))
    elif ln.startswith('NOTE|'):
        notes2.append(ln)
    elif ln.startswith('TEAM|'):
        teams2.append(ln)
print(f'MATCH rows: {len(rows2)} (expect 123) | TEAM rows: {len(teams2)} | END: {open("handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt").read().rstrip().endswith("END")}')
print(f'compTypes: {dict(Counter(r[3] for r in rows2))} | competition: {set(r[2] for r in rows2)}')
dups2 = len(rows2) - len({(r[1], r[4], r[7], r[8]) for r in rows2})
print(f'duplicates: {dups2} | future-dated: {len([r for r in rows2 if datetime.date.fromisoformat(r[1]) > datetime.date(2026, 8, 7)])}')
# slice membership per season
mem = {
 '2021-22': {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini','Malisheva','Ulpiana','Feronikeli'},
 '2022-23': {'KF Ballkani','Drita','Gjilani','Dukagjini','Prishtina','Malisheva','Llapi','Ferizaj',"Trepça'89",'Drenica Skenderaj'},
 '2023-24': {'KF Ballkani','Llapi','Drita','Malisheva','Prishtina','Gjilani','Dukagjini','Feronikeli','Fushë Kosova','Liria'},
 '2024-25': {'Drita','KF Ballkani','Malisheva','Gjilani','Ferizaj','Prishtina','Dukagjini','Llapi','Suhareka','Feronikeli'},
 '2025-26': {'Drita','Malisheva','KF Ballkani','Dukagjini','Gjilani','Drenica Skenderaj','Prishtina','Llapi','Ferizaj','Prishtina E Re'},
}
bad_slice = []
for r in rows2:
    tag = season_of(r[1])
    if not (r[4] in mem[tag] or r[7] in mem[tag]):
        bad_slice.append((tag, r[1], r[4], r[7]))
print(f'rows without a Superliga club of that season: {len(bad_slice)}')
for b in bad_slice[:5]:
    print('  ', b)
# advancement notes coverage
adv = [n for n in notes2 if n.startswith('NOTE|info|advancement')]
aet = [n for n in notes2 if n.startswith('NOTE|info|aet')]
awd = [n for n in notes2 if n.startswith('NOTE|warning|awarded')]
print(f'advancement notes: {len(adv)} | aet notes: {len(aet)} | awarded notes: {len(awd)}')
# ties per season + stage
sc = Counter()
for r in rows2:
    tag = season_of(r[1])
    sc[(tag, r[8].split(' ')[0])] += 1
for k in sorted(sc):
    print('  ', k, sc[k])
