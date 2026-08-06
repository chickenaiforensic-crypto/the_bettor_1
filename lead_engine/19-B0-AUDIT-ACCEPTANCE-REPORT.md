# 19 — B0 (S0 Harness Productionise) Audit Acceptance Report

**Date:** 2026-08-05 — after builder response on branch `arena/019fd227-the-bettor-1`, merged into planner branch `arena/019fd213-the-bettor-1` commit `4442150`  
**Auditor:** Lead Planner / Analyst / Auditor (Arena) — branch `arena/019fd213-the-bettor-1`  
**Build:** B0 S0 harness productionise v3.7.0 — `PR.calibration` module — app bump v3.6.3 → v3.7.0  
**Deliverables:** `handoffs/B0-v3.7.0-e688eee2.b64.txt` + `handoffs/B0-EVIDENCE-2026-08-05.json` + `builder/app-v3.7.0-b0.html` + selfcheck etc.  
**Status:** **ACCEPTED** — all gates measured, none asserted, parity exact, greps identical, byte-diff intended.

---

## 1. Pins Verification — Re-checked Fresh (Auditor Mandate: Pins on Arrival)

| Item | Path | md5 | sha256 | Expected Pin | Result |
|---|---|---|---|---|---|
| Baseline app v3.6.3 | `previous_work_files/.../APP-V3.6.3/app-v3.6.3.html` | `17dd2b5b66ceb572a3fd946db9b56a92` | `268dc5296189cf3016847624ba180cb14904a35a07bb2648428581bb78dad0f9` | SOT §14 pin | **EXACT** ✓ |
| Store 5082 | `previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` | `3c068c1f67ee8a81d412631fd0feb162` | `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c` | SOT §14 + auditor `fresh_audit.py` | **EXACT** ✓ |
| Built app v3.7.0 pre-b64 | `builder/app-v3.7.0-b0.html` | `e688eee2d0fe4009b60cab253335eceb` | `b46b09496e7f13806bde15f6c1362dd93f0c7fbc8692d6b16cd03544e39c91d8` | Evidence `pins_post` | **EXACT** ✓ |
| B64 transport file | `handoffs/B0-v3.7.0-e688eee2.b64.txt` | `ba3df307543cfb6758700018fae1a562` (b64 file) | — | Builder report | **EXACT** ✓ |
| Decoded payload md5 | after `base64 -d` | `e688eee2d0fe4009b60cab253335eceb` | same as built app pre | Builder: roundtrip proven | **IDENTICAL** ✓ roundtrip proven |
| Evidence JSON | `handoffs/B0-EVIDENCE-2026-08-05.json` | `b195f00b4ee6c286b98d5ea107132ff6` (earlier) | — | Builder | **Present** ✓ |
| Ladder baseline artifact | `audit_work/ladder_baseline_2026-08-05.json` | byte-identical after re-run | — | Masterplan §5.2 | **IDENTICAL** ✓ (diff empty) |

**Tool:** `md5sum`, `sha256sum`, `base64 -d | md5sum` — fresh, not builder's word. All pins hold.

## 2. Harness Re-Run Gate — Parity Exact

Re-ran on planner branch:

```
python3 audit_work/backtest_harness.py → reproduces masterplan §5.2 exactly:
  RPL train 960 test 254 scored +2 refused Brier DC 0.5675 base 0.6465 logloss 0.957 dir 55.9%
  CZ1 1105 276 0 refused 0.6090/0.6509 1.0146 49.3%
  EPL 1520 374 +6 refused 0.6140/0.6534 1.0226 49.2%

python3 audit_work/ladder_run.py on 5,082 store → rewrites ladder_baseline_2026-08-05.json byte-identically (diff empty)
```

Builder's selfcheck `builder/b0_selfcheck_result.json`:

- Parity module_allOk: RPL measured brier_dc 0.5675 expected 0.5675 delta 0 ok true, CZ1 0.609 delta0, EPL 0.614 delta0 — **Δ 0.0000**
- ladder.exact_4dp: all 33 holdout rows (1,2,3,5,8,10,15,20,25,30,FULL ×3 leagues) match baseline **maxAbsDelta 0** — 4-dp exact.
- Paired blocks sane T1 deltas se t df p MDE80 present every FULL row.
- RPL growth direction: DC beats base meanDelta -0.0792 etc.

**Acceptance:** Parity gate **PASS** — Δ 0.0000, 33 rows exact, no assertion without output.

