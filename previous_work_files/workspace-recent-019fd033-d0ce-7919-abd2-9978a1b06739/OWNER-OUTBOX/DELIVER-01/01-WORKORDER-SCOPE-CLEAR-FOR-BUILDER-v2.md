# WORK ORDER — Country-Scope Clear Control (builder commission WO-SCOPE-CLEAR-01)

**Issued:** 2026-08-04 · **By:** owner via auditor/orchestrator · **Target build:** app **v3.6.0** (new version; v3.5.2 stays sealed — md5 `6bd76ae025fc6eee68e3186ac52ac5ec`; any change to existing behaviour = FAIL) · **Registry refs:** decrees D12 (central requests), D13 (post-programme full audit), D14 + v0.64a (**NO MIXING, absolute**).
**Deliverable:** single updated `app-v3.6.0.html` + md5/sha256 pins + changelog. No zips. No partial patches.

---

## 0. READ FIRST — why this exists (the rule it serves)

Owner decree: old-seed rows and researcher-produced rows for the same scope must **never coexist** in the app ("no mixing, absolute"). The endgame for every country is:

> **Clear the old scope in the app → auditor approves the complete new packs → owner loads the new packs in (pure adds).**

Today the only replace mechanism is the auditor hand-building a migration `.json` per incident (works, but = coding every time). That stops now. This workorder commissions a **permanent UI control surface** that clears old data **per country scope**, generically, with **zero per-country code added ever after**. The app currently grows by country packs (Russia, Czechia, England, Spain, Italy, Germany, France, Kosovo, MLS, Scotland, US cups done and queued); the control must work for any country present or future, including ones unknown today.

Existing mechanics that ALREADY work and must not change: migration `.json` load = full-store replace (code line ~3354, log string `Store replaced by migration…`); pack ingest = add-if-new with duplicate fingerprint skip (`Skipped duplicate match`, ~line 999); hold cards for tie-linkage anomalies; localStorage persistence `pitch-rating-v3.store`.

## 1. The control surface (UX)

One new panel on the Data tab: **"Country packs — clear & replace"**.

1. **Scope list (derived 100% from the live store, §2):** a two-level hierarchy — **country** rows, each expandable to its **individual competitions** (leagues/cups). BOTH levels are selectable clear scopes: the owner can clear a whole country in one click, or select exactly **one league/competition** inside it (e.g. *Russian Cup* only, leaving *Russian Premier League* untouched). For each row show — name · match-row count · (per-competition counts at country level) · identity (club) count at country level. Sort by count desc. No country/league name may appear as a hardcoded string anywhere in the new code (gate G10).
2. **Click a scope (country OR single competition) → Preview screen** (the safety heart, mandatory before any action). The selection function takes a scope object `{country, competition|null}` — one shared code path for both levels. Shows, computed live and exactly:
   - matches in scope: per-competition counts + full row list (scrollable) with date / home / score / away;
   - clubs (identities) that would be removed because they belong to this country and would have zero remaining references — listed by name;
   - attached records that would go: season rows, venue rows (orphan rule §3), FORM/CTX records, teamStats entries, mute records on those rows;
   - the two actions as separate, clearly different buttons:
     - **MUTE scope (soft clear)** — reversible; rows stay visible (greyed), excluded from all computation. Adds an **UNMUTE scope** button on the same panel afterwards.
     - **PURGE scope (hard clear)** — destructive; enabled **only after a backup export `.json` has been automatically downloaded in the same click-flow** (see §3.3).
   - an honest line: *"There is no undo button inside the app. Undo = load the backup file you just downloaded (full replace, the existing migration feature)."*
3. **Confirm screen:** restates the exact counts ("Purge **Russia**: 644 matches (Russian Premier League 489 · Russian Cup 152 · Russian Relegation Playoffs 2 · Russian Super Cup 1), 26 clubs, N attached records"). One confirm. Numbers must be rendered from the same computation as the action itself (never re-derived differently).
4. Success: toast + Coverage tab recomputes live (existing derive pipeline); a log entry + integrity snapshots per §3.5.

Non-negotiable UX principle: the owner is non-technical. No devtools, no typed commands, no file editing — buttons and visible numbers only.

## 2. Scope model (generic; how rows belong to a country)

