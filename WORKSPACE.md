# WORKSPACE — Lead Planner / Analyst / Auditor Hub

**Branch:** `arena/019fd213-the-bettor-1`  
**Purpose:** Zero-market football prediction engine — compute from results only, no odds, no market influence.  
**Lead:** Current AI Agent (Arena) operating as Lead Planner, Analyst, Auditor.  
**Date:** 2026-08-05

This is the single collaborative workspace for all roles. Everything below is binding until owner changes it.

---

## 1. Where We Work (Git)

- **Repo:** `chickenaiforensic-crypto/the_bettor_1`
- **Active branch for this program:** `arena/019fd213-the-bettor-1`
  - Everyone checks out this branch: `git checkout arena/019fd213-the-bettor-1`
  - Push to it only: `git push origin arena/019fd213-the-bettor-1`
  - No other branches for this session — Arena tracks by this branch name.
- **Remote verified:** `origin` = GitHub, push succeeded 2026-08-05.
- **PR:** https://github.com/chickenaiforensic-crypto/the_bettor_1/pull/new/arena/019fd213-the-bettor-1

### Quick start for humans

```bash
git clone https://github.com/chickenaiforensic-crypto/the_bettor_1.git
cd the_bettor_1
git checkout arena/019fd213-the-bettor-1
git pull origin arena/019fd213-the-bettor-1
```

- **Do not edit `previous_work_files/`** — history, read-only.
- **Do not zip.** All data returns = plain `.txt` BP-TEAM-PACK v2.
- **All returns land in `handoffs/`** — one file per workorder.
- **All app builds land in `handoffs/`** as b64 armoured + evidence JSON.

---

## 2. Authority Chain

| Doc | What | Pin |
|---|---|---|
| `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` v1.3 | Whole system: engines R1/R2/R3, ledger M1-M20, amendments, live pins §14 | SOT is law; if conflict, SOT wins |
| `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` v1.1 | TARGET: one weighted singular engine, weighting table §2, approval by test run §5, cross-league fit-to-results loop §6, build order S0-S7 §8 | Supersedes nothing in SOT, translates it |
| `Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md` v1.0 | What app v3.6.3 does today, screen by screen, with L#### line refs | Verified against real file |
| `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` v1.0 | Independent re-audit of 5,000-row store, defect register D-1/D-2/D-3 | Fresh parsers only |
| `START-HERE-COLD-START.md` | 8-file reading order (mandatory) | Binding |

**Doctrines that never change (P1-P5):**
1. Results only, no market data in ANY role.
2. One gate. Rejections never stored.
3. Approval = measured test run on last-omitted window (ladder L-1 → L-n → FULL).
4. Backup first. Purge/import = backup-gated. Undo = load backup.
5. No silent rewrites. Pins live in SOT §14.

---

## 3. Workspace Layout (After Setup)

```
README.md                         — map
WORKSPACE.md                      — this file (collab hub)
CONTRIBUTING.md                   — git workflow + rules
TEAM-MESSAGE.md                   — paste-ready message for owner to send
COMMUNICATION-RULES-v1.md         — how we talk
START-HERE-COLD-START.md          — mandatory reading
Supervior/
  Build Docs/                     — SOT, masterplan, functionality, verification
  Workorder/                      — researcher queue 01-17 + builder B0-B7
  ROLES/                          — auditor / builder / researcher briefs
  updates/                        — session logs, relay messages
  other/                          — verified stores (5000 + D1 corrected + 5082)
handoffs/                         — ONLY door for returns (researcher .txt, builder b64+evidence)
builder/                          — future builder cold-start
audit_work/                       — live audit + backtest scripts (auditor-owned)
lead_engine/                      — NEW: Lead planner analysis hub
  00-INDEX.md
  01-STRUCTURAL-AUDIT.md
  02-COMPUTATIONAL-SYSTEMS-INVENTORY.md
  03-WEIGHTING-EFFECTIVENESS-MATRIX.md
  04-SINGULAR-ENGINE-BLUEPRINT.md
  05-DATA-VERIFICATION-PLAN.md
  06-ARCHITECTURE-BACKLOG.md
previous_work_files/              — history, never edit
```

---

## 4. Roles — How You Work With Me (Lead Planner)

### I am the bottleneck for truth
- Nothing enters store/app on trust — not from researcher, not from builder, not from previous auditor.
- Every claim traces to file / code line / pin.
- I re-run everything with fresh code.

### If you are Researcher (data)
- **Source:** `Supervior/Workorder/WORKORDER-*.md` + queue `WORKORDER-INDEX.md`
- **Read first:** `START-HERE-COLD-START.md` → `ROLE-RESEARCHER.md`
- **Return:** ONE `.txt` into `handoffs/` named exactly as workorder says (e.g. `UEFA-CONNECTOR-..._BP-TEAM-PACK_v2.txt`)
- **Grammar:** BP-TEAM-PACK v2, rows never tables, 90-min doctrine, tieIds shared, NOTE lines for AET/neutral/conflicts.
- **Gates you will face:** participation completeness, structure, 90-min, boundary/dedupe, name resolution, legacy cross-diff, table reproduction.
- **Work with me via:** drop file in `handoffs/`, ping in PR comments with md5+counts, I will audit in `audit_work/` and reply with acceptance card or defect list.

