# Masked-replay backtest — evidence engine (Gate 0 before the 20-game slate)

Date: 2026-07-31 · Method: every one of the 61 stored matches replayed blind — `cutoff = match date` hides the game itself and everything after (`beforeCutoff` strict). Engine: BlueprintEmbed v0.6-live, app frozen at v2.6.7-cross. Harness: `replay_test.js` (permanent — every future engine change must re-run this gate).

## Headline

| Bucket | Count |
|---|---|
| Replayed | 61 |
| NO CALL — no prior evidence (discipline) | 40 (66%) |
| Neutral / abstain (aggregate inside ±0.25) | 3 |
| Directional leans | 18 → **hit 9 · miss 9 = 50.0%** |

## Superpower sections, individually

| Section | Directional games | Hits | Rate | Read |
|---|---|---|---|---|
| h2h (previous meetings) | 14 | 5 | **36%** | **Anti-signal — below coin flip** |
| common (common opponents) | 7 | 4 | 57% | Noise, no strength proven |
| third (level-3 chains) | 8 | 4 | 50% | Noise |

Diagnosis of the h2h failure (mechanism, not vibes): the h2h estimate reuses previous-meeting goal difference **raw — no venue/home-flip adjustment, no shrinkage toward the mean**. Examples from the replay itself:

- Legia v Hibernian 28-08-2025: prior leg Hibernian 1-2 Legia **at Easter Road** → engine est merely +1.00 toward Legia, no home-boost for the return leg (draw → loss by settle rule).
- Malisheva v Drita 31-05-2026: prior Drita 2-0 Malisheva **at Drita** → est −2.00 (Drita advantage *at Malisheva*) → Malisheva won 3-2.
- Víkingur v Malisheva, Drita v Copenhagen: stronger side won both legs — raw reuse "worked" there (2 of the 5 hits). When legs flip, it fails. 36% over 14 games is exactly the signature of a missing venue algebra.

## What protected us (and held)

- **NO CALL discipline:** 66% abstention on a sparse two-club graph — the engine refuses where evidence is absent. (Rate overstated by our sparse coverage: only ~15-game windows per loaded club. Not a real-world defect.)
- **The Lean-only / Close-call caps:** none of these 18 leans was ever presented as a recommendation. The riskiest Scottish end-of-season games were correctly tagged Close call / NO CALL (Rangers v Hibernian, Hibernian v Motherwell, Celtic v Hearts — 1 hit, 1 miss, 1 abstain inside that tag).
- The failure lives in the **predictive surface (weights)**, not in the guardrails. That is precisely the unvalidated-weights debt the forward test was built to measure — the replay just measured it first, cheaper.

## Consequences

1. **No engine code changes yet.** Calibration comes from evidence, and the slate plan stays — but Lane 2 leans are now *expected-weak*, pre-registered, not assumed-sound.
2. **Calibration candidates (small-n flagged, all gated):**
   - **A — venue-corrected h2h:** transform previous-meeting GD through home-flip algebra (strip prior home advantage, add current one) + shrink toward zero by sample size. Must beat 36% → ≥60% on this same replay before any adoption.
   - **B — h2h phase demotion until corrected:** if A fails its replay gate, h2h must not stand as a lone superpower (current 36% is worse than abstaining).
   - **C — chains/common: no change on this evidence** (noise at n=7–8) — forward slate carries the question.
3. **Forward-test plan update:** this replay becomes **Gate 0** — mandatory re-run after any engine change; Lane 2's 8 UEFA fixtures are now pre-registered tests of candidates A/B, not validations.
4. **Scope honesty:** replay tests the evidence engine only. The calibrated domestic model (Lane 1) cannot be strip-tested locally (training data not in the app, ratings frozen at build) — it is validated purely prospectively in the 20-game slate.

## Full replay table

(61 rows — see `node replay_test.js` output; regenerate any time.)

Key directional rows:
- HIT: Víkingur v Malisheva (+1.00), Drita v Copenhagen (−2.00), Celje v Drita (+1.00), Hibernian v Hearts (−2.00), Prishtina v Malisheva (−3.00), Rangers v Hibernian (−0.50), Motherwell v Celtic (−1.29), Hearts v Falkirk (+3.45), Falkirk v Rangers (−2.05)
- MISS: Hibernian v Partizan (+2.00), Legia v Hibernian (+1.00, draw), Hearts v Motherwell (−0.50), Hibernian v Celtic (+1.00), Hibernian v Motherwell (+0.27), Llapi v Malisheva (−2.00), Malisheva v Drita (−2.00), Malisheva v Vllaznia (−1.00), Malisheva v Hibernian (−0.43)
- Note the Malisheva-in-Europe cluster: engine repeatedly leans away-side on raw prior GD and gets reversed by venue — the same failure shape the real second leg then confirmed (Hibernian 4-1).
