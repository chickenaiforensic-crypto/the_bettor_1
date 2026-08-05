# GATE EVIDENCE — P6 render pipeline + UI skin (2026-08-02, session amendment)

**Engineer:** agent build · **Auditor:** system-side · **Status:** 🟢 (skin approved in-build; Phase 8 designer pack follows)

## One normalized result object
`compute.selectFixture()` returns ONE object: `{ok, fixture, path, capability, sections[], confidence, honesty, provenance}`. The render layer (`ui.js`) reads ONLY this object. Same fixture through fitted vs evidence paths → same structure/vocabulary, differing only in numbers + capability labels (parity audit below).

## Parity audit (same fixture, each path)
| Fixture | Path | Card sections |
|---|---|---|
| Chelsea v Bournemouth | fitted | outlook · markets · scorelines · stars · venue |
| CSKA v Krylia | evidence | read (zone) · graph · goals · form · venue |
| Atlanta v Austin | evidence zero-path | form · honesty · venue |
| Raith v Morton (ghost) | none | no-view + honesty |
| Unknown sides | none | no-view + load guidance |

Structure identical (fixture head → path line → sections → confidence line → save row); vocabulary identical; capability labels differ (`Rated model` vs `Match history`).

## UI skin (classy and smooth — WO §3-7)
- Dark premium default + light editorial toggle (`data-theme`), serif wordmark, pitch-emerald accent, card system, status dots, icon-encoded console states (F-4), ≤3-step flows, toast confirmations, responsive grid.
- **Plain-language surface**: audit greps for backend vocabulary (contentHash, fingerprint, localStorage, CAL9, EVG2, PHASE_WEIGHT, raw shares, etc.) — none appear in user-visible strings; verified in smoke (no-jargon pins).
- Console: Files (drop/stage/approve) · Coverage · Requests (app writes the brief, F-5) · Calibration (replay + artifacts) · Log & Settlement · Integrity & Snapshots (mute manager).
- Data intake is file-only (dropzone/picker → ONE ingest gate → stage → approve → commit). No paste endpoint (grep pin ✅).

## Verified render output (node+vm drive of the real render())
- Chelsea v Bournemouth: fixture, probability bar, markets, scorelines, confidence, save row ✅
- CSKA v Krylia: zone read (calibrated display 52.6/24.7/22.6), section balances (H2H 60·40·0 Σw15.0), Total summation (62.5·25.0·12.5 + display), goals read (est 2.69 MID), form, venue ✅

## Performance
- Boot + seed load (9 packs → 1,436 rows) in VM: ~5 s (node); browser render budget within WO targets (derive <2 s, render <100 ms on 20k-row design — hash-cached).
