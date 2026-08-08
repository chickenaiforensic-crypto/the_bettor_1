# WORK ORDER — Scottish Cup Regeneration v1.0

**Document ID:** `WORKORDER-SCOCUP-2021-2026-REGENERATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Supersedes for dispatch:** the partial Scottish Cup candidate.
**Return:** `SCOCUP-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Scope

For each edition 2021-22 through 2025-26, collect every Scottish Cup tie from the round Premiership clubs enter through the final when at least one participant is a Premiership club in that season.

- Include replays as separate dated rows if officially played.
- Include both legs if the official edition used them.
- Exclude ties between two clubs that are both outside the Premiership membership for that edition.
- Include 2026-27 only if an in-scope match was completed by your return date.
- Do not reuse the prior partial candidate.

Every row must use:

```text
competitionName: Scottish Cup
compType: domestic-cup
country: Scotland
```

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` and `WORKORDER-SCO1-2021-2026-REPAIR-v1.0.md` before starting. The Scottish Premiership membership table in the league workorder controls the in-scope rule.

## 2. Sources

Primary:

```text
https://www.rsssf.org/tabless/scot2022.html
https://www.rsssf.org/tabless/scot2023.html
https://www.rsssf.org/tabless/scot2024.html
https://www.rsssf.org/tabless/scot2025.html
https://www.rsssf.org/tabless/scot2026.html
```

Use the Scottish FA official archive or official match record and one independent result index to cross-check every included tie. Every venue and city must be real and sourced.

## 3. Grammar and evidence

```text
MATCH|date|Scottish Cup|domestic-cup|home|hg|ag|away|round/leg|actual stadium|actual city|Scotland|tieId|sourceId
```

- Two-leg ties share one tieId.
- Extra time or penalties: store the 90-minute score and add an advancement NOTE.
- Neutral or relocated fixture: actual venue plus `neutral_venue` NOTE.
- Lower-division opponent: add a TEAM record only if it does not already exist and you have a source-backed identity record.
- Add one spot-audit round per edition, SOURCE lines for every source, and `END`.

## 4. Gates

1. The active-Premiership-club rule is true for every row.
2. Round counts and full bracket reproduce the official edition.
3. Semifinalists, finalists, champion, and all advancement outcomes are exact.
4. No missing replays, duplicate fingerprints, placeholders, invented clubs, or wrong compType.
5. Every row is cross-checked independently.

## 5. Return

Commit the complete pack on your own session branch. Send the director the branch, commit, path, MD5, SHA-256, edition/round counts, and all blockers. Do not import it.
