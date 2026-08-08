# WORK ORDER — US Open Cup Regeneration v1.0

**Document ID:** `WORKORDER-USOC-2021-2026-REGENERATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Supersedes for dispatch:** the incomplete three-season US Open Cup candidate.
**Return:** `USOC-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Exact scope

This is the Lamar Hunt US Open Cup. It is not MLS league play, Canadian Championship, Leagues Cup, or USL league play.

For each edition, collect every tie in which at least one participant is an MLS first team from that season:

| Edition | Required handling |
|---|---|
| 2021 | Competition cancelled. Return zero MATCH rows and one `NOTE|info|cancelled` with an official source. |
| 2022 | All in-scope MLS-club ties from entry round through final. |
| 2023 | All in-scope MLS-club ties from entry round through final. |
| 2024 | All in-scope MLS first-team ties; record the official MLS participation exception/format in a NOTE. |
| 2025 | All in-scope MLS-club ties from entry round through final. |
| 2026 | Only completed, source-confirmed in-scope ties through your actual return date. |

Use:

```text
competitionName: US Open Cup
compType: domestic-cup
```

Do not reuse the old 45-row candidate. It lacked seasons and declared source IDs.

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` and `WORKORDER-MLS-2021-2026-REPAIR-v1.0.md` in full before starting. The MLS workorder controls MLS identity strings and year-specific membership.

## 2. Sources

Primary:

```text
https://www.rsssf.org/tablesu/usa2022.html
https://www.rsssf.org/tablesu/usa2023.html
https://www.rsssf.org/tablesu/usa2024.html
https://www.rsssf.org/tablesu/usa2025.html
https://www.rsssf.org/tablesu/usa2026.html
```

Use the official U.S. Soccer competition archive as the official result/bracket authority and an independent result index for every included tie. A source ID must be declared before a row uses it.

## 3. Grammar and identities

```text
MATCH|date|US Open Cup|domestic-cup|home|hg|ag|away|round|actual stadium|actual city|United States|tieId|sourceId
```

- Extra time or penalty decision: 90-minute score plus advancement NOTE.
- Neutral or relocated match: actual venue and neutral-venue NOTE.
- Non-MLS opponent: add a TEAM record only if it is not in the existing application roster and you have source-backed identity/venue evidence.
- Do not make a lower-division TEAM record from a guessed or template name.

## 4. Gates

1. Mandatory 2021-cancelled NOTE; no invented 2021 matches.
2. Every non-cancelled edition contains every tie involving an active MLS first team.
3. Round counts, semifinalists, finalists, champion, and all advancement decisions reproduce the official bracket.
4. Every source ID resolves to a SOURCE line.
5. Every row has actual date, stadium, city, and correct `domestic-cup` type.
6. Zero duplicate fingerprints, placeholders, missing seasons, or source-ID failures.
7. One full source-linked round spot audit per active edition.

## 5. Return

Commit one complete text pack on your own session branch. Send the director the branch, commit, path, MD5, SHA-256, edition/round counts, exact 2026 cutoff, and every blocker. Do not import it.
