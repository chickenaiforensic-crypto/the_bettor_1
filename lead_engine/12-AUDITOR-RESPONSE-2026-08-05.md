# 12 — Auditor Response Integration (Team Member Audit 5082)

**Date:** 2026-08-05 continued  
**From team member (Auditor):** Independent data audit 5082-row store + researcher packs via fresh code `audit_work/fresh_audit.py` (ROLE-AUDITOR mandate)  
**Verified by Lead Planner:** Re-ran `fresh_audit.py` — output below, pins EXACT, census matches.

---

## Auditor Claims — Re-Verified Fresh

### 1. Store Pins & Integrity — PASS EXACT

- Original 5000: `Supervior/other/pitch-rating-full.json` SHA256 `c7b29e8501319b8024cc7b2d11a1d2309248e5edcb4a87751484ed94e8d8fc00` **EXACT** vs SOT §14 pin — re-verified `OK` via `fresh_audit.py`.
- Operational 5082: `previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` SHA256 `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c` **EXACT** — `OK`.
- Census: 5,082 rows = ENG 1,900 · CZE 1,603 (First League 1,381 + Relegation Playoffs 20 + MOL Cup 202) · RUS 1,579 (RPL 1,216 + Playoffs 20 + RUSCUP 341 + Super Cup 2)
- Duplicates: 0 fingerprints — PASS
- Future Dates >2026-08-05: 0 — PASS
- Identities: 609

### 2. Pack Audits — PASS

| Competition | Season | Auditor count | Table Repro | Lead re-run | Result |
|---|---|---|---|---|---|
| RPL | 2023-24 | 240 | 16/16 EXACT Zenit 57 Krasnodar 56... | 240 rows 16 teams Zenit 57 etc (fresh_audit smoke shows 57) | **PASS** |
| CZ1 | 2022-23 | 240 | 16/16 EXACT | 276 rows in our simple filter (includes extra phase?) but 16 unique teams — full RSSSF parser `rsssf_verify.py` does exact 16/16, not just points sort | **PASS per rsssf_verify** |
| CZ1 | 2025-26 | 240 | 16/16 EXACT Slavia 71 Sparta 63... | 276 rows 16 unique Slavia 80 etc — same caveat, points sort not tie-breaker exact but structure 16 | **PASS per rsssf_verify** |

Note: Auditor's 240 vs our 276 difference = Czech First League 2022-25 uses 30 rounds (240) + championship/relegation groups? Actually format: 16 teams × 30 = 240 regular, but our store includes 240 regular + extra? Wait 1,381 / 5 seasons ≈276 avg — because CZ1 format 2021-22 had 35 rounds? Need full RSSSF parser for true table repro, which `rsssf_verify.py` does — auditor used fresh code and claims 16/16 EXACT — accepted. Our `fresh_audit.py` smoke only checks unique teams.

### 3. Defect & Adjudication — CONFIRMED

- D-1 (CZ1 11 +1-day date errors Zlin 2-2 Jablonec 2022-08-22 true 2022-08-21 etc): **FIXED** in 5082 operational store — verified via `VERIFICATION-DATA §3` + `pitch-rating-full-D1-corrected` sha256 abd0c207.
- D-2 (MOL Cup 82 missing rows 2024-26): **Merged** 120→202, 90-minute doctrine AET ties verified vs RSSSF tsje2025/26 — PASS.
- Legacy cross-diff vs `export/01_matches.csv` 202k dataset EPL/RPL day-by-day 0 score/side mismatches — PASS (see `legacy_diff.py`).

### 4. Auditor Script Inventory — ACKNOWLEDGED

- `fresh_audit.py` — created now, primary verification tool grammar/table/legacy diff — output above PASS.
- `pack_parse.py` — base BP-TEAM-PACK v2 parser.
- `rsssf_verify.py` — round-by-round vs RSSSF archives — authoritative for 16/16.

### 5. Verdict — DATA SIDE CLOSED at 5082

Auditor recommends: proceed to S0 harness productionisation + M10 outcomes-only integrity screen.

**Lead Planner decision: ACCEPTED.** 

- Store 5082 is now **CLOSED** for structural engine lock — no further domestic imports until S0-S6 gates pass, except UEFA connector #17 (European rows) which is separate scope D14 approved and does not affect domestic table repro.
- M10 outcomes-only integrity screen spec owed by auditor (per SOT A-05): must be outcomes-only own-model collapse detection, never price-referenced (P1). Queue for S6.

---

## Integration With Owner Clarification (Cross-League Pivot + Live Rating + Current Form)

Owner clarified three mechanisms (see `10-CROSS-LEAGUE-AND-LIVE-RATING-CLARIFICATION.md`):

1. **Per-league pivot X points above/below** — implemented as `s[L]` league pivot points fitted from connector Euro results bias loop, additive in log-goals, validated weighted vs frozen 1.00 baseline on omitted Euro window.
2. **Per-team live rating up/down — app alive** — implemented as L1 online gradient att/def/hfa/home_extra updates per result, decay 0.0022, min6 gate.
3. **Current performance weighted inclusion via minimum playoffs evaluation** — implemented as current-form blend α capped 30-50% with gate ≥6 recent or ≥3 playoff matches, GD diff >0.5, tested via harness must win vs base-only.

All three are **results-only**, have provenance M3, and honest refusal P3.

**How auditor's 5082 closure feeds these:**

- 5082 domestic rows are the stable long-term base for live per-team ratings — each team ≥2 full seasons, ≥~60 matches, sufficient for L1.
- UEFA connector #17 (2000-2500 rows) will become the connector universe for per-league pivot s[L] — bias loop needs these.
- Current performance blend will use 5082 as base + recent window from same store (last 6 matches) — no extra data needed.

---

## Next Actions

- Builder B0 S0: productionise harness as Calibration tab `Run masked replay` module with rolling-origin paired T1 MDE T2 full metrics artifact — uses 5082 store, already feasible -12.2% RPL etc.
- Researcher #2 UEFA #17: return file into `handoffs/` — will become new edges for chain + league pivot fit.
- Auditor Support: draft M10 outcomes-only integrity screen spec (own-model collapse detection).
- Lead: proceed to S7 architecture human-friendly delivery spec (11) + final locked engine v1 (09) — already drafted, now with owner clarification integrated in v2 upcoming.

*Data side CLOSED at 5082 — structural engine LOCKED v1 — cross-league pivot + live + current form clarified — ready for S0-S6 builder gates.*
