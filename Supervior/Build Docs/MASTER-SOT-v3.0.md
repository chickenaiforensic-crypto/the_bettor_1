# PITCH RATING — MASTER SOURCE OF TRUTH v3.0
## The single authority. Every pack. Every engine. Every gap.

**Issued:** 2026-08-08
**Branch:** `arena/019fde32-the-bettor-1`
**Authority:** Lead Intelligence Officer — this document supersedes all others.

---

## 0. QUICK REFERENCE — WHAT TO TRUST

| Artifact | Location |
|---|---|
| Verified store (5,082 rows) | `main:previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` |
| Current engine v5.0 | `engine_rebuild/pitch_engine_v5.0.js` (this branch) |
| Current app v5.0.0 | `engine_rebuild/app-v5.0.0.html` (this branch) |
| This document | `Supervior/Build Docs/MASTER-SOT-v3.0.md` |

Everything else is historical, stale, or aspirational. Read status tags below.

---

# PART A — DATA REGISTER

## A1. APPROVED IN STORE (5,082 rows)
| Scope | Rows |
|---|---|
| England Premier League | 1,900 |
| Russia (RPL + Cup + playoffs) | 1,579 |
| Czechia (First League + MOL Cup + playoffs) | 1,603 |

Store md5: `3c068c1f67ee8a81d412631fd0feb162`
Audited by independent fresh-code verification 2026-08-05.

## A2. AUDITOR APPROVED MATCH DATA (pending D5 fix)
| Pack | Branch | MD5 | MATCH |
|---|---|---|---|
| KOS v2.1 | `019fd805` | `cde3688f...` | 910 |
| KOSCUP v2.1 | `019fd805` | `cca71b17...` | 123 |

Audit: `019fd74a:Supervior/Build Docs/AUDIT-KOS-KOSCUP-REAUDIT-2026-08-07-v1.0.md`
Match data APPROVED. D5 TEAM-row realignment pending (mechanical fix).

## A3. CANDIDATE (self-gated, needs independent audit)
| Pack | Branch | MD5 | MATCH |
|---|---|---|---|
| SPA v2 | `019fd805` | `81e553a4...` | 1,900 |
| ITA v2 | `019fd4e0` | `05344481...` | 1,901 |
| GER v2 | `019fd4e0` | `afc99d36...` | 1,540 |
| FRA v2 | `019fd4e0` | `4b302b17...` | 1,686 |
| USOC v2.1 | `019fdd64` | `5875319c...` | 138 |

## A4. RETURNED (defects documented)
| Pack | Branch | MD5 | Defect |
|---|---|---|---|
| SCO1 v2 | `019fdd60` | `3f7dae5a...` | 2025-26 season MISSING, 1 duplicate |
| SCOCUP v2 | `019fdd60` | `d4584498...` | 2 out-of-slice, aet score verify |
| SCOLC v2 | `019fdd60` | `2f6ddfb6...` | Group stage MISSING (~140 rows) |

Self-audit: `019fdd60:handoffs/AUDIT-SCO-2021-2026.md`

## A5. INCOMPLETE
| Pack | Missing |
|---|---|
| MLS | 2025 regular season + 2026-to-date |

## A6. REJECTED
UEFA-CONNECTOR old, UEFA-FULL old, KOS v2 old. All fabricated/superseded.

---

# PART B — ENGINE REGISTER

## B1. CURRENT: v5.0 (per-league calibrated)

**Key differences from ENGINE_SPEC (all intentional, audited):**
- GMU: per-league measured (E0:2.97, RPL:2.73, CZ1:2.86) — spec was 2.6186
- Base rates: per-league measured from training — spec was global 44.6/26.8/28.6
- DRAW_TABLE: 15 cells per-league from training — spec was 27 cells from 59k-legacy
- TIER_WEIGHTS: per-league fitted — spec was 0.2/0.5/0.5

**Unchanged DC constants:** LR 0.055, DECAY 0.0022, HFA_LR 0.010, RHO -0.06, all clamps — verified byte-identical to Python reference.

**Harness:** EPL 0.6140, RPL 0.5630, CZ1 0.6044. Matches masterplan.