- **Match → country:** `match.country` if set; else the country of its home/away identities when they agree; else bucket **"Multi-country / other"** (its own selectable scope, e.g. Europe ties). Rows with no resolvable country land in **"Unassigned"** — also a selectable, clearable scope (the current store has none; future packs may).
- **Competition grouping:** competitions are grouped under their country (from the matches). Display exactly the stored `competitionName` strings (the current "undefined (N rows)" Coverage-label gap is *not* in scope here, but this panel must show raw stored strings, so nothing is ever invisible).
- **League-level scope:** with a competition selected, the in-scope set = match rows whose `competitionName` equals that competition exactly. The identity-orphan rule in §3.4 then applies *within that narrowed removal* (a club is only purge-eligible if it loses its last reference — so clearing one league while another scope still references its clubs never strands them; cross-scope survivors land on the preview keep-list).
- **Identity → country:** `identity.country`. An identity is purge-eligible only when its country matches the scope **and** it has zero remaining references (matches / seasons / venues / forms / teamStats) after the match removal — orphan rule, §3.4.
- **Cross-border guard (hard rule):** a match whose competition does **not** belong to country X is never removed by purging X, even if one of its clubs is from X (example: a Czech club appearing in a European tie stays). Its club identity is *retained-by-reference* automatically.

Calibration truth (live store, export 2026-08-02, 1,432 rows — the UAT numbers in §5 come from here):

| Scope | Matches | Breakdown | Clubs |
|---|---|---|---|
| Russia | **644** | RPL 489 · Russian Cup 152 · Relegation Playoffs 2 · Super Cup 1 | 26 |
| Czech Republic | **632** | Czech First League 561 · MOL Cup 63 · Czech Relegation Playoffs 8 | 45 |
| United States | 81 | (MLS/USOC family) | — |
| Scotland | 34 | — | — |
| Kosovo | 19 | — | — |
| …smaller | 16 | single/dual rows | — |

## 3. Operation semantics (precise)

1. **MUTE scope:** sets `muted=true` (existing field) on every in-scope match row; one log entry (`type:'data', action:'scope-mute'`, scope + counts). UNMUTE reverses bitwise. Computation excludes muted rows exactly as existing MUTE-pack rows do (pipeline already exists).
2. **PURGE scope** removes, in one atomic mutation:
   - all in-scope match rows (muted or not);
   - season rows and FORM/CTX/teamStats records tied to in-scope teams/competitions;
   - venue rows that become orphaned (zero references) **and** belong to a purged identity;
   - mute records made moot by the row removal;
   - identities per the orphan rule, listed individually in preview beforehand.
3. **Backup gate (hard):** PURGE stays disabled until the app has downloaded a full export `.json` (existing export feature) in the same flow; the log entry records the backup filename. Suggested filename additive marker: `pitch-rating-full-data-<date>-pre-purge-<country>.json`. Implementation may trigger the existing export path programmatically — do not invent a second export format.
4. **Orphan rule:** identities with `country==X` are removed **only** when post-removal reference count == 0; anything still referenced (cross-border guard §2) is auto-retained and must appear on the preview under "kept (still referenced)".
5. **Atomics + audit trail:** one store mutation, one `STORE.save`, log entries `scope-purge` / `scope-mute` with scope, counts, backup filename; one integrity snapshot **before** and one **after** (existing snapshot machinery). App re-derives immediately (Coverage live). Operation is idempotent: purging an already-empty scope = honest no-op log line, never an error.
6. **Sources policy:** `sources` collection is provenance and is **kept** by default even when its rows are purged (append-only audit trail); preview shows this plainly. (Optional checkbox "also drop scope-exclusive sources" allowed, default OFF.)
7. **Replace handoff:** after a successful clear, focus the ordinary file-drop zone; the next pack(s) for that country then import as pure adds under the *existing* rules (dedupe-skip for true duplicates unchanged — proof of a clean clear per G7).

## 4. Canonical endgame runbook (what the owner will actually do — design to this)

1. Open Data tab → *Country packs — clear & replace* → click **Russia** → read the preview (644 / 26).
2. Click **PURGE scope** → backup `.json` downloads automatically → confirm → store drops to 788 matches; Russia bucket empty.
3. (Auditor has meanwhile approved the complete Russian packs.)
4. Drop the complete packs → pure adds → Coverage lands on the auditor's pinned expectation; log shows no `Skipped duplicate match` lines (any skip = FAIL G7 — leftover old row).

Identical flow later for Czech Republic (632 → 0), Scotland, Kosovo, MLS/USOC — with *no code change per country, ever*.

## 5. Acceptance gates (owner-run UAT; binary; every one must pass)

