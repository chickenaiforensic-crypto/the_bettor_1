# LEAGUE-BY-LEAGUE DATA-QUALITY AUDIT — opened 2026-08-02

**Scope (owner decree):** last 5 past years (2021-22 → 2025-26 + current season). Doctrine confirmed: the app holds **each team's own result rows**; when two teams are called it computes them against each other — nothing is stored as an "opinion".
**Data under audit:** the owner's live store (pitch-rating-full 2026-08-02, verified through the migration gate) — 1,432 rows, 22 competitions, window ends 2026-08-01.
**Method per league:** ① inventory (rows, span, teams, seasons) ② season completeness (expected vs held) ③ standings recomputed from rows ④ cross-check against official/external tables ⑤ gap → commission or accept. Pasted tables are test targets, never inputs.

---

## INVENTORY — what we actually hold (from rows, not claims)

| Competition | Rows | Span | Teams | Seasons held |
|---|---|---|---|---|
| Czech First League | 561 | 2024-07-19..2026-07-31 | 19 | 2024-25, 2025-26, 2026-27(s) |
| Russian Premier League | 489 | 2024-07-20..2026-08-01 | 19 | 2024-25, 2025-26, 2026-27(9) |
| Russian Cup | 152 | 2024-07-30..2026-05-24 | 25 | 2024-25, 2025-26 |
| MOL Cup (Czech) | 63 | 2024-10-23..2026-05-20 | 44 | 2024-25, 2025-26 |
| Major League Soccer | 36 | 2024-10-19..2026-07-31 | 30 | 2024(p-o), 2026(part) |
| MLS Cup Playoffs | 28 | 2024 | 18 | 2024 only |
| US Open Cup | 21 | 2024 | 23 | 2023-24/2024 |
| Scottish Premiership | 19+10 | 2026-02..05 | 11 | 2025-26 run-in only |
| Kosovo Superliga | 12 | 2026-03..05 | 10 | 2025-26 partial |
| UECL/UCL/UEL qualifiers+LP | ~26 | 2024-07..2026-07 | — | scattered, fixture-led |
| Czech Relegation Playoffs | 8 | 2025/2026 | 8 | both |
| Club Friendly | 4 | 2026-06/07 | 5 | friendlies only |
| Russian Releg. Playoffs/Super Cup | 3 | 2025-26 | — | ✓ |

**5-year reality:** deepest coverage starts **2024-07**. No league yet spans 2021–24. Full 5-year depth per league = a backfill commission per league (≈720 rows per top-flight league for 3 seasons).

---

## LEG 1 — RUSSIAN PREMIER LEAGUE

**Holdings:** 489 league rows — **2024-25: 240/240 complete · 2025-26: 240/240 complete · 2026-27: 9 rows (MD1 ×8 + MD2 ×1, through 2026-08-01)** · +Russian Cup 152 · Super Cup 1 · playoffs 2.

**Recomputed champions (from our rows):**
- 2024-25: **FC Krasnodar 67 pts** (20-7-3, GD +36) · Zenit 66 · CSKA 59
- 2025-26: **Zenit 68 pts** (20-8-2) · Krasnodar 66 · Lokomotiv 53

**Cross-check vs the pasted "5-Year Cumulative (2021–2026+)" table:**
| # | Check | Verdict |
|---|---|---|
| 1 | Internal arithmetic (MP = W+D+L every row; promo/relegation gaps consistent) | ✅ passes |
| 2 | "2024-25 Champion: **Zenit**" — called "certified, non-disputed" | ❌ **FALSE.** Our complete season: **Krasnodar 67, Zenit 66.** Hallucinated title. |
| 3 | "2025-26 Champion: Zenit" | ✅ our table agrees (68 pts) |
| 4 | Baltika cumulative 32p / **8 wins** claimed | ❌ **impossible** — we hold Baltika's full 2025-26: **30 games, 11 wins** alone (+MD1 loss). Their row omits an entire season we can prove. |
| 5 | Current-16 roster (their 16 = our MD1 16 exactly) | ✅ |
| 6 | Every team shown "+2 played" for 2026-27 | ➕ beyond our snapshot (we hold 9 rows through 08-01) — exactly what the weekly central-request fills next |
| 7 | Ever-present implied 2021–24 splits (e.g. Zenit 58-20-13) | ⚪ unverifiable — pre-window; needs the 2021–24 backfill |

**Verdict:** the pasted table is **not import-grade** (2 proven fabrications on a 16-row table). Nothing enters the store from it. Our rows govern.
**RPL 5-year gap:** 2021-22, 2022-23, 2023-24 (≈720 rows) — commission ready on owner's word (researcher: complete seasons, RSSSF-grade, per the same pack grammar + acceptance reconciliation).

---

## NEXT LEGS (owner picks order; default as listed)
2. **Czech First League** — deepest (561); same recomputation vs official tables · 3. **Scottish** — after the depth pack; currently run-in only · 4. **MLS** — await round-2 supplier; currently playoffs-2024 + partial-2026 · 5. qualifiers/friendlies — fixture-led, no table audit.

