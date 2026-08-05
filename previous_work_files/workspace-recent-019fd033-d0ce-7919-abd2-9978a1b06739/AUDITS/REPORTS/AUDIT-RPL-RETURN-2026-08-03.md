# AUDIT CARD — RPL league return (WO-RPL, queue ①) — 2026-08-03

**Return:** `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` · branch `arena/019fc462-the-bettor-1`
commit `e22f3a4` (2026-08-03T13:53:42Z) · 125,638 B · md5 `c3a72b35e834cc030d62b3d160c79b25` (pinned)
**Census:** 732 MATCH (720 league + 12 relegation playoffs) · 3 TEAM · 13 SOURCE · 20 NOTE · END ✓

## Verdict: **APPROVED for import** — every gate passed, zero defects.

| Gate | Result |
|---|---|
| **Table reproduction vs RSSSF (zero tolerance)** | **2021-22 16/16 ✓ · 2022-23 16/16 ✓ · 2023-24 16/16 ✓** — W-D-L and GF-GA exact for all 48 club-seasons, recomputed from his rows alone |
| Shape | 240/240/240 league rows; every club = 30 played ✓ |
| Boundary | max date 2024-06-01 < 2024-06-30 ✓ (playoffs 2024-06-01 inside) |
| Internal duplicates | 0 ✓ |
| Overlap vs held store | 0 (window disjoint from held 489 league + 2 playoff rows) ✓ |
| Errata applied | league = `domestic-league` ×720; playoffs = `other` ×12 — exact ✓ |
| Identity | ALL home/away strings resolve; 3 TEAM declarations = exactly the right ones (FC Ufa — RPL 2021-22, folded 2022; Yenisey Krasnoyarsk + SKA Khabarovsk — FNL playoff opponents) ✓ |
| Playoff content | 2 ties × 2 legs × 3 seasons — matches RSSSF structure (2022 Orenburg↔Ufa, SKA↔Khimki; 2023 Rodina↔Pari NN, Yenisey↔Fakel; 2024 Pari NN↔Arsenal Tula, Ural↔Akron — Akron promotion leg consistent with held 2024-25 roster) ✓ |

**Import note:** no auditor normalization needed on this file — it is byte-ready.
