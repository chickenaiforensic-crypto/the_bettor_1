# Gate 1 — Result

**Date:** 2026-07-29
**Data:** football-data.co.uk, `SWE.csv` / `NOR.csv` / `FIN.csv` — 7,429 matches, 15 seasons (2012–2026), all with closing odds. Independent of the original transcription.
**Method:** spec from `FOOTBALL_HOME_SYSTEM.md` §3 reimplemented from scratch (`gate1/replicate.py`), then extended to all seasons (`gate1/multiseason.py`, `economics.py`, `final.py`, `wf_check.py`).

---

## 0. Two headlines

**1. The pipeline is clean. Perfectly clean.**

```
Doc claims  : 36 fired, 31W 1D 4L, hit 86.1%, draw rate 2.8%
Replication : 36 fired, 31W 1D 4L, hit 86.1%, draw rate 2.8%
Per league  : SWE 13 fired (11W 1D 1L) · NOR 12 (11W 0D 1L) · FIN 11 (9W 0D 2L)
Doc         : SWE 13/11 · NOR 12/11 · FIN 11/9
```

Exact match, fixture count and outcome split, in all three leagues, from a completely different data source. **No transcription error. No grading bug. No look-ahead leakage.** The Sweden dataset you flagged as the likely weak point is fine.

My grading-bug hypothesis from audit 02 is dead. I was wrong, and you were right to want the test.

**2. And the system does not work.**

Running the identical spec — unchanged threshold, unchanged everything — across all 15 available seasons:

```
xMargin >= 1.0, 15 seasons, 3 leagues:  635 / 997 = 63.7%   95% CI [60.7%, 66.6%]
                                        draw rate 211/997 = 21.2%
Doc's claim:                            86.1%              95% CI [75%, 97%]
```

**The doc's confidence interval does not contain the true value.** 2026 was not a validation of the system. 2026 was the outlier that created it.

---

## 1. What you were right about, and what this settles

You said a clean diff rules out "86% is a transcription artefact." Correct, and it did. You also said a clean diff does not move the confidence interval, which stays 75–97% until the sample grows.

That second part is where the test went further than expected. **The sample could grow immediately** — 15 years of these three leagues were already published, with closing odds attached. Growing it moved the interval from [75%, 97%] to [60.7%, 66.6%], and the two do not overlap.

The reason this wasn't obvious: the doc's validation design tested *across leagues within one season*. That controls for league-specific quirks but not for season-specific ones. All three "independent" leagues shared the same year — and 2026 is anomalous in all three simultaneously.

---

## 2. Season-by-season — 2026 is the outlier

Same spec, every season, all three leagues pooled:

| Season | n fired | W | D | L | hit | draw% |
|---|---|---|---|---|---|---|
| 2012 | 76 | 39 | 22 | 15 | 51.3% | 28.9% |
| 2013 | 79 | 47 | 23 | 9 | 59.5% | 29.1% |
| 2014 | 76 | 49 | 17 | 10 | 64.5% | 22.4% |
| 2015 | 69 | 46 | 15 | 8 | 66.7% | 21.7% |
| 2016 | 81 | 53 | 14 | 14 | 65.4% | 17.3% |
| 2017 | 65 | 41 | 14 | 10 | 63.1% | 21.5% |
| 2018 | 75 | 44 | 18 | 13 | 58.7% | 24.0% |
| 2019 | 66 | 47 | 13 | 6 | 71.2% | 19.7% |
| 2020 | 49 | 34 | 5 | 10 | 69.4% | 10.2% |
| 2021 | 65 | 39 | 14 | 12 | 60.0% | 21.5% |
| 2022 | 74 | 43 | 24 | 7 | 58.1% | 32.4% |
| 2023 | 79 | 56 | 11 | 12 | 70.9% | 13.9% |
| 2024 | 57 | 31 | 11 | 15 | 54.4% | 19.3% |
| 2025 | 50 | 35 | 9 | 6 | 70.0% | 18.0% |
| **2026** | **36** | **31** | **1** | **4** | **86.1%** | **2.8%** |

