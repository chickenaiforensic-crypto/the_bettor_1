# RPL masked replay — Rubin Kazan / Akron Tolyatti (rich-data test)

Date run: 2026-08-01 · Engine: app-v2.6-cross (v2.6.7-cross), unmodified, inside node harness
Cutoff rule: strict causality `date < cutoff` · Venue labels: all standard home grounds (`home`) — Akron's home games are Samara Arena in both seasons (their regular venue, ~100 km from Tolyatti), so no relocation discount applies.

## Data universe (built and verified for this test)
- **610 matches**: 488 league (full 2024-25 + 2025-26 RPL seasons + verified 2026-27 MD1, 24–26 Jul) + 121 cup ties (incl. knockouts; shootout nights kept at 90-min score per blueprint) + 1 super cup.
- **Integrity proof: both RPL seasons reconcile 16/16** against RSSSF final tables (W-D-L, GF, GA per club) — no missing or phantom league rows.
- h2h series complete: 6 meetings 2024–2026 (Rubin: 3W, Akron: 0W, 2D; GD +9 Rubin).
- Known gaps, disclosed: (a) Akron's May-2026 relegation playoff double-header is not in RSSSF's parseable listings (≤2 rows, June form only); (b) 22 cup ties with AET/pen marks — kept at 90-min result where that was the line, none involved target clubs; (c) MD1 2026-27 added manually (cross-checked 3 sources: betexplorer, worldfootball, ESPN); (d) app boots with 29 embedded seed rows (Hibernian/Malisheva) — graph-disjoint from RPL web, zero influence.
- Analyzer runs: **I have not seen today's score.** Forward B is pre-result from my side.

## REPLAY A — target stripped: Rubin v Akron, 18 Apr 2026 (Kazan) · actual 1-1
Cutoff 2026-04-18; the fixture itself and the 29 later league rows + cups are invisible to the engine.

| Section | Paths | Weighted est | Direction |
|---|---|---|---|
| H2H (5 prior meetings) | 5 × w3 | **+1.80** | Rubin |
| Common-opponent differential (16 shared) | 16 × w2 | −0.07 | flat |
| Opponent-of-opponent chains | 20 × w1.5 | +1.02 | Rubin |
| **Aggregate** | effective 20 | **+0.72** | **Rubin lean** |
| Classification | — | — | **Lean only — "cross-border/unrated calibration is not loaded."** No percentages, no recommendation. |

Grade: direction Rubin, result draw → home-lean did not land (draw = loss for a home lean under the settle rule). The NO PLAY wrapper meant nothing was staked mechanically.

## FORWARD B — blind read: Akron v Rubin, 1 Aug 2026 (Samara) · result pending
Cutoff 2026-08-01; entire universe above visible except today's game.

| Section | Paths | Weighted est | Direction |
|---|---|---|---|
| H2H (all 6 meetings) | 6 × w3 | **−1.50** | Rubin |
| Common-opponent differential | 16 × w2 | −0.18 | flat |
| Opponent-of-opponent chains | 20 × w1.5 | −1.30 | Rubin |
| **Aggregate** | effective 21 | **−0.90** | **Rubin lean (away)** |
| Classification | — | — | **Lean only — "cross-border/unrated calibration is not loaded."** No percentages, no recommendation. |

Settle after FT with the 90-min score only.

## What this adds to the systems analysis
1. **Classifier guardrails held on rich foreign data.** 41 evidence paths, effective 20–21 — and the system still refuses a number for an unrated league. Output = direction + no-play wrapper, no fabricated probability. This is the designed behaviour, reproduced outside the test bench.
2. **The known h2h weakness reproduced on a second, independent league.** The h2h phase still prices raw historical GD at full weight with no venue-flip algebra and no shrinkage: the +1.80/−1.50 leans are carried by the 2024 blowouts (4-0, 3-0) even though the two most recent meetings were draws. That is the same failure shape the 61-game backtest isolated — **Candidate A (venue-corrected h2h + shrinkage) is now corroborated on an independent dataset.**
3. **Common-opponent differential was the stable middle** in both runs (≈0). In the backtest it was the best section (57%); here it correctly refused to join the h2h noise.
4. **Third chains followed the h2h sign both times** (magnitude diluted by web size). Cheap corroboration, not independent signal — chains are built from the same matches.
5. Blinding honest ledger: replay A = pure replay (data before 18 Apr only); forward B = true blind (result unseen at run time). MD1-2026/27 results were needed *for* B and verified from three sources; no later result was touched.

Artefact note: first run with id-less rows produced "effective 1" — injection artifact, fixed by writing exact app fingerprints before push; numbers here are the corrected run. Directional aggregates were identical in both runs.
