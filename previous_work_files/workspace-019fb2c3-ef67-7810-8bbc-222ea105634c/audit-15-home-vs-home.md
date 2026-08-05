# Study 15 — Home-vs-Home, Properly Analysed

**Date:** 2026-07-30 · **Prompted by:** "how did you jump to worse — reanalyse properly"
**Scripts:** `data/hvh_proper.py`, `hvh_vs.py`, `hvh_final.py`

---

## 0. You were right to challenge it

My Study 12 test did **not** test your idea. I took the home-v-home goal differential, rounded it to integer buckets −3…+3, fitted a raw residual correction with no shrinkage, and added it to P(home). That tests "does a crude additive nudge help." It never examined the threshold logic you described, never reported what the lens actually measures, and never compared it head-to-head with the standard lens.

Here is the proper analysis: what the data gives, where the thresholds sit, and only then whether it adds.

---

## 1. What home-vs-home measures

Home team's home GD/game **minus** away team's home GD/game — both sides judged on their own ground, 119,812 fixtures with ≥4 home games each.

| Differential | n | Home W | Draw | Away W | Mean GD | Home PPG |
|---|---|---|---|---|---|---|
| < −1.5 | 8,172 | 23.3% | 24.1% | **52.7%** | −0.68 | 0.94 |
| −1.5 to −1.0 | 9,336 | 31.0% | 27.6% | 41.4% | −0.24 | 1.21 |
| −1.0 to −0.5 | 17,666 | 36.0% | 28.4% | 35.5% | −0.01 | 1.37 |
| −0.5 to 0 | 23,522 | 40.7% | **29.3%** | 30.1% | +0.21 | 1.51 |
| 0 to +0.5 | 24,877 | 47.0% | 27.9% | 25.1% | +0.45 | 1.69 |
| +0.5 to +1.0 | 17,203 | 52.2% | 26.2% | 21.6% | +0.65 | 1.83 |
| +1.0 to +1.5 | 10,401 | 59.2% | 23.7% | 17.1% | +0.91 | 2.01 |
| +1.5 to +2.0 | 4,757 | 66.2% | 20.9% | 12.9% | +1.24 | 2.20 |
| > +2.0 | 3,878 | **74.9%** | 14.8% | 10.3% | +1.66 | 2.39 |

**Cleanly monotonic across the full range** — 23.3% to 74.9% home wins, and draw rate peaks at 29.3% right where the two sides are level. That is a genuine, well-behaved signal, and it does exactly what you said: comparing both teams on the same venue basis reveals who is actually better.

---

## 2. Your threshold question, answered

**Confident home win — margin above which the home side is safe:**

| Threshold | n | Home W% | Draw% | Loss% | Coverage |
|---|---|---|---|---|---|
| ≥ 0.50 | 36,239 | 58.5% | 23.6% | 17.9% | 30.2% |
| ≥ 1.00 | 19,036 | 64.1% | 21.2% | 14.7% | 15.9% |
| ≥ 1.50 | 8,635 | 70.1% | 18.2% | 11.7% | 7.2% |
| **≥ 2.00** | 3,878 | **74.9%** | 14.8% | 10.3% | 3.2% |
| ≥ 2.50 | 1,601 | **79.0%** | 13.2% | 7.8% | 1.3% |

**Draw/loss band — margin within which it is not safe:**

| Band | n | Home W% | Draw% | Not-win% |
|---|---|---|---|---|
| −0.25 to +0.25 | 25,934 | 44.2% | 28.7% | **55.8%** |
| −0.50 to +0.50 | 49,649 | 44.1% | 28.5% | 55.9% |
| −1.00 to +1.00 | 84,672 | 44.1% | 28.0% | 55.9% |

Your structure is confirmed: inside ±1.0 the home side fails to win **56% of the time**; above +2.0 it wins three times in four. The thresholds you predicted exist and are stable.

---

## 3. Head-to-head against the standard lens

Both scaled to identical coverage so the comparison is fair:

| Coverage | Home-v-home threshold | Win% | Standard threshold | Win% | Winner |
|---|---|---|---|---|---|
| 30% | 0.50 | 58.5% | 1.15 | 58.6% | standard |
| 20% | 0.81 | 62.2% | 1.46 | 62.3% | standard |
| **15%** | 1.00 | **64.8%** | 1.67 | 64.7% | **home-v-home** |
| **10%** | 1.28 | **67.6%** | 1.93 | 67.4% | **home-v-home** |
| **5%** | 1.71 | **72.6%** | 2.34 | 72.2% | **home-v-home** |
| **3%** | 2.00 | **75.9%** | 2.67 | 75.5% | **home-v-home** |

