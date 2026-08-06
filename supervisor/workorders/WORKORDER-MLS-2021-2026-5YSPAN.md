# WORK ORDER -- Major League Soccer 5-year-span 2021-2026 up-to-today (researcher commission WO-MLS-SPAN-07)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 7 (heaviest file; run last) - research may run in parallel with other commissions (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)
**Why:** the 5-year span decree, this league's leg. Our held coverage is slate-scatter (36 regular + 28 playoff rows -- appendix). This order delivers the complete league 2021-2025 plus 2026-to-date, minus the appendix rows.

---

## 0. READ FIRST -- federation check

This is **Major League Soccer -- the USA/Canada top flight**: LA Galaxy, Inter Miami, Seattle Sounders... It is **not** Mexico's Liga MX, not the USL (second tier), and the **Leagues Cup is explicitly OUT** (cross-border tournament, not this competition). **Before returning anything, scan your own rows: any club outside the section-3 table = wrong competition -- stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree. Our held coverage in this competition is slate-scatter/run-in only (listed in the appendix), so unlike the RPL/CZ1 orders there is **no date cutoff** -- you cover the whole span and simply **must not return any appendix row** (they are already stored; the auditor dedupes against this exact list). You supply the span minus its held fragment; the APPROVAL certifies it gap-free to today.

## 1. SCOPE -- complete seasons only

| Competition | Seasons | Expected rows |
|---|---|---|
| Major League Soccer -- regular season | 2021, 2022, 2023, 2024, 2025 | 459 + 476 + 493 + 493 + 510 |
| Major League Soccer -- regular season | 2026, through your return date | state the last round/date covered in a NOTE |
| MLS Cup Playoffs (championship playoff of the same season) | 2021, 2022, 2023, 2024, 2025 | per bracket -- state round-by-round counts in a NOTE |

Club counts per season -- any deviation = you are on the wrong year: **2021: 27 clubs - 2022: 28 (Charlotte FC joins) - 2023: 29 (St. Louis City SC joins) - 2024: 29 - 2025: 30 (San Diego FC joins) - 2026: 30.** Every club plays **34 regular-season matches** per completed season. Playoff formats differ by year (2021-22: single-elimination bracket; 2023 onward: wild-card singles + best-of-3 first round + single-elimination) -- record the format you used per season in a NOTE.

**Minus:** the 64 appendix rows (already held). **Scale warning:** this is the programme's biggest commission -- roughly 2,800 rows. Accuracy over speed; deliver in one file regardless.
**Not in this order:** US Open Cup, Leagues Cup, Canadian Championship, friendlies, CONCACAF competitions.

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-league` (all rows, playoffs too -- matches our existing rows)
  - Round/stage identifiable per row in the venue-detail field (`RS R17`, `QF leg2`, `Group-A R3`, `Relegation-Round` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. Ties settled on penalties or in extra time record the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced` -- without it brackets cannot be reconstructed.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every reconciliation decision, rename mapping, format reading, source conflict.
  - `<competition>` strings, verbatim: `Major League Soccer` - `MLS Cup Playoffs`
  - 2023+ playoff rounds: no aggregate; series games are individual rows; best-of-3 series get one `NOTE|info|advancement` naming the SERIES winner; single games decided on penalties (most MLS playoff rounds have no extra time) get their NOTE per game.
- `TEAM|<name>|<country>|<leagueName>|<leagueCode>|...` -- **NOT expected**: all 30 MLS clubs are already on our roster (section 3). If you think one is missing, stop and write `NOTE|warning|blocker`; do NOT invent an identity.
- End the file with `END`. No standings tables anywhere -- rows only.

## 3. IDENTITY DISCIPLINE (no duplicate clubs) -- the 30-club table

Use these **exact strings** in home/away for every season. All 30 exist on our roster; do NOT re-declare them. Right column = how source pages often write the same club -- map silently to our string, NOTE each mapping rule once:

