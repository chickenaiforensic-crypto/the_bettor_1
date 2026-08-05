import re, json, glob, os

NAME = {
 'Slovan Liberec':'Liberec','FK Teplice':'Teplice','Teplice':'Teplice','Slavia Prague':'Slavia','Sparta Prague':'Sparta',
 'Viktoria Plzeň':'Plzen','Jablonec':'Jablonec','Hradec Králové':'Hradec','Sigma Olomouc':'Olomouc',
 'Mladá Boleslav':'Ml.Boleslav','Bohemians 1905':'Bohemians','Slovácko':'Slovacko','Baník Ostrava':'Ostrava',
 'Karviná':'Karvina','Pardubice':'Pardubice','Dukla Praha':'Dukla','České Budějovice':'C.Budejovice',
 'Zlín':'Zlin','Zbrojovka Brno':'Zbrojovka','Artis Brno':'Artis Brno',
}
def fix(s):
    try: return s.encode('latin-1').decode('utf-8')
    except Exception: return s

rows=[]
for p in sorted(glob.glob('cze/pages/*.html')):
    ym=os.path.basename(p)[:-5]
    if ym.startswith('live_'): continue
    html=open(p,encoding='utf-8').read()
    m=re.search(r'window\.__INITIAL_DATA__="(.*?)";</script>', html, re.S)
    if not m: continue
    data=json.loads(m.group(1).encode().decode('unicode_escape'))
    key=[k for k in data['data'] if k.startswith('sport-data-scores-fixtures')]
    if not key: continue
    dd=data['data'][key[0]]['data']
    for g in dd['eventGroups']:
        for sg in g['secondaryGroups']:
            sect=sg.get('displayLabel') or ''
            for ev in sg['events']:
                hs,as_=ev['home'].get('score'),ev['away'].get('score')
                h,a=fix(ev['home']['fullName']),fix(ev['away']['fullName'])
                summ=ev.get('accessibleEventSummary','')
                aet='After extra time' in summ
                awarded='awarded' in summ.lower()
                dt=(ev.get('startDateTime') or '')[:10]
                if not dt: continue
                if awarded:
                    # Slavia v Sparta 2026-05-09 awarded 0-3 (standings arithmetic)
                    assert h=='Slavia Prague' and a=='Sparta Prague' and dt=='2026-05-09', (h,a,dt)
                    hs,as_=0,3
                if hs is None or as_ is None:
                    print('SKIP no-score:',dt,h,a,summ[:60]); continue
                hs,as_=int(hs),int(as_)
                if aet:
                    if (h,a,dt)==('Pardubice','Karviná','2026-05-10'): hs,as_=1,2
                    elif (h,a,dt)==('Sigma Olomouc','Bohemians 1905','2026-05-10'): hs,as_=0,2
                    else: print('UNHANDLED AET:',dt,h,a,hs,as_); continue
                note=''
                if sect=='Championship Round': note='g-champ'
                elif sect=='Relegation Round': note='g-rel'
                elif 'Play-off' in sect or 'Play-Off' in sect: note='po-middle'
                elif sect and 'Relegation' in sect: note='po-rel'
                if awarded: note=(note+'-awarded' if note else 'awarded')
                rows.append([dt,'CZE1',NAME[h],NAME[a],hs,as_,note])

# dedupe safety
seen={}
for r in rows:
    k=(r[0],r[2],r[3])
    if k in seen: print('DUP:',k,seen[k],r[4:6])
    seen[k]=r[4:6]
print('league rows:',len(rows))

with open('cze/cze_league_bbc.csv','w') as f:
    f.write('date,comp,home,away,hg,ag,note\n')
    for r in sorted(rows): f.write(','.join(map(str,r))+'\n')
print('wrote cze/cze_league_bbc.csv')
