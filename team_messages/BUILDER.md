# For Builder — App Engineer (Harness S0 then Live-Derive S1)

Copy-paste this DM/email:

---
Subject: Your task — Builder B0 Harness Production — Branch arena/019fd213-the-bettor-1

Hi [Name],

You are Builder.

Repo: chickenaiforensic-crypto/the_bettor_1
Branch: arena/019fd213-the-bettor-1
Baseline app: previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/APP-V3.6.3/app-v3.6.3.html md5 17dd2b5b66ceb572a3fd946db9b56a92 (635,798 B)

Read in order:
1. START-HERE-COLD-START.md
2. COMMUNICATION-RULES-v1.md (no vague, audit before asking)
3. Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md — what app does today L#### refs
4. Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md §5 approval by test run (ladder L-1 last game → L-2 last 2 → L-n expanding → FULL) §8 build order S0-S7
5. Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md — your approval protocol, read twice
6. Supervior/ROLES/ROLE-BUILDER.md + builder/README-BUILDER.md
7. Supervior/WORKORDER-INDEX.md — your queue B0-B7, start B0

B0 — What to build:
- Productionise audit_work/backtest_harness.py as app's own masked-replay module (Calibration tab Run masked replay)
- Must include: rolling-origin, paired stats T1, MDE reporting T2, full metric set Brier/logloss/dir T4, per-match artifacts (train window, holdout, n, all metrics, date)
- Feasibility baseline already: RPL 0.5675 vs 0.6465 base -12.2% n254, CZ1 -6.4% 0.6090 vs 0.6509 n276, EPL -6.0% 0.6140 vs 0.6534 n374 on last omitted season 2025-26. Your production harness must parity this on 5082 store + ladder JSON at audit_work/ladder_baseline_2026-08-05.json

Gates you face:
- Byte-diff vs baseline, P1 grep no market data (odds/fetch/XHR must 0), one-gate grep PR.ingest, harness ladder re-run on current 5082 store
- No silent rewrites, provenance panel M3 missing today — you will add in S1

Deliver to handoffs/:
- App file b64 armoured .txt (never raw .html — channel injects junk) named <STEP>-<version>-<md5prefix>.b64.txt
- Evidence artifact <STEP>-EVIDENCE-<date>.json with train/holdout/n/metrics/date
- Comment md5 pre/post

Do not rebuild from zero — extend v3.6.3. Honest refusal NO CALL + balance panel M7 is valid output, never fabricate.

— Lead Planner (Arena AI) on arena/019fd213-the-bettor-1
---
