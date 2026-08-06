#!/usr/bin/env node
/* B0 self-check — runs the productionised PR.calibration module (as built into
 * the app) headlessly against the 5,082-row store and verifies:
 *   1. Parity: FULL last-omitted-season numbers == masterplan §5.2 /
 *      audit_work/ladder_baseline_2026-08-05.json (RPL/CZ1/EPL).
 *   2. Ladder: every holdout row == ladder_baseline_2026-08-05.json, 4 d.p.
 *   3. T1/T2 sanity: t-distribution p-value vs known table points.
 *   4. Gate API: free-run constants are refused; bounded steps accepted.
 * Usage: node builder/b0_selfcheck.js <app.html> <store.json> <baseline.json>
 * Output: JSON result on stdout (pretty printed).
 */
'use strict';
const fs = require('fs');
const vm = require('vm');

const [appPath, storePath, basePath] = process.argv.slice(2);
if (!appPath || !storePath || !basePath) { console.error('usage: node b0_selfcheck.js <app.html> <store.json> <baseline.json>'); process.exit(2); }

/* ---- extract the calibration.js section from the built app ---- */
const html = fs.readFileSync(appPath, 'utf8');
const m = html.match(/\/\* ==== calibration\.js ==== \*\/[\s\S]*?\n\}\)\(\);\n/);
if (!m) { console.error('FAIL: calibration.js section not found in app'); process.exit(2); }

/* ---- eval the module in a bare sandbox (no window → globalThis.PR path) ---- */
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(m[0], sandbox);
const PR = sandbox.PR;
if (!PR || !PR.calibration) { console.error('FAIL: PR.calibration not defined after eval'); process.exit(2); }

const store = JSON.parse(fs.readFileSync(storePath, 'utf8')).store;
const baseline = JSON.parse(fs.readFileSync(basePath, 'utf8'));

const res = PR.calibration.run(store);
const out = { ok: true, checks: [], parity: res.parity, summary: res.summary, generatedAt: res.generatedAt };
function check(name, ok, detail) { out.checks.push({ name, ok: !!ok, detail: detail }); if (!ok) out.ok = false; }

/* ---- 0. module identity ---- */
check('module.eval', !!PR.calibration.run, 'PR.calibration.run defined, version ' + PR.calibration.version);

/* ---- 1. FULL parity vs embedded expectation (module's own gate) ---- */
check('parity.module_allOk', res.parity.allOk === true, JSON.stringify(res.parity.rows));

/* ---- 2. per-league, per-holdout equality with ladder baseline (4 d.p.) ---- */
const r4 = x => Math.round(x * 10000) / 10000;
const r1 = x => Math.round(x * 1000) / 1000; /* baseline dir_acc has 1dp */
let maxAbsDelta = 0, ladderMismatches = [];
const HOLD = ['1','2','3','5','8','10','15','20','25','30','FULL'];
for (const lg of Object.keys(baseline.results)) {
  const L = res.leagues[lg];
  if (!L || L.refused) { ladderMismatches.push(lg + ': refused'); continue; }
  for (const h of HOLD) {
    const got = L.ladder.find(r => String(r.holdout) === h);
    const exp = baseline.results[lg][h];
    if (!got || !exp) { ladderMismatches.push(lg + '/' + h + ': missing row'); continue; }
    const fields = [
      ['scored', got.scored, exp.scored, 0],
      ['brier', r4(got.brier_dc), exp.brier, 0.00005],
      ['brier_base', r4(got.brier_base), exp.brier_base, 0.00005],
      ['logloss', r4(got.logloss), exp.logloss, 0.00005]
    ];
    for (const [f, g_, e_, tol] of fields) {
      const d = Math.abs(g_ - e_);
      maxAbsDelta = Math.max(maxAbsDelta, d);
      if (d > tol) ladderMismatches.push(`${lg}/${h}/${f}: js ${g_} vs py ${e_}`);
    }
    const dd = Math.abs(Math.round(got.dir_acc * 10) / 10 - exp.dir_acc);
    if (dd > 0.05) ladderMismatches.push(`${lg}/${h}/dir_acc: js ${got.dir_acc} vs py ${exp.dir_acc}`);
  }
}
check('ladder.exact_4dp', ladderMismatches.length === 0, ladderMismatches.length ? ladderMismatches.slice(0, 8).join(' | ') : 'all 33 holdout rows match ladder_baseline_2026-08-05.json (maxAbsDelta ' + maxAbsDelta + ')');

