# FOR THE BUILDER — migration-gate packet (2026-08-02)

Send these 4 files. All plain text — no zip, no rename tricks except two files with `.txt` added at the end.

## After receiving, rename back (bytes never change, md5 proves it):

| File as sent | Rename to | md5 (must match after rename) |
|---|---|---|
| `pitch-rating-full-data-2026-08-02.json.txt` | `pitch-rating-full-data-2026-08-02.json` | `5a8ba49475acfa2340ce7fd66e4dfeb0` |
| `gate_migrate.js.txt` | `gate_migrate.js` | see note* |
| `MIGRATION-GATE-2026-08-02.md` | (keep name) | — |
| `R11-FORWARD-TO-BUILDER.md` | (keep name) | — |

Drill: `md5sum` the renamed file → must equal the pin. If it matches, the file is byte-perfect.

## What each file is
1. **The owner's REAL live-store export** (1,432 matches / 792 teams / 86 venues / 215 sources, out of the old app). R11 acceptance pins M1/M2/M3 against THIS file — run your repros on it.
2. **My node harness** that ran the whole gate (migrate → localStorage save → boot → probes). Run: `node gate_migrate.js` — *note: it reads `audit351/app-v3.5.1-decoded.html`; point line 2 at your copy of v3.5.1. Same checks work on your build.
3. **MIGRATION-GATE-2026-08-02.md** — the auditor's full evidence document (every number proven).
4. **R11-FORWARD-TO-BUILDER.md** — the work order itself (M1 intake wiring, M2/M3 provenance keys, M3b multi-league gate, doc notes + Southampton standalone pack requirement).

*transport note: md5 of `gate_migrate.js.txt` = `73e81a1db2e8c3b62d9b091603b78e07`.
