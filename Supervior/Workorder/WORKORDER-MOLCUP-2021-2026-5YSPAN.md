# WORK ORDER — MOL Cup 5-year-span 2021–2026 up-to-today (segment commission: new rows 2021–24) (researcher commission WO-MOLCUP-BACKFILL-04)

**Issued:** 2026-08-02 · **Status:** STAGED — queue position ④, opens only after ① RPL league, ② CZ1 league and ③ Russian Cup returns pass their gates (owner's one-at-a-time decree) · **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` — never zip, never paste fragments)
**Why:** completes the Czech leg of the 5-year audit. We hold the MOL Cup 2024-25 + 2025-26 (31–32 rows/season, auditor-proven slice, see §1). This order closes 2021-22, 2022-23, 2023-24.

---

## 0. READ FIRST — federation check

This is the **CZECH MOL Cup** (Pohár FAČR, sponsored name): Sparta/Slavia/Plzeň and lower-league Czech opponents. It is **not** the Russian Cup (position ③), not Slovakia's cup, not any other country's. **Before returning: scan your rows — any club not Czech = wrong competition, stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021–2026):** this commission stands for the full **5-year span 2021-22 → running into today** of the decree. Your NEW rows still stop at the hard cutoff 2024-06-30 — seasons 2024-25 and 2025-26 are ALREADY held and auditor-verified (do not recollect a single one), and the current season fills weekly via the central-request system. You supply the missing segment; the APPROVAL certifies the whole span gap-free.
## 1. SCOPE — the proven slice, not guesses

**Our live coverage is auditor-proven to be exactly this rule:** every official MOL Cup match in which **at least one participant is one of that season's 16 First League clubs**, from the round where first-league clubs enter onward, through every round they reach. Single-leg ties; ties with no first-league club on the pitch are **out of scope** (verified: 0 such rows in 63 held rows). For calibration: the proven 2024-25 slice = 32 rows; 2025-26 = 31.

Your return reproduces this rule for seasons **2021-22, 2022-23, 2023-24**. Row counts follow the official bracket each year — **state round-by-round counts in a NOTE tied to the source page; the auditor recomputes the slice rule and your declared counts must match it exactly.**

**Hard cutoff: nothing dated 2024-06-30 or later.** All three finals (played in May) sit inside the window.
**Not in this order:** league matches (WO-02), relegation playoffs (already inside WO-02), CZ2 league matches, Europe.

## 2. GRAMMAR (our loader is strict — match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<competition>` verbatim: `MOL Cup`
  - `<compType>`: `domestic-league` (our existing 63 cup rows use this)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. Ties settled in extra time or on penalties record the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced (aet/pens)` — without it the bracket cannot be reconstructed.
  - Round identifiable per row in the venue-detail field: `R3` / `R16` / `QF` / `SF` / `Final`.
- `TEAM|<name>|Czech Republic|<leagueName>|<leagueCode>|<aliases>|<stadium>|<city>|<country>|<surface>|<capacity>|<founded>|<website>` — **allowed and expected for lower-league opponents** (CZ2/ČFL/MSFL clubs are legitimate cup participants). Every TEAM row carries sources; leagueCode = the club's code that season (`CZ2`/`CZ3` etc.).
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for stage readings, name mappings, source conflicts.
- End with `END`. No standings tables anywhere — rows only.

## 3. IDENTITY DISCIPLINE (no duplicate clubs)

The 16 First League clubs per season = the rosters pinned in `Supervisor/WORKORDER-CZ1-2021-2026-5YSPAN.md` §3 — **use those same strings** (`Zlin` all three years, era names only in NOTEs; `Ceske Budejovice`, `Slovacko`, `Bohemians 1905`…).
**Important correction to a league-order clause:** the WO-02 anti-appear list does **not** apply here — `Dukla Prague` played CZ2 in 2021–24 and is a legitimate MOL Cup opponent; the identity already exists on our roster, reuse it and NOTE its second-tier status that season. Same logic for any other club whose league code changed across the window.
**Lower-league opponents:** check our roster FIRST (25 CZ2 clubs already exist — Zizkov, Vyskov, Jihlava, Trinec, Chrudim, Opava, Taborsko, Usti nad Labem, Varnsdorf, Frydek-Mistek, Loko Praha, Kromeriz, Hlucin, Zapy, Horovice, Police nad Metuji, Uhersky Brod, Benatky nad Jizerou, Brozany, Domazlice, Horni Redice, Lanznot, Hlinsko, Karlovy Vary, Nove Sady, Petrin Plzen — do not re-declare). Only genuinely unknown clubs (typically ČFL/MSFL survivors) get TEAM rows.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF = primary:** the Cup chapter of each season page — `rsssf.org/tablest/tsje2022.html#cup`, `tsje2023.html#cup`, `tsje2024.html#cup` (scores AND dates, round by round).
2. Cross-verify every round against one independent index (worldfootball.net / soccerway / official facr.fotbal.cz archive).
3. Conflicts → resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable → `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (re-run on receipt — failing any = returned incomplete)

- **Slice reproduction:** your rows = exactly the official matches with ≥1 First-League club, per your declared round counts; auditor recomputes the rule from RSSSF — mismatch = fail.
- **Bracket reproduction:** semifinalists, finalists and the champion per season match the official record; every AET/pens tie carries its advancement NOTE.
- **Boundary:** no row ≥ 2024-06-30; no dateless rows; no duplicates inside the file.
- **Names:** every First-League club string ∈ pinned roster; known CZ2 clubs reuse existing identities; new TEAM rows sourced; no duplicate identities.
- **Spot-audit:** one round per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is one segment of a **gap-free 5-year span running up to today** (2021-07 onward → return date). The 5-year cap governs how far BACK we build — it is never permission for holes. After your rows pass the gates above, the auditor diffs the ENTIRE federation span — your rows + our held 2024-26 rows + current-season rows — against the full research record. Any official match inside the span that exists but is stored nowhere = a written gap defect; the return stays open until each gap is either filled or NOTE-explained (postponed/cancelled ties, etc.). The purpose of researching all data is exactly this: to prove our old data is missing nothing.

## 6. RETURN PROTOCOL

Save as `MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` — or chat as .txt). Auditor drill: boundary/dedupe vs live store → slice + bracket recompute → one staged approval card → commit through the app's own intake. The Czech leg then reads 5 full seasons + current, league AND cup.
