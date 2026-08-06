# BUILDER WORKORDER MASTER — Zero-Harcode Engine Build

**Document ID:** WORKORDER-BUILDER-MASTER-v1  
**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**Application:** All builder engine build workorders  

---

## HOW TO USE THIS DOCUMENT

This is the MASTER TEMPLATE for all builder workorders. Every specific build step (B0-B7) is a filled-in instance of this template.

**Core principle:** Approval = test run. No system ships on documentation. Every build must pass the test-run ladder with measured numbers.

---

## SECTION 0: PRE-WORK REQUIREMENTS

### 0.1 Read These Documents in Full

```
[REQUIRED] START-HERE-COLD-START.md
[REQUIRED] COMMUNICATION-RULES-v1.md
[REQUIRED] Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md
[REQUIRED] Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md
[REQUIRED] Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md
[REQUIRED] builder/README-BUILDER.md
[REQUIRED] ROLE-BUILDER.md
```

### 0.2 Confirmation

```
I, [Builder Name], confirm I have read all required documents.
Signature: _______________
Date: _______________
```

### 0.3 The "Never" List for Builders

You must NEVER:

- [ ] Include market data (prices, odds, spreads) in any form — input, feature, benchmark, or fallback (P1)
- [ ] Ship without a measured test run artifact
- [ ] Claim "approved on documentation" as approval
- [ ] Hide machine provenance behind "AI-style" confidence language (A-02)
- [ ] Force a number when the system should say "I don't know" (P3)
- [ ] Use fetch/XHR/http for network calls (zero network dependency, I6)
- [ ] Edit probabilities with display-only components (L4/L5/R3 must not edit L1-L3)
- [ ] Deliver raw .html files (b64-armoured .txt only for transport)

---

## SECTION 1: BUILD ENVIRONMENT SETUP

### 1.1 Cold Start Procedure

```
1. Read START-HERE-COLD-START.md in full
2. Locate the baseline specified in your workorder (e.g., builder/app-v3.17.0-picker.html for defect correction; or a different baseline for new builds)
3. Verify md5 of baseline matches the expected value in your workorder
4. Set up your working directory
5. Document your environment (browser, OS, any tools used)
```

### 1.2 Baseline Pin Verification

```
Baseline file: [FROM YOUR WORKORDER — e.g., builder/app-v3.17.0-picker.html]
Expected md5: [FROM YOUR WORKORDER — e.g., d71b042308b0637a81d22ee75795f419]
Actual md5: ______
Match: YES / NO

If NO: STOP. Do not proceed with wrong baseline.
```

---

## SECTION 2: BUILD SPECIFICATION

### 2.1 What You Are Building

```
Build step: [B0-B7 from masterplan §8]
Step name: [e.g., S0: Universal Backtest Harness]
Masterplan reference: ENGINE-MASTERPLAN-2026-08-05.md §8
SOT ledger reference: BLUEPRINT-SOT-2026-08-04.md §10 (M1-M20)
```

### 2.2 Input Requirements

```
[REQUIRED] List every input your build needs
[REQUIRED] Verify every input exists and is accessible
[REQUIRED] Document input versions/pins
```

### 2.3 Output Requirements

```
[REQUIRED] List every output your build produces
[REQUIRED] Specify output format
[REQUIRED] Specify where output goes
```

### 2.4 Code Requirements

```
[REQUIRED] All code must be in the app file (single HTML file, no external dependencies)
[REQUIRED] No network calls (fetch/XHR/http must all be 0)
[REQUIRED] One ingest gate, no side doors
[REQUIRED] P1 grep: zero market data references
```

---

## SECTION 3: IMPLEMENTATION REQUIREMENTS

### 3.1 Fidelity Requirement (I1)

```
Your shipped code must reproduce the validated engine exactly.

[REQUIRED] For engine components: verify against ENGINE_SPEC.md constants
[REQUIRED] Document any spec-vs-code differences (write them down, never smooth over)
[REQUIRED] Legacy record: 0.00e+00 across 7 quantities (browser vs trainer)
[REQUIRED] Your implementation must match this fidelity standard
```

### 3.2 Test Coverage Requirement (I2)

```
[REQUIRED] Your build must include test coverage
[REQUIRED] Map your tests onto the programme's protocol suites:
  - Core tests
  - Update tests
  - Sync tests
  - Stars/consensus tests
  - Blueprint compliance tests
  - Engine compliance tests
[REQUIRED] Document your test suite mapping
```

### 3.3 Market Gating Requirement (I3)

```
[REQUIRED] Ship ≤2.7% error rate
[REQUIRED] Caution band: 3.0-3.3% must be labeled as caution
[REQUIRED] BTTS: withheld at 6.0% (must remain absent)
```