## B2. What exists in v5.0
| Layer | Status |
|---|---|
| L1 Dixon-Coles ratings | ✅ Python-verified |
| L2 scoreGrid + goalsGrid | ✅ Per-league GMU |
| L3 Star draw correction | ✅ Per-league tables |
| L4 Tier classification | ❌ Spec only |
| L5 Consensus labels | ❌ Spec only |
| R2 Evidence engine | ❌ LIVE-BLUEPRINT spec only, zero code |
| R3 ELO stars | ❌ Not built |

---

# PART C — DOCUMENT REGISTER

## Current / Binding
| Doc | Status |
|---|---|
| **MASTER-SOT-v3.0.md** (this) | ✅ SUPERSEDES ALL |
| AUDIT-ENGINE-REBUILD-R0-R1-2026-08-08.md | ✅ Current |
| AUDIT-SPEC-VS-ENGINE-v5.0-2026-08-08.md | ✅ Current |
| APP-EMBEDDED-SEED-REGISTER-v1.0.md (on 019fd71e) | ✅ Accurate |
| METHODOLOGY.md (md5 `6cd6c0c8...`) | ✅ Binding (P1-P5, I1-I6, T1-T8) |
| ENGINE_SPEC.md (md5 `91cd0cd5...`) | ⚠ DC math correct, constants stale |
| LIVE-BLUEPRINT.md (md5 `d01cfde0...`) | ⚠ SPEC ONLY — zero implementation |

## STALE — do not use for current state
- BLUEPRINT-SOT-2026-08-04.md — v3.6.3, 5,000-row, wrong pins
- ENGINE-MASTERPLAN-2026-08-05.md — no v5.0 reference
- FUNCTIONALITY-2026-08-05.md — describes v3.6.3 app
- VERIFICATION-DATA-2026-08-05.md — stops at 2026-08-05
- DIRECTOR-CONTROL-SOT-v1.0.md — wrong branch references
- All team_workspace/ docs — aspirational, references deleted branches

---

# PART D — BRANCH MAP

| Branch | Role |
|---|---|
| `019fde32` | THIS — Master SOT, v5.0 engine/app |
| `main` | v3.17.0-picker, 5,082 store, stale docs |
| `019fd805` | Researcher: KOS+KOSCUP+SPA |
| `019fd74a` | Auditor: KOS/KOSCUP D5 |
| `019fdd64` | Researcher3: USOC+MLS |
| `019fdd60` | Researcher2: Scottish (returned) |
| `019fd71e` | Director: seed register, design handoff |
| `019fd7e1` | Designer: UI/UX |
| `019fd4e0` | Builder: full chain, CONTAMINATED |
| `019fd213` | Planner: B0-B2, CONTAMINATED |

---

# PART E — GAP REGISTER

**Engine:** L4/L5 not built. R2 evidence engine not built. S5 cross-league blocked. I4/I5 not wired. M3 provenance not wired.

**Data:** KOS/KOSCUP D5 pending. SPA/ITA/GER/FRA awaiting audit. SCO returned. UEFA connector needed fresh. MLS incomplete.

**Docs:** BLUEPRINT-SOT stale. MASTERPLAN stale. FUNCTIONALITY obsolete. No v5.0 reference in any spec doc. LIVE-BLUEPRINT spec-only.

---

# PART F — NEVER-DO
1. No import without auditor approval
2. No seed data — quarantine
3. No KOS v2 / UEFA old packs
4. No ship without test-run artifact
5. No market data (P1)
6. No skip table reproduction
7. No reuse auditor scripts
8. No invent data
9. No wholesale merge of builder branch 019fd4e0
10. No claim country available without audit
11. No reference stale SOT/Functionality docs for current state
12. No global GMU 2.6186 or global base rates — use per-league

---

# PART G — PINS

| Asset | MD5 |
|---|---|
| Store 5,082 | `3c068c1f...` |
| App v5.0.0 | `0e2fdf9e104ddf246f0bb93ce49f4a04` |
| KOS v2.1 | `cde3688f...` |
| KOSCUP v2.1 | `cca71b17...` |
| SPA v2 | `81e553a4...` |
| SCO1 v2 | `3f7dae5a...` |
| SCOCUP v2 | `d4584498...` |
| SCOLC v2 | `2f6ddfb6...` |
| USOC v2.1 | `5875319c...` |
| ENGINE_SPEC | `91cd0cd5...` |
| METHODOLOGY | `6cd6c0c8...` |
| LIVE-BLUEPRINT | `d01cfde0...` |

---

*Single source of truth, 2026-08-08. Every claim traced to file/hash/branch/audit. If any other document disagrees, this one wins.*
