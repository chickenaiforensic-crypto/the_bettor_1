# 01 — STRUCTURAL AUDIT (Trust Nothing)

**Date:** 2026-08-05  
**Auditor:** Lead Planner (Arena AI) — fresh code, zero inherited trust  
**Inputs:** BLUEPRINT-SOT-2026-08-04.md v1.3, ENGINE-MASTERPLAN-2026-08-05.md v1.1, FUNCTIONALITY-2026-08-05.md, VERIFICATION-DATA-2026-08-05.md, `previous_work_files/workspace-019fb2c3/.../audit-01..24.md`, `app/engine.js`, `chain/`, `data/`

## 0. Approach — How We Audit When Trust Is Zero

- Read every file fully (COMMUNICATION-RULES binding #4: never skim).
- Re-parse with fresh code — never reuse old auditor script as evidence.
- Every system must show: where it lives (file+line), what it computes, measured effect (Brier/logloss), and gate status.
- If effect not measured → NOT allowed in singular engine until it passes harness.

## 1. Systems Inventory (From SOT §3 + Old Audits)

### Family R1 — Rating Engine (Dixon-Coles, 5 layers) — VERIFIED in app-v3.6.3

| Layer | File / Line | Computes | Measured Gain | Status |
|---|---|---|---|---|
| L0 DATA | store only | identities, matches, 90-min scores | substrate | LIVE — 5082 verified rows |
| L1 FIT | `engine.js` fit() L2056+, CONF L~1796 | λ_home = exp(μ[league]+att[home]-def[away]+hfa[league]+home_extra[home]), λ_away = exp(μ+att[away]-def[home]), clamp [0.05,6.0], def HIGHER=BETTER | Brier 0.6112 vs 0.6476 base = **+5.6%**, calibration ≤1.7% — **Dominant** | LIVE, but gate verdicts stale (G14) — needs S1 LIVE-DERIVE-01 |
| L1 constants | verified L1868 etc | LR 0.055, new-team 1.6× first 8, HFA_LR 0.010 (hfa×0.02 / home_extra×0.010), home_extra decay 0.999, att/def decay 0.0022/match, hfa clamp [0.05,0.55], home_extra ±0.25, min 6 matches, ρ -0.06, MU 2.6186, G_K 0.5 | fitted per league 1.20×–1.36× home mult | VERIFIED exact |
| L2 scoreGrid | `scoreGrid` | Poisson×Poisson × DC τ low scores ρ=-0.06, normalised → H/D/A raw (best who-wins) | shapes everything | LIVE |
| L2 goalsGrid | `goalsGrid` L1893 | total shrunk toward league mean G_K=0.5, GMU=2.6186 then λ rescaled → O/U + handicap | O2.5 error 10.3%→2.7% | LIVE, BTTS withheld 6.0% correctly absent |
| L3 star draw correction | ESPEC D | metric=(3W+D)/P, qualify P≥5, shrink weight 6 toward league mean, stars 1..5 quintile within league, hysteresis 0.05 (churn 21%→8.7%), target draw_table[tier|starGap] 27 cells else draw_base[tier], weights 0.2/0.5/0.5, cap ±0.02, proportional split | +0.047% full-1X2 Brier p<0.0000 n=59615, tier-2/3≈+0.09% — **real, small** | LIVE but sourcing break: live path starsHome null → M2/G17 omitted — needs S1 |
| L4 tiers/points | ESPEC E | points=round(100×H_cal), bands A+≥70 (78.5% win n7718), A≥60, B≥52, C≥45, D≥35, E<35, expected scoreline = max cell uncorrected grid ~13% freq | 0 prob impact, display only | LIVE, verified byte-identical |
| L5 consensus | ESPEC F | mean(HvH,AvA) goal-diff lenses, both sides ≥4 home & ≥4 away, Tier A/A+ only: >1.5 STRONG 78.6%, >1.0 CONFIRMED 74.8% vs 73.0% model top-10% +5.6pt, <0 CONFLICTED, |<0.2|&disagreement<0.5 DRAW-LEAN 31.8% | edits nothing (test-enforced) | LIVE, display filter |
| L1 dual sourcing | SOT §3.7 | migrated bootstrap (18 leagues, 414 teams, 342 records) vs live online fit (RPL/CZ1/EPL candidate) | bootstrap orphaned for replaced countries | A-01 demotes bootstrap to labelled bootstrap M3 provenance panel only |

Legacy audits 01-24 mapping:
- 01 baseline: base Brier 0.6476 established.
- 02 football system: L1 gate defined.
- 03 gate1 result: paired test lesson.
- 04 away venue study: home adv per-league.
- 05 pitch rating system: DC fit constants.
- 06 stars+familiarity: star metric defined, shipped unapproved historically → E7.
- 07 merger test: component isolation error E3.
- 08 star categorisation: quintile rank.
- 09 user star spec: user stars → system stars.
- 10 star v2 retest: shrink + hysteresis.
- 11 tier calibration: A+ 78.5% etc.
- 12 full merge: L1+L3 integration.
- 13 method audit: T1-T8 lessons.
- 14 corrected revalidation: E8 look-ahead fix.
- 15 home vs home, 16 hvh+ava joint, 17 transitive opponents, 18 chain on your fixture, 19 chain system, 20 fixture coverage, 21 app vs chain, 22 weighted scale, 23 league weighting, 24 segmentation — all chain/R2.
→ Key finding: many systems measured but few shipped with harness win. This audit will weight each by its measured win, not by audit number.

### Family R2 — Evidence Engine (match-history graph) — LIVE-BLUEPRINT

| Module | SOT §4 Status | Measured | Gate |
|---|---|---|---|
| 1 identity_store | LIVE L264-330 | substrate | — |
| 2 match_store | LIVE | tieIds, neutral, 90-min doctrine | — |
| 3 evidence_graph | LIVE L1506-1609 | h2h/common/third + opponent-of-opponent, effective/agree/nocall | LIVE |
| 4 cross_border_bridge | PARTIAL/STANDBY — evidence-cross display only, rated bridge not built — M9 | chain validation: r=+0.274 n=693 62.6% direction on 3rd phase, 2778 Euro matches, 2 defects: usability gate disproven, path discovery too narrow | held-out win over frozen 1.00 baseline needed |
| 5 goal_range_model | NOT BUILT M8 | promise but no win | held-out win required after M7 |
| 6 confidence_calibrator | PARTIAL — gate+labels live, artifacts stale M5 | zone ladder: STRONG 78%/92% pair n59, WIN 67/82, WIN-DRAW 49/75, lean 47, toss 45 monotone | held-out calibration, S0 |
| 7 balance_panel | PARTIAL M7 | NO CALL must show balance | S3 |
| 8 audit_log | LIVE | versions, settlement Brier/log-loss | — |

Gentle calibration, weighting candidates W1-W4 (H2H/common/3rd phase weights) — none operational until held-out win. Never-regress list kept.

### Family R3 — ELO / Performance Layer — A-03 pending

- INIT 1500, K20, home +65, star=clamp((ELO-1420)/2,0..100)→1-5★, perf window 6 min3 causal before cutoff.
- Live-derived every derive, display-only (never edits R1/R2).
- Unvalidated vs outcomes. Governance: adopt display-only with "not a prediction" label per A-03.

### Rejected / Dead Candidates (Do Not Rebuild)

- Recency weighting C6: measured 84/84 no discrimination → rejected.
- Venue correction + saturation Candidate A: A/B replay no gain, pocket worse → rejected, engine reverted.
- Spread-based chain gate: tight spread worse r0.195 vs 0.384 → rejected (T8,E6).

## 2. Data Layer Audit — Trust Nothing

- Store `pitch-rating-full.json` 5000 rows = six adopted packs byte-for-byte, 0 drift.
- Fresh re-parse: EPL 1900/1900 exact vs football-data lineage, RPL 1220/1220 exact vs RSSSF re-parse + 1 award adjudicated correct, RUSCUP 341/341 correct (3 RSSSF date misprints adjudicated pack correct), CZ1 1390/1401 exact + 11 date errors found (new D-1), MOL 120→202 (+82 verified), ADDENDUM 18/18.
- Adjudication register in VERIFICATION-DATA §4: all packs RIGHT vs archive misprints.
- Defect fixes: D-1 corrected file + D-2 fullspan → 5082 final store — 0 dup fingerprints, 609 identities, all ids resolve.
- No fabricated rows, no invented results, no wrong scores/teams/competitions.

- **Other branch mentioned by owner:** referenced as "another branch that contains fetched data which has been audited and complied by old person in charge" — verified as `main` branch at tip `12192a9b...` with `previous_work_files/workspace-recent-.../` 293 MB + `Supervior/other/` JSONs. Those files are the audited packs. Re-verified above independently; no trust assumed. No extra branches found on remote (only main + this arena branch) — old data lives in `previous_work_files/` and `Supervior/other/`, not a separate git branch.

## 3. App Layer Audit — Human-Friendliness (Pre-Architecture)

Current app v3.6.3 (md5 17dd2b5b66ceb572a3fd946db9b56a92, 635,798 B):
- One HTML file, no server, localStorage key `pitch-rating-v3.store` L381.
- Five tabs: Match, Data (Files/Coverage/Requests/Country packs), Calibration, Log & Settlement, Integrity & Snapshots.
- Finds: poor content quality noted by owner — AI-styled, machine strings in UI, missing plain language per A-02 decree UI-PLAIN-01, provenance panel missing (M3), form stars null on live path (G17), calibration artifacts stale (M5), no balance panel on NO CALL (M7), teamStats cache empty since migration (M6), coverage undefined label (M14), MOL shortfall fixed via 5082 store.
- One gate `PR.ingest` L709 — grammar, completeness, 90-min L887, COMP_TYPES whitelist L737 includes `uefa-cl/el/uecl` (already ready for connector), dupe fingerprint L321/L1016, no future dates, tie-linkage check.
- Outcome: Clean→staged Approve, Held Z-003 two-leg different tieIds (kept verbatim, human Approve verbatim button L3791-3814), Rejected never stored L3478.
- Dedupe add-if-new, migration atomic replace.
- Country packs tab scope=country optionally competition, preview→confirm, Mute scope soft clear (excluded every calc) vs Purge hard clear backup-gated (button reads "Download backup, then purge" L3434 auto-downloads full backup L3447).
- Backup exports wrapper format/version/schemaVersion/exportedAt + full store+log — verified 3,588,489 B, 5000 matches, 55 log entries, sha256 c7b29e85…8fc00.
- Doctrine rails table in FUNCTIONALITY §13 mapped.

## 4. Effectiveness Ledger (Preliminary) — To Be Formalised in 03

| Component | Gain | Weight Class |
|---|---|---|
| L1 DC live fit | +5.6% Brier (0.6476→0.6112) | Dominant — the probability |
| L2 scoreGrid Poisson+DC ρ-0.06 | shapes H/D/A | Core |
| L2 goalsGrid shrunk k0.5 | O2.5 ±10.3%→±2.7% | Separate family |
| L3 star draw correction ±0.02 | +0.047% full-1X2 p<0.0001 n59615 | Real small |
| L4 tiers | 0 prob | Display only |
| L5 consensus | STRONG 78.6% vs 73% top-10% | Filter only |
| R2 zone ladder | monotone 78/92 etc | Confidence |
| R2 chain cross-border | r+0.274 62.6% dir | Standby — needs harness win vs 1.00 baseline |
| R3 ELO stars | unvalidated | Display only |

Weighting rule: no component may consume another's output unless rank higher or display-only. L3 may edit L2 capped measured gain; L5/R2/R3 never edit L1-L3 enforced by tests.

## 5. Missed Work Ledger Gaps (SOT M1-M20) — Route-In Status

M1 live re-derive+auto re-validation: omitted YES → S1 LIVE-DERIVE-01 G14
M2 live form stars: omitted live path null YES → S1 G17
M3 provenance panel: omitted YES → S1 G15
M4 legacy market-gate flags inert: decision → A-04 drop+note
M5 calibration suite stale: YES → owner one-click replay owed + monthly
M6 teamStats cache empty: YES → D0 #7
M7 balance panel partial: YES → S3
M8 goal-range bins not built: YES gated → S4
M9 cross-border bridge standby 2 defects: analysis YES → S5
M10 integrity screening resolved in principle P1-non-compliant legacy: method ruling done → auditor drafts outcomes-only screen spec
M11 ELO spec adopt/retire decision: A-03 display-only
M12 old-trainer port not auditable old tree absent: YES on upload OLD-PORT-01
M13 METHODOLOGY.md closed received+integrated
M14 Coverage undefined cosmetic YES
M15 closing census leftover GER2/WAL2 pending fresh backup YES
M16 EPL rating source bootstrap→live revalidation YES → S1 G16
M17 settlement/venue-guard audit unaudited YES → S2 M17 acceptance pins
M18 compliance-suite lineage map unproven YES → S1 return req
M19 cross-league WEIGHTED bridge omitted zero code APPROVED-FOR-DOC → A-08 frozen plan S5
M20 MOLCUP shortfall open data defect D-2 → fixed to 5082 operational

## 6. What Needs Deep Dive Next

- Read chain/ build_graph.py, chain.py, weighted.py, league_strength.py, validate.py — measure vs masterplan §6 fit-to-results loop.
- Read data/ rating.py, star_*.py, venue.py, homevhome.py etc — extract constants and compare to ESPEC.
- Compute weighting-effectiveness matrix with paired stats T1 + MDE T2.
- Design singular engine blueprint: one store → one live fit → verdict card.

*No omission tolerated. Every system above traced to file/line/pin.*
