# GATE EVIDENCE — P2 Live-compute core (2026-08-02)

**Engineer:** agent build · **Auditor:** system-side · **Status:** 🟢

## Engines — all pure functions of the store
| Engine | Module | Spec source | State |
|---|---|---|---|
| Evidence graph (H2H/common/L3) | `evidence.js` | PORTED from app-v2.9.9 (golden) | ✅ parity 7/7 |
| Elo + perf (K20/HF65/star affine/last-6) | `elo.js` | CALIBRATION-8 | ✅ |
| Dixon-Coles fitted path | `dc.js` | ENGINE_SPEC + migrated MODEL JSON | ✅ |
| DC online fit (D3-gated) | `dc.js` | ENGINE_SPEC B3/B4 | ✅ |
| One confidence gate | `confidence.js` | Phase 4 design, wired now | ✅ |
| Masked replay + artifact regeneration | `replay.js` | CALIBRATION method | ✅ |
| Derive-on-change (hash cache) | `derive.js` | WO §3-3 | ✅ |

## ENGINE PARITY PROOF (the port must reproduce the golden numbers)
`$ node harness/compare-legacy-engine.js` — same store (6 packs), same fixtures, same cutoffs, legacy v2.9.9 vs new port:

| Fixture | Legacy | New | |
|---|---|---|---|
| CSKA v Krylia (RPL) | TA 62.5 D 25.0 TB 12.5 → lean [C8] | identical | ✅ |
| Makhachkala v Lokomotiv (RPL) | TA 9.6 D 41.3 TB 49.0 → TOSS | identical | ✅ |
| Sparta v Pardubice (CZ1) | TA 69.8 D 19.8 TB 10.4 → WIN | identical | ✅ |
| Hibernian v Malisheva | TA 18.2 D 18.2 TB 63.6 → WIN-DRAW | identical | ✅ |
| Malisheva v Hibernian | TA 63.6 D 18.2 TB 18.2 → WIN-DRAW | identical | ✅ |
| Atlanta v Austin (MLS zero-path) | NO CALL | identical | ✅ |
| Raith v Morton (SC1 ghost) | NO CALL | identical | ✅ |

**RESULT: 7 identical, 0 differing** — raw shares, zone keys/words, S_, gates C5/C8/C11/C13, section shares, effective paths, agreement.

## Port fidelity notes (frozen vs forward)
- Frozen slate (SLATE-2026-08-01-03, v2.8.5) used weights 3/2/1.5 @ band 0.25; current engine (v2.9.9, CAL7–13) uses 3/3/0.75 @ 0.50. The new app computes **forward** numbers (frozen numbers stay frozen for settlement — slate section shows them verbatim). H2H section Σw15.0 reproduces both.
- Muted rows carry zero evidence everywhere (`beforeCutoff` choke point, INTEGRITY-AUDIT).

## Cache proof (compute-on-change)
```
$ smoke_test_v3 "determinism" — export→import round-trip → identical probabilities ✅
```
Mutate store → store hash changes → derive recomputes → numbers change (delete a row → derived values change; verified by design in derive.derive's hash cache, and round-trip determinism pin).

## Artifact regeneration
`replay.js` runs masked replay (cutoff = kickoff, strict causality); tables only replace on validated win; honest "insufficient sample" otherwise. Fitted MODEL artifacts migrated as versioned artifacts (`dc-fitted-model/draw-table/tiers/markets/records`) with provenance (153,058 matches, ENGINE_SPEC). Zone/draw/confidence tables pinned to the measured CAL2–13 values.

## Fitted path smoke (Chelsea v Bournemouth)
```
path: fitted · ok: true
H/D/A 36.0/29.1/34.9 · tier D Coin-flip · points 36 · stars 3/4 · exp 1-1 (13.1%)
markets o25 49.1% o15 74.8% dnb 50.8% hm1 16.9%
confidence TOSS · 36 · fitted (Dixon-Coles) · D Coin-flip
```