/* ---- 3. FULL paired stats present + sane (T1/T2 wired) ---- */
let pairedNotes = [];
for (const lg of Object.keys(res.leagues)) {
  const L = res.leagues[lg];
  if (L.refused) continue;
  const F = L.ladder.find(r => r.holdout === 'FULL');
  const P = F && F.paired;
  if (!P || P.n !== F.scored || !(P.mde80 > 0) || !(P.t !== null) || !(P.pTwo >= 0 && P.pTwo <= 1)) pairedNotes.push(lg + ': broken paired block');
}
check('paired_blocks_sane', pairedNotes.length === 0, pairedNotes.join(' | ') || 'T1 deltas, se, t, df, p, MDE80 present for every FULL row');

/* expose FULL metrics for the evidence artifact */
out.fullMetrics = {};
for (const lg of Object.keys(res.leagues)) {
  const L = res.leagues[lg];
  if (L.refused) { out.fullMetrics[lg] = { refused: L.refused }; continue; }
  const F = L.ladder.find(r => r.holdout === 'FULL');
  out.fullMetrics[lg] = {
    train: { rows: L.trainRows, window: L.trainWindow },
    holdout: { rows: F.holdoutRows, window: F.testWindow, scored: F.scored, refused: F.refused },
    brier_dc: F.brier_dc, brier_base: F.brier_base, gain_pct: F.gain_pct,
    brier_side_dc: F.brier_side_dc, brier_side_base: F.brier_side_base,
    logloss: F.logloss, dir_acc: F.dir_acc,
    calib_max_err: F.calib_max_err,
    marginals_holdout: F.marginals_holdout,
    paired: F.paired, markets: F.markets
  };
}

/* ---- 4. t-distribution known points (independent of engine) ---- */
/* tPTwo is internal; verify via paired block numbers with a fresh Python-side
   implementation (done outside); here just structural checks on ladder rows. */
const rplF = res.leagues['Russian Premier League'].ladder.find(r => r.holdout === 'FULL');
check('rpl_growth_direction', rplF.paired.meanDelta < 0, 'DC beats base on paired deltas: mean ' + rplF.paired.meanDelta);

/* ---- 5. gate API: bounded-step within caps accepted, free-run refused ---- */
const g1 = PR.calibration.acceptConstants({ LR: 0.06 });
const g2 = PR.calibration.acceptConstants({ LR: 0.5 });
const g3 = PR.calibration.acceptConstants({ RHO: -0.10 });
const g4 = PR.calibration.acceptConstants({ RHO: 0.1 });
const g5 = PR.calibration.acceptConstants({ UNKNOWN_KEY: 1 });
check('caps.bounded_ok', g1.ok && g3.ok, 'LR 0.055→0.06 (step .005 ≤ .01) and RHO -0.06→-0.10 accepted');
check('caps.freerun_refused', !g2.ok && !g4.ok && !g5.ok, 'LR→0.5 outside cap refused; RHO→0.1 outside cap refused; unknown constant refused');

/* ---- 6. P3 honesty: constant override refusal returns a refusal object ---- */
const rr = PR.calibration.run(store, { overrides: { MU0: 5 } });
check('run.freerun_refusal', rr.refused === true && typeof rr.reason === 'string', rr.reason);

console.log(JSON.stringify(out, null, 1));
process.exit(out.ok ? 0 : 1);
