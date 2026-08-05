# CALIBRATION-11 — effective-paths discount + NO PLAY thresholds (section #7) → **NO-SHIP (gates validated as placed)**

## What was dissected
`aggregate()` independent-path discount (exact-duplicate chains deduped, then greedy match-id
reuse: each additional path sharing a match id is `reused`, not `effective`) and the three
classify/banner gates: `effective < 2`, `agree < 0.60`, `|weighted| < 0.35`.
All three are **display-layer demotions** (Lean only / Close call / NO PLAY strip) — they never
touch zones, gates C2–C11, shares or EV-G2.

## Dissection evidence (633-game replay, engine fixed, date-sorted split-halves)

**Do the gates mark the right games? YES — both halves:**
| cohort | n | actW | pair |
|---|---|---|---|
| banner passes all gates | 215 actionable | 67.9 / 70.6 (A/B) | 87.7 / 88.1 |
| any gate fires | 72 actionable | 62.5 / 50.0 | 77.5 / 78.1 |

- **agree:** clean monotone ladder both halves (W 45-46 → 61-65 → 67-73 across
  <0.6 / 0.6-0.75 / ≥0.75). 0.60 sits exactly at the elbow — below it is the bad cohort.
- **|weighted|:** monotone (W 41/36/38/57/65/68 across 0→1.5+ bins); 0.35-0.7 band noisy across
  halves (actW A 54.5 / B 62.5) — no consistent alternative cut.
- **eff:** fires only true single-path games (n=25, W56). eff=2 bucket tiny (n=12), halves
  disagree → noise. Discount-vs-raw-count: identical cohorts ±11 games, no gain either direction.
- Interplay: gates never fire on WIN zones (n=0) and only one STRONG game (which won); inside
  WIN-DRAW the fired games win 56.3 vs kept 65.7 — the banner demotion is directionally right.

## Threshold sweep (demote-only raises; objective: kept actW+pair beat baseline in BOTH halves)
| candidate | kept A actW/pair | kept B actW/pair | verdict |
|---|---|---|---|
| agree≥0.65 (vs 0.60) | 70.2 / 88.1 | 70.1 / **86.2** ↓ | mixed — no-ship |
| agree≥0.70 | 76.7 / 91.7 | 71.4 / **85.7** ↓ | halves disagree — no-ship |
| \|w\|≥0.45–0.75 | ≤ +0.7, pair −0.2 | +0.0, pair −0.1 | noise — no-ship |
| eff≥3 | +1.4 A pair | 0.0 change B | noise — no-ship |

No candidate wins both halves; the shipped values are the validated placement.

## Verdict
**NO-SHIP.** All three thresholds are measurably doing their job (fired cohorts are the bad games,
in both halves) and no recalibration beats them consistently. No app change, no version bump.

## Queue
#8 zone cut points (85/65/55/50) — last section, highest overfit risk.
