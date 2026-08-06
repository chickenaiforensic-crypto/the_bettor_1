# 13 — Singular Engine LOCKED v2 — With Owner Cross-League + Live + Current Form Clarification (Smooth English)

**Date:** 2026-08-05 continued  
**Version:** LOCKED v2 — upgrades v1 with owner clarification 10 + human-friendly delivery 11 + auditor closure 12  
**Status:** READY FOR BUILD — S0-S6 gates by test run, then S7 architecture human-friendly

---

## In Smooth English — What The System Is (For Humans, Not Bots)

**One store of real results is the only fuel.** 5,082 verified games — England 1,900, Czech 1,603, Russia 1,579 — every row checked against RSSSF archives, 0 duplicates, 0 future dates. No odds, no market, ever.

**Three things make it alive and real-world accurate:**

### 1. 🌍 Per-League Pivot — So Cross-League Predictions Are Real

Every team is first rated inside its own league. Arsenal only knows Premier League, Sparta only Czech league.

When English and Czech teams actually met in Europe (Champions League, Europa, Conference + qualifiers), we measured: did our per-league ratings predict those Euro scores correctly?

If English teams beat Czech teams by 0.4 goals MORE than we predicted, we bump English league up and Czech league down — a little bit at a time — until predictions match real Euro results.

The bump is called **league pivot points**. After fit, you can say: Premier League pivots +0.20 points above Czech league (based on 42 direct Euro meetings, bias converged to 0.01). Then any cross-league game (Arsenal vs Dynamo Moscow) uses team rating + league pivot on one common scale.

No UEFA coefficient tables — only direct results. That's why live computations stay real-world.

**How it fits:** `s[L]` league pivot, init 0, bias(L)=mean(predicted GD - actual GD) over Euro ties involving L, update `s[L] ← s[L] - step*bias` step 0.05-0.1, iterate 20-50 times until bias<0.02, validate weighted vs frozen 0 baseline on last hidden Euro season. If weighted wins, adopt; if not, say plain "no calibrated bridge" + show chain evidence.

### 2. 📈 Per-Team Rating Goes Up/Down — App Is Alive

Every time a new result comes in, four numbers for those two teams move:

- Attack up if they scored more than expected, down if less
- Defence up (better) if they conceded less than expected
- Home advantage for league and extra home for team — tiny adjustments
- All shrink a little (0.0022 per match) toward average so old form fades

A team needs 6 games before we rate it — otherwise we honestly say "not rated yet, need 6 matches" (P3 honesty).

So ratings go up after wins above expectation, down after poor results. The app is alive — every new row changes tomorrow's predictions.

**Icon:** 📈 ↑ if rating up last 3, 📉 ↓ if down, with small print: "Live from 960 games, last update 2026-08-02, beat base 12.2% on hidden season".

### 3. ⚡ Current Performance — Weighted Inclusion If Hot

If a team suddenly plays much better than its long-term base, we give current form extra weight — but only if we have enough recent proof.

- **Base rating:** long-term (≥2 seasons, ~60 games) — stable.
- **Current form:** short-term last 6 games (W-D-L + GD) or minimum playoffs (e.g., 3 playoff ties) — hot/cold.
- **Gate:** Only if ≥6 recent or ≥3 playoff matches in last 60 days, both home and away recent present, and current GD differs from base by >0.5 goals/match.
- **Weighting:** Blend final = (1-α)*base + α*current, α capped 30-50% max, proportional to how many recent games meet gate. So hot team gets 35% extra credit, but never dominates.

Example smooth English: "Sparta hot ⚡ — last 6: W5 L1 GD +8 vs base +2.3 — weighted 35% into this tip."

If gate not met, we ignore current form — base only. This prevents overreacting to one lucky win.

**Entry test:** Blend must beat base-only on last hidden season, paired Brier + direction, with MDE. Old recency 84/84 no discrimination rejected because it had no gate and no cap — this version has gate + cap + playoff filter, so it can pass.

---

## The One Weighted System (Locked)

