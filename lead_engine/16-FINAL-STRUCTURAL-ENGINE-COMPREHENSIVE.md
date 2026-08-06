# 16 — FINAL STRUCTURAL ENGINE COMPREHENSIVE (Zero-Market, Weighted, Singular)

**Date:** 2026-08-05 final — after team on task, auditor 5082 closure, owner clarifications integrated, current-form experiments v1/v2  
**Status:** LOCKED — single structural system that produces best computational wins, ready for architectural build  
**Authority:** SOT v1.3 §0-§14, Masterplan v1.1 §1-§10, Functionality v1.0, Verification v1.0, 01-15 audits, ladder baseline, fresh_audit, current_form_blend v1/v2 experiments  
**Compliance:** P1 no market in any role · P2 results only · P3 I don't know valid · P4 foundation→validation→superstructure · P5 shipping needs owner approval · T1-T8 testing · I1-I6 implementation · D14 scope frozen except UEFA approved

---

## Executive Summary (Smooth English, For Owner)

One store of 5,082 verified real results is the only fuel — England 1,900, Czech 1,603, Russia 1,579 — 0 duplicates, 0 future dates, 609 teams, every row checked against RSSSF archives + legacy 202k dataset, 0 fabricated. Verified fresh via `audit_work/fresh_audit.py` pins EXACT: original 5000 SHA256 `c7b29e85…8fc00` = SOT pin, operational 5082 `c9ad6a54…` closed.

Three computation families collapsed into one weighted singular system whose components are ranked by measured effectiveness, not preference:

**Dominant — the probability:** L1 Dixon-Coles live fit per-league LR0.055 DECAY0.0022 HFA_LR0.010 1.6× first 8 HFA clamp [0.05,0.55] home_extra ±0.25 decay 0.999 min6 ρ-0.06 λ[0.05,6.0] — online gradient per result, att/def goes up/down, app alive. Measured +5.6% Brier vs base (0.6476→0.6112) + feasibility on last hidden season 2025-26: RPL -12.2% Brier 0.5675 vs 0.6465 n254 dir 55.9%, CZ1 -6.4%, EPL -6.0% — ladder L-1→FULL converges noise→stable win.

**Core — shapes distribution:** L2 scoreGrid Poisson×Poisson DC τ low scores ρ-0.06 normalised → H/D/A raw best who-wins, max cell ~13% freq; goalsGrid shrunk G_K0.5 GMU2.6186 → O/U handicap separate family, O2.5 error 10.3%→2.7% shrinks toward league mean, BTTS withheld 6.0% correctly absent.

**Real small — only layer allowed to edit probability capped:** L3 star draw correction metric (3W+D)/P P≥5 shrink weight 6 toward mean quintile within league hysteresis 0.05 churn 21%→8.7%, target draw_table[tier|starGap] 27 cells else base weights 0.2/0.5/0.5 cap ±0.02 proportional renorm M4 never moves favourite — measured +0.047% full-1X2 Brier p<0.0000 n59615 tier-2/3 +0.09%.

**Confidence not probability:** R2 zone ladder STRONG→TOSS calibrated STRONG 78%/92% pair n59 WIN 67/82 WIN-DRAW 49/75 lean 47 toss 45 monotone gentle shrink versioned tables, always carries n/spread/calibration.

**Standby cross-border:** R2 chain phase2 shared opponent avg_gd diff + phase3 opponent-of-opponent est=ax+xy-yb r+0.274 n693 62.6% direction 2778 Euro matches, 2 defects usability gate disproven (tight spread worse r0.195 vs 0.384) + path discovery narrow — standby. League pivot s[L] per-league X points above/below from Euro connector Euro bias loop bias(L)=mean(predicted GD-actual) s[L]←s[L]-step*bias step0.05-0.1 20-50 iter bias<0.02, validated weighted vs frozen 1.00 baseline on last Euro hidden window — owner's bump-up/calibrate mechanism formalised.

**Filter only & display only:** L5 consensus mean(HvH,AvA) both ≥4H≥4A Tier A/A+ >1.5 STRONG 78.6% >1.0 CONFIRMED 74.8% vs 73% top10% +5.6pt <0 CONFLICTED etc edits nothing test-enforced; L4 tiers A+≥70 78.5% win n7718 etc 0 prob readability; R3 ELO stars INIT1500 K20 home+65 star clamp((ELO-1420)/2 0..100)→1-5★ window6 min3 causal perfView last-6 quick ordinal not prediction.

