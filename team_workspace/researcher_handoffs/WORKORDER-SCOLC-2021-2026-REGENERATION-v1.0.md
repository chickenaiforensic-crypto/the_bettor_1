# WORK ORDER — Scottish League Cup Regeneration v1.0

**Document ID:** `WORKORDER-SCOLC-2021-2026-REGENERATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Supersedes for dispatch:** the partial Scottish League Cup candidate.
**Return:** `SCOLC-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Scope

For editions 2021-22 through 2025-26, collect every Scottish League Cup match involving at least one Premiership club from that edition.

This includes:

- group-stage matches played by Premiership clubs;
- knockout matches after group stage;
- clubs receiving a European-entry bye: record the bye in a NOTE, never as a match;
- every completed in-scope 2026-27 match at your return date, if any.

Exclude fixtures in which both teams are outside that edition’s Premiership membership. Do not reuse the old partial candidate.

Every row must use:

```text
competitionName: Scottish League Cup
compType: league-cup
country: Scotland
```

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` and `WORKORDER-SCO1-2021-2026-REPAIR-v1.0.md` before starting. The league workorder’s season roster controls membership.

## 2. Source requirements

Primary RSSSF pages:

```text
https://www.rsssf.org/tabless/scot2022.html
https://www.rsssf.org/tabless/scot2023.html
https://www.rsssf.org/tabless/scot2024.html
https://www.rsssf.org/tabless/scot2025.html
https://www.rsssf.org/tabless/scot2026.html
```

Cross-check every group and knockout match using the official SPFL/League Cup record or another independent results index. Capture actual venue and city. Placeholder venue values fail the task.

## 3. Grammar and cup doctrine

```text
MATCH|date|Scottish League Cup|league-cup|home|hg|ag|away|group/round/leg|actual stadium|actual city|Scotland|tieId|sourceId
```

- A group-stage penalty shootout may affect the group point award, but the MATCH row remains the 90-minute result. Explain the shootout outcome in a NOTE.
- Knockout AET/penalty decisions: 90-minute score plus advancement NOTE.
- Two legs, if any: shared tieId.
- Neutral venue: actual venue plus neutral-venue NOTE.
- Lower-division identity: source-backed TEAM record only when required.

## 4. Gates

1. Every row involves an eligible Premiership club for that edition.
2. Group participation, qualifiers, bracket, finalists, and champion reproduce the official record.
3. All group-stage matches involving an eligible club are present; no entry-round gap is allowed.
4. Every row has a source, real date, actual venue, actual city, and correct `league-cup` type.
5. Zero duplicate fingerprints, placeholders, and unverified TEAM records.
6. One full source-linked spot-audit group/round per edition.

## 5. Return

Commit one complete pack on your own session branch. Send the director the branch, commit, path, MD5, SHA-256, edition/phase counts, and every blocker. Do not import it.
