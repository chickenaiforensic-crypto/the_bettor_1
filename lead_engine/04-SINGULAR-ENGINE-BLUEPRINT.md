# 04 — SINGULAR ENGINE BLUEPRINT (One Weighted System)

**Date:** 2026-08-05 draft — final after weighting matrix locked & harness S0 productionised  
**Authority:** SOT v1.3 §2-§11, Masterplan v1.1 §1-§10, Functionality v1.0, Verification v1.0, 03-weighting matrix  
**Doctrine:** One store, one live fit, one verdict card. Compute live from store or stay silent with plain label (A-01). Results only, zero market (P1). Approval = test run only (T1-T8, ladder).

## 1. Diagram — The Singular Flow

```
STORE — 5082 verified 90-min results only (P1/P2) — identities + date + venue + score + tieId + source
   | every derive strict causality D3 seq[:i] before cutoff
   |---> L1 LIVE DC FIT per-league online LR 0.055 DECAY 0.0022 HFA_LR 0.010 ρ -0.06 clamp [0.05,6.0] etc
   |         | fitted not constant — home 1.20-1.36×, home_extra decay 0.999 ±0.25, min6 P3
   |         v
   |---> L2 TWO GRIDS scoreGrid Poisson×Poisson DC τ → H/D/A raw best who-wins
   |         goalsGrid shrunk G_K0.5 GMU 2.6186 → O/U handicap separate family BTTS withheld 6%
   |         |
   |         v
   |----> L3 STAR DRAW CORRECTION metric (3W+D)/P P≥5 shrink6 quintile hysteresis0.05 ±0.02 cap prop renorm
   |         | target draw_table[tier|gap] 27cells else draw_base[tier] w0.2/0.5/0.5 — never moves favourite
   |         v
   |----> VERDICT CARD PROBABILITY: D_calibrated + H/A proportionally rescaled provenance-tagged M3
   |
   |---> R2 EVIDENCE GRAPH — H2H·common·3rd+opponent-of-opponent phase paths effective/agree/nocall causal
   |         |
   |         v
   |----> ZONE LADDER STRONG→TOSS calibrated rates WITH n/spread/calibration 78%/92% n59 etc monotone
   |----> BALANCE PANEL M7 NO CALL must show home/draw/away support shares — honesty shell P3
   |----> CHAIN CROSS-BORDER r+0.274 n693 62.6% dir standby — needs Euro connector + fit-to-results loop §6 A-08
   |
   |---> R3 ELO DISPLAY-ONLY INIT1500 K20 home+65 star clamp((ELO-1420)/2 0..100)→1-5★ window6 min3 causal
   |
   |---> L4 TIERS/POINTS readability A+≥70 78.5% n7718 etc points round(100×H_cal) labels
   |----> L5 CONSENSUS filter-only mean(HvH,AvA) ≥4H≥4A both sides Tier A/A+ >1.5 STRONG 78.6% etc
   |
   v
VERDICT CARD (ONE OUTPUT)
  probability (DC provenance-tagged) + confidence band (zones with cal) + labels (tiers/consensus display) + stars display-only + refusal path NO CALL with reasons + balance
   |
   v
SETTLEMENT draw=loss for home call never push I5 → calibration feedback M5 masked replay auto after any data change monthly full sweep
```

## 2. Computation Contract (MUST / MUST NOT per Layer — Masterplan §3)

| Layer | MUST | MUST NOT |
|---|---|---|
| L1 fit | fit online date order causality, constants LR0.055 DECAY0.0022 HFA_LR0.010 1.6×/8 ρ-0.06 clamps [0.05,6.0] HFA [0.05,0.55] home_extra ±0.25 decay0.999 min6 | use carried parameters, fit on future rows |
| L2 | two grids separated, goals shrunk toward league mean | let star correction leak into goals markets |
| L3 | draw_table[tier\|gap] 0.2/0.5/0.5 weights ±0.02 cap proportional renorm, metric (3W+D)/P P≥5 shrink6 quintile hysteresis0.05 | move favourite, exceed cap, edit goals |
| L4/L5 | label from corrected prob, consensus from ≥4H/≥4A both sides | alter any prob |
| R2 | paths only from prior results, calibrated zone or NO CALL, balance always shown M7 | dress evidence shares as prob |
| R3 | compute stars live from store every derive | edit R1/R2, claim predictive power |
| Output | provenance on every number source/window/n/calibration/date M3 | silent precomputed, market refs P1, forced number |

