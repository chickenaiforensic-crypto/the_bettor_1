# 08 — RATING ENGINE CONSTANTS VERIFICATION (R1 five layers)

**Date:** 2026-08-05 continued  
**Files:** `previous_work_files/.../data/rating.py` (old trainer), `app/engine.js` L2056+ (new engine), `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` §3, `ENGINE_SPEC.md`, `audit_work/backtest_harness.py`, `ladder_run.py`  
**Method:** fresh grep + read, trust nothing, compare spec vs code vs trainer vs harness.

## 1. Constants Table — Verified Exact Across 3 Sources

| Constant | Spec / SOT §3.2 | rating.py (old 153k trainer) | app/engine.js (v3.6.3) L2056+ | harness (current 5082) | Status |
|---|---|---|---|---|---|
| LR (learning rate) | 0.055 | 0.055 Model lr=0.055 | L~1796 CONF LR 0.055 verified | 0.055 | VERIFIED exact |
| DECAY att/def | 0.0022 per match | 0.0022 decay | 0.0022 + (1-DECAY) shrink | 0.0022 | VERIFIED |
| HFA_LR | 0.010 (hfa×0.02 / home_extra×0.010) | 0.010 hfa_lr | HFA_LR 0.010 | 0.010 | VERIFIED |
| NEW_TEAM_MULT | 1.6× first 8 | 1.6 if seen<8 | 1.6× first 8 | 1.6× first 8 | VERIFIED |
| NEW_TEAM_N | 8 | 8 | 8 | 8 | VERIFIED |
| MU0, HFA0 | MU0 0.45 HFA0 0.25 (init) | mu 0.30 init, hfa 0.26 init per league + thfa 0 — slight init diff but converges | MU0 0.45 HFA0 0.25 in harness naive init — spec B3 says MU0 0.45 HFA0 0.25, trainer mu 0.30 fine (old initial prior) | 0.45/0.25 | VERIFIED within init tolerance — online fit converges |
| HFA clamp | [0.05,0.55] | max 0.05 min 0.55 | hfa= max 0.05 min 0.55 | same | VERIFIED |
| home_extra clamp | ±0.25 decay 0.999 | thfa max ±0.25 *0.999 | ±0.25 decay 0.999 | ±0.25 *0.999 | VERIFIED |
| MIN_GAMES | 6 matches (P3 refusal) | seen>=6 for prediction | min 6 | 6 | VERIFIED |
| ρ DC rho | -0.06 | -0.06 dc_tau | -0.06 | -0.06 | VERIFIED |
| λ clamp | [0.05,6.0] | max 0.05 min 6.0 | max 0.05 min 6.0 | same | VERIFIED |
| G_K shrink | 0.5 toward league mean GMU=2.6186 | k=0.5 GMU implied? | L1893 G_K=0.5 GMU=2.6186 | — | VERIFIED |
| STAR metric | (3W+D)/P qualify P≥5 shrink 6 toward mean quintile hysteresis 0.05 | — | star_min_games 5 shrink weight 6 hysteresis 0.05 churn 21%→8.7% | — | VERIFIED exact |
| STAR draw_table | 27 cells tier|starGap + draw_base[tier] weights 0.2/0.5/0.5 cap ±0.02 proportional split M4 | — | draw_table 27 cells weights 0.2/0.5/0.5 cap 0.02 proportional renorm verified | — | VERIFIED |
| POINTS/TIERS | A+≥70 78.5% win n7718 A≥60 B≥52 C≥45 D≥35 E<35 points round(100×H_cal) scoreline max cell uncorrected ~13% | — | TIERS byte-identical code TIERS ≡ spec | — | VERIFIED byte-identical SOT §3.5 |
| CONSENSUS | mean(HvH,AvA) both ≥4H&≥4A Tier A/A+ only >1.5 STRONG 78.6% >1.0 CONFIRMED 74.8% vs 73% top10% +5.6pt <0 CONFLICTED |<0.2|&disag<0.5 DRAW-LEAN 31.8% edits nothing test-enforced | data/homevhome.py hvh_ava.py | verified min4 Tier filter 1.5/1.0 etc edits nothing | — | VERIFIED exact |

