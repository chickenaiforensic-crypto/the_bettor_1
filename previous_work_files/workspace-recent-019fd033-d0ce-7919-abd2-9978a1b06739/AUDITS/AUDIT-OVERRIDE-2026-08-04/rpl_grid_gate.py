#!/usr/bin/env python3
# WAVE-2 Gate: RPL full round-grid — every pack league row (date+pairing+score) must
# appear in RSSSF rus{2022..2026} round prints: score lines under [Mon d] date headers.
import re, unicodedata, datetime

PACK = 'RPL-2021-2026.txt'
RSS = {s: f'/home/user/REFERENCE/rsssf-ref/rus{y}.txt' for s, y in
       [('2021-22', 2022), ('2022-23', 2023), ('2023-24', 2024), ('2024-25', 2025), ('2025-26', 2026)]}
SPAN = {'2021-22': ('2021-07-01', '2022-06-30'), '2022-23': ('2022-07-01', '2023-06-30'),
        '2023-24': ('2023-07-01', '2024-06-30'), '2024-25': ('2024-07-01', '2025-06-30'),
        '2025-26': ('2025-06-20', '2026-06-30')}
MON = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()

ALIAS = {
 'zenit':'Zenit St Petersburg','dinamo ms':'Dynamo Moscow','dinamo':'Dynamo Moscow','cska':'CSKA Moscow',
 'lokomotiv':'Lokomotiv Moscow','spartak':'Spartak Moscow','torpedo':'Torpedo Moscow',
 'ahmat':'Akhmat Grozny','akhmat':'Akhmat Grozny','pari nn':'Pari Nizhny Novgorod',
 'dinamo mh':'Dynamo Makhachkala','fakel':'Fakel Voronezh','soci':'PFC Sochi','sochi':'PFC Sochi',
 'krylja s':'Krylia Sovetov Samara','ks samara':'Krylia Sovetov Samara','krylja sovetov':'Krylia Sovetov Samara',
 'nnovgorod':'Pari Nizhny Novgorod','akron':'Akron Tolyatti','ural':'Ural Yekaterinburg',
 'himki':'FC Khimki','khimki':'FC Khimki','ufa':'FC Ufa','baltika':'Baltika Kaliningrad',
 'orenburg':'FC Orenburg','arsenal':'Arsenal Tula','rubin':'Rubin Kazan','rostov':'FC Rostov',
 'krasnodar':'FC Krasnodar','nizhniy novgorod':'Pari Nizhny Novgorod','nizh novgorod':'Pari Nizhny Novgorod',
 'tambov':'Tambov','rotor':'Rotor Volgograd','arsenal tula':'Arsenal Tula',
}

line_re = re.compile(r'^\s*([A-Za-z\xc0-\xff][A-Za-z\xc0-\xff .\'-]*?)\s+(\d+)[\u2013-](\d+)\s+([A-Za-z\xc0-\xff][A-Za-z\xc0-\xff .\'-]*?)\s*(?:\[.*)?$')
date_re = re.compile(r'^\[([A-Z][a-z]{2})\s+(\d{1,2})(?:\s*[-\u2013]\s*(?:([A-Z][a-z]{2})\s+)?(\d{1,2}))?\]\s*$')
round_re = re.compile(r'^(?:Ladbrokes |MIR |FONBET |ALFA-BANK )?Round\s+(\d+)\b')

def load_rss(path, season_tag):
    rows = {}   # (normhome, normaway) -> list of (date, hg, ag)
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    cur_dates = []
    in_1l = False
    year_a = int(season_tag[:4]); year_b = year_a + 1
    for i, ln in enumerate(lines):
        if 'name="1ldet"' in ln or 'name="1l"' in ln: in_1l = True
        if 'name="kubok"' in ln or 'name="2l"' in ln: in_1l = False
        if not in_1l: continue
        rm = re.match(r'^Round\s+\d+\s+\[([A-Z][a-z]{2})\s+(\d{1,2})(?:\s*[-\u2013]\s*(?:([A-Z][a-z]{2})\s+)?(\d{1,2}))?', ln.strip())
        if rm:
            m1 = MON[rm.group(1).lower()]; d1 = int(rm.group(2))
            y1 = year_a if m1 >= 7 else year_b
            cur_dates = [f'{y1:04d}-{m1:02d}-{d1:02d}']
            if rm.group(4):
                m2 = MON[(rm.group(3) or rm.group(1)).lower()]; d2 = int(rm.group(4))
                y2 = year_a if m2 >= 7 else year_b
                cur_dates.append(f'{y2:04d}-{m2:02d}-{d2:02d}')
            continue
        m = date_re.match(ln.strip())
        if m:
            m1 = MON[m.group(1).lower()]; d1 = int(m.group(2))
            y1 = year_a if m1 >= 7 else year_b
            cur_dates = [f'{y1:04d}-{m1:02d}-{d1:02d}']
            if m.group(4):
                m2 = MON[(m.group(3) or m.group(1)).lower()]; d2 = int(m.group(4))
                y2 = year_a if m2 >= 7 else year_b
                cur_dates.append(f'{y2:04d}-{m2:02d}-{d2:02d}')
            continue
        lm = line_re.match(ln)
        if lm and cur_dates:
            h, g1, g2, a = lm.group(1).strip(), int(lm.group(2)), int(lm.group(3)), lm.group(4).strip()
            if 'Att:' in h or 'Att:' in a: continue
            hn, an = norm(h), norm(a)
            hn = norm(ALIAS.get(hn, hn)); an = norm(ALIAS.get(an, an))
            for d in cur_dates:
                rows.setdefault((hn, an), []).append((d, g1, g2))
    return rows

# parse pack league rows
pack_rows = []
for ln in open(PACK, encoding='utf-8'):
    if not ln.startswith('MATCH|'): continue
    p = ln.rstrip('\n').split('|')
    if p[2] != 'Russian Premier League': continue
    pack_rows.append((p[1], p[4], int(p[5]), int(p[6]), p[7]))
print('pack league rows:', len(pack_rows))

tot = ok = 0
fails = []
for s, path in RSS.items():
    a, b = SPAN[s]
    rows = load_rss(path, s)
    rss_rows = sum(len(v) for v in rows.values())
    prs = [r for r in pack_rows if a <= r[0] <= b]
    sok = 0
    for d, h, hg, ag, aw in prs:
        tot += 1
        keysw = [(norm(h), norm(aw))]
        hit = None
        for key in keysw:
            for cand in rows.get(key, []):
                if cand[1] == hg and cand[2] == ag:
                    hit = cand; break
            if hit: break
        if hit:
            if hit[0] == d: ok += 1; sok += 1
            else: fails.append((s, d, h, hg, ag, aw, 'DATE rsssf=' + hit[0]))
        else:
            fails.append((s, d, h, hg, ag, aw, 'NO MATCH/score in RSSSF'))
    print(f'{s}: pack rows {len(prs)} | rsssf parsed {rss_rows} | exact {sok}')
print(f'TOTAL exact: {ok}/{tot}')
for f in fails[:25]: print('FAIL:', f)
print('fail count:', len(fails))
