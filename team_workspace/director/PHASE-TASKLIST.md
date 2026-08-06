# PHASE TASKLIST — Zero-Harcode Football Prediction Engine

**Project:** the_bettor_1  
**Branch:** arena/019fd71e-the-bettor-1  
**Director:** Intelligence Coordination  
**Date:** 2026-08-06  
**Status:** PLANNING PHASE  
**REVISED:** Engine + UI moved to EARLY priority — app usable with verified leagues while data tops up  

---

## OVERVIEW

This document defines EVERY step required to reach the finish line.

**Core principle:** Zero-harcode system. Once team data is verified, we test/compute against the engine and recalibrate if necessary. No part of the engine is trusted until verified.

**NEW APPROACH:** Engine + UI design is now PRIORITY 2 (right after source-of-truth establishment). This creates a parallel track:
- **Track A (Data):** Verify → import → use verified leagues immediately
- **Track B (Engine+UI):** Build → verify → integrate with available data
- **Milestone:** Usable app with verified leagues WHILE other data comes in

---

## PHASE 0: SOURCE OF TRUTH ESTABLISHMENT (DAY 1-2)

### Objective
Locate and verify the ONE researcher's data that has the most accurate files. Establish this as the single source of truth for all team and tournament data.

### Current State
- **Verified data exists:** `previous_work_files/workspace-recent-019fd033-…/DATA-PACKS/IMPORT-READY-2026-08-03/`
  - RPL-2021-2026_BP-TEAM-PACK_v2.txt (md5: c3a72b35e834cc030d62b3d160c79b25) — 732 rows
  - RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt (md5: 91bce98de5ff5f999a2f03f3ee7d3caa) — 189 rows
  - MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt (md5: 662fe5dfe38002474855110b2a17ea6c) — 120 rows
  - CZ1-2021-2026_BP-TEAM-PACK_v2.txt (md5: 29c3b6c9d63906bde4db20ac4e6b742c) — 841 rows
- **Store has:** 5,000 verified rows (ENG 1,900 · RUS 1,579 · CZE 1,521)
- **Rejected data:** KOS, UEFA-FULL, UEFA-CONNECTOR (fabricated/defective)
- **In-flight:** SPA (parser fixed, not complete)
- **Queued:** ITA, GER, FRA, SCO1, SCOCUP, SCOLC, MLS, USOC

### Tasks
| # | Task | Owner | Deliverable |
|---|---|---|---|
| 0.1 | Verify md5/sha256 of all IMPORT-READY packs against declared pins | Auditor | Pin verification report |
| 0.2 | Re-parse every pack with FRESH code, compare row-by-row | Auditor | Fresh verification report |
| 0.3 | Table reproduction test: recompute standings from rows for each league/season | Auditor | Table reproduction report |
| 0.4 | Cross-diff all packs against independent second sources | Auditor | Cross-diff report |
| 0.5 | Declare VERIFIED packs as single source of truth | Director | Source-of-truth declaration document |
| 0.6 | Import D-2 fix: MOLCUP FULLSPAN (202 rows) → store becomes 5,082 | Owner | Store at 5,082 rows |

### Acceptance Criteria
- Every IMPORT-READY pack passes fresh parse + table reproduction + cross-diff
- Source of truth declaration cites specific md5 pins
- Store at 5,082 rows with verified data ready for engine

---

## PHASE 1: ENGINE + UI DESIGN (PRIORITY — PARALLEL TRACK A)

### Objective
Build/verify the engine and app UI so the system can be USED with verified leagues immediately, while other data continues to be collected. This is now PRIORITY 1 after Phase 0.

### Why Early?
- Owner can start using the app with verified leagues (RPL, CZ1, RUSCUP, MOLCUP, ENG)
- New data packs can be imported and tested as they arrive
- Engine verification happens against REAL data, not theoretical
- UI feedback can be gathered early

### 1.1 ENGINE INVENTORY + VERIFICATION

