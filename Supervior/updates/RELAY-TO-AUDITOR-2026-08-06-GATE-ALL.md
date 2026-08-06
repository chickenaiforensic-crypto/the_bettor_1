# RELAY TO AUDITOR — 2026-08-06 (planner: gate all current work)

**You have work to gate. Nothing gets adopted without your verification.**

---

## Data to audit

### MLS 2025 regular season (510 rows) — NOT YET GATED

Researcher delivered 510 rows from worldfootball.net. Tables claim to reproduce official RSSSF 2025 table with zero mismatches. **You verify this independently.** Don't trust the researcher's self-gate.

- Pack: `handoffs/MLS-2021-2026_BP-TEAM-PACK_v2.txt` (2,504 rows total, 510 new for 2025)
- Source files: `audit_work/.mls_raw/2025/md1.txt` through `md34.txt`
- Method: worldfootball.net matchday pages
- Claim: 2025 final table reproduces RSSSF official table club-for-club

**Your gates:**
1. Re-parse the 510 rows independently against worldfootball or RSSSF
2. Recompute the 2025 final table from the rows yourself — verify club-for-club
3. Check for duplicates vs existing store
4. Check source linkage (14 fields, source IDs match SOURCE blocks)
5. Check date sanity, score sanity

### MLS 2026 to-date (when researcher delivers)

Same gates as above. Worldfootball source. Verify against independent index.

### SCOCUP, SCOLC, KOSCUP — NOT YET FULLY GATED

Grammar re-gate passed, but you haven't verified the actual match data against independent sources. Spot-check at minimum: one random round per pack against RSSSF or worldfootball.

### UEFA-FULL cleaned pack (2,764 rows)

Researcher stripped 436 fabricated rows. Verify the remaining rows are real — spot-check a sample against RSSSF/uefa.com.

## Code to audit

### B5 v3.12.0 balance panel

Builder claims NO CALL shows support shares. Verify:
- `renderBalancePanel()` actually renders for NO CALL cases
- Balance bar shows home/draw/away percentages
- No market data introduced (fetch=0, XHR=0)
- Byte-diff vs B4 documented

### B4 v3.11.0 settlement + venue guard

Already audited M17 as FAIL on v3.9.0. Builder claims B4 fixes it. Verify:
- `classifyOutcome()` correctly classifies H/D/A
- Draw = loss, never push — test with 3 frozen rows
- `isVenueVerified()` hard blocks unknown venues
- Venue guard works on pack import (Z-003 style holds)

## Corrected store

`audit_work/pitch-rating-full-16193-corrected-2026-08-06.json` — 16,193 rows, 0 fabricated. Ladder re-run confirmed domestic results unchanged. **Verify independently:** run the harness yourself on this store, confirm parity.

---

*Nothing enters the store or ships without your verification. Fresh code, never the previous auditor's scripts.*
