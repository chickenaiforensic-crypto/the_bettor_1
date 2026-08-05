# CALIBRATION-8 — ELO/STAR ENGINE PARAMS + PERF WINDOW · shipped v2.8.7-cross · 2026-08-01

Section #4 of the dissection programme: the causal Elo chain and the C8/C11
performance window. Question: do the engine params (K, home bonus, star affine,
window) prove influence on replay, and where is the exploitable region?

## Stage A — pure Elo quality grid (705 store games; MAE on p, AUC on decisive)
K 12→64: MAE falls 0.3542→0.3370; AUC stays ~0.757-0.758 through K40, then degrades
(64: 0.754)·HF flat 45-100. Frontier interior optimum region K 32-48, but gains over
K=20 are ~0.005 MAE — marginal, and next stage shows downstream cost.

## Stage B — downstream zone metrics (633 pool, C7 weights shipped)
| variant | actW | pair | n | monotone | strong-rung W | c8/c11 fires |
|---|---|---|---|---|---|---|
| BASE K20 HF65 | 64.3 | 84.1 | 314 | ✓ | 88.9 | 41/66 |
| K32-K48 | 64.4-64.6 | ~84 | 311-312 | ✓ | 78-80 (**degraded**) | 46/90+ |
| K64 | 64.6 | 84.2 | 311 | ✗ | 75 | 46/95 |
| K40 + star (1400/2.5) | 64.6 | 83.9 | 311 | ✓ | 87.5 | 46/70 |
| K40 last6 window | 66.5 | 85.2 | 284 | ✗ | 80 | 95/85 |

K/HF verdict: **no ship.** Gains <= +0.3 actW (noise), but higher K speeds Elo drift
enough to drag the strong rung from 89% to ~78% — our showcase bucket pays the price.
HF shown empirically flat through the range — HEURISTIC OK.

## Stage C — rolling perf window (the real finding)
Season-to-date (Jul-1) → rolling last-N:
| variant | actW | pair | n | mono | C8 fired cohort (W/L) | kept W |
|---|---|---|---|---|---|---|
| BASE jul1 | 64.3 | 84.1 | 314 | ✓ | 49/22 | 64 |
| **K20 last6** | **66.2** | **85.4** | 287 | ✓ | 49/26 | 67 |
| K32 last6 | 66.4 | 85.7 | 286 | ✗ | 49/26 | 67 |
| K32 last10 | 66.2 | 86.0 | 299 | ✓ (strong 80) | 52/26 | 65 |
| K40 last8 | 66.3 | 85.4 | 288 | ✓ (strong 80) | 51/23 | 66 |

**Champion: K=20, HF=65, star (elo-1420)/2 — all unchanged — window last-6.**
The only variant that keeps the strong rung intact (88.9%), keeps the ladder
monotone, and adds actW +1.9 / pair +1.3 on a slightly leaner pool (-27 games, a
49%-win cohort correctly ejected; gate loss concentration improved to L26%).

## Split-half validation (ship discipline)
half-E: W 69.1→71.0, pair 83.6→85.5 · half-O: W 59.9→61.3, pair 84.6→85.2.
Both halves, both metrics. Ship approved.

## Shipped (v2.8.7-cross)
perfRatings perf(team): ms.filter(team).slice(-6), n>=3 else cold start.
K=20, HF=65, star affine, C11 threshold untouched — meaning C11 semantics unchanged.
Copy updated: "Recent form (last 6)" replaces current-tourney wording everywhere
(verdict card + request emitter + flag text).

## Post-ship zone table (shipped app, 633)
strong n=9 W89 pair89 · win n=64 W75 pair94 · windraw n=214 W63 pair83 ·
lean n=107 W46 pair72 · toss n=239 W43 pair72 — monotone.
Full suite green: smoke 88/88 · closure 19/19 · packs 27/27 · concat identical · replay stable.
EV-G2 unaffected (weights untouched).
Frozen calls still settle against published sheets (v2.8.5 slate).
Files: rpl/elo_sweep_a.js/.json, elo_sweep_b.js/.json, elo_sweep_c.js/.json.

## Queue
#5 draw-mass mapping (band beyond C7: neuW→Draw% calibration + goals-band link) ·
#6 venueFactor (1/0.75/0.55) · #7 effective-paths discount + NO PLAY thresholds ·
#8 zone cut points (highest overfit risk — last).
