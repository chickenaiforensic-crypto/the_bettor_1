# Study 06 — Star Ratings & Pitch Familiarity

**Date:** 2026-07-30 · **Data:** 132,915 rated fixtures (prior-only, strictly causal)
**Scripts:** `data/stars.py`, `fam_test.py`, `correction.py`, `starview.py`

---

## Summary

| Proposal | As a model input | As a display |
|---|---|---|
| Star matrix (5v5 → equal goals) | ❌ **rejected** — tested, made the model worse | ✅ **shipped** |
| Pitch familiarity 1–5 | ❌ **rejected** — already absorbed, unstable | ✅ inside ratings |

Both ideas point at something real. Neither survives as a scoring term. **One of them ships as a display layer, because the underlying instinct — showing an expected scoreline — was correct.**

---

## 1. The star hypothesis

Your claim: *5★ v 5★ → equal goals (0-0, 1-1, 2-2); 4★ v 5★ → 0-1.* Margin is a function of star difference.

I built stars 1–5 as in-league PPG quintiles, strictly from prior matches, then measured.

### Test 1 — do equal stars give equal goals?

| Matchup | n | Home goals | Away goals | Margin |
|---|---|---|---|---|
| 1★ v 1★ | 6,448 | 1.42 | 1.11 | **+0.30** |
| 2★ v 2★ | 4,482 | 1.42 | 1.09 | **+0.33** |
| 3★ v 3★ | 4,564 | 1.45 | 1.11 | **+0.33** |
| 4★ v 4★ | 4,766 | 1.52 | 1.13 | **+0.39** |
| 5★ v 5★ | 3,308 | 1.49 | 1.13 | **+0.36** |

**No.** The home side scores more in every equal-star cell. Equal teams do not produce equal goals, because playing at home is worth roughly **+0.34 goals** — and that never cancels out. This is the same finding as the audit-01 fix: home advantage is a first-class term, not something that washes away between equals.

Also note the draw rates: 27–29%, not the near-certainty the 0-0/1-1/2-2 framing implies. Exact 1-1 happens 13% of the time; exact 0-0 about 8%.

### Test 2 — is margin a function of star gap alone?

| Star gap | Cells | n | Mean margin | Range across cells |
|---|---|---|---|---|
| −3 | 2 | 11,053 | −0.29 | −0.46 (2v5) to −0.17 (1v4) |
| −1 | 4 | 22,602 | +0.10 | −0.13 (4v5) to +0.24 (2v3) |
| 0 | 5 | 23,568 | +0.34 | +0.30 (1v1) to +0.39 (4v4) |
| +1 | 4 | 21,870 | +0.58 | +0.43 (3v2) to **+0.82 (5v4)** |
| +2 | 3 | 16,311 | +0.79 | +0.62 (3v1) to **+1.09 (5v3)** |
| +3 | 2 | 10,289 | +1.05 | +0.95 (4v1) to +1.19 (5v2) |

**No.** A +1 gap means +0.43 goals at 3v2 but **+0.82 at 5v4** — nearly double. A 5★ v 4★ is not the same match as a 3★ v 2★. Strong teams beat their nearest rivals by more than weak teams beat theirs, because the gap between quintiles isn't linear in ability.

The full 5×5 matrix shows it cleanly — 5★ at home scores 2.16 v 1★ but 1.49 v 5★, while 1★ at home manages 1.42 v 1★ and 1.01 v 5★.

### Test 3 — does a single scoreline per cell work?

Predicting the rounded mean scoreline for each of the 25 cells: **11.8% accurate**. The full Dixon-Coles model's top scoreline hits **13.1%**. A fixed integer per cell is strictly worse, because it discards the distribution — and the distribution is where the information is.

---

## 2. Pitch familiarity as a 1–5 metric

Banded by the away team's prior visits to that ground: 1 = first visit, 5 = 11+ visits.

### Raw — looks promising

| Familiarity | Visits | n | Away win | Draw |
|---|---|---|---|---|
| 1 | 0 | 28,692 | 27.4% | 27.7% |
| 3 | 3–5 | 37,304 | 28.8% | 27.1% |
| 5 | 11+ | 17,108 | **31.3%** | 24.4% |

### Controlled — falls apart

Within narrow team-strength bands:

| Strength gap | Fam 1 | Fam 5 | Effect |
|---|---|---|---|
| −3..−1 (away much better) | 52.0% | 60.7% | +8.7pt |
| −1..−0.3 | 36.0% | 42.0% | +6.0pt |
| −0.3..0.3 (even) | 26.0% | 29.5% | +3.5pt |
| 0.3..1 | 18.7% | 19.0% | +0.3pt |
| **1..3 (away much worse)** | 10.1% | **7.7%** | **−2.4pt** |