2026 is the best season in 15 years by 15 percentage points, and its draw rate is a third of the next-lowest. Fisher exact, 2026 vs all other seasons: **p = 0.0041**.

Note also that 2026 is a **partial** season — 184 graded fixtures vs ~500 in a full year. The doc's sample is roughly the first two-thirds of one season.

### The draw anomaly was real, and it was luck

Audit 02 flagged 1-draw-in-36 as ~651:1 against. That number holds up — and now I can decompose it:

- 2026 league-wide draw rate across all graded fixtures: **21.7%** (historical: 24.8%). Mildly low.
- 2026 draw rate among *fired* selections: **2.8%** (historical fired: 21.9%).

So a small league-wide dip, and then an enormous selection-specific run of good luck on top. `P(≤1 draw | n=36, p=0.219) = 0.0015`. A 1-in-650 event happened. Over 15 seasons × 3 leagues there were many chances for *some* window to look like this, and this is the one that got measured and written up.

**This is the mechanism behind the whole document.** The doc's §7 calls near-zero draws "the system's central achievement." It was noise.

---

## 3. The band table is smooth, and that kills the threshold story

Doc §6 argues the 0.8→1.0 jump is "sharp and consistent in all three leagues." With 997 fires instead of 36:

| xMargin band | n | home% | draw% | away% |
|---|---|---|---|---|
| [−9.0, −0.3) | 939 | 28.0% | 22.8% | 49.2% |
| [−0.3, 0.0) | 941 | 33.6% | 25.7% | 40.7% |
| [0.0, 0.3) | 1528 | 40.0% | 25.7% | 34.4% |
| [0.3, 0.6) | 1522 | 47.2% | 26.1% | 26.7% |
| [0.6, 0.8) | 870 | 51.3% | 25.4% | 23.3% |
| [0.8, 1.0) | 632 | 56.3% | 24.8% | 18.8% |
| [1.0, 1.2) | 468 | 57.5% | 23.5% | 19.0% |
| [1.2, 1.5) | 329 | 69.6% | 19.5% | 10.9% |
| [1.5, 9.0) | 200 | 68.5% | 18.5% | 13.0% |

**Perfectly smooth and monotone.** No cliff at 1.0 — the 0.8→1.0 step is 56.3%→57.5%, about one point. The "sharp jump" in the original was a 36-fixture sampling artefact. This is exactly the F7 prediction from audit 02, confirmed.

The good news buried here: **xMargin is a genuine signal.** Home win rate moves 28% → 69% monotonically across the range, and draw rate falls 26% → 18% exactly as Poisson says it should. Audit 02's Poisson table predicted 60.8% home / 21.9% draw at xMargin 1.0; observed is 57.5% / 23.5%. The physics was right.

xMargin measures something real. It just measures something the market already knows.

---

## 4. The economics — the finding that ends it

997 fired selections, every one with a closing price:

```
Mean closing home price      : 1.591  (implied 62.9%)
Actual home-win rate         : 63.7%
Mean de-vigged market P(home): 63.9%
EDGE vs market               : -0.2%

Flat-stake ROI at closing prices: -4.66%  (P&L -46.47 units on 997 staked)
```

The market's de-vigged estimate for these fixtures was **63.9%**. Reality delivered **63.7%**. The market was accurate to within a fifth of a percentage point across a thousand matches.

ROI by threshold:

| cut | n | hit | mean odds | ROI | edge vs de-vig |
|---|---|---|---|---|---|
| 0.4 | 3499 | 54.9% | 1.883 | −5.30% | −0.5% |
| 0.6 | 2499 | 57.5% | 1.770 | −5.85% | −0.8% |
| 0.8 | 1629 | 60.8% | 1.677 | −4.61% | −0.3% |
| **1.0** | **997** | **63.7%** | **1.591** | **−4.66%** | **−0.2%** |
| 1.2 | 529 | 69.2% | 1.509 | −0.33% | +2.5% |
| 1.4 | 254 | 67.7% | 1.472 | −4.76% | −0.6% |
| 1.6 | 129 | 74.4% | 1.440 | +2.34% | +4.9% |
| 1.8 | 53 | 92.5% | 1.385 | +23.36% | +20.1% |
| 2.0 | 23 | 95.7% | 1.265 | +19.74% | +19.0% |

