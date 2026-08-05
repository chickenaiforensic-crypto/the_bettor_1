# METHODOLOGY — Football Prediction System

**Live blueprint. Version 1.1 · 2026-07-30**
Supersedes ad-hoc practice in Studies 01–19. Any future work must comply or explicitly amend this document.

**Companion document: `ENGINE_SPEC.md`** — the layer architecture, every constant, order of significance, output provenance and cold-start rebuild order. This document governs *how we work*; that one specifies *what the engine computes*. Amend together.

---

## PART I — FOUNDING PRINCIPLES

### P1. No market data. Ever.

Bookmaker odds, implied probabilities, market commentary and tipster content are **excluded from this system in all roles** — input, feature, benchmark, sanity check, or fallback.

*Rationale (user directive, confirmed by evidence):* prices are a commercial product, shaded to protect margin and partly a product of the same public narrative the system exists to see past. On the first live test the market rated Lech Poznań at 53% and the fixture finished 1–5 to Aarhus. Had the market been treated as ground truth, a correct call would have been recorded as a failure.

**Consequence:** "the market agrees/disagrees" is never evidence. The historical Gate 1 conclusion (Study 03) rested on market comparison and is therefore **suspended pending re-examination on outcomes alone**.

### P2. Results are the only ground truth

Every input derives from completed matches: teams, date, venue, goals. Nothing else enters.

### P3. The system must be able to say "I don't know"

Declining is a valid output. A refusal is preferable to a fabricated number. Unrated teams, unknown venue, insufficient matches, and out-of-scope competitions all produce explicit refusals.

### P4. Process order is fixed

Foundation → validation → superstructure. No feature is built before the layer beneath it is validated. No probability output before its signal is measured against outcomes.

### P5. Approval gate

No system is implemented without explicit user approval. Analysis and testing may proceed freely; **shipping may not**. (Violated once, Study 06 — stars shipped unapproved and later removed.)

---

## PART II — DATA LAYER

### D1. Sources

| Layer | Source | Volume | Role |
|---|---|---|---|
| Domestic | football-data.co.uk, 18 leagues 2003–2026 | 153,058 | core ratings |
| Domestic extra | Poland, Denmark | 7,049 | bridge coverage |
| European | openfootball CL/EL/Conference + qualifiers | 4,244 | cross-border bridges |
| **Total** | | **164,351 matches, 1,049 clubs, 56 countries** | |

### D2. Ingestion rules

1. Every row validated: parseable date, both teams present, teams differ, integer scores 0–20.
2. Result recomputed from goals and cross-checked against the source's own result column. Mismatch → reject.
3. Duplicates keyed on `league+season+date+home+away`.
4. **Rejections are counted and reported, never silent.** (Baseline: 591 of 153,649 = 0.38%, all benign.)
5. Structural sanity: match counts per league-season checked against known fixture lists.

### D3. Causality rule (absolute)

Every feature for a fixture uses **only matches played strictly before it**. Enforced structurally via `seq[:i]` slicing, not by date filtering after the fact.

*Failure mode this prevents:* Study 06's star cutoffs were computed once from end-of-dataset ratings, contaminating every backtest that used them. Detected in Study 08, removed in Study 14.

---

## PART III — MODEL LAYER

### M1. Core rating model (Dixon–Coles)

```
λ_home = exp( μ[league] + att[home] − def[away] + hfa[league] + home_extra[home] )
λ_away = exp( μ[league] + att[away] − def[home] )
P(i,j) = Poisson(i;λ_home) · Poisson(j;λ_away) · τ(i,j,ρ)     ρ = −0.06
```

Fitted online, one match at a time, in strict date order. New teams adapt 1.6× faster for 8 matches; time decay 0.22% per match; minimum 6 matches before a rating issues.

**Validated:** Brier 0.6112 vs 0.6476 base rate (+5.6%), calibration max error 1.66% excluding covid, stable across 4 rolling-origin splits (+6.4% to +7.0%).

### M2. Star ratings (user specification)

```
metric  = (3·won + drawn) / played
qualify = played ≥ 5
stars   = quintile rank 1–5 within league
shrink  = toward league mean, weight 6 games
hyst    = 0.05 percentile buffer at boundaries
```

