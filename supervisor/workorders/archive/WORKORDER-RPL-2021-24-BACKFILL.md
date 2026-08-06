# WORK ORDER — Russian Premier League 2021–24 backfill (researcher commission WO-RPL-BACKFILL-01)

**Issued:** 2026-08-02 · **Approved:** owner (verbatim "approved") · **Format of return:** ONE `BP-TEAM-PACK v2` block (text file `.txt` or `.md` — never zip, never paste fragments)
**Why:** the 5-year data-quality cap. We hold 2024-25 + 2025-26 complete (240/240 each) + 2026-27 in progress. This order closes 2021-22, 2022-23, 2023-24 — after it, Russia = 5 full seasons + current.

---

## 1. SCOPE — complete seasons only

| Competition | Seasons | Expected rows |
|---|---|---|
| Russian Premier League (league matches) | 2021-22, 2022-23, 2023-24 | 240 per season = **720** |
| Russian Relegation Playoffs (only where the season used them) | same window | ~2 legs × seasons (state count in a NOTE) |

**Hard cutoff: nothing dated 2024-06-30 or later** (our coverage resumes at MD1 2024-25 = 2024-07-20; a single overlapping row = duplicated work and a failed gate).
**Not in this order:** Russian Cup 2021–24 (separate order, later), FNL/friendlies/Europe.

## 2. GRAMMAR (our loader is strict — match the existing packs exactly)

- `MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>`
  - `<competition>` strings, verbatim: `Russian Premier League` · `Russian Relegation Playoffs`
  - `<compType>`: `domestic-league` (playoffs too, as in our existing rows)
  - 90-minute doctrine (league = full-time score; playoffs = 90-minute score, shootouts as draws + NOTE)
- `TEAM|<name>|<country>|<leagueName>|<leagueCode>|<aliases>|<stadium>|<city>|<country>|<surface>|<capacity>|<founded>|<website>` — **only for clubs NOT on our roster** (see §3). League code `RPL` for top-flight seasons of such clubs.
- `SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>` per §4.
- `NOTE|info\warning|<tag>|<text>` for every reconciliation decision, date conflict, dissolve/rename context (see §5).
- End the file with `END`.

## 3. IDENTITY DISCIPLINE (no duplicate clubs)

Already on our roster — **do not re-declare, use these exact names:**
Zenit St Petersburg · FC Krasnodar · CSKA Moscow · Spartak Moscow · Dynamo Moscow · Lokomotiv Moscow · FC Rostov · Akhmat Grozny · Krylia Sovetov Samara · Rubin Kazan · FC Orenburg · Fakel Voronezh · Akron Tolyatti · Dynamo Makhachkala · Baltika Kaliningrad · Rodina Moscow · Pari Nizhny Novgorod · PFC Sochi · FC Khimki (dissolved after 2024-25 — keep identity, no new club) · Ural Yekaterinburg · Arsenal Tula · Torpedo Moscow.

**Known additions expected:** **FC Ufa** (2021-22; club folded summer 2022 — NOTE it) and any other 2021–24 participant missing above. New TEAM rows carry full fields + sources.
**Rename trap:** FC Nizhny Novgorod → **Pari Nizhny Novgorod** (2022 sponsorship rename — same club, same identity; put the old name in the alias list of the EXISTING identity if absent — check first, alias-only updates are allowed as NOTE-explained TEAM-row replacement only if our loader would otherwise duplicate).

## 4. SOURCE HIERARCHY + VERIFICATION (non-negotiable)

1. **RSSSF round-by-round archives = primary** for scores AND dates.
2. Cross-verify every round listing against one more independent index (soccerstats / worldfootball / ESPN / betexplorer).
3. Any score/date conflict → resolve to RSSSF, then record it in a `NOTE|warning|source_conflict`.
4. User-reported or single-source rows: only with a second confirming source, marked in NOTE.
5. **Never guess. Anything unverifiable → `NOTE|warning|blocker`, not a row.**

## 5. ACCEPTANCE GATES (we re-run all of these on receipt — failing any = returned incomplete)

- **Table reproduction:** recomputed from your rows alone, each season's final table must reproduce the official table **16/16 clubs** — position-order W-D-L and GF-GA. Zero tolerance; any deviation documented in your NOTE with the reason (e.g., deducted points kept as official total but record row unaltered).
- **Completeness:** 240 league rows per season, all 38 rounds dated; every club's season sum = 30 played.
- **Boundary:** no row dated ≥ 2024-06-30; no dateless rows; no duplicates inside the file.
- **Names:** every home/away string resolves to a roster identity (ours or your declared ones) — unknown names = the #1 cause of rejection.
- **80/20 split reproduction** is not needed here — instead: one random matchday per season re-listed in a NOTE with its source URL (spot-audit trail).

## 6. RETURN PROTOCOL

Save as `RPL-2021-24_BP-TEAM-PACK_v2.txt`, hand to the owner (not the app directly). The auditor then: recomputes all three tables 16/16 → boundary/dupe scan vs the live store (1,447 rows) → owner reads one staged card and approves once. Logged, versioned, done — Russia leg of the audit then reads **5 full seasons + current**.
