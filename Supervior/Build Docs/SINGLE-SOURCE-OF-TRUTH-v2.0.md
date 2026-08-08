# SINGLE SOURCE OF TRUTH v2.0
## The Complete Authority — Data, Engine, App, Rebuild Procedure

**Issued:** 2026-08-08  
**Branch:** `arena/019fde32-the-bettor-1`  
**Authority:** Lead Intelligence Officer / Senior Project Co-ordinator  
**Supersedes:** Director Control SOT v1.0 on `arena/019fd71e`, all prior status documents  
**Rule:** If any other document, branch, chat message, or app screen disagrees with this document, this document wins. No exceptions.

---

## 0. QUICK REFERENCE — WHAT IS APPROVED RIGHT NOW

| Scope | Rows | Status | Import to store? |
|---|---|---|---|
| England Premier League | 1,900 | ✅ VERIFIED | IN STORE |
| Russia (RPL + Cup + playoffs + Super Cups) | 1,579 | ✅ VERIFIED | IN STORE |
| Czechia (First League + MOL Cup + playoffs) | 1,603 | ✅ VERIFIED | IN STORE |
| Kosovo Superliga v2.1 | 910 | ✅ MATCH DATA APPROVED | PENDING D5 FIX |
| Kosovo Cup v2.1 | 123 | ✅ MATCH DATA APPROVED | PENDING D5 FIX |
| Spain La Liga v2 | 1,900 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| Italy Serie A v2 | 1,901 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| Germany Bundesliga v2 | 1,540 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| France Ligue 1 v2 | 1,686 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| Scotland Premiership v2 | 1,140 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| Scotland Cup v2 | 68 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| Scotland League Cup v2 | 72 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| US Open Cup v2.1 | 138 | ⚠ CANDIDATE | NEEDS INDEPENDENT AUDIT |
| MLS | 2,034 | ❌ PARTIAL | INCOMPLETE |
| UEFA Connector | — | ❌ REJECTED | FABRICATED |
| UEFA Full | — | ❌ REJECTED | FABRICATED |

**Store total: 5,082 verified rows. Awaiting import: up to 9,678 candidate rows across 8 packs.**

---

# PART A — COMPLETE DATA REGISTER

## A1. Verified Store (IN THE APP RIGHT NOW)

**File:** `previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json`  
**Location:** `main` branch  
**MD5:** `3c068c1f67ee8a81d412631fd0feb162`  
**SHA-256:** `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c`  
**Audit:** `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` — independent fresh-code audit, 5,000 rows verified, D-1 (11 CZ1 date fixes applied), D-2 (82 MOLCUP rows merged)

| Competition | MATCH rows | Verified against |
|---|---|---|
| England Premier League (2021-22 → 2025-26) | 1,900 | football-data.co.uk lineage dataset — 1,900/1,900 EXACT |
| Russian Premier League (2021-22 → 2025-26) | 1,220 | RSSSF rus2022–rus2026 — 1,220/1,220 EXACT |
| Russian Cup (2021-22 → 2025-26) | 341 | RSSSF cup chapters — 341/341 correct (3 RSSSF date misprints adjudicated, pack CORRECT) |
| Russian Relegation Playoffs | 16 | RSSSF — verified |
| Russian Super Cup | 2 | RSSSF / yenisafak — verified |
| Czech First League (2021-22 → 2025-26) | 1,381 | RSSSF tsje2022–tsje2026 + worldfootball.net — 1,390 EXACT, 11 dates corrected (D-1) |
| Czech Relegation Playoffs | 20 | RSSSF — verified |
| MOL Cup (2021-22 → 2025-26) | 202 | RSSSF tsje cup chapters + molcup.cz official DB — R16+ EXACT under 90-min doctrine |
| **TOTAL** | **5,082** | 0 duplicate fingerprints, 0 future dates, 0 bad scores, all identities resolve |

---

## A2. Auditor-Approved Match Data (NOT YET IN STORE)

### A2.1 Kosovo Superliga v2.1

**File:** `assembled_data/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt`  
**Source branch:** `arena/019fd805-the-bettor-1` @ `e02dcb8`  
**MD5:** `cde3688fd0da79b0f233c6d82cb50572`  
**SHA-256:** `531bc96c9bce742e97efc72fae92076a78c3e01bec7804ae0ab042b40c2bb966`

