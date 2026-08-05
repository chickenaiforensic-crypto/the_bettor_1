# CALIBRATION-9 — draw-mass mapping (section #5 dissection) → **SHIPPED v2.8.8-cross**

## What was dissected
The displayed **3-way balance** (home / draw / away shares out of 100) is a pure weight ratio:
`share = bucketWeight / totalWeight` from `aggregate()` (bucket rule |est| > 0.50). It had never been
checked against realized results as a *probability-like* read. The draw bucket in particular
("draw mass") was mapped 1:1 to the screen with no calibration.

## Evidence (633-game masked replay, v2.8.7 engine, date-sorted split-halves)

**Dissection finding — the raw row is badly distorted:**

| displayed Draw% | n | realized draw |
|---|---|---|
| 0–10 (mean 4.5) | 88 | **19.3%** — under-stated 4× |
| 15–20 (mean 17.5) | 88 | 17.0% ✓ |
| 25–30 (mean 26.9) | 87 | 28.7% ✓ |
| 40–100 (mean 45.5) | 56 | **33.9%** — over-stated |
| top leader-share bucket (mean 93.6) | 34 | leader won only **76.5%** |

Raw row log-loss **1.4802** vs a flat base-rate row at **1.0695** — the raw display was *worse than
saying 44/24/32 every time*. Miscalibration lives in the squeezed tails (draw + trailer), not the mid-band.

**Rejected candidates (no-ship):**
- Draw-only affine map: slope ≈ 0 on both halves (draw-mass alone carries ~no monotone signal), test-half log-loss 1.39–1.59 — **worse than raw**. No-ship.
- Temperature map p^t: 1.10 best, loses to shrink. No-ship.
- Hold-leader-raw / fix remainder (C9b family): llB ≈ 1.36, more honest per rung but fails the split-half gate. No-ship.

**Winner — symmetric shrink of the whole row:**
`shown = 0.60·raw + 0.40·base` with base = draw 24.33, sides 37.835/37.835 (symmetric ⇒ leader can never flip; 0 flips, rows sum to 100 ± 6e-3 on all 633).

| metric | raw | shipped 0.60 | gate |
|---|---|---|---|
| log-loss half A | 1.4806 | **1.0010** | beat raw both halves ✓ |
| log-loss half B | 1.4797 | **1.0052** | ✓ |
| Brier A / B | .5982 / .6188 | **.5910 / .6007** | ✓ |

Optimum w interior on a 0.48–0.84 frontier grid (ll min at 0.58–0.64, Brier flat 0.66–0.72) → w=0.60 is not a grid edge. ~47 pp of the −48 pp gap to flat-base is captured; mean displayed draw 23.6% → sits on actual 24.3%.

## What shipped (display-layer only)
- `CAL9_W=0.60, CAL9_SIDE=37.835, CAL9_DRAW=24.33`, helpers `cal9()`, `cal9L()`.
- Total-summation bar + bold TA/Draw/TB line and zone-tag/zone-line leader share now render calibrated numbers.
- **Engine bit-identical**: `aggregate()`, `computeZone` ladder (raw S_ ≥85/65/55/50), gates C2/C5/C8/C11/CTX, effective paths, EV-G2 goals, log saves all read raw shares.
- Zone-table re-run: **strong 9 (W89/pair89) · win 64 (W75/pair94) · windraw 214 (W63/pair83) · lean 107 (W46/pair72) · toss 239 (W43/pair72)** — identical to v2.8.7.
- Smoke 96/96 · closure 19/19 · packs 27/27 · concat/replay/migration all pass.

## User-facing mapping
Displayed leader share is now compressed: raw cut points 85/65/55/50 read as **66.1/54.1/48.1/45.1**
on screen (e.g. a displayed 66+ = STRONG). Zone words are unchanged and still decided on the raw ladder.
Frozen slate sheets (e.g. "TB WIN 70.6%") stay frozen; forward numbers use the v2.8.8 scale.

## Queue
#6 venueFactor (1 / 0.75 / 0.55) → #7 effective-paths discount + NO PLAY thresholds → #8 zone cut points (last).
