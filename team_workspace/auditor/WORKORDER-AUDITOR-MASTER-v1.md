# AUDITOR WORKORDER MASTER — Zero-Harcode Verification

**Document ID:** WORKORDER-AUDITOR-MASTER-v1  
**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**Application:** All auditor verification workorders  

---

## HOW TO USE THIS DOCUMENT

This is the MASTER TEMPLATE for all auditor workorders. The auditor is the ONLY person allowed to say "this is true" — and earns it every time.

**Core principle:** Fresh code, always. Never reuse the previous auditor's scripts as evidence — write your own parser, compare outputs. Reuse only as a cross-check.

---

## SECTION 0: PRE-WORK REQUIREMENTS

### 0.1 Read These Documents in Full

```
[REQUIRED] START-HERE-COLD-START.md
[REQUIRED] COMMUNICATION-RULES-v1.md
[REQUIRED] Supervior/ROLES/ROLE-AUDITOR.md
[REQUIRED] Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md
[REQUIRED] Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md
[REQUIRED] METHODOLOGY.md (principles, testing protocol, implementation protocol)
```

### 0.2 Confirmation

```
I, [Auditor Name], confirm I have read all required documents.
Signature: _______________
Date: _______________
```

### 0.3 The "Never" List for Auditors

You must NEVER:

- [ ] Reuse the previous auditor's scripts as evidence (fresh code only)
- [ ] Trust a file on arrival without pinning (md5/sha256 first)
- [ ] Assume — if it's not confirmed in file/output, it's not known
- [ ] Guess — no inferences presented as facts
- [ ] Import a file that failed a gate "to see what happens"
- [ ] Silent-rewrite your own instrument errors (log them with your name)
- [ ] Accept "registered" self-reports as evidence (researcher self-checks are registered, never adopted)
- [ ] Use stories instead of file/code/pin citations

---

## SECTION 1: RECEIPT PROTOCOL

### 1.1 File Receipt

```
When you receive a file:

1. RECORD receipt: filename, date received, sender, delivery method
2. HASH IMMEDIATELY: compute md5 and sha256
3. COMPARE against declared pin (if any)
4. If hash doesn't match declared pin → REJECT → notify sender
5. If no declared pin → hash becomes the working pin for this session
6. NEVER process a file before hashing
```

### 1.2 Pin Registry

```
Maintain a pin registry for every file you verify:

File: _______________
Received: _______________
md5: _______________
sha256: _______________
Declared pin: _______________
Match: YES / NO
If NO: ACTION TAKEN: _______________
```

### 1.3 Raw CDN Policy

```
[REQUIRED] Raw CDN is never trusted
[REQUIRED] Git blobs or b64-armoured files are the trusted transport
[REQUIRED] If you must use CDN data, re-host it through git or b64 first
```

---

## SECTION 2: DATA PACK VERIFICATION PROTOCOL

### 2.1 Overview

Every data pack return must pass through this protocol. Failing ANY step = return to researcher with specific defects.

### 2.2 Step 1: Grammar Verification

```
[ ] Parse every line with fresh code
[ ] Verify MATCH lines match BP-TEAM-PACK v2 format exactly
[ ] Verify TEAM lines (if present) match format
[ ] Verify SOURCE lines have valid URL, access date, type, description
[ ] Verify NOTE lines have valid tag and structure
[ ] Verify file ends with END
[ ] Verify no standings tables anywhere
[ ] Verify no zip, no paste fragments

Fail action: Return with specific line numbers and format errors.
```

### 2.3 Step 2: Boundary Verification

```
[ ] Scan for dateless rows → list any found
[ ] Scan for duplicate fingerprints (date+home+away+competition) → list any found
[ ] Scan for future-dated rows (vs today's date or export date) → list any found
[ ] Scan for non-integer scores → list any found
[ ] Scan for scores > 30 → list any found
[ ] Scan for missing required fields → list any found

Fail action: Return with specific row IDs and defect types.
```

### 2.4 Step 3: Identity Verification

