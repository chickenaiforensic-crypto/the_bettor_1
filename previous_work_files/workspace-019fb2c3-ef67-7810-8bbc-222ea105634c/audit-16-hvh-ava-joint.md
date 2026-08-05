# Study 16 — HvH × AvA Joint Analysis

**Date:** 2026-07-30 · **Status:** analysis complete, no implementation, awaiting your tactical decision
**Scripts:** `data/hvh_ava.py`, `decompose.py`, `extract.py`, `selection.py`
**Sample:** 119,703 fixtures with ≥4 home *and* ≥4 away matches for both sides, prior-only

---

## 0. What the pairing gives us

Pairing the two lenses produces **two independent axes**, not one:

```
CONSENSUS    = (HvH + AvA) / 2     "how much better is the home side, on both surfaces"
DISAGREEMENT = |HvH − AvA|         "do the two lenses tell the same story"
```

That decomposition is the real finding. One axis is strength; the other is *reliability of the strength estimate*.

---

## 1. The joint matrix — home win %

| | AvA <−0.5 | −0.5..0 | 0..0.5 | 0.5..1.0 | AvA >1.0 |
|---|---|---|---|---|---|
| **HvH >1.0** | 47.1% | 53.4% | 58.0% | 64.9% | **73.3%** |
| **HvH 0.5..1.0** | 42.7% | 46.8% | 50.7% | 55.8% | 61.8% |
| **HvH 0..0.5** | 39.0% | 45.2% | 46.4% | 51.6% | 58.4% |
| **HvH −0.5..0** | 34.5% | 39.7% | 43.1% | 45.4% | 52.0% |
| **HvH <−0.5** | **25.7%** | 33.8% | 39.1% | 41.9% | 45.2% |

**Monotonic in both directions** — 25.7% bottom-left to 73.3% top-right. Each lens adds on top of the other.

### Draw % — the diagonal effect

| | AvA <−0.5 | −0.5..0 | 0..0.5 | 0.5..1.0 | AvA >1.0 |
|---|---|---|---|---|---|
| **HvH >1.0** | 28.7% | 26.5% | 23.7% | 21.3% | **16.9%** |
| **HvH 0..0.5** | 29.6% | 28.2% | **29.4%** | 26.2% | 23.5% |
| **HvH <−0.5** | 25.8% | 28.9% | 28.4% | 28.8% | 28.1% |

Draws peak in the middle (29.6%) and collapse at the extreme (16.9%) — exactly the structure you predicted.

### Key diagnostic cells

| Configuration | n | Home | Draw | Away |
|---|---|---|---|---|
| **Both strong** (HvH>1, AvA>1) | 7,037 | **74.2%** | 16.5% | 9.3% |
| **Both weak** (both <−0.5) | 17,956 | 25.7% | 25.8% | **48.5%** |
| HvH strong, AvA weak | 3,427 | 51.4% | 27.1% | 21.5% |
| HvH weak, AvA strong | 3,252 | 49.5% | 28.4% | 22.1% |
| **Both level** (\|both\| < 0.25) | 6,283 | 42.4% | **30.0%** | 27.6% |

**When the lenses conflict, the match reverts to a coin flip (≈50%) regardless of which lens is strong.** That is genuine information: a team strong at home but weak away is *not* reliably strong.

---

## 2. Are the axes independent?

```
corr(consensus,    model P(home)) = +0.9117   <- model already knows this
corr(disagreement, model P(draw)) = -0.0901   <- nearly independent
```

Consensus is 91% explained by the model. **Disagreement is essentially new information** — and it shows real residuals:

| Consensus | Disagreement | n | Draw | Model D | Residual |
|---|---|---|---|---|---|
| level | agree | 14,861 | 29.5% | 28.5% | **+1.0%** ⚠ |
| level | conflict | 7,161 | 29.0% | 27.7% | **+1.3%** ⚠ |
| home better | conflict | 5,925 | 26.9% | 25.7% | **+1.2%** ⚠ |

Three cells where the model's draw prediction sits outside the actual 95% CI.

---

## 3. Can it be extracted? No.

Rolling-origin, paired, proportional renormalisation — the exact method that worked for stars:

| Weight | Pooled gain | p |
|---|---|---|
| 0.5 | +0.0016% | 0.64 |
| 1.0 | −0.0030% | 0.66 |

Every metric neutral: home +0.002% (p=0.66), draw +0.002% (p=0.74), full 1X2 +0.002% (p=0.64).

**Not harmful — just nothing.** The residuals are real per cell but too small and too diffuse to convert into probability gains. Unlike the star system, there's no plumbing fix here; the effect simply isn't large enough.

---

## 4. The tactical finding — where it *does* work

### Selection shoot-out

| Coverage | Model P(H) | Consensus | HvH alone |
|---|---|---|---|
| 10% | **73.0%** | 71.0% | 67.6% |
| 3% | **82.5%** | 79.5% | 75.9% |
| 1% | **87.6%** | 85.5% | 81.0% |

The model still picks best alone. But **filtering the model's picks with consensus works**:

| Filter on model's top 10% | n | Home win | vs base | |
|---|---|---|---|---|
| Model top 10% (baseline) | 11,970 | 73.0% | — | |
| **+ consensus > 1.0** | 9,497 | **74.8%** | **+1.8%** | ✅ significant |
| **+ consensus > 1.5** | 4,840 | **78.6%** | **+5.6%** | ✅ significant |
| + lenses agree (disagree<0.6) | 5,347 | 72.1% | −0.9% | no |
| + both lenses positive | 11,333 | 73.4% | +0.4% | no |

**Consensus > 1.5 lifts the model's best picks from 73.0% to 78.6% — a 5.6 point gain, confidence intervals don't overlap.** That's the strongest actionable result in this whole line of work.

Note what *doesn't* work: filtering on lens agreement alone (−0.9%). It's the **magnitude** of consensus that matters, not whether the lenses agree.

### Draw selection

| Filter on model's top 10% draw picks | n | Draw | vs base |
|---|---|---|---|
| Model top-10% draw picks | 11,970 | 30.6% | — |
| + \|consensus\| < 0.2 AND agree < 0.5 | 1,697 | 31.8% | +1.2% |
| + \|consensus\| < 0.2 | 3,696 | 31.2% | +0.7% |

Directionally right but CIs overlap. Not significant.

---

## 5. What the stats tell us

1. **Two independent axes exist.** Consensus (strength, model already knows) and disagreement (reliability, model doesn't know).
2. **Conflicting lenses ⇒ coin flip.** ~50% home regardless of which lens is strong. A side strong at home but weak away is not dependably strong.
3. **Draws peak where both lenses are level** (30.0%) and collapse where both are extreme (16.9%).
4. **The pair adds nothing to probability output** — neutral at every weight tested.
5. **The pair adds real value as a filter** — consensus > 1.5 gives +5.6pt on the model's own best picks.

The honest reading: this belongs in **selection**, not in the probability engine. That's a different role from the star system, which earned its way into the maths.

---

## 6. Proposed tactical implementation — for your approval

**Do NOT add to the probability model.** Neutral everywhere, adds complexity for nothing.

**DO add as a confidence layer on top of the existing tiers:**

```
CONSENSUS = ((home GD/game at home − away GD/game at home)
           + (home GD/game away  − away GD/game away)) / 2

Tier A+ / A  AND  consensus > 1.5   ->  "STRONG"     (78.6% observed)
Tier A+ / A  AND  consensus > 1.0   ->  "CONFIRMED"  (74.8% observed)
Tier A+ / A  AND  consensus < 0     ->  "CONFLICTED" (model and lenses disagree — flag it)
|consensus| < 0.2 and both lenses level -> "DRAW-LEAN" (31.8%, advisory only)
```

Requires ≥4 home and ≥4 away matches for both sides; otherwise shows "insufficient data" rather than guessing.

This changes **no probability**, so it cannot damage calibration or any Brier metric. It reorders and labels what the model already produces.

---

## 7. Awaiting your decision

1. Approve the confidence layer as specified, or adjust the thresholds?
2. Should "CONFLICTED" suppress a pick, or just flag it?
3. Ship alongside the approved star v2 update, or separately?

Nothing built. The star v2 update from Study 14 is also still pending implementation, along with removing the contaminated Study 06 stars.