Purpose: goal-difference categorisation and draw detection. Same-star fixtures draw at 28.1% vs 26.4% for different-star (+1.68pt, CIs disjoint).

**Draw correction:** per-tier table, weights 0.2/0.5/0.5 by division tier, **cap 0.02**, applied with **proportional renormalisation** (see M4).

### M3. Consensus layer (selection only)

```
HvH = home side's home GD/game − away side's home GD/game
AvA = home side's away GD/game − away side's away GD/game
CONSENSUS    = (HvH + AvA) / 2
DISAGREEMENT = |HvH − AvA|
```

Labels applied to tier A/A+ fixtures: consensus > 1.5 → STRONG (78.6% observed), > 1.0 → CONFIRMED (74.8%), < 0 → CONFLICTED. Level both lenses → DRAW-LEAN (31.8%).

**Constraint:** this layer changes no probability. Enforced by test.

### M4. Renormalisation rule

When any component adjusts one outcome's probability, the remainder is redistributed **proportionally across the other two**, never absorbed by one.

*Why this is a rule:* Study 12 found the star draw correction net-negative. The cause was mechanical — P(draw) rose and P(away) absorbed all of it while P(home) never moved. Proportional splitting converted −0.009% into **+0.047%, p<0.0001**.

### M5. Chain system (standby, analysis only)

For fixtures the core model cannot rate — cross-border ties between disconnected league graphs.

```
direct    : the two clubs have met
2nd phase : shared opponent
3rd phase : opponent-of-opponent
```

**Validated on 2,778 cross-border European matches since 2021:**

| Method | n | r with actual GD | Direction correct |
|---|---|---|---|
| 2nd phase | 171 | +0.212 | 57.7% |
| 3rd phase | 693 | **+0.274** | **62.6%** |

Base rate for comparison: 48.8% home wins.

---

## PART IV — TESTING PROTOCOL (mandatory)

Derived from Study 13, where a single statistical error invalidated six studies' conclusions.

### T1. Paired tests for model comparison

Two models scored on the same matches must be compared on **per-match differences**, never by resampling absolute scores.

```
per-match Brier variance      : sd 0.2893
per-match difference variance : sd 0.0124   ← 23× smaller
```

Unpaired bootstrap gave CI [−0.00124, +0.00157] → "not significant".
Paired test gave CI [+0.0000051, +0.0002486] → **significant, p = 0.041**.

Same data. Same models. The unpaired test was **10× too crude.**

### T2. Report the minimum detectable effect

Every result states its MDE alongside the estimate. Without it, "not significant" is uninterpretable.

*Failure this prevents:* my measured gains (0.01–0.10%) sat **4–40× below my own detection threshold** of 0.438%. Detecting them by that method would have needed 4,063,176 matches. I had 45,108.

### T3. Rolling-origin validation

Minimum 4 expanding train/test splits. A single arbitrary cut date is not acceptable.

### T4. Measure the complete output

A component tuned on one metric must be re-measured on **all** of them: home Brier, draw Brier, away Brier, full 1X2, log loss, calibration.

*Failure this prevents:* Study 11 measured draw probability alone and reported +0.066%. On full 1X2 it was −0.009%, because the gain was taken entirely from the away side.

### T5. Test the user's construction, not your own

Before judging a proposed method, run it **as specified**, on the **case in question**, and report the intermediate numbers.

*Failures this prevents:*
- Study 12 tested a crude additive nudge and reported "home-v-home is worse". Properly analysed (Study 15), the lens beat the standard comparison at every selective threshold.
- Study 17 tested the 3rd phase inside domestic leagues (r=+0.105) where it is redundant by construction, then generalised to cross-border ties. Measured there (Study 19): **r=+0.274**, 2.6× stronger.

### T6. "Not significant" ≠ "no effect"

These are distinct claims. State the first; never imply the second.

### T7. Check test-period representativeness

Flag structural breaks. The covid window (Mar 2020 – Jun 2021, 17.8% of one test set) had home wins at 41.0% vs 45.2% in training — a 4.2pt collapse in the exact quantity under study.

