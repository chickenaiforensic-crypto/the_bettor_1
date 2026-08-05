# Study 23 — League Strength Weighting

**Date:** 2026-07-30 · **Prompted by:** "if cross-border leagues have strong difference then the leagues will have to get a weighting system"

---

## 0. Your premise is correct. The proposed fix makes things worse.

You identified a real gap: the chain engine treats a Moldovan link and a Dutch link as equivalent. I measured the difference, and it is large. I then built the weighting and tested it — it **degraded accuracy significantly**.

---

## 1. League strength is real and large

Measured from **European matches only** — the one arena where leagues meet. No external coefficient tables, results only.

| Country | Euro matches | GD per match |
|---|---|---|
| **ENG** | 785 | **+0.81** |
| ESP | 782 | +0.59 |
| GER | 679 | +0.48 |
| ITA | 632 | +0.37 |
| NOR | 136 | +0.28 |
| FRA | 501 | +0.19 |
| POR | 390 | +0.17 |
| NED | 319 | +0.12 |
| … | | |
| CRO | 108 | −0.63 |
| SRB | 118 | −0.80 |
| MDA | 68 | −0.87 |
| FIN | 58 | −0.91 |
| **BLR** | 62 | **−1.11** |

**Range: 1.92 goals per match. Standard deviation 0.42.**

That is not a rounding error. An English club's +1.0 goal difference and a Belarusian club's +1.0 describe very different achievements — exactly your point.

---

## 2. The weighting, implemented and tested

Each chain link adjusted by the strength gap between the two clubs' leagues:

```
adjusted_link = raw_GD − (strength[club_league] − strength[opponent_league])
```

Tested on **1,203 cross-border fixtures**, chains built from prior seasons only, paired comparison.

| Method | Correlation | Direction accuracy | 95% CI |
|---|---|---|---|
| **Raw goal difference** | **+0.3102** | **64.5%** | [61.5%, 67.5%] |
| League-adjusted | +0.1943 | 58.9% | [55.8%, 62.0%] |

**McNemar paired test:** adjusted right / raw wrong = 42 · raw right / adjusted wrong = **96** · **p < 0.0001**.

The adjustment is **significantly worse** — it loses 5.6 points of direction accuracy and a third of the correlation.

---

## 3. Why a correct premise produced a failing fix

**Double-counting.** A club's results *already encode* its league strength. When Sheriff beat a Moldovan rival 3-0, that scoreline reflects weak opposition. Subtracting a league-strength term removes information the raw result already carried correctly — then subtracts it again.

**Club ≠ league.** Sheriff Tiraspol is far stronger than the average Moldovan club. Penalising it by the Moldovan average punishes it for its rivals' weakness. The same applies in reverse to a mid-table English side receiving England's +0.81 credit.

**Chains amplify the error.** A 3-hop chain applies the correction three times, compounding the distortion at each link.

**The bridges are already European.** Cross-border links come from European ties — matches already played *between* leagues. Those results have league strength baked in by construction. Adjusting them corrects for something already accounted for.

---

## 4. What this means for the protocol

No change to Phase 3/4/5. Raw goal difference stays.

**But your instinct points somewhere the current system genuinely is weak**, and I want to name it rather than close the topic:

The problem is not that links need *reweighting* — it is that links differ in *reliability*. A European tie between two clubs is direct evidence. A domestic link inside Moldova tells you about Moldova. The chain engine currently mixes both.

An alternative worth testing later — **not now, and not without your approval**:
- weight links by *context* (European vs domestic) rather than by league strength
- restrict chains to European-only links where volume permits
- weight by number of matches behind each link rather than by league

Those are different hypotheses from the one just tested. Each would need its own validation.

---

## 5. Verdict

| Claim | Result |
|---|---|
| Leagues differ substantially in strength | ✅ **Confirmed** — 1.92 goal range |
| Ignoring it is a gap in the model | ✅ **Correct in principle** |
| Adjusting links by league strength fixes it | ❌ **Rejected** — p < 0.0001, significantly worse |

The measurement is kept in `chain/league_strength.pkl` — it is genuinely useful as *context* when reading a chain by eye, even though it fails as a correction term.

**Protocol unchanged. Ready for fixture #2 on your word.**