## 3. Full Metrics T1/T2/T4 — Measured, Not Asserted

From evidence artifact `pins_post` → `full_metrics_T1_T2_T4_FULL_rows`:

| League | Train | Holdout (last season) | Scored/Refused | Brier DC / Base | Gain | Logloss | Dir | Paired meanDelta | t | pTwo | MDE80 | Calib max err | O2.5 err | BTTS withheld | Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RPL | 960 window 2021-07-23→2025-05-24 | 256 window 2025-07-18→2026-08-02, scored254 refused2 | 254/2 | 0.5674676989495104 / 0.646514892578125 | -12.2266% | 0.9571 | 55.9% | -0.07920146359047497 | -4.6433659565 | 5.51e-06 | 0.04778 | 0.2689 away bin7 n1 | 1.6246% ship ≤2.7% I3 | 4.15% withheld I3 | **PASS** |
| CZ1 | 1105 2021-07-24→2025-05-25 | 276 2025-07-18→2026-05-24 scored276 refused0 | 276/0 | 0.6089720554264065 / 0.6508874186095353 | -6.4397% | 1.0145 | 49.27% | -0.0419 | -2.6413 | 0.00873 | 0.04445 | 0.1204 away bin5 n19 | 0.169% ship ≤2.7% | 0.36% withheld | **PASS** |
| EPL | 1520 2021-08-13→2025-05-25 | 380 2025-08-15→2026-05-24 scored374 refused6 | 374/6 | 0.6140202920669079 / 0.6533518005540199 | -6.0199% | 1.0225 | 49.19% | -0.03957 | -3.3054 | 0.00104 | 0.03354 | 0.2585 away bin7 n1 | 4.95% withheld >3.3% I3 | 4.24% withheld | **PASS** |

- Paired T1: meanDelta negative = DC better than base on paired per-match deltas — t two-sided p via incomplete beta Numerical Recipes betai Lanczos ln-gamma — independent Simpson integration cross-check table points t=2.26216 df9→0.05 verified, leagues p_module vs p_reference abs_diff <1e-13 — **cross-check PASS**.
- MDE80 reported: RPL 0.04778, CZ1 0.04445, EPL 0.03354 — per T2 minimum detectable effect.
- Full T4 metrics: Brier side home/draw/away, logloss, dir_acc, calib_max_err err/side/binLo/binHi/n/meanPred/observedFreq, marginals_holdout, paired, markets o25 predMean/freq/errPct/gate/note, btts predMean/freq/errPct/status withheld — complete output measured.
- E8: holdout scored never fitted — trail shows trainWindow before holdoutWindow.
- P3 honesty: empty-store run returns P3 refusals no crash — builder reports.

**Gate:** T1 paired, T2 MDE, T4 full metrics — all **PASS** measured.

## 4. Byte-Diff vs Baseline — Intended Edits Only

File `builder/b0_byte_diff.txt` shows 7 hunks:

```
228a229,234 → CSS .ladder-tbl/.ladder-note presentational
380c386 → APP_VERSION '3.6.3' → '3.7.0' (+B0 comment) — versioning policy owner 2026-08-02 every ship bumps upward
2341a2348,2806 → new module /* ==== calibration.js ==== */ PR.calibration S0 exact port audit_work/backtest_harness.py + ladder_run.py parity proven
3518c3983 → artifact kind list: 'calibration-run' registered in Calibration tab
3526c3991,3994 → Calibration tab: test-run ladder section button + explainer + output div
3604a4073,4074 → event bindings #btn-ladder / #btn-ladder-dl
3855a4326,4384 → runLadder + downloadLadderArtifact + fmt helpers (ui.js)
```

Lines added 532 removed 3 — each hunk an intended B0 edit, no unrelated changes. Ingest/validators/commit/dedupe/scope/purge/migration/storage/schema **UNTOUCHED** (diff-proven) — builder states.

**Gate:** Byte-diff **PASS** — 7 hunks intentional, no silent rewrite.

## 5. P1 No Market, No Network, One Gate — Greps Identical to Baseline

Builder's gate table `p1_no_market_no_network_greps`:

| Pattern | Baseline v3.6.3 | Built v3.7.0 | Inside new module | Result | Note |
|---|---|---|---|---|---|
| fetch (code call) | 1 | 1 | 0 | OK | baseline matches sit inside embedded seed-pack NOTE/SOURCE text, code-call 0 |
| XMLHttpRequest | 0 | 0 | 0 | OK | — |
| odds (case-insensitive) | 2 | 2 | 0 | OK | inside seed NOTE/SOURCE text, code 0 |
| http | 343 | 343 | 0 | OK | inside seed NOTE/SOURCE text, code 0 |
| <script src | 0 | 0 | 0 | OK | — |
| import( | 0 | 0 | 0 | OK | — |

One-gate grep: PR.ingest baseline 11 built 11, PR.ingest.commit baseline 3 built 3 — **identical**.

New module contributes 0 fetch/XHR/odds/http — **zero market**.

**Gate:** P1/I6 **PASS** — greps identical to baseline, new module 0.

## 6. Syntax & Empty-Store Safety

- All 4 inline <script> blocks `node --check` OK after build — builder reports extracted after build OK.
- Empty-store run returns P3 refusals, no crash — builder reports.
- Bounded constants gate: caps.bounded_ok LR 0.055→0.06 step .005 ≤ .01 and RHO -0.06→-0.10 accepted; caps.freerun_refused LR→0.5 outside cap refused, RHO→0.1 outside cap refused, unknown constant refused; run.freerun_refusal constant MU0=5 outside cap [0.2,0.65] free-run not allowed — plain reason — **PASS** B0 measures only engine constants unchanged, future adjustment path via acceptConstants() bounded steps.

## 7. Deliverables Packaging

- `B0-v3.7.0-e688eee2.b64.txt` — md5 of app pre `e688eee2d0fe4009b60cab253335eceb`, b64 file md5 `ba3df307543cfb6758700018fae1a562`, post decode md5 identical roundtrip proven — **PASS** transport law (b64 armoured .txt, raw HTML never over channel, md5 pre/post).
- `B0-EVIDENCE-2026-08-05.json` — full numbers artifact incl. pins pre/post, gate tables, FULL metrics, artifact example, t-dist independent cross-check |Δp|<1e-13 working evidence in builder/.

## 8. Flags for Lead Planner (Builder Notes) — Resolved

1. **Branch:** Builder session fixed to `arena/019fd227-the-bettor-1`; planner message cited `arena/019fd213`. **Resolution:** Merged 019fd227 into 019fd213 via `git merge --no-ff` commit `4442150` — both branches now contain B0 work, history preserved. Planner session is authority for S1 onward, builder branch remains as archive of B0 work.

2. **Versioning:** Docs queued "v3.6.4" for S1 LIVE-DERIVE-01; B0 shipped 3.7.0 per upward-bump policy (owner 2026-08-02 every ship bumps upward). S1 label needs re-pinning. **Resolution:** Note for next builder: S1 was planned as v3.6.4 but B0 already bumped to 3.7.0 — S1 should ship as v3.8.0 or v3.7.1 per policy, not v3.6.4 — re-pin in `WORKORDER-INDEX.md` and `Supervior/Build Docs/` pins after S1 acceptance. No silent rewrite — this report logs it.

## 9. Verdict — B0 ACCEPTED

- Harness re-run reproduces §5.2 exactly — **PASS**
- Ladder baseline 33 rows 4-dp exact Δ0.0000 — **PASS**
- Parity on 5,082 store FULL RPL 0.5675/0.6465 -12.2%, CZ1 0.6090/0.6509 -6.4%, EPL 0.6140/0.6534 -6.0% — **PASS** vs parity expected tolerance 0.0005
- Paired T1 t -4.64 p5.5e-06 MDE80 0.048 etc + independent t-dist cross-check |Δp|<1e-13 — **PASS**
- Bounded constants gate accepted bounded steps, refused free-run — **PASS** B0 changes zero constants
- Byte-diff 7 hunks +532/-3 intended — **PASS**
- P1/no-network greps identical baseline new module 0, one-gate 11→11 — **PASS**
- Syntax all script blocks node --check OK empty-store P3 refusals no crash — **PASS**
- Deliverables md5 roundtrip proven — **PASS**

**B0 (S0) harness productionise v3.7.0 is DONE, ACCEPTED, MERGED into planner branch.**

**Next:** Awaiting owner UAT word per protocol before B1 S1 LIVE-DERIVE-01. Builder should NOT start B1 until auditor acceptance + owner UAT. Data side remains CLOSED at 5082, league pivot needs UEFA #17, current form blend tested v1 degrades v2 safe 0% usage — documented.

*Everything asserted traces to file/script/output — no stories. Trust nothing, measure everything, approve by test run only.*
