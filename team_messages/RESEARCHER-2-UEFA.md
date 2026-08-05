# For Researcher #2 — UEFA Connector (PRIORITY #17)

Copy-paste this DM/email:

---
Subject: Your task — UEFA Connector #17 PRIORITY — Branch arena/019fd213-the-bettor-1

Hi [Name],

You are Researcher #2 — UEFA Connector, this is PRIORITY.

Repo: chickenaiforensic-crypto/the_bettor_1
Branch: arena/019fd213-the-bettor-1 (checkout exact, pull before push)

Read in order:
1. START-HERE-COLD-START.md
2. Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md §6 cross-league fit-to-results loop (why we need this)
3. Supervior/ROLES/ROLE-RESEARCHER.md
4. Supervior/Workorder/WORKORDER-UEFA-CONNECTOR-2021-2026-5YSPAN.md — read §0 federation check (this is UEFA clubs, not domestic) + §4 source hierarchy + §5 gates

Scope:
- UCL + Europa League + Conference League + qualifiers, seasons 2021-22..2025-26 + 2026-27 played
- In-scope: every tie with ≥1 club from programme leagues (ENG/RUS/CZE/SPA/ITA/GER/FRA)
- Expected ~2000-2500 rows — report exact counts in NOTE
- 90-min doctrine + shared tieId (both legs ONE tieId or app's Z-003 hold triggers) + neutral venue NOTE if needed
- Russian clubs expected 2021-22 only — if later appears, keep row + NOTE|info|unexpected_participant

Sources (use exactly):
- Primary: RSSSF country European sections #ec (eng2022..eng2026, span/ital/duit/fran quirks) + UEFA.com official archive
- Second: Wikipedia season articles per competition
- Third: worldfootball.net all_matches pages

Deliver:
- ONE file: UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt into handoffs/
- No zip, rows only

After:
```
md5sum handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt
```

Comment md5 + counts in PR. I re-run gates: participation completeness, structure, 90-min, boundary/dedupe, name resolution, legacy 4244-row European index cross-diff. This pack blocks league-strength weighting (M19/A-08) — weighted scale vs frozen 1.00 baseline on omitted European window.

Do not guess. Blockers become NOTE not fake row.

— Lead Planner (Arena AI) on arena/019fd213-the-bettor-1
---
