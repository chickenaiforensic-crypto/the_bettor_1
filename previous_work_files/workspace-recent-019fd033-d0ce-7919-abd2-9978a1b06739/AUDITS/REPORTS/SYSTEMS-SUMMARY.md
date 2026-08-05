# Systems summary — every measurement system in play, scored on the identical masked sample

Date: 2026-07-31 · Method state: masked replay, cutoff = match date, 61 games, store of 61+ rows.
Harnesses (permanent): `replay_test.js` (current engine), `old_replay.js` (old tool, real computeVerdict extracted unmodified).

| # | System | What it is | Measured replay performance | Calibration status | Verdict |
|---|---|---|---|---|---|
| 1 | Domestic model (Dixon–Coles, 18 leagues) | Percentage engine; claims max err 1.7 pts over 150,360 | Cannot replay locally (training data not shipped; ratings frozen at build) | **Claim inherited, unverified locally** — Lane-1 forward slate is the audit | Hold judgment until Lane 1 |
| 2 | Cross-league bridge (lambdasCross, scale 1.00) | Inter-league strength conversion | Not in replay path | Explicitly documented as *"approved working baseline"* = placeholder, never validated | Treat as provisional until the big calibration project |
| 3 | Evidence engine — h2h phase (w=3 ×venue 2.25) | Previous-meeting avgGD as estimate | **36% (5/14) — anti-signal** | Unvalidated weights; cause isolated: no venue-flip algebra, no shrinkage | **Fix or demote** — candidate A pending go |
| 4 | Evidence engine — common-opponent phase (w=2) | Shared-opponent GD comparison | 57% (4/7) — noise | Unvalidated | Watch on slate; no strength proven |
| 5 | Evidence engine — level-3 chains (w=1.5) | Opponent↔bridge↔opponent GD chains | 50% (4/8) — noise | Unvalidated | Same |
| 6 | Evidence engine — aggregate + classify() guardrails | Weighted combine; NO CALL / Lean only / Close call caps; % withheld uncalibrated | Leans 50% (9/18); **abstention 66%**; reasons enforced; lean never upgraded to call | **Guardrails verified as protection layer**; predictive surface unproven | Keep guardrails; surface under work |
| 7 | Old match-audit tool (subscale verdict + de-vig edge) | 5 weighted sections (.30/.25/.20/.10/.10) → sigmoid; PASS/INSUFF/TIDE/CLEAR tiers; needs odds + rich researcher inputs | Abstain 97%; directional **0/2** (both confident: p 0.91, p 0.74 — both lost) | Unknown; starved inputs here (blueprint is results-only — no odds, rankings, injuries, effort stats). Its own file documents past measurement bugs *fixed by its author* | Not calibration-grade either; different failure shape (silence + rare confident error) |
| 8 | Market/odds layer | Odds de-vig edge comparison (old app only) | Not present — blueprint bans odds | — | Out of our scope by design |

## On "my measures have been corrupted by engineers" — answered with mechanics

1. **Our pipeline is byte-clean.** After every build: MODEL payload compared byte-identical to the pristine v2.5 file. Nothing in this session's engineering altered the model's numbers, ratings, tables or texts. Mechanical proof, re-runnable any time.
2. **The v2.5 model's calibration claims are inherited, not verified.** The "1.7 points over 150,360" arrived inside the shipped file; no local artifact can re-derive it. That is the *only* place pre-existing corruption could hide, and I cannot acquit it from here — the Lane-1 forward slate exists precisely to audit it on live games.
3. **The managed evidence engine was never corrupted — it was never calibrated.** Weights 3/2/1.5 and bridge 1.00 were entered as working placeholders and labeled as such ("approved working baseline"). Placeholder is not corruption — but the replay shows trusting it as if measured produced real harm (h2h 36%). Same lesson as the Hibernian 4-1 case.
4. **The old tool's file honestly documents its own past measurement bugs** — draw-odds omission inflating edge, confidence renormalization inflation, league shared-count inflation, silent YES/NO defaults — each self-flagged as fixed by its author. That is the fingerprint of a system being audited, not doctored.

**Conclusion:** no engineered corruption found anywhere we can inspect; the real failure mode everywhere is *unvalidated defaults presented with more confidence than they earned*. The corrective is procedural, and it's already installed: replay gates are permanent, sleight-of-hand edits are blocked by exact-match builders, all systems score on identical masked samples before adoption, and no percentage unlocks without measured calibration.

## Forward from here

- Candidate A (venue-corrected h2h + shrinkage) — awaiting user go; must clear replay ≥60% before it ships, then must confirm on the live slate.
- 20-game slate unchanged; Lane 1 now also audits the inherited model claims everyone has been quoting.
|