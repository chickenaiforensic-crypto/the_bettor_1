# PITCH RATING — GENERAL FUNCTIONALITY (how the system works, all of it)

**Version v1.0 — 2026-08-05.** Companion to the SOT (`BLUEPRINT-SOT-2026-08-04.md`, v1.3). Division of labour: **SOT = what the engine computes and why; this document = what the app does and how you operate it.** Every feature below is verified against the live app `app-v3.6.3.html` (md5 `17dd2b5b66ceb572a3fd946db9b56a92`); `L####` = code line. For engines, math, doctrine and the missed-work ledger, go to the SOT — this document points there instead of repeating it.

Audience: owner, planner, auditor. Plain language only; machine names appear in brackets.

## 1. What the app is (the shape)

| Fact | Value | Proof |
|---|---|---|
| Form | One HTML file, runs in any browser, no server, no account | whole file |
| Storage | Browser localStorage, one key `pitch-rating-v3.store` | L381 |
| Version | v3.6.3 (badge in footer) | L380, L3459 |
| Data in | Text files you drop in ("packs") through one gate | L709-1058 |
| Data out | One full JSON backup, on demand or auto before every purge | L491, L3448-3451 |
| Undo | There is no undo button. Undo = load your backup | L2956 |
| Rule of truth | "Every number on screen is computed from the data you have" (footer) | L3553 |

## 2. Screen map (everything that exists on screen)

**Header:** theme toggle ◐ · **Backup** button (L3070-3071).

**Five tabs** (L3075):

| Tab | What it's for |
|---|---|
| Match | Pick two teams, get the rating card |
| Data | Files · Coverage · Requests · Country packs (4 sub-tabs, L3355) |
| Calibration | Run masked replay; see calibration artifacts |
| Log & Settlement | Settlement of saved rows |
| Integrity & Snapshots | Muted rows; snapshot trail |

## 3. Match tab — the daily screen

1. **Team picker** — searchable, tolerant of spelling variants, grouped by league (L3083). Knows a team by its name, its canonical name and its aliases.
2. **Predict** — produces the rating card. Two engines can answer (details: SOT §3, §3.7):
   - **Fitted card** (`predictFitted` L1974) for leagues carried in the calibrated model.
   - **Online card** (`predictOnline` L2090) — live re-fit from the store for the new programme leagues (RPL, CZ1).
3. **Save a row** — "Save this row" button (`btn-settle` L3178/3570) freezes the card's numbers for settlement; frozen numbers never change afterwards, live numbers may move (L3533 text).
4. **Swap** — ⇅ Swap flips home/away sides of the fixture (L3148/3567).
5. **Performance block** — each team's recent form shown next to names (`perfView` L2512): last-6 matches before cutoff from the live ELO state; displayed, never edited.
6. Stars, tiers and labels on the card come from the rating engine (SOT §3.4-§3.6). Machine strings belong in a small-print "Technical details" area only (decree UI-PLAIN-01 / A-02).

## 4. Files tab — how data gets in (the one gate)

All imports — team packs, country packs, central-request returns, full-store files — pass **one gate** (`PR.ingest`, L709). One gate, no side doors.

**Gate checks** (L724-951): row grammar (Annex B / legacy v1) · completeness of required fields · scores are non-negative integers = **90-minute scores only** (L887) · competition type from a fixed whitelist (`COMP_TYPES` L737) · duplicate fingerprint inside the file (L890) · no future dates · tie-linkage check.

**Outcome per file:**
- **Clean → staged card with Approve.** Approve commits; toast reads "Loaded — N matches." (`approveStaged` L3803, toast L3811).
- **Held (Z-003)** — exactly-two-leg cup ties whose legs carry different tie-ids instead of one shared id (L922-951). Rows are **kept verbatim**, grouped by competition + pair; a human presses **"Approve — keep rows verbatim"** (v3.6.3 fix, L3791-3814). Nothing is invented or rewritten.
- **Rejected** — reason shown; **rejected files are never stored** (L3478 text).

**Against the store:** dedupe by deterministic fingerprint — date + canonical team pair + competition (L321, L1016): a match already in the store is **skipped, never duplicated**; only new rows land (add-if-new). Pack commit reports count identities merged/created (e.g. log shows CZ1: 1,401 matches, 25 identities created).

