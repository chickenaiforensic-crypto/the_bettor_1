#!/usr/bin/env python3
"""B0 build — produces builder/app-v3.7.0-b0.html from the pinned baseline
app-v3.6.3.html (md5 17dd2b5b66ceb572a3fd946db9b56a92).

Every edit is anchored: if an anchor is not found EXACTLY once, the build
aborts. Insertions carry 'B0:' markers for the auditor's byte-diff.
Baseline file is never modified.
"""
import hashlib, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/APP-V3.6.3/app-v3.6.3.html"
MOD = ROOT / "builder/calibration_module.js"
OUT = ROOT / "builder/app-v3.7.0-b0.html"

base_md5 = hashlib.md5(BASE.read_bytes()).hexdigest()
assert base_md5 == "17dd2b5b66ceb572a3fd946db9b56a92", f"baseline md5 drifted: {base_md5}"

src = BASE.read_text(encoding="utf-8")
mod = MOD.read_text(encoding="utf-8").strip() + "\n"

def swap(old, new, tag):
    global src
    n = src.count(old)
    assert n == 1, f"anchor for {tag} found {n}x (need 1)"
    src = src.replace(old, new, 1)

# ---- Edit A: version bump → v3.7.0 (B0 ship) ----
swap("var APP_VERSION = '3.6.3';",
     "var APP_VERSION = '3.7.0'; /* B0: S0 calibration-ladder module (PR.calibration) + Calibration-tab ladder runner; engine + gate behavior otherwise byte-identical to v3.6.3 */",
     "A version bump")

# ---- Edit B: CSS for the ladder table (purely presentational) ----
CSS = """
.ladder-tbl{border-collapse:collapse;width:100%;font-size:12px;font-variant-numeric:tabular-nums;margin:8px 0}
.ladder-tbl th,.ladder-tbl td{padding:3px 8px;border-bottom:1px solid color-mix(in srgb,var(--line) 45%,transparent);text-align:right}
.ladder-tbl th:first-child,.ladder-tbl td:first-child{text-align:left}
.ladder-tbl tr.full td{font-weight:700;background:color-mix(in srgb,var(--accent) 8%,transparent)}
.ladder-note{font-size:12px;color:var(--ink2);margin:4px 0}
"""
swap(".replay-report .ok{color:var(--accent);font-weight:600;margin-top:6px}\n",
     ".replay-report .ok{color:var(--accent);font-weight:600;margin-top:6px}\n" + CSS,
     "B ladder css")

# ---- Edit C: the S0 module itself, placed between replay.js and compute.js ----
swap("/* ==== compute.js ==== */", mod + "\n/* ==== compute.js ==== */", "C module insert")

# ---- Edit D: Calibration tab — ladder section + artifact kind registration ----
old_console = """      '<button class="btn" id="btn-replay">Run masked replay</button><div id="replay-out"></div><h3>Artifacts</h3>' + artRows;"""
new_console = """      '<button class="btn" id="btn-replay">Run masked replay</button><div id="replay-out"></div>' +
      '<h3>Test-run ladder (B0)</h3>' +
      '<p class="dim">The test-run ladder re-fits the model from its earliest rows with the newest rows hidden, then scores the hidden tail — last game, last two, expanding, up to the whole last season (rolling origin, strict causality; hidden rows are scored, never fitted). It reports Brier (1X2 and each side), log loss, direction, calibration max error, and a paired per-match test against the window base rate with n and the smallest effect the run can detect (MDE). Goals markets are measured; BTTS stays withheld. Every run stores a numbers artifact below — that artifact is the approval record, and it self-checks parity against the pinned 2026-08-05 baseline.</p>' +
      '<button class="btn" id="btn-ladder">Run test-run ladder</button> <button class="btn ghost" id="btn-ladder-dl">Download ladder artifact (JSON)</button><div id="ladder-out"></div><h3>Artifacts</h3>' + artRows;"""
swap(old_console, new_console, "D console html")

old_kinds = "'market-calibration', 'replay-validation', 'dc-fitted-model'"
swap(old_kinds, "'market-calibration', 'replay-validation', 'calibration-run', 'dc-fitted-model'", "D2 artifact kind")

# ---- Edit E: bindings ----
swap("    on('#btn-replay', function () { runReplay(store, derived); });",
     "    on('#btn-replay', function () { runReplay(store, derived); });\n    on('#btn-ladder', function () { runLadder(store, derived); });\n    on('#btn-ladder-dl', function () { downloadLadderArtifact(store); });",
     "E bindings")

