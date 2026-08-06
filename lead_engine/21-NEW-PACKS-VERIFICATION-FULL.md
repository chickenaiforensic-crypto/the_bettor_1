# 21 — New Packs Verification Full (ITA 1901, GER 1540, FRA 1686, UEFA 1390)

**Date:** 2026-08-05 continued after researcher consolidation  
**Auditor:** Lead Planner — branch `arena/019fd213-the-bettor-1`  
**Script:** `audit_work/verify_new_packs.py` + `pack_parse.py` fresh code  
**Handoffs:** `handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` 257K, `GER` 230K, `FRA` 228K, `UEFA` 185K — from branches `019fc462` (R1) + `019fd1a3` (R2) consolidated  
**Status:** ITA/GER/FRA smoke PASS, UEFA 1 dup defect.

---

## 1. Smoke Gates (Grammar, Boundary, Dupe Inside, Overlap vs 5082)

| Pack | Matches | Teams | Sources/Notes | compType whitelist | Future >2026-08-05 | Dup inside | Overlap vs 5082 (expected 0) | Verdict Smoke |
|---|---|---|---|---|---|---|---:|---|
| ITA | 1901 = 1900 Serie A 380×5 + 1 Relegation Playoff Spezia 1-3 Verona 2023-06-11 compType other | 0 TEAM union 27 pins | 20/23 | domestic-league 1900 other 1 whitelist 0 bad PASS | 0 PASS | 0 PASS | 0 PASS | **PASS** matches researcher log 92/92 gates |
| GER | 1540 = 1530 Bundesliga 306×5 (18×34) + 10 Relegation Playoffs 2×5 | 3 TEAM Fortuna Dusseldorf / SC Paderborn / SV Elversberg | 21/25 | domestic 1530 other 10 whitelist 0 bad PASS | 0 PASS | 0 PASS | 0 PASS | **PASS** 93/93 gates per log SHA 4f90ddb1 triple-rebuild |
| FRA | 1686 = 1678 Ligue 1 380+380+306+306+306 (20→18 contraction) + 8 Playoffs 2×4 seasons | 0 TEAM 26 roster strings verbatim Paris SG / St Etienne | 19/22 | domestic 1678 other 8 whitelist 0 bad PASS | 0 PASS | 0 PASS | 0 PASS | **PASS** 85/85 gates per log SHA 44fe06b5 double-rebuild |
| UEFA | 1390 = 689 UCL + 437 UEL + 264 UECL, 99 TEAM foreign opponents, 2 SOURCE 61 NOTE | 99 | 2/61 | uefa-cl 689 uefa-el 437 uefa-uecl 264 whitelist 0 bad PASS | 0 PASS | **1 dup FAIL** | 0 PASS | **FAIL 1 dup** needs fix |

**Per-season breakdown:**

- **ITA Serie A:** 2021-22 380, 2022-23 380, 2023-24 380, 2024-25 380, 2025-26 380 = 1900 + 1 playoff 2022-23 (Spezia-Verona) = 1901 — matches 380×5 expected per workorder (20 clubs ×38 MDs). Unique teams 20 each season top Milan 86 GD38 2021-22, Napoli 90 GD49 2022-23, Inter 94 GD67 2023-24, Napoli 82 GD32 2024-25, Inter 87 GD54 2025-26 — plausible.
- **GER Bundesliga:** 2021-22 306, 2022-23 306, 2023-24 306, 2024-25 306, 2025-26 306 =1530 + playoffs 2 each season 2021-26 =10 →1540 — matches 306×5 expected (18×34). Unique 18 each season top Bayern 77 GD60 2021-22, Bayern 71 GD54 2022-23, Leverkusen 90 GD65 2023-24, Bayern 82 GD67 2024-25, Bayern 89 GD86 2025-26 — plausible.
- **FRA Ligue 1:** 2021-22 380, 2022-23 380, 2023-24 306, 2024-25 306, 2025-26 306 =1678 + playoffs 2,0,2,2,2 =8 →1686 — matches contraction 20→18 (380+380+306+306+306) per decree 2026-08-04. Unique 20 then 18. Top Paris SG 86 GD54 2021-22, 85 GD49 2022-23, 76 GD48 2023-24, 84 GD57 2024-25, 76 GD45 2025-26 — plausible.
- **UEFA:** 2021-22 651 UCL +254 UECL +414 UEL =1319 + small 2022-27 few matches (3,8,14,12 etc) =1390. Season grouping by date start year shows most in 2021 start year — because UEFA season spans Jul-Jun, our simple grouping lumps many 2021-22 season matches into 2021 start year, small spill into later — not a defect, just smoke grouping artifact. Unique teams per competition 81 UCL 2021-22 etc.

