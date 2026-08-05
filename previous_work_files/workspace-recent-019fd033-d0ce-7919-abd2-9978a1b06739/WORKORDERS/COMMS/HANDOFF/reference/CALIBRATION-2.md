# CALIBRATION-2 — secondary calibration study (2026-08-01)
Question: in the WIN zones (leader share ≥65%, n=240 of 600 replays), which section
acts as the weak link in games that ended draw or loss? Then propose the fix.

## 1) Failure forensics — the weak link is non-confirmation by COMMON

WIN+STRONG pool (S≥65, n=240): base 64% win / 16% draw / 18% loss.

| Condition | n | leader win | draw | loss | w-or-d |
|---|---|---|---|---|---|
| H2H agrees with leader (solo signal) | 140 | 67% | 12% | 19% | 79% |
| **COMMON agrees with leader** | **208** | **68%** | 16% | **15%** | **84%** |
| COMMON flat (<55) | 14 | 42% | 35% | 21% | 77% |
| COMMON contra (≥55) | 4 | 25% | 0% | **75%** | 25% |
| **COMMON does NOT confirm (flat/contra/absent)** | **32** | **40%** | 18% | **40%** | 58% |
| h2h-driven profile (h2h ≥75, common silent) | 14 | 42% | 14% | **42%** | 57% |
| 3/3 sections agree | 115 | 72% | 11% | 16% | 83% |
| 2/3 sections agree | 97 | 61% | 22% | 15% | 83% |
| **1/3 sections agree** | **28** | **42%** | 17% | **39%** | 58% |

Reading: the failures are not random — they cluster exactly where the aggregate
share was carried by raw H2H (and/or reused chains) **without common-opponent
confirmation**. H2H agreeing is nearly ubiquitous (its known inflation), so its
agreement adds little truth; COMMON agreeing is the strongest single quality
marker; COMMON absent/flat/contra is the failure signature. Level-3 leads at 75%+
win only 48% — corroboration, never standalone proof.

## 2) Tested fix candidates (measured, harness-only)

**Candidate C2a — engine phase re-weighting (h2h 3→2, common 2→3):** REJECTED.
Full 600-replay rerun: same gated outcomes (±1pt everywhere). Structural cause:
per-section shares are invariant to phase weights (each section's paths share one
weight), so weight shuffles only rescale totals — they cannot remediate
inside-section h2h inflation. Not the lever for this problem.

**Candidate C2b — zone confirmation gate (≥2 of 3 sections agree at ≥55):** WORKS.

| Pool | n | leader win | draw | loss | w-or-d |
|---|---|---|---|---|---|
| STRONG base (S≥85) | 74 | 72% | 12% | 14% | 85% |
| **STRONG + gate** | **60** | **78%** | 13% | **8%** | **91%** |
| WIN base (65–85) | 166 | 60% | 18% | 20% | 79% |
| **WIN + gate** | **152** | **63%** | 17% | 19% | 80% |
| gated-out (demoted) | 28 | 42% | 17% | 39% | 58% |

The gate quarantines precisely the weak-link bucket (42% win / 39% loss).
Variant "common confirms" measures within noise of "≥2 of 3" (208 vs 212 kept,
68%/84% pool-wide) — recommend ≥2-of-3 because it does not hinge on COMMON
being present.

Demotion destination is honest: gated-out games land in WIN-DRAW where the pair
covers ~58–63%, replacing a 42%-reliable win call. That is the calibration
doing its job, not hiding a bad zone.

## 3) Proposed secondary calibration C2 (zones v0.3)

1. **Confirmation gate:** WIN and STRONG zones require ≥2 of the 3 sections
   (H2H / Common / Level-3) to agree with the leader at ≥55% section share.
   Otherwise demote one step (STRONG→WIN, WIN→WIN-DRAW).
2. **Fragmentation rule:** games with only 1 of 3 sections agreeing demote
   regardless of share (their measured pool: 42% win / 39% loss).
3. **Contra flag:** any section contra-leading ≥55 prints under the zone line
   ("Common section contra at 61%") — rare (1 WIN-zone case) but decisive (0/4-4 pool went 25%/75%).
4. Unchanged: zone anchors (85/65/55/50), NO-CALL discipline, evidence-share notation.
5. Relationship to Candidate A: C2 is presentation-layer calibration on zones —
   it prices the current engine honestly. Candidate A (venue-flip + shrinkage)
   remains the source-level fix; when A ships, replay_zones.js reruns, gates and
   anchors re-tighten, and C2 may relax if the weak-link bucket shrinks.

Measured end state if shipped on the 600-game sample:
STRONG zone: 78% win / 91% w-or-d (n=60) — the best measured subgroup in the system.
WIN zone: 63% win / 80% w-or-d (n=152). WIN-DRAW zone: absorbs gated games at
~58–63% pair coverage. Demoted pool visibly flagged, never silently promoted.
