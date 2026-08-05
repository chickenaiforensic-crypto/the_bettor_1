# WORK ORDER -- Kosovo Superliga 5-year-span 2021-2026 up-to-today (researcher commission WO-KOS-SPAN-06)

**Issued:** 2026-08-02 - **Status:** STAGED -- queue position 6 - research may run in parallel with other commissions (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)
**Why:** the 5-year span decree, this league's leg. Our held coverage is the 2025-26 Malisheva run-in only (12 rows -- appendix). This order delivers the complete league 2021-22 through 2025-26, minus the appendix rows (Kosovo 2026-27 starts mid-August -- if it has begun by your return date, include it and state in a NOTE).

---

## 0. READ FIRST -- federation check

This is the **Superliga of KOSOVO** (Football Federation of Kosovo top flight): Ballkani, Drita, Prishtina, Malisheva... It is **not** Albania's Kategoria Superiore (name collision -- Albania's top flight is also called "Superliga"), not Serbia's SuperLiga. **Before returning anything, scan your own rows: any club outside the section-3 pool = wrong competition -- stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree. Our held coverage in this competition is slate-scatter/run-in only (listed in the appendix), so unlike the RPL/CZ1 orders there is **no date cutoff** -- you cover the whole span and simply **must not return any appendix row** (they are already stored; the auditor dedupes against this exact list). You supply the span minus its held fragment; the APPROVAL certifies it gap-free to today.

## 1. SCOPE -- complete seasons only

| Competition | Seasons | Expected rows |
|---|---|---|
| Kosovo Superliga | 2021-22 ... 2025-26 | 180 per season = **900** |
| Promotion/Relegation playoff (only where the season used it) | same window | ~1-2 per season -- state count in a NOTE |

Structure proven in our sources: 10 clubs, quadruple round-robin, 36 rounds, every club exactly 36 matches.
**Minus:** the 12 appendix rows (already held).
**Awarded/abandoned-match rule (this league has them):** the score that governs the official final table goes in the row -- e.g. an abandoned-at-1-1 later awarded 0-3 is returned as 0-3 with a `NOTE|warning|awarded` carrying the on-pitch score and reason. A revoked award gets its own NOTE-chain. Never return the on-pitch score silently.
**Not in this order:** Kupa e Kosoves (cup), Liga e Pare (second tier), Europe, friendlies.

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<compType>`: `domestic-league` (all rows, playoffs too -- matches our existing rows)
  - Round/stage identifiable per row in the venue-detail field (`RS R17`, `QF leg2`, `Group-A R3`, `Relegation-Round` ...)
  - **90-minute doctrine, knockout-critical:** scoreline = the 90-minute score. Ties settled on penalties or in extra time record the 90-min result (draw if equal) PLUS a mandatory `NOTE|info|advancement|<tie>: <club> advanced` -- without it brackets cannot be reconstructed.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every reconciliation decision, rename mapping, format reading, source conflict.
  - `<competition>` strings, verbatim: `Kosovo Superliga` - `Kosovo Relegation Playoffs` (**new catalog string prescribed by this order** for the pro/rel playoff; declare it once in a `NOTE|info|catalog`)
- `TEAM|<name>|Kosovo|Kosovo Superliga|KOS|<aliases>|...` -- **expected for:** Ulpiana - Feronikeli - Trepça'89 - Fushë Kosova - Liria - Suhareka (all legitimate 2021-25 participants missing from our roster). Full fields + sources.
- End the file with `END`. No standings tables anywhere -- rows only.

## 3. IDENTITY DISCIPLINE (no duplicate clubs) -- the 16-club pool

Already on our roster -- **do not re-declare, use these exact strings:**
`KF Ballkani` - `Drita` - `Gjilani` - `Llapi` - `Prishtina` - `Drenica Skenderaj` - `Dukagjini` - `Malisheva` - `Ferizaj` - `Prishtina E Re`
**Expected new TEAM rows (section 2):** `Ulpiana` - `Feronikeli` - `Trepça'89` - `Fushë Kosova` - `Liria` - `Suhareka`.

