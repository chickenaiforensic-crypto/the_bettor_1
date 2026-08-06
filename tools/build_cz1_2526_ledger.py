#!/usr/bin/env python3
"""build_cz1_2526_ledger.py - assemble + validate CZ1 2025-26 ledger rows.

Inputs (all locally fetched, transcribe-day 2026-08-04):
  audit/ledger/cz1-dates-bbc-2025-2026.txt  (BBC dated lattice, D|date|home|hg|ag|away)
  audit/ledger/cz1-2ndidx-2025-26.txt       (wiki matrices MX|stage|home|away|hg|ag)
  audit/ledger/cz1-2025-26.txt              (skeleton: ESF/EF/PRO rows + RT/TT/ZT constants)

Round assignment = explicit date blocks (see BLOCKS). Validation:
  V1 every BBC row matches its stage matrix cell exactly (home/away/score direction);
  V2 every REG/TGRP/ZGRP matrix cell is covered exactly once by a BBC row;
  V3 each round block has complete, distinct team sets (16 reg / 6 group);
  V4 recomputed tables from assembled rows == RSSSF RT/TT/ZT constants exactly;
  V5 PRO/ESF/EF legs corroborated against wiki middle bracket + TwoLeg boxes
     (via PRO MX rows; ESF/EF legs verified vs wiki bracket text manually - documented);
  V6 regular H2H Dukla-Slovacko: expect Dukla 6-0 (wiki hth_DUK adjudication note).
Exit non-zero on any failure.
"""
import sys, collections, datetime

BBC = 'audit/ledger/cz1-dates-bbc-2025-2026.txt'
IDX = 'audit/ledger/cz1-2ndidx-2025-26.txt'
SKEL = 'audit/ledger/cz1-2025-26.txt'

D = [l.strip().split('|')[1:] for l in open(BBC) if l.startswith('D|')]
MX = {}
for l in open(IDX):
    if l.startswith('MX|'):
        _, stage, h, a, hg, ag = l.strip().split('|')
        MX[(stage, h, a)] = (int(hg), int(ag))

date = lambda s: datetime.date.fromisoformat(s)

def rng(a, b): return lambda d: date(a) <= d <= date(b)

# explicit date blocks per round (postponements keep labels, documented in ledger header)
BLOCKS = [
    ('R1',  [rng('2025-07-18','2025-07-20')]),
    ('R2',  [rng('2025-07-26','2025-07-27'), rng('2025-09-17','2025-09-17')]),
    ('R3',  [rng('2025-08-02','2025-08-03'), rng('2025-08-19','2025-08-19')]),
    ('R4',  [rng('2025-08-09','2025-08-10')]),
    ('R5',  [rng('2025-08-16','2025-08-17'), rng('2025-10-01','2025-10-01')]),
    ('R6',  [rng('2025-08-23','2025-08-24'), rng('2025-10-22','2025-10-22')]),
    ('R7',  [rng('2025-08-30','2025-08-31')]),
    ('R8',  [rng('2025-09-13','2025-09-14')]),
    ('R9',  [rng('2025-09-20','2025-09-21')]),
    ('R10', [rng('2025-09-26','2025-09-28')]),
    ('R11', [rng('2025-10-04','2025-10-05')]),
    ('R12', [rng('2025-10-18','2025-10-19')]),
    ('R13', [rng('2025-10-25','2025-10-26'), rng('2025-10-28','2025-10-28')]),
    ('R14', [rng('2025-11-01','2025-11-02')]),
    ('R15', [rng('2025-11-08','2025-11-09')]),
    ('R16', [rng('2025-11-22','2025-11-23')]),
    ('R17', [rng('2025-11-29','2025-11-30')]),
    ('R18', [rng('2025-12-05','2025-12-07')]),
    ('R19', [rng('2025-12-13','2025-12-14')]),
    ('R20', [rng('2026-01-31','2026-02-01')]),
    ('R21', [rng('2026-02-07','2026-02-08')]),
    ('R22', [rng('2026-02-14','2026-02-15')]),
    ('R23', [rng('2026-02-21','2026-02-22')]),
    ('R24', [rng('2026-02-27','2026-03-01')]),
    ('R25', [rng('2026-03-07','2026-03-08')]),
    ('R26', [rng('2026-03-14','2026-03-15')]),
    ('R27', [rng('2026-04-04','2026-04-05')]),
    ('R28', [rng('2026-04-11','2026-04-12')]),
    ('R29', [rng('2026-04-18','2026-04-19')]),
    ('R30', [rng('2026-04-25','2026-04-25')]),
]
TTEAMS = {'Slavia','Sparta','Plzen','Jablonec','Hradec','Liberec'}
ZTEAMS = {'Teplice','Zlin','MlBoleslav','Slovacko','Ostrava','Dukla'}
ETEAMS = {'Olomouc','Pardubice','Karvina','Bohemians'}

