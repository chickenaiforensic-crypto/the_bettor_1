#!/usr/bin/env python3
"""Independent diff: adopted packs vs legacy 153k dataset (football-data lineage).
Auditor-owned. Maps names, compares date+home+away+score for overlapping span."""
import csv, sys, collections

LEGACY = "previous_work_files/workspace-019fb2c3-ef67-7810-8bbc-222ea105634c/export/01_matches.csv"

RUS_MAP = {
    "Akhmat Grozny":"Akhmat Grozny","Akron Togliatti":"Akron Tolyatti","Arsenal Tula":"Arsenal Tula",
    "Baltika":"Baltika Kaliningrad","CSKA Moscow":"CSKA Moscow","Dynamo Makhachkala":"Dynamo Makhachkala",
    "Dynamo Moscow":"Dynamo Moscow","Khimki":"FC Khimki","Krasnodar":"FC Krasnodar","Orenburg":"FC Orenburg",
    "FK Rostov":"FC Rostov","Ufa":"FC Ufa","Fakel Voronezh":"Fakel Voronezh","Krylya Sovetov":"Krylia Sovetov Samara",
    "Lokomotiv Moscow":"Lokomotiv Moscow","Sochi":"PFC Sochi","Pari NN":"Pari Nizhny Novgorod",
    "Rodina Moscow":"Rodina Moscow","R. Volgograd":"Rotor Volgograd","Rubin Kazan":"Rubin Kazan",
    "SKA Khabarovsk":"SKA Khabarovsk","Spartak Moscow":"Spartak Moscow","T. Moscow":"Torpedo Moscow",
    "Torpedo Moscow":"Torpedo Moscow","Ural":"Ural Yekaterinburg","Yenisey":"Yenisey Krasnoyarsk",
    "Zenit":"Zenit St Petersburg",
}
CZE_MAP = {
    "1. FC Slovácko":"Slovacko","AC Sparta Praha":"Sparta Prague","Baník Ostrava":"Banik Ostrava",
    "Bohemians Praha 1905":"Bohemians 1905","Dynamo České Budějovice":"Ceske Budejovice",
    "FC Fastav Zlín":"Zlin","FC Zlín":"Zlin","FC Hradec Králové":"Hradec Kralove",
    "FK Dukla Praha":"Dukla Prague","FK Jablonec":"Jablonec","FK MAS Táborsko":"Taborsko",
    "FK Mladá Boleslav":"Mlada Boleslav","FK Pardubice":"Pardubice","FK Teplice":"Teplice",
    "MFK Chrudim":"Chrudim","MFK Karviná":"Karvina","MFK Vyškov":"Vyskov","SFC Opava":"Opava",
    "Sigma Olomouc":"Sigma Olomouc","Slavia Praha":"Slavia Prague","Slovan Liberec":"Slovan Liberec",
    "Viktoria Plzeň":"Viktoria Plzen","Zbrojovka Brno":"Zbrojovka Brno","1. FK Příbram":"Pribram",
    "FC Sellier & Bellot Vlašim":"Vlasim","SK Líšeň":"Lisen",
}

def load_legacy(comp, name_map=None):
    rows = []
    with open(LEGACY, newline='', encoding='utf-8', errors='replace') as f:
        for x in csv.DictReader(f):
            if x['competition'] != comp:
                continue
            if x.get('date_precision','') != 'EXACT':
                continue
            h = x['home_team']; a = x['away_team']
            if name_map:
                h = name_map.get(h, h); a = name_map.get(a, a)
            rows.append((x['date'], h, a, int(x['home_goals']), int(x['away_goals'])))
    return rows

def diff(pack_rows, legacy_rows, label, date_tol_ok=True):
    lset = collections.defaultdict(list)
    for (d,h,a,hg,ag) in legacy_rows:
        lset[(d,h,a)].append((hg,ag))
    n_matched = n_missing = n_score = n_date = 0
    date_only = []
    score_mism = []
    missing = []
    for m in pack_rows:
        d, h, a = m['dateISO'], m['homeName'], m['awayName']
        key = (d,h,a)
        if key in lset:
            if any(hg==m['homeGoals'] and ag==m['awayGoals'] for hg,ag in lset[key]):
                n_matched += 1
            else:
                n_score += 1
                score_mism.append(m)
        else:
            # date-only variant: same teams+score on a different date
            found = False
            if date_tol_ok:
                for (ld, lh, la), scores in lset.items():
                    if lh==h and la==a and any(hg==m['homeGoals'] and ag==m['awayGoals'] for hg,ag in scores):
                        # any date within 14 days counts as date-discrepancy (adjudicate later)
                        from datetime import date as D
                        try:
                            d0 = D.fromisoformat(d); d1 = D.fromisoformat(ld)
                            if abs((d1-d0).days) <= 14:
                                found = True; date_only.append((m, ld)); break
                        except ValueError:
                            pass
            if not found:
                n_missing += 1
                missing.append(m)
    print(f"== {label} ==")
    print(f"  pack rows: {len(pack_rows)} | legacy overlap rows: {len(legacy_rows)}")
    print(f"  exact match (date+teams+score): {n_matched}")
    print(f"  score mismatch: {n_score} | date-only (<=14d): {len(date_only)} | missing: {n_missing}")
    for m, ld in date_only[:12]:
        print(f"    DATE-ONLY: pack {m['dateISO']} {m['homeName']} {m['homeGoals']}-{m['awayGoals']} {m['awayName']}  | legacy {ld}")
    for m in score_mism[:12]:
        print(f"    SCORE: pack {m['dateISO']} {m['homeName']} {m['homeGoals']}-{m['awayGoals']} {m['awayName']}")
    for m in missing[:12]:
        print(f"    MISSING: pack {m['dateISO']} {m['homeName']} {m['homeGoals']}-{m['awayGoals']} {m['awayName']}  src={m.get('sourceId')}")
    return n_matched, n_score, date_only, missing

if __name__ == "__main__":
    sys.path.insert(0, 'audit_work')
    from pack_parse import parse_pack
    base = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/AUDITS/AUDIT-OVERRIDE-2026-08-04"
    jobs = [
        ("EPL-2021-2026.txt", "DOM:E0", None, "EPL vs legacy(E0)"),
        ("RPL-2021-2026.txt", "DOM:RUS", RUS_MAP, "RPL vs legacy(RUS)"),
        ("CZ1-2021-2026.txt", "DOM:CZE", CZE_MAP, "CZ1 vs legacy(CZE)"),
    ]
    for fn, comp, mp, label in jobs:
        p = parse_pack(f"{base}/{fn}")
        # only league rows (playoffs compType 'other' not in legacy feed)
        rows = [m for m in p['matches'] if m['competitionName'] not in ('Russian Relegation Playoffs','Czech Relegation Playoffs')]
        lg = load_legacy(comp, mp)
        # dedupe legacy
        seen = set(); lg2 = []
        for r in lg:
            if r[:3] not in seen:
                seen.add(r[:3]); lg2.append(r)
        diff(rows, lg2, label)
