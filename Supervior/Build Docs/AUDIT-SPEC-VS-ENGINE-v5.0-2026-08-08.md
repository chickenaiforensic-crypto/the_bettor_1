# SPEC vs ENGINE CROSS-AUDIT — v5.0
## Every spec document audited against current code, data, and reality

**Auditor:** Lead Intelligence Officer
**Date:** 2026-08-08
**Branch:** `arena/019fde32-the-bettor-1`

---

## DOCUMENTS AUDITED

| # | Document | MD5 | Status |
|---|---|---|---|
| 1 | ENGINE_SPEC.md v1.0 | `91cd0cd5...` verified | Engine specification |
| 2 | LIVE-BLUEPRINT.md v1.0-live | `d01cfde0...` verified | Evidence engine spec |
| 3 | METHODOLOGY.md v1.1 | `6cd6c0c8...` verified | Principles, protocols |
| 4 | BLUEPRINT-SOT-2026-08-04.md v1.3 | `8bb8c23e...` | System register |
| 5 | ENGINE-MASTERPLAN-2026-08-05.md v1.1 | `2d5bb098...` | Build order |
| 6 | FUNCTIONALITY-2026-08-05.md v1.0 | `b4fbb7c9...` | App functionality |

---

## PART 1: ENGINE_SPEC.md vs v5.0 CODE — 20 of 24 constants match, 4 intentionally overridden

All DC gradient constants (LR, DECAY, HFA_LR, RHO, MIN_GAMES, clamps) match identically.

Overridden constants (audited and justified):
- GMU: spec 2.6186 → per-league measured (E0:2.97, RPL:2.73, CZ1:2.86)
- Base rates: spec 44.6/26.8/28.6 → per-league measured from training
- DRAW_TABLE: spec 27 cells from 59k-legacy → per-league 15 cells from 4k training
- TIER_WEIGHTS: spec 0.2/0.5/0.5 → per-league fitted (E0:0.41, RPL:0.35, CZ1:0.40)

L4 (tier labels) and L5 (consensus): spec exists, NOT in v5.0 code. Display-only, zero probability impact.

---

## PART 2: LIVE-BLUEPRINT.md vs REALITY — ZERO IMPLEMENTATION

All 8 evidence engine modules described in §8 are specifications only:
identity_store, match_store, evidence_graph, cross_border_bridge,
goal_range_model, confidence_calibrator, balance_panel, audit_log

**Verdict: R2 does not exist.** The binding rules (§1) are sound and should be preserved for future implementation.

---

## PART 3: BLUEPRINT-SOT-2026-08-04.md — STALE

- References app v3.6.3 (current: v5.0.0)
- References 5,000-row store (current: 5,082)
- M20 listed as open (resolved 2026-08-05)
- Repo pin `12192a9b` (current main: `eaeddb2`)
- App pin `17dd2b5b` (current: `0e2fdf9e`)

**Verdict: Frozen at 2026-08-05. All pins stale. Should be marked HISTORICAL.**

---

## PART 4: ENGINE-MASTERPLAN-2026-08-05.md — S0 done, S1-S7 unfinished

| Step | Status |
|---|---|
| S0 harness | Exists as Python script, not in app |
| S1 LIVE-DERIVE | v5.0 does live fit, no provenance panel |
| S2-I4/I5 | Not implemented |
| S3 balance panel | Not implemented |
| S4 goal bins | Partial (O/U exists, no bin calibration) |
| S5 cross-border | Not implemented, blocked on UEFA data |
| S6 calibration | Not implemented |
| S7 UI | v5.0 shell exists, not A-02 compliant |

Harness baselines (EPL 0.6140) match v5.0 at 4dp.

---

## PART 5: FUNCTIONALITY-2026-08-05.md — Describes obsolete app

References v3.6.3 with 5 tabs, seed packs, backup/purge. None of this exists in v5.0.0.

---

## PART 6: METHODOLOGY.md — Principles still binding

P1-P5, I1-I6, T1-T8 remain the correct engineering discipline.
P1 (no market data): confirmed 0 matches in v5.0.
I6 (zero network): confirmed 0 fetch/XHR.

---

## CONSOLIDATED GAPS (11 total)

| # | Gap | Severity |
|---|---|---|
| G1 | BLUEPRINT-SOT stale — frozen at 2026-08-05 | HIGH |
| G2 | R2 evidence engine: spec exists, zero code | HIGH |
| G3 | No docs reference v5.0 or per-league calibration | HIGH |
| G4 | Cross-league bridge S5: blocked on UEFA data | HIGH |
| G5 | L4/L5 tiers+consensus: spec only | MEDIUM |
| G6 | I4/I5 venue guard/settlement: not wired | MEDIUM |
| G7 | M3 provenance panel: not built | MEDIUM |
| G8 | FUNCTIONALITY doc describes v3.6.3 | MEDIUM |
| G9 | VERIFICATION-DATA stops at 2026-08-05 | LOW |
| G10 | DRAW_TABLE/GMU from spec (overridden in v5.0 code) | LOW |
| G11 | FUNCTIONALITY describes obsolete app | MEDIUM |

---

*Every claim traced to file, code line, or grep output. No stories.*
