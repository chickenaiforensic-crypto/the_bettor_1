# RESEARCHER WORKORDER MASTER — Data Collection v1.1

**Document ID:** `WORKORDER-RESEARCHER-MASTER-v1.1`
**Issued:** 2026-08-07
**Supersedes:** `WORKORDER-RESEARCHER-MASTER-v1` for every new or re-issued data task.
**Applies to:** Every researcher return.

## 1. Purpose

You collect completed football matches. You do **not** decide that a pack is true. The auditor decides that only after running fresh checks.

If you cannot prove a row, do not create it. Write:

```text
NOTE|warning|blocker|<what could not be verified and why>
```

## 2. Mandatory cold start

Before opening a source, read these files fully, in this order:

1. `COMMUNICATION-RULES-v1.md`
2. `START-HERE-COLD-START.md`
3. `README.md`
4. `Supervior/ROLES/ROLE-RESEARCHER.md`
5. This master workorder
6. Your specific workorder

Then reply with exactly these three facts before collecting rows:

```text
1. Competition and seasons I own: ...
2. Expected shape: ...
3. Primary source and independent second source: ...
```

## 3. Never do these things

- Never invent a club, score, date, stadium, city, source, or round.
- Never use odds, prices, bookmaker material, market rankings, or market-derived data.
- Never copy rows from an old candidate pack as evidence.
- Never use a default date such as a season-end date for many matches.
- Never use placeholder venue values such as `unknown`, `Stadium`, `City`, or `Europe`.
- Never add a club outside the season-specific roster.
- Never submit a zip, fragments, a table instead of rows, or a file without `END`.
- Never import data yourself.

A source conflict is not permission to guess. Record both values and the adjudication:

```text
NOTE|warning|source_conflict|<match>: primary says ...; second source says ...; resolved to ... because ...
```

## 4. BP-TEAM-PACK v2 grammar

Use the current application grammar exactly:

```text
MATCH|dateISO|competitionName|compType|home|homeGoals|awayGoals|away|venue|stadium|city|country|tieId|sourceId
SOURCE|sourceId|url|accessDate|kind|what-it-verified
NOTE|info-or-warning|tag|text
TEAM|name|country|leagueName|leagueCode|aliases|stadium|city|country2|surface|capacity|founded|website
END
```

A `MATCH` record needs a valid `sourceId` that appears in a `SOURCE` record. Do not leave its source blank.

Allowed competition types are:

```text
domestic-league
domestic-cup
league-cup
super-cup
uefa-cl
uefa-el
uefa-uecl
club-friendly
other
```

Use the exact type specified by your task. A cup is not a league. A separate promotion/relegation or championship playoff is normally `other` unless the workorder says differently.

Use a `TEAM` line only when the specific workorder permits it and the club is proven by a cited source. Do not create a TEAM record to make an unverified match look valid.

## 5. Sources and adaptations

Each workorder names its primary and independent second source.

1. Transcribe the primary source directly.
2. Cross-check every match or every stated round/phase against the independent source.
3. Use a third authoritative source only to adjudicate a conflict.
4. If the primary source has no fixture-level record for a required season or field, use the official competition/federation result record as the match carrier and write one `NOTE|info|source_adaptation` explaining the gap and replacement.
5. Record the real access date. Never copy a date from an example.

A source line must say exactly what it proves. “Everything” is not enough.

## 6. Mandatory self-gates before return

Your return is incomplete unless all applicable gates pass.

### G1 — Grammar

- Header is `BP-TEAM-PACK v2`.
- Every row has the required field count and legal compType.
- File ends with `END`.

### G2 — Boundary and date reality

- No duplicate fingerprint: date + competition + home + away.
- No future match after your return date.
- ISO dates are real played dates, not scheduled dates where a fixture was postponed.
- No suspicious bulk sentinel date. If many records share one date, prove that they were genuinely played that day or stop.
- Goals are integer 0–30.

### G3 — Identity and membership

- Every team string matches the workorder roster exactly.
- Every club belongs to that competition in that season.
- Every approved rename mapping appears once in a NOTE.
- No split identities such as two names for the same club.

### G4 — Provenance and venue

- Every MATCH has a declared source.
- Every stadium and city are the actual venue and actual city.
- Neutral or relocated matches carry `NOTE|info|neutral_venue` or `NOTE|info|venue_note`.
- A missing venue is a blocker, not a placeholder.

### G5 — Whole-competition reproduction

- League: reproduce every final table from your rows: club order, W-D-L, GF-GA, points, and membership.
- Cup: reproduce the bracket, semifinalists, finalists, champion, and every advancement path.
- Two-leg tie: both legs share one tieId.
- Extra-time or penalty tie: record the 90-minute score plus an advancement NOTE.

### G6 — Shape and continuity

- Per-season match counts equal the task’s stated format.
- Each club has the correct number of matches for its season.
- Every official in-scope match is present.
- Any real format change, replay, awarded result, abandoned match, or cancelled competition is documented in a NOTE.

### G7 — Independent cross-check

- Record a full cross-check, not a sample-only claim.
- Include one documented spot-audit matchday/round per season.
- Report every difference and its source-based resolution.

## 7. Return contents

Put one complete text file in `handoffs/` with the exact filename in the specific workorder. Also provide:

```text
- branch name and commit hash
- file path
- MD5 and SHA-256
- total rows and per-season/phase counts
- self-gate result
- every blocker or source conflict
```

Your self-check is evidence only. It is not approval. The auditor writes fresh verification code and decides whether the pack can be adopted.

## 8. Final acknowledgement

Before returning a pack, state:

```text
I read the master and my specific workorder in full.
I used no market data and created no unverified row.
I completed every stated gate or listed the blocker.
I understand that the auditor, not me, decides approval.
```