**Future gated:** goal-range bins 0-1/2/3+ M8 not built, current performance blend owner clarified but tested v1 generic recent 6 α0.35 degrades Brier -0.00963/-0.00415/-0.00802 t -0.68 to -1.92 NOT BETTER, v2 playoff-only α0.15 used 0% in 2025-26 regular test (relegation playoffs only 20 at season end) so safe 0 diff but no benefit yet — needs promotion playoff data + retune α 0.15-0.20 ELO-based efficiency relative to expectation.

Weighting rule (constitution): no component may consume higher-ranked output unless higher or display-only. L3 may edit L2 draw capped, current blend may edit via α capped gated, L5/R2/R3 never edit L1-L3 enforced by tests + grep.

Zero market proof: ingest grammar has no odds fields, engine has no odds input, grep fetch/XMLHttpRequest/odds/price/bookmaker =0, settlement draw=loss never push I5, calibration own masked replay Brier/logloss not vs market, historical Gate1 market-based conclusion SUSPENDED per P1.

Best computational wins = highest calibrated accuracy each output can carry on own data measured by masked replay Brier/logloss/calibration per market + settlement ledger I5 — NOT vs bookmaker P1 forbids — NOT hit rate.

---

## 1. One-Page Map — Singular Flow

```
STORE 5082 verified 90-min results only P1/P2 identity·date·venue·score·tieId·source D3 seq[:i] strict causality
  | every derive causality before cutoff
  |--> L1 LIVE DC FIT per-league online LR0.055 DECAY0.0022 HFA_LR0.010 1.6×/8 ρ-0.06 clamp [0.05,6.0] HFA[0.05,0.55] home_extra±0.25 decay0.999 min6 → per-team att/def up/down app alive 📈📉
  |      v
  |--> L2 TWO GRIDS scoreGrid Poisson DC τ → H/D/A raw best who-wins max ~13% | goalsGrid shrunk G_K0.5 GMU2.6186 → O/U handicap separate BTTS withheld 6%
  |      v
  |--> L3 STAR DRAW (3W+D)/P P≥5 shrink6 quintile hyst0.05 draw_table 27 cells cap±0.02 proportional M4 never moves fav +0.047% Brier
  |      v
  |--> CURRENT FORM BLEND (owner) gate ≥6 recent or ≥3 playoff GD diff>0.5 α capped 0.15-0.35 (1-α)base+αrecent playoff-only v2 safe 0% usage in 2025-26 regular — candidate S4
  |      v
  |--> VERDICT CARD PROBABILITY provenance-tagged M3 small-print 📅✅
  |
  |--> R2 EVIDENCE GRAPH H2H·common·3rd+opponent-of-opponent phase paths effective/agree/nocall causal
  |      |--> ZONE LADDER STRONG→TOSS calibrated rates WITH n/spread/calibration 78%/92% n59 monotone → confidence band not prob
  |      |--> BALANCE PANEL M7 home/draw/away support shares NO CALL must show ⚖️
  |      |--> CHAIN CROSS-BORDER r+0.274 n693 62.6% dir standby → LEAGUE PIVOT s[L] per-league X points above/below 🌍 bias loop 20-50 iter bias<0.02 validated weighted vs 1.00 frozen on last Euro omitted window A-08
  |
  |--> R3 ELO DISPLAY-ONLY INIT1500 K20 home+65 star clamp→1-5★ window6 min3 causal last-6 perfView
  |--> L4 TIERS A+≥70 78.5% n7718 etc readability | L5 CONSENSUS mean(HvH,AvA) ≥4H≥4A Tier A/A+ >1.5 STRONG 78.6% filter only
  |
  v
VERDICT CARD ONE OUTPUT smooth English: verdict sentence "Arsenal 62% to win at home" + icons 🛡️📈⚡🌍🔗⚖️ + why + confidence STRONG 78% (n=59) + current form tracked + balance if NO CALL + provenance small-print 📅✅
  |
  v
SETTLEMENT draw=loss never push I5 → calibration feedback M5 masked replay auto after data change monthly sweep
```

## 2. Weighting Effectiveness Matrix — Final Locked

