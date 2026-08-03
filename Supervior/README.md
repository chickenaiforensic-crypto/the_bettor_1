# handoffs — where returns land

Every return from a researcher or builder session is dropped here (via the owner) as ONE text file.

## Binding rules
1. **Match rows, never tables.** A return is a list of played games: date / home team / away team / score (90-minute doctrine). Standings tables are recompute *targets* — never accepted as input.
2. **Format:** BP-TEAM-PACK v2 exactly as defined in the Supervisor workorder that commissioned the work.
3. **Naming:** `<LEAGUE>-<scope>_BP-TEAM-PACK_v2.txt` (e.g. `RPL-2021-24_BP-TEAM-PACK_v2.txt`).
4. **Text files only. No .zip, ever.**
5. **Auditor verification before anything enters the app:** boundary scan, dedupe vs the live store, full-season table reproduction vs the official record (16/16 or the return is rejected). Nothing is imported on trust.
6. **Never guess.** If a fact in the workorder is genuinely unknowable, write a NOTE line — do not fabricate numbers.

## Currently open commission
`Supervisor/WORKORDER-RPL-2021-24-BACKFILL.md` — **Russian** Premier League (Zenit, CSKA, Spartak, Krasnodar… — NOT Rwanda), seasons 2021-22, 2022-23, 2023-24 → 720 league match rows + playoffs, cutoff < 2024-06-30.
