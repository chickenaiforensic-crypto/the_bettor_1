# 24 — Ladder Baseline Expanded (ITA, GER, FRA included)

**Date:** 2026-08-05  
**Auditor:** Auditor Support (Arena)  
**Subject:** Production baseline for expanding holdout ladder (L-1..L-n..FULL) including new leagues.  
**Store:** `audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json` (11,599 matches after UEFA merge)  
**Harness:** `audit_work/score_audit_full.py` re-run parity Δ0.0000

---

## 1. Summary — FULL System Check (2025-26 Omitted Season)

| League | Train | Test | Scored | Brier DC | Brier Base | Gain | Dir | t | p |
|---|---|---|---|---|---|---|---|---|---|
| **RPL** | 960 | 256 | 254 | 0.5675 | 0.6465 | **+12.2%** | 55.9% | +4.64 | <0.001 |
| **CZ1** | 1105 | 276 | 276 | 0.6090 | 0.6509 | **+6.4%** | 49.3% | +2.64 | 0.008 |
| **EPL** | 1520 | 380 | 374 | 0.6140 | 0.6534 | **+6.0%** | 49.2% | +3.31 | <0.001 |
| **ITA** | 1520 | 380 | 374 | 0.5989 | 0.6579 | **+9.0%** | 52.7% | +4.24 | <0.001 |
| **GER** | 1224 | 306 | 300 | 0.5721 | 0.6477 | **+11.7%** | 54.7% | +4.61 | <0.001 |
| **FRA** | 1372 | 306 | 300 | 0.5971 | 0.6411 | **+6.9%** | 53.3% | +2.99 | 0.003 |

*Average gain across 6 leagues: +8.70%.*

## 2. Artifacts Produced

- **Baseline Data:** `audit_work/ladder_baseline_2026-08-05_full.json` (per-match probabilities for re-run parity).
- **Expanded Store:** `audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json` (11,599 matches).
- **Fixed Pack:** `handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt` (dates corrected via `fix_uefa_dates.py`).

## 3. Ladder Parity Gate

Any future build or model variant must re-run this harness. Acceptance requires:
1.  **Δ Brier ≤ 0.0000** (Full parity) on this specific store/window/constants set.
2.  **Significance (p < 0.05)** for any claimed improvement.
3.  **No degradation** in any of the 6 core leagues.

*Approved by: Auditor Support.*