### T8. Data-driven gates only

A usability rule must be validated before it gates anything.

*Failure this prevents:* I built a spread-based rejection rule on the assumption that agreement between paths means reliability. Measured: spread 0–1.5 → r=+0.195; spread 3–5 → **r=+0.384**. Tight agreement was *worse*. The rule was rejecting the better chains.

---

## PART V — IMPLEMENTATION PROTOCOL

### I1. Fidelity requirement

Shipped code must reproduce the validated research code **exactly**. Verified numerically, not assumed.

*Standard achieved:* browser update engine vs Python trainer — max difference **0.00e+00** across 7 quantities.

### I2. Test coverage before ship

| Suite | Tests | Purpose |
|---|---|---|
| Core app | 28 | rating, tiers, markets, log |
| Update engine | 23 | overlay maths, persistence, fidelity |
| Sync protocol | 35 | parser + 11 adversarial attacks |
| Stars & consensus | 24 | v2 spec, draw correction, labels |
| **Blueprint compliance** | **31** | **every rule in this document, asserted** |
| **Engine spec compliance** | **26** | **every constant and layer rule in `ENGINE_SPEC.md`** |
| **Total** | **167** | |

Plus a full integrity sweep: all 9,506 possible fixtures verified for `P(H)+P(D)+P(A)=1` and market monotonicity.

**The compliance suites are the enforcement mechanism for both documents.**

`audit_compliance.js` asserts P1 (no market data in executable code), P3 (refusal paths), M2 (star constants), M3 (consensus alters no probability), M4 (proportional split, verified numerically), I3 (BTTS withheld), I4 (venue gate), I5 (no push outcome), I6 (no network).

`audit_engine.js` asserts every engine constant (ρ, LR, DECAY, HFA_LR, shrink k, GMU), the **def sign convention**, grid normalisation, the two-grid design, star monotonicity, the 0.02 cap, tier cuts, output provenance, and layer ordering.

Run both after any change.

### I3. Market gating

Each market ships only at its measured calibration error:

| Market | Max error | Status |
|---|---|---|
| 1X2, DC, DNB, O1.5, O2.5 | 1.6–2.7% | ship |
| Home −1, O3.5 | 3.0–3.3% | ship with caution flag |
| **BTTS** | **6.0%** | **withheld** |

### I4. Venue integrity (critical)

Home/away reversal is a live operational hazard — feeds and AI parsers flip sides, some books flip mid-match.

```
63.8% of fixtures — rating gap > 15pt, a flip is detectable
36.2% of fixtures — near-even, a flip is SILENT and undetectable
```

**Therefore the control is procedural, not statistical:**
1. Never trust a parsed venue.
2. Hard error if the stated home team has never hosted in that league.
3. Mandatory tick-box confirming venue against an official fixture list.
4. **Save button disabled until confirmed.**
5. Venue locked at entry; never re-parse a rated fixture.

### I5. Scoring rule

**A draw is a loss for a home-win call.** Never a push, never excluded from the denominator.

*Failure this prevents:* the original app scored draws as pushes and excluded them from hit rate — inflating apparent accuracy by roughly a third.

### I6. No network dependency

The app makes zero network calls (verified: `fetch` 0, `XMLHttpRequest` 0, `http://` 0, `https://` 0). Ratings are embedded; updates arrive by paste through a validated sync protocol with 11 adversarial checks.

---

## PART VI — CURRENT SYSTEM STATE

**Pitch Rating v2.0**, built 2026-07-30. 18 leagues, 414 rated teams, 342 current records.

| Component | Status | Evidence |
|---|---|---|
| Dixon–Coles core | shipped | +5.6% Brier, calibration 1.66% |
| Star draw correction | shipped | +0.047% full 1X2, p<0.0001, n=59,615 |
| Consensus layer | shipped | 73.0% → 78.6% on top-10% picks |
| Markets (5) | shipped | ≤2.7% calibration error |
| Sync protocol | shipped | 35 tests, 11 attacks blocked |
| Flip guard | shipped | procedural, 3 layers |
| Chain system | standby | r=+0.274, n=693 |

