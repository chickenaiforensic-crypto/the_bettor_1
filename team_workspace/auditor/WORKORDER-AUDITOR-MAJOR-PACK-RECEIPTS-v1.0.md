# WORK ORDER — Auditor: Major Pack Receipts v1.0

**Document ID:** `WORKORDER-AUDITOR-MAJOR-PACK-RECEIPTS-v1.0`
**Issued:** 2026-08-07
**Status:** READY — verification only, no import
**Rule:** Every result below is a candidate until you independently prove it with fresh code.

## 1. Audit sequence

| Order | Scope | Remote branch and path | Claimed rows | Current status |
|---:|---|---|---:|---|
| 1 | Spain La Liga | `origin/arena/019fd805-the-bettor-1:handoffs/SPA-2021-2026_BP-TEAM-PACK_v2.txt` | 1,900 | researcher return received; prep kit already delivered |
| 2 | Italy Serie A | `origin/arena/019fc462-the-bettor-1:handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` | 1,901 | candidate only |
| 3 | Germany Bundesliga | `origin/arena/019fc462-the-bettor-1:handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt` | 1,540 | candidate only |
| 4 | France Ligue 1 | `origin/arena/019fc462-the-bettor-1:handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt` | 1,686 | candidate only |

Fetch the branches and calculate the hash yourself. Do not trust an existing report, a researcher’s ledger, or this workorder’s claimed count as evidence.

## 2. Fresh-audit requirement

Read in full before running a check:

1. `COMMUNICATION-RULES-v1.md`
2. `START-HERE-COLD-START.md`
3. `Supervior/ROLES/ROLE-AUDITOR.md`
4. `team_workspace/auditor/WORKORDER-AUDITOR-MASTER-v1.md`
5. This workorder

Write fresh parser and validator code in `audit_work/`. Existing researcher and prior-auditor code may be used only as a comparison after your own result exists.

## 3. Universal gates

For each pack, independently prove:

- hash, grammar, legal compType, source linkage, and final `END`;
- no duplicate fingerprints, future dates, sentinel bulk dates, bad scores, blank source IDs, or placeholder venues;
- season membership and exact roster mapping;
- complete date/score/sides cross-diff against primary and independent sources;
- real stadium/city/country on every row;
- table reproduction for every league season; and
- full phase/bracket reproduction for every included playoff.

Write a separate approval or rejection card. A pass on one pack never approves another.

## 4. Scope-specific checks

### Spain

- Exactly 380 league rows for each 2021-22 through 2025-26 season.
- 20 clubs and 38 matches per club each season.
- Full table reproduction including La Liga tie-break order.
- Audit the 2025-26 source adaptation because RSSSF `span2026` was unavailable at preparation time.
- Review the documented Granada–Athletic abandonment/completion and every source conflict.

### Italy

- 1,900 Serie A rows: 380 × five seasons.
- One separate `Italy Relegation Playoffs|other` row is claimed for Spezia–Verona, 2023-06-11. Verify its scope, type, date, 90-minute score, and venue independently.
- Do not approve it merely because it is a genuine match; it must be inside the approved scope.

### Germany

- 1,530 Bundesliga rows: 306 × five seasons.
- Ten separate `Germany Relegation Playoffs|other` rows are claimed. Verify each separately and decide whether owner scope permits them.
- Verify all 18-club/34-matchday tables and awarded-result treatment.

### France

- 1,678 Ligue 1 rows: 380 + 380 + 306 + 306 + 306.
- Eight `France Relegation Playoffs|other` rows are claimed. Verify scope, 90-minute rule, and source provenance separately.
- Verify the 20-to-18-club format change and every table.

## 5. Deliverables

For each pack, create:

```text
Supervior/Build Docs/AUDIT-<SCOPE>-RECEIPT-2026-08-07-v1.0.md
Supervior/updates/SESSION-2026-08-07-<SCOPE>-AUDIT-v1.0.md
audit_work/<scope>_receipt_audit_2026-08-07-v1.0/
```

Each report must state one unambiguous verdict:

```text
APPROVED
REJECTED
BLOCKED — source gap
```

No data import, migration, or engine change is part of this workorder.