## 3. Refusal Paths P3 — Honesty Shell In Priority

1. League without replay win → evidence-only plain label A-01
2. Team <6 matches → no rating · <5 games no stars/draw correction · <4 home/away no consensus
3. Venue unproven → hard error save disabled I4
4. Cross-league tie without validated bridge → chain evidence or NO CALL + balance panel M7
5. BTTS → withheld I3
6. Draw settlement = loss for home call never push I5

Every refusal shows reason + balance when applicable — NO CALL is valid shown output.

## 4. Cross-League Weighting — Fit-to-Results Loop (Owner Example Formalised) Masterplan §6

Goal rate teams different leagues on one weighted common scale e.g. EPL vs Dynamo Moskva then standard applies.

1. CONNECTOR UNIVERSE actual cross-league results 2021-26 UEFA CL/EL/ECL + qualifiers involving programme leagues. Today 0 rows → researcher pack #17 required D14 approved.
2. MODEL team ratings per league own scale league strength s_L rescales onto common. Prediction vs actual every connector tie.
3. FIT LOOP each league pair enough ties measure bias(L)=mean(predicted GD - actual GD) over ties involving L then adjust s_L←s_L×(1+step×bias(L)) step≈0.05-0.1 re-predict re-measure iterate until bias converges below tolerance typ 20-50 passes gradient-descent on same loss harness scores. This IS bump until it matches each league weight driven by direct results vs others not opinion.
4. VALIDATION actual approval gate per §5: fit s_L on connector up to cutoff 2021-22..2024-25 test on LAST OMITTED window 2025-26 European matches untouched weighted vs frozen unweighted scale 1.00 baseline adopt ONLY if wins Brier/RMSE/direction paired on omitted window.
5. If adopted weighted common scale becomes L1 input for cross-league fixtures standard L2-L5 unchanged. If not stay silent plain "no calibrated bridge" label P3 — chain evidence view remains.

Guardrails no arbitrary multiplier weights from fit Euro-edge scale >1.00 degraded RMSE historically so frozen 1.00 incumbent connector data must pass same ingest/audit gates one gate M10 screen before use.

## 5. Verdict Card — One Fixture End to End (Post-Build Target) Masterplan §7

1. Pick fixture → same-league check → sufficiency check ≥2 full seasons in store D3-gated
2. If sufficient masked-replay verdict must be CURRENT auto-refresh on data change M1 DC must beat evidence → RATED card probabilities + provenance. Else labeled bootstrap below sufficiency / evidence view. NO CALL allowed.
3. Evidence graph always available paths → calibrated zone or NO CALL + balance M7
4. Goals two-grid outputs only O/U handicap scoreline = uncorrected grid max cell + true freq ~13%
5. Consensus/tier labels when data allows display. Stars display-only.
6. Save row → settlement ledger draw=loss → monthly masked replay M5 → calibration feedback.

What best computational wins means: highest calibrated accuracy each output can carry on app's own data measured by masked replay Brier/logloss/calibration per market + settlement ledger. NOT match bookmaker P1 forbids using prices even benchmark NOT highest hit rate draw is loss for home calls I5.

## 6. Build Order (Structural Then Architectural) Masterplan §8