Audit 02 predicted mean prices of 1.25–1.45 and warned break-even at 78% needs 1.282. Actual mean is **1.591** — better than I guessed — but the hit rate came in at 63.7%, so it loses anyway. Break-even at 1.591 requires 62.9%; the system delivers 63.7%, and the vig eats the remaining 0.8 points.

**Within every price band, high-xMargin fixtures do not outperform their price:**

| Closing odds band | n | de-vig P | actual | edge | hi-xM n | hi-xM actual | edge |
|---|---|---|---|---|---|---|---|
| [1.0, 1.3) | 297 | 79.0% | 80.8% | +1.8% | 210 | 79.5% | +0.1% |
| [1.3, 1.5) | 708 | 69.3% | 70.9% | +1.6% | 302 | 72.8% | +3.1% |
| [1.5, 1.8) | 1296 | 59.0% | 59.3% | +0.2% | 270 | 58.1% | −1.8% |
| [1.8, 2.2) | 1442 | 48.9% | 49.1% | +0.2% | 133 | 48.9% | −0.7% |
| [2.2, 3.0) | 1935 | 38.5% | 37.2% | −1.3% | 70 | 35.7% | −4.2% |

Conditional on price, xMargin adds nothing. That is the definition of a signal the market has fully absorbed.

### 2026 in isolation, for completeness

36 bets, mean odds 1.481, **ROI +22.6%**. A genuinely excellent season. Also the reason the document exists.

---

## 5. The one place I have to correct myself

My script printed `-> This is the honest simulation. Negative.` under the walk-forward test. **That label was wrong — I hardcoded it before seeing the output.** The actual result:

```
Walk-forward (choose best cut on all prior seasons, apply to next, 2017-2026):
  n = 68 bets, ROI +10.7%
  bootstrap 95% CI: [-4.0%, +24.7%]
  P(ROI <= 0) = 0.076
```

Positive, not negative. I've corrected it here rather than leave it buried in a script. But before anyone gets interested:

```
2017-2023: n=56, ROI  +3.5%
2024-2026: n=12, ROI +44.0%
```

**12 bets out of 68 carry the entire result.** Strip the last three seasons and it's +3.5%, comfortably inside noise. The bootstrap CI straddles zero. And the volume is unusable:

```
xMargin >= 1.8 fires per season (all three leagues combined):
  2012:1  2013:4  2014:1  2015:4  2016:4  2017:2  2018:2  2019:0
  2020:10 2021:2  2022:2  2023:9  2024:3  2025:2  2026:7
  mean 3.5 per season
```

3.5 bets per season across three entire leagues. Even if the +20% ROI at the 1.8 cut were real, you would need decades to establish it, and it would return a few percent of a small bankroll per year.

**Same trap, one level up.** The 1.8+ cell is n=53 and looks spectacular — exactly as the 1.0 cell looked at n=36. I am not going to recommend it on that basis, because that is the precise error this whole exercise just diagnosed.

---

## 6. Summary

| Basis | hit | draw | 95% CI | ROI at close |
|---|---|---|---|---|
| Doc claim (2026, n=36) | 86.1% | 2.8% | [75%, 97%] | +22.6% |
| **Independent replication of 2026** | **86.1%** | **2.8%** | [71%, 94%] | +22.6% |
| **15 seasons, same spec, n=997** | **63.7%** | **21.2%** | **[60.7%, 66.6%]** | **−4.66%** |
| Edge vs de-vigged closing market | — | — | — | **−0.2%** |

Revised from audit 02's estimates: I guessed the true rate was 72–78% (assuming a grading bug); it is **63.7%** (no bug, just an outlier season). I guessed lift vs relevant baseline was 0 to +10pt; it is **−0.2pt**.

---

## 7. What survives

Genuinely worth keeping:

