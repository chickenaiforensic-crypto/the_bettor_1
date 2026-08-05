# REPAIR-SPEC-R30-2026-08-03 — 16 misdated held RPL rows (auditor, wave-2 finding)

Decision pending: owner/builder choose the route. Auditor recommends ROUTE A (in-place date edit in the app data).
Do NOT repair via a correction import: the dedup key is date+home+away, so corrected rows would DUPLICATE the wrong ones.

## Route A — in-place edit (recommended): for each row below, change ONLY the date field (stored -> correct). Nothing else changes; scores/advancement untouched.

| # | competition | homeId | awayId | score | WRONG date (stored) | CORRECT date | round |
|---|---|---|---|---|---|---|---|
| 1 | Russian Premier League | `russia|akron tolyatti` | `russia|lokomotiv moscow` | 1-4 | 2025-05-19 | **2025-05-24** | R30 |
| 2 | Russian Premier League | `russia|cska moscow` | `russia|pari nizhny novgorod` | 2-0 | 2025-05-19 | **2025-05-24** | R30 |
| 3 | Russian Premier League | `russia|dynamo makhachkala` | `russia|fc rostov` | 1-1 | 2025-05-19 | **2025-05-24** | R30 |
| 4 | Russian Premier League | `russia|fakel voronezh` | `russia|krylia sovetov samara` | 1-1 | 2025-05-19 | **2025-05-24** | R30 |
| 5 | Russian Premier League | `russia|fc krasnodar` | `russia|dynamo moscow` | 3-0 | 2025-05-19 | **2025-05-24** | R30 |
| 6 | Russian Premier League | `russia|rubin kazan` | `russia|fc orenburg` | 4-2 | 2025-05-19 | **2025-05-24** | R30 |
| 7 | Russian Premier League | `russia|spartak moscow` | `russia|fc khimki` | 5-0 | 2025-05-19 | **2025-05-24** | R30 |
| 8 | Russian Premier League | `russia|zenit st petersburg` | `russia|akhmat grozny` | 3-0 | 2025-05-19 | **2025-05-24** | R30 |
| 9 | Russian Premier League | `russia|baltika kaliningrad` | `russia|dynamo moscow` | 1-2 | 2026-05-11 | **2026-05-17** | R30 |
| 10 | Russian Premier League | `russia|cska moscow` | `russia|lokomotiv moscow` | 3-1 | 2026-05-11 | **2026-05-17** | R30 |
| 11 | Russian Premier League | `russia|dynamo makhachkala` | `russia|spartak moscow` | 0-0 | 2026-05-11 | **2026-05-17** | R30 |
| 12 | Russian Premier League | `russia|fc krasnodar` | `russia|fc orenburg` | 3-0 | 2026-05-11 | **2026-05-17** | R30 |
| 13 | Russian Premier League | `russia|fc rostov` | `russia|zenit st petersburg` | 0-1 | 2026-05-11 | **2026-05-17** | R30 |
| 14 | Russian Premier League | `russia|krylia sovetov samara` | `russia|akron tolyatti` | 4-1 | 2026-05-11 | **2026-05-17** | R30 |
| 15 | Russian Premier League | `russia|pfc sochi` | `russia|akhmat grozny` | 1-1 | 2026-05-11 | **2026-05-17** | R30 |
| 16 | Russian Premier League | `russia|rubin kazan` | `russia|pari nizhny novgorod` | 2-2 | 2026-05-11 | **2026-05-17** | R30 |

## Route B — MUTE-and-re-add: MUTE these 16 rows (no-data-abolition doctrine keeps them visible-but-muted), then import the 16 corrected rows as a normal mini-pack. Slower, more moving parts; only if Route A is impossible app-side.

## Evidence (primary source, fetched fresh 2026-08-03)
- RSSSF Russia 2024/25 (rsssf-ref/rus2025.txt L745): `Round 30 [May 24. Total Att: 151,884]` followed by all 8 fixtures — scores/sides byte-identical to held rows.
- RSSSF Russia 2025/26 (rsssf-ref/rus2026.txt L740): `Round 30 [May 17. Total Att: 160,780]` followed by all 8 fixtures — scores/sides byte-identical to held rows.
- 5 lookalike rows on the two wrong dates were CLEARED (genuine R29 Monday games: rus2025 L741 `[May 19]`; rus2026 L729 `[May 11]`) and are NOT in this spec.
- Held store currently contains 0 rows on the two correct dates -> repair cannot collide.

## Verification after repair (owner can self-check)
- Coverage row count must NOT change (3,3xx -> same number; only dates move).
- RPL 2024-25 season should then show its final round on 2025-05-24; RPL 2025-26 final round on 2026-05-17.