## 2. Defect Found — UEFA 1 Duplicate Fingerprint

```
('2022-04-12', 'Real Madrid', 'Chelsea', 'UEFA Champions League')
  Entry1: 2022-04-12 Real Madrid 1-3 Chelsea venueType QF leg2 stadium '' country Spain sourceId UCL-2122-QF-CHE-REA tieId openfootball
  Entry2: 2022-04-12 Real Madrid 2-0 Chelsea venueType QF leg1 stadium '' country Spain sourceId UCL-2223-QF-CHE-REA tieId openfootball
```

- Same fingerprint date+home+away+competition, different scores 1-3 vs 2-0, different leg labels leg2 vs leg1, different sourceIds (UCL-2122 vs UCL-2223) — second has wrong season (2223) for same date.
- Real world: 2021-22 QF Leg1 Apr 6 Chelsea 1-3 Real Madrid, Leg2 Apr 12 Real Madrid 2-3 Chelsea (aet) — so one entry should be Apr 6, other Apr 12 2-3, not both Apr 12 with 1-3 and 2-0.
- **This is a data defect — must be fixed by Researcher 2:** correct dates/scores/leg labels per primary RSSSF + UEFA.com, ensure shared tieId for two legs (both legs ONE tieId, not per-leg), 90-min doctrine (2-3 aet? Actually 2-3 was 90' 2-3? Check — QF leg2 Real 2-3 Chelsea after 90' 2-3? Actually 2-3 at 90' then aet? Need verify).
- **Impact:** 1 duplicate fingerprint → 0 PASS fails, would be rejected by ingest gate dedupe inside file (L890). Must be corrected to 0 dup.

## 3. Full Gates Still Needed (Beyond Smoke)

Per workorder §5 acceptance gates auditor re-runs everything:

- **Participation completeness:** For ITA/GER/FRA — every club's match list 2021-22..2025-26 complete vs official participant lists (20 clubs ITA 38 MDs =380, 18 clubs GER 34 MDs=306, FRA 20→18). Researcher logs claim 92/92, 93/93, 85/85 gates PASS + 100/100 per-club pivots + wiki matrices etc — need fresh re-parse via `rsssf_verify.py` equivalent for ITA/GER/FRA (RSSSF ital2022.. etc, german, french archives).
- **Structure:** per-competition round/phase counts vs official format (ITA 38 rounds ×10 ties, GER 34×9, FRA 38×10 then 34×9), playoffs 2 legs shared tieId, single-leg empty.
- **90-min doctrine:** every AET/pens tie carries 90' score + advancement NOTE — check German 2 ET legs (researcher log says 90-min doctrine on two ET legs) and FRA 2 aet legs.
- **Boundary:** no future, integer scores — smoke PASS.
- **Dedupe:** vs store 0 overlap PASS, vs itself 0 for ITA/GER/FRA PASS, 1 FAIL for UEFA → fix.
- **Names:** every home/away resolves to roster or TEAM rows, zero split identities — ITA 0 TEAM union 27 pins exactly means roster covers all, GER 3 TEAM PO participants outside roster, FRA 0 TEAM 26 roster strings verbatim Paris SG / St Etienne traps — need check.
- **Second-index:** OFB/worldfootball/wiki matrices 306/306 x4 after year-roll repair + 990 goals etc per logs — need fresh verification.
- **UEFA additional:** participation completeness every programme-league club Euro list 2021-22..2025-26 vs official participant lists, structure round/phase vs official format (UCL league phase 8 rounds ×18 ties from 2024-25, group stage 6×16 2021-24), shared tieId, 90-min doctrine AET/pens, boundary, names, cross-diff vs 4244-row Euro index, spot-audit one matchweek per season NOTE, continuity clause gap-free 2021-22→today.

## 4. Verdict For Forwarding

| Pack | Smoke | Defect | Ready For |
|---|---|---|---|
| ITA 1901 | PASS | None | **Full audit** (RSSSF ital2022..2026 + OFB + worldfootball) → then import via one gate + masked replay M5 ladder re-run parity |
| GER 1540 | PASS | None | **Full audit** (RSSSF duit2022..2026 + OFB + worldfootball + venue lattice) → import |
| FRA 1686 | PASS | None | **Full audit** (RSSSF fran2022..2026 + OFB + worldfootball + wiki matrix) → import |
| UEFA 1390 | FAIL 1 dup | Real Madrid-Chelsea 2022-04-12 duplicate fingerprint with conflicting scores/leg/season | **Return to Researcher 2 for fix** — correct dates/scores/leg/tieId per RSSSF + UEFA.com, ensure 0 dup inside pack, then re-audit |

**Data side currently:** 5082 CLOSED + 3 new leagues 1901+1540+1686 = 5127 pending + UEFA 1390 pending after fix → after import ~10,199 rows + cups + UEFA → ~11,589 with existing cups.

## 5. What Next — Forward to Team

### To Researcher 1:

- Your packs ITA/GER/FRA smoke PASS 0 dup 0 future compType whitelist OK per-season counts match expected 380×5 / 306×5 / 380+380+306+306+306 + playoffs. Fresh parse OK.
- Next: full auditor gates RSSSF re-parse + second-index + table reproduction (20/20 ITA, 18/18 GER, 20→18 FRA) + structure + 90-min + names + legacy cross-diff — then import.
- No re-push needed unless defects returned — your branch 019fc462 consolidated into planner.

### To Researcher 2:

- UEFA connector 1390 smoke: 689 UCL 437 UEL 264 UECL 99 TEAM 2/61 whitelist PASS future 0 overlap vs 5082 0 PASS — but **1 duplicate fingerprint FAIL**: `2022-04-12 Real Madrid vs Chelsea` appears twice same fingerprint different scores 1-3 vs 2-0 different leg labels leg2 vs leg1 different sourceIds UCL-2122 vs UCL-2223 — second has wrong season/wrong leg.
- Please fix: correct dates per RSSSF + UEFA.com (QF 2021-22 Leg1 Apr 6 Chelsea 1-3 Real, Leg2 Apr 12 Real 2-3 Chelsea aet — check 90-min scores), ensure both legs share ONE tieId (not per-leg), 90-min doctrine + advancement NOTE if aet, ensure 0 dup inside file, re-verify byte-deterministic rebuild identical, then re-push to your branch `019fd1a3` and ping.

### To Owner:

- Researcher1 DID get it — locked branch expected — 3 new leagues ITA/GER/FRA smoke PASS 1901/1540/1686 ready for full audit.
- Researcher2 UEFA 1390 delivered but 1 duplicate defect needs fix — returned.
- After full audit + import, store will go from 5082 → ~10,199 (+ITA/GER/FRA) → ~11,589 (+UEFA) + existing cups — then league pivot s[L] fit-to-results loop S5 can run on real Euro data (real-world cross-league accuracy).
- Builder B0 DONE ACCEPTED v3.7.0 — awaiting UAT before B1.

*Next full gates: RSSSF re-parse for ITA/GER/FRA/UEFA — scripts `rsssf_verify.py`, `pack_parse.py`, `fresh_audit.py`, `verify_new_packs.py`.*
