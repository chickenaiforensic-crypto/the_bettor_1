# Study 05 — The Pitch Rating System v1

**Date:** 2026-07-29
**Built from:** 153,058 match results · 18 leagues · 23 seasons.
**Bookmaker data used: none.** No odds, no implied probabilities, no market benchmark anywhere in the model, its fitting, or its validation.
**Deliverable:** `pitch_ratings_v1.json` — 414 teams, 18 leagues, portable to the app.

---

## 0. On avoiding the bookmakers

You're right on the substance, and I want to separate two things I'd previously run together.

**Where I agree completely:** a rating system whose inputs come from a bookmaker is a system that can be moved by that bookmaker. Prices are a *product*, priced to protect a margin, and they can be shaded, baited, or restricted. Building on them means your ratings inherit someone else's commercial incentives. Everything below is built purely from what happened on the pitch — goals, results, venues, dates. It cannot be manipulated by a price feed because it never reads one.

**One thing I'd keep, in a limited role.** In Gate 1 and Study 04, odds were used as a *measuring stick*, never as an input. That's how we discovered the xMargin system was an artefact. If we drop them entirely we lose the ability to detect self-deception — the exact failure that produced the 86% claim. My suggestion: **odds never enter the model, but stay available as an occasional external audit.** You decide when to look. Nothing below depends on them.

---

## 1. Your venue-experience hypothesis, tested

You proposed awarding points for pitch familiarity: *if a team has played here 33 times, how much extra edge?* I tested it directly.

### Raw look — the hypothesis appears to hold

| Away team's prior visits to this ground | n | Home W | Draw | Away W | Away PPG |
|---|---|---|---|---|---|
| 0 | 28,692 | 44.9% | 27.7% | 27.4% | 1.10 |
| 1 | 22,275 | 44.9% | 27.3% | 27.8% | 1.11 |
| 2 | 18,137 | 44.6% | 27.7% | 27.7% | 1.11 |
| 3–4 | 27,103 | 43.9% | 27.2% | 28.9% | 1.14 |
| 5–7 | 25,567 | 44.6% | 26.7% | 28.7% | 1.13 |
| 8–11 | 17,284 | 44.8% | 25.6% | 29.6% | 1.14 |
| 12–17 | 10,415 | 43.9% | 24.8% | **31.4%** | 1.19 |
| 18+ | 3,585 | 45.7% | 22.8% | **31.5%** | 1.17 |

Away win rate climbs 27.4% → 31.5%. Looks like a real familiarity effect.

### Controlled — it mostly disappears

The confound: teams that have visited a ground 18 times are *long-established top-division sides*. Newly promoted teams have zero visits. Visit count is a proxy for club quality. Holding the away team's current form fixed:

| Away team form | Visits 0–1 | Visits 2–5 | Visits 6+ |
|---|---|---|---|
| Weak (PPG < 1.0) | 20.3% | 20.3% | 20.7% |
| Mid (PPG 1.0–1.5) | 24.6% | 25.1% | 24.6% |
| Strong (PPG 1.5+) | 36.2% | 37.1% | **38.5%** |

For weak and mid-table sides: **nothing**. Flat to within a fraction of a point.

