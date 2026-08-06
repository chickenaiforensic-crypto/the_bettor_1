#!/usr/bin/env python3
"""SPA venues ledger emitter (WO-SPA-SPAN-13).
Parses the 4 scoped venue archives + 2025-26 article archive -> audit/ledger/spa-venues.txt.
Gates: 103 rows (20x4 historical + 23 for 2025-26: 18 singles + Barcelona x3 + Vallecano x2),
pins subset of the 26-string roster, per-season membership complete, row arity 7.
Run: python3 tools/emit_spa_venues.py
"""
import re, unicodedata, sys

def asc(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()

PIN = {'Alavés':'Alaves','Almería':'Almeria','Athletic Bilbao':'Ath Bilbao','Atlético Madrid':'Ath Madrid',
 'Barcelona':'Barcelona','Cádiz':'Cadiz','Celta Vigo':'Celta','Elche':'Elche','Espanyol':'Espanol',
 'Getafe':'Getafe','Girona':'Girona','Granada':'Granada','Las Palmas':'Las Palmas','Leganés':'Leganes',
 'Levante':'Levante','Mallorca':'Mallorca','Osasuna':'Osasuna','Oviedo':'Oviedo','Rayo Vallecano':'Vallecano',
 'Real Betis':'Betis','Real Madrid':'Real Madrid','Real Sociedad':'Sociedad','Sevilla':'Sevilla',
 'Valencia':'Valencia','Valladolid':'Valladolid','Villarreal':'Villarreal'}
ROSTER = set('Alaves Almeria Ath Bilbao Ath Madrid Barcelona Betis Cadiz Celta Elche Espanol Getafe Girona '
 'Granada Las Palmas Leganes Levante Mallorca Osasuna Oviedo Real Madrid Sevilla Sociedad Valencia '
 'Valladolid Vallecano Villarreal'.split('\n')[0].replace('  ',' ').split(' ')[:0] or [])
# build roster properly (two-word pins)
ROSTER = {'Alaves','Almeria','Ath Bilbao','Ath Madrid','Barcelona','Betis','Cadiz','Celta','Elche','Espanol',
 'Getafe','Girona','Granada','Las Palmas','Leganes','Levante','Mallorca','Osasuna','Oviedo','Real Madrid',
 'Sevilla','Sociedad','Valencia','Valladolid','Vallecano','Villarreal'}

def parse_season(path):
    body = open(path, encoding='utf-8').read()
    i = body.index('===Stadiums and locations===')
    k = body.index('\\|}\n', i)
    t = body[i:k].replace('\\|','|').replace('\\[','[').replace('\\]',']').replace('\\_','_')
    wt = t[t.index('{| class'):]
    parsed = []
    for r in re.split(r'\|-\n', wt):
        if '{{nts|' not in r.lower(): continue
        cap = re.search(r'\{\{[Nn]ts\|([\d, ]+)\}\}', r).group(1)
        links = re.findall(r'\[\[(?:[^\[\]|]+\|)?([^\[\]]+)\]\]', r)
        links = [l.strip() for l in links if 'http' not in l and 'archive' not in l]
        loc = ' '.join(links[1:-1]) if len(links) > 2 else links[1]
        parsed.append([links[0], loc, links[-1], cap.replace(' ', '').replace(',', '')])
    return parsed

D = {s: parse_season(f'data/raw/wiki-es-{y}-venues-raw.txt')
     for s, y in [('2021-22','2122'),('2022-23','2223'),('2023-24','2324'),('2024-25','2425')]}
for s in D: assert len(D[s]) == 20, s

# 2025-26 (rowspan table in the full article archive); each row token-verified against raw
# 23 rows = 18 single-ground teams + Barcelona x3 + Vallecano x2 (upstream capacity cells)
body = open('data/raw/wiki-es-2526-article-raw.txt', encoding='utf-8').read()
D['2025-26'] = [
 ['Alavés','Vitoria-Gasteiz','Campo de Fútbol de Mendizorrotza','19840'],
 ['Athletic Bilbao','Bilbao','Estadio San Mamés','53289'],
 ['Atlético Madrid','Madrid','Estadio Riyadh Air Metropolitano','70692'],
 ['Barcelona','Sant Joan Despí','Estadi Johan Cruyff','6000'],
 ['Barcelona','Barcelona','Olímpic Lluís Companys','55926'],
 ['Barcelona','Barcelona','Camp Nou','105000'],
 ['Celta Vigo','Vigo','Estadio ABANCA Balaídos','24870'],
 ['Elche','Elche','Estadio Martínez Valero','31388'],
 ['Espanyol','Cornellà de Llobregat','RCDE Stadium','37776'],
 ['Getafe','Getafe','Estadio Coliseum','16500'],
 ['Girona','Girona','Estadio Municipal de Montilivi','14624'],
 ['Levante','Valencia','Estadio Ciutat de València','26354'],
 ['Mallorca','Palma','Estadi Mallorca Son Moix','23142'],
 ['Osasuna','Pamplona','Estadio El Sadar','23576'],
 ['Oviedo','Oviedo','Estadio Carlos Tartiere','30500'],
 ['Rayo Vallecano','Madrid','El Campo de Fútbol de Vallecas','14708'],
 ['Rayo Vallecano','Leganés','Estadio Ontime Butarque','12450'],
 ['Real Betis','Seville','Estadio Olímpico de la Cartuja','70000'],
 ['Real Madrid','Madrid','Bernabéu','83186'],
 ['Real Sociedad','San Sebastián','Reale Arena','39313'],
 ['Sevilla','Seville','Estadio Ramón Sánchez-Pizjuán','43883'],
 ['Valencia','Valencia','Camp de Mestalla','49430'],
 ['Villarreal','Villarreal','Estadio de la Cerámica','23008'],
]
tt = body.replace('\\|','|').replace('\\[','[').replace('\\]',']')
for team, loc, stad, cap in D['2025-26']:
    probe = {'Camp Nou':'Spotify Camp Nou','Estadi Johan Cruyff':'Estadi Johan Cruyff'}.get(stad, stad)
    assert probe in tt, (team, stad)
    assert cap in tt.replace(',', '') or '{:,}'.format(int(cap)) in tt, (team, cap)

SEQ = {
 '2021-22':['Alaves','Ath Bilbao','Ath Madrid','Barcelona','Cadiz','Celta','Elche','Espanol','Getafe',
   'Granada','Levante','Mallorca','Osasuna','Vallecano','Betis','Real Madrid','Sociedad','Sevilla','Valencia','Villarreal'],
 '2022-23':['Almeria','Ath Bilbao','Ath Madrid','Barcelona','Cadiz','Celta','Elche','Espanol','Getafe',
   'Girona','Mallorca','Osasuna','Vallecano','Betis','Real Madrid','Sociedad','Sevilla','Valencia','Valladolid','Villarreal'],
 '2023-24':['Alaves','Almeria','Ath Bilbao','Ath Madrid','Barcelona','Cadiz','Celta','Getafe','Girona',
   'Granada','Las Palmas','Mallorca','Osasuna','Vallecano','Betis','Real Madrid','Sociedad','Sevilla','Valencia','Villarreal'],
 '2024-25':['Alaves','Ath Bilbao','Ath Madrid','Barcelona','Celta','Espanol','Getafe','Girona','Las Palmas',
   'Leganes','Mallorca','Osasuna','Vallecano','Betis','Real Madrid','Sociedad','Sevilla','Valencia','Valladolid','Villarreal'],
 '2025-26':['Alaves','Ath Bilbao','Ath Madrid','Barcelona','Barcelona','Barcelona','Celta','Elche','Espanol',
   'Getafe','Girona','Levante','Mallorca','Osasuna','Oviedo','Vallecano','Vallecano','Betis','Real Madrid',
   'Sociedad','Sevilla','Valencia','Villarreal'],
}
NOTES = {
 ('2021-22','Ath Madrid'):"print 'Wanda Metropolitano' 68,456 (epoch: Wanda -> Civitas 22-23 -> Riyadh Air 25-26)",
 ('2021-22','Barcelona'):"print 'Camp Nou' 99,354 (pre-renovation)",
 ('2021-22','Cadiz'):"print 'Nuevo Mirandilla' 20,724",
 ('2021-22','Celta'):"print 'Abanca-Balaidos' 29,000",
 ('2021-22','Espanol'):"city printed Barcelona (ground is in Cornella; re-printed 22-23)",
 ('2021-22','Getafe'):"print 'Coliseum Alfonso Perez' 17,393",
 ('2021-22','Levante'):"print 'Ciutat de Valencia' 26,354",
 ('2021-22','Mallorca'):"print 'Visit Mallorca Estadi' 24,262",
 ('2021-22','Vallecano'):"print 'Vallecas' 14,708",
 ('2021-22','Betis'):"home Benito Villamarin 60,721 (Cartuja epoch starts 25-26)",
 ('2021-22','Sociedad'):"print 'Anoeta' 39,500",
 ('2021-22','Villarreal'):"print 'Estadio de la Ceramica' 24,890",
 ('2022-23','Ath Madrid'):"renamed Civitas Metropolitano 68,456",
 ('2022-23','Barcelona'):"renamed Spotify Camp Nou 99,354",
 ('2022-23','Real Madrid'):"capacity re-counted 65,000 (renovation)",
 ('2022-23','Valencia'):"49,430 re-count (was 55,000)",
 ('2022-23','Elche'):"31,388 re-count", ('2022-23','Getafe'):"16,500 re-count",
 ('2022-23','Villarreal'):"23,008 re-count",
 ('2022-23','Mallorca'):"renamed Son Moix 23,142",
 ('2022-23','Sociedad'):"renamed Reale Arena (link Anoeta Stadium) 39,500",
 ('2022-23','Espanol'):"city now Cornella de Llobregat; 40,000",
 ('2023-24','Barcelona'):"MOVED to Montjuic (Estadi Olimpic Lluis Companys) 49,472 - Camp Nou renovation",
 ('2023-24','Ath Madrid'):"re-counted 70,460; district San Blas-Canillejas",
 ('2023-24','Real Madrid'):"re-counted 83,186; district Chamartin",
 ('2023-24','Almeria'):"18,331 re-count",
 ('2023-24','Getafe'):"label renamed Coliseum (link Estadio Coliseum)",
 ('2023-24','Granada'):"19,189 re-count",
 ('2023-24','Sevilla'):"label hyphenated Ramon Sanchez-Pizjuan",
 ('2023-24','Vallecano'):"district Puente de Vallecas",
 ('2023-24','Celta'):"label ABANCA Balaidos",
 ('2024-25','Barcelona'):"Montjuic re-counted 55,926",
 ('2024-25','Ath Madrid'):"label plain Metropolitano 70,460",
 ('2024-25','Real Madrid'):"re-counted 78,297 (was 83,186)",
 ('2024-25','Celta'):"label plain Balaidos; 24,870 re-count",
 ('2024-25','Espanol'):"42,260 re-count", ('2024-25','Girona'):"14,624 re-count",
 ('2024-25','Las Palmas'):"32,392 re-count",
 ('2024-25','Sociedad'):"label restored Anoeta 39,313",
 ('2024-25','Alaves'):"label print 'Mendizorrotza' (stadium-article spelling)",
 ('2024-25','Villarreal'):"label 'La Ceramica'",
 ('2024-25','Sevilla'):"city print 'Sevilla' (was 'Seville'); district Nervion",
 ('2024-25','Betis'):"district Bellavista-La Palmera; final season at Villamarin",
 ('2024-25','Valladolid'):"27,618 re-count; SOURCE-TOKEN upstream style attr typo verbatim",
 ('2025-26','Ath Madrid'):"renamed Estadio Riyadh Air Metropolitano 70,692",
 ('2025-26','Espanol'):"37,776 re-count (was 42,260)",
 ('2025-26','Real Madrid'):"label plain Bernabeu 83,186",
 ('2025-26','Celta'):"label Estadio ABANCA Balaidos",
 ('2025-26','Girona'):"SOURCE-TOKEN quadruple-open-bracket upstream typo before stadium link - verbatim",
 ('2025-26','Betis'):"MOVED to Estadio Olimpico de la Cartuja 70,000 (Villamarin renovation)",
 ('2025-26','Levante'):"promoted; Ciutat de Valencia 26,354",
 ('2025-26','Oviedo'):"promoted; Carlos Tartiere 30,500",
 ('2025-26','Alaves'):"label 'Campo de Futbol de Mendizorrotza'",
}
BARCA3 = {
 'Estadi Johan Cruyff':"three-ground 25-26 (rowspan=3): Sant Joan Despi block 6,000",
 'Olimpic Lluis Companys':"three-ground 25-26: Montjuic block 55,926",
 'Camp Nou':"three-ground 25-26: Camp Nou return, rebuilt print 105,000 (link Spotify Camp Nou)",
}
HDR = """# SPA VENUES 2021-22..2025-26 (WO-SPA-SPAN-13) - transcribed 2026-08-05 from the Wikipedia
# season articles' "Stadiums and locations" tables (action=raw wikitext, fetch_page;
# 2021-22/2022-23/2023-24/2024-25 scoped venue archives + the full 2025-26 season
# article archive). Independent of RSSSF fixtures = venue second index.
# VENUE|<season>|<roster-string>|<stadium-print ASCII-folded>|<city ASCII-folded>|<cap folded>|<notes>
# Roster pins: Atletico->Ath Madrid (never Atletico), Athletic->Ath Bilbao, Rayo->
# Vallecano (never Rayo), Real Sociedad->Sociedad, Real Betis->Betis, Espanyol->Espanol,
# Cadiz/Alaves/Almeria/Leganes ASCII-folded. City districts (San Blas-Canillejas,
# Chamartin, Puente de Vallecas, Bellavista-La Palmera, Nervion) carried in notes only.
# Epochs (era data): Atletico Wanda Metropolitano 21-22 -> Civitas Metropolitano 22-23/
# 23-24 -> Metropolitano 24-25 -> Estadio Riyadh Air Metropolitano 25-26. Barcelona Camp
# Nou/Spotify Camp Nou 21-23 -> Olimpic Lluis Companys (Montjuic) 23-25 -> THREE-GROUND
# 25-26 split (Johan Cruyff 6,000 / Olimpic Lluis Companys 55,926 / Camp Nou 105,000;
# rowspan=3 upstream). Betis Benito Villamarin 21-25 -> Estadio Olimpico de la Cartuja
# 25-26. Sociedad Anoeta -> Reale Arena 22-24 -> Anoeta 24-25 -> Reale Arena 25-26 print
# swings. Capacity re-count waves carried VERBATIM per season table.
# 2025-26 VALLECANO TWO-GROUND SPLIT (rowspan=2 upstream): home El Campo de Futbol de
# Vallecas 14,708 + Estadio Ontime Butarque (Leganes) 12,450 ONE-OFF - MD Vallecano
# 3-0 Ath Madrid 2026-02-15 moved for poor Vallecas pitch (AS-cited efn, 5,335 att =
# season lowest). 2026-27 boundary article lists Vallecano back at Vallecas.
# Row count: 103 = 20 x 4 historical seasons + 23 for 2025-26 (18 single-ground teams
# + Barcelona x3 + Vallecano x2 upstream capacity cells). NOTE: a pre-parse scratch count
# of 22 cells was corrected to 23 on full parse same-day (18+3+2 arithmetic slip)."""

rows = []
for season in ['2021-22','2022-23','2023-24','2024-25','2025-26']:
    for (team, loc, stad, cap), pin_expected in zip(D[season], SEQ[season]):
        pin = PIN[team]
        assert pin == pin_expected, (season, team, pin, pin_expected)
        city = re.sub(r'\s+(San Blas-Canillejas|Puente de Vallecas|Bellavista-La Palmera|Nervión|Nervion|\(Chamartín\)|Chamartín|Chamartin)$','',loc).replace('()','').strip()
        if season == '2025-26' and pin == 'Barcelona':
            note = BARCA3[asc(stad)]
        elif season == '2025-26' and pin == 'Vallecano' and 'Butarque' in stad:
            note = "ONE-OFF: MD26 Vallecano 3-0 Ath Madrid 2026-02-15 at Butarque (Leganes) - poor Vallecas pitch; AS-cited; 5,335 att"
        elif season == '2025-26' and pin == 'Vallecano':
            note = "home ground 14,708 (Butarque one-off = second row)"
        else:
            note = NOTES.get((season, pin), f"print '{asc(stad)}' {int(cap):,}")
        rows.append(f"VENUE|{season}|{pin}|{asc(stad)}|{asc(city)}|{cap}|{note}")
assert len(rows) == 103, len(rows)
assert {r.split('|')[2] for r in rows} <= ROSTER
for s in ['2021-22','2022-23','2023-24','2024-25']:
    assert sum(1 for r in rows if r.split('|')[1] == s) == 20
assert sum(1 for r in rows if r.split('|')[1] == '2025-26') == 23
assert all(len(r.split('|')) == 7 for r in rows)
open('audit/ledger/spa-venues.txt','w',encoding='utf-8').write(HDR + '\n' + '\n'.join(rows) + '\n')
print(f'audit/ledger/spa-venues.txt: {len(rows)} VENUE rows (20x4 + 23); pins OK; arity OK')