- **G1** Cold boot on the 2026-08-02 snapshot: panel lists scope **Russia = 644 matches / 4 competitions / 26 clubs**; **Czech Republic = 632 / 3 / 45**. Zero tolerance.
- **G2** Russia preview renders the 489/152/2/1 breakdown, the full scrollable row list, and the 26-club remove/keep split.
- **G2-L** League-level selection: expand **Czech Republic**, select **MOL Cup** alone → preview = 63 matches, breakdown and keep-list correct; PURGE (post-backup) MOL Cup → Coverage **1,432 − 63 = 1,369**, Czech First League rows (561) and playoffs (8) untouched **and still render**; UNMUTE/restore paths work at league level too. Any casualty outside the 63 = FAIL.
- **G3** With no backup downloaded yet, PURGE is hard-disabled; becomes enabled only after the auto-download fires.
- **G4** MUTE Russia → Russian bucket excluded everywhere computable (Coverage shows it as held-out per existing muted convention); UNMUTE restores the exact prior counts (before/after counts diff = 0).
- **G5** PURGE Russia post-G3 → Coverage total **1,432 − 644 = 788**; log carries `scope-purge` + backup filename; full app reload persists 788.
- **G6** Load the just-downloaded backup via the existing migration loader → store returns to exactly 1,432 (undo path proven).
- **G7** After G5, drop the auditor-staged RPL pack (md5 `c3a72b35…`, 732 rows): imports with **zero** `Skipped duplicate match` log lines → new total **788 + 732 = 1,520**; zero hold cards expected.
- **G8** Repeat preview (no action) for Czech Republic: 632 with 561/63/8 breakdown, 45 clubs, cross-border keep-list rendered.
- **G9** Regression: load 1,432 snapshot again → drop the same RPL pack *twice*; second drop = every row `Skipped duplicate match`, totals unchanged; drop Southampton hold-fixed pack (md5 `c7dbb89b…`) → stages 'ok' / no hold (unchanged hold-rule behaviour).
- **G10** **No hardcoding:** country/competition names in the new feature are derived from store contents only. Auditor greps the diff: zero country/competition string literals introduced by this feature; deleting all Russia rows leaves no dead 'Russia' entry; importing a brand-new country pack auto-creates its scope on next render.
- **G11** Engine boot after purge and after replace completes without console errors; derive/Coverage recompute; muted-row exclusion math untouched; artefacts (DC fitted model/gate) survive or re-fit per existing boot logic — no new failure modes.
- **G12** Auditability: pre/post snapshots + log lines written for every operation; post-purge export diffed vs pre-purge export by the auditor = exactly the purged rows, byte-level accounting.

## 6. Engineering constraints / non-goals

- Single-file app stays single-file; no network calls; no new file/grammar formats; no change to dedupe fingerprint, migration replace, hold rules, Coverage math, pack staging statuses (`ok`/`hold`/`bad`).
- Do **not** touch the sealed v3.5.2 behaviours (auditor byte-diffs all shared code paths: ingest/migration/derive; anything changed there beyond this feature = reject).
- No per-row edit UI, no per-row delete buttons, no undo button (backup-restore is the documented undo, G6).
- Accessibility: all counts on preview/confirm rendered from the same single selection function used by the mutation (one source of truth in code).
- Ship `app-v3.6.0.html` + changelog + md5/sha256; owner UATs per §5 in order; auditor records the seal in ZONES.

---

## APPENDIX — v3.6.1 DELTA COMMISSION (auditor, 2026-08-04; after v3.6.0 audit)

v3.6.0 (md5 `edf52d78b2fa1690721aa3a72018b634`) is auditor-approved for country-level flows. This delta ships as **v3.6.1** and adds three items; everything else stays frozen.

**D1 (return R1) — league-level clear selection.** Extend the scope hierarchy one level down: each country row expands to its competitions; both levels selectable. Selection object generalises to `{country, competition|null}` through the ONE shared selection function (preview/confirm/mute/purge all read it — the identity-orphan rule already operates on the narrowed set; cross-scope survivors land on the keep-list). Gate **G2-L** as specified in §5 (MOL Cup 63 alone → 1,432−63 = 1,369, First League untouched).

**D2 (return R2) — preview list completeness.** The preview match list must render ALL in-scope rows (no silent 400-row cap) — virtualised/incremental rendering is fine, buttons-and-numbers intent unchanged.

**D3 (owner UX request, supersedes the §1 "sort by count desc" note) — alphabetical listings.** Every selectable/listed collection in this panel is ordered **A–Z by its display name** so the owner can type-jump to it:
- the country scope list (alphabetical by country);
- the competition rows inside a country (alphabetical by competition name);
- the removed-club / kept-club lists (alphabetical by club name);
- counts stay displayed next to every name exactly as now (sorting changes ordering, never content).
Gate **G13**: open the panel on the v3.6.0 UAT store → country list reads alphabetically; expand Russia → competitions read alphabetically (Russian Cup · Russian Premier League · Russian Relegation Playoffs · Russian Super Cup); removed-club list in the Russia preview reads alphabetically. Any out-of-order entry = FAIL.

Deliverable: `app-v3.6.1.html` + md5/sha256 pins + changelog; auditor byte-diffs against v3.6.0 (expect additive/handler edits only inside the scope feature; anything else = reject).


— end of workorder —
