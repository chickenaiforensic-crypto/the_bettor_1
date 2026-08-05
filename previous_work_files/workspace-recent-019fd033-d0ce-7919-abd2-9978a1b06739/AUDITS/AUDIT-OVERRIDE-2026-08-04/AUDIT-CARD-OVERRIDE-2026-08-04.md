# AUDIT — DECREE-2026-08-04 override packs (wave 1) — 2026-08-04

Scope: researcher full-span deliveries on branch `arena/019fc462-the-bettor-1`.
Transport of record: git blobs (raw.githubusercontent CDN was 404-lagging after the branch move).
Researcher self-reported gate counts registered, never adopted. All numbers below are auditor-computed.

## 0. Branch / transport facts

| fact | value | proof |
|---|---|---|
| remote tip | `5722cb61ea8f…` | git ls-remote (API rate-limited at probe time) |
| MOLCUP full-span commit `5d75e56` | **ABSENT from remote** (his push died w/ token) | API `No commit found for SHA: 5d75e56` |
| remote MOLCUP pack | OLD 120-row backfill, sha256 `5023eb33…`, md5 `662fe5dfe38002474855110b2a17ea6c` = my frozen approved copy byte-exact | raw fetch |
| RPL full-span 1,220 | sha256 `d71ed24f…db79` | = his claim EXACT |
| RUSCUP full-span 341 | sha256 `f89501cf…db91` | = his claim EXACT |
| CZ1 full-span 1,401 | sha256 `cbd5710b…0a6e` | = his claim EXACT |
| EPL full-span 1,900 | sha256 `707dd830…3036` | = his claim prefix EXACT |

## 1. Verdicts