```
[ ] Extract all unique home/away team strings
[ ] Compare against workorder §3 roster
[ ] List any strings not on roster
[ ] List any name variants (e.g., "Inter Milan" vs "Inter")
[ ] List any teams appearing in wrong seasons

Fail action: Return with specific team names and violations.
```

### 2.5 Step 4: Source Verification

```
[ ] Verify every MATCH row has a valid sourceLabel
[ ] Verify every sourceLabel matches a SOURCE line in the file
[ ] Verify SOURCE lines have:
  - Valid URL (test that URL is accessible or was accessible on access date)
  - Real access date (not invented)
  - Valid type (primary-archive, second-index, third-source, official-db)
  - Specific "what it verified" description
[ ] Verify primary source is appropriate for the competition
[ ] Verify second-index cross-verification was performed

Fail action: Return rows lacking sources or with invalid SOURCE lines.
```

### 2.6 Step 5: Table Reproduction Test (ZERO TOLERANCE)

```
[REQUIRED] Write fresh code to recompute standings from rows ONLY
[REQUIRED] For each season, compute:
  - Points per club (3 for win, 1 for draw, 0 for loss)
  - Goal difference (GF - GA)
  - Position order (points desc, then GD desc, then GF desc)
  - W-D-L record per club

[REQUIRED] Compare against official table from primary source:
  - Club-for-club match
  - Position-order match
  - W-D-L match
  - GF-GA match
  - Pts match

[REQUIRED] If ANY discrepancy → FAIL

Report format:
Season: [YYYY-YY]
Clubs: [N]
Recomputed table: [full table]
Official table: [full table]
Match: YES / NO
If NO: [list every discrepancy with position, club, stat]

Fail action: Return with specific season, position, and stat differences.
```

### 2.7 Step 6: Cross-Diff Against Independent Sources

```
[REQUIRED] For every row (or statistically significant sample):
  - Parse the same data from an independent source
  - Compare date, home, away, score
  - If all match → mark as verified
  - If any diff → adjudicate against third source

[REQUIRED] Document cross-diff method and sample size
[REQUIRED] Report any unresolved conflicts

Fail action: Return rows where cross-diff found unresolved conflicts.
```

### 2.8 Step 7: Sentinel Date Detection

```
[REQUIRED] Scan for rows dumped on sentinel dates (e.g., 20YY-06-30 patterns)
[REQUIRED] Check if multiple rows share identical dates in suspicious patterns
[REQUIRED] Verify dates match actual match dates from primary source

History: UEFA-FULL had 100% of main-stage rows on sentinel dates 20YY-06-30.
         KOS had all 180 rows on two dates: 2023-06-30 and 2024-06-30.

Fail action: If sentinel dates detected → REJECT entire pack as likely fabricated.
```

### 2.9 Step 8: Ghost Club Detection

```
[REQUIRED] For each team in the pack, verify it existed in the competition that season
[REQUIRED] Cross-reference against official league roster for that season
[REQUIRED] Flag any team that:
  - Never existed in that competition
  - Was not in that division that season
  - Is a renamed version of another team without disclosure

History: KOS had ghost clubs Ferizaj and Suhareka that were not in 2023-24 Superliga.

Fail action: If ghost clubs detected → REJECT entire pack.
```

### 2.10 Step 9: Score Verification (Knockout/European Matches)

```
[REQUIRED] For knockout ties and European matches:
  - Verify scores against UEFA.com or official competition site
  - Verify 90-minute doctrine: AET/pens = 90' score + NOTE|info|advancement
  - Verify correct leg identification (leg 1 vs leg 2)
  - Verify aggregate scores if reported

History: UEFA-FULL had fabricated scores:
  - PSG 4-3 Arsenal (final) → actual: 1-1, 4-3 pens
  - City–Madrid leg2 mirrored instead of real 3-0
  - PSG 5-2 Chelsea invented

Fail action: If scores don't match official records → REJECT pack.
```

### 2.11 Step 10: Approval Decision

