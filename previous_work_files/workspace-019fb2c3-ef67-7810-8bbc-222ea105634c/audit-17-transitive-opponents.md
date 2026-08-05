# Study 17 — Competition Context & the 3rd-Phase Common-Opponent Method

**Date:** 2026-07-30 · **Status:** analysis complete, nothing built, awaiting your decision
**Scripts:** `data/graph.py`, `data/transitive.py`, `/tmp/cl/` (Champions League data)

---

## 0. Two findings, one good and one cautionary

**Your 3rd-phase concept is structurally correct and I verified it works on the actual fixture.** Lech Poznań and AGF Aarhus have **zero** direct common opponents, but a path exists at exactly 3 hops. That is precisely the mechanism you described.

**But when I measured whether transitive strength actually predicts, it degrades sharply with each hop.** Details below — the concept is sound, the signal is weak.

---

## 1. Why the home system disappears — confirmed

You predicted this. Building the opponent graph from all 153,058 domestic matches:

```
clubs: 630   edges: 14,349   connected components: 11
  ENG 114 clubs | ESP 87 | ITA 82 | FRA 67 | GER 64 | TUR 52 | POR 39 | GRE 38 ...
```

**Every country is a sealed island.** Divisions connect internally via promotion/relegation, but there is **no path between countries at any degree** — 2nd, 3rd, or 10th. A Polish club and a Danish club share zero opponents, transitively, forever.

So for a cross-border fixture the domestic model cannot help at all — not just home advantage, but the entire rating structure.

---

## 2. European competition is the bridge

I found and loaded open-source Champions League data (1955–present, footballcsv):

```
6,554 matches | 501 clubs after name normalisation | 2,661 edges
connected components: 1  (100% of clubs in a single component)
```

**European competition welds the 11 islands into one graph.** That's the missing link your method needs.

### The actual fixture

```
Lech Poznan  : 12 distinct CL opponents
Aarhus GF    :  8 distinct CL opponents
DIRECT common opponents (2nd phase): 0

SHORTEST PATH: Lech Poznan -> Panathinaikos -> Jeunesse Esch -> Aarhus GF
degrees of separation: 3   <- exactly your 3rd phase

3rd-phase connectors found: 14 pairs
  (Basel, Benfica), (IFK Goteborg, Legia Warsaw), (Liverpool, Jeunesse Esch)...
```

**Your reasoning was right:** no direct link exists, and the 3rd phase is where the connection lives.

---

## 3. But does transitive strength predict?

I tested this inside domestic leagues, where there are 132,915 fixtures and real ground truth — a far more favourable setting than a 3-hop European chain.

| Signal | n | r with actual goal difference |
|---|---|---|
| **Direct form (1st phase)** | 132,915 | **+0.3304** |
| **Common opponents (2nd phase)** | 130,090 | **+0.2936** |
| **Opponents-of-opponents (3rd phase)** | 127,332 | **+0.1049** |

**Each hop loses roughly two-thirds of the signal.** And after removing what the 2nd phase already explains, the 3rd phase's residual correlation with the result is **+0.0652** — near noise.

That's with **13.7 second-degree connectors on average** and every match played in the same league, same season. The Lech–Aarhus chain has **14 connectors spread across different countries, competitions and years**, linked through clubs like Jeunesse Esch (Luxembourg, semi-professional).

**Extrapolating honestly:** a 3-hop cross-border chain would carry meaningfully less signal than +0.105, probably below +0.05. That is not enough to base a prediction on.

---

## 4. Why the decay happens

Each hop compounds three errors:

1. **Sampling noise** — one or two matches per link, often years apart.
2. **Time drift** — Lech's 2010 CL squad has no relation to their 2026 squad.
3. **Venue and context** — two-legged ties, neutral venues, dead rubbers.

Transitive comparison assumes strength is consistent and additive along a chain. Over one hop within a season that roughly holds. Over three hops across a decade and three countries, it doesn't.

---

## 5. What I recommend building

### A. Competition field — build it (approved)

The app currently assumes every fixture is domestic league. It needs to know what it's looking at:

```
DOMESTIC LEAGUE  -> full model, home advantage applied, tiers + consensus
DOMESTIC CUP     -> model applies, home advantage reduced, flag rotation risk
EUROPEAN TIE     -> model DECLINES: teams not comparably rated
NEUTRAL VENUE    -> home advantage set to zero
UNKNOWN          -> decline
```

Plus an explicit **neutral-venue toggle**, since as you said "home" is sometimes only nominal. This is honest scope control and it's the highest-value change here.

### B. European bridge ratings — worth building, with limits

Rather than chained transitive comparison, the sound approach is a **single unified rating fitted across domestic *and* European matches simultaneously**. European ties become direct constraints linking national rating scales, instead of a fragile hop-by-hop chain. This is how UEFA coefficients and Elo systems handle it.

That would let the model rate Lech v Aarhus properly. It's a substantial build — refitting the whole model on a combined dataset — and I'd want your approval before starting.

### C. 3rd-phase chaining — I'd advise against

Not because the idea is wrong. The graph theory is correct and the path exists. But the measured signal decay (+0.33 → +0.29 → +0.10, residual +0.065) says a 3-hop cross-border chain would produce numbers that look authoritative and aren't.

That's the exact failure pattern from the xMargin study: a plausible-looking construction with no predictive power behind it.

---

## 6. Honest summary

| Claim | Verdict |
|---|---|
| Home system disappears for cross-border fixtures | ✅ Confirmed — 11 disconnected islands |
| Head-to-head needed where home doesn't apply | ✅ Correct — but Lech/Aarhus have never met |
| Common opponents don't exist for this fixture | ✅ Confirmed — zero direct |
| 3rd phase provides a connection | ✅ **Confirmed — path is exactly 3 hops** |
| 3rd phase enables "nearly accurate determination" | ❌ r = +0.105, residual +0.065 |

Your structural analysis was right at every step. The obstacle is signal decay, which is a property of the data rather than a flaw in the reasoning.

---

## 7. Decisions needed

1. **Competition field** — build as specified in §A?
2. **Unified European ratings** (§B) — approve the larger build, or defer?
3. **3rd-phase chaining** (§C) — accept my recommendation to skip, or would you like it built as an advisory-only display so you can judge it against live fixtures?
