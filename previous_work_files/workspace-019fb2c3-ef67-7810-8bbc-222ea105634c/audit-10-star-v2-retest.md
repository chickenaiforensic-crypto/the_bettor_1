# Study 10 — Star v2 Rebuild and Re-test

**Date:** 2026-07-30 · **Status:** tested, nothing implemented, awaiting your decision
**Scripts:** `data/star_v2.py`, `retest.py`, `tier_split.py`

---

## 0. Headline

**My recommendation did not work.** I proposed rebuilding the star basis on the theory that a cleaner categorisation would produce a provable gain. The rebuild succeeded structurally and **failed to improve prediction**.

| | v1 (your spec) | v2 (rebuilt) |
|---|---|---|
| Weekly churn | 21.0% | **8.7%** ✅ |
| Draw separation | 1.68% | **2.52%** ✅ |
| **Held-out draw gain** | **+0.042%** | **+0.035%** ❌ |
| Bootstrap CI | [−0.00068, +0.00088] | [−0.00090, +0.00108] |
| Significant? | No | **No** |

The rebuild made the categorisation measurably better and the forecast slightly worse. I said C was the most likely route to a provable gain; it wasn't.

---

## 1. What was built

Your spec, unchanged:
```
metric  = (3×won + drawn) / played
qualify = played >= 5
stars   = 1..5 ranked within league
```

Plus the three Study 08 fixes:
1. **Rolling cutoffs** — recomputed at every fixture from prior matches only, removing the look-ahead contamination.
2. **Shrinkage** — a team's metric regresses toward the league mean based on games played, so a 5-game record isn't trusted as firmly as a 30-game one.
3. **Hysteresis** — a team must clear a boundary by a margin before changing star level.

Hyperparameters (shrink=6, hysteresis=0.05) chosen **on training data only**. Test set untouched until the end.

---

## 2. The fixes worked — on structure

| shrink | hysteresis | churn | draw separation |
|---|---|---|---|
| 0 | 0.00 | 21.4% | 1.41% |
| 0 | 0.10 | 6.6% | 2.52% |
| 3 | 0.05 | 9.7% | 2.42% |
| **6** | **0.05** | **8.9%** | **2.58%** |
| 6 | 0.10 | 4.7% | 2.39% |

Churn fell from 21% to 8.7% — star levels are now stable week to week instead of flipping for half the league. Draw separation rose from 1.68% to 2.52%, a **50% stronger** same-star signal.

Both of Study 08's defects are genuinely fixed.

---

## 3. And it still didn't help the forecast

Held-out test, 39,743 matches from Sept 2019:

```
v2 gain over the model : +0.0000662 Brier (+0.035%)
bootstrap 95% CI       : [-0.0008988, +0.0010787]
P(gain <= 0)           : 0.457
```

Worse than v1's +0.042%, and the interval still straddles zero. **5 of 7 seasons positive, 5 of 10 leagues positive** — no better than before.

**Why the structural fixes didn't convert:** the churn and contamination I removed weren't what was limiting the signal. The limit is overlap. The Dixon-Coles ratings already encode team quality continuously; a cleaner 5-bucket version of the same information is still the same information. Making the buckets steadier doesn't make them independent.

---

## 4. One genuine finding

Both versions showed the same pattern — lower divisions positive, top divisions negative. I tested that honestly: **selected the leagues on training data, then applied that fixed selection to the test set.**

Selection made on TRAIN: `B1, D1, D2, E0, E1, E2, E3, F2, N1, SP2, T1`

Applied to TEST (26,289 matches, never used in the choice):

```
gain             : +0.0001870 Brier (+0.098%)
bootstrap 95% CI : [-0.0007821, +0.0011788]
P(gain <= 0)     : 0.357
9 of 11 leagues held up out of sample
```

**The gain more than doubles** (+0.035% → +0.098%) and **9 of 11 leagues held their sign out of sample.** That's a meaningfully better result than the blanket application.

But the confidence interval **still includes zero**. Nine out of eleven holding up is encouraging; it is not proof. And I've been wrong twice now betting on encouraging patterns, so I'm not going to call this significant when the arithmetic says it isn't.

---

## 5. Practical size

Even taking the +0.098% at face value:

> Over 1,000 matches, the draw probability lands on average **1.37 percentage points** closer to reality.

That will not change a tier, flip a call, or alter a recommendation. It is a refinement, not a capability.

---

## 6. Where this leaves the star system

| Question | Answer |
|---|---|
| Is your specification sound? | ✅ Yes — same-star draw lift is real and monotonic |
| Did the rebuild fix the defects? | ✅ Yes — churn 21%→8.7%, separation 1.68%→2.52% |
| Does it improve draw prediction? | ⚠️ +0.035% blanket, +0.098% on selected leagues |
| Is that improvement provable? | ❌ No — CI includes zero in every configuration |
| Was my recommendation right? | ❌ No — v2 predicts slightly worse than v1 |

Three independent attempts (Study 07 merger, Study 09 v1, Study 10 v2) have now landed in the same place: **the star concept measures something real, and the model already measures it.**

---

## 7. Options — your call

**A. Ship v2 on the 11 selected leagues.** Best measured result (+0.098%, 9/11 held up). Honest label: "small improvement, not statistically proven."

**B. Ship v2 as display only.** Star ratings and the same-star draw lift shown as information; probability maths untouched. Zero risk, and the categorisation is now genuinely well-built.

**C. Keep v2 in the workspace, ship nothing.** Available if a future input makes it independent.

**D. Drop the star line and move to the home/away evaluation.**

**My read this time is B or D**, and I hold it more loosely than last time given I just got this wrong. The v2 categorisation is solid work — stable, uncontaminated, and it demonstrably separates draws. What it isn't is *additive* to a model built from the same match results.

The honest path to a star system that genuinely adds is the one Study 07 identified: build it from something Dixon-Coles cannot see. That remains the deferred Step 4.

---

## 8. Still outstanding

The contaminated Study 06 star version is **still live in the app** — it uses `att+dfn` with frozen cutoffs and misranks teams (Sunderland 1★, Nott'm Forest 4★). Whatever you decide above, that one should come out. Say the word and I'll remove it or swap it for v2 display-only.
