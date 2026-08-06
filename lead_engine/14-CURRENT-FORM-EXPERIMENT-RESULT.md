# 14 — Current Performance Blend Experiment Result (Owner Clarification Test)

**Date:** 2026-08-05 continued  
**Script:** `audit_work/current_form_blend.py` (fresh code, trust nothing)  
**Store:** 5082 closed operational `pitch-rating-full-5082-D1D2-2026-08-05.json` SHA256 c9ad6a54… EXACT  
**Method:** Base long-term L1 fit 2021-22..2024-25 vs Current form short-window last 6 matches + minimum playoffs gate ≥4 recent in 60 days, GD diff >0.5, α 0.35 base 0.5 playoff-heavy capped, blend GD_final = (1-α)GD_base + αGD_recent, avg total preserved, clamped [0.05,6.0], grid Poisson DC ρ-0.06, Brier paired T1.

## Result — Blend Does NOT Beat Base (Feasibility)

| League | Train | Test scored | Blend used | Brier base | Brier blend | Diff (base-blend positive=blend better) | t | Logloss base→blend | Dir base→blend | Verdict |
|---|---|---|---|---|---|---|---:|---|---|---|
| RPL | 960 | 254 | 115 (45.3%) | 0.5675 | 0.5771 | **-0.00963** | -1.92 | 0.9572→0.9701 | 55.9%→55.1% | NOT BETTER |
| CZ1 | 1105 | 276 | 140 (50.7%) | 0.6090 | 0.6131 | **-0.00415** | -0.68 | 1.0146→1.0202 | 49.3%→51.1% | NOT BETTER (dir up but Brier down) |
| EPL | 1520 | 374 | 238 (63.6%) | 0.6140 | 0.6220 | **-0.00802** | -1.50 | 1.0226→1.0326 | 49.2%→47.3% | NOT BETTER |

**Summary:** Base 0.5675/0.6090/0.6140 vs blend 0.5771/0.6131/0.6220 diff -0.00963/-0.00415/-0.00802 t negative → blend slightly worse, not significant at 95% (t -0.68 to -1.92) but directionally negative.

## Why This Happens — Matches Previous C6 Rejection

- Old recency weighting C6 tested 84/84 no discrimination → rejected.
- This version adds gate ≥6 recent, GD diff>0.5, α capped, playoff boost 0.5, but still uses simple recent_avg_GD = mean of last 6 GDs.
- Recent_avg is noisy (small n=6) vs base which has 960-1520 matches history. Weighting noisy signal degrades calibration — Brier increases.

## What Owner Intended vs What We Tested

Owner: "if team comes into league very efficient than it did before its current performance acquired through minimum number of playoffs evaluation provides weighted inclusion"

Our gate tried to capture efficiency jump (delta = recent_avg - long_avg >0.5) but we used all recent matches (league) not playoffs-specific.

**Playouts are different:** playoff legs are high-stakes, less noisy than random 6-game window. Minimum playoffs evaluation (≥3 playoff ties, win≥2) should be much stronger signal than generic recent 6.

Our experiment used playoff boost α 0.5 if playoff_cnt≥3 & wins≥2 but only 45-63% of test games triggered blend, many triggered on generic recent (not playoff-heavy). Need playoff-only gate.

## Next Tuning (Proposed, Must Win Harness to Ship)

1. **Playoff-only current form:** α only if playoff recent ≥3, ignore generic recent 6. Rationale: playoffs are clutch, less noise.
2. **Lower α:** 0.15-0.20 max, not 0.35-0.5 — current 35% is too aggressive for noisy signal.
3. **ELO-based current form not GD:** Use ELO short-window (last 6) change, not raw GD — ELO already smooths.
4. **Efficiency relative to expectation, not raw GD:** delta = recent_avg_GD - expected_GD_from_base (how much they beat expectation), not recent - long avg.
5. **Minimum playoffs + win streak:** require win streak ≥4 in last 6 + playoff appearance, not just GD diff.

## Verdict for Singular Engine v2

- **Current form blend as tested is NOT adopted** — fails harness gate (must beat base on omitted window paired).
- **Status remains:** candidate for S4, needs retuning per above, then re-test on 5082 + future UEFA connector #17.
- **Live per-team rating up/down stays:** L1 online fit already makes app alive — att/def moves on results, no extra blend needed for alive behavior.
- **Per-league pivot s[L] remains priority S5:** cross-league real-world accuracy depends on s[L], not current form.

## How to Communicate This in Smooth English (Human-Friendly)

Instead of "Blend diff -0.00963 t=-1.92 not significant" in main UI:

- Main: "Current form: we track last 6 games, but giving it 35% extra weight made predictions slightly worse on last season hidden (Brier +0.009), so we keep base rating for now. Playoff-heavy form test next."
- Icon ⚡ still shows hot/cold but tooltip: "Hot but not weighted into tip yet — testing if it helps our hidden-season test."
- Technical details small-print: table above with Brier diff, t, n, α, gate.

*This is approval by test run doctrine — we tested owner idea, it did not win yet, so we do not ship it. We tune and re-test, not ship on documentation.*

## Artifact

Script `audit_work/current_form_blend.py` re-runnable on any store path. Output above is approval record for this candidate — currently FAIL, needs retuning.

Next: tune α 0.15 playoff-only and re-run on same 5082 + future SPA/ITA/GER/FRA packs.
