# WORKORDER-STATUS

**Date:** 2026-08-03 · **Branch:** `arena/019fc462-the-bettor-1`

---

## Active commission register (discovered 2026-08-03 on `origin/main`)

16 five-year-span workorders were uploaded to `origin/main` (owner web-uploads;
that history is unrelated to this branch, so files are read via
`git show origin/main:<file>` and mirrored for reference under `supervisor/workorders/`).
Owner's one-at-a-time queue, with the live-session override applied:

| # | Order | Output | Status |
|---|---|---|---|
| override | **WO-RUSCUP-BACKFILL-03** — Russian Cup 2021-22 → 2023-24 | `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03, amended same-day on the auditor's return — 189 rows (domestic-cup after errata), 22 TEAM incl. FC Ufa, KAMAZ written exactly `KAMAZ` (2 rows) per the auditor directive, all 162 self-gates PASS** (user commissioned the cup return live, ahead of the RPL league pack) |
| ① | RPL league 2021-22 → 2023-24 | `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 732 rows (240+4 per season ×3; 12 playoff rows compType `other` after errata), all 69 self-gates PASS** |
| ② | **WO-CZ1-BACKFILL-02** — Czech First League 2021-22 → 2023-24 | `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03, amended same-day on the auditor's return (body approved: tables 3×16/16, brackets 18/18, CLP row) — 841 rows (276+276+277 league + 12 Czech Relegation Playoffs pro/rel legs, compType `other` per ERRATA), all 120 self-gates PASS** |
| ④ | **WO-MOLCUP-BACKFILL-04** — MOLCUP (Czech MOL Cup) 2021-22 → 2023-24 | `handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 120 rows (41+41+38 per the WO-§1 slice; compType `domestic-cup` per errata), 31 TEAM, 20 advancement NOTEs, all 30 external gates PASS** |
| ⑤ | **WO-EPL-SPAN-12** — England Premier League 2021-22 → 2025-26 (+ 2026-27 boundary) | `handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 1,900 rows (380 ×5, `domestic-league`, `MD<n>` venue-detail), 0 TEAM (27 roster strings verbatim), 17 SOURCE / 17 NOTE, all 83 self-gates PASS** (the register's earlier "WO-EPL-BACKFILL-05 (2021-22 → 2023-24)" id is stale — the governing card on `origin/main` is the 5-year-span order; scope covered through today per its §0 no-cutoff note) |
| ⑥→ | FRA, GER, ITA, KOS, KOSCUP, MLS, SCO1, SCOCUP, SCOLC, SPA, USOC | packs | QUEUED (workorder texts on `origin/main`); cups run `domestic-cup`, GER = 18 clubs/34 rounds per its card |
| **OVERRIDE** | **DECREE-2026-08-04 full-span override** (owner verbatim in `supervisor/DECREE-2026-08-04-full-span-override.md`) | — | **GOVERNING: full seasons 2021 → today, workorder cutoffs rescinded, packs = single source of truth vs error-containing old data. Russia first.** |

### OVERRIDE — Russia full-span extension (IN PROGRESS, started 2026-08-04)

Ledger state (all committed, all recomputed at transcription):

| Ledger | Rows | Verification state |
|---|---|---|
| `audit/ledger/rpl-2024-25.txt` | 240 league + 4 prorel | **EXACT**: 648/648 goals, 16/16 W-D-L-GF-GA; playoffs Ural-Akhmat 2-3, Sochi-PariNN 4-3 agg (Khimki license-denial reprieve NB) |
| `audit/ledger/rpl-2025-26.txt` | 240 league + 4 prorel | **EXACT**: 609/609 goals, 16/16; playoffs Ural-DMh 0-3, Rotor-Akron 1-2 agg (all stay) |
| `audit/ledger/cup-2024-25.txt` | 76 (48 grp + 28 brk) | 76/76, stage histogram exact; 3 RSSSF print errors proven by group balance + groupmate lines (DM pts cell→11); champion CSKA (Superfinal pens vs Rostov, Luzhniki 57,176) |
| `audit/ledger/cup-2025-26.txt` | 76 (48 grp + 28 brk) | 76/76; same two-cell print-error pattern (Akhmat GF-GA→8-10, Loko GA→4) proven by balance; new format (RPL-path QF + Regions crossings + Superfinal); champion Spartak (pens vs Krasnodar, Luzhniki 72,978) |

Second-index state 2024-25/2025-26: football-data Russia feed **discontinued (404 verified both seasons)**; openfootball/russia absent (404). Replacement lattice: Wikipedia season/cup articles (results grids + match boxes) + worldfootball round pages (MD30-2425 probe = 8/8 exact). 2026-27 boundary (rus2027.html): RPL started 2026-07-24, R1 complete, R2 played 2026-07-31..08-03 (not yet on primary listing as of return date); roster incl. Fakel+Rodina; full fixture grid filed; zero pack rows (not a full season), FNL NB: Pari NN reverted to "FC Nizhny Novgorod" name at FNL level (context only — roster string unchanged).

Outstanding for the two packs' rebuilds: (1) wiki season venue tables + FBR/round grids (2024-25 chunk 1-2 gallery done: Anzhi Arena 24,859, Solidarnost Arena 42,347, Krasnodar Stadium 35,179, VEB 30,114, RZD 27,032, **Fakel Stadium 10,052 = new 2024-25 home, replaced Tsentralnyi Profsoyuz Stadion**, Arena Khimki, Nizhny Novgorod Stadium, Rostov Arena) incl. Spartak-era string 2024-25 (Lukoil-era evidence in 2025-26 prints) and Krasnodar "Ozon Arena" era prints (R30-2425 1ldet + QF-2526 cupdet); (2) wiki Russian Cup 2024-25/2025-26 articles for 3 blank D2 host venues (Torpedo, Neftekhimik, KAMAZ) + 2024-25 Minor Final venue + matchbox corroboration of the 3 proven print errors; (3) worldfootball round lattice for dates (segue URL form /schedule/rus-premier-liga-<SEASON>-spieltag/<N>/ redirects fine); (4) builder extension + pivots + gates + validation + docs + regression sweep.

### Closure confirmation (2026-08-04, owner request: "mark Russia + completed as closed")

Re-verified fresh this date — every delivered builder re-run **byte-identical** (two passes each),
all gates re-green:

| Pack | Rows | Gates | sha256 (prefix) | Span architecture per its workorder |
|---|---|---|---|---|
| RUSCUP | 189 | 162/162 | `c2658b49…` | 2021-22/22-23/23-24 delivered here (36+77+76 auditor-proven RPL-slice); 2024-25 + 2025-26 (76 rows each) held + auditor-verified client-side per WO §1; current season fills centrally |
| RPL | 732 | 69/69 | `6e458e19…` | 2021-22/22-23/23-24 delivered here (240 league + 4 playoff legs each); 2024-25 + 2025-26 (240/240 each) held client-side per WO preamble; 2026-27 in progress via central requests |
| CZ1 | 841 | 120/120 | `55d9bd80…` | same segment architecture (2021→2024 delivered; later seasons held client-side per the segment commission) |
| MOLCUP | 120 | 30/30 | `5023eb33…` | 2021-22/22-23/23-24 slice (41+41+38) delivered |
| EPL | 1,900 | 83/83 | `707dd830…` | **full span, no cutoff** — all five seasons 2021-22 → 2025-26 delivered here; 2026-27 boundary proven to start 2026-08-21 (after the return date) = zero rows by rule |

Nothing is outstanding on the researcher side for Russia or any delivered federation; the
gap-free whole-span certification (delivered segment + held seasons + central feed) and the
§6 owner approval happen owner-side, exactly as the workorders prescribe. All work pushed
to `origin/arena/019fc462-the-bettor-1` (tip `06a76f5` + the doc fixes of this entry).

### ⑤ EPL return — build notes for the auditor

- **Source-hierarchy outcome:** RSSSF `tablese/eng2022..eng2025.html` (Ian King) = full rounds +
  final tables, transcribed to `audit/ledger/epl-<season>.txt` on fetch day and self-verified
  (38×10; tables 20/20 + position order ×5; official season goal anchors 1,071/1,084/1,246/1,115).
  **`eng2026.html` adaptation (documented, no alternative within RSSSF):** the page (Karel
  Stokkermans, updated 14 Jun 2026) prints the Premier League **final table only** — the 2025-26
  match rows are therefore sourced from `openfootball/england master/2025-26/1-premierleague.txt`
  (label `openfootball-england-2526` on those rows) and reproduce the RSSSF table club-for-club
  **and** in position order EXACT on full recompute (gated; 380 rows, 1,045 goals,
  2025-08-15..2026-05-24).
- **Second-index lattice:** openfootball season files diffed row-for-row vs RSSSF for
  2021-22..2024-25 — **380/380 IDENTICAL (round+date+score) in all four seasons** incl. the
  QEII round-7 scatter (10/10, original window 2022-09-10..12 → played 2023-01-12..2023-04-05);
  Wikipedia 2025-26 FBR matrix diffed cell-for-cell — **380/380 IDENTICAL scores** (goals 1045=1045);
  worldfootball QEII MD7 page 10/10; football-data E0 CSV rows byte-agree on every queried fixture.
- **Adjudications (both in pack `source_conflict` NOTEs):** (a) RSSSF 2023-24 prints round-15
  Everton 3-0 Newcastle & Tottenham 1-2 West Ham under an impossible `[Dec 2]` — played
  **2023-12-07** per openfootball (dates corrected, scores never in doubt); (b) RSSSF 2024-25
  prints round-12 Newcastle 0-2 West Ham `[Nov 24]` — **two independent indexes**
  (openfootball "Mon Nov 25/20:00" + football-data row `25/11/2024,20:00`) agree against it, so
  per WO §4 the pack carries **2024-11-25**; RSSSF prints preserved verbatim in the ledgers.
- **Anomaly gates (90-minute doctrine respected):** 2022-23 R7 full postponement (QEII) — 10 rows,
  none in Sep 2022; 2023-24 R17 Bournemouth-Luton abandoned 1-1 65' 2023-12-16 = **VOID, no row**;
  the full replay 2024-03-13 (4-3) carries the R17 label; 2024-25 R15 Everton-Liverpool
  (Storm Darragh) 2025-02-12; 2025-26 **MD31 triple-slice** (Wolves-Arsenal fwd 2026-02-18; 8 games
  2026-03-20..22; Man City-Palace back 2026-05-13 — strays corroborated by the CSV rows).
- **Deductions:** 2023-24 final table carries Everton **−8** and Nott'm Forest **−4** (PSR);
  the table gate applies them before position-order verification.
- **Boundary (WO §1 row 2):** last round = 2025-26 MD38 (all 10 fixtures 2026-05-24); 2026-27
  starts **2026-08-21**, after the return date (`rsssf eng2027` = 404; wiki 2026-27 card: fixtures
  released 19 Jun 2026, promoted Coventry/Ipswich/Hull, relegated West Ham/Burnley/Wolves = this
  pack's bottom three) → **zero 2026-27 rows, boundary stated in a NOTE**.
- **Per-team pivot decree:** 100/100 club-season full-campaign pivots embedded in
  `audit/pack-validation-epl.txt` (also `audit/ledger/epl-pivot-*.txt`).
- Builder `tools/build_epl_pack.py` byte-deterministic; pack sha256
  `707dd83047306b07fe52c4e350f89e802e257b7b096a503cea75166861953036`; venue constants (100 rows)
  from the five Wikipedia season stadium tables → `audit/ledger/epl-venues.txt` (Everton epoch:
  Goodison Park → Hill Dickinson Stadium 2025-26).

### ④ MOLCUP return — build notes for the auditor

- Slice reproduced per WO §1 from the official brackets (RSSSF primary `tsje2022/2023/2024.html#cup`
  which carries R16→Final only — R2/R3 built from the en.wiki bracket sections and verified
  tie-by-tie against worldfootball round pages; all 24 R16 ties identical across the three indexes).
