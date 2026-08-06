#!/usr/bin/env python3
"""Emit the SPA 2025-26 second-index MATRIX (MX) ledger from the archived Wikipedia
2025-26 La Liga article (data/raw/wiki-es-2526-article-raw.txt, FBR invoke section,
action=raw byte-safe, renderer escapes verbatim in archive).

  MX|homePin|awayPin|hg|ag    -> stdout

Cells: '\| match\_XXX\_YYY = S' where S is either a plain 'h-a' score or wrapped
'[[Some derby article|h-a]]' (decorations stripped). Article-matrix codes:
MLL=Mallorca, OVD=Oviedo (upstream ARTICLE-matrix tokens; template prints MAL/OVI
Census gates: 380 scored cells, 190 reciprocal pairs, GF == 1024 (infobox total goals),
0 unscored cells, code set == the 20 expected.
Usage: python3 tools/mx_es_2526.py
"""
import re

CODES = {'ALA': 'Alaves', 'ATH': 'Ath Bilbao', 'ATM': 'Ath Madrid', 'BAR': 'Barcelona',
         'BET': 'Betis', 'CEL': 'Celta', 'ELC': 'Elche', 'ESP': 'Espanol', 'GET': 'Getafe',
         'GIR': 'Girona', 'LEV': 'Levante', 'MLL': 'Mallorca', 'OSA': 'Osasuna',
         'OVD': 'Oviedo', 'RAY': 'Vallecano', 'RMA': 'Real Madrid', 'RSO': 'Sociedad',
         'SEV': 'Sevilla', 'VAL': 'Valencia', 'VIL': 'Villarreal'}

body = open('data/raw/wiki-es-2526-article-raw.txt', encoding='utf-8').read()
toks = list(re.finditer(r'match\\_([A-Z]{3})\\_([A-Z]{3})\s*=', body))
cells = []
for i, m in enumerate(toks):
    end = toks[i + 1].start() if i + 1 < len(toks) else len(body)
    v = body[m.end():end]
    # last token runs to end: cut at the first newline (score sits on the cell line)
    v = v.split('\n')[0]
    v = re.sub(r'[\\\|\s]+$', '', v).strip()
    sm = re.search(r'(\d+)[-\u2013\u2014](\d+)', v)  # hyphen / en-dash / em-dash (mixed upstream)
    if not sm:
        continue
    cells.append((CODES[m.group(1)], CODES[m.group(2)], int(sm.group(1)), int(sm.group(2))))

gf = sum(c[2] + c[3] for c in cells)
pairs = {}
for h, a, hg, ag in cells:
    pairs.setdefault(frozenset((h, a)), 0)
    pairs[frozenset((h, a))] += 1
assert len(cells) == 380, len(cells)
assert all(v == 2 for v in pairs.values()) and len(pairs) == 190, len(pairs)
assert gf == 1024, gf
assert {m.group(1) for m in toks} | {m.group(2) for m in toks} == set(CODES)

print("# SPA 2025-26 SECOND-INDEX MATRIX (MX) - emitted 2026-08-05 by tools/mx_es_2526.py from")
print("# data/raw/wiki-es-2526-article-raw.txt (FBR invoke, action=raw byte-safe; derby")
print("# wikilink decorations stripped). MX|homePin|awayPin|hg|ag ; 380 cells; goals=1024.")
print("# Source label for pack citations: wikimatrix-es-2526")
print()
for h, a, hg, ag in cells:
    print(f"MX|{h}|{a}|{hg}|{ag}")
