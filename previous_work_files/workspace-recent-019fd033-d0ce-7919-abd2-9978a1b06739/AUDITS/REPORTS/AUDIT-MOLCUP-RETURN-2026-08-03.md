# AUDIT CARD — MOL Cup return (queue ④) — 2026-08-03
**Return:** `handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt` · branch commit `210a9aaa` (2026-08-03T17:02:56Z), re-carried at HEAD `9dc08ee` · 38,372 B · md5 `662fe5dfe38002474855110b2a17ea6c` · sha256 `5023eb33fd7a63f5…` (matches commit message)
**Census:** 120 MATCH · 31 TEAM · 33 NOTE (20 advancement) · 15 SOURCE · END ✓ · every MATCH row = `MOL Cup` / `domestic-cup` (errata-consistent) · all rows 14-field uniform, TEAM 13-field uniform

## Verdict: APPROVED (every gate re-run by auditor, none accepted from the researcher's self-report)

| Gate (auditor re-run) | Result |
|---|---|
| **RSSSF R16→Final diff, 3 seasons** | **45/45 ties accounted** — 34 machine-verified (29 EXACT date+score+order; 6 AET/pens rows carry correct 90-min score; 1 disclosed postponement Plzeň–Zlín SF RSSSF [Apr 4] → real 2024-04-24, source_conflict NOTE present) + 3 documented no-top-flight exclusions absent as commissioned (Dukla–Vyškov, Velvary–Opava R16 2023-24; Opava–Dukla QF 2024) + 6 "1.FC Slovácko" ties manually line-verified (digit-leading name defeats the parser, not the data) |
| Slice rule (WO §1: ties with ≥1 top-flight club) | **41 + 41 + 38 = 120 ✓** (exclusions listed above are the only no-FL ties in-round — verified from RSSSF chapter) |
| 90-min doctrine | 20 aet/pens ties: **20/20 advancement NOTEs wired to exactly 1 MATCH row each**, 90-min score on the row, outcome scored correctly (pens rows all draws; aet winner directions all correct) |
| Silent-AET defect (Slovácko 3-1 Karviná, RSSSF prints no [aet]) | handled: row 1-1 + NOTE "(aet 3-1)"; conflict disclosed in pack ✓ (nothing silently propagated) |
| Duplicates | 0 (date+home+away) |
| Names | 0 unresolved (every MATCH name = held roster or declared TEAM/alias); **0 TEAM collisions** with the held roster (31/31 new) |
| Hold risk (app code re-read, lines 899-928) | none: no tieIds anywhere; pair-frequency >2 (Sparta–Slavia ×3) is skipped by the app's `legs.length !== 2 → return` rule — hold only fires on tieId groups >2 or per-leg tieIds on a 2-row pair |
| Boundary | min 2021-08-24 · max 2024-05-22 < 2024-06-30 hard cutoff ✓ (2024-25 + 2025-26 already held) |
| R2/R3 rounds (78 rows — outside the RSSSF page) | researcher's wiki+worldfootball dual transcription (ledgers `audit/ledger/molcup-*` on branch) + structural gates above + all 8 R2/R3-era advancement rows wire-checked. **Bulk machine-diff vs worldfootball queued to second pass** (same standard applied to RUSCUP group stages) |

**Import-order condition (binding):** MOLCUP lands BEFORE the CZ1 patch — it declares `TEAM|Vlasim` and `TEAM|Pribram`, neither held as of export 2026-08-02, which the CZ1 patch's 12 playoff rows reference.
