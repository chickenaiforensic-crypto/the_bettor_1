# WORK ORDER — Czech First League 5-year-span 2021–2026 up-to-today (segment commission: new rows 2021–24) (researcher commission WO-CZ1-BACKFILL-02)

**Issued:** 2026-08-02 · **Status:** STAGED — opens only after WO-RPL-BACKFILL-01 passes its acceptance gates (owner's one-league-at-a-time decree) · **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` — never zip, never paste fragments)
**Why:** the 5-year data-quality cap. We hold 2024-25 + 2025-26 complete (276/276 each, auditor-verified 16/16 vs official tables) + 2026-27 in progress. This order closes 2021-22, 2022-23, 2023-24 — after it, Czechia = 5 full seasons + current.

---

## 0. READ FIRST — federation check

This league is the **CZECH First League** (Fortuna:Liga, Czech Republic): Sparta Prague, Slavia Prague, Viktoria Plzeň. It is **not** the Russian league (that was WO-RPL-BACKFILL-01), not Slovakia, not any other league. **Before returning anything, scan your own rows: if any club not listed in §3 appears, you are on the wrong competition — stop.** (The previous return attempt on the sister order arrived as the wrong country and the wrong document class. That failure is recorded; do not repeat it.)

> **On the file name (2021–2026):** this commission stands for the full **5-year span 2021-22 → running into today** of the decree. Your NEW rows still stop at the hard cutoff 2024-06-30 — seasons 2024-25 and 2025-26 are ALREADY held and auditor-verified (do not recollect a single one), and the current season fills weekly via the central-request system. You supply the missing segment; the APPROVAL certifies the whole span gap-free.
## 1. SCOPE — complete seasons only

| Competition | Seasons | Expected rows |
|---|---|---|
| Czech First League — regular stage | 2021-22, 2022-23, 2023-24 | 240 per season |
| Czech First League — playoff stage (Skupina o Titul 15 + Skupina o Záchranu 15 + Skupina o Evropu 6) | same | 36 per season |
| **Total league** | | **276 per season = 828** |
| Czech Relegation Playoffs (only where the season used them) | same window | state count in a NOTE |

The Czech split format is proven in our own verified data: 12 clubs end on 35 games (title+relegation groups), 2 on 34 (Europe-group finalists), 2 on 32 (semifinal losers). 240+15+15+6 = 276. Any season deviating from this shape needs an explaining NOTE or it fails the gate.

**Hard cutoff: nothing dated 2024-06-30 or later** (our coverage resumes at MD1 2024-25 = 2024-07-19; a single overlapping row = duplicated work and a failed gate).
**Not in this order:** MOL Cup 2021–24 (separate order, later), CZ2/friendlies/Europe.

## 2. GRAMMAR (our loader is strict — match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<competition>` strings, verbatim: `Czech First League` (regular stage AND all three playoff-stage groups) · `Czech Relegation Playoffs` (pro/rel ties only)
  - `<compType>`: `domestic-league`
  - 90-minute doctrine (league = full-time score; any extra-time playoff leg = 90-minute score recorded as draw + NOTE)
  - **Playoff-stage group of each row** must be identifiable — put it in the venue-detail field as `Titul`/`Zachranu`/`Evropu` if the pack grammar has no dedicated field, exactly like this: `MATCH|2022-04-09|Czech First League|domestic-league|Sigma Olomouc|2|1|Slovan Liberec|Evropu-SF|...`
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>` per §4.
- `NOTE|info\warning|<tag>|<text>` for every reconciliation decision, rename mapping, shape deviation (see §5).
- End the file with `END`.
- **No TEAM rows expected at all** — every participant is already on our roster (§3). If you believe a club is missing, stop and write `NOTE|warning|blocker`; do NOT invent an identity.

## 3. IDENTITY DISCIPLINE (no duplicate clubs) — 17 clubs, all already ours

Use these **exact strings** in home/away, for every season, regardless of era sponsor names:

`Banik Ostrava` · `Bohemians 1905` · `Ceske Budejovice` · `Hradec Kralove` · `Jablonec` · `Karvina` · `Mlada Boleslav` · `Pardubice` · `Sigma Olomouc` · `Slavia Prague` · `Slovacko` · `Slovan Liberec` · `Sparta Prague` · `Teplice` · `Viktoria Plzen` · `Zbrojovka Brno` · `Zlin`

**Clubs that must NOT appear in 2021–24 rows:** `Dukla Prague` (promoted 2024), `Artis Brno` (promoted 2026). Their appearance = wrong season or wrong competition — automatic rejection.

**Per-season composition (pinned from RSSSF regular tables):**
- **2021-22:** Slavia, Plzeň, Sparta, Slovácko, Ostrava, Hradec K., Ml. Boleslav, Liberec, Olomouc, Č. Budějovice, Zlín, Teplice, Jablonec, Bohemians, Pardubice, Karviná
- **2022-23:** same 16 minus **Karviná** (relegated), plus **Zbrojovka Brno** (promoted)
- **2023-24:** same 16 minus **Zbrojovka Brno** (relegated), **Karviná** back (promoted)

**Rename traps (RSSSF itself confirms them — map silently to our strings, NOTE each mapping once):**
- FC Fastav Zlín → FC Trinity Zlín (2022 rename) — always `Zlin`
- MFK OKD Karviná / MFK Karviná — always `Karvina`
- FK Jablonec 97 / FK Baumit Jablonec — always `Jablonec`
- SK Dynamo České Budějovice — always `Ceske Budejovice`
- FC Bohemians 1905 Praha — always `Bohemians 1905`
- 1. FC Slovácko — always `Slovacko`
- AC Sparta Praha / SK Slavia Praha / FC Viktoria Plzeň / FC Baník Ostrava / FC Hradec Králové / FK Mladá Boleslav / FC Slovan Liberec / SK Sigma Olomouc / FK Pardubice / FK Teplice / FC Zbrojovka Brno → the §3 strings

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF round-by-round archives = primary** for scores AND dates: `rsssf.org/tablest/tsje2022.html` · `tsje2023.html` · `tsje2024.html`. Each page carries **both** the Regular Stage and the Playoff Stage — returning only the regular stage = 240/276 and a failed gate.
2. Cross-verify every round listing against one more independent index (worldfootball.net / soccerway / fortunaliga.cz flashscore mirror).
3. Any score/date conflict → resolve to RSSSF, then record it in a `NOTE|warning|source_conflict`.
4. **Never guess. Anything unverifiable → `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (we re-run all of these on receipt — failing any = returned incomplete)

- **Table reproduction:** recomputed from your rows alone, each season's **regular-stage table must reproduce the official table 16/16 clubs** — position-order W-D-L and GF-GA (the three tables are pinned in §3 for you to self-check before returning). Playoff-stage group tables must likewise reproduce 6/6 (Titul), 6/6 (Záchranu) and the Evropu bracket results.
- **Shape:** per season — 276 league rows; game counts per club = 12×35, 2×34, 2×32; every club's regular-stage sum = 30.
- **Boundary:** no row dated ≥ 2024-06-30; no dateless rows; no duplicates inside the file (two-legged Evropu ties are two rows, not one).
- **Names:** every home/away string ∈ the 17 pinned strings; anti-appear list empty; era renames absent (they belong in NOTEs only).
- **Spot-audit trail:** one random matchday per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is one segment of a **gap-free 5-year span running up to today** (2021-07 onward → return date). The 5-year cap governs how far BACK we build — it is never permission for holes. After your rows pass the gates above, the auditor diffs the ENTIRE federation span — your rows + our held 2024-26 rows + current-season rows — against the full research record. Any official match inside the span that exists but is stored nowhere = a written gap defect; the return stays open until each gap is either filled or NOTE-explained (postponed/cancelled ties, etc.). The purpose of researching all data is exactly this: to prove our old data is missing nothing.

## 6. RETURN PROTOCOL

Save as `CZ1-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (not the app directly) — destination folder in the repo: `handoffs/`. The auditor then: recomputes all three seasons (regular 16/16 + group tables) → boundary/dupe scan vs the live store → owner reads one staged card and approves once. Logged, versioned, done — the Czech leg of the audit then reads **5 full seasons + current**.
