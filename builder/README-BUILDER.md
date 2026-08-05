# BUILDER — cold-start space (2026-08-05)

**You are the future builder session. Everything you need to orient is in this repo; read in this order.**

## 1. Mandatory reading (in order)
1. `START-HERE-COLD-START.md` (repo root) — the orientation path.
2. `COMMUNICATION-RULES-v1.md` — how we work (binding).
3. `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` — the whole system + missed-work ledger M1–M20 + amendments + pins.
4. `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` — the TARGET: one weighted engine; **approval by test run** (§5); cross-league fit-to-results loop (§6); build order S0–S7 (§8).
5. `Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md` — the app today (v3.6.3), screen by screen.
6. `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — **your approval protocol.** Read it twice.
7. `Supervior/ROLES/ROLE-BUILDER.md` — your role brief.
8. `Supervior/WORKORDER-INDEX.md` — your queue (B0–B7); work starts at the row the owner approves.

## 2. What exists already (do not rebuild)
- App v3.6.3 (reference + diff baseline): `previous_work_files/workspace-recent-019fd033-…/APP-V3.6.3/app-v3.6.3.html` — md5 `17dd2b5b66ceb572a3fd946db9b56a92`.
- Verified store: `Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json` (5,000 rows) — the D-1 date fix is IN this file; the original is untouched.
- Backtest harness (feasibility): `audit_work/backtest_harness.py` — productionise it as S0 (the app's own masked-replay module with per-match artifacts and the expanding-holdout ladder).
- Engine constants, layer rules, refusal paths: ENGINE_SPEC + SOT (all pinned in SOT §14).

## 3. What "done" looks like
A build is done when: it passes the byte-diff vs baseline, the P1/no-network/one-gate greps, **its own test-run ladder on the current store shows the step's numbers** (artifact written), and the owner's UAT confirms it. Then it gets sealed with a version pin and logged.

## 4. Transport
Deliverables: b64-armoured `.txt` + evidence artifact, into `handoffs/` (see `handoffs/README-HANDOFFS.md`). Never raw `.html` over the channel; md5-verify before and after.

*The last builder delivered an honest engine — and once asserted gate evidence without output. "Asserted without output" is a failed gate. Show the numbers.*
