# AUTO-REQUESTS — standby optional request emitter (shipped v2.8.2, 2026-08-01)

User directive: "things not analyzable are data we can analyze — the system can auto-audit
and place standby optional requests; once answered by copy/paste in the parse format,
the system gains extra input around its gap spots and extra windows per game."

## Doctrine (unchanged, binding)
- OPTIONAL: an unanswered request changes nothing. The analysis stands as computed.
- Conditions answers (CTX lines) are demote-only context (C4/v2.7.0) — they can lower a
  zone one rung per flag against the leader; they NEVER raise a zone or add direction.
- Results answers (MATCH rows) are phase-1 evidence: parsed via the existing pack import
  with sources, 90-minute scores, strict causality (date < cutoff).
- No fabricated %: requests never invent numbers; they name the gap and the format.

## What the emitter checks per analysis (7 gap spots)
1. Sparse history: either side Elo-star < 5 → CTX conditions window request (template prefilled).
2. No H2H evidence (h2hN = 0) → historical mutual results as MATCH rows.
3. Cold start (<3 current-tourney games, either side) → early-season/preseason MATCH rows.
4. Cup-only side (rows exist, no league rows) → league season MATCH rows.
5. Ledger-open gap touching the competition → standing note (R-02 Czech 2.liga; R-06 Balkan
   dates; Russian First League scope gap).
6. Section conflict (contra section ≥55) → conditions for the contra-leading side (CTX).
7. Thin evidence ring (<20 paths) → additional common-opponent/league coverage.

## Answer formats (both already parse in-app, Data tab → import)
- CTX|Team Name|YYYY-MM-DD|keeper-change/star-absence/new-manager-debut/rotation-risk|detail|sourceRef
  (team name as shown in the analysis; date must equal the fixture date; demote-only)
- MATCH|YYYY-MM-DD|Competition|domestic-league|Home|HG|AG|Away|normal|unknown|City|Country||sourceId
  (plus the matching SOURCE row; per BP-TEAM-PACK v2)

## UI (v2.8.3)
- Block renders collapsed: "Standby optional requests (N)" + [Copy templates] + [Download
  .txt] buttons; "View all N requests" expands typed items + the answer file.
- Download filename: requests-003chome003e-v-003cold003e-003cdate003e.txt; payload identical to the
  on-screen answer file and to clipboard contents.

## Verification
- Display-only confirmed: Akron v Rubin 2026-08-01 zone bit-identical pre/post emitter
  (TB WIN 70.6%); emitter fired exactly one request (Akron cold start) — correct gap.
- Harnesses: smoke 79 ✓ packs 27 ✓ closure 19 ✓ concat ✓ replay unchanged ✓.
- Build: build_e_requests.py (5 edits). No zone, share, gate or ladder behavior touched.
- v2.8.3 render re-verified on CSKA v Krylya 2026-08-01: zone bit-identical
  (TA WIN-DRAW 56.5% vs pre-UI build); details/buttons/txt all present; harnesses green.
