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
`6e458e19…`), RUSCUP 162/162 (`audit/pack-validation.txt`, sha `18ba4695…`).

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
builder `tools/build_cz1_pack.py` byte-deterministic (pack sha256 `eee4686f…`).

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
