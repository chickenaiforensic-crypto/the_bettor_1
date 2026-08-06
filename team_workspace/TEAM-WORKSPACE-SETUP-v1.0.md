# TEAM WORKSPACE — the_bettor_1 Project

**Workspace Owner:** Director of Intelligence / Lead Engineer & Lead Researcher  
**Project:** Pitch Rating — zero-market football prediction engine  
**Branch:** arena/019fd71e-the-bettor-1  
**Date:** 2026-08-06  

---

## WORKSPACE STRUCTURE

```
team_workspace/
├── director/                    # Director's coordination & decisions
│   ├── assignments.md          # Active task assignments
│   ├── decisions_log.md        # Director decisions (dated)
│   └── team_status.md          # Current team status dashboard
├── intel_audit/                # Audit reports & intelligence findings
│   ├── external-audit-2026-08-06.md   # THIS audit report
│   └── findings_summary.md     # Quick-reference findings
├── researcher_handoffs/        # Researcher return tracking
│   └── queue_status.md         # Workorder queue status
├── builder/                    # Builder coordination
│   └── build_queue.md          # Builder step status
├── auditor/                    # Auditor coordination
│   └── audit_queue.md          # Verification queue
├── shared_pins/                # Shared verification pins (md5/sha256)
│   └── pins.json               # Current pin registry
└── team_log/                   # Communication log
    └── session-2026-08-06.md   # Today's coordination log
```

---

## SYNCHRONIZATION PROTOCOL

Every team member has their own workspace. Changes in this workspace are relayed to team members via the handoffs system. Each push to this branch simultaneously updates:

1. **Director's space** (this workspace) — coordination hub
2. **Researcher's space** — receives workorders + receives returns
3. **Builder's space** — receives build specifications
4. **Auditor's space** — receives files to verify

**Push protocol:** All work product flows through `handoffs/` in the main repo. This team_workspace is the coordination layer.

---

## TEAM ROLES (from project SOP)

| Role | Responsibility | Returns To |
|---|---|---|
| **Researcher** | Gather match data from RSSSF/primary sources | `handoffs/` — one .txt per workorder |
| **Builder** | Implement app builds per masterplan | `handoffs/` — b64 .txt + evidence artifact |
| **Auditor** | Verify all data/builds with FRESH code | `Supervior/Build Docs/` + `audit_work/` |
| **Director (me)** | Coordinate, assign, synthesize, report | This workspace + audit reports |

---

## RULES THAT BIND US

1. **No market data** — ever, in any role (P1)
2. **One gate** — all data enters through app's ingest gate
3. **Approval = test run** — measured proof, not documentation
4. **Backup first** — purge/import flows are backup-gated
5. **No silent rewrites** — changed numbers get dated log entries
6. **Fresh code for auditors** — never reuse previous auditor's scripts as evidence
7. **Rows, never tables** — standings are recompute targets, not inputs
8. **Never guess** — unverifiable = NOTE|warning|blocker

---

## CURRENT STATE (2026-08-06)

See `intel_audit/external-audit-2026-08-06.md` for complete audit findings.

**Store status:** 5,000 verified rows (corrected D-1) + 82 MOL Cup rows pending import (D-2) = 5,082 target

**Queue status:**
- Researcher: 8 packs adopted; SPA in flight; 10 queued (ITA, GER, FRA, SCO1, SCOCUP, SCOLC, KOS, KOSCUP, MLS, USOC) + UEFA-CONNECTOR
- Builder: B0-B7 all QUEUED
- Auditor: Ongoing verification of incoming packs

**Critical findings from prior audit:**
- KOS: FABRICATED — do not use (ghost clubs, 0/10 table reproduction)
- UEFA-FULL: REJECT — fabricated scores, sentinel dates, missing rounds
- UEFA-CONNECTOR: "dates fixed" claim FALSE — 1,388/1,390 sentinel-dated
- 8 overlapping domestic packs: VERIFIED EXACT against independent sources
