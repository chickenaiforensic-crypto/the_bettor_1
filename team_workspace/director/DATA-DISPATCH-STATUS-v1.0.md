# DATA DISPATCH STATUS v1.0

**Issued:** 2026-08-07
**Purpose:** Exact researcher dispatch state after branch and handoff audit.
**Rule:** “Candidate” means it exists but is not approved until the project auditor verifies it with fresh code.

## Do not send a researcher

| Scope | Status | Evidence | Required next step |
|---|---|---|---|
| England Premier League | adopted in the 5,082-row verified store | `previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` | none |
| Russia: RPL, Cup, addendum | adopted in the 5,082-row verified store | same store | none |
| Czechia: First League, MOL Cup | adopted in the 5,082-row verified store | same store | none |
| Spain La Liga | new 1,900-row return exists | `origin/arena/019fd805-the-bettor-1:handoffs/SPA-2021-2026_BP-TEAM-PACK_v2.txt` | auditor verification already requested |
| Italy Serie A | candidate 1,901-row return exists | `origin/arena/019fc462-the-bettor-1:handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` | auditor verification; do not duplicate research |
| Germany Bundesliga | candidate 1,540-row return exists | `origin/arena/019fc462-the-bettor-1:handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt` | auditor verification; do not duplicate research |
| France Ligue 1 | candidate 1,686-row return exists | `origin/arena/019fc462-the-bettor-1:handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt` | auditor verification; do not duplicate research |

## Send a researcher

| Priority | Scope | Required workorder |
|---:|---|---|
| 1 | Kosovo Superliga | `WORKORDER-KOS-2021-2026-REGENERATION-v1.0.md` |
| 2 | Kosovo Cup | `WORKORDER-KOSCUP-2021-2026-REGENERATION-v1.0.md` |
| 3 | Scottish Premiership | `WORKORDER-SCO1-2021-2026-REPAIR-v1.0.md` |
| 4 | Scottish Cup | `WORKORDER-SCOCUP-2021-2026-REGENERATION-v1.0.md` |
| 5 | Scottish League Cup | `WORKORDER-SCOLC-2021-2026-REGENERATION-v1.0.md` |
| 6 | US Open Cup | `WORKORDER-USOC-2021-2026-REGENERATION-v1.0.md` |
| 7 | MLS | `WORKORDER-MLS-2021-2026-REPAIR-v1.0.md` |
| 8 | UEFA connector | `WORKORDER-UEFA-CONNECTOR-2021-2026-REGENERATION-v1.0.md` |

## Why these eight are re-issued

- Kosovo league: prior candidate was fabricated-grade: wrong 2023-24 clubs, false scores, and sentinel dates.
- Kosovo Cup: prior candidate needs full fresh verification and correct cup typing.
- Scottish Premiership: existing scores need a full venue/provenance repair; placeholder venues are not acceptable.
- Scottish Cup and League Cup: existing candidates were partial and used the wrong competition type.
- US Open Cup: existing candidate covered only three seasons and contained undeclared source IDs.
- MLS: existing candidate omitted the 2024 playoffs and had blank venues.
- UEFA connector: existing candidate retained sentinel dates and false 2025-26 knockout results; it must not be reused.

## Auditor queue

1. SPA return from `arena/019fd805-the-bettor-1`.
2. ITA candidate return from `arena/019fc462-the-bettor-1`.
3. GER candidate return from `arena/019fc462-the-bettor-1`.
4. FRA candidate return from `arena/019fc462-the-bettor-1`.

The external branch’s report is evidence, not approval. The project auditor must use fresh parsers and write an approval or rejection card for each pack.
