# CALIBRATION-5 — C11 cold-trailer star guard (shipped v2.8.1, 2026-08-01)

Origin: user-commissioned failure analysis of the 26 leader-losses on STRONG+WIN
(rpl/replay_losses.json). Injuries/pre-match conditions were explicitly NOT usable:
results-only doctrine; CTX flags are user-supplied, demote-only, never direction inputs.

## Pool reconciliation (audit hygiene)
The canonical masked replay = app seeds (29) + imported packs (hibernian, malisheva,
malisheva-closure → 61 pre-seeded) + RPL universe (643) = 704 games, 632 with evidence.
Earlier partial-pool scripts (617) missed the pack imports; re-derived on the canonical
pool. Determinism confirmed: only 2 Math.random uses, both ID generation.

## Candidates measured (demote-one-rung gates, full 632 pool)
- C9 contra-section gate — REJECTED: flagged cohort n=7 won 71% (W5 L2); demoting
  would be net-negative despite catching 2 losses. Do not chase individual failures.
- C11 trailer-star<5 — cohort n=74 (of 167 actionable): W62 pair77 L23 vs
  trailer-star>=5 cohort (n=91) W70 pair90 L10. Separates 13 pair-pts.
- Also measured, no action: TB star-gap>=40 n=57 W68/pair88 (big-gap aways are fine);
  TB agree-3 W62/pair85 (no sweep anomaly); Loko-away W9 D2 L5 of 16 (small-n, and
  team-named rules are out of doctrine).

## C11 audit (ship bar, same as C2/C5/C8)
- Cohort split: from strong n=23 W70/pair87 (16W 4D 3L); from win n=51 W59/pair73
  (30W 7D 14L). Catches 17 of 26 actionable losses, 5 of 9 big-margin losses.
- Post-ship ladder (632): strong n=15 W80/pair93 · win n=101 W69/pair89 ·
  windraw n=240 W53/pair77 · lean n=116 W48/pair72 · toss n=160 W38/pair68.
  Strictly monotone on W and pair. Verified in-app bit-exact vs offline simulation.
- Trade-off (stated, accepted): actionable pool 167→116 (-31%); demoted calls
  surface one rung down (windraw absorbs 74 games, pair 78→77).
- Semantics: STRONG/WIN only; trailer = opponent of zone leader; star from the
  causal Elo chain (strictly pre-cutoff); pr null (no date) → no-op; demote-only.
- Order in computeZoneCtx: C2 gate → C5 → C8 → C11 → CTX flags.
- Overfit note: one round-number parameter (star<5), tuned on the calibration pool
  (as C2/C5/C8 were). Prospective slate + forward log remain the final arbiters.
- Harnesses: smoke 79 ✓ packs 27 ✓ closure 19 ✓ concat identical ✓ replay_test
  unchanged ✓. Build: build_d_c11.py (11 edits).
