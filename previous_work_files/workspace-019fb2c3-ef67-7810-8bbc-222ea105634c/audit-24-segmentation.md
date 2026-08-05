# Study 24 — Segmentation Test on the Opponents-of-Opponents Data

**Date:** 2026-07-30
**Prompted by:** you asking where the exhaustive test data was. It did not exist. This is that test.
**Question:** does chain accuracy depend on whether links are European ties or domestic matches?
**Output:** no predictions. This only judges whether the existing tier table is sound.

---

## 0. The data now exists

`chain/segment_rows.pkl` — **1,203 cross-border fixtures**, every chain tagged by link context, built strictly from prior seasons.

Segments:
- **EUR-only** — every link in the chain is a European tie
- **MIXED** — chain combines European ties with domestic league matches
- **DOM-heavy** — majority domestic (only 12 cases; too few to judge)

---

## 1. Direction accuracy by segment

| Segment | Fixtures | Decisive | Direction | 95% CI | r with GD |
|---|---|---|---|---|---|
| **EUR-only** | 463 | 369 | **65.0%** | [60.0%, 69.7%] | **+0.3710** |
| **MIXED** | 728 | 588 | **64.1%** | [60.2%, 67.9%] | +0.2588 |
| DOM-heavy | 12 | — | too few | — | — |

**Direction accuracy is effectively identical — 65.0% vs 64.1%, intervals almost fully overlapping.**

But the **correlation differs meaningfully**: +0.371 for European-only chains versus +0.259 for mixed. European-only chains get the *magnitude* right more often, even though both get the *direction* right at the same rate.

---

## 2. Tier tables rebuilt per segment

### EUR-only (n=463)
| Tier | Band | n | Home | Draw | Away |
|---|---|---|---|---|---|
| CH-F | ≤ −1.00 | 140 | 30.7% | 22.9% | 46.4% |
| CH-E | −1.00…−0.35 | 54 | 35.2% | 22.2% | 42.6% |
| CH-D | −0.35…+0.35 | 81 | 44.4% | 24.7% | 30.9% |
| CH-C | +0.35…+1.00 | 54 | 53.7% | 13.0% | 33.3% |
| CH-B | +1.00…+2.00 | 76 | 59.2% | 22.4% | 18.4% |
| **CH-A** | ≥ +2.00 | 58 | **79.3%** | 10.3% | 10.3% |

### MIXED (n=728)
| Tier | Band | n | Home | Draw | Away |
|---|---|---|---|---|---|
| CH-F | ≤ −1.00 | 153 | 35.9% | 21.6% | 42.5% |
| CH-E | −1.00…−0.35 | 139 | 36.0% | 23.0% | 41.0% |
| CH-D | −0.35…+0.35 | 143 | 55.2% | 18.9% | 25.9% |
| CH-C | +0.35…+1.00 | 142 | 62.7% | 14.1% | 23.2% |
| CH-B | +1.00…+2.00 | 91 | 64.8% | 16.5% | 18.7% |
| **CH-A** | ≥ +2.00 | 60 | **65.0%** | 21.7% | 13.3% |

### The two differences worth checking

**CH-A: 79.3% (EUR-only) vs 65.0% (MIXED)** — a 14-point gap.
```
EUR-only 46/58 = 79.3%  CI [67.2%, 87.7%]
MIXED    39/60 = 65.0%  CI [52.4%, 75.8%]
Fisher exact p = 0.1023  ->  NOT SIGNIFICANT
```

**CH-D: 44.4% vs 55.2%** — an 11-point gap.
```
Fisher exact p = 0.1282  ->  NOT SIGNIFICANT
```

Both gaps look large. Neither clears significance at these sample sizes.

---

## 3. Does the European fraction of a chain predict reliability?

| Euro fraction of links | n | Direction | 95% CI |
|---|---|---|---|
| 34–67% | 227 | 65.2% | [58.2%, 71.7%] |
| 67–99% | 504 | 63.9% | [59.1%, 68.4%] |
| 100% | 463 | 65.0% | [60.0%, 69.7%] |

**Flat.** The proportion of European links in a chain does not predict how reliable it is.

---

## 4. Verdict on the existing tier table

| Question | Answer |
|---|---|
| Is the tier table fitted on an unsegmented mix? | **Yes** — confirmed |
| Does direction accuracy differ by segment? | **No** — 65.0% vs 64.1%, overlapping |
| Do tier rates differ by segment? | Visibly, but **not significantly** (p = 0.10, 0.13) |
| Does euro-fraction predict reliability? | **No** — flat across bands |
| **Is the existing table unsound?** | **Not demonstrably.** It survives this audit. |

The blended table is **not proven wrong**. That is a weaker statement than "it is right" — the CH-A gap of 14 points is large enough to matter if real, and this sample cannot resolve it. With 58 and 60 fixtures per cell, only a difference above roughly 20 points would register as significant.

---

## 5. What this does and does not license

**Does:** continue using the current tier table. It passed the audit I should have run first.

**Does not:** claim European-only chains are equivalent to mixed ones. The correlation gap (+0.371 vs +0.259) is real in the data even where the direction test is flat, and it suggests mixed chains are noisier on magnitude. That matters for any market depending on margin — handicaps especially.

**One concrete change I would propose, not implement without approval:** report the segment alongside every call, so an EUR-only chain and a mixed chain are visibly different objects even while they share a tier table.

---

## 6. On the process failure

This test should have run before the 30 July card, not after you asked twice. The Maccabi call I gave you cited "64.3% measured direction accuracy" from a table I had not decomposed. That number now has support — 64.1% for mixed chains, which is what Maccabi's chains are — but I did not know that when I said it.