```
STORE 5082 verified (ENG1900 CZE1603 RUS1579) 0 dup 0 future 609 teams
  | strict causality seq[:i] before cutoff
  |
  |--> L1 LIVE FIT per-league LR0.055 DECAY0.0022 HFA_LR0.010 1.6×/8 clamp [0.05,6.0] HFA[0.05,0.55] home_extra±0.25*0.999 min6 ρ-0.06
  |      live per-team att/def goes up/down on results → app alive
  |      v
  |--> L2 TWO GRIDS scoreGrid Poisson×Poisson DC τ→H/D/A raw best who-wins | goalsGrid shrunk G_K0.5 GMU2.6186→O/U handicap BTTS withheld 6%
  |      v
  |--> L3 STAR DRAW (3W+D)/P P≥5 shrink6 quintile hyst0.05 draw_table 27 cells else base weights0.2/0.5/0.5 cap±0.02 proportional M4 never moves fav +0.047% Brier
  |      v
  |--> CURRENT FORM BLEND (owner clarified) gate ≥6 recent or ≥3 playoff GD diff>0.5 α capped 30-50% = (1-α)base+αcurrent → weighted inclusion if efficient
  |      v
  |--> VERDICT CARD PROBABILITY provenance-tagged M3 small print
  |
  |--> R2 EVIDENCE GRAPH H2H·common·3rd phase paths effective/agree/nocall causal
  |      |--> ZONE LADDER STRONG→TOSS calibrated 78%/92% n59 etc monotone → confidence band not prob
  |      |--> BALANCE PANEL M7 home/draw/away support shares NO CALL must show ⚖️
  |      |--> CHAIN CROSS-BORDER r+0.274 n693 62.6% dir 2778 Euro matches standby
  |           |--> LEAGUE PIVOT s[L] per-league X points above/below from Euro bias loop fit → 🌍 common scale for cross-league
  |
  |--> R3 ELO DISPLAY-ONLY INIT1500 K20 home+65 star clamp((ELO-1420)/2)→1-5★ window6 min3 causal perfView last-6
  |--> L4 TIERS A+≥70 78.5% n7718 etc points round(100×H_cal) readability
  |--> L5 CONSENSUS mean(HvH,AvA) ≥4H≥4A Tier A/A+ >1.5 STRONG 78.6% >1.0 CONFIRMED 74.8% filter only
  |
  v
VERDICT CARD ONE OUTPUT smooth English:
  verdict sentence "Arsenal 62% to win at home" + icons 🛡️📈⚡🌍 + why + confidence STRONG 78% (n=59) + current form 35% + balance if NO CALL + provenance small print 📅✅
  |
  v
SETTLEMENT draw=loss never push I5 → calibration feedback M5 masked replay auto after data change monthly sweep
```

## Weighting Constitution (Same as v1, Plus Current Form)

| Rank | Component | Gain | Weight | Verdict Role |
|---|---|---|---|---|
| 1 | L1 DC live fit | +5.6% Brier + RPL -12.2% etc | 1.00 ref | probability |
| 2 | L2 scoreGrid | shapes H/D/A | 1.00 tied | distribution |
| 3 | L2 goalsGrid | O2.5 10.3%→2.7% | separate | O/U handicap |
| 4 | L3 star draw | +0.047% Brier p<0.0000 | 0.15 correction | draw only capped |
| 4b | Current form blend | candidate — must beat base-only on omitted window paired | α 0-0.5 capped gated ≥6 recent/≥3 playoff GD>0.5 | weighted inclusion if hot |
| 5 | R2 zone ladder | monotone 78%/92% etc | confidence | confidence band |
| 6 | R2 chain + league pivot s[L] | r+0.274 62.6% dir + pivot X points above/below from Euro bias loop | standby → gated rated bridge | balance + cross-league rated if harness win vs 1.00 frozen |
| 7 | L5 consensus | +5.6pt over top10% filter | filter only | selection filter |
| 8 | L4 tiers | 0 prob | readability | labels |
| 9 | R3 ELO stars | unvalidated ordinal | display | 1-5★ not pred |

No component may consume higher-ranked output unless higher or display-only. L3 may edit L2 draw capped; current blend may edit L1/L2 via α capped; L5/R2/R3 never edit L1-L3.

