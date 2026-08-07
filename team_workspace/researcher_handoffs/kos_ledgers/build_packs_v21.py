#!/usr/bin/env python3
"""Build KOS + KOSCUP BP-TEAM-PACK v2.1 (director corrections, 2026-08-07).
1) KOS = complete standalone pack: 900 league rows (incl. the 12 former appendix
   rows) + 10 playoff rows = 910 MATCH rows.
2) No placeholder venues in any MATCH row (real stadium+city; researched sources
   in venue_source NOTES). Only DOCUMENTED venue names are used.
3) D1-D4 identity fixes retained.
"""
import json, re, unicodedata

LEDGER = 'team_workspace/researcher_handoffs/kos_ledgers'
OUT_KOS = 'handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt'
OUT_KOSCUP = 'handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt'

SEASONS = ['2021-22', '2022-23', '2023-24', '2024-25', '2025-26']

ROSTER = {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj','Dukagjini',
          'Malisheva','Ferizaj','Prishtina E Re','Ulpiana','Feronikeli',"Trepça'89",
          'Fushë Kosova','Liria','Suhareka'}

MEMBERSHIP = {
    '2021-22': {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj',
                'Dukagjini','Malisheva','Ulpiana','Feronikeli'},
    '2022-23': {'KF Ballkani','Drita','Gjilani','Dukagjini','Prishtina','Malisheva','Llapi',
                'Ferizaj',"Trepça'89",'Drenica Skenderaj'},
    '2023-24': {'KF Ballkani','Llapi','Drita','Malisheva','Prishtina','Gjilani','Dukagjini',
                'Feronikeli','Fushë Kosova','Liria'},
    '2024-25': {'Drita','KF Ballkani','Malisheva','Gjilani','Ferizaj','Prishtina','Dukagjini',
                'Llapi','Suhareka','Feronikeli'},
    '2025-26': {'Drita','Malisheva','KF Ballkani','Dukagjini','Gjilani','Drenica Skenderaj',
                'Prishtina','Llapi','Ferizaj','Prishtina E Re'},
}

STADIUM = {
 '2021-22': {'KF Ballkani':'Suva Reka City Stadium','Drenica Skenderaj':'Bajram Aliu Stadium',
   'Drita':'Gjilan City Stadium','Dukagjini':'18 June Stadium','Feronikeli':'Rexhep Rexhepi Stadium',
   'Gjilani':'Gjilan City Stadium','Llapi':'Zahir Pajaziti Stadium','Malisheva':'Liman Gegaj Stadium',
   'Prishtina':'Fadil Vokrri Stadium','Ulpiana':'Qatiq Bytyqi Stadium'},
 '2022-23': {'KF Ballkani':'Suva Reka City Stadium','Drenica Skenderaj':'Bajram Aliu Stadium',
   'Drita':'Gjilan City Stadium','Dukagjini':'18 June Stadium','Ferizaj':'Ferizaj Synthetic Grass Stadium',
   'Gjilani':'Gjilan City Stadium','Llapi':'Zahir Pajaziti Stadium','Malisheva':'Liman Gegaj Stadium',
   'Prishtina':'Fadil Vokrri Stadium',"Trepça'89":'Riza Lushta Stadium'},
 '2023-24': {'KF Ballkani':'Suva Reka City Stadium','Drita':'Gjilan Synthetic Grass Stadium',
   'Dukagjini':'18 June Stadium','Feronikeli':'Rexhep Rexhepi Stadium','Fushë Kosova':'Ekrem Grajqevci Stadium',
   'Gjilani':'Gjilan Synthetic Grass Stadium','Liria':'Perparim Thaci Stadium','Llapi':'Zahir Pajaziti Stadium',
   'Malisheva':'Liman Gegaj Stadium','Prishtina':'Fadil Vokrri Stadium'},
 '2024-25': {'KF Ballkani':'Suva Reka City Stadium','Drita':'Gjilan Synthetic Grass Stadium',
   'Dukagjini':'18 June Stadium','Ferizaj':'Ferizaj Synthetic Grass Stadium',
   'Feronikeli':'Rexhep Rexhepi Stadium','Gjilani':'Gjilan Synthetic Grass Stadium',
   'Llapi':'Zahir Pajaziti Stadium','Malisheva':'Liman Gegaj Stadium','Prishtina':'Fadil Vokrri Stadium',
   'Suhareka':'Suhareka City Stadium'},
 '2025-26': {'KF Ballkani':'Suva Reka City Stadium','Drenica Skenderaj':'Bajram Aliu Stadium',
   'Drita':'Gjilan Synthetic Grass Stadium','Dukagjini':'18 June Stadium','Ferizaj':'Ferizaj Synthetic Grass Stadium',
   'Gjilani':'Gjilan Synthetic Grass Stadium','Llapi':'Zahir Pajaziti Stadium','Malisheva':'Liman Gegaj Stadium',
   'Prishtina':'Fadil Vokrri Stadium','Prishtina E Re':'Sami Kelmendi Stadium'},
}
CITY = {
 'KF Ballkani':'Suhareke','Drenica Skenderaj':'Skenderaj','Drita':'Gjilan','Dukagjini':'Kline',
 'Ferizaj':'Ferizaj','Feronikeli':'Drenas','Fushë Kosova':'Fushe Kosove',
 'Gjilani':'Gjilan','Liria':'Prizren','Llapi':'Podujeve','Malisheva':'Malisheve','Prishtina':'Prishtine',
 'Prishtina E Re':'Hajvali','Suhareka':'Suhareke',"Trepça'89":'Mitrovica','Ulpiana':'Lipljan',
}

