# THE SINGULAR ENGINE — structural masterplan (zero-market, weighted, unified)

**Version 1.1 — 2026-08-05 · Issued by: Lead planner/analyst (auditor cross-checked)**
**v1.1 amendment (owner doctrine, 2026-08-05):** approval = measured test run, never documentation; universal bulk-backtest protocol added (§5, first live run shown); cross-league weighting formalised as a fit-to-results calibration loop (§6). D-1 date fix approved and applied (`pitch-rating-full-D1-corrected-2026-08-05.json`).
**Purpose:** collapse the three computation families (R1 rating engine, R2 evidence engine, R3 ELO layer — SOT §2) and every sub-system into **one structural system** whose components are weighted by *measured* effectiveness, not by origin or preference. The output is the plan the builder implements; the architectural/UI build follows it (next phase, per owner order).
**Compliance:** P1 no market data in any role · P2 results-only · P3 "I don't know" is a valid output · P4 foundation→validation→superstructure · P5 shipping needs owner approval · T1–T8 testing protocol · I1–I6 implementation protocol. All numbers below are the measured ones from METHODOLOGY/ENGINE_SPEC/LIVE-BLUEPRINT/ZONES, re-verified where possible in the 2026-08-05 data audit.

---

## 1. The one-page map (what the singular system IS)

```
                        ┌─────────────────────────────────────────┐
                        │  STORE — completed 90-min results only  │  (P1/P2; ingest gate;
                        │  (identity · date · venue · score)      │   dedupe, mute, backup-gated purge)
                        └───────────────┬─────────────────────────┘
                                        │  every derive, strict causality (D3: seq[:i])
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
   ┌──────────────────┐      ┌─────────────────────┐      ┌──────────────────┐
   │ L1 LIVE DC FIT   │      │ R2 EVIDENCE GRAPH   │      │ R3 ELO (display) │
   │ (per-league,     │      │ H2H · common · 3rd  │      │ stars 1–5 ★      │
   │  replay-gated)   │      │ phase paths         │      │ K20, home +65    │
   └────────┬─────────┘      └──────────┬──────────┘      └────────┬─────────┘
            ▼                          ▼                            │
   ┌──────────────────┐      ┌─────────────────────┐                │
   │ L2 TWO GRIDS     │      │ zone ladder         │                │
   │ scoreGrid → 1X2  │      │ STRONG→TOSS with    │                │
   │ goalsGrid → O/U  │      │ calibrated rates    │                │
   └────────┬─────────┘      └──────────┬──────────┘                │
            ▼                          ▼                            │
   ┌──────────────────┐      ┌─────────────────────┐                │
   │ L3 star draw     │      │ balance panel (M7)  │                │
   │ correction ±0.02 │      │ NO CALL must show   │                │
   └────────┬─────────┘      │ the balance         │                │
            ▼                └──────────┬──────────┘                │
   ┌────────────────────────────────────┼───────────────────────────┘
   │        VERDICT CARD (one output)                               │
   │  probability (DC, provenance-tagged) + confidence band (zones) │
   │  + labels (tiers/consensus, edits nothing) + stars (display)   │
   │  + refusal path: NO CALL with reasons (P3)                     │
   └────────────────────────────────────┬────────────────────────────┘
                                        ▼
                        SETTLEMENT (draw = loss, I5) → calibration feedback (M5)
```

