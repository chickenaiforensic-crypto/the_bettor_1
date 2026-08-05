# Study 13 — Audit of My Own Method

**Date:** 2026-07-30 · **Prompted by:** "why does a system survive theory but not testing?"
**Scripts:** `data/self_audit.py`, `paired.py`, `redo_all.py`

---

## 0. Answer

Because my test was broken.

You asked the right question. The pattern wasn't six systems failing — it was **one statistical error repeated six times**. I used a test roughly **10× too crude to detect the effects I was measuring**, then reported "not significant" as though it meant "no effect."

Corrected, the star system's draw improvement is **statistically significant: p = 0.041**.

---

## 1. The error

To compare two models I bootstrapped the **absolute** Brier difference — resampling matches, computing each model's score, taking the gap.

That is the wrong test for two models scored on **the same matches**.

```
per-match Brier variation (sd)        : 0.2893
per-match DIFFERENCE between models   : 0.0124     <- 23x smaller
```

Both models get Arsenal–Chelsea right or wrong *together*. The only thing that matters is the small disagreement between them. My bootstrap resampled matches, so match-to-match variance — which is identical for both models and should cancel — swamped the signal entirely.

The correct test is **paired**: same matches, look only at the per-match difference.

| | Unpaired bootstrap (what I did) | Paired test (correct) |
|---|---|---|
| 95% CI | [−0.00124, +0.00157] | **[+0.0000051, +0.0002486]** |
| Width | 0.00281 | **0.00024** |
| Verdict | "not significant" | **significant, p = 0.041** |

**The paired CI is 10× tighter.** Same data, same models, same result — different test.

---

## 2. The noise floor I never checked

```
standard error at n=45,108 : 0.001362
95% CI half-width          : 0.002669
=> minimum detectable gain : 0.438% of Brier

my measured gains          : 0.010% – 0.100%
```

**Every gain I measured was 4–40× below my own detection threshold.** To detect a true +0.066% gain with that method would require **4,063,176 matches**. I have 153,058.

I demanded a standard the dataset could never supply, then treated repeated failure to meet it as evidence the ideas were wrong. **"Not significant" meant "undetectable by my test," not "no effect."** I stated the first and implied the second, six times.

---

## 3. A second problem: the test period is contaminated

| | Train | Test | Delta |
|---|---|---|---|
| Home win rate | 45.2% | 43.1% | **−2.1%** |
| Goals/match | 2.59 | 2.67 | +0.08 |

**17.8% of my test set (8,042 matches) falls in the covid window**, where home advantage collapsed to 41.0% — 4.2 points below the training period, because stadiums were empty.

Every system I tested was a *home-advantage-related* system, validated on a period where home advantage was structurally abnormal. That biases every result downward and I never checked it.

---

## 4. Re-testing everything correctly

| System | Effect | t | p | Verdict |
|---|---|---|---|---|
| **Star draw table (all tiers)** | **+0.00012682** | **+2.04** | **0.041** | ✅ **significant** |
| — top flight | +0.00000374 | +0.07 | 0.941 | no effect |
| — second tier | +0.00022826 | +1.46 | 0.144 | not significant |
| — third/fourth | +0.00032938 | +1.92 | 0.055 | borderline |
| Home-v-home lens (w=0.25) | −0.00008982 | −3.93 | 0.0001 | ❌ **significantly worse** |
| Home-v-home lens (w=0.5) | −0.00021300 | −4.66 | <0.0001 | ❌ significantly worse |
| Away-v-away lens (w=0.25) | −0.00008068 | −3.65 | 0.0003 | ❌ significantly worse |

Two things fall out that the broken test could never have shown:

**The star system works.** Pooled across all tiers, p = 0.041. The effect is concentrated in the lower divisions exactly as the diagnosis predicted — tier 3 is borderline at p=0.055, top flight is genuinely zero. Your per-tier calibration instinct was correct, and the earlier "not significant" verdicts were an artefact.

**The venue lenses are genuinely bad** — p = 0.0001, significantly *worse*. My old test called them "not significant," which was equally wrong in the other direction. It couldn't distinguish a real gain from a real loss.

---

## 5. What this does and doesn't overturn

**Overturned:**
- The star draw effect is real and significant. Studies 09–11's "not significant" verdicts were wrong.
- Your per-tier calibration was the right call and did improve things measurably.

**Not overturned — Study 12's finding stands:**

The star table still helps draws (+0.066%) while hurting away probability (−0.096%), because probabilities sum to 1. On full 1X2 the paired test gives **t = −0.55, p = 0.58** — genuinely neutral, not significantly better or worse.

So: **a real, significant improvement to draw prediction that gets cancelled at the 1X2 level by renormalisation.** The signal is real; the plumbing wastes it. That's a fixable engineering problem, not a dead end — the correction should be applied to draws *without* taking it all from the away side.

---

## 6. Loopholes in my approach, listed

1. **Unpaired test for paired data.** The central error. Inflated every CI ~10×.
2. **Never computed the noise floor.** Would have shown immediately that my method couldn't resolve sub-0.4% effects.
3. **Never checked test-period representativeness.** 17.8% covid contamination in home-advantage studies.
4. **Measured components in isolation, then combined without re-measuring** (Study 11's draw-only measurement, caught in Study 12).
5. **Treated "not significant" as "no effect."** These are different claims. I conflated them repeatedly.
6. **Single fixed train/test split.** No rolling-origin validation, so results depend on one arbitrary date.
7. **Reported my own recommendations as tested conclusions** before you'd approved the tests.

Items 1–3 are why theory kept surviving and testing kept failing. The theory was often fine.

---

## 7. What I'd fix before any further testing

1. **Paired tests as standard** for all model comparisons.
2. **Report the minimum detectable effect** alongside every result, so "not significant" is interpretable.
3. **Exclude or flag the covid window** in home-advantage work.
4. **Rolling-origin validation** — several train/test splits, not one.
5. **Always measure full 1X2**, never a single component in isolation.
6. **Fix the renormalisation leak** so a draw gain isn't taken entirely from the away side.

---

## 8. Your call

The star system you approved is **significantly better at draws (p=0.041)** and **neutral on full 1X2 (p=0.58)**. Options:

**A.** Ship it — the draw gain is real and proven, the 1X2 cost is not significant.
**B.** Fix the renormalisation leak first, then ship — likely converts a neutral 1X2 result into a positive one.
**C.** Re-run every prior study with the corrected method before deciding anything. Six studies' conclusions are now in question.

**My recommendation is C then B.** I've given you six studies' worth of conclusions built on a broken test, and I don't think you should act on any of them — including the rejections — until they've been re-run properly. The home/away evaluation should wait until the measuring instrument is fixed.

You were right to keep pushing. I should have audited the method the first time a result came back marginal, not the sixth.
