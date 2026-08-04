# AUDIT — RPL 2021/22–2025/26 dataset

**Audit date:** 2026-08-02 · **Auditor pipeline:** `tools/assemble_validate.py` (output in
`audit/validation-report.txt`) + manual cross-verification against published official tables.
**Governing rule (client instruction):** never share unaudited data, never fabricate data.
Every figure in this repository traces to a fetched source; every anomaly is disclosed, none is silently repaired.

---

## 1. Provenance

| Item | Value |
|---|---|
| Data source (sole origin of every row) | `https://www.football-data.co.uk/new/RUS.csv` |
| Retrieved | **2026-08-02** (single audit session) |
| Source coverage | combined RPL file, 2012/13 → 2026/27 in progress; site index (football-data.co.uk/russia.php) shows the file refreshed 28 July 2026 |
| Licensing/usage | Source publishes its CSV feeds publicly for data analysis; rows are reproduced verbatim with attribution |
| Verification sources (comparison only, no data taken) | en.wikipedia.org `2021–22`…`2024–25 Russian Premier League` + table templates; tribuna.com/en/league/rpl/table/{season}; sportsmole.co.uk; betinf.com; 365scores.com; football.vpesports.com; sport-express.ru; sportbox.ru; championat.com — each claim cited inline below |

**Why this source.** The canonical football-data.co.uk per-season archives
(`mmz4281/<yy><yy>/RUS.csv`) return empty for recent RPL seasons — the author
removed RPL from the archive downloads. The combined `new/RUS.csv` is the same
author's live file and contains the identical schema for Russia. No other public
CSV source covers RPL results *plus* closing odds for all five seasons;

## 2. Fetch & assembly method (reproducible)

1. The fetching tool returns web pages in fixed ~8,000-byte slices (`chunkIndex`).
   `new/RUS.csv` = 51 slices (0–50); the five target seasons occupy slices **32–50**.
2. All 20 slices were read in order and stored byte-verbatim, then concatenated
   **without separators**. Slice boundaries may fall mid-record (observed:
   `Russia,Premie` + `r League`, `2.5` + `9,3.4,2.6`, `Russia,Premier L` + `eague`, …).
3. Records are re-assembled: every genuine record begins with `Russia,`; any line
   fragment not matching re-joins the previous record. One 12-byte leading fragment
   (tail of a 2020/2021 row from slice 31) was discarded and logged.
4. **Hard validation gate:** every re-assembled record must split into exactly **19
   fields**. All 1,275 records in slices 32–50 (incl. 2020/2021 and 2026/2027 rows)
   passed.
5. Season filter keeps `2021/2022 .. 2025/2026` (63 out-of-scope rows dropped: 55 ×
   2020/2021, 8 × 2026/2027). Boundary rows verified: first = 23/07/2021 FK Rostov
   0–2 Dynamo Moscow; last = 17/05/2026 Sochi 1–1 Akhmat Grozny.
6. Deliverable CSVs are written from the parsed records with the source's own header.
   **No field value is altered at any step.**

Automated checks (all PASS, see `audit/validation-report.txt`): exact row counts
244/244/244/240/240; 16 league teams × 30 matches each season (+2-match playoff
guests); no duplicate (date, home, away); chronology non-decreasing; `Res`
consistent with HG−AG on 1,212/1,212 rows; odds numeric-or-empty everywhere;
league-table cross-sums (ΣW = ΣL, W+D+L = 480, total points checksum) per season.

### Checksums (SHA-256)

| File | Rows | SHA-256 |
|---|---|---|
| `data/rpl/RPL-2021-22.csv` | 244 | `74b6b2518b2774edfd1601a7c5fe7b62b7fe74e51a171e9a3f486db026bf2948` |
| `data/rpl/RPL-2022-23.csv` | 244 | `31d7a5e2a20d2b596f7098ac6f47b4b6f9c6ca6f68bac08aa19c04b91c95d2d6` |
| `data/rpl/RPL-2023-24.csv` | 244 | `aa68b16ffbc97730712050b864d2d3f7129b9d0d67d7031fcbe6f0e5bae2d8f8` |
| `data/rpl/RPL-2024-25.csv` | 240 | `39cfc6a186ca521e93acfab56b7eb54f822886b4b5d70eb6f000d51f05f1601a` |
| `data/rpl/RPL-2025-26.csv` | 240 | `ddffa1be555b70599bae18b6597dbf5e3732b8c1d60643041b606686456b36b2` |
| `data/rpl/rpl_all_2021-2026.csv` | 1,212 | `bbf1935f60f431caf4febeaaa0c9e7c649e3947924aef6fc088d435e0d522f84` |

Raw fetch slices were working scratch only and were deleted after validation; the
deliverable CSVs *are* the byte-identical extraction, and the pipeline recreates
them from the live URL.

---

## 3. Cross-verification (computed tables vs official published tables)

Method: final league tables computed *solely from this dataset* (3-1-0; tiebreak —
points, head-to-head points, H2H GD, H2H goals, wins, GD, GF — matching the RPL
regulations chain; H2H-matches-won criterion collapses into the others in practice)
and compared row-by-row against independent published tables.

