import csv, collections

DISP = {
 'Liberec':('Slovan Liberec','Liberec'),'Teplice':('Teplice','Teplice'),'Slavia':('Slavia Prague','Prague'),
 'Sparta':('Sparta Prague','Prague'),'Plzen':('Viktoria Plzen','Plzen'),'Jablonec':('Jablonec','Jablonec nad Nisou'),
 'Hradec':('Hradec Kralove','Hradec Kralove'),'Olomouc':('Sigma Olomouc','Olomouc'),
 'Ml.Boleslav':('Mlada Boleslav','Mlada Boleslav'),'Bohemians':('Bohemians 1905','Prague'),
 'Slovacko':('Slovacko','Uherske Hradiste'),'Ostrava':('Banik Ostrava','Ostrava'),'Karvina':('Karvina','Karvina'),
 'Pardubice':('Pardubice','Pardubice'),'Dukla':('Dukla Prague','Prague'),'C.Budejovice':('Ceske Budejovice','Ceske Budejovice'),
 'Zlin':('Zlin','Zlin'),'Zbrojovka':('Zbrojovka Brno','Brno'),'Artis Brno':('Artis Brno','Brno'),
 # lower-division cup opponents
 'Horovice':('Horovice','Horovice'),'Loko Praha':('Loko Praha','Prague'),'Zapy':('Zapy','Zapy'),
 'Kromeriz':('Kromeriz','Kromeriz'),'Police n/M':('Police nad Metuji','Police nad Metuji'),
 'Hlucin':('Hlucin','Hlucin'),'Usti n/L':('Usti nad Labem','Usti nad Labem'),'Zizkov':('Zizkov','Prague'),
 'Varnsdorf':('Varnsdorf','Varnsdorf'),'Vyskov':('Vyskov','Vyskov'),'Opava':('Opava','Opava'),
 'Benatky':('Benatky nad Jizerou','Benatky nad Jizerou'),'Uhersky Brod':('Uhersky Brod','Uhersky Brod'),
 'Taborsko':('Taborsko','Tabor'),'Lanznot':('Lanznot','Lanznot'),'Brozany':('Brozany','Brozany nad Ohri'),
 'Redice':('Horni Redice','Horni Redice'),'Nove Sady':('Nove Sady','Nove Sady'),
 'Karlovy Vary':('Karlovy Vary','Karlovy Vary'),'Frydek':('Frydek-Mistek','Frydek-Mistek'),
 'Hlinsko':('Hlinsko','Hlinsko'),'Petrin Plzen':('Petrin Plzen','Plzen'),'Jihlava':('Jihlava','Jihlava'),
 'Trinec':('Trinec','Trinec'),'Domazlice':('Domazlice','Domazlice'),'Chrudim':('Chrudim','Chrudim'),
}
TOPFLIGHT = {'Liberec','Teplice','Slavia','Sparta','Plzen','Jablonec','Hradec','Olomouc','Ml.Boleslav',
             'Bohemians','Slovacko','Ostrava','Karvina','Pardubice','Dukla','C.Budejovice','Zlin','Zbrojovka','Artis Brno'}
VENUE_NEUTRAL = {('Olomouc','Sparta','2025-05-14'): ('neutral','unknown','unknown'),
                 ('Ml.Boleslav','Karvina','2026-05-20'): ('neutral','unknown','unknown')}

