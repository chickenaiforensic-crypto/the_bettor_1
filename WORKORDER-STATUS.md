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
| ② | **WO-CZ1-BACKFILL-02** — Czech First League 2021-22 → 2023-24 | `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03, amended same-day on the auditor's return (body approved: tables 3×16/16, brackets 18/18, CLP row) — 841 rows (276+276+277 league + 12 Czech Relegation Playoffs pro/rel legs, compType `other` per ERRATA), all 120 self-gates PASS** · **FULL SPAN per DECREE-2026-08-04 DELIVERED 2026-08-04 — 1,401 rows (five seasons + 20 pro/rel legs), all 175 self-gates PASS, sha `cbd5710b…`** |
| ④ | **WO-MOLCUP-BACKFILL-04** — MOLCUP (Czech MOL Cup) 2021-22 → 2025-26 (full span per OVERRIDE decree) | `handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 (3 seasons) + FULL-SPAN OVERRIDE 2026-08-04 — 202 rows (41+41+38+41+41 per the WO-§1 slice; compType `domestic-cup` per errata), 43 TEAM, 33 advancement NOTEs, all 32 external gates PASS, sha `50ead762…` double-rebuild identical. 2026-27 = boundary NOTE (zero rows, season incomplete)** |
| ⑤ | **WO-EPL-SPAN-12** — England Premier League 2021-22 → 2025-26 (+ 2026-27 boundary) | `handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 1,900 rows (380 ×5, `domestic-league`, `MD<n>` venue-detail), 0 TEAM (27 roster strings verbatim), 17 SOURCE / 17 NOTE, all 83 self-gates PASS** (the register's earlier "WO-EPL-BACKFILL-05 (2021-22 → 2023-24)" id is stale — the governing card on `origin/main` is the 5-year-span order; scope covered through today per its §0 no-cutoff note) |
| ⑥ | **WO-FRA-SPAN-16** — France Ligue 1 2021-22 → 2025-26 (+ 2026-27 boundary) | `handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED (FULL SPAN per DECREE-2026-08-04) 2026-08-04 — 1,686 rows (1,678 league 380+380+306+306+306 — 20→18 club shrink applied — + 8 France Relegation Playoffs pro/rel legs compType `other` per ERRATA; 90-min doctrine on the two aet legs), 0 TEAM (26 roster strings verbatim incl. the `Paris SG`/`St Etienne` traps), 19 SOURCE / 22 NOTE, all 85 self-gates PASS, sha `44fe06b5…` double-rebuild identical** |
| ⑦ | **WO-GER-SPAN-15** — Germany Bundesliga 2021-22 → 2025-26 (+ 2026-27 boundary) | `handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED (FULL SPAN per DECREE-2026-08-04) 2026-08-05 — 1,540 rows (1,530 league 306×5 — 18 clubs/34 MDs per its card — + 10 Germany Relegation Playoffs pro/rel legs compType `other` per ERRATA superseding the WO's playoff-out line; 90-min doctrine on the two ET legs), 3 TEAM (PO participants Fortuna Dusseldorf / SV Elversberg / SC Paderborn registered — WO section-3 covers league rows only), 21 SOURCE / 25 NOTE, all 93 self-gates PASS, sha `4f90ddb1…` double-rebuild identical. Second indexes 306/306 ×4 + wiki matrix 306/306 (990 goals both); two source_conflict NOTEs (RSSSF round-date misprint clusters adjudicated on two independents each); 2026-27 starts 2026-08-28 → zero rows (duit2027 404)** |
| ⑧ | **WO-ITA-SPAN-14** — Italy Serie A 2021-22 → 2025-26 (+ 2026-27 boundary) | `handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED (FULL SPAN per DECREE-2026-08-04) 2026-08-05 — 1,901 rows (1,900 league 380×5 — 20 clubs/38 MDs per the WO's 20/38 shape — + 1 'Italy Relegation Playoffs' row compType `other`: the 2022-23 relegation spareggio Spezia 1-3 Verona 2023-06-11, the single pro/rel decider touching the top flight in-window; the WO's conditioned spareggio clause fired exactly once), 0 TEAM (union = the 27 pinned roster strings exactly; spareggio participants are pins), 20 SOURCE / 23 NOTE, all 92 self-gates PASS, sha `e808c9f8…` double-rebuild identical. Second indexes: OFB diffs 380/380 ×3 + 379/380 with the quadruple-corroborated OFB-side MD30 Torino 0-0 Monza typo (RSSSF's 1-0 stands), wiki matrix 2025-26 380/380 (922 goals both); two source_conflict NOTEs (RSSSF 2022-23 R9 '[Oct 1]' date misprint adjudicated on two independents; OFB MD30 defect quarantined); Juventus 2022-23 FIGC −10 deduction arithmetic gated 71−10=61; abandonment doctrine (Ndicka R32, Bove R14 completions); Perth-cancelled Milan–Como ships 2026-02-18 at San Siro; 2026-27 starts 2026-08-23 → zero rows (ital2027 404)** |
| ⑨→ | KOS, KOSCUP, MLS, SCO1, SCOCUP, SCOLC, SPA, USOC | packs | QUEUED (workorder texts on `origin/main`); cups run `domestic-cup`; **⑨ KOS starts only after the owner's ITA touch-base** |
| **OVERRIDE** | **DECREE-2026-08-04 full-span override** (owner verbatim in `supervisor/DECREE-2026-08-04-full-span-override.md`) | — | **GOVERNING: full seasons 2021 → today, workorder cutoffs rescinded, packs = single source of truth vs error-containing old data. Russia first.** |

### OVERRIDE — Russia full-span extension (**DELIVERED 2026-08-04**)

Full-span rebuilds shipped under DECREE-2026-08-04 (workorder 2024-06-30 cutoffs rescinded; packs = single source of truth the legacy CSVs are audited against):

| Pack | Rows | Gates | sha256 | Contents |
|---|---|---|---|---|
| **RPL** (supersedes `6e458e19…`) | **1,220** ((240 league + 4 playoff legs) ×5; compType `domestic-league` / playoffs `other` per errata) | **95/95** | `d71ed24f3a321d6c2975bbff46a6ee405066a79870b4d158b6f5781c6ec9db79` | all five seasons 2021-22 → 2025-26 end-to-end; 2026-27 played rounds (R1+R2) ship in the **RUS-ADDENDUM companion pack below** per ADDENDUM-2026-08-04 REQ-2 rolling-append (this pin unchanged) |
| **RUSCUP** (supersedes `c2658b49…`) | **341** (36+77+76+76+76, auditor-proven RPL-slice) | **258/258** | `f89501cf25e10389e175579ef1a38105b5b02bde78a83362a65c1bb4a173db91` | all five seasons 2021-22 → 2025-26; 2026-27 Regions-path R1 (11 ties, zero RPL by design) documented, zero rows |
| **RUS-ADDENDUM** (supervisor/ADDENDUM-2026-08-04-RUSSIA-GAPS REQ-2+REQ-3; SPEC-2026-08-04 items 1+3) | **18** (RPL 2026-27 Round 1 ×8 `domestic-league` + Round 2 ×8 `domestic-league`; Russian Super Cup 2025 + 2026 ×2 `domestic-cup`) | **16/16** | `30576ac4894930b359db19193f08f05cd3f399ecd7d97f9975184ac02386dcea` | rolling-append to date 2026-08-04 (last played 2026-08-02; Round 3 starts 2026-08-08, zero rows); pins RPL `d71ed24f…` / RUSCUP `f89501cf…` untouched |

- **Ledgers** (all committed, recomputed at transcription): `rpl-2024-25.txt` EXACT 648/648, 16/16; `rpl-2025-26.txt` EXACT 609/609, 16/16; `cup-2024-25.txt` + `cup-2025-26.txt` 76/76 each with stage-histogram exact; champions Krasnodar/Zenit (league) and CSKA/Spartak (cup Superfinals, both on pens at Luzhniki).
- **Second index** (feed discontinuation handled): fdata Russia 404 both new seasons + openfootball/russia 404 → replacement lattice = Wikipedia FBR matrices **240/240 score-identical both league seasons** (`tools/diff_rpl_matrix.py`, matrix-recomputed tables 16/16 vs official, goals 648/609 anchors); wiki cup articles + RFS official match pages **152/152 identical** on the new cup rows (341/341 span-wide); worldfootball MD30-2425 third anchor 8/8 exact.
- **Adjudicated findings shipped in pack NOTEs**: 3 RSSSF group-table print errors (corroborated by RFU-sourced wiki tables; rows unaffected): 2024-25 Dynamo Moscow pts 8→**11**; 2025-26 Akhmat GF-GA 7-8→**8-10**; 2025-26 Lokomotiv GA 2→**4**. 2025-26 Arsenal Tula-Rubin venue/date conflict resolved to 2025-11-25 Arsenal Stadium per RFS 56055 + wiki box (two independent indexes vs RSSSF cupdet Khimki-tag); Arsenal's later Loko tie genuinely at Arena Khimki (RFS 56059).
- **Venue lattice** (clipboarded in `audit/ledger/rpl-venues.txt` VENUE/POV/EXCEPTION lines): Krasnodar Stadium→Ozon Arena mid-season R27 boundary; Fakel Stadium new ground (R27 one-off back at CTU Stadium; R23 behind closed doors att 0); Rubin R12 staged Nizhny Novgorod; Pari NN 2025-26 renovation groundshares (Kazan/Grozny/Saransk map R1-R9) + SovComBank Arena era R12+; Akron R13 staged Saransk; Anzhi Arena Kaspiysk; Solidarnost share; Rostech Arena era; playoff boxes incl. Rotor Volgograd Arena.
- **Membership governance** (RFU refs in pack NOTE): Khimki license denial 2025-05-24 (rfs.ru 222413) → Pari NN reinstated 2025-06-16 (222586; NOT relegated despite playoff loss); Torpedo excluded 2025-07-10 match-fixing (premierliga.ru 32356) → Orenburg reinstated 2025-07-11 (222692).
- Builders extended and byte-deterministic (double rebuild identical): `tools/build_rpl_pack.py` (5 seasons), `tools/build_pack.py` (5 seasons). Validation/pivots: `audit/pack-validation-rpl.txt` (80 club-season pivots), `audit/pack-validation.txt` (80 cup pivots). Legacy `data/rpl/*.csv` untouched (old data under audit).

### OVERRIDE — CZ1 full-span extension (**DELIVERED 2026-08-04**)

Second federation extended under DECREE-2026-08-04 (owner: "go back to the russian leagues and complete the
extra years … and any other league" — Russia first shipped, Czech First League immediately after):

| Pack | Rows | Gates | sha256 | Contents |
|---|---|---|---|---|
| **CZ1** (supersedes `55d9bd80…`) | **1,401** (276+276+277+276+276 league + 20 Czech Relegation Playoffs pro/rel legs compType `other` per errata) | **175/175** | `cbd5710ba24b8f819cadcdff015199d34391afba0041c2935569604e1a390a6e` | all five seasons 2021-22 → 2025-26 end-to-end; 2026-27 = boundary NOTE, zero rows (tsje2027 404, page not started; BBC fixture menu shows R1 scheduled 2026-08-07..09, after the 2026-08-04 return date) |

- **Build method per season:** 2024-25 transcribed from RSSSF tsje2025 (fetch day 2026-08-04) and verified EXACT (recompute: RT 16/16, TT/ZT 6/6+6/6, 627 regular goals; span 2024-07-19..2025-06-01). 2025-26 needed the page-form adaptation (RSSSF tsje2026 prints tables + playoff legs only — same class as the EPL 2025-26 return): the 270 league-stage rows were assembled from the **BBC dated month lattice** (12 month pages, 276 D-rows in `audit/ledger/cz1-dates-bbc-2025-2026.txt`) **× wiki FBR matrices** under `tools/build_cz1_2526_ledger.py` gates V1..V6 — BBC↔wiki cell bijection 270/270, recompute == RSSSF constants EXACT (16/16 + 6/6 + 6/6; 623 regular goals).
- **Second index:** staged MX grammar (`cz1-2ndidx-2024-25.txt` / `cz1-2ndidx-2025-26.txt`, 280 rows each = wiki FBR + group matrices + Evropu bracket + pro/rel TwoLeg boxes); `tools/diff_cz1_matrix.py` 280/280 score-identical vs the ledger both seasons (gate caught + fixed 3 MX transcription inversions). worldfootball dropped Czech coverage from 2024-25 (cze-* roots 404; ESPN cze.1 API empty) → the fixed-matchday spot-audit is documented n/a on the two new seasons and replaced by strictly stronger full-depth diffs.
- **Identity/scope:** all 17 pinned strings + `Dukla Prague` on 2024-25/2025-26 rows (anti-appear retired with the rescinded 3-season window); FNL pro/rel universe grows to 7 strings (Vlasim, Opava, Pribram, Vyskov, Taborsko, **Chrudim, Artis Brno**); 2024-25 Vyskov–Dukla settled by **pens 4-2** after 1-1 agg/aet (row scores stay the played 0-0/1-1; gate handles the decider); Artis Brno ground = Mestsky fotbalovy stadion Srbska, Brno (en.wiki SK Artis Brno infobox, fetched this build).
- **Findings shipped in pack NOTEs (all disclosed, nothing silently fixed):** 2026-05-09 T32 Prague derby **walkover** — abandoned 3-2 Slavia in stoppage time (fans on pitch; iDNES/Reuters), LFA awarded **0-3 Sparta** 2026-05-12 — the row carries the official 0-3 (`match_awarded`); 3 unicode-minus corrupted wiki Zachranu-matrix cells adjudicated 2-0/0-3/2-0 via BBC + arithmetic closure (`source_conflict`); RSSSF tsje2026 Zachranu position column misprint 13/13/15/14 (`print_error`); **Karvina incident** — 2025-26 cup winner + Evropu finalist administratively demoted after match-fixing accusations, Artis Brno (pro/rel playoff loser vs Slovacko 1-7 agg) promoted in its place, Karvina's Europa waiver (`karvina_incident`); Dukla 6-0 H2H over Slovacko at 23 adjudicated by wiki hth_DUK note (RSSSF prints no bracket).
- Validation: `audit/pack-validation-cz1.txt` (80 club-season pivots + 7 FNL 2-leg pivots; group constants reproduced 4 new tables incl. the 2024-25 Titul 63-63 title-path tie Sparta over Jablonec by regular points 62>51). Builder `tools/build_cz1_pack.py` (5 seasons) double-rebuild byte-identical → sha above.

### Closure confirmation (2026-08-04, owner request: "mark Russia + completed as closed")

Re-verified fresh this date — every delivered builder re-run **byte-identical** (two passes each),
all gates re-green:

| Pack | Rows | Gates | sha256 (prefix) | Span architecture per its workorder |
|---|---|---|---|---|
| RUSCUP | 189 | 162/162 | `c2658b49…` | 2021-22/22-23/23-24 delivered here (36+77+76 auditor-proven RPL-slice); 2024-25 + 2025-26 (76 rows each) held + auditor-verified client-side per WO §1; current season fills centrally |
| RPL | 732 | 69/69 | `6e458e19…` | 2021-22/22-23/23-24 delivered here (240 league + 4 playoff legs each); 2024-25 + 2025-26 (240/240 each) held client-side per WO preamble; 2026-27 in progress via central requests |
| CZ1 | 841 | 120/120 | `55d9bd80…` | same segment architecture (2021→2024 delivered; later seasons held client-side per the segment commission) — **superseded later this date by the DECREE-2026-08-04 full-span delivery: 1,401 rows, 175/175 gates, sha `cbd5710b…`** |
| MOLCUP | 202 | 32/32 | `50ead762…` | 2021-22..2025-26 full-span override delivered (41+41+38+41+41); 2026-27 boundary NOTE |
| EPL | 1,900 | 83/83 | `707dd830…` | **full span, no cutoff** — all five seasons 2021-22 → 2025-26 delivered here; 2026-27 boundary proven to start 2026-08-21 (after the return date) = zero rows by rule |

Nothing is outstanding on the researcher side for Russia or any delivered federation; the
gap-free whole-span certification (delivered segment + held seasons + central feed) and the
§6 owner approval happen owner-side, exactly as the workorders prescribe. All work pushed
to `origin/arena/019fc462-the-bettor-1` (tip `06a76f5` + the doc fixes of this entry).

**Update later the same date:** the RPL and RUSCUP rows above were superseded by the
DECREE-2026-08-04 full-span delivery (see the OVERRIDE block top of file): RPL → 1,220 rows
sha `d71ed24f…`, RUSCUP → 341 rows sha `f89501cf…`, both green (95/95 and 258/258 gates).

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

### ④ MOLCUP return — OVERRIDE-MOLCUP build notes (full-span decree 2026-08-04)

- Extended to the complete 5-season span 2021-22 → 2025-26 (Decree; the workorder's 2024-06-30
  cutoff and the '32+31 rows held client-side' note are rescinded; this pack is now the single
  source of truth). 202 MATCH rows = 41+41+38+41+41; champions: Slovacko 2022, Slavia 2023,
  Sparta 2024, **Sigma Olomouc 2025** (3-1 Sparta, Andruv stadion), **Karvina 2026** (3-1
  Jablonec, Malsovicka Arena) — Karvina's cup win in its match-fixing-sanction season is
  cross-referenced to the CZ1 pack `karvina_incident` NOTE (`integrity_flag`).
- Source coverage parity changed across the span (raw-fact, disclosed): RSSSF carries the cup
  from R16 on the 2021-24 pages but **from R3 (with dates) on the 2024-25/2025-26 pages**; R2 of
  every season = en.wiki raw bracket sections (27/27/27/27/26 ties) verified tie-by-tie vs
  worldfootball (diff 0 after one documented wiki typo: Rokycany 0-1 vs proven 0-6,
  `source_conflict` NOTE; wf match report ma11538503 six-goal timeline).
- Czech aet convention changed starting 2024-25: extra time now appears at R2/R3/R16 level
  (Taborsko-CBU R3, Slavia-Taborsko R16, Plzen-Zlin R16, Frydek-Pardubice R3, Trinec-Hradec R3,
  Artis-Liberec aet→pens R3, Pardubice-Ostrava R16) — all 13 extension settled ties carry
  90-minute doctrine rows + advancement NOTEs (33 total), timelines per wf reports.
- 12 new lower-league TEAM rows (tier + ground evidence ledgered): Usti nad Orlici, Milin,
  Aritma, Povltavska, Kurim, Bzenec, Ceska Lipa, Hodonin, Bohumin, Brandys nad Labem, Hranice,
  and the **Artis Brno** rename row (SK Lisen 2019 lineage; era-era rows: `Lisen` 2024-25 at
  Stadion SK Lisen, `Artis Brno` 2025-26 homes staged at **ShipEx Arena** = the sponsored Srbska
  ground, proven by per-tie reports ma11584736/ma11651261 — not by inference).
- POV venue exceptions proven per-tie: Povltavska v Liberec played at **Stadion Stechovice**
  (ma10704494); Ceska Lipa v Pardubice at **TJ Stadion Novy Bor** (ma11538494); Uhersky Brod v
  Jablonec at **Stadion Lapac** (ma10744100), Loko Praha v Hradec at **Stadion na Plynarne**
  (ma10744109); Pardubice R16 carried as CFIG Arena with the wf 'Stadion Arnosta Kostala'
  sponsor-lapse alias documented.
- FL memberships: 2024-25 = 2023-24 minus Zlin plus **Dukla Prague**; 2025-26 = minus
  Ceske Budejovice plus **Zlin** (so Kladno 2-3 CBU has no FL club → out of slice; Opava 1-2
  Zlin FNL-FNL out in 2024-25; Opava-Zlin's successor tie Plzen-Zlin stays in on Plzen's side).
- New slice counts: 2024-25 = 41 (R2 11/27, R3 15/16, R16 8, QF 4, SF 2, F 1);
  2025-26 = 41 (R2 10/26, R3 16/16, R16 8, QF 4, SF 2, F 1). 2026-27 = boundary NOTE, zero rows.
- Builder extended to 5 seasons byte-deterministic; pack sha256
  `50ead762d80070dce6cbf468dedd26eb4d4e3706dd264801194af49385791137` (double-rebuild identical);
  external validator v5 → `audit/pack-validation-molcup.txt` (**32/32 PASS**, incl. pivot
  ledgers over 18 pinned strings × 5 seasons).

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
| `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | Czech First League return (WO-CZ1-BACKFILL-02 + DECREE-2026-08-04 full-span override), BP-TEAM-PACK v2 grammar: **1,401 MATCH rows** (276 + 276 + 277 + 276 + 276 league, compType `domestic-league` per WO §2 + **20 Czech Relegation Playoffs pro/rel legs, compType `other` per ERRATA**), **0 TEAM** (WO §2 directive stands; 17 pinned strings + Dukla Prague on its two seasons; the seven FNL opponent strings are reused client-roster identities), 21 SOURCE, 27 NOTE (21 info incl. 5 spot-audit + 6 warning: source_conflict ×3, print_error, match_awarded, karvina_incident), `END`. Venue-detail = `Round n` / `Titul R31-35` / `Zachranu R31-35` / `Evropu-SF|F L1|L2` / `Evropu-CLP` / `Playoff leg1|leg2`; full span through 2026-05-31 (last pro/rel leg), zero 2026-27 rows (boundary NOTE). |
| `audit/pack-validation-cz1.txt` | 175/175 gates on the pack text: per-season 240 regular = 30 fully dated matchdays × 8 + 15 Titul + 15 Zachranu + 6/7 Evropu legs + 4 pro/rel; per-club pivots 16 clubs × exactly 30 regular games and full-campaign ledgers (**80 club-season pivots** incl. pro/rel legs, plus the seven FNL-opponent 2-leg pivots); regular tables reproduced 16/16 ×5 + group tables 6/6 ×10 vs independent constants; all 8 regular-stage H2H ties + 4 group ties recomputed incl. the 2022-23 title (Sparta over Slavia 78-78 by regular-season points 68>66) and the 2024-25 Titul 63-63 (Sparta over Jablonec by regular points 62>51); Evropu aggregates + winners + CLP row; second-index diff 1,378/1,381 league + **20/20 pro/rel legs** identical (3 defective wiki FBR cells whitelisted after RSSSF re-fetch adjudication; 2 wiki infobox goal scalars; 3 unicode-minus corrupted Z cells adjudicated identically in both indexes); worldfootball spot matchdays 24/24 identical on 2021-24 (n/a documented for the new seasons; 2025-26 BBC lattice bijection 270/270); pro/rel aggregates + venues + leg-structure gates green incl. the Dukla pens-4-2 decider. |
| `audit/ledger/cz1-2021-22.txt` … `cz1-2025-26.txt` · `cz1-2ndidx-*.txt` · `cz1-dates-bbc-2025-2026.txt` · `cz1-venues.txt` | Primary transcriptions of RSSSF tsje2022/…/2026 (R1-30 + T/Z31-35 + Evropu legs, tables with H2H brackets, pro/rel ties as `PRO` records; 2025-26 table-form → rows assembled from the BBC dated month lattice `cz1-dates-bbc-2025-2026.txt` (276 D-rows) + wiki matrices under `tools/build_cz1_2526_ledger.py` V1..V6, recompute == RSSSF constants EXACT); wiki FBR/group matrices + play-offs sections (PRB / staged MX records) + worldfootball spot rows 2021-24 (second index); venue + table/group-table constants for all five seasons incl. FNL pro/rel ground evidence (Chrudim Za Vodojemem, Artis Brno Srbska per en.wiki infoboxes). |
| `tools/build_cz1_pack.py` (5 seasons) · `tools/build_cz1_2526_ledger.py` · `tools/diff_cz1_matrix.py` | Reproducible builder + validator for the CZ1 pack (byte-identical rebuild verified by sha256 `cbd5710b…`); 2025-26 ledger assembler under V1..V6 gates; staged-MX second-index differ (280/280 both new seasons). |
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
