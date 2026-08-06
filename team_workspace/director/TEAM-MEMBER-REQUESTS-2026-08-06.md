# TEAM MEMBER REQUESTS — 2026-08-06

**From:** Director of Intelligence  
**To:** All Team Members  
**Priority:** HIGH — Project commencement  

---

## 🚨 FIRST ASSIGNMENT: AUDITOR — PHASE 0 VERIFICATION

We are starting with the AUDITOR. This is the critical first step — before any data is trusted, before any engine work begins, we need independent verification that the existing data packs are authentic.

### Auditor Assignment: Phase 0 Source of Truth Verification

**Workorder:** `team_workspace/auditor/WORKORDER-AUDITOR-PHASE0-VERIFICATION-v1.md`

**Your Mission:** Verify 4 IMPORT-READY data packs and establish them as the single source of truth.

**Files to verify:**
| File | Declared md5 | Rows |
|---|---|---|
| RPL-2021-2026_BP-TEAM-PACK_v2.txt | c3a72b35e834cc030d62b3d160c79b25 | 732 |
| RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt | 91bce98de5ff5f999a2f03f3ee7d3caa | 189 |
| MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt | 662fe5dfe38002474855110b2a17ea6c | 120 |
| CZ1-2021-2026_BP-TEAM-PACK_v2.txt | 29c3b6c9d63906bde4db20ac4e6b742c | 841 |

**Your verification protocol:**
1. Hash every file on arrival (md5 + sha256)
2. Fresh parse with your own code (never reuse previous auditor's scripts as evidence)
3. Grammar verification (BP-TEAM-PACK v2 format)
4. Boundary verification (dates, duplicates, scores)
5. Identity verification (roster match)
6. Source verification (every row sourced)
7. **Table reproduction test** (ZERO tolerance — every club-position must match official table)
8. Cross-diff against independent sources
9. Sentinel date detection (reject if ANY 20YY-06-30 patterns found)
10. Ghost club detection (teams not in league roster)
11. 90-minute doctrine verification

**Your deliverables:**
- Audit report in `Supervior/Build Docs/AUDIT-PHASE0-VERIFICATION-2026-08-06.md`
- Log entry in `Supervior/updates/SESSION-2026-08-06-AUDIT.md`
- Fresh scripts retained in `audit_work/`

**If all pass:** Issue approval card. These 4 packs become the single source of truth.
**If any fail:** Return with specific defects. Do NOT approve partially.

---

## HOW TO CLAIM THIS ASSIGNMENT

```
To claim the Auditor Phase 0 assignment, respond with:

ROLE: Auditor
ASSIGNMENT: Phase 0 Source of Truth Verification
NAME: [Your name]
ACKNOWLEDGMENT: I have read WORKORDER-AUDITOR-PHASE0-VERIFICATION-v1.md in full and understand:
- I must use FRESH CODE for all verification
- I must HASH every file on arrival
- I must perform TABLE REPRODUCTION for every season
- I must perform CROSS-DIFF against independent sources
- I must scan for SENTINEL DATES and GHOST CLUBS
- I will NOT use prior audit as evidence (only as cross-check)
- I will document EVERYTHING with specific row numbers

Signature: _______________
Date: _______________
```

---

## FUTURE ASSIGNMENTS (Waiting for Auditor Completion)

Once the auditor completes Phase 0 verification, the following assignments become active:

### Researcher Assignments (in priority order)

| # | League | Workorder | Rows | Priority |
|---|---|---|---|---|
| 1 | SPA (in flight) | WORKORDER-SPA-2021-2026 | 1,900 | HIGH — complete existing work |
| 2 | ITA | WORKORDER-ITA-2021-2026_RIGOROUS-v1.md | 1,900 | HIGH |
| 3 | GER | WORKORDER-GER-2021-2026_RIGOROUS-v1.md | 1,530 | HIGH |
| 4 | FRA | (to be created) | 1,900 | MEDIUM |
| 5 | UEFA CONNECTOR | WORKORDER-UEFA-CONNECTOR | TBD | CRITICAL — blocks cross-border features |

### Builder Assignments (can run parallel with researchers)

| # | Step | Workorder | Priority |
|---|---|---|---|
| 1 | B0: Harness productionise | WORKORDER-BUILDER-MASTER-v1.md (B0) | HIGH — needed for testing |
| 2 | B1: Live-derive | WORKORDER-BUILDER-MASTER-v1.md (B1) | MEDIUM — after Phase 0 |
| 3 | UI/UX design | A-02 compliant design | MEDIUM — parallel with B0 |

---

## COLD-START PROCESS (For Each Team Member)

When any team member comes onboard, they go through this sequence:

```
STEP 1: Orientation (45-60 minutes)
  - Read required documents (START-HERE, COMMUNICATION-RULES, README, role-specific)
  - Understand five rules that never change
  - Understand "never" list for their role
  - Read PHASE-TASKLIST.md to understand the big picture

STEP 2: Workorder Review (10-15 minutes)
  - Read their specific workorder in full
  - Understand every gate they must pass
  - Understand where their work goes and who verifies it

STEP 3: Acknowledgment (2 minutes)
  - Sign compliance acknowledgment
  - Confirm they will not invent data, skip gates, or ship without test runs

STEP 4: Begin Work
  - Researcher: start collecting data from RSSSF
  - Builder: start building/verifying engine
  - Auditor: start fresh verification

STEP 5: Deliver
  - Researcher → handoffs/ (one .txt per workorder)
  - Builder → handoffs/ (b64 .txt + evidence artifact)
  - Auditor → Supervior/Build Docs/ + Supervior/updates/

STEP 6: Verification
  - Auditor verifies researcher returns (fresh code)
  - Auditor byte-diffs + re-runs harness for builder returns
  - Approved → import/integrate | Rejected → fix defects, re-return
```

---

## WORKFLOW SUMMARY

```
PHASE 0: Auditor verifies existing data packs (CURRENT)
    ↓
PHASE 1: Engine + UI build + verification (parallel with Phase 2+)
    ↓
PHASE 2+: Researchers collect new league data (parallel, multiple researchers)
    ↓
    As each league is verified → import → available in app immediately
    ↓
PHASE 7: Full integration when all data + engine complete
```

**Key principle:** The app becomes usable with verified leagues AS SOON AS the engine is verified — no need to wait for all data to be collected.

---

## CONTACT

All work products go to:
- **Researchers:** `handoffs/` folder in repo
- **Builder:** `handoffs/` folder (b64 .txt + evidence artifact)
- **Auditor:** `Supervior/Build Docs/` + `Supervior/updates/`

Questions: Direct to Director (this workspace).

---

*Issued: 2026-08-06 by Director of Intelligence*
