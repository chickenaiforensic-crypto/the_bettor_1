#!/usr/bin/env python3
"""RSSSF Russia season pages (UTF-16) -> compact match universe CSV.
Sections by anchors: 1ldet=RPL rounds, prorel=REL, sup=SUP(yr base+1), cupdet=CUP,
2l/3la=LOWER (dropped). Cup kept only if a known RPL side (or reached stub) plays.
AET / penalty lines are EXCLUDED (90-min rule) and listed.
Integrity: recomputed league tables compared to RSSSF printed tables.
"""
import re, unicodedata

def decode(p): return open(p, 'rb').read().decode('utf-16', errors='ignore')

def norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', s.lower())

ALIAS = {
 'Dinamo Ms':'dinamo-msk','Dinamo Moscow':'dinamo-msk','Dinamo M':'dinamo-msk',
 'Baltika':'baltika','Spartak':'spartak','Zenit':'zenit','Lokomotiv':'lokomotiv',
 'Krylja S.':'krylja','Krylja Sovetov':'krylja','KS Samara':'krylja','KS':'krylja',
 'Akron':'akron','Akhmat':'akhmat','Ahmat':'akhmat','Rubin':'rubin','Rostov':'rostov',
 'Krasnodar':'krasnodar','CSKA':'cska','Orenburg':'orenburg','Fakel':'fakel',
 'Himki':'himki','Pari NN':'pari-nn','Nizhny Novgorod':'pari-nn',
 'Dinamo Mh':'dinamo-mkh','Dinamo Makhachkala':'dinamo-mkh','Soci':'sochi','Sochi':'sochi',
 'Ural':'ural','Rodina':'rodina','Rodina Ms':'rodina','Torpedo':'torpedo','SKA':'skaka',
 'SKA-Khabarovsk':'skaka','SKA-Habarovsk':'skaka','Enisey':'enisey','Jenisej':'enisey',
 'Sinnik':'shinnik','Shinnik':'shinnik','Rotor':'rotor','KAMAZ':'kamaz','Kamaz':'kamaz',
 'Arsenal':'arsenal-tula','Arsenal T.':'arsenal-tula','Cernomorec':'chernomorets',
 'Neftehimik':'neftekhimik','Tjumen':'tyumen','Volgar':'volgar','Sokol':'sokol',
 'Mordovia':'mordovia','Alania':'alania','Cajka':'chayka','Ufa':'ufa','Celjabinsk':'chelyabinsk',
}
CANON = {norm(k): v for k, v in ALIAS.items()}
KEYS = sorted(CANON, key=len, reverse=True)

def clean(s):
    s = re.sub(r'[\x00-\x1f\\<>_^`~]', '', s)
    s = s.split('(')[0].strip().rstrip('.').strip()
    return s

def canon(name):
    n = norm(name)
    if not n: raise ValueError('empty')
    if n in CANON: return CANON[n]
    for k in KEYS:
        if n.startswith(k) or k.startswith(n):
            return CANON[k]
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:24] or 'x'

MONTHS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
DATE = re.compile(r'^\[([A-Z][a-z]{2}) (\d{1,2})\]$')
SCORE = re.compile(r"^([A-Za-z0-9 .'~\^>-]{2,40}?) (\d{1,2})-(\d{1,2}) ([A-Za-z0-9 .'~\^>-]{2,40}?)$")
AET = re.compile(r'\[(aet|[^\]]*pen[^\]]*)\]\s*$', re.I)

ANCHORS = [('name="1ldet"','RPL'), ('name="prorel"','REL'), ('name="sup"','SUP'),
           ('name="cupdet"','CUP'), ('name="2l"','LOWER'), ('name="3la"','LOWER')]

