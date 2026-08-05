#!/usr/bin/env python3
# CZ1 Titul + Zachranu bulk diff: RSSSF tsje2022/23/24 playoff-group listings vs approved CZ1 pack (841-row v3).
import re
MON={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
MAP={'Plzeň':'Viktoria Plzen','Slovácko':'Slovacko','Olomouc':'Sigma Olomouc','Sparta':'Sparta Prague','Slavia':'Slavia Prague',
'Bohemians':'Bohemians 1905','Liberec':'Slovan Liberec','Hradec Králové':'Hradec Kralove','Mladá Boleslav':'Mlada Boleslav',
'České Budějovice':'Ceske Budejovice','Jablonec':'Jablonec','Baník Ostrava':'Banik Ostrava','Teplice':'Teplice',
'Zbrojovka Brno':'Zbrojovka Brno','Pardubice':'Pardubice','Zlín':'Zlin','Karviná':'Karvina','Ostrava':'Banik Ostrava',
'Brno':'Zbrojovka Brno','Trinity Zlín':'Zlin','Fastav Zlín':'Zlin','Budějovice':'Ceske Budejovice','Hradec':'Hradec Kralove'}
def parse(fn, baseyear):
    L=[l.rstrip() for l in open(fn, encoding='utf-8', errors='replace')]
    ps=[i for i,l in enumerate(L) if l.strip()=='Playoff Stage'][0]
    out=[]
    for grp in ('Skupina o Titul','Skupina o Záchranu'):
        # group match listing occurs AFTER the playoff-stage TOC; find second occurrence
        idx=[i for i,l in enumerate(L) if l.strip()==grp and i>ps]
        # the listing block is the occurrence followed soon by 'Round 31'
        gi=None
        for k in idx:
            nxt=None
            for j in range(k+1, min(k+6, len(L))):
                t=L[j].strip()
                if t and t!=' | ': nxt=t; break
            if nxt and (nxt.startswith('Final Table') or nxt.startswith('Round 31')):
                gi=k; break
        if gi is None: print('  !! no listing for',grp,'in',fn); continue
        cur=None; rnd=None; i=gi+1
        while i < len(L) and not L[i].strip().startswith('Round 31'): i+=1   # skip closing Final Table
        while i < len(L):
            s=L[i].strip()
            if s.startswith('Final Table'): break          # second occurrence = listing end
            if s in ('Skupina o Evropu','Skupina o Titul','Skupina o Záchranu'): break
            m=re.match(r'^Round (\d+)(?:\s+\[(\w+) (\d+)\])?$', s)
            if m:
                rnd=int(m.group(1))
                if m.group(2): cur=(MON[m.group(2)], int(m.group(3)))
                i+=1; continue
            m=re.match(r'^\[(\w+) (\d+)\]$', s)
            if m: cur=(MON[m.group(1)], int(m.group(2))); i+=1; continue
            m=re.match(r'^(.+?)\s+(\d+)-(\d+)\s+(.+?)\s*$', L[i])
            if m and cur and rnd and not s.startswith(('NB','|','Round')):
                h=MAP.get(m.group(1).strip(), m.group(1).strip()); a=MAP.get(m.group(4).strip(), m.group(4).strip())
                yr=baseyear+1
                out.append((f"{yr}-{cur[0]:02d}-{cur[1]:02d}", h, int(m.group(2)), int(m.group(3)), a, grp, rnd))
            i+=1
        pass
    return out

pack=[l.split('|') for l in open('IMPORT-READY-2026-08-03/CZ1-2021-2026_BP-TEAM-PACK_v2.txt') if l.startswith('MATCH|')]
def seatag(d):
    y,mo=int(d[:4]),int(d[5:7]); return y if mo>=7 else y-1
tot_bad=0
for fn, base, label in [('rsssf-ref/tsje2022.txt',2021,'2021-22'),('rsssf-ref/tsje2023.txt',2022,'2022-23'),('rsssf-ref/tsje2024.txt',2023,'2023-24')]:
    rss=parse(fn, base)
    pset={(r[1],r[4],int(r[5]),int(r[6]),r[7]): r[8] for r in pack if seatag(r[1])==base and (r[8].startswith('Titul') or r[8].startswith('Zachranu'))}
    rset={(d,h,hs,as_,a) for d,h,hs,as_,a,_,_ in rss}
    miss=rset-set(pset); extra=set(pset)-rset
    print(f'=== {label}: RSSSF {len(rss)} ties (Titul {sum(1 for t in rss if t[5].endswith("Titul"))} / Zachranu {sum(1 for t in rss if t[5].endswith("Záchranu"))}) vs pack {len(pset)} rows ===')
    for t in sorted(miss): print('  RSSSF-ONLY', t); tot_bad+=1
    for t in sorted(extra): print('  PACK-ONLY ', t, pset[t]); tot_bad+=1
    # round-label coherence: Titul R3x round numbers
    lbl_ok=all(pset[k].split()[1][1:].isdigit() for k in pset)
    print('   verdict:', 'EXACT' if not miss and not extra else f'DIFFS {len(miss)}/{len(extra)}', '| round labels sane:', lbl_ok)
print('\nTOTAL DIVERGENCES:', tot_bad)
