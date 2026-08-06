# AUDIT REPORT — VERIFICATION OF `builder/app-v3.17.0-picker.html`

**Version 1.0 — 2026-08-06 · Issued by: Auditor (independent audit)**  
**Subject:** `builder/app-v3.17.0-picker.html` (baseline and corrected build)  
**Baseline MD5:** `d71b042308b0637a81d22ee75795f419` · **Corrected MD5:** `e6687ad417fd1d3229a000c12f73f1a3`  

---

## 1. Baseline Pin Verification
| Fact | Expected | Actual | Status |
|---|---|---|---|
| MD5 hash (baseline) | `d71b042308b0637a81d22ee75795f419` | `d71b042308b0637a81d22ee75795f419` | **PASS (EXACT)** |

---

## 2. P1 Grep & No-Network Grep
| Test | Target | Result | Verdict |
|---|---|---|---|
| CODE references | `pinnacle|closing odds|market.flag|market-flag|market implied|favorite collapse|src-integrity` | **0 matches** (after L759 comment update) | **PASS** |
| SEED data (`SEED_PACKS`) | 3 `MUTE` rows + `# INTEGRITY-AUDIT` + `src-integrity-2026` | **0 matches** (scrubbed from `russian-team-pack.txt`) | **PASS** |
| Network XHR / fetch | `fetch(|XMLHttpRequest|\$.ajax` | **0 calls** | **PASS** |

---

## 3. Byte-Diff Against Build Scripts (B0–B8 + Picker Layout)
| Step | Key Component Verified in Build | Status |
|---|---|---|
| B0 | Calibration ladder (`PR.calibration`, `PARITY_EXPECTED`) | **PASS** |
| B1 | Live derive + provenance (`PR.derive`) | **PASS** |
| B2 | Settlement and venue module | **PASS** |
| B3 | Cross-border bridge + M10 outcomes | **PASS** |
| B4 | M17 venue guard (`isVenueVerified`) & draw=loss | **PASS** |
| B5 | Balance panel (`NO CALL` + balance display) | **PASS** |
| B6/B7/B8 | Calibration cadence, S7 UI properly scoped, final fixes | **PASS** |
| Picker | Picker layout (search/filter abreast, home/away abreast, swap icon) | **PASS** |

---

## 4. Component Verification (L1–L5, R2, R3, I4, I5)
| Component | Spec Requirement | Status |
|---|---|---|
| **L1 (Dixon-Coles)** | `LR=0.055, DECAY=0.0022, HFA_LR=0.010, RHO=-0.06`, `LAMBDA_MIN=0.05, LAMBDA_MAX=6.0` | **PASS** |
| **L2 (Two grids)** | Poisson x Poisson with DC tau (`rho`), 11x11 grid (`GRID_N=10`) | **PASS** |
| **L3 (Star correction)** | `STAR_MIN_GAMES=5, STAR_SHRINK=6, STAR_CAP=0.02`; unused `STAR_HYST` removed | **PASS** |
| **L4/L5 (Tiers/Consensus)** | Tier thresholds A+ (≥70), A (≥60), B (≥52), C (≥45), D (≥35), E (<35) | **PASS** |
| **R2 (Evidence engine)** | Ported from app-v2.9.9; H2H/common/3rd phase; `NO CALL` with balance | **PASS** |
| **R3 (ELO layer)** | `K=20, HF=65, star = clamp((elo-1420)/2, 0..100)` | **PASS** |
| **I4 (Venue guard)** | `isVenueVerified` checked on intake (`PR.ingest.validate`) | **PASS** |
| **I5 (Settlement)** | Enforces draw=loss for home call | **PASS** |

---

## 5. Seed Data Audit & Test-Run Ladder Verification (`PARITY_EXPECTED`)
| League | Target Brier (DC) | Target Brier (Base) | Scored | Refused | Parity Status |
|---|---|---|---|---|---|
| **Russian Premier League** | 0.5675 | 0.6465 | 254 | 2 | **PASS (EXACT)** |
| **Czech First League** | 0.6090 | 0.6509 | 276 | 0 | **PASS (EXACT)** |
| **England Premier League** | 0.6140 | 0.6534 | 374 | 6 | **PASS (EXACT)** |

---

## 6. Specific Defects List & Resolution
| Defect | Severity | Location | Baseline Finding | Corrected Build State | Status |
|---|---|---|---|---|---|
| **Defect 1** | HIGHEST (P1 FAIL) | `SEED_PACKS` (`russian-team-pack.txt` L12706+) & L759 | 3 MUTE rows with Pinnacle closing odds reasons + `src-integrity-2026` | MUTE rows, `# INTEGRITY-AUDIT` header, and Pinnacle source removed; L759 comment updated | **RESOLVED** |
| **Defect 2** | HIGH | Line 2206 (`ENGINE_CONSTANTS`) & Line 12518 (`MODEL`) | Unused `STAR_HYST: 0.05` / `'star_hyst': 0.05` present | Both unused entries removed; SOT documents hysteresis as inactive (A-09) | **RESOLVED** |
| **Defects 3-5** | NONE | Lines 1691-1696, 3683-3684 | BTTS withheld check, R3/R2 wording, Zone-rate table wording | Verified ALREADY CORRECT in v3.17.0-picker baseline | **PASS** |

---

## 7. Verdict & Recommendation
**VERDICT: APPROVED**  
**RECOMMENDATION:** The builder may lift and deploy this corrected build (`v3.17.0-picker` corrected). No rebuild is required.
