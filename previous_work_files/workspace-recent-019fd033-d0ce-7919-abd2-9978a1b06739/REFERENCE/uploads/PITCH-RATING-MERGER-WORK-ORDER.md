# Pitch Rating — Full System Merger — Engineer Work Order

**Purpose:** Merge the two currently-separate prediction engines running inside `app-v3_0_2-conform.html` into one application with one data store, one confidence system, and one display grammar. No new methodology is being invented — this is a merger of two systems that already work, done without breaking either.

**Binding governing documents (the engineer must read these before writing any code, and may not contradict them):**

| Document | Governs |
|---|---|
| `ENGINE_SPEC.md` | The Dixon-Coles rating engine — layer order, constants, fitting procedure, output provenance, refusal paths |
| `LIVE-BLUEPRINT.md` | The evidence-graph engine — binding operating rules, phase protocol, adaptive calibration, balance panel, known defects not to regress |
| `PITCH-RATING-COMPLETION-PHASE-LIST.md` | The original phase plan this work order supersedes/extends |
| `RESEARCHER-COLD-START-WORKORDER.md` / `RESEARCHER-FAST-BATCH-REQUEST.md` | The row formats and acceptance gates for any new match data commissioned during this build |

If any instruction in this work order conflicts with one of the above, the engineer stops and asks — does not silently pick one.

---

## 0. What currently exists (audit summary — verified against the code, not assumed)

Two engines run inside one HTML file, dispatched by `renderRate()`:

| | Dixon-Coles engine (`MODEL`) | Evidence-graph engine (`BP`) |
|---|---|---|
| Covers | 18 hard-coded leagues (`E0`, `SP1`, etc.) | Any team with loaded raw match rows (currently ~Russia, Czech Republic, small pools) |
| Core computation | Fitted `att`/`def`/`hfa` parameters, Poisson scoreline grid | H2H + common-opponent + opponent-of-opponent graph traversal |
| Needs raw match rows at runtime? | No — runs on fitted parameters + season aggregates | Yes — this is its only input |
| Live-updatable? | Yes — `applyResult()` (line ~2145) does incremental online-gradient updates matching `ENGINE_SPEC.md` Part B3, but **only for teams already in `MODEL.teams`** | Yes, trivially — just add match rows, no refit step exists because there's no fitted state |
| Output | H/D/A probabilities, tiers, markets (O/U, DNB, handicap), scoreline grid | Signed GD estimate → qualitative zone (STRONG CALL/WIN/WIN-DRAW/lean/TOSS/NO CALL) |
| Confidence gate | `consensusFor()` — home/away GD-split filter | `classify()`/`computeZone()` — agreement + path-count + 4 demotion rules (C5/C8/C11/C13) |
| Data store | `MODEL` object, hard-coded JSON literal in the file | `BP` object — `localStorage` + optional local-folder sync, separate identity/match/venue stores |
| Code origin | Original app | Later IIFE bolted on via `patchShowView()`/`patchSaveRating()` at `boot()`, with its own duplicate `esc()` (line 2736) |

**Confirmed gaps (not assumptions — checked in code and in the uploaded data export):**

1. `flipCheck()` never reads `BP.venues`, even though venue rows are collected (`addVenue`, line 2997). Cross/evidence fixtures always show the generic "cannot be auto-checked" warning regardless of whether venue data exists.
2. `pitch-rating-data.json` (the current live data export) has **zero raw match rows** for any of the 18 built-in leagues — only season aggregates (`teamStats`). Confirmed by direct count: 114 England identities, 0 England matches.
3. Real match rows for at least 3 built-in-league teams (Southampton; Ross County; St Johnstone) **were already researched and delivered** (`Southampton_BP-TEAM-PACK_v2.txt`, `Ross-County_St-Johnstone_BP-TEAM-PACK_v2.txt`) but never made it into the live store — the pack that *was* imported (`MASTER-RECORD-CLOSURE-ONLY-ALL-MISSING-v2.txt`) explicitly excludes MATCH rows by design (line 5: "excludes FORM and MATCH rows intentionally to avoid duplicate graph rows during record-closure test").
4. `applyResult()` (the live-update loop) hard-requires the team already exist in `MODEL.teams[lg]` — it cannot bootstrap a new league from zero. A new league needs one offline batch fit first (`ENGINE_SPEC.md` Part I, "Cold-Start Rebuild Order").
5. A separate, external, much larger dataset exists (`00_MANIFEST.md` — 202,092 matches, 1,532 clubs, 57 countries, built by a different Python pipeline, `chain.py`/`segment_test.py`) that is **not wired into the app at all** and carries documented defects that would violate `LIVE-BLUEPRINT.md`'s own binding rules if used as-is: season-stamped (not exact) European dates, no aggregate-tie linking for two-legged ties, no neutral/relocated venue flags, cup matches skipped at ingest entirely.
6. `FOOTBALL_HOME_SYSTEM.md` describes a **third, unrelated system** (xMargin, home-win-only, validated on Nordic leagues) that shares no code with either engine above. It is out of scope for this merger unless the user explicitly asks for a three-way merge — flag this to the user, do not silently fold it in or silently drop it.

