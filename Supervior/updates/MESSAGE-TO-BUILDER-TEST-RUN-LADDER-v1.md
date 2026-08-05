# MESSAGE TO BUILDER — THE TEST-RUN LADDER (approval-by-measure, owner doctrine 2026-08-05)

**Relay verbatim. This supersedes "approved on documentation" for every system, weight and constant.**

## What "approved" means from now on
No system, weight, or constant is adopted because a document says so. It is adopted when **its measured test run on our own data** wins. The app already has the right shape (masked replay); this message fixes the exact protocol.

## The ladder (per league, on current store data — 2021-22 onward, newest end first)

1. **L-1 — the last game:** train the candidate on ALL rows from 2021 up to but excluding the newest completed game; predict that one game; score it. Calibrate the designated constants (bounded steps, existing caps — never free-run) until the prediction matches.
2. **L-2 — the last 2 games:** hold out the newest 2 games, retrain on everything before them, test on both. Check accuracy; readjust if needed.
3. **L-n — expand the holdout:** repeat with 3, 4, … games (or one matchday at a time) until the holdout covers the whole last season.
4. **Full-system accuracy check:** with the final constants, run the whole system across ALL leagues on the full ladder and report the complete metric set: Brier (1X2 + home/draw/away), log loss, direction accuracy, calibration max error, per-market gates. Paired, per-match comparisons only (no resampled absolutes); report n and the minimum detectable effect.
5. **Readjust if necessary:** any league or metric that degrades on the expanding ladder gets its designated constant(s) adjusted and the ladder re-run from L-1. When the constants stop needing adjustment as the holdout grows, the system is **calibrated** and that candidate is **approved by test run**.

## Honest ground rules (non-negotiable)
- One game is noise. L-1/L-2 are calibration warm-up, not proof — proof is the ladder converging as it expands (this is why steps are bounded and caps stay).
- Never fit on the held-out games. The holdout is touched only by scoring.
- A draw is a loss for a home-win call (I5). BTTS stays withheld (I3).
- Every run leaves a numbers artifact (train window, holdout, n, all metrics, date) — the artifact IS the approval record, not a chat message.
- The feasibility instrument already exists: `audit_work/backtest_harness.py` (first live run: RPL 0.5675 vs 0.6465 base; CZ1 0.6090 vs 0.6509; EPL 0.6140 vs 0.6534). Productionise it as the app's own masked-replay module (S0) — same math, artifact output, per-league ladders.

## Where things live
- Workorders: repo `Supervior/Workorder/` (UEFA connector = queue #17, parallel allowed).
- Returns: repo `handoffs/` (one .txt per workorder, BP-TEAM-PACK v2).
- Store/backups: per the owner's repo hierarchy; every import still goes through the app's one gate.
