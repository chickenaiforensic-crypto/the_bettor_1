# WORKORDER-STATUS

**Date:** 2026-08-03 · **Branch:** `arena/019fc462-the-bettor-1`

---

## Active commission register (discovered 2026-08-03 on `origin/main`)

16 five-year-span workorders were uploaded to `origin/main` (owner web-uploads;
that history is unrelated to this branch, so files are read via
`git show origin/main:<file>` and mirrored for reference under `supervisor/workorders/`).
Owner's one-at-a-time queue, with the live-session override applied:

| # | Order | Output | Status |
|---|---|---|---|
| override | **WO-RUSCUP-BACKFILL-03** — Russian Cup 2021-22 → 2023-24 | `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 189 rows, all 162 self-gates PASS** (user commissioned the cup return live, ahead of the RPL league pack) |
| ① | RPL league 2021-22 → 2023-24 | `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` | QUEUED (next — builds on the audited CSV base below) |
| ② | CZ1 (Czech First League) | pack | QUEUED |
| ④→ | EPL, FRA, GER, ITA, KOS, KOSCUP, MLS, MOLCUP, SCO1, SCOCUP, SCOLC, SPA, USOC | packs | QUEUED (workorder texts on `origin/main`) |

## Delivered artifacts (this branch)

| Path | Contents |
|---|---|
| `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` | Russian Cup return, BP-TEAM-PACK v2 grammar: 189 MATCH rows (36 + 77 + 76), 21 TEAM rows (non-roster opponents), 10 SOURCE rows, 68 NOTE rows, `END`. 90-minute doctrine; stage in venue-detail. |
| `audit/pack-validation.txt` | Gate re-runs: slice counts per round, group members + table recompute (2022-23/2023-24 club-for-club W/WP/LP/L/GF/GA/pts; 2021-22 full 3-team tables vs full ledger), bracket reproduction (semifinalists/finalists/champions 2022 Spartak, 2023 CSKA, 2024 Zenit), 14 two-leg aggregates, per-club pivot ledgers (owner's per-team completeness technique), boundary/dupes/identity checks. |
| `tools/build_pack.py` | Reproducible builder + validator (embeds the official record used as gate expectations). |
| `data/rpl/*.csv`, `docs/`, `audit/validation-report.txt` | Prior deliverable: audited RPL league dataset 2021/22-2025/26 (1,212 rows + closing 1X2 odds), unchanged. Base for queue item ①. |
| `supervisor/workorders/` | All 16 owner commissions mirrored read-only in one folder (register: `supervisor/README.md`), + `archive/` with the superseded RPL order.

## Reconciliation of the old open item (from the 2026-08-02 status note)

The RPL CSV deliverable was built blind ("workorder text never received"). Meanwhile
the referenced document exists: `origin/main:Supervior/Handoff/WORKORDER-RPL-2021-24-BACKFILL.md`
(archived WO-RPL-BACKFILL-01, approved verbatim), superseded by
`WORKORDER-RPL-2021-2026-5YSPAN.md` (queue ①) which demands the **BP-TEAM-PACK v2
.txt** form, not CSV. The CSV season set (2021/22-2025/26) is a superset of the
needed 2021-24 window and will be used as the cross-checked base for the pack;
nothing in the CSV contradicts the workorder set.

## Method notes for the cup pack (disclosures the auditor will also see in NOTEs)

* **Format correction:** the workorder table described 2021-22 as "old straight-knockout,
  no group stage" — RSSSF + Wikipedia show an Elite Group Stage (11 groups × 3) that
  season; a `format_reading` NOTE documents this with the corrected round counts.
* **Source conflicts (3 dates, 2022-23):** RSSSF compact bracket headers run +1 day vs
  its own detailed chapter and the RFS/Wikipedia index; resolved to the detailed dates
  (`source_conflict` warning NOTE).
* **Per-club technique:** the owner's suggestion ("list all teams, pull each club's full
  history inside the window — per-team complete = everything complete") is implemented
  as the per-club pivot gate; ledgers in `audit/pack-validation.txt`.
* **Nothing imputed:** optional TEAM profile fields left blank where no captured source
  exists; reconciliations live in NOTE lines, never in match data.

## Known loose end

Two files the owner says were attached mid-session (`README.md`, `START-HERE.md`)
never became readable in the sandbox and are not in the repo — flagged in chat;
awaiting re-send or a GitHub web upload.
