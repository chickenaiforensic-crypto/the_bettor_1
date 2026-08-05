import json

# ---- Master slug map: alias-table slugs -> (official name, city, country, league name, code, extra aliases)
MLS = {
 'atlanta':('Atlanta United FC','Atlanta','United States'),
 'austin':('Austin FC','Austin','United States'),
 'charlotte':('Charlotte FC','Charlotte','United States'),
 'chicago':('Chicago Fire FC','Chicago','United States'),
 'colorado':('Colorado Rapids','Commerce City','United States'),
 'columbus':('Columbus Crew','Columbus','United States'),
 'dc-united':('D.C. United','Washington','United States'),
 'fc-dallas':('FC Dallas','Frisco','United States'),
 'houston':('Houston Dynamo FC','Houston','United States'),
 'la-galaxy':('LA Galaxy','Carson','United States'),
 'lafc':('Los Angeles FC','Los Angeles','United States'),
 'inter-miami':('Inter Miami CF','Fort Lauderdale','United States'),
 'minnesota':('Minnesota United FC','Saint Paul','United States'),
 'cf-montreal':('CF Montréal','Montreal','Canada'),
 'nashville':('Nashville SC','Nashville','United States'),
 'new-england':('New England Revolution','Foxborough','United States'),
 'nycfc':('New York City FC','New York','United States'),
 'ny-red-bulls':('New York Red Bulls','Harrison','United States'),
 'orlando':('Orlando City SC','Orlando','United States'),
 'philadelphia':('Philadelphia Union','Chester','United States'),
 'portland':('Portland Timbers','Portland','United States'),
 'real-salt-lake':('Real Salt Lake','Sandy','United States'),
 'san-diego':('San Diego FC','San Diego','United States'),
 'san-jose':('San Jose Earthquakes','San Jose','United States'),
 'seattle':('Seattle Sounders FC','Seattle','United States'),
 'sporting-kc':('Sporting Kansas City','Kansas City','United States'),
 'st-louis':('St. Louis City SC','St. Louis','United States'),
 'toronto':('Toronto FC','Toronto','Canada'),
 'vancouver':('Vancouver Whitecaps FC','Vancouver','Canada'),
 'fc-cincinnati':('FC Cincinnati','Cincinnati','United States'),  # MISSING from returned alias table (verification F-B1)
}
USLC = {  # USL Championship (round-1 USOC evidence carriers)
 'detroit-city':('Detroit City FC','Detroit'),
 'louisville-city':('Louisville City FC','Louisville'),
 'memphis-901':('Memphis 901 FC','Memphis'),
 'new-mexico':('New Mexico United','Albuquerque'),
 'oakland-roots':('Oakland Roots SC','Oakland'),
 'phoenix-rising':('Phoenix Rising FC','Phoenix'),
 'sacramento-republic':('Sacramento Republic FC','Sacramento'),
 'tampa-bay-rowdies':('Tampa Bay Rowdies','St. Petersburg'),
 'las-vegas-lights':('Las Vegas Lights FC','Las Vegas'),      # not in returned alias table (F-B2)
 'charleston-battery':('Charleston Battery','Charleston'),    # (F-B2)
 'fc-tulsa':('FC Tulsa','Tulsa'),                             # (F-B2)
 'loudoun-united':('Loudoun United FC','Leesburg'),           # (F-B2)
 'indy-eleven':('Indy Eleven','Indianapolis'),                # (F-B2)
}
USL1 = {  # USL League One
 'charlotte-independence':('Charlotte Independence','Charlotte'),
 'union-omaha':('Union Omaha','Omaha'),
}
ALIAS = {
 'lafc':'LAFC','nycfc':'NYCFC','ny-red-bulls':'NY Red Bulls;NYRB','sporting-kc':'Sporting KC',
 'real-salt-lake':'RSL','cf-montreal':'CF Montreal','la-galaxy':'Los Angeles Galaxy',
 'inter-miami':'Inter Miami','dc-united':'DC United','st-louis':'St Louis City SC;St. Louis CITY SC',
 'new-england':'New England Revolution FC','sacramento-republic':'Sacramento Republic',
}
def name(slug):
    if slug in MLS: return MLS[slug][0]
    if slug in USLC: return USLC[slug][0]
    if slug in USL1: return USL1[slug][0]
    raise KeyError('unknown slug '+slug)
