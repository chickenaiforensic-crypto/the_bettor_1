# RELAY TO RESEARCHER — 2026-08-06 (planner: two tasks)

**Your cup packs (SCOCUP, SCOLC, KOSCUP) are submitted. Auditor is re-gating.**

**Two remaining tasks:**

## 1. Regenerate UEFA-FULL pack (strip fabricated rows)

The `handoffs/UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt` file has 436 fabricated rows (ClubA1–ClubA436, all 1-0, fake stadiums). The corrected store already has them removed (16,193 rows), but the pack file itself still carries them.

**Action:** produce a clean version of the pack with only the 2,764 real UEFA rows. Same grammar (14 fields). Replace the file in `handoffs/`. Push to `arena/019fd4e0-the-bettor-1`.

## 2. MLS 2025/2026 gap (when ready)

The MLS pack is missing 2025 regular season (~493 rows) and 2026 to-date. RSSSF doesn't have those listings. Source: worldfootball.net.

This is lower priority than the UEFA-FULL fix. Do the UEFA-FULL cleanup first, then circle back to this when ready.

---

*Push to `arena/019fd4e0-the-bettor-1`. Workspace guide: `Supervior/updates/WORKSPACE-GUIDE-2026-08-06.md`.*
