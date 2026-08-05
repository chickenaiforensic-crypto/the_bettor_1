# Study 18 — The 3rd Chain Run on Lech Poznań v AGF Aarhus

**Date:** 2026-07-30 · **Status:** standby analysis system, as you directed
**Question you asked:** *where does it lean, and am I forcing the stats with a lean expectation?*

---

## 0. Direct answer to "are you forcing it"

**Partly yes.** I generalised from a domestic-league correlation (r = +0.105) to your cross-border fixture without ever running the chain on your actual teams. That was reasoning from a summary statistic instead of the case in front of me — the same mistake I made in Study 12 with home-vs-home, where I tested my own construction and reported it as though it settled your idea.

So I've now run it properly. **The chain does not lean toward either side. It has no lean at all — which is a different and more serious problem than bias.**

---

## 1. The chain, computed on your fixture

All 14 three-hop paths between the clubs, each producing an estimate of Lech's goal-difference edge:

| via X | via Y | Est. GD | Years spanned | Matches |
|---|---|---|---|---|
| Skonto | Jeunesse Esch | **+7.00** | 1987–1999 | 6 |
| Panathinaikos | Jeunesse Esch | +6.00 | 1970–1990 | 6 |
| Panathinaikos | Legia Warsaw | +4.50 | 1960–1995 | 6 |
| Spartak Moskva | Jeunesse Esch | +3.00 | 1980–1993 | 6 |
| IFK Göteborg | Jeunesse Esch | +0.33 | 1958–1992 | 7 |
| Spartak Moskva | Legia Warsaw | −0.50 | 1960–1995 | 6 |
| Liverpool | Jeunesse Esch | −0.50 | 1973–1987 | 6 |
| Beitar Jerusalem | Benfica | −1.00 | 1960–1998 | 8 |
| Sparta Praha | Benfica | −2.50 | 1960–2010 | 8 |
| IFK Göteborg | Legia Warsaw | −2.75 | 1960–1995 | 8 |
| Liverpool | Benfica | −3.25 | 1960–2005 | 14 |
| Marseille | Benfica | −3.50 | 1960–1990 | 8 |
| Basel | Benfica | −4.00 | 1960–2015 | 8 |
| Spartak Moskva | Benfica | **−4.50** | 1960–2012 | 8 |

```
MEAN     : Lech -0.12 goals
SD       : 3.67 goals
RANGE    : -4.50 to +7.00   (spread of 11.5 goals)
95% CI   : -7.31 to +7.07
```

**Where it leans: nowhere.** The mean is −0.12 goals, essentially dead level. But the estimates range from Lech winning by 7 to losing by 4.5.

**The problem isn't a biased lean — it's that the chain produces an answer indistinguishable from having no information.** A 95% interval of ±7 goals on a football match is the same as saying "I don't know." The mean looks reassuring and is an artefact of averaging noise in both directions.

Note also the **structure of the disagreement**: every chain through Jeunesse Esch (Luxembourg, semi-professional) favours Lech; every chain through Benfica favours Aarhus. The answer is decided entirely by which intermediary you route through, not by the two clubs.

---

## 2. The dates — the real killer

```
Lech European matches   : 1983–2015, most recent 2015
Aarhus European matches : 1955–1987, most recent 1987
Aarhus data is 39 YEARS OLD
Chain links span 1958 to 2015
```

**Aarhus's most recent European match in this dataset is from 1987.** The chain is comparing a Lech side from 2015 to an Aarhus side from 1987, via a Luxembourg club's form in 1990 and Benfica's in 1960.

No weighting or method fixes that. There is no recent information in the chain to extract.

---

## 3. Testing my own claim for bias

You asked whether I was forcing the result. So I tested my claim the way I'd test yours.

**Is it weak in both directions, or only where it suits my argument?**

| Subset | n | r |
|---|---|---|
| All fixtures | 127,332 | +0.1049 |
| Home side favoured by 3rd phase | 56,038 | +0.0705 |
| Away side favoured by 3rd phase | 70,432 | +0.0546 |

Weak symmetrically. Not a directional bias in my testing.

**Would more connectors rescue it?**

| Connectors | n | 2nd phase r | 3rd phase r |
|---|---|---|---|
| 1–4 | 9,383 | +0.1806 | **+0.1726** |
| 5–9 | 18,835 | +0.2700 | +0.1991 |
| 10–14 | 26,125 | +0.3792 | +0.1542 |
| 15–19 | 46,172 | +0.3737 | +0.0980 |
| 20–99 | 26,817 | +0.2464 | **+0.0395** |

**The 3rd phase gets *worse* with more connectors, while the 2nd phase gets better.** That's the opposite of a sample-size problem. More paths means more contradictory routes averaging toward zero — exactly what your 14 chains show.

This is genuine evidence *against* my hypothesis being a testing artefact: if the weakness were my construction, adding data would fix it.

**And where the 3rd phase is actually needed** (no direct common opponents): r = +0.1038 on 2,184 cases. No better.

---

## 4. What I got wrong and what stands

**Wrong:** I said the signal "degrades sharply with each hop" as though decay were the mechanism. The real mechanism is **path-dependence** — the answer depends on which intermediary you route through, and routes disagree by up to 11.5 goals. Averaging them doesn't extract signal, it cancels it.

**Also wrong:** I never ran it on your fixture before judging it. You were right to push.

**Stands:** the method can't determine this match. But for a better reason than I gave — not "the correlation is low," but "the 14 available paths span 1958–2015 and disagree by 11.5 goals, with Aarhus's most recent data 39 years old."

---

## 5. What the standby system will do

As directed, building it as an **analysis study system**, not a predictor. On any fixture it will report:

- every chain found, with intermediaries named
- each chain's estimate, year span, and match count
- **mean, spread, and range** — with the spread shown as prominently as the mean
- **data age warning** when links exceed ~5 years
- an explicit verdict: *usable* / *too dispersed* / *too old*

The spread is the output that matters. On your fixture it would print:

> **14 chains · mean −0.12 · spread ±3.67 · range −4.50 to +7.00 · oldest link 1958 · newest 2015**
> **VERDICT: NOT USABLE — chains disagree by 11.5 goals; Aarhus data 39 years old**

That's honest: it shows you the working and refuses to launder it into a number.

---

## 6. Where the method *would* work

The mechanism isn't broken — the data for this pair is. It should work where:

- both clubs play European football **regularly** (links within 2–3 years)
- chains are **short** (2 hops)
- intermediaries are **comparable** in level
- chains **agree** (low spread)

Two clubs from Netherlands and Belgium, both in Europe every season, would produce recent chains through shared opponents. **The standby system will tell us which fixtures qualify** — that's exactly what it's for, and we'll learn the qualifying conditions from live use rather than my assumptions.

---

## 7. On the broader question

You asked if I'm forcing stats with a lean expectation. Reviewing this project: I've been wrong in both directions — rejected your star system three times before finding my test was 10× too crude, then called home-vs-home "worse" after testing something you never proposed.

The pattern isn't a lean toward negative results. It's **testing my own construction and reporting it as a verdict on yours**. The fix is what happened here: run it on the actual case, show every intermediate number, and let you see where it breaks.

Ready to build the standby system on your confirmation.