def meta(slug):
    if slug in MLS:
        n,c,co=MLS[slug]; return n,c,co,'Major League Soccer','MLS'
    if slug in USLC:
        n,c=USLC[slug]; return n,c,'United States','USL Championship','USL'
    if slug in USL1:
        n,c=USL1[slug]; return n,c,'United States','USL League One','USL1'
    raise KeyError(slug)

out=['BP-TEAM-PACK v2']
out.append('NOTE|info|research_ack|WORKORDER-MLS round-1 return (2026-08-01): 2024 MLS decision day (11) + 2024 MLS Cup Playoffs (28) + 2024 US Open Cup from R32 (21) + 2026 MLS July rounds (25) = 85 rows. NOT a full-season universe: no 2024 MD1-33, no 2025 season, no 2026 Feb-Jul, no Leagues Cup. Evidence-carrier level only; replay/calibration gated on full bulk (round 2).')
out.append('NOTE|warning|coverage_gap|2024 season: only the Oct-19 decision-day round + playoffs; 2025 season: absent; 2026 season: Jul 22/25/31 rounds only. Do NOT draw zone/calibration conclusions from this slice.')
out.append('NOTE|warning|aet_corrections|5 returned rows carried AFTER-EXTRA-TIME scores mislabeled as 90-minute-compliant (union-omaha-SKC 2024-05-08, sacramento-san-jose 2024-05-21, SKC-fc-dallas 2024-07-10, LAFC-SKC 2024-09-25, LAFC-seattle 2024-11-23). All corrected to their 90-minute scorelines per doctrine; advancement facts kept as NOTE rows. See usa/usa_round1_notes.md.')
out.append('NOTE|info|alias_gaps|Returned master alias table missed fc-cincinnati (30th MLS club) and 5 lower-division slugs referenced by its own match rows (las-vegas-lights, charleston-battery, fc-tulsa, loudoun-united, indy-eleven). All 6 added here.')
out.append('NOTE|info|codes|League codes populated from day one (lesson from RPL CZ sweep): MLS = Major League Soccer, USL = USL Championship, USL1 = USL League One. Canadian clubs carry club-true country (Wales/England precedent).')

for slug in sorted(MLS, key=lambda s: MLS[s][0]):
    n,c,co=MLS[slug]
    aliases=ALIAS.get(slug,'')
    out.append(f"TEAM|{n}|{co}|Major League Soccer|MLS|{aliases}|unknown|{c}|{co}|unknown|unknown|unknown|unknown")
for d,code_lg,code in ((USLC,'USL Championship','USL'),(USL1,'USL League One','USL1')):
    for slug in sorted(d, key=lambda s: d[s][0]):
        n,c=d[slug]
        aliases=ALIAS.get(slug,'')
        out.append(f"TEAM|{n}|United States|{code_lg}|{code}|{aliases}|unknown|{c}|United States|unknown|unknown|unknown|unknown")

