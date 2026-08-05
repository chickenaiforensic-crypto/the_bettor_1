# PITCH RATING — REBUILD WORK ORDER (final, cold-start edition)

**Prepared 2026-08-02 · Owner: project owner · Engineer: you (cold start assumed) · Auditor: the system-side assistant.**
This document is self-contained. You do not need to know anything that is not written here or in the binding documents listed in §2. If anything here conflicts with a binding document, **stop and ask** — never silently pick one.

**The owner's three sentences that define this build:**
1. One new app = **one single source of truth**.
2. **Live computation**: select a fixture and every number shown is computed from the data store — nothing about a team or league is hardcoded.
3. Almost **all games should have full data** — a researcher (Annex A) is commissioned alongside this build to supply every missing row; you integrate as the bulk arrives, the auditor corrects and audits your work.

---

## 0. Cold start — how to work on this

**Read first, in this order:**
1. This document, all of it.
2. `uploads/LIVE-BLUEPRINT.md` — binding operating rules (evidence doctrine, no-fabrication rules, known defects not to regress).
3. `uploads/COMMUNICATION-RULES-v1.md` — working conduct (audit before editing; never assert without proof; every edit verified).
4. `ZONES.md` — change log with every shipped decision and WHY (fastest way to learn the project's scars; every rejection is recorded there).
5. `CALIBRATION-6.md`, `CALIBRATION-8.md`, `CALIBRATION-9.md`, `CALIBRATION-13.md` — how calibration ships (masked replay, split-half, failed candidates killed).

**How you will be judged (read before writing a line):** Nothing is accepted on your claim. Every phase has a gate; you present the gate's *evidence* (commands + outputs + numbers), and the auditor re-runs it. Self-certified "done" is not done. See §8 (hand-back protocol).

**Stop conditions (halt and report, do not improvise):** a conflict between this WO and a binding doc · a validation gate failing · data you cannot verify from two sources (NOTE-blocker it) · anything that would change a frozen settlement number.

---

## 1. What exists today (verified state, not assumed)

- `app-v2.6-cross.html` — single-file app, internally **two systems** (this is the problem being fixed):
  - `MODEL`: a hardcoded Dixon-Coles fit — 18 hardcoded leagues, ~350 teams, ratings/draw-table/market errors fitted offline on 153,058 matches and **baked into the file as a JSON literal**. The 18 leagues have **zero raw match rows** in the live store (season aggregates only).
  - `BP` (evidence engine): a separate store of imported match rows (currently **1,421 matches / 792 identities / 3 muted rows** across 6 packs: Russia RPL+FNL, Czech CZ1+CZ2, Scotland-related, Kosovo, MLS/USL) with its own identity/venue/season/schema, its own Elo form engine, its own renderer, and its own wording.
- Duplicate seams confirmed by audit: two "star" scales (0–5 vs 0–100), two match memories, two goals models, two verdict taxonomies, venue check only for the 18 leagues.
- What works and must not regress: 18-league pipeline outputs; evidence replay calibration (633-game masked replay pool, zone table frozen in `ZONES.md`); integrity MUTE channel; unified log; settlement discipline (frozen slates govern settlement even when forward numbers later move — see `SLATE-2026-08-01-03.md` header).
- Test scaffolding exists and is mandatory: `smoke_test.js` (**156/156** today), `replay_test.js`, `validate_packs.js`, `census_connectivity.js`, `audit_league_paths.js` (node + vm + DOM-stub idiom — no browser needed).

---

## 2. Binding documents

| Document | Governs | Where |
|---|---|---|
| `LIVE-BLUEPRINT.md` | Evidence doctrine, no-fabrication rules, demote rules, known defects not to regress | `uploads/` |
| `COMMUNICATION-RULES-v1.md` | Working conduct | `uploads/` |
| `ZONES.md` | Decision/changelog record you must append to, never rewrite | root |
| `CALIBRATION-*.md` | Replay/calibration method and results | root |
| `INTEGRITY-AUDIT.md` + `SLATE-2026-08-01-03.md` | Mute/settlement discipline | root |
| `ENGINE_SPEC.md` | Dixon-Coles layer order/fitting/provenance/refusals | **owner-side; request it before Phase 2 fit work** (until it arrives, follow the fitting conventions pinned in `CALIBRATION-7.md` and treat no DC behavior as changeable) |

---

## 3. Doctrine (binding architecture principles)

1. **Single source of truth = the data store.** One schema: `identities · matches · seasons · venues · sources · ctxFlags · mutes · log · artifacts`. No second schema, ever.
2. **Live computation.** Every displayed number is computed from the store. No hardcoded league list, no frozen per-team ratings, no "18 built-in leagues" concept. A league exists in the app *because its match data exists*.
3. **Compute-on-change, cached by content hash.** Any change to the store (import, result entry, edit, mute) changes its hash → the derived layer (ratings, Elo chains, goals model, league registry) is recomputed once and cached. Renders always read derived state that provably matches the current store. Delete a row → numbers change.
4. **Calibration constants are artifacts, not constants.** Zone cutoffs, display-share mapping (CAL9), goals bands (EVG2), market error tables: each is regenerated by the replay harness from the store, versioned, shipped with a validation report, and replaced only when regeneration wins on held-out data. Hand-editing an artifact = instant fail.
5. **Parity rule (owner directive).** No feature ships for one class of teams without the same-class rollout. Every league gets: display name, canonical naming, match rows, form stats, venue support, one card grammar. Visible differences must be capability-driven (fitted vs evidence) and labelled — never code-path-driven.
6. **The system may always refuse.** NO CALL / no data stated plainly is a feature; fabricating a number is the failure.
7. **UI is a skin — and the surface never speaks backend.** The render layer reads a normalized result object only; a professional designer work order follows the build (Phase 8). Every user-visible string is plain language: no store/hash/key/fingerprint/graph-row/engine-jargon, no raw JSON, no stack traces. Status is icon-encoded with detail behind one tap; every process is a linear flow of at most three visible steps. Classy and smooth is a hard requirement, not a style preference.
8. **No data abolition (owner rule).** No row and no field is ever canceled, stripped or deleted — declared data is kept verbatim. The only sanctioned exclusion from computation is a **MUTE flag** on a suspicious match row: the row stays visible, is excluded from every compute path, and is reversible on owner-approved lists only. Every data field that leads to the final computation must be fully available.

## 4. Data tree flow (the architecture you build)

```
SOURCES: team packs (work orders) · CSV bulk (football-data) · manual result entry (Update tab)
      │  all pass the same gate
      ▼
① INGEST — validate grammar · canon names+leagues · dedupe by fingerprint
           90-min doctrine (AET/pens → draw + advancement NOTE) · tieId on two-leg ties
           MUTE channel · SOURCE url per row · ghost bans (no league w/o matches, no team w/o league)
      ▼
② SINGLE STORE  (localStorage + drive-folder sync)  ←→ store content hash
      ▼
③ DERIVED LAYER (recomputed on change, cached, never hand-edited)
   league registry → from data | DC ratings per fitted league | one Elo chain for all teams
   goals model | calibration artifacts ← replay harness + validation report
      ▼
④ SELECT FIXTURE → one identity per side (or NO CALL)
   capability probe (fitted league? graph depth? venue known?) → PATH DECISION, printed on card
      ▼
⑤ COMPUTE live → fitted path: probabilities · markets · scorelines
                 evidence path: H2H/common/L3 shares · form · goals band
                 neither → NO CALL
      ▼
⑥ ONE CONFIDENCE GATE — one label vocabulary for both kinds (validated on replay pre-ship)
      ▼
⑦ ONE NORMALIZED RESULT OBJECT → ⑧ RENDER SKIN (replaceable)
      ▼
⑨ ONE LOG — every save settleable; settled results feed the replay harness (loop closes)
```

---

## 5. Decision register (owner-set, 2026-08-02 — do not re-litigate)

| # | Decision | Set value |
|---|---|---|
| D1 | Third system `FOOTBALL_HOME_SYSTEM.md` (xMargin) | **Excluded** — separately owned product; never fold in silently |
| D2 | External 202k-match dataset (`00_MANIFEST.md`) | **Not adopted as-is** (season-stamped dates, no tie links, no venue flags, no cups — blueprint violations); clean bulk is commissioned instead (Annex A) |
| D3 | Density floor for Dixon-Coles fit | ≥2 full seasons of complete league rounds from the unified store, **and** the fit must beat the evidence graph on masked replay for that league, else it stays evidence-path |
| D4 | Update cadence | Derived layer recomputes automatically on change; result entry stays manual: paste → preview → commit (owner keeps control) |
| D5 | New raw data | Annex-A researcher brief + football-data CSV primary; official-federation + fbref cross-checks |
| D6 | Runtime | One self-contained HTML file, internally layered as §4 (no backend, no build step, no framework) |
| D7 | Rollback | Enforced from Phase 0 (snapshot + golden behaviour matrix) |
| D8 | Validation loss on any gated component | **Hold the phase** — blueprint stop rule applies to architecture exactly as to predictions |
| D9 | Entry point | Data workstream (Annex A) starts **parallel, day one**; new-app build proceeds on current store; fixtures render with whatever data exists (parity-honest), and gain depth as bulk lands |
| D10 | Priority inside build | P0→P2 → P4/P5 parallel → P6 → P7; P3 integration is continuous as Annex-A bulk arrives |

---

## 6. Phases and gates

Each phase ends with **gate evidence** per §8. Do not start the next phase on code you have not gated.

### Phase 0 — Baseline freeze
Tasks: snapshot current app (file + md5 + store export); build the **golden behaviour matrix** (Annex C fixture set × every output class, both engines) pinned as a data file the harness can diff against; write the migration/rollback plan for Phase 1.
**Gate:** matrix captured and reproducible from a clean boot; snapshot stored; rollback tested at least once.

### Phase 1 — Single store and schema
Tasks: define the one schema (§3-1); migrate MODEL fitted parameters into it as team/league *attributes* (`fittedRatings`), migrate BP store and embedded seed, merge identity collisions to one row (Dynamo-Moscow class solved by canon/alias/fingerprint rules), unify helpers (one `esc`, one canon module), retire the duplicate IIFE patch pattern; migration of the owner's current live store (1,336+ rows + log) must run on first boot with a summary report.
**Gate:** every team resolves to exactly one identity row; migration report shown; golden matrix still passes (documented drift only, each line explained).

### Phase 2 — Live-compute core
Tasks: all engines become pure functions of the store: evidence engine (paths/sections/zones — mostly there), one global Elo chain, goals model, DC batch fit/online update rewritten over store rows; derived-layer cache keyed to store hash; league registry derived from data; artifact-regeneration pipeline (replay harness emits versioned artifacts + validation report). `ENGINE_SPEC.md` requested before DC fit details; until then you may port the fit procedure, not alter its conventions.
**Gate:** cache proven (mutate store → derived values change); identical inputs reproduce golden numbers (documented drift only); artifact report generated, not written by hand.

### Phase 3 — Data completion (continuous, fed by Annex A researcher)
Tasks: integrate arriving bulk per league through ① INGEST; publish the **coverage matrix** (league → rows · seasons · gaps · status); cure ghost classes by **attaching the commissioned match rows** — declarations are retained verbatim, never stripped; pending rows render the honest no-data state until their data lands; MLS round-2 closure per `WORKORDER-MLS.md`; load the already-delivered Southampton / Ross County / St Johnstone packs.
**Gate (final):** every displayed league has full match rows for the Annex-A window; coverage matrix shows no ghosts; reconciliation tables reproduced 20/20 per league-season.

### Phase 4 — One confidence gate, one strength scale
Tasks: one gate function accepting either computation kind, one label vocabulary; strength shown on one scale with provenance label (fitted vs Elo). Calibrated component: re-validate on held-out replay against both old gates before shipping (D8 applies).
**Gate:** one function/labels everywhere; validation table shown for both input kinds; ship only on win/tie.

### Phase 5 — Venue bridge + single router
Tasks: venue check reads unified venue data for every fixture; cross fixtures get a real check when data supports it, generic warning only when genuinely absent; router dispatches by capability probe, never by membership of a list.
**Gate:** cross fixtures with venue data receive the same category of venue check as fitted-league fixtures.

### Phase 6 — Single render pipeline (plain, skin-ready)
Tasks: one normalized result object (§4-⑦); one card component; content driven by capability+labels (percentages iff calibrated fit; evidence shares iff graph; NO CALL otherwise); retire duplicate card builders; old-model teams gain league-name framing, form stats, evidence sections — parity audit table in the gate evidence. Keep visuals deliberately plain: structure and wording complete, styling minimal; the skin is Phase 8's job.
**Gate:** same fixture driven through each path yields identical structure/vocabulary, differing only in numbers and capability labels; parity audit clean.

### Phase 7 — Compliance suite
Tasks: re-run every existing harness (extended, not shrunk); itemize `LIVE-BLUEPRINT.md` known-defects line-by-line pass/fail; provenance table check per output; refusal paths all fired; frozen-settlement discipline confirmed (no frozen number changed by the rebuild; settlement still keys to the slate artifact). Written report delivered.
**Gate:** the compliance report itself is the deliverable; auditor re-runs it.

### Phase 8 — Designer handoff work order
Tasks: produce the designer pack — normalized result-object spec, component/state inventory, wording table, sample fixtures per capability class; designer restyles the skin layer only; owner approves the skin before it ships.
**Gate:** design WO delivered; engine untouched by any design commit.

---

## 7. Engineering conventions (mandatory)

- Single HTML file, internally layered exactly as §4 (store / derived / compute / confidence / result-object / skin). No frameworks, no build step, no network calls from the app.
- All user- or data-derived strings pass through the one `esc()` before reaching innerHTML. **Backend vocabulary is banned from all user-visible text** (store, hash, key, fingerprint, graph rows, engine names, calibration constants, raw grammar); the audit greps for it.
- Data enters **only as files** through the linked drive folder (or the file picker, which writes to the same staging). Accepted: `.txt`/`.md` (pack blocks, type detected by header, not extension), `.csv` (defined schema), `.json` (unified backup). Paste-text input is retired; the legacy paste endpoint is removed in Phase 1 migration.
- Tests: `smoke_test.js`-style idiom (node + vm + DOM stub) is the pattern; every phase **adds** pins and keeps the whole suite green; suite output is part of your gate evidence. Version strings: badge + footer both, one version per ship, old strings removed; every ship has an md5-stamped backup in `backups/`.
- Performance budgets on a 20k-row store: derive-on-change < 2 s; fixture render < 100 ms; import of a 1,000-row pack < 5 s. Store budget: keep serialized state under localStorage limits at 20k rows (drive sync is the overflow path — already exists).
- Determinism: same store hash → same derived hash → same rendered numbers. Date-sensitive code takes the date as input, never hidden `new Date()` inside compute paths.

---

## 8. Hand-back and audit protocol (you → auditor)

Per phase, deliver: (1) the file(s); (2) test commands and their raw outputs; (3) the phase-gate evidence mapped line-by-line to §6; (4) a `ZONES.md` changelog entry draft (versioned, with numbers, including honest no-ships); (5) md5 snapshot in `backups/`.
The auditor will: re-run every harness from scratch; diff against the golden matrix and the pre-ship backup; verify claims against the store, not your prose; return a corrections list. **A gate you assert without output = failed gate.** Corrections are iterated until the auditor's runs confirm green.

---

## 9. Non-negotiables (regressing any of these fails the phase)

- Results only — no bookmaker odds, prices, implied probabilities, external Elo, analyst picks, injuries, lineups, suspensions, transfers, congestion, anywhere in any engine input. (Odds may exist only in the separate integrity-screen files, never entering the app.)
- 90-minute scores only; advancement/pens facts live in NOTE rows; two legs linked by tieId, never treated as independent.
- No absent-record-as-never-met without external check · no season-stamped dates as exact dates · no full home advantage at neutral/relocated venues · no raw chain estimate presented as probability · no GD-estimate-to-over/under conversion · no one-path high confidence · no outlier dominance without sensitivity note · no silent fixture substitution · no in-sample "validation" claims.
- No frozen settlement number is ever edited; new data may change forward numbers, not published ones.
- No feature for one class of teams without the same-class rollout (parity rule).
- Ghost ban: never create a new ghost (no league entry without match rows behind it; no team row without a real league). Existing ghost declarations are cured with data, not deleted.
- **No data field or row is ever canceled or abolished.** Suspicious games are MUTE-flagged only — visible, excluded from computation, reversible on owner-approved lists. Nothing else may exclude data.
- The system may always refuse (NO CALL) rather than fabricate.

---

## 10. Deliverables

1. The new app (one HTML file, `app-v3` line; old file kept untouched as legacy reference until Phase 7 sign-off).
2. Migration report (store schema, what moved, what was reconciled/dropped and why).
3. Coverage matrix (living document from Phase 3).
4. Compliance report (Phase 7).
5. Artifact-regeneration reports (zones/display shares/goals/markets — versioned, reproducible).
6. `ZONES.md` entries per ship; designer work order (Phase 8).

---

# ANNEX A — RESEARCHER DATA BRIEF (detachable; also a cold-start brief on its own)

**Goal: every league the app stocks gets full match rows — "almost all games should have full data."**
**Row completeness (owner rule):** every field that leads to the final computation must be fully populated — dates, competition name + type, home/away order, 90-minute scores, venue/stadium/city/country, tieId, sourceId, and every SEASON split field. A row missing a computation-relevant field is **rejected back to you**, not truncated. And no field is ever dropped from the grammar, even one no current computation uses — **no data field is canceled or abolished; we only blacklist suspicious games (MUTE), nothing else.**
Window per league: the two most recent **completed** seasons **+ the current season to the gather date** (future/dated-tomorrow rows are forbidden; today is the gather date).

**Scope (codes are mandatory in every TEAM/MATCH row from day one — no `NA`):**

| League code | Competition | Teams | ~League rows/season | Domestic cups in scope |
|---|---|---|---|---|
| E0 | England Premier League | 20 | 380 | FA Cup + League Cup: every tie involving ≥1 stocked club |
| E1/E2/E3 | England Championship / League One / League Two | 24 | 552 | same rule as E0 |
| SP1/SP2 | Spain La Liga / Segunda | 20/22 | 380/462 | Copa del Rey: same rule |
| D1/D2 | Germany Bundesliga / 2. Bundesliga | 18 | 306 | DFB-Pokal: same rule |
| I1/I2 | Italy Serie A / Serie B | 20 | 380 | Coppa Italia: same rule |
| F1/F2 | France Ligue 1 / Ligue 2 | 18 | 306 | Coupe de France: same rule |
| N1 | Netherlands Eredivisie | 18 | 306 | KNVB Cup: same rule |
| P1 | Portugal Primeira Liga | 18 | 306 | Taça de Portugal: same rule |
| B1 | Belgium Pro League | 16 | 240 + end-phase rows | Belgian Cup: same rule |
| G1 | Greece Super League | 14 | 182 + end-phase rows | Greek Cup: same rule |
| T1 | Turkey Super Lig | 19 | 342 | Turkish Cup: same rule |
| SC0 | Scotland Premiership | 12 | 198 + split-phase rows | Scottish Cup + League Cup: same rule |
| SC1 | Scotland Championship | 10 | 180 | (closes the known ghost league — full rows required) |
| RPL/FNL | Russia Premier / First League | 16/18 | 240/306 | Russian Cup: every tie with ≥1 stocked club (already-held methodology) |
| CZ1/CZ2 | Czech First League / FNL | 16 | 240 + group/playoff rows | MOL Cup: rounds where stocked clubs enter (R3+) |
| KOS | Kosovo Superliga | 10 | 180 | Kosovo Cup: same rule |
| MLS | USA Major League Soccer | 30 | ~510 incl. playoffs | **ALREADY COMMISSIONED — see `WORKORDER-MLS.md` round-2; do not duplicate, deliver the round-2 remainder only** |
| USL | USL Championship | 24 | ~360 incl. playoffs | US Open Cup: ≥1 stocked club |

End-phase/playoff structures (Belgium/Greece/Scotland/MLS) are in scope in full and must carry their official round/competition labels; a playoff tie decided on penalties or AET records the **90-minute score** with advancement in a NOTE.

**Sources hierarchy (conflict → higher wins, dispute recorded in NOTE):** (1) football-data.co.uk season CSVs (they cover every league above; they carry closing odds columns which go into the **separate** odds CSV, never the match pack); (2) official federation results pages (cross-check every cup row and every CSV anomaly); (3) fbref.com match logs (cross-check + home/away splits).

**Deliverables per league:** (a) one BP-TEAM-PACK v2 block (grammar in Annex B) or per-competition CSVs with the same fields; (b) `NAME|slug|Official Name (+accent aliases)` mapping sheet — one canonical spelling per club, aliases for every variant you encountered; (c) the final table per season with **W-D-L / GF-GA split home vs away per club and points** (deductions in NOTE with source) as reconciliation input; (d) SOURCE rows with plain URLs.

**Acceptance (the auditor recomputes):** row counts reconcile to official records per season/competition; your match rows reproduce each final-table split **20-team-out-of-20 per league-season** (or full league size); every cup row cross-checked; no duplicates, no self-games, ISO dates only, slugs stable across competitions; 90-min rule violations = whole return rejected.

**Estimated volume:** ~14,000–16,000 league rows + ~2,000–3,000 cup rows across the window. Deliver league-by-league (any order); each league is integrate-on-arrival.

---

# ANNEX B — BP-TEAM-PACK v2 grammar (canonical)

Header `BP-TEAM-PACK v2`, ends with `END`. One row per line, pipe-delimited, no pipes inside fields.
- `TEAM|name|country|leagueName|leagueCode|aliases(; separated)|stadium|city|country2|surface|capacity|founded|website` — **leagueCode mandatory, never NA**.
- `MATCH|date(ISO)|competitionName|compType|home|homeGoals|awayGoals|away|venue|stadium|city|country|tieId|sourceId` — compType ∈ `domestic-league|domestic-cup|league-cup|super-cup|uefa-cl|uefa-el|uefa-uecl|club-friendly|other`; **90-minute scores always**; two-leg ties share `tieId`.
- `SEASON|team|season|competitionName|scope|P|W|D|L|GF|GA|HP|HW|HD|HL|HGF|HGA|AP|AW|AD|AL|AGF|AGA|pos|pts|sourceId` — home/away splits mandatory.
- `VENUE|team|stadium|city|country|surface|capacity|type|note|sourceId` · `NOTE|level|team-or-tag|text` · `CTX|team|date|flag|detail|sourceId` (demote-only context; never direction inputs) · `MUTE|date|home|away|reason|sourceId` (integrity removals; stays a visible muted row, never silently deleted) · `SOURCE|sourceId|plain-url|date|kind|detail` — http(s) URLs only, no markdown; unverifiable item → `NOTE|warning|... blocker` and stop, never guess.

---

# ANNEX C — Golden behaviour matrix, fixture set (Phase 0 captures, every later phase diffs)

| Probe | League class | Must keep showing |
|---|---|---|
| Chelsea v Bournemouth (R·E0) | fitted domestic | full fitted card: probabilities, markets, scorelines, venue check |
| Arsenal v Bayern (E0×D1) | fitted cross | cross-bridge card with provenance note |
| CSKA Moscow v Spartak Moscow (RPL) | pack same-league | league-named card + evidence sections + zone statement |
| Malisheva v Drita (KOS) | pack same-league | same class as above |
| Atlanta United v Austin FC (MLS) | sparse league, zero-path | standalone-form honesty block, no fabricated split |
| Raith Rovers v Greenock Morton (SC1) | ghost league (cured by Annex A) | pre-cure: no-data honesty block; post-cure: full league card |
| Malisheva v Spartak Moscow | pack cross | cross evidence card, no league framing |
| Hibernian v Malisheva | model×pack mixed | evidence card with H2H path rows |
| Two sides with no shared rows at all | none | NO CALL, no numbers, load-guidance text |
For every probe: full output capture (markers per class), zone/word, splits, gates lines, goals line, save-row presence. Drift allowed only where a phase documents it, line by line.

---

# ANNEX D — Migration and user-state preservation

- Owner's live store (currently ~1,336–1,342 graph rows depending on branch history + saved log entries) must import on first boot of the new schema; produce a migration report (rows in/out, identities merged, mutes preserved — names canonicalized per the existing `TEAM_NAME_CANON` precedent).
- The unified export/import format (`pitch-rating-full`) keeps backward compatibility: old exports must load cleanly into the new app.
- Seeded embedded pack: its TEAMS without matches are **kept verbatim** (no data abolition, owner rule 2026-08-02) and cured by Annex-A commissioned rows (SC1 is commissioned in full); until their rows land they render the honest no-data state. Migration report lists them and their cure status.
- Old app file is never edited by this build; it stays the legacy reference and rollback anchor until Phase 7 sign-off, then is archived, not deleted.

---

# ANNEX E — Glossary (cold start)

**Dixon-Coles (DC) path** — fitted attack/defence/home-advantage ratings per team, Poisson score grid → probabilities/markets/scorelines. Needs a validated per-league fit (Decision D3).
**Evidence path** — path analysis over raw match rows: direct H2H, common opponents, level-3 chains → weighted shares + zone statement; no probabilities without a calibrated table.
**Zone** — a statement band over evidence shares (STRONG/WIN/WIN-DRAW/lean/TOSS) with demote-only gates (confirmation, draw-risk, perf, star, TB honesty, context). Statements, never instructions.
**Masked replay** — compute on historical games with later information hidden; the only permitted validation method for anything calibrated. Split-half: must win in both halves.
**CAL9/EVG2/zone table** — display-share mapping, goals-band table, win-rate table for zone labels; artifacts regenerated from replay (§3-4).
**Ghost** — a team/league entry that exists as a declaration with no match rows behind it. Forbidden end-state.
**Frozen** — published numbers that govern settlement forever; forward computations may move, frozen ones never change.
**MUTE** — integrity-flagged match row excluded from every computation path but visible and reversible on owner-approved lists only.

---

# ANNEX F — DATA OPERATIONS (target state; replaces any paste-box intake)

**One law: every byte of data enters through the same gate — no side doors. Nothing ever leaves except by MUTE flag (no-abolition rule).**

## F-1 Channels (three, identical rules)

1. **Drive folder (primary).** Owner links a folder once (browser folder access). Data arrives as files dropped there — researcher bulk, matchday updates, corrections. The app stages every new/changed file automatically.
2. **File picker.** Same pipeline, for when the folder is not linked; chosen files write into the same staging.
3. **Automated feed (future, optional).** Only if it passes F-2/F-3 untouched; until then it does not exist.

Formatting freedom for senders: `.txt`, `.md` (pack blocks — type detected by header, not extension), `.csv` (schema in Annex B), `.json` (unified backups). Paste-text input is **removed**.

## F-2 The file lifecycle (what the owner sees)

```
file lands in folder ─▶ staged file card (name · size · date · source tag)
   │ auto-validate: grammar · canon names/leagues · dupes · 90-min doctrine ·
   │                tieIds · completeness (no missing compute fields) · no future dates
   ▼
status icon set:   ✓ valid (tap → one-line summary)
                   🕐 hold (unverifiable rows — tap → exact rows and why)
                   ✕ rejected (tap → defect list; nothing stored)
   ▼ owner approves (one tap)
snapshot taken silently ▶ committed ▶ plain-language confirmation
   e.g. "Russia — 212 matches added · complete through MD3 · 1 suspicious row flagged for your review"
```

Backend never surfaces: no hashes, keys, fingerprints, row grammars, engine names in any confirmation — teams, leagues, dates, counts, states only.

## F-3 Audit position (unchanged, blocking)

Validation and owner approval do not replace the auditor: reconcile-checks (standings splits 20/20), cross-source spot checks, same-class sweep, and identity-merge previews (shown before any key rewrite) run before commit. The commit is atomic with a rollback snapshot.

## F-4 Icon vocabulary (highlight-led, details on tap)

| Icon | Meaning | Tap reveals |
|---|---|---|
| 🟢 | verified / complete | as-of date + row count in words |
| 🟡 | partial / season in progress | what's missing, who's supplying it |
| 🕐 | hold — unverifiable | exact rows, both sources |
| ✕ | rejected | defect list to return to sender |
| 🚫 | muted (integrity) | reason, evidence, restore control (owner-only) |
| 💾 | snapshot available | restore point |
| 📄 | request / document | the generated file |

## F-5 Data requests — the system writes the brief

"Request data" flow: pick a league or team → the app generates the request file itself — no hand-writing: exact scope (seasons, competitions, expected row counts), the required format (Annex-B grammar with a filled example for that league), the alias-sheet requirement, the sources hierarchy, and **the acceptance checks the auditor will run on the return** (row-count reconciliation, 20/20 split reproduction, dup/date rules). It also names the expected file (`league-<code>-<window>-<date>.txt`) and where to drop it in the folder. The file is saved to the drive folder, ready to send. Request states track as: drafted → sent → partial → complete, with the coverage matrix closing the loop.

## F-6 Data Ops console (structure only — skin is Phase 8)

Six modules, each one view + one primary action, nothing else:
**Files** (staged cards; approve) · **Coverage** (league cards: state icon + completeness in words) · **Requests** (generate/track request files) · **Calibration** (replay runs, artifact versions, win/loss record in plain words) · **Log & Settlement** (open statements vs frozen slates, ledger) · **Integrity & Snapshots** (mute manager — owner-only actions; rollback points, one-tap restore).
Wording standard: "Russia — complete through MD2", never "644 matches / 26 identities / hash a1b2…".

## F-7 League lifecycle (labels visible everywhere a league appears)

`REQUESTED → STAGED → LOADED (evidence-carrier, honest caps) → CALIBRATED (full fitted card, replay-validated) → STEADY (matchday deltas)`; `DORMANT` for ended competitions with all rows retained (no-abolition). Promotion needs the D3 fit gate (≥2 full seasons + masked-replay win in both halves); a league that never passes stays evidence-path, labelled, not ashamed.
