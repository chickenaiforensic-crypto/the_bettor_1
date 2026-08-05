# LEAD ENGINE — Index

**Lead:** AI Agent (Arena) — Lead Planner, Analyst, Auditor  
**Branch:** `arena/019fd213-the-bettor-1`  
**Date:** 2026-08-05  
**Mission:** Zero-market prediction engine — compute from results only, weight systems by measured effectiveness, collapse into one singular structural system that produces best computational wins. Architectural/human-friendly build follows.

## Files in this hub

| # | File | Purpose | Status |
|---|---|---|---|
| 01 | `01-STRUCTURAL-AUDIT.md` | Full audit of existing computational systems (R1/R2/R3 + legacy audits 01-24) — trust nothing | IN PROGRESS |
| 02 | `02-COMPUTATIONAL-SYSTEMS-INVENTORY.md` | Inventory of every system, layer, constant, with measured contribution | QUEUED |
| 03 | `03-WEIGHTING-EFFECTIVENESS-MATRIX.md` | Ranking by measured Brier/logloss gain, paired T1, MDE T2 — constitution of singular engine | QUEUED |
| 04 | `04-SINGULAR-ENGINE-BLUEPRINT.md` | The one weighted system: one store, one live fit, one verdict card | QUEUED — after 03 |
| 05 | `05-DATA-VERIFICATION-PLAN.md` | Plan to verify data for leagues etc is not false — independent re-parse, no trust in old auditor | QUEUED |
| 06 | `06-ARCHITECTURE-BACKLOG.md` | Human-friendly presentation + functionality fix list (after structural engine locked) | BACKLOG — S7 |

## Dependencies (Authority)

- SOT v1.3 `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` — ledger M1-M20, amendments A-01..A-08, pins §14
- Masterplan v1.1 `ENGINE-MASTERPLAN-2026-08-05.md` — weighting table §2, computation contract §3, approval by test run §5, cross-league fit loop §6, build order S0-S7 §8
- Functionality v1.0 `FUNCTIONALITY-2026-08-05.md` — current app v3.6.3 screen map, L#### refs
- Verification v1.0 `VERIFICATION-DATA-2026-08-05.md` — 5000-row independent re-audit, D-1/D-2 defects
- Harness `audit_work/backtest_harness.py` — first live run done (RPL -12.2%, CZ1 -6.4%, EPL -6.0%)

## Current Verified Store

- Original: `Supervior/other/pitch-rating-full.json` — 5000 rows, sha256 `c7b29e85…8fc00` (SOT pin)
- D1 fixed: `Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json` — 5000 rows, 11 CZ1 dates fixed, sha256 `abd0c207…`
- D1+D2 closed: `previous_work_files/workspace-recent-.../pitch-rating-full-5082-D1D2-2026-08-05.json` — 5082 rows (ENG 1900, CZE 1603, RUS 1579), sha256 `c9ad6a54…`

Operational = 5082. Future connector = UEFA ~2000-2500 rows (workorder 17).

## Process — Trust Nothing

1. Every system listed with its origin file, code line, measured effect.
2. Every data row traceable to primary archive (RSSSF re-parse + second index).
3. No system adopted on documentation — only test-run ladder L-1 → L-n → FULL on last-omitted window.
4. Every claim: file / code line / pin — no stories.

## Next Steps (This Session → Next)

- [x] Workspace setup on git (branch pushed, WORKSPACE.md, CONTRIBUTING.md, TEAM-MESSAGE.md)
- [ ] Complete 01-STRUCTURAL-AUDIT (read all audit-01..24 + chain + app/engine.js)
- [ ] Draft 02 inventory with layer constants LR 0.055, DECAY 0.0022, HFA_LR 0.010, ρ -0.06, etc.
- [ ] Draft 03 weighting matrix — dominant L1, small real L3, display L4/L5/R3, standby R2 chain
- [ ] Verify data: re-run rsssf_verify + pack_parse on all leagues
- [ ] Then architecture backlog (human-friendly, not AI-styled)

*All work on branch `arena/019fd213-the-bettor-1`. Push often, pull before push.*
