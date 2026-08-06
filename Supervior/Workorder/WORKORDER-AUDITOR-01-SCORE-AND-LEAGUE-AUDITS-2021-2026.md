# WORK ORDER — AUDITOR SCORE & LEAGUE AUDITS (2021-2026 5YSPAN)

**Issued:** 2026-08-05 · **Status:** QUEUED — position A-01 (Auditor queue, parallel with researcher/builder) — assigned per owner directive "assign your score audits to the auditor you brought on board to do it properly so you can attend to other things as team and league audits is very lengthy"  
**Why:** Full league audits lengthy + score audits lengthy — Lead Planner delegates fresh-code verification to Auditor Support, Lead attends to cross-league pivot s[L] fit-to-results, current form retune, architecture human-friendly S7, team coordination.  
**Authority:** ROLE-AUDITOR.md, COMMUNICATION-RULES-v1.md, BLUEPRINT-SOT-2026-08-04.md §14 pins, ENGINE-MASTERPLAN-2026-08-05.md §5 approval by test run ladder, VERIFICATION-DATA-2026-08-05.md, FUNCTIONALITY-2026-08-05.md, 20-RESEARCHER-RETURNS-CONSOLIDATION-AUDIT.md, 21-NEW-PACKS-VERIFICATION-FULL.md.

---

## 0. READ FIRST — Role Check

You are **Auditor Support** — second auditor, fresh code mandate. Before returning anything, scan your own work: any assertion without file/line/pin = story — stop, you must cite file/line/pin. (First auditor attempt missed 11 date errors CZ1 — your method must be fresh re-parse, not reuse old auditor scripts as evidence.)

> **On file name (2021-2026):** this commission stands for full 5-year span running into today — seasons 2021-22..2025-26 complete + 2026-27 played up to return date (state last round/date in NOTE). Approval certifies span gap-free.

## 1. SCOPE — Which Packs & Which Scores

### 1.1 Data Packs to Verify (in `handoffs/` on planner branch `arena/019fd213-the-bettor-1`)

| Pack File Path (Repo) | League | Matches | Expected Shape | Status |
|---|---|---|---|---|
| `handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` | Italy Serie A | 1901 = 1900 league 380×5 +1 Relegation Playoff Spezia 1-3 Verona 2023-06-11 compType other | 20 clubs ×38 MDs =380 per season, 0 TEAM union 27 pins exactly, 20 SOURCE 23 NOTE, 92/92 gates PASS per researcher log SHA e808c9f8 double-rebuild identical, venues 101-row lattice | **Smoke PASS** per `verify_new_packs.py` 0 dup 0 future whitelist OK — needs full gates |
| `handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt` | Germany Bundesliga | 1540 = 1530 league 306×5 (18×34) +10 Relegation Playoffs 2×5 | 18 clubs ×34 MDs =306 per season, 3 TEAM Fortuna Dusseldorf / SC Paderborn / SV Elversberg, 21 SOURCE 25 NOTE, 93/93 gates PASS SHA 4f90ddb1 triple-rebuild | **Smoke PASS** |
| `handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt` | France Ligue 1 | 1686 = 1678 league 380+380+306+306+306 across 20→18 contraction +8 Playoffs | 20 clubs 2021-23 38 MDs=380, 18 clubs 2023-26 34 MDs=306, 0 TEAM 26 roster strings verbatim Paris SG / St Etienne traps, 19 SOURCE 22 NOTE, 85/85 gates PASS SHA 44fe06b5 double-rebuild | **Smoke PASS** |
| `handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt` | UEFA CL/EL/ECL + quals | 1390 = 689 UCL +437 UEL +264 UECL, 99 TEAM foreign opponents, 2 SOURCE 61 NOTE | Ties with ≥1 programme-league club (ENG/RUS/CZE/SPA/ITA/GER/FRA), 0 dup expected (currently 1 dup FAIL Real Madrid-Chelsea 2022-04-12 duplicate fingerprint same date+home+away+competition different scores 1-3 vs 2-0 leg2 vs leg1 source IDs UCL-2122 vs UCL-2223) — **RETURNED for fix** to Researcher 2, re-audit after fix |

### 1.2 Score Audits (Calibration, Brier, Paired, MDE)