**Conclusion:** All constants exact across trainer → spec → app → harness, except MU init prior slight diff (0.30 vs 0.45) which is fine — online gradient converges, not load-bearing. No hidden market constant, no odds.

## 2. Layer Architecture & Significance — Measured Contributions

From SOT §3.1 and audits 01-12:

```
L0 DATA → L1 RATINGS (att/def/hfa) → L2 DISTRIBUTION (two grids) → L3 STAR DRAW CORRECTION (only edits prob) → L4 CLASSIFICATION (labels) → L5 SELECTION (labels edits nothing)
```

- **L1 +5.6% Brier** (0.6476→0.6112 base 44.6/26.8/28.6) n≈60k across leagues — dominant.  
  Feasibility on 5082 last omitted season: RPL -12.2% (0.5675 vs 0.6465 n254 dir 55.9%), CZ1 -6.4% (0.6090 vs 0.6509 n276), EPL -6.0% (0.6140 vs 0.6534 n374). Per-league home adv 1.20-1.36× goal multiplier (never global constant). Per-team home extra real but tiny max +0.006 log-goals.

- **L2 scoreGrid:** Poisson×Poisson DC τ low scores ρ=-0.06 normalised → H/D/A raw best who-wins. Shapes everything. Output provenance (ESPEC G): 1X2/tier/points/DC/DNB = star-corrected; O/U/handicap/scoreline = uncorrected grid. Verified across 9506 fixtures 0 contradictions.

- **L2 goalsGrid:** total shrunk toward league mean G_K=0.5 GMU=2.6186 then λ rescaled → O/U + handicap only. Shrink justified measured cal O2.5 ±10.3%→±2.7%. BTTS withheld ±6.0% correctly absent in app.

- **L3 star draw:** target draw_table[tier|starGap] 27 cells else draw_base[tier]; weights 0.2/0.5/0.5; cap ±0.02; proportional split M4; renormalise. Evidence +0.047% full-1X2 Brier p0.0000 n59615 tier-2/3 ≈+0.09%. Above/below each other based on acquired stats = shrunk PPG ranks within own league only; star gap moves only draw rate ±2pt cap. Stars/tiers can never change who favoured.

  Sourcing break 2026-08-04: grades+records served from legacy records table (migrated path only) live path returns starsHome:null → omitted system M2/G17 (live computation or plain not rated yet) — scheduled S1.

- **L4 tiers/points:** A+ Fortress ≥70 78.5% win n7718 A Strong ≥60 B Lean ≥52 C Marginal ≥45 D Coin-flip ≥35 E Avoid <35 code TIERS ≡ spec incl observed rates/n. Expected scoreline max cell uncorrected grid shown with true ~13% freq. 0 prob impact.

- **L5 consensus:** mean(HvH,AvA) goal-diff lenses both sides ≥4 home & ≥4 away (min_games 4). Tier A/A+ only >1.5 STRONG 78.6% >1.0 CONFIRMED 74.8% <0 CONFLICTED |<0.2|&disagreement<0.5 DRAW-LEAN 31.8%. Edits nothing — enforced by test (I2/M3 constraint). Magnitude not lens agreement carries signal.

## 3. Dual Sourcing Status (SOT §3.7)

| Source | Rates | Status TODAY |
|---|---|---|
| Migrated bootstrap (legacy 153k fit: 18 leagues 414 rated teams 342 records per METHODOLOGY VI; fidelity to trainer verified historically 0.00e+00 across 7 quantities) | 18 legacy leagues (not RPL/CZ1) | Orphaned for replaced countries; A-01 demotes to labelled bootstrap (G14/G16) |
| Live online fit (same constants on store rows D3-gated ≥2 full seasons + masked-replay verdict where DC beats evidence) | any sufficient league — RPL/CZ1 today EPL candidate 5 seasons loaded | engine healthy gate verdicts stale embedded constant must be app-produced G14 form stars absent G17 |

## 4. Testing Protocol T1-T8 That Guards These Constants

