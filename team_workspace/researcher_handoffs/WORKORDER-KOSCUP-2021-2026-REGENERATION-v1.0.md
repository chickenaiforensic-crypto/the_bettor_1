# WORK ORDER — Kosovo Cup Regeneration v1.0

**Document ID:** `WORKORDER-KOSCUP-2021-2026-REGENERATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND
**Supersedes for dispatch:** the old Kosovo Cup assignment and every prior Kosovo Cup candidate.
**Return:** `KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Why this is a regeneration

Do not reuse the previous candidate or its type labels. This task must produce a fresh, source-led cup slice with the correct `domestic-cup` type.

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` in full before this document.

## 2. Exact scope

For each completed edition 2021-22 through 2025-26, collect every Kosovo Cup tie from the first round in which that season’s Superliga clubs enter through the final **when at least one participant is a Superliga club from that season**.

- Include both legs where an edition uses two legs.
- Include replays as separate, dated rows when officially played.
- Exclude all-lower-division ties that never involve a Superliga club.
- Include 2026-27 only through your real return-date cutoff, if it has begun.
- Do not use a guessed row target. Derive and declare phase counts from the official bracket for each edition.

Every row must use:

```text
competitionName: Kosovo Cup
compType: domestic-cup
country: Kosovo
```

## 3. Superliga membership rule

The Superliga team and season roster is the authority in:

`WORKORDER-KOS-2021-2026-REGENERATION-v1.0.md`, section 3.

A cup tie belongs in this return only if at least one side is on that edition’s exact Superliga roster. Verify that rule before writing any MATCH row.

Lower-division opponents need a source-backed TEAM record only if they do not already exist in the application roster. Never create a TEAM record without a source.

## 4. Sources

Primary cup chapters:

```text
https://www.rsssf.org/tablesk/kosovo2022.html#kupa
https://www.rsssf.org/tablesk/kosovo2023.html#kupa
https://www.rsssf.org/tablesk/kosovo2024.html#kupa
https://www.rsssf.org/tablesk/kosovo2025.html#kupa
https://www.rsssf.org/tablesk/kosovo2026.html#kupa
```

Use the Kosovo federation or official competition record and one independent full-result index to cross-check every included tie. If RSSSF lacks a field, record `source_adaptation` and use the official match record; never fill the gap from memory.

## 5. Required grammar and evidence

```text
MATCH|date|Kosovo Cup|domestic-cup|home|hg|ag|away|round/leg|actual stadium|actual city|Kosovo|tieId|sourceId
```

- Give both legs of a two-leg tie the same tieId.
- For extra time or penalties, store the 90-minute score and add an `advancement` NOTE.
- For a neutral final or relocation, use the actual venue and add a `neutral_venue` NOTE.
- Declare every source, every identity mapping, every source conflict, and one spot-audit round per edition.
- End with `END`.

## 6. Gates you must report

1. Every included tie passes the active-Superliga-club rule.
2. Every edition’s phase counts and bracket reproduce the official source.
3. Semifinalists, finalists, champion, and all advancement outcomes are exact.
4. Every row has a real played date, real venue, real city, and declared source.
5. Zero duplicate fingerprints; zero placeholder values; zero wrong compTypes.
6. Cross-check every included tie against an independent source.

## 7. Return

Commit one complete pack on your own session branch. Send the director the branch, commit, file path, MD5, SHA-256, round-by-round counts, and every blocker. Do not import it.
