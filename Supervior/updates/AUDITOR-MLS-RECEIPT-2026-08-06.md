# Auditor Receipt — MLS Return (2026-08-06)

**Pack:** `handoffs/MLS-2021-2026_BP-TEAM-PACK_v2.txt`  
**Decision:** **RETURN_INCOMPLETE — do not import or approve.**  
**Fresh evidence:** `audit_work/audit_mls_return_20260806.py` and `audit_work/MLS-2021-2026-receipt-audit-2026-08-06.json`.

## Receipt findings

| Gate | Result |
|---|---|
| Parseable match rows | **FAIL:** all 1,994 `MATCH` rows have 13 fields, but BP-TEAM-PACK v2 requires 14 including `tieId` and `sourceId`. |
| Match provenance | **FAIL:** no row has a `sourceId`; its final token (`rsssf-mls`, 1,994 times) is parsed into `tieId` and matches none of the declared `SOURCE` ids (`rsssf-mls-2021` through `rsssf-mls-2025`). |
| Duplicate fingerprints | PASS: 0 within the return. |
| Canonical club strings / score/date structural checks | PASS on structurally readable rows. |
| 2021–24 regular-season delivery | Shape PASS after appendix exclusion: 459 / 476 / 493 / 482 rows. The 2024 expectation is 482 because 11 appendix rows are explicitly held. |
| 2025 regular season | **FAIL:** 0 / 510 required rows. The return itself declares a blocker. |
| 2026 to-date regular season | **FAIL:** 0 rows. The return itself declares a blocker. |
| Full five-year continuity / table and bracket reproduction | **Not runnable / not approvable** while grammar, provenance and scope gates fail. |

## Required correction

1. Reissue every match in complete v2 shape, retaining an empty `tieId` delimiter where needed and supplying a valid declared `sourceId` (for example: `...|country||rsssf-mls-2021`). Do not silently re-purpose the final field as a tie ID.
2. Supply independently verifiable 2025 regular-season rows (510 expected) and 2026-to-date rows, or keep the workorder open. A `NOTE|warning|blocker` documents absence but does not satisfy the coverage gate.
3. Return after the above are complete; then the auditor can run table, bracket, held-appendix and full-span reconciliation gates.

No data was imported and no partial approval is granted.