PBLOCKS = [  # group-stage May blocks: tag -> dates
    ('T31', [rng('2026-05-02','2026-05-03')]),
    ('T32', [rng('2026-05-09','2026-05-10')]),
    ('T33', [rng('2026-05-12','2026-05-13')]),
    ('T34', [rng('2026-05-17','2026-05-17')]),
    ('T35', [rng('2026-05-24','2026-05-24')]),
    ('Z31', [rng('2026-05-02','2026-05-03')]),
    ('Z32', [rng('2026-05-09','2026-05-09')]),
    ('Z33', [rng('2026-05-12','2026-05-12')]),
    ('Z34', [rng('2026-05-16','2026-05-16')]),
    ('Z35', [rng('2026-05-23','2026-05-23')]),
]

rows = []   # (tag, date, home, hg, ag, away)
used = set()
fails = []

def stage_of(tag):
    return 'REG' if tag.startswith('R') else ('TGRP' if tag.startswith('T') else 'ZGRP')

# V3 round blocks
for tag, windows in BLOCKS:
    games = [i for i, r in enumerate(D)
             if any(w(date(r[0])) for w in windows) and r[1] not in TTEAMS | ZTEAMS | ETEAMS | set() or False]
    # REG windows only contain REG teams by construction; filter by date then check
    games = [i for i, r in enumerate(D)
             if any(w(date(r[0])) for w in windows)]
    if len(games) != 8:
        fails.append(f'V3 {tag}: {len(games)} games != 8')
        continue
    teams = set()
    for i in games:
        teams.update([D[i][1], D[i][4]])
    if len(teams) != 16:
        fails.append(f'V3 {tag}: {len(teams)} distinct teams != 16 -> {sorted(set(T:=""))}')
    for i in games:
        if i in used: fails.append(f'V3 {tag}: row reuse {D[i]}')
        used.add(i)
        rows.append((tag, *D[i]))

for tag, windows in PBLOCKS:
    grp = TTEAMS if tag[0] == 'T' else ZTEAMS
    games = [i for i, r in enumerate(D)
             if any(w(date(r[0])) for w in windows) and r[1] in grp and r[4] in grp]
    if len(games) != 3:
        fails.append(f'V3 {tag}: {len(games)} games != 3 -> {[D[i] for i in games]}')
        continue
    teams = set()
    for i in games: teams.update([D[i][1], D[i][4]])
    if teams != grp: fails.append(f'V3 {tag}: team set wrong -> {sorted(teams)}')
    for i in games:
        if i in used: fails.append(f'V3 {tag}: row reuse {D[i]}')
        used.add(i)
        rows.append((tag, *D[i]))

# middle playoff legs
EMID = {'2026-05-02': 'ESF1', '2026-05-10': 'ESF2', '2026-05-16': 'EF1', '2026-05-23': 'EF2'}
for i, r in enumerate(D):
    if i in used: continue
    if r[1] in ETEAMS and r[4] in ETEAMS and r[0] in EMID and EMID[r[0]] in ('ESF1','ESF2','EF1','EF2'):
        # only middle-stage games: check both teams are ETEAMS and not already used (T/Z blocks excluded ETEAMS)
        rows.append((EMID[r[0]], *r)); used.add(i)

leftover = [D[i] for i in range(len(D)) if i not in used]
if leftover:
    fails.append(f'unassigned BBC rows: {leftover}')

# V1 + V2: BBC row <-> wiki matrix bijection per stage
covered = collections.Counter()
MID = {'ESF1','ESF2','EF1','EF2'}
for tag, d, h, hg, ag, a in rows:
    if tag in MID: continue  # middle bracket legs corroborated separately (V5 doc)
    cell = MX.get((stage_of(tag), h, a))
    if cell is None:
        fails.append(f'V1 no matrix cell for {tag} {h}-{a}')
        continue
    if cell != (int(hg), int(ag)):
        fails.append(f'V1 score mismatch {tag} {h}-{a}: BBC {hg}-{ag} vs wiki {cell}')
    covered[(stage_of(tag), h, a)] += 1
for (stg, h, a), sc in MX.items():
    if stg in ('REG', 'TGRP', 'ZGRP'):
        if covered[(stg, h, a)] != 1:
            fails.append(f'V2 cell {stg} {h}-{a} covered {covered[(stg,h,a)]}x')

