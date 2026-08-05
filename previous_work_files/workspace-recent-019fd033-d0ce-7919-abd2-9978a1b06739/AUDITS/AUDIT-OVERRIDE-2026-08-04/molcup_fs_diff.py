#!/usr/bin/env python3
# MOLCUP full-span wave-1 diff: pack 2024-25 + 2025-26 rows vs RSSSF tsje2025/2026
# cup chapters (R3, 1/8, QF, SF, F). 90-min doctrine: '[aet' WITHOUT 'pen' => printed
# score is post-AET -> cannot bind 90-min from RSSSF (wf evidence registered); score-adv
# NOTE existence is enforced via pack NOTEs mapped by fixture fingerprint.
import re, html, sys

PACK = '/home/user/AUDIT-OVERRIDE-2026-08-04/MOLCUP-FULLSPAN.txt'
FILES = {'2024-25': '/home/user/rsssf-ref/tsje2025.txt', '2025-26': '/home/user/rsssf-ref/tsje2026.txt'}
MON = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

def canon(s):
    return re.sub(r'[ \t]+', ' ', html.unescape(s)).rstrip()

# czech alias: normalised-lowercase rsssf print -> pack canonical
import unicodedata
def N(s):
    s = unicodedata.normalize('NFKD', html.unescape(s)).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
AL = {}
def a(k, v): AL[N(k)] = v
for k, v in [
 ('AC Sparta Praha','Sparta Prague'),('Sparta Praha','Sparta Prague'),('SK Slavia Praha','Slavia Prague'),('Slavia Praha','Slavia Prague'),
 ('FC Viktoria Plzen','Viktoria Plzen'),('Viktoria Plzen','Viktoria Plzen'),('1.FC Slovacko','Slovacko'),('1. FC Slovacko','Slovacko'),
 ('SK Sigma Olomouc','Sigma Olomouc'),('Sigma Olomouc','Sigma Olomouc'),('FC Banik Ostrava','Banik Ostrava'),
 ('FK Jablonec','Jablonec'),('FK Mlada Boleslav','Mlada Boleslav'),('FC Slovan Liberec','Slovan Liberec'),
 ('FK Teplice','Teplice'),('FC Hradec Kralove','Hradec Kralove'),('SK Dynamo Ceske Budejovice','Ceske Budejovice'),
 ('Bohemians 1905 Praha','Bohemians 1905'),('FC Zlin','Zlin'),('MFK Karvina','Karvina'),('FK Pardubice','Pardubice'),
 ('FC Zbrojovka Brno','Zbrojovka Brno'),('FK Dukla Praha','Dukla Prague'),('SK Lisen','Lisen'),('SK Lisen 2019','Lisen'),
 ('SK Artis Brno','Artis Brno'),('FK Varnsdorf','Varnsdorf'),('MFK Vyskov','Vyskov'),('SFC Opava','Opava'),
 ('Slezsky FC Opava','Opava'),('FC Tabor','Taborsko'),('FC Taborsko','Taborsko'),('FK Usti nad Labem','Usti nad Labem'),
 ('FK Viktoria Zizkov','Zizkov'),('FC Vysocina Jihlava','Jihlava'),('SK Hanacka Slavia Kromeriz','Kromeriz'),
 ('SK Kromeriz','Kromeriz'),('Spartak Police nad Metuji','Police nad Metuji'),('FC Hlucin','Hlucin'),
 ('FK Loko Praha','Loko Praha'),('SK Zapy','Zapy'),('SK Benatky nad Jizerou','Benatky nad Jizerou'),
 ('CSK Uhersky Brod','Uhersky Brod'),('SK Horovice','Horovice'),('FK MAS Taborsko','Taborsko'),
 ('MFK Chrudim','Chrudim'),('FC Sellier & Bellot Vlasim','Vlasim'),('FK Viagem Pribram','Pribram'),
 ('TJ Sokol Lanzhot','Lanzhot'),('SK Sokol Brozany','Brozany'),('FK Horni Redice','Horni Redice'),
 ('TJ Jiskra Domazlice','Domazlice'),('FK Nove Sady','Nove Sady'),('FC SK Artis Brno','Artis Brno'),
 ('FC Trinity Zlin','Zlin'),('TJ Jiskra Usti nad Orlici','Usti nad Orlici'),('FK Fotbal Trinec','Trinec'),
 ('FK Banik Sokolov','Sokolov'),('SK Petrin Plzen','Petrin Plzen'),('FK Admira Praha','Admira Praha'),
 ('1.SK Prostejov','Prostejov'),('FC Silon Taborsko','Taborsko'),('FC Silon Taborsko 2','Taborsko'),
 ('SK Dynamo ceske Budejovice','Ceske Budejovice'),('SK Han. Slavia Kromeriz','Kromeriz')]:
    a(k, v)

