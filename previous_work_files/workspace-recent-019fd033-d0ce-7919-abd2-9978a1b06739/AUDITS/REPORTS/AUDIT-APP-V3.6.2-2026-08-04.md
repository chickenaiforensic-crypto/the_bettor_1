# AUDIT — app v3.6.2 (WO-SCOPE-CLEAR-01 delta D1 + D3) — 2026-08-04

**Verdict: APPROVED FOR UAT.** Supersedes APP-V3.6.1 as the UAT target (strict superset).
Builder's self-reported suite counts are registered, never adopted at face value;
this approval rests on the independent checks below.

## 1. Transport (md5-on-arrival)

| item | MANIFEST claim | decoded actual | result |
|---|---|---|---|
| app-v3.6.2.html (634,591 B) | `c7f955d4aacdeaaca9a44e4314f2b14e` | `c7f955d4aacdeaaca9a44e4314f2b14e` | ✅ exact |
| ZONES-v3.6.2.md | `fd559974b2df643de45601e2bf04e45f` | same | ✅ exact |
| SCOPE-CLEAR-DELTA.md | `80ae2141e10400057d986d0f26f20006` | same | ✅ exact |

b64 armour again prevented transit junk: head `<!DOCTYPE`, tail `</html>`, no injected bytes
(cf. v3.6.0 which arrived with a 1,290-B Cloudflare tracking tail — stripped that time).

## 2. Diff vs pinned v3.6.1 (`762a62846eb5c9531627e1d67be365a8`, 630,593 B)

74 lines changed out / 121 lines in. **Every change confined to:**
- APP_VERSION bump 3.6.1 → 3.6.2 (+changelog comment) — version policy honoured.
- CSS block: `details.scope-country` tree styles + league-row hover (7 rules).
- `PR.scope` module (L2804–3000): D1 selection generalisation + D3 sorts + log labels.
- UI panel render + handlers: country `<details>` tree, per-competition rows,
  per-scope backup keying, filename slugs with competition.
- **Untouched (byte-identical):** ingest/dedupe (`Skipped duplicate match…` L1016),
  migration replace (`Store replaced by migration…` L3727), LS_KEY `pitch-rating-v3.store`
  (L378), hold/held-card logic, both sanctioned G4 muted-checks (L1223/L1283), engines.

## 3. Static gates

| gate | result |
|---|---|
| G10 no-hardcode inside PR.scope module | ✅ zero country/league literals (module L2804–3003, banned-list grep; earlier 1083/1173/8248 hits = pre-existing seed catalog + bundled pack text, out of module) |
| Network exfiltration | ✅ 0 fetch/XHR/beacon/WebSocket; 9 `https://` strings = inherited data constants, identical count to v3.6.1 |
| `slice(0, 400)` preview cap | ✅ 0 occurrences (D2 intact) |
| `C.esc` attribute safety | ✅ escapes `& < > "` (+`'`) — competition names in `data-scope-comp` safe |
| Versioning policy deviation | ✅ none — workorder said "v3.6.1 delta" but v3.6.1 was already sealed; builder correctly bumped to v3.6.2 (MANIFEST + Z-…-015 agree) |

## 4. Behavioural harness — the app's OWN module vs the live store

Method: extracted the exact `PR.scope` module (L2804–3000) from the pinned HTML,
ran it in Node 20 against the live export `pitch-rating-full-data-2026-08-02.json`
(1,432 rows) in store shape; stubs only for `PR.store.{log,save,contentHash}` and
`PR.derive.invalidate` — zero reimplementation of scope logic.
Script: `app-v362-audit/harness-v362.js` (re-runnable).

**RESULT: 32/32 PASS**, incl.:
- G1: 18 scopes, Σ = 1,432 (every row partitioned). NOTE: earlier memo "16 scopes" was
  loose — true count on this store is 18 (single-row scopes = European away legs /
  friendlies; Canada 4 = Canadian MLS home games). Big anchors exact: Russia 644,
  Czech Republic 632, US 81, Scotland 34, Kosovo 19 — identical to v3.6.0 census.
- D3/G13: countries A–Z; Russia competitions A–Z EXACTLY `Russian Cup 152 · Russian
  Premier League 489 · Russian Relegation Playoffs 2 · Russian Super Cup 1` (localeCompare).
- G2 (country level, backward-compat string form): Russia 644 selected · remaining 788.
- G2-L (D1 league level): MOL Cup 63 selected · remaining 1,369 · selection purity 0
  bleed · scopeKey label `Czech Republic / MOL Cup` · null-competition object form = 632.
- MUTE/UNMUTE: 644 flag→restore, 63 flag→restore; row count never moved; log lines carry
  `country`, `competition`, `preHash` (+post snapshot).
- PURGE MOL Cup (backup-gated call): −63 → 1,369 everywhere; **23 cup-only Czech clubs
  orphan-removed (Hořovice, Hlučín, Kroměříž … all proven zero remaining refs across
  matches/seasons/venues/ctxFlags/artifacts — the full keep-list)**; cross-scope
  survivors kept; sources kept by default; log carries backup filename; second purge =
  honest no-op with `scope-purge-noop` line.
- PURGE Russia (endgame rehearsal): → 788, zero Russia rows left.
- Unknown-scope guard: refuses, store untouched.
- Per-scope backup keying (code-read): `country '||' competition` — a country backup does
  NOT enable a league purge and vice versa (conservative, correct; documented in UAT G8).

## 5. Registered (not adopted) builder claims

DELTA doc: G2-L purge → 1,369 & CFL 561/playoffs 8 untouched ✓(proven here); G13 suite ✓(proven here);
D2 re-verify 644 rows ✓(cap grep = 0); suites "smoke 49/49 · scope 43/43 · parity 7/7 · legacy 156/156"
— registered, independent coverage = harness 32/32 above.

## 6. Known non-blocking notes

- Confirm-screen summary counts "45 clubs" for MOL Cup = all Czech-registered identities;
  actual deletions = orphans only (23) and the preview's remove/keep lists say so;
  purge log's `clubsRemoved` reports the true 23. Inherited country-level semantics
  from v3.6.0 — wording, not behaviour. Candidate cosmetic polish, no re-ship needed.
- Scopes with catalog-heavy club counts (e.g. Portugal: 1 match / 39 clubs) come from the
  seeded identity catalog; orphan rule still protects them at purge (zero-ref removal only).
- Researcher branch moved during this audit: HEAD `1da8826e205a` (2026-08-04T00:50:29Z) —
  RPL full-span ledger layer (32 official table lines + venues + wiki 2nd-index matrices
  240/240 score-identical ×2 seasons + RFU membership chain). Movement toward the
  complete-Russia commission (outbox file 02). Main unchanged `a98dffee709f`.

## 7. Pins

- app-v3.6.2.html `c7f955d4aacdeaaca9a44e4314f2b14e` (UAT: `APP-V3.6.2/`)
- v3.6.1 `762a62846eb5c9531627e1d67be365a8` (superseded, sealed) · v3.6.0 `edf52d78…` (sealed)
- rollback baseline v3.5.2 `6bd76ae0…` (sealed, untouched)
- harness `app-v362-audit/harness-v362.js` (re-run: `node harness-v362.js` → 32/32)
