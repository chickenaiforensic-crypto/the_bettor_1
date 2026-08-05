# WORK ORDER -- Italy Serie A 5-year-span 2021-2026 up-to-today (researcher commission WO-ITA-SPAN-14)

**Issued:** 2026-08-03 - **Status:** STAGED -- queue position 14 - research may run in parallel (owner decree 2026-08-02); auditor approvals remain one card per return in queue order - **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` -- never zip, never paste fragments)
**Why:** owner decree 2026-08-03 -- the major European leagues join the 5-year-span programme. We hold ZERO league matches for this competition (its clubs exist on our roster only as pack identities). This order delivers the complete league, five full seasons plus the running one, up to today.

---

## 0. READ FIRST -- federation check

This is **Italy Serie A** (Italy). **Before returning anything, scan your own rows: any club outside the section-3 roster = wrong competition -- stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** of the decree. We hold no match rows for this league, so there is no cutoff and no appendix: you cover the whole span 2021-22 season through today. The APPROVAL certifies the span gap-free.

## 1. SCOPE -- complete seasons only

| Competition | Seasons | League rows |
|---|---|---|
| Italy Serie A | 2021-22, 2022-23, 2023-24, 2024-25, 2025-26 | 380 per season = **1,900** |
| Italy Serie A | 2026-27 through your return date | state last round/date in a NOTE |

20 clubs, 38 matchdays, every club exactly 38 matches -- steady all five seasons.
**Not in this order:** Coppa Italia, Europe, Serie B.

## 2. GRAMMAR (our loader is strict -- match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<competition>` string, verbatim: `Italy Serie A` (declare it once in a `NOTE|info|catalog`)
  - `<compType>`: `domestic-league`
  - Round number per row in the venue-detail field (`MD17` ...)
  - 90-minute doctrine (league matches = full-time score, always).
- `TEAM|<name>|Italy||ITA|...` -- **NOT expected:** every club of the 2021-26 window is already on our roster (section 3). If you believe one is missing, stop and write `NOTE|warning|blocker`; do NOT invent an identity.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>`.
- `NOTE|info\warning|<tag>|<text>` for every rename mapping, source conflict, quirk.
- End the file with `END`. No standings tables anywhere -- rows only.

## 3. IDENTITY DISCIPLINE (no duplicate clubs) -- existing roster, use verbatim

Every 2021-26 member club of this league already exists on our roster. Use these **exact strings** in home/away -- abbreviated sponsoress forms are our canonical names:

`Atalanta` `Bologna` `Cagliari` `Como` `Cremonese` `Empoli` `Fiorentina` `Frosinone` `Genoa` `Inter` `Juventus` `Lazio` `Lecce` `Milan` `Monza` `Napoli` `Parma` `Pisa` `Roma` `Salernitana` `Sampdoria` `Sassuolo` `Spezia` `Torino` `Udinese` `Venezia` `Verona`

**Rename/spelling traps (map silently to the roster strings, NOTE each rule once):** Inter (never Internazionale) - Milan (never AC Milan) - Verona (never Hellas) ...

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF round-by-round + final tables = primary:** `rsssf.org/tablesi/ital<YEAR>.html` (2021-22 season = the `...2022.html` page, through 2025-26 = `...2026.html`; 2026-27 = `...2027.html`).
2. Cross-verify every round against one independent index (worldfootball.net / soccerway / official league site archive).
3. Conflicts --> resolve to RSSSF + `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable --> `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (re-run on receipt -- failing any = returned incomplete)

- **Table reproduction:** recomputed from your rows alone, each season's final table must reproduce the official table **club-for-club, position-order W-D-L, GF-GA, pts** -- all 20 (Germany: 18). Zero tolerance.
- **Shape:** section-1 row counts per season; every club's match count = the full schedule length (38 -- Germany 34) per season it was a member.
- **Boundary:** no dateless rows; no duplicates; no rows for clubs outside their membership season (relegated clubs absent from the wrong year = fail).
- **Names:** every home/away string from the roster above, verbatim.
- **Spot-audit trail:** one matchday per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full gap-free span of this league 2021-22 -> today. After the gates pass, auditor diffs the entire span against the research record: any official match stored nowhere = written gap defect; the return stays open until filled or NOTE-explained (postponements, etc.).

## 6. RETURN PROTOCOL

Save as `ITA-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` -- or chat as .txt). Auditor drill: recompute all five tables --> boundary/dedupe scan --> span-diff --> one staged approval card --> commit through the app's own intake.
