# Audit 02 — `FOOTBALL_HOME_SYSTEM.md` v1.0

**Audited:** 2026-07-29 · **Method:** every figure in the document recomputed from scratch (`audit_stats.py`, `audit_poisson.py`).
**Verdict:** the document is honest, well-structured, and self-critical — and it contains **one result that is very probably impossible**. That result has to be resolved before anything else is worth doing.

---

## 0. Executive summary

| | |
|---|---|
| Is the write-up disciplined? | **Yes.** Better than most. Held-out league, no re-tuning, rejected-attempts log, stated CI, admits normScore is redundant. |
| Do the numbers reproduce? | **Mostly yes.** Two arithmetic slips, both minor. |
| Is the 86% trustworthy? | **No — not yet.** One statistic inside it is ~651:1 against. |
| Is the true out-of-sample sample n=36? | **No. n=11.** |
| Is there a demonstrated betting edge? | **Unknown — no odds appear anywhere in the document.** |
| Should you keep going with football? | **Yes.** But fix F1 before collecting another call. |

**The single finding that matters:** among the 36 selections, **1 draw**. For fixtures of this profile, Poisson says to expect **~8**. That is p = 0.0015. Either you have discovered something genuinely remarkable, or there is a defect in the pipeline. The second is far more likely, and it is cheap to test.

---

## 1. Verification — what reproduces

I recomputed every headline number. Credit where due:

| Doc claim | My recomputation | Status |
|---|---|---|
| 31/36 = 86% | 86.1% | ✅ |
| 95% CI 75%–97% | Wilson [71.3%, 93.9%]; Clopper-Pearson [70.5%, 95.3%] | ⚠️ **optimistic** — true lower bound is ~71%, not 75% |
| "True rate 75% → 31/36-or-better ~8% of the time" | 8.35% | ✅ exactly right |
| Coverage 36/179 = 20% | 20.1% | ✅ |
| Finland band table totals to 53% baseline | 33/62 = 53.2% | ✅ |
| Outcome split 31W / 1D / 4L | sums to 36 ✅; failure table lists 5 misses across the right leagues ✅ | ✅ internally consistent |
| "0.8 → 1.0 jump is sharp and consistent" | Fisher exact, ≥1.0 vs 0.8–1.0 band: **p = 0.0028**, OR 7.75 | ✅ genuinely sharp |

**The self-criticism in §9 and the rejected-attempts log in §10 are the most valuable parts of the document.** Recording that DRAW_LIKELY was mathematically unreachable, and that the support system correlated r=+0.79 with normScore, is exactly the discipline that prevents re-treading dead ends. Keep that section growing.

---

## 2. Findings

🔴 = must resolve before more data collection · 🟠 = materially changes the conclusion · 🟡 = cleanup

---

### 🔴 F1 — The draw rate is not physically plausible

This is the finding. Everything else is secondary.

Model these fixtures as independent Poisson with Nordic-typical total goals (~2.8) split to match the selection criterion:

| xMargin | λ home | λ away | P(home) | **P(draw)** | P(away) | fair odds |
|---|---|---|---|---|---|---|
| 0.6 | 1.70 | 1.10 | 51.4% | 24.0% | 24.6% | 1.95 |
| 0.8 | 1.80 | 1.00 | 56.1% | 23.1% | 20.8% | 1.78 |
| **1.0** | 1.90 | 0.90 | **60.8%** | **21.9%** | 17.3% | 1.64 |
| 1.5 | 2.15 | 0.65 | 72.1% | 18.1% | 9.9% | 1.39 |
| 2.0 | 2.40 | 0.40 | 82.0% | 13.5% | 4.6% | 1.22 |

Against that:

```
Observed:  1 draw in 36
Expected:  ~7.9 draws  (at the 21.9% rate for xMargin = 1.0)
P(≤1 draw | n=36, p=0.219) = 0.00154        ≈ 651 : 1 against
```

Even granting the most favourable assumption — that every selection behaved like a **1.5** xMargin blowout candidate (18.1% draw rate) — you get p = 0.0069, still 145:1 against.

For 1-in-36 to be merely unlucky rather than anomalous, the true draw rate of these fixtures would have to be **≤10%**. No football selection method achieves that. The structural floor for heavy favourites is 13–18%, because the draw is an absorbing state that even dominant sides fall into.

The document treats this as its "central achievement" (§7). I'd treat it as the **primary alarm**. Three candidate explanations, in order of likelihood:

1. **Look-ahead leakage.** Something in the feature pipeline sees post-match information. The `xMargin` formula reads `date < fixture date`, but if the underlying match table was assembled per-season and the "prior matches" filter is applied to an already-filtered frame, or if a team's own fixture is included in its own mean, decisive matches get selected by construction. This would inflate hit rate *and* suppress draws simultaneously — which is exactly the joint signature observed.
2. **Selection/coding error in grading.** E.g. draws silently dropped, or `winnerSide == "draw"` mapped to a non-outcome and excluded from the 36. Note this is **precisely the bug I found in the app** (F4 in audit 01: draws scored as `push` and excluded from the hit-rate denominator). If the backtest shares any grading code with the app, this is the first place to look. A dropped-draw bug would convert a true 31W/8D/4L (72%) into a reported 31/36 (86%) — and 72% is almost exactly what Poisson predicts.
3. **It's real.** Possible, but it needs to survive a pre-registered test before being believed.

**Explanation 2 deserves emphasis: it would reproduce the entire headline result, including the draw anomaly, exactly.** 31 wins / 8 draws / 4 losses = 31/43 = 72%, and 72% sits right on the Poisson expectation of ~76% for this fixture profile. That is a disturbingly clean fit.

**Test (do this first, costs an hour):** take the 36 fired fixtures, pull their final scores from an independent source (football-data.co.uk has all three leagues, free CSV), and recount W/D/L by hand. If the draw count is 6–9, the system's true rate is ~72–75% and the rest of this audit's plan applies. If it really is 1, escalate to a full leakage audit of `system_v3.py`.

---

### 🔴 F2 — True out-of-sample n is 11, not 36

The document is careful about this and then quietly forgets it in the headline.

| League | Role | n | Hit |
|---|---|---|---|
| Allsvenskan | threshold **chosen here** — in-sample | 13 | 85% |
| Eliteserien | "test 1" — but §10 shows 7 variants were tried and rejected across development | 12 | 92% |
| Veikkausliiga | **"never touched during development"** | 11 | 82% |

Only Finland is clean. Pooling in-sample with out-of-sample and quoting one CI overstates the evidence.

```
Finland alone:  9/11 = 81.8%
  Wilson 95% CI          [52.3%, 94.9%]
  Clopper-Pearson 95% CI [48.2%, 97.7%]
  vs Finland's 53% baseline: one-sided p = 0.0501
```

**p = 0.05 exactly, on the single genuinely held-out league.** That is the honest headline. It is suggestive. It is not established. The lower bound admits a coin-flip-plus-a-bit.

Norway's status as a clean test is also weaker than it looks: §10 records seven rejected attempts. If Norway was the evaluation set for any of them, it has been partially consumed as a validation set — the garden-of-forking-paths problem. Only Finland is untouched.

---

### 🔴 F3 — Accuracy is being compared against the wrong baseline

The document claims **+29 to +41 percentage points of lift** by comparing 86% against "back every home team" (44–55%).

That is not the relevant comparison. You are not choosing between *this system* and *backing every home team at random*. You are choosing between *this system* and *the price the market offers on these specific fixtures*.

The correct baseline is the structural rate for fixtures of this profile:

| Comparison | Lift |
|---|---|
| vs unconditional home baseline (doc's framing) | +31 to +41 pt |
| **vs Poisson expectation for xMargin ≥ 1.0 fixtures (~76%)** | **+10 pt** |
| vs market price for such fixtures (typically 1.25–1.45 → 69–80% implied) | **+6 to +17 pt, and possibly zero** |

Most of the advertised lift is simply the tautology that *fixtures with a large expected goal margin are won by the home side more often than average fixtures are*. The market already knows this and prices it. The genuine question — is the market's price for these fixtures wrong? — is not addressed anywhere in the document.

---

### 🔴 F4 — No odds appear anywhere in the document

There is not a single price in 305 lines. Accuracy without prices cannot establish profitability.

```
Break-even decimal odds:
  at 86.1% (point estimate) →  1.161
  at 78%   (doc's own plan) →  1.282
  at 75%   (CI lower bound) →  1.333
```

EV per unit staked, by offered price:

| Odds | Implied | EV @86% | EV @78% | EV @75% |
|---|---|---|---|---|
| 1.20 | 83.3% | +3.3% | −6.4% | −10.0% |
| 1.25 | 80.0% | +7.6% | −2.5% | −6.2% |
| **1.30** | 76.9% | +11.9% | **+1.4%** | −2.5% |
| 1.35 | 74.1% | +16.2% | +5.3% | +1.3% |
| 1.40 | 71.4% | +20.5% | +9.2% | +5.0% |

Read the 78% column — the doc's own recommended planning number. **The system is break-even at 1.30 and loses money below it.** Fixtures where a strong home side hosts a weak away side in a Nordic league routinely price at **1.20–1.35**. It is entirely possible for this system to be 86% accurate and still lose money.

**Every future logged call must record the price.** Ideally the closing price, since beating the close is the standard test of whether a selection method contains information the market lacks. Without this, no amount of additional accuracy data settles the question.

---

### 🟠 F5 — The threshold sits inside the noise band of its own estimator

`xMargin` is built from four sample means, each over as few as 3 matches (the stated minimum).

```
Per-match goals variance ≈ 1.3 (Poisson-ish)
SE of a 4-match mean     ≈ 0.57 goals
SE of xMargin (4 such terms, each weighted 0.5) ≈ 0.57 goals
95% interval on a measured xMargin of 1.0  ≈  [-0.1, +2.1]
```

Early in a season, a fixture measured at `xMargin = 1.0` could plausibly have a true value anywhere from 0 to 2. The decision boundary is not resolvable at that sample size. Two consequences:

- The sharp 0.8→1.0 cliff may partly be an artefact of *which fixtures have enough data to be measured precisely* rather than of the threshold itself.
- Raising the minimum-matches requirement from 3 to 6 should, if the signal is real, **increase** hit rate. That is a cheap, powerful falsification test — see plan step 3.

---

### 🟠 F6 — No opponent-strength adjustment

`H_scored_home` is a raw mean. A side whose first five home fixtures happened to be against the bottom five gets an inflated xMargin with no correction, and the system cannot tell that apart from genuine quality.

The measured correlation of **r = +0.371** with actual match margin is respectable, and the comparison against normScore's +0.015 is a genuinely valuable finding — venue-splitting is clearly the right instinct. But a properly fitted **Dixon–Coles** or bivariate-Poisson model, which estimates attack and defence ratings *net of schedule*, typically reaches r = 0.45–0.55 on the same task. There is meaningful headroom, and it comes from a well-documented standard method rather than more threshold-hunting.

---

### 🟠 F7 — The bands are not monotonic

Real signal should show dose-response: more xMargin → more home wins. Finland's held-out table doesn't:

| Band | n | Hit | 95% CI |
|---|---|---|---|
| −1.0 to −0.3 | 8 | 38% | [0.14, 0.69] |
| −0.3 to 0.0 | 7 | 29% | [0.08, 0.64] |
| 0.0 to +0.3 | 16 | 38% | [0.18, 0.61] |
| **+0.3 to +0.6** | 13 | **77%** | [0.50, 0.92] |
| **+0.6 to +1.0** | 7 | **43%** | [0.16, 0.75] |
| ≥ +1.0 | 11 | 82% | [0.52, 0.95] |

The 0.3–0.6 band outperforms the 0.6–1.0 band by 34 points, which should be impossible under a clean monotone relationship. Fisher exact gives p = 0.17, so it's *consistent with noise* — but that cuts both ways: at these sample sizes the band structure carries almost no information, and the same noise that produced this inversion could equally have produced the ≥1.0 cell.

Pooled across all three leagues the implied bands are similarly unstable:

| Implied band | n | Hit | 95% CI |
|---|---|---|---|
| 0.6–0.8 | 16 | 56% | [0.33, 0.77] |
| 0.8–1.0 | 18 | 44% | [0.25, 0.66] |
| 1.0–1.2 | 10 | 80% | [0.49, 0.94] |
| ≥1.2 | 26 | 88% | [0.71, 0.96] |

A step function that jumps from 44% to 80% across a boundary of 0.2 goals — a boundary whose measurement error is ±0.57 goals (F5) — is not a plausible physical relationship. **A real effect would be a smooth curve.** This pattern is what a threshold fitted to noise looks like.

---

### 🟠 F8 — The accumulator section is EV-negative and should be deleted

§8 presents compounding tables that make 4- and 5-leg accumulators look attractive. With realistic pricing they are not:

```
4-leg acca, each leg at true p, priced at fair odds minus 5% margin per leg:

  p = 0.861 → hit 55.0%, odds 1.48, EV = −18.5%
  p = 0.780 → hit 37.0%, odds 2.20, EV = −18.5%
```

The vig compounds multiplicatively. Four legs at 5% overround each costs ~18.5% of stake regardless of how good the legs are. **A positive-EV single becomes a negative-EV accumulator.** Correlation between same-weekend legs (which the doc correctly flags) makes it worse in variance terms but is second-order next to the vig.

If the selections are genuinely +EV, the correct action is flat singles. The accumulator table converts a possibly-profitable system into a certainly-unprofitable one, and it is the most financially dangerous page in the document.

---

### 🟡 F9 — Two arithmetic slips

1. **§5 cell table doesn't reconcile.** 34 + 37 + 105 = **176**, not 179. The missing fourth cell (`normScore < 0.30 AND xMargin ≥ 1.0`) must hold 2 fixtures (since 36 − 34 = 2), giving 178. **One fixture is still unaccounted for.**
2. **§1 CI is slightly tight.** Stated 75%–97%; Wilson gives 71.3%–93.9%, Clopper-Pearson 70.5%–95.3%. The doc's interval appears to use a normal approximation, which is unreliable near p=0.86 at n=36. Minor, but it makes the "plan against 78%" advice less conservative than intended — **plan against 71%.**

---

### 🟡 F10 — normScore should be deleted, not retained

§5 states plainly: *"xMargin ≥ 1.0 alone, ignoring normScore entirely, scores 31/36 = 86%. normScore adds essentially nothing."*

My recomputation shows it is worse than nothing: the AND rule scores **29/34 (85.3%)** versus xMargin alone at **31/36 (86.1%)**. The normScore filter removed 2 fixtures and **both were wins**. It is a small sample, so this isn't proof of harm — but there is zero evidence of benefit, and every retained parameter is a degree of freedom that inflates overfitting risk and complicates the audit trail.

Delete it. The `leagueHFA` measurement inside it is worth keeping separately — measuring home advantage per league rather than hard-coding it is a genuine improvement over the app's approach, and §11's finding that MLB home advantage measured 0.0 is a nice validation of that instinct.

---

### 🟡 F11 — Nordic-only, and mid-season-only

The doc flags the Nordic limitation (§9.2). It does not flag the seasonal one. The 3-prior-home / 3-prior-away requirement means no fixture before ~matchweek 7 is ever graded, so every call comes from mid-to-late season, when tables have separated and end-of-season motivation effects (safe mid-table sides, already-relegated sides) are strongest. That is a real and exploitable effect — but it is a *calendar* effect, not evidence the method generalises. Expect degradation in the opening third of any season.

---

## 3. What I think is actually true

Stripping out the issues above, my best estimate:

| Claim | Doc | My estimate |
|---|---|---|
| Hit rate on fired calls | 86% | **72–78%** (once draws are recounted per F1) |
| Clean out-of-sample n | 36 | **11** |
| Lift vs relevant baseline | +29 to +41 pt | **0 to +10 pt** |
| Demonstrated profitability | implied | **Unknown — no prices recorded** |
| Is venue-splitting the right instinct? | yes | **Yes — this is the real find** |

The genuine, defensible discovery in this document is **§3: venue-split goal rates correlate with match margin at r = +0.371 where season aggregates manage +0.015.** That is a large, believable, mechanistically sensible effect, and it is the foundation worth building on. The 86% headline is probably an artefact sitting on top of it.

---

## 4. Plan — backtest football to settled

You want one sport taken to high accuracy before moving on. Agreed. Here is the sequence. **Steps 1–3 are gates: do not proceed past a failed gate.**

### Gate 1 — Recount the 36 (1 hour)
Pull final scores for all 36 fired fixtures from an independent source (football-data.co.uk CSVs cover SWE/NOR/FIN, free). Recount W/D/L by hand.

- Draw count 6–9 → grading bug confirmed. True rate ~72–75%. Fix the grader, restate the headline, proceed to Gate 2.
- Draw count still 1 → **stop and audit `system_v3.py` for look-ahead leakage** before anything else. Specifically: confirm the prior-match filter excludes the fixture itself, and that team means are computed on a frame filtered by date *at the row level*, not per-season.

**Nothing downstream is worth doing until this is settled.** Every subsequent number inherits this error if it exists.

### Gate 2 — Attach prices retrospectively (2–3 hours)
football-data.co.uk CSVs include closing odds (B365, Pinnacle) for these leagues. Join them to the 36 calls and compute:

- Mean closing price on fired calls
- Realised ROI at flat stakes
- **Closing-line value:** how often the selection's price shortened from open to close

CLV is the real test. A method that consistently backs teams whose price shortens has found information before the market did. A method that backs teams whose price drifts has not, regardless of hit rate. If mean closing odds < 1.30, the system is accurate but unprofitable and the objective must change (see step 6).

### Gate 3 — Two falsification tests on existing data (2 hours)
Both are cheap and both are informative whichever way they land.

1. **Raise minimum matches 3 → 6.** If signal is real, precision improves and hit rate rises. If hit rate falls, the threshold was fitting measurement noise (F5).
2. **Replace the step function with a smooth curve.** Fit `P(home win)` as logistic in continuous xMargin across all 179 fixtures. If the fitted curve is smooth and monotone, the ≥1.0 threshold is a reasonable discretisation of a real effect. If the data only supports a cliff at exactly 1.0, that's F7 confirmed — an artefact.

### Step 4 — Rebuild the feature properly
Replace raw venue-split means with a **Dixon–Coles bivariate Poisson**: attack and defence ratings per team, home-advantage term, exponential time-decay on older matches, low-score correlation correction. This is a well-established method, roughly 150 lines, and it fixes F5 and F6 at once — ratings are schedule-adjusted and pool information across all matches instead of 3-match slices.

Output should be a **full scoreline distribution**, which gives you P(home), P(draw), P(away) natively — and therefore the draw prediction the app currently cannot make, plus over/under and handicap markets that §F8 of audit 01 flagged as unbacked.

Validate by comparing r-with-margin against the current +0.371. Expect 0.45–0.55.

### Step 5 — Expand the sample honestly
Historical backtesting is far faster than forward-logging, and football-data.co.uk has ~15 years of these leagues plus the big five.

- Fit on 2015–2022, test on 2023–2026. Never look at the test years while tuning.
- Target **≥300 fired calls** in the test period.
- Report by league and by season, not pooled.

Sample-size reality:

| Calls | 95% CI at 86% | Width |
|---|---|---|
| 36 (now) | [71.3%, 93.9%] | 22.6 pt |
| 75 | [75.6%, 91.6%] | 16.0 pt |
| 150 | [79.5%, 90.7%] | 11.1 pt |
| 300 | [81.6%, 89.5%] | 7.9 pt |

To *distinguish* 86% from 75% at 80% power: **~84 calls** (≈420 fixtures at 20% coverage). To distinguish from 70%: ~43 calls. So ~85 clean calls is the real minimum for the headline to mean anything — the doc's instinct toward 300 is right but the doc's route (forward-logging four Nordic seasons) is unnecessarily slow when the history already exists.

### Step 6 — Switch the objective from accuracy to calibration
Once a Dixon–Coles model exists, "hit rate on fired calls" stops being the right metric. Measure:

- **Brier score** and reliability curve (predicted 70% should win ~70%)
- **Log loss** vs the closing line as benchmark
- **ROI and CLV** at flat stakes
- Coverage/volume as a secondary constraint

A calibrated model that says "this is 74%, the market says 71%, bet it" is worth far more than an uncalibrated filter that says 86% with no price attached.

### Step 7 — Only then, wire it into the app
The app changes from audit 01 (home/away as a first-class variable, league-aware questions, draw scored as a loss, per-tier calibration stats) should be implemented *against the finished model*, not before it. Otherwise you'll build UI twice.

**Do not touch baseball or tennis until football clears Gate 3 and reaches 300 test-period calls.** §11's recommendation to avoid baseball is well-supported — MLB home advantage measuring 0.0 and CLEAR_WIN firing twice in 185 games is a clear signal that this architecture doesn't transfer there.

---

## 5. Immediate next action

**Gate 1.** Give me the 36 fixtures — dates, teams, leagues — and I'll pull the independent scores, recount the draws, and settle F1 today. If you have `three_league.py` and the data files, send those instead and I'll re-run the pipeline against fresh score data and diff the two.

That one test determines whether we're refining an 86% system or repairing a 72% one, and every subsequent decision depends on the answer.

---

## 6. Questions

1. **Can you share the source files** (`system_v3.py`, `three_league.py`, the data modules)? A leakage audit needs the code, not just the spec.
2. **Where did the match data come from** — manually entered, scraped, or an API? Manual entry is the most common source of the kind of silent omission F1 suspects.
3. **Do you have odds for any of the 36 calls**, even a few? Even a handful anchors the profitability question immediately.
4. **What's the actual goal — profit, or accuracy?** If profit, F4 makes prices the top priority and we should reorder. If it's a modelling exercise where accuracy is the score, Gate 2 can wait.
