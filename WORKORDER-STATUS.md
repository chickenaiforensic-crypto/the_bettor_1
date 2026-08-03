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
| override | **WO-RUSCUP-BACKFILL-03** — Russian Cup 2021-22 → 2023-24 | `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 189 rows (domestic-cup after errata), 22 TEAM incl. FC Ufa, KAMAZ exact-form, all 162 self-gates PASS** (user commissioned the cup return live, ahead of the RPL league pack) |
| ① | RPL league 2021-22 → 2023-24 | `handoffs/RPL-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 732 rows (240+4 per season ×3; 12 playoff rows compType `other` after errata), all 69 self-gates PASS** |
| ② | **WO-CZ1-BACKFILL-02** — Czech First League 2021-22 → 2023-24 | `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | **DELIVERED 2026-08-03 — 829 rows (276+276+277; pro/rel legs held out pending owner roster decision), all 105 self-gates PASS** |
| ④ | MOLCUP (Czech MOL Cup) 2021-22 → 2023-24 | pack | **NEXT** (compType `domestic-cup` per errata) |
| ⑤→ | EPL, FRA, GER, ITA, KOS, KOSCUP, MLS, SCO1, SCOCUP, SCOLC, SPA, USOC | packs | QUEUED (workorder texts on `origin/main`) |

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
RPL `6e458e19…` (69/69 gates) · RUSCUP `18ba4695…` (162/162 gates).

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
| `handoffs/CZ1-2021-2026_BP-TEAM-PACK_v2.txt` | Czech First League return (WO-CZ1-BACKFILL-02), BP-TEAM-PACK v2 grammar: 829 MATCH rows (276 + 276 + 277; every row compType `domestic-league` per WO §2), **0 TEAM** (WO §2 directive), 12 SOURCE, 21 NOTE (17 info incl. 3 spot-audit + 4 warning incl. 2 source_conflict), `END`. Venue-detail = `Round n` / `Titul R31-35` / `Zachranu R31-35` / `Evropu-SF|F L1|L2` / `Evropu-CLP`; cutoff honoured (last row the 2024-05-31 Conference League playoff Final). |
| `audit/pack-validation-cz1.txt` | 105/105 gates on the pack text: per-season 240 regular = 30 fully dated matchdays × 8 + 15 Titul + 15 Zachranu + 6/7 Evropu legs; per-club pivots 16 clubs × exactly 30 regular games and full-campaign ledgers (48 pivots, game-count shapes {35×12, 34×2, 32×2} and 2023-24 {36×1, 35×12, 34×1, 32×2} as documented); regular tables reproduced 16/16 ×3 + group tables 6/6 ×6 vs independent wiki constants; all 4 regular-stage H2H ties + 3 group ties recomputed incl. the 2022-23 title (Sparta over Slavia 78-78 by regular-season points 68>66); Evropu aggregates + winners + CLP row; second-index diff 826/829 identical (3 defective wiki FBR cells whitelisted after RSSSF re-fetch adjudication, each proven wrong by the article's own table; 2 wiki infobox goal scalars likewise contradicted by their own articles); worldfootball spot matchdays 24/24 identical (1 wf listing-date nuance documented). |
| `audit/ledger/cz1-2021-22.txt` · `cz1-2022-23.txt` · `cz1-2023-24.txt` · `cz1-2ndidx-*.txt` · `cz1-venues.txt` | Primary transcriptions of RSSSF tsje2022/2023/2024 (R1-30 + T/Z31-35 + Evropu legs, tables with H2H brackets, pro/rel ties as comment records); wiki A FBR/group matrices + worldfootball spot rows (second index); venue + table/group-table constants. |
| `tools/build_cz1_pack.py` | Reproducible builder + validator for the CZ1 pack (byte-identical rebuild verified by sha256 `eee4686f…`). |
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

## Known loose ends

* Two files the owner says were attached mid-session (`README.md`, `START-HERE.md`)
  never became readable in the sandbox and are not in the repo — flagged in chat;
  awaiting re-send or a GitHub web upload.
* The uploaded `ERRATA-2026-08-03.md` likewise never materialized (checked repo root,
  `/home/user/uploads/`, full `origin/main` tree) — applied verbatim from the owner's
  inline relay; mirror at `supervisor/ERRATA-2026-08-03.as-relayed.md`; owner asked to
  re-upload the original.
* Owner decision pending: sanction 5 TEAM declarations (Vlasim, Opava, Viagem Pribram,
  Vyskov, Silon Taborsko) so the 12 Czech pro/rel legs can be appended to the CZ1 pack
  as compType `other` rows — or confirm the NOTE-only default.