**The doctrine that makes it singular:** one store, one live fit, one verdict card. A league is either *rated* (its live DC fit won the app's own masked replay) or *evidence-only with a plain label* (A-01). There is no second rating universe, no carried bootstrap, no hidden input (M3 provenance panel; `__DC_GATE__`/legacy blob demoted to provenance text).

---

## 2. Weighting the effectiveness — the measured ledger

Every component is ranked by its **measured contribution to outcome accuracy**. This table is the system's constitution: a component's rank = its evidence, nothing else.

| # | Component | What it answers | Measured effect | Weight class | Gate to STAY in the system |
|---|---|---|---|---|---|
| 1 | **L1 Dixon-Coles live fit** | who wins, how much | Brier 0.6112 vs 0.6476 base = **+5.6%**; calibration ≤1.7% | **Dominant — the probability** | masked replay on current store rows must beat evidence + base rate (auto re-run on any data change, M1) |
| 2 | **League home advantage (per-league)** | venue strength | 1.20×–1.36× goal multiplier — league-specific, never global | inside λ | fitted, not constant |
| 3 | **L2 scoreGrid** | H/D/A distribution | Poisson + DC ρ=−0.06, normalised | shapes everything | calibration ≤2.7% on 1X2 |
| 4 | **L2 goalsGrid (shrunk k=0.5)** | O/U, handicap | O2.5 error 10.3%→**2.7%**; BTTS 6.0% **withheld** | separate family — never merged with 1X2 | per-market calibration gate (I3) |
| 5 | **L3 star draw correction** | draw-rate refinement | **+0.047%** full-1X2 (p<0.0001, n=59,615); tier-2/3 ≈ +0.09%; cap ±0.02 | real, small | paired test, all five metrics (T4), proportional split (M4) |
| 6 | **L4 tiers/points** | readability | 0 probability impact; calibrated labels (A+ 78.5%…) | display | labels must match observed rates |
| 7 | **L5 consensus** | selection filter | STRONG 78.6% / CONFIRMED 74.8% vs 73.0% model top-10% (**+5.6pt**) | filter only | changes no probability (test-enforced) |
| 8 | **R2 zone ladder** | confidence band | STRONG 78%/92% pair (n=59) · WIN 67/82 · WIN-DRAW 49/75 · lean 47 · toss 45 — monotone | confidence statement, NOT probability | held-out calibration; n + spread shown with every call |
| 9 | **R2 chain (cross-border)** | disconnected-league ties | 3rd phase r=+0.274, 62.6% direction (n=693) | standby | held-out win over frozen scale-1.00 baseline (A-08/M9) |
| 10 | **R3 ELO stars** | quick ordinal read | unvalidated vs outcomes | display only | A-03: adopt display-only with "not a prediction" label |
| 11 | **Data layer** | truth of everything above | audit: 5,000/5,000 rows verified; 11 date defects found & fixed | substrate | ingest gate + audit protocol + M10 outcomes-only screen |

**Weighting rule:** no component may consume another's output unless its rank is higher or it is display-only. L3 may edit L2's probabilities (capped, measured gain); L5/R2/R3 may never edit L1–L3 (enforced by tests). This is the *singularity*: the hierarchy is fixed by measurement and enforced in code.

---

## 3. The computation contract (what each layer MUST and MUST NOT do)

| Layer | MUST | MUST NOT |
|---|---|---|
| L1 fit | fit online, date order, causality; constants LR 0.055 · DECAY 0.0022 · HFA_LR 0.010 · 1.6×/8 · ρ −0.06 · clamps | use carried parameters; fit on future rows |
| L2 | two grids, separated; goals shrunk toward league mean | let star correction leak into goals markets |
| L3 | draw_table[tier\|gap] with 0.2/0.5/0.5 weights, ±0.02 cap, proportional renormalisation | move the favourite; exceed the cap |
| L4/L5 | label from corrected probability; consensus from ≥4 home/≥4 away both sides | alter any probability |
| R2 | paths only from prior results; calibrated zone or NO CALL; balance always shown | dress evidence shares as probabilities |
| R3 | compute stars live from store | edit R1/R2; claim predictive power |
| Output | provenance on every number (source, window, n, calibration, date — M3) | silent precomputed material; market references (P1) |

**Refusal paths (P3) — the honesty shell, in priority order:**
1. League without a replay win → **evidence-only, plain label** (A-01).
2. Team < 6 matches → no rating · < 5 games → no stars/draw correction · < 4 home/away → no consensus.
3. Venue unproven → hard error, save disabled (I4).
4. Cross-league tie without a validated bridge → chain evidence or **NO CALL** + balance panel (M7).
5. BTTS → withheld (I3). Draw settlement = loss for a home call, never a push (I5).

---

## 4. Weighting candidates that are NOT yet allowed (and their exact entry test)

Nothing below is operational. Each has a written, measured entry test — no intuition gates (T8):

| Candidate | Promise | Entry test | Currently |
|---|---|---|---|
| W1–W4 phase weights (H2H/common/3rd) | better evidence direction | held-out win on untouched fixtures vs unweighted baseline, all metrics (LIVE-BLUEPRINT §5) | NOT operational |
| A-08 weighted cross-league bridge (league-strength scale from UEFA 2021-26) | EPL side vs Dynamo Moskva on one rated scale | §6 fit-to-results loop, harness win vs frozen scale-1.00 baseline on the omitted European window | APPROVED for documentation only; zero code; loop spec ready |
| Recency weighting (C6) | fresher evidence counts more | measured 84/84 no discrimination → **rejected** | dead |
| Venue correction + saturation (Candidate A) | fix h2h blowout pocket | A/B replay: no gain, pocket worse → **rejected, engine reverted** | dead |
| Spread-based chain gate | reject wide-spread chains | measured: tight spread *worse* (r 0.195 vs 0.384) → **rejected** (T8, E6) | dead |
| Goal-range bins 0–1/2/3+ (M8) | calibrated goal bands | separate calibration + held-out win, after M7 | not built |
| Injuries/lineups/xG (open item 6) | context | deferred by owner | out of scope |

The register of rejected ideas is as important as the register of live ones — it prevents re-litigating measured failures (E1–E9).

---

## 5. APPROVAL BY TEST RUN — the universal backtest instrument

**Owner doctrine (2026-08-05), binding:** no system, weight, or constant is adopted because a document approves it. Every candidate ships only when **its measured test run on our own data** says it wins. "Approved for documentation" is a planning state only; the adoption state is "won the backtest."

### 5.1 The instrument (one harness for every candidate)

**Owner's ladder (2026-08-05, binding):** test runs start from 2021's data up to the newest, with the **final game omitted** for test calibration. When the last game is fully calibrated, hold out the **last 2 games**, re-check, then keep expanding the holdout backwards; finish with a **full-system accuracy check** and readjust if necessary.

```
L-1  train 2021 → (newest game − 1); predict the newest game; calibrate constants
     (bounded steps, existing caps) until it matches.
L-2  hold out the newest 2 games; retrain on all before; test on both; readjust if needed.
L-n  expand holdout (3, 4, … or one matchday at a time) until it covers the whole
     last season.
FULL full-system accuracy check, all leagues, complete metric set (T4), paired (T1),
     with n and MDE (T2). Any degradation → adjust the designated constant → re-run
     the ladder from L-1. When constants stop needing adjustment as the holdout
     grows, the system is CALIBRATED and the candidate is APPROVED BY TEST RUN.
```

Honest rule (T2/E2): single-game steps are noise-level — L-1/L-2 are calibration warm-up, not proof; proof is the ladder converging as it expands. Held-out games are touched only by scoring, never by fitting (E8). Every run writes a numbers artifact (train window, holdout, n, all metrics, date) — the artifact is the approval record.

### 5.2 First live run of the harness (2026-08-05, on the D-1-corrected store)

Simplified fit (spec B3 constants; naive init; no star correction, no evidence ensemble) — a **feasibility run of the instrument**, not the approved engine calibration:

| League | train | test (last omitted season) | Brier DC | Brier base | gain | log loss | direction |
|---|---|---|---|---|---|---|---|
| RPL | 2021-22..2024-25 (960) | 2025-26 (254 scored, 2 refused P3) | **0.5675** | 0.6465 | **−12.2%** | 0.957 | 55.9% |
| CZ1 | 2021-22..2024-25 (1,105) | 2025-26 (276) | **0.6090** | 0.6509 | **−6.4%** | 1.015 | 49.3% |
| EPL | 2021-22..2024-25 (1,520) | 2025-26 (374 scored, 6 refused) | **0.6140** | 0.6534 | **−6.0%** | 1.023 | 49.2% |

Reading: the live DC fit beats the base rate on every league's last omitted season, in line with the legacy engine's measured +5.6% (RPL stronger on five full seasons). This is the baseline every candidate (star correction, evidence ensemble, zone ladder, cross-league bridge) must beat **per league, on the omitted window, paired** — that is the gate. Script: `audit_work/backtest_harness.py` (re-runnable; part of the repo).

### 5.3 Cadence
- Every candidate that reaches "documented" gets a harness entry; the harness output table IS the approval record.
- After any data change: masked replay auto-reruns (M1); monthly: full harness sweep (M5).
- Settlement feeds the test windows (I5: draw = loss), so the omitted window is scored on settled outcomes.

## 6. CROSS-LEAGUE WEIGHTING — the fit-to-results loop (owner example, formalised)

**Goal:** rate teams from different leagues on one weighted common scale (e.g. EPL side vs Dynamo Moskva) — then the standard computation applies (M19/A-08).

**The loop ("bump the league up until it matches"):**

```
1. CONNECTOR UNIVERSE — actual cross-league results 2021-26 (UEFA CL/EL/ECL + qualifiers
   involving our leagues). Today: ZERO rows in store → researcher pack required
   (D14 scope expansion needs owner approval; workorder shape = existing cup packs).
2. MODEL — team ratings exist per league on their own scale; league strength s_L
   rescales them onto the common scale. Prediction vs actual for every connector tie.
3. FIT LOOP — for each league pair with enough ties, measure the bias:
       bias(L) = mean(predicted GD − actual GD) over ties involving L
   then adjust:   s_L ← s_L × (1 + step × bias(L))     (step ≈ 0.05–0.1)
   re-predict, re-measure, iterate until the bias converges below tolerance
   (typically 20–50 passes; gradient-descent on the same loss the harness scores).
   This IS the "bump until it matches": each league's weight is driven by its
   direct results against the others, not by opinion.
4. VALIDATION (the actual approval gate, per §5):
   fit s_L on connector matches up to cutoff (2021-22..2024-25);
   test on the LAST OMITTED window (2025-26 European matches, untouched);
   weighted scale vs frozen unweighted scale 1.00 (LIVE-BLUEPRINT §3 baseline);
   adopt ONLY if it wins on Brier/RMSE/direction, paired, on the omitted window.
5. If adopted: weighted common scale becomes the L1 input for cross-league
   fixtures; standard layers L2–L5 apply unchanged. If not: stay silent with a
   plain "no calibrated bridge" label (P3) — the chain evidence view remains.
```

**Guardrails:** no arbitrary multiplier (LIVE-BLUEPRINT §3) — the weights come from the fit; European-edge scale >1.00 degraded RMSE historically, so the frozen 1.00 baseline is the incumbent to beat; connector data must pass the same ingest/audit gates as domestic data (one gate, M10 screen before use).

## 7. The singular flow for ONE fixture (post-build target)

```
1. Pick fixture → same-league check → sufficiency check (≥2 full seasons in store, D3-gated).
2. If sufficient: masked-replay verdict must be CURRENT (auto-refresh on data change, M1);
   DC must beat evidence → RATED card (probabilities + provenance).
   Else: labeled bootstrap below sufficiency / evidence view. NO CALL allowed.
3. Evidence graph always available: paths → calibrated zone or NO CALL + balance (M7).
4. Goals: two-grid outputs only (O/U, handicap); scoreline = uncorrected grid max cell + true freq.
5. Consensus/tier labels when data allows (display). Stars display-only.
6. Save row → settlement ledger (draw = loss) → monthly masked replay (M5) → calibration feedback.
```

**What "best computational wins" means in this system (stated plainly):** the highest *calibrated* accuracy each output can carry on the app's own data — measured by masked replay (Brier/log-loss/calibration per market) and by the settlement ledger. It does NOT mean "match the bookmaker" (P1 forbids using prices even as a benchmark) and does NOT mean "highest hit rate" (a draw is a loss for home calls, I5).

---

## 8. Build order (structural, then architectural — approval by test run per ship, P5)

| Step | Work | Gates (all = measured test runs, §5) | Ledger items |
|---|---|---|---|
| S0 | **Universal backtest harness** (exists: `audit_work/backtest_harness.py`; productionise: rolling-origin, paired stats, MDE, full metric set, artifact output) | harness self-check vs §5.2 numbers | — |
| S1 | **LIVE-DERIVE-01**: live re-derive + auto re-validation + provenance panel; retire `__DC_GATE__`/legacy blob to provenance text; live form stars from store (or "not rated yet") | G14/G15/G16/G17 | M1, M2, M3, M4, M16 |
| S2 | Settlement & venue-guard audit (I5 draw=loss enforced on the settlement tab; I4 entry-side flip guard) | M17 acceptance pins | M17 |
| S3 | Balance panel full build (NO CALL shows home/draw/away support shares) | held-out calibration | M7 |
| S4 | Goal-range bins 0–1/2/3+ with own calibration | harness win vs current best, omitted window | M8 |
| S5 | Cross-border: UEFA connector pack (**UCL/UEL/UECL + quals, 2021-26 — owner-confirmed scope 2026-08-05; D14 expansion approved**) → fit-to-results loop (§6) → weighted scale vs frozen 1.00 baseline on the omitted European window | A-08 harness acceptance | M9, M19 |
| S6 | Calibration cadence: one-click masked replay after every data change, monthly full sweep | M5 pins | M5, M6 |
| S7 | **ARCHITECTURAL/UI BUILD** (next phase, per owner): human-first presentation, plain language (A-02), provenance small-print, performance & accessibility | UI-PLAIN-01 acceptance | A-02 |

**Every S-step's "gate" column is a harness output table — no gate passes on description alone.**

**Standing orders that never change:** data enters only through the one gate; nothing ships without the paired-test protocol (T1) and minimum-detectable-effect reporting (T2); every ship bumps the SOT pin (§14) and the ZONES trail.

---

## 9. What this plan changes vs today's app (v3.6.3)

| today | after S1–S6 |
|---|---|
| rated card depends on carried stamps/legacy records (G17 finding) | live derive or plain "not rated yet" — no hidden precompute |
| form stars null on live path | live form stars from store |
| no provenance on precomputed inputs | provenance panel on every number |
| no balance panel on NO CALL | balance always shown |
| calibration artifacts stale since imports | masked replay auto-regenerated on data change + monthly full sweep |
| systems approved on documentation | **approved only by harness test run on the omitted window (§5)** |
| cross-league = silent/standby | gated bridge from fit-to-results loop (§6), wins a place only on evidence |
| BTTS present-but-flagged | withheld (unchanged, I3) |
| 11 CZ1 rows misdated; MOL Cup 120/202 | corrected store (D-1/D-2 from the 2026-08-05 data audit) |

---

## 10. Explicitly NOT planned (so no one builds them by accident)

- Unified European ratings without the A-08 replay win (SOT open item 5 — proposed, never approved).
- Any market/odds input, feature, benchmark, sanity check or fallback (P1 — permanent).
- Injuries, lineups, transfers, congestion features (deferred by owner).
- Profitability claims (calibrated ≠ profitable; only calibration is claimed).
- Any UI that hides machine provenance behind "AI-style" confidence language (A-02: plain words, numbers provable).

*This plan supersedes nothing in the SOT; it is the SOT's §10/§11/§12 translated into one weighted buildable structure. Amendments to this document follow the SOT amendment register (A-xx, owner-approved).*
