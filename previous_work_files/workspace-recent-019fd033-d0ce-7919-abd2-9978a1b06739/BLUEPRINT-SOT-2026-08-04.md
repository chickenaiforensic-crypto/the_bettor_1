# PITCH RATING — SINGLE SOURCE OF TRUTH
## Engine blueprint + complete system register + missed-work ledger

**Version 1.1 · 2026-08-04 (UTC) · Issued by: Auditor · Authority: OWNER (approves amendments)**
**v1.1 amendment (A-07):** integrates `METHODOLOGY.md` v1.1 (md5 `6cd6c0c8ebc695a8fe3afc313ddc90ac` — now supplied; closes M13), adds founding principles, testing and implementation protocols, error register, compliance-suite inventory, the COLD-START KIT definition, and ledger updates (M10 resolved-in-principle; M17/M18 added). v1.0 md5 `5898cccd764c755448a12ab0bc57da5c` (superseded, kept in ZONES for traceability).

**Rule:** this document consolidates the three foundation documents — audited line-by-line against shipped app **v3.6.3** (md5 `17dd2b5b66ceb572a3fd946db9b56a92`):

| Foundation doc | Role | md5 |
|---|---|---|
| `METHODOLOGY.md` v1.1 (2026-07-30) | HOW we work: principles, testing, implementation protocols | `6cd6c0c8ebc695a8fe3afc313ddc90ac` |
| `ENGINE_SPEC.md` v1.0 (2026-07-30) | WHAT the engine computes: layers, constants, rebuild order | `91cd0cd5420cd494a799bd4050cb2ef8` |
| `LIVE-BLUEPRINT.md` v1.0-live (2026-07-30) | Evidence-engine protocol, calibration, cross-border, integration | `d01cfde0b7e75f62646bb20eb470233a` |

Every status below cites a code line, doc section, or pinned file. Where spec and code differ, the difference is written down, not smoothed over.

---

# 0. COLD-START KIT (what you need to orient fully — pinned set)

| # | Document | Purpose | Location | md5 |
|---|---|---|---|---|
| K1 | **THIS DOCUMENT (SOT v1.1)** | the map: systems, status, doctrine, ledger | root | (self-pinned in ZONES) |
| K2 | METHODOLOGY.md | principles P1–P5 · testing T1–T8 · implementation I1–I6 · error register E1–E9 | uploads/ | `6cd6c0c8ebc695a8fe3afc313ddc90ac` |
| K3 | ENGINE_SPEC.md | engine layers/constants · compliance assertions · cold-start rebuild order (its Part I) | uploads/ | `91cd0cd5420cd494a799bd4050cb2ef8` |
| K4 | LIVE-BLUEPRINT.md | evidence protocol · gentle calibration · integration modules | uploads/ | `d01cfde0b7e75f62646bb20eb470233a` |
| K5 | App v3.6.3 | the running system itself | APP-V3.6.3/ | `17dd2b5b66ceb572a3fd946db9b56a92` |
| K6 | Audit card (+ADDENDA) | data-side proof: every pack row-verified | AUDITS/AUDIT-OVERRIDE-2026-08-04/ | `b9e1775eb56128978b88efef4af876cb` |
| K7 | Pack format spec (DELIVER-02) | BP-TEAM-PACK grammar — required to produce data | OWNER-OUTBOX/DELIVER-02/ | `0613624f3a513f80a5c332ed24562b5f` |
| K8 | START-HERE-2026-08-04.md | operations runbook (imports/purges, expected numbers) | root | `8b2ac2e590fec397ab589afce6f98045` |
| K9 | COMMUNICATION-RULES-v1.md + ZONES.md | working rules + full decision/event trail (v0.86+) | root | pins in ZONES tail |
| K10 | Baseline store export (pre-programme) | rollback reference of the data world | REFERENCE/ | `5a8ba49475acfa2340ce7fd66e4dfeb0` |

**Cold-start verdict (auditor, honest):** with K1–K10 a newcomer can fully orient, operate the app, produce/import data, and rebuild every in-app engine layer. The **legacy off-app trainer** (`data/rating.py`, the 153k-match dataset, original 167-test suite code) is NOT in this workspace — full old-side rebuild stays blocked behind **M12** until the old tree is uploaded (OLD-PORT-01). This document says so rather than pretending completeness.

