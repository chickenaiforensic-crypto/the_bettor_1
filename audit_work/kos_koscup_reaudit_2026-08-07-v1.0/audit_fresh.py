#!/usr/bin/env python3
"""FRESH AUDIT of the three returned packs (SPA, KOS, KOSCUP).
Independent of the build pipeline: parses the shipped .txt files only and
cross-checks against independently re-fetched sources (Wikipedia matrices,
RSSSF pages). 2026-08-07. v2 (fixed round-parse + false-positive expectations)."""
import re, datetime
from collections import Counter

FAIL = []
def check(cond, label, detail=''):
    print(('  PASS  ' if cond else '  FAIL  ') + label + ((' | ' + detail) if detail else ''))
    if not cond:
        FAIL.append(label)

def parse_pack(path, comp=None, ct=None):
    rows, notes, teams = [], [], []
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('MATCH|'):
            f = ln.split('|')
            assert len(f) == 14, f'field count {len(f)} in {path}: {ln[:80]}'
            if comp and f[2] != comp:
                continue
            if ct and f[3] != ct:
                continue
            rows.append(f)
        elif ln.startswith('NOTE|'):
            notes.append(ln)
        elif ln.startswith('TEAM|'):
            teams.append(ln)
    return rows, notes, teams

def season_of(date):
    d = datetime.date.fromisoformat(date)
    y0 = d.year if d.month >= 8 else d.year - 1
    return f'{y0}-{str(y0 + 1)[2:]}'

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

# ================================================================ SPA PACK
print('=' * 28, 'SPA pack', '=' * 28)
spa, spa_notes, _ = parse_pack('handoffs/SPA-2021-2026_BP-TEAM-PACK_v2.txt')
check(len(spa) == 1900, f'SPA row count 1900 (got {len(spa)})')
check(len(spa) == len({(x[1], x[4], x[7]) for x in spa}), 'SPA no duplicates')
check(len(spa) == len({(x[1], x[4], x[7], x[5], x[6]) for x in spa}), 'SPA no identical rows')
check(all(datetime.date.fromisoformat(x[1]) <= datetime.date(2026, 8, 6) for x in spa), 'SPA no future-dated rows')
check(all(x[5].isdigit() and x[6].isdigit() and int(x[5]) <= 30 and int(x[6]) <= 30 for x in spa), 'SPA scores sane')
spa_by_season = {}
for x in spa:
    spa_by_season.setdefault(season_of(x[1]), []).append(x)
check(set(spa_by_season) == {'2021-22','2022-23','2023-24','2024-25','2025-26'}, 'SPA five seasons present')

CODE = {'Alaves':'ALA','Ath Bilbao':'ATH','Ath Madrid':'ATM','Barcelona':'BAR','Betis':'BET',
        'Celta':'CEL','Elche':'ELC','Espanol':'ESP','Getafe':'GET','Girona':'GIR','Levante':'LEV',
        'Mallorca':'MLL','Osasuna':'OSA','Oviedo':'OVD','Vallecano':'RAY','Real Madrid':'RMA',
        'Sociedad':'RSO','Sevilla':'SEV','Valencia':'VAL','Villarreal':'VIL'}
matrix = {}
for ln in open('team_workspace/researcher_handoffs/spa_ledgers/wikipedia-2025-26-matrix.txt', encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    m = re.match(r'^match_([A-Z]{3})_([A-Z]{3})=([0-9]+)-([0-9]+)$', ln)
    if m:
        matrix[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)))
check(len(matrix) == 380, f'SPA matrix cells 380 (got {len(matrix)})')
miss = mism = 0
for x in spa_by_season['2025-26']:
    key = (CODE[x[4]], CODE[x[7]])
    if key not in matrix:
        miss += 1
    elif matrix[key] != (int(x[5]), int(x[6])):
        mism += 1
        print('    MISMATCH:', x[4], x[5], x[6], x[7], 'matrix says', matrix[key])
check(miss == 0, f'SPA 2025-26 all 380 fixtures in matrix (missing {miss})')
check(mism == 0, f'SPA 2025-26 380/380 scores identical to Wikipedia matrix (mismatches {mism})')

