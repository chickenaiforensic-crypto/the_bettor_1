# WORK ORDER — UEFA FULL 2021-2026 (researcher commission WO-UEFA-FULL-02) — ENTIRE COMPETITIONS

**Issued:** 2026-08-05 continued — after Researcher 2 delivered connector fix 0 dup 1390 matches shared tieId UCL-2122-QF-CHE-REA md5 35ca08f70da0bee77258c6b9ab5355dc — thank you for fix, but work not finished — entire UEFA data still needed per owner directive 2026-08-05 evening  
**Status:** QUEUED — position 18 (new, after #17 connector) — parallel allowed, researcher may run in parallel, owner decree — auditor approvals remain one card per return in queue order  
**Why:** Owner: "researcher 2 needs to gather the entire UFA champions league data europa data etc" — previous workorder #17 UEFA-CONNECTOR was SCOPED to ties with ≥1 programme-league club (ENG/RUS/CZE/SPA/ITA/GER/FRA) — 1390 rows — useful for league pivot s[L] fit but NOT entire competitions. For cross-league weighting real-world accuracy + evidence graph enrichment + future full European ratings, we need ENTIRE UCL + UEL + UECL + qualifiers 2021-22..2025-26 + 2026-27 played up to return date — every match, not just connector. This is the full fuel for league-strength bridge and for future unified European ratings (SOT open item 5 proposed not approved — needs full Euro data).

**Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` — never zip, never paste fragments) — same grammar as connector, but scope = entire competitions, not filtered. App's grammar already accepts these competitions (`uefa-cl`, `uefa-el`, `uefa-uecl` — verified in loader's COMP_TYPES L737) — no app change needed to ingest.

---

## 0. READ FIRST — Federation Check vs Connector Scope

Previous workorder #17 was **connector** — ≥1 programme-league club per tie — you did 1390 rows 689 UCL 437 UEL 264 UECL 99 TEAM 4 SOURCE 61 NOTE 0 dup after fix — PASS thank you. **This workorder #18 is FULL** — every match of all three competitions + qualifiers, regardless of programme-league involvement — e.g., Real Madrid vs Man City (both non-programme? Actually both programme? But even if both non-programme like Benfica vs Porto, still in-scope for FULL). Before returning, scan your own rows: any row that is domestic league/cup = wrong competition — stop. (First return attempt in programme history arrived as wrong country Rwanda instead of Russia — federation check in section 0 exists because of that.)

> **On file name (2021-2026):** this commission stands for full 5-year span running into today — seasons 2021-22 through 2025-26 complete, plus 2026-27 matches completed up to return date (state last round/date in NOTE). Approval certifies span gap-free for every club in entire competitions, not just programme clubs.

## 1. SCOPE — Which Matches, Exactly (FULL, Not Connector)

| Competition | compType (verbatim) | Seasons | In-scope rule FULL |
|---|---|---|---|
| UEFA Champions League (incl. qualifying rounds) | `uefa-cl` | 2021-22 .. 2025-26 + 2026-27 played | **EVERY tie** of competition — group/league phase + knockouts + qualifiers — all matches |
| UEFA Europa League (incl. qualifying rounds) | `uefa-el` | same | **EVERY tie** |
| UEFA Conference League (incl. qualifying rounds) | `uefa-uecl` | same (from 2021-22) | **EVERY tie** |

- Both legs of two-leg ties have both legs with shared tieId (e.g., `UCL-2122-R16-ARS-PSG`) — mandatory per Z-003 hold lesson — single-leg ties (league phase, finals) tieId may be empty.
- Not in this order: UEFA Super Cup, Youth League, women's, friendlies.
- Expected shape (planning estimate, NOT a gate — gates are §5): 
  - UCL per season: qualifiers ~80-100 matches + group/league phase: 2021-24 group 6 rounds ×16 ties=96, 2024-25 league phase 8 rounds ×18 ties=144, 2025-26 similar 144 + knockouts R16 16 + QF 8 + SF 4 + Final 1 ≈ 30 + qualifiers — ~200-250 per season ×5 = 1000-1250
  - UEL similar ~200 per season ×5 = 1000
  - UECL ~200 per season ×5 = 1000
  - **Total ~3000-3500 rows** for five full seasons for all three competitions — your ledger states exact counts, auditor recomputes structurally.
- Programme-league clubs expected: English clubs all seasons, Russian 2021-22 only (UEFA participant lists — if Russian appears later, record NOTE|info|unexpected_participant, do not drop, do not invent), Czech, Spanish, Italian, German, French all seasons.
- Russian clubs European matches expected 2021-22 only — if later appears, record NOTE|info|unexpected_participant, do not drop, do not invent.

## 2. GRAMMAR (loader strict — match existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<roundLeg>|<stadium>|<city>|<country>|<tieId>|<sourceLabel>`
  - `<competition>` strings verbatim declared once in NOTE|info|catalog: `UEFA Champions League` · `UEFA Europa League` · `UEFA Conference League`
  - `<compType>`: `uefa-cl` / `uefa-el` / `uefa-uecl` (qualifying rounds keep competition's type)
  - `<roundLeg>`: stage + leg e.g., `Q2 leg1`, `League phase MD1`, `R16 leg2`, `QF leg1`, `Final`
  - `<tieId>`: both legs of two-leg tie share ONE tieId string e.g., `UCL-2122-R16-ARS-PSG` mandatory: per-leg distinct tieIds trigger app's Z-003 hold screen proven in programme — single-leg ties (league phase, finals) tieId may be empty
  - `<country>`: home side's country (store convention)
  - **90-minute doctrine:** any tie decided in extra time or penalties carries 90-minute score plus mandatory `NOTE|info|advancement` which side advanced how pens score — never after-ET score
  - **Neutral/relocated venues:** designated home side per official record stays home, stadium+city actual venue, every neutral/relocated match carries `NOTE|info|neutral_venue|<reason>` — engine rule no home advantage for neutral matches builder-side not yours
- `TEAM|<name>|<country>|<leagueName>|<leagueCode>|<aliases>|<stadium>|<city>|...` — only for clubs not already on roster — programme-league clubs exist from league packs (use exact strings), every foreign opponent (e.g., PSG, Benfica, Shakhtar, Maccabi Tel Aviv, Young Boys) that appears and NOT on roster needs exactly one TEAM row — if programme club missing, stop and write `NOTE|warning|blocker` do NOT invent identity
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>` — one per source used, label primary/second/third index
- `NOTE|info|warning|<tag>|<text>` for every rename mapping, source conflict, postponement, AET/pens advancement, neutral venue, quirk
- End file with `END` — **No standings tables anywhere — rows only**

## 3. IDENTITY DISCIPLINE (No Duplicate Clubs)

- Programme-league clubs: use roster strings from league packs verbatim (e.g., Arsenal, Man City, Nott'm Forest, Sparta Prague, Slavia Prague, Viktoria Plzen, Slovacko, Zenit St Petersburg, CSKA Moscow, Atletico Madrid, Bayern Munich, Paris SG — pack strings govern)
- Foreign clubs: ONE identity per club across all three competitions and all seasons (e.g., never Benfica and SL Benfica, pick common form, keep other as alias in TEAM row)
- Rename/spelling traps: map silently to roster/your TEAM strings, NOTE each rule once (e.g., Nott'm Forest apostrophe, Maccabi Tel Aviv, Turkish/Austrian/Swiss/Scottish transliterations)

## 4. SOURCE HIERARCHY + VERIFICATION (Non-Negotiable)

**Concrete sources (use these, in this order):**

1. **Primary — RSSSF country archives European sections (#ec / European chapters on club's country page) + UEFA.com official archive (uefa.com/uefachampionsleague/history, uefaeuropaleague, uefaconferenceleague — season structure, dates, results):**
   - https://www.rsssf.org/tablese/eng2022.html … eng2026.html (England clubs European matches, in English year pages European sections)
   - https://www.rsssf.org/tablesr/rus2022.html (Russia — 2021-22 only expected)
   - https://www.rsssf.org/tablest/tsje2022.html … tsje2026.html (Czech clubs European matches)
   - https://www.rsssf.org/tabless/span2022.html / …/ital2022.html / …/duit2022.html / …/fran2022.html (Spain/Italy/Germany/France — RSSSF quirks span/ital/duit/fran not spa/ita/ger/fra) — each season's year page = season that ended in that year
   - https://www.uefa.com/uefachampionsleague/ (structure + dates + results authority)
   - **For FULL scope, also use UEFA.com full competition brackets per season, not just country sections — entire competition is needed, not just programme-league clubs.**
2. **Second index (independent) — Wikipedia season articles for UCL/UEL/UECL results matrices:**
   - https://en.wikipedia.org/wiki/2022–23_UEFA_Champions_League etc. per season per competition — knockout bracket + league/group phase results
3. **Third index — worldfootball.net per-round pages date-level anchors:**
   - https://www.worldfootball.net/all_matches/uefa-champions-league-2021-2022/ etc. per-season all-matches pages
4. Conflicts → resolve to RSSSF/UEFA + NOTE|warning|source_conflict with both values
5. Never guess. Anything unverifiable → NOTE|warning|blocker not a row

**RSSSF per-club/per-competition alternatives if season page lacks European chapter:** individual club pages or tablesu/ UEFA pages — if page missing, record NOTE|info|source_gap and use second/third index for that tie — do not leave hole unlabelled

## 5. ACCEPTANCE GATES (Auditor Re-Runs Everything on Receipt — Failing Any = Returned Incomplete)

- **Participation completeness FULL:** every club's European match list for 2021-22..2025-26 complete against official participant lists per competition (a club that qualified has every match of every phase it played — league phase, knockouts, qualifiers — present, club absent from phase it played = gap defect) — for FULL scope, this means all clubs in competition, not just programme leagues.
- **Structure:** per-competition round/phase counts reproduce official format for each season (e.g., UCL league phase 2024-25 8 rounds ×18 ties=144, group stage 2021-24 6 rounds ×16 ties=96 per season), two-leg ties both legs with shared tieId, single-leg ties flagged as such.
- **90-min doctrine:** every AET/pens tie carries 90' score + advancement NOTE (auditor checks against RSSSF/uefa prints and official scorelines).
- **Boundary:** no dateless rows, no future-dated rows at return, no duplicates (date+home+away+competition fingerprint) — previous defect Real Madrid-Chelsea duplicate fingerprint fixed in connector — 0 dup required for FULL.
- **Names:** every home/away string resolves to roster or TEAM rows, zero split identities.
- **Independent cross-diff (auditor-side):** return diffed against in-repo 4,244-row European index (football-data/openfootball lineage) for scores/sides + expanded Euro index for FULL.
- **Spot-audit trail:** one European matchweek per season re-listed in NOTE with source URL.

## 5.1 CONTINUITY CLAUSE (Owner Decree 2026-08-02)

This return is full gap-free span of entire European competitions 2021-22 → today. After gates pass, auditor diffs whole span against research record: any official in-scope tie stored nowhere = written gap defect, return stays open until filled or NOTE-explained (e.g., postponed/abandoned tie).

## 6. RETURN PROTOCOL

Save as `UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt`, hand to owner (repo folder `handoffs/` — or chat as .txt). Auditor drill: participation completeness FULL → structure → 90-min → boundary/dedupe → name resolution → legacy cross-diff → one staged approval card → commit through app's own intake.

**If you are Researcher 2 (who did connector 1390 0 dup fix md5 35ca08f70da0bee77258c6b9ab5355dc):** Thank you for fix — 0 dup — ready for S5 league pivot — but work not finished — connector was scoped to ≥1 programme-league club, FULL is entire competitions regardless of programme involvement. Previous thank you was for defect fix, not for finishing European work — to avoid relax, this new workorder #18 FULL is next. Keep on task — entire UEFA data still needed per owner directive "gather the entire UFA champions league data europa data etc" — connector 1390 was step 1, FULL ~3000-3500 is step 2.

**Why this matters (so work meaningful):** Connector 1390 gave us programme-club vs others Euro results for league pivot s[L] bias loop — improvement +6.72% MSE better on last hidden window 35 matches. FULL ~3000-3500 gives us entire Euro universe — all clubs, all phases — for evidence graph enrichment (H2H, common opponents, opponent-of-opponent) + for future unified European ratings (SOT open item 5 proposed not approved — needs full Euro data, not just connector). No FULL rows = limited bridge, with FULL rows cross-league fixtures even between non-programme clubs can be evidenced and eventually rated.

**Owner directive evening 2026-08-05:** entire UEFA data needed — not just connector — to avoid relax after thank you.

---

*File path: Supervior/Workorder/WORKORDER-UEFA-FULL-2021-2026-5YSPAN.md — this file — your commission for Researcher 2 next.*
