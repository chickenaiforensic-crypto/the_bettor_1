# WORK ORDER — Scottish Premiership Full Repair v1.0

**Document ID:** `WORKORDER-SCO1-2021-2026-REPAIR-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Return:** `SCO1-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Why this is a full repair

A prior 1,140-row candidate reproduced a table but used placeholder stadium and city values. It is not ready for intake. Do not copy its rows or placeholders. Rebuild the full span from sources, including real venue and provenance fields.

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` in full before this document.

## 2. Exact scope

For every completed season 2021-22 through 2025-26, deliver:

| Phase | Rows per season | Competition name | Type |
|---|---:|---|---|
| Regular stage: 33 rounds | 198 | `Scottish Premiership` | `domestic-league` |
| Top-six post-split: 5 rounds | 15 | `Scottish Premiership Championship Round` | `domestic-league` |
| Bottom-six post-split: 5 rounds | 15 | `Scottish Premiership Relegation Round` | `domestic-league` |
| **Whole season** | **228** | | |

The completed five-season total is **1,140 rows**. Each club must have 38 league matches: 33 regular-stage plus 5 post-split.

If 2026-27 has started at your return date, include only completed source-confirmed matches and state its last included date and round in a NOTE.

Exclude Scottish Cup, Scottish League Cup, European fixtures, friendlies, and lower-league fixtures.

## 3. Exact team strings and membership

Use these strings only:

| Season | Exact roster |
|---|---|
| 2021-22 | `Aberdeen`, `Celtic`, `Dundee`, `Dundee United`, `Hearts`, `Hibernian`, `Livingston`, `Motherwell`, `Rangers`, `Ross County`, `St Johnstone`, `St Mirren` |
| 2022-23 | `Aberdeen`, `Celtic`, `Dundee United`, `Hearts`, `Hibernian`, `Kilmarnock`, `Livingston`, `Motherwell`, `Rangers`, `Ross County`, `St Johnstone`, `St Mirren` |
| 2023-24 | `Aberdeen`, `Celtic`, `Dundee`, `Hearts`, `Hibernian`, `Kilmarnock`, `Livingston`, `Motherwell`, `Rangers`, `Ross County`, `St Johnstone`, `St Mirren` |
| 2024-25 | `Aberdeen`, `Celtic`, `Dundee`, `Dundee United`, `Hearts`, `Hibernian`, `Kilmarnock`, `Motherwell`, `Rangers`, `Ross County`, `St Johnstone`, `St Mirren` |
| 2025-26 | `Aberdeen`, `Celtic`, `Dundee`, `Falkirk`, `Hearts`, `Hibernian`, `Kilmarnock`, `Livingston`, `Motherwell`, `Rangers`, `St Mirren`, `Dundee United` |

Source mappings must be noted once, including `Heart of Midlothian -> Hearts`, `Saint Mirren -> St Mirren`, and `Saint Johnstone -> St Johnstone`.

## 4. Sources

Primary RSSSF season pages:

```text
https://www.rsssf.org/tabless/scot2022.html
https://www.rsssf.org/tabless/scot2023.html
https://www.rsssf.org/tabless/scot2024.html
https://www.rsssf.org/tabless/scot2025.html
https://www.rsssf.org/tabless/scot2026.html
```

Cross-check every round against an independent source such as the official SPFL result archive or BBC Sport. Prove actual stadium and city from official club/competition records. No `unknown`, `Stadium`, or `City` values are allowed.

## 5. Required records

Use `MD1` through `MD33` for the regular stage. Make the post-split phase explicit in the venue field, for example:

```text
Championship Round MD34
Relegation Round MD36
```

Each row needs a real source, venue, city, country `Scotland`, and its exact competition name/type from section 2.

If a result is awarded, postponed, or abandoned, use the official standing result and describe the event in a NOTE.

## 6. Gates you must report

1. Five complete seasons × 228 rows = 1,140 rows.
2. Regular 12-club table exact for each season.
3. Championship and relegation six-club group tables exact for each season.
4. Every club has 33 + 5 matches in the correct phase.
5. Every row has real date, source, stadium, and city; zero placeholders.
6. Every round cross-checked independently; zero duplicate fingerprints.
7. One full source-linked spot-audit round per season.

## 7. Return

Commit one complete source-built pack on your own session branch. Send the director the branch, commit, path, MD5, SHA-256, counts by phase and season, and every blocker. Do not import it.
