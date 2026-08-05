import csv
rows=[r for r in csv.DictReader(open('cze_universe2.csv')) if r['comp']=='CZE1']
def rec(sub, team):
    w=d=l=gf=ga=0
    for r in sub:
        h,a=r['home'],r['away']
        if team not in (h,a): continue
        hg,ag=int(r['hg']),int(r['ag'])
        f,c=(hg,ag) if team==h else (ag,hg)
        gf+=f; ga+=c
        if f>c: w+=1
        elif f==c: d+=1
        else: l+=1
    return w,d,l,gf,ga

EXP={
 ('2024-25','reg'):{'Slavia':(25,3,2,61,11),'Plzen':(20,5,5,59,28),'Ostrava':(20,4,6,52,26),'Sparta':(19,5,6,56,33),'Jablonec':(15,6,9,47,25),'Olomouc':(12,7,11,46,41),'Liberec':(11,9,10,45,31),'Karvina':(11,8,11,40,52),'Hradec':(11,7,12,33,31),'Bohemians':(8,10,12,32,42),'Ml.Boleslav':(9,7,14,40,40),'Teplice':(9,7,14,32,42),'Slovacko':(7,9,14,25,51),'Dukla':(5,9,16,23,47),'Pardubice':(4,7,19,22,49),'C.Budejovice':(0,5,25,14,78)},
 ('2024-25','all'):{'Slavia':(29,3,3,77,18),'Plzen':(23,5,7,71,36),'Ostrava':(22,5,8,58,34),'Sparta':(19,6,10,61,44),'Jablonec':(19,6,10,60,33),'Olomouc':(12,9,14,48,53),'Liberec':(12,9,11,47,35),'Karvina':(11,8,13,40,57),'Hradec':(14,7,13,40,32),'Bohemians':(10,10,14,37,46),'Ml.Boleslav':(11,8,16,48,48),'Teplice':(12,8,15,41,45),'Slovacko':(9,11,15,31,56),'Dukla':(8,10,17,34,55),'Pardubice':(6,7,22,25,56),'C.Budejovice':(0,6,29,16,86)},
 ('2025-26','reg'):{'Slavia':(21,8,1,63,23),'Sparta':(19,6,5,60,33),'Plzen':(15,8,7,50,34),'Jablonec':(15,6,9,41,33),'Hradec':(14,7,9,43,34),'Liberec':(12,10,8,43,30),'Olomouc':(12,7,11,34,34),'Pardubice':(11,8,11,39,46),'Karvina':(12,3,15,43,51),'Bohemians':(10,6,14,26,35),'Ml.Boleslav':(8,11,11,44,52),'Zlin':(9,7,14,37,48),'Teplice':(6,11,13,29,38),'Dukla':(4,11,15,20,42),'Slovacko':(5,8,17,26,45),'Ostrava':(5,7,18,25,45)},
 ('2025-26','all'):{'Slavia':(24,8,3,74,31),'Sparta':(23,7,5,69,34),'Plzen':(18,9,8,60,38),'Hradec':(16,8,11,50,41),'Jablonec':(16,7,12,45,47),'Liberec':(12,10,13,45,39),'Olomouc':(15,7,12,44,38),'Pardubice':(12,8,12,42,49),'Karvina':(13,3,18,47,61),'Bohemians':(11,6,15,29,38),'Ml.Boleslav':(9,13,13,49,57),'Zlin':(11,8,16,43,56),'Teplice':(10,12,13,40,42),'Dukla':(5,11,19,23,51),'Slovacko':(7,9,19,30,51),'Ostrava':(7,8,20,32,49)},
}
fails=0
for (season,seg),teams in EXP.items():
    if season=='2024-25':
        sub=[r for r in rows if '2024-07-01'<=r['date']<='2025-06-30']
        reg=[r for r in sub if r['date']<='2025-04-19']
    else:
        sub=[r for r in rows if '2025-07-01'<=r['date']<='2026-06-30']
        reg=[r for r in sub if r['date']<='2026-04-25']
    pool = reg if seg=='reg' else sub
    print(f"== {season} {seg}: rows in pool {len(pool)}")
    for t,exp in teams.items():
        got=rec(pool,t)
        ok = got==exp
        if not ok:
            fails+=1
            print(f"  FAIL {t}: got {got} exp {exp}")
print('FAILED CHECKS:',fails)
# 2026-27 rows listing
print('== 2026-27 rows:')
for r in rows:
    if r['date']>='2026-07-01': print('  ',r['date'],r['home'],r['hg'],r['ag'],r['away'])
