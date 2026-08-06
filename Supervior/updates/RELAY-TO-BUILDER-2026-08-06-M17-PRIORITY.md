# RELAY TO BUILDER — 2026-08-06 (planner decision: M17 is top priority)

**M17 audit result: FAIL on both I5 and I4.** Auditor confirmed. Your next build fixes this before anything else.

---

## What's broken

### I5: draw = loss — the app can't do settlement

The app saves prediction snapshots but cannot record actual match results. There's no way to enter home/away goals after a match is played, no win/loss/draw classification, no draw-as-loss enforcement. The Log & Settlement tab shows labels, not settlement logic.

**Build this:**
1. After a match is played, the user enters the actual 90-minute score (home goals, away goals)
2. The app classifies the outcome: home win / draw / away win
3. For settlement: if the prediction was "home win" and the result is a draw → that's a **loss**, never a push
4. Surface the outcome + immutable prediction/result evidence in the Log & Settlement view
5. Settlement data feeds into calibration (M5) and integrity screening (M10)

**Acceptance test:** save three frozen rows; enter home win, away win, and draw results; assert exactly the draw is recorded as `loss` (never `push`).

### I4: entry-side venue guard — the app doesn't verify venues

The import parser requires a `venue` field but never checks if the home team has ever hosted there. No verified-venue list, no confirmation tick-box, no hard save block for unknown venues.

**Build this:**
1. Maintain a per-league verified-venue list (populated from existing store data — every venue where a team has hosted)
2. On import/save: if the home team has never hosted at the stated venue in that league → **hard block**, save disabled
3. User must confirm via explicit approval (official-list tick-box) or mark as `neutral_venue` with NOTE
4. Venue locked at entry — no silent flip

**Acceptance test:** attempt to save a row whose home team is absent from that competition's verified-venue list → assert hard block. Then confirm through explicit approval → assert durable rationale + venue lock.

---

## Priority order

1. **M17 I5 settlement** — build first (this is foundational — M10 integrity screen and M5 calibration both depend on settlement data)
2. **M17 I4 venue guard** — build second
3. Then proceed to B3 (balance panel), B4 (goal-range bins), etc.

## M10 — auditor signed off, you can implement after M17

M10 spec is P1-approved. Build it after M17 settlement exists (Brier shock needs settlement data). See `Supervior/updates/RELAY-TO-BUILDER-2026-08-06-M10-AUDITOR-SIGNOFF.md`.

## Pivot — not adopting

+0.17% Brier gain is too small. UEFA dates need fixing first (343 malformed). Researcher is assigned to fix them. After that, re-run the pivot with clean data before considering promotion.

---

*Auditor report: `Supervior/updates/AUDITOR-REPORT-2026-08-06-FULL-LADDER-M17-M10.md`. Pivot report: `Supervior/updates/AUDITOR-PIVOT-REFIT-2026-08-06.md`.*