**Live results log: 1 case.** Lech Poznań 1–5 AGF Aarhus — chain called AGF at 58.1%, correct; direction right, magnitude understated.

---

## PART VII — OPEN ITEMS

| # | Item | Origin |
|---|---|---|
| 1 | Chain usability gate rebuilt from evidence (spread rule disproven) | Study 19 |
| 2 | Chain path discovery too narrow — found 1 path where manual search found 2 | Study 19 |
| 3 | Gate 1 conclusion suspended — rested on market comparison, needs outcome-only re-test | P1 |
| 4 | Competition field (domestic / cup / European / neutral venue) — approved, not built | Study 17 |
| 5 | Unified European ratings — proposed, not approved | Study 17 |
| 6 | Injuries / lineups / xG — deferred by user | Step 4 |

---

## PART VIII — ERROR REGISTER

Kept so the same mistakes are not repeated.

| # | Error | Consequence | Fix |
|---|---|---|---|
| E1 | Unpaired test on paired data | 6 studies wrongly concluded | T1 |
| E2 | Never computed noise floor | Demanded undetectable precision | T2 |
| E3 | Measured component in isolation | Star system wrongly rejected | T4 |
| E4 | Tested own construction, not user's | Home-v-home wrongly dismissed | T5 |
| E5 | Wrong setting for 3rd-phase test | Understated signal 2.6× | T5 |
| E6 | Gate built on assumption | Rejected the better chains | T8 |
| E7 | Shipped without approval | Contaminated stars went live | P5 |
| E8 | Look-ahead in star cutoffs | Inflated r from 0.263 to 0.367 | D3 |
| E9 | Renormalisation leak | Real gain read as neutral | M4 |

---

---

## PART IX — COMPLIANCE AUDIT RECORD

**Audit 1 — 2026-07-30, against v1.0 of this document.**

Method: assert every rule against the *running* application, not against source review or memory.

Result: **31 checks, 31 pass, 0 fail.** Full suite 141 tests passing.

Three initial failures were investigated and proved to be **defects in the audit script, not the system**:

| Reported | Reality | Resolution |
|---|---|---|
| "market terminology found (odds=4, bookmaker=3)" | All 4 in comments, a UI column header "Fair odds" (computed as 1/P from our own model), and sync-brief prose *instructing* the source not to use odds feeds | Audit now strips comments and prose; tests executable code only |
| "MODEL market fields present" | `MODEL.markets` is the **calibration-error table** (1X2: 1.7, BTTS: 6.0), not prices | Audit now asserts the field holds only numbers |
| "'push' concept present" | Every hit was `Array.push()` | Audit now matches push-as-outcome specifically |

**Lesson recorded:** the first audit run produced three false accusations against a compliant system. A test that cannot distinguish `Array.push()` from a void-bet outcome is not a test. This mirrors error E1 — the failure was in the instrument, not the subject. **Audit scripts are themselves subject to T5: verify the finding before reporting it.**

**Audit 2 — 2026-07-30, engine specification.**

`ENGINE_SPEC.md` written by extracting the pipeline from the running code, not from memory. 26 assertions, **26 pass**.

One architectural property was discovered during extraction and had never been documented: **the engine produces two families of output.** 1X2, tier, points, double-chance and DNB use star-corrected probabilities; over/under, handicap and expected scoreline use the *uncorrected* grid. This is correct — the star correction is a draw-rate refinement, and propagating it into goals markets would corrupt their separately-validated calibration (O2.5 at ±2.7%).

Verified safe across all 9,506 fixtures: likeliest scoreline contradicts the 1X2 lean in **0 cases**, DNB inconsistency **0**, over/under non-monotonicity **0**. Now documented in `ENGINE_SPEC.md` Part G and asserted by test.

Numerically verified during audit, not merely asserted:
- Proportional renormalisation: `dH=+0.00603, dD=−0.00891, dA=+0.00288` — both H and A absorb the change, confirming M4 is live and E9 is fixed.
- 9,506 fixtures: probabilities sum to 1, over/under monotone throughout.

---

*This document is live. Amend it when evidence requires — and record the amendment.*
