# For Auditor Support — Activate — Lengthy League Audits + Score Audits

Copy-paste to Auditor Support (dormant — activate now):

---
Subject: Activate — Auditor Score & League Audits A-01 — Branch arena/019fd213-the-bettor-1

Hi [Auditor Name],

You are Auditor Support — assigned lengthy team and league audits per owner directive (owner said lengthy, assign to you properly so Lead can attend to other things).

Branch: arena/019fd213-the-bettor-1 — checkout exact, pull.

Your workorder (formal commission):
Supervior/Workorder/WORKORDER-AUDITOR-01-SCORE-AND-LEAGUE-AUDITS-2021-2026.md — read §0 role check + §1 scope + §2 where you work file paths table + §3 Grammar & Gates (data gates + score gates T1-T8 I1-I6) + §4 Return Protocol + §5 Why Answers Owner Question.

Your inputs (in handoffs/ on planner branch, consolidated from locked branches 019fc462 + 019fd1a3 + 019fd227):
- ITA 1901 matches (1900 Serie A 380×5 +1 playoff) 0 TEAM 20 SOURCE 23 NOTE 92/92 gates PASS SHA e808c9f8 — smoke PASS 0 dup 0 future
- GER 1540 (1530 league 306×5 +10 playoffs) 3 TEAM Fortuna/Paderborn/Elversberg 21/25 93/93 PASS SHA 4f90ddb1
- FRA 1686 (1678 league 380+380+306+306+306 across 20→18 contraction +8 playoffs) 0 TEAM 19/22 85/85 PASS SHA 44fe06b5
- UEFA Connector 1390 (689 UCL 437 UEL 264 UECL) 99 TEAM 2/61 — smoke FAIL 1 dup fingerprint Real Madrid-Chelsea 2022-04-12 duplicate same fingerprint different scores 1-3 vs 2-0 leg2 vs leg1 source IDs UCL-2122 vs UCL-2223 — returned to Researcher2 for fix, re-audit after fix

Your tasks (lengthy — fresh code mandate, never reuse old auditor scripts as evidence — write new parser, compare):

A. Data Verification Full (ITA/GER/FRA/UEFA after fix):
- Grammar BP-TEAM-PACK v2, boundary no future >2026-08-05 integer scores, dedupe fingerprint date+home+away+competition 0 dup inside vs store 0 overlap new leagues vs 5082 PASS, structure per competition season counts 38×10=380 ITA 34×9=306 GER 38×10 then 34×9 FRA + playoffs shared tieId ONE per Z-003 single-leg empty, 90-min doctrine AET/pens 90' + advancement NOTE neutral venue NOTE, names every home/away resolves roster or TEAM rows zero split Paris SG / St Etienne traps, table repro recompute FROM rows vs RSSSF/Wikipedia 20/20 ITA 18/18 GER 20→18 FRA, second-index Wikipedia worldfootball openfootball 380/380 fixtures AND dates identical per researcher logs, legacy cross-diff vs 202k dataset + 4244-row Euro index 0 mismatches, participation completeness every club Euro list complete vs official participant lists, spot-audit one matchweek per season NOTE, continuity gap-free, pins on arrival md5/sha256.

