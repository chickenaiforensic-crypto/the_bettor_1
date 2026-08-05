# WORK ORDER — BUILDER B0: THE TEST-RUN HARNESS (first builder commission)

**Issued:** 2026-08-05 · **Status:** QUEUED — starts on owner's word · **To:** the future builder session (cold-started via `START-HERE-COLD-START.md` + `builder/README-BUILDER.md`)

## What this step is
Productionise the backtest harness into the app's own masked-replay module, exactly to the owner's ladder protocol (`Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md`). This is step S0 of the masterplan (§8). Everything after it (S1–S7) runs on it — this is the measuring stick of the whole programme.

## Inputs (all in the repo)
- Reference app v3.6.3 (diff baseline): `previous_work_files/workspace-recent-019fd033-…/APP-V3.6.3/app-v3.6.3.html` (md5 `17dd2b5b66ceb572a3fd946db9b56a92`)
- Operational store (5,082 rows, D-1+D-2 applied): `previous_work_files/workspace-recent-019fd033-…/pitch-rating-full-5082-D1D2-2026-08-05.json`
- Feasibility harness to productionise: `audit_work/backtest_harness.py`
- Engine constants/layers: SOT §3 + ENGINE_SPEC (pins in SOT §14)

## Deliverables
1. App file (b64-armoured `.txt`) with the masked-replay module: per-league ladder runs (L-1 last game → L-2 last 2 → L-n expanding → FULL season), full metric set, **artifact output** (train window, holdout, n, Brier per side + 1X2, log loss, direction, calibration max error, date) stored with the run.
2. Evidence artifact of your own runs on the 5,082 store.

## Acceptance (all measured, none asserted)
- **Parity:** your module reproduces the feasibility numbers on the 5,082 store within tolerance — RPL Brier ≈0.5675 vs base 0.6465; CZ1 ≈0.6090 vs 0.6509; EPL ≈0.6140 vs 0.6534 (last-omitted-season holdout) — and reports per-match n.
- **Ladder:** L-1/L-2/L-n/FULL all runnable per league; constants adjustable only in bounded steps within the existing caps (star ±0.02, clamps, shrink k=0.5…) — no free-run calibration.
- **P1/no-network/one-gate greps** clean (same as v3.6.3); byte-diff vs baseline documented.
- Artifact = the approval record; no chat-only numbers.

## Rules
Approval = the acceptance above, not this document. Do not touch the store. Do not change engine constants as part of B0 (measurement only). Transport per `handoffs/README-HANDOFFS.md` (b64 + artifact).