### 3.4 Venue Integrity Requirement (I4)

```
[REQUIRED] Never trust parsed venue
[REQUIRED] Hard error if home team never hosted in league
[REQUIRED] Tick-box vs official list
[REQUIRED] Save disabled until confirmed
[REQUIRED] Venue locked at entry
```

### 3.5 Scoring Rule Requirement (I5)

```
[REQUIRED] Draw = loss for home-win call (never a push, never excluded)
[REQUIRED] Settlement ledger must enforce this
[REQUIRED] Log & Settlement tab must exist
```

### 3.6 Zero Network Requirement (I6)

```
[REQUIRED] fetch/XHR/http count = 0
[REQUIRED] Updates via validated file/paste intake only
[REQUIRED] Single static file
```

---

## SECTION 4: TEST-RUN LADDER (APPROVAL BY MEASURED TEST)

### 4.1 Ladder Protocol (From Owner Doctrine 2026-08-05)

```
L-1:  Train 2021 → (newest game − 1); predict newest game; calibrate constants
      until prediction matches.

L-2:  Hold out newest 2 games; retrain on all before; test on both; readjust.

L-n:  Expand holdout (3, 4, … or one matchday at a time) until covers whole last season.

FULL: Full-system accuracy check, all leagues, complete metric set (T4), paired (T1),
      with n and MDE (T2). Any degradation → adjust designated constant → re-run from L-1.
      When constants stop needing adjustment as holdout grows → CALIBRATED → APPROVED.
```

### 4.2 Required Metrics (T4 — Complete Output Measurement)

```
[REQUIRED] Home win Brier score
[REQUIRED] Draw Brier score
[REQUIRED] Away win Brier score
[REQUIRED] 1X2 Brier score (combined)
[REQUIRED] Log loss
[REQUIRED] Calibration (error percentage)
[REQUIRED] Direction accuracy (%)
[REQUIRED] n (number of matches)
[REQUIRED] Minimum detectable effect (MDE)
[REQUIRED] Train window specification
[REQUIRED] Holdout window specification
[REQUIRED] Date of run
```

### 4.3 Paired Test Requirement (T1)

```
[REQUIRED] Use paired tests for model comparison (per-match differences)
[REQUIRED] Never use unpaired tests on paired data
[REQUIRED] Report per-match differences, not resampled absolutes
```

### 4.4 Artifact Requirements

```
[REQUIRED] Every test run must produce a numbers artifact
[REQUIRED] Artifact must include: train window, holdout, n, all metrics, date
[REQUIRED] Artifact is the approval record
[REQUIRED] Numbers in chat are NOT approval
```

---

## SECTION 5: BUILD STEPS (BY STEP)

### B0: S0 — Universal Backtest Harness (Productionise)

```
Input: audit_work/backtest_harness.py (exists, needs productionising)
Output: Production-ready harness with rolling-origin, paired stats, MDE, full metric set, artifact output

Requirements:
[ ] Harness self-check vs §5.2 numbers from masterplan
[ ] Rolling-origin validation (≥4 expanding splits, T3)
[ ] Paired statistics (T1)
[ ] Minimum detectable effect reporting (T2)
[ ] Complete metric set (T4)
[ ] Artifact output (JSON/txt with all required fields)
[ ] Works on current store (5,000+ verified rows)

Gates:
[ ] Harness produces correct numbers on known test cases
[ ] Artifact format is machine-readable and complete
[ ] No network calls
```

### B1: S1 — LIVE-DERIVE-01 (Live Re-Derive + Auto Re-Validation)

```
Input: Verified store (5,082 rows after D-2)
Output: App with live DC fit, auto re-validation on data change, provenance panel

Requirements:
[ ] Live DC fit per league (not carried parameters)
[ ] Auto re-validation when data changes (M1)
[ ] Provenance panel on every number (M3): source, window, n, calibration, date
[ ] Retire __DC_GATE__/legacy blob to provenance text (G14)
[ ] Live form stars from store or "not rated yet" (G17)
[ ] EPL rating source: bootstrap → live revalidation attempt (G16)

Gates:
[ ] G14: Live derive works on all sufficient leagues
[ ] G15: Provenance panel shows on every output
[ ] G16: EPL revalidation attempt completed
[ ] G17: Form stars live or "not rated yet" (not null)
```

### B2: S2 — Settlement/Venue Audit

```
Input: App with settlement and entry surfaces
Output: Verified I4/I5 enforcement

Requirements:
[ ] I5: Draw = loss for home call enforced on settlement tab
[ ] I4: Entry-side flip guard (hard error if home team never hosted)
[ ] Both surfaces audited this session

Gates:
[ ] M17: Settlement tab enforces draw=loss
[ ] M17: Entry surface has venue flip guard
```

