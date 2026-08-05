# CALIBRATION-3 — Candidate A verdict, off-points study, C5 shipped (2026-08-01)

Ship-run of the approved batch: Candidate A (venue-corrected h2h + shrinkage),
C4 (context flags), then the next-category study: WIN/STRONG off-points (draws + losses).
Every number below is masked-replay on the shipped engine: 600 games with evidence
(469 RPL + 131 UEFA/pack rows), 71 NO CALL discipline, strict causality.

## 1. Candidate A — MEASURED, FALSIFIED, REVERTED

Built fully, harnessed, then A/B-replayed against the v2.6.9 baseline on identical universes
(replay_variants.js + replay_ab_check.js). V0 reproduced the baseline exactly
(95–100 pocket 65%, 7 losses — instrument verified before judging variants).

| Metric (post-gate zones) | V0 = v2.6.9 | V2 = Candidate A |
|---|---|---|
| STRONG | 78% w (n=60) | 77% w (n=60) |
| WIN | 63% w / 80% pair (n=151) | 63% / 80% (n=153) |
| TA/TB gap (strong+win pooled) | TA 73% vs TB 62% (+11pp) | TA 72% vs TB 62% (+10pp) |
| h2h-only pocket (h2h≥75, common silent, S≥85) | 44% w (n=9) | **36% w (n=11) — worse** |
| 95–100 share bin | 65% w, L=7 | 59% w, L=9 |

Why it fails: venue-correcting *boosts* away h2h wins, pushing more one-sided h2h piles
over S≥85 — the rotten cohort. The pocket is an **evidence-depth** problem (h2h-only games,
share ~100% at any weight), not a venue-mix problem — and the C2 gate already quarantines it.
No gain on any stated motive, small harm on one → **rejected; engine math = v2.6.9 exactly.**

## 2. Off-points study (study_offpoints.js on the shipped engine)

Pools: post-gate STRONG n=60 (78/13/8), post-gate WIN n=151 (63/18/19). Probes H1–H6:

- **H1 thin aggregate margin (|weighted| < 0.8):** n=13 → L 31% vs pool 19%, but removing it
  changes WIN pool W 63→63%. No discrimination → rejected.
- **H2 no-H2H evidence (WIN pool):** n=26 → **D 31%** vs pool 18% (draw-risk!), W 54 / L 15.
  → became rule C5 below. STRONG no-H2H cohort: n=20 → W 80% — rule must NOT touch STRONG.
- **H3 third-section contra ≥45:** only 2 games leak past the C2 gate → already handled.
- **H4 cup corridor:** cup games in WIN zone: n=32 → **W 84%, D 0%, L 16%**. Cup demotion
  would *hurt* — direction rejected; corridor confirm stays as-is.
- **H5 engine draw-share as draw predictor:** dead both ways — inside WIN/STRONG pools the
  engine D-share never exceeds 28% (n=4 at 20–28, 2 of them draws) and across all 600 it's
  non-monotone. No draw model derivable from shares alone; draw zone stays heuristic.
- **H6 sub-bands:** STRONG 85–90 → **0% loss, 100% leader-or-draw (n=23)**; STRONG ≥90 →
  14% loss (n=37) — every post-gate STRONG loss lives at S≥90 (the pollution tail survives
  the gate at low frequency; variance, not a rule — n=5).

## 3. Loss residue (34 post-gate WIN+STRONG losses, listed in study output)

Dominant theme by inspection: **regime-shift upsets** — promoted/collapsing sides
(Sochi tail, Akron away wins, Khimki/Baltika/Dynamo-Mkh home wins) beating season-old
evidence. Follow-up sim (study_c5_age.js): losses' median evidence age 260d vs winners' 207d —
but as an actionable split it does NOT discriminate (≤180d cohort: W 72 pair 84 / >180d: W 65
pair 84, L=16% both). **C6 recency-weighting: measured-weak, not proposed.**
These are exactly the facts C4 context flags exist for (keeper change, star absence,
new-manager debut, rotation risk) — C4 is the designed catch; date-sourced CTX packs to feed.

## 4. C5 draw-risk drop — SHIPPED (v2.7.1-cross)

Rule: post-gate **WIN** with **zero H2H evidence** → demote to WIN-DRAW.
Measured (600 replays, study_c5_age.js):

| Zone | Before C5 | After C5 |
|---|---|---|
| WIN | n=151, W 63%, D 18%, pair 81% | **n=125, W 65%, D 15%, pair 80%** |
| WIN-DRAW | n=175, pair 70% | **n=201, pair 72%** |
| Demoted cohort (win & no-h2h) | — | n=26, D 31% (signal), pair 85% |
| STRONG | n=60, W 78% | untouched (cohort wins 80%) |

Shipped zone table (zone_tally.js on the frozen build):
STRONG n=60 → 78/13/8 · WIN n=125 → 65/15/20 · WIN-DRAW n=201 → 48/24/28 ·
lean n=97 → 53% · TOSS n=117 → 43%.

## 5. What shipped / what didn't (ledger)

| Item | Verdict | Where |
|---|---|---|
| Candidate A venue-corrected h2h + shrinkage | **REJECTED on replay** (all motives flat, pocket worse) | reverted; record above |
| C4 context flags (pack rows, demote-only tripwires) | SHIPPED dormant | v2.7.0-cross; arms when CTX packs are fed |
| C5 draw-risk drop | **SHIPPED** | v2.7.1-cross, computeZone + tags + zone notes |
| C6 recency weighting | rejected (no discrimination) | record above |
| STRONG ≥90 loss tail | annotated, no rule (n=5) | ZONES.md warning |

Pack syntax for C4 (armed by feeding, demote-only per blueprint):
`CTX|team|YYYY-MM-DD|keeper-change|detail|source` (also `star-absence`,
`new-manager-debut`, `rotation-risk`; strict v2 takes a SOURCE label as 6th field).

Forward queue unchanged: 20-game slate under frozen v2.7.1; settle Akron v Rubin
(TB WIN 69.4%, saved under v2.6.9) by 90-min score; C3 side-adjusted anchors still
held for prospective n; tennis after gate passes.
