# CALIBRATION-6 — TOTAL GOALS (EV-G2) · shipped v2.8.5-cross · 2026-08-01

Turn: total estimated goals as an exploited category. Re-analysed the entire canonical
masked replay (633 games with evidence; same pool as the zone ladder) from the
goals-scored perspective, categorised the failures, calibrated, shipped the winner.

## What the estimator is (results-only, causal, zero odds)
EV raw: per-side weighted mean of total goals in evidence matches touching that side
(path-id weights = the same PHASE weights as direction; max-wins dedupe per match),
averaged across sides. B0: rolling all-store mean with date < cutoff.

## Measurement before calibration (633 games)
- Base rates: O1.5 74.7% · O2.5 50.2% · O3.5 27.5% · draw 24.3% · mean 2.68
- MAE: EV raw 1.315 · B0-flat 1.323 · B1 last-10 1.325 → raw signal real but thin.

## Failure classes (what went wrong by region/category)
1. **Tail regression — the structural class.** Expected <2.2 (n=54): landed 2.76
   (bias −0.84). Expected >3.2 (n=50): landed 3.12 (bias +0.43). The pure evidence
   mean overcommits to extremes; anything read off the tails was mispriced.
2. **Thin-path collapse.** paths<20 (n=40): big-miss 40%, MAE 1.851, bias −0.38 —
   evidence-starved estimates skew LOW and fail worst. (Analogue of the C11/star
   finding: sparse history = inflated confidence, here under-prediction.)
3. No-H2H cohort: big-miss 24.4% (vs 19.1% league baseline).
4. Cup games: no bias (−0.07); the 90-min settle rule is not distorting totals.
5. Worst single misses are one-off avalanches (Víkingur–Malisheva 0-8 exp 1.00;
   Krylya–Dynamo 3-6 exp 3.27): irreducible variance, not a pattern class.

## Calibration tested (all scored out-of-sample where params are fit)
- C1 OLS shrink (LOO): actual ≈ 1.349 + 0.492·EV — MAE 1.314, tail re-bucketing ugly.
- C2 evidence-volume blend: est = w·EV + (1−w)·B0, w = npaths/(npaths+K), K swept 5–60,
  best K=10 — **MAE 1.301, winner** (beats every baseline).
- C3 = C1 on top of C2 (LOO): 1.304 — no extra win, adds complexity; rejected.

## Shipped rule (display-only; never feeds zone/gates/agreement)
est = w·EV + (1−w)·B0, w = npaths/(npaths+10).
Regions measured on the replay:
| region | n | est mean | actual | U2.5 | O2.5 | O1.5 | O3.5 | draw |
|---|---|---|---|---|---|---|---|---|
| LOW <2.40 | 72 | 2.27 | 2.32 | **59.7%** | 40% | 65% | 17% | 26% |
| MID 2.40–2.80 | 341 | 2.62 | 2.55 | 50% | 50% (coin-flip) | 72% | 25% | 22% |
| HIGH ≥2.80 | 220 | 2.98 | 3.01 | 45% | 55% | **82%** | 35% | 28% |
Region biases after calibration: LOW +0.05 · MID −0.07 · HIGH +0.03 — tails fixed.

## Categorical fallbacks now available (measured, n-attached)
- LOW region → 2–3 goal games: under 2.5 hits 59.7% (base 49.8%) — the one clean UNDER edge.
- HIGH region → over 1.5 hits 82%; over 2.5 only 55% — treat 2.5 there as near-coin-flip.
- MID region → the 2.5 line is a true coin-flip; no totals claim honest.
- Outcome link (measured, noted, NOT gated): draw-share peaks in the 2.2–2.5 expected
  band (30.2%, base 24.3%) — context for WIN-DRAW zones only; no rule changed.

## Ship mechanics
app v2.8.5-cross: evidenceGoalsEstimate() + evidenceGoalsHtml() rendered in the verdict
card; EV-G2_TABLE pinned in smoke_test (83/83); zone logic untouched (pin asserts).
Zone ladder after ship: unchanged (633: strong 80/93 · win 70/89 · windraw 53/77 ·
lean 48/72 · toss 38/68) — display-only confirmed by full harness re-run.
Files: rpl/goals_replay.json (633 rows), rpl/goals_replay.js, rpl/goals_analyze.py,
rpl/goals_calibrate.py, rpl/goals_final_map.py, rpl/goals_cal.json, rpl/goals_final.json.
Paste-type: none — zero data added; computation only.