Scripts you own in audit_work/: backtest_harness.py, ladder_run.py, legacy_diff.py, pack_parse.py, rsssf_verify.py, fresh_audit.py pins EXACT c7b29e85/c9ad6a54 0 dup 0 future, verify_new_packs.py smoke, current_form_blend.py v1 degrades -0.00963, current_form_blend_v2.py playoff-only safe 0% usage, score_audit_full.py expanded store 10209 0 overlap, plus you create new rere_parse_all.py (already created — verifies 1900/1900 ITA handling Oct10 2022 misprint, 1529/1530 GER handling Feb20 2022 Aug20 2023 misprints 70' abandonment, 1674/1678 FRA handling contraction postponement/replay), rere_parse_uefa.py (checks dup + per competition + Z-003 hold).

B. Score Audits (Calibration):
- Brier 1X2 full + per-side home/draw/away, logloss, dir accuracy, calibration max error bins, O2.5 and BTTS measured markets I3 gates ship ≤2.7% caution 3.0-3.3% withheld 6.0%, paired T1 per-match deltas mean/sd/se/t/df/pTwo independent Simpson cross-check |Δp|<1e-13, MDE80 T2, rolling-origin T3 ≥4 expanding splits, full metric set T4, user construction T5, not sig≠no effect T6, representativeness T7 covid window 2020-03-01 to 2021-06-30 flagged, data-driven gates T8, bounded constants free-run refused, empty-store P3 refusals.
- Train 2021-22..2024-25 test last omitted season 2025-26 per league expanding holdouts 1,2,3,5,8,10,15,20,25,30,FULL per ladder L-1→FULL per owner MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1, holdout scored never fitted E8, muted rows excluded doctrine exclusion=mute (0 mutes on 5082 store).

Deliverables from you:
- Data verification report per pack ITA/GER/FRA/UEFA after fix: lead_engine/23-...-VERIFICATION-*.md or Supervior/Build Docs/VERIFICATION-ITA-GER-FRA-2026-08-05.md + Supervior/updates/SESSION-AUDITOR-2026-08-05-*.md log with pins, defects, adjudications, verdict PASS/FAIL, recommended next import + masked replay M5 + ladder re-run parity, must cite file/line/pin no stories.
- Score audit artifacts per league: audit_work/ladder_baseline_2026-08-05.json expanded + audit_work/score_audit_ita.json etc + lead_engine/24-SCORE-AUDIT-ITA-GER-FRA.md with train rows/window holdout rows/window scored/refused Brier DC/base gain% Brier side home/draw/away logloss dir_acc calib_max_err err/side/binLo/binHi/n/meanPred/observedFreq marginals_holdout paired n/meanDelta/sd/se/t/df/pTwo/mde80/note markets o25 predMean/freq/errPct/gate/note btts predMean/freq/errPct/status withheld full metric set T4 numbers artifact IS approval record. Already did expanded store 10209 average gain +8.70% ITA +9.0% n=374 p<0.01 GER +11.7% n=300 p<0.001 FRA +6.9% n=300 p<0.05 — verify fresh.
- M10 outcomes-only integrity screen spec: lead_engine/XX-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md already drafted — Brier shock settlement variance >2.0σ, rating jumps >0.5 goal shifts without results, venue ghosting guard teams never hosted verified venue I4, plus relegation anomaly score extremes dup fingerprint future dates, mute vs purge doctrine exclusion=MUTE purge backup-gated standard replace flow backup→purge→import→toast→fresh backup, what screen does NOT do P1 no market, implementation after owner P5 approval as Integrity & Snapshots tab enhancement — refine and get owner P5 approval.

Where you work file paths (owner asked where is file file path):
- Your scripts: audit_work/ you own them fresh code only
- Packs to audit input: handoffs/ITA-...txt etc
- Your reports: Supervior/Build Docs/ + lead_engine/21-*,23-* + updates/SESSION-*
- Your evidence artifacts: audit_work/*.json ladder baseline + score_audit_*.json
- Workorder you are reading now: Supervior/Workorder/WORKORDER-AUDITOR-01-SCORE-AND-LEAGUE-AUDITS-2021-2026.md
- Workorder index: Supervior/WORKORDER-INDEX.md researcher 01-17 builder B0-B7 auditor A-01
- Role brief: Supervior/ROLES/ROLE-AUDITOR.md binding fresh code pins on arrival third-source adjudication errata owned harness yours no stories
- Handoff transport rules: handoffs/README-HANDOFFS.md
- Lead assignment that delegated to you: lead_engine/22-AUDITOR-ASSIGNMENTS-SCORE-AUDITS.md
- Builder B0 deliverables: handoffs/B0-...b64.txt + B0-EVIDENCE + builder/app-v3.7.0-b0.html ACCEPTED report 19-B0-AUDIT
- Prototype human-friendly UI: prototype-human-friendly.html target S7

Current status: ITA/GER/FRA smoke PASS ready for full gates, UEFA FAIL 1 dup returned to Researcher2, store 5082 CLOSED pins EXACT, builder B0 ACCEPTED.

Next: After your full audit PASS → import via app one gate add-if-new + masked replay M5 + ladder re-run parity vs new baseline 10209 → ~11,589 with UEFA after fix → S5 league pivot s[L] bias loop fit-to-results owner bump-up per-league X points above can run real Euro data real-world accuracy.

Please start now — lengthy — fresh code only — push to planner branch arena/019fd213-the-bettor-1 and comment md5 + counts in PR.

— Lead Planner (Arena AI) — branch arena/019fd213-the-bettor-1

---