#### Tasks
| # | Task | Owner | Deliverable |
|---|---|---|---|
| 1.1.1 | Inventory every engine component in builder/app-v3.17.0-picker.html | Auditor | Component inventory with code line references |
| 1.1.2 | Cold-start rebuild: run engine from scratch on verified store | Builder + Auditor | Rebuild report; compare to pinned baseline |
| 1.1.3 | L1 verification: Dixon-Coles constants match spec exactly | Auditor | Constant verification report |
| 1.1.4 | L2 verification: two-grid implementation correct | Auditor | Grid verification report |
| 1.1.5 | L3 verification: star correction within ±0.02 cap | Auditor | Correction verification report |
| 1.1.6 | L4/L5 verification: labels + consensus correct | Auditor | Label verification report |
| 1.1.7 | R2 verification: evidence graph path slicing correct | Auditor | Graph verification report |
| 1.1.8 | R3 verification: ELO stars display-only, correct formula | Auditor | ELO verification report |
| 1.1.9 | I4/I5 verification: venue guard + settlement enforcement | Auditor | Guard verification report |
| 1.1.10 | P1 verification: zero market data in code (grep fetch/XHR/http) | Auditor | P1 compliance report |
| 1.1.11 | No-network verification: zero network calls | Auditor | Network verification report |
| 1.1.12 | One-gate verification: single ingest gate, no side doors | Auditor | Gate verification report |

#### Engine Components to Verify
| Component | What It Does | Verification Method |
|---|---|---|
| **L1: Dixon-Coles live fit** | Ratings (att/def/hfa) per league | Cold-start rebuild; compare to pinned baseline |
| **L2: Two grids** | scoreGrid → 1X2; goalsGrid → O/U | Verify Poisson + DC τ; check calibration ≤2.7% |
| **L3: Star draw correction** | Draw-rate refinement ±0.02 cap | Verify 27-cell draw_table; proportional split |
| **L4: Classification** | Tier labels from corrected probability | Verify band thresholds match observed rates |
| **L5: Consensus** | Selection filter (STRONG/CONFIRMED) | Verify min_games 4; test that it edits nothing |
| **R2: Evidence engine** | H2H + common-opponent path graph | Verify phase slicing; test NO CALL with balance |
| **R3: ELO layer** | Display-only stars 1-5 ★ | Verify K20, home +65, star formula |
| **M1: Auto re-validation** | Live re-derive on data change | Test that data change triggers re-fit |
| **M3: Provenance panel** | Source/window/n/calibration/date on every number | Verify panel shows for every output |

### 1.2 UI/UX DESIGN (A-02 COMPLIANT)

#### Design Principles (from A-02)
- **Plain language** — machine strings live in small-print "technical details" only
- **Human-first presentation** — no "AI-style" confidence language
- **Provenance small-print** — every number shows its source
- **Honest refusal** — "I don't know" is a valid, shown output (P3)
- **Numbers provable** — every claim traces to code or data

#### UI Components to Design/Verify
| Component | Purpose | Design Requirement |
|---|---|---|
| **Verdict Card** | Main output: probability + confidence + labels | Plain language; provenance visible; NO CALL with reasons |
| **Balance Panel** | Shows home/draw/away support shares on NO CALL | Must show on every NO CALL (M7) |
| **Provenance Panel** | Source/window/n/calibration/date for every number | Small-print but accessible (M3) |
| **Settlement Ledger** | Log of calls + outcomes | Draw = loss for home call (I5) |
| **Coverage Tab** | Shows which leagues/teams have data | Clear display of data availability |
| **Data Import Interface** | Drop zone for pack files | One gate; held cards visible; approve order clear |

#### UI Acceptance Criteria
- [ ] No market data references anywhere in UI (P1)
- [ ] No "AI-style" confidence language (A-02)
- [ ] Every probability shows provenance
- [ ] NO CALL shows balance panel + reasons
- [ ] User can see which leagues have data and which don't
- [ ] Import process is clear: drop → held cards → approve in order
- [ ] System can say "I don't know" without forcing a number

### 1.3 TEST-RUN LADDER (B0 — HARNESS PRODUCTIONISE)

#### Tasks
| # | Task | Owner | Deliverable |
|---|---|---|---|
| 1.3.1 | Productionise backtest harness | Builder | `audit_work/backtest_harness.py` production-ready |
| 1.3.2 | Add rolling-origin validation (≥4 expanding splits, T3) | Builder | Harness with T3 compliance |
| 1.3.3 | Add paired statistics (T1) | Builder | Harness with T1 compliance |
| 1.3.4 | Add minimum detectable effect reporting (T2) | Builder | Harness with T2 compliance |
| 1.3.5 | Add complete metric set (T4): Brier, log loss, calibration, direction, n, MDE | Builder | Harness with T4 compliance |
| 1.3.6 | Add artifact output (JSON/txt with all required fields) | Builder | Artifact format spec |
| 1.3.7 | Self-check vs masterplan §5.2 numbers | Builder + Auditor | Self-check report |