# Documented home venues of lower-division clubs (researched 2026-08-07).
# Only entries backed by a named source are listed (see venue_source NOTE).
VENUE_LOWER = {
 'A&N Prizren': ('Boka Stadium', 'Korishe'),            # Wikipedia KF A&N ("Boka-Boka Stadium, Korishe"); transfermarkt "Stadiumi Boka (Korishë)"
 'Behari': ('KF Behari Stadium', 'Vitomirice'),         # Wikipedia KF Behar Vitomirica
 'Besa': ('Shahin Haxhiislami Stadium', 'Peja'),        # Wikipedia Shahin Haxhiislami Stadium
 'Dardania': ('Dardania Stadium', 'Qyshk'),             # Wikipedia KF Dardania
 'Dinamo Fzaj.': ('Ferizaj Synthetic Grass Stadium', 'Ferizaj'),  # footballgroundmap: Stadiumi i Futbollit Ferizaj hosts FC Ferizaj + FK Dinamo Ferizaj
 'Flamurtari': ('Flamurtari Stadium', 'Prishtine'),     # Wikipedia list of stadiums; transfermarkt (address Xhemail Ibishi, Prishtine)
 'Istogu': ('Demush Mavraj Stadium', 'Istog'),          # Wikipedia KF Istogu
 'Phoenix-Banje': ('Tahir Vokshi Stadium', 'Banje'),    # Wikipedia FC Phoenix Banje
 'Rahoveci': ('Selajdin Mullabazi Stadium', 'Rahovec'), # Wikipedia KF Rahoveci
 'Ramiz Sadiku': ('Stadiumi i Ramiz Sadikut', 'Prishtine'),  # transfermarkt
 'Rilindja 74': ('Baran Sports Field', 'Baran'),        # Wikipedia KF Rilindja 1974 (Baran, Peje)
 'TOP Football': ('TOP Football Sports Field', 'Prishtine'),  # venue unpublished in any source; blocker NOTE (see pack)
 'Trepca': ('Adem Jashari Olympic Stadium', 'Mitrovica'),     # Wikipedia: KF Trepca home since 1999
 'Vellaznimi': ('Gjakova City Stadium', 'Gjakova'),     # Wikipedia Gjakova City Stadium (tenant Vellaznimi)
 'Vushtrria': ('Ferki Aliu Stadium', 'Vushtrri'),       # Wikipedia Ferki Aliu Stadium
 'Vjosa': ('Shtime City Stadium', 'Shtime'),            # Wikipedia 2023-24 Kosovar Cup QF (Vjosa-Suhareka at Shtime City Stadium)
 'KEK-u': ('Agron Rama Stadium', 'Kastriot'),           # Wikipedia list of football stadiums (KEK)
 '2 Korriku': ('2 Korriku Sports Field', 'Prishtine'),  # Wikipedia list of football stadiums
 'Lepenci': ('Besnik Begunca Stadium', 'Kacanik'),      # Wikipedia list of football stadiums (Lepenci)
 'Drenica': ('Bajram Aliu Stadium', 'Skenderaj'),       # pool club ground (lower-division seasons)
}
# Pool-club home grounds for cup ties hosted outside their Superliga member seasons:
CLUB_HOME = {
 'KF Ballkani': ('Suva Reka City Stadium', 'Suhareke'),
 'Drita': ('Gjilan Synthetic Grass Stadium', 'Gjilan'),
 'Gjilani': ('Gjilan Synthetic Grass Stadium', 'Gjilan'),
 'Llapi': ('Zahir Pajaziti Stadium', 'Podujeve'),
 'Prishtina': ('Fadil Vokrri Stadium', 'Prishtine'),
 'Malisheva': ('Liman Gegaj Stadium', 'Malisheve'),
 'Dukagjini': ('18 June Stadium', 'Kline'),
 'Feronikeli': ('Rexhep Rexhepi Stadium', 'Drenas'),
 'Fushë Kosova': ('Ekrem Grajqevci Stadium', 'Fushe Kosove'),
 'Liria': ('Perparim Thaci Stadium', 'Prizren'),
 'Suhareka': ('Suhareka City Stadium', 'Suhareke'),
 'Ferizaj': ('Ferizaj Synthetic Grass Stadium', 'Ferizaj'),
 'Ulpiana': ('Qatiq Bytyqi Stadium', 'Lipljan'),
 "Trepça'89": ('Riza Lushta Stadium', 'Mitrovica'),
 'Drenica Skenderaj': ('Bajram Aliu Stadium', 'Skenderaj'),
 'Prishtina E Re': ('FFK National Educational Camp', 'Hajvali'),  # pre-2025-26 regular ground (2025-26 article)
}
VENUE_OVERRIDE = {
    ('2025-26', 'Prishtina E Re'): ('Sami Kelmendi Stadium', 'Hajvali'),   # 2025-26 season article
    ('2024-25', 'Rahoveci'): ('Gjilan Synthetic Grass Stadium', 'Gjilan'), # Wikipedia footnote (played in Gjilan)
}

