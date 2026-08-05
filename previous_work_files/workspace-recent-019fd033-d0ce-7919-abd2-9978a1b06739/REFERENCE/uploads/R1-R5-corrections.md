# GATE EVIDENCE — Auditor corrections R1–R5 (2026-08-02, second working session)

**Engineer:** agent build · **Auditor:** system-side · **Status:** 🟢 all five corrections shipped and proven

Final file: `app/app-v3.html` · md5 `3048f269c7153fe18c9a7eae944cd752` (586,532 B) · backup `backups/app-v3.0.0-3048f269.html`

---

## R1 (blocking) — Picker/findability ✅
- Free-text search box (`#pick-search`) filters the team list instantly; match is canon-substring over name + canonical name + **all aliases** + league label, so "krasnodar" → `FC Krasnodar` (suffix/alias tolerant).
- League grouping via `<optgroup>` per league; **no league filter** — every identity in the store is listed (empty query returns all 539).
- **Acceptance (≤3 steps from cold boot)** — `harness/acceptance-r1-r4.js`:
  ```
  step 1 — type "krasnodar" → ["FC Krasnodar"]
  step 1 — type "fakel"     → ["Fakel Voronezh"]
  step 2/3 — FC Krasnodar & Fakel Voronezh selectable → true
  ```
- Audit pins (smoke): empty query lists all 539; "krasnodar"→FC Krasnodar; "fakel"→Fakel Voronezh; KOS evidence-only team (Drita) and SC1 ghost (Raith Rovers) both reachable; optgroup `Russian Premier League` present; `value="FC Krasnodar"`/`value="Fakel Voronezh"` present in the rendered picker. **No league filter hides evidence-only leagues.**

## R2 (blocking) — Final file + trail + CF grep ✅
- `grep -c "cdn-cgi\|challenge-platform" app-v3.html` → **0** (shown above; exit 1 = no match, gate passes).
- Seeds log as **`system` / `seed`** (9 entries), **zero** seed entries stamped `ownerApproved` (commit now branches on `opts.seed`).
- Mute reasons carry pack rationale: `integrity: market-flagged favorite collapse (IA-01/02/03)` — pinned in store + smoke.
- `"effective ? paths"` / `"? paths"` / `"? connections"` placeholders **gone**: confidence gate now receives real `effective`/`agree` from compute; rendered-card pin asserts no `?` placeholders; rendered proof: `effective 3 connections · agreement 54%` (R3 output above).

## R3 — Evidence card two-sided presentation ✅
- `evidence.sectionShares` now attaches each side's own record per section (H2H / Common opponents / Level-3 chains): `{p,w,d,l,gf,ga,from,to}` computed over the exact match ids that formed that section.
- Rendered (Malisheva v Drita, evidence card):
  ```
  H2H          read: 0% · 0% · 100%
               Malisheva 0W-0D-1L · 0-2 (1 game, 2026) · Drita 1W-0D-0L · 2-0 (1 game, 2026)
  Level-3      read: 60% · 40% · 0%
               Malisheva 1W-0D-0L · 2-0 (1 game, 2026) · Drita 0W-1D-4L · 5-10 (5 games, 2025–26)
  ```
- Pin: every section carries both sides' records with GF/GA + date ranges. Owner reads both performances without arithmetic.

## R4 — RPL fitted-card work order ✅ (DC WINS → fitted card enabled)
`harness/dc-vs-evidence-gate.js` — per-league DC online fit → masked replay vs evidence engine (strict causality: fit/predict only on rows with date < cutoff) → split-half validation:

| League | pool evBrier | pool dcBrier | half A ev/dc | half B ev/dc | verdict |
|---|---|---|---|---|---|
| RPL (641 rows, 2 full seasons + MD1) | 0.5929 | **0.5621** | 0.5940 / **0.5587** | 0.5917 / **0.5653** | ✅ DC wins (all three) |
| CZ1 (631 rows) | 0.6314 | **0.5822** | 0.6208 / **0.5609** | 0.6419 / **0.6013** | ✅ DC wins (all three) |

- Fitted card **enabled** for RPL and CZ1 with provenance on the card:
  `fitted on Russian Premier League 2024–26 — validated on 568 of 641 masked rows, 2026-08-02`
- Rendered: CSKA v Krylia → `Home 59.1% · Draw 23.9% · Away 17.0%` (fitted bar) + markets/scorelines + provenance banner.
- The verdict artifact (`data/artifacts/dc-gate-verdict.json`) is embedded in the build; `d3Gate` grants fitted only on `win` + ≥2 seasons. If a league fails the gate it stays evidence-path — the table is the answer (same offer for any league, including the remaining ones).
- Drift vs Annex C (RPL row expected evidence card): R4 supersedes it — the fitted card is the replay-validated, better-calibrated view; documented here line-by-line.

## R5 — Confirmation line ✅
```
PR.store.load().identities.length = 539
  declared (pack/seed TEAM rows):     149
  match-anchored (from match rows):    34
  model-rated (migrated fitted roster): 372
```
**Final number: 539** (matches the owner's recount; the earlier "520" was a stale pre-fix assembly — the same build now reports 539). Breakdown: 149 declared TEAM rows (7 packs + 2 embedded seeds) + 34 match-anchored identities (opponents seen only in match rows) + 372 model-rated (the migrated 153,058-match fitted roster, Annex D) = 539.

---

## Full harness state at ship
| Suite | Result |
|---|---|
| `smoke_test_v3.js` (new app) | **43/43** |
| `compare-legacy-engine.js` (evidence parity) | **7/7 identical** |
| `smoke_test.js` (legacy golden, untouched) | 156/156 |
| `dc-vs-evidence-gate.js` | RPL ✅ · CZ1 ✅ |
| CF grep gate | 0 |