---

## 1. Definition of done ("gapless")

The merger is complete only when **all** of the following are true simultaneously:

- [ ] One data store (identity, venue, match, season, calibration) — no `MODEL` object and `BP` object as separate schemas.
- [ ] One confidence-gate function used by every fixture, regardless of which computation path produced the underlying estimate.
- [ ] One display grammar — one "star"/rating scale, one verdict-label taxonomy, one card layout — used by every fixture. No two cards for the same kind of information looking or reading differently for reasons that aren't about the actual evidence available.
- [ ] `flipCheck` consults venue data from whichever store holds it, for every fixture, not just `MODEL` leagues.
- [ ] Every league currently covered by `MODEL` OR by `BP` is still covered after the merge, with no silent loss of a working capability (markets, scoreline grid, H2H/common-opponent evidence, cross-border bridge, etc.).
- [ ] A fixture's computation path (Dixon-Coles vs evidence-graph) is chosen by **data sufficiency**, stated in the output, and never silently defaults.
- [ ] The already-delivered-but-unloaded match packs (Southampton, Ross County, St Johnstone) are loaded, or a documented reason is given for why not.
- [ ] All refusal paths from `ENGINE_SPEC.md` Part H and all "known defects not to regress" from `LIVE-BLUEPRINT.md` §7 still hold after the merge — verified by the compliance suite (§7 below), not assumed.
- [ ] Every prediction, from either computation path, is logged to one shared log, in one format, settleable the same way.

---

## 2. Phase-by-phase build order

Each phase has a **pass gate**. The engineer does not start the next phase until the current one's gate is met and shown to the user.

### Phase 1 — Single data store