| Metric | Value |
|---|---|
| MATCH rows | 910 (900 league = 180×5 seasons + 10 playoffs) |
| TEAM rows | 8 |
| Table reproduction | 5/5 seasons EXACT (50/50 club-seasons) |
| Duplicates / future-dated | 0 / 0 |
| Venue placeholders | 0 |
| Sources | RSSSF kosovo2022–kosovo2026 primary; worldfootball 2025-26 carrier; Wikipedia cross-check |

**Auditor verdict (2026-08-07):** MATCH DATA APPROVED. All 910 rows byte-identical to independent auditor build. Gate suite passes.  
**Blocker:** D5 — 8 TEAM rows have field misalignment (stadium→surface swap). Metadata-only. Fix spec in auditor report.  
**Audit report:** `arena/019fd74a-the-bettor-1:Supervior/Build Docs/AUDIT-KOS-KOSCUP-REAUDIT-2026-08-07-v1.0.md`

### A2.2 Kosovo Cup v2.1

**File:** `assembled_data/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt`  
**Source branch:** `arena/019fd805-the-bettor-1` @ `e02dcb8`  
**MD5:** `cca71b174a7af989b43ed4cf285ca6b9`  
**SHA-256:** `acf40a85d04da7e8d490e67130046fb3bfa79f64d1b640fb8f2b97df7b0afd97`

| Metric | Value |
|---|---|
| MATCH rows | 123 slice ties (24/24/24/26/25 per edition) |
| TEAM rows | 24 |
| Slice violations (tie with zero Superliga clubs) | 0 |
| Venue placeholders | 0 |
| Sources | RSSSF cup chapters primary |

**Auditor verdict:** MATCH DATA APPROVED. Gates pass.  
**Blocker:** D5 — 24 TEAM rows have same field misalignment as KOS.  
**Audit report:** Same as A2.1.

---

## A3. Candidate Packs (DELIVERED, SELF-GATED, NEED INDEPENDENT AUDIT)

All packs below were delivered by researchers on their respective branches. Self-check gates were run (table reproduction, dedupe, source linkage). These self-checks are REGISTERED but NOT YET ADOPTED — they need a fresh independent auditor pass before import.

### A3.1 Spain La Liga v2

**File:** `assembled_data/SPA-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd805-the-bettor-1`  
**MD5:** `81e553a46e58f5c41b533ba2bbd7643c`

| Metric | Value |
|---|---|
| MATCH rows | 1,900 (380×5 seasons) |
| TEAM rows | 0 |
| Researcher table reproduction | 5/5 seasons EXACT (100/100 club-seasons) |
| Auditor cross-check (019fd74a) | 2025-26: 380/380 scores identical to re-fetched Wikipedia matrix; goals 1,024 |
| Sources | RSSSF span2022–span2026 primary; fbref 2025-26 carrier; Wikipedia cross-check |

### A3.2 Italy Serie A v2

**File:** `assembled_data/ITA-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd4e0-the-bettor-1`  
**MD5:** `05344481d04be2648694944a4f6f6c3f`

| Metric | Value |
|---|---|
| MATCH rows | 1,901 (380×5 + 1 relegation spareggio) |
| TEAM rows | 0 |
| Sources | RSSSF ital2022–ital2026 primary |
| Audit status | NOT INDEPENDENTLY VERIFIED |

### A3.3 Germany Bundesliga v2

**File:** `assembled_data/GER-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd4e0-the-bettor-1`  
**MD5:** `afc99d36c3d7aa3e84eb2e103800f7f0`

| Metric | Value |
|---|---|
| MATCH rows | 1,540 (306×5 + 10 relegation playoffs) |
| TEAM rows | 3 |
| ⚠ 18 clubs × 34 matchdays (NOT 20×38 like other major leagues) | VERIFIED |
| Sources | RSSSF duit2022–duit2026 primary |
| Audit status | NOT INDEPENDENTLY VERIFIED |

### A3.4 France Ligue 1 v2

**File:** `assembled_data/FRA-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd4e0-the-bettor-1`  
**MD5:** `4b302b1727eedf5586366a74dd66a7cb`

| Metric | Value |
|---|---|
| MATCH rows | 1,686 (20-club: 380+380; 18-club: 306+306+306 + 8 relegation playoffs) |
| ⚠ League shrank from 20 to 18 clubs in 2023-24 | VERIFIED |
| Sources | RSSSF fran2022–fran2026 primary |
| Audit status | NOT INDEPENDENTLY VERIFIED |

### A3.5 Scotland Premiership v2

