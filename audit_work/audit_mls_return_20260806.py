#!/usr/bin/env python3
"""Independent structural receipt audit for the MLS workorder return."""
import datetime as dt, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PACK=ROOT/'handoffs/MLS-2021-2026_BP-TEAM-PACK_v2.txt'
OUT=ROOT/'audit_work/MLS-2021-2026-receipt-audit-2026-08-06.json'
CLUBS={'Atlanta United FC','Austin FC','CF Montréal','Charlotte FC','Chicago Fire FC','Colorado Rapids','Columbus Crew','D.C. United','FC Cincinnati','FC Dallas','Houston Dynamo FC','Inter Miami CF','LA Galaxy','Los Angeles FC','Minnesota United FC','Nashville SC','New England Revolution','New York City FC','New York Red Bulls','Orlando City SC','Philadelphia Union','Portland Timbers','Real Salt Lake','San Diego FC','San Jose Earthquakes','Seattle Sounders FC','Sporting Kansas City','St. Louis City SC','Toronto FC','Vancouver Whitecaps FC'}
# 2024 has 11 regular-season appendix rows deliberately held outside this return.
EXPECTED_RS={2021:459,2022:476,2023:493,2024:482,2025:510}
rows=[];errors=[];notes=[];team_decl=[];source_ids=[]
for line_no,raw in enumerate(PACK.open(),1):
 p=raw.rstrip('\n').split('|')
 if p[0]=='MATCH':
  if len(p)<14: errors.append(f'L{line_no}: MATCH has {len(p)} fields (<14)')
  try:dt.date.fromisoformat(p[1])
  except ValueError:errors.append(f'L{line_no}: invalid calendar date {p[1]}')
  if p[2] not in {'Major League Soccer','MLS Cup Playoffs'}:errors.append(f'L{line_no}: out-of-scope competition {p[2]}')
  if p[3]!='domestic-league':errors.append(f'L{line_no}: unexpected compType {p[3]}')
  if p[4] not in CLUBS or p[7] not in CLUBS:errors.append(f'L{line_no}: noncanonical club')
  try:
   if int(p[5])<0 or int(p[6])<0:errors.append(f'L{line_no}: negative score')
  except ValueError:errors.append(f'L{line_no}: noninteger score')
  rows.append((line_no,p))
 elif p[0]=='NOTE':notes.append(p)
 elif p[0]=='TEAM':team_decl.append(p[1])
 elif p[0]=='SOURCE':source_ids.append(p[1])
# With 13 fields, the final token is parsed as tieId, leaving sourceId absent;
# compare it explicitly to declared SOURCE ids to make the provenance failure clear.
misplaced_source_tokens=Counter(p[12] for _,p in rows if len(p)==13 and p[12])
source_ref_integrity={'declared_source_ids':source_ids,'match_sourceId_present':sum(1 for _,p in rows if len(p)>=14 and p[13]),'misplaced_final_tokens':dict(misplaced_source_tokens),'misplaced_tokens_matching_declared_source':sum(n for k,n in misplaced_source_tokens.items() if k in source_ids)}
fps=Counter((p[1],p[2],p[4],p[7]) for _,p in rows)
dup=[k for k,v in fps.items() if v>1]
by=Counter((int(p[1][:4]),p[2]) for _,p in rows)
rs={str(y):by[(y,'Major League Soccer')] for y in range(2021,2027)}
playoffs={str(y):by[(y,'MLS Cup Playoffs')] for y in range(2021,2027)}
blockers=[n[3] for n in notes if len(n)>3 and n[1]=='warning' and n[2]=='blocker']
missing=[]
for y,want in EXPECTED_RS.items():
 if rs[str(y)]<want:missing.append(f'{y} regular season has {rs[str(y)]}/{want} required rows')
if rs['2026']==0:missing.append('2026 regular season has 0 rows; workorder requires to-date coverage')
error_counts=Counter(e.split(': ',1)[1] if ': ' in e else e for e in errors)
a={'pack':str(PACK.relative_to(ROOT)),'matches':len(rows),'team_declarations':len(team_decl),'structural_error_count':len(errors),'structural_error_categories':dict(error_counts),'structural_error_examples':errors[:3],'source_reference_integrity':source_ref_integrity,'duplicate_fingerprints':len(dup),'regular_season_rows':rs,'playoff_rows':playoffs,'researcher_blockers':blockers,'scope_missing':missing,'decision':'RETURN_INCOMPLETE' if missing or errors or dup else 'STRUCTURAL_PASS_PENDING_TABLE_BRACKET_REPRODUCTION'}
json.dump(a,OUT.open('w'),indent=2);print(json.dumps(a,indent=2))
