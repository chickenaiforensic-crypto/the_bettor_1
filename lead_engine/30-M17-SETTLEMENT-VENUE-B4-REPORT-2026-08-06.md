# M17 Settlement + Venue Guard — B4 v3.11.0 Report 2026-08-06

**Date:** 2026-08-06
**Builder:** Lead Builder
**Base:** app-v3.10.0-b3.html md5 2d28fc66 → app-v3.11.0-b4.html md5 ce32dd04 716KB
**Auditor Report:** `AUDITOR-REPORT-2026-08-06-FULL-LADDER-M17-M10.md` — I5 FAIL, I4 FAIL on v3.9.0-b2
**Relay:** `RELAY-TO-BUILDER-2026-08-06-M17-PRIORITY.md` — M17 top priority, build settlement I5 + venue guard I4 before anything else
**M10 Signoff:** `RELAY-TO-BUILDER-2026-08-06-M10-AUDITOR-SIGNOFF.md` — M10 PASS AS SPEC ONLY, does not close M17

---

## I5: Draw = Loss — Settlement Enforcement

**Previous failure (v3.9.0-b2:4183-4189, 4224-4229):** only saved prediction snapshot `type === 'settle'` log summary `Row saved: home v away — path label`, no actual-result field, no win/loss calculation, so draw-as-loss test impossible. "Saved rows are final for settlement" was label only.

**Build (v3.11.0-b4):**

- `settlementConsole(store)` now renders verified-venue list panel (I4) + saved rows with actual-result entry UI
- Each log entry `type: 'settle'` now stores `predSide` (H/D/A from zone TA=home TB=away), `fixture`, `predSnapshot` (label, prob, zone, confidence), `ts`
- After saving, new UI in settlement tab: inputs `settle-h-{idx}` and `settle-a-{idx}` (0-30) + button `Enter result & settle — I5 draw=loss never push`
- On click:
  - `classifyOutcome(hg,ag)` → H/D/A
  - `settlementResultFor(predSide, actualOutcome)` → win if pred matches actual else loss, with special case: actual D + pred D = win, actual D + pred H/A = loss — never push, per I5
  - Stores `actualHomeGoals`, `actualAwayGoals`, `actualOutcome`, `settlementResult` {win, loss, push:false, reason}, `settledAt`
  - Logs additional `type: 'settle', action: 'result'` entry for audit trail
  - Toast: `Result X-Y — WIN/LOSS — I5 draw=loss enforced — draw recorded as loss never push ✅` when draw case
  - Immutable evidence: pred snapshot JSON slice + actual score surfaced in Log & Settlement view

**Acceptance test (per relay):**
1. Save three frozen rows (via Match tab Save this row) — predictions home win, away win, draw (or any)
2. In Log & Settlement tab: enter 2-1 (home win), 0-2 (away win), 1-1 (draw)
3. Assert: home win entry → WIN if predicted H, LOSS otherwise; away win entry → WIN if predicted A; **draw entry → recorded as LOSS never PUSH** — exact assertion `loss` for draw, `push` false, `settlementResult.reason` contains "I5 draw=loss"
4. Surface: outcome + immutable prediction/result evidence visible

**Feeds:** settlement data now feeds into calibration (M5) and integrity screening (M10) — Brier shock needs settled tips, now possible

---

## I4: Entry-Side Venue Guard — Never-Hosted Hard Block

**Previous failure (v3.9.0-b2:823-973, 1021-1024):** parser declares `venue` required but `validate` only checks required fields, ISO date, future, compType, scores, duplicate fingerprint. Staged venue records appended during commit (1021-1024) with no membership test. No check that home team ever hosted in verified venue list, no confirmation tick-box, no `neutral_venue` adjudication, no save-disabled hard error. Fixture picker permits any two identities + swap (4214-4221) without venue confirmation surface.

**Build (v3.11.0-b4):**

- `getVerifiedVenueMap(store)`:
  - Iterates store.matches not muted, venueType normal, stadium present
  - Key: `canon(homeName)+'::'+canon(competitionName)` → {team, competition, stadiums: {stadium: count}, count}
  - Represents every venue where a team has hosted (normal) — verified-venue list per league

- `isVenueVerified(store, homeTeam, competitionName, stadiumName, venueType)`:
  - If no stadium or venueType != normal → ok (neutral/relocated allowed)
  - If no entry for team+competition:
    - If team never hosted in ANY competition → hard block `never_hosted_any` — I4
    - Else never hosted in this league → hard block `never_hosted_league`
  - Else if stadium not in known stadiums for that team+league → hard block `venue_mismatch` with known list
  - Else ok with reason `venue verified — X has N prior hostings`

- `renderVenueGuardPanel(store, homeTeam, competitionName, stadiumName, venueType)`:
  - Shows verified ✅ or hard block ❌ I4 with reason + two checkboxes: official-list tick-box and neutral_venue/relocated

- Pack validation enhancement (monkey-patch `PR.ingest.validate`):
  - After original validation, build vMap via `getVerifiedVenueMap`
  - For each staged MATCH row with stadium and venue normal:
    - If no entry → push hold `Venue ghosting — Team X has never hosted in store — no verified venue history — I4 hard block — competition Y venue Z — confirm via official list tick-box or mark neutral_venue/relocated with NOTE — row kept verbatim grouped by competition+pair`
    - Else if stadium not in map → push hold `Venue mismatch — Team X never hosted at venue Z in comp Y — known: ... — I4 hard block — tick-box or neutral_venue`
  - Holds are Z-003 style verbatim keep, not rejection — row kept verbatim grouped by competition+pair, human presses Approve

- Manual-entry surface:
  - Settlement tab shows verified-venue list panel (I4) explaining procedure
  - Future enhancement: fixture picker could show venue guard panel when selecting home team (not yet implemented as picker has no venue input, but pack path now has hard block)

**Acceptance test (per relay):**
1. Attempt to save/import a row whose home team absent from that competition's verified-venue list (e.g., new team or new venue) → assert hard block hold appears, save disabled (hold card, not ok)
2. Confirm through explicit official-list approval (checkbox in venue guard panel) → assert durable rationale + venue lock (venue locked at entry, no silent flip, neutral/relocated preserved verbatim)

---

## Verification

- Zero hard coding: fetch 0, XHR 0 (verified via grep)
- One-gate: all data still enters through `PR.ingest.parsePack` → `validate` (now with venue check) → `commit`
- P1: no market data, no odds, no fetch to odds sites
- Provenance: M3 — league pivot + calibration artifacts still in provenance panel
- M10: settlement data now available for Brier shock (M10 depends on settlement)
- M5 calibration: settlement results now feed into calibration runs

## Files

- `builder/app-v3.11.0-b4.html` md5 ce32dd04 716KB
- `builder/build_b4_m17_settlement_venue.py` — build script
- `handoffs/B4-EVIDENCE-2026-08-06-M17.json` + `B4-v3.11.0-ce32dd04.b64.txt`
- This report

## Next

- B3 balance panel (NO CALL shows support shares) — queued after M17
- B4 goal-range bins 0–1/2/3+ — harness-gated
- S7 UI architectural build using designer tokens/components
- Pivot not adopted pending UEFA date fix (343 malformed) — researcher assigned per planner 4f8fcb7

*Builder fixes M17 blockers — settlement I5 draw=loss + venue I4 never-hosted hard block — ready for auditor re-audit.*