After ITA/GER/FRA/UEFA pass full data gates and import via app one gate (add-if-new) + masked replay M5 + ladder re-run parity:

- Per league (ITA, GER, FRA, plus existing RPL, CZ1, EPL) train 2021-22..2024-25 test last omitted season 2025-26 (or expanding holdouts 1,2,3,5,8,10,15,20,25,30,FULL per ladder) — Brier 1X2 full + per-side home/draw/away, logloss, direction accuracy, calibration max error bins, O2.5 and BTTS measured markets with I3 gates ship ≤2.7% caution 3.0-3.3% withheld 6.0%, paired T1 per-match deltas mean/sd/se/t/df/pTwo, MDE80 T2, rolling-origin T3 ≥4 expanding splits, full metric set T4, E8 holdout scored never fitted, T7 covid/structural break, T8 data-driven gates only.

### 1.3 M10 Outcomes-Only Integrity Screen (Spec Owed)

Per SOT A-05 RESOLVED: legacy market-price mute screen is P1-non-compliant — purge loss doctrine-consistent — do NOT restore. Replacement = outcomes-only screen, spec owed by auditor, owner P5 approval required.

## 2. WHERE YOU WORK — File Paths (This Answers Owner Question)

| What | Path in Repo (planner branch `arena/019fd213-the-bettor-1`) | Purpose |
|---|---|---|
| **Your scripts (fresh code only)** | `audit_work/` — you own them | Write fresh parsers here, never reuse old auditor's scripts as evidence. Existing: `backtest_harness.py`, `ladder_run.py`, `legacy_diff.py`, `pack_parse.py`, `rsssf_verify.py`, `fresh_audit.py` (pins EXACT c7b29e85/c9ad6a54 0 dup 0 future), `verify_new_packs.py` (smoke ITA 1901 GER 1540 FRA 1686 UEFA 1390), `current_form_blend.py` v1 degrades -0.00963, `current_form_blend_v2.py` playoff-only safe 0% usage. You create new: `rere_parse_ita.py`, `rere_parse_ger.py`, `rere_parse_fra.py`, `rere_parse_uefa.py`, `second_index_ita.py` etc, `score_audit_ita.py`, `score_audit_ger.py`, `score_audit_fra.py`, `score_audit_uefa_connector_league_pivot.py`, `m10_outcomes_only_spec.py`. |
| **Packs to audit (input)** | `handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` etc — see table above | Input — read via `pack_parse.py` base parser, not trust researcher WORD — re-parse fresh. |
| **Your reports (data verification)** | `Supervior/Build Docs/` — e.g., `VERIFICATION-DATA-2026-08-05.md` is precedent | Your full audit reports go here (or `lead_engine/` as working then promoted). Example: `lead_engine/21-NEW-PACKS-VERIFICATION-FULL.md` already smoke, you extend to full. |
| **Your log (session trail)** | `Supervior/updates/SESSION-*.md` or `lead_engine/XX-*.md` | Every finding, decision, dated — e.g., `SESSION-2026-08-05-AUDIT-AND-MASTERPLAN.md` precedent with 8 turns. Log pins, defects, adjudications. |
| **Your evidence artifacts (score audits)** | `audit_work/` — e.g., `ladder_baseline_2026-08-05.json` baseline artifact | Ladder baseline expanded after import of new leagues, plus per-league score artifacts JSON with Brier/base/gain/logloss/dir/paired meanDelta sd se t df pTwo mde80 calib max err markets o25/btts etc — numbers artifact IS approval record. |
| **Workorder you are reading now (this file)** | `Supervior/Workorder/WORKORDER-AUDITOR-01-SCORE-AND-LEAGUE-AUDITS-2021-2026.md` | This file — your commission — queued. |
| **Workorder index (queue)** | `Supervior/WORKORDER-INDEX.md` | Researcher queue 01-17 + Builder B0-B7 + Auditor A-01 (this). |
| **Role brief** | `Supervior/ROLES/ROLE-AUDITOR.md` | Binding rules: fresh code always, verify instrument before verdict, pins on arrival md5/sha256, third-source adjudication, errata owned, harness yours, no stories. |
| **Handoff transport rules** | `handoffs/README-HANDOFFS.md` | Researcher one .txt rule, builder b64+evidence, auditor verification before import. |
| **Lead Planner assignment that delegated to you** | `lead_engine/22-AUDITOR-ASSIGNMENTS-SCORE-AUDITS.md` | Details why delegate lengthy audits, score audits delegated (data verification + calibration Brier paired MDE etc + M10 spec), lead attends to cross-league pivot s[L] fit-to-results, current form retune, architecture human-friendly S7, builder coordination. |
| **Builder B0 deliverables (already accepted)** | `handoffs/B0-v3.7.0-e688eee2.b64.txt` + `B0-EVIDENCE-2026-08-05.json` + `builder/app-v3.7.0-b0.html` + `b0_byte_diff.txt` etc | B0 S0 harness productionise v3.7.0 ACCEPTED report `lead_engine/19-B0-AUDIT-ACCEPTANCE-REPORT.md` — all gates measured pins EXACT parity Δ0.0000 33 rows exact greps identical byte-diff 7 hunks intended. Awaiting owner UAT before B1. |
| **Prototype human-friendly UI** | `prototype-human-friendly.html` | Target S7 architecture human-friendly delivery — smooth English not bot scattered, icon system 🛡️📈📉⚡❄️🌍🔗⚖️📅✅🚫💾 with tooltips. |

