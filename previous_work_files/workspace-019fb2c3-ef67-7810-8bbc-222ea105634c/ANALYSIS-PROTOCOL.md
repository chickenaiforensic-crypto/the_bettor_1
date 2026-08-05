# ANALYSIS PROTOCOL — Per-Fixture Method

**Status: AUDITED AND ENFORCED IN CODE. Version 1.0 · 2026-07-30**
Audit found 3 gaps between document and implementation. All 3 fixed and re-verified.

---

## PART 0 — THREE CORRECTIONS YOU NEED BEFORE APPROVING

### C1. My over/under numbers were fabricated

```python
def grid(gd, tot=2.65, ...):   # ← total goals HARDCODED for every fixture
```

Every O2.5 figure I published came from a fixed constant of **2.65 goals**. It was never measured from either club's scoring rate. The numbers appeared to vary only because the *split* between home and away changed — the *total* never did.

| Chain estimate | xG shown | Total | O2.5 shown |
|---|---|---|---|
| +0.11 | 1.45–1.21 | 2.66 | 49.6% |
| +0.42 | 1.61–1.06 | 2.67 | 50.0% |
| +1.29 | 2.07–0.65 | 2.71 | 51.0% |

The total is pinned at ~2.65 by construction in every case.

**Consequence: every over/under figure I gave you must be discarded.** They are not evidence.

### C2. Your weighted scale was tested on a narrower basis than you may have intended

I tested it as a **chain metric** — summing scores across opponent links. Result: r = +0.273 vs +0.310 for plain goal difference, McNemar p = 0.0495. Significantly worse *for that specific use*.

I did **not** test it as a team-strength rating, a form table, or a draw filter. Those are different jobs and the verdict does not transfer.

### C3. What validated static data exists right now

| Asset | Records | Status |
|---|---|---|
| `edges.pkl` — match graph | 202,092 | built, identity-merged |
| `chain_calib.pkl` — tier calibration | 1,304 | **validated** vs outcomes |
| `weighted_test.pkl` — weighted-scale test | 1,203 | **validated** |
| `fix30_merged.pkl` — current card | 17 | **unvalidated output** |

The graph and the two calibration sets are solid ground. The fixture card is not, until it passes the protocol below.

---

## PART 1 — PRINCIPLES

**P1. Results only.** No odds, no market, no commentary. Standing directive.

**P2. Home perspective.** Every output framed as home wins / draws / loses.

**P3. Strict causality.** Only matches played before the fixture date.

**P4. Nothing published without a measured base rate.** If a quantity has not been validated against outcomes, it is not reported. This is the rule C1 broke.

**P5. Evidence grade travels with every number.** A figure without its path count, spread and grade is incomplete.

**P6. The measured ceiling governs.** Chain tier CH-A tops out at **65.7%**. Anything above is extrapolation and must be labelled so.

**P7. The system may refuse.** NO CALL beats a fabricated number.

**P8. Test the user's construction as specified**, not my reinterpretation.

**P9. One test at a time**, reported before the next begins.

**P10. Every phase audited before the next starts.** Failed audit = stop.

---

## PART 2 — PHASES

### PHASE 1 — Data integrity
**Do:** resolve both names to canonical identities; count matches, opponents, date range, domestic vs European split.
**Audit:** both resolved? ≥10 matches each? data within 5 years? no split identity?
**Fail → STOP.**

### PHASE 2 — Direct evidence (head-to-head)
**Do:** all prior meetings — scoreline, date, competition, venue.
**Audit:** within 5 years? comparable context?
**Output:** H2H record, or "never met".

### PHASE 3 — Second phase (shared opponents)
**Do:** opponents both clubs have faced; each club's goal difference against them.
**Audit:** path count, date spread, any single path carrying the result.
**Output:** per-path table.

### PHASE 4 — Third phase (opponent-of-opponent)
**Do:** two-hop chains where no shared opponent exists.
**Audit:** count, spread, year span, context mix.
**Output:** per-path table.

### PHASE 5 — Aggregate and grade
**Do:** pool evidence, 2nd phase weighted ×2. Mean, sd, spread. Grade from the **measured** table (B+/B/C/C−/D/D4).
**Audit:** grade matches measured direction accuracy? Mean driven by one outlier?

### PHASE 6 — Goal difference → tier
**Do:** map estimate to calibrated tier CH-A…CH-F.
**Audit:** tier's *historical* rate quoted, not the Poisson output? Ceiling respected?

### PHASE 7 — Goal TOTAL — **CURRENTLY UNBUILT**
**Do:** derive expected total from both clubs' actual scoring/conceding rates.
**Audit:** validated against outcomes with a stated correlation, or the market is not offered.
**Status: NOT VALIDATED. No over/under published until this passes.**

### PHASE 8 — Market selection
**Do:** from tier + grade, pick the lowest-risk expression — 1X, DNB, home win, handicap.
**Audit:** every market traces to a validated quantity. Handicap needs Phase 6; over/under needs Phase 7.

### PHASE 9 — Verdict
**Do:** state call, confidence, reason, and what would falsify it.
**Audit:** confidence matches the measured grade, not the modelled percentage.

### PHASE 10 — Log for scoring
**Do:** record prediction, grade, tier, date. Brier-scored on result.

---

## PART 3 — SELF-AUDIT OF THIS PROTOCOL

| Check | Result |
|---|---|
| Prevents C1 (fabricated totals)? | Yes — Phase 7 blocks over/under until validated |
| Prevents unbacked handicaps? | Yes — Phase 8 requires Phase 6 |
| Prevents single-path calls? | Yes — Phase 5 flags, Phase 9 gates |
| Prevents quoting inflated percentages? | Yes — P6 + Phase 6 audit |
| Enforces one-at-a-time? | Yes — P9 |
| Any phase unvalidated? | **Yes — Phase 7.** Declared AND now blocked in code |
| Covers your weighted scale? | **No — gap declared below** |

### Audit of implementation vs document (2026-07-30)

The document said the right things; the **code did not enforce them**. Three gaps found:

| # | Gap | Evidence | Fix | Verified |
|---|---|---|---|---|
| G1 | P6 ceiling not enforced — engine emitted 95.6% with no guard | Ajax modelled 95.6% vs measured ceiling 65.7% | `analyse()` now returns `ceiling` and `extrapolated=True` | PASS |
| G2 | P4/Phase 7 not enforced — `o25` still returned despite being unvalidated | `o25=0.72` emitted for Ajax | `o25` now returns `None` + `o25_status="WITHHELD"` | PASS |
| G3 | Phase 10 had no persistence — no log existed | no `predictions_log.json` | built `plog.py` with record/settle/Brier | PASS |

**Verified working:** the single-path gate was already correct — Gent (1 path, grade D) and Zira (2 paths, C−) both return NO CALL.

**Live log seeded:** Lech Poznań 1–5 Aarhus — Brier **0.2638**, direction correct. `settled: 1 | direction: 1/1`.

**Known gap:** the protocol does not yet place your **+1 / +2 / +4 / +6 / −4 / −6** scale. It failed as a chain metric; it has not been tested as a team-rating or form measure. Phase 5 currently uses goal difference.

---

## PART 4 — DECISIONS NEEDED

1. Approve or amend the **10 principles**.
2. Approve or amend the **10 phases**.
3. **Phase 7:** build and validate the totals model, or leave over/under permanently off the card?
4. **Your weighted scale:** re-test as a team-strength rating rather than a chain metric?
5. **Confirm the first fixture** to run through the protocol.

Nothing starts until you sign off.
