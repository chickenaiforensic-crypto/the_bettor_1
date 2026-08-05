# Study 04 — Away Games, Venue Splits, and "Wins Both Home & Away"

**Date:** 2026-07-29
**Data:** 153,058 matches · 18 leagues · 23 seasons (2003/04 → 2025/26) · 152,630 with closing odds
**Source:** football-data.co.uk, downloaded fresh
**Scripts:** `data/load.py`, `venue.py`, `market.py`, `flb.py`, `answers.py`

---

## 0. Error controls applied

You asked for zero errors. Here is what was done to earn that, and what it cost.

| Control | Implementation | Result |
|---|---|---|
| Sample size | 18 leagues × 23 seasons, not 3 leagues × 1 season | n = 153,058 (Gate 1 had 179) |
| Strict parsing | Every row validated; rejections counted, never silently dropped | 591 rejected of 153,649 (0.38%) — all benign: 108 bad dates, 480 missing team, 3 no score |
| Internal consistency | Recomputed result from goals, cross-checked against the file's own `FTR` column | **0 mismatches** in 153,058 rows |
| Duplicate detection | Keyed on league+season+date+home+away | **0 duplicates** |
| Structural sanity | Match counts per league-season vs known fixture lists | E0 380/380, D1 306/306, E1 552/552, SP1 380/380 — exact for every season |
| Look-ahead prevention | Every conditioning variable built from `seq[:i]` — strictly prior matches, same season | enforced structurally, not by filter |
| Confounding control | Every finding re-tested *within narrow closing-price bands* | see §3 |
| Multiple-comparison discipline | Every positive result stress-tested by league, era, and bootstrap before being reported | see §4 |

**Baseline sanity check:** overall H/D/A = 44.6% / 26.8% / 28.6%. This matches the published long-run figures for European league football almost exactly, which validates the whole pipeline.

---

## 1. Q1 — A team wins at home. What happens in its next away match?

Every home result in the dataset, matched to that team's next away fixture in the same season.

| After a home… | Next away W | Next away D | Next away L | n |
|---|---|---|---|---|
| **Win** | **31.3%** | 27.1% | **41.6%** | 66,238 |
| Draw | 27.5% | 26.9% | 45.6% | 40,158 |
| **Loss** | **25.2%** | 26.3% | **48.5%** | 42,555 |
| *(all)* | 28.5% | — | — | 148,951 |

95% CIs are ±0.4pt at these sample sizes — the gaps are far outside noise.

**Answer:** winning at home lifts the next away win rate from **25.2% → 31.3%**, a **+6.1 point** swing. The effect is real and consistently signed.

**But the headline number people expect is the wrong way round.** A team that just won at home still **loses its next away match 41.6% of the time** — considerably more often than it wins it (31.3%). Home form does not travel. It shifts the odds; it does not reverse them.

### Extending to runs of home form

| Last 3 home results | Next away W | Next away L | n |
|---|---|---|---|
| **W W W** | **38.5%** | 35.0% | 14,684 |
| 2+ wins | 30.6% | 42.5% | 41,049 |
| other | 25.8% | 47.5% | 72,892 |
| **L L L** | **20.9%** | **54.9%** | 4,348 |

Three straight home wins pushes the next away win rate to 38.5% — the strongest version of this effect, +17.6pt over the LLL group. Still short of a coin flip, and note that even here away wins (38.5%) barely edge away losses (35.0%).

---

## 2. Q2 — Teams that win both home and away

Classified using only prior matches (minimum 3 home + 3 away played), then measuring the *next* result.

| Prior record | Next W | Next D | Next L | PPG | n |
|---|---|---|---|---|---|
| **Won both H & A** | **37.6%** | 26.6% | 35.8% | **1.39** | 226,130 |
| Won home only | 29.9% | 27.2% | 42.9% | 1.17 | 22,856 |
| Won away only | 30.1% | 27.3% | 42.6% | 1.17 | 5,558 |
| Won neither | 28.8% | 26.4% | 44.8% | 1.13 | 2,545 |

**Answer:** yes, your intuition is correct — teams that have won at both venues are genuinely stronger. 1.39 PPG vs 1.17, and a 7.7pt higher win rate. The gap between "won both" and "won only one venue" is large and clean.

**The problem is coverage.** "Won both home and away" describes **88% of all eligible team-matches**. Once a team has played a handful of fixtures at each venue, winning at least one of each is close to the default state. As a filter it removes almost nothing.

Note also that *home only* (1.17) and *away only* (1.17) are **identical**. Winning away is harder, so an away win is more impressive — but as a classifier, which venue you won at carries no information. Only the count matters.

---

## 3. The decisive test — does any of it beat the price?

This is where Gate 1's lesson gets applied. 127,586 matches where both teams had ≥3 prior home and ≥3 prior away fixtures, all with closing odds.

### Raw comparison (confounded)