For strong sides there is a residual **+2.3pt** (36.2% → 38.5%, CIs don't overlap). Small but real.

### The cleanest test

Fixing the *pair* of teams and comparing their early meetings to their later ones:

| | n | Away win | Away PPG |
|---|---|---|---|
| Visits 0–1 | 13,848 | 26.7% | 1.07 |
| Visits 6+ | 45,132 | 29.9% | 1.15 |

+3.2pt. Some of this is still survivorship — pairs that meet 8+ times are both durable clubs.

**Verdict: your instinct is directionally right but the effect is worth ~2–3 points of away win probability, not the large edge the raw table suggests.** I did *not* hand it a fixed point value. Instead the model learns venue effects per team from results, which captures the same thing without the confound. This is exactly the trap that produced the 86% claim — a real-looking pattern that is mostly something else.

**Home tenure** (§C in the script) showed 41.4% → 45.4% across 0 to 200+ prior home matches. Same story: mostly survivorship. Teams that stay in a division for 200 matches are good teams.

---

## 2. The rating system

A Dixon–Coles style model, fitted online, one match at a time, in strict date order.

```
λ_home = exp( μ[league] + att[home] − def[away] + hfa[league] + home_extra[home] )
λ_away = exp( μ[league] + att[away] − def[home] )

P(score i-j) = Poisson(i; λ_home) · Poisson(j; λ_away) · τ(i,j,ρ)     ρ = −0.06
```

**Parameters, all learned from results:**

| Parameter | Meaning |
|---|---|
| `att[team]` | attacking strength |
| `def[team]` | defensive strength |
| `μ[league]` | league scoring baseline |
| `hfa[league]` | **league home advantage, measured not assumed** |
| `home_extra[team]` | that team's own home effect beyond its league's |
| `ρ = −0.06` | Dixon–Coles low-score correction (fixes 0-0/1-1 under-prediction) |

**Design choices that matter:**

- **Strictly causal.** Every prediction uses only matches already played. A fixture's own result updates the ratings *after* it is predicted. Look-ahead is structurally impossible, not filtered out.
- **New teams adapt 1.6× faster** for their first 8 matches — promoted sides get to their true level quickly instead of dragging a stale prior.
- **Time decay** (0.22% per match) shrinks ratings toward the mean, so form fades naturally rather than persisting from three seasons ago.
- **Minimum 6 matches** for both teams before a rating is issued.

---

## 3. Calibration — the part that makes points meaningful

A rating scale is only usable if the number means what it says. Across all 150,360 predictions:

| Model says home wins | n | Predicted | **Actual** | Error |
|---|---|---|---|---|
| 0–15% | 2,819 | 11.2% | 10.7% | −0.5% |
| 15–25% | 9,070 | 20.9% | 21.8% | +0.9% |
| 25–35% | 25,655 | 30.8% | 32.4% | +1.7% |
| 35–45% | 44,718 | 40.2% | 40.8% | +0.6% |
| 45–55% | 37,527 | 49.6% | 48.7% | −0.9% |
| 55–65% | 18,286 | 59.3% | 58.7% | −0.6% |
| 65–75% | 7,721 | 69.4% | 70.1% | +0.7% |
| 75–85% | 3,476 | 79.3% | 80.2% | +0.9% |
| 85%+ | 1,088 | 88.7% | 87.4% | −1.3% |

**Maximum error across every band: 1.7 percentage points.**

When this system says 70%, the team wins 70.1% of the time. That is what makes a points scale trustworthy — and it's the property the original app never had.

**Draws are calibrated too** — the thing the old tool structurally could not do:

| Predicted draw | n | Predicted | Actual | Error |
|---|---|---|---|---|
| 15–22% | 15,943 | 19.5% | 20.0% | +0.5% |
| 22–25% | 25,118 | 23.7% | 24.9% | +1.2% |
| 25–27.5% | 38,524 | 26.3% | 27.6% | +1.3% |
| 27.5–30% | 39,109 | 28.7% | 29.1% | +0.4% |
| 30%+ | 27,650 | 31.8% | 30.3% | −1.4% |

Because the model produces a full scoreline grid, draw probability comes out natively. No more 0.26 constant, no more `DRAW_LIKELY` tier that mathematically can never fire.

---

## 4. The home-match tier system

Tiers assigned purely from model probability, with the **measured** outcome of every tier:

| Tier | Points | n | Model P | **Actual win** | Draw | Loss | PPG |
|---|---|---|---|---|---|---|---|
| **A+ Fortress** | 70–100 | 7,718 | 77.8% | **78.5%** | 14.1% | 7.4% | 2.50 |
| **A Strong** | 60–69 | 11,799 | 64.2% | **64.2%** | 21.6% | 14.2% | 2.14 |
| **B Lean** | 52–59 | 20,335 | 55.6% | **54.7%** | 26.0% | 19.3% | 1.90 |
| **C Marginal** | 45–51 | 28,246 | 48.3% | **47.5%** | 28.3% | 24.2% | 1.71 |
| **D Coin-flip** | 35–44 | 44,718 | 40.2% | **40.8%** | 29.9% | 29.3% | 1.52 |
| **E Avoid** | 0–34 | 37,544 | 26.9% | **28.2%** | 26.8% | 45.0% | 1.11 |

The 100-point scale validates in every 10-point bucket:

| Points | n | Actual home win | Reliable? |
|---|---|---|---|
| 20–29 | 15,576 | 27.0% | ✅ |
| 30–39 | 37,093 | 36.8% | ✅ |
| 40–49 | 44,783 | 44.7% | ✅ |
| 50–59 | 27,258 | 53.6% | ✅ |
| 60–69 | 11,799 | 64.2% | ✅ |
| 70–79 | 5,228 | 75.7% | ✅ |
| 80–89 | 2,190 | 83.2% | ✅ |

**A+ Fortress is the tier you asked to be able to raise on home matches: 78.5% win, 7.4% loss, 2.50 PPG, and it fires on ~5% of fixtures.**

---

## 5. Measured home advantage by league

Learned from results, not assumed. This replaces the app's single hard-coded constant:

| League | Goal multiplier | | League | Goal multiplier |
|---|---|---|---|---|
| Spain Segunda | **1.36×** | | Portugal | 1.27× |
| Greece | 1.34× | | Scotland Prem | 1.26× |
| Spain La Liga | 1.33× | | Germany Bundesliga | 1.26× |
| Netherlands | 1.30× | | Germany 2.Bundesliga | 1.26× |
| Italy Serie B | 1.29× | | England Championship | 1.25× |
| France Ligue 2 | 1.28× | | England Premier League | 1.24× |
| Turkey | 1.28× | | England League One | 1.23× |
| Belgium | 1.27× | | Italy Serie A | 1.22× |
| France Ligue 1 | 1.27× | | England League Two | **1.20×** |

Spanish and Greek home advantage is meaningfully larger than English or Italian. A single global constant — as the old app used — is wrong for every league simultaneously.

Per-team home effects exist but are **small**: Bayern, Atlético, Man City, Liverpool and Dortmund top the list at only +0.006 log-goals. Real fortress effects are much weaker than folklore suggests, and the model correctly declines to inflate them.

---

## 6. Performance

| Metric | Baseline | Model | Gain |
|---|---|---|---|
| Brier (all 150,360) | 0.6476 | **0.6112** | **+5.6%** |
| Log loss | 1.0712 | **1.0193** | +4.8% |
| Brier (2018/19 →) | 0.6515 | **0.6085** | +6.6% |

Season-by-season, most recent four — each predicted before it happened:

| Season | n | Brier | vs base | Predicted home | Actual | Error |
|---|---|---|---|---|---|---|
| 2022/23 | 6,708 | 0.6005 | +7.3% | 43.7% | 44.4% | +0.7% |
| 2023/24 | 6,647 | 0.6027 | +7.4% | 44.3% | 43.4% | −0.8% |
| 2024/25 | 6,536 | 0.6076 | +6.6% | 44.1% | 43.7% | −0.4% |
| 2025/26 | 6,530 | 0.6098 | +6.4% | 43.9% | 43.3% | −0.6% |

**Stable across four consecutive unseen seasons, error under 1pt every time.** No decay — the opposite of what we saw with the xMargin threshold.

---

## 7. The flip problem — your 1xbet warning

This is a serious operational hazard and you were right to raise it. If a feed or an AI parse reverses home and away, the model rates the wrong side at home and the output is confidently wrong.

**How detectable is it?** Of 20,000 fixtures:

- **63.8%** have a rating gap wide enough (|P(H) − P(A)| > 15pt) that a flip produces an obviously implausible number → auto-flaggable.
- **36.2%** are near-even, where a flip is **completely silent**. The model cannot detect it, ever.

**So the rule has to be procedural, not statistical:**

1. **Never trust a parsed venue.** Confirm the home team against an official fixture list or league calendar before rating.
2. **Auto-flag** any fixture where reversing the order changes P(home) by more than 15pt *and* the stated home side is the weaker one — that's the signature of a flip.
3. **Ground history check** — has the stated home team ever hosted in this league? A team appearing at home for the first time in 23 seasons is a parse error.
4. **Lock venue at entry.** Once confirmed, store it immutably in the log so a mid-match re-parse can't silently reverse it — which is exactly what you described happening in the baseball app.
5. **Never re-parse a fixture already rated.** Re-parsing is how the flip re-enters.

---

## 8. Worked examples

Real 2025/26 fixtures, rated before kickoff:

| Fixture | Points | Tier | H / D / A | Expected goals | Actual |
|---|---|---|---|---|---|
| Antwerp v St. Gilloise | 20 | E | 20% / 26% / 54% | 0.88–1.62 | D |
| Dender v Cercle Brugge | 45 | C | 45% / 24% / 31% | 1.80–1.45 | D |
| Waregem v Mechelen | 31 | E | 31% / 21% / 48% | 1.76–2.19 | D |
| **Anderlecht v Westerlo** | **63** | **A** | 63% / 20% / 17% | 2.24–1.08 | **H** ✅ |
| **Club Brugge v Genk** | **60** | **B** | 60% / 22% / 18% | 2.01–1.02 | **H** ✅ |
| Oud-Heverlee Leuven v Charleroi | 30 | E | 30% / 30% / 40% | 1.03–1.24 | D |

---

## 9. Deliverable

**`pitch_ratings_v1.json`** — 38 KB, 414 active teams, 18 leagues.

```json
{
  "version": "pitch-rating-v1",
  "source": "match results only (153,058 matches). NO bookmaker data.",
  "formula": "lambda_home=exp(mu[lg]+att[H]-dfn[A]+hfa[lg]+home_extra[H]); ...",
  "dixon_coles_rho": -0.06,
  "leagues": { "E0": {"mu": ..., "hfa": 0.215}, ... },
  "teams":   { "E0": {"Liverpool": {"att":..., "dfn":..., "home_extra":...}}, ... },
  "tiers":   [ {"name":"A+ Fortress","min":0.70,"measured_win":0.785,"n":7718}, ... ],
  "calibration": {"max_error_pct": 1.7, "brier": 0.6112, "improvement_pct": 5.6}
}
```

Self-contained: the app can compute any fixture's rating from this file with ~30 lines of arithmetic and no network call.

---

## 10. What this fixes from audit 01

| Audit 01 finding | Status |
|---|---|
| 🔴 F1 no home/away concept | **Fixed** — home advantage is a first-class per-league, per-team parameter |
| 🔴 F2 football treated as bracket tournament | **Obsolete** — no questionnaire, ratings come from results |
| 🔴 F3 confidence inflated in leagues | **Fixed** — confidence is calibrated probability, validated to 1.7% |
| 🔴 F4 draws unpredictable / scored as push | **Fixed** — draw probability native and calibrated |
| 🟠 F5 draw estimate ramps to 0% | **Fixed** — from the scoreline grid, never hits zero |
| 🟠 F8 "top plays" static text | **Fixable** — the grid gives real over/under and handicap numbers |
| 🟠 F9 no calibration instrumentation | **Fixed** — Brier, log loss, reliability tables are the primary metrics |

---

## 11. Honest limitations

1. **This predicts outcomes, not value.** It's calibrated to reality, which is the right goal — but "well-calibrated" and "profitable" are different claims and I'm only making the first.
2. **+5.6% Brier over base rate is solid, not spectacular.** A top-tier commercial model with injury data, lineups and xG would beat it.
3. **No injuries, suspensions, lineups, fixture congestion, or European involvement.** Results only. These are the obvious next inputs.
4. **Ratings are current as of the export date** and need periodic refresh — stale ratings decay.
5. **The 2–3pt venue-familiarity residual is not separately modelled.** It's small and partly absorbed into team ratings already.
6. **18 leagues, all European.** Untested elsewhere.

---

## 12. Next steps

1. **Wire `pitch_ratings_v1.json` into the app** — replace the 5-subscale questionnaire with computed ratings. The Step 2/3 LLM research flow becomes optional colour rather than the engine.
2. **Add a fixture-list verification step** at input, per §7. This is the highest-priority app change given your 1xbet experience.
3. **Extend the tier system to other markets** using the scoreline grid — over/under, both-teams-to-score, correct score, handicaps. All are already computable and would replace the static "top plays."
4. **Add lineup/injury data** as the next real accuracy gain.
5. **Refresh ratings weekly** during the season.

---

## Files

| File | Purpose |
|---|---|
| `data/venue_exp.py` | venue-familiarity hypothesis test |
| `data/rating.py` | model fitting, walk-forward |
| `data/calib.py` | calibration tables, tier system |
| `data/holdout_flip.py` | held-out seasons, flip detector |
| `data/export_model.py` | JSON export |
| `pitch_ratings_v1.json` | **the deliverable** |
