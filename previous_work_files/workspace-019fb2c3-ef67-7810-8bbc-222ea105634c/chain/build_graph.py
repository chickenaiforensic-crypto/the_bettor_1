"""
CHAIN SYSTEM — FOUNDATION STEP 1
Build the club-opponent graph from RESULTS ONLY.
  layer 1: domestic leagues (18 countries + Poland, Denmark)
  layer 2: European competition (CL/EL/Conference + qualifiers) = the bridges
No odds. No market. No commentary.
"""
import pickle, re, glob, csv, os
from collections import defaultdict

CTRY = {'E0':'ENG','E1':'ENG','E2':'ENG','E3':'ENG','SC0':'SCO','D1':'GER','D2':'GER',
        'SP1':'ESP','SP2':'ESP','I1':'ITA','I2':'ITA','F1':'FRA','F2':'FRA','N1':'NED',
        'B1':'BEL','P1':'POR','T1':'TUR','G1':'GRE'}

edges = []   # (date, comp, country_home, home, country_away, away, hg, ag)

rows = pickle.load(open("/home/user/data/all_matches.pkl", "rb"))
for m in rows:
    c = CTRY[m['lg']]
    edges.append((m['date'].strftime('%Y-%m-%d'), 'DOM:' + m['lg'],
                  c, m['home'], c, m['away'], m['hg'], m['ag']))
print(f"domestic edges: {len(edges):,}")

key = lambda d: (d[6:10], d[3:5], d[:2])
for code, ctry, path in [('POL', 'POL', '/tmp/POL.csv'), ('DNK', 'DEN', '/tmp/DNK.csv')]:
    if not os.path.exists(path):
        print(f"  {code}: MISSING {path}")
        continue
    n = 0
    for r in csv.DictReader(open(path, encoding='utf-8-sig')):
        if not r.get('HG'):
            continue
        y, mo, dd = key(r['Date'])
        edges.append((f"{y}-{mo}-{dd}", 'DOM:' + code, ctry, r['Home'].strip(),
                      ctry, r['Away'].strip(), int(r['HG']), int(r['AG'])))
        n += 1
    print(f"{code}: {n:,} edges")

line_re = re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)')
ne = 0
for f in sorted(glob.glob("/tmp/ucl/champions-league-master/*/*.txt")):
    season = f.split('/')[-2]
    comp = os.path.basename(f).replace('.txt', '').upper()
    yr = season[:4]
    for ln in open(f, encoding='utf-8', errors='replace'):
        m = line_re.match(ln.strip('\r\n'))
        if m:
            edges.append((f"{yr}-06-30", 'EUR:' + comp, m.group(2), m.group(1).strip(),
                          m.group(4), m.group(3).strip(), int(m.group(5)), int(m.group(6))))
            ne += 1
print(f"european edges: {ne:,}")
print(f"TOTAL: {len(edges):,}")

pickle.dump(edges, open("/home/user/chain/edges.pkl", "wb"))
clubs = set()
for e in edges:
    clubs.add((e[2], e[3]))
    clubs.add((e[4], e[5]))
print(f"clubs: {len(clubs):,}  countries: {len(set(c for c, _ in clubs))}")