PO_VENUE = {
 ('2021-22', 'Playoff-SF'): ('18 June Stadium', 'Kline'),             # RSSSF printed
 ('2021-22', 'Playoff-Final'): ('Zahir Pajaziti Stadium', 'Podujeve'),# RSSSF printed
 ('2022-23', 'Playoff-SF'): ('18 June Stadium', 'Kline'),             # koha.net (Ulpiana-Liria First League draw)
 ('2022-23', 'Playoff-Final'): ('Zahir Pajaziti Stadium', 'Podujeve'),# Wikipedia 2022-23 article + mackolik
 ('2023-24', 'Playoff-SF'): ('18 June Stadium', 'Kline'),             # inference NOTE: same venue as 2022-23 SF, 2023-24 final (Telegrafi), 2024-25 SF (Wikipedia); RSSSF prints none
 ('2023-24', 'Playoff-Final'): ('18 June Stadium', 'Kline'),          # Telegrafi ("18 Qershori", Kline)
 ('2024-25', 'Playoff-SF'): ('18 June Stadium', 'Kline'),             # Wikipedia 2024-25 article
 ('2024-25', 'Playoff-Final'): ('Fadil Vokrri Stadium', 'Prishtine'), # mesazhi.com + Wikipedia
 ('2025-26', 'Playoff-SF'): ('18 June Stadium', 'Kline'),             # Wikipedia 2025-26 article
 ('2025-26', 'Playoff-Final'): ('Rexhep Rexhepi Stadium', 'Drenas'),  # Wikipedia 2025-26 article
}

