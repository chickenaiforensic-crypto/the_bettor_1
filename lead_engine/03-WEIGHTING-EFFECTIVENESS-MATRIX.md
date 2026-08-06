# 03 — WEIGHTING EFFECTIVENESS MATRIX (The Constitution of the Singular Engine)

**Date:** 2026-08-05  
**Method:** Measured contribution, not origin/preference. Paired tests T1, MDE T2, rolling-origin T3, complete output T4. Every number from real store 5082 or legacy 59k calibration.

## Ranking Table — What Stays, How Much It Weighs, Gate to Stay

| # | Component | What It Answers | Measured Effect | Weight Class | Numeric Weight (Planning) | Gate |
|---|---|---|---|---|---|---|
| 1 | **L1 Dixon-Coles live fit per-league** | who wins, how much (λ) | Brier 0.6112 vs 0.6476 base = **+5.6%** absolute, RPL feasible -12.2% vs base (0.5675 vs 0.6465 n254), CZ1 -6.4% (0.6090 vs 0.6509 n276), EPL -6.0% (0.6140 vs 0.6534 n374), calibration ≤1.7%, per-league home 1.20-1.36×, ρ -0.06 | DOMINANT — supplies probability | 1.00 (reference) | masked replay on current store must beat evidence + base rate, auto re-run on data change M1, paired T1, MDE T2 |
| 2 | **L2 scoreGrid** Poisson×Poisson DC τ low | H/D/A distribution shape | shapes prob, normalised, max cell ~13% freq | CORE inside L1 | 1.00 (tied to L1) | calibration ≤2.7% 1X2 per I3 |
| 3 | **L2 goalsGrid shrunk k=0.5** | O/U, handicap | O2.5 error 10.3%→2.7% after shrink GMU 2.6186, BTTS 6.0% withheld correctly absent | SEPARATE family — never merged H/D/A | display separate | per-market gate I3 ≤2.7% ship, 3.0-3.3% caution, BTTS 6.0% withheld |
| 4 | **L3 star draw correction** | draw-rate refinement only | +0.047% full-1X2 Brier p<0.0000 n59615, tier-2/3 ≈+0.09%, cap ±0.02, proportional split M4 (no leak), churn 21%→8.7% via hysteresis 0.05, metric (3W+D)/P P≥5 shrink 6, quintile within league | REAL SMALL — may edit L2 prob capped | 0.15 (correction weight 0.2/0.5/0.5 applied on draw only) | paired all 5 metrics T4, cap enforced, must never move favourite |
| 5 | **R2 zone ladder** confidence band | confidence statement, NOT prob | STRONG 78%/92% pair n59 monotone, WIN 67/82, WIN-DRAW 49/75, lean 47, toss 45, gentle shrink, versioned tables, always carries n+spread+calibration | CONFIDENCE | display only | held-out calibration, n + spread shown every call |
| 6 | **R2 chain cross-border** disconnected ties | cross-league evidence direction | 3rd phase r +0.274 n693 62.6% direction, 2778 Euro matches, European-edge scale >1.00 degraded RMSE historically, frozen 1.00 baseline to beat | STANDBY | gated — scale 1.00 frozen until fit-to-results loop wins | harness win vs frozen 1.00 on omitted European window §6 bias loop s_L←s_L×(1+step×bias) step 0.05-0.1 20-50 passes |
| 7 | **L5 consensus** HvH AvA | selection filter, magnitude carries signal not lens agreement | STRONG 78.6% / CONFIRMED 74.8% vs 73.0% model top-10% +5.6pt, DRAW-LEAN 31.8%, both sides ≥4H & ≥4A min | FILTER ONLY edits nothing test-enforced | filter weight — prob unchanged | changes no prob, magnitude test |
| 8 | **L4 tiers/points** | readability labels | 0 prob impact, calibrated: A+ ≥70 78.5% win n7718, A ≥60, B ≥52, C ≥45, D ≥35, E <35, points round(100×H_cal) | DISPLAY | readability | labels must match observed rates |
| 9 | **R3 ELO stars** 1500 K20 home+65 | quick ordinal 1-5★ | unvalidated vs outcomes, perf window6 min3 causal | DISPLAY ONLY | ordinal display | A-03 adopt display-only with "not a prediction" label, never edits R1/R2 |
| 10 | **Goal-range bins 0-1/2/3+** | calibrated goal bands | NOT BUILT M8 — promise but no held-out win yet | FUTURE — gated | — | separate calibration + held-out win after M7 |
| 11 | **Data substrate** | truth of all above | 5082 verified 0 dup, 11 date defects D-1 fixed, 82 shortfall D-2 fixed, adjudication 7 cases pack correct | SUBSTRATE | — | ingest one gate + audit protocol + M10 outcomes-only screen |

**Weighting rule (building code):** no component may consume another's output unless its rank is higher or it is display-only. L3 may edit L2 draw prob capped small; L5/R2/R3 may never edit L1-L3. Enforced by tests — builder must grep.

## How Numeric Weights Become Code