STAGE_ORDER = ['Round 3', '1/8 Finals', 'Quarterfinals', 'Semifinals', 'Final']
def parse_tsje(path):
    L = open(path, encoding='utf-8', errors='replace').read().splitlines()
    start = next(i for i, l in enumerate(L) if 'name="cup"' in l)
    ties = []
    stage = None; yd = None  # (mon, day)
    i = start
    while i < len(L):
        line = canon(L[i])
        s = line.strip()
        hit = False
        for st in STAGE_ORDER:
            if s.startswith(st):
                stage = st; hit = True
                mfin = re.search(r'May (\d{1,2})', s)
                if st.startswith('Final'): yd = (5, int(mfin.group(1))) if mfin else None
                break
        if s.startswith('Národní') or '<h4>' in s and stage:
            break
        if not hit:
            m = re.match(r'^\[([A-Z][a-z]{2}) (\d{1,2})', s)
            if m: yd = (MON[m.group(1)], int(m.group(2)))
            else:
                m2 = re.match(r'^(.+?) (\d+)-(\d+) (.+?)( \[(.*))?$', s)
                if m2 and stage:
                    home, hg, ag, away = m2.group(1), int(m2.group(2)), int(m2.group(3)), m2.group(4)
                    bracket = m2.group(6) or ''
                    # wrapped bracket tail (next line continues)
                    j = i + 1
                    while ('[' in s and ']' not in s) and j < len(L):
                        bracket += ' ' + canon(L[j]).strip(); s += ']'; j += 1
                    ties.append(dict(stage=stage, d=yd, home=home.strip(), hg=hg, ag=ag, away=away.strip(), bk=bracket))
        i += 1
    return ties

def parse_pack(path, season):
    lo, hi = {'2024-25': ('2024-07-01', '2025-06-30'), '2025-26': ('2025-07-01', '2026-06-30')}[season]
    rows = []
    for l in open(path, encoding='utf-8'):
        if not l.startswith('MATCH|'): continue
        p = l.rstrip('\n').split('|')
        d = p[1]
        if lo <= d <= hi: rows.append(dict(date=d, home=p[4], hg=int(p[5]), ag=int(p[6]), away=p[7], st=p[8]))
    return rows

STMAP = {'Round 3': 'R3', '1/8 Finals': 'R16', 'Quarterfinals': 'QF', 'Semifinals': 'SF', 'Final': 'Final'}
def cname(x):
    n = N(x)
    if n in AL: return AL[n]
    hits = [v for k, v in AL.items() if n and (n in k or k in n)]
    return hits[0] if len(hits) == 1 else x

errs = []
for season, path in FILES.items():
    ties = parse_tsje(path)
    rows = parse_pack(PACK, season)
    print(f'--- {season}: tsje ties {len(ties)} vs pack rows {len(rows)}')
    used = set()
    for t in ties:
        stg = STMAP.get(t['stage'], t['stage'])
        h, aw = cname(t['home']), cname(t['away'])
        # find pack row same stage + side pairing (any order)
        cand = [k for k, r in enumerate(rows)
                if k not in used and r['st'] == stg and {r['home'], r['away']} == {h, aw}]
        if not cand:
            errs.append(f'{season} {stg}: NO PACK ROW for {t["home"]} {t["hg"]}-{t["ag"]} {t["away"]} [{t["bk"]}] ({h}/{aw})'); continue
        k = cand[0]; r = rows[k]; used.add(k)
        aet = 'aet' in t['bk'].lower(); pen = 'pen' in t['bk'].lower()
        if r['home'] != h:  # orientation flip check
            errs.append(f'{season} {stg}: ORIENTATION pack {r["home"]}-{r["away"]} vs rsssf {h}-{aw}'); continue
        if pen or not aet:
            if (r['hg'], r['ag']) != (t['hg'], t['ag']):
                errs.append(f'{season} {stg}: SCORE pack {r["hg"]}-{r["ag"]} vs rsssf {t["hg"]}-{t["ag"]} for {h}-{aw} (bk={t["bk"]})')
        else:  # pure aet: printed = post-aet final; pack must carry 90-min (different) + advancement NOTE
            if (r['hg'], r['ag']) == (t['hg'], t['ag']):
                errs.append(f'{season} {stg}: AET tie {h}-{aw}: pack score == rsssf FINAL {t["hg"]}-{t["ag"]} — 90-min doctrine violated?')
            # advancement note check
            txt = open(PACK, encoding='utf-8').read()
            if not re.search(r'NOTE\|info\|advancement\|[^\n]*' + re.escape(r['home']), txt):
                errs.append(f'{season} {stg}: AET tie {h}-{aw}: no advancement NOTE for {r["home"]}')
        # date compare (RSSSF day vs pack dateISO)
        if t['d']:
            pm, pd = int(r['date'][5:7]), int(r['date'][8:10])
            if (pm, pd) != t['d']:
                errs.append(f'{season} {stg}: DATE pack {r["date"]} vs rsssf {t["d"]} for {h}-{aw}')
    left = [k for k in range(len(rows)) if k not in used and rows[k]['st'] in ('R3', 'R16', 'QF', 'SF', 'Final')]
    r3 = [k for k in range(len(rows)) if k not in used and rows[k]['st'] == 'R2']
    for k in left: errs.append(f'{season}: PACK ROW NOT ON RSSSF: {rows[k]}')
    print(f'   matched {len(used)} | pack R2 rows (non-RSSSF by design): {len(r3)}')
print('=== MOLCUP fs-diff ERRORS ===' if errs else '=== MOLCUP fs-diff: NO ERRORS ===')
for e in errs: print('  ', e)