OFF_SPA = {
 '2021-22': (951, {'Real Madrid':(26,8,4,80,31),'Barcelona':(21,10,7,68,38),'Ath Madrid':(21,8,9,65,43)}),
 '2022-23': (955, {'Barcelona':(28,4,6,70,20),'Real Madrid':(24,6,8,75,36),'Ath Madrid':(23,8,7,70,33)}),
 '2023-24': (1005, {'Real Madrid':(29,8,1,87,26),'Barcelona':(26,7,5,79,44),'Girona':(25,6,7,85,46)}),
 '2024-25': (995, {'Barcelona':(28,4,6,102,39),'Real Madrid':(26,6,6,78,38),'Ath Madrid':(22,10,6,68,30)}),
 '2025-26': (1024, {'Barcelona':(31,1,6,95,36),'Real Madrid':(27,5,6,77,35),'Villarreal':(22,6,10,72,46)}),
}
for tag, (goals, top) in OFF_SPA.items():
    rs = spa_by_season[tag]
    st = standings(rs)
    g = sum(int(x[5]) + int(x[6]) for x in rs)
    ok = g == goals
    for club, (W, D, L, GF, GA) in top.items():
        s = st[club]
        if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, 3*W+D):
            ok = False
            print('    TABLE mismatch', tag, club, s)
    check(ok, f'SPA {tag} goals {g}=={goals} + top-3 table reproduction')
    per = Counter()
    for x in rs:
        per[x[4]] += 1; per[x[7]] += 1
    check(all(v == 38 for v in per.values()), f'SPA {tag} every club 38 matches ({len(per)} clubs)')

# ================================================================ KOS PACK
print('=' * 28, 'KOS pack', '=' * 28)
kos, kos_notes, kos_teams = parse_pack('handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.txt')
league = [x for x in kos if x[2] == 'Kosovo Superliga']
po = [x for x in kos if x[2] == 'Kosovo Relegation Playoffs']
check(len(kos) == 898, f'KOS total rows 898 (got {len(kos)})')
check(len(league) == 888 and len(po) == 10, f'KOS 888 league + 10 playoff (got {len(league)}/{len(po)})')
check(len(kos) == len({(x[1], x[4], x[7]) for x in kos}), 'KOS no duplicates')
check(all(datetime.date.fromisoformat(x[1]) <= datetime.date(2026, 8, 7) for x in kos), 'KOS no future-dated rows')
check(all(x[5].isdigit() and x[6].isdigit() for x in kos), 'KOS scores integer')
ROSTER = {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini',
          'Malisheva','Ferizaj','Prishtina E Re','Ulpiana','Feronikeli',"Trepça'89",
          'Fushë Kosova','Liria','Suhareka'}
extra = ({x[4] for x in league} | {x[7] for x in league}) - ROSTER
check(not extra, f'KOS league names all in 16-pool (extra: {sorted(extra) or "none"})')
po_extra = ({x[4] for x in po} | {x[7] for x in po}) - ROSTER
check(po_extra <= {'Vushtrria', 'Dinamo Fzaj.'}, f'KOS playoff outsiders only declared (got {sorted(po_extra)})')
check(len(kos_teams) == 8, f'KOS 8 TEAM rows (got {len(kos_teams)})')
labels = Counter(x[-1] for x in league)
check(labels.get('wf-kos-2526', 0) == 168 and 'rsssf-kosovo2026' not in labels,
      f'KOS 2025-26 league rows labeled wf-kos-2526 x168 (labels: {dict(labels)})')
plabels = Counter(x[-1] for x in po)
exp_pl = {'rsssf-kosovo2022': 2, 'rsssf-kosovo2023': 2, 'rsssf-kosovo2024': 2,
          'rsssf-kosovo2025': 2, 'rsssf-kosovo2026': 2}
check(dict(plabels) == exp_pl, f'KOS playoff rows labeled per-season RSSSF x2 each (got {dict(plabels)})')

KCODE = {'KF Ballkani':'BAL','Drenica Skenderaj':'DRE','Drita':'DRI','Dukagjini':'DUK',
         'Ferizaj':'FER','Gjilani':'GJI','Llapi':'LLA','Malisheva':'MAL','Prishtina':'PRI',
         'Prishtina E Re':'PRE'}
