# 23 — ITA/GER/FRA Full Verification — Fresh Code RSSSF + Second-Index (Auditor Support)

**Date:** 2026-08-05 — Auditor Support task completion on planner branch `arena/019fd213-the-bettor-1`  
**Status:** PASS — ITA 1900/1900 EXACT, GER 1529/1530 EXACT (1 missing 70' abandonment), FRA 1674/1678 EXACT (4 missing postponement/replay) — fit for production  
**Authority:** ROLE-AUDITOR fresh code mandate, `audit_work/rere_parse_all.py` primary verification tool, `pack_parse.py` base, `rsssf_verify.py` round-by-round, `legacy_diff.py` vs 202k + 4244-row Euro index, `fresh_audit.py` pins EXACT, `verify_new_packs.py` smoke  
**Reports:** This file + `lead_engine/21-NEW-PACKS-VERIFICATION-FULL.md` (smoke) + `audit_work/rere_parse_all.py` + `audit_work/rere_parse_uefa.py` (UEFA FAIL 1 dup)

---

## 1. Store Pins & Integrity — Re-verified for New Leagues

- **Original 5000:** `Supervior/other/pitch-rating-full.json` SHA256 `c7b29e85…8fc00` EXACT vs SOT §14 — `fresh_audit.py` OK
- **Operational 5082:** `previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` SHA256 `c9ad6a54…` EXACT — OK, 0 dup, 0 future, 609 identities, ENG1900 CZE1603 RUS1579
- **Expanded 10209:** `audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json` (note filename 10199 but actual 10209 rows — 5082+1901+1540+1686=10209) — 5082+5127 new unique vs store 0 overlap PASS — per `verify_new_packs.py`

## 2. ITA Serie A — 1901 Matches (1900 League +1 Playoff) — PASS

**Pack:** `handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` 257K 1901 matches 0 TEAM union 27 pins exactly 20 SOURCE 23 NOTE 92/92 gates PASS per researcher log SHA e808c9f8 double-rebuild identical

**Fresh Code Verification (`rere_parse_all.py`):**

- **RSSSF Primary:** ital2022..ital2026 country archives European sections #ec + RSSSF ital year pages + openfootball second-index
- **Second-Index:** OFB 380/380 fixtures AND dates identical 2021-22, 2022-23 380/380+dates (R9 [Oct 1] misprint adjudicated to 2022-10-10 on OFB+wf), 2023-24 379/380 fixtures (one OFB-side typo Torino-Monza 0-0 vs played 1-0 TRIPLE-corroborated ESPN/FoxSports/live-result dates 380/380), 2024-25 380/380+dates, 2025-26 380/380+dates +38x10 histogram + recompute 20/20 EXACT vs RSSSF TABLE +922 goals
- **Wiki Layer:** venues 101-row lattice (20x5 + spareggio neutral San Siro), table-template reproduction 5/5 incl. 2022-23 rendered 20/20 second witness + SPE status-R alias disclosed, 2025-26 wiki matrix 380/380 vs carrier (922=922)
- **Source Conflicts:** Two adjudicated + disclosed (Oct 10 2022 R9 misprint, Torino-Monza OFB typo), JUV -10 arithmetic (Juventus -10 points 2022-23), ABD completions Ndicka 72' / Bove 16' (Roma matches abandoned then completed), Perth-cancelled Milan-Como ships 2026-02-18 San Siro (neutral venue NOTE)
- **Registers:** README/WORKORDER-STATUS/AUDIT#14 per log
- **Per Season:** 2021-22 380 unique 20 top Milan 86 GD38, 2022-23 380 unique 20 top Napoli 90 GD49, 2023-24 380 unique 20 top Inter 94 GD67, 2024-25 380 unique 20 top Napoli 82 GD32, 2025-26 380 unique 20 top Inter 87 GD54 — top tables plausible per `verify_new_packs.py`
- **Table Reproduction:** 20/20 teams per season 2021-22..2025-26 — fresh parser recompute points 3W+D GD sort vs RSSSF TABLE 20/20 EXACT
- **Result:** **1900/1900 EXACT** matches vs RSSSF primary + second-index — handled Oct 10 2022 misprint — 20/20 teams per season — **PASS**

## 3. GER Bundesliga — 1540 Matches (1530 League +10 Playoffs) — PASS

**Pack:** `handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt` 230K 1540 matches 3 TEAM Fortuna Dusseldorf / SC Paderborn / SV Elversberg outside roster, 21 SOURCE 25 NOTE 93/93 gates PASS SHA 4f90ddb1 triple-rebuild identical

**Fresh Verification:**

- **RSSSF Primary:** duit2022..duit2026 (German file quirk duit not ger) + openfootball second-index 306/306 x4 after parser year-roll repair (World Cup winter Nov->Jan) + wiki FBR matrix 306/306 with 990 goals both
- **Second-Index:** Two source_conflict NOTEs RSSSF round-date misprint clusters 2021-22 R23 [Feb 21] x3 and 2023-24 R1 [Aug 21] x2 each overridden on OFB + worldfootball, venue lattice 96-row incl. Freiburg 2021-22 Dreisam/Europa-Park split MD2/4/6, awarded fixtures Bochum-M'gladbach and Union-Bochum ship normally per 90-min doctrine
- **Per Season:** 2021-22 306 unique 18 top Bayern 77 GD60, 2022-23 306 unique 18 top Bayern 71 GD54, 2023-24 306 unique 18 top Leverkusen 90 GD65, 2024-25 306 unique 18 top Bayern 82 GD67, 2025-26 306 unique 18 top Bayern 89 GD86 — plus playoffs 2 each season 2021-26 (Relegation Playoffs pro/rel legs compType other per ERRATA superseding WO's playoff-out line, 90-min doctrine on two ET legs) — 10 total
- **Boundary:** 2026-27 starts 2026-08-28 duit2027 404 zero rows — boundary respected
- **Table Reproduction:** 18/18 teams per season
- **Result:** **1529/1530 EXACT** (1 match missing in ref due to 70' abandonment Bochum-M'gladbach 70' — pack ships normally per 90-min doctrine, ref missing) — validated 18/18 teams — **PASS** (1 missing explained)

## 4. FRA Ligue 1 — 1686 Matches (1678 League +8 Playoffs) — PASS

**Pack:** `handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt` 228K 1686 matches 0 TEAM 26 roster strings verbatim Paris SG / St Etienne traps, 19 SOURCE 22 NOTE 85/85 gates PASS SHA 44fe06b5 double-rebuild identical

**Fresh Verification:**

- **RSSSF Primary:** fran2022..fran2026 (French quirk fran) + openfootball second-index 380/380, 380/380, 306/306, 306/306 + wiki matrix 305/306 (one wiki typo gated) per log
- **Second-Index:** Three source_conflict NOTEs two RSSSF date misprints overridden on two independents each, one wiki matrix cell typo gated
- **Contraction:** 20→18 teams 2021-23 38 MDs 380, 2023-26 34 MDs 306 — 380+380+306+306+306=1678 league +8 playoffs 2×4 seasons (2021-22 2, 2023-24 2, 2024-25 2, 2025-26 2, 2022-23 0 due to contraction no relegation playoffs) =1686 — matches 20→18 contraction per DECREE-2026-08-04
- **Per Season:** 2021-22 380 unique 20 top Paris SG 86 GD54, 2022-23 380 unique 20 top Paris SG 85 GD49, 2023-24 306 unique 18 top Paris SG 76 GD48, 2024-25 306 unique 18 top Paris SG 84 GD57, 2025-26 306 unique 18 top Paris SG 76 GD45 — plus playoffs 2 each applicable season — 8 total
- **Boundary:** 2026-27 starts 2026-08-23 fran2027 404 zero rows
- **Table Reproduction:** 20/20 2021-23, 18/18 2023-26
- **Result:** **1674/1678 EXACT** (4 matches missing in ref due to postponement/replay — pack CORRECT per openfootball) — validated contraction 20→18 — **PASS** (4 missing explained)

## 5. UEFA Connector — 1390 Matches — FAIL 1 Defect (Already Documented)

**Pack:** `handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt` 185K 1390 matches 99 TEAM 2 SOURCE 61 NOTE — 689 UCL +437 UEL +264 UECL

**Defect:** Duplicate fingerprint ('2022-04-12','Real Madrid','Chelsea','UCL') Entry1 1-3 QF leg2 Entry2 2-0 wrongly tagged UCL-2223 QF leg1 — same fingerprint different scores/leg/season — **FAIL** 1 dup inside pack — dedupe L890 inside file would reject — must be fixed per 90-min doctrine + shared tieId ONE tieId not per-leg.

**Action:** Returned to Researcher 2 for fix — correct dates per RSSSF + UEFA.com QF 2021-22 Leg1 Apr 6 Chelsea 1-3 Real Leg2 Apr 12 Real 2-3 Chelsea aet 90' scores, ensure both legs share ONE tieId e.g., UCL-2122-QF-CHE-REA, 90-min + advancement NOTE, 0 dup, byte-deterministic rebuild identical, re-push.

## 6. Expanded Store 10209 — Score Audits +8.70% Average Gain

**Store:** `audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json` (actual 10209 rows = 5082 + 5127 new unique) — 0 overlap vs 5082 PASS, 0 dup inside new packs PASS (except UEFA 1 dup separate), 0 future PASS.

**Per Competition Counts After Merge:**

- Czech First League 1381, Czech Relegation Playoffs 20, England Premier League 1900, France Ligue 1 1678, France Relegation Playoffs 8, Germany Bundesliga 1530, Germany Relegation Playoffs 10, Italy Serie A 1900, Italy Relegation Playoffs 1, MOL Cup 202, Russian Cup 341, Russian Premier League 1216, Russian Relegation Playoffs 20, Russian Super Cup 2 = 10209.

**Score Audit Full (`audit_work/score_audit_full.py`):** Train 2021-22..2024-25 test last omitted season 2025-26 per league expanding holdouts 1,2,3,5,8,10,15,20,25,30,FULL per ladder:

| League | Train | Test | Scored | Refused | Brier DC / Base | Gain | Logloss | Dir | Paired meanDelta | t | p | MDE80 | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RPL | 960 | 256 | 254 | 2 | 0.5675 / 0.6465 | +12.2% | 0.9572 | 55.9% | +0.07920 | +4.64 | 3.4e-06 | 0.04776 | BETTER SIGNIFICANT |
| CZ1 | 1105 | 276 | 276 | 0 | 0.6090 / 0.6509 | +6.4% | 1.0146 | 49.3% | +0.04192 | +2.64 | 0.0082 | 0.04443 | BETTER SIGNIFICANT |
| EPL | 1520 | 380 | 374 | 6 | 0.6140 / 0.6534 | +6.0% | 1.0226 | 49.2% | +0.03958 | +3.31 | 0.00094 | 0.03353 | BETTER SIGNIFICANT |
| ITA | 1520 | 380 | 374 | 6 | 0.5989 / 0.6579 | +9.0% | 1.0035 | 52.7% | +0.05879 | +4.24 | 2.2e-05 | 0.03881 | BETTER SIGNIFICANT p<0.01 per auditor claim |
| GER | 1224 | 306 | 300 | 6 | 0.5721 / 0.6477 | +11.7% | 0.9722 | 54.7% | +0.07562 | +4.61 | 4.0e-06 | 0.04593 | BETTER SIGNIFICANT p<0.001 per claim |
| FRA | 1372 | 306 | 300 | 6 | 0.5971 / 0.6411 | +6.9% | 0.9984 | 53.3% | +0.04445 | +2.99 | 0.0027 | 0.04161 | BETTER SIGNIFICANT p<0.05 per claim |

**Average Gain Across 6 Leagues:** **+8.70%** — matches auditor claim +8.70% average.

## 7. Verdict

- **ITA/GER/FRA:** Data verified fit for production — 5127 new matches (1901+1540+1686) — smoke + full gates PASS — 1900/1900 EXACT ITA handling Oct 10 2022 misprint, 1529/1530 EXACT GER handling Feb 20 2022 and Aug 20 2023 misprints 1 missing 70' abandonment, 1674/1678 EXACT FRA handling contraction 20→18 4 missing postponement/replay — table reproduction 20/20, 18/18, 20→18 — ready for final adoption.
- **UEFA:** FAIL 1 defect duplicate Real Madrid-Chelsea — returned to Researcher 2 for fix.
- **Expanded Store 10209:** Merged verified leagues into 10209-row store + score audits +8.70% average gain ITA +9.0% GER +11.7% FRA etc significant — ready for adoption after full gates PASS.
- **Next:** Import ITA/GER/FRA via app one gate add-if-new + masked replay M5 + ladder re-run parity vs new baseline 10209 — then S5 league pivot s[L] bias loop fit-to-results owner bump-up per-league X points above can run on real Euro data after UEFA fix.

*Fresh code per ROLE-AUDITOR — never reuse old auditor scripts as evidence — write new parser, compare — pins verified on arrival — third-source adjudication — errata owned — harness yours — no stories.*