## 3. GRAMMAR & GATES (Your Acceptance Gates — Failing Any = Returned Incomplete)

### 3.1 Data Gates (Per Workorder §5)

- **Grammar:** BP-TEAM-PACK v2 exactly — MATCH|date|competition|compType|home|hg|ag|away|round|stadium|city|country|tieId|source — TEAM lines only for clubs not on roster, SOURCE label|URL|accessed|type|what verified, NOTE info/warning/blocker, END marker, no tables. Whitelist compType: domestic-league, other, uefa-cl, uefa-el, uefa-uecl (loader L737 already ready).
- **Boundary:** No dateless, no future >2026-08-05, integer 90-min scores 0-30, required keys present.
- **Dedupe:** Fingerprint date+canon(home/away/competition) inside file 0 dup (ITA/GER/FRA PASS, UEFA currently 1 dup FAIL Real Madrid-Chelsea must be 0), vs store 5082 fingerprints 0 overlap for new leagues ITA/GER/FRA/UEFA expected 0 — reported PASS in verify_new_packs.
- **Names:** Every home/away resolves to roster canon/alias or TEAM rows, zero split identities — ITA 0 TEAM union 27 pins exactly means roster covers all, GER 3 TEAM PO participants outside roster, FRA 0 TEAM 26 roster strings verbatim Paris SG / St Etienne traps — check.
- **Structure:** Per competition season counts vs official format: ITA 38×10 ties =380 per season, GER 34×9=306, FRA 38×10 then 34×9 after contraction 20→18, playoffs 2 legs shared tieId per Z-003 hold lesson (both legs ONE tieId, not per-leg), single-leg empty, roundLeg field not blank, venueType field etc.
- **90-min doctrine:** Every AET/pens tie carries 90' score + advancement NOTE info/advancement which side advanced how pens score, neutral venue NOTE info/neutral_venue reason — check German 2 ET legs, French 2 aet legs, ITA spareggio neutral.
- **Table reproduction:** Recompute final tables FROM your rows, compare vs RSSSF/Wikipedia 20/20 ITA, 18/18 GER, 20→18 FRA per season (and 16/16 RPL/CZ1, 20/20 EPL already done) — auditor re-runs with fresh parser never reuse old.
- **Second-index:** Wikipedia season articles results matrices + worldfootball.net all_matches per-round pages per season + openfootball second-index ledgers 380/380 fixtures and dates identical etc per researcher logs 92/92, 93/93, 85/85 gates PASS — need fresh verification.
- **Legacy cross-diff:** vs football-data/openfootball lineage `export/01_matches.csv` 202k dataset + 4244-row European index for UEFA connector — 0 score/side mismatches day-by-day.
- **Participation completeness (UEFA):** Every programme-league club Euro list 2021-22..2025-26 complete vs official participant lists — club that qualified has every match of every phase it played present, absent = gap defect.
- **Spot-audit trail:** One matchweek per season re-listed in NOTE with source URL.
- **Continuity:** Full gap-free span 2021-22→today for programme clubs, any official in-scope tie stored nowhere = gap defect.
- **Pins on arrival:** md5/sha256 on arrival vs declared pin before anything else, raw CDN never trusted git blobs or b64 — per ROLE-AUDITOR binding #3.

