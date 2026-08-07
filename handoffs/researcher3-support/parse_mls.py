import re, os, datetime, collections, json
REF=os.environ.get("REF","/tmp/mls-work/tables-master/tablesu")
CANON = {
 "Atlanta United FC":"Atlanta United FC","Atlanta United":"Atlanta United FC",
 "Austin FC":"Austin FC","CF Montréal":"CF Montréal","Montreal Impact":"CF Montréal","Montréal CF":"CF Montréal",
 "Charlotte FC":"Charlotte FC","Chicago Fire FC":"Chicago Fire FC","Chicago Fire":"Chicago Fire FC",
 "Colorado Rapids":"Colorado Rapids","Columbus Crew":"Columbus Crew","D.C. United":"D.C. United","DC United":"D.C. United",
 "FC Cincinnati":"FC Cincinnati","FC Dallas":"FC Dallas","Houston Dynamo FC":"Houston Dynamo FC","Houston Dynamo":"Houston Dynamo FC",
 "Inter Miami CF":"Inter Miami CF","Inter Miami":"Inter Miami CF","LA Galaxy":"LA Galaxy","Los Angeles Galaxy":"LA Galaxy",
 "Los Angeles FC":"Los Angeles FC","Minnesota United FC":"Minnesota United FC","Minnesota United":"Minnesota United FC",
 "Nashville SC":"Nashville SC","New England Revolution":"New England Revolution","New York City FC":"New York City FC","New York City":"New York City FC",
 "New York Red Bulls":"New York Red Bulls","Orlando City SC":"Orlando City SC","Orlando City":"Orlando City SC",
 "Philadelphia Union":"Philadelphia Union","Portland Timbers":"Portland Timbers","Real Salt Lake":"Real Salt Lake",
 "San Diego FC":"San Diego FC","San Jose Earthquakes":"San Jose Earthquakes","Seattle Sounders FC":"Seattle Sounders FC","Seattle Sounders":"Seattle Sounders FC",
 "Sporting Kansas City":"Sporting Kansas City","St. Louis City SC":"St. Louis City SC","Saint Louis City SC":"St. Louis City SC","St. Louis CITY SC":"St. Louis City SC",
 "Toronto FC":"Toronto FC","Vancouver Whitecaps FC":"Vancouver Whitecaps FC","Vancouver Whitecaps":"Vancouver Whitecaps FC",
}
MLS=set(CANON.values())
MONTHS={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
DATE_RE=re.compile(r'^\[([A-Z][a-z]{2})\s+(\d+)(?:,\s*(\d{4}))?\]')
SCORE_RE=re.compile(r'^\s*(.+?)\s+(\d+)\s*[-–]\s*(\d+)\s+(.+?)\s*$')
def clean(s):
    s=re.sub(r'\s*\[.*$','',s)
    s=re.sub(r'\s+(?:on\s+[A-Z][a-z]+\s+\d+\)?|[a-z].*?)\]\s*$','',s)
    s=s.strip()
    return re.sub(r'\s+',' ',s)
def parse_date(s,year):
    m=DATE_RE.match(s.strip())
    if not m: return None
    y=int(m.group(3)) if m.group(3) else year
    return datetime.date(y,MONTHS[m.group(1)],int(m.group(2)))
def parse_score(line):
    m=SCORE_RE.match(line.rstrip('\r'))
    if not m: return None
    return clean(m.group(1)),int(m.group(2)),int(m.group(3)),clean(m.group(4))
def resolve(name): return CANON.get(name.strip())
def parse_year(path,year):
    rows=[]; cur_date=None; section='pre'; round_label=None; skip_next_trailer=False
    for raw in open(path,encoding='utf-8-sig').read().splitlines():
        s=raw.strip()
        if not s: continue
        if s.startswith('=====') and 'Regular Season' in s: section='reg'; continue
        if s.startswith('=====') and 'Championship Playoff' in s: section='playoff'; round_label=None; continue
        if s.startswith('====') and 'US Open Cup' in s: section='usoc'; continue
        if s=='Final Tables:' and section=='reg' and len(rows)>0: section='tables'; continue
        if section=='reg':
            m=re.match(r'^Round\s+(\d+)\s*$',s)
            if m: round_label=f"MD{int(m.group(1)):02d}"; continue
            if s.startswith('Moved Matches'): round_label='MD-moved'; continue
        if section=='playoff':
            for key,lab in [('Conference Wild Card','WC'),('First Round','WC'),('Conference Quarterfinals','CQF'),
                            ('First Legs','CQF-L1'),('Second Legs','CQF-L2'),('Third Legs','CQF-L3'),('Third Leg','CQF-L3'),
                            ('Conference Semifinals','CSF'),('Conference Finals','CF'),('MLS Cup','MLSCup')]:
                if key in s and not s.startswith('['): round_label=lab; break
        d=parse_date(s,year)
        if d: cur_date=d; continue
        m=re.search(r'\[([A-Z][a-z]{2})\s+(\d+)(?:,\s*(\d{4}))?\]\s*$',s)
        if m and (s.startswith('Eastern') or s.startswith('Western') or s.startswith('MLS Cup')):
            y=int(m.group(3)) if m.group(3) else year
            cur_date=datetime.date(y,MONTHS[m.group(1)],int(m.group(2))); continue
        if section in ('reg','playoff') and cur_date:
            if s.endswith('bye') or s=='n/p' or ' n/p ' in (' '+s+' '): continue
            if re.match(r'^\s*\d+[. ]',s) or s.startswith('- - -') or s in ('Eastern Conference','Western Conference') or s.startswith('NB') or s.startswith('Round') or s.startswith('[*]'): continue
            if s.startswith('MLS Cup') or s.startswith('Western') or s.startswith('Eastern'): continue
            if (s.endswith('due to') or s.endswith('due to\r')) and not re.search(r'\d\s*[-–]\s*\d',s):
                skip_next_trailer=True; continue
            if s.endswith('due to') and not re.search(r'\d\s*[-–]\s*\d',s):
                skip_next_trailer=True; continue
            if skip_next_trailer:
                skip_next_trailer=False
                mt=re.match(r'^\s*(.+?)\s+(\d+)\s*[-–]\s*(\d+)\s+(.+?)\s*$',s)
                if not (mt and resolve(clean(mt.group(1))) and resolve(clean(mt.group(4)))):
                    continue
            if s.endswith(']') and not s.startswith('['):
                mt=re.match(r'^\s*(.+?)\s+(\d+)\s*[-–]\s*(\d+)\s+(.+?)\s*$',s)
                if not (mt and resolve(clean(mt.group(1))) and resolve(clean(mt.group(4)))):
                    continue
            if ('[remaining' in s or '[second half' in s) and not s.rstrip().endswith(']'):
                skip_next_trailer=True
            if ' abd ' in s and s.rstrip().endswith(']'): continue
            if '[abandoned' in s: skip_next_trailer=True; continue
            if not re.search(r'\d\s*[-–]\s*\d',s): continue
            sp=parse_score(raw)
            if not sp: continue
            h,hg,ag,a=sp
            hc=resolve(h); ac=resolve(a)
            if not hc or not ac: continue
            if hc not in MLS or ac not in MLS: continue
            rows.append({'date':cur_date.isoformat(),'home':hc,'away':ac,'hg':hg,'ag':ag,
                         'section':section,'round':round_label or ('MD' if section=='reg' else '')})
    return rows
if __name__=='__main__':
    all_rows=[]
    for y in [2021,2022,2023,2024,2025]:
        p=os.path.join(REF,f"usa{y}.txt")
        if not os.path.exists(p): continue
        rows=parse_year(p,y)
        print(y,len(rows),dict(collections.Counter(r['section'] for r in rows)))
        all_rows.extend(rows)
    os.makedirs("out",exist_ok=True)
    json.dump(all_rows,open("out/mls_parsed_2021_2025.json","w"),indent=1)
    print("saved",len(all_rows))
