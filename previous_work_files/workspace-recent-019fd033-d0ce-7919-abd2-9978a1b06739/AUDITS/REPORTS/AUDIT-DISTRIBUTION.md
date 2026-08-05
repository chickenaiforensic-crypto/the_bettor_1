# AUDIT-DISTRIBUTION — post-C2 audit of the calibration study (2026-08-01)
Full rerun of all 671 replays with richer per-game columns (audit log: `replay_audit.csv`).
Check that nothing was missed in CALIBRATION-2, map the mass distribution of the
share instrument, and inventory blind spots = "what to feed in" proposal.

## 1) C2 audit — gate verified on the shipped build (v2.6.9)
- Gated pool (n=29 demoted games): as win calls they go **44% win / 37% loss**;
  as WIN-DRAW pair calls they cover **62%**. Quarantine works exactly as designed.
- Gate behaves symmetrically: TA-gated 42% win, TB-gated 46% win — not side-biased, it catches weak games on both sides.
- NO CALL discipline re-verified: the 71 silenced games came out H 47 / D 19 / A 32 ≈ base rates (45/21/32). Silence hides no signal; it is honest abstention.
- Nothing missed structurally: effective-independence cut (≥15 vs <15) shows **no quality difference (64% both)** — the engine's reuse counter is not a predictor, so no gate needed there (missed-nothing finding, in writing).

## 2) Distribution pattern of the share instrument (600 games with evidence)
- **Mass concentration:** 60% of all games sit at leader share 45–65% (the dual/lean region). Only 13.7% reach WIN+, 12.3% reach STRONG. The instrument is conservative by construction — most matches are genuinely close.
- **Calibration shape is monotone at the top:** 65–70: 67%, 70–75: 65%, 85–95: 78–80% — but with the **75–80 dip (51%)** and the **95–100 pollution (65%, 7 losses)** = h2h-blowout inflation pockets, both now fenced by gate/warning.
- **TA/TB asymmetry (NEW finding):** at identical shares the home-led call outperforms:
  - STRONG: TA 77% vs TB 69%
  - WIN: TA 65% vs TB 55%
  - Tilt ≈ 8–10 points — the evidence engine scores GD without a home-advantage term in cross estimation (venueFactor handles relocation, not plain home edge). Base-rate home edge visible at 45% H vs 32% A.
- **Draw-share is NOT a draw predictor:** D<12.5% games still draw 15%; no D-bucket deciles materially beat the 21% base draw rate. The engine's neutral bucket is padding, not signal — the draw zone (D≥15% live rule) stays heuristic. Fix path: needs an explicit draw model (future work), not more evidence weight.
- **Source pockets:** cup/intl pool inside S≥65 (n=59) hits 77% — lopsided UEFA qualifiers are easy corridors, fine; relocated-venue rows n=2 — zero information, no venue-correction possible from data; rest-days (RPL, n=181): ≤3 days 64% vs ≥4 days 59% — no rest signal worth a rule (in writing).

## 3) Blind-spot inventory — "what to feed in" (measured need → proposed feed)
| Blind spot | Cost measured today | Proposed feed (results-only compliant) |
|---|---|---|
| **No home-advantage term in estimates** | TB zones overcalled ~10 pts (77v69, 65v55) | C3 candidate: side-adjusted anchors (TB needs ~+5pp share for same zone) — tune after slate; or venue-corrected h2h in Candidate A partially absorbs it |
| **Blowouts carried at full h2h weight** | 95–100 tail: 7/31 losses | Candidate A (venue-flip + shrinkage) — already queued |
| **No player context (reds, injuries, keepers rotation)** | unmeasurable here — zero fields exist | C4 context flag layer: pack-level flags that can ONLY demote/warn (never promote), same shape as your old app's availability/anomaly tripwires: confirmed keeper change, star-striker absence, post-manager-change debut, heavy-rotation cup tie |
| **Cup rotation / B-teams invisible** | cup/intl corridor over-promises (77% at small n) — attractive-looking but fragile | flag on cup fixtures; lower cap on cup-fed h2h ests (Candidate A territory) |
| **Lineups/referee/weather/travel** | none measurable in results-only data | NOT proposed — violates blueprint independence; would need user sign-off to change the contract |
| **Long-term form trend** | per-section shares static over season | feed exists (dates); engine could down-weight old meetings — part of Candidate A shrinkage by age |

Blueprint boundary respected: nothing above adds odds/lineups as *inputs to direction*.
The context layer only gates confidence — same philosophy as the confirmation gate you approved.

## 4) Immediate queue after this audit
1. C3: side-adjusted zone anchors — measure on forward slate first (n grows), then tune.
2. Candidate A: venue-corrected h2h + shrinkage — biggest single source-level fix; kills the 95–100 pocket and part of the TA/TB tilt.
3. C4: context-flag pack fields (optional, demote-only) — needs your sign-off on pack format before building.
4. Forward 20-game slate under frozen v2.6.9 instrument — generates prospective calibration n.
