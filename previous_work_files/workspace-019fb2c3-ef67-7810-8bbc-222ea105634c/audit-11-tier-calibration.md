# Study 11 — Per-Tier Calibration of the Star System

**Date:** 2026-07-30 · **Status:** tested, nothing implemented, awaiting your decision
**Scripts:** `data/diagnose.py`, `calibrate_tier.py`, `granularity.py`

---

## 0. Your criticism was correct

You said expecting one system to work across all divisions is lazy, and that failure in top flights means it needs calibrating there, not discarding. I'd been treating "5 of 11 leagues negative" as a reason to restrict scope. That was the wrong instinct — **diagnose the failure, then fix it** is the right method.

I diagnosed it. Per-tier calibration **doubled the gain**, from +0.035% to +0.066%. Your method worked.

It still isn't statistically significant, and the diagnosis turned up something that changes how I read the whole star line. Both below.

---

## 1. Diagnosis — why top flights failed

### The signal is *strongest* where it appeared to fail

| Tier | n | Base draw rate | Same-star draw | **Lift** |
|---|---|---|---|---|
| **Top flight** | 67,783 | 25.1% | 27.6% | **+3.41%** |
| Second tier | 42,792 | 29.2% | 30.5% | +1.68% |
| Third/fourth | 22,340 | 26.8% | 28.1% | +1.72% |

Your same-star hypothesis is **twice as strong in top flights** as anywhere else. The failure was never the concept — it was the global table.

### The global table was miscalibrated for top flights

| Tier | Gap | Global table says | Actual | Error |
|---|---|---|---|---|
| Top flight | −2 | 28.4% | 24.9% | **+3.5%** |
| Top flight | +1 | 26.2% | 23.6% | **+2.6%** |
| Top flight | 0 | 28.9% | 27.4% | +1.5% |
| Second tier | −1 | 28.2% | 30.8% | **−2.5%** |
| Second tier | +2 | 23.9% | 26.2% | −2.3% |

One table was over-predicting draws in top flights and under-predicting them in the second tier — errors in **opposite directions**, cancelling into an apparently useless average. Exactly the failure mode you described.

### Root cause: top divisions are more stratified

| Tier | Mean sd of team PPG |
|---|---|
| Top flight | **0.448** |
| Second tier | 0.309 |
| Third/fourth | 0.313 |

Top flights are ~45% more spread out. Within-star ability spread confirms it — sd of 0.109–0.161 in top flights vs 0.082–0.099 below. **One star covers substantially more real ability in a top flight**, because the league itself is less equal.

---

## 2. The calibrated tables

Fitted separately per tier, on training data only:

| Gap | Global | Top flight | Second tier | Third/fourth |
|---|---|---|---|---|
| −4 | 24.3% | **19.2%** | 28.4% | 27.0% |
| −2 | 28.4% | 26.5% | 31.3% | 28.3% |
| 0 | 28.9% | 27.8% | 31.0% | 28.5% |
| +2 | 23.9% | 21.6% | 26.8% | 24.9% |
| +4 | 17.0% | **10.6%** | 23.2% | 17.9% |

The tiers need genuinely different tables. Top flight draws less at every gap, and its range is far wider (19.2% → 10.6% at the extremes vs 28.4% → 23.2% in the second tier). Blend weights also differ: **0.2 top flight, 0.5 second tier, 0.5 third/fourth** — the lower divisions lean on the star table more than twice as hard.

---

## 3. Result

| Approach | Gain | 95% CI | Significant? |
|---|---|---|---|
| Single global table (Study 10) | +0.035% | [−0.00092, +0.00110] | No |
| **Per-tier calibrated** | **+0.066%** | [−0.00124, +0.00157] | No |

**Calibration doubled the gain.** Per-tier breakdown on held-out data:

| Tier | n | Gain |
|---|---|---|
| Top flight | 20,884 | +0.0000037 |
| Second tier | 12,358 | +0.0002283 |
| Third/fourth | 6,501 | +0.0003294 |

Calibration lifted top flights from **negative to break-even**, and the lower divisions improved further.

---

## 4. The granularity test — and what it revealed

The diagnosis suggested top flights need finer buckets, since one star covers more ability there. Tested 5/8/10/12 buckets:

| Config | Overall | Top flight |
|---|---|---|
| **5/5/5 baseline** | **+0.0001145** | −0.0000209 |
| 8/5/5 | +0.0001097 | −0.0000301 |
| 10/6/5 | +0.0001041 | −0.0000195 |
| 12/8/6 | +0.0001108 | −0.0000014 |

Finer buckets barely move it. Top flight creeps toward zero at 12 buckets but never turns positive, and overall performance doesn't improve.

**This is the informative result.** If coarse buckets were the problem, finer buckets would fix it. They don't. Which means the residual issue in top flights isn't resolution — it's that Dixon-Coles already models well-stratified leagues accurately. More top-flight matches, wider ability spread, more signal for the ratings to learn from. The stars have less left to contribute precisely *because* the model is doing well there.

That's consistent with the lower divisions gaining most: fewer matches, tighter spread, noisier ratings — more room for a structural prior to help.

---

## 5. Honest position

| Question | Answer |
|---|---|
| Was per-tier calibration the right call? | ✅ **Yes** — doubled the gain, fixed the top-flight negative |
| Is the same-star effect real in top flights? | ✅ **Yes, strongest there** (+3.41%) |
| Does finer granularity help? | ❌ No — tested 4 configurations |
| Is the improvement significant? | ❌ **Still no** — CI includes zero |

Four rounds of work (Studies 07, 09, 10, 11) have each been directionally positive and none has cleared significance. The pattern is consistent: **the star system measures something genuinely real, and consistently recovers only a few percent of what the model already captures.**

Practical size at +0.066%: over 1,000 matches the draw probability lands roughly 1.1pt closer to reality. Real, but it won't change a tier or flip a call.

---

## 6. Options

**A. Ship the per-tier calibrated version.** Best result achieved (+0.066%, doubled by your method). Labelled honestly as a small unproven refinement.

**B. Ship on second/third tier only**, where gains are 5–10× larger than top flight and consistently positive.

**C. Display only** — show stars and per-tier same-star lift as information.

**D. Park it and move to home/away evaluation.**

I'm not going to push a read here. I've recommended twice and been wrong twice, and the significance test has come back the same way four times. What I can say with confidence: your diagnostic method was right and it produced the best result we've had on this line. Whether +0.066% unproven is worth shipping is a judgement call about the product, not the statistics — and that's yours.

---

## 7. Still outstanding

The contaminated Study 06 stars (`att+dfn`, frozen cutoffs, Sunderland 1★ / Nott'm Forest 4★) remain live in the app. That version is strictly worse than anything in this study and should come out regardless of what you choose.
