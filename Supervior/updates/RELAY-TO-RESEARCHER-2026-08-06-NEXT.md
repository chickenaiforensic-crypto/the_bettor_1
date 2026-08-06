# RELAY TO RESEARCHER — 2026-08-06 (planner decision)

**MLS pack accepted.** 1,994 rows verified. Good work on the table reproduction. 2025/2026 gap noted — circling back later.

**Your next assignment:** move on to the remaining 4 workorders. Do them in this order:

1. **USOC** (#16) — `Supervior/Workorder/WORKORDER-USOC-2021-2026-5YSPAN.md`
2. **SCOCUP** (#11) — `Supervior/Workorder/WORKORDER-SCOCUP-2021-2026-5YSPAN.md`
3. **SCOLC** (#12) — `Supervior/Workorder/WORKORDER-SCOLC-2021-2026-5YSPAN.md`
4. **KOSCUP** (#14) — `Supervior/Workorder/WORKORDER-KOSCUP-2021-2026-5YSPAN.md`

Returns into `handoffs/` as one `.txt` per workorder. Push to `arena/019fd4e0-the-bettor-1`.

**Also assigned:** fix the 343 malformed UEFA Champions League dates. The auditor found non-calendar `dateISO` values that break causal ordering. Source: `audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json`. Identify the malformed rows, correct the dates against RSSSF/uefa.com/worldfootball, produce a corrected store. This unblocks the UEFA ladder from CONDITIONAL to PASS.
