# WORK ORDER — Kosovo Superliga Regeneration v1.0

**Document ID:** `WORKORDER-KOS-2021-2026-REGENERATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Supersedes for dispatch:** the old Kosovo league assignment and every prior Kosovo candidate pack.
**Return:** `KOS-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Why this is a regeneration

The previous Kosovo candidate is rejected. It used false bulk dates, wrong 2023-24 clubs, and scores that did not reproduce the official table. Do not open, copy, repair, or use it as evidence.

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` in full before this document.

## 2. Exact scope

Collect the complete Kosovo Superliga regular seasons:

| Season | League rows | Clubs | Matches per club |
|---|---:|---:|---:|
| 2021-22 | 180 | 10 | 36 |
| 2022-23 | 180 | 10 | 36 |
| 2023-24 | 180 | 10 | 36 |
| 2024-25 | 180 | 10 | 36 |
| 2025-26 | 180 | 10 | 36 |
| **League total** | **900** | | |

Also include a promotion/relegation playoff only when the official season page records a tie involving a Superliga club. Use:

```text
competitionName: Kosovo Relegation Playoffs
compType: other
```

If 2026-27 has started by your return date, include only completed, source-confirmed matches and write the exact cutoff date and round in a NOTE.

Exclude Kosovo Cup, friendlies, Europe, lower-league fixtures, and every unplayed fixture.

## 3. Exact team strings and membership

Use only these strings. Source spellings map once in a `name_rename` NOTE.

| Season | Exact roster |
|---|---|
| 2021-22 | `KF Ballkani`, `Drita`, `Gjilani`, `Llapi`, `Prishtina`, `Drenica Skenderaj`, `Dukagjini`, `Malisheva`, `Ulpiana`, `Feronikeli` |
| 2022-23 | `KF Ballkani`, `Drita`, `Gjilani`, `Dukagjini`, `Prishtina`, `Malisheva`, `Llapi`, `Ferizaj`, `Trepça'89`, `Drenica Skenderaj` |
| 2023-24 | `KF Ballkani`, `Llapi`, `Drita`, `Malisheva`, `Prishtina`, `Gjilani`, `Dukagjini`, `Feronikeli`, `Fushë Kosova`, `Liria` |
| 2024-25 | `Drita`, `KF Ballkani`, `Malisheva`, `Gjilani`, `Ferizaj`, `Prishtina`, `Dukagjini`, `Llapi`, `Suhareka`, `Feronikeli` |
| 2025-26 | `Drita`, `Malisheva`, `KF Ballkani`, `Dukagjini`, `Gjilani`, `Drenica Skenderaj`, `Prishtina`, `Llapi`, `Ferizaj`, `Prishtina E Re` |

Critical 2023-24 rule: `Ferizaj` and `Suhareka` do **not** belong in that season. Their presence is an immediate failure.

Expected source mappings include:

```text
Ballkani -> KF Ballkani
Prishtina KF -> Prishtina
Drenica KF -> Drenica Skenderaj
Prishtina e Re -> Prishtina E Re
```

## 4. Sources

Primary, season by season:

```text
https://www.rsssf.org/tablesk/kosovo2022.html
https://www.rsssf.org/tablesk/kosovo2023.html
https://www.rsssf.org/tablesk/kosovo2024.html
https://www.rsssf.org/tablesk/kosovo2025.html
https://www.rsssf.org/tablesk/kosovo2026.html
```

Use an independent second source for every round and an official FFK record or other authoritative third source for conflicts. The actual match date, score, stadium, and city must be proved. No placeholder venue is permitted.

## 5. Required records

```text
MATCH|date|Kosovo Superliga|domestic-league|home|hg|ag|away|MD1..MD36|actual stadium|actual city|Kosovo||sourceId
MATCH|date|Kosovo Relegation Playoffs|other|...|Playoff ...|actual stadium|actual city|Kosovo|tieId|sourceId
```

Include SOURCE lines, one `catalog` NOTE, all rename/conflict/awarded/venue NOTES, one spot-audit round per season, and `END`.

For an awarded match, use the official standing result and explain it in a NOTE. For a penalty or extra-time playoff, use the 90-minute score and an advancement NOTE.

## 6. Gates you must report

1. Exactly 180 regular-league rows for each completed season.
2. Exactly 10 clubs and 36 league matches per club per completed season.
3. Every final table reproduces RSSSF club-by-club: W-D-L, GF-GA, points, and order.
4. Every round cross-checked against an independent source.
5. Zero duplicate fingerprints, zero bulk sentinel dates, zero placeholders, and zero clubs outside their season roster.
6. All playoff rows, if any, reproduce the official playoff bracket.

## 7. Return

Commit the one complete text return on your own session branch. Send the director the branch, commit, file path, MD5, SHA-256, counts by season and playoff, and all blockers. Do not import it.
