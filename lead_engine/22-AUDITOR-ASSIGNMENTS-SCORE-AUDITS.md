# 22 — Auditor Assignments: Score Audits Delegated (Per Owner: lengthy, assign to auditor)

**Date:** 2026-08-05 continued  
**Owner directive:** "you can also assign your score audits to the auditor you brought on board to do it properly so you can attend to other things as team and league audits is very lengthy"  
**Assigned by:** Lead Planner (Arena) — branch `arena/019fd213-the-bettor-1`  
**Assignee:** Auditor Support (team member from ROLE-AUDITOR, fresh code mandate)  
**Status:** ASSIGNED — Lead attends to structural finalization, cross-league pivot, architecture human-friendly build, team coordination.

---

## Why Delegate

- Full league audits are lengthy: each new pack ITA 1901 (380×5), GER 1540 (306×5), FRA 1686 (380+380+306+306+306), UEFA 1390 (689+437+264) requires RSSSF re-parse, second-index OFB/worldfootball/wiki, table reproduction 20/20 or 18/18 per season, participation completeness, structure shared tieId, 90-min doctrine, boundary/dedupe/name resolution, legacy cross-diff vs 4244-row Euro index, spot-audit one matchweek per season NOTE, continuity gap-free.
- Score audits are lengthy: per league calibration — Brier 1X2 full + per-side home/draw/away, logloss, direction accuracy, calibration max error bins, O2.5 and BTTS measured markets with I3 gates ship ≤2.7% caution 3.0-3.3% withheld 6.0%, paired T1 per-match deltas mean/sd/se/t/df/pTwo, MDE80 T2, rolling-origin T3 ≥4 expanding splits, full metric set T4, E8 holdout scored never fitted, T7 covid/structural break, T8 data-driven gates only.
- Lead needs to attend to: cross-league pivot s[L] bias loop fit-to-results per owner clarification (league X points above), per-team live up/down app alive, current form blend retune playoff-only α0.15, architectural human-friendly prototype smooth English icons with context, builder B0→B1 coordination, researcher returns consolidation.

## Score Audits Delegated to Auditor

### A. Data Verification (Already Smoke PASS, Need Full)

For each pack in `handoffs/` (ITA, GER, FRA, UEFA after fix):

