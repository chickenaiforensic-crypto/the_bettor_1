# LIVE BLUEPRINT — Predictive Football Evidence System

**Status:** Active working specification  
**Version:** 1.0-live  
**Last updated:** 2026-07-30  
**Owner:** User + Senior Supervisor  
**Purpose:** Preserve all agreed rules, amendments, audits, refusals, and open work so the system does not regress or lose context.

---

## 1. Binding operating rules

1. Results-only evidence.
2. No bookmaker odds, market prices, implied probabilities, external Elo, analyst predictions, injuries, lineups, suspensions, transfers, or fixture-congestion inputs.
3. Every fixture is reported from the home team’s perspective: home win, draw, or home loss.
4. Strict causality: only completed matches before the fixture date may enter evidence.
5. Every phase is audited before the next phase.
6. Failed audit means STOP and **NO CALL**.
7. No quantity is published without its evidence path, sample size, spread, and calibration status.
8. Over/under and BTTS are separate goals outputs and must not be inferred from 1X2 evidence.
9. A draw is not a home-win success when settling a home-win direction.
10. The system may refuse a fixture. Refusal is preferable to fabricated certainty.

---

## 2. Fixture protocol

### Phase 1 — Identity and data integrity

Verify:

- canonical identity of both clubs;
- country and competition;
- sufficient prior records;
- exact dates or explicit date precision;
- no duplicate records;
- no split identities;
- home/away order;
- venue, neutral, or relocated status.

### Phase 2 — Direct H2H

Use all prior meetings inside the allowed time window. Record:

- date;
- competition;
- venue;
- score;
- home perspective;
- context comparability.

A single H2H is usable evidence but cannot automatically create high confidence.

### Phase 3 — Common opponents

Find clubs both teams faced before the fixture. Record each path separately:

- opponent;
- both results;
- goal differences;
- dates;
- competition context;
- independence from other paths.

### Phase 4 — Common opponents of opponents

Use when direct common-opponent evidence is sparse. Record the full chain and all match IDs. Do not treat a reused match as an independent path.

### Phase 5 — Aggregate and confidence

Calculate:

- weighted estimate;
- unweighted estimate;
- path count;
- effective independent path count;
- alignment;
- weighted spread;
- date spread;
- context mix;
- outlier sensitivity.

### Phase 6 — Goal-difference tier

Map the estimate to a measured historical tier. Quote the observed outcome rate for that tier, not a raw modelled percentage.

### Phase 7 — Goals

Only publish goal totals after a separately validated goals model passes its calibration gate. BTTS remains withheld unless its calibration is repaired.

### Phase 8 — Selection

Select only expressions traceable to validated quantities. If evidence is weak or conflicting, use NO CALL rather than force a selection.

### Phase 9 — Verdict

Report:

- direction;
- calibrated confidence;
- evidence grade;
- fallback, if justified;
- what would falsify the call;
- withheld outputs.

### Phase 10 — Log

Record the fixture, date, estimate, confidence, evidence grade, prediction, and eventual result for scoring.

---

## 3. Cross-border extension

Cross-border rating is allowed and required when the fixture involves different domestic leagues.

It must not use an arbitrary league multiplier.

The extension must preserve:

- domestic club attack/defence evidence;
- league-strength bridge estimated from completed cross-border results;
- home, neutral, and relocated venue treatment;
- strict date ordering;
- identity resolution;
- held-out validation.

The supplied 2026-07-30 audit extract found that European-edge scale values above 1.00 degraded RMSE. The current working baseline is therefore **unweighted scale = 1.00** until a superior method wins on held-out data.

---

## 4. Adaptive evidence and gentle calibration — APPROVED

This is the approved **gentle calibration** amendment: evidence thresholds are relaxed, while weak evidence is shrunk toward base rates instead of being rejected or overstated.

The system will not impose an unnecessarily rigid minimum number of shared opponents.

Evidence quantity affects confidence gradually:

| Evidence state | Output treatment |
|---|---|
| H2H plus aligned common-opponent paths | stronger directional confidence if calibration supports it |
| one H2H or one common opponent | provisional lean, strongly shrunk |
| one third-level path | evidence only unless other gates pass |
| conflicting paths | low confidence or NO CALL |
| identity/date/venue failure | hard NO CALL |