**Rule carried into every leg:** pasted tables are hypotheses; the store is truth; discrepancies are resolved by re-verification against official archives, and every fix enters via a sourced pack, one approval, logged.

---

## COMPLETENESS VERDICTS vs independent archive (RSSSF, fetched 2026-08-02) — the standing gate

**Standing completeness gate (owner's design, formalized):** whole-tournament shape (every team uniform game count) **+** recomputed final tables must reproduce the official tables club-for-club (W-D-L, GF-GA, pts). Both required; both machine-re-runnable.

| Season | Shape test | Table diff vs RSSSF | Verdict |
|---|---|---|---|
| RPL 2024-25 | 240 rows · 16 clubs × 30 uniform | **16/16 EXACT** | ✅ complete + correct |
| RPL 2025-26 | 240 rows · 16 clubs × 30 uniform | **16/16 EXACT** | ✅ complete + correct |
| CZ1 2024-25 | 276 rows · split-format shape {35:12, 34:2, 32:2} | **12 group clubs EXACT + 4 placement EXACT** | ✅ complete + correct |
| CZ1 2025-26 | 276 rows · same shape | **12 + 4 EXACT** | ✅ complete + correct |
| RPL/CZ1 2026-27 | 9+9 rows (live, MD1+1) | n/a — season running | 🔄 fills weekly via D12 |
| Russian Cup 24-25/25-26 (152) · MOL Cup (63) · Czech pro/rel playoffs (8) | claimed complete per pack NOTEs | not yet re-diffed auditor-side | ⏳ queued (next audit step) |
| MLS / Scotland / Kosovo / UEFA quals / friendlies | partial by construction | n/a | ⚪ fixture-led, no full-tournament claim |

Bonus confirmations from the diff: Baltika's 2025-26 RPL membership **proven by official table** (46 pts, 6th) — the pasted 5-year table's Baltika row stands permanently refuted. The two "intruder" rows (Zbrojovka, Artis Brno) are correctly-tagged 2026-27 games of the newly promoted clubs — no mis-tagging.

## Repo: github.com/chickenaiforensic-crypto/the_bettor_1
Checked 2026-08-02: **public, 0 files (empty)**. Recommended content (anyone with write access commits via GitHub web UI): ① researcher returns (WORKORDER-RPL-2021-24 pack lands here as `RPL-2021-24_BP-TEAM-PACK_v2.txt`) ② per-season official final tables (RSSSF snapshots) so every future verification runs offline ③ match packs archive. Transport + verification rules unchanged: text files, md5 pinned, pasted tables never enter the store.

---
## 2026-08-02 — RPL backfill "return" FAILED AT INTAKE (nothing entered any pipeline)
Researcher session reported 5 files committed to repo (`data/rpl_standings_2021_22_to_2025_26.csv/.json`, `data/rpl_season_summary_...csv`, `docs/RPL_DATA_AUDIT.md`, README.md) covering "RPL 2021-22 … 2025-26".
**Auditor probe (this session):** git tree of `main` still shows ONLY `README.md` (15 B); single commit `d14c043a` "Initial commit"; both claimed files return **404** on raw probe. Zero bytes committed.
**Fatal defect on their own admission:** "I treated RPL as **Rwanda** Premier League" — wrong federation. Programme RPL = Russian PL (Zenit/CSKA/Krasnodar…). Rwanda data is inadmissible in full.
**Fatal defect 2:** deliverable class wrong even before content — standings tables, while the workorder demands **match-result rows** (date/home/away/score, 3×240 + playoffs, cutoff <2024-06-30). Doctrine: tables are recompute TARGETS, never inputs.
**Also refuted by record:** 2024-25 + 2025-26 are already held complete + verified 16/16 vs RSSSF — re-collecting them was out of scope.
Disposition: no import possible; correction message issued to researcher (re-read WORKORDER-RPL-2021-24-BACKFILL.md; return `RPL-2021-24_BP-TEAM-PACK_v2.txt` via chat/b64 or a COMMITTED repo push). Repo remains effectively empty until a push is provable by probe.


---
## 2026-08-02 — DECREE CLARIFICATION (owner, verbatim reasoning): the window is continuous, not capped slices
"we are getting all 5 year season data up to today … ensure our data (old) is not missing anything … we are researching all data so that we dont get gaps."
**Registered doctrine:** the 5-year rule defines how far back each league/cup is built (2021-22 season onward). It does NOT cap the forward edge: each federation's span must run **continuously to today** and must be **gap-free end to end** (backfill segments + held 2024-26 segments + current-season weekly updates joined seamlessly). Researcher-side research of all data = the CONTROL RECORD; auditor diffs the full span against it after every return. Any official match in the span stored nowhere = written gap defect; commission stays open until filled or explained. Weekly D12 central-request keeps the leading edge current thereafter. The four workorders carry this as "§5.1 Continuity clause"; handoffs README rule 7.
