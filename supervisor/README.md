# supervisor — commissions from the owner

Everything here is **owner-supplied** (mirrored read-only). Researcher returns land in `../handoffs/`.

## Binding rules (owner's handoffs convention)

1. **Match rows, never tables.** A return is a list of played games: date / home team / away team / score (90-minute doctrine). Standings tables are recompute *targets* — never accepted as input.
2. **Format:** BP-TEAM-PACK v2 exactly as defined in the workorder that commissioned the work.
3. **Naming:** `<LEAGUE>-<scope>_BP-TEAM-PACK_v2.txt`.
4. **Text files only. No .zip, ever.**
5. **Auditor verification before anything enters the app:** boundary scan, dedupe vs the live store, reproduction vs the official record — nothing is imported on trust.
6. **Never guess.** If a fact in the workorder is genuinely unknowable, write a NOTE line — do not fabricate numbers.

## Workorder register (mirrored 2026-08-03 from `origin/main`; those copies are authoritative)

| # in queue | Workorder | Commission | Return artifact | Status |
|---|---|---|---|---|
| ③ — **overridden live → done first** | `workorders/WORKORDER-RUSCUP-2021-2026-5YSPAN.md` | Russian Cup 2021-22 → 2023-24 (WO-RUSCUP-BACKFILL-03) | `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` | **RETURNED 2026-08-03 · 189 rows · 162/162 self-gates PASS · re-issued under ERRATA-2026-08-03: compType domestic-cup, 22 TEAM (FC Ufa added), KAMAZ exact-form** |
| ① | `workorders/WORKORDER-RPL-2021-2026-5YSPAN.md` | Russian Premier League 2021-22 → 2023-24 (+ playoffs) | `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` | **RETURNED 2026-08-03 · 732 rows · 69/69 self-gates PASS · re-issued under ERRATA-2026-08-03: 12 playoff rows compType other (corrected WO fingerprint 9903cf856877d173ba71d72cef64e9c6)** |
| ② | `workorders/WORKORDER-CZ1-2021-2026-5YSPAN.md` | Czech First League 2021-22 → 2023-24 | `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | **RETURNED 2026-08-03 · 829 rows (276+276+277) · 0 TEAM per §2 · 105/105 self-gates PASS · 12 pro/rel legs held out pending owner roster sanction (`roster_scope`)** |
| ④ | `workorders/WORKORDER-MOLCUP-2021-2026-5YSPAN.md` | Czech MOL Cup 2021-22 → 2023-24 | pending | next (compType `domestic-cup` per ERRATA-2026-08-03) |
| — | `workorders/WORKORDER-EPL-2021-2026-5YSPAN.md` | English Premier League | pending | queued |
| — | `workorders/WORKORDER-SPA-2021-2026-5YSPAN.md` | Spanish league | pending | queued |
| — | `workorders/WORKORDER-FRA-2021-2026-5YSPAN.md` | French league | pending | queued |
| — | `workorders/WORKORDER-GER-2021-2026-5YSPAN.md` | German league | pending | queued |
| — | `workorders/WORKORDER-ITA-2021-2026-5YSPAN.md` | Italian league | pending | queued |
| — | `workorders/WORKORDER-KOS-2021-2026-5YSPAN.md` | Kosovo league | pending | queued |
| — | `workorders/WORKORDER-KOSCUP-2021-2026-5YSPAN.md` | Kosovo cup | pending | queued |
| — | `workorders/WORKORDER-MLS-2021-2026-5YSPAN.md` | MLS | pending | queued |
| — | `workorders/WORKORDER-SCO1-2021-2026-5YSPAN.md` | Scotland Premiership | pending | queued |
| — | `workorders/WORKORDER-SCOCUP-2021-2026-5YSPAN.md` | Scottish Cup | pending | queued |
| — | `workorders/WORKORDER-SCOLC-2021-2026-5YSPAN.md` | Scottish League Cup | pending | queued |
| — | `workorders/WORKORDER-USOC-2021-2026-5YSPAN.md` | US Open Cup | pending | queued |
| archived | `workorders/archive/WORKORDER-RPL-2021-24-BACKFILL.md` | Superseded commission WO-RPL-BACKFILL-01 (owner "approved" the CSV-era return; kept for history) | superseded by the 5YSPAN RPL order | archived |

All commissions share the same envelope: 5-year span 2021-07 → today, hard cutoff
**no new rows dated ≥ 2024-06-30** (2024-25 + 2025-26 held client-side, current season fills
centrally), RSSSF-primary sourcing, roster discipline from WO-RPL §3 for Russia.
