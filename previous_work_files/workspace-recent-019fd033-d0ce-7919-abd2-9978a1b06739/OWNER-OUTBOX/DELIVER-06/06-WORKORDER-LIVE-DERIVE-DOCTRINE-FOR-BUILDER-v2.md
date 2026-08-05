# WORKORDER v2 — LIVE-DERIVE-01 (doctrine) + UI-PLAIN-01: retire bootstrap ratings, compute live or stay silent, show provenance in-app

- **Date:** 2026-08-04 (UTC) · **From:** Auditor (owner directive) · **To:** Builder · **Priority:** P1 — one drop after the import run closes. Supersedes DELIVER-05 (never sent; kept as history).
- **Base file:** v3.6.3 · md5 `17dd2b5b66ceb572a3fd946db9b56a92` · 635,798 B
- **Ship:** v3.6.4 · full HTML only, never a zip · return md5 + sha256 + bytes + UTC build (+ commit sha if a repo exists, else honest note)

---

## Owner doctrine (verbatim intent, binding)

The system is a **live-computing** system: every number on screen is derived from the store's match rows by engine code running in the app. Precomputed material brought in from the old project ("bootstrap") must not silently pose as live computation, must not be load-bearing once sufficient data exists, and its presence must be disclosed. Where the data cannot support a live rating, the app says so plainly — it never hides, never fakes.

## D0 — BLOB-INVENTORY-01: full disclosure of every precomputed input (audit base, code-proven on v3.6.3)

Embedded / brought-in, NOT derived from the owner's store (this is the complete list — builder must confirm each line or correct it with code references):

| # | Item | Lives in | Origin | Load-bearing for | State after the 2026-08-04 data programme |
|---|---|---|---|---|---|
| 1 | `window.__FITTED_MODEL__` (~419 KB: 18 league attrs, per-league team rosters [att,def,homeExtra], draw_table/base, star_*/rho/shrink params, 6 global tiers, markets coefs, consensus/records) | inside the app file | legacy model fitted externally on 153,058 matches | migrated rating path (`fittedAvailable` stamps) for its 18 leagues (incl. E0, SC0) — NOT RPL/CZ1 | **Orphaned** for replaced countries: identity rows carrying stamps were purged (RUS 26, ENG ~114); stamps never re-run |
| 2 | `window.__DC_GATE__ = {RPL:true, CZ1:true}` | inside the app file | replay validation run outside the app (legacy) | enables live (online) fitted path for RPL/CZ1 | stale provenance — verdict predates the new 5-season data; must be re-producible by the app itself |
| 3 | `dc-fitted-*` artifacts (model/draw-table/tiers/markets/records) | store | stamped once from #1 | migrated path lookups | intact (purge cannot delete them) but detached from current identity rows |
| 4 | `dc-gate-validation` artifact | store | stamped once from #2 | `gateVerdict()` | as #2 |
| 5 | Calibration artifacts (`zone-table`, `draw-table`, `confidence-table`, `goals-band`, `market-calibration`, `replay-validation`) | store | app-run masked replay (live-capable) | confidence/display | need regeneration on the new data (one button exists: Run masked replay) |
| 6 | Engine constants (ELO.INIT/K/HF; DC defaults) | code/blob | engine defaults | live ELO + DC | fine as defaults; must be documented, not hidden |
| 7 | `teamStats` cache | store | derived cache | derived displays | empty since migration — must rebuild at derive (register + fix if not) |

Live-derived and healthy (no action): evidence engine (zone graph/shared-match analysis), ELO table + ELO stars (rebuilt from rows every derive), online DC fit (`derived.dcFit` → `predictOnline`), dedupe/ingest/scope machinery.

## D1 — LIVE-DERIVE-01 (the fix)

1. **Rated capability is derived, not carried.** A league is rateable ONLY when the app's own masked replay on current store rows shows the DC fit beating the evidence engine (split-half, strict causality). Verdict artifacts carry the numbers every time: n, window, Brier(DC) vs Brier(evidence), validation date.
2. **Auto re-validation on data change.** Any commit/purge/migration invalidates league verdicts; next derive recomputes (fit + replay) for leagues with sufficient window (≥2 full seasons). No once-ever gating.
3. **No rating pinned to purgeable rows.** Ratings/stamps are recomputed at derive or resolved by canon name at compute time. Purge-and-replace cycles must leave the rated layer consistent (this is gate G14 below).
4. **Bootstrap demotion.** Legacy fitted params (#1) may rate a league ONLY below the sufficiency threshold, and the card must say in plain words: "Rated from the historical model — not from your data yet." Once live validation passes, live params take over and the bootstrap label disappears from that league.
5. **Retire #2 as an input.** `__DC_GATE__` may remain only as dated provenance text; it must not enable anything. Enabling comes solely from the app's own replay verdicts.
6. **Live form stars G17 (auditor finding 2026-08-04, code-proven):** the ONLINE (live) path's predictor returns `starsHome:null, starsAway:null, starAdj:false, consensus:null, confidence:null` — form stars and venue-record labels were NEVER computed from store rows; they existed only via legacy records-table lookups (`starsFor`). Compute form stars + venue-record consensus from store rows on the live path (same shrink/min-games/hysteresis rules, parameters derived per league), or render a plain "not rated yet" label. Nothing in between.
7. **Retire inert blob content honestly:** legacy `ship`/`caution`/`blocked` market-gating flags are written into an artifact but read by NO code path (grep-proven). Either consume them (visible market gating) or stop carrying them + say so in the provenance panel.
8. **Provenance panel (G15):** a plain "Where do these numbers come from?" view listing EVERY precomputed input from the D0 table with origin + last-derived date + status (live / bootstrap / stale). Nothing hidden ever again.

## D2 — UI-PLAIN-01 (owner decree, carried from DELIVER-05)

Every owner-facing string in plain English sentences; machine keys (validator pair strings, `( / )`, codes like Z-003) only inside a small-print "Technical details" line. String layer only.

## D3 — Acceptance gates

- **G14:** after purge + re-import of a rated league's country, the rated card returns (derived), with replay numbers shown; no dependence on legacy stamps.
- **G15:** provenance panel renders the D0 inventory verbatim-complete; auditor tick-checks each row against code.
- **G16:** bootstrap label test — under-sufficient league shows the plain bootstrap sentence; after sufficient data + passing replay, label is gone.
- G17: live form stars present (derived) or plain not-yet label; G13 + all prior suites stay green (smoke 49, scope 43, legacy 156, hold 9).
- Honesty: anything the builder judges impossible inside this file must be stated in the return, not worked around silently.

## D4 — Explicitly out of scope

Data changes (none), hold-detection logic, dedupe fingerprints, storage keys. No new external data files; this workorder concerns computation and disclosure only.
