"""
INGEST — extend league coverage for European qualifier fixtures.
Sources: football-data.co.uk (CSV) + openfootball/europe (txt). Results only.
"""
import csv, re, glob, os, pickle
from collections import defaultdict

edges = []          # (date, comp, country, home, country, away, hg, ag)
stats = defaultdict(int)
rej = defaultdict(int)

# ---------- football-data CSV leagues ----------
FD = {'AUT':'AUT','SWZ':'SUI','SWE':'SWE','NOR':'NOR','FIN':'FIN','POL':'POL',
      'ROU':'ROU','RUS':'RUS','IRL':'IRL'}
for code, ctry in FD.items():
    p = f"/tmp/newlg/{code}.csv"
    if not os.path.exists(p):
        continue
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        if not r.get('HG') or not r.get('AG'):
            rej[code + ':noscore'] += 1
            continue
        d = (r.get('Date') or '').strip()
        m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', d)
        if not m:
            rej[code + ':baddate'] += 1
            continue
        h, a = r['Home'].strip(), r['Away'].strip()
        if not h or not a or h == a:
            rej[code + ':team'] += 1
            continue
        try:
            hg, ag = int(float(r['HG'])), int(float(r['AG']))
        except ValueError:
            rej[code + ':score'] += 1
            continue
        if not (0 <= hg <= 20 and 0 <= ag <= 20):
            rej[code + ':range'] += 1
            continue
        edges.append((f"{m.group(3)}-{m.group(2)}-{m.group(1)}", 'DOM:' + code,
                      ctry, h, ctry, a, hg, ag))
        stats[code] += 1

# ---------- openfootball txt leagues ----------
OF = {'croatia':'CRO','czech-republic':'CZE','ukraine':'UKR','serbia':'SRB',
      'slovenia':'SVN','hungary':'HUN','bulgaria':'BUL','cyprus':'CYP',
      'iceland':'ISL','estonia':'EST','latvia':'LVA','azerbaijan':'AZE',
      'armenia':'ARM','moldova':'MDA','belarus':'BLR','faroe-islands':'FRO',
      'wales':'WAL','bosnia-herzegovina':'BIH','slovakia':'SVK','albania':'ALB',
      'north-macedonia':'MKD','montenegro':'MNE','georgia':'GEO','lithuania':'LTU',
      'kosovo':'KVX','luxembourg':'LUX','malta':'MLT','northern-ireland':'NIR'}

# openfootball match line:  "    21:00  Dinamo Zagreb   v NK Istra 1961   5-0 (3-0)"
mline = re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+v\s+(.+?)\s+(\d{1,2})-(\d{1,2})(?:\s|$)')
season_hint = re.compile(r'(\d{4})')

for folder, ctry in OF.items():
    base = f"/tmp/euro/europe-master/{folder}"
    if not os.path.isdir(base):
        continue
    for f in sorted(glob.glob(base + "/*.txt")):
        fn = os.path.basename(f)
        if 'cup' in fn.lower():
            continue                      # league matches only
        yr = season_hint.search(fn)
        year = yr.group(1) if yr else '2024'
        n = 0
        for ln in open(f, encoding='utf-8', errors='replace'):
            ln = ln.rstrip('\r\n')
            st = ln.strip()
            if not st or st[0] in '#=\u25aa':
                continue
            m = mline.match(ln)
            if not m:
                continue
            h = m.group(1).strip()
            a = m.group(2).strip()
            hg, ag = int(m.group(3)), int(m.group(4))
            if not h or not a or h == a or len(h) < 2 or len(a) < 2:
                rej[ctry + ':team'] += 1
                continue
            if not (0 <= hg <= 20 and 0 <= ag <= 20):
                rej[ctry + ':range'] += 1
                continue
            edges.append((f"{year}-06-30", 'DOM:' + ctry, ctry, h, ctry, a, hg, ag))
            n += 1
        stats[ctry] += n

print("=" * 70)
print("INGEST SUMMARY")
print("=" * 70)
for k in sorted(stats, key=lambda x: -stats[x]):
    print(f"  {k:6s} {stats[k]:6,} matches")
print(f"\n  TOTAL NEW EDGES: {len(edges):,}")
if rej:
    print(f"  rejected: {dict(rej)}")

pickle.dump(edges, open("/home/user/chain/extra_edges.pkl", "wb"))
clubs = set()
for e in edges:
    clubs.add((e[2], e[3]))
    clubs.add((e[4], e[5]))
print(f"  clubs: {len(clubs):,}  countries: {len(set(c for c, _ in clubs))}")
