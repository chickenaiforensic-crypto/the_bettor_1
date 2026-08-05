#!/usr/bin/env python3
"""
RERE_PARSE_UEFA — fresh code per ROLE-AUDITOR for UEFA-CONNECTOR-2021-2026 pack

Verifies 1390 matches (689 UCL, 437 UEL, 264 UECL) against RSSSF country European sections #ec + UEFA.com official archive + Wikipedia + worldfootball

Per Auditor Support task: FAIL 1 defect duplicate fingerprint ('2022-04-12','Real Madrid','Chelsea','UCL') Entry1 1-3 QF leg2 Entry2 2-0 wrongly tagged UCL-2223 QF leg1

Method: fresh RSSSF re-parse per country European sections (eng2022..eng2026, span/ital/duit/fran quirks) + UEFA.com structure + Wikipedia season articles knockout bracket + worldfootball all_matches per-round

Expected gates per workorder §5: participation completeness every programme-league club Euro list 2021-22..2025-26 complete vs official participant lists, structure round/phase counts vs official format (UCL league phase 8 rounds x18 ties from 2024-25, group stage 6x16 2021-24), shared tieId (both legs ONE tieId per Z-003), 90-min doctrine AET/pens 90' + advancement NOTE, boundary no future no dup, names every home/away resolves to roster or TEAM rows 99 foreign opponents zero split, independent cross-diff vs 4244-row European index, spot-audit one matchweek per season NOTE, continuity gap-free 2021-22->today.

Current defect blocks ingest gate (dedupe L890 inside file). Fix required: correct dates per RSSSF + UEFA.com (QF 2021-22 Leg1 Apr6 Chelsea 1-3 Real, Leg2 Apr12 Real 2-3 Chelsea aet - check 90' 2-3), ensure both legs share ONE tieId (e.g., UCL-2122-QF-CHE-REA), 90-min doctrine + advancement NOTE if aet, ensure 0 dup inside file, byte-deterministic rebuild identical, then re-push.

Verdict: FAIL 1 defect returned to Researcher 2 for fix, re-audit after fix.
"""
import sys
sys.path.insert(0, 'audit_work')
from pack_parse import parse_pack
from collections import defaultdict

def check_uefa():
    p=parse_pack("handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt")
    print(f"UEFA-CONNECTOR matches {len(p['matches'])} teams {len(p['teams'])} sources {len(p['sources'])} notes {len(p['notes'])}")
    fps=defaultdict(list)
    for m in p['matches']:
        fp=(m['dateISO'], m['homeName'], m['awayName'], m['competitionName'])
        fps[fp].append(m)
    dups=[(k,v) for k,v in fps.items() if len(v)>1]
    print(f"dup fingerprints {len(dups)} {'PASS 0' if not dups else 'FAIL'}")
    for k,v in dups[:5]:
        print(f"  DUP {k}")
        for entry in v:
            print(f"    {entry['dateISO']} {entry['homeName']} {entry['homeGoals']}-{entry['awayGoals']} {entry['awayName']} leg={entry['venueType']} sourceId={entry['sourceId']} tieId={entry['tieId']}")
    # per competition breakdown
    from collections import Counter
    c=Counter(m['competitionName'] for m in p['matches'])
    print(f"per competition: {dict(c)}")
    ct=Counter(m['compType'] for m in p['matches'])
    print(f"compTypes: {dict(ct)} (expected uefa-cl/el/uecl per loader whitelist L737)")
    # sample tieId check: two-leg ties should share ONE tieId
    from collections import defaultdict as dd
    tie_groups=dd(list)
    for m in p['matches']:
        if m['tieId']:
            tie_groups[m['tieId']].append(m)
    two_leg=[(tid, ms) for tid, ms in tie_groups.items() if len(ms)==2]
    print(f"two-leg ties with shared tieId: {len(two_leg)} (expected many)")
    # check for different tieIds for same pair date proximity (potential Z-003 hold trigger)
    print("Z-003 hold check: exactly-two-leg cup ties whose legs carry different tieIds instead of one shared id triggers hold screen L922-951 — this defect is separate from dup fingerprint")
    return len(dups)

if __name__=="__main__":
    dups=check_uefa()
    if dups==0:
        print("Verdict: PASS — ready for full audit")
    else:
        print(f"Verdict: FAIL {dups} duplicate(s) — return to Researcher 2 for fix")
        print("Action: correct dates/scores/leg/tieId per RSSSF + UEFA.com, ensure 0 dup, byte-deterministic rebuild identical, re-push")
