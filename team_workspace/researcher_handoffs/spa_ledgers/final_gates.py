#!/usr/bin/env python3
"""Final acceptance gates on the SPA pack file (fresh code, mirrors WO section 5)."""
import re, datetime
from collections import Counter

PACK = 'handoffs/SPA-2021-2026_BP-TEAM-PACK_v2.txt'
ROSTER = {'Alaves','Almeria','Ath Bilbao','Ath Madrid','Barcelona','Betis','Cadiz','Celta',
          'Elche','Espanol','Getafe','Girona','Granada','Las Palmas','Leganes','Levante',
          'Mallorca','Osasuna','Oviedo','Real Madrid','Sevilla','Sociedad','Valencia',
          'Valladolid','Vallecano','Villarreal'}

# Official tables: (W, D, L, GF, GA) per club per season. 2021-22..2024-25 = RSSSF printed
# tables (local primary); 2025-26 = LaLiga official table via Wikipedia template.
TABLES = {
'2021-22': {'Real Madrid':(26,8,4,80,31),'Barcelona':(21,10,7,68,38),'Ath Madrid':(21,8,9,65,43),
 'Sevilla':(18,16,4,53,30),'Betis':(19,8,11,62,40),'Sociedad':(17,11,10,40,37),'Villarreal':(16,11,11,63,37),
 'Ath Bilbao':(14,13,11,43,36),'Valencia':(11,15,12,48,53),'Osasuna':(12,11,15,37,51),'Celta':(12,10,16,43,43),
 'Vallecano':(11,9,18,39,50),'Elche':(11,9,18,40,52),'Espanol':(10,12,16,40,53),'Getafe':(8,15,15,33,41),
 'Mallorca':(10,9,19,36,63),'Cadiz':(8,15,15,35,51),'Granada':(8,14,16,44,61),'Levante':(8,11,19,51,76),
 'Alaves':(8,7,23,31,65)},
'2022-23': {'Barcelona':(28,4,6,70,20),'Real Madrid':(24,6,8,75,36),'Ath Madrid':(23,8,7,70,33),
 'Sociedad':(21,8,9,51,35),'Villarreal':(19,7,12,59,40),'Betis':(17,9,12,46,41),'Osasuna':(15,8,15,37,42),
 'Ath Bilbao':(14,9,15,47,43),'Mallorca':(14,8,16,37,43),'Girona':(13,10,15,58,55),'Vallecano':(13,10,15,45,53),
 'Sevilla':(13,10,15,47,54),'Celta':(11,10,17,43,53),'Cadiz':(10,12,16,30,53),'Getafe':(10,12,16,34,45),
 'Valencia':(11,9,18,42,45),'Almeria':(11,8,19,49,65),'Valladolid':(11,7,20,33,63),'Espanol':(8,13,17,52,69),
 'Elche':(5,10,23,30,67)},
'2023-24': {'Real Madrid':(29,8,1,87,26),'Barcelona':(26,7,5,79,44),'Girona':(25,6,7,85,46),
 'Ath Madrid':(24,4,10,70,43),'Ath Bilbao':(19,11,8,61,37),'Sociedad':(16,12,10,51,39),'Betis':(14,15,9,48,45),
 'Villarreal':(14,11,13,65,65),'Valencia':(13,10,15,40,45),'Alaves':(12,10,16,36,46),'Osasuna':(12,9,17,45,56),
 'Getafe':(10,13,15,42,54),'Celta':(10,11,17,46,57),'Sevilla':(10,11,17,48,54),'Mallorca':(8,16,14,33,44),
 'Las Palmas':(10,10,18,33,47),'Vallecano':(8,14,16,29,48),'Cadiz':(6,15,17,26,55),'Almeria':(3,12,23,43,75),
 'Granada':(4,9,25,38,79)},
'2024-25': {'Barcelona':(28,4,6,102,39),'Real Madrid':(26,6,6,78,38),'Ath Madrid':(22,10,6,68,30),
 'Ath Bilbao':(19,13,6,54,29),'Villarreal':(20,10,8,71,51),'Betis':(16,12,10,57,50),'Celta':(16,7,15,59,57),
 'Vallecano':(13,13,12,41,45),'Osasuna':(12,16,10,48,52),'Mallorca':(13,9,16,35,44),'Sociedad':(13,7,18,35,46),
 'Valencia':(11,13,14,44,54),'Getafe':(11,9,18,34,39),'Espanol':(11,9,18,40,51),'Alaves':(10,12,16,38,48),
 'Girona':(11,8,19,44,60),'Sevilla':(10,11,17,42,55),'Leganes':(9,13,16,39,56),'Las Palmas':(8,8,22,40,61),
 'Valladolid':(4,4,30,26,90)},
'2025-26': {'Barcelona':(31,1,6,95,36),'Real Madrid':(27,5,6,77,35),'Villarreal':(22,6,10,72,46),
 'Ath Madrid':(21,6,11,62,44),'Betis':(15,15,8,59,48),'Celta':(14,12,12,53,48),'Getafe':(15,6,17,32,38),
 'Vallecano':(12,14,12,41,44),'Valencia':(13,10,15,46,55),'Sociedad':(11,13,14,59,61),'Espanol':(12,10,16,43,55),
 'Ath Bilbao':(13,6,19,43,58),'Sevilla':(12,7,19,46,60),'Alaves':(11,10,17,44,56),'Elche':(10,13,15,49,57),
 'Levante':(11,9,18,47,61),'Osasuna':(11,9,18,44,50),'Mallorca':(11,9,18,47,57),'Girona':(9,14,15,39,55),
 'Oviedo':(6,11,21,26,60)},
}
SEASON_OF = {}
for tag in TABLES:
    y0 = int(tag[:4]); y1 = y0 + 1
    SEASON_OF[(y0, y1)] = tag

