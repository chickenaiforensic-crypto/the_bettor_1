# RELAY TO AUDITOR — 2026-08-06 (planner: re-gate 5 packs)

**5 packs have been grammar-fixed and need your receipt audit.**

| Pack | Rows | What changed |
|---|---|---|
| MLS | 1,994 | Grammar fixed to 14 fields, round moved to NOTE, advancement NOTES restored, season-specific source IDs |
| USOC | 45 | Same grammar fix |
| SCOCUP | 68 | New return — RSSSF R16→Final, early-round blocker noted |
| SCOLC | 72 | New return — RSSSF R16→Final, early-round blocker noted |
| KOSCUP | 120 | New return — full coverage R1→Final (no blocker) |

All in `handoffs/` on `arena/019fd4e0-the-bettor-1`. All 14 fields verified by planner.

**Also:** the UEFA-FULL pack (`handoffs/UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt`) still contains 436 fabricated rows. The corrected store (16,193) has them removed, but the pack file itself needs a clean version. Researcher is assigned to regenerate it.

**Corrected store:** `audit_work/pitch-rating-full-16193-corrected-2026-08-06.json` — 16,193 rows, 0 fabricated, adopted as baseline.
