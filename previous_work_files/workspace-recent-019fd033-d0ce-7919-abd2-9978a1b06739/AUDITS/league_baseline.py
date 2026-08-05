#!/usr/bin/env python3
"""league_baseline.py - auditor baseline builder for La Liga / Serie A / Bundesliga / Ligue 1
from local RSSSF pages (span|ital|duit|fran<Y>.txt), peer of epl_baseline.py.

Gate per season: exact match count (La Liga/Serie A 380; Bundesliga 306; Ligue 1 380
for 2021-23 and 306 from 2023-24), 0 date+pair dupes, printed Final Table fully
reproduced from round listings (W-D-L-GF-GA per club; point deductions reported
separately). Builds seasons 2021-22 .. 2024-25 into audit-baseline/.

Quirks encoded (learned 2026-08-03):
- encodings per file differ (UTF-16LE / UTF-8 / latin-1): smart-decode done separately;
  this script reads the normalized UTF-8 .txt files.
- team names may START with digits ('1. FC Köln') -> table-row name group starts [\\w].
- relegation separator dashes inside tables -> never line-break the table scan; a repeat
  team name marks the start of the second (duplicate) table print -> stop there.
- blank line directly under 'Final Table:' header -> skip-before-first-row logic.
- match listings use the column-aligned short tokens ('Paris-SG', 'Mönchengladbach', ...)
  mapped via frozen audit-baseline/majors-aliases.json (built with prefix/substr auto-map
  + hand overrides Madrid->Real Madrid CF, Barcelona->FC Barcelona, Paris-SG/Rennes).
- 'Wolverhampton'-style column overflow tolerated via single-space regex.
"""
import re, json, sys, os, unicodedata

MONTHS = {m: i+1 for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug',
                                        'Sep','Oct','Nov','Dec'])}
LEAGUES = {  # base: (anchor, out_name, {yearfile: season_start_year}, expected_matches)
    'span': ('laliga', 'laliga', {2022:2021, 2023:2022, 2024:2023, 2025:2024}, {2022:380,2023:380,2024:380,2025:380}),
    'ital': ('seriea', 'seriea', {2022:2021, 2023:2022, 2024:2023, 2025:2024}, {2022:380,2023:380,2024:380,2025:380}),
    'duit': ('1bl', 'bundesliga', {2022:2021, 2023:2022, 2024:2023, 2025:2024}, {2022:306,2023:306,2024:306,2025:306}),
    'fran': ('l1', 'ligue1', {2022:2021, 2023:2022, 2024:2023, 2025:2024}, {2022:380,2023:380,2024:306,2025:306}),
}
ALIASES = json.load(open('audit-baseline/majors-aliases.json'))

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

def section(base, fn):
    lines = open(fn, encoding='utf-8').read().split('\n')
    a = b = None
    for i, l in enumerate(lines):
        if f'name="{LEAGUES[base][0]}"' in l: a = i
        elif a is not None and '<a name=' in l: b = i; break
    return [l.rstrip('\r') for l in lines[a:b]]