def parse_doc(path, base, cutoff):
    txt = decode(path)
    lines = txt.split('\n')
    out, excluded, sec, cur = [], [], None, None
    for ln in lines:
        ln = re.sub(r'[\x00-\x1f]', '', ln).strip()
        low = ln.lower()
        for a, s in ANCHORS:
            if a in low: sec = s
        if sec is None: continue
        dm = DATE.match(ln)
        if dm:
            y = (base + 1) if sec == 'SUP' else (base if MONTHS[dm.group(1)] >= 7 else base + 1)
            cur = '%04d-%02d-%02d' % (y, MONTHS[dm.group(1)], int(dm.group(2)))
            continue
        sm = SCORE.match(ln)
        if sm and cur and sec != 'LOWER':
            h, a = clean(sm.group(1)), clean(sm.group(4))
            hg, ag = int(sm.group(2)), int(sm.group(3))
            if AET.search(ln):
                excluded.append((cur, sec, h, hg, ag, a)); continue
            rest = ln[sm.end():]
            if AET.search(rest):
                excluded.append((cur, sec, h, hg, ag, a)); continue
            if re.search(r'\d', h) or re.search(r'\d', a): continue  # standings debris
            try:
                hid, aid = canon(h), canon(a)
            except ValueError:
                continue
            if len(hid) < 3 or len(aid) < 3: continue
            out.append((cur, sec, hid, aid, hg, ag))
    # cup scope filter
    RPL_SET = {'zenit','spartak','cska','dinamo-msk','lokomotiv','krasnodar','rostov','rubin',
               'akhmat','orenburg','fakel','sochi','pari-nn','himki','dinamo-mkh','akron','krylja','baltika'}
    kept, scope = [], set(RPL_SET)
    for _ in range(3):
        for m in out:
            if m in kept: continue
            if m[1] == 'CUP':
                if m[2] in scope or m[3] in scope:
                    kept.append(m); scope.add(m[2]); scope.add(m[3])
            else:
                kept.append(m); scope.add(m[2]); scope.add(m[3])
    final, seen = [], set()
    for m in sorted(kept):
        if m[0] >= cutoff: continue
        k = (m[0], m[2], m[3], m[4], m[5])
        if k in seen: continue
        seen.add(k); final.append(m)
    return final, excluded

allm = []
for path, base, cutoff in (('rus2025.html', 2024, '2025-12-31'), ('rus2026.html', 2025, '2026-08-01')):
    m, ex = parse_doc(path, base, cutoff)
    m = [x for x in m if x[0] < cutoff]
    print('%s -> %d matches kept (%d AET/pen excluded)' % (path, len(m), len(ex)))
    for e in ex:
        if e[5].lower().startswith(('akron', 'rubin')) or e[2].lower().startswith(('akron', 'rubin')):
            print('   EXCLUDED-AET/PEN involving target team:', e)
    allm += m
with open('rpl_universe.csv', 'w') as f:
    f.write('date,comp,home,away,hg,ag\n')
    for r in sorted(set(allm)):
        f.write('%s,%s,%s,%s,%d,%d\n' % r)
uniq = sorted(set(allm))
print('total unique:', len(uniq))
from collections import Counter
print(Counter(m[1] for m in uniq))

for season, want in (('2024-07-01|2025-06-30', {'krasnodar':(20,7,3,59,23),'zenit':(20,6,4,58,18),'cska':(17,8,5,47,21),'spartak':(17,6,7,56,25),'dinamo-msk':(16,8,6,61,35),'lokomotiv':(15,8,7,51,41),'rubin':(13,6,11,42,45),'rostov':(10,9,11,41,43),'akron':(10,5,15,39,55),'krylja':(8,7,15,36,51),'dinamo-mkh':(6,11,13,27,35),'himki':(6,11,13,35,56),'pari-nn':(7,6,17,27,54),'akhmat':(4,13,13,27,48),'orenburg':(4,7,19,28,56),'fakel':(2,12,16,14,42)}),
                     ('2025-07-01|2026-06-30', {'zenit':(20,8,2,53,19),'krasnodar':(20,6,4,60,23),'lokomotiv':(14,11,5,54,39),'spartak':(15,7,8,47,39),'cska':(15,6,9,44,33),'baltika':(11,13,6,38,21),'dinamo-msk':(12,9,9,51,40),'rubin':(11,10,9,29,30),'akhmat':(9,10,11,35,39),'rostov':(8,9,13,25,32),'krylja':(8,8,14,35,50),'orenburg':(7,8,15,29,44),'akron':(6,9,15,35,53),'dinamo-mkh':(5,11,14,19,37),'pari-nn':(6,5,19,26,50),'sochi':(6,4,20,29,60)})):
    lo, hi = season.split('|')
    tab = {}
    for m in uniq:
        d, c, h, a, hg, ag = m
        if c != 'RPL' or not (lo <= d <= hi): continue
        for t, gf, ga, w, dr_, l in ((h, hg, ag, hg > ag, hg == ag, hg < ag), (a, ag, hg, ag > hg, ag == hg, ag < hg)):
            r = tab.setdefault(t, [0, 0, 0, 0, 0]); r[3] += gf; r[4] += ga
            r[0] += 1 if w else 0; r[1] += 1 if dr_ else 0; r[2] += 1 if l else 0
    bad = 0
    for t, exp in want.items():
        got = tab.get(t)
        if not got or list(exp) != got:
            bad += 1; print('  MISMATCH', t, 'want', exp, 'got', got)
    print('season integrity %s: %s' % (season, 'PASS (16/16)' if bad == 0 else 'FAIL %d' % bad))
