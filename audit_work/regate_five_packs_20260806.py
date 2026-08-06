#!/usr/bin/env python3
"""Independent grammar/provenance receipt re-gate for the five 2026-08-06 packs."""
import datetime as dt, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PACKS=['MLS-2021-2026_BP-TEAM-PACK_v2.txt','USOC-2021-2026_BP-TEAM-PACK_v2.txt','SCOCUP-2021-2026_BP-TEAM-PACK_v2.txt','SCOLC-2021-2026_BP-TEAM-PACK_v2.txt','KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt']
OUT=ROOT/'audit_work/regate-five-packs-2026-08-06.json'
def audit(name):
 rows=[]; sources=set(); warnings=[]; errors=[]
 for n,line in enumerate((ROOT/'handoffs'/name).open(),1):
  x=line.rstrip('\n').split('|')
  if x[0]=='MATCH':
   if len(x)!=14: errors.append(f'L{n}: field_count={len(x)}, expected 14')
   if len(x)>=14:
    try: dt.date.fromisoformat(x[1])
    except ValueError: errors.append(f'L{n}: invalid calendar date {x[1]}')
    try:
     if int(x[5])<0 or int(x[6])<0:errors.append(f'L{n}: negative score')
    except ValueError:errors.append(f'L{n}: non-integer score')
    rows.append((n,x))
  elif x[0]=='SOURCE' and len(x)>1:sources.add(x[1])
  elif x[0]=='NOTE' and len(x)>2 and x[1]=='warning':warnings.append('|'.join(x[2:]))
 fps=Counter((x[1],x[2],x[4],x[7]) for _,x in rows)
 duplicate_count=sum(v-1 for v in fps.values() if v>1)
 refs=Counter(x[13] for _,x in rows)
 unmatched=sorted(set(refs)-sources)
 years=Counter(x[1][:4] for _,x in rows)
 decision='GRAMMAR_PROVENANCE_PASS' if not errors and not duplicate_count and not unmatched else 'FAIL'
 return {'match_rows':len(rows),'match_fields_14':len(rows),'dates_by_calendar_year':dict(sorted(years.items())),'declared_sources':sorted(sources),'source_refs':dict(refs),'unmatched_source_ids':unmatched,'duplicate_fingerprints':duplicate_count,'warning_notes':warnings,'errors':errors[:20],'error_count':len(errors),'decision':decision}
report={'date':'2026-08-06','scope':'grammar, date/score shape, duplicate fingerprint, declared source reference and stated blockers; not a table/bracket reproduction approval','packs':{n:audit(n) for n in PACKS}}
json.dump(report,OUT.open('w'),indent=2);print(json.dumps(report,indent=2))