The effect shrinks as the away side gets weaker and **reverses sign** in the last band. A genuine familiarity effect would be roughly constant. This is residual team quality that PPG banding didn't fully remove — strong clubs are also the ones who've visited a ground 11+ times.

### Is it already in the model?

| Familiarity | n | Model P(away) | Actual | Residual |
|---|---|---|---|---|
| 1 | 25,994 | 28.9% | 27.4% | −1.6% |
| 3 | 37,304 | 29.2% | 28.8% | −0.4% |
| 5 | 17,108 | 30.6% | 31.3% | **+0.8%** |

Residuals under 2 points. The Dixon-Coles model already absorbs this through team ratings and per-team home advantage. **Your point that "more visits ≈ more matches played" is exactly right** — and that's precisely why it's redundant: the model already knows how good the team is.

---

## 3. The decisive test

The residuals weren't perfectly flat, so I gave both ideas a fair shot: fit a correction on 70% of the data (105,252 matches), measure on the held-out 30% (45,108 matches, from Sept 2019).

| Correction | Test Brier | Change |
|---|---|---|
| **Baseline (no correction)** | **0.60877** | — |
| + star-gap correction | 0.60904 | **−0.044%** |
| + familiarity correction | 0.60916 | **−0.064%** |
| + both | 0.60963 | **−0.141%** |

**Every correction made the model worse.** And the reason is visible:

| Star gap | TRAIN residual | TEST residual | Same sign? |
|---|---|---|---|
| −4 | +0.0129 | −0.0047 | **NO** |
| −2 | +0.0158 | −0.0080 | **NO** |
| 0 | +0.0079 | −0.0138 | **NO** |
| +2 | +0.0104 | −0.0076 | **NO** |
| +3 | +0.0185 | −0.0005 | **NO** |

**2 of 9 bands keep their sign out of sample.** The residuals were noise. Fitting them is exactly the mistake that produced the 86% xMargin claim — a pattern that looked real in-sample and evaporated out of it.

---

## 4. What shipped

Stars fail as an input but are **excellent as a display**, so I derived them *from* the model's own ratings (attack + defence, quintiled per league) and put them on screen.

Verified against 13,066 recent fixtures:

| Matchup | n | Model xG | Actual goals | Home win |
|---|---|---|---|---|
| 5★ v 5★ | 471 | 1.62–1.26 | 1.62–1.34 | 42.9% |
| 5★ v 4★ | 583 | 1.91–1.04 | **1.91–1.03** | 58.3% |
| 5★ v 3★ | 528 | 1.96–0.94 | 1.96–0.80 | 66.7% |
| 4★ v 5★ | 584 | 1.31–1.48 | 1.33–1.41 | 33.2% |
| 4★ v 4★ | 514 | 1.51–1.18 | 1.54–1.21 | 43.0% |
| 3★ v 3★ | 439 | 1.44–1.13 | 1.52–1.09 | 47.6% |

Model xG matches reality to within ~0.1 goals in every cell.

**Three additions to the app:**
1. **Star ratings** (★★★★☆) beside each team, per-league quintiles.
2. **Likeliest scoreline** with its true probability — "2–1 (11.4% of the time)". This is your expected-scoreline idea, made honest by attaching the frequency rather than implying certainty.
3. Stars in the saved log.

**Guarded by tests:** `lambdas()` contains no star term, `rateFixture` doesn't adjust probability by stars, and all 9,506 fixtures still sum to 1. Stars read the model; they never write to it.

Star distribution across 414 teams: 81 / 85 / 82 / 83 / 83 — clean quintiles.

---

## 5. On closing loopholes

You said a well-built goal evaluation "will start to close loopholes." The instinct is right, and the model already does this — but via a distribution rather than a point estimate.

For Liverpool v Southampton the model doesn't say "2–1." It says 2–1 is the single likeliest at ~11%, and simultaneously gives P(over 2.5) = 61%, P(home −1) and the full 1X2. That's strictly more information than a fixed scoreline, and it's why correct-score sits at 13% while the 1X2 output is calibrated to 1.7pt.

The loophole that matters isn't in the goal model. Studies 03 and 04 found the market already prices goal-based strength to within 0.2–0.7pt across 128,000 matches. **Refining the goal estimate further improves the forecast, not the edge.**

---

## 6. Test status

| Suite | Tests | Result |
|---|---|---|
| Core app | 28 | ✅ |
| Update engine | 23 | ✅ |
| Sync protocol | 35 | ✅ |
| **Stars & scoreline** | **20** | ✅ |
| **Total** | **106** | **all passing** |
