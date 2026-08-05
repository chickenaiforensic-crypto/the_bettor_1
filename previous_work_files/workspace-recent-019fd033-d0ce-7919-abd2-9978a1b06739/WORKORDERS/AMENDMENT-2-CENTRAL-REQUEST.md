# AMENDMENT 2 — Central Request System (binding, 2026-08-02)

To: rebuild WO `WORKORDER-PITCH-RATING-REBUILD.md`, Annex F (Data Operations) — Requests module.
**Owner decree (verbatim):** *"a central system update that takes snapshots of everything, the
teams' last game updates and the request date — so that from a central request you can cover the
entire system and also return it there."*

**Registered as D12.** The prior per-league request-file design (Annex F: "league-\<code\>-\<window\>
-\<date\>.txt") is **superseded** wherever it conflicts with this document. Per-league *detail*
survives only as **sections inside the one request** and as the Coverage view (state display is not
a request). This requirement predates Annex F; it was never written down. Now it is.

---

## D12-1 · One button: Snapshot & Request

Requests tab holds ONE primary action: **"New central request"**. On tap, the app produces:

1. **`system-snapshot-<yyyymmdd>-<hash8>.json`** — full store export (the existing backup payload:
   identities/matches/venues/seasons/sources/ctxFlags/mutes/log/artifacts/notes/meta) + snapshot
   header `{ requestDate, storeHash }`. This is the "snapshot of everything" and the rollback point.
2. **`central-request-<yyyymmdd>.txt`** — ONE file covering the ENTIRE system (see D12-2).
3. A log entry `system/request` naming both files + requestDate + hash.

## D12-2 · The one central request file — grammar

```
PITCH-RATING CENTRAL-REQUEST v1
request-date|<date>
store-hash|<hash8>
system-snapshot|system-snapshot-<yyyymmdd>-<hash8>.json
return-to|data intake (Files) — drop results here; name returns central-request-<yyyymmdd>-r<n>.txt

# SECTION per league that needs work (staleness rule D12-3); system-wide by default:
SECTION|Russian Premier League|RPL|window=<from>..<requestDate>
team|<name>|<data-current-through date>|<what's missing in words>
team|FC Krasnodar|2026-07-26|league rounds MD3..latest + any cup ties played
...
acceptance|<row reconciliation vs official table>|<20/20 split reproduction>|<dup/date rules>|<sources hierarchy>
END-SECTION
... (one SECTION per league; Annex-A new leagues appear as SECTION with "new league" scope)
END
```

Every team listed carries **its last-game date in the store** (`data-current-through`) — the
researcher sees, line by line, exactly what "everything" means and where each team's data stops.
Scope rules, alias-sheet requirement, sources hierarchy, and the acceptance checks the auditor runs
are generated per section from Annex A/B — same machinery as before, one file instead of many.

## D12-3 · What gets a section

Default = **the entire system**: every league whose newest store row is older than the request date
(stale), every REQUESTED/partial league from Annex A still incomplete, and any league the owner
flags. Nothing is omitted because a filter said so; omission needs a written reason on the section
(`excluded|<league>|<reason>`), e.g. `excluded|Kosovo Superliga|no fixtures until season start`.

## D12-4 · Central return — results come back to the same place

- Return files drop into the **same Files intake** (drag/drive folder), named
  `central-request-<yyyymmdd>-r<n>.txt`. Intake **matches them to the open central request** and
  shows fulfilment per section.
- ONE approval covers the whole return (preview shows per-section validation: reconciliation,
  20/20 splits, dup/date rules — the unchanged Annex-B checks).
- On commit: store updates, coverage closes per section, request state moves
  `drafted → sent → partial → complete`, and the Integrity module stamps a **post-return snapshot**
  (rollback pairs: before/after every return).
- Partial returns are normal: sections stay open until complete; the request stays visibly partial.

## D12-5 · What is REMOVED

Generation of separate per-league/per-team request files. The Requests tab shows: the
[New central request] button, the open central request with per-section fulfilment icons, and the
request archive. Nothing else. (Coverage tab unchanged — it displays state, it does not request.)

## R8 — Builder acceptance pins (run, show output)

1. Cold boot → Requests shows exactly one action; tapping it writes the two files + log line.
2. Request file contains every stale league as a SECTION; **each team line carries its real
   last-store-game date** (spot-check vs store for 5 teams).
3. A return file named per D12-4 lands in intake → matches the open request → one approval commits
   → coverage icons flip per section → post-return snapshot exists in Integrity.
4. Greps: zero matches for `league-<code>-<window>` filename generation; request grammar header is
   `PITCH-RATING CENTRAL-REQUEST v1`.
