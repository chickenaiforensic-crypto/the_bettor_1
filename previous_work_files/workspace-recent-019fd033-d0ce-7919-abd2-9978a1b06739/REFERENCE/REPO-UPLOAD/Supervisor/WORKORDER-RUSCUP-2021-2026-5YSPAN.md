# WORK ORDER — Russian Cup 5-year-span 2021–2026 up-to-today (segment commission: new rows 2021–24) (researcher commission WO-RUSCUP-BACKFILL-03)

**Issued:** 2026-08-02 · **Status:** STAGED — queue position ③, opens only after ① RPL league and ② CZ1 league returns pass their gates (owner's one-at-a-time decree) · **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` — never zip, never paste fragments)
**Why:** completes the Russia leg of the 5-year audit. We hold the Russian Cup 2024-25 + 2025-26 at 76 rows/season (auditor-proven slice, see §1). This order closes 2021-22, 2022-23, 2023-24.

---

## 0. READ FIRST — federation check

This is the **RUSSIAN Cup** (Cup of Russia, Fonbet-era branding irrelevant): Zenit, CSKA, Spartak, Krasnodar… It is **not** the Rwanda cup, not the Czech MOL Cup (that is its own order, position ④). **Before returning: scan your rows — any club not Russian = wrong competition, stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021–2026):** this commission stands for the full **5-year span 2021-22 → running into today** of the decree. Your NEW rows still stop at the hard cutoff 2024-06-30 — seasons 2024-25 and 2025-26 are ALREADY held and auditor-verified (do not recollect a single one), and the current season fills weekly via the central-request system. You supply the missing segment; the APPROVAL certifies the whole span gap-free.
## 1. SCOPE — the proven slice, not guesses

**Our live coverage is auditor-proven to be exactly this rule:** every official Russian Cup match in which **at least one participant is one of that season's 16 Premier League clubs**, followed through every round they reach — including after RPL-path clubs drop into the Regions path. Two-legged ties = two rows. Ties with no top-flight club on the pitch are **out of scope** (verified: 0 such rows in 152 held rows).

Your return reproduces this same rule for:

| Season | Format reality (verify against source, state in NOTE) |
|---|---|
| 2021-22 | **Old straight-knockout format** — RPL clubs enter at the later rounds; no group stage this season |
| 2022-23 | New format: RPL path group stage (4 groups × 4 clubs, 6 rounds) + two-legged bracket |
| 2023-24 | Same new format |

**Row counts are dictated by the official format each season — state your round-by-round counts in a NOTE tied to the source page. The auditor recomputes the slice rule against RSSSF and your declared counts must match it exactly.** (For calibration: the proven 2024-25 slice = 76 rows = 48 group + 28 bracket.)

**Hard cutoff: nothing dated 2024-06-30 or later.** Cup finals inside the window (May/June each year) ARE included.
**Not in this order:** Premier League matches (WO-01), Russian Super Cup, Europe, FNL league matches.

## 2. GRAMMAR (our loader is strict — match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<competition>` verbatim: `Russian Cup`
  - `<compType>`: `domestic-cup` (our existing 152 cup rows use this — corrected 2026-08-03, was wrongly `domestic-league`; see ERRATA-2026-08-03.md)
  - **90-minute doctrine, knockout-critical:** every scoreline is the 90-minute score. Ties decided in extra time or on penalties are recorded as the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced (aet/pens)` — without the advancement NOTE the bracket cannot be reconstructed.
  - Round identifiable per row: put the stage in the venue-detail field — `Group-A R3` / `QF leg2` / `Regions-R5` / `SF leg1` / `Final`.
- `TEAM|<name>|Russia|<leagueName>|<leagueCode>|<aliases>|<stadium>|<city>|<country>|<surface>|<capacity>|<founded>|<website>` — **allowed and expected for non-top-flight opponents** (FNL/lower clubs are legitimate participants). Every TEAM row carries sources; leagueCode = the club's code that season (`FNL` etc.).
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for each format reading, name mapping, source conflict.
- End with `END`. No standings tables anywhere — rows only.

## 3. IDENTITY DISCIPLINE (no duplicate clubs)

The 16 top-flight clubs per season = exactly the rosters pinned in `Supervisor/WORKORDER-RPL-2021-2026-5YSPAN.md` §3 — **use those same strings** (e.g. `Pari Nizhny Novgorod` across the whole window, era names only in NOTEs). FC Ufa and other folded clubs keep their WO-01 NOTE context.
**Rename traps inherited:** Nizhny Novgorod → Pari NN (2022); any cup-era sponsor suffixes map silently to roster strings.
**Lower-league opponents:** check our roster FIRST (Shinnik, Tyumen, Ural, Arsenal Tula, Torpedo, Neftekhimik, KamAZ already exist — do not re-declare). Only genuinely unknown clubs get TEAM rows.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF = primary:** the Cup chapter of each season page — `rsssf.org/tablesr/rus2022.html`, `rus2023.html`, `rus2024.html` (scores AND dates, group tables and bracket).
2. Cross-verify every round against one independent index (soccerway / worldfootball / flashscore mirror).
3. Conflicts → resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable → `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (re-run on receipt — failing any = returned incomplete)

- **Slice reproduction:** your rows = exactly the official matches with ≥1 top-flight club, per your declared round-by-round counts; auditor recomputes the rule from RSSSF — mismatch = fail.
- **Group tables 2022-23 + 2023-24:** recomputed from your rows, all 4 groups per season reproduce official standings club-for-club.
- **Bracket reproduction:** semifinalists, finalists and the champion per season match the official record; every AET/pens tie carries its advancement NOTE.
- **Boundary:** no row ≥ 2024-06-30; no dateless rows; no duplicates (two-legged ties = exactly two rows).
- **Names:** every top-flight club string ∈ pinned roster; no duplicate identities; new TEAM rows sourced.
- **Spot-audit:** one round per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is one segment of a **gap-free 5-year span running up to today** (2021-07 onward → return date). The 5-year cap governs how far BACK we build — it is never permission for holes. After your rows pass the gates above, the auditor diffs the ENTIRE federation span — your rows + our held 2024-26 rows + current-season rows — against the full research record. Any official match inside the span that exists but is stored nowhere = a written gap defect; the return stays open until each gap is either filled or NOTE-explained (postponed/cancelled ties, etc.). The purpose of researching all data is exactly this: to prove our old data is missing nothing.

## 6. RETURN PROTOCOL

Save as `RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` — or chat as .txt). Auditor drill: boundary/dedupe vs live store → slice + groups + bracket recompute → one staged approval card → commit through the app's own intake. The Russia leg then reads 5 full seasons + current, league AND cup.