- L1 probability = softmax of grids from λ. This is 1.00 — final H/D/A always this unless L3 correction applies.
- L3 correction: if stars qualify P≥5 and tier exists, target draw from draw_table[tier|gap] with 0.2/0.5/0.5 blending, then D_cal = D_raw + w×(target-D_raw) with w as per table, clamp |D_cal-D_raw| ≤0.02, proportionally renormalise H and A to keep favourite, i.e. H_cal = H_raw × (1-D_cal)/(1-D_raw) if H_raw≥A_raw else similar preserving ratio.
- R2 zone: does NOT multiply prob — displays alongside as confidence band with its own historic calibration.
- R2 chain weighted bridge (future): league strength s_L rescales att/def onto common scale for cross-league fixtures only, standard L2-L5 apply unchanged after rescaling, but only if weighted scale beats frozen 1.00 baseline on omitted European window (A-08).
- L5 consensus: if Tier A/A+ and ≥4H/≥4A both sides, compute mean goal-diff lenses, threshold >1.5 STRONG, >1.0 CONFIRMED, <0 CONFLICTED, |<0.2|&disag<0.5 DRAW-LEAN — display only, never prob.
- R3 stars: compute ELO live from store every derive, display ★ only.

## Why This Weighting Is Best Computational Wins

- "Best" = highest calibrated accuracy on our own data — measured by masked replay Brier/logloss/calibration per market + settlement ledger I5 draw=loss, NOT vs bookmaker (P1 forbids), NOT raw hit rate.
- Single best system per league on last omitted season already beats base by 6-12% (feasibility) — full engine with star correction historically +5.6% total.
- Singular engine removes second rating universe (bootstrap orphaned), removes hidden precompute (M3 provenance), forces live derive or plain "not rated yet" (A-01), shows balance on NO CALL (M7 P3 honesty).
- Rejected ideas register prevents re-litigating measured failures (recency 84/84 no disc, venue correction pocket worse, spread gate tight worse) — E1-E9 errors not repeated.

## Approval by Test Run (Universal Instrument) — Ladder

Owner doctrine binding: L-1 train up to newest-1 predict newest calibrate constants bounded steps existing caps until matches; L-2 hold out newest 2 test both readjust; L-n expand holdout (3,4,… or matchday) until last season covered; FULL full-system accuracy all leagues complete metric set T4 paired T1 with n and MDE T2 — any degradation adjust designated constant re-run ladder from L-1, when constants stop needing adjustment as holdout grows → CALIBRATED APPROVED BY TEST RUN. Held-out touched only by scoring never fitting E8. Every run writes numbers artifact (train window, holdout, n, all metrics, date) — artifact IS approval record.

First live feasibility run (D-1 store, simplified fit no stars no evidence ensemble, naive init):
- RPL train 960 test 254 scored +2 refused P3 <6 games: Brier DC 0.5675 vs base 0.6465 -12.2% logloss 0.957 dir 55.9%
- CZ1 train 1105 test 276 scored 0 refused: 0.6090 vs 0.6509 -6.4% logloss 1.015 dir 49.3%
- EPL train 1520 test 374 scored +6 refused: 0.6140 vs 0.6534 -6.0% logloss 1.023 dir 49.2%

Baseline every candidate must beat per league on omitted window paired — that is gate. Script audit_work/backtest_harness.py re-runnable; production harness S0 will include rolling-origin, paired stats, MDE, full metric set, artifact output.

Script ladder baseline expanding holdout JSON at audit_work/ladder_baseline_2026-08-05.json shows convergence from noise at L-1..L-30 to stable FULL win — proves instrument feasible.

## Cross-League Weighted Bridge — Fit-to-Results Loop (Formalised Owner Example)

Goal: rate teams different leagues on one weighted common scale e.g. EPL side vs Dynamo Moskva then standard compute applies (M19/A-08).

Loop "bump league up until it matches":
1. CONNECTOR UNIVERSE actual cross-league results 2021-26 UEFA CL/EL/ECL + qualifiers involving programme leagues. Today 0 rows in store → researcher pack #17 required (D14 domestic-scope expansion approved owner 2026-08-05).
2. MODEL team ratings per league own scale, league strength s_L rescales onto common. Predict vs actual every connector tie.
3. FIT LOOP each league pair enough ties measure bias bias(L)=mean(predicted GD - actual GD) over ties involving L then adjust s_L←s_L×(1+step×bias(L)) step ≈0.05-0.1 re-predict re-measure iterate until bias converges below tolerance typ 20-50 passes gradient-descent on same loss harness scores. This IS bump until matches: each league weight driven by direct results vs others not opinion.
4. VALIDATION actual approval gate per §5: fit s_L on connector matches up to cutoff 2021-22..2024-25 test on LAST OMITTED window 2025-26 Euro matches untouched weighted vs frozen unweighted scale 1.00 (LIVE-BLUEPRINT §3 baseline) adopt ONLY if wins Brier/RMSE/direction paired on omitted window.
5. If adopted: weighted common scale becomes L1 input for cross-league fixtures standard L2-L5 unchanged. If not: stay silent plain "no calibrated bridge" label P3 — chain evidence view remains.

Guardrails: no arbitrary multiplier — weights from fit; Euro-edge scale >1.00 degraded RMSE historically so frozen 1.00 baseline incumbent to beat; connector data must pass same ingest/audit gates as domestic (one gate, M10 screen before use).

*This matrix IS the constitution — weight = evidence. No component outranks its measured win.*
