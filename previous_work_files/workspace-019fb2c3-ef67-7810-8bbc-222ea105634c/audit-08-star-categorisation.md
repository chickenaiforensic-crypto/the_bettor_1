# Study 08 — Audit of the Star Categorisation System

**Date:** 2026-07-30 · **Status:** analysis only, nothing implemented, awaiting your decision
**Scripts:** `data/star_audit1.py`, `star_audit2.py`, `star_audit3.py`

---

## 0. Scope correction

You've redefined the star system's job: **measure possible goal difference and improve draw detection** — not win probability. That is a different target from what I tested in Studies 06/07, and you're right that it changes the assessment. This audit examines the categorisation itself for robustness, as instructed. No changes made.

---

## 1. What I actually shipped

```
starsFor(lg, team):
    v = att[team] + dfn[team]              ← equal-weighted sum
    stars = 1 + count(cutoffs[lg] ≤ v)     ← per-league quintiles
    cutoffs frozen at build time
```

Three structural defects.

---

## 2. Defect 1 — the composite collapses two dimensions into one

Goal difference comes from an **interaction**: home attack vs away defence. A team's own `att + dfn` total can't express that. Same star, opposite profiles:

| League | Star | Attack-heavy | att−dfn | Defence-heavy | att−dfn |
|---|---|---|---|---|---|
| SP2 | 4★ | Almeria | +0.522 | Burgos | −0.536 |
| SP1 | 4★ | Sociedad | +0.276 | Getafe | −0.702 |
| B1 | 5★ | Club Brugge | +0.467 | St. Gilloise | −0.421 |
| T1 | 1★ | Ad. Demirspor | +0.377 | Bodrumspor | −0.594 |

Teams sharing a star differ by **over 1.0** in attacking/defensive balance. For a win-probability system that's tolerable. **For a goal-difference system it's the central defect** — Almeria vs Burgos should produce very different scorelines, and the stars say they're identical.

---

## 3. Defect 2 — look-ahead contamination in the cutoffs

The cutoffs were computed **once, from ratings at the end of the dataset**. Two consequences:

- **Any backtest using them is contaminated.** The 2024/25 star ratings were set using information from 2025/26.
- **They will skew over time.** As sync updates ratings, teams drift across fixed boundaries, so the 1–5 distribution won't stay quintiles.

Cutoffs also vary hugely by league (spread 0.410 to 1.027), so a 5★ in Greece is not a 5★ in England. Fine within a fixture; meaningless across leagues.

---

## 4. Defect 3 — boundary fragility

**53.9% of teams (223 of 414) sit within 0.05 of a cutoff.** A single match moves `att+dfn` by roughly that much, so more than half the league can flip category week to week.

Measured on a properly-built version: **17.3% of teams change star level between consecutive matches**, 1.3% jump two or more levels.

---

## 5. Defect 4 — it misranks real teams

Checked against the actual 2025/26 Premier League table:

| Pos | Team | Pts | GD | Stars | |
|---|---|---|---|---|---|
| 5 | Liverpool | 60 | +10 | 5★ | |
| 6 | Bournemouth | 57 | +4 | 5★ | |
| **7** | **Sunderland** | **54** | **−6** | **1★** | ❌ |
| 10 | Chelsea | 52 | +6 | 3★ | |
| **16** | **Nott'm Forest** | **44** | **−3** | **4★** | ❌ |
| 17 | Tottenham | 41 | −9 | 1★ | |

**Root cause:** `dfn` has a wider effective spread than `att` in places, so the sum is dominated by whichever component happens to be extreme. Arsenal's `dfn = 0.888` drags it to 5★; Tottenham's balanced profile scores 1★ despite similar quality.

**The composite is not a strength measure. It's an artefact of adding two differently-scaled numbers.**

---

## 6. The important finding — the *concept* works

Despite all four defects, the star gap tracks goal difference genuinely well:

| Star gap | n | Mean GD | Draw % | Home win % |
|---|---|---|---|---|
| −4 | 7,524 | −0.47 | 26.4% | 26.8% |
| −2 | 15,152 | −0.07 | 28.2% | 35.0% |
| −1 | 18,891 | +0.02 | **28.7%** | 36.5% |
| **0** | 28,548 | +0.35 | 28.2% | 44.5% |
| +1 | 18,504 | +0.66 | 26.3% | 52.0% |
| +2 | 14,617 | +0.77 | 25.1% | 55.1% |
| +4 | 6,764 | **+1.22** | **20.8%** | 65.8% |

Monotonic in goal difference across all nine levels. And **your draw hypothesis is supported**: draw rate falls from **28.7% at narrow gaps to 20.8% at gap +4** — a 7.9 point spread. Close-star matches really do draw more often.

**Correlation with actual goal difference: r = +0.367**, versus +0.378 for the continuous model. **Discretising into 5 buckets costs only 3% of the signal** — far less than I'd have guessed, and a real point in favour of the star approach.

---

## 7. Candidate constructions tested

All rebuilt properly — rolling cutoffs from prior data only, no look-ahead:

| Construction | n | r with GD | Draw separation |
|---|---|---|---|
| A — att+dfn (shipped) | 132,915 | +0.2632 | 4.5% |
| **B — goal difference per game** | 132,915 | **+0.2632** | **4.6%** |
| C — points per game | 132,915 | +0.2510 | 4.1% |
| D — venue-split GD | 128,204 | +0.2213 | 3.5% |

**Construction B (goal difference per game) is the best candidate**, and it's the natural choice: if the stars are meant to measure goal difference, rate teams on goal difference. It matches the shipped version on correlation while being far simpler, interpretable, and free of the scaling artefact that misranks Sunderland and Tottenham.

Note all four score lower here (~0.26) than the shipped version did in §6 (0.367) because these use honest rolling cutoffs — the 0.367 was inflated by look-ahead. **That gap is the measure of the contamination.**

Venue-split GD performing *worst* is worth noting: the home system already handles venue, so splitting it here just thins the sample.

---

## 8. Assessment

| Question | Answer |
|---|---|
| Is the shipped categorisation robust? | **No** — four defects, one contaminating |
| Is the star *concept* sound for goal difference? | **Yes** — monotonic, r=+0.367, only 3% below continuous |
| Does it help with draws? | **Yes** — 28.7% → 20.8% across the gap range |
| Best construction | **B: goal difference per game**, rolling quintiles |

Your instinct that stars suit goal-difference and draw work better than win probability is **supported by the data**. The concept is sound; my implementation of it is not.

---

## 9. Proposed rebuild — for your approval, not yet built

If you approve, I'd rebuild as:

1. **Rate on goal difference per game** (construction B), not `att+dfn`.
2. **Rolling cutoffs** recomputed from prior matches only — removes look-ahead and keeps quintiles honest as ratings update.
3. **Hysteresis at boundaries** — require a team to clear a threshold by a margin before changing star level, to cut the 17.3% weekly churn.
4. **Minimum 5 prior matches** before a star is assigned; show "unrated" rather than guessing.
5. **Keep it display-only** until we test it for the goal/draw system, as you've directed.

**Questions for you:**

- Approve construction B, or would you rather specify the rating basis yourself?
- Should stars stay separate from the model, or feed the draw calculation once tested?
- The shipped version is still live and contaminated — remove it now, or leave it until the rebuild is approved?
