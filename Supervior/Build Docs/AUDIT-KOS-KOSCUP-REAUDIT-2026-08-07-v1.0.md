========================================
KOS / KOSCUP RE-AUDIT v1.0 — Director correction order (2026-08-07)
========================================
Auditor: Auditor (fresh session, zero inherited trust — fresh code only)
Date: 2026-08-07
Targets (new versioned files, built per Director's correction order):
  handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt
  handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt
Evidence: audit_work/kos_koscup_reaudit_2026-08-07-v1.0/ (build_v21.py,
gates_v21.py — fresh, re-runnable)

CONTEXT
--------------------------------------------------------
Director blocked both packs from import for three reasons:
1. KOS must be a complete standalone pack: 900 Superliga + 10 playoff =
   910 MATCH rows (the 12 "already-held" rows are NOT in the 5,082 store,
   which holds zero Kosovo rows).
2. Replace every venue placeholder (unknown / blank / Stadium / City):
   KOS 6 playoff rows (stadium+city); KOSCUP 39 stadiums + 1 city.
3. Audit artifacts must be on an accessible remote branch.
D1-D4 (KOSCUP identity fixes) were NOT to be redone.

RESULT (verified with fresh code)
--------------------------------------------------------
| File | md5 | sha256 | MATCH | SOURCE | TEAM | NOTE | END |
|---|---|---|---|---|---|---|---|
| KOS-…v2.1.txt | 98530ecdbbcb595ac59f13705844336c | f7139dae64886ac632f98a36ee2d01b523fbe2ef6cd289ec19ba31b1d5ac2641 | 910 | 8 | 8 | 29 | 1 |
| KOSCUP-…v2.1.txt | a171c25f6995ad44ed899e39e54f1514 | 1aaa5fa0df5663c0ce242faf3d4c99b456114446e2eb36dcb4665bea21bfc2c6 | 123 | 6 | 24 | 47 | 1 |

CORRECTION 1 — KOS COMPLETENESS: PASS
- 910 MATCH rows = 900 Kosovo Superliga (180 x 5) + 10 Kosovo Relegation
  Playoffs. 12/12 previously-excluded rows present and verified against the
  worldfootball carrier (dates, MD labels RS R23/R26-R36, scores):
  2026-03-09 Malisheva 3-0 Prishtina; 2026-03-22 Malisheva 2-0 Llapi;
  2026-04-05 Drita 2-0 Malisheva; 2026-04-11 Prishtina E Re 2-1 Malisheva;
  2026-04-19 Malisheva 4-2 KF Ballkani; 2026-04-26 Dukagjini 0-1 Malisheva;
  2026-04-29 Malisheva 3-1 Gjilani; 2026-05-02 Prishtina 0-1 Malisheva;
  2026-05-10 Ferizaj 1-1 Malisheva; 2026-05-17 Malisheva 4-1 Drenica
  Skenderaj; 2026-05-24 Llapi 3-2 Malisheva; 2026-05-31 Malisheva 3-2 Drita.
  All carry source label wf-kos-2526 (180 rows total for 2025-26).
- Table reproduction (fresh recompute, pack ALONE — no appendix arithmetic):
  5/5 seasons EXACT, 50/50 club-seasons, P/W/D/L/GF/GA/Pts + membership.
  2025-26 now reproduces the official RSSSF table (Drita 66 champions) from
  the pack's own 180 rows. Goals 463/446/432/446/481 — all official.
- Shape: 36 rounds x 5 per season; every club 36 (incl. Malisheva 2025-26);
  membership per season matches the workorder pins; 0 duplicates; 0 future
  dates; playoff rows compType other / comp "Kosovo Relegation Playoffs".

CORRECTION 2 — VENUE PLACEHOLDERS: PASS (both packs)
- KOS: 0 rows with unknown/blank stadium or city (was 6). The six playoff
  venues now carry documented home grounds:
  2023-05-27 Liria-Ulpiana SF -> Perparim Thaci Stadium, Prizren (Liria)
  2023-06-04 Ferizaj-Liria Final -> Ferizaj Synthetic Grass Stadium, Ferizaj
  2024-05-26 Prishtina E Re-Dinamo Fzaj. SF -> Sami Kelmendi Stadium, Hajvali
  2024-06-01 Prishtina E Re-Feronikeli Final -> Sami Kelmendi Stadium, Hajvali
  2025-05-25 Liria-Vushtrria SF -> Perparim Thaci Stadium, Prizren
  2025-05-31 Vushtrria-Llapi Final -> Ferki Aliu Stadium, Vushtrri
  (RSSSF/Wikipedia print no venues for these legs; home-ground convention
  applied and documented in the pack's venue NOTE.)
- KOSCUP: 0 rows with unknown/blank stadium or city (was 39 stadiums + 1
  city). All 23 home clubs resolved to documented grounds — pack constants
  where they existed (Drenica Skenderaj, Trepça'89, Liria, Fushë Kosova,
  Suhareka, Feronikeli, Ferizaj, Prishtina E Re, KF Ballkani-adjacent) and
  researched grounds for the lower-division clubs (Gjakova City Stadium,
  Shahin Haxhiislami Stadium, Ramiz Sadiku Stadium, Selajdin Mullabazi
  Stadium, Adem Jashari Olympic Stadium, Flamurtari Stadium, Ferki Aliu
  Stadium, Rilindja Stadium, Tahir Vokshi Stadium, Demush Mavraj Stadium,
  Dardania Stadium, KF Behari Stadium, Perparim Thaci Stadium for A&N
  Prizren, Ferizaj ground for Dinamo Fzaj.). ONE documented inference:
  TOP Football (Prishtina academy) has no published ground in any accessible
  index; its two home ties vs Prishtina are recorded at Fadil Vokrri
  Stadium, Prishtine — the only licensed Prishtina venue per FFK practice —
  and flagged in the pack's venue_policy NOTE for confirmation.
- Rilindja 74's city also fixed (Prishtine).

REGRESSION (D1-D4 + prior gates, fresh code): PASS
- KOSCUP: 0 rows with team "A" (D1); 0 "Ph'nix-Banje" rows (D2, only
  Phoenix-Banje); 0 lowercase "Prishtina e Re" (D3); 24 TEAM rows all
  non-pool (D4). Slice 24/24/24/26/25 = 123; finals match the official
  record (Llapi, Prishtina, Ballkani, Prishtina, Dukagjini); 0 duplicates;
  0 future dates; 0 degenerate names.
- KOS: unchanged data vs v2.0 except the 12 added rows, the 6 playoff
  venues, and the updated NOTES (pack_id/catalog/round_counts/perclub/
  appendix_inclusion/venue). No other drift.

OVERALL VERDICT
--------------------------------------------------------
**PASS — both v2.1 packs correct per the Director's correction order.**
All three blocking reasons are resolved and re-verified with fresh code:
complete standalone KOS (910 rows, 5/5 table reproduction from the pack
alone), zero venue placeholders in either pack, artifacts on the branch.

NOTE (transparency, not a defect): TOP Football's ground is a documented
inference flagged in the pack (see venue_policy NOTE); if the Director or a
later source confirms a different ground, the two rows are a one-line fix.

Evidence: audit_work/kos_koscup_reaudit_2026-08-07-v1.0/ (build_v21.py,
gates_v21.py, outputs; the gates script re-runs the full suite above).
========================================
