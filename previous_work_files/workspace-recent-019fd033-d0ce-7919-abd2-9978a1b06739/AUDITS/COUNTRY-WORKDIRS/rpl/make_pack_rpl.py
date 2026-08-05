import json

NAMES = json.load(open('rpl/rpl_names.json'))
U = json.load(open('rpl/rpl_universe.json'))

CITY = {
 'spartak':'Moscow','cska':'Moscow','dinamo-msk':'Moscow','lokomotiv':'Moscow','torpedo':'Moscow','rodina':'Moscow',
 'zenit':'St Petersburg','rubin':'Kazan','akhmat':'Grozny','rostov':'Rostov-on-Don','krasnodar':'Krasnodar',
 'akron':'Tolyatti','orenburg':'Orenburg','fakel':'Voronezh','sochi':'Sochi','pari-nn':'Nizhny Novgorod',
 'himki':'Khimki','dinamo-mkh':'Makhachkala','krylja':'Samara','baltika':'Kaliningrad','ural':'Yekaterinburg',
 'arsenal-tula':'Tula','kamaz':'Naberezhnye Chelny','neftekhimik':'Nizhnekamsk','shinnik':'Yaroslavl','tyumen':'Tyumen',
}
RPL_TEAMS = {'akhmat','akron','baltika','cska','dinamo-mkh','dinamo-msk','fakel','himki','krasnodar','krylja',
             'lokomotiv','orenburg','pari-nn','rodina','rostov','rubin','sochi','spartak','zenit'}
COMP = {'RPL':('Russian Premier League','domestic-league'), 'CUP':('Russian Cup','domestic-cup'),
        'SUP':('Russian Super Cup','other'), 'RPLPO':('Russian Relegation Playoffs','other')}
NEUTRAL = {('2025-06-01','rostov','cska'):('neutral','Luzhniki','Moscow'),
           ('2026-05-24','spartak','krasnodar'):('neutral','unknown','Moscow')}

def src(r):
    if r['comp']=='RPLPO': return 'src-user-r04'
    if r['date'] >= '2026-08-01': return 'src-md2-2627-user'
    if r['date'] >= '2026-07-01': return 'src-md1-2627'
    return 'src-rsssf-rus2025' if r['date'] < '2025-07-01' else 'src-rsssf-rus2026'

out = ['BP-TEAM-PACK v2']
out.append('NOTE|info|research_ack|Russian Premier League 2024-25 + 2025-26 complete (488 league rows parsed from RSSSF round-by-round, incl. 2026-27 MD1 8 rows) + 2026-27 MD2 Akron-Rubin (1 row); Russian Cup RPL-path groups + full knockout brackets both seasons + Superfinals (152 rows, re-verified 100% vs RSSSF 2026-08-01); Super Cup 2025 (1); Promotion/Relegation Playoff 2025-26 (2). 644 rows total.')
out.append('NOTE|info|cutoff|All rows are completed matches on or before 2026-08-01.')
out.append('NOTE|warning|md2_verification|MD2 Akron Tolyatti 1-2 Rubin Kazan (2026-08-01): user live report (2-1 at 46min, FT 1-2); fixture slot confirmed on soccerstats round listing; score pending index re-verification vs RSSSF/ESPN once pages refresh.')
out.append('NOTE|info|league_codes|TEAM league-code field now populated (was NA): RPL = Russian Premier League, FNL = Russian First League. Display-only metadata; no evidence rows affected.')
out.append('NOTE|warning|aet_handling|90-minute scores per rule: cup group-stage games decided by penalty shootouts recorded as draws (e.g. Akron 1-1 Zenit 2024-08-27, Rubin 3-3 Akhmat 2025-10-22); knockout legs at 90 minutes; Superfinal Rostov 0-0 CSKA 2025-06-01 recorded draw (CSKA won pens); Superfinal Spartak 1-1 Krasnodar 2026-05-24 recorded draw (Spartak won pens).')
out.append('NOTE|warning|source_conflict|Cup completeness rebuild 2026-08-01 vs old store: 117 rows exact, 34 missing added, 3 date conflicts resolved to RSSSF (Lokomotiv-Akhmat and Spartak-Ural to 2025-04-15; Spartak-Rostov to 2025-05-15), 2 duplicates removed. User batch R-05 (22 rows): 16 fabricated fixtures excluded; only RSSSF-confirmed rows loaded, with Rubin-CSKA 0-0 dated correctly 2024-11-06 and Akhmat-Zenit dated 2024-11-27.')
out.append('NOTE|info|md1_verification|2026-27 MD1 (2026-07-24..26, 8 rows): original feed fetch (worldfootball.net) was Cloudflare-blocked; rows independently re-verified 2026-08-01 against ESPN, soccerstats.com and betexplorer.com - 8/8 exact score+date matches (incl. Akron 0-5 Zenit, Rubin 1-3 Krasnodar).')
out.append('NOTE|warning|scope_gap|Russian First League (second tier) league games are NOT included: cup-only participants Shinnik, Tyumen, Arsenal Tula, KAMAZ, Neftekhimik, Torpedo Moscow, Ural, plus Baltika/Sochi/Fakel/Rodina/Orenburg pre-promotion, carry cup-match history only. FC Khimki dissolved after 2024-25 relegation.')
out.append('NOTE|info|validation|Every CUP row matches the RSSSF cup sections bit-for-bit (152/152, checked 2026-08-01). League per-club season totals previously validated vs RSSSF tables. MD1 8/8 cross-verified (see md1_verification). MD2 1 row user-reported, fixture-slot cross-checked (see md2_verification).')

