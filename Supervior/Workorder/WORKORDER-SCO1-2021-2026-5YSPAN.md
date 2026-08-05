# WORK ORDER -- Scottish Premiership 5-year-span 2021-2026 up-to-today (researcher commission WO-SCO-SPAN-05)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 5 - research may run in parallel with other commissions (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)
**Why:** the 5-year span decree, this league's leg. Our held coverage is the 2025-26 run-in only (29 rows -- appendix). This order delivers the complete league 2021-22 through 2025-26 plus 2026-27 to-date, minus the appendix rows.

---

## 0. READ FIRST -- federation check

This is the **SCOTTISH Premiership** (top flight of Scotland): Celtic, Rangers, Hearts, Hibernian... It is **not** the English Premier League, not the Scottish Championship (second tier), not the Scottish Cup or League Cup. **Before returning anything, scan your own rows: any club outside the section-3 pool = wrong competition -- stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree. Our held coverage in this competition is slate-scatter/run-in only (listed in the appendix), so unlike the RPL/CZ1 orders there is **no date cutoff** -- you cover the whole span and simply **must not return any appendix row** (they are already stored; the auditor dedupes against this exact list). You supply the span minus its held fragment; the APPROVAL certifies it gap-free to today.

## 1. SCOPE -- complete seasons only

| Competition | Seasons | Expected rows |
|---|---|---|
| Scottish Premiership -- regular stage (33 rounds) | 2021-22 ... 2025-26 | 198 per season |
| Scottish Premiership -- Championship Playoff + Relegation Playoff groups (post-split, 5 rounds each) | same | 30 per season |
| Whole season total | | **228 per season** |
| Scottish Premiership | 2026-27 through return date | state last round/date in a NOTE |

Structure proven in our sources: 12 clubs, 33 regular rounds, then the split -- top 6 play the Championship group, bottom 6 the Relegation group, 5 more matches each (38 per club, uniform).
**Minus:** the 29 appendix rows (already held -- the 2025-26 Hibernian run-in + bridge fixtures).
**Not in this order:** Scottish Cup, League Cup, Europe, friendlies.

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-league` (all rows, playoffs too -- matches our existing rows)
  - Round/stage identifiable per row in the venue-detail field (`RS R17`, `QF leg2`, `Group-A R3`, `Relegation-Round` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. Ties settled on penalties or in extra time record the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced` -- without it brackets cannot be reconstructed.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every reconciliation decision, rename mapping, format reading, source conflict.
  - `<competition>` strings, verbatim: `Scottish Premiership` (regular stage) - `Scottish Premiership Championship Round` (top-6 group -- matches our held rows) - `Scottish Premiership Relegation Round` (bottom-6 group -- **new catalog string prescribed by this order**; declare it once in a `NOTE|info|catalog` so the taxonomy stays honest)
- `TEAM|<name>|Scotland|Scottish Premiership|SC0|<aliases>|...` -- **expected for Dundee United** (2021-23 and 2024-25 participant, not yet on our roster) and any other Premiership club missing from section 3's roster list. League code `SC0`. Full fields + sources.
- End the file with `END`. No standings tables anywhere -- rows only.

## 3. IDENTITY DISCIPLINE (no duplicate clubs) -- the 14-club pool

Already on our roster -- **do not re-declare, use these exact strings:**
`Aberdeen` - `Celtic` - `Dundee` - `Falkirk` - `Hearts` - `Hibernian` - `Kilmarnock` - `Livingston` - `Motherwell` - `Rangers` - `Ross County` - `St Johnstone` - `St Mirren`
**Expected new TEAM row:** `Dundee United`.

**Rename traps (map silently to our strings, NOTE each rule once):** Heart of Midlothian --> `Hearts` - Saint Mirren --> `St Mirren` - Saint Johnstone --> `St Johnstone` - Dundee United FC --> `Dundee United`.