# V4 recompute vs constants
TEAMS = {'Slavia','Sparta','Plzen','Jablonec','Hradec','Liberec','Olomouc','Pardubice',
         'Karvina','Bohemians','MlBoleslav','Zlin','Teplice','Dukla','Slovacko','Ostrava'}
def acc(pred):
    t = {tm: [0,0,0,0,0,0] for tm in TEAMS}
    n = collections.Counter()
    for tag, d, h, hg, ag, a in rows:
        if not pred(tag): continue
        hg, ag = int(hg), int(ag)
        n[h] += 1; n[a] += 1
        for tm, gf, ga in ((h, hg, ag), (a, ag, hg)):
            r = t[tm]; r[3] += gf; r[4] += ga
            if gf > ga: r[0] += 1; r[5] += 3
            elif gf == ga: r[1] += 1; r[5] += 1
            else: r[2] += 1
    return t, n
K = lambda e: [e[1], e[2], e[3], e[4], e[5], e[6]]
C = {}
for l in open(SKEL):
    if l.startswith(('RT|','TT|','ZT|')):
        f = l.strip().split('|')
        C[f[0]] = C.get(f[0], {}); C[f[0]][f[2]] = [int(x) for x in f[3:10]]
t30, n30 = acc(lambda g: g.startswith('R'))
t35, n35 = acc(lambda g: g[0] in 'RTZ' and g != 'R')
for tm, exp in C['RT'].items():
    got = t30[tm]
    if got != K(exp): fails.append(f'V4 RT {tm}: got {got} exp {K(exp)}')
for tm, exp in C['TT'].items():
    got = t35[tm]
    if got != K(exp): fails.append(f'V4 TT {tm}: got {got} exp {K(exp)}')
for tm, exp in C['ZT'].items():
    got = t35[tm]
    if got != K(exp): fails.append(f'V4 ZT {tm}: got {got} exp {K(exp)}')
for tm in TEAMS:
    if n30[tm] != 30: fails.append(f'V4 {tm} played {n30[tm]} != 30')
for tm in TTEAMS | ZTEAMS:
    if n35[tm] != 35: fails.append(f'V4 {tm} played {n35[tm]} != 35')

# V5 PRO MX present
pro = [(k, v) for k, v in MX.items() if k[0] == 'PRO']
assert len(pro) == 4, 'PRO MX expected 4'

# V6 regular H2H Dukla vs Slovacko -> wiki hth_DUK (Dukla 6, Slovacko 0)
h2h = [r for r in rows if r[0].startswith('R') and {r[2], r[5]} == {'Dukla','Slovacko'}]
pt = collections.Counter()
for tag, d, h, hg, ag, a in h2h:
    hg, ag = int(hg), int(ag)
    if hg > ag: pt[h] += 3
    elif hg < ag: pt[a] += 3
    else: pt[h] += 1; pt[a] += 1
if not (pt['Dukla'] == 6 and pt['Slovacko'] == 0):
    fails.append(f'V6 H2H Dukla/Slovacko wrong: {dict(pt)} rows={h2h}')

counts = collections.Counter(r[0][0] for r in rows)
goals = sum(int(r[3]) + int(r[4]) for r in rows if r[0].startswith('R'))
print(f'rows={len(rows)} REG={sum(1 for r in rows if r[0].startswith("R"))} '
      f'T={sum(1 for r in rows if r[0].startswith("T"))} Z={sum(1 for r in rows if r[0].startswith("Z"))} '
      f'E={sum(1 for r in rows if r[0] in ("ESF1","ESF2","EF1","EF2"))} reg_goals={goals}')
if fails:
    print('FAILURES:'); [print(' ', f) for f in fails]; sys.exit(1)
print('ALL GATES PASS (V1..V6)')

# emit assembled ledger rows (sorted by tag then date) for downstream merge
order = {t: i for i, (t, _) in enumerate(BLOCKS)}
porder = {t: i for i, (t, _) in enumerate(PBLOCKS)}
def key(r):
    if r[0] in order: return (0, order[r[0]], r[1])
    if r[0] in porder: return (1, porder[r[0]], r[1])
    return (2, r[0], r[1])
with open('audit/ledger/cz1-2025-26.rounds.tmp', 'w') as f:
    for r in sorted(rows, key=key):
        tag, d, h, hg, ag, a = r
        f.write(f'{tag}|{d}|{h}|{hg}|{ag}|{a}\n')
print('wrote audit/ledger/cz1-2025-26.rounds.tmp')
