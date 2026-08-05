#!/usr/bin/env python3
# Wave-2 FINAL: RUSCUP new-surface rows (2024-25 / 2025-26) vs RSSSF rus2025/rus2026 cup chapters.
import re, unicodedata

MON={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
MONL={k.lower():v for k,v in MON.items()}
ALIAS = {
 'lokomotiv':'Lokomotiv Moscow','lokomotiv moskva':'Lokomotiv Moscow','spartak':'Spartak Moscow','spartak moskva':'Spartak Moscow',
 'rubin':'Rubin Kazan','rubin kazan':'Rubin Kazan','rubin kazn':'Rubin Kazan','zenit':'Zenit St Petersburg','zenit sankt peterburg':'Zenit St Petersburg',
 'krasnodar':'FC Krasnodar','fc krasnodar':'FC Krasnodar','cska':'CSKA Moscow','cska moskva':'CSKA Moscow',
 'dinamo moskva':'Dynamo Moscow','dinamo ms':'Dynamo Moscow','dinamo moscow':'Dynamo Moscow',
 'dinamo mahackala':'Dynamo Makhachkala','dinamo mh':'Dynamo Makhachkala','dynamo mahackala':'Dynamo Makhachkala',
 'ahmat':'Akhmat Grozny','ahmat groznyj':'Akhmat Grozny','akhmat':'Akhmat Grozny','ahmat grozny':'Akhmat Grozny',
 'fakel':'Fakel Voronezh','orenburg':'FC Orenburg','fc orenburg':'FC Orenburg','rostov':'FC Rostov','fc rostov':'FC Rostov',
 'pari nn':'Pari Nizhny Novgorod','ks samara':'Krylia Sovetov Samara','krylya sovetov samara':'Krylia Sovetov Samara',
 'krylja sovetov samara':'Krylia Sovetov Samara','krylja s':'Krylia Sovetov Samara','ks':'Krylia Sovetov Samara','himki':'FC Khimki','khimki':'FC Khimki','fc himki':'FC Khimki',
 'akron':'Akron Tolyatti','akron togliatti':'Akron Tolyatti','baltika':'Baltika Kaliningrad','baltika kaliningrad':'Baltika Kaliningrad',
 'sochi':'PFC Sochi','fc soci':'PFC Sochi','pfc soci':'PFC Sochi','soci':'PFC Sochi',
 'ural':'Ural Yekaterinburg','ural jekaterinburg':'Ural Yekaterinburg',
 'sinnik':'Shinnik Yaroslavl','sinnik jaroslavl':'Shinnik Yaroslavl','shinnik':'Shinnik Yaroslavl',
 'tjumen':'Tyumen','fc tjumen':'Tyumen','kamaz':'KAMAZ','torpedo':'Torpedo Moscow','torpedo moskva':'Torpedo Moscow',
 'arsenal':'Arsenal Tula','arsenal tula':'Arsenal Tula',
 'neftehimik':'Neftekhimik Nizhnekamsk','neftehimik niznekamsk':'Neftekhimik Nizhnekamsk',
}
def base_norm(s):
    d = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+',' ',d.lower()).strip()
def canon(raw):
    s = re.sub(r'\[[^\]]*\]','',raw)              # [D2],[ML],[pen..],[agg..]
    withp = base_norm(s)
    if withp in ALIAS: return ALIAS[withp]
    nop = base_norm(re.sub(r'\([^)]*\)','',s))
    return ALIAS.get(nop, nop)
def ymd(base,mo,d):
    y = base if mo>=7 else base+1
    return f"{y:04d}-{mo:02d}-{d:02d}"

DATEPAT = re.compile(r'\[(\w{3}) (\d{1,2})(?:,\s*(?:(\w{3})\s+)?(\d{1,2}))?(?:[\].,])')
TWOLEG  = re.compile(r'^(.+?)\s+(\d+)-(\d+)\s+(\d+)-(\d+)\s+(.+?)\s*(\[(agg|pen)[^\]]*\])?\s*$')
SINGLE  = re.compile(r'^(.+?)\s+(\d+)-(\d+)\s+(.+?)\s*(\[(pen|agg)[^\]]*\])?\s*$')

def parse(fn, base):
    L=open(fn,encoding='utf-8',errors='replace').read().splitlines()
    out=[]; inkap=False; dates=[]
    for l in L:
        if 'name="kubok"' in l: inkap=True
        elif inkap and re.match(r'<h4><a name="(?!kubok)',l): inkap=False
        if not inkap: continue
        s=l.strip()
        # skip scorer/info continuation lines before any other logic
        if s.startswith('[1.') or s.startswith('[2.') or s.startswith('NB') or s.startswith('[Shoot'): continue
        dm=DATEPAT.search(s)
        if dm and dm.group(1).lower() in MONL and 'Att' not in s[:dm.start()+3]:
            d1=(MONL[dm.group(1).lower()],int(dm.group(2)))
            dates=[d1]
            if dm.group(4):
                mo2=MONL[dm.group(3).lower()] if dm.group(3) else d1[0]
                dates.append((mo2,int(dm.group(4))))
            continue
        t=TWOLEG.match(s)
        if t and len(dates)==2:
            hn,an=canon(t.group(1)),canon(t.group(6))
            out.append((ymd(base,*dates[0]),hn,int(t.group(2)),int(t.group(3)),an))
            out.append((ymd(base,*dates[1]),an,int(t.group(5)),int(t.group(4)),hn))
            continue
        t=SINGLE.match(s)
        if t and len(dates)==1:
            h,a=t.group(1),t.group(4)
            nh,na=canon(h),canon(a)
            if nh and na and 'att:' not in (nh+na).lower():
                out.append((ymd(base,*dates[0]),nh,int(t.group(2)),int(t.group(3)),na))
            continue
    return out

for fn,base,sea in [('/home/user/REFERENCE/rsssf-ref/rus2025.txt',2024,('2024-07-01','2025-06-30')),
                    ('/home/user/REFERENCE/rsssf-ref/rus2026.txt',2025,('2025-07-01','2026-06-30'))]:
    rows=parse(fn,base); rset=set(rows)
    pack=[]
    for l in open('RUSCUP-2021-2026.txt'):
        if not l.startswith('MATCH|'): continue
        p=l.rstrip('\n').split('|')
        if sea[0]<=p[1]<=sea[1]: pack.append((p[1],p[4],int(p[5]),int(p[6]),p[7]))
    pset=set(pack)
    sw=lambda t:(t[0],t[4],t[3],t[2],t[1])
    real_p=[t for t in rset-pset if sw(t) not in pset]
    real_r=[t for t in pset-rset if sw(t) not in rset]
    # regions-vs-RPL split of RSSSF-only (regions rounds are intentionally out of pack scope)
    import collections
    print(f'=== {fn} === rsssf {len(rows)} | pack {len(pack)} | RSSSF-only {len(real_p)} | PACK-only {len(real_r)}')
    for t in sorted(real_r): print('  PACK-ONLY',t)
