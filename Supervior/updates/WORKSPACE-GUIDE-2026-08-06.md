# WORKSPACE GUIDE — how to access shared state (2026-08-06)

**All team work lives on one shared branch.** Pull it before doing anything.

---

## The branch

```
arena/019fd4e0-the-bettor-1
```

This is the single source of truth for all work in progress. Every team member must pull from this branch at the start of their session.

## How to set up your workspace

```bash
git fetch origin arena/019fd4e0-the-bettor-1
git checkout arena/019fd4e0-the-bettor-1
```

## What's on this branch

| What | Where |
|---|---|
| Current store (16,629 rows) | `audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json` |
| All pack returns (14) | `handoffs/*_BP-TEAM-PACK_v2.txt` |
| App builds (B0, B1, B2) | `builder/app-v3.7.0-b0.html`, `app-v3.8.0-b1.html`, `app-v3.9.0-b2.html` |
| Builder evidence | `handoffs/B0-EVIDENCE-*.json`, `B2-EVIDENCE-*.json` |
| Builder deliverables (b64) | `handoffs/B0-v3.7.0-*.b64.txt`, `B2-v3.9.0-*.b64.txt` |
| Workorder index (current) | `Supervior/WORKORDER-INDEX.md` |
| Workorders | `Supervior/Workorder/WORKORDER-*.md` |
| Relay messages | `Supervior/updates/RELAY-TO-*-2026-08-06.md` |
| Cold-start notes | `Supervior/updates/COLD-START-*-2026-08-06.md` |
| Assignments | `Supervior/updates/ASSIGN-RESEARCHER-REMAINING-2026-08-06.md` |
| Audit reports | `Supervior/updates/AUDIT-REPORT-2026-08-06.md` |
| Harness scripts | `audit_work/backtest_harness.py`, `ladder_run.py`, `score_audit_full.py` |
| Expanded stores | `audit_work/pitch-rating-full-10199/11599/13429/16629-*.json` |
| League pivot artifacts | `audit_work/league_pivot_artifact.json`, `league_pivot_full_artifact.json` |
| Lead engine docs | `lead_engine/00-INDEX.md` through `26-*` |
| Designer deliverables | `designer/design-tokens.css`, `components.css`, `prototypes/index.html` |
| Team messages | `team_messages/*.md` |
| Role briefs | `Supervior/ROLES/ROLE-RESEARCHER.md`, `ROLE-BUILDER.md`, `ROLE-AUDITOR.md` |
| SOT / Masterplan | `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md`, `ENGINE-MASTERPLAN-2026-08-05.md` |

## How to save your work

```bash
# After making changes / adding files:
git add <your files>
git commit -m "description of what you did"
git push origin arena/019fd4e0-the-bettor-1
```

**Always push to `arena/019fd4e0-the-bettor-1`.** No other branch.

## If you see stale state

If your checkout shows old dates or missing files, you're on the wrong branch or haven't pulled. Run:

```bash
git fetch origin arena/019fd4e0-the-bettor-1
git reset --hard origin/arena/019fd4e0-the-bettor-1
```

This will match your local checkout to exactly what's on the remote.

---

*The planner maintains this branch. If anything is missing or stale, the planner will fix it — ask.*