kmatrix = {}
for ln in open('team_workspace/researcher_handoffs/kos_ledgers/wikipedia-2025-26-matrix.txt', encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    m = re.match(r'^(match[12])_([A-Z]{3})_([A-Z]{3})=\s*([0-9]+)-([0-9]+)$', ln)
    if m:
        kmatrix[(m.group(1), m.group(2), m.group(3))] = (int(m.group(4)), int(m.group(5)))
check(len(kmatrix) == 180, f'KOS matrix cells 180 (got {len(kmatrix)})')
APP = {('2026-03-09','Malisheva','Prishtina'), ('2026-03-22','Malisheva','Llapi'),
 ('2026-04-05','Drita','Malisheva'), ('2026-04-11','Prishtina E Re','Malisheva'),
 ('2026-04-19','Malisheva','KF Ballkani'), ('2026-04-26','Dukagjini','Malisheva'),
 ('2026-04-29','Malisheva','Gjilani'), ('2026-05-02','Prishtina','Malisheva'),
 ('2026-05-10','Ferizaj','Malisheva'), ('2026-05-17','Malisheva','Drenica Skenderaj'),
 ('2026-05-24','Llapi','Malisheva'), ('2026-05-31','Malisheva','Drita')}
k26 = [x for x in league if season_of(x[1]) == '2025-26']
kmis = 0
for x in k26:
    leg = 'match1' if int(re.search(r'\d+', x[8]).group()) <= 18 else 'match2'
    key = (leg, KCODE[x[4]], KCODE[x[7]])
    if kmatrix.get(key) != (int(x[5]), int(x[6])):
        kmis += 1
        print('    MISMATCH:', x[1], x[4], x[5], x[6], x[7], 'matrix', kmatrix.get(key))
check(kmis == 1, f'KOS 2025-26 vs matrix: exactly 1 divergence (MD12 award; got {kmis})')
full26 = [x[:] for x in k26]
for (d, h, a) in APP:
    full26.append([None, d, 'Kosovo Superliga', 'domestic-league', h, '0', '0', a, 'RS'])
for x in full26:
    if x[5] == '0' and x[6] == '0' and (x[1], x[4], x[7]) in APP:
        key = ('match2', KCODE[x[4]], KCODE[x[7]])
        hg, ag = kmatrix[key]
        x[5], x[6] = str(hg), str(ag)
OFF_KOS = {
 '2021-22': {'KF Ballkani':(23,7,6,61,26,76),'Drita':(18,10,8,56,25,64),'Gjilani':(16,14,6,57,36,62)},
 '2022-23': {'KF Ballkani':(20,13,3,62,32,73),'Drita':(20,10,6,63,31,70),'Gjilani':(13,15,8,34,34,54)},
 '2023-24': {'KF Ballkani':(23,9,4,62,26,78),'Llapi':(21,8,7,56,27,71),'Drita':(19,10,7,49,27,67)},
 '2024-25': {'Drita':(22,8,6,59,26,74),'KF Ballkani':(17,11,8,61,39,62),'Malisheva':(14,11,11,44,39,53)},
 '2025-26': {'Drita':(20,6,10,50,35,66),'Malisheva':(18,5,13,58,50,59),'KF Ballkani':(17,7,12,61,41,58)},
}
for tag in OFF_KOS:
    rs = [x for x in full26] if tag == '2025-26' else [x for x in league if season_of(x[1]) == tag]
    st = standings(rs)
    ok = True
    for club, (W, D, L, GF, GA, Pts) in OFF_KOS[tag].items():
        s = st[club]
        if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, Pts):
            ok = False
            print('    TABLE mismatch', tag, club, s)
    check(ok, f'KOS {tag} top-3 table reproduction')
pk = {(x[1], x[4], x[7]) for x in k26}
check(not (pk & APP), 'KOS no appendix rows leaked')
for tag in OFF_KOS:
    rs = [x for x in league if season_of(x[1]) == tag]
    check(len({x[4] for x in rs} | {x[7] for x in rs}) == 10, f'KOS {tag} 10 clubs')