rows, notes, sources = [], [], []
for ln in open(PACK, encoding='utf-8'):
    ln = ln.rstrip('\n')
    if ln.startswith('MATCH|'):
        f = ln.split('|')
        assert len(f) == 14, f'field count {len(f)}: {ln[:80]}'
        rows.append(f)
    elif ln.startswith('NOTE|'):
        notes.append(ln)
    elif ln.startswith('SOURCE|'):
        sources.append(ln)

print(f'MATCH rows: {len(rows)} (expect 1900) | NOTE lines: {len(notes)} | SOURCE lines: {len(sources)}')
assert rows[-1] and open(PACK).read().rstrip().endswith('END'), 'END terminator missing'

# per-season structure
by_season = {}
for f in rows:
    d = datetime.date.fromisoformat(f[1])
    y0 = d.year if d.month >= 8 else d.year - 1
    tag = SEASON_OF[(y0, y0 + 1)] if (y0, y0 + 1) in SEASON_OF else None
    by_season.setdefault(tag, []).append(f)
for tag, r in sorted(by_season.items(), key=lambda kv: kv[0] or ""):
    rc = Counter(x[8] for x in r)   # MD label
    goals = sum(int(x[5]) + int(x[6]) for x in r)
    dup = len(r) - len({(x[1], x[4], x[7]) for x in r})
    print(f'  {tag}: rows={len(r)} rounds={len(rc)} goals={goals} dupes={dup} '
          f'span={min(x[1] for x in r)}..{max(x[1] for x in r)}')

# roster check
names = {x[4] for x in rows} | {x[7] for x in rows}
bad = names - ROSTER
print(f'non-roster names: {sorted(bad) if bad else "none"}')
# scores
badscore = [x for x in rows if not (x[5].isdigit() and x[6].isdigit()) or int(x[5]) > 30 or int(x[6]) > 30]
print(f'non-integer/oversize scores: {len(badscore)}')
# future dates
today = datetime.date(2026, 8, 6)
fut = [x for x in rows if datetime.date.fromisoformat(x[1]) > today]
print(f'future-dated rows: {len(fut)}')
# competition string + comptype
comp = {x[2] for x in rows}; ct = {x[3] for x in rows}
print(f'competition strings: {comp} | compTypes: {ct} | venue MD labels: {len({x[8] for x in rows})} distinct')
# table reproduction from pack rows
def standings(r):
    st = {}
    for x in r:
        for s in ('home','away'):
            st.setdefault(x[4] if s=='home' else x[7], {'W':0,'D':0,'L':0,'GF':0,'GA':0,'Pts':0})
        h = st[x[4]]; a = st[x[7]]
        hg, ag = int(x[5]), int(x[6])
        h['GF'] += hg; h['GA'] += ag; a['GF'] += ag; a['GA'] += hg
        if hg > ag: h['W'] += 1; a['L'] += 1; h['Pts'] += 3
        elif hg < ag: a['W'] += 1; h['L'] += 1; a['Pts'] += 3
        else: h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
    return st
allok = True
for tag, r in sorted(by_season.items(), key=lambda kv: kv[0] or ""):
    st = standings(r)
    off = TABLES[tag]
    for club, (W, D, L, GF, GA) in off.items():
        s = st.get(club)
        if s is None or (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, 3*W+D):
            print(f'  TABLE MISMATCH {tag} {club}: official {W}-{D}-{L} {GF}-{GA} {3*W+D} vs {s}')
            allok = False
    per_club = Counter()
    for x in r:
        per_club[x[4]] += 1; per_club[x[7]] += 1
    badc = {c: n for c, n in per_club.items() if n != 38}
    if badc:
        print(f'  CLUB-COUNT MISMATCH {tag}: {badc}'); allok = False
print(f'table reproduction (all 5 seasons, 100 clubs): {"PASS" if allok else "FAIL"}')
print(f'END line present: {open(PACK).read().rstrip().endswith("END")}')