def build(base, yfile, y0):
    alias = ALIASES[base]
    sec = section(base, f'rsssf-ref/{base}{yfile}.txt')
    matches, cur, rnd, anomalies = [], None, None, []
    for l in sec:
        m = re.match(r'^Round (\d+)', l)
        if m: rnd = int(m.group(1)); continue
        m = re.match(r'^\[([A-Za-zÀ-ž][a-z]{2}) (\d{1,2})\]$', l.strip())
        if m and m.group(1)[:3].title() in MONTHS:
            mo = MONTHS[m.group(1)[:3].title()]; yr = y0 if mo >= 7 else y0+1
            cur = f"{yr}-{mo:02d}-{int(m.group(2)):02d}"; continue
        if re.search(r'\sabd\s', l) and cur:
            anomalies.append(('ABANDONED', rnd, cur, l.strip()[:80])); continue
        m = re.match(r"^([A-Za-zÀ-ž][\w .&'/-]*?) awd ([A-Za-zÀ-ž][\w .&'/-]*?)\s+\[awarded (\d+)-(\d+)[;\]]", l)
        if m and cur and rnd:
            h, a, hg, ag = m.group(1).strip(), m.group(2).strip(), int(m.group(3)), int(m.group(4))
            if h not in alias or a not in alias:
                anomalies.append(('UNKNOWN', h, a, rnd, cur)); continue
            anomalies.append(('AWARDED', rnd, cur, f'{h} {hg}-{ag} {a}', re.search(r'\[([^\]]*)', l).group(1)[:90]))
            matches.append(dict(round=rnd, date=cur, home=alias[h], hg=hg, ag=ag, away=alias[a])); continue
        m = re.match(r"^([A-Za-zÀ-ž][\w .&'/-]*?)\s+(\d+)-(\d+)\s+(\S.*)$", l)
        if m and cur and rnd:
            h, hg, ag, rest = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4)
            a = None; tail = ''
            for tok in sorted(alias, key=len, reverse=True):
                if rest == tok or (rest.startswith(tok) and (len(rest) == len(tok) or rest[len(tok)] in ' \t[')):
                    a = tok; tail = rest[len(tok):].strip(); break
            if h not in alias or a is None:
                anomalies.append(('UNKNOWN', h, rest.split('  ')[0].strip()[:30], rnd, cur)); continue
            if tail and re.search(r'abandon|award|cardiac|crowd|walked', tail, re.I):
                anomalies.append(('COUNTED-WITH-NOTE', rnd, cur, f'{h} {hg}-{ag} {a}', tail[:90]))
            elif tail and not tail.startswith('['):
                anomalies.append(('TAIL-REVIEW', rnd, cur, f'{h} {hg}-{ag} {a}', tail[:60]))
            matches.append(dict(round=rnd, date=cur, home=alias[h], hg=hg, ag=ag, away=alias[a]))
    tbl = {}
    for l in sec:
        m = re.match(r"^\s*(\d+)\.\s*([\wÀ-ž][\w .&'/()-]*?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*-\s*(\d+)\s+(-?\d+)", l)
        if m:
            nm = m.group(2).strip()
            if nm in tbl: break
            tbl[nm] = dict(p=int(m.group(3)), w=int(m.group(4)), d=int(m.group(5)), l=int(m.group(6)),
                           gf=int(m.group(7)), ga=int(m.group(8)), pts=int(m.group(9)))
    der = {}
    for mt in matches:
        for t, gf, ga in ((mt['home'], mt['hg'], mt['ag']), (mt['away'], mt['ag'], mt['hg'])):
            s = der.setdefault(t, dict(p=0, w=0, d=0, l=0, gf=0, ga=0))
            s['p'] += 1; s['gf'] += gf; s['ga'] += ga
            s['w' if gf > ga else 'd' if gf == ga else 'l'] += 1
    exact = sum(1 for t, r in tbl.items() if t in der and
                tuple(der[t][k] for k in ('p','w','d','l','gf','ga')) == tuple(r[k] for k in ('p','w','d','l','gf','ga')))
    ded = {t: tbl[t]['pts'] - (der[t]['w']*3 + der[t]['d']) for t in tbl
           if t in der and tbl[t]['pts'] != der[t]['w']*3 + der[t]['d']}
    seen, dups = set(), 0
    for mt in matches:
        k = (mt['date'], mt['home'], mt['away'])
        if k in seen: dups += 1
        seen.add(k)
    rounds_ok = {mt['round'] for mt in matches}
    exp = LEAGUES[base][3][yfile]
    status = 'PASS' if len(matches) == exp and exact == len(tbl) and dups == 0 else 'CHECK'
    return status, matches, tbl, der, exact, ded, anomalies, dups, exp, len(rounds_ok)

if __name__ == '__main__':
    os.makedirs('audit-baseline', exist_ok=True)
    allok = True
    for base, (_, out_name, years, _) in LEAGUES.items():
        for yfile, y0 in years.items():
            status, matches, tbl, der, exact, ded, anomalies, dups, exp, nrounds = build(base, yfile, y0)
            if status != 'PASS': allok = False
            season = f'{y0}-{str(y0+1)[2:]}'
            print(f"{out_name} {season}: matches={len(matches)}/{exp} table-exact={exact}/{len(tbl)} "
                  f"dups={dups} rounds={nrounds} pts-adj={ded} anomalies={len(anomalies)} -> {status}")
            for an in anomalies[:5]: print('   ', an)
            if status == 'PASS':
                out = dict(season=season, league=out_name, source=f'rsssf-{base}{yfile}',
                           note='printed table reproduced from round listings; deductions separate',
                           deductions=ded, anomalies=anomalies, matches=matches)
                json.dump(out, open(f'audit-baseline/{out_name}-{season}.json', 'w'), indent=1)
    print('ALL LOCKED' if allok else 'NOT ALL LOCKED')
    sys.exit(0 if allok else 1)
