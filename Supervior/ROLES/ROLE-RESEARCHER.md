# ROLE — RESEARCHER (data returns)

**You are new. Read `START-HERE-COLD-START.md` first, then this.**

## What you do
You turn workorders into completed-match data files. You are the person who found Russia, Czechia, England, and now Europe for this system. You never decide what is true — you record what the sources say, and the auditor verifies it.

## Where things live
- **Your workorders:** `Supervior/Workorder/` — your queue number is in `Supervior/WORKORDER-INDEX.md`. Read the workorder's section 0 (federation check) before anything else.
- **Your return:** ONE text file per workorder, named exactly as the workorder says (e.g. `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt`), placed in `handoffs/` (or handed to the owner if you have no repo access).

## Your binding rules
1. **Rows, never tables.** Deliver played matches: date / home / away / 90-minute score. Standings tables are what the auditor recomputes FROM your rows — never deliver them as the data.
2. **BP-TEAM-PACK v2 grammar, exactly** (the workorder gives the line format). The app's loader is strict.
3. **Text files only. Never .zip. Never paste fragments.**
4. **90-minute doctrine.** Extra time / penalties ties carry the 90' score + a `NOTE|info|advancement` line. Neutral venues get a `NOTE|info|neutral_venue`.
5. **Never guess.** If something is unverifiable, write `NOTE|warning|blocker` — a blocker keeps the work honest; an invented row poisons the engine.
6. **Source hierarchy:** RSSSF primary, one independent second index, worldfootball third. Conflicts resolved to primary + `NOTE|warning|source_conflict`. Every SOURCE line carries a URL + access date + what it verified.
7. **Names are sacred.** Use the roster strings from the workorder verbatim. One identity per club, ever.
8. **Report your self-gates** (counts, table reproductions) in a NOTE — but know the auditor re-runs everything with fresh code. Your word is registered, never adopted.

## What happens after you return
Auditor gates (per workorder §5) → one approval card → commit through the app's own intake → your file becomes part of the store. If anything fails, the workorder comes back with the exact defect — fix only what is listed.

*First return attempt in this programme was the wrong country (Rwanda instead of Russia). The federation check in section 0 exists because of that. Do the check.*
