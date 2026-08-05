# TEAM MESSAGE — Paste Ready for Owner to Send to Everyone

**Copy everything below this line and send to team / Slack / email / GitHub Discussions.**

---

**Subject: Workspace Live — Zero-Market Engine — Lead Planner Setup Done — Branch `arena/019fd213-the-bettor-1`**

Team,

The lead planner/auditor workspace is now live on git. We are building a zero-market football prediction engine — results only, no odds ever, zero market influence. Trust nothing — previous omissions found (11 CZ1 date errors + 82 MOL shortfall already fixed, now 5082 verified rows).

**Git — where we work:**

- Repo: `chickenaiforensic-crypto/the_bettor_1`
- Active branch: `arena/019fd213-the-bettor-1` (pushed, live)
  ```
  git clone https://github.com/chickenaiforensic-crypto/the_bettor_1.git
  cd the_bettor_1
  git checkout arena/019fd213-the-bettor-1
  git pull origin arena/019fd213-the-bettor-1
  ```
- PR link: https://github.com/chickenaiforensic-crypto/the_bettor_1/pull/new/arena/019fd213-the-bettor-1
- All work on this branch only. No other branches for this session.
- Commit prefix: `researcher: ...` / `builder: ...` / `auditor: ...` / `planner: ...`

**Docs — read in this order (mandatory):**

1. `COMMUNICATION-RULES-v1.md` — how we talk (clear, brief, no guessing, audit before asking)
2. `START-HERE-COLD-START.md` — cold start 8 files ~45 min
3. `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` v1.3 — whole system, ledger M1-M20, amendments, pins §14 — this is law
4. `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` v1.1 — TARGET singular weighted engine, weighting table §2, approval by test run §5, cross-league fit-to-results loop §6, build order S0-S7 §8
5. `Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md` — current app v3.6.3 screen by screen
6. `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` — independent 5000-row re-audit, defects D-1/D-2 fixed to 5082
7. `WORKSPACE.md` — NEW: collab hub, how you work with lead planner (me)
8. `CONTRIBUTING.md` — NEW: git workflow + checks
9. Your role brief: `Supervior/ROLES/ROLE-RESEARCHER.md` or `ROLE-BUILDER.md` or `ROLE-AUDITOR.md`
10. Your queue: `Supervior/WORKORDER-INDEX.md`

**Current data truth (verified fresh, not old auditor word):**

- Original: `Supervior/other/pitch-rating-full.json` 5000 rows sha256 `c7b29e85…8fc00` = SOT pin EXACT
- D1 corrected: `Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json` 5000 rows 11 CZ1 dates fixed sha256 `abd0c207…`
- Closed operational: `previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` 5082 rows ENG1900 CZE1603 RUS1579 sha256 `c9ad6a54…` — this is what harness runs on
- No fabricated rows found. Every pack row traces to real played match. Re-verified with fresh RSSSF re-parse + second index.

Other branch mentioned that contains fetched audited data? Investigated — only `main` + this branch exist on remote. Data lives in `Supervior/other/` + `previous_work_files/workspace-recent-.../` — those were re-verified. If you have another branch name, share it and I will fetch + re-verify.

**For Researchers (data):**

- Queue `Supervior/Workorder/` — 17 workorders. #17 UEFA-CONNECTOR priority.
- Return: ONE `.txt` BP-TEAM-PACK v2 into `handoffs/` named exactly as workorder says (e.g. `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt`). No zip, rows never tables, 90-min doctrine (AET/pens 90' + NOTE advancement), tieIds shared.
- Gates: grammar, boundary, dedupe, names, structure, table reproduction, RSSSF fresh re-parse, legacy cross-diff. I re-run fresh code only.
- Drop file + comment md5: `md5sum handoffs/yourfile.txt` + row counts.

**For Builders (app):**

- Read `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — approval = measured test run ladder L-1 last game → L-2 last 2 → L-n expanding → FULL full-system. Numbers artifact IS approval record.
- Baseline app v3.6.3 md5 `17dd2b5b66ceb572a3fd946db9b56a92` at `previous_work_files/.../APP-V3.6.3/app-v3.6.3.html`
- Harness `audit_work/backtest_harness.py` already ran feasibility: RPL -12.2% vs base, CZ1 -6.4%, EPL -6.0% on last omitted season (2025-26). Production S0 must build rolling-origin + paired stats T1 + MDE T2.
- Return: b64 armoured `.txt` + evidence JSON into `handoffs/`.

**For Auditors/Analysts:**

- Own `audit_work/` scripts — fresh parsers only. Pins on arrival md5/sha256. Third-source adjudication.
- Harness is yours — re-run ladder on every candidate + build.

**What I (Lead Planner) am doing now:**

- Phase 0 done: workspace setup (this message, WORKSPACE.md, CONTRIBUTING.md, lead_engine/ hub)
- Phase 1 in progress: structural audit — trust nothing, map all computational systems (R1 L1-L5, R2 evidence graph + zone ladder + chain, R3 ELO display) weighting by measured effectiveness into singular structural system
- Phase 2 next: weighting matrix → singular blueprint (one store, one live fit, one verdict card)
- Phase 3 after: architecture/human-friendly build plan (current app too AI-styled, poor content/functionality per owner) — after S0-S6 gates pass by test run, S7 human-first.

**Lead engine hub (new):**

- `lead_engine/00-INDEX.md` — index
- `lead_engine/01-STRUCTURAL-AUDIT.md` — full audit of existing systems
- `lead_engine/02-COMPUTATIONAL-SYSTEMS-INVENTORY.md` — inventory every system layer constant measured gain
- `lead_engine/03-WEIGHTING-EFFECTIVENESS-MATRIX.md` — ranking by Brier/logloss, constitution of singular engine
- `lead_engine/04-SINGULAR-ENGINE-BLUEPRINT.md` — one weighted system blueprint
- `lead_engine/05-DATA-VERIFICATION-PLAN.md` — how we prove data not false, protocol for new leagues
- `lead_engine/06-ARCHITECTURE-BACKLOG.md` — human-friendly backlog after structural lock

**Standing rules that never change:**

1. Results only, no market data in any role (P1)
2. One gate, rejections never stored
3. Approval = test run ladder on last-omitted window (not doc)
4. Backup first, undo = load backup, no in-app undo
5. No silent rewrites, pins live in SOT §14, errata owned

**How to work with me:**

- Pull before push, one workorder = one commit = one handoff file, name exactly, md5 on arrival, no trust, evidence not stories, one direct question if blocked with file/line/pin.
- I am bottleneck for truth — nothing enters store/app on trust, I re-run everything.
- Ask via GitHub Issue/PR comment with file/line/pin.

**Next actions for you:**

- If researcher: checkout branch, read cold start, pick workorder 17 UEFA connector (parallel allowed), start row collection per source hierarchy (RSSSF country European sections #ec + UEFA.com + Wikipedia + worldfootball), return to handoffs/.
- If builder: checkout branch, read ladder message, start B0 harness productionise in `builder/` — read `builder/README-BUILDER.md`.
- If owner: load 5082 store into app (migration toast should read "5082 matches · 609 teams") and click Run masked replay once — then ladder numbers come from app itself.

Nothing asserted without file/script/output. Fresh code always. Zero market.

— Lead Planner / Auditor (Arena AI) — branch `arena/019fd213-the-bettor-1` — 2026-08-05

---

**End of paste.**