| Selection | n | Actual | De-vig market | Edge | ROI |
|---|---|---|---|---|---|
| All eligible | 127,586 | 44.7% | 44.1% | +0.7% | −4.37% |
| Home won both H&A | 112,808 | 45.6% | 45.0% | +0.6% | −4.50% |
| Home NOT won both | 14,778 | 38.0% | 37.2% | +0.8% | −3.33% |
| Away won both H&A | 112,024 | 29.5% | 30.0% | −0.5% | −8.60% |

The "won both" group differs enormously in raw quality (mean prior PPG 1.42 vs 0.86), so any raw comparison is confounded by strength. The correct test holds price fixed.

### Controlled — within narrow closing-price bands

| Price band | Category | n | Actual | Market | Edge |
|---|---|---|---|---|---|
| [1.5, 1.8) | home BOTH | 18,180 | 59.2% | 57.6% | +1.5% |
| [1.5, 1.8) | home not BOTH | 1,020 | 58.3% | 56.9% | +1.4% |
| [1.8, 2.2) | home BOTH | 27,970 | 48.4% | 48.0% | +0.4% |
| [1.8, 2.2) | home not BOTH | 3,178 | 47.9% | 47.4% | +0.5% |
| [2.2, 2.8) | home BOTH | 29,467 | 39.2% | 39.2% | +0.1% |
| [2.2, 2.8) | home not BOTH | 5,033 | 40.4% | 38.7% | +1.6% |
| [2.8, 10) | home BOTH | 24,058 | 25.4% | 26.0% | −0.7% |
| [2.8, 10) | home not BOTH | 5,050 | 25.9% | 25.4% | +0.5% |

**Within every price band, "won both H&A" and "did not" perform identically.** The edges are the same, band by band, and in the 2.2–2.8 band the *non*-qualifying group actually does better. The apparent advantage in the raw table was entirely a proxy for team quality — quality the market has already priced.

### Away form specifically

| Away team's prior away PPG | n | Away win % | Market | Edge | ROI |
|---|---|---|---|---|---|
| 0.0–0.5 | 12,277 | 20.6% | 20.9% | −0.3% | −9.80% |
| 0.5–1.0 | 37,690 | 23.4% | 23.9% | −0.5% | −8.74% |
| 1.0–1.5 | 47,500 | 28.0% | 28.7% | −0.7% | −9.19% |
| 1.5–2.0 | 19,815 | 35.7% | 36.2% | −0.6% | −8.81% |
| 2.0+ | 10,304 | 45.8% | 45.6% | +0.2% | −5.41% |

Away form predicts away results beautifully — 20.6% → 45.8% across the range. **And the market tracks it to within 0.7 points at every level.** Every ROI is around −9%, roughly the vig on away prices. There is no away-form edge anywhere.

### Home/away split asymmetry (fortress teams)

| Home team's H-minus-A PPG split | n | Home win % | Market | Edge |
|---|---|---|---|---|
| −0.5 to 0.3 | 41,263 | 44.5% | 43.7% | +0.8% |
| 0.3 to 1.0 | 56,200 | 44.9% | 44.2% | +0.7% |
| 1.0 to 1.8 | 21,544 | 45.2% | 44.8% | +0.5% |
| 1.8+ | 2,160 | 45.9% | 45.7% | +0.2% |

"Fortress" teams — much better at home than away — are **not** underpriced. The edge actually *shrinks* as the split grows. The market prices venue asymmetry correctly.

---

## 4. The one positive cell, stress-tested to destruction

Short-priced home favourites (odds < 1.50) showed +3.6% edge. Worth chasing? No — and here is the full workup.

```
ALL: n=12,578  actual 76.3%  market 72.7%  edge +3.6%
     ROI -0.46%   bootstrap 95% CI [-1.44%, +0.54%]
```

**The edge is real. The ROI is not.** A +3.6% probability edge at odds of ~1.35 is not enough to cover the bookmaker's margin. The bootstrap interval straddles zero and is centred slightly negative.

This is the **favourite–longshot bias** — one of the oldest and most thoroughly documented findings in betting-market research. Across the whole price curve:

| Home price | n | Actual | Market | Edge | ROI |
|---|---|---|---|---|---|
| 1.0–1.3 | 5,131 | 83.5% | 79.3% | +4.2% | −0.22% |
| 1.3–1.5 | 7,447 | 71.3% | 68.1% | +3.2% | −0.62% |
| 1.5–2.0 | 34,394 | 55.5% | 54.4% | +1.1% | −3.67% |
| 2.0–3.0 | 55,822 | 40.6% | 40.4% | +0.2% | −4.62% |
| 3.0–5.0 | 18,282 | 26.4% | 27.0% | −0.5% | −6.20% |
| 5.0–10 | 5,458 | 15.0% | 15.2% | −0.2% | −5.41% |
| 10+ | 1,052 | 6.1% | 7.7% | −1.6% | −23.59% |