### EPL 1,900 — **ADOPT (cleanest pack; no Wave-2 blockers)**
- 380×5 counts ✓ · compClass `England Premier League|domestic-league` ×1,900 · MD<n> venue detail ×1,900 · internal dupes 0 · zero 2026-27 rows (season starts 2026-08-21, boundary NOTE present).
- Seasons 2021-22..2024-25 row-diff vs auditor sha-pinned baselines: **scores/sides/rounds 1,520/1,520 identical**; 43 rows differ on DATE ONLY — every one adjudicated in the pack's favour by independent third-index evidence:
  - final-round Sundays (2022-05-22, 2023-05-28, 2024-05-19, 2025-05-25) vs my baselines' round-window Mondays — simultaneous final-day convention; baseline artifact class logged as ERRATA (dates only; scores/tables/anchors untouched).
  - `Everton 3-0 Newcastle` + `Tottenham 1-2 West Ham` **2023-12-07** — RSSSF eng2024 prints them under impossible `[Dec 2]` (both clubs already had R14 games that day); reality = Thursday Amazon double (Dec 7, 2023). His ledgers: 2 indexes agree; wiki season page carries NO Dec-7 date lines (transcluded fixtures) — misprint proven.
  - `Newcastle 0-2 West Ham` **2024-11-25** — football-data E0.csv row `25/11/2024,20:00,Newcastle,West Ham,0,2,A` verified byte-level by auditor (RSSSF's Nov-24 = misprint).
- **2025-26 table 20/20 profile-exact** vs RSSSF eng2026 final table (page matured since my earlier skeletal probe; Arsenal 26-7-5 71-27 85 champions reproduced from pack rows).
- 2023-24 deductions (Everton −8, Nott'm Forest −4) — his own gate applies before position check; transitive coverage: pack score-grid == baseline grid which already locks those tables 20/20.

### RPL 1,220 — **ADOPT-PENDING-WAVE2 (conditional) + 2 gaps owned by researcher**
- **Tables: 80/80 profile-exact** recomputed from pack rows vs rus2022..rus2026 final tables (genuine comparison; alias map 100% transliteration, zero numeric rescues).
- Playoffs: 4 legs × 5 seasons = 20/20; existence confirmed in all five rus files (13th/14th flagged + prorel sections); legs row-exact for 2021-22 (May 25/28 prints) and 2025-26 (incl. Akron 0-1 Rotor leg-2, aggregate convention check vs att/scorer prints).
- Structure: 240×5 league + 20; compType `domestic-league`/`other` classes per errata mirror; dupes 0; TEAM rows (Ufa/Yenisey/SKA/Rotor) = non-roster playoff opponents ✓.
- **GAP F1 — 2026-27 missing:** decree = "full seasons 2021 → today"; RPL R1 played 2026-07-24..26 (+R2 rows by 2026-08-04). Pack shipped zero 2026-27 rows with boundary NOTE. Store currently holds 9 such rows (auditor-verified clean) that purge would erase → researcher must append played rounds (est. 8-12 rows today) before Russia clears.
- **GAP F2 — Super Cups missing:** outbox spec (file 02) required Super Cup 2025 + 2026 (2 rows). Neither RPL nor RUSCUP pack carries any Super Cup row (grep 0). rus2026 `#sup` confirms 2026 game exists (Zenit 1-1 Spartak pen 4-2, 2026-07-18). Researcher addendum required.
- Wave-2 registered: full date-exact round-grid diff 1,200 rows vs rus round listings (span-diff machinery); playoffs 2022-23/2023-24/2024-25 leg row-exact confirmation (brackets cross-checked vs anchors, deep-score compare pending).

### RUSCUP 341 — **ADOPT-PENDING-WAVE2**
- **Continuity PERFECT: all 189 rows of the approved old pack (153/153 bulk-diffed 2026-08-03) preserved VERBATIM inside the new 341** (superset, zero rewrites) → audit surface = the +152 rows (2024-25: 76, 2025-26: 76) + 119 NOTEs (advancement doctrine intact; 90-min rows).
- Wave-2 registered: score-diff the 152 rows vs rus2025/rus2026 cup chapters + advancement-NOTE spot audit.

### CZ1 1,401 — **ADOPT-PENDING-WAVE2 (light)**
- **Phase tables 140/140 profile-exact:** REGULAR 5×16=80/80 · TITUL 5×6=30/30 · ZACHRANU 5×6=30/30 (2025-26 Zachranu print is position-scrambled in RSSSF — duplicate 13, 14-after-15 — verified row-by-row 6/6 separately; RSSSF NB confirms Karviná match-fixing demotion, cross-referenced with pack `karvina_incident` NOTE).
- **Pro/rel playoff legs 20/20 row-exact** vs tsje2022..tsje2026 prorel sections (incl. Dukla 1-1 Vyškov [aet, 4-2 pen] 90-min doctrine: row = 90-min score, pens in bracket).
- Rules: Artis Brno on league rows = 0 ✓ (promotion effective 2026-27); counts 276+276+277+276+276 + 20 ✓; span 2021-07-24..2026-05-31; zero 2026-27 rows ✓ correct (Czech R1 = 2026-08-07..09, boundary NOTE).
- Wave-2 registered: Evropu-path 31 legs (SF 20, F 10, CLP 1) score-diff vs `Play-off o umístění` sections (e.g. 2025-26 Karviná/Pardubice aet prints — feed 90-min check).

### MOLCUP full-span (202 rows claimed) — **NO-GO: not on branch**
Commit `5d75e56` local-only at researcher side; push died with his token. Remote holds only the old approved 120-row pack. His report (regression 30/30 → 32/32, champions Sigma Olomouc 2025 & MFK Karviná 2026, 13 aet-settled ties at 90-min, Rokycany 0-6 typo ruling, Artis Brno ground proofs) registered as self-reported until bytes land. **Owner action: reconnect his GitHub.**

## 2. Auditor errata (own instrument, honest log)
`audit-baseline/epl-202*.json`: 43 rows carry round-window dates instead of per-day dates
(12/12/10/11 by season… printed detail in scripts/epl_gate.py run log; scores, tables,
goal anchors and all sha pins unaffected). Correction: adopt pack per-day dates as canon;
baseline JSONs re-pinned at next rebuild, errata noted here first (never silent-rewrite).

## 3. Clearing decision matrix (D14 endgame; purge = v3.6.2 backup-gated control)

| country | old rows held | package state | verdict TODAY |
|---|---|---|---|
| Russia | 644 | RPL+RUSCUP pushed & wave-1 gated; F1+F2 open; no Super Cup | **NOT YET** — researcher addendum + Wave-2 |
| Czechia | 632 | CZ1 pushed & near-full gated; **MOLCUP full-span missing** | **NOT YET** — his GitHub reconnect, then MOLCUP audit |
| England | **0** | EPL pushed; fully gated clean | **ELIGIBLE NOW** — pure adds, nothing to purge; owner decides immediate import vs batch (D14-letter safe: no old/new mixing exists) |
| Scotland/Kosovo/US | 34/19/81 | not yet delivered (queue: FRA next) | untouched |

## 4. Runbook when a country package completes (unchanged; needs owner UAT first)
G1-G7 UAT rehearsal (v3.6.2) → per-scope backup download → PURGE country (Russia 644→788,
Czechia 632→800) → import audited packs as pure adds → Coverage totals verified against
auditor pins → log lines with country+competition+backupFile checked.

## 5. Files produced this audit
`rpl_table_gate.py` (80/80) · `cz1_table_gate2.py` (134/134 + manual 6/6) · `epl_gate.py` (row-exact + 20/20) ·
ruscup continuity diff · all four packs md5/sha-pinned in `/home/user/AUDIT-OVERRIDE-2026-08-04/`.

## ADDENDUM 2026-08-04 (close-out): MOLCUP FULL-SPAN AUDIT — **ADOPT** · Czechia first clearing-eligible country
Supersedes the earlier "MOLCUP NO-GO (not on branch)" — bytes have since landed and are now audited in full. The NO-GO section above is kept verbatim as the honest record of its moment.

### Transport (verified on actual bytes)
- Branch tip `84d9471d2c31835eb2370f15e567e1cf568690d2` (researcher recovered local-only `5d75e56`, re-verified, pushed).
- Pack sha256 `50ead762d80070dce6cbf468dedd26eb4d4e3706dd264801194af49385791137` = researcher claim **EXACT** via git blob (raw CDN not trusted).
- Structure counted on bytes: 202 MATCH (41+41+38+41+41) · 43 TEAM · 53 NOTE (34 advancement-class incl. 1 documented source_conflict) · 23 SOURCE · compType grammar `MOL Cup|domestic-cup` ×202 · 0 duplicate fingerprints.

### Gates (all run, shown, on this machine)
| gate | result |
|---|---|
| Continuity vs old approved 120-row pack | **120/120 rows verbatim** (superset, zero drift) |
| Champions/finals 2021-22..2025-26 | **5/5 verified** — Slovácko 3-1 Sparta · Sparta 0-2 Slavia · Plzeň 1-2 Sparta · Sigma Olomouc 3-1 Sparta (tsje2025 exact, Andrův) · Jablonec 1-3 Karviná (wiki box 2026-05-20, Malšovická aréna, att 7,352) |
| tsje2025 (2024-25 season) full diff | clean — 30/31 mechanical score+date+sides; Opava 1-2 Zlín correctly SLICED OUT (FNL-vs-FNL, zero FL involvement); Táborsko–ČB 0-0 90-min (aet 0-2) doctrine ✓ NOTE'd |
| tsje2026 (2025-26 season) full diff | 25/31 mechanical + 5 auditor-alias closes (Lanznot/Karlovy Vary/Frydek-Mistek/Hlinsko/Trinec — scores verified equal, incl. 2 pure-aet ties with advancement NOTEs) + SF dates 2026-04-21 ×2 ✓ |
| RSSSF tsje2026 final print | **RSSSF wrong** ("Mladá Boleslav 1-3 Karviná" = stale finalist, contradicted by its own SF lines) — pack correct; adjudication logged |
| R2 2025-26 vs wiki season page | **10/10 exact** (Rokycany 0–6 carried as documented source_conflict vs wiki 0-1 print; wf double-proof registered, 4th source pending — not a fail) |
| R2 2024-25 vs wiki season page | **11/11 EXACT** (close-out rerun: pso-brace-aware OneLegResult parser + global link-unwrap; prior 3 misses were my parser artifacts — display-pipe link + tier suffix. Milín 0-2 Teplice · Motorlet 0-1 Hradec · Povltavská 1-3 Liberec · Kroměříž 1-0 Karviná · Příbram 2-2 ČB all byte-checked) |
| 90-min doctrine | 13 aet-settled ties carried at 90-min score + advancement NOTE ✓ |
| 2026-27 boundary | zero rows ✓ correct (MOL Cup 2026-27 not started at audit date) |

### Verdict
**ADOPT** — eligible for import as pure adds immediately after scope-clear. Czechia package now complete: CZ1 1,401 + MOLCUP 202, both audited.

### Clearing matrix (updated this addendum)
| country | verdict TODAY |
|---|---|
| **Czechia** | 🟢 **ELIGIBLE — pending owner UAT v3.6.2 only.** Runbook: backup → PURGE 632→800 → import CZ1 1,401 + MOLCUP 202 → expected total **2,403**, zero skips expected |
| England | 🟢 ELIGIBLE NOW (no purge needed) — owner decision: import now vs batch |
| Russia | 🔴 NO-GO (F1 2026-27 rows + F2 Super Cups + Wave-2) |
| Scotland/Kosovo/US | untouched (researcher on FRA next) |

## ADDENDUM-2 2026-08-04: RUS-ADDENDUM-2026 (18 rows) — **ADOPT** · F1/F2 CLOSED · Russia red->amber
### Transport (verified on actual bytes)
- Branch tip `8e867a8aff7b441d6aa3a121b03b2a31a6dc2785`; pack sha256 `30576ac4894930b359db19193f08f05cd3f399ecd7d97f9975184ac02386dcea` = claim **EXACT** via git blob (raw CDN not trusted).
- Structure on bytes: 18 MATCH (16 RPL 2026-27 R1+R2 + 2 Super Cups) · 1 TEAM (Rodina Moscow top-flight identity, shape = pinned RPL-pack grammar) · 7 SOURCE · 13 NOTE · 0 internal dupes · span 2025-07-12..2026-08-02, no row past return date.
### Gates (all run, shown, on this machine — researcher's 16/16 registered, never adopted)
| gate | result |
|---|---|
| R1 2026-27 vs RSSSF rus2027 (my own ref, primary) | **8/8 EXACT** date+score+sides; attendance anchors sum to printed Total 102,232 exactly; R1 table 16/16 reproducible from pack rows |
| R2 2026-27 pairings vs RSSSF rus2027 fixture list | **8/8 EXACT** (RSSSF printed fixtures-only at fetch — matches researcher's SOURCE ledger) |
| R1+R2 2026-27 scores vs wiki FBR matrix (updated 2026-08-02, independent) | **16/16 EXACT**; reverse check: 16 filled cells = 16 pack rows, no extra/missing tie |
| R2 date spot-proof | Orenburg 0-3 Zenit = **2026-08-02 proven** by wiki hat-trick cite (premierliga match_16251 "date=2 August 2026"); remaining R2 dates inside RSSSF window [Jul 31-Aug 3]; premierliga match-centre CAPTCHA-walled to me (registered, not a fail) |
| Super Cup 2025 row vs my rus2025 #sup | **EXACT** — Krasnodar 0-1 CSKA, Divejev 48, Cobnan red 89; wiki 2nd index (Ak Bars, 34,677, Chistyakov) agrees |
| Super Cup 2026 row vs my rus2026 #sup | **EXACT** — Zenit 1-1 Spartak [pen 4-2], Martins 25 / Sobolev 90+8 pen, Nizhny Novgorod, 42,139; 90-min doctrine rows + advancement NOTEs ✓ |
| Store-supercup nuance | live store's old 2025 Super Cup row = same dedupe fingerprint (date+home+away+comp) → at purge-first import, zero collision; compType domestic-cup flagged in NOTE per 02-SPEC rule ✓ accepted |
| Rodina provenance | strings appear in pinned RPL pack 2022-23 playoff rows (0-3/2-0 Pari NN) ✓; TEAM row Arena Khimki consistent with rus2026 + rss2027 NBs (Samara/Kaspiysk staging) ✓ |
### Auditor errata OWNED (mine)
My SPEC-02 playoff enumeration named 2026 as 'Shinnik-Akron' — WRONG (actual 2026 ties: Akron-Rotor, Ural-Dynamo Makhachkala; Shinnik was First League 8th). Researcher's playoff_composition NOTE correct; his 20-leg pack stands. Logged here, never silent-rewrite.
### Rolling-append registered
R3 2026-27 (starts 2026-08-08) will ship as the next small addendum; same arrival protocol (branch probe → git-blob sha → my gates) each drop.
### Verdict
**ADOPT.** Gaps F1 (RPL played rows through today) and F2 (Super Cups 2025+2026) CLOSED. Russia moves 🔴→🟡: all packs received and primary-verified; pre-clear remainder = MY Wave-2 row-diffs (RPL 1,200-row round-grid dates, playoff legs 2022-23..2024-25, RUSCUP +152 surface). No researcher action owed on Russia until R3 completes.

## ADDENDUM-3 2026-08-04 (wave-2 close-out): ALL ROW-DIFFS COMPLETE · Russia 🟢 fully audited · Czechia 🟢 fully audited
Wave-1 verdict was adopt-pending-Wave-2 for RPL/RUSCUP/CZ1. Wave-2 now executed, every gate run on this machine against my own pinned RSSSF texts (not the researcher's copies).

### Wave-2 gates (all run and shown)
| gate | result |
|---|---|
| RPL full round-grid date+pair+score diff (1,200 league rows vs rus2022..2026 round prints; gate rpl_grid_gate.py) | **1,200/1,200 EXACT** (per season 240/240 x5). Instrument taught: Round-N header dates are the scheduled-day prints; one alias class ('Dinamo' prints) + round-header date extraction fixed on my side |
| RPL relegation playoff legs remaining 3 seasons (2022-23..2024-25 = 12 legs) | **12/12 EXACT** (with wave-1 8/8: **20/20 total**) |
| RUSCUP new surface vs rus2025/rus2026 cup chapters (76+76 rows; gate ruscup_w2_diff.py) | **152/152 EXACT** — 0 unexplained pack rows; RSSSF-only remainder = regions-path rounds (out of pack scope by design; includes same-city name traps like Zenit Penza [D4] != Zenit St Petersburg, proven by line prints) + '#cupdet' reprint duplicates (parser artifact on my side, harmless) |
| CZ1 Evropu middle-four playoff legs (31 rows incl. single 2023-24 CLP) vs tsje2022..2026 'Skupina o Evropu'/'Play-off o umisteni' | **31/31 EXACT** (SF 20, F 10, CLP 1: 2024-05-31 Mlada Boleslav 3-1 Hradec Kralove) |

### Instrument bugs found and fixed on MY side during wave-2 (none touched pack verdicts)
- rpl_grid_gate.py: season-year calc (y1:04d -> 0022 bug), 'Dinamo' alias missing, Round-N header dates not extracted.
- ruscup_w2_diff.py: junk-filter 'att' not in names destroyed every row involving **Akron Tolyatti** (substring 'ATT' in TOLYATTI) + Krylia Sovetov alias gap ('Krylja S.' print) + two-leg header dates cleared after first tie (lost SF ties of same header). All fixed; final result 0/0 unexplained.

### Registered exception R-EX-1 (documented deviation, accepted)
CZ1 2025-26 Evropu SF leg-2s (Pardubice 1-3 Karvina; Olomouc 1-2 Bohemians) went to extra time. Pack carries the after-ET scores of record (as the official record + RSSSF print them), tie outcomes documented in its playoff_outcomes NOTE. This differs from strict 90-min doctrine rows (90-min + advancement NOTE) used for pens ties; it is 2 rows, source-faithful, explicitly marked. Convention for future packs stays: 90-min + advancement NOTE. Not a re-work item.

### Closing verdicts (data side complete)
- **RPL pack 1,220 rows (sha d71ed24f…)**: tables 80/80 (wave-1) + round-grid 1,200/1,200 + playoff legs 20/20 => **FULLY VERIFIED, ADOPTED.**
- **RUSCUP pack 341 rows (sha f89501cf…)**: old-scope 189 verbatim continuity + 152/152 new rows exact => **FULLY VERIFIED, ADOPTED.**
- **CZ1 pack 1,401 rows (sha cbd5710b…)**: phase tables 140/140 (wave-1) + pro/rel 20/20 (wave-1) + Evropu 31/31 => **FULLY VERIFIED, ADOPTED.**
- **MOLCUP pack 202 rows (sha 50ead762…)**: ADDENDUM-1, already ADOPTED.
- **RUS-ADDENDUM 18 rows (sha 30576ac4…)**: ADDENDUM-2, already ADOPTED.
- **EPL pack 1,900 rows (sha 707dd830…)**: wave-1 ADOPTED (no wave-2 open).

### Clearing matrix (DATA side final; programme side awaits owner UAT)
| country | old rows | packages | verdict |
|---|---|---|---|
| Russia | 644 | RPL 1,220 + RUSCUP 341 + ADDENDUM 18 = **1,579 rows** | 🟢 **CLEARED TO EXECUTE after UAT passes** (purge 644 -> 788, then import) |
| Czechia | 632 | CZ1 1,401 + MOLCUP 202 = **1,603 rows** | 🟢 **CLEARED TO EXECUTE after UAT passes** (purge 632 -> 800, then import; expected total 2,403 or 2,391 with Russia first) |
| England | 0 | EPL 1,900 | 🟢 owner decision: import-now (pure adds) vs batch |
| Scotland/Kosovo/US | 34/19/81 | not yet delivered (FRA in progress per researcher) | untouched |
