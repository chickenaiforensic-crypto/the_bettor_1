# WORK ORDER — Major League Soccer Full Repair v1.0

**Document ID:** `WORKORDER-MLS-2021-2026-REPAIR-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Return:** `MLS-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Why this is a full repair

A prior candidate was incomplete: it omitted the 2024 MLS Cup Playoffs and used blank venue fields. Do not copy it. Build one full, source-led return with real dates, scores, venues, cities, sources, and postseason records.

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` in full before this document.

## 2. Exact scope

### Regular season

| Season | Clubs | Matches per club | Expected rows |
|---|---:|---:|---:|
| 2021 | 27 | 34 | 459 |
| 2022 | 28 | 34 | 476 |
| 2023 | 29 | 34 | 493 |
| 2024 | 29 | 34 | 493 |
| 2025 | 30 | 34 | 510 |
| **2021-25 total** | | | **2,431** |

Use:

```text
competitionName: Major League Soccer
compType: domestic-league
```

### MLS Cup Playoffs

Collect every completed playoff match for 2021, 2022, 2023, 2024, and 2025, including wild-card, best-of-three first-round series games, and single-elimination rounds. Use:

```text
competitionName: MLS Cup Playoffs
compType: other
```

For 2026, include only completed official regular-season matches and playoff matches before your actual return date. State the final included date, source, and any postponed-fixture gap in a NOTE.

Exclude Leagues Cup, US Open Cup, Canadian Championship, friendlies, CONCACAF competition, USL leagues, and youth/reserve sides.

## 3. Exact club strings

Use only these strings. A club cannot appear before its entry season.

```text
Atlanta United FC
Austin FC
CF Montréal
Charlotte FC
Chicago Fire FC
Colorado Rapids
Columbus Crew
D.C. United
FC Cincinnati
FC Dallas
Houston Dynamo FC
Inter Miami CF
LA Galaxy
Los Angeles FC
Minnesota United FC
Nashville SC
New England Revolution
New York City FC
New York Red Bulls
Orlando City SC
Philadelphia Union
Portland Timbers
Real Salt Lake
San Diego FC
San Jose Earthquakes
Seattle Sounders FC
Sporting Kansas City
St. Louis City SC
Toronto FC
Vancouver Whitecaps FC
```

Entry rules:

```text
Charlotte FC: from 2022
St. Louis City SC: from 2023
San Diego FC: from 2025
Austin FC: all completed seasons in scope
```

Map names such as `Inter Miami`, `LAFC`, `Seattle Sounders`, `DC United`, and `Montreal` to these strings once in rename NOTES. The country field must be the real home-club country: Canada for CF Montréal, Toronto FC, and Vancouver Whitecaps FC; United States for the others.

## 4. Sources

Primary season pages:

```text
https://www.rsssf.org/tablesu/usa2021.html
https://www.rsssf.org/tablesu/usa2022.html
https://www.rsssf.org/tablesu/usa2023.html
https://www.rsssf.org/tablesu/usa2024.html
https://www.rsssf.org/tablesu/usa2025.html
https://www.rsssf.org/tablesu/usa2026.html
```

Cross-check regular season and playoff rounds against the official MLS result archive or another independent fixture index. Use the official match record or official club source to verify any venue/city field missing from RSSSF.

## 5. Required grammar and doctrine

```text
MATCH|date|Major League Soccer|domestic-league|...|round|actual stadium|actual city|home-country||sourceId
MATCH|date|MLS Cup Playoffs|other|...|round/series game|actual stadium|actual city|home-country|tieId|sourceId
```

- Each 2023+ best-of-three series gets one shared tieId and an advancement NOTE naming the series winner.
- A single playoff match decided by penalties or extra time uses the 90-minute score plus an advancement NOTE.
- Record a neutral or relocated match at its actual venue with a NOTE.
- No blank stadium, city, country, or source fields.

## 6. Gates you must report

1. Exact 2021-25 regular-season counts: 459, 476, 493, 493, 510.
2. Every club has 34 regular-season matches in its membership year.
3. Both final conference tables reproduce from rows for every completed season.
4. Every playoff bracket reproduces the official finalists and MLS Cup champion, including the previously missing 2024 playoffs.
5. Every row has a real venue/city and declared source.
6. Zero duplicate fingerprints, no club before its entry year, and no wrong competition/type.
7. One full source-linked regular round and one playoff spot check per completed season.

## 7. Return

Commit one complete pack on your own session branch. Send the director the branch, commit, path, MD5, SHA-256, counts by season and playoff phase, exact 2026 cutoff, and every blocker. Do not import it.