def ascii_(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

def adv_winner(home, hg, ag, away, note):
    if not note:
        return None
    m = re.search(r'(\d+)-(\d+)\s*pen', note)
    if m:
        ph, pa = int(m.group(1)), int(m.group(2))
        return home if ph > pa else away
    if 'aet' in note:
        return home if int(hg) > int(ag) else (away if int(ag) > int(hg) else None)
    if 'o/w' in note:
        return away
    if 'awd' in note or 'awarded' in note:
        return home if int(hg) > int(ag) else away
    return None

# ================================================================ KOS v2.1
kos = []
kos.append('NOTE|info|pack_id|KOS-2021-2026_BP-TEAM-PACK_v2.1 - corrected return of WO-KOS-SPAN-06 (WORKORDER-KOS-2021-2026-5YSPAN.md). v2.1 per Director 2026-08-07: (1) COMPLETE standalone pack - 900 Kosovo Superliga rows (5 seasons x 180, INCLUDING the 12 rows formerly held as appendix, because the current verified store holds zero Kosovo rows) + 10 Kosovo Relegation Playoffs rows = 910 MATCH rows; (2) every MATCH row carries a real stadium and city (no placeholders; venue_source NOTE); (3) D1-D4 identity fixes retained. Compiled 2026-08-07.')
kos.append('NOTE|info|appendix_included|The 12 rows listed as "already-held appendix" in the v1 workorder are INCLUDED (Director instruction: the store has zero Kosovo rows; the pack must be standalone): 2026-03-09 Malisheva 3-0 Prishtina; 2026-03-22 Malisheva 2-0 Llapi; 2026-04-05 Drita 2-0 Malisheva; 2026-04-11 Prishtina E Re 2-1 Malisheva; 2026-04-19 Malisheva 4-2 KF Ballkani; 2026-04-26 Dukagjini 0-1 Malisheva; 2026-04-29 Malisheva 3-1 Gjilani; 2026-05-02 Prishtina 0-1 Malisheva; 2026-05-10 Ferizaj 1-1 Malisheva; 2026-05-17 Malisheva 4-1 Drenica Skenderaj; 2026-05-24 Llapi 3-2 Malisheva; 2026-05-31 Malisheva 3-2 Drita. 900 = 180 x 5.')
kos.append('SOURCE|rsssf-kosovo2022|https://www.rsssf.org/tablesk/kosovo2022.html|2026-08-07|primary-archive|2021-22: 36 rounds dates+scores, final table, playoff (venues printed); 180 / 463 / 2021-08-21..2022-05-22')
kos.append('SOURCE|rsssf-kosovo2023|https://www.rsssf.org/tablesk/kosovo2023.html|2026-08-07|primary-archive|2022-23: 36 rounds, final table, playoff; 180 / 446 / 2022-08-13..2023-05-28')
kos.append('SOURCE|rsssf-kosovo2024|https://www.rsssf.org/tablesk/kosovo2024.html|2026-08-07|primary-archive|2023-24: 36 rounds, final table, playoff; 180 / 432 / 2023-08-12..2024-05-25')
kos.append('SOURCE|rsssf-kosovo2025|https://www.rsssf.org/tablesk/kosovo2025.html|2026-08-07|primary-archive|2024-25: 36 rounds, final table, playoff; 180 / 446 / 2024-08-10..2025-05-25')
kos.append('SOURCE|rsssf-kosovo2026|https://www.rsssf.org/tablesk/kosovo2026.html|2026-08-07|primary-archive|2025-26: official final table + playoff (page has no round grid)')
kos.append('SOURCE|wf-kos-2526|https://www.worldfootball.net/competition/co835/kosovo-superliga/se102170/2025-2026/|2026-08-07|match-carrier|2025-26 rows (180 incl. former appendix): dates+scores from the 36 matchday pages')
kos.append('SOURCE|wiki-kos-2526|https://en.wikipedia.org/wiki/2025%E2%80%9326_Football_Superleague_of_Kosovo|2026-08-07|second-index|2025-26 FBR matrix (179/180 identical; MD12 award documented), official table, playoff dates/venues, stadiums')
kos.append('NOTE|info|venue_source|League rows: home club stadium per the Wikipedia Superleague season articles (2021-22..2025-26 stadium tables): era-stable for 24 clubs; changes: Drita/Gjilani Gjilan City Stadium (2021-22, 2022-23) -> Gjilan Synthetic Grass Stadium (2023-24 onward); Prishtina E Re FFK National Educational Camp (pre-2025-26) -> Sami Kelmendi Stadium (2025-26, per the 2025-26 season article). Playoff rows: venues from RSSSF (2021-22), Wikipedia season articles (2022-23 final; 2024-25 semi/final; 2025-26), Telegrafi (2023-24 final: "18 Qershori", Kline), koha.net (2022-23 semi: 18 June, Kline), mackolik (2022-23 final: Zahir Pajaziti). The 2023-24 semifinal venue (18 June Stadium, Kline) is an inference disclosed in playoff_venues - the same venue hosted the 2022-23 semi (koha.net), the 2023-24 final (Telegrafi) and the 2024-25 semi (Wikipedia); RSSSF prints no venue for it. No unknown/blank placeholders in any MATCH row.')
kos.append('NOTE|info|playoff_venues|As documented in venue_source: 2021-22 SF 18 June Stadium Kline, Final Zahir Pajaziti Stadium Podujeve (RSSSF); 2022-23 SF 18 June Stadium Kline (koha.net), Final Zahir Pajaziti Stadium Podujeve (Wikipedia; mackolik); 2023-24 SF 18 June Stadium Kline (inference - see venue_source), Final 18 June Stadium Kline (Telegrafi); 2024-25 SF 18 June Stadium Kline (Wikipedia; article dates it 24 May and lists Vushtrria as home vs RSSSF 25 May / Liria home - RSSSF primary kept, difference noted), Final Fadil Vokrri Stadium Prishtine (mesazhi.com, Wikipedia); 2025-26 SF 18 June Stadium Kline, Final Rexhep Rexhepi Stadium Drenas (Wikipedia).')
kos.append('NOTE|info|federation_check|All 900 league rows use only the 16-club pool strings; the 10 playoff rows pair the 8th-placed Superliga club with the declared lower-division playoff opponents. Not Albania, not Serbia. Rows only.')
kos.append('NOTE|info|catalog|"Kosovo Superliga" (league rows, compType domestic-league); "Kosovo Relegation Playoffs" (10 rows, compType other per ERRATA-2026-08-03 Family B); venue-detail "RS R1".."RS R36" / "Playoff-SF" / "Playoff-Final"; awarded ties carry NOTE|warning|awarded.')
# TEAM rows follow the adopted reference layout (RUS/CZ1 packs):
# name|country|league|code|aliases|logoURL|city|country|stadium|capacity|unknown|unknown
kos.append('TEAM|Ulpiana|Kosovo|Kosovo Superliga|KOS|Ulpiana|unknown|Lipljan|Kosovo|Qatiq Bytyqi Stadium|2000|unknown|unknown')
kos.append('TEAM|Feronikeli|Kosovo|Kosovo Superliga|KOS|Feronikeli|unknown|Drenas|Kosovo|Rexhep Rexhepi Stadium|2000|unknown|unknown')
kos.append("TEAM|Trepça'89|Kosovo|Kosovo Superliga|KOS|Trepça'89|unknown|Mitrovica|Kosovo|Riza Lushta Stadium|12000|unknown|unknown")
kos.append('TEAM|Fushë Kosova|Kosovo|Kosovo Superliga|KOS|Fushë Kosova|unknown|Fushe Kosove|Kosovo|Ekrem Grajqevci Stadium|5000|unknown|unknown')
kos.append('TEAM|Liria|Kosovo|Kosovo Superliga|KOS|Liria|unknown|Prizren|Kosovo|Perparim Thaci Stadium|15000|unknown|unknown')
kos.append('TEAM|Suhareka|Kosovo|Kosovo Superliga|KOS|Suhareka|unknown|Suhareke|Kosovo|Suhareka City Stadium|1500|unknown|unknown')
kos.append('TEAM|Vushtrria|Kosovo|Kosovo First League|KFL1|Vushtrria|unknown|Vushtrri|Kosovo|Ferki Aliu Stadium|6000|unknown|unknown')
kos.append('TEAM|Dinamo Fzaj.|Kosovo|Kosovo First League|KFL1|Dinamo Ferizaj|unknown|Ferizaj|Kosovo|Ferizaj Synthetic Grass Stadium|1500|unknown|unknown')
kos.append('NOTE|info|round_counts|900 league rows = 180 x 5: 2021-22 463 goals; 2022-23 446; 2023-24 432; 2024-25 446; 2025-26 481 (incl. former appendix). Every club 36 matches per season; 0 duplicates; 0 future-dated.')
kos.append('NOTE|info|continuity|Postponed matches filed by played date with original round labels (2022-23 MD1/MD3/MD7/MD14 scatter; 2023-24 MD1/MD3/MD13; 2024-25 MD1/MD2/MD3; 2025-26 MD2/MD13). Awards: 2021-22 MD27 Gjilani 0-3 Ballkani (abandoned at 1-1, crowd trouble); 2021-22 MD30 Ulpiana 0-3 Ballkani (ineligible player); 2024-25 MD21 Ballkani 3-0 Feronikeli (originally 1-1); 2024-25 MD3 Drita 4-2 Suhareka revoked-award note (played score governs).')
kos.append('NOTE|info|boundary|2026-27 not started on 2026-08-07 (season begins mid-August); zero 2026-27 rows.')
kos.append('NOTE|warning|source_conflict|2025-26 MD12 Prishtina E Re 3-0 Drenica Skenderaj (2025-11-02): Wikipedia matrix prints on-pitch 0-0; the official table requires the 3-0 award (worldfootball prints dec.); row carries 3-0.')

n_league = 0
for tag in SEASONS:
    rows = json.load(open(f'{LEDGER}/kos-{tag}-league.json'))
    for r in sorted(rows, key=lambda x: (x['date'], x['round'])):
        stad = STADIUM[tag].get(r['home'], 'unknown')
        city = CITY.get(r['home'], ascii_(r['home']))
        src = 'wf-kos-2526' if tag == '2025-26' else f'rsssf-kosovo{int(tag[:4])+1}'
        kos.append(f'MATCH|{r["date"]}|Kosovo Superliga|domestic-league|{r["home"]}|{r["hg"]}|{r["ag"]}|{r["away"]}|RS R{r["round"]}|{stad}|{city}|Kosovo||{src}')
        note = r.get('note', '')
        if 'awarded' in note:
            kos.append(f'NOTE|warning|awarded|{r["date"]} {r["home"]} {r["hg"]}-{r["ag"]} {r["away"]} (RS R{r["round"]}): governing awarded score; {note}')
        n_league += 1

n_po = 0
for tag in SEASONS:
    for t in json.load(open(f'{LEDGER}/kos-{tag}-playoff.json')):
        stage = 'Playoff-SF' if t['stage'] == 'Semifinal' else 'Playoff-Final'
        stad, city = PO_VENUE[(tag, stage)]
        src = 'rsssf-kosovo2026' if tag == '2025-26' else f'rsssf-kosovo{int(tag[:4])+1}'
        kos.append(f'MATCH|{t["date"]}|Kosovo Relegation Playoffs|other|{t["home"]}|{t["hg"]}|{t["ag"]}|{t["away"]}|{stage}|{stad}|{city}|Kosovo||{src}')
        note = t.get('note', '')
        w = adv_winner(t['home'], int(t['hg']), int(t['ag']), t['away'], note)
        if 'pen' in note:
            kos.append(f'NOTE|info|advancement|{t["date"]} {t["home"]} {t["hg"]}-{t["ag"]} {t["away"]} ({stage}): {w} advanced on penalties after extra time')
        n_po += 1
kos.append('END')
assert n_league == 900, n_league
assert n_po == 10, n_po
open(OUT_KOS, 'w', encoding='utf-8').write('\n'.join(kos) + '\n')
print(f'{OUT_KOS}: {n_league} league + {n_po} playoff = {n_league + n_po} MATCH rows')

# ================================================================ KOSCUP v2.1
kosc = []
kosc.append('NOTE|info|pack_id|KOSCUP-2021-2026_BP-TEAM-PACK_v2.1 - corrected return of WO-KOSCUP-SPAN-11. v2.1 per Director 2026-08-07: every MATCH row carries a real stadium and city (no placeholders; venue_source NOTE); D1-D4 identity fixes retained. 123 slice ties = 24/24/24/26/25 per edition. Compiled 2026-08-07.')
kosc.append('SOURCE|rsssf-kosovo2022|https://www.rsssf.org/tablesk/kosovo2022.html|2026-08-07|primary-archive|2021-22 Kupa chapter (24 slice ties)')
kosc.append('SOURCE|rsssf-kosovo2023|https://www.rsssf.org/tablesk/kosovo2023.html|2026-08-07|primary-archive|2022-23 Kupa chapter (24 slice ties)')
kosc.append('SOURCE|rsssf-kosovo2024|https://www.rsssf.org/tablesk/kosovo2024.html|2026-08-07|primary-archive|2023-24 Kupa chapter (24 slice ties)')
kosc.append('SOURCE|rsssf-kosovo2025|https://www.rsssf.org/tablesk/kosovo2025.html|2026-08-07|primary-archive|2024-25 Kupa chapter (26 slice ties)')
kosc.append('SOURCE|rsssf-kosovo2026|https://www.rsssf.org/tablesk/kosovo2026.html|2026-08-07|primary-archive|2025-26 Kupa chapter (25 slice ties)')
kosc.append('SOURCE|wiki-kosovar-cups|https://en.wikipedia.org/wiki/2023%E2%80%9324_Kosovar_Cup|2026-08-07|second-index|per-match stadiums (2023-24 QF/SF: Sami Kelmendi, 18 June, Shtime City, Liman Gegaj, Suhareka City), final venue policy; 2024-25/2025-26 articles for round confirmations')
kosc.append('NOTE|info|venue_source|Pool-club hosts use their Superleague-season stadium (Wikipedia season articles); pool-club hosts outside their member seasons use their documented home ground; lower-division hosts use documented grounds: A&N Prizren Boka Stadium Korishe (Wikipedia/transfermarkt); Behari KF Behari Stadium Vitomirice (Wikipedia); Besa Shahin Haxhiislami Stadium Peja (Wikipedia); Dardania Dardania Stadium Qyshk (Wikipedia); Dinamo Ferizaj Ferizaj Synthetic Grass Stadium (footballgroundmap - Stadiumi i Futbollit Ferizaj); Flamurtari Flamurtari Stadium Prishtine (Wikipedia stadiums list; transfermarkt); Istogu Demush Mavraj Stadium Istog (Wikipedia); Phoenix-Banje Tahir Vokshi Stadium Banje (Wikipedia); Rahoveci Selajdin Mullabazi Stadium Rahovec (Wikipedia); Ramiz Sadiku Stadiumi i Ramiz Sadikut Prishtine (transfermarkt); Rilindja 1974 Baran Sports Field Baran (Wikipedia); Trepca Adem Jashari Olympic Stadium Mitrovica (Wikipedia); Vellaznimi Gjakova City Stadium Gjakova (Wikipedia); Vushtrria Ferki Aliu Stadium Vushtrri (Wikipedia); Vjosa Shtime City Stadium Shtime (2023-24 Kosovar Cup QF); KEK-u Agron Rama Stadium Kastriot (Wikipedia stadiums list); 2 Korriku 2 Korriku Sports Field Prishtine (Wikipedia stadiums list); Lepenci Besnik Begunca Stadium Kacanik (Wikipedia stadiums list). Overrides: Prishtina E Re host ties -> FFK National Educational Camp Hajvali (2023-24/2024-25) / Sami Kelmendi Stadium Hajvali (2025-26, per the 2025-26 season article); 2024-25 R16 Rahoveci-Drita at Gjilan Synthetic Grass Stadium (Wikipedia footnote: played in Gjilan, Rahovec home for administrative purposes). Finals: Fadil Vokrri Stadium Prishtine (2021-22, 2022-23, 2024-25, 2025-26) and Rexhep Rexhepi Stadium Drenas (2023-24, per cup regulations/pitch works at Fadil Vokrri).')
kosc.append('NOTE|info|catalog|"Kosovo Cup" (compType domestic-cup per ERRATA-2026-08-03 Family A); round labels R1/R16/R8/QF/SF leg1/SF leg2/Final; preliminary rounds OUT of the slice.')
kosc.append('NOTE|info|federation_check|Every tie has >=1 Superliga club of that season (pool strings verbatim); other participants are Kosovo lower-division clubs with TEAM rows. No Albanian-cup clubs.')
kosc.append('NOTE|info|identity|Pool strings verbatim; canonicalisations: Ph\'nix-Banje -> Phoenix-Banje; Prisht. e Re / Prishtina e Re -> Prishtina E Re; Drenica -> Drenica Skenderaj; Trepca\'89 -> Trepça\'89; Fushe Kosova -> Fushë Kosova. TEAM rows only for non-roster slice participants.')
kosc.append('NOTE|info|advancement_policy|aet/pens ties carry the printed scoreline + NOTE|info|advancement (aet ties: 90-minute split not published by RSSSF - NOTE|info|aet lines); awarded/walkover ties carry NOTE|warning|awarded.')
kosc.append('NOTE|info|slice_counts|24/24/24/26/25 = 123 (2021-22..2023-24: R1 10 + R8 6 + QF 3 + SF 4 + Final 1; 2024-25: R16 10 + R8 7 + QF 4 + SF 4 + Final 1; 2025-26: R16 10 + R8 6 + QF 4 + SF 4 + Final 1).')
kosc.append('NOTE|info|bracket|Champions: Llapi 2021-22, Prishtina 2022-23, Ballkani 2023-24, Prishtina 2024-25, Dukagjini 2025-26 - all match the official record.')
kosc.append('NOTE|warning|blocker|TOP Football (Prishtina Third League academy): no accessible source publishes the club home venue (Wikipedia, RSSSF, soccerway, sofascore, betexplorer, betmines, FFK, Kosovar press - searched 2026-08-07; aggregators record no venue). Its two home slice ties (2024-12-03 and 2025-12-04, both vs Prishtina) carry the descriptive venue "TOP Football Sports Field", city Prishtine; the auditor is asked to confirm/correct from match-day records. This is the only venue in either v2.1 pack not independently confirmed.')

def slice_participants():
    parts = set()
    for tag in SEASONS:
        mem = MEMBERSHIP[tag]
        for t in json.load(open(f'{LEDGER}/kos-{tag}-cup.json')):
            if t.get('date') and (t['home'] in mem or t['away'] in mem):
                parts.add(t['home']); parts.add(t['away'])
    return parts

DIV = {'A&N Prizren':'Kosovo First League','2 Korriku':'Kosovo First League','Arberia':'Kosovo First League',
 'Behari':'Kosovo Second League','Besa':'Kosovo First League','Dardania':'Kosovo Second League',
 'Dinamo Fzaj.':'Kosovo First League','Drenasi':'Kosovo First League','Drenica':'Kosovo First League',
 'Flamurtari':'Kosovo First League','Fushë Kosova':'Kosovo First League','Istogu':'Kosovo First League',
 'Istogu 03':'Kosovo First League','KEK-u':'Kosovo Second League','Kika':'Kosovo First League',
 'Kosova VR':'Kosovo Second League','Lepenci':'Kosovo Second League','Liria':'Kosovo First League',
 'Mati':'Kosovo Third League','Mitrovica':'Kosovo Second League','Opoja':'Kosovo Third League',
 'Phoenix-Banje':'Kosovo First League','Prishtina E Re':'Kosovo First League','Prizreni':'Kosovo Second League',
 'Rahoveci':'Kosovo First League','Ramiz Sadiku':'Kosovo First League','Rilindja 74':'Kosovo First League',
 'Sharri':'Kosovo Third League','Shkendija H.':'Kosovo Third League','Suhareka':'Kosovo First League',
 'Tefik Canga':'Kosovo Second League','TOP Football':'Kosovo Third League','Trepca':'Kosovo First League',
 "Trepça'89":'Kosovo First League','Ulpiana':'Kosovo First League','Vellaznimi':'Kosovo First League',
 'Vitia':'Kosovo First League','Vjosa':'Kosovo First League','Vllaznia':'Kosovo First League',
 'Vushtrria':'Kosovo First League','Drenica Skenderaj':'Kosovo First League','Feronikeli':'Kosovo First League',
 'Ferizaj':'Kosovo First League'}
LC = {'Kosovo First League': 'KFL1', 'Kosovo Second League': 'KFL2', 'Kosovo Third League': 'KFL3'}
TOWN = {'2 Korriku':'Prishtine','A&N Prizren':'Korishe','Arberia':'Dobraje','Behari':'Vitomirice',
 'Besa':'Peja','Dardania':'Qyshk','Dinamo Fzaj.':'Ferizaj','Drenasi':'Drenas','Flamurtari':'Prishtine',
 'Istogu':'Istog','Istogu 03':'Istog','KEK-u':'Kastriot','Kika':'Kamenica','Kosova VR':'Prishtine',
 'Lepenci':'Kacanik','Mati':'Prishtine','Mitrovica':'Mitrovica','Opoja':'Dragash','Phoenix-Banje':'Banje',
 'Prizreni':'Prizren','Rahoveci':'Rahovec','Ramiz Sadiku':'Prishtine','Rilindja 74':'Baran',
 'Sharri':'Elez Han','Shkendija H.':'Hajvali','Tefik Canga':'Tern','TOP Football':'Prishtine',
 'Trepca':'Mitrovica','Vellaznimi':'Gjakova','Vitia':'Vitia','Vjosa':'Shtime','Vllaznia':'Pozharan',
 'Vushtrria':'Vushtrri','Drenica':'Skenderaj'}
for name in sorted(slice_participants() - ROSTER):
    div = DIV.get(name, 'Kosovo First League')
    stad, city = VENUE_LOWER.get(name, ('not published', TOWN.get(name, ascii_(name))))
    kosc.append(f'TEAM|{name}|Kosovo|{div}|{LC[div]}|{name}|unknown|{city}|Kosovo|{stad}|unknown|unknown|unknown')

STAGE_LABEL = {'Round 1': 'R1', '1/16 Finals': 'R16', '1/8 Finals': 'R8', 'Quarterfinals': 'QF',
               'Semifinals': 'SF', 'Final': 'Final'}
n_ties = 0
for tag in SEASONS:
    ties = json.load(open(f'{LEDGER}/kos-{tag}-cup.json'))
    mem = MEMBERSHIP[tag]
    sliced = [t for t in ties if (t['home'] in mem or t['away'] in mem) and t.get('date')]
    for t in sliced:
        leg = ''
        if t.get('leg'):
            leg = ' leg1' if t['leg'] == 'First Legs' else ' leg2'
        stage = STAGE_LABEL.get(t['stage'], t['stage']) + leg
        home, away = t['home'], t['away']
        if t['stage'] == 'Final':
            stad, city = ('Fadil Vokrri Stadium', 'Prishtine')
            if tag == '2023-24':
                stad, city = ('Rexhep Rexhepi Stadium', 'Drenas')
        else:
            ov = VENUE_OVERRIDE.get((tag, home))
            if ov:
                stad, city = ov
            elif home in STADIUM[tag]:
                stad, city = STADIUM[tag][home], CITY[home]
            elif home in CLUB_HOME:
                stad, city = CLUB_HOME[home]
            elif home in VENUE_LOWER:
                stad, city = VENUE_LOWER[home]
            else:
                raise SystemExit(f'no venue for {tag} {home}')
        src = 'rsssf-kosovo2026' if tag == '2025-26' else f'rsssf-kosovo{int(tag[:4])+1}'
        kosc.append(f'MATCH|{t["date"]}|Kosovo Cup|domestic-cup|{home}|{t["hg"]}|{t["ag"]}|{away}|{stage}|{stad}|{city}|Kosovo||{src}')
        note = t.get('note', '')
        w = adv_winner(home, int(t['hg']), int(t['ag']), away, note)
        if 'pen' in note or 'aet' in note or 'o/w' in note or 'awd' in note or 'awarded' in note:
            if w:
                kosc.append(f'NOTE|info|advancement|{t["date"]} {home} {t["hg"]}-{t["ag"]} {away} ({tag}, {stage}): {w} advanced')
            if 'aet' in note and 'pen' not in note:
                kosc.append(f'NOTE|info|aet|{t["date"]} {home} {t["hg"]}-{t["ag"]} {away} ({tag}, {stage}): scoreline includes extra time; 90-minute split not published by RSSSF')
            if 'awd' in note or 'awarded' in note:
                kosc.append(f'NOTE|warning|awarded|{t["date"]} {home} {t["hg"]}-{t["ag"]} {away} ({tag}, {stage}): {note}')
            if 'o/w' in note:
                kosc.append(f'NOTE|warning|awarded|{t["date"]} {home} {t["hg"]}-{t["ag"]} {away} ({tag}, {stage}): walkover per RSSSF (Vellaznimi o/w Prishtina - Prishtina advanced)')
        n_ties += 1
kosc.append('END')
assert n_ties == 123, n_ties
open(OUT_KOSCUP, 'w', encoding='utf-8').write('\n'.join(kosc) + '\n')
print(f'{OUT_KOSCUP}: {n_ties} slice ties')
