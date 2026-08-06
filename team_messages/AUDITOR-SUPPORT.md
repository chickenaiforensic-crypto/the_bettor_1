# For Auditor Support / Data Verifier

Copy-paste this DM/email:

---
Subject: Your task — Auditor Support — Verification — Branch arena/019fd213-the-bettor-1

Hi [Name],

You are Auditor Support.

Repo: chickenaiforensic-crypto/the_bettor_1
Branch: arena/019fd213-the-bettor-1

Read:
1. START-HERE-COLD-START.md
2. Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md — how D-1 (11 CZ1 +1-day) and D-2 (MOL 120→202 +82) were found
3. Supervior/ROLES/ROLE-AUDITOR.md
4. lead_engine/05-DATA-VERIFICATION-PLAN.md

Your space: audit_work/
Scripts: pack_parse.py, rsssf_verify.py, legacy_diff.py, backtest_harness.py, ladder_run.py

What to do:
- Fresh parsers only — never reuse old auditor script as evidence, write new parser, compare
- On receipt of any handoff .txt: md5/sha256 on arrival vs declared, grammar → boundary (no future, 90-min int) → dedupe fingerprint date+canon(pair)+comp vs store → names (every home/away resolves, zero split) → structure (season counts vs official fixtures) → table reproduction (recompute tables FROM rows, compare vs RSSSF/Wikipedia 16/16) → legacy cross-diff vs football-data/openfootball + 4244-row Euro index → third-source adjudication if archive vs pack disagree (transfermarkt/soccerway/official league site) → one approval card
- Keep errata owned — log your own instrument errors, never silent rewrite
- Re-verify one league per quarter end-to-end (how D-1 found)

Current verified store:
- Original 5000 sha256 c7b29e85…8fc00 = SOT pin EXACT
- 5082 closed sha256 c9ad6a54… operational — 0 dup, all ids resolve, 609 teams
- Pins live in SOT §14 — if file moves, re-pin before citing

Also spec M10 outcomes-only integrity screen (P1 forbids market prices — own-model collapse detection only).

Comment approvals/defects in PR with file/line/pin — no stories.

— Lead Planner (Arena AI) on arena/019fd213-the-bettor-1
---
