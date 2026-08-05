# Study 19 — Chain System Foundation

**Date:** 2026-07-30 · **Status:** foundation built and validated
**Files:** `chain/build_graph.py`, `chain/chain.py`, `chain/validate.py`
**Data:** results only. No odds, no market, no commentary — permanently.

---

## 0. On Brier

Brier compares our predicted probability to **what actually happened on the pitch**:

```
Brier = Σ (predicted − actual)²      actual = 1 if it occurred, 0 if not
```

The only inputs are our number and the scoreline. It's the tool that caught my broken test in Study 13, using match results alone. I applied it to the market once to show that price scored worse — that comparison was optional and is now retired. The ruler stays; the market doesn't.

Your process point is taken. Foundation first.

---

## 1. Foundation built

```
domestic edges : 153,058   (18 leagues)
Poland         :   4,091
Denmark        :   2,958
European       :   4,244   (CL / EL / Conference + qualifiers) ← the bridges
TOTAL          : 164,351 matches, 1,049 clubs, 56 countries
```

European competition welds the previously disconnected national islands into one graph. Name resolution handles the different spellings across sources (`Aarhus` / `Aarhus GF`, `Lech Poznan` / `Lech Poznań`).

The engine reports direct meetings, 2nd phase (shared opponents), and 3rd phase (opponent-of-opponent), with every path's estimate, year span, match count, and whether it mixes domestic and European context.

---

## 2. Validation — and I was wrong twice

Tested on **2,778 real cross-border European matches since 2021**, chains built only from links predating each tie. 864 scoreable estimates.

### Finding 1: the 3rd phase is far stronger than I claimed

| Setting | r with actual goal difference |
|---|---|
| Study 17 — 3rd phase inside domestic leagues | **+0.105** |
| **Study 19 — 3rd phase on cross-border ties** | **+0.274** |

**2.6× stronger where it's actually needed.**

My Study 17 test measured the 3rd phase *inside domestic leagues* — where every club already shares 14 direct opponents, so the transitive route is redundant by construction. I then generalised that to cross-border fixtures, which is exactly the setting where it isn't redundant. **Wrong test, wrong conclusion, and I stated it as settled.**

### Finding 2: the 3rd phase beats the 2nd on these fixtures

| Method | n | r | Direction correct |
|---|---|---|---|
| 2nd phase (shared opponents) | 171 | +0.212 | 57.7% |
| **3rd phase (opponent-of-opponent)** | **693** | **+0.274** | **62.6%** |

More paths, better correlation, better direction calls. Your instinct that the 3rd phase carries real weight is supported.

### Finding 3: my usability rule was wrong

I built the system to reject high-spread chains. The data says the opposite:

| Spread between paths | n | r |
|---|---|---|
| 0–1.5 (tight agreement) | 37 | +0.195 |
| 1.5–3 | 151 | +0.073 |
| **3–5** | 269 | **+0.384** |
| 5+ | 407 | +0.251 |

**Tight agreement is not better.** In Study 18 I told you the Lech–Aarhus chains were "not usable" because they disagreed by 11.5 goals. That reasoning was unfounded — high-spread chains predict *better* here, probably because spread rises with the number of paths, and more paths means more information.

The `verdict()` function encodes my wrong rule and must be rebuilt from this evidence.

---

## 3. The live case

**Lech Poznań 1–5 AGF Aarhus** — logged as case #1.

| Source | AGF win % | Called it? |
|---|---|---|
| Our 3rd-phase chain | 58.1% | **YES** |
| (market, for the record) | 21.7% | no |

Chain estimates −0.44 and −2.00 (mean −1.22); actual −4.00. Direction right, magnitude understated.

Rebuilt through the new engine with a 2021+ window it finds only one path (Crvena Zvezda → Midtjylland, −0.76) and correctly reports **THIN**. The original manual analysis used a wider net across both domestic and European layers. That gap between what the engine finds and what a manual search finds is the next thing to fix.

---

## 4. Honest state

**Working:** graph foundation, name resolution across sources, chain discovery, transparent per-path output, validated signal at r=+0.274 on 693 real cross-border ties.

**Not working:** the usability rule (built on my assumption, contradicted by data), and path discovery is too narrow — it found 1 path where manual search found 2 usable ones.

**Not yet built:** converting a chain estimate into probabilities, and integration with the main app.

r=+0.274 is a real signal but not a strong one. Direction is right 62.6% of the time against a 48.8% home-win base rate. Useful as an analysis tool for fixtures the main model cannot rate at all — which is exactly the standby role you specified.

---

## 5. Next steps, awaiting your call

1. **Rebuild the usability rule from evidence** rather than my assumption — spread should probably not gate anything.
2. **Widen path discovery** so the engine finds what a manual search finds.
3. **Test what actually predicts** — path count, recency, context mixing — and gate on those.
4. Only then: probabilities, and only then: app integration.

Foundation is laid. Nothing built on top of it without your word.
