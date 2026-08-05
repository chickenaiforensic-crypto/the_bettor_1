#!/usr/bin/env python3
# MOL Cup R2/R3: en.wiki season pages (second index) vs approved MOLCUP pack.
# aet/pso ties: pack row must be a 90-min DRAW; wiki final score must equal the pack's advancement NOTE aet score.
import json, unicodedata, re, urllib.request

PAGES={('2021','22'):'2021%E2%80%9322_Czech_Cup',('2022','23'):'2022%E2%80%9323_Czech_Cup',('2023','24'):'2023%E2%80%9324_Czech_Cup'}
MON={m:i+1 for i,m in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'])}
def ascii_(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
def canon_wiki(s):
    s=ascii_(s)
    s=re.sub(r'\[\[|\]\]','',s); s=re.sub(r"'''",'',s).strip()
    return s
ALIASES={'Sellier & Bellot Vlasim':'Vlasim','Viagem Pribram':'Pribram','FC Viagem Pribram':'Pribram','Lisen':'Lisen','SK Lisen':'Lisen',
'Hanacka Slavia Kromeriz':'Kromeriz','Trinity Zlin':'Zlin','FC Trinity Zlin':'Zlin','Silon Taborsko':'Taborsko','FC Silon Taborsko':'Taborsko',
'Vyskov':'Vyskov','MFK Vyskov':'Vyskov','SFC Opava':'Opava','Sigma Olomouc':'Sigma Olomouc','FK Dukla Prague':'Dukla Prague','Dukla Prague':'Dukla Prague',
'Slovan Liberec':'Slovan Liberec','FC Slovan Liberec':'Slovan Liberec','FK Jablonec':'Jablonec','Zbrojovka Brno':'Zbrojovka Brno',
'FC Zbrojovka Brno':'Zbrojovka Brno','Hradec Kralove':'Hradec Kralove','FC Hradec Kralove':'Hradec Kralove','MFK Karvina':'Karvina',
'Bohemians 1905':'Bohemians 1905','Bohemians Praha 1905':'Bohemians 1905','Banik Ostrava':'Banik Ostrava','FC Banik Ostrava':'Banik Ostrava',
'FK Teplice':'Teplice','AC Sparta Prague':'Sparta Prague','SK Slavia Prague':'Slavia Prague','FC Viktoria Plzen':'Viktoria Plzen',
'FK Mlada Boleslav':'Mlada Boleslav','SK Dynamo Ceske Budejovice':'Ceske Budejovice','1. FC Slovacko':'Slovacko','FK Pardubice':'Pardubice',
'FK Viktoria Zizkov':'Zizkov','Slovan Velvary':'Velvary','1. SK Prostejov':'Prostejov','FK Varnsdorf':'Varnsdorf','SK Unicov':'Unicov',
'MFK Chrudim':'Chrudim','SK Zapy':'Zapy','TJ Start Brno':'Start Brno','FC Slovan Rosice':'Rosice','FK Caslav':'Caslav','FC Hlucin':'Hlucin',
'FC Vysočina Jihlava':'Jihlava','FC Vysocina Jihlava':'Jihlava','FK Motorlet Prague':'Motorlet Praha','FK Prepere':'Prepere',
'FK Chlumec nad Cidlinou':'Chlumec nad Cidlinou','TJ Jiskra Domazlice':'Domazlice','TJ Spartak Sobeslav':'Sobeslav',
'SK Kladno':'Kladno','FC Rokycany':'Rokycany','FK Banik Most-Sous':'Banik Most-Sous','FC Viktoria Marianske Lazne':'Marianske Lazne',
'SK Benesov':'Benesov','Sokol Hostoun':'Hostoun','FK Banik Sokolov':'Sokolov','FK Zbuzany':'Zbuzany','FK Admira Prague':'Admira Praha',
'TJ Tatran Sedlcany':'Sedlcany','FC TVD Slavicin':'Slavicin','FK Blansko':'Blansko','FK Olympie Brezova':'Brezova','TJ Velke Hamry':'Velke Hamry',
'SK Slavoj Vysehrad':'Vysehrad','FC Slavoj Vysehrad':'Vysehrad','SK Usti nad Orlici':'Usti nad Orlici','FK Kolín':'Kolin','SK Kolin':'Kolin',
'FC Slavia Karlovy Vary':'Slavia KV','FK Loko Vltavin':'Loko Praha','FK Loko Praha':'Loko Praha'}
def packname(s):
    s=canon_wiki(s)
    if s in ALIASES: return ALIASES[s]
    # strip common prefixes, try again
    t=re.sub(r'^(FC|FK|SK|TJ|AC|SC|MFK|SFC|1\.)\s+','',s)
    if t in ALIASES: return ALIASES[t]
    if s in ALIASES.values() or t in ALIASES.values(): return t if t in ALIASES.values() else s
    return t
def fetch(page):
    url='https://en.wikipedia.org/w/api.php?action=parse&page='+page+'&prop=wikitext&format=json&formatversion=2'
    req=urllib.request.Request(url, headers={'User-Agent':'ArenaAudit/1.0'})
    return json.load(urllib.request.urlopen(req, timeout=30))['parse']['wikitext']
def parse_round(wt, rname, nxt, y1):
    a=wt.index(rname); b=wt.index(nxt); sec=wt[a:b]
    cur=None; out=[]
    for line in sec.split('\n'):
        m=re.search(r'align=center\|\'\'\'(\d+) (\w+) (\d{4})\'\'\'', line)
        if m: cur=f"{m.group(3)}-{MON[m.group(2)]:02d}-{int(m.group(1)):02d}"; continue
        m=re.match(r'\{\{OneLegResult\|(.+?)\s*\|\|\s*(\d+)–(\d+)\s*(\{\{aet\}\}|\{\{pso\|([\d–]+)\}\})?\s*\|\s*(.+?)\}\}', line.strip())
        if m:
            h=packname(re.sub(r'\[\[|\]\]','',m.group(1)))
            a2=packname(re.sub(r'\[\[|\]\]','',m.group(6)).replace("'''",''))
            aet=bool(m.group(4))
            out.append((cur,h,int(m.group(2)),int(m.group(3)),a2,aet))
    return out

pack=[l.split('|') for l in open('IMPORT-READY-2026-08-03/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt') if l.startswith('MATCH|')]
packrows={(r[1],r[4],int(r[5]),int(r[6]),r[7]) for r in pack}
packdraws={(r[1],r[4],r[7]) for r in pack if r[5]==r[6]}
notes=[l for l in open('IMPORT-READY-2026-08-03/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt') if l.startswith('NOTE|info|advancement|')]
def note_aet_score(date,h,a):
    for n in notes:
        if date in n and h in n and a in n:
            m=re.search(r'\((aet|pens) (\d+)-(\d+)', n)
            if m: return (int(m.group(2)),int(m.group(3)))
    return None
TOPFLIGHT={'Sparta Prague','Slavia Prague','Viktoria Plzen','Bohemians 1905','Slovacko','Sigma Olomouc','Hradec Kralove','Jablonec','Mlada Boleslav','Teplice','Banik Ostrava','Zlin','Ceske Budejovice','Slovan Liberec','Pardubice','Karvina','Zbrojovka Brno'}
unmapped=set(); tot={'EXACT':0,'AET-OK':0,'EXCL-OK':0,'BAD':0}
for (y1,y2),page in PAGES.items():
    try: wt=fetch(page)
    except Exception as e: print('FETCH FAIL',y1,e); continue
    for rname,nxt,rlabel in [('== Second round ==','== Third round ==','R2'),('== Third round ==','== Fourth round ==','R3')]:
        if rname not in wt: print('no section',rname,'in',y1); continue
        ties=parse_round(wt,rname,nxt,y1)
        print(f'=== {y1}-{y2} {rlabel}: wiki ties={len(ties)} ===')
        for d,h,hs,as_,a,aet in ties:
            if h==a or not d: continue
            if h not in TOPFLIGHT and a not in TOPFLIGHT:
                if (d,h,hs,as_,a) in packrows or any(dd==d and hh==h and aa==a for dd,hh,aa in packdraws):
                    print('  EXCLUDED-FAIL', d,h,hs,'-',as_,a); tot['BAD']+=1
                else: tot['EXCL-OK']+=1
                continue
            if (d,h,hs,as_,a) in packrows and not aet:
                tot['EXACT']+=1; print('  EXACT  ', d,h,hs,'-',as_,a)
            elif aet:
                if (d,h,a) in packdraws:
                    ns=note_aet_score(d,h,a)
                    if ns==(hs,as_): tot['AET-OK']+=1; print('  AET-OK ', d,h,hs,'-',as_,a,'(pack 90-min draw + NOTE', ns,')')
                    else: tot['BAD']+=1; print('  AET-NOTE-MISMATCH', d,h,hs,'-',as_,a,'pack NOTE:',ns)
                else:
                    # maybe pack has it as exact draw with same score (pso after 0-0 etc)
                    cand=[r for r in packrows if r[0]==d and {r[1],r[4]}=={h,a}]
                    tot['BAD']+=1; print('  AET-BUT-NO-DRAW', d,h,hs,'-',as_,a,'cand:',cand)
            else:
                cand=[r for r in packrows if r[0]==d and {r[1],r[4]}=={h,a}]
                if cand: tot['BAD']+=1; print('  SCORE-DIFF', d,h,hs,'-',as_,a,'pack:',cand)
                else:
                    print('  MISSING  ', d,h,hs,'-',as_,a); tot['BAD']+=1
print('\nTOTALS:', tot)
