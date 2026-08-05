# MIGRATION GATE — live store export → app v3.5.1 — 2026-08-02

**Source file:** `pitch-rating-full-data-2026-08-02.json` · 1,132,200 B · md5 `5a8ba49475acfa2340ce7fd66e4dfeb0` · format `pitch-rating-full` v1 · exported by owner from the live old app.
**Method:** stripped source census, then the app's OWN machinery end-to-end in a vm harness (`STORE.deserialize → migrate` → save to localStorage → `boot()` → reload → probes). Every claim below is printed output, not assumption.

## Source census (what the owner sent)
1,432 matches (2024-05-07 → 2026-08-01, 22 competitions) · 792 identities (object keyed by id, e.g. `kosovo|malisheva`) · 86 venues · 215 sources · 1,078-entry aliases map · 74 teamStats records · calibration null · log empty · **0 muted rows, 0 mutes array** (nothing to preserve — no-abolition not exercised) · 0 undeclared match references (no ghost class).

## Gate results
| Check | Result |
|---|---|
| migrate() | `ok:true`, rowsIn **2,525 = rowsOut 2,525**, unmapped: `[app, exported, blueprintVersion, aliases, teamStats, calibration]` (listed honestly) |
| Identities | 792 in → **792 out** ✓ |
| Matches | 1,432 in → **1,432 out**, per-row replay of all 1,432: **0 mismatched** on name/score/date/competition ✓ |
| Venues / sources | 86/86 · 215/215 ✓ |
| Migration log | `system/migration — 2525 rows carried` ✓ |
| **Real boot** (save → boot → reload) | artifacts stamped: `dc-fitted-model` + draw-table/tiers/markets/records + `dc-gate-validation`; log adds `system/fitted-migrate`, `system/dc-gate` |
| Fitted path on migrated store | **CSKA–Krylia = `fitted`** 0.589/0.239/0.172, markets+scorelines+stars+graph sections present (seed store reads 0.591/0.239/0.170 — drift explained by the 11 owner-only rows; data governs) |
| Gate grant | artifact data keys = **RPL, CZ1** (CZ team leagueCodes correct: Sparta/Slavia/Plzeň = CZ1) |
| Picker | 792 reachable · krasnodar→FC Krasnodar · **ross→Ross County · johnstone→St Johnstone** (Scottish teams ride along — no longer ghosts) |

## Reconciliation vs seeds (replace semantics)
- Owner store = **1,432** (their live truth; +11 rows since the builder's fixture census: 10 Scottish Premiership 2025-26 rows incl. Hibernian's run-in + MOL Cup 2025-04-09 Sparta–Teplice) — carried, authoritative.
- Seeds = 1,436 = same base **+15 Southampton rows** (the July-30 pack that reached the builder directly and lives only in seeds). A replace-migration drops those 15; the Southampton pack re-adds cleanly through the normal pack intake afterwards (one approval).
- This is why the owner's export must be the base: their live rows are real work, not fixtures.

## Defects found (→ R11)
- **M1 (blocker, owner-facing):** the migration machinery has **no UI path**. Dropping this exact file into the Data tab routes it to the pack parser → staged card **"Rejected — 38,877 defect(s)"** (`Line 1: unknown row type "{"`). `deserialize/migrate` is reachable only via the boot/localStorage path. The drive-upload decree makes this a must-fix: file-format sniff in `handleFiles` → migration card with explicit replace warning.
- **M2 (provenance):** mapper reads `m.sourceId` only; the real export keys it `m.source` → **1,432/1,432 migrated rows lose source linkage**.
- **M3 (provenance):** mapper reads `t.sourceIds/t.sourceId`; the real key is `t.source` (`MODEL.teams`, `BP-TEAM-PACK`…) → **792/792 identities lose provenance**.
- **M3b (design question):** 242 multi-league identities migrate with `leagueCode=null`; `d3Gate` season-count checks identity `leagueCode` for coded leagues → codeless teams invisible to future fitted-gate season counts. No impact on today's granted leagues (RPL/CZ1 teams single-coded).
- **Doc notes:** top-level aliases map + `teamStats` are derivable from carried rows (1,087 identity-level aliases carried) — acceptable as *derived-not-carried*, must be stated in the migration report, not silently dropped. `__DC_GATE__` is a build-time verdict stamped on any store lacking it — fine for today's identical data; the honest re-earn path is the Replay button (`replay-validation` artifact also accepted by d3Gate). Replay league-key hygiene: codeless competitions report by raw name (`uecl q2`, `Kosovo Superliga`) — cosmetic.

**Verdict: the migration CORE is sound and the owner's data survives whole — but the owner cannot use it until M1 ships (R11).** Evidence trail: this file + `audit351/gate_migrate.js` + harness outputs in session.
