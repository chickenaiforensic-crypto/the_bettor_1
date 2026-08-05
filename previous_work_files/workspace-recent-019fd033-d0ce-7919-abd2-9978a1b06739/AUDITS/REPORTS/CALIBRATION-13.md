# CALIBRATION-13 — TB away-leader honesty gate (SHIPPED v2.9.0-cross)

Date: 2026-08-01. Pool: canonical 633-game masked replay (post-mute state:
IA-01/02/03 muted rows carry no evidence). Engine: C7 weights+band, C8 last-6
window, C11 star guard, C9 display calibration.

## Objective (pre-registered at measurement, decision delegated by user 2026-08-01)

Zones led by the AWAY side (TB) over-claim their top rungs. Correct the labels
without cutting coverage. Demote-only; never boosts; TA side untouched.

## Guardrails

- actW and pair must not regress in EITHER chronological half.
- Actionable set and its size (n=304) must not change (all C13 moves stay inside
  strong/win/windraw).
- Raw shares, the S_ ladder, CAL9 display, perf ratings and goals read untouched.

## Evidence (633-game replay, split by leader side)

Home/away experiment window: HF=0 replay leaves the zone table ~unchanged — home
advantage is already priced into the evidence itself. The ACTIONABLE asymmetry
is instead in who leads:

| leader side | n | W% | pair% | half A W/pair | half B W/pair |
|---|---|---|---|---|---|
| TA (home) | 152 | 72.4 | 85.5 | 74.0 / 85.7 | 70.7 / 85.3 |
| TB (away) | 152 | 59.9 | 85.5 | 59.5 / 86.5 | 60.3 / 84.6 |

Pair rates are IDENTICAL in both halves — the evidence finds the right pair;
it is the win-label that over-fires on the away side. Rung detail:

| rung | TA n / W% / pair% | TB n / W% / pair% |
|---|---|---|
| strong | 9 / 100 / 100 | 6 / 83.3 / 100 |
| win | 32 / 78.1 / 87.5 | 37 / 62.2 / 94.6 |
| windraw | 111 / 68.5 / 83.8 | 109 / 57.8 / 82.6 |

TB strong runs like a TA win; TB win runs like a windraw. Both halves replicate.

## Candidates measured

- **V1 — demote ALL TB zones one rung:** actW A 71.1 / B 70.4, pair A 86.6 /
  B 87.8 (both halves up) but actionable n 304 → 195 (−36% coverage). Real
  frontier trade, against the standing coverage preference.
- **V2 — demote TB strong→win and TB win→windraw only (SHIPPED):** totals
  identical to pre-C13 in both halves (66.9/86.1 · 65.4/85.0, n=304); rungs
  purified (table below). Zero regression, zero coverage loss.
- **V3 — demote TB win only:** subsumed by V2; rejected (leaves TB strong
  dishonest).

Decision: V2 shipped. V1 recorded as an available strict-mode trade
(+4-5 actW pts / +1.5 pair pts for −36% volume) — not default; user may
request it as an opt-in later.

## Shipped implementation (v2.9.0-cross)

Gate C13 in `computeZoneCtx`, after C11, before CTX:
`if (zinfo.side === "TB" && (zinfo.key === "strong" || zinfo.key === "win"))`
→ demote one rung, marker `c13From`, tag suffix "(TB drop: away-leader
honesty)", `tb` flag in the zone line. ZoneLadder help notes refreshed to the
post-C13 cohorts.

## Shipped zone table (zone_tally_ctx.js, 633 games)

| zone | n | W% | pair% |
|---|---|---|---|
| strong | 9 | 100.0 | 100.0 |
| win | 38 | 78.9 | 86.8 |
| windraw | 257 | 63.0 | 84.8 |
| lean | 101 | 47.5 | 73.3 |
| toss | 228 | 38.6 | 68.9 |

Actionable: n=304, actW 66.1 / pair 85.5 · half A 66.9/86.1 (n=151) ·
half B 65.4/85.0 (n=153) — bit-identical to v2.8.9 totals, labels now honest.

## Frozen vs forward

- SLATE-2026-08-01-03.md stays governed by its frozen v2.8.5 numbers; C13
  changes nothing retroactively. Settlement continues against the frozen sheet.
- Forward note (instance, NOT evidence): the frozen TB lean that settled
  2026-08-01 (Makhachkala 2-1 Loko) is one out-of-sample game consistent with
  V1's direction. V2 deliberately leaves the lean/toss rungs untouched — that
  is the abstention lane, agreed with the user same day. One game moves nothing.
- Forward audits (audit_fixtures.js) inherit C13 via computeZoneCtx.

## Dependency chain

- Draw replay / CAL9: share-based mapping, bit-identical (no share moved).
- C10/C11/C12 sweeps: closed no-ships on the S_ axis; C13 relabels TB zones
  without moving any replay total — conclusions stand.
- EV-G2: goals reader untouched.

## Harness state at ship

smoke_test.js 108/108 (C17 pin group added, incl. functional TB-demote /
TA-untouched checks) · validate_closure 19/19 · validate_packs 27/27 ·
verify_rpl_pack import clean (26 teams, 644 matches, 6 sources) ·
concat_test 61 rows · verify_migration / verify_return_path diagnostics normal
(demote-only invariant holds under C13).