#### Ladder Protocol (from owner doctrine 2026-08-05)
```
L-1:  Train 2021 → (newest game − 1); predict newest game; calibrate constants
L-2:  Hold out newest 2 games; retrain on all before; test on both
L-n:  Expand holdout until covers whole last season
FULL: Full-system check, all leagues, complete metric set, paired, with n and MDE
```

### 1.4 FIRST MEASURED TEST (on verified leagues)

#### Tasks
| # | Task | Owner | Deliverable |
|---|---|---|---|
| 1.4.1 | Run L-1 on each verified league (RPL, CZ1, ENG) | Builder + Auditor | L-1 artifact per league |
| 1.4.2 | Run L-2 on each verified league | Builder + Auditor | L-2 artifact per league |
| 1.4.3 | Compare against masterplan §5.2 baseline numbers | Auditor | Comparison report |
| 1.4.4 | Document calibration status | Auditor | Calibration report |

#### Baseline Numbers (from masterplan §5.2)
| League | Train | Test | Brier DC | Brier base | Gain | Log loss | Direction |
|---|---|---|---|---|---|---|---|
| RPL | 2021-22..2024-25 (960) | 2025-26 (254) | 0.5675 | 0.6465 | −12.2% | 0.957 | 55.9% |
| CZ1 | 2021-22..2024-25 (1,105) | 2025-26 (276) | 0.6090 | 0.6509 | −6.4% | 1.015 | 49.3% |
| EPL | 2021-22..2024-25 (1,520) | 2025-26 (374) | 0.6140 | 0.6534 | −6.0% | 1.023 | 49.2% |

**Note:** These are the baseline numbers. Our harness must reproduce comparable results on verified data.

### Phase 1 Acceptance Criteria
- [ ] Engine components verified against spec (L1-L5, R2, R3, I4, I5)
- [ ] P1 grep: zero market data
- [ ] No-network grep: zero fetch/XHR/http
- [ ] One-gate verified
- [ ] Harness productionised and self-checked
- [ ] First test-run artifacts produced on verified leagues
- [ ] UI design meets A-02 plain language requirement
- [ ] NO CALL shows balance panel
- [ ] Provenance visible on every number

---

## PHASE 2: DATA COMPLETION — DOMESTIC LEAGUES (PARALLEL TRACK B)

### Objective
Complete all 5-year-span domestic league packs. These can be imported and used AS THEY ARE VERIFIED — no need to wait for all data to be complete before using the app.

### Task Sequence (researchers can work in parallel per owner decree)

#### 2.1 SPA — Spain La Liga (IN FLIGHT — HIGH PRIORITY)
| # | Task | Owner | Gate |
|---|---|---|---|
| 2.1.1 | Complete ledgers from RSSSF spanish sources | Researcher | All 1,900 rows accounted for |
| 2.1.2 | Cross-verify every round against worldfootball.net | Researcher | Source conflict notes |
| 2.1.3 | Table reproduction: 5 seasons × 20 clubs = 100 club-positions | Researcher | All 100 exact |
| 2.1.4 | Return pack to handoffs/ | Researcher | SPA-2021-2026_BP-TEAM-PACK_v2.txt |
| 2.1.5 | Auditor fresh-parse + table repro + cross-diff | Auditor | Pass/fail report |
| 2.1.6 | APPROVED → import to store | Auditor + Owner | SPA data in store |

#### 2.2 ITA — Italy Serie A
Same structure. 1,900 rows (20 clubs × 38 matches × 5 seasons).

#### 2.3 GER — Germany Bundesliga
Same structure. 1,530 rows (18 clubs × 34 matches × 5 seasons). **NOTE: Germany has 34 matchdays, not 38.**

#### 2.4 FRA — France Ligue 1
Same structure. 1,900 rows (20 clubs × 38 matches × 5 seasons).

### Data Import Protocol (Per League)
```
When a pack is approved:
1. Auditor issues approval card
2. Owner imports pack through app's ingest gate
3. Verify expected row count after import
4. Run M1: auto re-validation triggers
5. League becomes available in app
6. Log import in store.log

IMPORT ORDER (if dependent):
- MOLCUP before CZ1 (TEAM rows)
- League before cup (if cup references league teams)
- No other dependencies between leagues
```

