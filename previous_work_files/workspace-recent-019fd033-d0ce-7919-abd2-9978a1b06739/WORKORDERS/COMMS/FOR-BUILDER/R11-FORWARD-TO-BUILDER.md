# R11 — migration gate fixes (v3.5.2) — FORWARD VERBATIM TO BUILDER

Context: the owner's REAL live-store export has arrived and was run through your migration machinery end-to-end. Core mapper works (2,525/2,525 carried, 0/1,432 row mismatches; real-boot flow stamps fitted + gate artifacts; fitted path live on the migrated store). Four fixes, acceptance contract below. Full evidence: auditor's MIGRATION-GATE-2026-08-02.md. Ship as **v3.5.2 via b64**. No other changes this round.

## M1 (P0) — wire store migration to the Data-tab intake
Today: dropping `pitch-rating-full-data-2026-08-02.json` into Data Ops routes to `parsePack` → staged card **"Rejected — 38,877 defect(s)"** (`Line 1: unknown row type "{"`). `STORE.deserialize/migrate` is unreachable from the UI.
Fix: in `handleFiles`, before the pack path, sniff JSON store exports (`.json` name AND/OR parsed object with `format==='pitch-rating-full'`) → call `STORE.deserialize` → stage a **migration card** (distinct from a pack card): summary like *"Store migration — 1,432 matches · 792 teams · 86 venues · 215 sources · REPLACES the current store — export first if unsure"* → approve runs save + re-render + toast + one `data/migration-commit` log line; discard does nothing.
Pin: feeding the real export file stages the migration card (not "Rejected"); approving it leaves the store at 1,432/792 with migration log present; the old pack path untouched.

## M2 — match provenance
Real export keys match source as `m.source` (`statarea-hib-last15`, `src-espn-bal-l1`, …); mapper reads only `m.sourceId` → 1,432/1,432 migrated rows get `sourceId:null`.
Fix: `sourceId: m.sourceId || m.source || null`. Pin: after migration, 0 matches with null sourceId when the source provided one.

## M3 — identity provenance
Real export keys identity source as `t.source` (`MODEL.teams`, `MODEL.hosted`, `BP-TEAM-PACK`, `BP-TEAM-PACK-v2`); mapper reads only `t.sourceIds/t.sourceId` → 792/792 lose provenance.
Fix: `sourceIds: t.sourceIds ? t.sourceIds.slice() : (t.sourceId ? [t.sourceId] : (t.source ? [t.source] : []))`. Pin: 792/792 migrated identities carry a non-empty sourceIds.

## M3b — multi-league identities invisible to the fitted gate
242 identities carry `leagues:[c1,c2,…]` (length>1) and migrate with `leagueCode=null`. `d3Gate`'s season count checks `identity.leagueCode === league.code` for coded leagues → those teams' fixtures never count toward fitted-gate seasons for their own leagues (no impact on RPL/CZ1 today).
Fix either: d3Gate additionally falls back to `canon(m.competitionName) === league.key` when the identity code is null/absent — or migration assigns the primary (first) league code. Pin: a synthetic 2-season store whose only league's teams all carry multi-league arrays with null code still reports `seasons >= 2` in d3Gate.

## Also required (documentation, not code)
State in the migration report/ZONES: top-level `aliases` map + `teamStats` are derived-not-carried (identity-level aliases carried: 1,087); `__DC_GATE__` is a build-time verdict for seed-era data, re-earnable any time via Replay (d3Gate accepts `replay-validation` artifacts); replay league-key hygiene (codeless competitions print raw names).

## Packaging note
A replace-migration drops the 15 Southampton rows that exist only inside your embedded seed (the owner never had them in the old app). Include the **Southampton pack as a standalone b64 file** in the v3.5.2 package so the owner can re-add it through the normal pack intake right after migrating (one approval).

**Acceptance contract (auditor will re-run verbatim):** gate script on the owner's real file → rowsIn=rowsOut=2,525 · 792/1,432/86/215 carried · 0 mismatched rows · M2/M3 null-counts → 0 · booted flow: gate artifact RPL+CZ1, CSKA–Krylia `fitted` · UI pin: real file stages migration card, approves to 1,432/792.
