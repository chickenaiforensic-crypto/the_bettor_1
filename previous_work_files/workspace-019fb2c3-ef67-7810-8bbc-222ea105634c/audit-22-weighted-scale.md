# Study 22 — Two Questions Answered

**Date:** 2026-07-30
**Q1:** these fixtures have lots of head-to-head and opponent data — why no conclusive result?
**Q2:** does the weighted result scale (+1/+2/+4/+6, −4/−6) improve the system?

---

## Q1 — Why so little, when the data looks plentiful

You were right to push. I found a **real bug**, and then the real answer.

### The bug: 76 clubs were split into duplicate identities

```
'AFC Ajax'            and  'Ajax'            = two separate nodes
'ACF Fiorentina'      and  'Fiorentina'      = two separate nodes
'FK Shakhtar Donetsk' and  'Shakhtar Donetsk'
'Djurgardens IF'      and  'Djurgårdens IF'
'SL Benfica'          and  'Benfica'
... 76 in total
```

European sources write `AFC Ajax`; domestic sources write `Ajax`. My normaliser stripped accents but not club-type prefixes, so **the same club existed twice** — and crucially, **its European record and its domestic record were on different nodes.**

Since European matches are the *only* thing that bridges countries, splitting exactly those clubs severed the bridges. Fixed: normaliser now strips `FC/AFC/ACF/FK/NK/SL/RSC/...` tokens. Canonical identities went from 1,474 → **1,444**, merging the duplicates.

### The real answer: cross-border sparsity

Even with identities merged, Panathinaikos v Paksi still has **zero shared opponents**. Here is why:

```
domestic match-links : 197,848   (98%)  ← connect clubs INSIDE one country
european match-links :   4,244   ( 2%)  ← the ONLY links that bridge countries

clubs with any european match : 364 of 1,444
median european opponents/club: 5
```

**Your teams have hundreds of matches each — but ~98% of them are against domestic rivals who can never connect to a foreign club.** Panathinaikos has 699 matches and 54 opponents, but only **17** are European. Paksi has 7. Two sets of 17 and 7 drawn from hundreds of possible European clubs rarely intersect.

That is not missing data. **It is the actual structure of European football**: clubs mostly play their own league, and cross-border fixtures are rare and non-overlapping.

The chain method works — it found 8 two-hop connectors for that fixture. It simply cannot manufacture certainty from a graph that thin.

---

## Q2 — Your weighted scale, tested

Implemented exactly as specified in `chain/weighted.py`:

| Result | Score |
|---|---|
| Draw 0-0 | **+1** |
| Draw 1-1, 2-2, … | **+2** |
| Win by 1 | **+4** |
| Win by 2+ | **+6** |
| Loss by 1 | **−4** |
| Loss by 2+ | **−6** |

Tested against plain goal difference on **1,203 cross-border fixtures**, chains built only from prior seasons.

### Result

| Metric | Plain goal difference | **Your weighted scale** |
|---|---|---|
| Correlation with outcome | **+0.3102** | +0.2732 |
| Direction accuracy | **64.5%** | 62.5% |
| 95% CI | [61.5%, 67.5%] | [59.4%, 65.5%] |

**Paired comparison (McNemar):** weighted right / GD wrong = 37 · GD right / weighted wrong = **57** · **p = 0.0495**.

Plain goal difference wins, and the difference is statistically significant at the 5% level.

### Draw detection

| Metric | Level-band draw rate |
|---|---|
| Plain GD | 21.1% |
| Weighted | 19.1% |
| Baseline | 19.6% |

Separating 0-0 from 1-1 did **not** improve draw detection — the weighted level band actually landed *below* the baseline.

### Why it underperforms

The scale is **non-linear in a way that loses information at the top end.** A 5-0 win and a 2-0 win both score +6. Goal difference keeps that distinction, and in a chain you are *summing* links — so compressing large margins discards exactly the signal that distinguishes a strong club from an average one.

It also **over-weights the draw/win boundary**: a 1-0 win scores +4 while a 1-1 draw scores +2, a gap of 2 points, whereas the same step in goal difference is 1. That amplifies noise around the most common scorelines.

The intuition — that a 0-0 differs from a 1-1, and a narrow win from a thrashing — is sound. But goal difference already encodes the second, and the first turns out not to carry usable signal here.

---

## Verdict

| Item | Result |
|---|---|
| Duplicate-identity bug | **Fixed** — 76 clubs merged, bridges restored |
| Why so few conclusive calls | **Structural**: 2% of links are cross-border, median 5 European opponents/club |
| Weighted scale as chain metric | **Rejected** — significantly worse (p=0.0495) |

Kept in `chain/weighted.py` in case you want it for a different purpose — a league table or form display, where its readability is an advantage and the compression doesn't matter.

---

## Rebuilding coverage after the identity fix

The merge changes the graph. All 17 fixtures need re-running before the card is trustworthy — several may now find paths that were previously severed. That is the next step.

One housekeeping note: `/tmp` was cleared between sessions and took the European competition files with it. They are now stored in `/home/user/chain/ucl/`, inside the workspace, so this cannot recur.
