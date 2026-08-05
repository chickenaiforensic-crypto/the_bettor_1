/* ==== calibration.js ==== */
/* ============================================================================
 * PR.calibration — S0 masked-replay test-run ladder (WO-BUILDER-B0, 2026-08-05).
 * Productionised from audit_work/backtest_harness.py + ladder_run.py (exact
 * math port; parity proven vs audit_work/ladder_baseline_2026-08-05.json and
 * reported in the evidence artifact of every run).
 * Protocol (owner, MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1):
 *   L-1 last game → L-2 last two → L-n expanding holdout → FULL last season,
 *   per league; rolling-origin with ≥4 expanding splits (T3); paired per-match
 *   comparisons only (T1); minimum detectable effect reported (T2); complete
 *   metric set (T4); held-out rows are scored, never fitted (E8).
 * Honesty shell (P3): a league without a window to score is refused with a
 * plain reason. L-1/L-2 are warm-up — one game is noise (T2/E2), the artifact
 * says so next to the small-n rows.
 * B0 measures only — engine constants unchanged. Any future adjustment path
 * passes through acceptConstants(): bounded steps inside the existing caps,
 * never free-run. The UI ships with overrides unused.
 * Zero network: this module reads only the store it is handed (P1/I6).
 * ==========================================================================*/
'use strict';

var PR = (typeof window !== 'undefined')
  ? (window.PR || (window.PR = {}))
  : (globalThis.PR || (globalThis.PR = {}));