```
After completing all steps:

If ALL steps pass:
  → Issue ONE approval card
  → Card must include: pack ID, row count, verification method, date, auditor name
  → Card is the only approval document

If ANY step fails:
  → Return to researcher with EXACT defect list
  → Include: step Failed, specific rows/values, expected vs actual
  → Do NOT approve partially

APPROVAL CARD FORMAT:
========================================
APPROVAL CARD — [Pack ID]
========================================
Date: [YYYY-MM-DD]
Auditor: [Name]
Pack: [filename]
Rows: [count]
Verification method: [brief description]
Gates passed: [list]
Table reproduction: [season-by-season result]
Cross-diff: [method and result]
Sentinel date scan: [pass/fail]
Ghost club scan: [pass/fail]
Score verification: [pass/fail / N/A]
========================================
APPROVED / REJECTED
========================================
```

---

## SECTION 3: BUILD VERIFICATION PROTOCOL

### 3.1 Overview

Every builder return must pass through this protocol. Failing ANY step = return to builder with specific defects.

### 3.2 Step 1: Byte-Diff Against Baseline

```
[ ] Compute md5 of submitted build file
[ ] Compute md5 of pinned baseline (e.g., builder/app-v3.17.0-picker.html = d71b042308b0637a81d22ee75795f419 for the current correction assignment)
[ ] Perform byte-diff
[ ] Document every change
[ ] Verify changes match what builder claims to have built

Fail action: Return if diff doesn't match claimed changes.
```

### 3.3 Step 2: P1 Grep (No Market Data)

```
[ ] Grep for: fetch, XMLHttpRequest, http, https, www., com/, odds, price, market, bookmaker, bet, wager
[ ] Count must be 0 for market-related terms
[ ] Any market data reference → FAIL

Fail action: Return with specific line numbers and terms found.
```

### 3.4 Step 3: No-Network Grep

```
[ ] Grep for: fetch, XMLHttpRequest, $.ajax, axios, httpRequest
[ ] Count must be 0
[ ] Any network call → FAIL

Fail action: Return with specific line numbers.
```

### 3.5 Step 4: One-Gate Grep

```
[ ] Verify single ingest gate exists
[ ] Verify no side doors (hidden inputs, alternate pathways)
[ ] Verify all data enters through the same gate

Fail action: Return if multiple gates or side doors found.
```

### 3.6 Step 5: Test-Run Ladder Re-Run

```
[REQUIRED] Run the test-run ladder on the builder's build:
  - L-1: Train to newest−1, predict newest
  - L-2: Hold out newest 2, test both
  - L-n: Expand holdout
  - FULL: Full-system check

[REQUIRED] Compare builder's claimed numbers against your re-run
[REQUIRED] If numbers don't match → investigate why
[REQUIRED] If build degrades performance → return with specific metrics

Fail action: Return with specific metrics that failed.
```

### 3.7 Step 6: Acceptance Pin Verification

```
[ ] Version bump occurred (not shipping on old version)
[ ] No network calls introduced
[ ] One gate maintained
[ ] Artifact present (test-run output)

Fail action: Return if any acceptance pin missing.
```

### 3.8 Step 7: Build Approval

```
APPROVAL CARD FORMAT:
========================================
BUILD APPROVAL CARD — [Step ID]
========================================
Date: [YYYY-MM-DD]
Auditor: [Name]
Builder: [Name]
Build file: [filename]
Build md5: [md5]
Baseline md5: [md5]
Byte-diff: [summary of changes]
P1 grep: PASS / FAIL
No-network grep: PASS / FAIL
One-gate grep: PASS / FAIL
Test-run ladder: PASS / FAIL
  L-1 result: [metrics]
  L-2 result: [metrics]
  FULL result: [metrics]
Artifact present: YES / NO
========================================
APPROVED / REJECTED
========================================
```

---

## SECTION 4: STORE AUDIT PROTOCOL

### 4.1 Store Change Audit