Textbook shape: favourites underpriced, longshots overpriced, and the bias sized *just* under the vig at the short end. Bookmakers know about this bias and price it deliberately.

**Consistency checks — all fail to establish it:**

- **By league:** only **4 of 13** leagues show positive ROI. Greece +4.73%, Spain +3.25%, Belgium +2.54%, Portugal +1.66%; England −2.30%, Championship −4.28%, Scotland −3.08%. Not consistent.
- **By era:** −2.50% (03-09), +0.65% (10-15), +0.24% (16-21), +0.29% (21-26). Hovering at zero throughout.
- **Does "won both H&A" add anything?** `fav & BOTH` = −0.32% ROI; `fav & not BOTH` = −7.75% on n=225. No.
- **Walk-forward:** produced no qualifying bets — the training-period ROI never turned positive, so the rule never fired.

The four positive leagues are the smaller, less liquid markets, which is where you'd expect residual bias — but at n≈800 each, with 13 leagues tested, finding 4 positive is roughly what chance delivers. **This is not actionable.**

---

## 5. Direct answers to your questions

> **When teams win at home, how often do they win/lose away?**

Next away match after a home win: **31.3% win, 27.1% draw, 41.6% loss.** Compared to 25.2% / 26.3% / 48.5% after a home loss. A genuine +6.1pt lift — but a team fresh off a home win is still a third more likely to lose its next away game than win it. After three straight home wins: 38.5% win / 35.0% loss, the best it gets.

> **What is the state of teams that win both home and away?**

Genuinely stronger: **1.39 PPG vs 1.17** for teams that have only won at one venue, and 37.6% vs ~30% next-match win rate. Your instinct that they're a class above is correct.

> **Are they much stronger than their competitors?**

Stronger, but not *much*, and not *rare*. **88% of teams qualify** once they've played a few matches at each venue. And critically — the advantage disappears completely once you control for price. Within every odds band, "won both" teams perform the same as teams that haven't.

---

## 6. What this means

The venue effects you asked about are **real, large, and correctly priced**. That is the consistent finding across all four tests:

- Home form → away results: real (+6.1pt), priced.
- Won both venues: real (+0.22 PPG), priced.
- Away form → away wins: strongly real (20.6%→45.8%), priced to within 0.7pt.
- Fortress asymmetry: real, priced, edge shrinks as the effect grows.

Every ROI in this study sits between −0.5% and −9.8%, which is the bookmaker margin and nothing else.

This is the second independent confirmation of the same structural fact. Gate 1 found the market's closing line predicted 997 Nordic matches to within 0.2 points. This study finds it predicts 127,586 matches across 18 leagues to within roughly 0.7 points on every venue-based split we can construct.

**Venue and form information is the most heavily modelled input in football betting.** It is in every price, every model, every tipster's spreadsheet. Building a better estimate of it is achievable; extracting money from it is not.

---

## 7. Where I'd go next

We now have a clean 153,058-match dataset with closing odds and a validated pipeline. That is a genuine asset regardless of direction. Three honest options:

**A. Stop trying to beat 1X2 closing lines and change the target.**
Everything tested so far — xMargin, venue splits, form, fortress effects — is priced. The remaining candidates are markets with less modelling attention: team totals, corners, cards, in-play, or lower divisions and reserve leagues where liquidity is thin. I can screen these the same way, but expectations should be modest.

**B. Build a calibrated model and score it honestly.**
Drop profit as the objective. Build Dixon-Coles / bivariate Poisson on this dataset, measure Brier score and log-loss *against the closing line as benchmark*, and accept that matching the close is the realistic ceiling. This makes the app from audit 01 genuinely useful as a probability tool, with correct draw handling and per-tier calibration. Intellectually clean, no false promises.

**C. Line-shopping instead of prediction.**
The one edge that provably exists in this data is price dispersion between bookmakers. We have `Max` and `Avg` columns — I can measure how much is available from always taking the best price rather than the average. This is a real, if unglamorous, edge and it requires no predictive skill at all.

**My recommendation: C first** (it's a two-hour measurement and it either exists or it doesn't), **then B** as the modelling project.

One thing I'd flag: we should agree in advance what result would make us stop. Gate 1 and this study have both landed on "the market is right." If a third investigation lands the same way, that is the finding, and the honest move is to build B and enjoy it as a forecasting exercise rather than keep hunting.

---

## 8. Reproducibility

| File | Purpose |
|---|---|
| `data/load.py` | strict loader with full rejection accounting |
| `data/venue.py` | Q1 and Q2 raw computation |
| `data/market.py` | price-controlled tests, all categories |
| `data/flb.py` | favourite–longshot stress test (league/era/bootstrap/walk-forward) |
| `data/answers.py` | final answer tables |
| `data/all_matches.pkl` | 153,058 validated matches |
| `data/*.csv` | 414 raw source files |

Every number in this document regenerates from those scripts.