| Step | Work | Gates measured test runs §5 | Ledger |
|---|---|---|---|
| S0 | Universal backtest harness exists audit_work/backtest_harness.py productionise rolling-origin paired stats MDE full metric artifact | harness self-check vs §5.2 numbers RPL 0.5675 vs 0.6465 -12.2% etc | — |
| S1 | LIVE-DERIVE-01 live re-derive + auto re-validation + provenance panel retire __DC_GATE__/legacy blob to provenance text live form stars from store or not rated yet | G14/G15/G16/G17 | M1 M2 M3 M4 M16 |
| S2 | Settlement venue-guard audit I5 draw=loss enforced on settlement tab I4 entry-side flip guard | M17 acceptance pins | M17 |
| S3 | Balance panel full build NO CALL shows home/draw/away support shares | held-out calibration | M7 |
| S4 | Goal-range bins 0-1/2/3+ own calibration | harness win vs current best omitted window | M8 |
| S5 | Cross-border UEFA connector pack UCL/UEL/UECL+quals 2021-26 owner-confirmed scope D14 expansion approved → fit-to-results loop §6 → weighted scale vs frozen 1.00 baseline on omitted Euro window | A-08 harness acceptance | M9 M19 |
| S6 | Calibration cadence one-click masked replay after any data change monthly full sweep | M5 pins | M5 M6 |
| S7 | ARCHITECTURAL/UI BUILD next phase per owner human-first plain language A-02 provenance small-print | UI-PLAIN-01 acceptance | A-02 |

Every S-step gate column is harness output table — no gate passes on description alone.

## 7. What Changes vs Today's App v3.6.3

| today | after S1-S6 |
|---|---|
| rated card depends on carried stamps/legacy records G17 finding | live derive or plain not rated yet no hidden precompute |
| form stars null on live path | live form stars from store |
| no provenance on precomputed inputs | provenance panel on every number |
| no balance panel on NO CALL | balance always shown |
| calibration artifacts stale since imports | masked replay auto-regenerated on data change + monthly full sweep |
| systems approved on documentation | approved only by harness test run on omitted window §5 |
| cross-league silent/standby | gated bridge from fit-to-results loop §6 wins place only on evidence |
| BTTS present-but-flagged | withheld unchanged I3 |
| 11 CZ1 rows misdated MOL Cup 120/202 | corrected store D-1/D-2 5082 |

## 8. Explicitly NOT Planned (So No One Builds By Accident)

- Unified European ratings without A-08 replay win (open item 5 proposed never approved)
- Any market/odds input feature benchmark sanity check fallback P1 permanent
- Injuries lineups transfers congestion features deferred owner
- Profitability claims calibrated ≠ profitable only calibration claimed
- UI that hides machine provenance behind AI-style confidence language A-02 plain words numbers provable

*This blueprint supersedes nothing in SOT it is SOT §10/§11/§12 translated into one weighted buildable structure. Amendments follow SOT amendment register A-xx owner-approved.*

## 9. Implementation Fidelity

- Shipped code reproduces validated research code exactly historical record 0.00e+00 across 7 quantities browser vs trainer
- Test coverage before ship suites historic core28 update23 sync35 stars/consensus24 blueprint compliance31 engine compliance26=167 current builder suites smoke49 R8 13 R9 7 R10 12 R11 18 scope43 hold9 parity7 legacy156 lineage map unproven M18 builder must map 167 onto today's suite names in v3.6.4 return
- Market gating ship ≤2.7% caution 3.0-3.3% BTTS withheld 6.0% LIVE
- Venue integrity procedural never trust parsed venue hard error if home team never hosted league tick-box vs official list save disabled until confirmed venue locked at entry PARTIAL venue/neutral/relocated flags in match rows + no-reflip at ingest entry-side flip guard belongs manual-entry surface unaudited this session M17
- Scoring rule draw is loss for home-win call never push never excluded Log&Settlement tab exists rule-enforcement check pending M17
- Zero network dependency fetch/XHR/http 0 updates via validated file/paste intake LIVE single static file ingest gate + holds adversarial surface
- Update protocol lineage OLD app used validated paste sync protocol 35 tests 11 adversarial attacks blocked NEW app replaced with file ingest pack drop one gate + holds mapped no action

*Living doc amendments per §12 SOT. Everything asserted traces to doc section code line or pinned file no stories.*
