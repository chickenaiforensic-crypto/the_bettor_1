# the_bettor_1

**Audited football match dataset — Russian football first: the 5-year-span audit programme (2021-07 → today).**
Every return is a **verbatim extract** from fetched sources with a full audit trail — no invented, repaired or
back-filled values. Where the source is silent, the artefact is silent (documented), and every known source-side
defect is flagged with cross-checks instead of being silently "fixed".

## Folder structure

```
supervisor/          ← owner commissions, read-only mirrors (workorder register in supervisor/README.md)
  workorders/        ← all 16 five-year-span workorders + archive/ (superseded RPL WO)
handoffs/            ← return artifacts, ONE text file each (BP-TEAM-PACK v2, .txt only)
data/rpl/            ← audited RPL league CSV dataset 2021/22–2025/26 (1,212 rows + closing 1X2 odds)
docs/                ← audit trail, data dictionary, per-season notes
audit/               ← machine validation output (pack gates, CSV validation, ledger transcriptions)
tools/               ← reproducible builder/validator scripts
WORKORDER-STATUS.md  ← live queue register and reconciliation notes
```

## Delivered returns

| Return | Artifact | Verification |
|---|---|---|
| **Russian Premier League 2021-22 → 2025-26 FULL SPAN** (WO-RPL-BACKFILL-01, returned 2026-08-03, re-issued under errata ERRATA-2026-08-03; **extended full-span 2026-08-04 under owner override DECREE-2026-08-04 — cutoff rescinded; supersedes sha `6e458e19…`**) | `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` — **1,220 MATCH rows** ((240 league, compType `domestic-league` + 4 playoff, compType `other` per errata) ×5), 4 TEAM (Rotor Volgograd added) / 16 SOURCE / 22 NOTE, `END`; 2026-27 played rounds (R1+R2) ship in the RUS-ADDENDUM companion pack (rolling per REQ-2; this pin unchanged) | `audit/pack-validation-rpl.txt` — **95/95 gates PASS** (round counts 240×5 + 20 playoff legs, final tables 16/16 ×5 vs RSSSF official incl. all H2H ties recomputed (2024-25 DMh-over-Khimki bracket at 29), 10 playoff aggregates + outcomes (Sochi promotion + Pari NN Khimki-reprieve, all-stay 2025-26), totals 639/730/637/648/609, per-club pivots 30×16 ×5, boundary/dupes/identity, second index: fdata diff 730/732 ×3 with 2 documented conflicts + **wiki FBR matrices 240/240 score-identical ×2** (feed discontinued). Builder: `tools/build_rpl_pack.py`, raw ledger: `audit/ledger/rpl-*.txt`. |
| **Russian Cup 2021-22 → 2025-26 FULL SPAN** (WO-RUSCUP-BACKFILL-03, returned 2026-08-03, re-issued under errata ERRATA-2026-08-03; **extended full-span 2026-08-04 under owner override DECREE-2026-08-04 — cutoff rescinded; supersedes sha `c2658b49…`**) | `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` — **341 MATCH rows** (36+77+76+76+76, compType `domestic-cup` per errata), **25 TEAM** (incl. `TEAM|FC Ufa` per standing cup-audit instruction; KAMAZ exactly `KAMAZ`; newcomers Tyumen, Shinnik Yaroslavl, Neftekhimik Nizhnekamsk) / 16 SOURCE / 119 NOTE, `END`; 2026-27 boundary NOTE (Regions-path R1 played, 0 RPL by design — zero rows, sourced) | `audit/pack-validation.txt` — **258/258 gates PASS** (slice counts ×5, group tables club-for-club ×5 incl. 3 corroborated RSSSF print-error corrections (DM pts→11; Akhmat→8-10; Loko GA→4), bracket→champions 2022 Spartak / 2023 CSKA / 2024 Zenit / 2025 CSKA / 2026 Spartak, 28 aggregates, 27 advancement NOTEs, per-club pivots ×5, boundary/dupes/identity; second index 341/341 match-for-match; Arsenal-Khimki venue conflict adjudicated via RFS). Builder: `tools/build_pack.py`, raw ledger: `audit/ledger/`. |
| **Russia ADDENDUM — RPL 2026-27 played rounds + Super Cups 2025/2026** (supervisor/ADDENDUM-2026-08-04-RUSSIA-GAPS REQ-2+REQ-3, SPEC-2026-08-04 items 1+3) | `handoffs/RUS-ADDENDUM-2026_BP-TEAM-PACK_v2.txt` — **18 MATCH rows** (RPL 2026-27 Round 1 ×8 + Round 2 ×8, compType `domestic-league`; Russian Super Cup 2025 + 2026, compType `domestic-cup`), **1 TEAM** (Rodina Moscow top-flight registration) / 7 SOURCE / 13 NOTE, `END` | `audit/pack-validation-rus-addendum.txt` — **16/16 gates PASS** (Round-1 rows 8/8 vs RSSSF rus2027 print; Round-2 rows 8/8 vs RPL official heritage match centre (RSSSF fixture-only, adaptation NOTE) + wiki FBR/table triangulation 16/16; goals 51; R1 attendance 102,232 anchor; roster/stadium strings verbatim pinned; both finals' advancement NOTEs; rolling boundary). Builder `tools/build_rus_addendum_pack.py` (double-rebuild identical, sha `30576ac4…`); ledgers `audit/ledger/rpl-2026-27.txt`, `audit/ledger/rus-supercup-2025-2026.txt`. |
| **Czech First League 2021-22 → 2025-26 FULL SPAN** (WO-CZ1-BACKFILL-02, returned 2026-08-03, amended same-day on the auditor's return — body approved, pro/rel block reinstated; **extended full-span 2026-08-04 under owner override DECREE-2026-08-04 — cutoff rescinded; supersedes sha `55d9bd80…`**) | `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` — **1,401 MATCH rows** (276+276+277+276+276 league compType `domestic-league` + **20 Czech Relegation Playoffs pro/rel legs compType `other` per ERRATA**), **0 TEAM** (WO §2 directive; 17 pinned strings + Dukla Prague on its two seasons; 7 FNL opponent strings reused from the client roster) / 21 SOURCE / 27 NOTE, `END`; 2026-27 boundary NOTE (tsje2027 404; BBC menu shows R1 2026-08-07..09 after the return date — zero rows, sourced) | `audit/pack-validation-cz1.txt` — **175/175 gates PASS** (per season 240 regular = 30 dated matchdays × 8 + 15 Titul + 15 Zachranu + 6-7 Evropu legs + 4 pro/rel, **80 club-season pivots** + 7 FNL 2-leg pivots, regular tables 16/16 ×5 and group tables 6/6 ×10 vs independent constants, all 8 regular H2H ties + 4 group ties incl. the 2022-23 title 78-78 by regular points 68>66 and the 2024-25 Titul 63-63 by regular points 62>51, second-index diff 1,378/1,381 league + 20/20 pro/rel legs with 3 documented wiki matrix defects + 2 infobox scalars + 3 corrupted Z cells adjudicated, worldfootball spot matchdays 24/24 for 2021-24 (wf dropped Czech — n/a documented; **BBC dated lattice bijection 270/270 for 2025-26**), pro/rel aggregates/venues/leg structure incl. the Dukla pens-4-2 decider, T32 derby walkover 0-3 award + Karvina match-fixing demotion disclosed in warning NOTEs). Builders: `tools/build_cz1_pack.py` (5 seasons, byte-deterministic sha `cbd5710b…`), `tools/build_cz1_2526_ledger.py`, `tools/diff_cz1_matrix.py`; raw ledgers: `audit/ledger/cz1-*.txt`. |
| **England Premier League 2021-22 → 2025-26** (WO-EPL-SPAN-12, returned 2026-08-03) | `handoffs/EPL-2021-2026_BP-TEAM-PACK_v2.txt` — **1,900 MATCH rows** (380 ×5 full seasons, compType `domestic-league`, venue-detail `MD<n>`), **0 TEAM** (WO §2; the 27 roster strings used verbatim, `Nott'm Forest` apostrophe form incl.) / 17 SOURCE / 17 NOTE, `END`; 2026-27 boundary NOTE (season starts 2026-08-21, after the return date — zero rows, sourced) | `audit/pack-validation-epl.txt` — **83/83 gates PASS** (38×10 rounds ×5, final tables 20/20 club-for-club **and** position order ×5 recomputed from the pack's own rows — 2023-24 with Everton −8 / Nott'm Forest −4 PSR deductions, membership-season boundary swaps 3↔3 at all four seams, second indexes: openfootball diffs 380/380 IDENTICAL round+date+score ×4 seasons and Wikipedia FBR matrix 380/380 IDENTICAL scores for 2025-26, 100/100 per-club full-campaign pivots — owner pivot decree, dupes/date-sort/venue/roster-domain/ASCII, QEII 2022-23 R7 scatter + 2023-24 R17 abandoned-game VOID/replay + 2024-25 R12 two-index date override + 2025-26 MD31 triple-slice anomaly gates). Builder: `tools/build_epl_pack.py` (byte-deterministic), raw ledgers: `audit/ledger/epl-*.txt`, pivot ledgers: `audit/ledger/epl-pivot-*.txt`. |
| **RPL league dataset 2021/22–2025/26** (CSV-era return, 2026-08-02) | `data/rpl/RPL-2021-22.csv` … `RPL-2025-26.csv` + `rpl_all_2021-2026.csv` (1,212 rows: FT score + closing 1X2 odds) | `docs/AUDIT.md` + `audit/validation-report.txt` — computed final tables reproduce the official tables row-for-row for all five seasons (2 source defects identified, kept verbatim). Pipeline: `tools/assemble_validate.py`. |

## Sources

* **RPL league pack (full span):** RSSSF season pages league chapters (`rus2022..rus2026.html`
  #1l + #1ldet + #prorel, scores AND dates, primary; final tables + venue prints) +
  football-data.co.uk match feeds as the diffed second index for 2021-24 (730/732 identical;
  2 documented conflicts resolved to RSSSF) and — the feed being discontinued after 2023-24
  (2425/2526 = 404; openfootball/russia absent) — Wikipedia season FBR results matrices as the
  replacement score-level second index for 2024-25/2025-26 (**240/240 score-identical both
  seasons**; matrix-recomputed tables 16/16) + worldfootball round pages (MD30-2425 8/8) +
  RFU/RPL official decision pages (membership chain; playoff venues via wiki/RFS match boxes).
* **Russian Cup pack (full span):** RSSSF season pages (`rsssf.org/tablesr/rus2022..rus2026.html`
  — #kubok + #cupdet chapters, scores AND dates, primary) + Wikipedia season pages with linked
  RFS (rfs.ru) match sheets as the independent second index; every one of the 341 rows
  cross-checked match-for-match, with RFS official match pages supplying D2-host grounds and the
  Arsenal-Tula venue/date adjudication.
* **Czech First League pack (full span):** RSSSF season pages (`rsssf.org/tablest/tsje2022..2026.html`,
  scores AND dates, primary; tsje2026 prints table-form only — a documented `source_adaptation`
  where the 2025-26 rows were assembled from the BBC `czech-first-league` dated month lattice
  (12 month pages, stage-labelled) × wiki FBR matrices, recompute == RSSSF constants EXACT) +
  English Wikipedia season articles fetched at full depth (1,200 regular + 150 group-stage +
  30 Evropu scores diffed cell-for-cell against the FBR/group matrices, official tables and
  venue tables ×5, TwoLeg pro/rel boxes) as the second index + worldfootball.net matchday
  spot-audits for 2021-24 (24/24 identical; wf dropped Czech coverage 2024-25 on, documented
  n/a); 3 wiki matrix cells proved defective by the articles' own official tables and resolved
  to RSSSF after re-fetch adjudication; 3 unicode-minus corrupted 2025-26 Z-group cells
  adjudicated via BBC + arithmetic closure; FNL pro/rel grounds via club articles (incl. MFK
  Chrudim, SK Artis Brno).
* **England Premier League pack:** RSSSF season pages (`rsssf.org/tablese/eng2022..eng2026.html`)\n  as primary — Ian King's 2021-22..2024-25 pages carry full round-by-round dates+scores+final\n  tables; the 2025-26 page (Karel Stokkermans) carries the **final table only**, a documented\n  `source_adaptation`: the 2025-26 match rows come from openfootball/england\n  (`master/2025-26/1-premierleague.txt`, labelled carrier) and reproduce the RSSSF table **exactly**\n  on full recompute. Second indexes: openfootball season files (4 × 380/380 diffs IDENTICAL),\n  the Wikipedia 2025-26 FBR results matrix (380/380 scores IDENTICAL), worldfootball matchday\n  pages (QEII round-7 10/10), football-data.co.uk E0 CSVs (adjudicated + MD31 stray dates,\n  byte-for-byte), Wikipedia season articles (venue tables ×5, 2026-27 boundary evidence).\n* **RPL CSV dataset:** football-data.co.uk combined RPL file (retrieved 2026-08-02, only data
  origin); verification-only cross-checks vs Wikipedia/tribuna/sportsmole/365scores and the
  Russian sports press, cited inline in `docs/AUDIT.md`.
* **Czech MOL Cup pack (full span 2021-22 → 2025-26 under the owner override):** RSSSF season
  pages (`tsje2022..tsje2026.html#cup`, primary — 2021-24 carry R16→Final only, the 2024-25 +
  2025-26 pages carry R3 onward, a documented adaptation) + English Wikipedia bracket sections
  (R2/R3 coverage ×5, QF/SF/F match boxes) as the full-coverage index + worldfootball.net round
  pages, per-tie match reports (goal timelines = all 33 aet/pens 90-minute splits; silent-aet
  defect found in both bracket sources for Slovacko–Karvina 2021-11-12; one wiki score typo
  Rokycany 0-1 vs proven 0-6 in 2025-26) and season stadium indexes as the third anchor;
  lower-league tiers pinned from cs.wiki CFL/MSFL/Divize season tables and club pages; Czech
  aet-convention rule change from 2024-25 (extra time at R2/R3/R16 level) evidenced per-tie.

## Provenance guarantee

* Machine validation on every deliverable; outputs committed under `audit/`.
* 90-minute doctrine everywhere: shootouts/aet live in NOTE lines, match rows carry 90-minute scores.
* Identity discipline: pinned roster strings (WO-RPL §3), renames documented in NOTEs, no duplicate clubs.
* Next in the owner queue: **⑥ FRA** and the remaining 5-year-span workorders listed in
  `supervisor/README.md` — see `WORKORDER-STATUS.md` for the live register.