---

# 1. FOUNDING PRINCIPLES (METHODOLOGY Part I — binding, integrated)

| # | Principle | Consequence in practice |
|---|---|---|
| P1 | **No market data. Ever.** Excluded in ALL roles — input, feature, benchmark, sanity check, fallback | Prices/shadow are never evidence. Historical Gate 1 conclusion (market-based) is **SUSPENDED** pending outcome-only re-test (open item 3). **Doctrine ruling (A-05, RESOLVED):** the legacy integrity screen that muted 3 RPL rows used market closing prices → that METHOD is P1-non-compliant; its loss at the 2026-08-04 purge is doctrine-consistent; any future integrity screen must be **outcomes-only** (own-model collapse detection), never price-referenced |
| P2 | Results are the only ground truth | teams, date, venue, goals — nothing else enters |
| P3 | The system must be able to say "I don't know" | explicit refusals everywhere; NO CALL is a valid, shown output |
| P4 | Foundation → validation → superstructure | no layer ships before the layer beneath validates (ESPEC Part I gates) |
| P5 | Approval gate: analysis free, **shipping requires explicit owner approval** | violated once historically (Study 06, stars shipped unapproved → E7); mapped to today's owner→workorder→auditor-gate→UAT chain |

# 2. THE WHOLE SYSTEM ON ONE PAGE (plain language)

One store of completed results is the only fuel. Three computation families read it:

| Family | What it answers | How (one line) | Born in |
|---|---|---|---|
| **R1 — Rating engine** | strengths + exact probabilities | Dixon-Coles ratings → two Poisson grids → corrected H/D/A | ENGINE_SPEC v2.0 |
| **R2 — Evidence engine** | what shared history itself says; can we call this | H2H + common-opponent path graph → calibrated direction or NO CALL | LIVE-BLUEPRINT |
| **R3 — ELO/performance layer** | quick ordinal strength reading | per-match Elo updates → 1–5 ★ | app code (CAL8 port) — **not in the foundation docs** → amendment A-03 pending |

Wrapped by the **honesty shell** (P3: refuse rather than fabricate) and the **data lifecycle** (ingest gate, holds, dedupe, scopes, backup-gated purge, migration-as-undo, mutes, central requests, snapshots).

**Doctrine (owner, 2026-08-04 — A-01, ADOPTED):** *compute live from the store, or stay silent with a plain label. Precomputed carried-over material is bootstrap-only, always labelled, never load-bearing once sufficient data exists.*

---

# 3. R1 — THE RATING ENGINE (Dixon-Coles, five layers)

## 3.1 Layer architecture and significance order (ESPEC Part A — VERIFIED in code)

```
L0 DATA → L1 RATINGS (att/def/hfa) → L2 DISTRIBUTION (two grids) → L3 STAR DRAW CORRECTION
(only layer that edits probability) → L4 CLASSIFICATION (labels) → L5 SELECTION (labels, edits nothing)
```
Measured contributions: L1 +5.6% Brier · L3 +0.047% · L4/L5 zero (display only).

## 3.2 Layer 1 — ratings (ESPEC Part B — VERIFIED exact)

```
λ_home = exp( μ[league] + att[home] − def[away] + hfa[league] + home_extra[home] )
λ_away = exp( μ[league] + att[away] − def[home] )        clamp [0.05, 6.0]
def: HIGHER = BETTER defence; subtracted from opponent attack (sign convention verified L1868)
```
Online fit (`fit()` L2056+; `CONF` L~1796) — constants all verified: `LR 0.055` · new-team `1.6×` first `8` · `HFA_LR 0.010` (hfa ×0.02 / home_extra ×0.010) · home_extra decay `0.999` · att/def decay `0.0022`/match · hfa clamp [0.05,0.55] · home_extra ±0.25 · min `6` matches · `ρ −0.06`. Per-league measured home advantage 1.20×–1.36× (no global constant). Per-team home extra real but tiny (max ≈ +0.006 log-goals).

## 3.3 Layer 2 — distribution (ESPEC Part C — VERIFIED exact)

