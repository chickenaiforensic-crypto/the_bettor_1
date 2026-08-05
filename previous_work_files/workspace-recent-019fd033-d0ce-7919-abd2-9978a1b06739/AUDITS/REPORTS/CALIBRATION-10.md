# CALIBRATION-10 — venueFactor (section #6 dissection) → **NO-SHIP (provably inert in pool)**

## What was dissected
`venueFactor(m.venue)` tiers: normal/home/club-home **1.0** · relocated/partial-home **0.75** ·
neutral **0.55** · unknown (default) **0.75**.
Audit finding: it is read in **exactly one place** — the H2H path weight
(`PHASE_WEIGHT.h2h * venueFactor(m.venue)`). Common-opponent and level-3 paths have **no venue
discount at all**, and it prices the *evidence-match* venue, never the fixture's own venue.

## Pool census (what it can even touch)
- RPL universe: 644 rows, all venue `home` → factor 1.0 everywhere.
- Imported packs: 53 normal, 1 unknown, **6 relocated** (Malisheva European home rows). Zero neutral rows.
- Discounted-H2H fixtures in the 633-game replay: **exactly 2** — and both are single-path fixtures
  (S=100). With one path, path weight cancels out of every normalized output (shares, weighted
  estimate, EV-G2 mean), so the factor is mathematically inert there.

## Sweep evidence (rpl/venue_sweep.js, full 633 replays per variant)
| variant (relocated / neutral / unknown) | games changed≠shipped | zone flips | actW / pair |
|---|---|---|---|
| shipped 0.75 / 0.55 / 0.75 | — | — | 66.2 / 85.4 (n=287) |
| 1.00 / 1.00 / 1.00 (no discount) | **0** | **0** | 66.2 / 85.4 |
| 0.50 / 0.30 / 0.50 (harder) | **0** | **0** | 66.2 / 85.4 |
| 0.85 / 0.75 / 0.85 (softer) | **0** | **0** | 66.2 / 85.4 |

Moving the tiers from 0.30 to 1.00 changes **zero** games, zones, and balances anywhere in the pool.

## Verdict
**NO-SHIP.** The current tiers produce no measurable accuracy effect on replay — the pool lacks
relocated/neutral H2H depth (2 single-path fixtures) to prove influence, which is the shipment bar.
The 1.0/0.75/0.55 values stay as unverified doctrine defaults, kept for the day neutral-site cup
games enter the data pool. No app change, no version bump, no harness change.

## Honest scope note
Two real structural limits were found and recorded (not fixed, unfounded either way on this pool):
1. venue discount never reaches common-opponent / level-3 evidence;
2. the fixture's own venue is not an input to anything.

## Queue
#7 effective-paths discount + NO PLAY thresholds (eff<2, agree<0.60, |weighted|<0.35) → #8 zone cut points.
