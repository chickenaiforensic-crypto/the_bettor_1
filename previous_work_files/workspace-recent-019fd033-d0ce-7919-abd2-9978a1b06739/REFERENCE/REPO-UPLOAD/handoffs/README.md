# handoffs — where returns land

Every return from a researcher or builder session is dropped here (via the owner) as ONE text file.

## Binding rules
1. **Match rows, never tables.** A return is a list of played games: date / home team / away team / score (90-minute doctrine). Standings tables are recompute *targets* — never accepted as input.
2. **Format:** BP-TEAM-PACK v2 exactly as defined in the Supervisor workorder that commissioned the work.
3. **Naming:** `<LEAGUE>-2021-2026_BP-TEAM-PACK_v2.txt` (e.g. `RPL-2021-2026_BP-TEAM-PACK_v2.txt`) — span-named even though NEW rows stop at 2024-06-30, because approval certifies the whole 5-year span up to today.
4. **Text files only. No .zip, ever.**
5. **Auditor verification before anything enters the app:** boundary scan, dedupe vs the live store, full-season table reproduction vs the official record (16/16 or the return is rejected). Nothing is imported on trust.
6. **Never guess.** If a fact in the workorder is genuinely unknowable, write a NOTE line — do not fabricate numbers.
7. **Continuity (owner decree 2026-08-02):** the 5-year window runs GAP-FREE from 2021-07 up to today. The cap limits how far back we build — never how current we are. Every return is audited against the full research record for the whole federation span; an unexplained hole — in the new rows OR in our old rows — keeps the commission open.

## Commission queue (research may run in PARALLEL -- owner decree 2026-08-02; auditor approvals stay one card per return, processed in queue order)
1. **OPEN:** `Supervisor/WORKORDER-RPL-2021-2026-5YSPAN.md` -- **Russian Premier League**, 2021-22/22-23/23-24 new rows (2024-26 already held+verified) -> ~720 rows.
2. **STAGED:** `Supervisor/WORKORDER-CZ1-2021-2026-5YSPAN.md` -- **Czech First League**, same window -> 828 rows (276/season incl. playoff stage).
3. **STAGED:** `Supervisor/WORKORDER-RUSCUP-2021-2026-5YSPAN.md` -- **Russian Cup**, same window -> the audited slice (every tie with a top-flight club, all rounds).
4. **STAGED:** `Supervisor/WORKORDER-MOLCUP-2021-2026-5YSPAN.md` -- **Czech MOL Cup**, same window -> the audited slice.
5. **STAGED:** `Supervisor/WORKORDER-SCO1-2021-2026-5YSPAN.md` -- **Scottish Premiership**, full span 2021-22 -> today minus 29 held rows -> ~1,100 rows (228/season incl. both post-split groups).
6. **STAGED:** `Supervisor/WORKORDER-KOS-2021-2026-5YSPAN.md` -- **Kosovo Superliga**, full span 2021-22 -> 2025-26 minus 12 held rows -> ~890 rows (NOT Albania or Serbia -- name collision, read section 0).
7. **STAGED:** `Supervisor/WORKORDER-MLS-2021-2026-5YSPAN.md` -- **Major League Soccer**, full span 2021 -> today minus 64 held rows -> ~2,800 rows, THE BIG ONE.
8. **STAGED:** `Supervisor/WORKORDER-USOC-2021-2026-5YSPAN.md` -- **US Open Cup** (editions 2022-2026; 2021 was cancelled, the NOTE is mandatory) -> slice: every tie with an MLS club, minus 21 held rows -> ~230.
9. **STAGED:** `Supervisor/WORKORDER-SCOCUP-2021-2026-5YSPAN.md` -- **Scottish Cup** -> slice: every tie with a Premiership club (entry: 4th round), 2021-22 -> today -> ~130. Zero held rows.
10. **STAGED:** `Supervisor/WORKORDER-SCOLC-2021-2026-5YSPAN.md` -- **Scottish League Cup** -> slice incl. group stage + European-club byes as NOTEs -> ~170. Zero held rows.
11. **STAGED:** `Supervisor/WORKORDER-KOSCUP-2021-2026-5YSPAN.md` -- **Kosovo Cup** (Kupa e Kosoves) -> slice: every tie with a Superliga club -> ~100. Zero held rows.
12. **STAGED:** `Supervisor/WORKORDER-EPL-2021-2026-5YSPAN.md` -- **England Premier League** (owner decree 2026-08-03, major leagues) -> 1,900 rows. All 27 clubs already on roster.
13. **STAGED:** `Supervisor/WORKORDER-SPA-2021-2026-5YSPAN.md` -- **Spain La Liga** -> 1,900 rows. All 26 clubs already on roster.
14. **STAGED:** `Supervisor/WORKORDER-ITA-2021-2026-5YSPAN.md` -- **Italy Serie A** -> 1,900 rows. All 27 clubs already on roster.
15. **STAGED:** `Supervisor/WORKORDER-GER-2021-2026-5YSPAN.md` -- **Germany Bundesliga** (18 clubs / 306 per season, NOT 20/38) -> 1,530 rows. All 25 clubs already on roster.
16. **STAGED:** `Supervisor/WORKORDER-FRA-2021-2026-5YSPAN.md` -- **France Ligue 1** (TRAP: 20 clubs until 2023, then 18) -> 1,678 rows. All 26 clubs already on roster.

Items 1-4 use a hard 2024-06-30 cutoff (2024-26 already held+verified; recollecting = automatic fail). Items 5-8 have appendix DO-NOT-RETURN lists (items 9-11 hold nothing, no appendix). All 16 share the same doctrine: tables/brackets must reproduce the official record; 90-minute scores + advancement NOTEs on every AET/pens tie; no guessing, NOTE-blocker instead.
**NOT commissioned (fixture-led tier -- no complete-tournament claim exists to verify):** UEFA Champions/Europa/Conference League qualifiers & group ties (we hold only our tracked clubs' ties, added as they occur), Club Friendlies, and the one-match Super Cups.