| Gate | What to Do | Script | Expected Result |
|---|---|---|---|
| Grammar | BP-TEAM-PACK v2 line format MATCH|date|competition|compType|home|hg|ag|away|round|stadium|city|country|tieId|source, TEAM lines, SOURCE URL+date+what verified, NOTE info/warning/blocker, END marker, no tables | `pack_parse.py` | 0 bad compType whitelist domesleague/other/uefa-cl/el/uecl PASS |
| Boundary | No future >2026-08-05, integer 0-30 scores, required keys, dateISO valid | `fresh_audit.py` + `verify_new_packs.py` | 0 future, 0 bad, 0 missing PASS |
| Dedupe inside | Fingerprint date+home+away+competition inside file 0 dup | `verify_new_packs.py` | ITA 0 dup PASS, GER 0, FRA 0, UEFA currently 1 dup FAIL → fix pending (Real Madrid-Chelsea) |
| Dedupe vs Store | vs 5082 store fingerprints 0 overlap for new leagues ITA/GER/FRA/UEFA | `verify_new_packs.py` | 0 overlap PASS |
| Structure | Per competition season counts vs official format: ITA 38×10 ties, GER 34×9, FRA 38×10 then 34×9 after contraction 20→18, playoffs 2 legs shared tieId per Z-003, single-leg empty, roundLeg field not blank | workorder §5 + manual | 380×5 ITA, 306×5 GER, 380+380+306+306+306 FRA +8 playoffs etc PASS |
| 90-min doctrine | Every AET/pens tie carries 90' score + advancement NOTE info/advancement which side advanced how pens score, neutral venue NOTE info/neutral_venue reason | workorder grammar | Check German 2 ET legs, French 2 aet legs, ITA spareggio neutral, etc |
| Names | Every home/away resolves to roster canon/alias or TEAM rows, zero split identities — check Paris SG / St Etienne traps FRA, M'gladbach GER, etc | `pack_parse.py` + roster from workorder section 3 | 0 split PASS |
| Table reproduction | Recompute final tables FROM your rows, compare vs RSSSF/Wikipedia 20/20 ITA, 18/18 GER, 20→18 FRA per season, 16/16 RPL/CZ1 already done — auditor re-runs with fresh parser | `rsssf_verify.py` + fresh parser you write (never reuse old) | 5/5 ITA 20/20, 5/5 GER 18/18 EXACT, 5/5 FRA 20/20 then 18/18 EXACT, RPL 16/16 etc |
| Second-index | Wikipedia season articles results matrices + worldfootball.net all_matches per-round pages per season + openfootball second-index ledgers 380/380 fixtures and dates identical etc per researcher logs | `diff_ita_second_index.py` equivalents | 380/380 etc PASS, source_conflicts adjudicated vs third source (transfermarkt/soccerway/official) + NOTE warning/source_conflict |
| Legacy cross-diff | vs football-data/openfootball lineage `export/01_matches.csv` 202k dataset + 4244-row European index for UEFA connector | `legacy_diff.py` | 0 score/side mismatches day-by-day PASS |
| Participation completeness | Every programme-league club Euro list for UEFA connector + every club domestic list for ITA/GER/FRA complete vs official participant lists — club that qualified has every match of every phase it played present, absent = gap defect | workorder §5 | Complete |
| Spot-audit trail | One matchweek per season re-listed in NOTE with source URL | workorder §5 | Present |
| Continuity | Full gap-free span 2021-22→today for programme clubs, any official in-scope tie stored nowhere = gap defect | workorder §5.1 | Gap-free |
| Pins on arrival | md5/sha256 on arrival vs declared pin before anything else, raw CDN never trusted git blobs or b64 | ROLE-AUDITOR binding #3 | Pins EXACT |

