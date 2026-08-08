/**
 * PITCH RATING ENGINE v4.0 — ZERO-MARKET DIXON-COLES
 * Written from ENGINE_SPEC.md v1.0. No legacy code. No embedded data. No network.
 * Verified against Python reference trainer (engine_rebuild/trainer_ref.py).
 * 
 * Constants (ENGINE_SPEC §B4):
 *   LR 0.055 · DECAY 0.0022 · HFA_LR 0.010
 *   new-team 1.6× first 8 · home_extra decay 0.999 · min 6 games
 *   ρ −0.06 · λ clamp [0.05, 6.0] · hfa clamp [0.05, 0.55] · home_extra clamp [−0.25, 0.25]
 * 
 * Usage:
 *   const engine = new PitchEngine();
 *   engine.ingest(matches);         // [{date, league, home, away, hg, ag}]
 *   const pred = engine.predict({league, home, away});
 *   // {H, D, A, lambda_home, lambda_away}
 */

const PitchEngine = (function() {
  'use strict';

  // ── CONSTANTS (ENGINE_SPEC §B4) ──
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

  // ── Factorial cache ──
  const _fact = (function() {
    const f = [1];
    for (let i = 1; i < K_GRID; i++) f[i] = f[i-1] * i;
    return f;
  })();

  // ── Dixon-Coles τ correction (ENGINE_SPEC §C1) ──
  function dcTau(i, j, lh, la) {
    if (i === 0 && j === 0) return 1 - lh * la * RHO;
    if (i === 0 && j === 1) return 1 + lh * RHO;
    if (i === 1 && j === 0) return 1 + la * RHO;
    if (i === 1 && j === 1) return 1 - RHO;
    return 1.0;
  }

  // ── Probability distribution (ENGINE_SPEC §C1) ──
  function probs(lh, la) {
    const ph = new Array(K_GRID);
    const pa = new Array(K_GRID);
    for (let i = 0; i < K_GRID; i++) {
      ph[i] = Math.exp(-lh) * Math.pow(lh, i) / _fact[i];
      pa[i] = Math.exp(-la) * Math.pow(la, i) / _fact[i];
    }
    let H = 0, D = 0, A = 0;
    for (let i = 0; i < K_GRID; i++) {
      for (let j = 0; j < K_GRID; j++) {
        const p = ph[i] * pa[j] * dcTau(i, j, lh, la);
        if (i > j) H += p;
        else if (i === j) D += p;
        else A += p;
      }
    }
    const t = H + D + A;
    return { H: H/t, D: D/t, A: A/t };
  }

  // ── Model ──
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  function Engine() {
    // State maps: string key → float
    this.att = Object.create(null);
    this.dfn = Object.create(null);
    this.hfa = Object.create(null);
    this.thfa = Object.create(null);
    this.mu = Object.create(null);
    this.seen = Object.create(null);
    this._hfa_init = HFA_INIT;
    this._mu_init = MU_INIT;
  }

  Engine.prototype._get = function(map, key, init) {
    return (key in map) ? map[key] : (map[key] = init);
  };

  Engine.prototype._getHfa = function(league) {
    return this._get(this.hfa, league, this._hfa_init);
  };

  Engine.prototype._getMu = function(league) {
    return this._get(this.mu, league, this._mu_init);
  };

  Engine.prototype._getSeen = function(team) {
    return this._get(this.seen, team, 0);
  };

  // ── λ computation (ENGINE_SPEC §B1) ──
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

  // ── Update (ENGINE_SPEC §B3) ──
  Engine.prototype.update = function(m) {
    const { league, home, away, hg, ag } = m;
    const { lambda_home: lh, lambda_away: la } = this.lam(league, home, away);

    const eh = hg - lh;
    const ea = ag - la;

    const seen_h = this._getSeen(home);
    const seen_a = this._getSeen(away);
    const kh = LR * (seen_h < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);
    const ka = LR * (seen_a < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);

    // Attack/defence updates
    this.att[home] = this._get(this.att, home, 0) + kh * eh * 0.5;
    this.dfn[away] = this._get(this.dfn, away, 0) - ka * eh * 0.5;
    this.att[away] = this._get(this.att, away, 0) + ka * ea * 0.5;
    this.dfn[home] = this._get(this.dfn, home, 0) - kh * ea * 0.5;

    // Home advantage updates
    const hfa_old = this._getHfa(league);
    this.hfa[league] = clamp(hfa_old + HFA_LR * (eh - ea) * 0.02, HFA_MIN, HFA_MAX);

    // Per-team home extra
    const thfa_old = this._get(this.thfa, home, 0);
    this.thfa[home] = clamp((thfa_old + HFA_LR * (eh - ea) * 0.010) * HOME_EXTRA_DECAY, HOME_EXTRA_MIN, HOME_EXTRA_MAX);

    // League baseline
    this.mu[league] = this._getMu(league) + MU_LR * ((eh + ea) / 2);

    // Time decay
    for (const t of [home, away]) {
      this.att[t] = (this._get(this.att, t, 0)) * (1 - DECAY);
      this.dfn[t] = (this._get(this.dfn, t, 0)) * (1 - DECAY);
    }

    this.seen[home] = seen_h + 1;
    this.seen[away] = seen_a + 1;
  };

  // ── Predict (returns null if insufficient data) ──
  Engine.prototype.predict = function(m) {
    const { league, home, away } = m;
    const seen_h = this._getSeen(home);
    const seen_a = this._getSeen(away);

    if (seen_h < MIN_GAMES || seen_a < MIN_GAMES) {
      return null;  // NO CALL — insufficient data (ENGINE_SPEC §H)
    }

    const { lambda_home, lambda_away } = this.lam(league, home, away);
    const p = probs(lambda_home, lambda_away);

    return {
      H: p.H,
      D: p.D,
      A: p.A,
      lambda_home: lambda_home,
      lambda_away: lambda_away,
      provenance: {
        home_games: seen_h,
        away_games: seen_a,
        league: league
      }
    };
  };

  // ── Ingest: feed a batch of matches in date order, return predictions ──
  Engine.prototype.ingest = function(matches) {
    // Sort by date, then league, then home, then away — matches Python reference exactly
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
      if (pred) {
        predictions.push({
          match: m,
          prediction: pred
        });
      }
      this.update(m);
    }

    return predictions;
  };

  // ── Score a set of predictions ──
  Engine.score = function(predictions) {
    const base = { H: 0.446, D: 0.268, A: 0.286 };
    let brierModel = 0, brierBase = 0, loglossModel = 0, loglossBase = 0;
    let dirCorrect = 0;
    const n = predictions.length;

    for (const p of predictions) {
      const { H, D, A } = p.prediction;
      const res = p.match.res;
      const y = {
        H: res === 'H' ? 1 : 0,
        D: res === 'D' ? 1 : 0,
        A: res === 'A' ? 1 : 0
      };

      brierModel += (H - y.H)**2 + (D - y.D)**2 + (A - y.A)**2;
      brierBase += (base.H - y.H)**2 + (base.D - y.D)**2 + (base.A - y.A)**2;

      const pRes = res === 'H' ? H : (res === 'D' ? D : A);
      loglossModel += -Math.log(Math.max(pRes, 1e-12));
      const pBase = res === 'H' ? base.H : (res === 'D' ? base.D : base.A);
      loglossBase += -Math.log(Math.max(pBase, 1e-12));

      const predRes = H > D ? (H > A ? 'H' : 'A') : (D > A ? 'D' : 'A');
      if (predRes === res) dirCorrect++;
    }

    return {
      n: n,
      brier_model: brierModel / n,
      brier_base: brierBase / n,
      brier_gain_pct: ((brierBase - brierModel) / brierBase) * 100,
      logloss_model: loglossModel / n,
      logloss_base: loglossBase / n,
      direction: dirCorrect / n
    };
  };

  // ── Serialize/deserialize state for persistence ──
  Engine.prototype.toJSON = function() {
    return {
      att: Object.assign({}, this.att),
      dfn: Object.assign({}, this.dfn),
      hfa: Object.assign({}, this.hfa),
      thfa: Object.assign({}, this.thfa),
      mu: Object.assign({}, this.mu),
      seen: Object.assign({}, this.seen)
    };
  };

  Engine.prototype.fromJSON = function(state) {
    this.att = Object.assign(Object.create(null), state.att || {});
    this.dfn = Object.assign(Object.create(null), state.dfn || {});
    this.hfa = Object.assign(Object.create(null), state.hfa || {});
    this.thfa = Object.assign(Object.create(null), state.thfa || {});
    this.mu = Object.assign(Object.create(null), state.mu || {});
    this.seen = Object.assign(Object.create(null), state.seen || {});
    return this;
  };

  return Engine;
})();

// Export for Node.js testing (browser: attach to window)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PitchEngine;
} else if (typeof window !== 'undefined') {
  window.PitchEngine = PitchEngine;
}