# ---- Edit F: ladder runner + artifact download (ui.js, next to runReplay) ----
RUNNER = """
  /* ---------------- B0: test-run ladder (PR.calibration) ---------------- */
  function fmt4(x) { return (x == null || !isFinite(x)) ? '—' : Number(x).toFixed(4); }
  function fmt1(x) { return (x == null || !isFinite(x)) ? '—' : Number(x).toFixed(1); }

  function runLadder(store, derived) {
    var out = document.getElementById('ladder-out');
    var res = PR.calibration.run(store);
    if (res.refused) {
      if (out) out.innerHTML = '<div class="replay-report"><b>Test-run ladder refused.</b><p class="dim">' + C.esc(res.reason) + '</p></div>';
      return;
    }
    /* the run's numbers artifact IS the approval record — stored with the run */
    store.artifacts = store.artifacts.filter(function (a) { return a.kind !== 'calibration-run'; });
    store.artifacts.push({ id: STORE.nextId(store, 'a'), kind: 'calibration-run', version: PR.calibration.version, generatedAt: res.generatedAt, data: res, note: res.summary });
    STORE.log(store, { type: 'calibration', action: 'calibration-ladder', summary: res.summary, detail: 'Ladder artifact stored as calibration-run ' + PR.calibration.version + ' · parity ' + (res.parity.allOk ? 'PASS' : 'FAIL') });
    PR.derive.invalidate(); STORE.save(store);

    var html = '<div class="replay-report"><b>' + C.esc(res.summary) + '</b>';
    Object.keys(res.leagues).forEach(function (lg) {
      var L = res.leagues[lg];
      if (L.refused) { html += '<p class="ladder-note">⚠ ' + C.esc(lg + ' — ' + L.refused) + '</p>'; return; }
      html += '<p class="ladder-note"><b>' + C.esc(lg) + '</b> — train ' + L.trainRows + ' rows (' + C.esc(L.trainWindow[0]) + ' → ' + C.esc(L.trainWindow[1]) + ') · last season ' + L.lastSeasonRows + ' rows (' + C.esc(L.lastSeasonWindow[0]) + ' → ' + C.esc(L.lastSeasonWindow[1]) + ')</p>';
      html += '<table class="ladder-tbl"><thead><tr><th>holdout</th><th>n</th><th>refused</th><th>Brier DC</th><th>Brier base</th><th>gain</th><th>log loss</th><th>direction</th><th>cal max err</th><th>MDE80</th><th>t (df)</th><th>p</th></tr></thead><tbody>';
      L.ladder.forEach(function (r) {
        if (r.insufficient) { html += '<tr><td>' + C.esc(String(r.holdout)) + '</td><td colspan="11" class="dim">' + C.esc(r.reason) + '</td></tr>'; return; }
        var p = r.paired || {};
        html += '<tr' + (r.holdout === 'FULL' ? ' class="full"' : '') + '>' +
          '<td>' + C.esc(String(r.holdout)) + '</td><td>' + r.scored + '</td><td>' + r.refused + '</td>' +
          '<td>' + fmt4(r.brier_dc) + '</td><td>' + fmt4(r.brier_base) + '</td><td>' + fmt1(r.gain_pct) + '%</td>' +
          '<td>' + fmt4(r.logloss) + '</td><td>' + fmt1(r.dir_acc) + '%</td>' +
          '<td title="' + C.esc(r.calib_max_err ? (r.calib_max_err.side + ' bin ' + r.calib_max_err.binLo.toFixed(1) + '–' + r.calib_max_err.binHi.toFixed(1) + ', n ' + r.calib_max_err.n + ', mean ' + r.calib_max_err.meanPred.toFixed(3) + ' vs freq ' + r.calib_max_err.observedFreq.toFixed(3)) : '') + '">' + fmt4(r.calib_max_err && r.calib_max_err.err) + '</td>' +
          '<td>' + fmt4(p.mde80) + '</td><td>' + fmt1(p.t) + ' (' + (p.df == null ? '—' : p.df) + ')</td><td>' + (p.pTwo == null ? '—' : (p.pTwo < 0.0001 ? '<0.0001' : p.pTwo.toFixed(4))) + '</td></tr>';
      });
      html += '</tbody></table>';
      var F = L.ladder.filter(function (r) { return r.holdout === 'FULL'; })[0];
      if (F && !F.insufficient) {
        var par = res.parity.rows[lg];
        html += '<p class="ladder-note">FULL detail — Brier H/D/A ' + fmt4(F.brier_side_dc.home) + ' / ' + fmt4(F.brier_side_dc.draw) + ' / ' + fmt4(F.brier_side_dc.away) +
          ' (base ' + fmt4(F.brier_side_base.home) + ' / ' + fmt4(F.brier_side_base.draw) + ' / ' + fmt4(F.brier_side_base.away) + ')' +
          ' · paired Δ Brier mean ' + fmt4(F.paired.meanDelta) + ' ± se ' + fmt4(F.paired.se) +
          ' · O2.5 ' + fmt1(F.markets.o25.errPct) + '% err (' + C.esc(F.markets.o25.gate) + ')' +
          ' · BTTS ' + fmt1(F.markets.btts.errPct) + '% err (' + C.esc(F.markets.btts.status) + ')' +
          (par ? ' · parity vs 2026-08-05 baseline: <b>' + (par.ok ? 'PASS' : 'FAIL — Δ ' + fmt4(par.delta)) + '</b>' : '') + '</p>';
      }
    });
    html += '<p class="ladder-note">Artifact stored in-store as <b>calibration-run ' + C.esc(PR.calibration.version) + '</b> (' + C.esc(res.generatedAt.slice(0, 19)) + 'Z) — listed under Artifacts below and downloaded with the button above. Small-holdout rows (L-1, L-2) are warm-up only; one game is noise.</p></div>';
    if (out) out.innerHTML = html;
    toast('Test-run ladder complete — artifact stored.');
  }

  function downloadLadderArtifact(store) {
    var art = null;
    store.artifacts.forEach(function (a) { if (a.kind === 'calibration-run') art = a; });
    if (!art) { toast('No ladder artifact yet — run the test-run ladder first.'); return; }
    download('calibration-run-' + String(art.generatedAt).slice(0, 10) + '.json', JSON.stringify(art, null, 1));
    toast('Ladder artifact downloaded.');
  }

  function today() {"""
swap("  function today() {", RUNNER, "F runner")

OUT.write_text(src, encoding="utf-8")
b = OUT.read_bytes()
print("baseline md5 :", base_md5)
print("built bytes  :", len(b))
print("built md5    :", hashlib.md5(b).hexdigest())
print("built sha256 :", hashlib.sha256(b).hexdigest())
