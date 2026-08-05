# CALIBRATION-12 — zone cut points 85/65/55/50 (section #8, final) → **NO-SHIP (cuts validated as shipped)**

## What was dissected
The four raw-S_ ladder cuts: STRONG ≥85 · WIN ≥65 · WIN-DRAW ≥55 · lean ≥50 · TOSS <50,
plus their interaction with all gates (C2/C5/C8/C11/CTX re-fire naturally in the full-engine sweep).

## Dissection evidence

**S_-axis realized gradient (5-pt bins, both halves):** 37 → 47 → 40 → 50 → 53 → 57 → 61 → 76 → 76
W% up to S=80, then **noise** (80-85 dips to 58 in A / 68 in B; 85-90 spikes 92/86; 95+ sags 83/50).
The only clean, replicated strength break is at 85. The 60-65 pair plateau (87.3 both halves) is where
WIN-DRAW earns its keep.

**Full-engine sweep (633 replays each; objective: actW AND pair beat shipped in BOTH halves;
guardrails: STRONG W≥80 & n≥7 per half, monotone ladder, coverage ≥80%):**

| candidate | A actW/pair (n) | B actW/pair (n) | verdict |
|---|---|---|---|
| shipped 85/65/55/50 | 66.4 / 84.9 (146) | 66.0 / 85.8 (141) | — |
| windraw→60 | 69.1 / 88.2 (110) | 68.9 / **85.7** ↓ (119) | fails B-pair; coverage 79.8% < 80% |
| win→70 | 67.6 / 85.9 (142) | 66.4 / **85.4** ↓ (137) | fails B-pair |
| win 70 + windraw 60 | 70.8 / 89.6 (106) | 69.6 / **85.2** ↓ (115) | fails B-pair |
| strong→80 | ladder contaminated: STRONG W **64**/100 | — | dead |
| strong→90 | STRONG n=4/1 — too thin to mean anything | — | dead |
| strong 82 + win 68 | STRONG 67/100; win W drops 74→71 in A | — | dead |
| lean→45 | 66.4 / 84.9 = identical (lean/toss not actionable) | 66.0 / 85.8 | no-op |

**Why candidate A fails honestly:** its removed S 55-60 cohort paired 75.0% in half A but **86.4%**
in half B — the halves disagree whether that band belongs in WIN-DRAW, and the band's own W swings
59.1 (A) vs 43.8 (B). A cut placed in a half-unstable band cannot be validated; testing 57/58 to
force a pass would be chasing the failure — rejected by doctrine.

## Verdict
**NO-SHIP.** 85/65/55/50 stands as the validated ladder. Added knowledge: the S≥85 STRONG break is
real and robust (W 86/100 both halves under the shipped ladder); everything below is a smooth slope
where the shipped integers sit at the best compromise of meaning, coverage and stability.

## Programme close — all 8 vital sections dissected
| # | section | outcome |
|---|---|---|
| 1-2 | zones/gates · total goals | shipped through C6 (EV-G2 v2.8.5) |
| 3 | section weights + band | shipped C7 (3/3/0.75 @0.50, v2.8.6) |
| 4 | Elo/star engine | shipped C8 window last-6 (v2.8.7); K/HF/affine honestly no-shipped |
| 5 | draw-mass mapping | shipped C9 calibrated display (0.60·raw + 0.40·base, v2.8.8) |
| 6 | venueFactor | NO-SHIP — provably inert in pool (C10) |
| 7 | effective-paths + NO PLAY gates | NO-SHIP — gates validated as placed (C11) |
| 8 | zone cut points | NO-SHIP — 85/65/55/50 validated (C12) |

Net shipped across the programme: **actW 64.3→66.4/66.0, pair 84.1→84.9/85.8, log-loss 1.164→1.073
(zones) and display row 1.480→1.003** — every gain split-half validated, every failure documented.