**Scripts to use/create (fresh code only, never reuse old auditor's scripts as evidence — write new parser, compare):**

- `audit_work/fresh_audit.py` — grammar, table repro smoke, census 5082, pins EXACT c7b29e85/c9ad6a54, 0 dup 0 future, RPL 240 rows 16 teams etc — already PASS.
- `audit_work/verify_new_packs.py` — smoke ITA 1901 GER 1540 FRA 1686 UEFA 1390 per-season counts, per-season unique teams, top tables, dedupe vs 5082 — already smoke PASS except UEFA 1 dup.
- `audit_work/pack_parse.py` — base BP-TEAM-PACK v2 parser.
- `audit_work/rsssf_verify.py` — round-by-round vs RSSSF archives — authoritative 16/16.
- `audit_work/legacy_diff.py` — vs 202k dataset + 4244-row Euro index.
- **NEW you create:** `audit_work/rere_parse_ita.py`, `rere_parse_ger.py`, `rere_parse_fra.py`, `rere_parse_uefa.py` — fresh RSSSF re-parsers for ITA (ital2022..2026), GER (duit2022..2026), FRA (fran2022..2026), UEFA (country European sections #ec + UEFA.com + Wikipedia + worldfootball) — structural (Jul-Dec = season-1 year, Jan-Jun = season year) + postponed blocks + transliterations normalised.
- `audit_work/second_index_*.py` — OFB/worldfootball/wiki matrices.

**Deliverable from you (auditor):** One approval card per pack (or defect list with exact defect — fix only what listed) + updated `lead_engine/21-NEW-PACKS-VERIFICATION-FULL.md` → full audit section + pins.

### B. Score Audits (Calibration, Brier, Paired, MDE)

After ITA/GER/FRA/UEFA pass full audit and import via app one gate (add-if-new) + masked replay M5 + ladder re-run parity:

| Score Gate | What to Do | Script | Expected |
|---|---|---|---|
| Brier 1X2 full + per-side home/draw/away | Compute per league train 2021-22..2024-25 test last omitted season 2025-26 (or expanding holdout 1,2,3,5,8,10,15,20,25,30,FULL per ladder) — Brier DC vs base marginals + per-side | `audit_work/backtest_harness.py` + `ladder_run.py` + `current_form_blend.py` v1/v2 + builder `PR.calibration` module in app v3.7.0 | RPL 0.5675 vs base 0.6465 -12.2% n254+2 refused PASS, CZ1 0.6090/0.6509 -6.4%, EPL 0.6140/0.6534 -6.0%, ITA/GER/FRA must beat base per league on omitted window paired — gate to stay |
| Logloss + direction accuracy | Same train/test — logloss = -mean log max(p_y,1e-9), dir_acc = outcomeCall == y | same | Logloss RPL 0.957 etc, dir 55.9% etc |
| Calibration max error | Bin predictions 0-0.1,0.1-0.2...0.9-1.0 per side home/draw/away, meanPred vs observedFreq per bin, max err + side + binLo/binHi + n + meanPred + observedFreq | `PR.calibration` module | Calib ≤2.7% per I3, err max 0.26 etc — must report |
| Measured markets O2.5 + BTTS | O2.5 predMean freq errPct gate ship ≤2.7% caution 3.0-3.3% withheld 6.0% — BTTS withheld correctly absent in app per I3 | same | O2.5 RPL predMean 0.4886 freq 0.4724 err 1.62% ship, BTTS predMean 0.4939 freq 0.5354 err 4.15% withheld — etc per evidence artifact |
| Paired T1 | Per-match deltas base_error - variant_error, mean/sd/se/t/df/pTwo, positive = variant better, t-distribution via incomplete beta Numerical Recipes betai Lanczos ln-gamma independent Simpson cross-check \|Δp|<1e-13 | same + `b0_selfcheck.js` t-dist | RPL t -4.64 p5.5e-06 MDE80 0.048 etc — must report |
| MDE80 T2 | Minimum detectable effect 80% power alpha .05 two-sided = 2.8*sd/sqrt(N) | same | Report with every result — not sig uninterpretable without MDE |
| Rolling-origin T3 | ≥4 expanding splits train_frac 0.55 etc — not just one cut | `harness.py` rolling_splits | 4+ splits |
| Full output T4 | Home/draw/away Brier + 1X2 + logloss + calibration — component gains can hide as other side loss Study11 | same | All 5 metrics |
| User construction T5 | Test user's construction as specified on case with intermediates shown — crude stand-ins produced wrong verdicts twice Studies12,17 — audit scripts included verify finding before reporting | — | Verify finding before reporting |
| Not sig ≠ no effect T6 | Distinct claims never merged | — | Distinct |
| Representativeness T7 | Check structural breaks covid window flipped home-win 4.2pt | — | Covid Start/End 2020-03-01 to 2021-06-30 flagged |
| Data-driven gates T8 | No assumed spread-gate rejected better chains — measured 84/84 no discrimination recency rejected, venue correction pocket worse rejected, spread-based gate tight worse r0.195 vs 0.384 rejected | — | No intuition gates |
| Bounded constants | Adjustments accepted only within existing caps/steps floor/ceiling/max step per key LR [0.01,0.10,0.01] etc — free-run refused plain reason | `PR.calibration.acceptConstants()` + `b0_selfcheck.js` caps.bounded_ok + caps.freerun_refused | LR 0.055→0.06 step .005 ≤.01 accepted, LR→0.5 outside cap refused, MU0=5 outside [0.2,0.65] refused |
| Empty-store P3 refusals | Empty store run returns P3 refusals no crash | selfcheck | PASS |

**Deliverables:**

- `audit_work/score_audit_ita.py`, `score_audit_ger.py`, `score_audit_fra.py`, `score_audit_uefa_connector_league_pivot.py` — each runs ladder L-1→FULL per league, outputs Brier base vs DC, gain %, logloss, dir, paired meanDelta sd se t df pTwo mde80, calib max err, markets o25/btts, artifact JSON.
- Updated `audit_work/ladder_baseline_2026-08-05.json` after import of ITA/GER/FRA/UEFA — byte-identical re-run check + new baseline with expanded leagues.
- One approval card per league: "League X FULL Brier DC X vs base Y -Z% n ... paired t ... p ... MDE80 ... cal max err ... o25 errPct ... gate ship/caution/withheld" — numbers artifact IS approval record.

### C. M10 Outcomes-Only Integrity Screen (Spec Owed)

Per SOT A-05 RESOLVED: legacy market-price mute screen is P1-non-compliant — purge loss doctrine-consistent — do NOT restore. Replacement = outcomes-only screen, spec owed by auditor, owner P5 approval required.

**Task:** Draft `lead_engine/XX-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md`:

- No market data in any role — own-model collapse detection only: e.g., team rating jumps >X in Y matches without results? Or own-model predicted prob collapse vs settlement Brier sudden increase? Or team that never hosted per I4 venue guard?
- Muted rows kept visible excluded every calc never deleted — Restore reverses.
- Snapshots taken before every commit.
- Spec must be outcomes-only, P1 compliant, P3 honest.

## Lead Attends To (Not Delegated)

While auditor does above lengthy audits, Lead (me) attends to:

1. **Cross-league pivot s[L] fit-to-results loop** — Owner clarification per-league X points above/below — implement `audit_work/league_pivot_fit.py` that takes connector UEFA 1390 + domestic ratings and iteratively fits s[L] bias loop step0.05-0.1 20-50 iter bias<0.02, validates weighted vs frozen 1.00 baseline on last Euro omitted window — produces `dc-fitted-league-pivot` artifact with n/window/Brier/date provenance M3.

2. **Current form blend retune** — v1 generic recent 6 α0.35 degrades Brier -0.00963, v2 playoff-only α0.15 safe 0% usage — retune v3 playoff-only α0.15-0.20 ELO-based efficiency relative to expectation (actual GD - expected GD) + minimum playoffs 3 + win streak, test on 5082 + new leagues after import, must win harness vs base-only to ship S4.

3. **Architecture human-friendly build S7** — Smooth English not bot scattered, icon highlights with context explanation, screen redesign per `11-HUMAN-FRIENDLY-DELIVERY-SPEC` + `15-PROTOTYPE` + `17-DETAILED` — prototype HTML `prototype-human-friendly.html` demonstrating Match tab verdict sentence + icons + why + Technical details small-print + balance panel M7 + provenance M3 + primary CTA obvious.

4. **Builder coordination** — B0 ACCEPTED v3.7.0 merged, awaiting owner UAT before B1 S1 LIVE-DERIVE-01 — review B1 returns, byte-diff vs baseline, P1/no-network/one-gate greps, harness ladder re-run parity, evidence artifact.

5. **Team coordination** — Researcher1 consolidated (ITA/GER/FRA), Researcher2 UEFA defect returned for fix, Builder B0 done, Auditor assignments as per this doc, Owner standby.

## Communication Rules (Binding)

- Clear, Brief, Summarised like owner has no idea.
- Never skim read, never assume, never guess, always audit and confirm before touching anything, do what user wants not what seems logical, ask when unclear one direct question, before writing anything plan first, audit before every question — question already answered by system is failure.
- Every claim traces to file/line/pin — no stories.
- Fresh code always for auditor — never reuse old auditor scripts as evidence — write new parser, compare.

## Next Actions For Auditor (You)

1. Checkout planner branch `arena/019fd213-the-bettor-1` && pull.
2. Read `20-RESEARCHER-RETURNS-CONSOLIDATION-AUDIT.md` + `21-NEW-PACKS-VERIFICATION-FULL.md` + this assignment.
3. Create fresh parsers `rere_parse_ita.py` etc — run full gates — produce defect lists or approval cards per pack into `lead_engine/` or `Supervior/updates/`.
4. After full gates PASS — import packs via app one gate (add-if-new) + masked replay M5 + ladder re-run parity — produce new baseline artifact.
5. Run score audits per league — produce Brier/logloss/dir/paired/MDE/calib/markets artifacts — approval cards.
6. Draft M10 spec.

**Lead will continue cross-league pivot + current form + architecture prototype + builder coordination.**

*Assignment issued — Lead attends to other things, auditor attends to lengthy team and league audits properly with fresh code.*