### B3: S3 — Balance Panel

```
Input: Evidence engine with NO CALL capability
Output: NO CALL shows home/draw/away support shares

Requirements:
[ ] Balance panel shows on every NO CALL
[ ] Support shares: home%, draw%, away%
[ ] Panel is visible, not hidden

Gates:
[ ] M7: Balance panel complete and visible
```

### B4: S4 — Goal-Range Bins

```
Input: goalsGrid with calibration data
Output: 0-1 / 2 / 3+ goal bins with own calibration

Requirements:
[ ] Separate calibration for each bin
[ ] Held-out win required before adoption
[ ] After M7 (balance panel)

Gates:
[ ] M8: Bin calibration complete
[ ] Harness win vs current best on omitted window
```

### B5: S5 — Cross-Border Bridge

```
Input: UEFA CONNECTOR pack (Phase 4 deliverable)
Output: Weighted cross-league rating bridge

Requirements:
[ ] UEFA connector data in store (2021-26, ties with ≥1 programme-league club)
[ ] Fit-to-results loop (masterplan §6): bias measurement → weight adjustment → iteration
[ ] Weighted scale vs frozen 1.00 baseline on omitted European window
[ ] Adopt ONLY if wins on Brier/RMSE/direction, paired, on omitted window
[ ] If not: stay silent with "no calibrated bridge" label (P3)

Gates:
[ ] A-08: Weighted scale beats frozen 1.00 baseline on omitted window
[ ] If not approved: chain evidence view remains, no weighted bridge
```

### B6: S6 — Calibration Cadence

```
Input: App with masked replay capability
Output: One-click masked replay + monthly full sweep

Requirements:
[ ] One-click masked replay after every data change
[ ] Monthly full harness sweep
[ ] Calibration artifacts regenerated automatically

Gates:
[ ] M5: Replay run produces current artifacts
[ ] M6: TeamStats cache populated
```

### B7: S7 — UI/Architecture Build

```
Input: Verified engine + verified data
Output: Human-first presentation layer

Requirements:
[ ] Plain language in UI (A-02)
[ ] Machine strings in small-print "technical details" only
[ ] Provenance small-print on every number
[ ] Performance & accessibility considerations

Gates:
[ ] A-02: UI presents plain language, not "AI-style" confidence
[ ] Provenance visible but not overwhelming
```

---

## SECTION 6: TRANSPORT REQUIREMENTS

### 6.1 File Format

```
[REQUIRED] App file: b64-armoured .txt (never raw .html)
[REQUIRED] Evidence artifact: .json or .txt with all required fields
[REQUIRED] Filename format: <STEP>-<version>-<md5prefix>.b64.txt
[REQUIRED] Evidence filename: <STEP>-EVIDENCE-<date>.json/.txt
```

### 6.2 Delivery Location

```
[REQUIRED] handoffs/ folder in repo
[REQUIRED] Or specified delivery channel
```

### 6.3 Pre-Delivery Verification

```
[ ] md5 of b64 file computed before delivery
[ ] md5 verified after delivery (no transport corruption)
[ ] Evidence artifact complete with all required fields
[ ] No test-run numbers asserted without artifact
```

---

## SECTION 7: POST-BUILD PROCESS

### 7.1 What Happens After You Return

1. Auditor byte-diffs your build against pinned baseline
2. Auditor runs P1 grep (zero market data)
3. Auditor runs no-network grep (zero fetch/XHR/http)
4. Auditor runs one-gate grep (single ingest gate)
5. Auditor re-runs test-run ladder on your build
6. Auditor verifies acceptance pins (version bump, no network, one gate, artifact present)
7. Owner UAT
8. Sealed

**Rule:** A build that fails its test run comes back with the exact numbers that failed.

### 7.2 Version Bump

```
[REQUIRED] Every ship bumps the SOT pin (§14)
[REQUIRED] ZONES log entry for every decision/event
[REQUIRED] No silent rewrites
```

---

## SECTION 8: COMPLIANCE ACKNOWLEDGMENT

```
I, [Builder Name], acknowledge:

1. I have read all required documents in full
2. I understand that approval = measured test run, not documentation
3. I will NEVER include market data in any form (P1)
4. I will NEVER ship without a complete test-run artifact
5. I will NEVER hide provenance behind "AI-style" confidence language (A-02)
6. I will NEVER force a number when the system should say "I don't know" (P3)
7. I will deliver b64-armoured .txt, not raw .html
8. I understand my build will be byte-diffed and test-run by the auditor
9. I understand that if my build fails its test run, it comes back with exact failure numbers

Builder signature: _______________
Date: _______________
```

---

*End of Builder Workorder Master v1*
*This document is binding for all builder engine build workorders.*
