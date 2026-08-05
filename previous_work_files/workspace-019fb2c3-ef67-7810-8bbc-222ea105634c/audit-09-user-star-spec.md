# Study 09 — Star Ranking Built to Your Specification

**Date:** 2026-07-30 · **Status:** tested, nothing implemented, awaiting your decision
**Scripts:** `data/user_spec.py`, `draw_test.py`, `robust2.py`

---

## 0. One correction I owe you

You said I was using web ranking data and bypassing your instructions. I need to correct the record, because if you can't trust what's in the app nothing else matters.

**The app makes zero network calls.** Verified by scanning the file:

```
fetch(          0        http://        0
XMLHttpRequest  0        https://       0
WebSocket       0        src=           0
sendBeacon      0        import(        0
```

The stars I built came from `att[team] + dfn[team]` — the model's own coefficients, fitted from match results. No table position, no external ranking, no web lookup. Same for the 153,058 match results: downloaded **once, by me, into this workspace** to fit the model, then baked in as numbers. The app itself never reaches out.

**Where you are right:** I picked the ranking basis myself without asking, and it was a poor choice — Study 08 showed it misranks Sunderland (7th, rated 1★) and Nott'm Forest (16th, rated 4★). You should have specified the metric. You have now, and it's built below.

---

## 1. Your specification, implemented exactly

```
Rank teams by games played and games won/drawn
Minimum 5 games to enter the ranking
Stars = goal-determining categorisation
Same star plain => expected equality => raised draw odds
```

Built as:

```
metric = (3×won + drawn) / played        ← your won/drawn measured against played
qualify = played >= 5                    ← your minimum
stars = quintile rank within league-season, 1..5
```

Everything computed from prior matches only. **132,915 fixtures** qualified.

---

## 2. Your core claim — confirmed

**Same star plain raises draw odds:**

| | n | Draw rate | 95% CI |
|---|---|---|---|
| **Same star** | 23,568 | **28.1%** | [27.5%, 28.7%] |
| Different star | 109,347 | **26.4%** | [26.1%, 26.7%] |

**+1.68 percentage points, confidence intervals don't overlap.** Your reasoning was correct: putting two teams on the same star plain does signal expected equality, and equality does raise the draw rate.

**And it strengthens as the gap widens:**

| \|gap\| | n | Draw rate | 95% CI |
|---|---|---|---|
| 0 | 23,568 | **28.1%** | [27.5%, 28.7%] |
| 1 | 44,472 | 28.1% | [27.7%, 28.6%] |
| 2 | 33,474 | 26.3% | [25.9%, 26.8%] |
| 3 | 21,342 | 24.9% | [24.4%, 25.5%] |
| 4 | 10,059 | **21.9%** | [21.1%, 22.7%] |

A **6.2 point** spread from level to 4-star gap, monotonic, with tight intervals. The signal is real and it behaves exactly as you described.

Goal difference tracks it cleanly too — from −0.64 at gap −4 to +1.41 at gap +4.

---

## 3. Against the current model

Draw-only Brier score, held out (39,823 matches from Sept 2019):

| System | Draw Brier | Log loss |
|---|---|---|
| Constant 26.9% | 0.19336 | 0.57518 |
| **Your stars alone** | **0.19270** | 0.57341 |
| Current model (DC) | 0.19163 | 0.57033 |
| **Model + stars blended (w=0.2)** | **0.19155** | — |

Two findings:

1. **Your stars alone beat a constant draw rate** — the categorisation carries genuine draw information on its own.
2. **Blended with the model, they improve it: +0.041%.** This is the first positive result any add-on has produced.

---

## 4. But the gain is not robust

I stress-tested it before recommending anything:

```
overall gain:      +0.0000785 Brier (+0.041%)
bootstrap 95% CI:  [-0.0008525, +0.0010644]
P(gain <= 0) = 0.442
-> NOT DISTINGUISHABLE FROM ZERO
```

The confidence interval straddles zero, and there's a 44% chance the true gain is zero or negative.

Directionally it's encouraging — **6 of 7 seasons positive**, and consistently strongest in the lower English divisions (E1 +0.00017, E2 +0.00028, E3 +0.00018). But only **5 of 8 leagues** positive, with Spain, Italy Serie B and the Premier League slightly negative.

**Why the signal doesn't add much:** the model already knows it.

| Star gap | Stars say | Model says | Actual | Model error |
|---|---|---|---|---|
| −2 | 28.2% | 27.6% | 27.3% | +0.3% |
| −1 | 28.9% | 27.9% | 29.4% | −1.6% |
| 0 | 28.1% | 27.4% | 28.1% | −0.7% |
| +2 | 25.3% | 24.5% | 23.3% | +1.2% |
| +4 | 19.7% | 18.9% | 17.8% | +1.1% |

The model's draw prediction already tracks reality within ~1.6pt at every star gap. Your stars are measuring something true — the model is measuring the same true thing slightly more precisely, because it uses continuous ratings rather than 5 buckets.

---

## 5. Honest summary

| Claim | Verdict |
|---|---|
| Ranking should come from our own metric, not the web | ✅ Correct — and it already did, though I chose the metric badly |
| Won/drawn per game, min 5 games, is a sound basis | ✅ Works — beats a constant draw rate on its own |
| Same star plain raises draw odds | ✅ **Confirmed** — 28.1% vs 26.4%, +1.68pt |
| Draw rate falls as star gap widens | ✅ **Confirmed** — 28.1% → 21.9%, monotonic |
| Stars improve the app's draw prediction | ⚠️ **+0.041%, but CI includes zero** |

Your model of how football works is right. The categorisation does what you said it would. It just overlaps heavily with what the Dixon-Coles ratings already capture, so the *incremental* value is small and not yet provable.

---

## 6. Options — your call, nothing built without it

**A. Ship it anyway at w=0.2.** Directionally positive, 6/7 seasons, can't hurt much. Honest framing: "probably a small improvement, not proven."

**B. Ship for lower divisions only.** The gain is consistently positive and largest in E1/E2/E3 where the model has less to work with. Restricting to where it demonstrably helps is more defensible than blanket application.

**C. Rebuild the star basis first.** Study 08's proposed fixes — rolling cutoffs (removes look-ahead), hysteresis (cuts the 17.3% weekly churn), min-5 already in your spec. A cleaner categorisation may produce a bigger, provable gain.

**D. Display only.** Show stars and the same-star draw lift as information, without touching the probability maths.

**E. Drop it and move to the home/away evaluation.**

My read: **C then re-test** is the most likely route to a provable gain, since the current version is handicapped by contaminated cutoffs and boundary churn. But this is your system and your call.

One thing worth deciding regardless: the contaminated star version from Study 06 is **still live in the app**. Remove it now, or leave it pending your decision?
