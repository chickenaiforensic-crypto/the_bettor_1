# Auditor Gate-All Initial Findings — 2026-08-06

## MLS 2025 regular season — PASS (table gate)

I independently recomputed the 2025 regular-season table from the 510 `Major League Soccer` match rows in `handoffs/MLS-2021-2026_BP-TEAM-PACK_v2.txt` and compared every club's P/W/D/L/GF/GA/points to RSSSF's final Eastern and Western conference tables: <https://www.rsssf.org/tablesu/usa2025.html>.

**Result: 30/30 clubs match exactly.** Each club has 34 matches. Examples independently recomputed: Philadelphia 20-6-8, 57-35, 66; Inter Miami 19-8-7, 81-55, 65; San Diego 19-6-9, 64-41, 63; Vancouver 18-9-7, 66-38, 63. The 2025 row grammar is 14 fields; source ID `rsssf-mls-2025` resolves; score/date sanity and within-pack duplicate gate pass.

This approves the **2025 regular-season table claim**, not the still-missing 2026-to-date MLS scope.

## Corrected 16,193 store — harness PASS, with stated scope

Fresh execution: `python3 audit_work/ladder_run_16193.py`.

The run completed and wrote `audit_work/ladder_baseline_2026-08-06_16193.json`. Its FULL aggregate across eight usable domestic leagues is **+8.63% Brier gain**. Spain is .5863 vs .6299 base (+6.92%, p=.000905) and Scotland is .5828 vs .6470 (+9.93%, p=.001074). Kosovo remains without a usable full holdout in the runner, so it is not included in this aggregate. This establishes the harness runs on the corrected 16,193 store; it is not approval to reintroduce the known fabricated UEFA rows.

## B4 v3.11 M17 code audit — I5 PASS, I4 FAIL

- **I5 settlement PASS by source inspection:** `classifyOutcome` at `builder/app-v3.11.0-b4.html:2281` returns H/D/A; `settlementResultFor` explicitly returns `loss:true,push:false` for an H/A prediction when actual is D; the result-entry handler at `:4597-4607` persists scores/outcome/result. This corrects the former no-settlement implementation.
- **I4 venue guard FAIL:** `isVenueVerified` is implemented (`:2244-2270`), but the only occurrences are its definition and `renderVenueGuardPanel` (`:2272`). It is not invoked from pack validation/commit or the import approval path. Therefore an unknown imported venue is not hard-blocked at ingestion; displayed tick boxes are not an enforceable Z-003 hold. M17 remains blocked on I4.

## B5 balance panel — NOT GATEABLE FROM PRESENT TREE

The relay names v3.12.0/B5, but the current builder directory stops at `app-v3.11.0-b4.html`. B4's `zoneBlock` renders H/D/A calibrated display bars (`:4257-4264`), but that is not evidence that a B5 `renderBalancePanel()` renders on **NO CALL** cases. No B5 byte-diff or application artifact is available here; no approval granted.

## Cup and UEFA spot checks

The prior grammar re-gate remains recorded in `AUDITOR-REGATE-FIVE-PACKS-2026-08-06.md`. Full independent source spot checks for the cups and cleaned UEFA pack are still pending; do not mark them adopted from this report. The currently named UEFA-FULL handoff remains the known fabricated-row version and cannot be approved until the clean 2,764-row handoff is actually delivered.
