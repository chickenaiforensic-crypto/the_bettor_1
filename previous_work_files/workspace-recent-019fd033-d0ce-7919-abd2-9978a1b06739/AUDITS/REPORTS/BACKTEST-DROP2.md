# BACKTEST DROP-2 — last-two-results masking (2026-08-01)

User order: previous masking dropped only the last result; this round drops each side's
**last TWO results** before the fixture, so the call is made without the two freshest
form rows ("check the one before the last also"). Both variants keep strict causality
(cutoff = fixture date). Frozen v2.7.1 engine, 600 evidence games (671 universe, 71 NO CALL).
Log: `drop2_log.csv`, runner: `drop2_backtest.js`.

## Zone quality: baseline (full history) vs drop-2

| Zone | Baseline | Drop-2 | Δ |
|---|---|---|---|
| STRONG | n=60, W 78%, L 8%, pair 92% | n=59, W 76%, L 10%, pair 90% | −2pp w |
| WIN | n=125, W 65%, L 20%, pair 80% | n=114, W 59%, L 23%, pair 77% | −6pp w |
| WIN-DRAW | n=201, W 48%, pair 72% | n=194, W 52%, pair 79% | +7pp pair |
| lean | n=97, 53% | n=97, 56% | — |
| TOSS | n=117, 43% | n=104, 46% | — |

Zone-word or side churn: **174 of 600 (29%)**. Among churned games the drop-2 call
beat the baseline 12:6 (small-n; many churn rows are season-start games going NO CALL
because the stripped window empties a young team's evidence — correct discipline).

## Read
1. **The system is robust to the freshest-two strip.** STRONG loses ~2pp, WIN ~6pp —
   the win zone leans modestly on fresh form, the strong zone barely.
2. WIN-DRAW actually improves under drop-2 (pair 72→79%) — the demoted near-calls it
   absorbs are exactly the pair-shaped ones. No rule change implied (anchors are tuned
   on full history; this is a sensitivity proof, not a re-calibration).
3. Early-season games correctly fall to NO CALL when the strip empties evidence.
4. Requested pair check — Rubin v Akron 2026-04-18 (the one before the last): baseline
   TA WIN-DRAW 61.0% → drop-2 **identical (61.0%, WIN-DRAW)**, actual 1-1 → zone-hit
   holds with the last two results removed. Forward 2024-11-22 also holds
   (windraw 59.7→61.0, actual home win).

## Where the system gets great data (user question 2, measured)
| Universe | Evidence yield | Note |
|---|---|---|
| RPL closed league graph (610 rows, tables reconciled 16/16) | **96%** (488→469) | 2 full seasons + cups, dense 3-section evidence |
| UECL/domestic pack rows | 72% (183→131) | sparse graph, 52 NO CALL correct |
| 18 rated domestic leagues (Dixon–Coles model, 153k results built-in) | 100% by construction | deepest data: full probabilities (e.g. Celtic 80.5 / D 12.4 / Dundee 7.1) |

Conclusion: deepest = the 18 rated leagues; for the evidence engine, a **closed dense
league graph (RPL-type) is the sweet spot**; cross-border corridors stay thin until
per-league graph packs exist.