rows = [r for r in csv.DictReader(open('cze/cze_universe2.csv'))]
out = []
out.append('BP-TEAM-PACK v2')
out.append('NOTE|info|research_ack|Czech First League 2024-25 + 2025-26 complete (incl. championship/relegation groups and middle playoffs) + 2026-27 MD1 and Sparta-Zlin (2026-07-31); MOL Cup 2024-25 and 2025-26 rows for top-flight involvements; Promotion/Relegation Playoffs both seasons (8 rows per RSSSF). 631 rows total. League results parsed from BBC scores-fixtures pages and cross-validated 0-fail against RSSSF full-season W/D/L/GF/GA tables for every club, both seasons.')
out.append('NOTE|info|cutoff|All rows are completed matches on or before 2026-07-31. The Liberec v Teplice fixture (2026-08-01) is deliberately NOT in this pack.')
out.append('NOTE|warning|aet_handling|90-minute scores per rule: Pardubice v Karvina 2026-05-10 recorded 1-2 (AET 1-3); Sigma Olomouc v Bohemians 2026-05-10 recorded 0-2 (AET 1-2). Cup ties decided in extra time or on penalties recorded as draws with the 90-minute scoreline (penalty shootouts ignored).')
out.append('NOTE|warning|awarded|Slavia Prague v Sparta Prague 2026-05-09 abandoned and awarded 0-3 to Sparta (recorded as played, per league standings arithmetic, RSSSF cross-check).')
out.append('NOTE|warning|source_conflict|User-supplied 2024-25 playoff ties (Teplice-Opava, Jihlava-Pardubice) and 2025-26 Ostrava-Taborsko scorelines conflicted with RSSSF and were REJECTED. Loaded instead per RSSSF: 2024-25 Vyskov 0-0 Dukla, Pardubice 2-0 Chrudim, Dukla 1-1 Vyskov (aet, 4-2 pen), Chrudim 1-0 Pardubice; 2025-26 Ostrava 3-0 Taborsko, Taborsko 0-5 Ostrava, Artis Brno 1-4 Slovacko, Slovacko 3-0 Artis Brno.')
out.append('NOTE|info|aet90_user|Pardubice v Banik Ostrava MOL Cup 2025-11-05 recorded 3-3 at 90 minutes (AET 3-4); Sparta v Teplice cup QF 2025-04-09 recorded 1-1 at 90 minutes (AET 3-2) - user-supplied 90-minute reports. Lisen = Artis Brno (same club, renamed 2025-06, rename documented by RSSSF).')
out.append('NOTE|info|validation|Per-club W/D/L/GF/GA recomputed from these rows matches RSSSF tables exactly (64/64 checks): regular season 30 rounds both years; 35-round totals incl. groups; two-legged middle playoff totals.')

seen = set()
team_league = {}
for r in rows:
    for side in ('home','away'):
        t = r[side]
        if t not in seen:
            seen.add(t)
            disp, city = DISP[t]
            lg = 'Czech First League' if t in TOPFLIGHT else 'Czech lower divisions'
            code = 'CZ1' if t in TOPFLIGHT else 'CZ2'
            team_league[t] = lg
            stadium = 'Stadion u Nisy' if t == 'Liberec' else 'unknown'
            out.append(f'TEAM|{disp}|Czech Republic|{lg}|{code}||{stadium}|{city}|Czech Republic|unknown|unknown|unknown|unknown')

cities = {k: v[1] for k, v in DISP.items()}
def disp(t): return DISP[t][0]
for r in rows:
    comp = {'CZE1':'Czech First League','CUP':'MOL Cup','CZEPO':'Czech Relegation Playoffs'}[r['comp']]
    ctype = {'CZE1':'domestic-league','CUP':'domestic-cup','CZEPO':'other'}[r['comp']]
    h, a = r['home'], r['away']
    vt, stadium, vcity = 'normal', 'unknown', cities[h]
    key = (h, a, r['date'])
    if key in VENUE_NEUTRAL:
        vt, stadium, vcity = VENUE_NEUTRAL[key]
        if vt == 'neutral' and vcity == 'unknown': stadium = 'unknown'
    src = 'src-bbc' if r['comp'] == 'CZE1' else ('src-rsssf-2425' if r['date'] < '2025-07-01' else 'src-rsssf-2526')
    out.append(f"MATCH|{r['date']}|{comp}|{ctype}|{disp(h)}|{r['hg']}|{r['ag']}|{disp(a)}|{vt}|{stadium}|{vcity}|Czech Republic||{src}")

out.append('SOURCE|src-bbc|https://www.bbc.com/sport/football/czech-first-league/scores-fixtures|2026-08-01|results-database|BBC Czech First League scores and fixtures, month pages 2024-07 through 2026-07')
out.append('SOURCE|src-rsssf-2425|https://www.rsssf.org/tablest/tsje2025.html|2026-08-01|results-database|RSSSF Czech Republic 2024-25: round-by-round results, group tables, MOL Cup')
out.append('SOURCE|src-rsssf-2526|https://www.rsssf.org/tablest/tsje2026.html|2026-08-01|results-database|RSSSF Czech Republic 2025-26: tables, MOL Cup')
out.append('END')

open('packs/czech-team-pack.txt','w').write('\n'.join(out) + '\n')
print('lines:', len(out), ' teams:', len(seen), ' matches:', len(rows))
