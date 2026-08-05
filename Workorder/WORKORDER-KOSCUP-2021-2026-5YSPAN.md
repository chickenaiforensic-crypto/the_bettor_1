# WORK ORDER -- Kosovo Cup 5-year-span 2021-2026 up-to-today (researcher commission WO-KOSCUP-SPAN-11)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 11 - research may run in parallel (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)

---

## 0. READ FIRST -- federation check
This is the **cup of KOSOVO** (Kupa e Kosoves). It is **not** Albania's Kupa e Shqiperise -- same collision family as the league order; **scan your finished rows: any club outside section 3 = wrong competition -- stop.**

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree, exactly as defined in `START-HERE.md`. Coverage mechanics per this workorder's section 1 (cutoff or appendix list). Approval certifies the span gap-free to today for this competition.

## 1. SCOPE -- the audited slice, proven on our held data
**Slice:** every cup tie in which **at least one participant is a Superliga club of that season**, from the round Superliga clubs enter to the final. All-lower ties are OUT.
Editions: **2021-22, 2022-23, 2023-24, 2024-25, 2025-26** complete + 2026-27 if started by your return date (NOTE).
Roughly 15-25 ties per edition -- **declare round-by-round counts in a NOTE; the auditor recomputes.**
**Held appendix: none.**

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-league` (matches our existing cup rows)
  - Round identifiable per row in the venue-detail field (`R32`, `R16`, `QF`, `SF`, `Final`, `Group-B`, `R2` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. These cups are single-leg: every tie settled in extra time or on penalties records the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced`.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every format reading, rename mapping, source conflict, awarded tie.
- End the file with `END`. No standings tables anywhere -- rows only.
  - `<competition>` string, verbatim: `Kosovo Cup` (**new catalog string prescribed by this order**; NOTE the source name "Kupa e Kosoves" maps to it)
- `TEAM|<name>|Kosovo|<leagueName>|<leagueCode>|...` -- expected for lower-division cup opponents.

## 3. IDENTITY DISCIPLINE (no duplicate clubs)
**Superliga clubs:** the 16-club pool in `Supervisor/WORKORDER-KOS-2021-2026-5YSPAN.md` section 3 applies verbatim, with per-season membership exactly as pinned there (10 clubs per season).

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)
1. **RSSSF = primary:** the Kupa chapter of `rsssf.org/tablesk/kosovo<YEAR>.html` (2021-22 = `kosovo2022.html` ... 2025-26 = `kosovo2026.html`).
2. One independent index (worldfootball.net / soccerway / flashscore mirror).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess --> `NOTE|warning|blocker`.**

## 5. ACCEPTANCE GATES (re-run on receipt -- failing any = returned incomplete)
- **Slice reproduction:** ties with >=1 Superliga club since the entry round, per your declared counts; auditor recomputes.
- **Bracket reproduction:** semifinalists, finalists and the champion per edition match the official record; advancement NOTEs complete.
- **Boundary:** no dateless rows; no duplicates.
- **Names:** Superliga strings in the WO-06 pool; no Albanian-cup clubs anywhere.
- **Spot-audit:** one round per edition with URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full gap-free span of this competition's audited slice (every tie involving a top-flight club of that season) running up to today, minus any appendix rows. Auditor diffs the entire slice against the research record; any missing official tie = written gap defect; the return stays open until filled or NOTE-explained.

## 6. RETURN PROTOCOL
Save as `KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: slice + bracket recomputation --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake.