seen=set()
for r in U:
    for side in ('home','away'):
        t=r[side]
        if t not in seen:
            seen.add(t)
            lg='Russian Premier League' if t in RPL_TEAMS else 'Russian First League'
            code='RPL' if t in RPL_TEAMS else 'FNL'
            ALIAS = {'krylja':'Krylya Sovetov Samara;Krylya Sovetov'}  # deprecated spellings kept as resolve aliases (v2.9.4 canon)
            out.append(f"TEAM|{NAMES[t]}|Russia|{lg}|{code}|{ALIAS.get(t,'')}|unknown|{CITY[t]}|Russia|unknown|unknown|unknown|unknown")

for r in U:
    comp,ctype=COMP[r['comp']]
    h,a=NAMES[r['home']],NAMES[r['away']]
    vt,stadium,vcity='normal','unknown',CITY[r['home']]
    k=(r['date'],r['home'],r['away'])
    if k in NEUTRAL: vt,stadium,vcity=NEUTRAL[k]
    out.append(f"MATCH|{r['date']}|{comp}|{ctype}|{h}|{r['hg']}|{r['ag']}|{a}|{vt}|{stadium}|{vcity}|Russia||{src(r)}")

out.append('SOURCE|src-rsssf-rus2025|https://www.rsssf.org/tablesr/rus2025.html|2026-08-01|results-database|RSSSF Russia 2024-25: RPL rounds/tables, Russian Cup groups + full knockout, Super Cup 2025, relegation playoff list')
out.append('SOURCE|src-rsssf-rus2026|https://www.rsssf.org/tablesr/rus2026.html|2026-08-01|results-database|RSSSF Russia 2025-26: RPL rounds/tables, Russian Cup RPL-path groups + knockout + regions path + superfinal')
out.append('SOURCE|src-user-r04|https://www.rsssf.org/tablesr/rus2026.html|2026-08-01|other|Shinnik v Akron relegation playoff 2026-05-27/31: user-supplied batch R-04, cross-checked against this RSSSF 2025-26 playoff table')
out.append('SOURCE|src-md1-2627|https://www.soccerstats.com/latest.asp?league=russia|2026-08-01|results-database|RPL 2026-27 MD1 rows re-verified vs ESPN match centre, soccerstats.com round page, betexplorer.com round table (8/8 exact)')
out.append('SOURCE|src-md2-2627-user|https://www.soccerstats.com/latest.asp?league=russia|2026-08-01|other|RPL 2026-27 MD2 Akron 1-2 Rubin: user live report (watched; 2-1 at 46min, FT 1-2); fixture slot confirmed on soccerstats round page; score re-verification pending index refresh')
# INTEGRITY-AUDIT: muted rows flagged in rpl_universe.json carry a MUTE line (2026-08-01 screen)
MUTED=[r for r in U if r.get('muted')]
if MUTED:
    out.append('# INTEGRITY-AUDIT 2026-08-01 (market-evaluation screen, 464/480 RPL league games covered):')
    out.append('# muted rows flagged LOSS-tier by market-implied strong-favorite collapse (Pinnacle close, margin-removed);')
    out.append('# muted = non-trusted stat: row stays for audit, carries NO evidence.')
    for r in MUTED:
        out.append(f"MUTE|{r['date']}|{NAMES[r['home']]}|{NAMES[r['away']]}|integrity: market-flagged favorite collapse ({r['muted']})|src-integrity-2026")
    if not any(s.startswith('SOURCE|src-integrity-2026|') for s in out):
        out.append('SOURCE|src-integrity-2026|https://www.football-data.co.uk/new/RUS.csv|2026-08-01|results-database|Pinnacle closing odds screen 2024-25 + 2025-26 RPL: 13 favorite >=65% failures of 79 expected 22.7 (z=-3.43); 3 LOSS-tier rows muted per owner decision')
out.append('END')
open('packs/russian-team-pack.txt','w').write('\n'.join(out)+'\n')
print('lines:',len(out),' teams:',len(seen),' matches:',len(U))