**Rename/diacritic traps (map silently, NOTE each rule once):** Ballkani (Suharekë) --> `KF Ballkani` - Prishtina KF --> `Prishtina` - Drenica KF (Skenderaj) --> `Drenica Skenderaj` - source diacritics (Podujevë, Klinë, Suharekë...) never enter the club strings.

**Per-season composition (pinned from RSSSF final tables):**
- **2021-22:** Ballkani, Drita, Gjilani, Llapi, Prishtina, Drenica, Dukagjini [P], Malisheva [P], Ulpiana [P], Feronikeli
- **2022-23:** minus Ulpiana, minus Feronikeli (relegated), plus Ferizaj [P], plus Trepça'89 [P]
- **2023-24:** minus Drenica, minus Trepça'89, minus Ferizaj, plus Feronikeli [P], plus Fushë Kosova [P], plus Liria [P]
- **2024-25:** minus Fushë Kosova, minus Liria (relegated), plus Ferizaj [P], plus Suhareka [P]
- **2025-26:** minus Feronikeli, minus Suhareka (relegated), plus Drenica Skenderaj, plus Prishtina E Re
- Club counts: exactly 10 per season, every season -- no exceptions.

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF round-by-round + final tables = primary:** `rsssf.org/tablesk/kosovo<YEAR>.html` (2021-22 = `kosovo2022.html` ... 2025-26 = `kosovo2026.html`) -- full round grids plus the playoff chapter are on the same page.
2. Cross-verify every round against one independent index (worldfootball.net / soccerway / flashscore mirror).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`. The round grids in this league carry postponed-match quirks -- file by PLAYED date.
4. **Never guess. Anything unverifiable --> `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (we re-run all of these on receipt -- failing any = returned incomplete)

- **Table reproduction:** recomputed from your rows alone, each season's final table must reproduce the official table **10/10 clubs** -- position-order W-D-L and GF-GA. Awarded-match scores must be the governing versions or the tables cannot tie out.
- **Shape:** 180 league rows per season; every club exactly 36; 10 clubs per season matching the section-3 lines.
- **Boundary:** none of the 12 appendix rows returned; no dateless rows; no duplicates; playoff rows only where the season used them.
- **Names:** every home/away string in the 16-club pool (+ your declared new ones); no Albanian/Serbian league clubs anywhere.
- **Spot-audit trail:** one round per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full **gap-free 5-year span running up to today** for this competition (minus the appendix's already-held rows). After your rows pass the gates above, the auditor diffs the ENTIRE span -- your rows + our held rows -- against the full research record. Any official match inside the span stored nowhere = a written gap defect; the return stays open until each gap is filled or NOTE-explained (postponed/abandoned/awarded ties, etc.). The purpose of researching all data is exactly this: to prove our old data is missing nothing.
## 6. RETURN PROTOCOL

Save as `KOS-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: recompute all five tables 10/10 --> exclusion/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake. Kosovo leg then reads **5 full seasons + current** -- and Malisheva finally has real league tables behind its card.

---

## APPENDIX -- DO NOT RETURN (already held; auditor dedupes against this exact list, 12 rows)

### Kosovo Superliga -- held (12)
2026-03-09 | Malisheva 3-0 Prishtina
2026-03-22 | Malisheva 2-0 Llapi
2026-04-05 | Drita 2-0 Malisheva
2026-04-11 | Prishtina E Re 2-1 Malisheva
2026-04-19 | Malisheva 4-2 KF Ballkani
2026-04-26 | Dukagjini 0-1 Malisheva
2026-04-29 | Malisheva 3-1 Gjilani
2026-05-02 | Prishtina 0-1 Malisheva
2026-05-10 | Ferizaj 1-1 Malisheva
2026-05-17 | Malisheva 4-1 Drenica Skenderaj
2026-05-24 | Llapi 3-2 Malisheva
2026-05-31 | Malisheva 3-2 Drita
