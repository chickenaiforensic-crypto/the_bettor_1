#!/usr/bin/env python3
"""Validate the 2025-26 carrier rows (fbref transcription) for the SPA pack."""
import sys, json, datetime

ROSTER = {'Alaves','Almeria','Ath Bilbao','Ath Madrid','Barcelona','Betis','Cadiz','Celta',
          'Elche','Espanol','Getafe','Girona','Granada','Las Palmas','Leganes','Levante',
          'Mallorca','Osasuna','Oviedo','Real Madrid','Sevilla','Sociedad','Valencia',
          'Valladolid','Vallecano','Villarreal'}

# Official 2025-26 final table (Wikipedia Template:2025-26 La Liga table, source LaLiga EA Sports)
# club: (W, D, L, GF, GA)
OFFICIAL = {
    'Barcelona':   (31, 1, 6, 95, 36),
    'Real Madrid': (27, 5, 6, 77, 35),
    'Villarreal':  (22, 6, 10, 72, 46),
    'Ath Madrid':  (21, 6, 11, 62, 44),
    'Betis':       (15, 15, 8, 59, 48),
    'Celta':       (14, 12, 12, 53, 48),
    'Getafe':      (15, 6, 17, 32, 38),
    'Vallecano':   (12, 14, 12, 41, 44),
    'Valencia':    (13, 10, 15, 46, 55),
    'Sociedad':    (11, 13, 14, 59, 61),
    'Espanol':     (12, 10, 16, 43, 55),
    'Ath Bilbao':  (13, 6, 19, 43, 58),
    'Sevilla':     (12, 7, 19, 46, 60),
    'Alaves':      (11, 10, 17, 44, 56),
    'Elche':       (10, 13, 15, 49, 57),
    'Levante':     (11, 9, 18, 47, 61),
    'Osasuna':     (11, 9, 18, 44, 50),
    'Mallorca':    (11, 9, 18, 47, 57),
    'Girona':      (9, 14, 15, 39, 55),
    'Oviedo':      (6, 11, 21, 26, 60),
}

def load(path):
    rows = []
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        md, date, home, hg, ag, away, venue = ln.split('|')
        rows.append({'round': int(md[2:]), 'date': date, 'home': home, 'hg': int(hg),
                     'ag': int(ag), 'away': away, 'venue': venue})
    return rows

def standings(rows):
    st = {}
    for x in rows:
        for side in ('home', 'away'):
            st.setdefault(x[side], {'P':0,'W':0,'D':0,'L':0,'GF':0,'GA':0,'Pts':0})
        h, a = st[x['home']], st[x['away']]
        h['P'] += 1; a['P'] += 1
        h['GF'] += x['hg']; h['GA'] += x['ag']
        a['GF'] += x['ag']; a['GA'] += x['hg']
        if x['hg'] > x['ag']: h['W'] += 1; a['L'] += 1; h['Pts'] += 3
        elif x['hg'] < x['ag']: a['W'] += 1; h['L'] += 1; a['Pts'] += 3
        else: h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
    return st

rows = load('team_workspace/researcher_handoffs/spa_ledgers/spa-2025-26-fbref.txt')
print(f'rows: {len(rows)} (expect 380)')
# round counts
from collections import Counter
rc = Counter(r['round'] for r in rows)
bad = {k: v for k, v in rc.items() if v != 10}
print(f'rounds: {len(rc)}, bad rounds (!=10): {bad if bad else "none"}')
# duplicates
dups = len(rows) - len({(r['date'], r['home'], r['away']) for r in rows})
print(f'duplicates: {dups}')
# names
off = {r['home'] for r in rows} | {r['away'] for r in rows}
print(f'non-roster names: {sorted(off - ROSTER) if off - ROSTER else "none"}')
# future dates
today = datetime.date(2026, 8, 6)
future = [r for r in rows if datetime.date.fromisoformat(r['date']) > today]
print(f'future-dated rows: {len(future)}')
# date-sorted?
ds = [r['date'] for r in rows]
print(f'date-sorted: {ds == sorted(ds)}; span: {ds[0]}..{ds[-1]}')
# goals
print(f'goals: {sum(r["hg"]+r["ag"] for r in rows)} (expect 1024)')
# table reproduction
st = standings(rows)
ok = True
for club, (W, D, L, GF, GA) in OFFICIAL.items():
    s = st[club]
    if (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, 3*W+D):
        print(f'  MISMATCH {club}: official {W}-{D}-{L} {GF}-{GA} {3*W+D} vs recompute '
              f'{s["W"]}-{s["D"]}-{s["L"]} {s["GF"]}-{s["GA"]} {s["Pts"]}')
        ok = False
print(f'table reproduction vs official: {"PASS" if ok else "FAIL"} ({len(OFFICIAL)} clubs)')
# per-club match counts
cnt = Counter()
for r in rows:
    cnt[r['home']] += 1; cnt[r['away']] += 1
badc = {c: n for c, n in cnt.items() if n != 38}
print(f'per-club 38-gate: {"PASS" if not badc else badc} ({len(cnt)} clubs)')
json.dump(rows, open('team_workspace/researcher_handoffs/spa_ledgers/spa-2025-26-rows.json', 'w'), indent=1)
print('saved spa-2025-26-rows.json')
