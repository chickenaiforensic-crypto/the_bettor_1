# COLD-START PACKAGE — Team Member Onboarding

**For:** All new team members (Researcher, Builder, Auditor)  
**Branch:** arena/019fd75e-the-bettor-1 (PR #3) 
**Date:** 2026-08-06  
**Director:** Intelligence Coordination  

---

## HOW TO USE THIS PACKAGE

This is your complete cold-start kit. Follow these steps IN ORDER. Do not skip steps.

```
Estimated time: 45-60 minutes for full orientation
```

---

## STEP 1: READ THESE DOCUMENTS (IN ORDER)

### 1.1 Mandatory Reading (All Roles)

| # | Document | Location | Purpose |
|---|---|---|---|
| 1 | COMMUNICATION-RULES-v1.md | repo root | How we talk and work (binding) |
| 2 | START-HERE-COLD-START.md | repo root | Operations runbook, standing truths, what NEVER to do |
| 3 | README.md | repo root | The map: who works where, five rules that never change |

### 1.2 Role-Specific Reading

**IF YOU ARE A RESEARCHER:**
| # | Document | Location |
|---|---|---|
| 4 | ROLE-RESEARCHER.md | Supervior/ROLES/ |
| 5 | WORKORDER-RESEARCHER-MASTER-v1.md | team_workspace/researcher_handoffs/ |
| 6 | Your specific league workorder (e.g., WORKORDER-ITA-2021-2026_RIGOROUS-v1.md) | team_workspace/researcher_handoffs/ |

**IF YOU ARE A BUILDER:**
| # | Document | Location |
|---|---|---|
| 4 | ROLE-BUILDER.md | Supervior/ROLES/ |
| 5 | WORKORDER-BUILDER-MASTER-v1.md | team_workspace/builder/ |
| 6 | ENGINE-MASTERPLAN-2026-08-05.md | Supervior/Build Docs/ |
| 7 | MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md | Supervior/updates/ |

**IF YOU ARE AN AUDITOR:**
| # | Document | Location |
|---|---|---|
| 4 | ROLE-AUDITOR.md | Supervior/ROLES/ |
| 5 | WORKORDER-AUDITOR-MASTER-v1.md | team_workspace/auditor/ |
| 6 | VERIFICATION-DATA-2026-08-05.md | Supervior/Build Docs/ |
| 7 | BLUEPRINT-SOT-2026-08-04.md | Supervior/Build Docs/ |

### 1.3 Understanding the Project

| # | Document | Location |
|---|---|---|
| 8 | PHASE-TASKLIST.md | team_workspace/director/ |
| 9 | external-audit-2026-08-06.md | team_workspace/intel_audit/ |
| 10 | findings_summary.md | team_workspace/intel_audit/ |

---

## STEP 2: UNDERSTAND THE CORE PRINCIPLES

### The Five Rules That Never Change

1. **Results only.** No market data in any role (P1).
2. **One gate.** All data enters through the app's ingest gate; rejections never stored.
3. **Approval = test run.** A system is adopted only when it wins the harness on the last-omitted window.
4. **Backup first.** Purge/import flows are backup-gated; undo = load the backup.
5. **No silent rewrites.** Changed numbers/decisions get a dated log entry.

### The "Never" List (ALL ROLES)

- [ ] Never use bookmaker odds, market data, prices, spreads in ANY role
- [ ] Never invent a team, score, or date
- [ ] Never deliver a file that failed a gate "to see what happens"
- [ ] Never guess at unverifiable data — write `NOTE|warning|blocker` instead
- [ ] Never reuse the previous auditor's scripts as evidence (auditors only)
- [ ] Never ship without a measured test run artifact (builders only)
- [ ] Never skip the table reproduction test (researchers only)
- [ ] Never assume — if it's not confirmed in file/output, it's not known

### What "Zero-Harcode" Means

The system is designed so that once we have verified team data, we can test/compute against the engine and recalibrate if necessary. No hardcoded predictions. No hardcoded team strengths. Everything computed from verified match results.

---

## STEP 3: YOUR WORKSPACE

### Where You Work

| Role | Your Workspace | Where Work Goes |
|---|---|---|
| **Researcher** | Your own session + repo access | `handoffs/` — one .txt per workorder |
| **Builder** | Your own session + repo access | `handoffs/` — b64 .txt + evidence artifact |
| **Auditor** | `audit_work/` (scripts) + `Supervior/Build Docs/` (reports) | Reports in `Supervior/Build Docs/` + log in `Supervior/updates/` |

### Your Role in the System

```
DATA FLOW:
Researcher collects data → returns .txt to handoffs/
     ↓
Auditor verifies with fresh code → approval card or defect list
     ↓
Owner imports through app's ingest gate → store
     ↓
Builder builds/verifies engine → test-run artifacts
     ↓
App uses verified store + verified engine → predictions
```

### Your Boundaries

- **Researcher:** You collect data. You do NOT decide what is true. You record what sources say. Auditor verifies.
- **Builder:** You build/verify engine. You do NOT ship without test-run artifact. Auditor byte-diffs + re-runs harness.
- **Auditor:** You verify. You are the ONLY person allowed to say "this is true." You earn it every time with fresh code.

---

## STEP 4: YOUR WORKORDER

### Locate Your Workorder

Your workorder tells you EXACTLY what to do, what gates you face, and what deliverable you produce.

**Researchers:** See `team_workspace/researcher_handoffs/WORKORDER-*-RIGOROUS-v1.md`  
**Builders:** See `team_workspace/builder/WORKORDER-BUILDER-MASTER-v1.md`  
**Auditors:** See `team_workspace/auditor/WORKORDER-AUDITOR-MASTER-v1.md`

### Read Your Workorder IN FULL

Do not skim. The last audit that skimmed missed 11 date errors (found later, fixed).

### Sign Your Acknowledgment

At the end of your workorder is a compliance acknowledgment. Sign it before starting work.

---

## STEP 5: YOUR FIRST TASK

### For Researchers

```
YOUR FIRST TASK: [Specific league pack]

Steps:
1. Federation check: verify all clubs are from the correct competition
2. Parse primary source (RSSSF) for every match
3. Cross-verify every round against second index
4. Perform table reproduction test for EVERY season
5. Document every source with URL + access date
6. Return file to handoffs/

DO NOT START until you have:
- Read your workorder in full
- Signed the acknowledgment
- Understood every gate you must pass
```

### For Builders

```
YOUR FIRST TASK: Correct defects in builder/app-v3.17.0-picker.html

Steps:
1. Pull builder/app-v3.17.0-picker.html from arena/019fd4fb-the-bettor-1
2. Verify md5: d71b042308b0637a81d22ee75795f419
3. Read the audit report (Supervior/Build Docs/AUDIT-V3.17.0-PICKER-2026-08-06.md)
4. Correct defects listed in audit report (P1 market data, star_hyst)
5. Run test-run ladder to verify no degradation
6. Produce b64 .txt + evidence artifact
7. Return to handoffs/
8. Push to BOTH your branch AND arena/019fd75e-the-bettor-1

DO NOT START until you have:
- Read your workorder in full
- Read MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md
- Signed the acknowledgment
- Verified baseline pin (md5 d71b042308b0637a81d22ee75795f419)
```

### For Auditors

```
YOUR FIRST TASK: [Specific verification]

Steps:
1. Receive file from researcher/builder
2. HASH IMMEDIATELY (md5 + sha256)
3. Compare against declared pin (if any)
4. Write fresh parser (never reuse previous auditor's scripts as evidence)
5. Run verification protocol (grammar → boundary → identity → source → table repro → cross-diff)
6. Issue approval card OR return with defect list
7. Log everything in Supervior/updates/SESSION-*.md

DO NOT START until you have:
- Read your workorder in full
- Understood "fresh code, always" rule
- Located your audit scripts in audit_work/
- Signed the acknowledgment
```

---

## STEP 6: TOOLS AND REFERENCES

### For Researchers

| Tool | Purpose | Location |
|---|---|---|
| RSSSF | Primary source for match data | rsssf.org |
| worldfootball.net | Second-index cross-verification | worldfootball.net |
| Pack format spec (DELIVER-02) | BP-TEAM-PACK v2 grammar | OWNER-OUTBOX/DELIVER-02/ |
| Existing verified packs | Examples of correct format | previous_work_files/.../DATA-PACKS/IMPORT-READY-2026-08-03/ |

### For Builders

| Tool | Purpose | Location |
|---|---|---|
| builder/app-v3.17.0-picker.html | Current baseline to correct | arena/019fd4e0 or arena/019fd4fb branch, builder/ folder |
| Backtest harness | Test-run ladder instrument | audit_work/backtest_harness.py |
| calibration_module.js | Engine constants (PR.calibration) | builder/ folder in build branch |
| ENGINE_SPEC.md | Engine constants and layers | Arena workspace uploads/ |
| METHODOLOGY.md | Principles and protocols | Arena workspace uploads/ |

### For Auditors

| Tool | Purpose | Location |
|---|---|---|
| pack_parse.py | Parse BP-TEAM-PACK v2 files | audit_work/ |
| rsssf_verify.py | Verify against RSSSF | audit_work/ |
| legacy_diff.py | Cross-diff against legacy | audit_work/ |
| backtest_harness.py | Run test-run ladder | audit_work/ |

---

## STEP 7: COMMUNICATION

### How to Report

```
Researcher returns: handoffs/ folder (one .txt per workorder)
Builder returns: handoffs/ folder (b64 .txt + evidence artifact)
Auditor reports: Supervior/Build Docs/ + Supervior/updates/SESSION-*.md
```

### How to Ask Questions

1. **Audit first** — check if the system already answers your question
2. **One direct question** — no proceeding blind
3. **Ask when unclear** — don't guess

### Escalation

| Situation | Escalate To |
|---|---|
| Source conflict you can't resolve | Auditor |
| Gate failure you can't fix | Auditor + Director |
| Blocker you can't work around | Director |
| App bug you found | Builder + Auditor |
| Data you believe is missing/wrong | Auditor (don't fix it yourself) |

---

## STEP 8: YOUR SIGN-OFF

Before starting work, complete this sign-off:

```
COLD-START ACKNOWLEDGMENT

I, [NAME], confirm:

1. I have read all required documents for my role (listed in Step 1)
2. I understand the five rules that never change
3. I understand the "never" list for my role
4. I have read my workorder in full
5. I understand every gate I must pass
6. I understand where my work goes and who verifies it
7. I will NOT invent data, skip gates, or ship without test runs
8. I will ask when unclear rather than guess

Role: [Researcher/Builder/Auditor]
Assignment: [Specific workorder]
Date: [DATE]

Signature: _______________
```

---

## QUICK REFERENCE CARD

### If You're a Researcher
- **Your job:** Collect match data from RSSSF + cross-verify
- **Your deliverable:** One .txt file per league, BP-TEAM-PACK v2 format
- **Your gates:** Grammar, boundary, identity, source, table reproduction, shape, 90-min doctrine, continuity
- **Your rule:** Never invent, never guess, always document sources
- **Your destination:** handoffs/ folder

### If You're a Builder
- **Your job:** Build/verify engine components, produce test-run artifacts
- **Your deliverable:** b64 .txt app file + evidence artifact
- **Your gates:** P1 grep, no-network grep, one-gate, test-run ladder, acceptance pins
- **Your rule:** Approval = test run, not documentation
- **Your destination:** handoffs/ folder

### If You're an Auditor
- **Your job:** Verify everything with fresh code
- **Your deliverable:** Approval cards or defect lists
- **Your gates:** Fresh parse, table reproduction, cross-diff, sentinel date scan, ghost club scan
- **Your rule:** Fresh code, always. You are the only one who can say "this is true."
- **Your destination:** Supervior/Build Docs/ + Supervior/updates/

---

*End of Cold-Start Package*
*Return to Director when you have completed Step 8 and are ready to begin work.*
