# DECREE-2026-08-04 — owner full-span override (registered verbatim, governs over all workorders)

**Issued:** 2026-08-04 by the owner, live session.
**Verbatim:** "well l said that l require you to deliver full season files regardless of what
the workorder said so for russia and any other league ensure my authority overrides
everything - so go back to the russian leagues and complete the extra years l want one
source of truth because our old data contains errors that will be audited against your
full data"

## Operative effect (registered by the lead researcher)

1. **Owner authority overrides every workorder clause.** The 2021–2024 segment cutoffs
   (`nothing dated 2024-06-30 or later`) in WO-RPL-BACKFILL-01, WO-CZ1-BACKFILL-02,
   WO-RUSCUP-BACKFILL-03, WO-MOLCUP-BACKFILL-04 are **rescinded**.
2. **Full span 2021 → today for every league and cup** in the programme. Russia first
   ("go back to the russian leagues"): RPL and RUSCUP extend through 2024-25 and 2025-26
   (complete seasons). The already-returned CZ1/MOLCUP packs extend the same way. The
   remaining queue (FRA…USOC) was already commissioned full-span and proceeds unchanged.
3. **One source of truth:** the researcher-built packs are the authoritative data the
   owner's legacy store (which is known to contain errors) will be audited AGAINST.
   The legacy in-repo CSVs (`data/rpl/*`) are left untouched — they are the
   to-be-audited old data, not the truth.
4. **Scope rule unchanged, years extended:** for the cups, the auditor-proven slice
   (every official match with ≥1 top-flight participant) stays the scope definition —
   the override extends the years, not the membership rule. For RPL the relegation
   playoffs remain commissioned where the season used them (compType `other` per
   ERRATA-2026-08-03; cups `domestic-cup`).
5. **2026-27 (season in progress at the return date)** is not a full season: covered by
   a boundary NOTE stating the documented start and the status as of the return date
   (it fills via the owner's central-request system), exactly as done for EPL.
6. Verification doctrine unchanged: RSSSF primary, ≥1 independent index, conflicts
   resolved to RSSSF unless two independent indexes agree against it (then theirs +
   `NOTE|warning|source_conflict`), no fabrication, per-club pivot ledgers, builders
   byte-deterministic.
