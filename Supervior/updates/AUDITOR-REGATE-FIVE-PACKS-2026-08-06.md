# Auditor Re-gate — Five Grammar-Fixed Packs (2026-08-06)

**Scope:** independent receipt re-gate of exact v2 field count, calendar dates, non-negative integer scores, within-pack match fingerprints, declared `SOURCE` linkage, and stated coverage blockers. This is not a substitute for the later full table/bracket reconstruction gate.

**Evidence:** `audit_work/regate_five_packs_20260806.py` → `audit_work/regate-five-packs-2026-08-06.json`.

| Pack | Rows | Grammar/date/duplicate | Source linkage | Receipt decision |
|---|---:|---|---|---|
| MLS | 1,994 | PASS — all 14 fields, valid dates, 0 duplicates | PASS — all row source IDs declared | **Grammar re-gate PASS; workorder remains open** |
| USOC | 45 | PASS — all 14 fields, valid dates, 0 duplicates | **FAIL** — 45 rows reference `rsssf-mls-2022/2023/2025`, none declared by the pack | **RETURN FOR SOURCE-ID FIX** |
| SCOCUP | 68 | PASS — all 14 fields, valid dates, 0 duplicates | PASS | **Grammar re-gate PASS; partial coverage only** |
| SCOLC | 72 | PASS — all 14 fields, valid dates, 0 duplicates | PASS | **Grammar re-gate PASS; partial coverage only** |
| KOSCUP | 120 | PASS — all 14 fields, valid dates, 0 duplicates | PASS | **Receipt re-gate PASS** |

## Required adjudications

### MLS — grammar correction accepted, full-span approval withheld

The prior 13-field/source-position defect is fixed: every match is now 14 fields and every source ID is declared. However, its own warning notes state that the 2025 MLS regular season (0/510 rows) and 2026-to-date regular season (0 rows) are absent. The original full-span workorder cannot be approved or imported as complete until those rows are returned and later table/appendix gates run.

### USOC — source integrity fail

The one declared source ID does not match any match-row source ID. Reissue the rows with a declared season-specific ID, or add matching `SOURCE` rows. Do not import before this is corrected. Its R32 and 2026 coverage blockers also keep full-scope approval open.

### SCOCUP and SCOLC — grammar correction accepted, full-span approval withheld

Both packs pass this receipt grammar/provenance audit. Their explicit warnings say that pre-R16 / entry-round coverage is not returned, so their `2021–2026` workorders remain incomplete. They must not be represented as full cup histories.

### KOSCUP — receipt re-gate pass

KOSCUP passes all tested receipt gates and has no blocker note. It may proceed to the next full content gate (season/bracket/champion reconstruction); this report does not itself certify that later gate.