| Rank | Component | Answers | Measured | Weight | Role | Gate to Stay |
|---|---|---|---|---|---|---|
| 1 | L1 DC live fit per-league | who wins how much λ | Brier 0.6112 vs 0.6476 +5.6% RPL -12.2% 0.5675 vs 0.6465 n254 CZ1 -6.4% EPL -6.0% cal ≤1.7% home 1.20-1.36× | 1.00 ref | probability | masked replay beats evidence+base auto re-run M1 paired T1 MDE T2 |
| 2 | L2 scoreGrid / goalsGrid | H/D/A shape / O/U handicap | max cell ~13% O2.5 10.3%→2.7% BTTS 6.0% withheld | 1.00 tied / separate family | distribution | cal ≤2.7% I3 |
| 3 | L3 star draw | draw refinement only | +0.047% Brier p<0.0000 n59615 tier2/3 +0.09% cap±0.02 churn21%→8.7% | 0.15 correction | edits draw capped | paired all5 T4 cap favourite preserved |
| 3b | Current form blend | hot team weighted inclusion if efficient | v1 generic recent6 α0.35 diff -0.00963/-0.00415/-0.00802 t -0.68 to -1.92 NOT BETTER degrades, v2 playoff-only α0.15 used 0% safe 0 diff | α 0-0.5 gated ≥6 recent or ≥3 playoff GD>0.5 capped | candidate weighted inclusion | must beat base-only on omitted window paired to ship S4 |
| 4 | R2 zone ladder | confidence band not prob | STRONG 78%/92% n59 WIN67/82 etc monotone | confidence | confidence band + n/spread/cal | held-out cal |
| 5 | R2 chain + league pivot s[L] | cross-league evidence / rated bridge | r+0.274 n693 62.6% dir 2778 Euro matches range few goals per match enough to matter pivot X points above/below | standby → gated rated bridge | balance panel M7 + cross-league rated if harness win vs 1.00 frozen | harness win vs frozen baseline A-08 §6 bias loop |
| 6 | L5 consensus | selection filter | STRONG78.6% CONFIRMED74.8% vs73% top10% +5.6pt | filter only | filter display | edits nothing test |
| 7 | L4 tiers | readability | 0 prob A+≥70 78.5% n7718 etc | readability | labels must match observed | — |
| 8 | R3 ELO stars | quick ordinal | unvalidated ordinal | display only | 1-5★ not prediction | A-03 display-only |

## 3. Computation Contract Final

| Layer | MUST | MUST NOT |
|---|---|---|
| L1 | fit online date order seq[:i] causality constants LR0.055 DECAY0.0022 HFA_LR0.010 1.6×/8 ρ-0.06 clamp [0.05,6.0] HFA[0.05,0.55] home_extra±0.25*0.999 min6 P3 per-team up/down app alive | use carried params fit future global home constant |
| L2 | two grids separated goals shrunk GMU2.6186 | star leak into goals |
| L3 | draw_table 0.2/0.5/0.5 ±0.02 cap proportional M4 metric P≥5 shrink6 quintile hyst0.05 never moves fav | move fav exceed cap edit goals |
| Current form | gate ≥6 recent or ≥3 playoff GD diff>0.5 α capped 0.15-0.35 playoff-only 0.15 retuned blend (1-α)base+αrecent avg total preserved efficiency relative to expectation ELO optional | use without gate dominate base no cap generic recent without playoff filter |
| R2 chain+ pivot | paths only prior results zone or NO CALL balance always M7 league pivot s[L] from Euro bias loop step0.05-0.1 20-50 iter bias<0.02 validated weighted vs 1.00 frozen on last Euro omitted window | dress shares as prob arbitrary multiplier split identities |
| R3 | compute stars live window6 min3 causal | edit R1/R2 claim pred |
| Output | smooth English main sentence + icons 🛡️📈⚡🌍🔗⚖️ with tooltip + provenance small-print source/window/n/cal/date M3 + honest NO CALL + balance bar | bot scattered numbers silent precompute market refs P1 forced number |

## 4. Data Side CLOSED — Verification

- Pins EXACT via fresh_audit.py: original 5000 c7b29e85…8fc00 = SOT §14, operational 5082 c9ad6a54… CLOSED, 0 dup fingerprints PASS, 0 future PASS, 609 identities, per-comp counts ENG1900 CZE1381( +20 playoffs +202 MOL)=1603 RUS1216+20+341+2=1579, D1 11 date errors fixed, D2 MOL 82 merged 90-min doctrine AET, legacy cross-diff 0 mismatches vs 202k dataset.
- Table reproduction smoke: RPL 2023-24 240 rows 16 teams Zenit 57, CZ1 2022-23/2025-26 16 unique teams — full RSSSF parser rsssf_verify.py does 16/16 exact.
- Team verified via ROLE-AUDITOR fresh code — script inventory fresh_audit.py pack_parse.py rsssf_verify.py.
- Recommended next S0 harness productionisation + M10 outcomes-only integrity screen (own-model collapse detection never price P1).