### Acceptance Gates (EVERY pack must pass ALL)
| Gate | Test | Fail Action |
|---|---|---|
| **G1: Grammar** | Every row matches BP-TEAM-PACK v2 format | Return with format errors |
| **G2: Boundary** | No dateless/duplicate/future rows | Return with row numbers |
| **G3: Identity** | Every name matches roster verbatim | Return with violations |
| **G4: Source** | Every row has SOURCE line; RSSSF primary + second index | Return rows lacking sources |
| **G5: Table reproduction** | Recomputed standings match official table EXACT | Return with diffs |
| **G6: Shape** | Row counts match spec; every club's match count correct | Return with count diffs |
| **G7: 90-minute doctrine** | No ET/pen scores in league matches | Return with violations |
| **G8: Continuity** | Span gap-free; missing matches = written defect | Return with gap list |

---

## PHASE 3: DATA COMPLETION — DOMESTIC CUPS (PARALLEL)

### Objective
Complete cup competition packs. Can be imported as verified.

#### 3.1 SCO1 — Scottish Premiership
#### 3.2 SCOCUP — Scottish Cup
#### 3.3 SCOLC — Scottish League Cup
#### 3.4 RUSCUP — Russian Cup (ALREADY VERIFIED — 341 rows)
#### 3.5 MOLCUP — MOL Cup (ALREADY VERIFIED — import pending D-2)
#### 3.6 KOSCUP — Kosovo Cup (HALTED — KOS pack rejected)

### Special Gates for Cups
| Gate | Test |
|---|---|
| **Cup-specific G5** | Cup results match official brackets/rounds |
| **Two-leg ties** | Both legs separately with correct dates |
| **AET/pen handling** | 90' score + NOTE\|info\|advancement |
| **Neutral venues** | NOTE\|info\|neutral_venue for finals |

---

## PHASE 4: DATA COMPLETION — AMERICAN + OTHER (PARALLEL)

### 4.1 MLS — Major League Soccer (heaviest file; run last)
### 4.2 USOC — US Open Cup
### 4.3 Additional leagues as assigned

---

## PHASE 5: UEFA CONNECTOR DATA (CROSS-BORDER)

### Objective
Deliver clean UEFA competition data for cross-league rating bridge (M19/A-08).

### Critical: Prior Version Rejected
- UEFA-FULL: FABRICATED — fake scores, sentinel dates, missing rounds
- UEFA-CONNECTOR (prior): "dates fixed" claim FALSE — 1,388/1,390 sentinel-dated

### New Pack Requirements
| Requirement | Detail |
|---|---|
| **No sentinel dates** | Every date must be actual match date |
| **Real scores only** | Verified against UEFA.com |
| **Complete rounds** | No missing semifinals, finals, playoff rounds |
| **TEAM roster clean** | No ghost ClubA ids, no invented teams |
| **Venue data real** | No placeholder venues |

### Can Run in Parallel with Phase 2-4

---

## PHASE 6: RECALIBRATION (IF NECESSARY)

### Trigger
If test-run results from Phase 1.4 show degradation vs baseline numbers, recalibrate.

### Triggers for Recalibration
| Trigger | Action |
|---|---|
| Brier degradation on any league | Adjust LR (0.055) or decay (0.0022) within spec bounds |
| Calibration >2.7% on 1X2 | Investigate L2 grid implementation |
| Star correction outside ±0.02 cap | Fix L3 implementation |
| Evidence chain worse than baseline | Reject evidence ensemble; stay with DC-only |

### Tasks
| # | Task | Owner | Deliverable |
|---|---|---|---|
| 6.1 | Analyze test-run artifacts for degradation | Auditor | Degradation report |
| 6.2 | Identify constant(s) to adjust | Auditor + Builder | Adjustment proposal |
| 6.3 | Apply adjustment within spec bounds | Builder | Updated code |
| 6.4 | Re-run ladder from L-1 | Builder + Auditor | New artifact set |
| 6.5 | Compare new vs old artifacts | Auditor | Comparison report |
| 6.6 | Repeat until no degradation or explained | Team | Final calibrated artifact set |

---

## PHASE 7: FULL SYSTEM INTEGRATION

### Objective
All verified data + verified engine + verified UI → production system.

### Tasks
| # | Task | Owner | Deliverable |
|---|---|---|---|
| 7.1 | Import all verified packs into store | Owner (via app) | Complete store |
| 7.2 | Run M5: masked replay regeneration on full store | Builder | Calibration artifacts |
| 7.3 | Run M10: outcomes-only integrity screen | Auditor | Screen report |
| 7.4 | Verify store census: row counts, dedupe, date sanity | Auditor | Store census report |
| 7.5 | Verify every output has provenance (M3) | Auditor | Provenance verification |
| 7.6 | Verify NO CALL shows balance panel (M7) | Auditor | Balance panel verification |
| 7.7 | UAT: owner tests system on real fixtures | Owner | UAT sign-off |
| 7.8 | Version bump + pin | Builder | New version pinned in SOT |
| 7.9 | ZONES log entry | Auditor | Decision/event trail updated |

