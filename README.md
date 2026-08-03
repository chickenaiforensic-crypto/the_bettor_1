# the_bettor_1

**Audited football match dataset — Russian football first: the 5-year-span audit programme (2021-07 → today).**
Every return is a **verbatim extract** from fetched sources with a full audit trail — no invented, repaired or
back-filled values. Where the source is silent, the artefact is silent (documented), and every known source-side
defect is flagged with cross-checks instead of being silently "fixed".

## Folder structure

```
supervisor/          ← owner commissions, read-only mirrors (workorder register in supervisor/README.md)
  workorders/        ← all 16 five-year-span workorders + archive/ (superseded RPL WO)
handoffs/            ← return artifacts, ONE text file each (BP-TEAM-PACK v2, .txt only)
data/rpl/            ← audited RPL league CSV dataset 2021/22–2025/26 (1,212 rows + closing 1X2 odds)
docs/                ← audit trail, data dictionary, per-season notes
audit/               ← machine validation output (pack gates, CSV validation, ledger transcriptions)
tools/               ← reproducible builder/validator scripts
WORKORDER-STATUS.md  ← live queue register and reconciliation notes
```

## Delivered returns

| Return | Artifact | Verification |
|---|---|---|
| **Russian Premier League 2021-22 → 2023-24** (WO-RPL-BACKFILL-01, returned 2026-08-03, **re-issued same-day under errata ERRATA-2026-08-03**) | `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` — 732 MATCH rows ((240 league, compType `domestic-league` + 4 playoff, compType `other` per errata) ×3), 3 TEAM / 13 SOURCE / 17 NOTE, `END` | `audit/pack-validation-rpl.txt` — **69/69 gates PASS** (round counts, final tables 16/16 ×3 vs RSSSF official incl. all 7 H2H ties recomputed, 6 playoff aggregates + outcomes, totals 639/730/637, per-club pivots 30×16, boundary/dupes/identity, second-index diff 730/732 with 2 documented conflicts). Builder: `tools/build_rpl_pack.py`, raw ledger: `audit/ledger/rpl-*.txt`. |
| **Russian Cup 2021-22 → 2023-24** (WO-RUSCUP-BACKFILL-03, returned 2026-08-03, **re-issued same-day under errata ERRATA-2026-08-03**) | `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` — 189 MATCH rows (36+77+76, compType `domestic-cup` per errata), **22 TEAM** (incl. `TEAM|FC Ufa` per standing cup-audit instruction; KAMAZ in exact form) / 10 SOURCE / 69 NOTE, `END` | `audit/pack-validation.txt` — **162/162 gates PASS** (slice counts, group tables club-for-club, bracket→champions 2022 Spartak / 2023 CSKA / 2024 Zenit, 14 aggregates, per-club pivots, boundary/dupes/identity). Builder: `tools/build_pack.py`, raw ledger: `audit/ledger/`. |
| **RPL league dataset 2021/22–2025/26** (CSV-era return, 2026-08-02) | `data/rpl/RPL-2021-22.csv` … `RPL-2025-26.csv` + `rpl_all_2021-2026.csv` (1,212 rows: FT score + closing 1X2 odds) | `docs/AUDIT.md` + `audit/validation-report.txt` — computed final tables reproduce the official tables row-for-row for all five seasons (2 source defects identified, kept verbatim). Pipeline: `tools/assemble_validate.py`. |

## Sources

* **RPL league pack:** RSSSF season pages league chapters (`rus2022/2023/2024.html`, scores AND
  dates, primary; final tables + stadium table) + football-data.co.uk match feeds as the diffed
  second index (730/732 identical; 2 documented conflicts resolved to RSSSF) + Wikipedia season
  articles (venue tables, playoff match boxes, infobox totals) as third anchor.
* **Russian Cup pack:** RSSSF season pages (`rsssf.org/tablesr/rus2022.html`, `rus2023.html`,
  `rus2024.html` — cup chapters, scores AND dates, primary) + Wikipedia season pages with linked
  RFS (rfs.ru) match sheets as the independent second index; every one of the 189 rows
  cross-checked match-for-match.
* **RPL CSV dataset:** football-data.co.uk combined RPL file (retrieved 2026-08-02, only data
  origin); verification-only cross-checks vs Wikipedia/tribuna/sportsmole/365scores and the
  Russian sports press, cited inline in `docs/AUDIT.md`.

## Provenance guarantee

* Machine validation on every deliverable; outputs committed under `audit/`.
* 90-minute doctrine everywhere: shootouts/aet live in NOTE lines, match rows carry 90-minute scores.
* Identity discipline: pinned roster strings (WO-RPL §3), renames documented in NOTEs, no duplicate clubs.
* Next in the owner queue: CZ1 Czech First League pack (②) and the remaining workorders listed in
  `supervisor/README.md` — see `WORKORDER-STATUS.md` for the live register.
