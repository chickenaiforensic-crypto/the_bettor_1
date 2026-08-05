# DATA-REQUESTS — every known gap in the app data (2026-08-01)

Send each item in either of these formats and I'll convert, validate and reload:
```
YYYY-MM-DD | Home Team | score | Away Team            (one per line; ET games give the 90' score, final in brackets)
```
or ready-made BP-TEAM-PACK v2 MATCH rows.

## What is NOT missing (don't spend time on these)
- Czech First League: 100% of 2024-25 and 2025-26 league rows (552 incl. groups/playoffs) + 2026-27 played rounds — recomputed W/D/L/GF/GA matches RSSSF exactly, 64/64 checks.
- RPL league rows both seasons — reconcile 16/16 vs official tables.
- All H2H series, all standings, 2023-24 season (outside the frozen 2-season window), friendlies (excluded by policy), Czech cup rounds 1-2 (no top-flight side enters before R3), odds/injury feeds as direction inputs (banned by blueprint — they can only ever be CTX demote flags).

## R-00 — RESOLVED in this exchange
Pardubice v Baník Ostrava, MOL Cup 2025-11-05: 90' = 3-3 (AET 3-4), user-supplied. Patched into universe + pack (623 matches); analysis unchanged.

## R-01 — Czech MOL Cup ET games: exact 90-minute scores (6 games) — ✅ LOADED 2026-08-01
Your 90' reports matched my records on 5 of 6; one real correction applied:
Sparta v Teplice cup QF 2025-04-09 → 1-1 at 90' (was inferred 2-2). Draw/GD unchanged; data-truth fix.
ORIGINAL LIST (closed):
Impact: goal-difference averages only (all these are recorded as draws regardless).
| date | fixture | final (aet) | currently recorded |
|---|---|---|---|
| 2025-02-27 | Viktoria Plzeň v Zlín | 4-1 aet | 1-1 (inferred) |
| 2025-04-09 | Sparta Prague v Teplice | 3-2 aet | 2-2 (inferred) |
| 2025-09-24 | Frýdek-Místek v Pardubice | 1-2 aet | 1-1 (inferred) |
| 2025-09-30 | Artis Brno v Slovan Liberec | 1-1 aet, 6-5 pen | 1-1 (could be 0-0 at 90') |
| 2025-10-01 | Třinec v Hradec Králové | 3-4 aet | 3-3 (could be 2-2) |
| 2026-03-03 | Jablonec v Slavia Prague | 2-2 aet, 3-2 pen | 2-2 (could be 1-1) |

## R-02 — 2. liga 2025-26, full seasons for Zbrojovka Brno and Artis Brno — ⏳ WAITING ON YOU
Answer to your format question: send the COMPLETE dump — all 30 rounds, all games,
home AND away (filtered views would bias the star calibration). Dates mandatory.
Bonus if easy: full round-by-round for the whole division (also sharpens Taborsko/Chrudim context).

## R-03 — Czech relegation playoffs — ⚠️ RESOLVED VIA RSSSF AFTER SOURCE CONFLICT 2026-08-01
Your 2024-25 ties (Teplice-Opava, Jihlava-Pardubice) and 2025-26 Ostrava-Táborsko scorelines
CONFLICTED with RSSSF and were rejected (Teplice finished 11th on the validated 2024-25 table —
playoff sides were 14th Dukla and 15th Pardubice). Loaded per RSSSF tsje2025/tsje2026:
2024-25: Vyskov 0-0 Dukla (May 28) · Pardubice 2-0 Chrudim (May 28) · Dukla 1-1 Vyskov aet 4-2 pen (Jun 1) · Chrudim 1-0 Pardubice (Jun 1)
2025-26: Ostrava 3-0 Taborsko (May 26) · Taborsko 0-5 Ostrava (May 30) · Artis Brno 1-4 Slovacko (May 27) · Slovacko 3-0 Artis Brno (May 31)
NB RSSSF: all remain at former level; Artis later promoted via Karvina demotion.

## R-04 — RPL: Akron's May-2026 relegation playoff double-header — ✅ LOADED 2026-08-01
2026-05-27 Shinnik 1-2 Akron · 2026-05-31 Akron 1-0 Shinnik (comp RPLPO, user-supplied).
Impact check on the frozen Akron v Rubin call: zone and summation IDENTICAL pre/post
(TB WIN 69.4%, 42 paths) — playoff opponents sit outside the mutual web used; frozen call stands.

## R-05 — RPL cup ties with AET/pens (22 fixtures): exact 90' scores — ⏳ TEMPLATE RETURNED BLANK
Your message echoed the 22 fixtures back with empty "-" scores; they still need the true 90' numbers
(lowest priority — GD-only, none touch target clubs).

## R-06 — Kosovo Superliga 2025-26 + Albanian Superliga 2025-26
Full results WITH match dates (Wikipedia matrices carry no dates → currently unusable per causal rules).
Closes the documented Hibernian/Malisheva pack gap. Situational: only if we revisit those fixture classes.

## R-07 — Standing CTX feed (any time, per fixture)
`CTX|Team Name|YYYY-MM-DD|keeper-change / star-absence / new-manager-debut / rotation-risk|detail|sourceRef`
The demote-only layer (v2.7.0) is shipped and dormant — it arms as soon as you feed it.

## R-08 — C7 prospective (when the 20-game slate runs)
Old-app TIDE value per slate game (number or screenshot) so the TIDE-veto simulation settles prospectively.

## CUP-COMPLETENESS — RPL universe rebuild (2026-08-01, DONE by assistant from RSSSF rus2025/rus2026)
- Built authoritative cup row set (152 rows: 48+28 games 2024-25, 48+27 games 2025-26 + superfinals) in rpl/rpl_cup_full.csv.
- Diff vs old universe: 117 exact, 34 missing (added), 4 date conflicts → resolved: akhmat-zenit QF L2 = 2024-11-27 (universe correct, my transcription fixed); loko-akhmat & spartak-ural minor SF = 2025-04-15 (universe wrong, fixed); spartak-rostov minor final = 2025-05-15 (universe wrong, fixed); 2 duplicate rows removed.
- Universe now 643 rows; CUP rows 100% RSSSF-verified. R-05 partially moot: its 3 verified rows (Akron 1-1 Zenit 2024-08-27, Spartak 0-1 Rostov 2024-11-05, Akhmat 1-2 Zenit 2024-11-26... note: real leg date 2024-11-27) now live; its 16 fabrications confirmed absent; Rubin-CSKA 0-0 correctly dated 2024-11-06.
- App payload built: packs/russian-team-pack.txt (BP-TEAM-PACK v2, 26 teams, 643 matches, 4 sources, 7 provenance NOTEs incl. scope-gap + MD1-verification). Import through real app parser: 0 errors; replays Akron v Rubin bit-exact (TA 10.0/D 19.4/TB 70.6, TB WIN). Load THIS file into the app (Data -> Blueprint import); rpl_cup_full.csv stays as audit artifact only.

## C11 SHIPPED (v2.8.1) — from the 26-loss failure analysis
Trailer-star<5 demote-one-rung on STRONG/WIN. Post-ship: strong pair 89→93, win pair 83→89; monotone ladder; 17/26 losses + 5/9 big-margin caught; pool 167→116 actionable. C9 contra-section measured, rejected. Canonical replay pool fixed at 704/632 (pack imports included). App = v2.8.1-cross, all harnesses green.

## AUTO-REQUESTS shipped (v2.8.2) — in-app standby optional request emitter
Per-fixture auto-audit emits OPTIONAL, copy-ready requests (7 gap-spot checks); answers parse via existing CTX (demote-only) and MATCH import paths. Display-only: zones bit-identical, smoke 79 green. Spec: AUTO-REQUESTS.md. The standing ledger above stays the manual queue; the emitter automates its per-fixture edge.