MATCHES = [
 # (date, compLabel, compType, homeSlug, hg, ag, awaySlug, noteKey(None or 'pens'/'aet'), noteText)
 ('2024-10-19','Major League Soccer','domestic-league','philadelphia',1,2,'fc-cincinnati',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','dc-united',0,3,'charlotte',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','orlando',1,2,'atlanta',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','inter-miami',6,2,'new-england',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','minnesota',4,1,'st-louis',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','real-salt-lake',2,1,'vancouver',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','seattle',1,1,'portland',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','houston',2,1,'la-galaxy',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','austin',3,2,'colorado',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','fc-dallas',2,1,'sporting-kc',None,None),
 ('2024-10-19','Major League Soccer','domestic-league','lafc',3,1,'san-jose',None,None),
 ('2024-10-22','MLS Cup Playoffs','other','cf-montreal',2,2,'atlanta','pens','Atlanta advanced 5-4 on penalties'),
 ('2024-10-24','MLS Cup Playoffs','other','vancouver',5,0,'portland',None,None),
 ('2024-10-25','MLS Cup Playoffs','other','inter-miami',2,1,'atlanta',None,None),
 ('2024-10-26','MLS Cup Playoffs','other','la-galaxy',5,0,'colorado',None,None),
 ('2024-10-27','MLS Cup Playoffs','other','orlando',2,0,'charlotte',None,None),
 ('2024-10-27','MLS Cup Playoffs','other','lafc',2,1,'vancouver',None,None),
 ('2024-10-28','MLS Cup Playoffs','other','fc-cincinnati',1,0,'nycfc',None,None),
 ('2024-10-28','MLS Cup Playoffs','other','seattle',0,0,'houston','pens','Seattle advanced 5-4 on penalties'),
 ('2024-10-29','MLS Cup Playoffs','other','columbus',0,1,'ny-red-bulls',None,None),
 ('2024-10-29','MLS Cup Playoffs','other','real-salt-lake',0,0,'minnesota','pens','Minnesota advanced 5-4 on penalties'),
 ('2024-11-01','MLS Cup Playoffs','other','charlotte',0,0,'orlando','pens','Charlotte advanced 3-1 on penalties'),
 ('2024-11-01','MLS Cup Playoffs','other','colorado',1,4,'la-galaxy',None,None),
 ('2024-11-02','MLS Cup Playoffs','other','nycfc',3,1,'fc-cincinnati',None,None),
 ('2024-11-02','MLS Cup Playoffs','other','atlanta',2,1,'inter-miami',None,None),
 ('2024-11-02','MLS Cup Playoffs','other','minnesota',1,1,'real-salt-lake','pens','Minnesota advanced 3-1 on penalties'),
 ('2024-11-03','MLS Cup Playoffs','other','ny-red-bulls',2,2,'columbus','pens','New York Red Bulls advanced 5-4 on penalties'),
 ('2024-11-03','MLS Cup Playoffs','other','houston',1,1,'seattle','pens','Seattle advanced 7-6 on penalties'),
 ('2024-11-03','MLS Cup Playoffs','other','vancouver',3,0,'lafc',None,None),
 ('2024-11-08','MLS Cup Playoffs','other','lafc',1,0,'vancouver',None,None),
 ('2024-11-09','MLS Cup Playoffs','other','fc-cincinnati',0,0,'nycfc','pens','New York City FC advanced 6-5 on penalties'),
 ('2024-11-09','MLS Cup Playoffs','other','orlando',1,1,'charlotte','pens','Orlando advanced 4-1 on penalties'),
 ('2024-11-09','MLS Cup Playoffs','other','inter-miami',2,3,'atlanta',None,None),
 ('2024-11-23','MLS Cup Playoffs','other','lafc',1,1,'seattle','aet','90m 1-1; Seattle won 2-1 after extra time [AET-CORRECTED from returned 1-2]'),
 ('2024-11-24','MLS Cup Playoffs','other','orlando',1,0,'atlanta',None,None),
 ('2024-11-24','MLS Cup Playoffs','other','la-galaxy',6,2,'minnesota',None,None),
 ('2024-11-30','MLS Cup Playoffs','other','orlando',0,1,'ny-red-bulls',None,None),
 ('2024-11-30','MLS Cup Playoffs','other','la-galaxy',1,0,'seattle',None,None),
 ('2024-12-07','MLS Cup Playoffs','other','la-galaxy',2,1,'ny-red-bulls',None,None),
 ('2024-05-07','US Open Cup','domestic-cup','atlanta',3,0,'charlotte-independence',None,None),
 ('2024-05-07','US Open Cup','domestic-cup','houston',3,3,'detroit-city','pens','Detroit City advanced 10-9 on penalties'),
 ('2024-05-07','US Open Cup','domestic-cup','fc-dallas',1,0,'memphis-901',None,None),
 ('2024-05-07','US Open Cup','domestic-cup','san-jose',1,0,'oakland-roots',None,None),
 ('2024-05-08','US Open Cup','domestic-cup','union-omaha',1,1,'sporting-kc','aet','90m 1-1; Sporting KC won 2-1 after extra time [AET-CORRECTED from returned 1-2]'),
 ('2024-05-08','US Open Cup','domestic-cup','new-mexico',4,2,'real-salt-lake',None,None),
 ('2024-05-08','US Open Cup','domestic-cup','seattle',2,2,'louisville-city','pens','Seattle advanced 5-4 on penalties'),
 ('2024-05-08','US Open Cup','domestic-cup','las-vegas-lights',1,3,'lafc',None,None),
 ('2024-05-21','US Open Cup','domestic-cup','charleston-battery',0,0,'atlanta','pens','Atlanta advanced 5-4 on penalties'),
 ('2024-05-21','US Open Cup','domestic-cup','sporting-kc',4,0,'fc-tulsa',None,None),
 ('2024-05-21','US Open Cup','domestic-cup','sacramento-republic',3,3,'san-jose','aet','90m 3-3; Sacramento won 4-3 after extra time [AET-CORRECTED from returned 4-3]'),
 ('2024-05-21','US Open Cup','domestic-cup','lafc',3,0,'loudoun-united',None,None),
 ('2024-05-22','US Open Cup','domestic-cup','tampa-bay-rowdies',1,2,'fc-dallas',None,None),
 ('2024-05-22','US Open Cup','domestic-cup','seattle',2,1,'phoenix-rising',None,None),
 ('2024-07-09','US Open Cup','domestic-cup','atlanta',1,2,'indy-eleven',None,None),
 ('2024-07-10','US Open Cup','domestic-cup','sacramento-republic',1,2,'seattle',None,None),
 ('2024-07-10','US Open Cup','domestic-cup','sporting-kc',1,1,'fc-dallas','aet','90m 1-1; Sporting KC won 2-1 after extra time [AET-CORRECTED from returned 2-1]'),
 ('2024-07-10','US Open Cup','domestic-cup','lafc',3,1,'new-mexico',None,None),
 ('2024-08-27','US Open Cup','domestic-cup','sporting-kc',2,0,'indy-eleven',None,None),
 ('2024-08-28','US Open Cup','domestic-cup','seattle',0,1,'lafc',None,None),
 ('2024-09-25','US Open Cup','domestic-cup','lafc',1,1,'sporting-kc','aet','90m 1-1; LAFC won 3-1 after extra time [AET-CORRECTED from returned 3-1]'),
 ('2026-07-22','Major League Soccer','domestic-league','nashville',1,0,'cf-montreal',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','houston',1,1,'dc-united',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','sporting-kc',2,1,'minnesota',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','austin',3,1,'seattle',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','colorado',1,0,'san-diego',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','lafc',3,1,'real-salt-lake',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','portland',2,2,'fc-dallas',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','san-jose',0,4,'orlando',None,None),
 ('2026-07-22','Major League Soccer','domestic-league','la-galaxy',1,3,'st-louis',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','ny-red-bulls',0,2,'charlotte',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','columbus',2,1,'fc-cincinnati',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','philadelphia',1,0,'seattle',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','cf-montreal',0,1,'inter-miami',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','nycfc',3,1,'chicago',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','dc-united',2,1,'toronto',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','new-england',4,1,'atlanta',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','houston',3,0,'austin',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','minnesota',0,0,'vancouver',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','st-louis',1,0,'colorado',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','orlando',1,0,'nashville',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','san-diego',1,0,'fc-dallas',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','san-jose',1,1,'la-galaxy',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','lafc',4,0,'sporting-kc',None,None),
 ('2026-07-25','Major League Soccer','domestic-league','portland',2,1,'real-salt-lake',None,None),
 ('2026-07-31','Major League Soccer','domestic-league','nycfc',1,1,'toronto',None,None),
]
n_pens=n_aet=0
for d,label,ctype,h,hg,ag,a,kind,note in MATCHES:
    hn,hc,hco,_,_=meta(h); an,ac,aco,_,_=meta(a)
    out.append(f"MATCH|{d}|{label}|{ctype}|{hn}|{hg}|{ag}|{an}|normal|unknown|{hc}|{hco}||src-user-mls-r1")
    if note:
        key='90min-pens' if kind=='pens' else '90min-aet'
        sec=f"{d} {hn} {hg}-{ag} {an}: {note}."
        out.append(f"NOTE|info|{key}|{sec}")
        if kind=='pens': n_pens+=1
        else: n_aet+=1
out.append('SOURCE|src-user-mls-r1|https://www.ussoccer.com/|2026-08-01|results-database|WORKORDER-MLS round-1 return: user-supplied MLS bulk (85 matches, 90-minute doctrine applied incl. 5 AET corrections); USOC rows per supplier verification matrix (ussoccer.com + fallback logs)')
out.append('END')
open('packs/usa-team-pack.txt','w').write('\n'.join(out)+'\n')
n_match=sum(1 for l in out if l.startswith('MATCH'))
n_team=sum(1 for l in out if l.startswith('TEAM'))
print('teams',n_team,'matches',n_match,'pens-notes',n_pens,'aet-notes',n_aet,'lines',len(out))
