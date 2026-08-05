# WORK ORDER — UEFA CONNECTOR 2021-2026 (researcher commission WO-UEFA-CONNECTOR-01)

**Issued:** 2026-08-05 · **Status:** QUEUED — position 17 (research may run in parallel, owner decree 2026-08-02; auditor approvals remain one card per return in queue order)
**Why:** owner decree 2026-08-05 — the European competitions are major and important; the system needs **actual cross-league results** (back-end store rows) to fit league-strength weights ("bump the league until it matches") and to enrich the evidence graph for cross-league fixtures. Today the store holds ZERO European matches.
**Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` — never zip, never paste fragments). The app's grammar already accepts these competitions (`uefa-cl`, `uefa-el`, `uefa-uecl` — verified in the loader's COMP_TYPES); no app change is needed to ingest your file.

---

## 0. READ FIRST — federation check

This is **UEFA club competitions** (Europe-wide). **Before returning anything, scan your own rows: any row that is a domestic league/cup match = wrong competition — stop.** (The first return attempt in this programme arrived as the wrong country; that failure is on record.)

> **On the file name (2021-2026):** this commission stands for the full **5-year span running into today** — seasons 2021-22 through 2025-26 complete, plus 2026-27 matches completed up to your return date (state the last round/date in a NOTE). The APPROVAL certifies the span gap-free for every club in scope.

## 1. SCOPE — which matches, exactly

| Competition | compType (verbatim) | Seasons | In-scope rule |
|---|---|---|---|
| UEFA Champions League (incl. qualifying rounds) | `uefa-cl` | 2021-22 .. 2025-26 + 2026-27 played | every tie involving **at least one club from a programme league** (below) |
| UEFA Europa League (incl. qualifying rounds) | `uefa-el` | same | same |
| UEFA Conference League (incl. qualifying rounds) | `uefa-uecl` | same (from 2021-22) | same |

**Programme leagues (a club from any of these makes the tie in-scope):** England (EPL), Russia (RPL), Czech Republic (First League), Spain (La Liga), Italy (Serie A), Germany (Bundesliga), France (Ligue 1) — the leagues of the 5YSPAN programme.

- Both legs of a two-leg tie are in scope if the tie itself is in scope; group/league-phase rounds include every match of the phase the qualifying club played in.
- **Not in this order:** UEFA Super Cup, UEFA Youth League, women's competitions, club friendlies.
- **Expected shape (planning estimate, NOT a gate — the gates are §5):** roughly 450–550 in-scope ties per season across the three competitions + qualifiers → **≈2,000–2,500 rows** for the five full seasons. Your own ledger states the exact counts; the auditor recomputes them structurally.
- **Russian clubs:** European matches for Russian clubs are expected for **2021-22 only** (UEFA participant lists). If a Russian club appears in any later season's ties, that is new information — record it with a `NOTE|info|unexpected_participant`, do not drop it and do not invent it.

## 2. GRAMMAR (our loader is strict — match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<roundLeg>|<stadium>|<city>|<country>|<tieId>|<sourceLabel>`
  - `<competition>` strings, verbatim, declared once in a `NOTE|info|catalog`:
    `UEFA Champions League` · `UEFA Europa League` · `UEFA Conference League`
  - `<compType>`: `uefa-cl` / `uefa-el` / `uefa-uecl` (qualifying rounds keep their competition's type).
  - `<roundLeg>` (venue-detail field): the stage + leg, e.g. `Q2 leg1`, `League phase MD1`, `R16 leg2`, `QF leg1`, `Final`. This is also where the loader's duplicate-protection context lives — do not leave it blank.
  - `<tieId>`: **both legs of a two-leg tie share ONE tieId string** (e.g. `UCL-2122-R16-ARS-PSG`). This is mandatory: per-leg distinct tieIds trigger the app's Z-003 hold screen (proven in this programme). Single-leg ties (league phase, finals): tieId may be empty.
  - `<country>`: home side's country (store convention).
  - **90-minute doctrine:** any tie decided in extra time or on penalties carries the **90-minute score** plus a mandatory `NOTE|info|advancement` (which side advanced, how, pens score). Never the after-ET score.
  - **Neutral/relocated venues:** the designated home side per the official record stays home; stadium + city are the ACTUAL venue; every neutral/relocated match carries `NOTE|info|neutral_venue|<reason>`. (Engine rule: no home advantage for neutral matches — builder-side, not yours.)
- `TEAM|<name>|<country>|<leagueName>|<leagueCode>|<aliases>|<stadium>|<city>|...` — **only for clubs not already on our roster.** Programme-league clubs exist on the roster from their league packs (use those exact strings). Every foreign opponent (e.g. PSG, Benfica, Shakhtar, Maccabi Tel Aviv, Young Boys) that appears in your rows and is NOT on the roster needs exactly one TEAM row. If you believe a programme club is missing, stop and write `NOTE|warning|blocker`; do NOT invent an identity.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>` — one per source used; label the primary/second/third index.
- `NOTE|info|warning|<tag>|<text>` for every rename mapping, source conflict, postponement, AET/pens advancement, neutral venue, quirk.
- End the file with `END`. **No standings tables anywhere — rows only.**

## 3. IDENTITY DISCIPLINE (no duplicate clubs)

- Programme-league clubs: use the roster strings from their league packs verbatim (e.g. `Arsenal`, `Man City`, `Nott'm Forest`, `Sparta Prague`, `Slavia Prague`, `Viktoria Plzen`, `Slovacko`, `Zenit St Petersburg`, `CSKA Moscow`, `Atletico Madrid`, `Bayern Munich`, `Paris SG` — pack strings govern).
- Foreign clubs: ONE identity per club across all three competitions and all seasons (e.g. never `Benfica` and `SL Benfica`; pick the common form, keep the other as an alias in the TEAM row).
- Rename/spelling traps: map silently to the roster/your TEAM strings, NOTE each rule once (e.g. `Nott'm Forest` apostrophe form; `Maccabi Tel Aviv`; Turkish/Austrian/Swiss/Scottish transliterations).

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

**Concrete sources (use these, in this order):**

1. **Primary — RSSSF country archives, European sections** (`#ec` / European chapters on the club's country page) + **UEFA.com official archive** (uefa.com/uefachampionsleague/history, uefaeuropaleague, uefaconferenceleague — season structure, dates, results):
   - `https://www.rsssf.org/tablese/eng2022.html` … `eng2026.html` (England clubs' European matches, in the English year pages' European sections)
   - `https://www.rsssf.org/tablesr/rus2022.html` (Russia — 2021-22 only expected)
   - `https://www.rsssf.org/tablest/tsje2022.html` … `tsje2026.html` (Czech clubs' European matches)
   - `https://www.rsssf.org/tabless/span2022.html` / `…/ital2022.html` / `…/duit2022.html` / `…/fran2022.html` (Spain / Italy / Germany / France — the RSSSF file-name quirks are `span`/`ital`/`duit`/`fran`, not `spa`/`ita`/`ger`/`fra`); each season's year page = season that ended in that year.
   - `https://www.uefa.com/uefachampionsleague/` (structure + dates + results authority).
2. **Second index (independent) — Wikipedia season articles** for UCL/UEL/UECL (results matrices):
   - `https://en.wikipedia.org/wiki/2022–23_UEFA_Champions_League` etc. (per season, per competition — knockout bracket + league/group phase results)
3. **Third index — worldfootball.net per-round pages** (date-level anchors):
   - `https://www.worldfootball.net/all_matches/uefa-champions-league-2021-2022/` etc. (per-season all-matches pages)
4. Conflicts → resolve to RSSSF/UEFA + `NOTE|warning|source_conflict` with both values.
5. **Never guess. Anything unverifiable → `NOTE|warning|blocker`, not a row.**

**RSSSF per-club/per-competition alternatives if a season page lacks the European chapter:** the individual club pages (e.g. `rsssf.org` club-season archives) or the `tablesu/` UEFA pages. If a page is missing, record `NOTE|info|source_gap` and use the second/third index for that tie — do not leave a hole unlabelled.

## 5. ACCEPTANCE GATES (auditor re-runs everything on receipt — failing any = returned incomplete)

- **Participation completeness:** every programme-league club's European match list for 2021-22..2025-26 is complete against the official participant lists (a club that qualified for a competition has every match of every phase it played — league phase, knockouts, qualifiers — present; a club absent from a phase it played = gap defect).
- **Structure:** per-competition round/phase counts reproduce the official format for each season (e.g. UCL league phase = 8 rounds × 18 ties from 2024-25; group stage = 6 rounds × 16 ties 2021-24); two-leg ties have both legs with a shared tieId; single-leg ties flagged as such.
- **90-min doctrine:** every AET/pens tie carries the 90' score + advancement NOTE (auditor checks against RSSSF/uefa prints and the official scorelines).
- **Boundary:** no dateless rows; no future-dated rows at return; no duplicates (date+home+away+competition fingerprint).
- **Names:** every home/away string resolves to the roster or to your TEAM rows; zero split identities.
- **Independent cross-diff (auditor-side):** the return is diffed against the in-repo 4,244-row European index (football-data/openfootball lineage) for scores/sides; conflicts adjudicated vs RSSSF/UEFA.
- **Spot-audit trail:** one European matchweek per season re-listed in a NOTE with its source URL.

## 5.1 CONTINUITY CLAUSE (owner decree 2026-08-02)

This return is the full gap-free span of European participation 2021-22 → today for the programme clubs. After the gates pass, the auditor diffs the whole span against the research record: any official in-scope tie stored nowhere = written gap defect; the return stays open until filled or NOTE-explained (e.g. a postponed/abandoned tie).

## 6. RETURN PROTOCOL

Save as `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt`, hand to the owner (repo folder `handoffs/` — or chat as .txt). Auditor drill: participation completeness → structure → 90-min → boundary/dedupe → name resolution → legacy cross-diff → one staged approval card → commit through the app's own intake.

**If you are a NEW researcher (second researcher, added 2026-08-05):** the repo also holds your orientation — `START-HERE-COLD-START.md` (reading order) and `Supervior/ROLES/ROLE-RESEARCHER.md` (your brief). You work the SAME grammar, gates and source hierarchy as the first researcher; each of you owns your assigned workorder numbers and returns them separately into `handoffs/`.

**Why this matters (so the work is meaningful to you):** these rows are the fuel for the league-strength bridge — the system measures how each league's teams actually perform against the others and weights the leagues until the predictions match the real results. No European rows = no bridge; with them, cross-league fixtures (e.g. Arsenal vs Dynamo Moscow) can eventually be rated on one scale instead of refused.