## Computation Contract v2 (Updated With Clarifications)

| Layer | MUST | MUST NOT |
|---|---|---|
| L1 live per-team | fit online date order seq[:i] constants as above min6 P3 att/def up/down on results shrink 0.0022 | use carried params, fit future, global home constant |
| L2 | two grids separated goals shrunk GMU2.6186 | star leak into goals |
| L3 | draw_table 0.2/0.5/0.5 cap±0.02 proportional M4 P≥5 shrink6 quintile hyst0.05 | move fav exceed cap |
| Current form | gate ≥6 recent or ≥3 playoff GD diff>0.5 α capped 30-50% blend (1-α)base+αcurrent, perfView last-6 | use without gate, dominate base, no cap |
| R2 chain + pivot | paths only prior results, zone or NO CALL balance always M7, league pivot s[L] from Euro bias loop step0.05-0.1 20-50 iter bias<0.02, validated weighted vs 1.00 frozen on last Euro omitted window | dress shares as prob, arbitrary multiplier, split identities |
| R3 | compute stars live window6 min3 | edit R1/R2 claim pred |
| Output | smooth English main sentence + icons with tooltip + provenance small-print source/window/n/cal/date M3 + honest NO CALL + balance bar | bot scattered numbers, silent precompute, market refs P1, forced number |

## Delivery — Smooth English Not Bot (Owner Directive)

- **Main UI:** One sentence verdict + icons + why. No bot dump.
- **Technical details:** Collapsible small-print = λ, Poisson, draw_table, att/def, ELO, Brier, n, window, date.
- **Icons with context:** 🛡️📈📉⚡❄️🌍🔗⚖️📅✅🚫💾 each has title tooltip smooth English.
- **Progressive disclosure:** Summary → why → technical. User can stop at summary.
- **Empty honest:** "Not rated yet — needs 6 matches" + "No calibrated bridge — need 20+ Euro ties, we have 12" not blank.
- **Primary CTA obvious per tab:** Predict / Drop file / Run replay — one CTA.
- **Example:** See `11-HUMAN-FRIENDLY-DELIVERY-SPEC.md` — full screen redesign with smooth English examples.

## Build Order (Same, Now With Clarifications)

| Step | Work | Gate artifact |
|---|---|---|
| S0 | Harness productionisation rolling-origin paired T1 MDE T2 full metrics | self-check vs ladder baseline RPL -12.2% etc |
| S1 | LIVE-DERIVE-01 live re-derive auto re-validation provenance M3 retire blob live form stars + current form gate | G14/G15/G16/G17 |
| S2 | Settlement venue-guard I5 draw=loss I4 | M17 |
| S3 | Balance panel NO CALL support shares | held-out cal M7 |
| S4 | Goal-range bins 0-1/2/3+ + current form blend α (owner clarified) — gated | harness win vs base-only omitted window |
| S5 | UEFA connector #17 → chain + league pivot s[L] bias loop → weighted vs 1.00 frozen | A-08 |
| S6 | Calibration cadence one-click masked replay + monthly sweep + M10 outcomes-only integrity screen | M5 M6 M10 |
| S7 | Architectural/UI build human-first smooth English icons with context per 11 | UI-PLAIN-01 |

Gates = harness output tables artifact IS approval.

## Pins (Live Authority)

- Store 5082 sha256 c9ad6a54… EXACT via fresh_audit.py — CLOSED (auditor)
- Store original 5000 sha256 c7b29e85… EXACT
- D1 corrected sha256 abd0c207…
- App v3.6.3 md5 17dd2b5b66ceb572a3fd946db9b56a92
- Harness ladder baseline + fresh_audit.py outputs — feasibility + integrity proof
- Foundation docs METHODOLOGY 6cd6c... ENGINE_SPEC 91cd0c... LIVE-BLUEPRINT d01cf... — pre-exist any personal claim

*Locked v2 — Trust nothing, measure everything, approve by test run only. Smooth English delivery, icons with context, app alive via per-team live rating + per-league pivot + current form weighted inclusion.*
