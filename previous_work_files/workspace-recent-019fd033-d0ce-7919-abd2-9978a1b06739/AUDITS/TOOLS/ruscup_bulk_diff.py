#!/usr/bin/env python3
# Bulk diff: RSSSF rus2023/rus2024 cup chapters (compact sections) vs approved RUSCUP pack rows.
import re, sys, collections

MON={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
NAME={'khimki':'FC Khimki','krasnodar':'FC Krasnodar','fc krasnodar':'FC Krasnodar','pari nn':'Pari Nizhny Novgorod',
'pari':'Pari Nizhny Novgorod','lokomotiv':'Lokomotiv Moscow','spartak':'Spartak Moscow','ks samara':'Krylia Sovetov Samara',
'krylya sovetov':'Krylia Sovetov Samara','zenit':'Zenit St Petersburg','fakel':'Fakel Voronezh','akhmat':'Akhmat Grozny',
'orenburg':'FC Orenburg','rostov':'FC Rostov','fc rostov':'FC Rostov','dinamo':'Dynamo Moscow','ural':'Ural Yekaterinburg',
'sochi':'PFC Sochi','torpedo':'Torpedo Moscow','cska':'CSKA Moscow','volga':'Volga Ulyanovsk','akron':'Akron Tolyatti',
'zvezda':'Zvezda Sankt-Peterburg','fc ufa':'FC Ufa','rodina':'Rodina Moscow','volgar':'Volgar Astrakhan','ska':'SKA Khabarovsk',
'baltika':'Baltika Kaliningrad','baltika kaliningrad':'Baltika Kaliningrad','rubin':'Rubin Kazan',
'fc orenburg':'FC Orenburg','fc sochi':'PFC Sochi','fc khimki':'FC Khimki','fc pari':'Pari Nizhny Novgorod'}
def canon(s):
    s=re.sub(r'\s*\([^)]*\)','',s)                  # drop (city)
    s=re.sub(r'\s*\[[^\]]*\]','',s)                 # drop [D2], [Agg..], [Pen..] markers
    s=re.sub(r'\s+',' ',s).strip()
    k=s.lower()
    return NAME.get(k, k.title())
def ymd(base, mo, d):
    yr=base if mo>=7 else base+1
    return f"{yr}-{mo:02d}-{d:02d}"

def parse(fn, baseyear):
    L=[l.rstrip() for l in open(fn, encoding='utf-8', errors='replace')]
    out=[]   # (date, home, hs, as, away, tag)
    # ---- locate compact sections (skip the TOC at the top of the file) ----
    chap=[i for i,l in enumerate(L) if re.match(r'(?i)^russian cup \d{4}/\d{2}', l.strip())][0]
    try: rpl=[i for i,l in enumerate(L) if l.strip()=='RPL PATH' and i>chap][0]
    except IndexError: print('no RPL PATH in',fn); sys.exit(1)
    det=[i for i,l in enumerate(L) if l.strip()=='Russian Cup Details' and i>rpl][0]
    sec=L[rpl:det]
    # ---- groups ----
    rnd=None; pending=None; i=0
    while i < len(sec):
        l=sec[i]; s=l.strip()
        if s.startswith('Final Tables'): break
        m=re.match(r'^Round (\d+)', s)
        if m: rnd=int(m.group(1)); i+=1; continue
        m=re.match(r'^GROUP [A-D](?:\s+\[(\w+) (\d+)\])?\s*$', s)
        if m:
            if m.group(1): pending=(MON[m.group(1)], int(m.group(2)))
            i+=1; continue
        m=re.match(r'^\[(\w+) (\d+)\]$', s)
        if m: pending=(MON[m.group(1)], int(m.group(2))); i+=1; continue
        m=re.match(r'^([A-ZА-Я][^[\]]*?)\s{1,}(\d+)-(\d+)\s+(.*?)\s*(\[pen [\d-]+\])?\s*$', l)
        if m and rnd and pending and not s.startswith(('NB','[W]','Point')):
            h=re.sub(r'\s+$','',m.group(1)); a=m.group(4)
            out.append((ymd(baseyear,*pending), canon(h), int(m.group(2)), int(m.group(3)), canon(a), f'group R{rnd}'))
        i+=1
    # ---- knockout ----
    ko=sec[i:]
    d1=d2=None; single=None; stage='?'
    j=0
    while j < len(ko):
        l=ko[j]; s=l.strip()
        for st in ('QUARTERFINALS','SEMIFINALS','FINALS','SUPER FINAL'):
            if s.startswith(st): stage=st
        m=re.match(r'.*\[(\w+) (\d+), (\w+) (\d+)\]$', s)   # two-leg pair, cross-month [Feb 23, Mar 1]
        if not m: m=re.match(r'.*\[(\w+) (\d+), (\d+)\]$', s)  # two-leg pair, same month [Feb 22, 27]
        if m and 'Att' not in s and 'SUPER' not in s:
            try:
                g1,g2,g3,g4=m.group(1),int(m.group(2)),(m.group(3) if m.lastindex==4 else m.group(1)),int(m.group(m.lastindex))
                d1=(MON[g1], g2); d2=(MON[g3], g4); j+=1; continue
            except KeyError: pass
        m=re.match(r'^\[(\w+) (\d+)[,\]]', s)               # single date or begin of pair line handled above
        if m: single=(MON[m.group(1)], int(m.group(2))); j+=1; continue
        m=re.match(r'^SUPER FINAL \[(\w+) (\d+)', s)         # superfinal header with venue
        if m:
            single=(MON[m.group(1)], int(m.group(2))); stage='SUPER FINAL'; j+=1; continue
        m=re.match(r'^.*\[(\w+) (\d+)\]$', s)               # 'Second Phase [Apr 19]'
        if m and 'Att' not in s:
            try: single=(MON[m.group(1)], int(m.group(2))); j+=1; continue
            except KeyError: pass
        t=re.match(r'^(.+?)\s+(\d+)-(\d+)\s+(\d+)-(\d+)\s+(.+?)\s*(\[agg [\d-]+\])?\s*$', l)  # two-leg tie
        if t and d1 and d2:
            h=t.group(1).strip(); a=t.group(6).strip()
            l1h,l1a,l2h,l2a=int(t.group(2)),int(t.group(3)),int(t.group(4)),int(t.group(5))
            out.append((ymd(baseyear,*d1), canon(h), l1h, l1a, canon(a), stage+' leg1'))
            out.append((ymd(baseyear,*d2), canon(a), l2a, l2h, canon(h), stage+' leg2'))  # flip: 2nd score home-perspective
            j+=1; continue
        t=re.match(r'^(.+?)\s+(\d+)-(\d+)\s+(.+?)\s*(\[(pen|agg)[^\]]*\])?\s*$', l)          # single
        if t and single:
            h=t.group(1).strip(); a=t.group(4).strip()
            if not h.startswith(('NB','[','Participants')) and len(h)>2:
                out.append((ymd(baseyear,*single), canon(h), int(t.group(2)), int(t.group(3)), canon(a), stage))
        j+=1
    return out

def packrows(packfile, y1, y2):
    rows=[l.split('|') for l in open(packfile) if l.startswith('MATCH|')]
    def sea(d):
        y,mo=int(d[:4]),int(d[5:7]); return (y if mo>=7 else y-1)
    return {(r[1],r[4],int(r[5]),int(r[6]),r[7]) for r in rows if sea(r[1])==y1}, rows

def run(fn, base, packy, packfile):
    rss=parse(fn, base)
    rset={(d,h,hs,as_,a) for d,h,hs,as_,a,_ in rss}
    pset,_=packrows(packfile, packy, packfile)
    missing_in_pack=rset-pset; extra_in_pack=pset-rset
    print(f'=== {fn} ({packy}-{packy+1}) ===')
    print('RSSSF ties:', len(rss), '| pack rows:', len(pset), '| not in pack:', len(missing_in_pack), '| not in RSSSF:', len(extra_in_pack))
    for t in sorted(missing_in_pack): print('  RSSSF-ONLY', t)
    for t in sorted(extra_in_pack):
        # check swap-order
        sw=(t[0],t[4],t[3],t[2],t[1])
        tag=' (mirror of RSSSF row?)' if sw in rset else ''
        print('  PACK-ONLY ', t, tag)
    # per-tag sanity
    print('  tags:', dict(collections.Counter(t[5] for t in rss)))

run('rsssf-ref/rus2023.txt', 2022, 2022, 'IMPORT-READY-2026-08-03/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt')
run('rsssf-ref/rus2024.txt', 2023, 2023, 'IMPORT-READY-2026-08-03/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt')
