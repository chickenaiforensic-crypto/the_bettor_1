# CALIBRATION-7 — SECTION WEIGHTS + NEUTRAL BAND · shipped v2.8.6-cross · 2026-08-01

Programme (user directive): dissect every vital app section privately; calibrate only
what proves influence on the masked replay; each ship lifts accuracy in its own
small way. Section #3 after zones/gates (C-3/4/5) and total goals (C-6).

## Section under dissection
Evidence-weight mechanics: PHASE_WEIGHT {h2h,common,third} + the ±deadband that
allocates path mass to home/draw/away shares. Never tuned since the engine was written.

## Method (pre-registered)
Pool: canonical 633 games with evidence. Primary objective: 3-way share log-loss
(floor 0.01). Guardrails: zone table — actionable (strong+win+windraw) W% and pair%,
ladder monotonicity, coverage. Validation: every candidate must win log-loss on
BOTH date-split halves. Sweep harness re-implements aggregate reweighting (validated:
baseline config reproduces the shipped 633 zone table bit-for-bit before any change).

## Stage 1 (one-factor moves, band fixed 0.25)
Third down 1.5→0.75: ll −0.021, actW +2.5 — third was overweighted ~2×.
Common up 2→3: same direction, confirms third:common ratio was wrong, not scale.

## Stage 2 (joint grid, winner region)
Band widens → share calibration improves monotonically; zone quality climbs with it.

## Stage 3 (frontier check + integrity)
Optimum at band 0.50 (0.55+ rises; at 0.65 mean draw share 24.5% overshoots the
24.3% actual — band confirmed NOT at grid edge). third 0.25 breaks monotonicity.

## Champion
PHASE_WEIGHT = {h2h:3, common:3, third:0.75} · NEUTRAL_BAND = 0.50
| metric | baseline 3/2/1.5 @0.25 | champion |
|---|---|---|
| log-loss (both halves) | 1.1637 (1.1281/1.1993) | **1.0728 (1.0782/1.0672) ✓** |
| mean draw share vs 24.3% actual | under-cooked | **23.1% ✓** |
| actionable W | 59.1% (n=357) | **64.3% (n=314)** |
| actionable pair | 81.0% | **84.1%** |
| zone ladder | 80/70/53/48/38 | **89/74/61/48/42 monotone ✓** |
Trade: actionable pool −12% (weak games honestly demoted to lean/toss).
Runner-up 3/2/0.5@0.50 within noise (ll −0.0006); 3/3/0.75 picked on primary metric.

## Post-ship zone table (shipped app, 633)
strong n=9 W89 pair89 · win n=68 W74 pair93 · windraw n=237 W61 pair81 ·
lean n=88 W48 pair73 · toss n=231 W42 pair72. Monotone.

## Dependency chain (audited)
- EV-G2 goals read consumes path weights → full goals recalibration re-run:
  K=10 re-confirmed (MAE 1.302), thresholds 2.40/2.80 kept (pre-registered,
  no chasing), table re-measured: LOW n=68 U2.5 **57.4%** · MID n=332 coin-flip ·
  HIGH n=233 O1.5 **82%** / O2.5 55%. EVG2_TABLE in app updated + smoke re-pinned.
- validate_closure 3 multiplicative pins rebased to v2.8.6 values (old pins were
  weight-products; zone_tally reproducing the sweep champion on shipped code is
  the integrity proof).
- smoke 86/86 · closure 19/19 · packs 27/27 · concat identical · replay_test stable.
- zone_tally_ctx label: v2.8.6.

## Frozen vs forward (settlement discipline)
All published frozen calls (Akron TB WIN 70.6 HIT; slate SLATE-2026-08-01-03.md)
settle against the published numbers. v2.8.6 changes FORWARD computations;
the slate sheet carries a top-note with the delta list. Notable forward shifts:
Orenburg–Zenit TB WIN 82.5→**TB STRONG 85.2**; Liberec 58.6 WIN-DRAW→TOSS 46.2
(frozen governs tonight); Baltika–Dynamo draw share 35.9→46.4 (still TOSS);
Bohemians–Hradec leader flips TA→TB (still TOSS both sides).

## Queue (programme continues)
#4 Elo/star engine params (K=20, home+65, star curve) · #5 draw-mass mapping beyond
the band (draw-band 2.2–2.5 link from C-6) · #6 venueFactor (1/0.75/0.55) ·
#7 effective-paths discount + NO PLAY thresholds · #8 zone cut points (last,
highest overfit risk).
