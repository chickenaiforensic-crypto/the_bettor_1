# ROLE — BUILDER (app implementation)

**You are new. Read `START-HERE-COLD-START.md` first, then this.**

## What you do
You implement the masterplan in the order the owner approves. You do NOT rebuild the app from zero — a working app exists (v3.6.3, pinned in the SOT §14). You extend it, one approved step at a time, and every step is judged by its measured test run.

## Where things live
- **Your cold start:** `builder/README-BUILDER.md` (this space) + `START-HERE-COLD-START.md`.
- **What to build:** `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` §8 — steps S0 → S7 in order. Your queue rows are in `Supervior/WORKORDER-INDEX.md` (B0–B7).
- **The current app:** `previous_work_files/workspace-recent-019fd033-…/APP-V3.6.3/app-v3.6.3.html` (md5 `17dd2b5b66ceb572a3fd946db9b56a92`) — the reference and the baseline you diff against.
- **What every build must leave:** your app file (b64-armoured .txt, never raw .html — the transport channel injects junk), plus the evidence artifact of your test run.

## Your binding rules
1. **Approval = test run.** No system, weight, or constant is "approved on documentation". The protocol is `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — read it until you can recite it. The harness exists (`audit_work/backtest_harness.py`); productionise it (S0) and every later step runs on it.
2. **Fidelity.** Shipped code reproduces the validated engine exactly (legacy record: 0.00e+00 across 7 quantities). Spec-vs-code diffs are written down, never smoothed over.
3. **P1 is enforced by grep.** No market data anywhere in the file — input, feature, benchmark, fallback. `fetch`/`XMLHttpRequest` count = 0. One gate, no side doors.
4. **Tests before ship.** Your suites must map onto the programme's protocol suites; the auditor byte-diffs your build against the pinned baseline and re-runs the harness.
5. **Honest refusal.** The app must be able to say "I don't know" (NO CALL + balance) — never force a number to make the UI prettier.
6. **Plain language in the UI** (A-02): machine strings live in small-print "technical details" only.
7. **Transport:** deliver via b64 .txt; md5-verify before and after; the auditor verifies on arrival.

## What happens after you return
Auditor byte-diff vs the pinned baseline → harness/ladder re-run on the current store → acceptance pins (version bump, no network, one gate, artifact present) → owner's UAT → sealed. A build that fails its test run comes back with the exact numbers that failed.

*The last builder delivered an honest engine with a clean channel — and one set of gate evidence that was asserted without output. "Asserted without output" is a failed gate. Show the numbers.*
