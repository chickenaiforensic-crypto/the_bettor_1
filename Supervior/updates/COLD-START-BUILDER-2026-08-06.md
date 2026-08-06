# COLD-START NOTE — BUILDER (2026-08-06)

**From:** Lead planner/analyst (covering during team break)
**To:** Builder — when you return, read this FIRST, then the files referenced.

---

## What happened while you were away

1. **Store CLOSED at 5,082 rows.** D-1 (11 CZ1 date fixes) + D-2 (MOL Cup +82) applied. Breakdown: ENG 1,900 · CZE 1,603 · RUS 1,579.
2. **Engine masterplan written** (`Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md`) — one weighted engine, build order S0–S7. THIS IS YOUR BUILD ROADMAP.
3. **Approval doctrine changed:** no system ships on documentation. Every build is approved by its **measured test run on our own data** using the ladder protocol. See `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — read it twice.
4. **Feasibility harness exists** (`audit_work/backtest_harness.py`) — first run: RPL 0.5675 vs 0.6465 base (−12.2%), CZ1 0.6090 vs 0.6509 (−6.4%), EPL 0.6140 vs 0.6534 (−6.0%). Your S0 task is to productionise this into the app.
5. **Workorder B0 drafted** (`Supervior/Workorder/WORKORDER-BUILDER-B0-HARNESS.md`) — your first commission.

---

## Your queue (what to build, in order)

| Step | Code | What | Status |
|---|---|---|---|
| S0 | B0 | Test-run harness → app's masked-replay module with ladder | **START HERE** |
| S1 | B1 | LIVE-DERIVE-01: live re-derive, auto re-validation, provenance panel | QUEUED (after B0) |
| S2 | B2 | Settlement/venue audit (draw=loss, flip guard) | QUEUED |
| S3 | B3 | Balance panel (NO CALL shows support shares) | QUEUED |
| S4 | B4 | Goal-range bins (0–1 / 2 / 3+, own calibration) | QUEUED |
| S5 | B5 | Cross-border bridge (UEFA connector → fit-to-results loop) | QUEUED (needs data) |
| S6 | B6 | Calibration cadence (one-click replay + monthly sweep) | QUEUED |
| S7 | B7 | UI/architecture build (plain language, provenance small-print) | QUEUED (design phase) |

**Every step ships only on its measured test run. No exceptions.**

---

## Key reminders (read these files in this order)

1. `START-HERE-COLD-START.md` — mandatory reading order
2. `COMMUNICATION-RULES-v1.md` — binding work rules
3. `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` — the whole system + ledger M1–M20
4. `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` — your TARGET structure
5. `Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md` — the app today (v3.6.3)
6. `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — your approval protocol
7. `Supervior/ROLES/ROLE-BUILDER.md` — your role brief
8. `Supervior/Workorder/WORKORDER-BUILDER-B0-HARNESS.md` — your first workorder

## Standing rules

- **Fidelity:** shipped code reproduces validated engine exactly (legacy record: 0.00e+00 across 7 quantities).
- **P1 enforced by grep:** no market data anywhere. `fetch`/`XMLHttpRequest` count = 0.
- **Tests before ship:** suites must map onto the programme's protocol.
- **Transport:** deliver b64-armoured `.txt` + evidence artifact into `handoffs/`. Never raw .html. md5-verify before and after.
- **"Asserted without output" = failed gate.** Show the numbers.

## Reference files (do not rebuild)

- App v3.6.3 (baseline): `previous_work_files/workspace-recent-019fd033-…/APP-V3.6.3/app-v3.6.3.html` — md5 `17dd2b5b66ceb572a3fd946db9b56a92`
- Operational store (5,082): `previous_work_files/workspace-recent-019fd033-…/pitch-rating-full-5082-D1D2-2026-08-05.json`
- Feasibility harness: `audit_work/backtest_harness.py`

---

*If this note conflicts with a workorder, the workorder wins — stop and ask.*
