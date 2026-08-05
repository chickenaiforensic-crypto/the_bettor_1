# AUDIT CARD — CZ1 patch return (12 pro/rel rows) — 2026-08-03
**Return:** `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` (v3) · branch commit `9dc08ee` (2026-08-03T19:21:15Z) · 148,571 B · md5 `29c3b6c9d63906bde4db20ac4e6b742c` · sha256 `55d9bd80ef3d…` (matches commit message)
**Census:** 841 MATCH (829 league `domestic-league` + 12 `Czech Relegation Playoffs` `other`) · 0 TEAM · 21 NOTE · 14 SOURCE · END ✓

## Verdict: APPROVED — with the import-order condition (MOLCUP first)

| Gate (auditor re-run) | Result |
|---|---|
| Body preservation | byte-diff vs approved `c4b4664e`: **the only MATCH-line change is +12 rows** (NOTE/SOURCE scaffold texts updated; zero league rows touched) |
| **12 playoff rows vs my RSSSF pins** | **12/12 EXACT** — 2022: Opava 0-1 Bohemians, Teplice 3-0 Vlašim (05-19); Bohemians 2-0 Opava, Vlašim 2-2 Teplice (05-22) · 2023: Příbram 0-2 Pardubice, Zlín 1-0 Vyškov (06-01); Pardubice 0-0 Příbram, Vyškov 0-0 Zlín (06-04) · 2024: Č.Budějovice 2-1 Táborsko, Vyškov 0-1 Karviná (05-30); Karviná 1-0 Vyškov, Táborsko 1-1 Č.Budějovice (06-02) — dates, scores, home/away order all exact; venues era-correct (Vyškov at Drnovice, Pardubice at CFIG from 2023 spring) |
| compType | playoff rows `other` per ERRATA ✓ · league rows `domestic-league` ✓ |
| Hold risk | none: no tieIds; each pair = exactly 2 rows |
| Advancement NOTEs | correctly absent (all 6 ties settled inside 180', no shootouts) |
| Roster strings | Opava/Vyškov/Táborsko held ✓ · **Vlašim + Příbram NOT held** (export 2026-08-02) → supplied by the MOLCUP pack's TEAM rows. The patch NOTE's phrase "already-on-the-client-roster" is over-broad for these two — a NOTE-text inaccuracy only, zero row defect; the import order below closes it |

**Binding order:** RPL → RUSCUP → **MOLCUP → CZ1 patch**. Swapping the last two leaves 4 CZ1 rows (Vlašim ×2, Příbram ×2) referencing undeclared names.

Second-pass items still queued (unchanged): 2022-23/2023-24 Titul+Záchranu bulk diff; Russia span-diff.