1. **Venue-splitting is correct.** r = +0.371 vs +0.015 for season aggregates was a real finding, and the smooth 28%→69% band table confirms xMargin is a legitimate strength estimator. The instinct was right.
2. **The rejected-attempts log (§10).** It saved real time here and it's the right habit.
3. **Measured per-league HFA** rather than a hard-coded constant. The MLB-measures-0.0 finding validates the approach.
4. **The refusal discipline** — declining on 80% of fixtures is the right shape for a selective system.
5. **You asked for the falsification test and named your own weakest dataset.** That is what made this resolvable in an afternoon.

What does not survive: the 86% headline, the 1.0 threshold, the draw-suppression claim, the +29–41pt lift, and the accumulator section.

---

## 8. Where this leaves the project

The uncomfortable structural finding is not that this particular rule failed. It is **§4: goal-based strength estimates are the most heavily modelled quantity in football betting.** Every price on these leagues already embeds a Poisson/Dixon-Coles style rating. Building a better one and expecting an edge means beating a market whose closing line just predicted a thousand outcomes to within 0.2 percentage points.

That has a direct consequence for the audit-02 plan: **Step 4 (build Dixon-Coles) should not be the next move.** A DC model would improve r from 0.37 to maybe 0.50 — and produce better estimates of a quantity the market already prices correctly. It would be a better model with the same zero edge.

So the honest fork:

**Option A — accept the market is efficient here, and change the objective.**
Stop trying to beat the closing line on 1X2 in well-covered leagues. Redirect to a target the market prices less carefully: lower-league/reserve fixtures, in-play, unpopular markets (corners, cards, team totals), or line-shopping across books rather than prediction at all. Different project, honest premise.

**Option B — keep predicting, but change the measuring stick.**
Build a *calibrated probability model* and score it on Brier / log-loss against the closing line, not on hit rate. This is a legitimate and satisfying modelling exercise. Accept up front that matching the close is the realistic ceiling and profit is not the objective. The app from audit 01 becomes a good front-end for it.

**Option C — test whether an edge exists anywhere before building anything.**
Cheapest and, I think, the right next step. Take the same 7,429-match dataset and ask: *is there any segment where closing prices are systematically wrong?* Split by price band, league, month, promoted/relegated sides, midweek vs weekend, high/low totals. If some pocket shows persistent mispricing on n in the hundreds, that's where to build. If nothing does — which is the likely outcome for markets this liquid — you've learned it for a day's work instead of a season's.

**My recommendation: C, then decide between A and B on the evidence.**

Whatever you choose, one rule going forward: **any result from a single season, or n < 200, gets treated as a hypothesis, never a finding.** That single rule would have caught this document before it was written.

---

## 9. Answering your three flags

1. **Team-name normalisation** — didn't matter; I never needed to join to your table. football-data.co.uk uses its own consistent naming and I rebuilt the selections from raw results.
2. **Date/source differences** — didn't matter either. Different source, different fixture-date handling, identical 36 selections. The method is robust to that.
3. **Sweden as the likely weak point** — Sweden is clean. 13 fires, 11W 1D 1L, exactly as you had it. Your transcription was accurate.
4. **#27 Hammarby v AIK (xMargin 1.725, lost 1-2)** — not an anomaly needing explanation. At xMargin 1.7, Poisson puts the home side at ~77%, so roughly one loss in four is expected. It was a normal outcome that only looked strange against an 86% backdrop.
5. **#16 and #19 at exactly 1.000** — both reproduced on the correct side of the boundary. Given the band table is smooth, boundary sensitivity turned out not to matter.

---

## Files

| File | Contents |
|---|---|
| `gate1/replicate.py` | spec reimplemented from scratch, 2026 — exact match |
| `gate1/multiseason.py` | 15 seasons, unchanged threshold |
| `gate1/economics.py` | closing-odds ROI, edge vs de-vig, price-band calibration |
| `gate1/final.py` | high-cut bootstrap, walk-forward, market absorption |
| `gate1/wf_check.py` | walk-forward correction and volume check |
| `gate1/{SWE,NOR,FIN}.csv` | source data, 7,429 matches with closing odds |