| Our string (verbatim) | Sources may write |
|---|---|
| Atlanta United FC | Atlanta United |
| Austin FC | -- |
| CF Montréal | Montréal CF - CF Montreal - Montreal |
| Charlotte FC | -- |
| Chicago Fire FC | Chicago Fire |
| Colorado Rapids | -- |
| Columbus Crew | -- |
| D.C. United | DC United (the dots matter) |
| FC Cincinnati | -- |
| FC Dallas | -- |
| Houston Dynamo FC | Houston Dynamo |
| Inter Miami CF | Inter Miami |
| LA Galaxy | Los Angeles Galaxy - LA Galaxy |
| Los Angeles FC | LAFC |
| Minnesota United FC | Minnesota United |
| Nashville SC | -- |
| New England Revolution | -- |
| New York City FC | New York City - NYCFC |
| New York Red Bulls | -- |
| Orlando City SC | Orlando City |
| Philadelphia Union | -- |
| Portland Timbers | -- |
| Real Salt Lake | RSL |
| San Diego FC | (**never before 2025**) |
| San Jose Earthquakes | -- |
| Seattle Sounders FC | Seattle Sounders |
| Sporting Kansas City | Sporting KC - SKC |
| St. Louis City SC | Saint Louis City SC - St Louis CITY SC (**never before 2023**) |
| Toronto FC | -- |
| Vancouver Whitecaps FC | Vancouver Whitecaps |

Absence traps: **San Diego FC** row dated before 2025 = fail - **St. Louis City** before 2023 = fail - **Charlotte** in 2021 = fail - Austin FC is present in every completed season of the window.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF round-by-round + final tables = primary:** `rsssf.org/tablesu/usa<YEAR>.html` (2021 = `usa2021.html` ... 2026 = `usa2026.html`) -- the regular-season grid AND the championship-playoff bracket are on the same page.
2. Cross-verify every round against one independent index (mlssoccer.com / worldfootball.net / soccerway).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable --> `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (we re-run all of these on receipt -- failing any = returned incomplete)

- **Table reproduction:** recomputed from your rows alone, each completed season's final tables -- **both conferences, club-for-club, W-D-L, GF-GA, pts** -- reproduce the official tables. Zero tolerance.
- **Bracket reproduction:** per season the playoff bracket you return must produce the official MLS Cup finalists and champion; every pens/aet game and every best-of-3 series carries its advancement NOTE.
- **Shape:** 34 matches per club per completed season (2026: uniform to-date count per club -- a one-match gap demands a NOTE-reason, e.g. postponed).
- **Boundary:** none of the 64 appendix rows returned; no dateless rows; no duplicates.
- **Names:** every home/away string in the 30-string table; source-spelling variants appear only in NOTEs; expansion-absence traps clean.
- **Spot-audit trail:** one round per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full **gap-free 5-year span running up to today** for this competition (minus the appendix's already-held rows). After your rows pass the gates above, the auditor diffs the ENTIRE span -- your rows + our held rows -- against the full research record. Any official match inside the span stored nowhere = a written gap defect; the return stays open until each gap is filled or NOTE-explained (postponed/abandoned/awarded ties, etc.). The purpose of researching all data is exactly this: to prove our old data is missing nothing.
## 6. RETURN PROTOCOL

Save as `MLS-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: recompute all five tables + brackets --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake. USA leg then reads **5 full seasons + current**.

---

## APPENDIX -- DO NOT RETURN (already held; auditor dedupes against this exact list, 64 rows)