### If you are Builder (app)
- **Source:** `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` §8 S0-S7 + `WORKORDER-INDEX.md` B0-B7 + `builder/README-BUILDER.md`
- **Read first:** `START-HERE-COLD-START.md` → `ROLE-BUILDER.md` → `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md`
- **Return:** b64-armoured `.txt` + evidence artifact (train window, holdout, n, Brier/logloss/dir, date) into `handoffs/`
- **Gates:** byte-diff vs baseline, P1 grep (no market), no-network grep, one-gate grep, harness ladder re-run.
- **Current baseline:** `previous_work_files/workspace-recent-.../APP-V3.6.3/app-v3.6.3.html` md5 `17dd2b5b66ceb572a3fd946db9b56a92`

### If you are Auditor / Analyst (second auditor, helpers)
- You own `audit_work/` scripts. Fresh parsers only — never reuse old auditor scripts as evidence.
- Pins on arrival: md5/sha256.
- Third-source adjudication for any archive vs pack conflict.
- Harness in `audit_work/backtest_harness.py` — first live run already done (RPL -12.2%, CZ1 -6.4%, EPL -6.0% vs base on last omitted season).

### Communication
- **Clear, Brief, Summarised, No guessing.**
- One question at a time if unclear.
- All decisions logged in `Supervior/updates/` or `lead_engine/`.

---

## 5. Current Data State (Verified 2026-08-05)

- **Original store:** `Supervior/other/pitch-rating-full.json` — 5,000 matches, sha256 `c7b29e8501319b8024cc7b2d11a1d2309248e5edcb4a87751484ed94e8d8fc00` — matches SOT pin EXACT.
- **D-1 corrected:** `Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json` — same 5,000, 11 CZ1 date errors fixed, sha256 `abd0c207897148e1e490a5adc8f956e0756f97df4280b5960f31930047ce5b40`.
- **D-1+D-2 closed:** `previous_work_files/workspace-recent-.../pitch-rating-full-5082-D1D2-2026-08-05.json` — 5,082 rows (ENG 1900, CZE 1603 incl MOL 202, RUS 1579) sha256 `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c`.
  - This is the operational store. Harness feasibility run already run on D-1 store; production harness S0 will target 5082.
- **Verified per league:** EPL 1900/1900 exact, RPL 1220/1220 vs RSSSF, RUSCUP 341/341, CZ1 1390/1401 (11 date fixes), MOL 120→202 (+82 verified), ADDENDUM 18/18.
- **Open defect:** None on 5082, except M10 outcomes-only integrity screen pending.
- **Tooling:** `audit_work/pack_parse.py`, `rsssf_verify.py`, `legacy_diff.py`, `backtest_harness.py`, `ladder_run.py`.

---

## 6. What I am Doing Next (Lead Plan)

**Phase 0 — Workspace Setup (THIS):** git branch pushed, folder structure created, message ready.

**Phase 1 — Structural Audit (Trust Nothing):**
- Inventory every computational system in old tree (audit-01..24, chain/, data/, app/engine.js)
- Map significance order (measured: L1 +5.6% Brier dominant, L3 +0.047% small real, L4/L5 zero prob, R2 zone ladder calibrated, R3 ELO display-only)
- Verify data for each league against independent source (RSSSF re-parse, not old auditor's word)

**Phase 2 — Weighting & Singular Engine:**
- Produce weighting-effectiveness matrix (SOT §2 + masterplan §2) — rank by measured Brier/logloss gain, paired T1, MDE T2.
- Collapse into one structural system: one store, one live DC fit, one verdict card (probability + confidence band + display labels + refusal path). Star draw correction capped ±0.02, consensus filter-only, ELO display-only.
- Define computation contract (MUST/MUST NOT per layer) + refusal paths P3.

**Phase 3 — Architecture / Human-Friendly Build (After engine locked):**
- Audit current app v3.6.3 content quality — it is AI-styled, not human-friendly (plain language decree A-02).
- Plan human-first presentation: Match tab simplicity, Coverage honesty, Calibration transparency, Log audit trail, Integrity clarity, Provenance panel M3.
- Only after S0-S6 (harness, live-derive, settlement audit, balance panel, goal bins, cross-league bridge) gates pass by test run.

Every step ships only when its test-run ladder artifact wins on last-omitted window.

---

## 7. How to Work With Me Day-to-Day

1. **Pull before you push.** `git pull origin arena/019fd213-the-bettor-1` always.
2. **One workorder = one commit = one handoff file.** Never batch unrelated workorders.
3. **Name exactly.** Workorder says `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt` — not `uefa.txt`.
4. **MD5 on arrival.** When you drop in `handoffs/`, also comment MD5: `md5sum handoffs/yourfile.txt`
5. **No trust.** If you see a number, verify it. If you can't verify, write NOTE|warning|blocker.
6. **Ask via GitHub Issue or PR comment** — tag the file/line/pin, not "it doesn't work".
7. **Evidence, not stories.** Every PR description must cite file hash, test output, or code line.

**Contact loop:**
- Researcher/Builder → handoffs/ + PR comment → Auditor (me) runs gates in audit_work/ → approval card or defect list in `Supervior/updates/` or GitHub → owner relays → next workorder.

---

*This workspace is the single source for collaboration. If anything here conflicts with SOT, SOT wins — file an erratum, don't silently rewrite.*
