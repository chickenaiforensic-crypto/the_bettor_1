# ENGINE CORRECTION TASKLIST — v5.0 Recalibration
## Fix every inherited constant to match our data

**Issued:** 2026-08-08
**Branch:** `arena/019fde32-the-bettor-1`
**Status:** BUILDING

---

## AUDIT FINDINGS (what's wrong)

| # | Defect | Impact |
|---|---|---|
| D1 | Global base rate (44.6/26.8/28.6) doesn't match our data (43.7/24.0/32.3) | Gain claims inflated by 3-5pp |
| D2 | GMU 2.6186 vs our 2.83 — 8% off | Goals-grid shrinks toward wrong mean |
| D3 | DRAW_TABLE from 153k-match legacy — star gap rates wrong for our leagues | Star correction pushes toward wrong targets |
| D4 | Cup matches (MOL Cup: H=23%) mixed with leagues (CZ1: H=45%) | Per-league ratings polluted |
| D5 | Per-league draw rates differ (E0=23.0%, RPL=24.3%, CZ1=23.3%) | One global base can't serve all |
| D6 | Brier scoring always uses global base — dishonest comparison | Must report vs local base |

---

## PHASE 1 — ENGINE CORRECTION (v5.0)

### Measured per-league constants (from audit)

| Constant | E0 | RPL | CZ1 | ALL |
|---|---|---|---|---|
| Base H | 44.5% | 45.1% | 43.0% | 43.7% |
| Base D | 23.0% | 24.3% | 23.3% | 24.0% |
| Base A | 32.4% | 30.6% | 33.7% | 32.3% |
| GMU | 2.91 | 2.72 | 2.84 | 2.83 |
| League-only H | 44.2% | 45.1% | 44.9% | — |
| League-only D | 23.9% | 25.5% | 24.3% | — |
| League-only GMU | 2.93 | 2.73 | 2.78 | — |

### Tasks

- [x] T1.1: Measure all per-league constants from our data (done)
- [ ] T1.2: Fit per-league DRAW_TABLE from training (masked, 2021-24)
- [ ] T1.3: Build corrected engine v5.0 — per-league config, no global defaults
- [ ] T1.4: Replace GMU with per-league measured mean
- [ ] T1.5: Engine.score() reports vs local base (primary) + global (reference)
- [ ] T1.6: Run harness with corrected constants
- [ ] T1.7: Compare O2.5 calibration with corrected GMU
- [ ] T1.8: Audit — all constants traced to measured data
- [ ] T1.9: Audit report documenting every change and measured impact

## PHASE 2 — APP SHELL v5.0

- [ ] T2.1: Embed corrected v5.0 engine inline
- [ ] T2.2: Per-league base rate display
- [ ] T2.3: Honest gain reporting vs local base
- [ ] T2.4: O/U calibration display
- [ ] T2.5: Zero seeds, zero pivot, zero network, zero market data

## PHASE 3 — UI/UX REBUILD

- [ ] T3.1: Verdict card — probability + confidence + league context
- [ ] T3.2: NO CALL with balance panel and reasons
- [ ] T3.3: Coverage tab — what leagues have data, what's missing
- [ ] T3.4: Data import — one gate, held cards, approve order
- [ ] T3.5: Settlement ledger — draw = loss (I5)
- [ ] T3.6: Provenance panel on every number
- [ ] T3.7: Plain language (A-02) throughout
- [ ] T3.8: Single HTML file, zero network

## PHASE 4 — DATA IMPORT (after audit)

- [ ] T4.1: Load 5,082 verified store
- [ ] T4.2: Import KOS v2.1 after D5 fix (+1,033)
- [ ] T4.3: Import SPA/ITA/GER/FRA v2 after audit (~7,027)
- [ ] T4.4: Re-run harness on expanded store

---

*Every task traced to the audit. No inherited constants. No silent rewrites.*
