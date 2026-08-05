import re, json, glob, os

MONTHS = sorted(os.path.basename(p)[:-5] for p in glob.glob('pages/*.html'))
rows = []
for ym in MONTHS:
    html = open(f'pages/{ym}.html', encoding='utf-8').read()
    m = re.search(r'window\.__INITIAL_DATA__="(.*?)";</script>', html, re.S)
    if not m:
        print(ym, 'NO DATA'); continue
    data = json.loads(m.group(1).encode().decode('unicode_escape'))
    key = [k for k in data['data'] if k.startswith('sport-data-scores-fixtures')]
    if not key:
        print(ym, 'no scores key'); continue
    dd = data['data'][key[0]]['data']
    n0 = len(rows)
    for g in dd['eventGroups']:
        for sg in g['secondaryGroups']:
            sect = sg.get('displayLabel') or ''
            for ev in sg['events']:
                h, a = ev['home'], ev['away']
                hs, as_ = h.get('score'), a.get('score')
                status = ev.get('status','')
                dt = (ev.get('startDateTime') or '')[:10]
                summary = ev.get('accessibleEventSummary','')
                aet = 'After extra time' in summary
                awarded = 'awarded' in summary.lower()
                rows.append(dict(date=dt, month=ym, section=sect, home=h['fullName'], away=a['fullName'],
                                 hs=hs, as_=as_, status=status, aet=aet, awarded=awarded,
                                 ht=(h.get('runningScores') or {}).get('halftime','')))
    print(ym, len(rows)-n0, 'events')

rows.sort(key=lambda r: (r['date'] or '', r['home']))
with open('cze_bbc_raw.csv','w') as f:
    f.write('date,section,home,away,hs,as,status,aet,awarded\n')
    for r in rows:
        f.write(','.join(str(r[k]) for k in ('date','section','home','away','hs','as_','status','aet','awarded')).replace('\n',' ')+'\n')
print('TOTAL', len(rows))
# distinct team names
names = sorted({r['home'] for r in rows} | {r['away'] for r in rows})
print(len(names), 'teams:', names)
