"""Strict loader. Every rejection is counted and reported. Nothing dropped silently."""
import csv, os, glob, pickle
from datetime import datetime
from collections import Counter

LEAGUE_NAMES={'E0':'England Premier League','E1':'England Championship','E2':'England League One',
 'E3':'England League Two','SC0':'Scotland Premiership','D1':'Germany Bundesliga','D2':'Germany 2.Bundesliga',
 'SP1':'Spain La Liga','SP2':'Spain Segunda','I1':'Italy Serie A','I2':'Italy Serie B','F1':'France Ligue 1',
 'F2':'France Ligue 2','N1':'Netherlands Eredivisie','B1':'Belgium Pro League','P1':'Portugal Liga',
 'T1':'Turkey Super Lig','G1':'Greece Super League'}

def parse_date(s):
    s=(s or '').strip()
    if not s: return None
    for f in ("%d/%m/%Y","%d/%m/%y"):
        try:
            d=datetime.strptime(s,f)
            if d.year<1990 or d.year>2030: return None
            return d
        except ValueError: pass
    return None

rows=[]; rej=Counter()
for path in sorted(glob.glob("*.csv")):
    base=os.path.basename(path)[:-4]
    lg,seas=base.split("_")[0],base.split("_")[1]
    try: f=open(path,encoding='utf-8-sig',errors='replace')
    except Exception: rej['unopenable']+=1; continue
    for r in csv.DictReader(f):
        if r.get('Div') is None: rej['no_div_col']+=1; continue
        d=parse_date(r.get('Date'))
        if d is None: rej['bad_date']+=1; continue
        h=(r.get('HomeTeam') or '').strip(); a=(r.get('AwayTeam') or '').strip()
        if not h or not a: rej['missing_team']+=1; continue
        if h==a: rej['same_team']+=1; continue
        try: hg=int(float(r['FTHG'])); ag=int(float(r['FTAG']))
        except (TypeError,ValueError,KeyError): rej['no_score']+=1; continue
        if not (0<=hg<=20 and 0<=ag<=20): rej['impossible_score']+=1; continue
        res=r.get('FTR','').strip()
        derived='H' if hg>ag else ('D' if hg==ag else 'A')
        if res and res!=derived: rej['ftr_mismatch']+=1; continue
        def fl(*keys):
            for k in keys:
                v=r.get(k)
                if v not in (None,'','NA'):
                    try:
                        x=float(v)
                        if 1.0<x<1000: return x
                    except ValueError: pass
            return None
        rows.append(dict(lg=lg,season=seas,date=d,home=h,away=a,hg=hg,ag=ag,res=derived,
            oh=fl('PSCH','PSH','B365CH','B365H','AvgCH','BbAvH','AvgH'),
            od=fl('PSCD','PSD','B365CD','B365D','AvgCD','BbAvD','AvgD'),
            oa=fl('PSCA','PSA','B365CA','B365A','AvgCA','BbAvA','AvgA')))
    f.close()

# dedupe: same league+season+date+home+away
seen=set(); ded=[]
for r in rows:
    k=(r['lg'],r['season'],r['date'],r['home'],r['away'])
    if k in seen: rej['duplicate']+=1; continue
    seen.add(k); ded.append(r)
rows=ded
rows.sort(key=lambda x:(x['lg'],x['season'],x['date']))

print(f"LOADED {len(rows):,} matches")
print(f"Rejections: {dict(rej) if rej else 'none'}")
print(f"Leagues {len(set(r['lg'] for r in rows))}  Seasons {len(set(r['season'] for r in rows))}")
print(f"Date range {min(r['date'] for r in rows).date()} -> {max(r['date'] for r in rows).date()}")
print(f"With closing odds: {sum(1 for r in rows if r['oh'] and r['od'] and r['oa']):,}")
h=sum(1 for r in rows if r['res']=='H'); d=sum(1 for r in rows if r['res']=='D')
print(f"Overall H/D/A: {h/len(rows):.1%} / {d/len(rows):.1%} / {(len(rows)-h-d)/len(rows):.1%}")
pickle.dump(rows,open("all_matches.pkl","wb"))

# sanity: season-team-match counts
print("\nSanity — matches per league-season (expect ~380 E0, ~306 D1, ~552 E1):")
from collections import defaultdict
cnt=defaultdict(int)
for r in rows: cnt[(r['lg'],r['season'])]+=1
for lg in ['E0','D1','E1','SP1']:
    v=[cnt[(l,s)] for (l,s) in cnt if l==lg]
    print(f"  {lg}: min {min(v)} max {max(v)} median {sorted(v)[len(v)//2]}")
