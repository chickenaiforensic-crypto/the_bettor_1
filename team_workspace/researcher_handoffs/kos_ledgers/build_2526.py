#!/usr/bin/env python3
"""Build 2025-26 Kosovo Superliga rows: worldfootball carrier (dates+scores) cross-checked
against the Wikipedia FBR matrix; verify vs the RSSSF official table."""
import json, re

LEDGER = 'team_workspace/researcher_handoffs/kos_ledgers'

CODE = {'KF Ballkani':'BAL','Drenica Skenderaj':'DRE','Drita':'DRI','Dukagjini':'DUK',
        'Ferizaj':'FER','Gjilani':'GJI','Llapi':'LLA','Malisheva':'MAL','Prishtina':'PRI',
        'Prishtina E Re':'PRE'}

# official 2025-26 table (RSSSF kosovo2026): club -> (W, D, L, GF, GA, Pts)
OFFICIAL = {
 'Drita': (20, 6, 10, 50, 35, 66), 'Malisheva': (18, 5, 13, 58, 50, 59),
 'KF Ballkani': (17, 7, 12, 61, 41, 58), 'Dukagjini': (13, 12, 11, 42, 36, 51),
 'Gjilani': (14, 9, 13, 47, 48, 51), 'Drenica Skenderaj': (15, 5, 16, 46, 55, 50),
 'Prishtina': (13, 10, 13, 52, 51, 49), 'Llapi': (13, 10, 13, 46, 50, 49),
 'Ferizaj': (9, 9, 18, 40, 55, 36), 'Prishtina E Re': (8, 7, 21, 39, 60, 31),
}

# appendix rows (already held - MUST NOT be returned)
APPENDIX = {
 ('2026-03-09','Malisheva','Prishtina'), ('2026-03-22','Malisheva','Llapi'),
 ('2026-04-05','Drita','Malisheva'), ('2026-04-11','Prishtina E Re','Malisheva'),
 ('2026-04-19','Malisheva','KF Ballkani'), ('2026-04-26','Dukagjini','Malisheva'),
 ('2026-04-29','Malisheva','Gjilani'), ('2026-05-02','Prishtina','Malisheva'),
 ('2026-05-10','Ferizaj','Malisheva'), ('2026-05-17','Malisheva','Drenica Skenderaj'),
 ('2026-05-24','Llapi','Malisheva'), ('2026-05-31','Malisheva','Drita'),
}

# load matrix
matrix = {}
for ln in open(f'{LEDGER}/wikipedia-2025-26-matrix.txt', encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    m = re.match(r'^(match[12])_([A-Z]{3})_([A-Z]{3})=\s*(\d+)-(\d+)$', ln)
    if m:
        matrix[(m.group(1), m.group(2), m.group(3))] = (int(m.group(4)), int(m.group(5)))
print(f'matrix cells: {len(matrix)} (expect 180)')

# load carrier
rows = []
for ln in open(f'{LEDGER}/wf-2025-26-carrier.txt', encoding='utf-8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'):
        continue
    md, date, home, hg, ag, away = ln.split('|')
    nm = {'Drenica': 'Drenica Skenderaj', 'Ballkani': 'KF Ballkani'}
    home, away = nm.get(home, home), nm.get(away, away)
    rows.append({'season': '2025-26', 'round': int(md[2:]), 'date': date,
                 'home': home, 'hg': int(hg), 'ag': int(ag), 'away': away})
print(f'carrier rows: {len(rows)} (expect 180)')

# cross-check vs matrix
mism = []
for r in rows:
    leg = 'match1' if r['round'] <= 18 else 'match2'
    key = (leg, CODE[r['home']], CODE[r['away']])
    mv = matrix.get(key)
    if mv is None:
        mism.append((r, 'NO MATRIX CELL'))
    elif mv != (r['hg'], r['ag']):
        mism.append((r, f'matrix {mv[0]}-{mv[1]}'))
print(f'matrix mismatches: {len(mism)}')
for r, why in mism:
    print('  ', r['round'], r['date'], r['home'], r['hg'], r['ag'], r['away'], '->', why)

# table reproduction
st = {}
for r in rows:
    for side in ('home','away'):
        st.setdefault(r[side], {'W':0,'D':0,'L':0,'GF':0,'GA':0,'Pts':0})
    h, a = st[r['home']], st[r['away']]
    h['GF'] += r['hg']; h['GA'] += r['ag']; a['GF'] += r['ag']; a['GA'] += r['hg']
    if r['hg'] > r['ag']: h['W'] += 1; a['L'] += 1; h['Pts'] += 3
    elif r['hg'] < r['ag']: a['W'] += 1; h['L'] += 1; a['Pts'] += 3
    else: h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
ok = True
for club, (W, D, L, GF, GA, Pts) in OFFICIAL.items():
    s = st[club]
    if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, Pts):
        print(f'  TABLE MISMATCH {club}: official {W}-{D}-{L} {GF}-{GA} {Pts} vs {s}')
        ok = False
print(f'table reproduction vs RSSSF 2025-26: {"PASS" if ok else "FAIL"} ({len(OFFICIAL)} clubs)')

# appendix presence check
car = {(r['date'], r['home'], r['away']) for r in rows}
missing_app = APPENDIX - car
print(f'appendix rows found in carrier: {len(APPENDIX - missing_app)}/12; missing: {missing_app or "none"}')

# goals + span
print(f'goals: {sum(r["hg"]+r["ag"] for r in rows)} (RSSSF table GF sum check: {sum(v[3] for v in OFFICIAL.values())})')
print(f'span: {rows[0]["date"]}..{rows[-1]["date"]}')
json.dump(rows, open(f'{LEDGER}/kos-2025-26-league.json', 'w'), indent=1)
print('saved kos-2025-26-league.json')