**Per-season composition (pinned from RSSSF regular-stage tables):**
- **2021-22:** Celtic, Rangers, Hearts [P], Dundee United, Ross County, Motherwell, Hibernian, Livingston, Aberdeen, St Mirren, St Johnstone, Dundee [P]
- **2022-23:** minus Dundee (relegated), plus Kilmarnock [P]
- **2023-24:** minus Dundee United (relegated), plus Dundee [P]
- **2024-25:** minus Livingston (relegated), plus Dundee United [P]
- **2025-26:** minus St Johnstone, minus Ross County (relegated), plus Falkirk, plus Livingston [P]
- **2026-27:** same 12 as 2025-26 unless the source says otherwise -- NOTE it.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF round-by-round + final tables = primary:** `rsssf.org/tabless/scot<YEAR>.html` (2021-22 = `scot2022.html` ... 2025-26 = `scot2026.html`; 2026-27 = `scot2027.html`) -- each page carries Regular Stage, Championship Playoff AND Relegation Playoff sections. Returning only the regular stage = 198/228 and a failed gate.
2. Cross-verify every round against one independent index (worldfootball.net / soccerway / BBC Sport archive).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`. Postponed rounds (e.g. the September-2022 postponements) are filed under their PLAYED date, with the original round in the venue-detail field and a NOTE if needed.
4. **Never guess. Anything unverifiable --> `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (we re-run all of these on receipt -- failing any = returned incomplete)

- **Table reproduction:** recomputed from your rows alone, each season's **regular-stage table must reproduce the official table 12/12 clubs** -- position-order W-D-L, GF-GA. Both post-split group tables must likewise reproduce 6/6 each.
- **Shape:** per completed season -- 228 rows; every club exactly 33 regular + 5 group matches; promotion/relegation movement consistent with the section-3 lines (any extra/missing club = wrong year or wrong tier).
- **Boundary:** none of the 29 appendix rows returned; no dateless rows; no duplicates.
- **Names:** every home/away string in the pool above (+ your declared `Dundee United`); `Hearts` never "Heart of Midlothian" in a row.
- **Spot-audit trail:** one round per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full **gap-free 5-year span running up to today** for this competition (minus the appendix's already-held rows). After your rows pass the gates above, the auditor diffs the ENTIRE span -- your rows + our held rows -- against the full research record. Any official match inside the span stored nowhere = a written gap defect; the return stays open until each gap is filled or NOTE-explained (postponed/abandoned/awarded ties, etc.). The purpose of researching all data is exactly this: to prove our old data is missing nothing.
## 6. RETURN PROTOCOL

Save as `SCO1-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: recompute all five seasons (regular 12/12 + both groups 6/6) --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake. Scotland leg then reads **5 full seasons + current** -- and the Ross County / St Johnstone packs finally sit on real tables.

---

## APPENDIX -- DO NOT RETURN (already held; auditor dedupes against this exact list, 29 rows)

### Scottish Premiership -- held (19)
2026-02-14 | Hibernian 2-0 St Mirren
2026-02-22 | Celtic 1-2 Hibernian
2026-02-28 | Dundee 3-3 Hibernian
2026-03-14 | Hibernian 0-0 Livingston
2026-03-21 | Motherwell 0-0 Hibernian
2026-04-04 | Hibernian 3-0 Kilmarnock
2026-04-11 | Aberdeen 2-0 Hibernian
2026-04-11 | Hearts 3-1 Motherwell
2026-04-11 | Falkirk 3-6 Rangers
2026-04-26 | Hibernian 1-2 Hearts
2026-05-03 | Hibernian 1-2 Celtic
2026-05-09 | Falkirk 1-3 Hibernian
2026-05-10 | Celtic 3-1 Rangers
2026-05-13 | Rangers 1-2 Hibernian
2026-05-13 | Motherwell 2-3 Celtic
2026-05-13 | Hearts 3-0 Falkirk
2026-05-16 | Hibernian 0-1 Motherwell
2026-05-16 | Celtic 3-1 Hearts
2026-05-16 | Falkirk 2-5 Rangers
### Scottish Premiership Championship Round -- held (10)
2026-04-26 | Hibernian 1-2 Hearts
2026-05-03 | Hibernian 1-2 Celtic
2026-05-09 | Falkirk 1-3 Hibernian
2026-05-10 | Celtic 3-1 Rangers
2026-05-13 | Rangers 1-2 Hibernian
2026-05-13 | Motherwell 2-3 Celtic
2026-05-13 | Hearts 3-0 Falkirk
2026-05-16 | Hibernian 0-1 Motherwell
2026-05-16 | Celtic 3-1 Hearts
2026-05-16 | Falkirk 2-5 Rangers