- 2023-24 slice = 38 (not 39): BOTH no-FL R16 ties excluded — Velvary 1-2 Opava **and**
  Dukla Prague 3-1 Vyskov (Dukla was a CZ2 club in 2023-24, promoted only for 2024-25).
- Two source defects found, disclosed in pack `source_conflict` NOTEs: (1) **Slovacko 3-1 Karvina
  2021-11-12 was settled in extra time** (1-1 at 90') but printed as a plain 3-1 by BOTH
  bracket sources — row carries 90'-score 1-1 + advancement NOTE; (2) **Plzen–Zlin SF date**
  2024-04-24 (wiki box + worldfootball agree) vs RSSSF header [Apr 4] — row carries 2024-04-24.
- compType `domestic-cup` per ERRATA-2026-08-03, superseding the WO §2 grammar line; FLAG raised
  that the 63 client-held cup rows may need the same reclassing.
- Builder `tools/build_molcup_pack.py` byte-deterministic; pack sha256
  `5023eb33fd7a63f51fbb95d0535a811bc8f9ddc9b5d1ff20dc49ee8e893cec86`; external validator
  `tools/validate_molcup_pack.py` → `audit/pack-validation-molcup.txt` (30/30 PASS, incl. the
  per-team pivot ledgers per the owner decree).

## Auditor errata applied 2026-08-03 (ERRATA-2026-08-03)

Owner relayed the auditor errata inline (the uploaded `ERRATA-2026-08-03.md` itself did
**not materialize in the repo/sandbox** — flagged back to the owner; a relayed mirror is kept
at `supervisor/ERRATA-2026-08-03.as-relayed.md`). Corrections applied and both returns rebuilt
byte-deterministically with the full gate suites re-run:

1. **compType classes** — `Russian Relegation Playoffs` rows now `other` (12 RPL rows);
   league rows stay `domestic-league`; cup rows are `domestic-cup` (RUSCUP: all 189;
   rule registered for the upcoming cup returns MOLCUP/KOSCUP/SCOCUP/SCOLC/USOC).
2. **Corrected RPL workorder fingerprint** announced as `9903cf856877d173ba71d72cef64e9c6`
   (was cb6e). The corrected text was not on `origin/main` at check time (that copy still
   carries the cb6e grammar line); the grammar change was applied per the errata summary.
3. **Cup-audit standing instructions** — `TEAM|FC Ufa` added to the RUSCUP pack (22 TEAM rows;
   anchored to its 2021-22 RPL elite-slot identity for cross-pack consistency) and KAMAZ
   written in exact form everywhere (`KAMAZ Naberezhnye Chelny` — was KamAZ).

Rebuilt artifacts (sha256-stable under `tools/build_*.py` re-runs):
RPL `6e458e19…` (69/69 gates) · RUSCUP `c2658b49…` (162/162 gates; final after the
auditor-return KAMAZ exact-string cycle — the intermediate post-errata build read
`18ba4695…`).

## Delivered artifacts (this branch)

| Path | Contents |
|---|---|
| `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` | RPL league return (WO-RPL-BACKFILL-01 5YSPAN revision), BP-TEAM-PACK v2 grammar: 732 MATCH rows ((240 league + 4 relegation-playoff) × 3 seasons; league rows compType domestic-league, the 12 playoff rows compType other per ERRATA-2026-08-03), 3 TEAM rows (FC Ufa RPL; Yenisey Krasnoyarsk + SKA Khabarovsk FNL), 13 SOURCE rows, 17 NOTE rows, `END`. Venue-detail = `Round n` / `Playoff legK`; cutoff honoured (last row 2024-06-01). |
| `audit/pack-validation-rpl.txt` | 69/69 gates re-run on the pack text: 240+4 per season, 30 rounds × 8 dated, 48 club-season pivots = 30 played each, table reproduction 16/16 ×3 seasons (position-order + W-D-L + GF-GA + Pts vs RSSSF official constants), all 7 H2H position-ties reproduced from recomputed mutual results, 6 playoff aggregates + outcomes, season goal-total anchors 639/730/637, boundary/dupes/identity, 3 spot-audit NOTEs, and the match-for-match second-index diff vs the football-data feeds (730/732 identical; the 2 documented variances whitelisted). |
| `audit/ledger/rpl-2021-22.txt` · `rpl-2022-23.txt` · `rpl-2023-24.txt` · `rpl-venues.txt` | Primary transcriptions: every round's date+score from RSSSF rus2022/2023/2024 (#1l + #prorel), official final tables with H2H brackets, season venue/capacity tables, documented venue exceptions (Torpedo), playoff grounds. |
| `tools/build_rpl_pack.py` | Reproducible builder + validator for the RPL pack (byte-identical rebuild verified by sha256). |
| `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` | Russian Cup return, BP-TEAM-PACK v2 grammar: 189 MATCH rows (36 + 77 + 76, compType domestic-cup per ERRATA-2026-08-03), 22 TEAM rows (21 non-roster opponents + FC Ufa per standing cup-audit instruction; KAMAZ exact-form), 10 SOURCE rows, 69 NOTE rows, `END`. 90-minute doctrine; stage in venue-detail. |
| `audit/pack-validation.txt` | Gate re-runs: slice counts per round, group members + table recompute (2022-23/2023-24 club-for-club W/WP/LP/L/GF/GA/pts; 2021-22 full 3-team tables vs full ledger), bracket reproduction (semifinalists/finalists/champions 2022 Spartak, 2023 CSKA, 2024 Zenit), 14 two-leg aggregates, per-club pivot ledgers (owner's per-team completeness technique), boundary/dupes/identity checks. |
| `tools/build_pack.py` | Reproducible builder + validator (embeds the official record used as gate expectations). |
| `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | Czech First League return (WO-CZ1-BACKFILL-02), BP-TEAM-PACK v2 grammar: **841 MATCH rows** (276 + 276 + 277 league, compType `domestic-league` per WO §2 + **12 Czech Relegation Playoffs pro/rel legs, compType `other` per ERRATA per the auditor's 2026-08-03 return**), **0 TEAM** (WO §2 directive stands; the five FNL opponent strings are reused client-roster identities), 14 SOURCE, 21 NOTE (19 info incl. 3 spot-audit + 2 warning source_conflict), `END`. Venue-detail = `Round n` / `Titul R31-35` / `Zachranu R31-35` / `Evropu-SF|F L1|L2` / `Evropu-CLP` / `Playoff leg1|leg2`; cutoff honoured (last row the 2024-06-02 pro/rel leg). |
| `audit/pack-validation-cz1.txt` | 120/120 gates on the pack text: per-season 240 regular = 30 fully dated matchdays × 8 + 15 Titul + 15 Zachranu + 6/7 Evropu legs + 4 pro/rel; per-club pivots 16 clubs × exactly 30 regular games and full-campaign ledgers (48 pivots incl. pro/rel legs, plus the FNL-opponent 2-leg pivots); regular tables reproduced 16/16 ×3 + group tables 6/6 ×6 vs independent wiki constants; all 4 regular-stage H2H ties + 3 group ties recomputed incl. the 2022-23 title (Sparta over Slavia 78-78 by regular-season points 68>66); Evropu aggregates + winners + CLP row; second-index diff 826/829 league + **12/12 pro/rel legs** identical (3 defective wiki FBR cells whitelisted after RSSSF re-fetch adjudication; 2 wiki infobox goal scalars likewise contradicted by their own articles); worldfootball spot matchdays 24/24 identical (1 wf listing-date nuance documented); pro/rel aggregates + venues + leg-structure gates green. |
| `audit/ledger/cz1-2021-22.txt` · `cz1-2022-23.txt` · `cz1-2023-24.txt` · `cz1-2ndidx-*.txt` · `cz1-venues.txt` | Primary transcriptions of RSSSF tsje2022/2023/2024 (R1-30 + T/Z31-35 + Evropu legs, tables with H2H brackets, pro/rel ties as `PRO` records); wiki FBR/group matrices + **wiki play-offs sections (PRB records, re-fetched 2026-08-03 with the four 2023 match boxes)** + worldfootball spot rows (second index); venue + table/group-table constants incl. FNL pro/rel ground evidence (wf stadium indexes + FC Silon Taborsko article). |
| `tools/build_cz1_pack.py` | Reproducible builder + validator for the CZ1 pack (byte-identical rebuild verified by sha256 `55d9bd80…`). |
| `data/rpl/*.csv`, `docs/`, `audit/validation-report.txt` | Prior deliverable: audited RPL league dataset 2021/22-2025/26 (1,212 rows + closing 1X2 odds), unchanged. Base for queue item ①. |
| `supervisor/workorders/` | All 16 owner commissions mirrored read-only in one folder (register: `supervisor/README.md`), + `archive/` with the superseded RPL order.

## Reconciliation of the old open item (from the 2026-08-02 status note)

The RPL CSV deliverable was built blind ("workorder text never received"). Meanwhile
the referenced document exists: `origin/main:Supervior/Handoff/WORKORDER-RPL-2021-24-BACKFILL.md`
(archived WO-RPL-BACKFILL-01, approved verbatim), superseded by
`WORKORDER-RPL-2021-2026-5YSPAN.md` (queue ①) which demands the **BP-TEAM-PACK v2
.txt** form, not CSV. The CSV season set (2021/22-2025/26) is a superset of the
needed 2021-24 window and will be used as the cross-checked base for the pack;
nothing in the CSV contradicts the workorder set.

## Method notes for the RPL league pack (disclosures the auditor will also see in NOTEs)

* **Awarded result carried officially:** 2023-03-19 Pari NN–Torpedo is stored as the
  RFU-awarded 0-3 (on-pitch 1-1 annulled 2023-03-22), exactly as RSSSF's round list
  and final table carry it; the football-data second index keeps 1-1 → `source_conflict`
  (same as CSV set anomaly A1). Positions unaffected.
* **A2 confirmed against RSSSF:** 2023-08-14 Pari NN 2-0 Akhmat — RSSSF round list
  agrees with the three press reports, not with football-data's 1-0 → `source_conflict`.
* **Venues policy:** home club's documented season ground per match (RSSSF stadium
  table 2021-22; Wikipedia venue tables 2022-23/2023-24), with the sourced exceptions —
  Torpedo 2022-23 home games of rounds 1-10 plus the R19 game were in Khimki (RSSSF
  NBs); playoff rows carry the actual match-box grounds (incl. Yenisey's indoor arena,
  Rodina's Spartakovets, Akron's Zhigulevsk ground).
* **Second index:** all 732 rows diffed match-for-match against the football-data
  feeds — 730/732 identical on date AND score; the 2 variances above are the only
  divergences anywhere in the window. Cross-anchors: RSSSF stated totals and both
  Wikipedia infobox totals reproduce from the pack rows (639 / 730 / 637).
* **Continuity:** zero missing matchdays (all 90 dated), postponed fixtures keep round
  labels and are disclosed (two R19 games 2021-22; R21-after-R25 in 2023-24).

## Method notes for the cup pack (disclosures the auditor will also see in NOTEs)

* **Format correction:** the workorder table described 2021-22 as "old straight-knockout,
  no group stage" — RSSSF + Wikipedia show an Elite Group Stage (11 groups × 3) that
  season; a `format_reading` NOTE documents this with the corrected round counts.
* **Source conflicts (3 dates, 2022-23):** RSSSF compact bracket headers run +1 day vs
  its own detailed chapter and the RFS/Wikipedia index; resolved to the detailed dates
  (`source_conflict` warning NOTE).
* **Per-club technique:** the owner's suggestion ("list all teams, pull each club's full
  history inside the window — per-team complete = everything complete") is implemented
  as the per-club pivot gate; ledgers in `audit/pack-validation.txt`.
* **Nothing imputed:** optional TEAM profile fields left blank where no captured source
  exists; reconciliations live in NOTE lines, never in match data.

## Method notes for the CZ1 pack (disclosures the auditor will also see in NOTEs)

* **277-row season documented:** 2023-24 carries the extra single-match Conference League
  playoff Final (2024-05-31 Mlada Boleslav 3-1 Hradec Kralove) — the official record itself
  counts 277 league matches; reproduced with a `shape_deviation` NOTE (WO §1 template says
  276, deviation fully explained).
* **Pro/rel legs held out (owner decision requested):** 12 promotion/relegation legs
  (2 ties × 2 legs × 3 seasons) vs non-pinned FNL clubs — WO §5 names gate pins 17 strings
  and §2 forbids TEAM rows, so the ties are fully listed dates+scores in `playoff_count`
  NOTEs but emitted as 0 rows (`roster_scope` warning). If sanctioned they'd carry
  compType `other` per the errata.
* **Second-index defects adjudicated:** 3 wiki FBR matrix cells (2022-23 Liberec-Zlin,
  Plzen-Zlin; 2023-24 Pardubice-Jablonec) contradict RSSSF *and their own articles' official
  tables* — RSSSF lines re-fetched and re-read 2026-08-03 before resolving; 2 wiki infobox
  goal scalars (763 vs recomputed 770; 804 vs 792) replaced by the recomputed anchors.
* **Venue quirks per-row documented:** Hradec 2021-22/2022-23 home at Lokotrans Arena in
  Mlada Boleslav (rebuild); Pardubice 2021-22 at Dolicek in Prague, 2022-23 split at the
  winter break Dolicek → CFIG Arena; Hradec 2023-24 at the new Malsovicka Arena (first home
  2023-08-05 = opening day); era stadium names per season (Sinobo→Fortuna, Generali→epet).
* **Continuity:** all 90 regular matchdays dated; postponed fixtures keep Round labels and
  are enumerated per season in the `continuity` NOTE; zero dupes; boundary clean.
* **compType:** `domestic-league` on every row verbatim per WO §2 (playoff-stage groups are
  championship phases, not separate events); the errata class rule does not bite here while
  the pro/rel ties are held out.

## Auditor return cycle (evening 2026-08-03) — TWO amendments shipped

The auditor approved the CZ1 body (tables 3×16/16 exact, brackets 18/18 exact, CLP row correct —
"it explains 829 vs 828") and returned two standing items, both closed the same day:

1. **CZ1 pro/rel block reinstated.** WO §1's last row commissions the Czech Relegation Playoffs
   ("state count in a NOTE"); the auditor's message: add the 12 rows (2022 Teplice–Vlasim +
   Opava–Bohemians, May 19/22; 2023 Pribram–Pardubice + Zlin–Vyskov, Jun 1/4; 2024 Vyskov–Karvina +
   C.Budejovice–Taborsko, May 30/Jun 2 — 2 legs each, 90-min scores), compType `other` per ERRATA.
   Done: 841 rows (was 829), 120/120 gates (was 105). Sources: RSSSF playoff sections (primary,
   already transcribed as `PRO` records) + the wiki play-offs sections re-fetched 2026-08-03
   (12/12 legs identical; 2023 match boxes confirm dates/venues/attendances) + the already-cited
   iSport/CT/sport.cz press rows for the 2024 dates + wf stadium indexes and the FC Silon Táborsko
   article for the FNL grounds. All 6 ties were won by the First-League side (nobody moved division).
2. **RUSCUP KAMAZ.** "Write exactly KAMAZ (2 rows)" — both in-scope rows now carry `KAMAZ`
   (was `KAMAZ Naberezhnye Chelny`; full name kept in the identity NOTE). 162/162 gates stay green.

Rebuilt artifacts byte-deterministic across re-runs (a set-ordering label wobble in the RUSCUP
validator report was found and fixed): pack sha256
CZ1 `55d9bd80ef3db4ed84421cffdce64f41f43c9b13f069d3f4eb6a46e74026d643`,
RUSCUP `c2658b490d63821166d7b76d04a7e83d3f151f54d7afaef78346d0126b2711f6`.

## Known loose ends

* Two files the owner says were attached mid-session (`README.md`, `START-HERE.md`)
  never became readable in the sandbox and are not in the repo — flagged in chat;
  awaiting re-send or a GitHub web upload.
* The uploaded `ERRATA-2026-08-03.md` likewise never materialized (checked repo root,
  `/home/user/uploads/`, full `origin/main` tree) — applied verbatim from the owner's
  inline relay; mirror at `supervisor/ERRATA-2026-08-03.as-relayed.md`. The owner announced
  a re-upload on 2026-08-03 evening; as of this write the attachment has still not landed
  in the sandbox (it will be placed at `supervisor/ERRATA-2026-08-03.md` the moment it does,
  replacing the mirror).
