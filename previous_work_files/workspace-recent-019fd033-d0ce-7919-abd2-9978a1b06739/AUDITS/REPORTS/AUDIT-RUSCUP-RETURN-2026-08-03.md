# AUDIT CARD — RUSCUP return (WO-RUSCUP-BACKFILL-03) — staged 2026-08-03

**Return:** `handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` on branch `arena/019fc462-the-bettor-1`
commit `5134d94` (2026-08-03T10:58:55Z), layout re-org `675f894` (11:09:43Z). Main branch untouched (`bb0b453`).
**File:** 49,083 B · 289 lines · md5 `aef7f5ed402909b83565bf3f5ed42d59` (pinned).
**Content census:** 189 MATCH · 21 TEAM · 10 SOURCE · 68 NOTE · END ✓

## Verdict: RESEARCHER FIX REQUIRED (2 small items), then import-eligible.
Everything structurally hard — boundary, dupes, grammar, season shape, spot truth — PASSED.

## Gate results (all re-run auditor-side, never taken from his claims)

| Gate | Result |
|---|---|
| Boundary | PASS — max date 2024-06-02 < 2024-06-30 cutoff |
| Overlap vs held store (1,432 rows) | PASS — 0 collisions |
| Internal duplicates | PASS — 0 |
| Season shape vs his claim | PASS — 36 + 77 + 76 = 189 |
| **2021-22 row-level vs RSSSF** | **PASS — 36/36** date+teams+score exact (phase counts proven on RSSSF elite-group D1 tags: 22 group + 7 R16 + 4 QF + 2 SF + 1 final) |
| 2022-23 / 2023-24 bulk | SPOT SUITE PASS (incl. tricky dates: QF-up leg2 Dinamo 1-1 Krylya = 01.03.23 VTB ✓; SF leg2 Zenit 0-0 Spartak = 17.04.24 Gazprom ✓; CSKA 2-0 Baltika 16.04.24 ✓; SF leg1 Spartak 1-2 Zenit 04.04.24 ✓). Full-machine diff continues as second pass before import |
| Advancement-NOTE doctrine | PASS — 23 non-group draws analyzed: 14 NOTEd; 9 flagged → all 9 verified benign (7 = drawn FIRST legs; 2 = drawn second legs where the tie was decided on AGGREGATE, no shootout: Krylya 3-2 agg; Zenit 2-1 agg) |
| SOURCE discipline | PASS — RSSSF primary ×3 + Wikipedia second index ×3 + club-tier evidence, per §4 |

## Defect 1 — FC Ufa missing TEAM row (researcher)
3 MATCH rows use `FC Ufa` (2021-22 cup — Ufa were RPL that season, proven RSSSF rus2022 final table, 14th).
Ufa is NOT on our roster (our store starts 2024-25) and he did not declare it → rows unresolvable at load.
His own RPL-league workorder names Ufa as an expected addition ("club folded summer 2022 — NOTE it").
**Fix:** add `TEAM|FC Ufa|Russia|Russian Premier League|RPL|<aliases>|…` + fold NOTE.

## Defect 2 — KamAZ string mismatch (researcher)
2 rows use `KamAZ Naberezhnye Chelny`. Held identity = **`KAMAZ`** (seed pack, FNL, Naberezhnye Chelny).
At load this creates a DUPLICATE club. §3 identity discipline: use verbatim held names.
**Fix:** write `KAMAZ` (RSSSF prints "KamAZ Naberezhnyye Chelny" — our roster form governs).

## Defect 3 — compType `domestic-league` on cup rows (AUDITOR-OWNED, not researcher)
My workorder line was wrong ("matches our existing cup rows" — false; held rows = `domestic-cup`).
Loader keeps enum values verbatim → rows would type as league. **Erratum issued** (all 5 cup orders
→ `domestic-cup`; SCOLC → `league-cup`); auditor normalizes this pack's 189 rows at import-prep.

## Observation (accepted, logged) — round labels in venue field
Workorder-prescribed ("put the stage in the venue-detail field"). Loader treats non-enum venue values
as `normal` for venue logic → functionally safe, richer than held rows. Kept.

## Researcher logistics verdict
- 16/16 workorder mirrors on branch = **bit-identical** to pins (md5-verified). ✓
- Stale 2021-24 RPL order correctly archived. ✓
- Register (`supervisor/README.md`), status doc, audit ledgers, build tools present — good practice.
- Reminder stands: everything lives on the BRANCH; main unchanged. Merge decision = owner's after import approval.

---

## v2 — CORRECTED PACK (commit e22f3a4, 2026-08-03T13:53:42Z) — md5 `d8e3ff9e741de6db9ab9295dc0aaae30` (pinned)

- FC Ufa TEAM row present (full fields + alias chain) ✓ · TEAM rows now 22 ✓
- compType `domestic-cup` ×189 — errata applied by researcher himself, no normalization owe✓ ✓
- boundary ✓ (max 2024-06-02) · 0 dupes · 0 overlap vs held ✓ · season shape 36/77/76 unchanged ✓
- **1 micro-defect survives:** KAMAZ written `KAMAZ Naberezhnye Chelny` (2 rows) — held identity is exactly `KAMAZ`; the suffix makes it a NEW string → unresolvable at load / duplicate risk. Requested: write exactly `KAMAZ`. One-word patch, import-blocking by name-discipline rule.

## Status: content approved; import gated on the KAMAZ one-word patch (+ RUSCUP seasons 2/3 bulk machine-diff in second pass — spot suite + season-2021-22 36/36 already exact).

## v3 ADDENDUM (2026-08-03, commit `9dc08ee` 19:21:15Z) — KAMAZ-aligned, byte-pure
Researcher's own rebuild now writes exactly `KAMAZ` on the 2 rows (2021-10-27 v Ural; 2022-03-03 v Zenit) and carries the identity NOTE in-line. md5 `91bce98de5ff5f999a2f03f3ee7d3caa` · sha256 `c2658b490d63…` (matches commit message).
Auditor gates: byte-diff vs the approved `d8e3ff9e` — **MATCH-row delta = the 2 KAMAZ strings and nothing else** (189 MATCH / 22 TEAM / all `domestic-cup` / END ✓). Semantically identical to the auditor's hand-normalized import copy, which is therefore RETIRED (kept in `returns/RUSCUP/` as history; staging now uses the researcher's byte-pure file).
Self-reported "162/162" not accepted at face value per standing rule; verification above is by row-level diff + census, the gates of record.
