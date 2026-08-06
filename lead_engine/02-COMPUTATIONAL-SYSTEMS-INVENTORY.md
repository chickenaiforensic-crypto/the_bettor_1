# 02 — COMPUTATIONAL SYSTEMS INVENTORY (All Systems, Weighted Significance)

**Date:** 2026-08-05  
**Purpose:** Cleanly map every computational system, where it lives, what it computes, and measured effectiveness — input to singular structural system.

## How This List Was Built

- Read SOT §2-§5 (R1/R2/R3 families), masterplan §2 weighting ledger, audits 01-24, `app/engine.js`, `chain/*.py`, `data/*.py`
- No market influence — zero — verified by grep `fetch|XMLHttpRequest|odds|price` = 0 in app (per builder binding rule #3)
- Trust nothing — old team omissions noted (form stars null, provenance missing, calibration stale, etc.)

## Master List — All Computation

### DATA SUBSTRATE (P1/P2)

| ID | Name | Location | Input | Output | Measured |
|---|---|---|---|---|---|
| D0 | Store | `store.matches` + `identities` | completed 90-min results only | canon teams, aliased names, date, competition, score | 5082 verified, 0 dup, 0 future |
| D1 | Ingest Gate | `PR.ingest` L709 app-v3.6.3 | pack .txt | clean|held Z-003|rejected, rejections never stored | grammar + completeness + 90-min L887 + COMP_TYPES L737 + dedupe L321/L1016 + no future + tie linkage | LIVE |
| D2 | Dedupe | L321/L1016 | fingerprint date+canon(pair)+comp | add-if-new, skip existing | 0 dup in 5082 |
| D3 | Scope/Mute/Purge | `scopeView` L3369, `muteScope` L2928, `purgeScope` L2957 | country (+ competition) | preview counts → confirm → mute (soft) vs purge (hard) backup-gated L3433-3451 | backup auto-download rule live |
| D4 | Migration | `migrate` L519 | full JSON backup | atomic replace whole store | log seq 4,8,9 |
| D5 | Backup | `exportFull` L491 | store+log | wrapper format/version/schemaVersion/exportedAt + store+log | 5082 file verified |

### R1 RATING ENGINE — 5 Layers (ESPEC Part A)

| ID | Layer | Location | Constants | Input → Output | Measured Gain | Weight |
|---|---|---|---|---|---|---|
| R1-L1 | Dixon-Coles Live Fit | `fit()` L2056+, CONF L~1796, `audit_work/backtest_harness.py` | LR 0.055, DECAY 0.0022, HFA_LR 0.010 (hfa×0.02/home_extra×0.010), NEW_TEAM 1.6× first 8, HFA clamp [0.05,0.55], home_extra ±0.25 decay 0.999, min 6 matches, ρ -0.06, MU0 0.45 HFA0 0.25, per-league home 1.20-1.36×, MU 2.6186, G_K 0.5 | date-ordered matches → att/def/hfa/home_extra per team/league, λ_home, λ_away clamp [0.05,6.0] | Brier 0.6112 vs 0.6476 base = +5.6%, calibration ≤1.7%, RPL -12.2% vs base on last omitted season (2025-26), CZ1 -6.4%, EPL -6.0% (feasibility run) | DOMINANT — probability is this |
| R1-L2a | scoreGrid | `scoreGrid` | DC ρ -0.06, Poisson n=10 grid, normalised | λ pair → H/D/A distribution (raw best who-wins) | shapes everything | CORE |
| R1-L2b | goalsGrid | L1893 | G_K 0.5 shrink toward league mean GMU 2.6186 | λ pair → O/U + handicap only | O2.5 error 10.3%→2.7%, BTTS 6.0% withheld correctly | SEPARATE family — never merge with 1X2 |
| R1-L3 | Star Draw Correction | ESPEC D, draw_table[tier|gap] 27 cells + draw_base[tier], weights 0.2/0.5/0.5 | metric (3W+D)/P, qualify P≥5, shrink weight 6 toward league mean, stars 1..5 quintile within league, hysteresis 0.05 churn 21%→8.7%, cap ±0.02, proportional renormalisation M4 rule | corrected prob H_cal D_cal A_cal (never moves favourite) | +0.047% full-1X2 Brier p<0.0000 n=59615, tier-2/3 +0.09% | REAL SMALL — may edit L2 capped |
| R1-L4 | Tiers/Points | ESPEC E, TIERS | points round(100×H_cal), bands A+ Fortress ≥70 78.5% win n7718, A Strong ≥60, B Lean ≥52, C Marginal ≥45, D Coin-flip ≥35, E Avoid <35, expected scoreline max cell uncorrected grid ~13% freq | labels from corrected prob | 0 prob impact, readability | DISPLAY — must match observed rates |
| R1-L5 | Consensus | ESPEC F | min_games 4 home+4 away both sides, Tier A/A+ only: >1.5 STRONG 78.6%, >1.0 CONFIRMED 74.8% vs 73.0% model top-10% +5.6pt, <0 CONFLICTED, \|<0.2\|&disagreement<0.5 DRAW-LEAN 31.8%, mean(HvH,AvA) goal-diff lenses | selection filter, edits nothing enforced by test | +5.6pt over top-10% model but filter only | FILTER ONLY — never edits prob |

Dual sourcing note: migrated bootstrap 18 leagues 414 rated teams 342 records orphaned for replaced countries per A-01 → demoted to provenance text only (M3). Live path = online fit per league, replay-gated.

### R2 EVIDENCE ENGINE — Match-History Graph (LIVE-BLUEPRINT)

| ID | Module | Location | Input → Output | Measured | Gate to Stay |
|---|---|---|---|---|---|
| R2-1 | identity_store | L264-330 | canon/aliases | substrate | LIVE |
| R2-2 | match_store | app | date+venue+score+tieId+neutral | substrate + 90-min doctrine + AET→NOTE | LIVE |
| R2-3 | evidence_graph | L1506-1609 | prior results seq[:i] strict causality → h2h/common/3rd+opponent-of-opponent paths, effective/agree/nocall | path discovery | LIVE |
| R2-4 | zone ladder | blueprint §4/mod6 | path → calibrated zone STRONG→TOSS with n/spread/calibration | STRONG 78%/92% pair n59, WIN 67/82, WIN-DRAW 49/75, lean 47, toss 45 monotone | held-out calibration — confidence band, NOT prob |
| R2-5 | balance panel | M7 partial | home/draw/away support shares, NO CALL must show balance | missing in v3.6.3 | S3 build — full build needs held-out cal |
| R2-6 | cross_border_bridge | M9 standby | disconnected league ties, 2778 Euro matches | r +0.274 n693 62.6% dir on 3rd phase, two defects: usability gate disproven, path discovery too narrow | held-out win vs frozen 1.00 baseline (A-08) |
| R2-7 | confidence_calibrator | partial | gentle shrink, versioned tables | gate+labels live, artifacts stale M5 | S0 one-click masked replay post any data change, monthly full sweep |
| R2-8 | goal_range_model 0-1/2/3+ bins | M8 not built | own calibration | promise, no win yet | after M7, held-out win |
| R2-9 | audit_log | LIVE | versions, settlement Brier/log-loss | append-only | LIVE |

Weighting candidates W1-W4 (phase weights H2H/common/3rd): NOT operational — need held-out win vs unweighted baseline.

Rejected: Recency weighting C6 84/84 no discrimination → dead; Venue correction+sat A no gain → dead + reverted; Spread-based gate tight worse → dead (E6).

### R3 ELO / PERFORMANCE LAYER

| ID | Name | Location | Constants | Input → Output | Measured | Weight |
|---|---|---|---|---|---|---|
| R3-1 | ELO stars | CAL8 port in app, not in foundation docs | INIT 1500 K20 home+65 star=clamp((ELO-1420)/2 0..100)→1-5★ perf window6 min3 causal before cutoff | quick ordinal strength reading 1-5★ + perfView L2512 last-6 | unvalidated vs outcomes | DISPLAY ONLY — adopt display-only per A-03, label "not a prediction" |

### CALIBRATION / HONESTY SHELL (P3)

| ID | Name | Location | Rule |
|---|---|---|---|
| C1 | Refusal paths | masterplan §3 | League without replay win → evidence-only plain label A-01; team<6 no rating, <5 no stars/draw, <4 home/away no consensus; venue unproven hard error save disabled I4; cross-league without validated bridge → chain evidence or NO CALL + balance M7; BTTS withheld I3 |
| C2 | Settlement | Log&Settlement tab L3529-3536 | draw=loss for home call never push/excluded I5 — feeds calibration, pending audit M17 |
| C3 | Masked replay | Calibration tab L3517-3527 Run masked replay | later info hidden, model predicts, results compared, artifacts replaced only when validation numbers written (n/window/Brier/score/date), artifacts store `dc-fitted-*` L1902-1912 |
| C4 | Provenance panel | M3 omitted | every precomputed input origin+last-derived date — required for v3.6.4 G15 |
| C5 | TeamStats cache | M6 empty since migration | reconciliation-only FORM rows never hidden compute input L1053 |
| C6 | Integrity & Snapshots | L3537-3547 | muted rows kept visible excluded every calc never deleted doctrine exclusion=MUTE, restore button L3542, snapshots taken before every data commit L3548 + purge hash snapshots scope-post |

## Significance Order (Measured)

Dominant → Real Small → Display/Filter → Standby → Dead

1. **L1 DC live fit** +5.6% Brier — provides probability
2. **L2 grids** — shape distributions, goals separate family
3. **L3 star draw** +0.047% Brier capped ±0.02 — only layer allowed to edit prob, small real, never moves favourite
4. **R2 zone ladder** monotone calibrated — confidence band, not prob
5. **R2 chain** r+0.274 — standby cross-border
6. **L5 consensus** filter-only STRONG 78.6% — never edits prob
7. **L4 tiers** display 78.5% observed — readability
8. **R3 ELO stars** display-only
9. **Goal-range bins** not built — gated
10. **Recency/venue-correction/spread-gate** dead — measured failures, do NOT rebuild

Weighting rule (singular engine constitution): no component may consume another's output unless rank higher or display-only. Enforced in code by tests.

## Zero Market Influence — Proof

- Ingest grammar has no odds fields; engine has no odds input (SOT §1, FUNCTIONALITY §13)
- `grep -R "fetch\|XMLHttpRequest\|odds\|price\|bookmaker" previous_work.../APP-V3.6.3/` = 0 for network, 0 for market (per builder rule #3)
- Settlement rule draw=loss not push, never profit claim
- Calibration = own masked replay Brier/logloss, not vs market
- METHODOLOGY P1 SUSPENDED historical Gate1 market-based conclusion pending outcome-only re-test — market never evidence

*All above traced to file/line/pin. Next → weighting matrix formalises this into numeric weights for singular engine.*