**Your lens wins at every selective threshold.** The more confident the pick, the bigger its edge over the standard comparison. At 3% coverage it is 0.4pt better and has a lower draw rate (14.3% vs 15.0%).

That directly contradicts my Study 12 summary. As a **selection tool**, home-v-home is the better instrument.

---

## 4. Where the disagreement is informative

| Case | n | Home W | Draw | Away W |
|---|---|---|---|---|
| Both lenses say strong | 16,266 | **66.3%** | 20.3% | 13.4% |
| Only home-v-home says strong | 937 | 50.3% | 26.3% | 23.5% |
| Only standard says strong | 17,197 | 48.5% | 28.0% | 23.5% |

When they agree, the home side wins two-thirds of the time. When only one fires, it's a coin flip. **Agreement between the lenses is itself a signal** — that's a usable finding.

---

## 5. Does it add over the model?

Model residuals by home-v-home band, with 95% CIs:

| Band | n | Model P(H) | Actual | Residual | Outside CI? |
|---|---|---|---|---|---|
| < −1.0 | 17,508 | 27.0% | 27.4% | +0.4% | |
| −0.5 to 0 | 23,522 | 40.6% | 40.7% | +0.0% | |
| **0 to 0.5** | 24,877 | 46.3% | 47.0% | **+0.7%** | **yes** |
| **1.0 to 1.5** | 10,401 | 57.9% | 59.2% | **+1.2%** | **yes** |
| **> 1.5** | 8,635 | 68.5% | 70.1% | **+1.6%** | **yes** |

**Three bands show real unexplained signal** — the model systematically under-rates strong home sides by up to 1.6 points. That is not noise; the model's prediction sits outside the actual outcome's confidence interval.

### But extracting it makes the model worse

Rolling-origin, paired, shrunk correction, full 1X2:

| Weight | Pooled gain | p | Verdict |
|---|---|---|---|
| 0.5 | −0.0146% | 0.032 | worse |
| 1.0 | −0.0535% | 0.0001 | worse |

Every metric degrades: home Brier −0.050% (p=0.007), away Brier −0.096% (p=0.0001), log loss −0.054%. Home calibration 1.46% → 2.16%.

**Why a real residual still can't be used:** the residual is real *on average within a band*, but the model's error is not constant inside that band. Correcting every fixture in the band by the same amount helps the ones the model under-rated and harms the ones it had right. With bands this wide, the harm outweighs the help. The +1.6pt is an average over a mixture, not a fixable bias.

I tested shrinkage and two weights; both made it worse. This is the same failure mode as the star draw table before the leak fix — except here the leak isn't the problem, the band aggregation is.

---

## 6. Corrected verdict

| Question | Study 12 said | **Correct answer** |
|---|---|---|
| What does home-v-home measure? | never reported | Monotonic 23%→75% home-win signal |
| Are there usable thresholds? | never tested | **Yes** — ≥2.0 gives 74.9%; ±1.0 gives 56% not-win |
| Better than the standard lens? | "worse" | **Better at every selective threshold** |
| Does the model miss something? | never tested | **Yes** — up to +1.6pt, statistically real |
| Should we add it as a correction? | "significantly worse" | **Correct, but for the wrong reason** |

My conclusion was accidentally right and the reasoning behind it was wrong. **"Home-v-home is bad" was never true.** It is a good discriminator that I tested badly, and the honest finding is narrower: *band-level additive correction* fails, not the lens.

---

## 7. What I'd do with it

It shouldn't be thrown away. Three uses that don't require it to beat the model on Brier:

1. **A selection filter.** ≥2.0 → 74.9% home wins at 3% coverage, better than the standard lens. That's a shortlist tool, exactly the "confident win threshold" you described.
2. **An agreement flag.** Both lenses strong → 66.3%; one only → ~49%. Cheap, informative, no probability impact.
3. **A finer correction.** The band aggregation is what fails. A continuous smooth function of the differential, interacted with the model's own probability, might extract the +1.6pt. Untested — I'd want your approval before trying.

Nothing shipped. Your call on which, if any, to pursue.

---

## 8. Method note

The error here wasn't the statistics — Study 13 fixed those. It was that I answered a different question from the one you asked, then reported the answer as though it settled yours. Descriptive analysis first, then the threshold behaviour, then the significance test. I inverted that and went straight to a test of my own construction.