- `scoreGrid`: independent Poissons × DC τ on low scores (ρ=−0.06), normalised → H/D/A (raw; best *who-wins* estimate).
- `goalsGrid`: total shrunk toward league mean (`G_K=0.5`, `GMU=2.6186`, L1893) then λ rescaled → O/U + handicap only. Shrink justified by measured calibration (O2.5 ±10.3%→±2.7%). **BTTS withheld** (±6.0%) — correctly absent in app.
- Output provenance (ESPEC G): 1X2/tier/points/DC/DNB = star-corrected; O/U/handicap/scoreline = uncorrected grid. Verified then across 9,506 fixtures: 0 contradictions.

## 3.4 Layer 3 — star draw correction (ESPEC Part D — numbers VERIFIED exact; sourcing PARTIAL)

**The team-categorisation system (owner's example), exactly as specified:**
```
metric=(3W+D)/P · qualify P≥5 (star_min_games=5 ✓) · shrink weight 6 toward league mean ✓
stars = 1..5 rank WITHIN league (quintile) · hysteresis 0.05 ✓ (churn 21.0%→8.7%)
```
Correction: target `draw_table[tier|starGap]` (27 cells ✓) else `draw_base[tier]`; weights 0.2/0.5/0.5 ✓; **cap ±0.02** ✓; **proportional split** (M4 rule) ✓; renormalise ✓. Evidence: +0.047% full-1X2 Brier (p 0.0000, n 59,615; tier-2/3 ≈ +0.09%).

**"Above or below each other based on acquired stats" (formalised):** shrunk PPG ranks teams inside **their own league only**; the star *gap* moves only the draw rate (±2pt cap). Stars/tiers can never change who the model favours.

**Sourcing break (2026-08-04):** grades+records were served from the legacy records table (migrated path only); the live path returns `starsHome:null` → **omitted system M2/G17** (live computation or plain "not rated yet").

## 3.5 Layer 4 — classification (ESPEC E — VERIFIED byte-identical)

Points = `round(100×H_calibrated)`; bands A+ Fortress ≥70 (78.5% win, n 7,718) · A Strong ≥60 · B Lean ≥52 · C Marginal ≥45 · D Coin-flip ≥35 · E Avoid <35 — code TIERS ≡ spec incl. observed rates/n. Expected scoreline = max cell of the **uncorrected** grid, shown with its true ~13% frequency.

## 3.6 Layer 5 — selection (ESPEC F — VERIFIED exact)

Consensus = mean(HvH, AvA) goal-diff lenses, both sides ≥4 home & ≥4 away (min_games 4 ✓). Tier A/A+ only: `>1.5` STRONG (78.6%) · `>1.0` CONFIRMED (74.8%) · `<0` CONFLICTED · `|<0.2| & disagreement<0.5` DRAW-LEAN (31.8%). **Edits nothing — enforced by test** (I2/M3 constraint). Magnitude, not lens agreement, carries the signal.

## 3.7 R1 dual sourcing (status after 2026-08-04 programme)

| Source | Rates | Status TODAY |
|---|---|---|
| **Migrated bootstrap** (legacy 153k fit: 18 leagues, 414 rated teams, 342 records — per METHODOLOGY Part VI; fidelity to trainer verified historically at 0.00e+00 across 7 quantities) | the 18 legacy leagues (not RPL/CZ1) | **Orphaned** for replaced countries; A-01 demotes to labelled bootstrap (G14/G16) |
| **Live online fit** (same constants, on store rows; D3-gated: ≥2 full seasons + masked-replay verdict where DC beats evidence) | any sufficient league — RPL/CZ1 today; EPL candidate (5 seasons loaded) | engine healthy; **gate verdicts stale** (embedded constant, must be app-produced, G14); **form stars absent** (G17) |

---

# 4. R2 — THE EVIDENCE ENGINE (match-history graph)

**Binding rules (LIVE-BLUEPRINT §1 — all enforced):** results-only · no market data in any role (P1) · home-perspective · strict causality (structural `seq[:i]` slicing doctrine) · phase-gated audits · failed audit = NO CALL · published quantities carry n/spread/calibration · goals ≠ 1X2 inference · draw = home-win failure at settlement (I5) · refusal preferable to fabrication.

**Module status (blueprint §8, code-proven):**

| # | Module | Status |
|---|---|---|
| 1 identity_store | **LIVE** (identities/aliases/canon, L264-330) |
| 2 match_store (tieIds, neutral/relocated, 90-min doctrine, AET→NOTE) | **LIVE** |
| 3 evidence_graph (h2h / common / third + opponent-of-opponent; effective, agree, nocall) | **LIVE** (L1506-1609) |
| 4 cross_border_bridge | **PARTIAL/STANDBY** — evidence-cross display only; rated bridge not built → **M9** (chain validation: r=+0.274, n=693, 62.6% direction on 3rd phase, 2,778 European matches; two open defects: usability gate disproven, path discovery too narrow — open items 1-2) |
| 5 goal_range_model (0–1/2/3+ bins, separately calibrated) | **NOT BUILT** → **M8** (approved; gated on held-out win) |
| 6 confidence_calibrator (gentle shrink, versioned tables) | **PARTIAL** — gate+labels live; calibration artifacts stale → **M5** |
| 7 balance_panel (home/draw/away support shares; NO CALL must show balance) | **PARTIAL** → **M7** |
| 8 audit_log (versions, settlement, Brier/log-loss) | **LIVE** |

Gentle calibration (§4), weighting candidates W1–W4 (§5, none operational until held-out win), never-regress list (§7) — all recorded; ingest gate + Z-003 holds enforce the data-side items today.
**Explicit non-approval:** unified European ratings = **proposed, NOT approved** (open item 5) — must not be built without owner decree.

---

# 5. R3 — ELO / PERFORMANCE LAYER (in app, absent from foundation docs)

INIT 1500 · K 20 · home +65 · star = `clamp((ELO−1420)/2, 0..100)` → 1–5 ★ · perf window 6, min 3, causal before cutoff. Live-derived every derive; display-only (never edits R1/R2). **Governance:** adopt or retire — amendment **A-03 pending owner**.

---

# 6. TESTING PROTOCOL (METHODOLOGY Part IV — mandatory for any change)

| # | Rule | Teeth (failure it exists for) |
|---|---|---|
| T1 | Paired tests for model comparison (per-match differences, never resampled absolutes) | unpaired test was 10× too crude (Study 13) |
| T2 | Report the minimum detectable effect with every estimate | "not significant" uninterpretable without MDE |
| T3 | Rolling-origin validation, ≥4 expanding splits | single cut date insufficient |
| T4 | Measure the complete output (home/draw/away Brier, 1X2, log loss, calibration) | component gains can hide as another side's loss (Study 11) |
| T5 | Test the user's construction, as specified, on the case, with intermediates shown | crude stand-ins produced wrong verdicts twice (Studies 12, 17); **audit scripts included: verify the finding before reporting** |
| T6 | "Not significant" ≠ "no effect" | distinct claims, never merged |
| T7 | Check representativeness (structural breaks) | covid window flipped home-win rate 4.2pt |
| T8 | Data-driven gates only | assumed spread-gate rejected the better chains |

# 7. IMPLEMENTATION PROTOCOL (METHODOLOGY Part V — enforced)

| # | Rule | State |
|---|---|---|
| I1 | Fidelity: shipped code reproduces validated research code exactly (historical record: 0.00e+00 across 7 quantities, browser vs trainer) | applies to engine ports (verified §3); trainer itself = M12 |
| I2 | Test coverage before ship — suites (historic): core 28 · update 23 · sync 35 · stars/consensus 24 · **blueprint compliance 31** · **engine compliance 26** = 167; current builder suites: smoke 49 · R8 13 · R9 7 · R10 12 · R11 18 · scope 43 · hold 9 · parity 7 · legacy 156 | legacy↔current lineagemap unproven → **M18** (builder must map the 167-set onto today's suite names in the v3.6.4 return) |
| I3 | Market gating by measured error: ship ≤2.7% · caution 3.0–3.3% · **BTTS withheld 6.0%** | LIVE (BTTS absent; caution rows = provenance text) |
| I4 | Venue integrity is procedural, not statistical: never trust parsed venue · hard error if home team never hosted in league · tick-box vs official list · save disabled until confirmed · venue locked at entry | **PARTIAL** — venue/neutral/relocated flags in match rows + no-reflip at ingest; the entry-side flip guard (never-hosted hard error, confirm tick-box) belongs to the manual-entry surface, unaudited this session → **M17** audit row |
| I5 | Scoring rule: **a draw is a loss for a home-win call — never a push, never excluded** | Log & Settlement tab exists; rule-enforcement check pending → **M17** |
| I6 | Zero network dependency (fetch/XHR/http all 0; updates via validated file/paste intake) | LIVE (single static file; ingest gate + holds are the adversarial surface) |
| — | Update protocol lineage: OLD app used a validated paste *sync protocol* (35 tests, 11 adversarial attacks blocked); NEW app replaced it with file ingest (pack drop, one gate + holds) | mapped — no action |

# 8. ERROR REGISTER (METHODOLOGY Part VIII — kept so nothing repeats)

| # | Error | Fix rule |
|---|---|---|
| E1 unpaired test on paired data (6 studies wasted) | T1 |
| E2 no noise floor (demanded undetectable precision) | T2 |
| E3 component measured in isolation (stars wrongly rejected) | T4 |
| E4/E5 tested own construction / wrong setting (underrated home-v-home; 3rd-phase signal understated 2.6×) | T5 |
| E6 gate built on assumption (rejected better chains) | T8 |
| E7 shipped without approval | P5 |
| E8 look-ahead in star cutoffs (r inflated 0.263→0.367) | D3 causality, structural slicing |
| E9 renormalisation leak (real gain read as neutral) | M4 proportional split |

# 9. DATA LIFECYCLE LAYER (the 2026 programme)

Unchanged from v1.0 (all LIVE and current): ingest one-gate (grammar · completeness · 90-min · duplicates · no future dates — rejections never stored); Z-003 holds with human approve (v3.6.3); dedupe fingerprint date+canon(home/away/competition), add-if-new; identity canon/aliases, orphan refs rule; scope packs with preview; **backup-gated purge** (no in-app undo; undo = load backup); migration = full atomic replace; mutes = exclusion with rationale (see A-05 resolution — future screens outcomes-only); central requests D12; **D14 no-mixing**; results-only bans (P1/P2, 90-min doctrine, no zips; b64/git transport).
**Data-side quality chain (mirror of METHODOLOGY D2):** validated rows, recomputed results cross-checked, structure counts vs fixture lists, rejections counted+reported — performed auditor-side per pack (audit card K6): EPL 1,900 · CZ1 1,401 · MOLCUP 202 · RPL 1,220 · RUSCUP 341 · ADDENDUM 18, all gate-verified against independent sources.

# 10. MISSED / OMITTED SYSTEMS LEDGER (complete to 2026-08-04; route-in per row)

| # | System | Origin | Status | Approved? | Route in |
|---|---|---|---|---|---|
| M1 | Rated-layer live re-derive + auto re-validation on data change | A-01 doctrine | omitted | YES | DELIVER-06 v2 G14 → v3.6.4 |
| M2 | Live form stars + venue-record consensus from store | ESPEC D1/F | omitted (live path null) | YES | DELIVER-06 v2 G17 |
| M3 | Provenance panel (every precomputed input, origin + last-derived date) | A-01 doctrine | omitted | YES | DELIVER-06 v2 G15 |
| M4 | Legacy market-gate flags ship/caution/blocked | legacy blob | **inert** (read by no code) | DECISION | A-04 (recommend drop + note) |
| M5 | Calibration suite regeneration (zone/draw/confidence/goals/market/replay) | blueprint §8, I2 cadence | stale since imports | YES | Owner one-click "Run masked replay" post-close; monthly after |
| M6 | teamStats cache | app | empty since migration | YES | DELIVER-06 D0 #7 |
| M7 | Balance panel full build (support shares; NO CALL shows balance) | blueprint §4/mod 7 | partial | YES | builder stage after v3.6.4 |
| M8 | Goal-range bins 0–1/2/3+ (own calibration) | blueprint mod 5 | not built | YES (gated) | after M7; held-out win required |
| M9 | Cross-border rated bridge + competition awareness (cups/Europe) | blueprint §3; ESPEC J-4; METH o.i. 1-2 | standby; 2 known chain defects | analysis YES | staged research; scale=1.00 until held-out win |
| M10 | Integrity screening of new data | programme; P1 | **RESOLVED in principle (A-05):** legacy market-price screen is P1-non-compliant; do NOT restore; replacement = outcomes-only screen, spec owed | method ruling done | auditor drafts P1-compliant screen spec → owner approval (P5) |
| M11 | ELO/CAL8 spec adoption | app | live but undocumented here | DECISION | A-03 (recommend adopt display-only) |
| M12 | Old-trainer port audit (data/rating.py, 153k dataset, original suites) | ESPEC B4/I1 | **not auditable — old tree absent** | YES on upload | OLD-PORT-01 on receipt |
| M13 | METHODOLOGY.md | ESPEC header | **CLOSED — received + integrated into this § kit (md5 above)** | — | done in v1.1 |
| M14 | Coverage `undefined` label | app defect | cosmetic | YES | DELIVER-06 defect list |
| M15 | Closing census + leftover load-test rows (GER 2 + WAL 2) | programme | **pending owner fresh backup** | YES | owner → auditor decision record |
| M16 | EPL rating source (bootstrap → live revalidation attempt mandatory; fail → plain evidence label) | A-01 | scheduled | YES | DELIVER-06 v2 G16 |
| M17 | Settlement/venue-guard audit: I5 draw=loss enforcement + I4 entry-side flip guard on the app's settlement/entry surfaces | METH I4/I5 | **unaudited this session** | YES | auditor checks on v3.6.4 + M5 replay run; findings logged |
| M18 | Compliance-suite lineage map (historic 167 tests ↔ builder's current suites incl. legacy-156) | METH I2 | unproven | YES | DELIVER-06 v2 return requirement |

# 11. HOW IT ALL ADDS UP — one fixture, end to end (post-v3.6.4 doctrine)

```
1) Data in: completed 90-minute results; ingest gate + holds; dedupe; identity resolve.
2) Fixture picked → same-league check → sufficiency check (≥2 full seasons in store).
3) If sufficient: CURRENT replay verdict required (auto-refreshed after any data change);
   DC must beat evidence on masked replay → live rated card (§3) with numbers shown.
   If not: honest fallback — labeled bootstrap below sufficiency, else evidence view. NO CALL allowed (P3).
4) R2 always available: path graph → calibrated direction or NO CALL + balance panel (M7).
5) R3 ★ display-only. Every output: provenance via M3 panel (source/window/n/calibration/date).
6) Settlement: draw = loss for a home call (I5) — never a push; feeds calibration (M5, monthly cadence).
```

# 12. AMENDMENTS REGISTER

- Rule: numbered amendments (A-xx), owner-approved, ZONES-logged with md5; builder acts only on workorders quoting SOT sections; every ship bumps version + pins.
- **A-01** live-derive-or-silent — ADOPTED (2026-08-04) · **A-02** UI-PLAIN-01 — ADOPTED (2026-08-04)
- **A-03** ELO layer adopt/retire — PENDING (recommend adopt display-only) · **A-04** blob gate flags consume-or-drop — PENDING (recommend drop + note) · **A-05** integrity screen method — **RESOLVED 2026-08-04 (P1 doctrine; outcomes-only spec owed)** · **A-06** goal-range timing — PENDING (recommend after M7)
- **A-07** (document): METHODOLOGY integrated; cold-start kit defined; protocols onboarded; ledger M10 resolved, M13 closed, M17/M18 added → SOT v1.0 (`5898cccd…`) → v1.1 (this file).

# 13. REFERENCE PINS

| Item | Pin |
|---|---|
| METHODOLOGY.md | `6cd6c0c8ebc695a8fe3afc313ddc90ac` |
| ENGINE_SPEC.md | `91cd0cd5420cd494a799bd4050cb2ef8` |
| LIVE-BLUEPRINT.md | `d01cfde0b7e75f62646bb20eb470233a` |
| App v3.6.3 | md5 `17dd2b5b66ceb572a3fd946db9b56a92` · sha256 `268dc529…78dad0f9` · 635,798 B |
| Baseline store | `5a8ba49475acfa2340ce7fd66e4dfeb0` (1,432) |
| Audit card | `b9e1775eb56128978b88efef4af876cb` (+ADDENDA) |
| DELIVER-06 v2 (v3.6.4 workorder) | `9941cf900cf3cc688084da455465023a` |
| SOT v1.0 (superseded) | `5898cccd764c755448a12ab0bc57da5c` |

*Living document. Amendments per §12. Everything asserted traces to a doc section, code line, or pinned file — no stories.*