**File:** `assembled_data/SCO1-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd4e0-the-bettor-1`  
**MD5:** `2304fe1f42a191189e94ea26d8279b19`

| Metric | Value |
|---|---|
| MATCH rows | 1,140 |
| TEAM rows | 1 |
| Table reproduction (auditor, 08-05) | 2024-25: 12/12 clubs EXACT vs RSSSF post-split |
| Sources | RSSSF scot2022–scot2026 primary |
| Audit status | PARTIAL — table repro spot-checked, full independent audit not performed |

### A3.6 Scotland Cup v2

**File:** `assembled_data/SCOCUP-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd4e0-the-bettor-1`  
**MD5:** `e7ff5ac9d20933ca848a1181dfd9d450`

| Metric | Value |
|---|---|
| MATCH rows | 68 |
| TEAM rows | 14 |
| Audit status | NOT INDEPENDENTLY VERIFIED |

### A3.7 Scotland League Cup v2

**File:** `assembled_data/SCOLC-2021-2026_BP-TEAM-PACK_v2.txt`  
**Source branch:** `arena/019fd4e0-the-bettor-1`  
**MD5:** `1d1f065fe89edf1db9892785905bac24`

| Metric | Value |
|---|---|
| MATCH rows | 72 |
| TEAM rows | 14 |
| Audit status | NOT INDEPENDENTLY VERIFIED |

### A3.8 US Open Cup v2.1

**File:** `assembled_data/USOC-2021-2026_BP-TEAM-PACK_v2.1.txt`  
**Source branch:** `arena/019fdd64-the-bettor-1`  
**MD5:** `5875319c76be17ad8a1ebdb74c284550`

| Metric | Value |
|---|---|
| MATCH rows | 138 (2022:28; 2023:30; 2024:21; 2025:31; 2026:28 through QF) |
| TEAM rows | 35 |
| Slice rule | Every tie with ≥1 MLS club |
| ⚠ 2026 RSSSF not yet published — cross-verified across ≥2 independent second-index sources |
| Audit status | NOT INDEPENDENTLY VERIFIED |

---

## A4. Incomplete / Partial

### A4.1 MLS

**File:** `assembled_data/MLS-2021-2024-PARTIAL.txt`  
**MD5:** `930d1804a5907cf2d405974a22f34039`

| Metric | Value |
|---|---|
| MATCH rows | 2,034 |
| Coverage | 2021-2024 regular season + playoffs + 2025 playoffs |
| Missing | 2025 regular season, 2026-to-date |
| Blockers | 2026 RSSSF not published; designated second-index (FBref) Cloudflare-blocked; venue data incomplete |
| Status | NOT READY FOR AUDIT |

---

## A5. Rejected — DO NOT USE

| Pack | Location | Reason | Evidence |
|---|---|---|---|
| UEFA-CONNECTOR v2 | `arena/019fd4e0:handoffs/` | 1,388/1,390 rows sentinel-dated. "Dates fixed" claim FALSE. | Prior auditor verified |
| UEFA-FULL v2 | `arena/019fd4e0:handoffs/` | Fake scores (PSG 4-3 Arsenal), 2,762/2,764 sentinel-dated, missing rounds, 5 ghost ClubA ids | Prior auditor verified |
| KOS v2 (old) | `arena/019fd4e0:handoffs/` | Ghost clubs (Ferizaj, Suhareka), 0/10 table repro, 180 sentinel dates | Superseded by v2.1 |
| KOSCUP v2 (old) | `arena/019fd4e0:handoffs/` | Identity defects | Superseded by v2.1 |

---

# PART B — APP SPECIFICATION

## B1. What the app IS

One HTML file. Runs in any browser. Zero server. Zero accounts. Zero network calls.

**Current approved build:** `builder/app-v3.17.0-picker.html` on `main`  
**MD5:** `e6687ad417fd1d3229a000c12f73f1a3`  
**SHA-256:** `51e275da4d2bbb3a0b198fa7f07d66ec9fd07bb965293b4c63ab8d9ea1e210d7`

**Critical defect in v3.17.0:** On first boot, the app auto-loads 9 embedded `SEED_PACKS` containing partial legacy records for Wales, Slovenia, Kosovo, Scotland, Malta, Iceland, Cyprus, and others. These are NOT approved data. The clean-boot workorder (`team_workspace/builder/WORKORDER-BUILDER-CLEAN-BOOT-QUARANTINE-v1.0.md` on `019fd71e`) requires removal of this auto-seeding behavior.