### 3.2 Score Gates (Per Masterplan §5 + METHODOLOGY T1-T8 + I1-I6)

- **Brier 1X2 full + per-side home/draw/away:** Train 2021-22..2024-25 test last omitted season 2025-26 (or expanding holdouts 1,2,3,5,8,10,15,20,25,30,FULL per ladder L-1→FULL per league) — Brier DC vs base marginals + per-side. Must beat base per league on omitted window paired to stay.
- **Logloss + direction accuracy:** -mean log max(p_y,1e-9), dir_acc outcomeCall == y.
- **Calibration max error:** Bin predictions 0-0.1...0.9-1.0 per side, meanPred vs observedFreq, max err + side + binLo/binHi + n + meanPred + observedFreq.
- **Measured markets O2.5 + BTTS:** O2.5 predMean freq errPct gate ship ≤2.7% caution 3.0-3.3% withheld 6.0%, BTTS withheld correctly absent in app per I3.
- **Paired T1:** Per-match deltas base_error - variant_error positive = variant better, mean/sd/se/t/df/pTwo two-sided p via incomplete beta Numerical Recipes betai Lanczos ln-gamma independent Simpson cross-check |Δp|<1e-13 — as proven in B0 evidence.
- **MDE80 T2:** Minimum detectable effect 80% power alpha .05 two-sided = 2.8*sd/sqrt(N) — report with every result — not sig uninterpretable without MDE.
- **Rolling-origin T3:** ≥4 expanding splits train_frac 0.55 etc — not just one cut.
- **Full output T4:** Home/draw/away Brier + 1X2 + logloss + calibration — component gains can hide as other side loss Study11.
- **User construction T5:** Test user's construction as specified on case with intermediates shown — crude stand-ins produced wrong verdicts twice Studies12,17 — audit scripts included verify finding before reporting.
- **Not sig ≠ no effect T6:** Distinct claims never merged.
- **Representativeness T7:** Check structural breaks covid window flipped home-win 4.2pt — covid Start/End 2020-03-01 to 2021-06-30 flagged.
- **Data-driven gates T8:** No assumed spread-gate rejected better chains — measured 84/84 no discrimination recency rejected, venue correction pocket worse rejected, spread-based gate tight worse r0.195 vs 0.384 rejected.
- **Bounded constants:** Adjustments accepted only within existing caps/steps floor/ceiling/max step per key LR [0.01,0.10,0.01] etc — free-run refused plain reason — via PR.calibration.acceptConstants() + b0_selfcheck.js caps.bounded_ok + caps.freerun_refused.
- **Empty-store P3 refusals:** Empty store run returns P3 refusals no crash.

## 4. RETURN PROTOCOL — Where Your Work Goes

| Your Deliverable | File Path to Place It | Naming | What It Must Contain |
|---|---|---|---|
| **Data verification report per pack (ITA/GER/FRA/UEFA after fix)** | `lead_engine/23-...-VERIFICATION-*.md` or `Supervior/Build Docs/VERIFICATION-ITA-GER-FRA-2026-08-05.md` + `Supervior/updates/SESSION-AUDITOR-2026-08-05-*.md` log | `VERIFICATION-ITA-2021-2026-*.md` etc | Pins on arrival md5/sha256, grammar/boundary/dedupe/structure/90-min/names/table repro 20/20/18/18, second-index 380/380 etc, legacy cross-diff 0 mismatches, participation completeness, spot-audit trail, continuity, adjudication register where archive vs pack disagreed pack RIGHT vs RSSSF misprint etc, defect register (e.g., UEFA dup), verdict PASS/FAIL, recommended next import + masked replay M5 + ladder re-run parity. Must cite file/line/pin — no stories. |
| **Score audit artifacts per league** | `audit_work/ladder_baseline_2026-08-05.json` expanded + `audit_work/score_audit_ita.json` etc + `lead_engine/24-SCORE-AUDIT-ITA-GER-FRA.md` | `score_audit_*.json` + evidence md | Train rows/window, holdout rows/window scored/refused, Brier DC/base gain%, Brier side home/draw/away, logloss, dir_acc, calib_max_err err/side/binLo/binHi/n/meanPred/observedFreq, marginals_holdout, paired n/meanDelta/sd/se/t/df/pTwo/mde80/note, markets o25 predMean/freq/errPct/gate/note btts predMean/freq/errPct/status withheld — full metric set T4, numbers artifact IS approval record. |
| **M10 outcomes-only integrity screen spec** | `lead_engine/25-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md` + `Supervior/Build Docs/` | `M10-SPEC-*.md` | No market data in any role — own-model collapse detection only: e.g., team rating jumps >X in Y matches without results, predicted prob collapse vs settlement Brier sudden increase, team never hosted per I4 venue guard, etc. Muted rows kept visible excluded every calc never deleted Restore reverses, snapshots before every commit, spec P1 compliant, P3 honest, owner P5 approval required. |

