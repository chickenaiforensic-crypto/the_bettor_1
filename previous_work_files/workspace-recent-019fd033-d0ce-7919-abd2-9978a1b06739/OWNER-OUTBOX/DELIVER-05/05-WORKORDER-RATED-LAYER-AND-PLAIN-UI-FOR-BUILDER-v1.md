# WORKORDER v1 — RATED-LAYER-01 + UI-PLAIN-01 (combined drop): restore rated cards after country replace + plain-language UI

- **Date:** 2026-08-04 (UTC) · **From:** Auditor · **To:** Builder · **Priority:** P1 (ships AFTER the import run closes; one drop, one audit)
- **Base file:** v3.6.3 · md5 `17dd2b5b66ceb572a3fd946db9b56a92` · 635,798 B
- **Ship:** v3.6.4 (every ship bumps upward; badge + footer). No changes to ingest/commit/dedupe/scope/purge/migration/storage/schema except where stated. Never a zip.

---

## D1 — RATED-LAYER-01: rated layer must survive purge-and-replace (code-proven gap)

**Mechanism (auditor evidence on v3.6.3):**
1. Rated fixture card (Match outlook + Form stars + tier classification) needs `fittedAvailable = home.fittedRatings && away.fittedRatings && home.leagueAttrs` (L2398) for the migrated path; stamps are attached to identity rows once by `loadFitted` (L1855-1895), which runs only when the `dc-fitted-model` artifact is absent — i.e. **once ever**.
2. `purgeScope` deletes orphan identity rows (proven: Russia purge removed 26 clubs; England purge removed the ~114 model-created team rows) and does NOT touch `dc-fitted-*`/`dc-gate-validation` artifacts (by design).
3. Re-imported pack teams create **bare** identity rows (commit L985/1103) and are never re-stamped → every fixture involving them fails `fittedAvailable` → app falls back to evidence view. Honest, but rated UI "disappears" (owner-reported 2026-08-04).
4. Context for correct scoping: the legacy fitted model covers 18 leagues (B1,D1,D2,E0,E1,E2,E3,F1,F2,G1,I1,I2,N1,P1,SC0,SP1,SP2,T1) — **not** RPL/CZ1; RPL/CZ1 rate via the online replay-validated path (`__DC_GATE__ = {RPL:true, CZ1:true}`).

**Required fix:**
1. Make fitted stamping **idempotent and re-runnable**: after boot/derive (or on explicit Calibration action), stamp `fittedRatings`/`leagueAttrs` on any existing identity whose canon name matches the fitted roster and that lacks stamps. Log stamped counts (type 'system', action 'fitted-refresh', provenance 'migrated model 153,058 matches').
2. **Do NOT** recreate pure model-team identity rows for teams with no match rows (ghost class stays cured — ZONES v0.14/history).
3. Re-run masked replay on the current data window and refresh gate verdicts: RPL and CZ1 now hold 5 full in-store seasons each (data-side verified 1,220 and 1,401+202 rows); EPL holds 5 seasons (1,900) — if the replay wins for a league, record it in the `dc-gate-validation` artifact with n, window, validated date; if not, league stays evidence (honesty rule).
4. Migration/boot stamping of a store that already has artifacts must converge to the same stamped state (idempotence), no duplicates in artifacts.

## D2 — UI-PLAIN-01 (owner decree 2026-08-04): every owner-facing screen in plain human language

1. All owner-facing strings (hold lines, staged/toast messages, scope/purge screens, migration summaries, request/coverage labels, calibration cards) must read as plain English sentences. Machine keys — e.g. `czech relegation playoffs|bohemians 1905~opava`, `( / )`, codes like Z-003 — allowed only inside a collapsed/small-print **"Technical details"** line under the human sentence.
2. Example rewrite for hold #1: plain line → "These two teams played each other twice but the file doesn't link the matches as a pair. Nothing will be changed — scores are kept as written." Technical details → the original validator string verbatim.
3. No logic/behaviour change — string layer only (auditor byte-diff must show strings/labels only, plus D1 code).

## D3 — Acceptance gate additions

- **G14 (new, mandatory):** rated-layer regression — fixture in a fitted-model league whose country was purged+re-imported shows the rated card (outlook, Form stars, tier) after refresh; stamping counts logged; replay refresh evidence shown (masked replay numbers on new window for RPL/CZ1, EPL attempt recorded either way).
- G13 (hold-approve) re-run green; all prior suites stay green (smoke 49, scope 43, legacy 156, hold 9).
- Return: full HTML + md5 + sha256 + byte size + UTC build stamp; repo commit sha if a repo exists (state honestly if not).

## D4 — Explicitly out of scope

Data changes (none permitted; D-rule), hold-detection logic, dedupe fingerprints, scope/purge semantics, storage keys.