```
Every store change must be audited:

1. HASH: Compute md5/sha256 of store before and after change
2. CENSUS: Count rows by competition, season
3. FINGERPRINTS: Check for duplicates
4. DATE SANITY: Check for future dates, sentinel dates
5. LOG RECONCILIATION: Verify store.log entries match actual changes
```

### 4.2 Store Import Audit

```
When a pack is imported into the store:

1. Verify pack was approved (valid approval card exists)
2. Verify import order (some packs must land before others)
3. Verify expected row count after import
4. Re-run fingerprint check on new store
5. Re-run date sanity check on new store
6. Update pin registry with new store hash
```

### 4.3 Store Purge Audit

```
Before any purge:

1. BACKUP FIRST: Create backup of current store
2. Document what is being purged and why
3. After purge: verify only specified rows removed
4. Verify undo path: backup can restore

Rule: Undo = load the backup. There is no other undo.
```

---

## SECTION 5: INSTRUMENTS AND SCRIPTS

### 5.1 Fresh Code Requirement

```
[REQUIRED] Every verification must use fresh code written by you
[REQUIRED] Never reuse previous auditor's scripts as evidence
[REQUIRED] You may reuse as cross-check, but not as primary evidence
[REQUIRED] Your scripts must be kept in audit_work/ for re-run
```

### 5.2 Instrument Self-Verification

```
Before trusting your instrument's output:

[REQUIRED] Test that your instrument can distinguish correct from incorrect data
[REQUIRED] Test your instrument on known-correct and known-incorrect data
[REQUIRED] Document your instrument's bug fixes
[REQUIRED] Your instrument's bugs get fixed and logged, never touch pack verdict unless re-run

Quote from ROLE-AUDITOR.md:
"A test that cannot distinguish Array.push() from a void-bet is not a test."
```

### 5.3 Required Scripts

```
Maintain these scripts in audit_work/:

[ ] pack_parse.py — Parse BP-TEAM-PACK v2 files
[ ] rsssf_verify.py — Verify against RSSSF sources
[ ] legacy_diff.py — Cross-diff against legacy datasets
[ ] backtest_harness.py — Run test-run ladder
[ ] [league-specific scripts as needed]

Every script must be:
- Freshly written or verified as still correct
- Documented with what it verifies and how
- Re-runnable by anyone
```

---

## SECTION 6: REPORTING REQUIREMENTS

### 6.1 Audit Report Format

```
Every audit report must include:

1. WHAT was audited (file/pack/build identifier)
2. HOW it was audited (method, scripts, sources)
3. WHAT WAS FOUND (specific results, not summaries)
4. VERDICT (approve/reject with specific reasoning)
5. PINS (md5/sha256 of all files referenced)
6. ERRATA (any instrument errors, logged with your name)

Every assertion must cite: a file, a code line, or a pin.
No stories.
```

### 6.2 Log Requirements

```
Maintain audit log in Supervior/updates/SESSION-*.md:

[REQUIRED] Every finding, dated
[REQUIRED] Every decision, dated
[REQUIRED] Every defect found, with specific rows/values
[REQUIRED] Every approval, with card reference
[REQUIRED] Every rejection, with defect list reference
```

---

## SECTION 7: COMPLIANCE ACKNOWLEDGMENT

```
I, [Auditor Name], acknowledge:

1. I have read all required documents in full
2. I understand that I am the ONLY person allowed to say "this is true"
3. I will NEVER reuse previous auditor's scripts as evidence
4. I will NEVER trust a file without hashing it first
5. I will NEVER assume — if it's not in file/output, it's not known
6. I will NEVER guess — no inferences as facts
7. I will NEVER silent-rewrite my own instrument errors
8. I will NEVER accept "registered" self-reports as evidence
9. I will NEVER use stories instead of file/code/pin citations
10. I understand that my own bugs get fixed and logged, never touch verdict unless re-run

Auditor signature: _______________
Date: _______________
```

---

*End of Auditor Workorder Master v1*
*This document is binding for all auditor verification workorders.*