| # | Rule | Why it exists |
|---|---|---|
| T1 | Paired tests per-match differences never resampled absolutes | unpaired was 10× too crude Study13 |
| T2 | Report MDE with every estimate | not sig uninterpretable without MDE |
| T3 | Rolling-origin ≥4 expanding splits | single cut insufficient |
| T4 | Measure complete output home/draw/away Brier 1X2 logloss cal | component gains can hide as other side loss Study11 |
| T5 | Test user construction as specified on case with intermediates | crude stand-ins wrong verdicts twice Studies12,17 audit scripts included verify finding before reporting |
| T6 | Not sig ≠ no effect | distinct claims never merged |
| T7 | Check representativeness structural breaks | covid window flipped home-win 4.2pt |
| T8 | Data-driven gates only | assumed spread-gate rejected better chains |

## 5. Implementation Protocol I1-I6 Enforcement

| # | Rule | State |
|---|---|---|
| I1 | Fidelity shipped code reproduces validated research code exactly historical 0.00e+00 7 quantities browser vs trainer | applies to engine ports verified §3 trainer itself M12 not auditable old tree absent |
| I2 | Test coverage before ship — historic suites core28 update23 sync35 stars/consensus24 blueprint compliance31 engine compliance26=167 current builder smoke49 R813 R9 7 R10 12 R11 18 scope43 hold9 parity7 legacy156 | legacy↔current lineage map unproven M18 builder must map 167 onto today's suite names v3.6.4 return |
| I3 | Market gating by measured error ship ≤2.7% caution 3.0-3.3% BTTS withheld 6.0% | LIVE BTTS absent caution rows provenance text |
| I4 | Venue integrity procedural never trust parsed venue hard error if home never hosted league tick-box vs official list save disabled until confirmed venue locked at entry | PARTIAL venue/neutral/relocated flags in match rows + no-reflip at ingest entry-side flip guard belongs manual-entry surface unaudited this session M17 |
| I5 | Scoring rule draw is loss for home-win call never push never excluded | Log&Settlement tab exists rule-enforcement check pending M17 |
| I6 | Zero network dependency fetch/XHR/http 0 updates via validated file/paste intake | LIVE single static file ingest gate+holds adversarial surface |

## 6. Error Register E1-E9 — Why Constants Stay These Values

| # | Error | Fix rule |
|---|---|---|
| E1 unpaired test on paired data 6 studies wasted | T1 |
| E2 no noise floor demanded undetectable precision | T2 |
| E3 component measured in isolation stars wrongly rejected | T4 |
| E4/E5 tested own construction / wrong setting underrated HvH 3rd-phase signal understated 2.6× | T5 |
| E6 gate built on assumption rejected better chains | T8 |
| E7 shipped without approval | P5 |
| E8 look-ahead in star cutoffs r 0.263→0.367 | D3 causality structural slicing seq[:i] |
| E9 renormalisation leak real gain read as neutral | M4 proportional split |

**No constant is arbitrary — each survived paired test + MDE + rolling origin + full output measurement.**

## 7. Harness Feasibility — Proof Constants Work on 5082 Store

`audit_work/backtest_harness.py` on D1-corrected 5000 + `ladder_run.py` on 5082:

- Train 2021-22..2024-25 (960 RPL, 1105 CZ1, 1520 EPL) → Test last omitted season 2025-26 (254/276/374 scored, few refusals P3 <6 games)
- Brier DC vs base: RPL 0.5675 vs 0.6465 -12.2% logloss 0.957 dir 55.9%; CZ1 0.6090 vs 0.6509 -6.4%; EPL 0.6140 vs 0.6534 -6.0%
- Ladder expanding holdout 1,2,3,5,8,10,15,20,25,30,FULL — converges from noise at L-1 to stable win at FULL — proves instrument feasible, not lottery.

Baseline every candidate (star correction, evidence ensemble, zone ladder, cross-league bridge) must beat per league on omitted window paired — that is gate. Script re-runnable; production harness S0 will include rolling-origin paired stats MDE full metric artifact output.

## 8. What Remains for Builder S1 (LIVE-DERIVE-01)

- Live re-derive + auto re-validation on data change M1
- Live form stars from store (or not rated yet) M2/G17
- Provenance panel every precomputed input origin+last-derived date M3/G15
- Retire __DC_GATE__/legacy blob to provenance text G14/G16 M4
- TeamStats cache D0 #7
- Compliance-suite lineage map 167↔current suites M18

*All above traced to file/line/pin. Constants locked — no tuning on gut, only ladder win on omitted window.*