PR.calibration = (function () {

  /* ---- pinned spec B3 constants — byte-identical port of
         audit_work/backtest_harness.py / ladder_run.py ---- */
  var HCONF = {
    LR: 0.055, DECAY: 0.0022, HFA_LR: 0.010, RHO: -0.06,
    NEW_TEAM_MULT: 1.6, NEW_TEAM_N: 8,
    MU0: 0.45, HFA0: 0.25, MU_STEP: 0.004,
    MIN_GAMES: 6,
    LAMBDA_MIN: 0.05, LAMBDA_MAX: 6.0,
    HFA_CLAMP_LO: 0.05, HFA_CLAMP_HI: 0.55,
    HOME_EXTRA_CLAMP: 0.25, HOME_EXTRA_DECAY: 0.999,
    GRID_N: 10,               /* scores 0..10 per side — 11x11 grid, as harness */
    GMU: 2.6186, G_K: 0.5     /* shrunk goals grid (measured markets block only) */
  };

  /* ---- existing caps: the only adjustment surface, bounded-step, never
         free-run (owner ladder rule). Shape per key:
         [floor, ceiling, max |step| away from the pinned spec value].
         B0 ships with zero overrides. ---- */
  var CAPS = {
    LR:     [0.01,  0.10, 0.01 ],
    DECAY:  [0.0,   0.01, 0.002],
    HFA_LR: [0.001, 0.05, 0.01 ],
    RHO:    [-0.20, 0.0,  0.05 ],
    MU0:    [0.20,  0.65, 0.10 ],
    HFA0:   [0.05,  0.55, 0.10 ]
  };

  /* ---- programme leagues (harness scope — competitionName exact filter) ---- */
  var LEAGUES = [
    { name: 'Russian Premier League', seasonStartYear: 2021 },
    { name: 'Czech First League',     seasonStartYear: 2021 },
    { name: 'England Premier League', seasonStartYear: 2021 }
  ];
  var HOLDOUT_SCHEDULE = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 'FULL'];

  /* ---- parity reference: FULL rows of audit_work/ladder_baseline_2026-08-05.json
         (5,082-row store, D-1+D-2 applied; identical to masterplan §5.2).
         Tolerance = 4th-decimal agreement (rounding level). ---- */
  var PARITY_EXPECTED = {
    'Russian Premier League': { brier_dc: 0.5675, brier_base: 0.6465, scored: 254, refused: 2, logloss: 0.9572, dir_acc: 55.9 },
    'Czech First League':     { brier_dc: 0.6090, brier_base: 0.6509, scored: 276, refused: 0, logloss: 1.0146, dir_acc: 49.3 },
    'England Premier League': { brier_dc: 0.6140, brier_base: 0.6534, scored: 374, refused: 6, logloss: 1.0226, dir_acc: 49.2 }
  };
  var PARITY_TOL = 0.0005;

  /* ------------------------------------------------------------------ *
   * exact-port math (order of operations mirrors the Python line by line)
   * ------------------------------------------------------------------ */
  var FACT = (function () { var f = [1], i; for (i = 1; i <= 10; i++) f.push(f[i - 1] * i); return f; })();

  function pmf(k, lam) { return Math.exp(-lam) * Math.pow(lam, k) / FACT[k]; }

  function gval(map, key) { var v = map[key]; return v === undefined ? 0 : v; }

  function predict(K, st, h, a) {
    var lh = Math.exp(st.mu + gval(st.att, h) - gval(st.def, a) + st.hfa + gval(st.hex, h));
    var la = Math.exp(st.mu + gval(st.att, a) - gval(st.def, h));
    if (lh < K.LAMBDA_MIN) lh = K.LAMBDA_MIN; else if (lh > K.LAMBDA_MAX) lh = K.LAMBDA_MAX;
    if (la < K.LAMBDA_MIN) la = K.LAMBDA_MIN; else if (la > K.LAMBDA_MAX) la = K.LAMBDA_MAX;
    return [lh, la];
  }

  function freshState(K) { return { att: {}, def: {}, hex: {}, seen: {}, mu: K.MU0, hfa: K.HFA0 }; }

  function seenOf(st, t) { var v = st.seen[t]; return v === undefined ? 0 : v; }

  /* One completed row folds into the state — exact port of harness update(). */
  function update(K, st, m) {
    var pr = predict(K, st, m.homeName, m.awayName), lh = pr[0], la = pr[1];
    var eh = m.homeGoals - lh, ea = m.awayGoals - la;
    var kh = K.LR * (seenOf(st, m.homeName) < K.NEW_TEAM_N ? K.NEW_TEAM_MULT : 1.0);
    var ka = K.LR * (seenOf(st, m.awayName) < K.NEW_TEAM_N ? K.NEW_TEAM_MULT : 1.0);
    st.att[m.homeName] = gval(st.att, m.homeName) + kh * eh * 0.5;
    st.def[m.awayName] = gval(st.def, m.awayName) - ka * eh * 0.5;
    st.att[m.awayName] = gval(st.att, m.awayName) + ka * ea * 0.5;
    st.def[m.homeName] = gval(st.def, m.homeName) - kh * ea * 0.5;
    st.hfa += K.HFA_LR * (eh - ea) * 0.02;
    st.hex[m.homeName] = gval(st.hex, m.homeName) + K.HFA_LR * (eh - ea) * 0.010;
    st.hex[m.homeName] *= K.HOME_EXTRA_DECAY;
    st.mu += K.MU_STEP * (eh + ea) / 2;
    if (st.hfa < K.HFA_CLAMP_LO) st.hfa = K.HFA_CLAMP_LO; else if (st.hfa > K.HFA_CLAMP_HI) st.hfa = K.HFA_CLAMP_HI;
    if (st.hex[m.homeName] < -K.HOME_EXTRA_CLAMP) st.hex[m.homeName] = -K.HOME_EXTRA_CLAMP;
    else if (st.hex[m.homeName] > K.HOME_EXTRA_CLAMP) st.hex[m.homeName] = K.HOME_EXTRA_CLAMP;
    st.att[m.homeName] *= (1 - K.DECAY); st.def[m.homeName] *= (1 - K.DECAY);
    st.att[m.awayName] *= (1 - K.DECAY); st.def[m.awayName] *= (1 - K.DECAY);
    st.seen[m.homeName] = seenOf(st, m.homeName) + 1;
    st.seen[m.awayName] = seenOf(st, m.awayName) + 1;
  }

  /* Poisson x Poisson with DC tau (rho), normalised — exact port of grid_prob().
     Returns the full grid + H/D/A + measured goals-market tails. */
  function gridProb(K, lh, la) {
    var n = K.GRID_N, p = [], i, j, t, s = 0, ph = 0, pd = 0, o25 = 0, btts = 1;
    for (i = 0; i <= n; i++) {
      p[i] = [];
      for (j = 0; j <= n; j++) {
        t = 1.0;
        if (i === 0 && j === 0) t = 1 - lh * la * K.RHO;
        else if (i === 0 && j === 1) t = 1 + lh * K.RHO;
        else if (i === 1 && j === 0) t = 1 + la * K.RHO;
        else if (i === 1 && j === 1) t = 1 - K.RHO;
        p[i][j] = pmf(i, lh) * pmf(j, la) * t;
      }
    }
    for (i = 0; i <= n; i++) for (j = 0; j <= n; j++) s += p[i][j];
    var row0 = 0, col0 = 0;
    for (i = 0; i <= n; i++) for (j = 0; j <= n; j++) {
      var q = p[i][j] / s;
      if (i > j) ph += q; else if (i === j) pd += q;
      if (i + j > 2.5) o25 += q;
      if (i === 0) row0 += q;
      if (j === 0) col0 += q;
    }
    var pa = 1 - ph - pd;              /* pa by complement — harness convention */
    btts = 1 - row0 - col0 + p[0][0] / s;
    return { ph: ph, pd: pd, pa: pa, o25: o25, btts: btts };
  }

  function yOf(m) { return m.homeGoals > m.awayGoals ? 0 : (m.homeGoals === m.awayGoals ? 1 : 2); }

  function brier3(probs, y) {
    var s = 0, i;
    for (i = 0; i < 3; i++) { var t = probs[i] - (i === y ? 1.0 : 0.0); s += t * t; }
    return s;
  }

  function logloss(probs, y) { return -Math.log(Math.max(probs[y], 1e-9)); }

  function outcomeCall(probs) {
    return (probs[0] >= probs[1] && probs[0] >= probs[2]) ? 0 : (probs[1] >= probs[2] ? 1 : 2);
  }

  /* ------------------------------------------------------------------ *
   * T1/T2 statistics — paired per-match deltas; t two-sided p via the
   * incomplete beta (Numerical Recipes betai; Lanczos ln-gamma). No libs.
   * ------------------------------------------------------------------ */
  var LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  function lgamma(z) {
    if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lgamma(1 - z);
    z -= 1;
    var x = LANCZOS[0], i;
    for (i = 1; i < 9; i++) x += LANCZOS[i] / (z + i);
    var t = z + 7.5;
    return 0.9189385332046727 + (z + 0.5) * Math.log(t) - t + Math.log(x);
  }
  function betacf(a, b, x) {
    var MAXIT = 200, EPS = 3e-14, FPMIN = 1e-300;
    var qab = a + b, qap = a + 1, qam = a - 1;
    var c = 1.0, d = 1 - qab * x / qap;
    if (Math.abs(d) < FPMIN) d = FPMIN;
    d = 1 / d;
    var h = d, m, m2, aa, del;
    for (m = 1; m <= MAXIT; m++) {
      m2 = 2 * m;
      aa = m * (b - m) * x / ((qam + m2) * (a + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
      c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
      d = 1 / d; h *= d * c;
      aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
      c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
      d = 1 / d; del = d * c; h *= del;
      if (Math.abs(del - 1) < EPS) break;
    }
    return h;
  }
  function betai(x, a, b) {
    if (x <= 0) return 0; if (x >= 1) return 1;
    var bt = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
    if (x < (a + 1) / (a + b + 2)) return bt * betacf(a, b, x) / a;
    return 1 - bt * betacf(b, a, 1 - x) / b;
  }
  /* two-sided p for |t| with df degrees of freedom */
  function tPTwo(t, df) {
    if (!(df > 0) || !isFinite(t)) return null;
    return betai(df / (df + t * t), df / 2, 0.5);
  }
  var Z_0975 = 1.959963986120195, Z_080 = 0.8416212335729143; /* α=0.05 two-sided, power 0.80 */

  function pairedStats(deltas) {
    var n = deltas.length;
    if (n < 2) {
      return { n: n, meanDelta: n ? deltas[0] : null, sd: null, se: null, t: null, df: null, pTwo: null, mde80: null,
        note: 'paired stats need ≥2 scored rows — one game is noise (T2/E2)' };
    }
    var mean = 0, i;
    for (i = 0; i < n; i++) mean += deltas[i];
    mean /= n;
    var v = 0;
    for (i = 0; i < n; i++) { var d = deltas[i] - mean; v += d * d; }
    v /= (n - 1);
    var sd = Math.sqrt(v), se = sd / Math.sqrt(n);
    var t = se > 0 ? mean / se : null;
    var df = n - 1;
    return { n: n, meanDelta: mean, sd: sd, se: se, t: t, df: df, pTwo: tPTwo(t, df), mde80: (Z_0975 + Z_080) * se, note: null };
  }

  /* ------------------------------------------------------------------ *
   * Bounded-step constants acceptance — the only adjustment surface.
   * ------------------------------------------------------------------ */
  function acceptConstants(overrides) {
    var K = {}, k;
    for (k in HCONF) K[k] = HCONF[k];
    overrides = overrides || {};
    for (k in overrides) {
      if (!CAPS[k]) return { ok: false, reason: 'constant "' + k + '" is not adjustable in the ladder (not a designated constant)' };
      var v = overrides[k];
      if (typeof v !== 'number' || !isFinite(v)) return { ok: false, reason: 'constant "' + k + '" must be a finite number' };
      var cap = CAPS[k], spec = HCONF[k];
      if (v < cap[0] || v > cap[1]) return { ok: false, reason: 'constant "' + k + '" = ' + v + ' is outside the existing cap [' + cap[0] + ', ' + cap[1] + '] — free-run calibration is not allowed' };
      if (Math.abs(v - spec) > cap[2]) return { ok: false, reason: 'constant "' + k + '" = ' + v + ' steps more than ±' + cap[2] + ' from the pinned spec ' + spec + ' — bounded steps only' };
      K[k] = v;
    }
    return { ok: true, constants: K };
  }

  /* ------------------------------------------------------------------ *
   * Ladder — L-1 → L-2 → L-n expanding → FULL, rolling-origin.
   * ------------------------------------------------------------------ */
  function runHoldout(K, trainAll, testSeason, holdoutSpec) {
    var nhold = holdoutSpec === 'FULL' ? testSeason.length : holdoutSpec;
    var label = String(holdoutSpec);
    if (nhold < 1) return { holdout: label, insufficient: true, reason: 'empty holdout' };
    if (nhold > testSeason.length) {
      return { holdout: label, insufficient: true, reason: 'holdout ' + nhold + ' exceeds completed rows in the last season (' + testSeason.length + ')' };
    }
    var train = trainAll.concat(testSeason.slice(0, testSeason.length - nhold));
    var test = testSeason.slice(testSeason.length - nhold);
    var i, m, y, s;

    /* base vector + base Brier over ALL holdout rows (refused included) —
       harness convention, preserved for parity. */
    var marg = [0, 0, 0], tot = test.length;
    for (i = 0; i < tot; i++) marg[yOf(test[i])]++;
    var base = [marg[0] / tot, marg[1] / tot, marg[2] / tot];
    var bBaseAll = 0;
    for (i = 0; i < tot; i++) bBaseAll += brier3(base, yOf(test[i]));
    bBaseAll /= tot;

    /* fit: train rows only; the holdout is scored, never fitted first (E8) */
    var st = freshState(K);
    for (i = 0; i < train.length; i++) update(K, st, train[i]);

    var scored = 0, refused = 0, bDC = 0, bl = 0, hits = 0;
    var bSideDC = [0, 0, 0], bSideBase = [0, 0, 0], margScored = [0, 0, 0];
    var deltas = [];
    var cal = [
      { n: [0,0,0,0,0,0,0,0,0,0], p: [0,0,0,0,0,0,0,0,0,0], h: [0,0,0,0,0,0,0,0,0,0] },
      { n: [0,0,0,0,0,0,0,0,0,0], p: [0,0,0,0,0,0,0,0,0,0], h: [0,0,0,0,0,0,0,0,0,0] },
      { n: [0,0,0,0,0,0,0,0,0,0], p: [0,0,0,0,0,0,0,0,0,0], h: [0,0,0,0,0,0,0,0,0,0] }
    ];
    var o25pred = 0, o25freq = 0, bttsPred = 0, bttsFreq = 0;

    for (i = 0; i < tot; i++) {
      m = test[i];
      y = yOf(m);
      if (seenOf(st, m.homeName) < K.MIN_GAMES || seenOf(st, m.awayName) < K.MIN_GAMES) {
        refused++; update(K, st, m); continue;            /* P3 refusal, then fold the row */
      }
      var lam = predict(K, st, m.homeName, m.awayName);
      var g = gridProb(K, lam[0], lam[1]);
      var probs = [g.ph, g.pd, g.pa];
      var bI = brier3(probs, y), bB = brier3(base, y);
      scored++;
      margScored[y]++;
      bDC += bI;
      bl += logloss(probs, y);
      if (outcomeCall(probs) === y) hits++;
      deltas.push(bI - bB);
      for (s = 0; s < 3; s++) {
        bSideDC[s] += Math.pow(probs[s] - (s === y ? 1 : 0), 2);
        bSideBase[s] += Math.pow(base[s] - (s === y ? 1 : 0), 2);
        var bin = Math.min(9, Math.floor(probs[s] * 10));
        cal[s].n[bin]++; cal[s].p[bin] += probs[s]; if (y === s) cal[s].h[bin]++;
      }
      /* measured goals markets — shrunk goals grid (app goalsGrid semantics;
         measured only, never an output of this module) */
      var totLam = lam[0] + lam[1];
      var scale = totLam > 1e-12 ? (K.GMU + K.G_K * (totLam - K.GMU)) / totLam : 1;
      var gg = gridProb(K, lam[0] * scale, lam[1] * scale);
      o25pred += gg.o25; if (m.homeGoals + m.awayGoals > 2.5) o25freq++;
      bttsPred += gg.btts; if (m.homeGoals > 0 && m.awayGoals > 0) bttsFreq++;
      update(K, st, m);                                  /* online causality: fold after scoring */
    }

    /* calibration max error — decile bins per side (T4) */
    var calMax = null;
    var sideNames = ['home', 'draw', 'away'];
    for (s = 0; s < 3; s++) {
      for (var b = 0; b < 10; b++) {
        if (!cal[s].n[b]) continue;
        var meanP = cal[s].p[b] / cal[s].n[b], freq = cal[s].h[b] / cal[s].n[b];
        var err = Math.abs(meanP - freq);
        if (!calMax || err > calMax.err) {
          calMax = { err: err, side: sideNames[s], bin: b, binLo: b / 10, binHi: (b + 1) / 10, n: cal[s].n[b], meanPred: meanP, observedFreq: freq };
        }
      }
    }

    var brierDC = scored ? bDC / scored : null;
    var result = {
      holdout: label, holdoutRows: tot,
      trainRows: train.length,
      trainWindow: [train[0].dateISO, train[train.length - 1].dateISO],
      testWindow: [test[0].dateISO, test[test.length - 1].dateISO],
      scored: scored, refused: refused,
      brier_dc: brierDC,
      brier_base: bBaseAll,
      gain_pct: (bBaseAll && brierDC != null) ? (brierDC / bBaseAll - 1) * 100 : null,
      brier_side_dc:   scored ? { home: bSideDC[0] / scored, draw: bSideDC[1] / scored, away: bSideDC[2] / scored } : null,
      brier_side_base: scored ? { home: bSideBase[0] / scored, draw: bSideBase[1] / scored, away: bSideBase[2] / scored } : null,
      logloss: scored ? bl / scored : null,
      dir_acc: scored ? hits / scored * 100 : null,
      calib_max_err: calMax,
      marginals_holdout: base,
      marginals_scored: scored ? [margScored[0] / scored, margScored[1] / scored, margScored[2] / scored] : null,
      paired: pairedStats(deltas),
      markets: scored ? {
        o25:  { predMean: o25pred / scored, freq: o25freq / scored, errPct: Math.abs(o25pred / scored - o25freq / scored) * 100,
                gate: (Math.abs(o25pred / scored - o25freq / scored) * 100) <= 2.7 ? 'ship ≤2.7% (I3)'
                    : (Math.abs(o25pred / scored - o25freq / scored) * 100) <= 3.3 ? 'caution 3.0–3.3% (I3)' : 'withheld >3.3% (I3)',
                note: 'shrunk goals grid k=0.5 GMU 2.6186 — measured only' },
        btts: { predMean: bttsPred / scored, freq: bttsFreq / scored, errPct: Math.abs(bttsPred / scored - bttsFreq / scored) * 100,
                status: 'withheld (I3) — measured only, never an output' }
      } : null
    };
    return result;
  }

  function runLeague(K, league, rowsSorted) {
    var cutoff = (league.seasonStartYear + 4) + '-07-01';
    var trainAll = [], testSeason = [], i;
    for (i = 0; i < rowsSorted.length; i++) {
      if (rowsSorted[i].dateISO < cutoff) trainAll.push(rowsSorted[i]); else testSeason.push(rowsSorted[i]);
    }
    if (testSeason.length < 1 || trainAll.length < 1) {
      return { refused: 'not enough completed rows for a masked replay (train ' + trainAll.length + ', last-season window ' + testSeason.length + ') — no verdict produced' };
    }
    var ladder = [];
    for (i = 0; i < HOLDOUT_SCHEDULE.length; i++) ladder.push(runHoldout(K, trainAll, testSeason, HOLDOUT_SCHEDULE[i]));
    return {
      league: league.name, cutoff: cutoff, seasonStartYear: league.seasonStartYear,
      trainRows: trainAll.length, lastSeasonRows: testSeason.length,
      trainWindow: [trainAll[0].dateISO, trainAll[trainAll.length - 1].dateISO],
      lastSeasonWindow: [testSeason[0].dateISO, testSeason[testSeason.length - 1].dateISO],
      ladder: ladder
    };
  }

  function round4(x) { return Math.round(x * 10000) / 10000; }

  /* ------------------------------------------------------------------ *
   * run(store, opts) → the artifact. opts: { overrides } (bounded, capped).
   * ------------------------------------------------------------------ */
  function run(store, opts) {
    opts = opts || {};
    var acc = acceptConstants(opts.overrides);
    var generatedAt = new Date().toISOString();
    if (!acc.ok) {
      return { refused: true, reason: acc.reason, generatedAt: generatedAt };
    }
    var K = acc.constants;
    var out = {
      module: 'PR.calibration vB0.1',
      engine: 'Dixon-Coles online fit — spec B3 constants (LR 0.055 · DECAY 0.0022 · HFA_LR 0.010 · new-team 1.6x/8 · rho -0.06 · clamps) · naive init mu 0.45 hfa 0.25 · no star correction · no evidence ensemble — exact port of audit_work/backtest_harness.py + ladder_run.py',
      protocol: 'owner ladder 2026-08-05: L-1 → L-2 → L-n expanding → FULL last season per league · rolling-origin ≥4 expanding splits (T3) · paired per-match (T1) · MDE reported (T2) · full metric set (T4) · holdout scored never fitted (E8) · muted rows excluded (doctrine: exclusion = mute; on the 5,082 store 0 mutes, so rows are byte-identical to the harness set) · BTTS withheld (I3)',
      constants: K, caps: CAPS,
      generatedAt: generatedAt,
      storeRows: store.matches.length,
      leagues: {}, refusals: [],
      parity: {
        reference: 'audit_work/ladder_baseline_2026-08-05.json FULL rows (= masterplan §5.2 first live run)',
        tolerance: PARITY_TOL, rows: {}, allOk: null
      },
      summary: null
    };
    var li, lg, rows, name;
    for (li = 0; li < LEAGUES.length; li++) {
      lg = LEAGUES[li]; name = lg.name;
      rows = [];
      for (var i = 0; i < store.matches.length; i++) {
        var m = store.matches[i];
        if (m.muted) continue;                       /* exclusion = mute (0 mutes on the pinned store) */
        if (m.competitionName === name) rows.push(m);
      }
      /* stable sort by date — same row order as the Python run on the same file */
      rows = rows.slice().sort(function (a, b) { return a.dateISO < b.dateISO ? -1 : (a.dateISO > b.dateISO ? 1 : 0); });
      if (!rows.length) {
        out.leagues[name] = { refused: 'no completed rows for this league — no verdict produced' };
        out.refusals.push(name);
        continue;
      }
      out.leagues[name] = runLeague(K, lg, rows);
      /* parity vs the pinned 2026-08-05 baseline (FULL row) */
      var L = out.leagues[name], exp = PARITY_EXPECTED[name];
      if (L.refused) { continue; }
      var F = null;
      for (var lix = 0; lix < L.ladder.length; lix++) if (L.ladder[lix].holdout === 'FULL') F = L.ladder[lix];
      if (F && F.brier_dc != null) {
        var dcR = round4(F.brier_dc), baseR = round4(F.brier_base);
        out.parity.rows[name] = {
          measured: { brier_dc: dcR, brier_base: baseR, scored: F.scored, refused: F.refused },
          expected: exp,
          delta: round4(dcR - exp.brier_dc),
          ok: Math.abs(dcR - exp.brier_dc) <= PARITY_TOL && Math.abs(baseR - exp.brier_base) <= PARITY_TOL && F.scored === exp.scored && F.refused === exp.refused
        };
      }
    }
    var names = Object.keys(out.parity.rows);
    out.parity.allOk = names.length === LEAGUES.length && names.every(function (n) { return out.parity.rows[n].ok; });
    var parts = [];
    for (li = 0; li < LEAGUES.length; li++) {
      name = LEAGUES[li].name;
      var L2 = out.leagues[name];
      if (L2.refused) { parts.push(name.split(' ')[0] + ': refused'); continue; }
      var F2 = null;
      for (var lj = 0; lj < L2.ladder.length; lj++) if (L2.ladder[lj].holdout === 'FULL') F2 = L2.ladder[lj];
      if (F2) parts.push(name.split(' ')[0] + ' FULL ' + F2.brier_dc.toFixed(4) + ' vs base ' + F2.brier_base.toFixed(4) + ' (' + (F2.gain_pct).toFixed(1) + '%, n ' + F2.scored + (F2.refused ? ' +' + F2.refused + ' refused' : '') + ')');
    }
    out.summary = 'Calibration ladder (' + parts.length + ' leagues): ' + parts.join(' · ') + ' — parity vs 2026-08-05 baseline: ' + (out.parity.allOk ? 'PASS' : 'FAIL');
    return out;
  }

  return {
    run: run,
    acceptConstants: acceptConstants,
    HCONF: HCONF, CAPS: CAPS, LEAGUES: LEAGUES, HOLDOUT_SCHEDULE: HOLDOUT_SCHEDULE,
    PARITY_EXPECTED: PARITY_EXPECTED, PARITY_TOL: PARITY_TOL,
    version: 'B0.1'
  };
})();
