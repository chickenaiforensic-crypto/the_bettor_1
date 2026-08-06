# WORK ORDER -- US Open Cup 5-year-span 2021-2026 up-to-today (researcher commission WO-USOC-SPAN-08)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 8 - research may run in parallel (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)

---

## 0. READ FIRST -- federation check
This is the **national cup of the USA** (Lamar Hunt US Open Cup, USSF). It is **not** the Canadian Championship, not the Leagues Cup. **Scan your finished rows: any club outside section 3 = wrong competition -- stop.**

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree, exactly as defined in `START-HERE.md`. Coverage mechanics per this workorder's section 1 (cutoff or appendix list). Approval certifies the span gap-free to today for this competition.

## 1. SCOPE -- the audited slice, proven on our held data
**Slice (proven on our held rows -- 0 ties exist without an MLS club in all 21 held rows):** every tie of the tournament in which **at least one participant is an MLS club**, every round MLS clubs play. Ties between two non-MLS clubs are OUT.
| Edition | Notes |
|---|---|
| 2021 | **CANCELLED (covid), as was 2020.** The "2021" slot produces zero rows -- a `NOTE|info|cancelled` stating this is MANDATORY; its absence proves you skipped the year silently and fails the gate |
| 2022 | first edition of the window -- MLS clubs enter at the Round of 32 |
| 2023 | MLS clubs enter at the Round of 32 |
| 2024 | **quirk edition:** several MLS clubs fielded no senior team (Next Pro sides entered instead). Slice = ties of the 8 senior MLS participants + any tie involving an MLS first team. NOTE your reading of participation |
| 2025 | MLS clubs enter at the Round of 32 |
| 2026 | in progress through your return date -- state the last round covered in a NOTE |

Expect roughly 40-60 ties per edition -- **declare round-by-round counts in a NOTE; the auditor recomputes the slice rule against the source and your counts must match.**
**Minus:** the 21 appendix rows (already held).
**Not in this order:** MLS league+playoffs (WO-07), Leagues Cup, Canadian Championship, USL league matches.

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-league` (matches our existing cup rows)
  - Round identifiable per row in the venue-detail field (`R32`, `R16`, `QF`, `SF`, `Final`, `Group-B`, `R2` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. These cups are single-leg: every tie settled in extra time or on penalties records the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced`.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every format reading, rename mapping, source conflict, awarded tie.
- End the file with `END`. No standings tables anywhere -- rows only.
  - `<competition>` string, verbatim: `US Open Cup`
- `TEAM|<name>|United States|<leagueName>|USL|...` -- **allowed and expected for non-MLS opponents** (USL/lower-division clubs are legitimate cup participants; several already exist on our roster -- check first: New Mexico United, Sacramento Republic, Indy Eleven, Detroit City, Memphis 901, Oakland Roots, Louisville City, Las Vegas Lights, Charleston Battery, FC Tulsa, Loudoun United, Tampa Bay Rowdies, Phoenix Rising, Charlotte Independence, Union Omaha exist -- do NOT re-declare).

## 3. IDENTITY DISCIPLINE (no duplicate clubs)
**MLS clubs:** the 30-string table in `Supervisor/WORKORDER-MLS-2021-2026-5YSPAN.md` section 3 applies verbatim -- same strings, same rename traps.
**Non-MLS opponents:** TEAM rows per section 2 for every participant not on our roster. Defence of the slice: every tie must contain at least one MLS club.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)
1. **RSSSF = primary:** the US Open Cup chapter of each season page -- `rsssf.org/tablesu/usa<YEAR>.html` (2022 = `usa2022.html` ... 2026 = `usa2026.html`).
2. Cross-verify every round against one independent index (ussoccer.com / worldfootball.net / soccerway).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable --> `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (re-run on receipt -- failing any = returned incomplete)
- **Slice reproduction:** your rows = exactly the official ties with >=1 MLS club, per your declared round counts; auditor recomputes the rule -- mismatch = fail.
- **Bracket reproduction:** semifinalists, finalists and the champion per edition match the official record; every aet/pens tie carries its advancement NOTE.
- **2021-cancelled NOTE present.** **Boundary:** none of the 21 appendix rows returned; no dateless rows; no duplicates.
- **Names:** every MLS string in the 30-string table; new TEAM rows sourced.
- **Spot-audit:** one round per edition re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full gap-free span of this competition's audited slice (every tie involving a top-flight club of that season) running up to today, minus any appendix rows. Auditor diffs the entire slice against the research record; any missing official tie = written gap defect; the return stays open until filled or NOTE-explained.

## 6. RETURN PROTOCOL
Save as `USOC-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: slice + bracket recomputation --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake.

---

## APPENDIX -- DO NOT RETURN (already held; auditor dedupes against this exact list, 21 rows)

### US Open Cup -- held (21)
2024-05-07 | Atlanta United FC 3-0 Charlotte Independence
2024-05-07 | Houston Dynamo FC 3-3 Detroit City FC
2024-05-07 | FC Dallas 1-0 Memphis 901 FC
2024-05-07 | San Jose Earthquakes 1-0 Oakland Roots SC
2024-05-08 | Union Omaha 1-1 Sporting Kansas City
2024-05-08 | New Mexico United 4-2 Real Salt Lake
2024-05-08 | Seattle Sounders FC 2-2 Louisville City FC
2024-05-08 | Las Vegas Lights FC 1-3 Los Angeles FC
2024-05-21 | Charleston Battery 0-0 Atlanta United FC
2024-05-21 | Sporting Kansas City 4-0 FC Tulsa
2024-05-21 | Sacramento Republic FC 3-3 San Jose Earthquakes
2024-05-21 | Los Angeles FC 3-0 Loudoun United FC
2024-05-22 | Tampa Bay Rowdies 1-2 FC Dallas
2024-05-22 | Seattle Sounders FC 2-1 Phoenix Rising FC
2024-07-09 | Atlanta United FC 1-2 Indy Eleven
2024-07-10 | Sacramento Republic FC 1-2 Seattle Sounders FC
2024-07-10 | Sporting Kansas City 1-1 FC Dallas
2024-07-10 | Los Angeles FC 3-1 New Mexico United
2024-08-27 | Sporting Kansas City 2-0 Indy Eleven
2024-08-28 | Seattle Sounders FC 0-1 Los Angeles FC
2024-09-25 | Los Angeles FC 1-1 Sporting Kansas City