## 5. Build Order S0-S7 — Gates Are Harness Output Tables

| Step | Work | Gate artifact | Ledger |
|---|---|---|---|
| S0 | Harness productionise rolling-origin paired T1 MDE T2 full metrics artifact | self-check vs ladder baseline RPL 0.5675 -12.2% etc | — |
| S1 | LIVE-DERIVE-01 live re-derive auto re-validation provenance M3 retire __DC_GATE__/legacy blob live form stars + current form gate | G14/G15/G16/G17 | M1 M2 M3 M4 M16 M18 |
| S2 | Settlement venue-guard I5 draw=loss I4 | M17 | M17 |
| S3 | Balance panel NO CALL support shares ⚖️ | held-out cal | M7 |
| S4 | Goal-range bins 0-1/2/3+ + current form blend α (owner) | harness win vs base-only omitted window | M8 + current form candidate |
| S5 | UEFA connector #17 → chain + league pivot s[L] bias loop → weighted vs 1.00 frozen | A-08 | M9 M19 |
| S6 | Calibration cadence one-click masked replay after any data change monthly full sweep + M10 outcomes-only screen | M5 M6 M10 | M5 M6 |
| S7 | Architectural/UI build human-first smooth English icons with context per 11,15 | UI-PLAIN-01 | A-02 |

Every gate is harness output table — artifact IS approval record, numbers in chat are not.

## 6. What Changes vs v3.6.3 Today

| today v3.6.3 md5 17dd2b... | after S0-S6 locked v2 |
|---|---|
| rated card depends on carried stamps/legacy records G17 | live derive or plain not rated yet no hidden precompute |
| form stars null live path | live form stars from store window6 min3 + current form tracked not weighted until wins |
| no provenance | provenance panel source/window/n/cal/date M3 small-print |
| no balance panel on NO CALL | balance always shown ⚖️ bar chart |
| calibration artifacts stale since imports | masked replay auto-regenerated on data change + monthly full sweep M5 |
| systems approved on documentation | approved only by harness test run on omitted window §5 |
| cross-league silent/standby | gated bridge §6 s[L] pivot X points above/below wins place only on evidence |
| BTTS present-but-flagged | withheld I3 unchanged |
| 11 CZ1 misdated 120 vs 202 MOL | corrected store D-1/D-2 5082 |

## 7. NOT Planned

- Unified European ratings without A-08 replay win (open item 5 proposed never approved)
- Any market/odds input feature benchmark sanity check fallback P1 permanent
- Injuries lineups xG etc deferred owner
- Profitability claims calibrated≠profitable only calibration claimed
- UI that hides provenance behind AI-style confidence language A-02 plain words numbers provable

## 8. Pins Live Authority

- SOT v1.3, METHODOLOGY 6cd6c..., ENGINE_SPEC 91cd0c..., LIVE-BLUEPRINT d01cf..., App v3.6.3 md5 17dd2b5b..., Store 5000 sha c7b29e85..., D1 corrected abd0c207..., 5082 closed c9ad6a54..., Audit card b9e177..., MOL FULLSPAN 202 md5 f2ee000..., old 120 md5 662fe5d... SUPERSEDED, Harness baseline ladder_baseline_2026-08-05.json RPL -12.2% etc, fresh_audit.py pins EXACT, current_form_blend v1/v2 experiments DEGRADES 0 diff safe.

*Living doc amendments per SOT A-xx owner-approved. Everything asserted traces to doc section code line or pinned file — no stories. Trust nothing, measure everything, approve by test run only. Smooth English delivery with icons context.*

---

## Best Computational Wins Defined (Owner Purpose)

- Highest calibrated accuracy each output can carry on own data — measured by masked replay Brier/logloss/calibration per market + settlement ledger I5 draw=loss — NOT vs bookmaker P1 forbids — NOT hit rate.
- Singular system removes second rating universe, removes hidden precompute, forces live derive or plain not rated yet, shows balance on NO CALL, shows provenance small-print, icons with context.
- Per-team live + per-league pivot + current form gated makes app alive when takes results + cross-league accurate/real-world + efficient teams get weighted inclusion only if minimum playoffs evaluation passes harness gate.

*Ready for architectural build after S0-S6.*