Confidence uses four components:

1. **Direction:** proportion of paths agreeing.
2. **Strength:** distance of aggregate estimate from zero.
3. **Reliability:** effective independent paths, spread, recency, context, venue.
4. **Calibration:** held-out historical outcome rate for comparable situations.

Raw probability must be gently shrunk toward the relevant base rate:

```text
calibrated probability =
    reliability_weight × raw probability
    + (1 − reliability_weight) × base rate
```

The reliability weight and shrinkage constant must be learned from historical data, not selected by intuition.

Confidence labels:

- **Calibrated strong**
- **Calibrated moderate**
- **Lean only**
- **Close call**
- **NO CALL**

“Decisive direction” and “calibrated confidence” are separate. A fixture may have a decisive direction but only moderate calibrated confidence, as in the Real Madrid–Celtic audit.

### Transparent balance panel — APPROVED

A NO CALL must still show the balance that produced the refusal. Human review should not see only “not recommended.”

Every output should display:

```text
home support:       raw and weighted evidence
 draw support:      raw and weighted evidence
away support:       raw and weighted evidence
neutral/uncertain:   evidence not strong enough to assign
aggregate estimate: signed home-perspective goal-difference estimate
path alignment:     agreeing / conflicting paths
calibrated range:   only when validated
```

Evidence share is not the same as match probability. For example, in Anderlecht v Hammarby:

- H2H was level: weight 3 toward neutral evidence;
- two common-opponent paths favoured Hammarby: weight 4 combined;
- the internal evidence balance was therefore Hammarby 4 / neutral 3;
- this is an evidence balance, not a claim that Hammarby had a 57.1% match probability.

Once the calibration layer is trained, the panel may show outcome bands such as home/draw/away percentages or intervals. Until then, percentages are withheld and the evidence balance is shown instead.

---

## 5. Weighting candidates to test

No candidate is operational until it wins on untouched historical fixtures.

Phase-weight candidates:

```text
W1: H2H 3.0, common opponent 2.0, opponent-of-opponent 1.0
W2: H2H 2.0, common opponent 2.0, opponent-of-opponent 1.0
W3: H2H 1.0, common opponent 2.0, opponent-of-opponent 1.0
W4: H2H 2.0, common opponent 1.0, opponent-of-opponent 0.5
```

Required comparisons:

- unweighted baseline;
- phase-weighted candidates;
- recency candidates;
- independence controls;
- context candidates;
- combined models.

Selection criteria:

- rolling-origin or time-split validation;
- direction accuracy;
- Brier score after calibration;
- log loss;
- goal-difference RMSE and MAE;
- calibration slope/intercept;
- confidence-interval coverage;
- performance by evidence count and context.

No single metric may be used alone.

---

## 6. Current audit record

### Real Madrid v Celtic — 2 November 2022

Independent pre-match protocol test, not run from the 2026 package.

- H2H before fixture: Celtic 0–3 Real Madrid.
- Common opponents: Leipzig and Shakhtar.
- Common-opponent estimates: +2.5 and +0.5 for Real Madrid.
- Candidate weighted estimate: +2.14.
- Direction: Real Madrid.
- Confidence: moderate, because only three independent evidence lines were available.
- Actual result: Real Madrid 5–1 Celtic.
- Direction: correct.
- Goal-total output: withheld.

This is one successful retrospective direction test, not proof of calibrated probabilities.

### Maccabi Tel Aviv v Sheriff Tiraspol — 30 July 2026

The first-leg record is now present in the attached audit extract:

```text
2026-07-23 Sheriff Tiraspol 0–5 Maccabi Tel Aviv
```

Current rebuild using the supplied graph:

- 13 simple paths up to three edges;
- 1 direct H2H path;
- 12 common-opponent paths;
- 0 third-level paths;
- European fraction: 0.258;
- context: DOM-heavy;
- neutral estimate: +1.8294 Maccabi;
- normal-home estimate: +2.1094 Maccabi.

