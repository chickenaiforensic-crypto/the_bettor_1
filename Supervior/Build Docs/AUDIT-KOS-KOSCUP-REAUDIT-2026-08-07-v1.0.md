========================================
KOS / KOSCUP v2.1 — INDEPENDENT AUDITOR VERIFICATION (2026-08-07)
========================================
Auditor: Auditor (fresh session, zero inherited trust — fresh code only)
Date: 2026-08-07
Target: researcher's corrected v2.1 packs
  branch arena/019fd805-the-bettor-1 @ e02dcb82d9db1a44913038f7a818632bfeaf97a1
  (fetched from origin; parent f9700e6 = the D1–D4 KOSCUP re-return)
Files (extracted via git show at that exact commit, evidence in
audit_work/kos_koscup_reaudit_2026-08-07-v1.0/remote_e02dcb8/):
  handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt
  handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt
Note: this is the independent verification the researcher's relay awaited
("Ready for the auditor's verification pass before import"). The report on
the researcher's branch is their self-report; this document is the
auditor's own, produced with the auditor's own scripts.

1. HASHES (computed on the extracted files — match the relay's declaration)
--------------------------------------------------------
| File | MD5 | SHA-256 | MATCH | SOURCE | TEAM | NOTE | END |
|---|---|---|---|---|---|---|---|
| KOS-…v2.1.txt | cde3688fd0da79b0f233c6d82cb50572 ✓ | 531bc96c9bce742e97efc72fae92076a78c3e01bec7804ae0ab042b40c2bb966 ✓ | 910 | 7 | 8 | 17 | 1 |
| KOSCUP-…v2.1.txt | cca71b174a7af989b43ed4cf285ca6b9 ✓ | acf40a85d04da7e8d490e67130046fb3bfa79f64d1b640fb8f2b97df7b0afd97 ✓ | 123 | 6 | 24 | 41 | 1 |

2. DIRECTOR'S THREE BLOCKING REASONS — all verified satisfied
--------------------------------------------------------
(1) KOS complete standalone: 910 MATCH = 900 Kosovo Superliga (180×5,
    INCLUDING the 12 former "already-held" rows — all present, verified
    against the worldfootball carrier: dates, RS R23/R26–R36 labels,
    scores) + 10 Kosovo Relegation Playoffs. Table reproduction from the
    pack ALONE: 5/5 seasons EXACT (50/50 club-seasons, P/W/D/L/GF/GA/Pts),
    2025-26 (180 rows in-pack) reproduces the official RSSSF table (Drita
    66 champions). Goals 463/446/432/446/481 all official. Every club 36/36
    (incl. Malisheva 2025-26). 0 duplicates, 0 future dates.
(2) Venue placeholders: 0 rows in either pack with unknown/blank/"Stadium"/
    "City" in the stadium or city fields (fresh scan of all 1,033 MATCH
    rows). All 39+1 KOSCUP and 6 KOS corrections are named stadiums+cities,
    sourced per the packs' venue_source/playoff_venues/venue_policy NOTES.
(3) Artifacts on an accessible remote branch: audit report, session log,
    gate scripts, builder and RETURN addendum present on 019fd805 @ e02dcb8
    (verified via git ls-tree). Branch is fetchable (fetched successfully).

3. MATCH-DATA VERIFICATION (independent cross-check)
--------------------------------------------------------
The researcher's v2.1 was diffed field-by-field against the auditor's own
independently-built v2.1 (branch 019fd74a @ bcaee73):
  - Data-only diff (date|comp|ctype|home|hg|ag|away|round|country|tie|src):
    **0 lines for both packs** — every match fact is byte-identical to the
    independently verified build. Only stadium/city fields differ (the
    researcher's venue refinements, see §4).
  - Auditor's gate suite (gates_v21.py, run on the researcher's files):
    KOS 910/900+10 · appendix 12/12 · 0 placeholders · 0 dups · 0 future ·
    180×5 · goals exact · table reproduction 5/5 EXACT · playoff comp/
    ctype correct.
    KOSCUP 123 · 0 placeholders · 0 dups · slice 24/24/24/26/25 · D1–D4
    retained (0 "A", 0 Ph'nix, 0 lowercase "Prishtina e Re", 24 non-pool
    TEAM rows) · finals match the official record (Llapi, Prishtina,
    Ballkani, Prishtina, Dukagjini).
    PROBLEMS: 0.
  - Source linkage: every MATCH row's sourceId has a SOURCE row (0 orphans);
    RSSSF primary per season + wf-kos-2526 carrier for 2025-26 league +
    second indexes; KOSCUP wiki-kosovar-cups second index.

4. VENUE SPOT-VERIFICATION (independent)
--------------------------------------------------------
- Rilindja 74 → "Baran Sports Field, Baran": CONFIRMED independently
  (Wikipedia KF Rilindja 1974: based in Baran, Pejë; ground Baran Sports
  Field, cap 500). Correct.
- 2025-26 MD12 award (Prishtina E Re 3-0 Drenica): source_conflict NOTE
  present; governing score required by the official table; correct.
- 2024-25 playoff SF date (2025-05-25, RSSSF primary): kept; the pack's
  playoff_venues NOTE discloses Wikipedia prints 24 May with the opposite
  home side — RSSSF primary kept per doctrine. Acceptable.
- 2023-24 playoff SF venue (18 June Stadium, Kline): the researcher
  discloses this is an INFERENCE (RSSSF prints no venue). Flagged in-pack.
- TOP Football (2 rows, 2024-12-03 & 2025-12-04 vs Prishtina): venue
  "TOP Football Sports Field, Prishtine" is NOT confirmed by any accessible
  source (Wikipedia, RSSSF, soccerway, sofascore, betexplorer, FFK,
  Kosovar press — the researcher's own search). It is a descriptive label,
  disclosed with NOTE|warning|blocker asking for match-day confirmation.
  This is the ONLY venue value in either pack that this auditor cannot
  independently confirm.

5. NEW FINDING — D5: TEAM-ROW FIELD MISALIGNMENT (both packs)
--------------------------------------------------------
Every TEAM row places the ground name in the SURFACE slot (field 9) and
the STADIUM slot (field 6) as the literal string "unknown". Examples:
  KOSCUP L16: TEAM|2 Korriku|Kosovo|Kosovo First League|KFL1|2 Korriku|
      unknown|Prishtine|Kosovo|2 Korriku Sports Field|unknown|unknown|unknown
  KOS L14:  TEAM|Ulpiana|Kosovo|Kosovo Superliga|KOS|Ulpiana|unknown|
      Lipljan|Kosovo|Qatiq Bytyqi Stadium|2000|unknown|unknown
Authoritative field order (app-v3.6.3 PR.ingest GRAMMAR):
  name|country|leagueName|leagueCode|aliases|stadium|city|country2|
  surface|capacity|founded|website
Adopted reference (AUDIT-OVERRIDE RUSCUP pack):
  TEAM|Leningradets St-Peterburg|Russia|Russian Second League|2D|aliases|
      Kirovets Stadium|St Petersburg|Russia||||  ← stadium at field 6
At app ingest (positional mapping), the v2.1 TEAM rows yield:
  identity.stadium = "unknown" (literal string), identity.surface = the
  real ground name, identity.capacity = NaN on KOSCUP rows ("unknown"),
  2 rows carry surface="not published" (KOSCUP L18 Arberia, L26 Drenasi).
Impact: identity metadata only — zero effect on match rows, table
reproduction, or engine computation (MATCH rows carry the authoritative
venues). But it contradicts the researcher's claim that the TEAM layout was
"fixed to match the reference exactly", and it stores garbage in identity
venue fields. (Honest note: the v2.0 TEAM blocks were also misaligned —
this auditor's earlier passes checked TEAM names, not field placement; the
misalignment is caught here for the first time. Errata owned.)

6. VERDICT
--------------------------------------------------------
**Match data: APPROVED.** All three Director reasons are satisfied and
independently verified; the 1,033 MATCH rows are byte-identical to the
auditor's independently verified build; every data gate passes.

**Packs: RETURNED for a mechanical TEAM-block realignment (D5).**
Fix spec (one field shift per row, 32 rows total — KOS 8 + KOSCUP 24):
  move the ground name into the stadium slot (field 6), keep city in the
  city slot (field 7), country in country2 (field 8); set surface to "" or
  the true surface (not "not published"); set capacity to the numeric
  capacity or "" (not "unknown"); founded/website "" where unknown. No
  MATCH row changes. Re-hash and re-return; re-verification is a 2-minute
  run of the auditor's gate suite.

Owner confirmation items (do not block the match data; block clean import
of the identity/venue metadata):
  (a) TOP Football venue — confirm from match-day records, or accept the
      disclosed descriptive label + blocker NOTE;
  (b) 2023-24 playoff SF venue (18 June Stadium, Kline — disclosed
      inference).

7. PARALLEL-VERSION NOTE
--------------------------------------------------------
The auditor's own earlier v2.1 build (branch 019fd74a @ bcaee73) is
superseded by the researcher's corrected v2.1 (019fd805 @ e02dcb8). The
researcher's commit is the authoritative artifact; the auditor's build was
used purely as the independent cross-check (§3: data-identical). Both
branches remain on the remote.

Evidence: audit_work/kos_koscup_reaudit_2026-08-07-v1.0/ (remote_e02dcb8/
extracted files, gates_v21.py runs, this report); hashes recomputed this
session.
========================================
