# WORK ORDER — UEFA Connector Regeneration v1.0

**Document ID:** `WORKORDER-UEFA-CONNECTOR-2021-2026-REGENERATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY TO SEND — HIGH-RISK REBUILD
**Supersedes for dispatch:** every prior UEFA-FULL and UEFA-CONNECTOR candidate.
**Return:** `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt`

## 1. Why this is a clean rebuild

The previous UEFA candidates are rejected. They used bulk season-end dates, placeholder venues, split/ghost identities, missing phases, and false knockout scorelines. Do not copy, patch, parse, or cite those candidate rows as evidence.

Read `WORKORDER-RESEARCHER-MASTER-v1.1.md` in full before this document.

## 2. Exact scope

Collect every completed UEFA match involving at least one club from a programme league:

```text
England Premier League
Russian Premier League
Czech First League
Spain La Liga
Italy Serie A
Germany Bundesliga
France Ligue 1
```

Competitions and types:

| Competition | compType |
|---|---|
| UEFA Champions League, including qualifying | `uefa-cl` |
| UEFA Europa League, including qualifying | `uefa-el` |
| UEFA Conference League, including qualifying | `uefa-uecl` |

Coverage:

```text
2021-22
2022-23
2023-24
2024-25
2025-26
2026-27 only through your actual return date
```

Include both legs when a tie is in scope. Include all group-stage or league-phase matches played by an in-scope club. Exclude UEFA Super Cup, Youth League, women’s competition, friendlies, and domestic matches.

The expected count is not a licence to pad. Derive and report exact counts by season, competition, phase, and programme league.

## 3. Source order

For every MATCH, use the official UEFA competition match record as the primary date/score/venue authority.

Then cross-check the fixture against:

1. an independent full-results source such as worldfootball’s relevant competition season page; and
2. RSSSF country/European records or an official national federation record where available.

For every source, record URL, real access date, and exact coverage. If sources conflict, preserve the conflict in a NOTE and use the official UEFA record only when it actually contains the relevant fact.

## 4. Non-negotiable structure

Before emitting match rows, create a per-season structure ledger showing:

```text
competition -> phase -> in-scope programme club -> official opponent(s) -> required match count
```

Use the ledger to prove no group/league-phase round, qualifying leg, knockout leg, or final is missing.

### Date rule

A season end date is never a match date unless the official match was actually played on that date. Run a sentinel-date lint before return. A cluster of `YYYY-06-30` or another default date is a failure unless each row is independently proved.

### Score rule

For extra time or penalties, the MATCH row is the score at 90 minutes. Add:

```text
NOTE|info|advancement|<tie and winner, including ET/pens outcome>
```

Do not convert a shootout score into a football scoreline.

### Tie rule

Both legs of the same tie share one stable tieId, for example:

```text
UCL-2024-25-R16-CLUB1-CLUB2
```

Group/league-phase matches and a final may have empty tieId.

## 5. Identity and venue rule

- Use one identity for every club across all seasons and competitions.
- Programme-league club names must match their auditor-approved domestic pack strings when the auditor provides them. Until then, keep a source-backed mapping ledger; do not silently create variants.
- Foreign opponent requires one source-backed TEAM record if it does not exist already.
- `country` is the actual home side’s country, not `Europe`.
- Stadium and city are the actual venue and city. Neutral or relocated matches require `neutral_venue` NOTE.
- Placeholder `Stadium`, `City`, `unknown`, and `Europe` values fail the task.

## 6. Required grammar

```text
MATCH|date|UEFA Champions League|uefa-cl|home|hg|ag|away|phase/leg|actual stadium|actual city|home-country|tieId|sourceId
MATCH|date|UEFA Europa League|uefa-el|home|hg|ag|away|phase/leg|actual stadium|actual city|home-country|tieId|sourceId
MATCH|date|UEFA Conference League|uefa-uecl|home|hg|ag|away|phase/leg|actual stadium|actual city|home-country|tieId|sourceId
```

Also return `UEFA-CONNECTOR-EVIDENCE-v1.0.md` containing the structure ledger, counts, all source adaptations, every conflict, and one complete matchweek spot audit per competition and season.

## 7. Gates you must report

1. Participation ledger complete for every programme-league club.
2. Phase/format counts exact for each competition and season.
3. Every two-leg tie has two rows and one shared tieId.
4. Every AET/penalty case carries 90-minute score plus advancement NOTE.
5. Every row has exact played date, actual stadium/city/country, and declared source.
6. Zero sentinel date clusters, placeholders, duplicate fingerprints, ghost TEAM rows, or name variants.
7. Every MATCH independently cross-checked.
8. Exact 2026-27 cutoff declared; no future rows.

## 8. Return

Commit the pack and the versioned evidence ledger on your own session branch. Send the director the branch, commit, both paths, MD5 and SHA-256 for the pack, counts by season/competition/phase, and every blocker. Do not import it.