**Your reports are audited by Lead Planner (me) — fresh parsers only — and pins verified on arrival before anything enters app.**

## 5. WHY THIS WORKFLOW ANSWERS OWNER QUESTION

Owner asked: "so where the workorder/handoff for the auditor to work etc - you are the planner l should tell you to produce this - also where is the file file path?"

- **Workorder file path:** This file itself `Supervior/Workorder/WORKORDER-AUDITOR-01-SCORE-AND-LEAGUE-AUDITS-2021-2026.md` — this is the commission you produce as planner for auditor to work.
- **Handoff for auditor:** Not `handoffs/` (that's for researcher/builder returns) — auditor's inputs are in `handoffs/` (ITA/GER/FRA/UEFA packs to verify), auditor's scripts in `audit_work/`, auditor's outputs in `lead_engine/` + `Supervior/Build Docs/` + `Supervior/updates/` + `audit_work/*.json`.
- **File paths table:** See §2 above — complete map of where auditor works, where files live.

## 6. CURRENT STATUS OF PACKS FOR YOUR WORK

- **ITA 1901, GER 1540, FRA 1686:** Smoke PASS 0 dup 0 future whitelist OK per-season counts match expected 380×5 / 306×5 / 380+380+306+306+306 + playoffs, top tables plausible Milan 86 Napoli 90 Inter 94 etc Bayern 77/71/90/82/89 Paris SG 86/85/76/84/76 — ready for full gates.
- **UEFA 1390:** Smoke FAIL 1 dup fingerprint Real Madrid-Chelsea 2022-04-12 duplicate same fingerprint different scores 1-3 vs 2-0 leg2 vs leg1 source IDs UCL-2122 vs UCL-2223 wrong season — defect, returned to Researcher 2 for fix, re-audit after fix.
- **Store 5082:** CLOSED, pins EXACT c7b29e85 original 5000 = SOT §14 and c9ad6a54 5082 0 dup 0 future 609 teams — auditor already verified via `fresh_audit.py` + `verify_new_packs.py`.
- **Builder B0:** v3.7.0 ACCEPTED report `19-B0-AUDIT-ACCEPTANCE-REPORT.md` — pins EXACT parity Δ0.0000 33 rows exact greps identical byte-diff 7 hunks intended syntax OK empty-store P3 refusal no crash bounded constants — merged into planner.

**Next:** After your full audit PASS → import via app one gate (add-if-new) + masked replay M5 + ladder re-run parity vs new baseline → after import store ~10,199 rows (+ITA/GER/FRA) → ~11,589 (+UEFA after fix) → S5 league pivot s[L] bias loop fit-to-results (owner bump-up/calibrate per-league X points above) can run on real Euro data — real-world cross-league accuracy.

---

*This workorder is your commission — produce it as planner — file path is here. Auditor works from `audit_work/` reads from `handoffs/` writes to `lead_engine/` + `Supervior/Build Docs/` + `audit_work/*.json` + logs in `Supervior/updates/` — all paths listed in §2.*

**Assigned per owner directive — lengthy team and league audits delegated to auditor properly with fresh code, Lead attends to cross-league pivot + current form + architecture + team coordination.**