# ================================================================ KOSCUP
print('=' * 28, 'KOSCUP pack', '=' * 28)
cup, cup_notes, cup_teams = parse_pack('handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt')
check(len(cup) == 123, f'KOSCUP ties 123 (got {len(cup)})')
check(len(cup) == len({(x[1], x[4], x[7], x[8]) for x in cup}), 'KOSCUP no duplicates')
check(all(datetime.date.fromisoformat(x[1]) <= datetime.date(2026, 8, 7) for x in cup), 'KOSCUP no future-dated')
check(all(x[3] == 'domestic-cup' for x in cup), 'KOSCUP compType domestic-cup')
MEM = {
 '2021-22': {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini','Malisheva','Ulpiana','Feronikeli'},
 '2022-23': {'KF Ballkani','Drita','Gjilani','Dukagjini','Prishtina','Malisheva','Llapi','Ferizaj',"Trepça'89",'Drenica Skenderaj'},
 '2023-24': {'KF Ballkani','Llapi','Drita','Malisheva','Prishtina','Gjilani','Dukagjini','Feronikeli','Fushë Kosova','Liria'},
 '2024-25': {'Drita','KF Ballkani','Malisheva','Gjilani','Ferizaj','Prishtina','Dukagjini','Llapi','Suhareka','Feronikeli'},
 '2025-26': {'Drita','Malisheva','KF Ballkani','Dukagjini','Gjilani','Drenica Skenderaj','Prishtina','Llapi','Ferizaj','Prishtina E Re'},
}
bad_slice = [x for x in cup if not (x[4] in MEM[season_of(x[1])] or x[7] in MEM[season_of(x[1])])]
check(not bad_slice, f'KOSCUP every tie has >=1 Superliga club of that season ({len(bad_slice)} bad)')
sc = Counter((season_of(x[1]), x[8].split(' ')[0]) for x in cup)
exp_counts = {('2021-22','R1'):10, ('2021-22','R8'):6, ('2021-22','QF'):3, ('2021-22','SF'):4, ('2021-22','Final'):1,
              ('2022-23','R1'):10, ('2022-23','R8'):6, ('2022-23','QF'):3, ('2022-23','SF'):4, ('2022-23','Final'):1,
              ('2023-24','R1'):10, ('2023-24','R8'):6, ('2023-24','QF'):3, ('2023-24','SF'):4, ('2023-24','Final'):1,
              ('2024-25','R16'):10, ('2024-25','R8'):7, ('2024-25','QF'):4, ('2024-25','SF'):4, ('2024-25','Final'):1,
              ('2025-26','R16'):10, ('2025-26','R8'):6, ('2025-26','QF'):4, ('2025-26','SF'):4, ('2025-26','Final'):1}
check(dict(sc) == exp_counts, 'KOSCUP per-edition stage counts match expected', str(dict(sc)))
finals = {season_of(x[1]): (x[4], int(x[5]), int(x[6]), x[7]) for x in cup if x[8] == 'Final'}
exp_finals = {'2021-22': ('Llapi', 2, 1, 'Drita'), '2022-23': ('Prishtina', 2, 0, 'Gjilani'),
              '2023-24': ('KF Ballkani', 2, 2, 'Prishtina'), '2024-25': ('Prishtina', 1, 0, 'Llapi'),
              '2025-26': ('Ferizaj', 1, 2, 'Dukagjini')}
check(finals == exp_finals, 'KOSCUP finals match RSSSF', str(finals))
for tag in ['2021-22','2022-23','2023-24','2024-25','2025-26']:
    sf = {x[4] for x in cup if season_of(x[1]) == tag and x[8].startswith('SF')}
    sf |= {x[7] for x in cup if season_of(x[1]) == tag and x[8].startswith('SF')}
    check(len(sf) == 4, f'KOSCUP {tag} four semifinalists', str(sorted(sf)))
adv_notes = [n for n in cup_notes if n.startswith('NOTE|info|advancement')]
spot = {
 ('2021-12-01','Feronikeli','Fushë Kosova'): 'Fushë Kosova',
 ('2021-12-02','Drita','Drenasi'): 'Drita',
 ('2022-02-05','Ulpiana','Arberia'): 'Ulpiana',
 ('2022-02-06','Prishtina','Drenica Skenderaj'): 'Prishtina',
 ('2022-03-17','KF Ballkani','Prishtina'): 'Prishtina',
 ('2022-11-17','Vellaznimi','Prishtina'): 'Prishtina',
 ('2022-11-17','Behari','Ferizaj'): 'Behari',
 ('2023-02-04','Feronikeli',"Trepça'89"): "Trepça'89",
 ('2024-12-03','Rilindja 74','KF Ballkani'): 'Rilindja 74',
 ('2026-02-10','Drenica Skenderaj','Ferizaj'): 'Ferizaj',
 ('2026-02-11','Prishtina','KF Ballkani'): 'KF Ballkani',
}
for (d, h, a), winner in spot.items():
    found = [n for n in adv_notes if d in n and h in n and a in n]
    ok = bool(found) and winner in found[0]
    check(ok, f'KOSCUP advancement {d} {h}-{a} -> {winner}', found[0][:100] if found else 'NO NOTE')
wo = [n for n in cup_notes if 'walkover' in n]
check(len(wo) >= 1 and any('Vellaznimi' in n and 'Prishtina advanced' in n for n in wo),
      'KOSCUP walkover awarded NOTE present')
non_sl = set()
for x in cup:
    for side in (4, 7):
        if x[side] not in ROSTER:
            non_sl.add(x[side])
teamed = {t.split('|')[1] for t in cup_teams}
check(not (non_sl - teamed), f'KOSCUP TEAM rows cover all {len(non_sl)} lower-division clubs')

print('=' * 28, 'SUMMARY', '=' * 28)
if FAIL:
    print(f'{len(FAIL)} FAILURES:')
    for f in FAIL:
        print('  -', f)
else:
    print('ALL CHECKS PASSED — the three packs are internally consistent and match the independently re-fetched sources.')
