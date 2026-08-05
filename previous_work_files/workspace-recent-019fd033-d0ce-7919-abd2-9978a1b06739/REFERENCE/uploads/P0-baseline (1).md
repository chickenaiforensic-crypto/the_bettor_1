# GATE EVIDENCE — P0 Baseline freeze (2026-08-02)

**Engineer:** agent build · **Auditor:** system-side · **Status:** 🟢

## Golden reference freeze
- Legacy app `app-v2.6-cross.html` (md5 `14a7a9572f2428eb1689a2f601c3583c`) verified = **v2.9.9** content (matches the ZONES v0.18 backup hash exactly; the "legacy" file is the newest build). Never edited — it is the rollback anchor and port source.
- Legacy store census confirmed live: **792 identities / 1,421 matches / 3 mutes** — bit-exact vs ZONES v0.14.

## Commands + raw outputs (auditor re-runs)
```
$ node harness/smoke_test.js          → RESULT: 156 passed, 0 failed
$ node harness/validate_packs.js      → RESULT: 27 passed, 0 failed
$ node harness/validate_closure.js    → RESULT: 19 passed, 0 failed
$ node harness/concat_test.js         → combined 61 | sequential 61 | fingerprints identical: true
$ node harness/replay_test.js         → ran clean (h2h 5/14 · common 4/7 · third 4/8)
$ node harness/usa_verify.js          → ran clean (aetScore 1-1 · usl true · usoc 21)
$ node harness/verify_rpl_pack.js     → ran clean (TB WIN-DRAW 48.5%)
$ node harness/census_connectivity.js → ran clean (RPL 171/171 · FNL 21/21 · CZ1 171/171 · CZ2 325/325 · KOS 45/45 · DEN 3/3 · MLS 343/435 · USL 48/78 · SC1 0/21 ghosts · USL1 1/1)
$ node harness/census_filter.js       → ran clean
$ node harness/audit_league_paths.js  → ran clean (Chelsea v Bournemouth → DOMESTIC)
```

## Harness notes
- `zone_tally_ctx.js` requires `rpl/rpl_universe.json` — an external calibration file NOT in the bundle. Per no-fabrication rule we did not invent it; regeneration from the russian pack is queued in P2 artifacts (same pipeline the WO mandates). `audit_fixtures.js`/`audit_flip.js` reference the same file; both are exercised against the canonical store via `run-legacy-audits.js`.

## Rollback rehearsal
- `backups/app-v3.0.0-<md5>.html` — md5-stamped pre-ship snapshot of the new app (see P1/P2 gate evidence).
- Rollback path: legacy `app-v2.6-cross.html` untouched at `reference/` + `/home/user/app-v2.6-cross.html`; restore = revert to it (smoke 156/156 still green on it).