| Season | Champion (computed) | Official champion | Points | Table match |
|---|---|---|---|---|
| 2021/22 | Zenit (65) | Zenit ✓ | 16/16 rows: **identical** (P, W, D, L, GF, GA, Pts) | ✅ [Wikipedia table template; sportsmole; tribuna](https://en.wikipedia.org/wiki/Template:2021%E2%80%9322_Russian_Premier_League_table) |
| 2022/23 | Zenit (70) | Zenit ✓ | 14/16 rows identical; 2 rows differ **exactly as explained by A1** (awarded game) | ✅ [tribuna 2022/2023](https://tribuna.com/en/league/rpl/table/2022-2023/) + [Wikipedia season article](https://en.wikipedia.org/wiki/2022%E2%80%9323_Russian_Premier_League) |
| 2023/24 | Zenit (57) | Zenit ✓ | 14/16 rows identical; 2 rows differ by one goal **exactly as explained by A2** | ✅ [tribuna 2023/2024](https://tribuna.com/en/league/rpl/table/2023-2024/), betinf, [Wikipedia season article](https://en.wikipedia.org/wiki/2023%E2%80%9324_Russian_Premier_League) |
| 2024/25 | Krasnodar (67) | Krasnodar ✓ (1st title) | 16/16 rows: **identical** | ✅ [Wikipedia table template](https://en.wikipedia.org/wiki/Template:2024%E2%80%9325_Russian_Premier_League_table) |
| 2025/26 | Zenit (68) | Zenit ✓ | 16/16 rows: **identical** (incl. GD) | ✅ [365scores](https://www.365scores.com/en-us/football/league/premier-liga-89/standings), [vpesports](https://football.vpesports.com/leagues/rpl/) |

Goal-total cross-checks against official season statistics: 639 vs 639 (21/22) ✅;
729 vs 730 (22/23) — gap = exactly the A1 awarded-game accounting ✅; 636 vs 637
(23/24) — gap = exactly the A2 misrecorded goal ✅; 648 vs 648 (24/25) ✅.
Relegation/promotion movements between consecutive datasets match the historical
record (e.g., 22/23 direct relegations Khimki + Torpedo; newcomers Torpedo/Fakel/
Orenburg for 22/23; Baltika/Rubin for 23/24; Akron/Khimki/Dynamo Makhachkala for
24/25; Baltika/Sochi for 25/26).

---

## 4. Anomaly register (all kept **verbatim**, disclosed, explained)

### A1 — Awarded game recorded as the on-pitch result (2022/23)

* **Row:** `2022/2023, 19/03/2023, Pari NN, Torpedo Moscow, 1, 1, D` (and 0–0 H2H
  09/10/2022, which is unaffected).
* **Verdict:** the source records the *on-pitch* 1–1. The RFU later awarded
  Torpedo a **3–0 win** because Pari NN fielded the ineligible Yaroslav Mikhaylov.
  Official tables therefore list Torpedo 13 pts (W3, 22/61) and Pari NN 30 pts
  (33/50); this dataset — like football-data and most result feeds — keeps the
  played score, yielding 11 pts (2-5-23, 20/62) and 31 pts (8-7-15, 34/48).
  No standings position changes either way (Pari NN 13th, Torpedo 16th).
* **Evidence:** [Wikipedia 2022–23 RPL](https://en.wikipedia.org/wiki/2022%E2%80%9323_Russian_Premier_League)
  documents the 22/03/2023 RFU decision; [tribuna official-style table](https://tribuna.com/en/league/rpl/table/2022-2023/)
  carries the awarded figures. No ineligible-player cases affected any other row (goal-difference archaeology across all five seasons confirms — every other divergence would have shown in the table cross-checks above).

### A2 — One score misrecorded at source (2023/24)

* **Row:** `2023/2024, 14/08/2023, Pari NN, Akhmat Grozny, 1, 0, H`.
* **Verdict:** the actual official result was **2–0** (Sevikyan 1′, Suleymanov 38′)
  — confirmed by three independent match reports:
  [Sport-Express](https://www.sport-express.ru/football/rfpl/news/pari-nn-ahmat-rezultat-matcha-4-go-tura-rpl-14-avgusta-2023-goda-2112333/),
  [Sportbox](https://news.sportbox.ru/Vidy_sporta/Futbol/Russia/premier_league/spbnews_NI1931501_Pari_NN_obygral_Ahmat_i_oderzhal_pervuju_pobedu_v_tekushhem_sezone_RPL),
  [Championat](https://www.championat.com/football/_russiapl/tournament/5441/match/1101525/).
  The source's 1–0 is a simple transcription error. Points are unaffected (same
  winner); only GF/GA differ by one vs official columns (NN 28→29, Akhmat GA 44→45),
  which is precisely the single-goal gap between this dataset's season goal total
  (636) and the official 637. Kept verbatim because the mandate is verbatim source
  fidelity + disclosure, not silent correction.

### A3 — Relegation-playoff rows absent for 2024/25 (and 2025/26 to date)

* Source includes the two-legged RPL/FNL playoffs for 21/22, 22/23, 23/24 (hence
  244-row seasons) but the 24/25 block jumps from the final round (24/05/2025)
  straight to the 25/26 opener (18/07/2025); likewise no 25/26 playoff rows as of
  the 28/07/2026 file refresh. This is a source coverage gap, not deleted data.
* **What actually happened (from official reporting, season docs only — NOT added
  to the CSVs):** Akhmat beat Ural **3–2 on aggregate** and stayed up; Pari NN lost
  to Sochi but were **reprieved** when Khimki (12th) were denied a 2025/26 licence
  on 24/05/2025 and later dissolved; Orenburg, originally relegated, were
  reinstated 11/07/2025 after promoted First-League winners **Torpedo Moscow were
  excluded for attempted match-fixing**; Baltika (First League champions) and Sochi
  took the top-flight spots. Source: [Wikipedia 2024–25 RPL](https://en.wikipedia.org/wiki/2024%E2%80%9325_Russian_Premier_League)
  + Wikiwand mirror of the playoffs/notes sections. Consistency proof: the 2025/26
  roster in this dataset is exactly those 16 clubs.
* 2025/26 playoffs (13th Akron Togliatti, 14th Dynamo Makhachkala vs First League
  sides, ~late May 2026) are **outside** the regular-season data; outcomes not
  included anywhere in this deliverable.

### A4 — Odds-feed coverage pattern shifts inside 2025/26

* Round-1 rows carry all 12 odds but Max == Avg (single price source behind both).
* 25/07/2025 – 05/10/2025 (80 rows): only PSCH/PSCD/PSCA populated; MaxC*/AvgC* empty.
* 18/10/2025 – 27/10/2025 (24 rows): all 12 populated, Max == Avg on every row.
* From 31/10/2025 (136 rows): PSCH/D/A empty; only MaxC*/AvgC* (identical) populated.
* Interpretation: the site's RPL bookmaker panel collapsed during the season; the
  delivered cells are exactly what the source published. Season bucket counts:
  `full-12`: 24, `PSC-only`: 80, `MaxC/AvgC-only`: 136 (machine-counted).

### A5 — Truncated `MaxCA = 22` constant on 8 rows (01–03/05/2026)

Round-28 rows (Krylya–Spartak, Lokomotiv–Dynamo, Dynamo Makhachkala–FK Rostov,
Baltika–Rubin, CSKA–Zenit, Sochi–Orenburg, Akron–Krasnodar, Akhmat–Pari NN) carry
`MaxCA` literally equal to `22` where the matching `AvgCA` is ~11.7–12.9 — an
upstream feed glitch. Kept verbatim; treat `MaxCA` on those rows as unreliable
(`AvgCA` present and plausible; rounded `1×2` strategy users should use AvgC).

### Naming note (not an anomaly)

`Pari NN` ≡ FC Nizhny Novgorod (rebrand June 2022; source applies the new name
retroactively to 2021/22). `FK Rostov` ≡ Rostov. See DATA-DICTIONARY alias map.

---

## 5. What this dataset deliberately does **not** contain

* Half-time scores, match statistics, shots/corners/cards — not published for RPL.
* Over/Under, BTTS, Asian handicap odds — not published for RPL.
* Opening odds — source publishes closing odds only.
* The 2026/27 season (underway at retrieval date, out of scope).

Any consumer requiring these fields needs an additional source; do not synthesise
them from AvgCA percentages — that would violate the no-fabrication rule.

## 6. Reproduce

```bash
# requires the 20 raw slices in .rawchunks/ (re-fetchable slice-by-slice from the
# live URL) — then:
python3 tools/assemble_validate.py
```

The script rebuilds the CSVs, re-runs every check, and rewrites
`audit/validation-report.txt`. Exit code non-zero if any check fails.

---

## Addendum (2026-08-03) — Russian Cup pack (WO-RUSCUP-BACKFILL-03)

The repository now also carries the Russian Cup 2021-22 → 2023-24 return artifact
(`handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt`, BP-TEAM-PACK v2 grammar). Its audit
trail is separate and self-contained: every acceptance gate in the workorder (slice
counts per round, group-table recompute club-for-club, bracket reproduction through
the champions 2022 Spartak / 2023 CSKA / 2024 Zenit, 14 two-leg aggregates, boundary
< 2024-06-30, no dupes/dateless rows, identity discipline incl. per-club pivot
ledgers) is re-run by `tools/build_pack.py` and printed in `audit/pack-validation.txt`
(162 PASS / 0 FAIL). Dual source base: RSSSF cup chapters (rus2022/2023/2024, primary)
cross-checked match-for-match (189/189) against the Wikipedia season pages with linked
RFS match sheets (second index); three RSSSF-compact date defects resolved to its
detailed chapter and disclosed in the pack's `source_conflict` NOTE.

---

## Addendum (2026-08-03, second entry) — RPL league pack (WO-RPL-BACKFILL-01, 5YSPAN revision)

The Russian Premier League 2021-22 → 2023-24 return artifact
(`handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt`, BP-TEAM-PACK v2 grammar) carries 732
MATCH rows — (240 league + 4 relegation-playoff) per season × 3 — plus 3 TEAM rows
(FC Ufa RPL; Yenisey Krasnoyarsk and SKA Khabarovsk FNL), 13 SOURCE rows and 17 NOTE
rows (16 before the same-day errata below). Gates re-run on the pack text by
`tools/build_rpl_pack.py` and printed in
`audit/pack-validation-rpl.txt` (69 PASS / 0 FAIL after the errata): per-season 240+4 counts; all 30
matchdays × 8 fixtures dated; 48 club-season pivots = exactly 30 played each (owner
per-club technique); official final tables of all three seasons reproduced 16/16 —
position-order, W-D-L, GF-GA and points — against the RSSSF table constants in
`audit/ledger/rpl-venues.txt`; all seven equal-points table decisions reproduced from
recomputed mutual results (Lokomotiv>Dynamo 2022-23 decided at H2H away goals 4:3);
all six playoff aggregates and promotion/relegation outcomes; season goal totals
639/730/637 (= RSSSF stated totals and both Wikipedia infobox figures); boundary
< 2024-06-30 (last row 2024-06-01); no dupes/dateless; identity discipline.

Relationship to this audit's earlier anomaly register: **A1** (2023-03-19 Pari
NN–Torpedo) is stored in the pack as the RFU-awarded **0-3** — i.e. resolved the
opposite way from the CSV set (which keeps the on-pitch 1-1 verbatim) — because RSSSF,
the workorder's primary source, carries the award as the round-20 result and in the
final table; both readings are disclosed in the pack NOTEs (`source_conflict`). **A2**
(2023-08-14 Pari NN–Akhmat) is independently confirmed by RSSSF's round list: the
official 2-0 stands; the feed's 1-0 is the second conflict NOTE. Second-index
coverage: all 732 rows diffed match-for-match against the football-data feeds —
730/732 identical on date and score, the two documented variances aside. Venue fields
follow the documented home-ground policy (RSSSF stadium table 2021-22; season-article
venue tables 2022-23/2023-24) with explicitly sourced exceptions: Torpedo 2022-23
rounds 1-10 and the round-19 game at Arena Khimki (RSSSF NBs), and the playoff
grounds from the season-article match boxes (Lenin Stadium Khabarovsk, Futbol-Arena
Yenisey, Spartakovets Stadium, Kristall Stadium Zhigulevsk — the last two also
corroborated by FotMob/ESPN/Sofascore pages listed in the pack SOURCE block).

---

## Addendum (2026-08-03, third entry) — auditor errata ERRATA-2026-08-03 applied to both returns

The owner relayed the auditor's errata inline (the uploaded `ERRATA-2026-08-03.md` did
**not materialize in the sandbox** — checked repo root, `/home/user/uploads/` and the
`origin/main` tree; the corrected WORKORDER-RPL fingerprint `9903cf856877d173ba71d72cef64e9c6`
text is likewise absent — `origin/main` still carries the cb6e grammar line. A relayed
mirror is kept at `supervisor/ERRATA-2026-08-03.as-relayed.md`; the owner was asked to
re-upload the original).

Applied corrections (both packs rebuilt byte-deterministically by their builders, full
gate suites re-run the same day):

1. **compType classes** — `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt`: the 12 Russian
   Relegation Playoffs rows now carry compType `other` (league rows unchanged,
   `domestic-league`); every other field byte-identical to the cb6e return.
   `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt`: all 189 rows now `domestic-cup`.
   Registered for the remaining queue: MOLCUP/KOSCUP/SCOCUP/SCOLC/USOC = `domestic-cup`;
   future promotion/relegation-playoff rows = `other`.
2. **`TEAM|FC Ufa` added to the cup pack** — `TEAM|FC Ufa|Russia|Russian Premier
   League|RPL|Ufa;Ufa FC;Bashinformsvyaz-Dinamo Ufa|BetBoom Arena|Ufa|Russia||13573||`
   (anchored to its 2021-22 RPL elite-slot identity, capacity from the RSSSF rus2022.html
   #1l stadium table, same page as the cited cup chapter). RUSCUP pack now 22 TEAM rows.
3. **KAMAZ exact-form** — `KamAZ Naberezhnye Chelny` corrected to `KAMAZ Naberezhnye
   Chelny` in the cup pack rows/NOTEs (2 MATCH rows + 2 NOTEs), the builder constants and
   the primary ledger; zero remaining mixed-case occurrences repo-wide outside the owner's
   own workorder mirror (left verbatim).

Gate evidence after rebuild: RPL 69/69 (`audit/pack-validation-rpl.txt`, sha
`6e458e19…`), RUSCUP 162/162 (`audit/pack-validation.txt`, sha `18ba4695…` —
intermediate post-errata build; superseded by final `c2658b49…` after the auditor-return
KAMAZ exact-string cycle, see the sixth addendum below).

---

## Addendum (2026-08-03, fourth entry) — WO-CZ1-BACKFILL-02 returned (Czech First League 2021-22 → 2023-24)

`handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt`: 829 MATCH rows (276 + 276 + 277), 0 TEAM rows
(WO section-2 directive — every participant already on the client roster), 12 SOURCE rows,
21 NOTE rows (17 info incl. 3 `spot_audit`; 4 warning = `playoff_count`, `roster_scope`, 2 ×
`source_conflict`), `END`. compType `domestic-league` on every row verbatim per WO section-2
(Titul/Zachranu/Evropu stages are league championship phases, not separate events). Cutoff
honoured — last row the 2024-05-31 Conference League playoff Final; zero rows dated ≥ 2024-06-30.

**Structure reproduced per season:** 240 regular-stage rows = all 30 matchdays × 8 dated fixtures
(each of the 16 clubs exactly 30 played, pivot-gated); 15 Titul + 15 Zachranu group rows
(rounds 31-35 × 3 fixtures each); 6 Evropu play-off legs (two-legged SF ×2 + final), plus the
documented 2023-24 shape deviation: the single extra Conference League playoff Final
(2024-05-31 Mlada Boleslav 3-1 Hradec Kralove, Lokotrans Arena — the official record itself
counts the season as 277 league matches). Per-club game-count shapes: 2021-22/2022-23
{35×12, 34×2, 32×2}; 2023-24 {36×1, 35×12, 34×1, 32×2} — all enumerated in
`audit/pack-validation-cz1.txt` per-club pivots.

**Sourcing:** RSSSF `tablest/tsje2022|2023|2024.html` primary for dates AND scores (transcribed
to `audit/ledger/cz1-<season>.txt` on fetch day); second index = the English Wikipedia season
articles at full depth — 720 regular scores diffed cell-for-cell vs the FBR matrices, 90
group-stage scores vs the Titul/Zachranu matrices, 19 playoff legs vs the printed brackets, plus
official tables/venues; worldfootball.net matchday pages R10/R20/R25 as date+score spot-audits
(24/24 identical; one listed-date nuance documented). Adjudication: three wiki FBR cells
(2022-23 Liberec 2-1 Zlin R26, Plzen 4-0 Zlin R28; 2023-24 Pardubice 0-0 Jablonec R2) conflict
with RSSSF *and with the hosting article's own official table* — RSSSF lines re-fetched and
re-verified 2026-08-03 before resolving per WO section-4(3). Two wiki infobox goal scalars
(763/804) contradict their own articles' tables (770/792 recomputed) — recomputed anchors
carried, `source_conflict` NOTEs.

**Tables and ties:** official regular tables reproduced 16/16 per season from the pack rows
(position order + W-D-L + GF-GA + Pts vs independent wiki constants); group tables 6/6 per
season per group; all four regular-stage equal-points decisions reproduced from recomputed
mutual results (incl. the 2022-23 three-way at 35 pts); group-stage ties decided by the
documented class rule 'regular-season points, then regular-season H2H' — incl. the 2022-23 title:
Sparta over Slavia at 78-78 by regular points 68>66 (RSSSF NB + wiki class_rules).

**Held out, owner decision requested (`roster_scope` + `playoff_count` warnings):** the 12 Czech
promotion/relegation legs (2 ties × 2 legs × 3 seasons, all 'league side stays') involve FNL
clubs outside the 17 pinned section-3 strings while section-2 forbids TEAM rows — dates, scores,
venues and aggregates fully listed in NOTEs, emitted as 0 rows. If sanctioned with 5 TEAM
declarations they would carry compType `other` per ERRATA-2026-08-03 and append without touching
the 829 delivered rows.

**Venue/city per the documented home ground of the season** (wiki venue tables, second index):
Hradec 2021-22/2022-23 at Lokotrans Arena, Mlada Boleslav (rebuild; city follows location);
Pardubice 2021-22 at Dolicek, Prague, and 2022-23 split at the winter break Dolicek → CFIG
Arena; Hradec 2023-24 at the new Malsovicka Arena (first home game 2023-08-05 = opening);
era sponsor names per season. Gates: 105 PASS / 0 FAIL (`audit/pack-validation-cz1.txt`);
builder `tools/build_cz1_pack.py` byte-deterministic (pack sha256 `eee4686f…` — v2.1
829-row build; superseded by `55d9bd80…` after the pro/rel reinstatement in the sixth
addendum below).

## Addendum (2026-08-03, fifth entry) — WO-MOLCUP-BACKFILL-04 returned (Czech MOL Cup 2021-22 → 2023-24)

`handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt`: 120 MATCH rows (41 + 41 + 38 by the WO-§1
auditor-proven slice), 31 TEAM rows (the genuinely-unknown lower-league opponents; the 18
client-roster CZ2/lower strings + Dukla Prague reused, not re-declared), 15 SOURCE rows,
33 NOTE rows (incl. 20 `advancement`, 3 `spot_audit`; 2 `source_conflict` warnings), `END`.
compType `domestic-cup` on every row per standing ERRATA-2026-08-03 — **superseding this
workorder's §2 grammar line `domestic-league`**; the supersession is documented in the pack
`comp_class` NOTE with a flag that the 63 client-held cup rows presumably need the same
reclassing. Cutoff honoured — last row the 2024-05-22 Final; zero rows ≥ 2024-06-30.

**Slice reproduced:** every official tie from the round where First-League clubs enter onward
with ≥1 of that season's 16 pinned clubs: R2 11/28 + R3 15/16 + R16 8 + QF 4 + SF 2 + F 1 = 41
(2021-22); R2 11/27 + R3 15/16 + 8 + 4 + 2 + 1 = 41 (2022-23); R2 11/27 + R3 15/16 + R16 6 +
QF 3 + SF 2 + F 1 = **38** (2023-24 — TWO no-FL R16 ties excluded: Velvary 1-2 Opava and
**Dukla Prague 3-1 Vyskov**, Dukla being a CZ2 club in 2023-24). Round-by-round counts are
declared in the pack `slice`/`round_counts` NOTEs tied to the source pages; out-of-slice
exclusions itemized for the auditor's recompute in the `continuity` NOTE and the 2nd-idx ledgers.

**Sourcing & adjudication:** RSSSF `tsje2022|2023|2024.html#cup` primary — but it carries the
cup **from R16 onward only** (documented `source_adaptation`, not inferred); R2/R3 built from
the en.wiki bracket sections, every tie cross-verified against worldfootball.net round pages
(100% date+score agreement on all in- and out-of-scope ties), and all 24 R16 ties identical
across the three indexes. Two defects found and disclosed per WO §4(3): (1) **Slovacko 3-1
Karvina 2021-11-12 (R16) is silently aet in BOTH bracket sources** — the wf match report proves
1-1 at 90' (Jurečka 90', aet goals 105' pen + 108') — the row carries the 90-minute 1-1 +
advancement NOTE; (2) **Plzen–Zlin SF date**: RSSSF header [Apr 4] vs wiki box 2024-04-24 18:00
+ wf 24.04.2024 18:00 — two independent indexes agree, row carries 2024-04-24, RSSSF documented
in `source_conflict`. All 20 aet/pens in-slice ties carry 90-minute splits proven by wf
match-report goal timelines / wiki box goal minutes (register: `audit/ledger/molcup-venues-teams.txt`,
and every one has its mandatory `advancement` NOTE (gate G13/G14).

**MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt integrity:** builder `tools/build_molcup_pack.py`
byte-deterministic across rebuilds; pack sha256
`5023eb33fd7a63f51fbb95d0535a811bc8f9ddc9b5d1ff20dc49ee8e893cec86`; external gate mirror
`tools/validate_molcup_pack.py` → `audit/pack-validation-molcup.txt` — **30/30 PASS**
(slice reproduction, bracket reproduction incl. champions Slovacko/Slavia/Sparta, advancement
completeness, boundary, identity universe, venue-string consistency with the CZ1 pack for shared
FL grounds, per-team pivot ledgers per the owner decree). Identity/rename proofs archived:
SK Líšeň→SK Artis Brno rename (Brno press, Dec 2025; wf back-renames historically = documented
quirk), FK Loko Vltavín→FK Loko Praha rename June 2024 (roster string `Loko Praha` reused),
Hradec's wf label "FINEP Arena" = Malsovicka Arena working-name alias (pinned string used),
Vyšehrad CFL-A entry + corruption-scandal reassignment (leagueCode CZ3, 0 league matches).

---

## Addendum 2026-08-03 (sixth) — auditor return cycle: CZ1 pro/rel block reinstated + RUSCUP KAMAZ exact-string

The auditor approved the CZ1 body (tables 3×16/16 exact, brackets 18/18 exact, CLP row correct —
"good catch: it explains 829 vs 828") and returned two items; both closed the same day.

**1. CZ1-2021-2026_BP-TEAM-PACK_v2.txt v2.2 — 841 rows (was 829), 120/120 gates (was 105).**
The workorder §1 scope table always commissioned the Czech Relegation Playoffs ("state count in a
NOTE"); the v2.1 return held them out over the §2/§3 roster conflict (`roster_scope` warning). The
auditor's return message resolves it: "Add the 12 rows … compType 'other' per ERRATA … 2 legs each,
90-min scores." Emitted: 2022 Teplice 3-0 / 2-2 Vlasim and Opava 0-1 / 0-2 Bohemians 1905 (May 19/22);
2023 Pribram 0-2 / 0-0 Pardubice and Zlin 1-0 / 0-0 Vyskov (Jun 1/4); 2024 Vyskov 0-1 / 0-1 Karvina
and Ceske Budejovice 2-1 / 1-1 Taborsko (May 30 / Jun 2). All six ties won by the First-League side —
no club changed division (RSSSF NB + wiki TwoLeg results agree). No extra time anywhere; every row is
the plain full-time score (90-minute doctrine untouched). The five FNL opponent strings
(Vlasim, Opava, Pribram, Vyskov, Taborsko) are reused client-roster identities — the identical strings
the MOL Cup return documents — not TEAM declarations; WO §2 "no TEAM rows" stands (0 TEAM rows).
Venue evidence: league homes reuse the pinned per-season constants (the 2023 Pardubice/Zlin/Pribram
legs are corroborated by the wiki match boxes incl. attendances 4350/5442/3500); FNL homes from the
worldfootball cup-stadium indexes (Opava 7758, Vlasim 6000, Pribram 7120), Vyskov's Sportovni areal
Drnovice (wiki 2023-06-04 box att 4500; wf's "Stadion FK Drnovice" is the same ground), and Taborsko's
Stadion v Kvapilove ulici, Tabor (en.wiki FC Silon Taborsko infobox + lead, fetched 2026-08-03).

**2. RUSCUP KAMAZ.** "Write exactly KAMAZ (2 rows)": the two in-scope rows
(2021-10-27 KAMAZ 1-0 Ural, Group-2 R3; 2022-03-03 Zenit 6-0 KAMAZ, R16) now carry the roster string
`KAMAZ` verbatim — superseding the earlier exact-form interpretation ("KAMAZ Naberezhnye Chelny",
the RSSSF source-listing string, kept in the identity NOTE). 162/162 gates stay green; group-table
pivot references updated consistently.

Determinism sweep: CZ1 pack sha256
`55d9bd80ef3db4ed84421cffdce64f41f43c9b13f069d3f4eb6a46e74026d643`; RUSCUP pack sha256
`c2658b490d63821166d7b76d04a7e83d3f151f54d7afaef78346d0126b2711f6`.
A residual nondeterminism in the RUSCUP validator *report* (club-pair order inside two gate labels,
from an unsorted set join; pack bytes were always stable) was found during the double-rebuild check
and fixed (`sorted(pair)`); report regenerates byte-identical since.

Still outstanding at close: the owner-announced upload of the original `ERRATA-2026-08-03.md`
(attachment listed on the 2026-08-03 evening message) had not materialized in the sandbox
(`/home/user/uploads/` absent) — the as-relayed mirror continues to govern; the original will be
placed at `supervisor/ERRATA-2026-08-03.md` when it lands.

## Addendum 2026-08-03 (seventh) — WO-EPL-SPAN-12 returned (England Premier League 2021-22 → 2025-26 + 2026-27 boundary)

**Deliverable:** `handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt` — 1,900 MATCH rows (380 × five full
seasons, competition `England Premier League`, compType `domestic-league`, venue-detail `MD1..MD38`),
0 TEAM (WO §2 directive; the 27 pinned roster strings appear verbatim — `Tottenham`, `Wolves`,
`Man City`, `Man United`, `Nott'm Forest` apostrophe form, `Sheffield United`), 17 SOURCE / 17 NOTE,
`END`. Validation: `audit/pack-validation-epl.txt` — **83/83 gates PASS**; builder
`tools/build_epl_pack.py` is byte-deterministic (two consecutive builds → identical sha256
`707dd83047306b07fe52c4e350f89e802e257b7b096a503cea75166861953036`).

**Primary source behaviour.** RSSSF `tablese/eng2022..eng2025.html` (Ian King) carry full
round-by-round dates+scores plus the official final tables; transcribed `audit/ledger/epl-*.txt`
same-day and machine-verified (rounds 38×10 every season; recompute reproduces each final table
club-for-club **and in position order**, incl. pts/GD/GF ordering; official goal anchors
1,071 / 1,084 / 1,246 (all-time PL season record) / 1,115 all hit exactly).
`eng2026.html` (Karel Stokkermans, updated 14 Jun 2026) is the **documented adaptation**: it prints
the Premier League **final table only** — no round listings (full-page verification, chunks 0-2).
The 2025-26 match rows are therefore sourced from `openfootball/england
master/2025-26/1-premierleague.txt` (row label `openfootball-england-2526`) and recompute to the
RSSSF table **exact** (club-for-club + position order); the Wikipedia FBR matrix provides the
score-level second index (380/380 IDENTICAL; goals 1045 = 1045) and football-data.co.uk /
worldfootball spot rows cover date-level corroboration (MD1 block, both MD31 strays byte-for-byte,
QEII round-7 10/10, final-day MD38 all 2026-05-24).

**Second-index lattice (all transcribed 2026-08-03).** openfootball season files 2021-22..2024-25
diffed row-for-row vs RSSSF: **380/380 IDENTICAL round+date+score in all four seasons**
(`tools/diff_epl_second_index.py`); Wikipedia 2025-26 FBR matrix
(`tools/diff_epl_matrix.py`, `audit/ledger/epl-2ndidx-2025-26.txt`): **380/380 IDENTICAL scores**.
Two RSSSF misprints found and adjudicated (full verbatim evidence retained in ledger headers):
(a) 2023-24 round-15 pair Everton 3-0 Newcastle / Tottenham 1-2 West Ham printed under `[Dec 2]`
(impossible — both clubs already in round 14 Dec 2/3): openfootball MD15 confirms played
**2023-12-07** → dates carried corrected, scores identical everywhere;
(b) 2024-25 round-12 Newcastle 0-2 West Ham printed `[Nov 24]`: **two independent indexes**
(openfootball "Mon Nov 25 / 20:00"; football-data row `E0,25/11/2024,20:00,Newcastle,West Ham,0,2`)
agree against it → per WO §4 their **2024-11-25** is carried, `NOTE|warning|source_conflict` issued.

**Continuity doctrine.** All 190 matchweeks dated; no cancelled fixture in the window. Rows keep
original MD labels, file date-sorted: 2022-23 R7 postponed in full (death of Queen Elizabeth II;
played 2023-01-12..2023-04-05); 2023-24 R17 Bournemouth-Luton abandoned 1-1 65' (Tom Lockyer)
2023-12-16 = **VOID — no row** (the ROW-level doctrine: never a fabricated score), complete rematch
2024-03-13 (4-3) carries R17; 2024-25 R15 Everton-Liverpool (Storm Darragh) 2025-02-12 plus the
R29/R34 stragglers; 2025-26 MD31 triple-slice (Wolves-Arsenal fwd 2026-02-18, main body
2026-03-20..22, Man City-Palace back 2026-05-13). **Deductions:** 2023-24 table carries
Everton **−8** / Nott'm Forest **−4** PSR brackets; the table gate applies them before order checks.
**Membership boundary** verified 4/4: bottom-3 clubs of each season absent next season, promoted
trios appear (incl. Luton 2023-24, Ipswich 2024-25, Sunderland 2025-26).

**Boundary statement (WO §1 row 2).** Last completed round of the span = 2025-26 MD38
(2026-05-24, all ten fixtures). 2026-27 had **not started** on the return date: `eng2027.html` 404;
the season card fixes 21 Aug 2026 – 30 May 2027 with fixtures released 19 Jun 2026; promoted
Coventry City / Ipswich Town / Hull City; relegated West Ham / Burnley / Wolves = this pack's bottom
three → zero 2026-27 rows emitted, stated in the `boundary` NOTE (not a blocker).

**Owner pivot decree.** 100/100 club-season full-campaign pivots re-derived from the pack's own
rows and embedded in the validation output (each club 38 games in round order; TEAMPIVOT summaries
reproduce the final-table lines, deductions flagged inline); copies in `audit/ledger/epl-pivot-*.txt`.
**Venues:** 100 constants from the five Wikipedia season stadium tables
(`audit/ledger/epl-venues.txt`); Everton epoch Goodison Park → Hill Dickinson Stadium from 2025-26;
no groundshares or neutral-venue league fixtures in the window; Man United city canonicalized as
Manchester across the span (source prints Trafford/Manchester variants — documented).

---

## Addendum 8 — OWNER OVERRIDE DECREE-2026-08-04: Russia full-span delivery (RPL + RUSCUP)

**Decree (owner verbatim, `supervisor/DECREE-2026-08-04-full-span-override.md`):** full season
files 2021 → today for every league **regardless of what the workorder said** — owner authority
overrides everything; packs become the single source of truth the error-containing old data is
audited against. Effects: the 2024-06-30 hard cutoffs in WO-RPL/WO-RUSCUP (and later
WO-CZ1/WO-MOLCUP) are rescinded; legacy `data/rpl/*.csv` untouched (audit target, not a source).

**RPL pack — full span (supersedes `6e458e19…`, 732 rows).** `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt`
= **1,220 MATCH rows** ((240 league `domestic-league` + 4 prorel legs `other`) ×5, 2021-22..2025-26),
4 TEAM / 16 SOURCE / 22 NOTE, sha256 **`d71ed24f3a321d6c2975bbff46a6ee405066a79870b4d158b6f5781c6ec9db79`**,
**95/95 gates PASS** (`tools/build_rpl_pack.py`, byte-deterministic double rebuild). New-season
primary transcription from RSSSF rus2025/rus2026 (#1l + #prorel + #1ldet): EXACT recomputes
(648/648 and 609/609 goals, tables 16/16 incl. the 2024-25 DMh-over-Khimki H2H bracket at 29
reproduced from mutual results; 2025-26 has zero points ties). Playoff outcomes: 2024-25 Sochi
promoted 4-3 agg **with Pari NN not relegated (Khimki license-denial reprieve)**, Akhmat stays
3-2; 2025-26 all four stay (DMh 3-0 Ural, Akron 2-1 Rotor) — no shootouts in any of the ten ties
of the span. **Second-index switch (documented):** football-data R1.csv discontinued for
2425/2526 (404 verified) and openfootball/russia absent (404) → Wikipedia season FBR matrices
transcribed (`audit/ledger/rpl-2ndidx-*.txt` via `tools/diff_rpl_matrix.py`): **240/240
score-identical vs RSSSF primary both seasons**, matrix-recomputed tables 16/16 vs official,
goal anchors green; worldfootball matchday pages third anchor (MD30-2425 8/8 exact); fdata
diffs for 2021-24 unchanged (730/732 + 2 documented conflicts). **Venue lattice** from the wiki
venue tables + #1ldet per-match prints: Krasnodar→Ozon Arena mid-season rename boundary R27;
Fakel Stadium (new 2024-25 ground; R23 behind closed doors att 0; R27 one-off back at the old
CTU Stadium); Rubin R12-2425 staged Nizhny Novgorod; Pari NN 2025-26 renovation groundshares
(R1 Kazan 2,142 / R3 Grozny 232 / R5+R8+R9 Saransk) returning R12+ under sponsor era SovComBank
Arena (= Nizhny Novgorod Stadium); Akron R13 staged Saransk 8,531; Solidarnost share KS/Akron;
Anzhi Arena in Kaspiysk; Rostech Arena era for Baltika; playoff grounds via wiki/RFS boxes
(incl. Rotor's Volgograd Arena; Akhmat leg2 att taken from wiki box — RSSSF prints "Att: ?").
**Membership chain** (RFU refs in pack NOTE): Khimki+Chernomorets license denial 2025-05-24
(222413) → Pari NN reinstated 2025-06-16 (222586); Torpedo excluded 2025-07-10 (premierliga.ru
32356) → Orenburg reinstated 2025-07-11 (222692). **Boundary 2026-27** (rus2027.html): R1
played 2026-07-24..26 (8 games), R2 printed fixtures-only at return date → zero rows per the
not-a-full-season rule; FNL-level context noted (Pari NN reverts name to FC Nizhny Novgorod there).

**RUSCUP pack — full span (supersedes `c2658b49…`, 189 rows).**
`handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` = **341 MATCH rows** (36+77+76+76+76, compType
`domestic-cup`), 25 TEAM / 16 SOURCE / 119 NOTE, sha256
**`f89501cf25e10389e175579ef1a38105b5b02bde78a83362a65c1bb4a173db91`**, **258/258 gates PASS**
(`tools/build_pack.py`, byte-deterministic). Slice rule unchanged (every match with ≥1 of that
season's 16 RPL clubs): 48 group + 28 bracket per new edition (reproduces the auditor-proven
76-row calibration twice more). New formats documented: 2024-25 Major/Minor double elimination;
2025-26 RPL-path QF (two legs) + Regions-path crossings + Superfinal. Champions: CSKA Moscow
2024-25 (Superfinal 0-0 Rostov, pens 4-3, Luzhniki 57,176); Spartak Moscow 2025-26 (Superfinal
1-1 Krasnodar, pens 4-3, Luzhniki 72,978, ref Tanashev). **Second index 152/152 identical**
(wiki cup articles + RFS official match pages; span-wide 341/341). **Findings:** 3 RSSSF
group-table print errors proven by group balance and corroborated exactly by the RFU-sourced
wiki tables (2024-25 Dynamo Moscow pts 8→**11**; 2025-26 Akhmat GF-GA 7-8→**8-10**; 2025-26
Lokomotiv GA 2→**4** — MATCH rows unaffected, `NOTE|warning|print_error`); 2025-26 Arsenal
Tula-Rubin venue/date adjudicated **against** RSSSF cupdet via two independent indexes (RFS
56055 + wiki box: 2025-11-25, Arsenal Stadium, Tula, att 6,717; the same evening's Torpedo tie
genuinely at Arena Khimki, as is Arsenal's later Loko tie per RFS 56059). New TEAM rows: Tyumen
(Geolog Stadium), Shinnik Yaroslavl, Neftekhimik Nizhnekamsk (cap 3,046 per RFS). 2026-27
boundary: Regions-path R1 played (11 ties, 0 RPL by design) → zero rows. KAMAZ exact-string
discipline continues on its 2025-26 row per ERRATA-2026-08-03.

**Queue state after this delivery:** ① RPL ✅ full span, ② CZ1 ✅ (extra-years extension
2024-25+2025-26 next under the same decree), ③ RUSCUP ✅ full span, ④ MOLCUP ✅ (extra years
queued), ⑤ EPL ✅ full span, then ⑥ FRA (2021-22 ledger already transcribed), GER, ITA, KOS,
KOSCUP, MLS, SCO1, SCOCUP, SCOLC, SPA, USOC.

## Addendum 2026-08-04 (ninth entry) — DECREE-2026-08-04 full-span override: CZ1 extra years shipped (2024-25 + 2025-26)

The owner override (register: `supervisor/DECREE-2026-08-04-full-span-override.md`) orders every
pack extended to the full span 2021 → today, "one source of truth because our old data contains
errors that will be audited against your full data" — Russia first (shipped), **Czech First League
completed immediately after**. All workorder hard cutoffs (2024-06-30) rescinded; legacy client
data untouched.

**CZ1 pack — full span (supersedes `55d9bd80…`, 841 rows).**
`handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` = **1,401 MATCH rows** (276+276+277+276+276 league
compType `domestic-league` + **20 Czech Relegation Playoffs pro/rel legs** compType `other` per
ERRATA), 0 TEAM / 21 SOURCE / 27 NOTE, sha256
**`cbd5710ba24b8f819cadcdff015199d34391afba0041c2935569604e1a390a6e`**, **175/175 gates PASS**
(`tools/build_cz1_pack.py` extended to 5 seasons, byte-deterministic — double rebuild identical).

**Construction of the two new season layers.**
- 2024-25: RSSSF tsje2025 #1gamb transcribed on fetch day (`audit/ledger/cz1-2024-25.txt`,
  280 rows = 240R+15T+15Z+6 Evropu+4 PRO) and verified EXACT by recompute (RT 16/16, TT 6/6,
  ZT 6/6, 627 regular goals; span 2024-07-19..2025-06-01). Notable: Slavia champions (78 reg →
  90 after Titul); regular three-way H2H at 34 (Bohemians 8 > MlBoleslav 7 > Teplice 1 — RSSSF
  bracket = wiki hth_BOH = recompute); Titul 63-63 decided by regular points (Sparta 62 >
  Jablonec 51 — same rule as the 2022-23 title); CBudejovice relegated winless (0-5-25 regular,
  0-6-29 after Zachranu); prorel NB "all remain at former level": Vyskov 0-0/1-1(aet) Dukla —
  **Dukla survived pens 4-2** (gate + NOTE carry the shootout, rows stay the played scores);
  Pardubice 2-1 agg Chrudim; no Conference League playoff from this season (league abolished it).
- 2025-26: RSSSF tsje2026 prints **page-form** (official tables + playoff legs only, no round
  listings — same adaptation class as the EPL 2025-26 return). The 270 league-stage rows were
  assembled by `tools/build_cz1_2526_ledger.py` from the **BBC "Czech Liga" dated month lattice**
  (12 server-rendered month pages, 276 D-rows incl. stage labels and the 'Match awarded' print,
  `audit/ledger/cz1-dates-bbc-2025-2026.txt`) × **wiki FBR matrices** under gates V1..V6 —
  BBC↔wiki cell bijection 270/270; recompute == RSSSF constants EXACT (16/16 regular + 6/6 Titul
  + 6/6 Zachranu; 623 regular goals). Postponements keep Round labels (R2 Ostrava-Teplice→09-17;
  R3 MlBoleslav-Plzen→08-19; R5 Pardubice-Ostrava→10-01; R6 Bohemians-MlBoleslav→10-22;
  R13 Sparta-Bohemians→10-28).
- Second index both seasons: staged MX grammar ledgers (280 rows each: wiki FBR + group matrices
  + Evropu bracket + pro/rel TwoLeg boxes), `tools/diff_cz1_matrix.py` **280/280 score-identical
  vs the primary ledger both seasons**; the gate caught and fixed 3 MX transcription inversions.
  worldfootball dropped Czech coverage from 2024-25 (cze-* roots 404; ESPN cze.1 API empty) —
  the fixed-matchday spot-audit is documented n/a on the two new seasons, replaced by strictly
  stronger full-depth diffs (every game, not one matchday).

**Findings shipped in the pack (all disclosed as warning NOTEs; nothing silently fixed):**
1. **2026-05-09 T32 Prague derby walkover** — abandoned in stoppage time at 3-2 Slavia after
   fans stormed the pitch (iDNES.cz, Reuters same-day; BBC 'Match awarded'); LFA awarded **0-3
   Sparta** on 2026-05-12. The row carries the official 0-3 (score of record; all post-decision
   tables and the recompute gates agree). `match_awarded`.
2. **Wiki 2025-26 Zachranu matrix malformation** — three cells carry a unicode minus inside the
   score string (unparsable, and conflicting with the article's own group table); adjudicated
   2-0/0-3/2-0 via the BBC lattice + arithmetic closure; both indexes carry the corrected cells
   identically, so the diff gate stays a true 1:1. `source_conflict`.
3. **RSSSF tsje2026 Zachranu position column** prints 13/13/15/14 (impossible duplicate-13
   pattern) beside fully consistent W-D-L/GF-GA/Pts constants — position strings NOT propagated;
   constants + wiki order govern. `print_error`.
4. **Karvina incident** — MFK Karvina finished 2025-26 as Czech Cup **winner** and Evropu
   **finalist** (1-7 agg to Sigma Olomouc), then was **administratively demoted** after
   match-fixing accusations (RSSSF NB 'Karvia [sic] relegated'; wiki note_KAR), waiving its
   Europa League play-off spot; **SK Artis Brno** — which had LOST its pro/rel playoff to
   Slovacko 1-7 agg — was promoted to the 2026-27 First League in Karvina's place (en.wiki SK
   Artis Brno); Dukla Prague's sporting relegation (Zachranu 6th) stands. Off-field close-season
   membership decisions change no row in the pack. `karvina_incident`.
5. Regular-stage tie adjudication: 2025-26 Dukla over Slovacko at 23 by H2H 6-0 (recomputed
   1-0H/2-1A) — RSSSF prints no bracket; wiki hth_DUK note is the adjudicator of record.

**Identity/scope deltas under full span:** the retired anti-appear list resolves as designed —
`Dukla Prague` joins league rows for its exactly-two top-flight seasons (2024-25/2025-26),
Artis Brno appears only on pro/rel rows (its First-League promotion takes effect 2026-27, past
the boundary); FNL pro/rel universe = 7 reused roster strings (Vlasim, Opava, Pribram, Vyskov,
Taborsko, **Chrudim** — Za Vodojemem per en.wiki MFK Chrudim, 1,500; **Artis Brno** — Mestsky
fotbalovy stadion Srbska, Brno per en.wiki SK Artis Brno, 10,200, moved there for 2025-26,
groundshare with Zbrojovka). Consistency decree honoured: all stadium/city strings byte-identical
to the earlier packs; 2025-26 capacity reprints documented in `cz1-venues.txt` only.

**Boundary 2026-27:** RSSSF tsje2027.html = 404 (page not started); BBC fixture menu shows
2026-27 R1 scheduled 2026-08-07..09 (Zbrojovka Brno + Artis Brno in; Karvina + Dukla out) —
NOT a full season at the 2026-08-04 return date → zero rows, boundary NOTE in the pack.

Validation: `audit/pack-validation-cz1.txt` regenerated — **80 club-season pivots** + 7 FNL
2-leg pivots (owner per-team technique, five seasons); regular tables 16/16 ×5 and group tables
6/6 ×10 reproduced against independent constants; all 8 regular-stage H2H ties + 4 group ties
recomputed; second-index diff 1,378/1,381 league + 20/20 pro/rel legs (3 whitelisted wiki cell
defects from the old window; nothing new).

## Addendum 2026-08-04 (tenth entry) — DECREE-2026-08-04 full-span override: MOLCUP extra years shipped (2024-25 + 2025-26)

**What/why:** the owner's override decree (pack-to-span) applied to queue item ④. The MOL Cup
pack now covers **all five completed seasons 2021-22 → 2025-26**: 202 MATCH rows
(41+41+38+41+41 by the WO-§1 slice rule), 43 TEAM rows (12 new lower-league identities + the
Artis Brno rename row), 33 advancement NOTEs, sha256
`50ead762d80070dce6cbf468dedd26eb4d4e3706dd264801194af49385791137` (double-rebuild sha-identical),
**32/32 external gates PASS** (incl. Artis-rename-era and 2026-27 boundary gates).

**Evidence chain (all three anchors per season):** RSSSF season cup chapters (primary; coverage
paradox disclosed — 2021-24 pages carry R16 onward, the 2024-25/2025-26 pages carry **R3 onward
with dates**), en.wiki raw bracket sections 4-9 per season (R2 of all five seasons, QF/SF/F
boxes), worldfootball all_matches/stadiums indexes per season **plus 22 per-tie match reports**
(goal timelines proving all 13 extension settled-tie 90-minute splits; stadium lines proving the
Stechovice/Novy Bor/Lapac/Plynarne/ShipEx per-tie venues — every venue-by-inference candidate
was killed in favour of report evidence, per decree).

**Source incidents disclosed (pack NOTEs):** wiki 2025-26 R2 print `Rokycany 0-1 Mlada Boleslav`
vs wf double-print **0:6** (six-goal timeline ma11538503) — row carries 0-6, typo documented.
 wf keeps folding penalties into the scoreline (`4:5 pso`, `6:5 pso`) — quirk documented, rows
carry 90-minute scores. Czech aet convention changed from 2024-25 (aet now occurs at R2/R3/R16),
replacing the 2021-24 "R1-R4 straight to pens" rule — scope change disclosed.

**Bracket truth for the auditor:** champions 2025 **Sigma Olomouc** (3-1 Sparta, Andruv stadion,
att 12014) and 2026 **MFK Karvina** (3-1 Jablonec, Malsovicka Arena, att 7352). Karvina's cup
double-season (cup win + league match-fixing demotion) is cross-referenced between this pack and
the CZ1 pack (`integrity_flag` NOTE). 2025-26 sensation rows: Nove Sady (D4) 3-2 Sigma Olomouc
R3; Artis Brno pens 6-5 v Liberec R3; Artis's homes staged at ShipEx Arena (= sponsored Srbska,
per-tie reports) — Artis is also the club administratively promoted to the 2026-27 First League.

**Boundaries:** 2026-27 cup = boundary NOTE only, zero rows (season incomplete inside span).

**Files:** `handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt` (202 MATCH rows),
`tools/build_molcup_pack.py`, `tools/validate_molcup_pack.py` (v5), ledgers
`audit/ledger/molcup-2024-25.txt`, `molcup-2025-26.txt`, `molcup-venues-teams.txt` (sections
A-I: WFSTA ×5 seasons, 33-row SPLIT register, TIER + TEAMREG extensions, identity/venue POV
proofs), `audit/pack-validation-molcup.txt` (32/32).

**Queue state after this delivery:** ① RPL ✅ full span, ② CZ1 ✅ **full span**, ③ RUSCUP ✅
full span, ④ MOLCUP ✅ **full span** (override extra years shipped 2026-08-04), ⑤ EPL ✅ full
span, then ⑥ FRA (2021-22 ledger already transcribed + verified EXACT), GER, ITA, KOS, KOSCUP,
MLS, SCO1, SCOCUP, SCOLC, SPA, USOC.

---

## Addendum 2026-08-04 (#11) — RUS-ADDENDUM pack: REQ-1/2/3 of ADDENDUM-2026-08-04-RUSSIA-GAPS closed

**Incoming owner/auditor documents** (uploaded to `main` `Supervior/` 2026-08-04; archived
verbatim researcher-side as `supervisor/SPEC-2026-08-04-RUSSIA-COMPLETE.as-relayed.md` and
`supervisor/ADDENDUM-2026-08-04-RUSSIA-GAPS.as-relayed.md`):
- **02-SPEC** restates the Russia-complete scope (RPL 5 seasons + 2026-27-to-date, expected
  1,209 rows "today"; playoffs 16; Super Cups 2025+2026; RUSCUP full span).
- **03-ADDENDUM** registers three requests: REQ-1 push MOLCUP full-span (transport);
  REQ-2 RPL 2026-27 played rows (D14-blocking); REQ-3 Super Cup 2025+2026 (D14-blocking);
  REQ-2+3 to ship as one small addendum pack with own sha, announced in WORKORDER-STATUS.

**REQ-1 — already satisfied before the document arrived.** The MOLCUP full-span delivery
(commit `84d9471`, sha `50ead762…`, 32/32 gates) was pushed 2026-08-04 after the GitHub
token refresh and verified as the remote tip; the auditor's "local only at 5722cb61" note was
stale by the time it was written. A sandbox re-clone incident orphaned the first local commit
(`5d75e56`) — content recovered byte-exact from the working tree (899+/92- footprint
identical, double-rebuild + gates re-run) and recommitted as `84d9471`. md5/sha-on-arrival
policy unaffected: `50ead762…` unchanged.

**REQ-2 — 16 league rows (RPL 2026-27 R1 ×8 + R2 ×8), rolling.**
- Sources: RSSSF `rus2027.html#1l` primary (R1 complete with attendances, Total 102,232; R2
  fixture-only at fetch) — adaptation: R2 dated/scored from the **RPL official heritage match
  centre** (`match_16249..16256`, proves the window completed 2026-07-31..08-02) and reconciled
  against wiki 2026-27 in all three of its structures (FBR 16/16, table-through-2026-08-02
  recomputed from pack rows 16/16 club-for-club, infobox 16 matches/51 goals). worldfootball
  has no 2026-27 season page (404 both slug shapes) — third index absent, documented.
- Cumulative league rows to date: 1,200 (pinned pack) + 16 = **1,216**; the SPEC's 1,209
  estimate and REQ-2's "8 + played R2" estimate were drafted against an earlier R2 snapshot
  (variance NOTE in pack).

**REQ-3 — Russian Super Cup 2025 + 2026, 90-minute doctrine.**
- 2025: Krasnodar 0-1 CSKA (Diveyev 48), 2025-07-12, Ak Bars Arena (RSSSF prints era name
  "Kazan Arena"), att 34,677 — verified RSSSF `rus2025.html#sup` + wiki box (rfs 55756).
  **REQ-3's hedge ("2025 game = Zenit vs Krasnodar-class") is WRONG; the 02-SPEC print was
  right. So reported.**
- 2026: Zenit 1-1 Spartak, pens 4-2 Zenit, 2026-07-18, Nizhny Novgorod Stadium, att 42,139 —
  verified RSSSF `rus2026.html#sup` (lineups + shoot-out lines) + wiki box (rfs 57020). Row
  carries 1-1; advancement NOTE holds the shoot-out detail.
- compType `domestic-cup` (ERRATA cup class), flagged per the 02-SPEC "pending builder
  confirm" rule; competition string `Russian Super Cup`; 2021-2024 editions = outside
  commissioned scope (NOTE).

**Errors/anomalies caught and registered this round:**
1. en.wiki 2026-27 hat-trick table: Glushenkov treble dated "2 August **2025**" — editorial
   year typo; true date 2026-08-02 (official match_16251 + table stamps). Row carries truth.
2. ru.wiki infobox goals 48 vs en.wiki 51 — mirror snapshot lag (mid-day Aug-2 state), no
   score conflict; en index governs.
3. Igor Diveyev appearing for **Zenit** in the 2026 Super Cup — verified a real summer-2026
   signing from CSKA (RSSSF lineup); an earlier provisional session read had flagged it as a
   possible wiki anomaly — withdrawn explicitly.
4. 02-SPEC mismatches (registered, NOT patched): playoff enumeration "16 rows" skipping the
   2025 ties and naming 2026 "Shinnik-Akron"; pack truth = 20 legs incl. 2025
   (Sochi-PariNN, Ural-Akhmat) and 2026 Akron-Rotor / Ural-Dynamo Makhachkala (Shinnik not a
   participant, FL 8th). Pinned pack untouched.

**Delivery:** `handoffs/RUS-ADDENDUM-2026_BP-TEAM-PACK_v2.txt` — **18 rows, sha256
`30576ac4894930b359db19193f08f05cd3f399ecd7d97f9975184ac02386dcea`** (double-rebuild
identical), 1 TEAM (Rodina Moscow top-flight registration; all 16 club strings already pinned
in the RPL pack), 7 SOURCE / 13 NOTE; `tools/build_rus_addendum_pack.py`,
`tools/validate_rus_addendum_pack.py` → `audit/pack-validation-rus-addendum.txt` **16/16
PASS** (deterministic report, per-club pivots); ledgers `audit/ledger/rpl-2026-27.txt`,
`audit/ledger/rus-supercup-2025-2026.txt`, `audit/ledger/fra-2025-26.txt` (captured
fetch-day for the FRA build). Register rows updated in WORKORDER-STATUS + README.
Pins untouched: RPL `d71ed24f…`, RUSCUP `f89501cf…`, MOLCUP `50ead762…`, CZ1 `cbd5710b…`,
EPL `707dd830…`.

**Queue state:** Russia addendum closed (REQ-1..3). Next: FRA full span (fran2022 ledger
EXACT-verified in a prior session; fran2026 tables/cup layer captured 2026-08-04), then
GER, ITA, KOS, KOSCUP, MLS, SCO1, SCOCUP, SCOLC, SPA, USOC.

---

## Addendum #12 — FRA Ligue 1 full span shipped (2026-08-04)

**Scope:** WO-FRA-SPAN-16 on DECREE-2026-08-04 override — France Ligue 1 seasons 2021-22,
2022-23, 2023-24, 2024-25, 2025-26 end-to-end + the pro/rel playoff legs touching the top
flight + sourced 2026-27 boundary. The 20→18 club contraction from 2023-24 (the WO's
membership trap) applied: 380+380+306+306+306 = 1,678 league rows + 8 `other` legs =
**1,686 MATCH rows**.

**Evidence chain (all fetched 2026-08-04, ledgers transcribed immediately):**
- PRIMARY RSSSF `fran2022..fran2025.html` full round-by-round → `audit/ledger/fra-<s>.txt`
  (2021-22 pre-existing EXACT; 2022-23/2023-24/2024-25 written new). **`fran2026.html`
  prints NO league round-by-round** (final table + playoff + cups only, single-chunk page,
  same shape as EPL's eng2026) → 2025-26 carrier = openfootball/europe `2025-26_fr1.txt`
  (raw verbatim in `data/raw/`, parser `tools/parse_ofb_fra.py`, R-annex appended to the
  ledger) gated by full recompute: **18/18 club-for-club EXACT, 863 goals** — documented
  `source_adaptation`.
- Second indexes: openfootball season files 2021-22..2024-25 → diffs **380/380, 380/380
  (after one adjudication), 306/306, 306/306 (after one adjudication)** identical
  round+date+score (`tools/diff_epl_second_index.py`); Wikipedia 2025-26 FBR matrix
  (`fra-2ndidx-2025-26-MX.txt`) **305/306 + one wiki typo**; worldfootball matchday pages
  ×5 (one full round per season, incl. both adjudicated rounds and the 2025-26 RS26 stray);
  Wikipedia season articles → 94-row venue lattice (`fra-venues.txt`) + playoff boxes
  (90-min splits via goal minutes).
- Boundary: `fran2027.html` 404 + wiki 2026-27 (starts **2026-08-23**, Troyes/Le Mans up,
  Metz/Nantes down, PSG five-time defending) → zero 2026-27 rows.

**Adjudications shipped (rule: RSSSF stands unless two independents agree against it):**
1. `source_conflict` 2022-23 R2 Lorient 3-1 Lyon — RSSSF `[Aug 14]` misprint; openfootball
   AND worldfootball (07.09.2022 19:00) agree → row dated **2022-09-07** (ledger edited,
   diff re-run to 380/380).
2. `source_conflict` 2024-25 R9 Rennes 1-0 Le Havre — RSSSF `[Oct 26]` misprint;
   openfootball (Fri Oct 25) AND worldfootball (25.10.2024 20:45) agree → **2024-10-25**
   (ledger edited, diff re-run to 306/306).
3. `source_conflict` wiki 2025-26 matrix prints Brest-Lens **3-0** against FOUR agreements
   for **3-3** (RSSSF table GF43/GA35, the article's own table template, the OFB carrier
   MD31|2026-04-24, the 863-goal total — matrix sums 860 with the typo): wiki typo,
   verbatim kept, diff gate tolerates exactly this cell.

**Doctrine disclosures in the pack:** abandonments — 3 VOID games with full replays
carrying round labels (2021-22 R3 Nice-OM 2021-10-27; R14 Lyon-OM 2022-02-01; 2023-24 R8
Montpellier-Clermont 2023-11-29 closed doors + the −1 deduction), 2 results that STOOD
(2024-25 R26 Montpellier 0-2 StE 62'; 2025-26 Nantes 0-0 Toulouse 22' pitch-invasion, LFP
upheld via wiki efn). Postponement strays mapped incl. 2025-26 RS5 Monday le Classique,
RS26 (wf-corroborated) and RS29 (title decider at Lens 2026-05-13). Playoff 90-minute
splits (goal-minute verified): 2021-22 leg2 1-1 at 90 (pens 5-4 Auxerre up); 2023-24
Metz 2-1 at 90 (aet 2-2; StE up 4-3); 2024-25 Reims 1-1 at 90 (aet 1-3; Metz up 4-2);
2025-26 plain (Nice 4-1 agg, leg2 behind closed doors). L2-internal rounds =
NOT-COMMISSIONED ledger context only (8 lines). Deductions applied in the table gates:
2021-22 Nice −1 / Lyon −1; 2023-24 Montpellier −1. Ligue 1 tie-break depth reproduced:
pts → GD → H2H pts → H2H GD → H2H away goals (2023-24 Metz/Lorient, RSSSF bracket
`[2 1 0 1 4-4 3; 3 ag]` vs `[.. 2 ag]`).

**Delivery:** `handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt` — **1,686 rows, sha256
`44fe06b53af78c0849321ef82815e461181c1747a0a22ea0ba182348cd09b562`** (double-rebuild
identical), 0 TEAM (26 pinned strings incl. the `Paris SG`/`St Etienne` traps; Dijon
pinned-but-never-in-window documented in federation_check), 19 SOURCE / 22 NOTE;
`tools/build_fra_pack.py` → `audit/pack-validation-fra.txt` **85/85 PASS** (per-club
pivots 94/94, venue lattice 94, Monaco cross-border disclosed under venue_policy).
Roster-faithful stock map (ParisSG→Paris SG, SaintEtienne→St Etienne, LeHavre→Le Havre,
ParisFC→Paris FC). Pins untouched: RPL `d71ed24f…`, RUSCUP `f89501cf…`, CZ1 `cbd5710b…`,
MOLCUP `50ead762…`, EPL `707dd830…`, RUS-ADDENDUM `30576ac4…`.

**Queue state:** FRA closed. Next on the owner's one-at-a-time queue: GER (workorder
staged; 18 clubs/34 rounds per its card — same shape as FRA 2023-24+, builder pattern
reusable), then ITA, KOS, KOSCUP, MLS, SCO1, SCOCUP, SCOLC, SPA, USOC.