**Migrations:** dropping a full-store/backup file atomically **replaces** the whole store ("Store replaced by migration: …", `migrate` L519; owner's log seq 4, 8, 9). Old schemas are carried, never degraded (L528-534).

**First boot only:** 9 seed packs embedded in the file are loaded by migration (`SEED_PACKS` L11061-11100). After that, your store in the browser is the only truth.

## 5. Country packs tab — scoped import and purge (the programme workhorse)

(`scopeView` L3369, `purgeScope` L2957)

- Scope = a country (optionally one competition). The tab walks a safe chain: list → **preview** counts → **confirm** (`scopeListView` L3379, `scopePreviewView` L3400, `scopeConfirmView` L3439): matches, clubs, attached records, competition breakdown shown **before** anything happens (L3441-3445). Sources are kept as audit trail even when rows are cleared (L3429).
- **Mute scope (soft clear)** — first-class doctrine: exclusion = MUTE. One action mutes a whole scope ("excluded from every calculation", toast text L3620) and **Unmute scope (restore)** reverses it (`muteScope` L2928, buttons L3431). Nothing is deleted by a mute.
- **Purge = hard clear of that scope.** Backup-gated by machine, not by promise: before backup exists the button reads **"Download backup, then purge"** (L3434); pressing it **auto-downloads** a full backup named `pitch-rating-full-data-<date>-pre-purge-<scope>.json` (`downloadBackup` L3447); only then does it unlock as "backup ready" (L3433). The purge log entry records the backup's filename (L2988). In-app text states the rule outright: "There is no undo button inside the app. Undo = load the backup file you just downloaded" (L3436).
- Purge removes the scope's matches and orphaned club identities; mutes attached to removed matches go with them (L2976); engine artifacts survive.
- Standard replace flow (programme runbook): backup → purge scope → import new pack → confirm toast counts → fresh backup.

## 6. Coverage tab — what we hold, league by league

(L3481-3491) One row per league: seasons held with row counts · gaps flagged in amber · status pill (`complete / partial / requested`). This is the honest inventory — it shows what is missing, not just what exists.

## 7. Requests tab — the central request system (D12)

(L3492-3516, `newCentralRequest` L3817-3834). One button: **"New central request"** — snapshots the whole system and writes one request file listing every league that needs rows (per team, with the date). Downloads both files (`central-request-<date>.json` + `.txt`), logs the event, tracks state (open → sections complete/partial → archived, L3507-3513). Returns come back through the Files gate and are matched to the open request (L3757). Owner decree D12: this is the only channel for asking data — one request, whole system, no drip-asking.

## 8. Calibration tab — masked replay + artifacts

(L3517-3527) **"Run masked replay"** re-computes the fitted model from current store rows: later information is hidden, the model predicts, results are compared; artifacts replaced only when the validation numbers are written into the artifact (n, window, Brier/score, date). Artifacts live in the store as `dc-fitted-*` records (model, draw table, tiers, markets — L1902-1912). Rule (A-01 doctrine, workorder LIVE-DERIVE-01 queued for v3.6.4): rate only if your own replay on current data wins, else stay silent with a plain label. **Owner duty:** click it after any data change — right now it is owed after the 2026-08-04 imports (M5).

## 9. Log & Settlement tab

(L3529-3536) Lists settled rows (log entries of type `settle`, newest 20). The audit trail itself (every event — migrations, commits, purges, snapshots, requests) is kept inside the store `log` and travels in every backup; it is append-only and provable (used for the 2026-08-05 closing census: 55 entries, zero unreconciled). Settlement-rule audit (draw = loss, entry-side flip guard) is queued as ledger item **M17** — unaudited as of this document. Honest status, not smoothed.

## 10. Integrity & Snapshots tab

(L3537-3547)
- **Muted rows** — suspicious games are flagged with a rationale, **kept visible and excluded from every calculation — never deleted** (doctrine: exclusion = MUTE, no data abolition). Restore button reverses a mute (L3542). New-data integrity screening must be outcomes-only (A-05; owner-collision screen spec owed by auditor).
- **Snapshots** — taken silently before every data commit (L3548); the purge flow adds hash snapshots (`scope-post` entries seen in the real log).

## 11. Backup — the safety object

(L491 `exportFull`, L3569) Header button downloads `pitch-rating-full.json`: wrapper `format / version / schemaVersion / exportedAt` + full `store` + full `log`. Verified on the real one (2026-08-05, sha256 `c7b29e85…8fc00`): 3,588,489 bytes, complete store of 5,000 matches + 55-entry audit log. Habits that kept this programme safe: backup before every purge, backup after every import round, backups are raw JSON everywhere (never zipped — transport rule).

## 12. The data model on one page

Store keys (seen in the real backup): `meta` (schema v3.0.0, creation stamp, seed pack names, seq) · `identities` (teams with canon names + aliases) · `matches` (each with date, competition, compType, home/away, 90-min goals, venue, country, tieId, sourceId) · `seasons` · `venues` · `sources` (every match rows to a source URL+date) · `notes` (AET/penalty explanations ride with the data, 90-min doctrine) · `ctxFlags` · `mutes` · `log` (audit trail) · `artifacts` (calibration + form declarations + central requests — FORM rows are reconciliation-only, **never a hidden compute input**, L1053).

## 13. Doctrine rails — where each rule lives in the machine

| Rule | Where enforced |
|---|---|
| Results-only, no market data in any role (P1) | Ingest grammar has no odds fields; engine has no odds input (SOT §1) |
| 90-minute doctrine (AET/pens → 90' score + NOTE) | Gate integer-score check L887; note system rides with rows |
| Compute live or stay silent (A-01) | Footer truth sentence; LIVE-DERIVE-01 workorder → v3.6.4 |
| No data abolition (exclusion = MUTE; purge backup-gated) | Mute mechanics L528-534/3538; purge gate L3433-3451/2988 |
| One gate, rejections never stored | L709, L3478 |
| Dedupe add-if-new, rows kept verbatim | L321/1016, L3458-3814 |
| D12 central request only | §7 above |
| Plain language in UI (A-02) | Console texts (L3478, 3525, 3531, 3541) written for humans; machine names bracketed |
| Every claim provable | Log in every backup; ZONES chain outside the app |

## 14. Current operational state (2026-08-05, census-verified)

Store = **5,000 matches** (England 1,900 · Russia 1,579 · Czech 1,401 + MOL Cup 120) · 589 identities · 0 mutes · 55 log entries. Known open items: **M20** — MOL Cup short 82 (old pack file imported; fix = import FULLSPAN, toast must read 82, final 5,082) · **M5** — masked replay owed · **M17** — settlement audit owed · live form stars on the online path + provenance panel → v3.6.4 (DELIVER-06 ready to send). Full ledger: SOT §10 (M1-M20).

## 15. Where everything lives

Full pin table = SOT §14 (the live authority): repo commit `12192a9b…` (2026-08-05T06:04:16Z) for the old tree + fresh backup; workspace md5 pins for app, packs, foundation docs, audit card. If this document and the SOT ever disagree, the SOT wins — file an erratum, not a rewrite.

*Every feature above was verified against app-v3.6.3.html by grep before writing (ZONES v0.91). No stories.*
