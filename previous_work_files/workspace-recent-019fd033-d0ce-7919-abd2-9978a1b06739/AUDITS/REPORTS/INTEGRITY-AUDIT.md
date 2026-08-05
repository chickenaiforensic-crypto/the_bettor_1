# INTEGRITY-AUDIT — market screen for "controlled games" → **MUTE channel SHIPPED (v2.8.9)**

## Verdict on the system question
- **No league-wide fixing signal.** 79 RPL games where a favorite was ≥65% market-implied: expected
  failures **22.7**, observed **13** (z = −3.43). Favorites fail *less* often than fair odds predict.
- **But three traceable patterns exist in the corners:**
  1. **Zenit concentration** — 6 of 13 flags touch them; brand odds-shading habitually overprices them.
  2. **Season-boundary timing** — flags cluster at winter-break edges (Dec 1/7, Mar 1/8) and openers (MD2).
  3. **Nothing-to-lose beneficiaries** — Akron (3 flags) and Krylya (3) absorbing rotated giants' points.

## What shipped — 3 rows muted (owner-approved mechanism, data-level, reversible)
| flag | match | market said | happened |
|---|---|---|---|
| IA-01 | 2024-12-07 Zenit 1-2 Akron | 82.8% implied home win | lost 1-2, winter-break edge |
| IA-02 | 2024-12-01 Zenit 2-3 Krylya | 76.5% | lost 2-3, **same week's second Zenit home collapse** |
| IA-03 | 2025-04-11 Spartak 1-2 Dynamo Makhachkala | 73.5% | lost 1-2 to relegation side, run-in |

**Mute ≠ delete.** `MUTE|date|home|away|reason|sourceId` rows in `packs/russian-team-pack.txt`
(+ generator `rpl/make_pack_rpl.py`, + `muted` flag in `rpl/rpl_universe.json`). Muted rows stay
visible for audit but carry **zero evidence**: H2H/common/level-3 paths (choke point `beforeCutoff`),
Elo chain, and EV-G2 goals means all skip them. One pack edit unmutes.
Watchlist kept (no action): CSKA 0-1 Sochi, Spartak 0-3 Baltika, Dynamo M 1-2 Akron, 6 draw-tier rows.

## Before/after on the 633-game masked replay
| metric | before | after (3 muted) |
|---|---|---|
| STRONG | n=9 W89/pair89 | **n=15 W93/pair93** |
| WIN | n=64 W75/pair94 | n=69 W70/pair91 |
| WIN-DRAW | n=214 W63/pair83 | n=220 W63/pair83 |
| actW / pair (actionable) | 66.2 / 85.4 (n=287) | 66.1 / 85.5 (n=304) |
| halves A / B actW | 66.4 / 66.0 | 66.9 / 65.4 |
| halves A / B pair | 84.9 / 85.8 | 86.1 / 85.0 |
| CAL9 display log-loss | 1.0031 | 1.0031 |
| EV-G2 goals MAE | 1.302 | **1.302** (LOW 71·MID 333·HIGH 229 counts ≈same) |

Accuracy is **quality-preserving** while 3 non-trusted stats stop poisoning Zenit/Spartak ratings;
STRONG coverage doubles at a higher hit-rate because muted losses no longer drag the Elo chain.
72/633 zone labels and 6 leader flips moved — expected: the muted games were evidence widely.

## How we use it to our advantage (ongoing)
1. **Trusted slate context:** watchlist rows ride along as slate notes (never raise a zone).
2. **Market-inversion spots (your call, outside the app):** brand giants ≥ ~80% implied at season
   boundaries are where prices are soft — our evidence zones don't read prices, so a modest app
   statement next to an extreme market price flags a candidate value-underdog window (Akron/Krylya pattern).
3. **Re-screen on refresh:** when football-data fills 26/27 odds + cup coverage, rerun
   `rpl/market_audit.py`; new flags go through the same review → user-approved MUTE only.

## Harness
smoke 102/102 (6 new MUTE pins) · closure 19/19 · packs 27/27 · zone_tally_ctx = post-mute table ·
`rpl/mute_compare.js/.json` holds the exact before/after rows · generator `rpl/make_pack_rpl.py` re-emits mutes.
App: **v2.8.9-cross**. Frozen slate numbers (SLATE-2026-08-01-03) stay frozen under v2.8.5 rules.