Calibration was insufficient for a published probability. Prior status: **NO CALL**, with a provisional 1X fallback only if forced.

This fixture will be re-tested after the live blueprint and adaptive-calibration rules are applied.

### Anderlecht v Hammarby — 30 July 2026

First close-call goal-range test under the live blueprint.

- First-leg H2H: Hammarby 1–1 Anderlecht.
- Confirmed common opponents: Charleroi and BK Häcken.
- Both common-opponent paths favour Hammarby by +1.50 goal-difference units.
- H2H GD from Anderlecht perspective: 0.00.
- Unweighted aggregate estimate from the three evidence lines: −1.00.
- Candidate W1 phase-weighted estimate: −0.8571 from Anderlecht’s perspective.
- Direction: Hammarby lean, but not decisive.
- Goal evidence is split across low, exactly-two, and 3+ totals and remains uncalibrated.
- Confidence label: Close call / lean only.
- No primary winner or goal-range recommendation published.

---

## 7. Known defects not to regress

- Do not treat absent records as “never met” without checking external historical sources.
- Do not use season-end placeholder dates as exact match dates.
- Do not treat two legs of one tie as independent without an aggregate identifier.
- Do not give full home advantage to neutral or relocated matches.
- Do not use raw chain estimates as probabilities.
- Do not convert a goal-difference estimate into over/under.
- Do not call one path high confidence.
- Do not let one outlier dominate without sensitivity reporting.
- Do not silently substitute a different fixture when the selected fixture is unavailable.
- Do not claim a weighting is validated from an in-sample result.

---

## 8. Application integration status

The blueprint is ready as an **application specification**, but it is not yet production-ready as embedded code.

The current app can display a domestic rating, but embedding the full system requires these modules:

1. `identity_store` — canonical teams, aliases, countries, leagues, identity IDs.
2. `match_store` — completed results, exact dates, competition, venue, neutral/relocated flags, extra-time and shootout flags, aggregate tie IDs.
3. `evidence_graph` — H2H, common-opponent, and opponent-of-opponent paths with match fingerprints.
4. `cross_border_bridge` — validated league connection without arbitrary multipliers.
5. `goal_range_model` — 0–1 / exactly 2 / 3+ bins, separately calibrated from 1X2.
6. `confidence_calibrator` — gentle shrinkage toward base rates with versioned calibration tables.
7. `balance_panel` — home/draw/away evidence shares, uncertainty, path alignment, estimate, and calibrated bands.
8. `audit_log` — data version, model version, cutoff date, sources, result settlement, and Brier/log-loss records.

The app must refuse to save or publish a rating when identity, date, venue, or calibration gates fail.

### Update cadence

- **After completed matches:** ingest results; do not immediately change calibration constants.
- **Daily or before a fixture:** update the evidence graph and team ratings using only completed results.
- **Weekly:** run data-integrity, duplicate, identity, and venue audits.
- **Monthly:** refresh calibration tables if the held-out window is large enough.
- **Quarterly or after a major data rebuild:** compare the live model with the previous version and preserve rollback snapshots.

Every update must preserve:

```text
training cutoff
source version
model version
calibration version
rows added
rows rejected
rows corrected
```

## 9. Next work order

1. Apply this blueprint to the Maccabi–Sheriff rebuild.
2. Recalculate adaptive evidence features.
3. Produce raw and gently calibrated outputs separately.
4. Audit venue treatment again.
5. Compare against the previous unweighted result.
6. Implement the balance panel in the app.
7. Validate the goal-range bins on a historical cluster.
8. Issue a call only if the calibration and evidence gates pass.
9. Record amendments and decide whether to promote this document to v2.

**No v2 promotion occurs until the re-test is audited.**

---

## 10. Change log

### 2026-07-30 — v1.0-live

- Added approved cross-border support requirement.
- Added adaptive evidence requirements.
- Added gentle calibration toward base rates.
- Separated decisive direction from calibrated confidence.
- Preserved no-market and no-fabrication rules.
- Added weighting candidate grid and held-out selection criteria.
- Added Real Madrid–Celtic and Maccabi–Sheriff audit records.
