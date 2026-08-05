# WORK ORDER -- Scottish League Cup 5-year-span 2021-2026 up-to-today (researcher commission WO-SCOLC-SPAN-10)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 10 - research may run in parallel (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)

---

## 0. READ FIRST -- federation check
This is the **Scottish LEAGUE Cup** (Premier Sports Cup era name). It is **not** the Scottish FA Cup (WO-09), not England's EFL Cup. **Scan your finished rows: any club outside section 3 = wrong competition -- stop.**

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree, exactly as defined in `START-HERE.md`. Coverage mechanics per this workorder's section 1 (cutoff or appendix list). Approval certifies the span gap-free to today for this competition.

## 1. SCOPE -- the audited slice, proven on our held data
**Slice:** every tie of the League Cup in which **at least one participant is a Premiership club of that season** -- **including group-stage games**: non-European Premiership clubs play the July group stage; European-qualified Premiership clubs join at the knockout rounds (they receive byes -- record the bye situation in a NOTE, not as rows).
Editions: **2021-22, 2022-23, 2023-24, 2024-25, 2025-26** complete + **2026-27** through your return date (its group stage runs in July -- rows may exist already; cover through return date).
Roughly 30-45 ties per edition -- **declare round-by-round counts in a NOTE; the auditor recomputes the slice rule against the source.**
**Held appendix: none** (we hold zero League Cup rows).

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-league` (matches our existing cup rows)
  - Round identifiable per row in the venue-detail field (`R32`, `R16`, `QF`, `SF`, `Final`, `Group-B`, `R2` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. These cups are single-leg: every tie settled in extra time or on penalties records the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced`.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every format reading, rename mapping, source conflict, awarded tie.
- End the file with `END`. No standings tables anywhere -- rows only.
  - `<competition>` string, verbatim: `Scottish League Cup` (**new catalog string prescribed by this order**; declare it once in a `NOTE|info|catalog`)
- `TEAM` rows for lower-division opponents -- same rules as WO-09 section 2.

## 3. IDENTITY DISCIPLINE (no duplicate clubs)
Identical to WO-09 section 3: the WO-05 Premiership pool and per-season membership pins govern.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)
1. **RSSSF = primary:** the Cup Tournaments chapter of `rsssf.org/tabless/scot<YEAR>.html` (League Cup section).
2. One independent index (BBC Sport archive / worldfootball.net / soccerway).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess --> `NOTE|warning|blocker`.**

## 5. ACCEPTANCE GATES (re-run on receipt -- failing any = returned incomplete)
- **Slice reproduction:** ties with >=1 Premiership club incl. group stage, per your declared counts; auditor recomputes.
- **Bracket reproduction:** knockout qualifiers from the group stage + semifinalists/finalists/champion per edition match the official record; advancement NOTEs on every aet/pens tie.
- **Boundary:** no dateless rows; no duplicates.
- **Names:** as WO-09. **Spot-audit:** one round per edition with URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full gap-free span of this competition's audited slice (every tie involving a top-flight club of that season) running up to today, minus any appendix rows. Auditor diffs the entire slice against the research record; any missing official tie = written gap defect; the return stays open until filled or NOTE-explained.

## 6. RETURN PROTOCOL
Save as `SCOLC-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: slice + bracket recomputation --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake.