**Tasks:**
- Define one schema: `identity_store`, `venue_store`, `match_store`, `season_store`, `calibration_store`, `audit_log` (per `LIVE-BLUEPRINT.md` §8's module list — these were already specified, just never unified).
- Migrate `MODEL.teams`/`MODEL.leagues`/`MODEL.records`/`MODEL.hosted` into this schema without losing the fitted `att`/`def`/`hfa` parameters (they become a "fitted rating" attribute on a team/league, not a separate object).
- Migrate `BP.identities`/`BP.matches`/`BP.venues`/`BP.teamStats` into the same schema.
- Resolve identity collisions: a team known to both systems (e.g. Southampton, appears in `MODEL.teams.E0` and in `BP.identities`) must become **one row**, not two, using the existing `LEAGUE_ALIAS`/`canonLg`/alias-merge logic as the starting point.
- Remove the duplicate `esc()` (and any other duplicated helper) — one shared helper library.

**Pass gate:** every team, whichever system currently rates it, resolves to exactly one identity row. No two objects hold the same team's data under different keys.

### Phase 2 — Close the known data-loading gap

**Tasks:**
- Load `Southampton_BP-TEAM-PACK_v2.txt` and `Ross-County_St-Johnstone_BP-TEAM-PACK_v2.txt` — these contain real, sourced MATCH rows for 3 built-in-league teams that exist but were never imported.
- Decide, with the user, whether to re-import `MASTER-RECORD-CLOSURE-ONLY-ALL-MISSING-v2.txt`'s match-stripped version for the *other* teams in that pack, or commission fresh full packs (with MATCH rows) for them via `RESEARCHER-FAST-BATCH-REQUEST.md`. Do not silently keep the aggregate-only version if a match-row version exists or can be commissioned.
- Run the existing duplicate/conflict checks (`INTEGRITY-AUDIT`, `dedupeIdentities`, `matchFingerprint`) across the merged set.

**Pass gate:** every built-in-league team has, at minimum, `TEAM`/`VENUE`/`SEASON`/`SOURCE` rows, and a documented status (has match rows / commissioned / explicitly deferred) for `MATCH` rows.

### Phase 3 — Bootstrap remaining leagues into Dixon-Coles form (only where the user wants this)

**Tasks:**
- For each league currently evidence-graph-only that has enough raw match density (engineer must state the density threshold used and why, referencing `ENGINE_SPEC.md`'s own "min matches to rate: 6" and the 153k-match scale of the original fit), run one offline batch fit per `ENGINE_SPEC.md` Part I ("Cold-Start Rebuild Order"), validated on held-out data before shipping.
- Leagues that do not clear that density bar stay on the evidence-graph path — this is not a failure, it's the correct refusal per `LIVE-BLUEPRINT.md` rule 10.
- Once bootstrapped, `applyResult()`'s live-update loop covers the league the same way it covers EPL.

**Pass gate:** every league is explicitly classified as "Dixon-Coles fitted" or "evidence-graph only," with the reason recorded, not left implicit in which code path happens to fire.

### Phase 4 — Merge the one true duplicate: the confidence gate

**Tasks:**
- Replace `consensusFor()` (Dixon-Coles side) and `classify()`/`computeZone()` (evidence-graph side) with **one** confidence-gate function.
- It must accept either kind of input (a Dixon-Coles probability triple, or an evidence-graph path set) and apply one shared notion of "how much do we trust this," producing one shared label vocabulary.
- This is a calibrated component. Per `LIVE-BLUEPRINT.md` §5, no candidate weighting/gate is operational until it wins on untouched historical fixtures — re-run the held-out validation before shipping, do not just port the old thresholds unchanged and call it merged.

**Pass gate:** one function, one set of confidence labels, used everywhere; validation results shown for both input types.

### Phase 5 — Venue bridge

**Tasks:**
- Wire `flipCheck()` (or its replacement) to consult venue data from the unified store for every fixture, not just `MODEL` leagues.
- Cross/evidence fixtures should get a real venue check when data supports it, and only fall back to the generic "confirm by hand" warning when venue data is genuinely absent — not by default.

**Pass gate:** a fixture between two evidence-graph teams with loaded venue data gets the same category of venue check as a Dixon-Coles fixture.

### Phase 6 — Single routing logic and single display grammar

**Tasks:**
- One dispatch function: for a given fixture, determine computation path from data sufficiency (fitted rating available and calibrated? raw match graph sufficient? neither → NO CALL), not from a hard-coded "is this one of 18 leagues" check.
- One render pipeline. Retire the duplicate card-building functions (`renderDomesticRate`/`renderCrossLeague` vs `evidenceCardHtml`/`evidenceSectionsCardHtml`/`renderEvidenceFixture`) in favor of one component that takes a normalized result object and displays it consistently, with the *result's own calibration status* determining what's shown (percentages vs evidence share vs NO CALL) — matching `LIVE-BLUEPRINT.md` §4's "Transparent balance panel" spec, which was written for exactly this purpose and never implemented as the single source of truth.
- One "star"/strength scale, used by both paths, clearly labelled with its source (fitted rating vs Elo-chain replay) so it's disambiguated by label, not by silently being two different numbers under the same word.

**Pass gate:** feed the same fixture through the pipeline via each computation path (using test fixtures) and confirm identical structure/vocabulary in the output, differing only in the actual numbers and calibration status.

### Phase 7 — Carry over each engine's "extra" capability without loss

**Tasks:**
- Markets (`O/U`, `DNB`, handicap) and the scoreline grid stay available wherever a calibrated Dixon-Coles fit exists — do not remove these for leagues that have them.
- For evidence-graph-only fixtures, markets stay withheld until a goal model is separately built and calibrated for that data (per `LIVE-BLUEPRINT.md` §7/Phase 7 gate) — do not fabricate markets from the GD estimate.
- H2H/common-opponent/chain evidence stays available for every fixture where raw match data supports it — including, once Phase 1–2 are done, built-in-league fixtures that previously could never show it (e.g. an EPL fixture could show real H2H if match rows are loaded for those teams).

**Pass gate:** no capability present in either engine today is missing from the merged app for the leagues that had it.

### Phase 8 — Compliance suite (run before promotion, not after)

**Tasks:**
- Re-run `ENGINE_SPEC.md` Part I's "31 checks + 110 functional tests" against the merged system.
- Re-verify every item in `LIVE-BLUEPRINT.md` §7 ("Known defects not to regress") explicitly, one by one, with a pass/fail line for each — not a general "looks fine."
- Re-verify the "Output provenance" table in `ENGINE_SPEC.md` Part G (which outputs are star-corrected, which use the shrunk goals grid, etc.) still holds after the merge.
- Confirm refusal paths in `ENGINE_SPEC.md` Part H still fire correctly (unknown team, <5 games, <4 home/away games, never-hosted flip, evenly-matched flip, unconfirmed venue, BTTS).

**Pass gate:** a written compliance report, itemized, delivered to the user before the merged app replaces the current one.

---

## 3. Questions the engineer must ask before starting — for the user to answer and hand back

The engineer should not guess on any of these. Collect answers first.

1. **Scope of `FOOTBALL_HOME_SYSTEM.md`:** is the xMargin/home-win system in scope for this merger at all, or is it a separate product? (It shares no code with either engine today.)
2. **Scope of the 202k-match external dataset (`00_MANIFEST.md`):** should the engineer repair its documented defects (season-stamped European dates, missing aggregate-tie links, missing venue flags, missing cup matches) and adopt it as the raw match source, or is it out of scope for now, with the smaller `BP.matches` store remaining the source of truth?
3. **Density threshold for "bootstrap a new league into Dixon-Coles form":** how many raw matches, over what time span, should be the minimum before a league is offline-batch-fit rather than left on the evidence-graph path? The original 18-league fit used 153,058 matches — what's the acceptable floor for a new league?
4. **Live-update cadence:** should `applyResult()`-style incremental updates run automatically on a schedule, or remain a manual "paste results → preview → commit" action, for the merged app? (`LIVE-BLUEPRINT.md` §8 specifies daily/weekly/monthly/quarterly cadences by task type — does the user want this automated, or do they want to keep triggering it themselves?)
5. **Where does new raw match data come from going forward** — continued use of the `RESEARCHER-COLD-START-WORKORDER.md`/`RESEARCHER-FAST-BATCH-REQUEST.md` manual research workflow, an API/feed, or both?
6. **Hosting/runtime:** does the merged app stay a single self-contained HTML file (current architecture), or should the engineer split it into a proper app with a backend/database? This changes almost every phase above.
7. **Rollback requirement:** `LIVE-BLUEPRINT.md` §8 requires rollback snapshots on major rebuilds — does the user want this enforced from Phase 1, or added later?
8. **Priority conflict rule:** if a phase's held-out validation fails to beat the current separate-systems baseline (e.g., the merged confidence gate in Phase 4 tests worse than the two old ones), does the engineer proceed anyway (ship the merge for architecture reasons) or hold that phase back until it wins on data? `LIVE-BLUEPRINT.md` rule 6 says "failed audit means STOP and NO CALL" — confirm this applies to *architecture* changes the same way it applies to predictions.

---

## 4. Non-negotiables (carried forward unchanged from `LIVE-BLUEPRINT.md` §7 and §1)

The engineer must not regress any of these during the merge:

- No treating an absent record as "never met" without checking external sources.
- No season-end placeholder dates used as exact match dates.
- No treating two legs of one tie as independent without an aggregate identifier.
- No full home advantage for neutral or relocated matches.
- No raw chain estimates presented as probabilities.
- No converting a goal-difference estimate into an over/under call.
- No calling one path high confidence.
- No letting one outlier dominate without sensitivity reporting.
- No silently substituting a different fixture when the selected one is unavailable.
- No claiming a weighting is validated from an in-sample result.
- No bookmaker odds, market prices, implied probabilities, external Elo, analyst predictions, injuries, lineups, suspensions, transfers, or fixture-congestion inputs, anywhere in either engine.
- The system may always refuse (NO CALL) rather than fabricate certainty.

---

## 5. Deliverables

- One application (single file or proper app, per the user's answer to Question 6 above).
- Migration report: what moved from `MODEL`/`BP` into the unified store, and any data dropped or reconciled, with reasons.
- Compliance report (Phase 8).
- Updated `LIVE-BLUEPRINT.md` change log entry and `ENGINE_SPEC.md` amendment log entry, since this merge changes application-integration status described in `LIVE-BLUEPRINT.md` §8.
- Rollback snapshot of the pre-merge app (per the freeze principle already used in `PITCH-RATING-COMPLETION-PHASE-LIST.md` Phase 0).
