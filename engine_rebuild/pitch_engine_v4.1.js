/**
 * PITCH RATING ENGINE v4.1 — L1 + L2 (Ratings + Distribution)
 * Zero-market Dixon-Coles with score-grid and shrunk goals-grid.
 * Written from ENGINE_SPEC.md v1.0 Parts B, C, G.
 * 
 * v4.1 adds:
 *   - L2 scoreGrid: Dixon-Coles τ-corrected scoreline → H/D/A (ENGINE_SPEC §C1)
 *   - L2 goalsGrid: totals shrunk toward league mean (G_K=0.5, GMU=2.6186) → O/U (ENGINE_SPEC §C2)
 *   - Goals-grid shrinkage justified by O2.5 calibration (10.3%→2.7%)
 *   - Grid provenance: 1X2 from scoreGrid, O/U from goalsGrid (ENGINE_SPEC §G)
 *   - BTTS withheld — ±6.0% calibration (I3 gate)
 */

const PitchEngineV2 = (function() {
  'use strict';

  // ── CONSTANTS ──
  const LR = 0.055;
  const DECAY = 0.0022;
  const HFA_LR = 0.010;
  const NEW_TEAM_MULT = 1.6;
  const NEW_TEAM_GAMES = 8;
  const HOME_EXTRA_DECAY = 0.999;
  const MIN_GAMES = 6;
  const RHO = -0.06;
  const LAMBDA_MIN = 0.05;
  const LAMBDA_MAX = 6.0;
  const HFA_MIN = 0.05;
  const HFA_MAX = 0.55;
  const HOME_EXTRA_MIN = -0.25;
  const HOME_EXTRA_MAX = 0.25;
  const HFA_INIT = 0.26;
  const MU_INIT = 0.30;
  const MU_LR = 0.004;
  const K_GRID = 11;

  // Goals-grid shrinkage (ENGINE_SPEC §C2)
  const G_K = 0.5;
  const GMU = 2.6186;

  // ── Factorial cache ──
  const _fact = (function() {
    const f = [1];
    for (let i = 1; i < K_GRID; i++) f[i] = f[i-1] * i;
    return f;
  })();

  // ── Helpers ──
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  // ── Dixon-Coles τ (ENGINE_SPEC §C1) ──
  function dcTau(i, j, lh, la) {
    if (i === 0 && j === 0) return 1 - lh * la * RHO;
    if (i === 0 && j === 1) return 1 + lh * RHO;
    if (i === 1 && j === 0) return 1 + la * RHO;
    if (i === 1 && j === 1) return 1 - RHO;
    return 1.0;
  }

  /**
   * L2: scoreGrid — Dixon-Coles τ-corrected Poisson grid.
   * Returns { H, D, A, grid } with H+D+A normalised to 1.
   * ENGINE_SPEC §C1
   */
  function scoreGrid(lh, la) {
    const ph = new Array(K_GRID);
    const pa = new Array(K_GRID);
    for (let i = 0; i < K_GRID; i++) {
      ph[i] = Math.exp(-lh) * Math.pow(lh, i) / _fact[i];
      pa[i] = Math.exp(-la) * Math.pow(la, i) / _fact[i];
    }
    let H = 0, D = 0, A = 0;
    const grid = new Array(K_GRID);
    for (let i = 0; i < K_GRID; i++) {
      grid[i] = new Array(K_GRID);
      for (let j = 0; j < K_GRID; j++) {
        const p = ph[i] * pa[j] * dcTau(i, j, lh, la);
        grid[i][j] = p;
        if (i > j) H += p;
        else if (i === j) D += p;
        else A += p;
      }
    }
    const t = H + D + A;
    return { H: H / t, D: D / t, A: A / t, grid: grid };
  }

  /**
   * L2: goalsGrid — totals shrunk toward league mean.
   * Used for Over/Under markets only. NOT used for 1X2.
   * ENGINE_SPEC §C2
   */
  function goalsGrid(sh, sa) {
    const total = sh + sa;
    const shrunk = GMU + G_K * (total - GMU);
    const scale = shrunk / total;
    const lh = sh * scale;
    const la = sa * scale;
    return scoreGrid(lh, la);
  }

  /**
   * Expected scoreline: highest-probability cell of the UNCORRECTED grid.
   * ENGINE_SPEC §E2. Reported with true frequency (~13%).
   */
  function expectedScoreline(lh, la) {
    const { grid } = scoreGrid(lh, la);
    let maxP = -1, bestI = 0, bestJ = 0;
    for (let i = 0; i < K_GRID; i++) {
      for (let j = 0; j < K_GRID; j++) {
        if (grid[i][j] > maxP) {
          maxP = grid[i][j];
          bestI = i;
          bestJ = j;
        }
      }
    }
    return { home: bestI, away: bestJ, probability: maxP };
  }

  /**
   * Over/Under markets — from shrunk goalsGrid.
   * BTTS computed but withheld per I3.
   * ENGINE_SPEC §G
   */
  function overUnder(lh, la) {
    const { grid } = goalsGrid(lh, la);
    let over15 = 0, over25 = 0, over35 = 0, total = 0;
    let btts = 0;

    for (let i = 0; i < K_GRID; i++) {
      for (let j = 0; j < K_GRID; j++) {
        const p = grid[i][j];
        total += p;
        const t = i + j;
        if (t > 1.5) over15 += p;
        if (t > 2.5) over25 += p;
        if (t > 3.5) over35 += p;
        if (i > 0 && j > 0) btts += p;
      }
    }

    return {
      over15: over15 / total,
      over25: over25 / total,
      over35: over35 / total,
      _btts: btts / total   // withheld per I3
    };
  }

  // ── Model ──
  function Engine() {
    this.att = Object.create(null);
    this.dfn = Object.create(null);
    this.hfa = Object.create(null);
    this.thfa = Object.create(null);
    this.mu = Object.create(null);
    this.seen = Object.create(null);
    this._leagueGoals = Object.create(null);
  }

  Engine.prototype._get = function(map, key, init) {
    return (key in map) ? map[key] : (map[key] = init);
  };

  Engine.prototype._getHfa = function(league) {
    return this._get(this.hfa, league, HFA_INIT);
  };

  Engine.prototype._getMu = function(league) {
    return this._get(this.mu, league, MU_INIT);
  };

  Engine.prototype._getSeen = function(team) {
    return this._get(this.seen, team, 0);
  };

  Engine.prototype._getGMU = function(league) {
    const d = this._get(this._leagueGoals, league, { totalGoals: 0, matchCount: 0 });
    if (d.matchCount === 0) return GMU;
    return d.totalGoals / d.matchCount;
  };

  // ── λ ──
  Engine.prototype.lam = function(league, home, away) {
    const att_h = this._get(this.att, home, 0);
    const def_h = this._get(this.dfn, home, 0);
    const att_a = this._get(this.att, away, 0);
    const def_a = this._get(this.dfn, away, 0);
    const thfa_h = this._get(this.thfa, home, 0);
    const hfa = this._getHfa(league);
    const mu = this._getMu(league);

    const lh = Math.exp(mu + att_h - def_a + hfa + thfa_h);
    const la = Math.exp(mu + att_a - def_h);

    return {
      lambda_home: clamp(lh, LAMBDA_MIN, LAMBDA_MAX),
      lambda_away: clamp(la, LAMBDA_MIN, LAMBDA_MAX)
    };
  };

  // ── Update ──
  Engine.prototype.update = function(m) {
    const { league, home, away, hg, ag } = m;
    const { lambda_home: lh, lambda_away: la } = this.lam(league, home, away);

    const g = this._get(this._leagueGoals, league, { totalGoals: 0, matchCount: 0 });
    g.totalGoals += (hg + ag);
    g.matchCount += 1;

    const eh = hg - lh;
    const ea = ag - la;

    const seen_h = this._getSeen(home);
    const seen_a = this._getSeen(away);
    const kh = LR * (seen_h < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);
    const ka = LR * (seen_a < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);

    this.att[home] = this._get(this.att, home, 0) + kh * eh * 0.5;
    this.dfn[away] = this._get(this.dfn, away, 0) - ka * eh * 0.5;
    this.att[away] = this._get(this.att, away, 0) + ka * ea * 0.5;
    this.dfn[home] = this._get(this.dfn, home, 0) - kh * ea * 0.5;

    this.hfa[league] = clamp(
      this._getHfa(league) + HFA_LR * (eh - ea) * 0.02,
      HFA_MIN, HFA_MAX
    );

    const thfa_old = this._get(this.thfa, home, 0);
    this.thfa[home] = clamp(
      (thfa_old + HFA_LR * (eh - ea) * 0.010) * HOME_EXTRA_DECAY,
      HOME_EXTRA_MIN, HOME_EXTRA_MAX
    );

    this.mu[league] = this._getMu(league) + MU_LR * ((eh + ea) / 2);

    for (const t of [home, away]) {
      this.att[t] = (this._get(this.att, t, 0)) * (1 - DECAY);
      this.dfn[t] = (this._get(this.dfn, t, 0)) * (1 - DECAY);
    }

    this.seen[home] = seen_h + 1;
    this.seen[away] = seen_a + 1;
  };

  /**
   * Predict — full L1+L2 output.
   * 1X2 from scoreGrid (star-corrected later, L3).
   * O/U from shrunk goalsGrid. BTTS withheld.
   */
  Engine.prototype.predict = function(m) {
    const { league, home, away } = m;
    const seen_h = this._getSeen(home);
    const seen_a = this._getSeen(away);

    if (seen_h < MIN_GAMES || seen_a < MIN_GAMES) {
      return null;
    }

    const { lambda_home, lambda_away } = this.lam(league, home, away);
    const sg = scoreGrid(lambda_home, lambda_away);
    const expScore = expectedScoreline(lambda_home, lambda_away);
    const ous = overUnder(lambda_home, lambda_away);

    return {
      H: sg.H, D: sg.D, A: sg.A,
      lambda_home, lambda_away,
      expectedScore: expScore,
      overUnder: {
        over15: ous.over15,
        over25: ous.over25,
        over35: ous.over35
      },
      provenance: {
        home_games: seen_h,
        away_games: seen_a,
        league: league,
        gmu_league: this._getGMU(league)
      }
    };
  };

  // ── Ingest: multi-key sort matching Python reference ──
  Engine.prototype.ingest = function(matches) {
    const sorted = matches.slice().sort((a, b) => {
      if (a.date < b.date) return -1;
      if (a.date > b.date) return 1;
      if (a.league < b.league) return -1;
      if (a.league > b.league) return 1;
      if (a.home < b.home) return -1;
      if (a.home > b.home) return 1;
      if (a.away < b.away) return -1;
      if (a.away > b.away) return 1;
      return 0;
    });

    const predictions = [];
    for (const m of sorted) {
      const pred = this.predict(m);
      if (pred) predictions.push({ match: m, prediction: pred });
      this.update(m);
    }
    return predictions;
  };

  // ── Score ──
  Engine.score = function(predictions) {
    const base = { H: 0.446, D: 0.268, A: 0.286 };
    let brierModel = 0, brierBase = 0, loglossModel = 0, loglossBase = 0;
    let dirCorrect = 0;
    const n = predictions.length;

    for (const p of predictions) {
      const { H, D, A } = p.prediction;
      const res = p.match.res;
      const y = { H: res === 'H' ? 1 : 0, D: res === 'D' ? 1 : 0, A: res === 'A' ? 1 : 0 };

      brierModel += (H - y.H) ** 2 + (D - y.D) ** 2 + (A - y.A) ** 2;
      brierBase += (base.H - y.H) ** 2 + (base.D - y.D) ** 2 + (base.A - y.A) ** 2;

      const pRes = res === 'H' ? H : (res === 'D' ? D : A);
      loglossModel += -Math.log(Math.max(pRes, 1e-12));
      loglossBase += -Math.log(Math.max(base[res === 'H' ? 'H' : res === 'D' ? 'D' : 'A'], 1e-12));

      const predRes = H > D ? (H > A ? 'H' : 'A') : (D > A ? 'D' : 'A');
      if (predRes === res) dirCorrect++;
    }

    return {
      n, brier_model: brierModel / n, brier_base: brierBase / n,
      brier_gain_pct: ((brierBase - brierModel) / brierBase) * 100,
      logloss_model: loglossModel / n, logloss_base: loglossBase / n,
      direction: dirCorrect / n
    };
  };

  // ── O/U calibration check ──
  Engine.calibrateOU = function(predictions) {
    const mkt = { over15: { p: 0, a: 0 }, over25: { p: 0, a: 0 }, over35: { p: 0, a: 0 } };
    for (const x of predictions) {
      const ou = x.prediction.overUnder;
      const t = x.match.hg + x.match.ag;
      mkt.over15.p += ou.over15; mkt.over15.a += (t > 1.5 ? 1 : 0);
      mkt.over25.p += ou.over25; mkt.over25.a += (t > 2.5 ? 1 : 0);
      mkt.over35.p += ou.over35; mkt.over35.a += (t > 3.5 ? 1 : 0);
    }
    const n = predictions.length;
    const result = {};
    for (const [k, v] of Object.entries(mkt)) {
      result[k] = { n, pred: v.p / n, actual: v.a / n, error_pct: Math.abs(v.p / n - v.a / n) * 100 };
    }
    return result;
  };

  // ── Serialize ──
  Engine.prototype.toJSON = function() {
    return {
      att: Object.assign({}, this.att),
      dfn: Object.assign({}, this.dfn),
      hfa: Object.assign({}, this.hfa),
      thfa: Object.assign({}, this.thfa),
      mu: Object.assign({}, this.mu),
      seen: Object.assign({}, this.seen),
      _leagueGoals: Object.assign({}, this._leagueGoals)
    };
  };

  Engine.prototype.fromJSON = function(state) {
    this.att = Object.assign(Object.create(null), state.att || {});
    this.dfn = Object.assign(Object.create(null), state.dfn || {});
    this.hfa = Object.assign(Object.create(null), state.hfa || {});
    this.thfa = Object.assign(Object.create(null), state.thfa || {});
    this.mu = Object.assign(Object.create(null), state.mu || {});
    this.seen = Object.assign(Object.create(null), state.seen || {});
    this._leagueGoals = Object.assign(Object.create(null), state._leagueGoals || {});
    return this;
  };

  return Engine;
})();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = PitchEngineV2;
} else if (typeof window !== 'undefined') {
  window.PitchEngineV2 = PitchEngineV2;
}
