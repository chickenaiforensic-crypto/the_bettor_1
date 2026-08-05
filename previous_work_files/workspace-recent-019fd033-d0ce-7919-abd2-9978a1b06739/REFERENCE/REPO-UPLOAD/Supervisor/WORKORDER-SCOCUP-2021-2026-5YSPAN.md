# WORK ORDER -- Scottish Cup 5-year-span 2021-2026 up-to-today (researcher commission WO-SCOCUP-SPAN-09)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 9 - research may run in parallel (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)

---

## 0. READ FIRST -- federation check
This is the **national cup of SCOTLAND** (Scottish FA Cup -- the oldest). It is **not** the English FA Cup, not the League Cup (that is WO-10). **Scan your finished rows: any club outside section 3 = wrong competition -- stop.**

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree, exactly as defined in `START-HERE.md`. Coverage mechanics per this workorder's section 1 (cutoff or appendix list). Approval certifies the span gap-free to today for this competition.

## 1. SCOPE -- the audited slice, proven on our held data
**Slice (same family as Russian/MOL/US cups):** every tie of the Scottish Cup in which **at least one participant is a Premiership club of that season**, from the round Premiership clubs enter (the fourth round) to the final. All-lower-league ties are OUT.
Editions: **2021-22, 2022-23, 2023-24, 2024-25, 2025-26** complete + **2026-27** through your return date (its Premiership-round ties start in January -- likely none yet; NOTE).
Roughly 20-30 ties per edition -- **declare round-by-round counts in a NOTE; the auditor recomputes the slice rule against the source.**
**Held appendix: none** (we hold zero Scottish Cup rows).

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-cup` (matches our existing cup rows — corrected 2026-08-03, was wrongly `domestic-league`; see ERRATA-2026-08-03.md)
  - Round identifiable per row in the venue-detail field (`R32`, `R16`, `QF`, `SF`, `Final`, `Group-B`, `R2` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. These cups are single-leg: every tie settled in extra time or on penalties records the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced`.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every format reading, rename mapping, source conflict, awarded tie.
- End the file with `END`. No standings tables anywhere -- rows only.
  - `<competition>` string, verbatim: `Scottish Cup` (**new catalog string prescribed by this order**; declare it once in a `NOTE|info|catalog`)
- `TEAM|<name>|Scotland|<leagueName>|<leagueCode>|...` -- **allowed and expected for lower-division cup opponents** (Championship/League One/lower clubs; leagueCode = the club's tier code that season e.g. SC1/SC2 -- copy the pattern from existing identities).

## 3. IDENTITY DISCIPLINE (no duplicate clubs)
**Premiership clubs:** the 14-club pool in `Supervisor/WORKORDER-SCO1-2021-2026-5YSPAN.md` section 3 applies verbatim (including the rename traps: Saint Mirren --> `St Mirren`, Heart of Midlothian --> `Hearts`...), with per-season top-flight membership exactly as pinned there.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)
1. **RSSSF = primary:** the Cup Tournaments chapter of each season page -- `rsssf.org/tabless/scot<YEAR>.html` (2021-22 = `scot2022.html` ... 2025-26 = `scot2026.html`; 2026-27 = `scot2027.html`).
2. Cross-verify every round against one independent index (BBC Sport archive / worldfootball.net / soccerway).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable --> `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (re-run on receipt -- failing any = returned incomplete)
- **Slice reproduction:** your rows = exactly the official ties with >=1 Premiership club since the entry round, per your declared counts; auditor recomputes.
- **Bracket reproduction:** semifinalists, finalists and the champion per edition match the official record; every aet/pens tie carries its advancement NOTE (replays, where an edition had them, are separate dated rows + NOTE).
- **Boundary:** no dateless rows; no duplicates.
- **Names:** Premiership strings in the WO-05 pool; lower-division TEAM rows sourced.
- **Spot-audit:** one round per edition re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full gap-free span of this competition's audited slice (every tie involving a top-flight club of that season) running up to today, minus any appendix rows. Auditor diffs the entire slice against the research record; any missing official tie = written gap defect; the return stays open until filled or NOTE-explained.

## 6. RETURN PROTOCOL
Save as `SCOCUP-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: slice + bracket recomputation --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake.