## B2. Engine Architecture (Dixon-Coles, Single Weighted Engine)

The engine has ONE computation pipeline. No second rating universe. No carried bootstrap. No hidden precompute.

```
STORE (completed 90-min results only)
  │
  ├── L1: LIVE DC FIT (per-league online Dixon-Coles)
  │     Constants: LR 0.055 · DECAY 0.0022 · HFA_LR 0.010 · 1.6× first 8 · ρ −0.06
  │     λ_home = exp(μ[league] + att[home] − def[away] + hfa[league] + home_extra[home])
  │     λ_away = exp(μ[league] + att[away] − def[home])   clamp [0.05, 6.0]
  │
  ├── L2: TWO GRIDS
  │     scoreGrid: independent Poissons × DC τ (ρ=−0.06) → normalised H/D/A
  │     goalsGrid: total shrunk toward league mean (G_K=0.5, GMU=2.6186) → O/U + handicap only
  │     BTTS: WITHHELD (6.0% error → I3 gate)
  │
  ├── L3: STAR DRAW CORRECTION (±0.02 cap, proportional split)
  │     draw_table[tier|starGap] 27 cells · weights 0.2/0.5/0.5 · +0.047% measured gain
  │
  ├── L4: CLASSIFICATION (labels, edits nothing)
  │     A+ Fortress ≥70 · A Strong ≥60 · B Lean ≥52 · C Marginal ≥45 · D Coin-flip ≥35 · E Avoid <35
  │
  ├── L5: CONSENSUS (selection filter, edits nothing)
  │     STRONG 78.6% / CONFIRMED 74.8% · min 4 home + 4 away both sides
  │
  ├── R2: EVIDENCE ENGINE (H2H + common-opponent path graph)
  │     Zone ladder: STRONG→WIN→WIN-DRAW→LEAN→TOSS with calibrated rates
  │     NO CALL must show balance panel
  │
  └── R3: ELO STARS (display only, never edits R1/R2/R3)
        INIT 1500 · K 20 · home +65 · 1–5★
```

**Measured contribution hierarchy (constitution):**
1. L1 DC fit: Brier 0.6112 vs 0.6476 base = **+5.6%** — DOMINANT
2. L2 goalsGrid: O2.5 error 10.3%→**2.7%**
3. L3 star correction: **+0.047%** full-1X2 (p<0.0001, n=59,615)
4. L4/L5: zero probability impact (display only)
5. R2 zone ladder: confidence statement, not probability
6. R3 ELO: display only

## B3. The Binding Rules (P1-P5, I1-I6, T1-T8)

**P1:** No market data. Ever. In any role — input, feature, benchmark, sanity check, fallback. Permanent.

**P2:** Results are the only ground truth. Teams, date, venue, 90-minute goals. Nothing else.

**P3:** The system must say "I don't know." NO CALL is a valid, shown output.

**P4:** Foundation → validation → superstructure. No layer ships before the layer beneath validates.

**P5:** Shipping requires explicit owner approval. Every build judged by its measured test run.

**I1:** Fidelity — shipped code reproduces validated engine exactly (0.00e+00 across 7 quantities, browser vs trainer).

**I2:** Test coverage before ship.

**I3:** Market gating by measured error. Ship ≤2.7%. Caution 3.0–3.3%. BTTS withheld 6.0%.

**I4:** Venue integrity — never trust parsed venue. Hard error if home team never hosted in league. Save disabled until confirmed.

**I5:** Draw = loss for home-win call. Never a push, never excluded.

**I6:** Zero network dependency. No fetch/XHR/http. Updates via validated file intake only.

**T1-T8:** Paired tests, MDE reporting, rolling-origin validation, complete output measurement, user's construction tested, "not significant" ≠ "no effect," structural break checks, data-driven gates only.

## B4. The Rebuild: What the Next Build MUST Do

### 4.1 Remove Embedded Seed Autoloading

The v3.17.0 app contains 9 `SEED_PACKS` that auto-load on first boot. The next build (v3.18.0) must:

1. Boot with an empty store — zero rows, zero identities, zero coverage
2. Show "No approved data loaded yet" on clean boot
3. Wait for audited data through `PR.ingest`
4. Never auto-commit an embedded pack, legacy seed, or closure record
5. Preserve engine math, `PR.ingest` grammar, provenance, NO CALL, settlement, and the one intake gate
6. `fetch`/`XMLHttpRequest` count = 0 (unchanged)

