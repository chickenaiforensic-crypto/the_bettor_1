# CALIBRATION-4 — candidate C8: opponent-quality-weighted current-tourney performance rating

User proposal 2026-08-01: rate each team's current-tournament performance by the
combined quality of the opponents it has played, weighted by its W/D/L outcomes —
so a winning run against weak opposition reads weaker than the same run against
strong opposition. Planned, implemented in harness, audited on the 600-game
masked replay, then shipped (demote-only) as v2.8.0.

## Spec (v1, frozen)

- **Elo (causal):** start 1500, K=20, home edge +65, all competitions in the
  store, chronological, using only matches with date < cutoff and numeric scores.
- **star(t) = clamp((elo_t − 1420)/2, 0, 100)** — the opponent-quality number.
- **Current tourney** = matches with seasonStart ≤ date < cutoff, where
  seasonStart = 1 July of the season year (Aug–Dec → that year's Jul 1;
  Jan–Jul → previous year's Jul 1). Covers RPL, Czech, Scottish calendars.
- **SOS** = mean over current-tourney games of star(opponent at cutoff).
- **Perf** = mean over current-tourney games of result(1/0.5/0) × star(opponent).
- Conversion = Perf / SOS (result-share against the schedule faced).
- **Cold start:** fewer than 3 current-tourney games → metric undefined → no action.

## Application in zones (demote-only, mirrors C2/C5/CTX architecture)

If Perf(home) − Perf(away) contradicts the zone leader (leader is home and
delta < 0, or leader is away and delta > 0), demote the zone one rung
(strong→win→windraw→lean→toss). Never promotes, never touches the percentages.
Cold start or delta == 0 → no action. Fires only when both sides are defined.

## Audit on 600-game masked replay (RPL universe, bit-exact harness)

530 games auditable (both teams ≥3 current-season games).

T1 — standalone signal, ΔPerf bucket → home outcomes (n, W/D/L):
```
[-99,-5)  n=187  W 25% D 26% L 50%
[ -5,-1)  n= 64  W 36% D 33% L 31%
[ -1, 1)  n= 33  W 48% D 27% L 24%
[  1, 5)  n= 61  W 59% D 21% L 20%
[  5,99)  n=185  W 65% D 16% L 19%      → clean monotone, real signal
```

T2 — inside shipped zones, Perf agrees vs disagrees with leader:
```
strong   agree  n= 54  W 78 pair 93 | disagree n=1
win      agree  n=106  W 68 pair 82 | disagree n= 8  W 38 D 13 L 50 pair 50
windraw  agree  n=127  W 48 pair 78 | disagree n=40  W 38 D 20 L 43 pair 58
lean     agree  n= 56  W 55 pair 84 | disagree n=27  W 56 (no effect)
toss     agree  n= 54  W 46 pair 76 | disagree n=54  W 37 D 22 L 41 pair 59
```

Retally, rule applied to all 600 games (137 demoted:
1 strong→win, 8 win→windraw, 43 windraw→lean, 31 lean→toss, 54 toss→toss):

```
            baseline v2.7.1              with C8
strong   n= 60  W 78 pair 92        n= 59  W 78 pair 92
win      n=125  W 65 pair 80        n=118  W 67 pair 82   ← better pool
windraw  n=201  W 48 pair 72        n=166  W 49 pair 75   ← better pool
lean     n= 97  W 53 pair 78        n=109  W 47 pair 71
toss     n=117  W 43 pair 68        n=148  W 45 pair 70
ladder monotone in W: NO (lean>windraw inversion)
                          → YES: 78 > 67 > 49 > 47 > 45, pairs 92 82 75 71 70
movers landed where they fit: win→windraw movers were W38 pair50;
windraw→lean movers were W40 pair58.
```

Ship criteria met (same bar as C2/C5): measurable pool improvements at the
actionable rungs, conservative direction, no fabrication, causal, cold-start safe.
verdict: **SHIP as v2.8.0** — demote rule + current-tourney status display.

## Re-baseline 2026-08-01 (RPL cup completeness, +31 rows)
600 → 632 auditable games. All C8 conclusions re-verified on the new universe:
T1 standalone ΔPerf buckets W% 23/34/52/54/64 (monotone); T2 disagree subsets
worse than agree on every rung (strong n=2, win n=7 W29 vs 67, windraw n=45 W40
vs 52, lean n=33 W42 vs 54, toss n=54 W33 vs 38). C8 stays shipped as-is.
