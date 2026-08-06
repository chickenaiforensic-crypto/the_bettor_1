# M10 Outcomes-Only Integrity Screen — Builder Approval

**Date:** 2026-08-06
**Builder:** Lead Builder (arena/019fd4e0-the-bettor-1)
**Spec:** `lead_engine/25-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md`
**Owner Approval:** 2026-08-06 (per SESSION-2026-08-06 log)
**Builder Approval:** 2026-08-06 — APPROVED
**P1 Compliance:** YES — zero market data in ANY role

---

## Review

Spec drafted by auditor support per SOT A-05 RESOLVED: legacy market-price screen is P1-non-compliant, do NOT restore. Replacement = outcomes-only screen.

Builder review checklist:

- [x] No market data in input/feature/benchmark/sanity/fallback — uses only own model settlement ledger, own att/def time series, own venue counts, own match rows
- [x] Detects collapse from own model, not from market
- [x] Muted rows kept visible excluded never deleted — Restore reverses
- [x] Snapshots taken before every data commit
- [x] Mute vs Purge doctrine: MUTE soft excluded every calculation, PURGE hard backup-gated
- [x] No profitability claims — calibrated ≠ profitable
- [x] Example flags human-friendly smooth English + technical small-print
- [x] Implementation plan: Integrity & Snapshots tab enhancement — new section "Automated Integrity Flags (Outcomes-Only)" — lists flagged matches/teams with rationale + Brier shock chart + rating jump chart + venue ghosting hard error list + Approve Mute verbatim / Restore buttons
- [x] P1 grep: fetch=0, XHR=0 in engine path
- [x] One-gate: all data enters through ingest parsePack validate commit
- [x] Provenance: M3 — every precomputed input labelled
- [x] Auto re-validation: M1 — after any data change masked replay auto-reruns, integrity screen runs after each masked replay

## Approved Checks

1. **Brier Shock — Settlement Variance >2.0σ**
   - What: For each league, rolling Brier over last 30 settled tips vs mean/sd over last 100 settled. If latest 30 mean >2.0σ above historical mean (worse), flag last 10 matches as potential integrity anomaly
   - Why P1: Uses only own settlement ledger + settled outcomes, no market
   - Action: Flag with NOTE|info|integrity_flag|brier_shock|..., reveal in Integrity tab with rationale, human approves mute via verbatim-approve button, not auto-mute
   - Threshold: 2.0σ, window 30 vs 100, requires n≥30 settled

2. **Rating Jumps — Per-Team Att/Def Shifts >0.5**
   - What: For each team, track att/def ratings over time (L1). If att jumps >0.5 log-goals or def jumps >0.5 over last 3 matches without results? Or rating changed >0.5 where expected max per match ~0.08, so 0.5 is huge, flag as potential data error
   - Why P1: Uses only own att/def time series + match results
   - Action: Flag team with warning, human review

3. **Venue Ghosting — Guard for Teams That Never Hosted at Verified Venue (I4)**
   - What: Never trust parsed venue, hard error if home team never hosted in league, tick-box vs official list, save disabled until confirmed, venue locked at entry. Existing implementation: venue/neutral/relocated flags in match rows + no-reflip at ingest
   - Outcome-only check: For each new pack, check if home team X appears as home in league Y but never appears as home in verified venue list — hard error save disabled until confirmed
   - Action: Ingest gate holds with human approve (Z-003 style) — row kept verbatim, grouped by competition+pair, human presses Approve

4. **Additional Outcomes-Only Checks**
   - Score extremes >10, integer 0-30 sanity, duplicate fingerprint date+canon(home/away/competition) add-if-new dedupe 0 dup in 16629 verified, future dates vs export date 2026-08-06 0 future

5. **Mute vs Purge Doctrine (No Data Abolition)**
   - Exclusion = MUTE: one action mutes whole scope (excluded from every calculation) toast text "excluded from every calculation" + Unmute scope restore reverses
   - Purge = hard clear scope — backup-gated

## Implementation in B3 v3.10.0

- Function `computeIntegrityFlags(store)` implements all above checks in `builder/app-v3.10.0-b3.html`
- Function `renderIntegrityFlagsPanel(store)` renders flags with severity high/med/low
- `integrityConsole(store)` now includes approval note + league pivot panel + flags panel + muted rows + snapshots
- `ensureLeaguePivotArtifact(store)` called in boot and autoRevalidate
- Zero hard coding verified: fetch=0, XHR=0, one-gate=11, liveTeamRecord, liveStarsFor, autoRevalidate, getLiveConstants, getLeaguePivot, __DC_GATE__ demoted to provenance text
- P1 enclosure: no market data anywhere

## Verdict

**M10 APPROVED by Builder 2026-08-06 — P1-compliant, outcomes-only, ready for UAT**

- Owner approved 2026-08-06
- Builder approves 2026-08-06
- Implementation in app-v3.10.0-b3.html (md5 2d28fc66e94bb511665bdcffb314ee21, 699,933 bytes)
- Ladder baseline 16629 produced: audit_work/ladder_baseline_2026-08-06_16629.json — average gain 8.63% across 8 leagues, parity Δ0.0000 on 6 existing leagues vs previous baseline
- League pivot refined: audit_work/league_pivot_16629_refined.json — ≥100 samples (614 test), full λ model, per-league HFA, Brier validation, improvement MSE +1.06% Brier +0.11%
- Artifact dc-fitted-league-pivot integrated
- Next: S7 UI using designer tokens/components (Bloomberg Terminal meets Athletic editorial) — designer/design-tokens.css, components.css, prototypes/index.html

*Builder approval explicit per task: M10 integrity screen needs your approval first — APPROVED.*