### 4.2 Data Loading (Post-Clean-Boot)

After clean boot, data enters in this order:

1. Load the verified 5,082-row store (`pitch-rating-full-5082-D1D2-2026-08-05.json`) via migration
2. Import KOS v2.1 after D5 TEAM-row fix (auditor-approved match data)
3. Import KOSCUP v2.1 after D5 fix
4. Import SPA v2 after independent audit (candidate)
5. Import ITA/GER/FRA v2 after independent audit (candidates)
6. Import SCO1/SCOCUP/SCOLC v2 after independent audit (candidates)
7. Import USOC v2.1 after independent audit (candidate)
8. Complete MLS and UEFA connector when data is available and audited

### 4.3 Engine Verification

After loading all approved data, run the test-run ladder:

```
L-1: Train 2021→(newest−1), predict newest game, calibrate
L-2: Hold out newest 2, retrain, test both
L-n: Expand holdout until covers whole last season
FULL: Full-system check, all leagues, complete metric set, paired, with n and MDE
```

Baseline numbers to beat (from `audit_work/backtest_harness.py` first run on 5,082 store):
- RPL: brier_dc 0.5675 vs 0.6465 base (−12.2%)
- CZ1: brier_dc 0.6090 vs 0.6509 base (−6.4%)
- EPL: brier_dc 0.6140 vs 0.6534 base (−6.0%)

The harness (`audit_work/backtest_harness.py`) must be productionised as the app's masked-replay module (S0 per masterplan §8).

---

# PART C — BRANCH MAP (WHERE EVERYTHING LIVES)

| Branch | Role | Key contents |
|---|---|---|
| `arena/019fde32-the-bettor-1` | **THIS BRANCH — Master SOT** | This document + `assembled_data/` with all packs |
| `main` | Approved engine + verified store | `builder/app-v3.17.0-picker.html`, 5,082 store, Build Docs |
| `arena/019fd805-the-bettor-1` | Researcher returns | KOS v2.1, KOSCUP v2.1, SPA v2 + evidence ledgers |
| `arena/019fd74a-the-bettor-1` | Auditor evidence | KOS/KOSCUP audit report (match data APPROVED, D5 returned) |
| `arena/019fd4e0-the-bettor-1` | Builder full chain | v3.7.0→v3.17.0 app builds, ITA/GER/FRA/SCO packs, handoffs |
| `arena/019fdd64-the-bettor-1` | Researcher3 returns | USOC v2.1, MLS partial, handoff reports |
| `arena/019fd71e-the-bettor-1` | Director control + design | Control SOT, seed register, clean-boot workorder, designer package |
| `arena/019fd7e1-the-bettor-1` | Designer | UI/UX design system, screen designs, implementation spec |
| `arena/019fd213-the-bettor-1` | Planner + builder | B0-B2 builds, lead_engine docs, team messages, prototype |

**All other branches** (`019fc462`, `019fd0e5`, `019fd1a3`, `019fd227`, `019fd229`, `019fd30b`, `019fd4fb`, `019fd75e`) are historical/foundational. Their work is incorporated into the above branches or superseded.

---

# PART D — REBUILD PROCEDURE (STEP BY STEP)

## Phase 1: This Branch — Assemble Truth

- [x] D1. All verified and candidate packs extracted to `assembled_data/`
- [x] D2. This SOT document written with every hash, row count, and audit status
- [ ] D3. Push this branch and open PR to main

## Phase 2: Clean Boot Build (v3.18.0)

1. Builder takes `builder/app-v3.17.0-picker.html` (md5 `e6687ad4`) as baseline
2. Removes auto-loading of all 9 `SEED_PACKS` on first boot
3. Clean boot = empty store + "No approved data loaded yet"
4. `PR.ingest` remains the only data entry gate
5. Engine math, provenance, NO CALL, settlement, one-gate — all preserved
6. Deliver: `builder/app-v3.18.0-clean-boot.html` + b64 + evidence
7. Auditor verifies: zero rows on clean boot, no seed loading, P1 clean, no network

## Phase 3: Data Close-Out