### Major League Soccer -- held (36)
2024-10-19 | Philadelphia Union 1-2 FC Cincinnati
2024-10-19 | D.C. United 0-3 Charlotte FC
2024-10-19 | Orlando City SC 1-2 Atlanta United FC
2024-10-19 | Inter Miami CF 6-2 New England Revolution
2024-10-19 | Minnesota United FC 4-1 St. Louis City SC
2024-10-19 | Real Salt Lake 2-1 Vancouver Whitecaps FC
2024-10-19 | Seattle Sounders FC 1-1 Portland Timbers
2024-10-19 | Houston Dynamo FC 2-1 LA Galaxy
2024-10-19 | Austin FC 3-2 Colorado Rapids
2024-10-19 | FC Dallas 2-1 Sporting Kansas City
2024-10-19 | Los Angeles FC 3-1 San Jose Earthquakes
2026-07-22 | Nashville SC 1-0 CF Montréal
2026-07-22 | Houston Dynamo FC 1-1 D.C. United
2026-07-22 | Sporting Kansas City 2-1 Minnesota United FC
2026-07-22 | Austin FC 3-1 Seattle Sounders FC
2026-07-22 | Colorado Rapids 1-0 San Diego FC
2026-07-22 | Los Angeles FC 3-1 Real Salt Lake
2026-07-22 | Portland Timbers 2-2 FC Dallas
2026-07-22 | San Jose Earthquakes 0-4 Orlando City SC
2026-07-22 | LA Galaxy 1-3 St. Louis City SC
2026-07-25 | New York Red Bulls 0-2 Charlotte FC
2026-07-25 | Columbus Crew 2-1 FC Cincinnati
2026-07-25 | Philadelphia Union 1-0 Seattle Sounders FC
2026-07-25 | CF Montréal 0-1 Inter Miami CF
2026-07-25 | New York City FC 3-1 Chicago Fire FC
2026-07-25 | D.C. United 2-1 Toronto FC
2026-07-25 | New England Revolution 4-1 Atlanta United FC
2026-07-25 | Houston Dynamo FC 3-0 Austin FC
2026-07-25 | Minnesota United FC 0-0 Vancouver Whitecaps FC
2026-07-25 | St. Louis City SC 1-0 Colorado Rapids
2026-07-25 | Orlando City SC 1-0 Nashville SC
2026-07-25 | San Diego FC 1-0 FC Dallas
2026-07-25 | San Jose Earthquakes 1-1 LA Galaxy
2026-07-25 | Los Angeles FC 4-0 Sporting Kansas City
2026-07-25 | Portland Timbers 2-1 Real Salt Lake
2026-07-31 | New York City FC 1-1 Toronto FC
### MLS Cup Playoffs -- held (28)
2024-10-22 | CF Montréal 2-2 Atlanta United FC
2024-10-24 | Vancouver Whitecaps FC 5-0 Portland Timbers
2024-10-25 | Inter Miami CF 2-1 Atlanta United FC
2024-10-26 | LA Galaxy 5-0 Colorado Rapids
2024-10-27 | Orlando City SC 2-0 Charlotte FC
2024-10-27 | Los Angeles FC 2-1 Vancouver Whitecaps FC
2024-10-28 | FC Cincinnati 1-0 New York City FC
2024-10-28 | Seattle Sounders FC 0-0 Houston Dynamo FC
2024-10-29 | Columbus Crew 0-1 New York Red Bulls
2024-10-29 | Real Salt Lake 0-0 Minnesota United FC
2024-11-01 | Charlotte FC 0-0 Orlando City SC
2024-11-01 | Colorado Rapids 1-4 LA Galaxy
2024-11-02 | New York City FC 3-1 FC Cincinnati
2024-11-02 | Atlanta United FC 2-1 Inter Miami CF
2024-11-02 | Minnesota United FC 1-1 Real Salt Lake
2024-11-03 | New York Red Bulls 2-2 Columbus Crew
2024-11-03 | Houston Dynamo FC 1-1 Seattle Sounders FC
2024-11-03 | Vancouver Whitecaps FC 3-0 Los Angeles FC
2024-11-08 | Los Angeles FC 1-0 Vancouver Whitecaps FC
2024-11-09 | FC Cincinnati 0-0 New York City FC
2024-11-09 | Orlando City SC 1-1 Charlotte FC
2024-11-09 | Inter Miami CF 2-3 Atlanta United FC
2024-11-23 | Los Angeles FC 1-1 Seattle Sounders FC
2024-11-24 | Orlando City SC 1-0 Atlanta United FC
2024-11-24 | LA Galaxy 6-2 Minnesota United FC
2024-11-30 | Orlando City SC 0-1 New York Red Bulls
2024-11-30 | LA Galaxy 1-0 Seattle Sounders FC
2024-12-07 | LA Galaxy 2-1 New York Red Bulls
