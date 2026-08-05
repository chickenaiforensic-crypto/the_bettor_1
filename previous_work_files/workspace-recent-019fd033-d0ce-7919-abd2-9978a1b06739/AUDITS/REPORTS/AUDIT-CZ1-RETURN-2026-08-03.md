# AUDIT CARD — CZ1 league return (queue ②) — 2026-08-03
**Return:** `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` · branch commit `8034d90` (2026-08-03T14:28:09Z) · 143,566 B · md5 `c4b4664e123002794229c64e8a026c6c` (pinned)
**Census:** 829 MATCH (no TEAM rows — correct, all clubs held) · 12 SOURCE · 21 NOTE · END ✓

## Verdict: BODY APPROVED — 1 OMISSION (12 pro/rel playoff rows), patch requested

| Gate (auditor re-run) | Result |
|---|---|
| **Regular-stage tables vs RSSSF** | **3 seasons × 16 clubs = 48/48 EXACT** (W-D-L GF-GA recomputed) |
| Evropu playoff brackets | **18/18 rows exact** (all 3 SFs + Fs, dates+scores) |
| Conference-league playoff (+1) | exact — Boleslav 3-1 Hradec 2024-05-31 ✓ (explains his 829 vs my 828 estimate: real format adds the CLP single game in 2023-24 — his count is RIGHT, my workorder estimate was the approximation) |
| 2021-22 Titul + Záchranu groups | 30/30 rows exact; 2022-23/2023-24 counts 15/15 each (spot suite green, second-pass bulk diff queued) |
| Shape | 240 regular ×3 ✓; stage totals 36/36/37 ✓ |
| Boundary | max 2024-05-31 < cutoff ✓ |
| Names / dupes / overlap held | all resolve held short-forms / 0 / 0 ✓ |
| compType | league rows all `domestic-league` ✓ (errata-consistent) |

## OMISSION — `Czech Relegation Playoffs` rows missing (workorder §1 commissions them; compType `other` per ERRATA)
RSSSF-proven ties inside the window, none present in the pack:
- 2021-22: Teplice 3-0 Vlašim (2022-05-19), Vlašim 2-2 Teplice (2022-05-22) · Opava 0-1 Bohemians (05-19), Bohemians 2-0 Opava (05-22)
- 2022-23: Příbram 0-2 Pardubice (2023-06-01), Pardubice 0-0 Příbram (06-04) · Zlín 1-0 Vyškov (06-01), Vyškov 0-0 Zlín (06-04)
- 2023-24: Vyškov 0-1 Karviná (2024-05-30), Karviná 1-0 Vyškov (06-02) · Č. Budějovice 2-1 Táborsko (05-30), Táborsko 1-1 Č. Budějovice (06-02)
= **12 rows**, competition string `Czech Relegation Playoffs`, compType `other`. All aggregate-decided in 90-minute legs (no shootouts → no advancement NOTEs needed). Every club already held (Opava ✓ Vlašim? — check aliases: Vlašim held as 'Sellier & Bellot Vlašim'? CZ2 list has Vlašim? — roster CZ2 includes Opava, Vyskov, Taborsko, Pribram? — NOTE: Příbram/Vlašim presence to be re-verified at patch audit; if absent, TEAM rows required).
