# RETURN — KOS + KOSCUP (Researcher, 2026-08-07)

**Deliverables:**
- `handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.txt` — Kosovo Superliga (workorder WO-KOS-SPAN-06)
- `handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.txt` — Kosovo Cup (workorder WO-KOSCUP-SPAN-11)

**Relay note:** the message referenced `team_workspace/researcher_handoffs/RELAY-MESSAGES-DATA-RESEARCH-2026-08-07-v1.0.md`, which does not exist in the repo. The two item numbers (1. Kosovo Superliga, 2. Kosovo Cup) map to the two HALTED workorders (#13 KOS, #14 KOSCUP per WORKORDER-INDEX), whose prior packs were rejected as fabricated. Both are now re-delivered from authentic sources. If a separate relay file exists, drop it and I will reconcile.

---

## What was delivered

### KOS — 898 MATCH rows
- **888 league rows** = 5 full seasons × 180, minus the 12 already-held appendix rows (2025-26 Malisheva run-in; appendix-exclusion gate: 0 leaks).
- **10 playoff rows** = Kosovo Relegation Playoffs, semifinal + final per season (competition string `Kosovo Relegation Playoffs`, compType `other` per ERRATA-2026-08-03 Family B).
- **8 TEAM rows**: Ulpiana, Feronikeli, Trepça'89, Fushë Kosova, Liria, Suhareka (workorder §2) + Vushtrria, Dinamo Fzaj. (playoff opponents).
- Venue-detail `RS R1`..`RS R36`, `Playoff-SF`, `Playoff-Final`; stadium/city from Wikipedia season-article stadium tables.

### KOSCUP — 123 slice ties
- Every cup tie with ≥1 Superliga club of that season, entry round → final: 2021-22 = 24, 2022-23 = 24, 2023-24 = 24, 2024-25 = 26, 2025-26 = 25 (counts recomputed in the pack's slice_counts NOTE).
- compType `domestic-cup` per ERRATA-2026-08-03 Family A (cited in the pack).
- 47 TEAM rows for lower-division opponents (division per RSSSF page tables).
- 23 advancement + 7 aet + 3 awarded NOTE lines (brackets reconstructible).

## Sources
- **Primary:** RSSSF `tablesk/kosovo2022..2026.html` — round grids, final tables, cup chapters, playoffs (fetched 2026-08-07; transcriptions + fresh parser in `kos_ledgers/`).
- **2025-26 adaptation:** the RSSSF kosovo2026 page carries the final table but **no round-by-round grid** → rows carried by worldfootball.net matchday pages (36/36 fetched, dates+scores), cross-checked against the Wikipedia FBR matrix (source FFK): **179/180 identical**; the single divergence is the MD12 award (see below).
- **Second indexes:** Wikipedia season-article FBR matrices (2021-22..2024-25 sampled diffs all identical), Wikipedia 2025-26 article (table, playoff dates/venues, stadiums), worldfootball 2024-25 MD26 (adjudication).

## Self-check gates (fresh code, re-runnable: `kos_ledgers/final_gates_kos.py`)
| Gate | Result |
|---|---|
| KOS rows | 888 league + 10 playoff ✓ |
| Table reproduction | **PASS — all 5 seasons, 50/50 club-seasons** (2025-26 = pack + appendix = 180 → official table) |
| Per-club 36-match | PASS per club-season (counts reflect appendix exclusions exactly) |
| Duplicates / future-dated | 0 / 0 ✓ |
| Names | league rows 100% from the 16-pool; playoff outsiders declared TEAM rows ✓ |
| Appendix | 0 leaks; all 12 verified present in source data ✓ |
| KOSCUP slice | 123 ties, **0 rows without a Superliga club of that season** ✓ |
| KOSCUP dupes/future | 0 / 0 ✓ |
| Bracket | champions per edition match the official record (Llapi, Prishtina, Ballkani, Prishtina, Dukagjini) ✓ |

## Documented items the auditor should see
1. **2025-26 primary gap:** RSSSF kosovo2026 has no round grid — adaptation NOTE in the pack (same pattern as SPA/EPL precedents).
2. **MD12 award (2025-26):** Prishtina E Re 3-0 Drenica (2025-11-02) — Wikipedia matrix prints on-pitch 0-0; worldfootball prints 3-0 (dec.); the RSSSF official table reproduces **only** with 3-0 → row carries 3-0, `NOTE|warning|source_conflict` + `NOTE|warning|awarded`.
3. **Awarded league ties:** 2021-22 MD27 Gjilani 0-3 Ballkani (abandoned at 1-1, crowd trouble); 2021-22 MD30 Ulpiana 0-3 Ballkani (ineligible player); 2024-25 MD21 Ballkani 3-0 Feronikeli (originally 1-1). 2024-25 MD3 Drita 4-2 Suhareka carries the revoked-award note (played score governs).
4. **Walkover:** 2022-23 cup R1 Vëllaznimi o/w Prishtina → row Vellaznimi 0-3 Prishtina + awarded NOTE (Prishtina advanced; consistent with the cup bracket).
5. **Postponed matches** filed by played date with original round labels (listed in the continuity NOTE).

## Working files (evidence)
`kos_ledgers/` — RSSSF transcriptions, Wikipedia matrix, worldfootball carrier, parser, per-season JSONs, pack builders, gate scripts.

— Researcher, 2026-08-07
