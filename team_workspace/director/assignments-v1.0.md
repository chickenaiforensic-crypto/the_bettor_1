# DIRECTOR ASSIGNMENTS — Active Task Queue

**Director:** Intelligence Coordination  
**Date:** 2026-08-06  
**Status:** Active coordination phase  

---

## PRIORITY 1: AUDIT COMPLETION (Current Focus)

### Task: Finalize External Audit Report
- **Assigned to:** Director (synthesizing prior auditor findings)
- **Status:** IN PROGRESS — compiling findings
- **Deliverable:** `intel_audit/external-audit-2026-08-06.md`
- **Source material:** Prior auditor's findings (provided in session context)

---

## PRIORITY 2: TEAM COORDINATION

### Task: Researcher Assignments
- **Need to assign:** 10 queued workorders + SPA continuation
- **Priority order:**
  1. SPA (in flight — parser fixed, needs completion)
  2. ITA (next in queue per INDEX)
  3. GER
  4. FRA
  5. SCO1
  6. SCOCUP
  7. SCOLC
  8. MLS
  9. USOC
  10. KOS (HALT — flagged fabricated, needs replacement)
  11. KOSCUP (HALT — dependent on KOS fix)
  12. UEFA-CONNECTOR (HALT — prior version rejected)

### Task: Builder Coordination
- **Queue:** B0-B7 all queued
- **Dependency:** B5 (cross-border bridge) needs UEFA-CONNECTOR data first
- **Priority:** B0 (harness productionise) → B1 (live derive) → others

### Task: Auditor Briefing
- **Need:** Fresh audit scripts for incoming packs
- **Focus:** SPA completion verification, then ITA

---

## TEAM MEMBER REQUESTS

I need to request the following team members to report in:

| Role | Needed For | Urgency |
|---|---|---|
| Researcher (SPA) | Complete La Liga pack — parser fixed, ledgers + pack remaining | HIGH — in flight |
| Researcher (domestic) | Pick up ITA, GER, FRA from queue | MEDIUM |
| Researcher (UEFA) | NEW clean UEFA connector pack (prior rejected) | HIGH — blocks B5 |
| Builder | B0 harness productionise, then B1 live-derive | MEDIUM |
| Auditor | Verify SPA completion, prepare for ITA | HIGH — gate before import |

---

## DIRECTOR DECISION LOG

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-06 | KOS pack REJECTED — fabricated | Ghost clubs, 0/10 table reproduction, sentinel dates |
| 2026-08-06 | UEFA-FULL REJECTED — fabricated | Fake scores (PSG 4-3 Arsenal), sentinel dates, missing rounds |
| 2026-08-06 | UEFA-CONNECTOR prior version REJECTED | "Dates fixed" claim false; 1,388/1,390 sentinel-dated |
| 2026-08-06 | 8 domestic packs VERIFIED — adoptable | Row-level identical to RSSSF-verified packs |

---

## SYNCHRONIZATION NOTES

When team members complete work:
1. Researcher drops `.txt` in `handoffs/`
2. Builder drops b64 `.txt` + evidence in `handoffs/`
3. Auditor verifies → reports in `Supervior/Build Docs/`
4. Director synthesizes → updates this log + audit report

**All pushes to branch arena/019fd71e-the-bettor-1 sync to all team spaces.**
