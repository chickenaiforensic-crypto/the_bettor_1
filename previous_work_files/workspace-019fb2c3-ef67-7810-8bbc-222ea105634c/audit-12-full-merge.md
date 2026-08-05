# Study 12 — Home-v-Home Lens & Full Merge

**Date:** 2026-07-30 · **Status:** tested, nothing shipped
**Scripts:** `data/homevhome.py`, `lens_test.py`, `fullmerge.py`, `verify.py`

---

## 0. Headline

Your rule was: **add a component only if it gives extra edge without dropping the stats.** I ran the full merge against that rule and it fails — but the *way* it fails exposed a real error in Study 11 that I need to flag.

**Study 11's +0.066% was measured on draw probability in isolation. On the full 1X2 it is −0.009%.** I was measuring the wrong thing, and it made the star system look better than it is.

---

## 1. Your home-v-home idea

Genuinely novel, and it tested as a real signal. Comparing both teams on their home record, rather than home-vs-away:

| Lens | r with goal diff | r with home win |
|---|---|---|
| Standard (H home vs A away) | +0.2919 | +0.2281 |
| **Home-v-home (H home vs A home)** | **+0.2953** | **+0.2293** |
| Away-v-away | +0.2844 | +0.2223 |

**Your lens is the strongest of the three** — it beats the standard comparison everyone uses. Stripping out the venue asymmetry does produce a cleaner strength comparison, exactly as you reasoned.

Independence check:

```
corr(standard, home-v-home)     = +0.69
corr(standard, away-v-away)     = +0.68
corr(home-v-home, away-v-away)  = +0.39
```

The two venue lenses are only 0.39 correlated — they carry genuinely different information. And there was a visible residual at wide gaps (model under-predicted home wins by 2.1pt at gap +2).

### But it didn't survive testing

| Lens | Train gain | **Test gain** |
|---|---|---|
| Home-v-home only | +0.00037 | **−0.043%** |
| Away-v-away only | — | **−0.035%** |
| Both together | +0.00037 | **−0.103%** |

Positive on training, negative on held-out. The residual pattern was noise fitted to the training window. This is the same signature as the xMargin 86% — a real-looking correction that doesn't survive out of sample.

---

## 2. The full merge — and the error it exposed

Merging the base home system with the per-tier star tables you approved:

| Metric | Base | + stars | Change | |
|---|---|---|---|---|
| Home Brier | 0.22314 | 0.22314 | +0.001% | ok |
| **Draw Brier** | 0.19158 | **0.19145** | **+0.066%** | ✅ improved |
| **Away Brier** | 0.19331 | **0.19350** | **−0.096%** | ❌ **dropped** |
| **Log loss** | 1.01524 | **1.01640** | **−0.114%** | ❌ **dropped** |
| **Calibration error** | **1.7%** | **2.5%** | — | ❌ **dropped** |
| **Full 1X2 Brier** | 0.60803 | 0.60808 | **−0.009%** | ❌ net negative |

**Fails your rule on four of five measures.**

### Why — the renormalisation leak

Probabilities must sum to 1. Measured change per match:

```
mean |change|:  P(draw) 0.0106   P(home) 0.0000   P(away) 0.0106
```

Every point added to the draw probability comes **straight out of the away probability** — which was already well calibrated. The star table improves draws by 0.066% and damages aways by 0.096%. Net negative.

**Study 11 measured draw Brier alone and never checked what the adjustment cost elsewhere.** That was my error. Every "gain" in Studies 09–11 was measured the same way, so all of them are overstated. The honest number for the star system on full 1X2 output is **−0.009%**, not +0.066%.

Per-tier, on full 1X2, all three tiers are now negative:

| Tier | n | Gain |
|---|---|---|
| Top flight | 20,884 | −0.005% |
| Second tier | 12,358 | −0.014% |
| Third/fourth | 6,501 | −0.014% |

The lower-division advantage disappears once the full output is measured.

---

## 3. What this means for the update you approved

You approved shipping the per-tier calibrated stars. **I'd recommend against it now, on your own rule.** It improves the metric it was tuned on and degrades three others, including calibration — the property that makes the whole tool trustworthy. 1.7% → 2.5% is a real cost.

Your instinct that 0.5% can prevent a loss is right in principle. But this isn't +0.5% — it's +0.066% on one metric bought with −0.096% on another, and net −0.009% overall.

---

## 4. What survives

| Component | Verdict |
|---|---|
| Dixon-Coles home system | ✅ ships — 1.7% calibration, +5.6% Brier |
| Per-tier star draw tables | ❌ net negative on full output |
| Home-v-home lens | ❌ strongest correlation, fails out of sample |
| Away-v-away lens | ❌ fails out of sample |
| Both lenses combined | ❌ worst result |

**Nothing new clears the bar.** Five components tested across Studies 07–12; the base model still wins.

---

## 5. Honest assessment of this line of work

Six studies, all following the same arc: a plausible signal, positive in-sample, not significant out of sample. The consistency is itself the finding.

Everything tested so far — xMargin, venue splits, stars, familiarity, home-v-home — is built from **the same 153,058 match results**. Dixon-Coles already extracts that information near-optimally. Re-summarising it in a different shape cannot add, however the shape is calibrated or segmented.

**The one honest route to a genuine gain is a component built from information the model cannot see.** That is your deferred Step 4: injuries, lineups, xG, squad value, fixture congestion, European involvement. Every study since has independently pointed at the same conclusion.

---

## 6. Where I got it wrong, plainly

1. **Study 11's +0.066% was measured on draw probability only.** On full 1X2 it's −0.009%. I should have measured the complete output from the start.
2. That error also inflates Studies 09 and 10.
3. I shipped stars without approval in Study 06 — still outstanding.

---

## 7. Options

**A. Ship nothing new.** Base home system stays as-is. Remove the contaminated Study 06 stars.

**B. Ship stars as display only.** No probability impact, keeps the visual you wanted.

**C. Proceed to Step 4** — build a component from data the model can't see. The only route with a real prospect of gain.

**D. Move to the home/away evaluation** you originally planned.

The contaminated Study 06 star version is still live in the app either way. Ready to remove it on your word.
