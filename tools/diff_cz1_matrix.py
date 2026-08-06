#!/usr/bin/env python3
"""diff_cz1_matrix.py - cross-check a CZ1 ledger season against its wiki FBR second index.

Usage: python3 tools/diff_cz1_matrix.py <season-ledger> <2ndidx-file>
Gate: every REG/TGRP/ZGRP MX cell is covered exactly once by a ledger R*/T*/Z* row with
identical direction+score; every such ledger row exists in the matrix; PRO MX rows match
ledger PRO rows (date-agnostic, order-agnostic).
"""
import sys, collections

led, idx = sys.argv[1], sys.argv[2]
L = [l.strip().split('|') for l in open(led)
     if l.strip() and not l.startswith('#') and l.split('|')[0] not in ('RT','TT','ZT')]
M = {}
for l in open(idx):
    if l.startswith('MX|'):
        _, stg, h, a, hg, ag = l.strip().split('|')
        M[(stg, h, a)] = (int(hg), int(ag))

def stg(tag):
    if tag.startswith('R') and tag != 'RT': return 'REG'
    if tag.startswith('T'): return 'TGRP'
    if tag.startswith('Z'): return 'ZGRP'
    if tag in ('ESF1','ESF2','EF1','EF2','CLP'): return 'MID'
    return tag

fails = []
covered = collections.Counter()
for f in L:
    tag, d, h, hg, ag, a = f[0], f[1], f[2], f[3], f[4], f[5]
    s = stg(tag)
    if s == 'PRO':
        key = ('PRO', h, a)
    elif s in ('REG', 'TGRP', 'ZGRP', 'MID'):
        key = (s, h, a)
    else:
        continue
    cell = M.get(key)
    if cell is None:
        fails.append(f'ledger row w/o matrix cell: {f}')
        continue
    if cell != (int(hg), int(ag)):
        fails.append(f'SCORE DIFF {key}: ledger {hg}-{ag} vs wiki {cell}')
    covered[key] += 1
for key, cell in M.items():
    if covered[key] != 1:
        fails.append(f'matrix cell {key} covered {covered[key]}x')
print(f'{led} vs {idx}: rows={len(L)} cells={len(M)} covered={sum(covered.values())}')
if fails:
    print('FAILURES:')
    [print(' ', x) for x in fails]
    sys.exit(1)
print('DIFF GATE PASS: ledger <-> wiki matrix 1:1 score-identical')