---

## PHASE 8: ONGOING MAINTENANCE

### Cadence
| Activity | Frequency | Owner |
|---|---|---|
| Monthly full harness sweep (M5) | Monthly | Builder + Auditor |
| New pack audit | Per delivery | Auditor |
| Store census | Per import | Auditor |
| P1 grep check | Per build | Auditor |
| ZONES log update | Per decision/event | Auditor |
| Engine re-verification | Per major build | Auditor |

---

## REVISED SUMMARY: TOTAL TASK COUNT

| Phase | Description | Tasks | Can RunParallel |
|---|---|---|---|
| **Phase 0** | Source of Truth | 6 | — |
| **Phase 1** | **ENGINE + UI + HARNESS (PRIORITY)** | **~25** | **Parallel with Phase 2-5** |
| Phase 2 | Domestic Leagues (SPA, ITA, GER, FRA) | ~36 | Parallel with Phase 1 |
| Phase 3 | Domestic Cups | ~40 | Parallel with Phase 1 |
| Phase 4 | American + Other | ~24 | Parallel with Phase 1 |
| Phase 5 | UEFA Connector | ~9 | Parallel with Phase 2-4 |
| Phase 6 | Recalibration (if needed) | ~6 | After Phase 1.4 |
| Phase 7 | Full Integration | ~9 | After Phase 1-5 complete |
| Phase 8 | Maintenance | Ongoing | Post-deployment |

**Total discrete tasks: ~155+ (excluding recalibration iterations)**

---

## KEY CHANGE: USABLE APP MILESTONE

### Milestone 1: Engine Verified + UI Ready (Phase 1 complete)
**When:** After Phase 1 acceptance criteria met  
**What user can do:**
- Open app and see verified leagues (RPL, CZ1, RUSCUP, MOLCUP, ENG)
- Get predictions for fixtures in those leagues
- See provenance on every number
- See NO CALL with balance panel when appropriate
- Import new verified packs as they arrive
- Watch engine auto-revalidate on new data

**What user CANNOT do yet:**
- Get predictions for leagues not yet in store (ITA, GER, FRA, etc.)
- Use cross-border bridge (needs UEFA connector data)
- Use goal-range bins (not built yet)

### Milestone 2: More Leagues Added (Phase 2-4 complete)
**When:** As each league pack is verified and imported  
**What user gains:**
- Predictions for new leagues as they come online
- More data = better calibration

### Milestone 3: Full Integration (Phase 7 complete)
**When:** All phases complete  
**What user gains:**
- Complete system with all available data
- Full calibration
- All engine features operational

---

## BLOCKERS

| Blocker | Resolves When | Blocks |
|---|---|---|
| KOS pack rejected | Drop KOS/KOSCUP or source new authentic data | Phase 3 (Kosovo) |
| UEFA-FULL rejected | Fresh UEFA pack required | Phase 5 |
| UEFA-CONNECTOR rejected | Fresh UEFA connector pack required | Phase 5, cross-border features |
| D-2 pending (MOLCUP import) | Import FULLSPAN file → 5,082 rows | Phase 0 (store completeness) |
| SPA incomplete | Complete ledgers + pack | Phase 2.1 |
| B0 harness not productionised | Builder completes B0 | Phase 1.3 |

---

## TEAM WORKFLOW

### Cold-Start Sequence for New Team Members

```
1. Member receives assignment + workorder
2. Member reads workorder in full + required SOP documents
3. Member signs acknowledgment
4. Member begins work
5. Member delivers to handoffs/ (researcher/builder) or Supervior/Build Docs/ (auditor)
6. Auditor verifies (fresh code)
7. If approved: import/integrate
8. If rejected: fix listed defects, re-return
```

### Parallel Work Rule
- Researchers can work on multiple leagues in parallel (owner decree 2026-08-02)
- Builder can work on engine/UI while researchers collect data
- Auditor verifies each return as it arrives (one card per return)
- No waiting for all data before starting engine work

---

*This tasklist is the master plan. Every task must be completed and signed off before the next phase begins. No skipping gates. No importing on trust. No silent rewrites.*

*Last updated: 2026-08-06 by Director — REVISED to prioritize engine + UI*