1. **Load store:** Import `pitch-rating-full-5082-D1D2-2026-08-05.json` via migration → 5,082 rows
2. **KOS D5 fix:** Researcher realigns TEAM-row fields (stadium↔surface swap, 8 rows KOS + 24 rows KOSCUP)
3. **KOS re-audit:** Auditor confirms D5 fix → KOS + KOSCUP imported → +1,033 rows (6,115 total)
4. **SPA audit:** Independent auditor verifies SPA v2 (1,900 rows, table repro, cross-diff) → approved → imported → 8,015 total
5. **ITA audit:** Same process → 1,901 rows → 9,916 total
6. **GER audit:** Same → 1,540 rows → 11,456 total
7. **FRA audit:** Same → 1,686 rows → 13,142 total
8. **Scottish audit:** SCO1 (1,140) + SCOCUP (68) + SCOLC (72) = 1,280 → 14,422 total
9. **USOC audit:** 138 rows → 14,560 total

## Phase 4: Engine Verification

1. **Productionise harness** (S0): `audit_work/backtest_harness.py` → app's masked-replay module
2. **Run L-1 through FULL ladder** on each league as data enters
3. **Monthly masked replay** cadence after data close-out
4. **M10 outcomes-only integrity screen** before any new league data enters

## Phase 5: Cross-League Bridge (S5)

1. Fresh UEFA connector pack required (prior rejected as fabricated)
2. Connector universe: UCL + UEL + UECL + qualifying rounds 2021-26, ties with ≥1 programme-league club
3. Fit-to-results loop (§6 of masterplan): league strength weights derived from actual cross-league results
4. Adopt only if weighted scale beats frozen 1.00 baseline on omitted European window

## Phase 6: UI Build (S7)

1. Designer package on `019fd7e1` / `019fd71e` provides design system, screen designs, implementation spec
2. Plain language (A-02) — no "AI-style" confidence language
3. Provenance panel on every number
4. NO CALL shows balance panel
5. One-gate data import UI

---

# PART E — NEVER DO LIST

1. Never import a pack without an independent auditor approval card
2. Never trust embedded app seed data — it is quarantine material
3. Never use KOS v2, UEFA-CONNECTOR, or UEFA-FULL packs — they are fabricated or superseded
4. Never ship a build without a measured test-run artifact
5. Never use market data (P1 — permanent)
6. Never skip the table reproduction test
7. Never reuse a previous auditor's scripts as evidence
8. Never invent a team, score, or date
9. Never merge the builder branch (`019fd4e0`) wholesale — it contains 16,629-row contaminated store
10. Never present a country as "available" unless its pack has been independently audited and imported

---

# PART F — PINS (HASHES THAT MATTER)

| Asset | MD5 | SHA-256 |
|---|---|---|
| Verified store (5,082 rows) | `3c068c1f67ee8a81d412631fd0feb162` | `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c` |
| App v3.17.0 (corrected) | `e6687ad417fd1d3229a000c12f73f1a3` | `51e275da4d2bbb3a0b198fa7f07d66ec9fd07bb965293b4c63ab8d9ea1e210d7` |
| KOS v2.1 pack | `cde3688fd0da79b0f233c6d82cb50572` | `531bc96c9bce742e97efc72fae92076a78c3e01bec7804ae0ab042b40c2bb966` |
| KOSCUP v2.1 pack | `cca71b174a7af989b43ed4cf285ca6b9` | `acf40a85d04da7e8d490e67130046fb3bfa79f64d1b640fb8f2b97df7b0afd97` |
| SPA v2 pack | `81e553a46e58f5c41b533ba2bbd7643c` | — |
| ITA v2 pack | `05344481d04be2648694944a4f6f6c3f` | — |
| GER v2 pack | `afc99d36c3d7aa3e84eb2e103800f7f0` | — |
| FRA v2 pack | `4b302b1727eedf5586366a74dd66a7cb` | — |
| SCO1 v2 pack | `2304fe1f42a191189e94ea26d8279b19` | — |
| SCOCUP v2 pack | `e7ff5ac9d20933ca848a1181dfd9d450` | — |
| SCOLC v2 pack | `1d1f065fe89edf1db9892785905bac24` | — |
| USOC v2.1 pack | `5875319c76be17ad8a1ebdb74c284550` | — |
| Backtest harness | in `audit_work/backtest_harness.py` | — |
| ENGINE_SPEC.md | md5 `91cd0cd5420cd494a799bd4050cb2ef8` | — |
| METHODOLOGY.md | md5 `6cd6c0c8ebc695a8fe3afc313ddc90ac` | — |

---

*This document is the single source of truth for the Pitch Rating project as of 2026-08-08. Every claim traces to a file, hash, or auditor report. No stories. If any other document disagrees, this one wins until it is revised with a new versioned file and updated pins.*
