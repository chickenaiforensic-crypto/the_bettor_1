# the_bettor_1 — Pitch Rating: zero-market football prediction engine

**What this is:** a football prediction system whose only fuel is completed match results (90-minute scores). No bookmaker odds, no market data, in any role — permanent. All systems are approved **by measured test runs** on our own data, never by documentation.

**Current state (2026-08-05):** store = 5,000 verified rows (ENG 1,900 · RUS 1,579 · CZE 1,521) + date-fix applied (`Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json`); backtest harness live (`audit_work/backtest_harness.py`); research queue = 17 workorders (UEFA connector = #17, queued).

---

## THE MAP — who works where

| Role | Gets work from | Works in | Returns to | Gate before it matters |
|---|---|---|---|---|
| **Researcher** (data) | `Supervior/Workorder/` (your queue number in `Supervior/WORKORDER-INDEX.md`) | repo, your own session | `handoffs/` — ONE `.txt` per workorder, `BP-TEAM-PACK v2`, never zip | auditor verification (never on trust) |
| **Builder** (app) | `Supervior/WORKORDER-INDEX.md` (builder rows) + `builder/README-BUILDER.md` | your own session | `handoffs/` (app file b64-armoured + evidence artifact) | auditor byte-diff + **test-run ladder** (`Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md`) |
| **Auditor** (verification) | every return + every build | `audit_work/` (scripts) + `Supervior/updates/` (log) | reports in `Supervior/Build Docs/` | pins verified on arrival; fresh parsers only; errata owned |
| **Owner** (approvals) | anything above | repo | decisions → `Supervior/updates/` log | backup-first rule; nothing imported on trust |
| **New to the project?** | — | — | — | read `START-HERE-COLD-START.md` first |

## The tree

```
README.md                        ← this map
START-HERE-COLD-START.md         ← mandatory reading for every new session
COMMUNICATION-RULES-v1.md        ← how we talk (binding)
Supervior/
  Build Docs/                    ← the authority: SOT, masterplan, functionality, verification
  Workorder/                     ← the queue: WORKORDER-INDEX.md + WORKORDER-*.md
  ROLES/                         ← per-role briefs (researcher / builder / auditor)
  updates/                       ← session logs, relay messages, specs
  other/                         ← store backups (pitch-rating-full*.json)
handoffs/                        ← ALL returns land here (researcher + builder)
builder/                         ← builder cold-start space (README + protocol pointers)
audit_work/                      ← live audit + backtest scripts (auditor-owned)
previous_work_files/             ← history of past sessions (read-only, never edit)
```

## The five rules that never change
1. **Results only.** No market data in any role (P1).
2. **One gate.** All data enters through the app's ingest gate; rejections never stored.
3. **Approval = test run.** A system is adopted only when it wins the harness on the last-omitted window (see masterplan §5).
4. **Backup first.** Purge/import flows are backup-gated; undo = load the backup.
5. **No silent rewrites.** Changed numbers/decisions get a dated log entry; pins live in the SOT (§14) and are re-verified on arrival.

*Anything asserted traces to a file, code line, or pin — no stories.*
