/**
 * PITCH RATING v5.0 — CORRECTED ENGINE
 * Dixon-Coles L1 + L2 + L3 with per-league measured constants.
 * No inherited spec constants. Everything measured from our 5,082-row store.
 * 
 * v5.0 fixes:
 *   - Per-league base rates (not global 44.6/26.8/28.6)
 *   - Per-league GMU (not 2.6186) → goals-grid calibrated to our data
 *   - Per-league DRAW_TABLE fitted from training (masked 2021-24)
 *   - Engine.score() reports vs per-league base + global reference
 * 
 * v4.2 inheritance: Dixon-Coles gradient, scoreGrid, goalsGrid, star correction
 * v4.0 inheritance: sort-order fix, Python-verified L1 math
 */

const PitchEngineV5 = (function() {
  'use strict';

  // ── DC CONSTANTS (unchanged — ENGINE_SPEC verified) ──
  const LR = 0.055;
  const DECAY = 0.0022;
  const HFA_LR = 0.010;
  const NEW_TEAM_MULT = 1.6;
  const NEW_TEAM_GAMES = 8;
  const HOME_EXTRA_DECAY = 0.999;
  const MIN_GAMES = 6;
  const MIN_STAR_GAMES = 5;
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
  const G_K = 0.5;
  const STAR_SHRINK_WEIGHT = 6;
  const STAR_CAP = 0.02;

  // ── Global spec reference (for comparison only, NOT used in scoring) ──
  const SPEC_BASE = { H: 0.446, D: 0.268, A: 0.286 };
  const SPEC_GMU = 2.6186;

  // ── Per-league measured constants (from our 5,082-row store, training 2021-24) ──
  const LEAGUES = {
    E0: {
      base: { H: 0.4454, D: 0.2303, A: 0.3243 },
      gmu: 2.9711,
      draw_table: { 0:0.2568, 1:0.2309, 2:0.2306, 3:0.2115, 4:0.1786 },
      draw_base: 0.2303,
      tier_weight: 0.41
    },
    RPL: {
      base: { H: 0.4512, D: 0.2425, A: 0.3062 },
      gmu: 2.7349,
      draw_table: { 0:0.2740, 1:0.2390, 2:0.2508, 3:0.2125, 4:0.2316 },
      draw_base: 0.2425,
      tier_weight: 0.35
    },
    CZ1: {
      base: { H: 0.4298, D: 0.2332, A: 0.3370 },
      gmu: 2.8580,
      draw_table: { 0:0.3110, 1:0.2598, 2:0.2291, 3:0.1966, 4:0.1264 },
      draw_base: 0.2332,
      tier_weight: 0.40
    }
  };

  // ── Factorial cache ──
  const _fact = (function() {
    const f = [1];
    for (let i = 1; i < K_GRID; i++) f[i] = f[i-1] * i;
    return f;
  })();

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  // ── League config lookup ──
  function getLeague(league) {
    const lg = LEAGUES[league];
    if (!lg) return null;
    return lg;
  }

  // ── Dixon-Coles τ ──
  function dcTau(i, j, lh, la) {
    if (i === 0 && j === 0) return 1 - lh * la * RHO;
    if (i === 0 && j === 1) return 1 + lh * RHO;
    if (i === 1 && j === 0) return 1 + la * RHO;
    if (i === 1 && j === 1) return 1 - RHO;
    return 1.0;
  }

  // ── L2: scoreGrid ──
  function scoreGrid(lh, la) {
    const ph = new Array(K_GRID), pa = new Array(K_GRID);
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
        if (i > j) H += p; else if (i === j) D += p; else A += p;
      }
    }
    const t = H + D + A;
    return { H: H/t, D: D/t, A: A/t, grid };
  }

  // ── L2: goalsGrid (per-league GMU) ──
  function goalsGrid(sh, sa, gmu) {
    const total = sh + sa;
    const gm = gmu != null ? gmu : SPEC_GMU;
    const shrunk = gm + G_K * (total - gm);
    const scale = shrunk / total;
    return scoreGrid(sh * scale, sa * scale);
  }

  function expectedScoreline(lh, la) {
    const { grid } = scoreGrid(lh, la);
    let maxP = -1, bi = 0, bj = 0;
    for (let i = 0; i < K_GRID; i++)
      for (let j = 0; j < K_GRID; j++)
        if (grid[i][j] > maxP) { maxP = grid[i][j]; bi = i; bj = j; }
    return { home: bi, away: bj, probability: maxP };
  }

  function overUnder(lh, la, gmu) {
    const { grid } = goalsGrid(lh, la, gmu);
    let o15 = 0, o25 = 0, o35 = 0, tot = 0;
    for (let i = 0; i < K_GRID; i++)
      for (let j = 0; j < K_GRID; j++) {
        tot += grid[i][j];
        const s = i + j;
        if (s > 1.5) o15 += grid[i][j];
        if (s > 2.5) o25 += grid[i][j];
        if (s > 3.5) o35 += grid[i][j];
      }
    return { over15: o15/tot, over25: o25/tot, over35: o35/tot };
  }

  // ── L3: Star Classification ──
  function computeStars(teams) {
    if (teams.length === 0) return {};
    const qualified = teams.filter(t => t.played >= MIN_STAR_GAMES);
    if (qualified.length === 0) return {};

    const rawPPG = qualified.map(t => ({
      name: t.name,
      ppg: (3 * t.w + t.d) / Math.max(t.played, 1),
      played: t.played
    }));

    const leagueMean = rawPPG.reduce((s, t) => s + t.ppg, 0) / rawPPG.length;

    const shrunk = rawPPG.map(t => ({
      name: t.name,
      ppg: t.ppg,
      shrunk: (t.ppg * t.played + leagueMean * STAR_SHRINK_WEIGHT) / (t.played + STAR_SHRINK_WEIGHT),
      played: t.played
    }));

    shrunk.sort((a, b) => b.shrunk - a.shrunk);

    const n = shrunk.length;
    const result = {};
    for (let i = 0; i < n; i++) {
      const quintile = Math.floor((i / n) * 5) + 1;
      result[shrunk[i].name] = { ppg: shrunk[i].ppg, shrunk: shrunk[i].shrunk, stars: quintile };
    }
    return result;
  }

  // ── L3: Apply star draw correction (per-league tables) ──
  function applyStarCorrection(rawH, rawD, rawA, homeStars, awayStars, leagueCfg) {
    if (!leagueCfg || homeStars == null || awayStars == null) {
      return { H: rawH, D: rawD, A: rawA, corrected: false };
    }

    const gap = Math.abs(homeStars - awayStars);
    const drawTable = leagueCfg.draw_table;
    const drawBase = leagueCfg.draw_base;
    const tgt = (drawTable && drawTable[gap] != null) ? drawTable[gap] : drawBase;
    const w = leagueCfg.tier_weight || 0.4;

    let D2 = (1 - w) * rawD + w * tgt;
    D2 = clamp(D2, rawD - STAR_CAP, rawD + STAR_CAP);

    const rem = 1 - D2;
    const ratio = rawH + rawA;
    const H2 = ratio > 0 ? rem * rawH / ratio : 0.5 * rem;
    const A2 = ratio > 0 ? rem * rawA / ratio : 0.5 * rem;

    return { H: H2, D: D2, A: A2, corrected: true, gap };
  }

  // ── Engine ──
  function Engine() {
    this.att = Object.create(null);
    this.dfn = Object.create(null);
    this.hfa = Object.create(null);
    this.thfa = Object.create(null);
    this.mu = Object.create(null);
    this.seen = Object.create(null);
    this._leagueGoals = Object.create(null);
    this._records = Object.create(null);
  }

  Engine.prototype._get = function(map, key, init) {
    return (key in map) ? map[key] : (map[key] = init);
  };

  Engine.prototype._gethfa = function(league) {
    return this._get(this.hfa, league, HFA_INIT);
  };

  Engine.prototype._getmu = function(league) {
    return this._get(this.mu, league, MU_INIT);
  };

  Engine.prototype._getSeen = function(team) {
    return this._get(this.seen, team, 0);
  };

  Engine.prototype._getGMU = function(league) {
    const lg = getLeague(league);
    if (lg) return lg.gmu;
    const d = this._get(this._leagueGoals, league, { totalGoals: 0, matchCount: 0 });
    return d.matchCount === 0 ? SPEC_GMU : d.totalGoals / d.matchCount;
  };

  Engine.prototype._getRecord = function(league, team) {
    return this._get(this._records, league + '|' + team, { w: 0, d: 0, l: 0, played: 0 });
  };

  Engine.prototype._updateRecord = function(league, home, away, hg, ag) {
    const hr = this._getRecord(league, home);
    const ar = this._getRecord(league, away);
    if (hg > ag) { hr.w++; ar.l++; }
    else if (hg === ag) { hr.d++; ar.d++; }
    else { hr.l++; ar.w++; }
    hr.played++; ar.played++;
  };

  Engine.prototype.getStars = function(league) {
    const teams = [];
    for (const [key, rec] of Object.entries(this._records)) {
      const pipe = key.indexOf('|');
      const lg = key.substring(0, pipe);
      const team = key.substring(pipe + 1);
      if (lg === league && rec.played >= MIN_STAR_GAMES) {
        teams.push({ name: team, w: rec.w, d: rec.d, l: rec.l, played: rec.played });
      }
    }
    return computeStars(teams);
  };

  // ── λ ──
  Engine.prototype.lam = function(league, home, away) {
    const att_h = this._get(this.att, home, 0);
    const def_h = this._get(this.dfn, home, 0);
    const att_a = this._get(this.att, away, 0);
    const def_a = this._get(this.dfn, away, 0);
    const thfa_h = this._get(this.thfa, home, 0);
    const hfa = this._gethfa(league);
    const mu = this._getmu(league);
    return {
      lambda_home: clamp(Math.exp(mu + att_h - def_a + hfa + thfa_h), LAMBDA_MIN, LAMBDA_MAX),
      lambda_away: clamp(Math.exp(mu + att_a - def_h), LAMBDA_MIN, LAMBDA_MAX)
    };
  };

  // ── Update ──
  Engine.prototype.update = function(m) {
    const { league, home, away, hg, ag } = m;
    const { lambda_home: lh, lambda_away: la } = this.lam(league, home, away);

    const g = this._get(this._leagueGoals, league, { totalGoals: 0, matchCount: 0 });
    g.totalGoals += (hg + ag); g.matchCount++;

    this._updateRecord(league, home, away, hg, ag);

    const eh = hg - lh, ea = ag - la;
    const sh = this._getSeen(home), sa = this._getSeen(away);
    const kh = LR * (sh < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);
    const ka = LR * (sa < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);

    this.att[home] = this._get(this.att, home, 0) + kh * eh * 0.5;
    this.dfn[away] = this._get(this.dfn, away, 0) - ka * eh * 0.5;
    this.att[away] = this._get(this.att, away, 0) + ka * ea * 0.5;
    this.dfn[home] = this._get(this.dfn, home, 0) - kh * ea * 0.5;

    this.hfa[league] = clamp(this._gethfa(league) + HFA_LR * (eh - ea) * 0.02, HFA_MIN, HFA_MAX);

    const thfa_old = this._get(this.thfa, home, 0);
    this.thfa[home] = clamp((thfa_old + HFA_LR * (eh - ea) * 0.010) * HOME_EXTRA_DECAY, HOME_EXTRA_MIN, HOME_EXTRA_MAX);

    this.mu[league] = this._getmu(league) + MU_LR * ((eh + ea) / 2);

    for (const t of [home, away]) {
      this.att[t] = (this._get(this.att, t, 0)) * (1 - DECAY);
      this.dfn[t] = (this._get(this.dfn, t, 0)) * (1 - DECAY);
    }

    this.seen[home] = sh + 1; this.seen[away] = sa + 1;
  };

  // ── Predict ──
  Engine.prototype.predict = function(m) {
    const { league, home, away } = m;
    const sh = this._getSeen(home);
    const sa = this._getSeen(away);

    if (sh < MIN_GAMES || sa < MIN_GAMES) return null;

    const { lambda_home: lh, lambda_away: la } = this.lam(league, home, away);
    const raw = scoreGrid(lh, la);

    const leagueCfg = getLeague(league);
    const gmu = leagueCfg ? leagueCfg.gmu : this._getGMU(league);

    // L3: Star correction with per-league tables
    const stars = this.getStars(league);
    const homeStars = stars[home] ? stars[home].stars : null;
    const awayStars = stars[away] ? stars[away].stars : null;
    const corrected = applyStarCorrection(raw.H, raw.D, raw.A, homeStars, awayStars, leagueCfg);

    const expScore = expectedScoreline(lh, la);
    const ous = overUnder(lh, la, gmu);

    return {
      H: corrected.H, D: corrected.D, A: corrected.A,
      raw_H: raw.H, raw_D: raw.D, raw_A: raw.A,
      lambda_home: lh, lambda_away: la,
      expectedScore: expScore,
      overUnder: {
        over15: ous.over15, over25: ous.over25, over35: ous.over35
      },
      starCorrection: {
        applied: corrected.corrected,
        home_stars: homeStars, away_stars: awayStars,
        star_gap: corrected.gap,
        draw_adjustment: corrected.D - raw.D
      },
      provenance: {
        home_games: sh, away_games: sa, league: league,
        gmu_league: Number(gmu.toFixed(2)),
        base_H: leagueCfg ? leagueCfg.base.H : null,
        base_D: leagueCfg ? leagueCfg.base.D : null,
        base_A: leagueCfg ? leagueCfg.base.A : null
      }
    };
  };

  // ── Ingest ──
  Engine.prototype.ingest = function(matches) {
    const sorted = matches.slice().sort((a, b) => {
      if (a.date < b.date) return -1; if (a.date > b.date) return 1;
      if (a.league < b.league) return -1; if (a.league > b.league) return 1;
      if (a.home < b.home) return -1; if (a.home > b.home) return 1;
      if (a.away < b.away) return -1; if (a.away > b.away) return 1;
      return 0;
    });
    const preds = [];
    for (const m of sorted) {
      const pred = this.predict(m);
      if (pred) preds.push({ match: m, prediction: pred });
      this.update(m);
    }
    return preds;
  };

  // ── Score — reports vs per-league base AND global reference ──
  Engine.score = function(predictions) {
    let brierM = 0, brierLocal = 0, brierSpec = 0, llM = 0, dir = 0;
    const n = predictions.length;

    for (const p of predictions) {
      const { H, D, A } = p.prediction;
      const res = p.match.res;
      const y = { H: res === 'H' ? 1 : 0, D: res === 'D' ? 1 : 0, A: res === 'A' ? 1 : 0 };

      brierM += (H-y.H)**2 + (D-y.D)**2 + (A-y.A)**2;

      // Per-league base
      const lg = getLeague(p.match.league);
      const lb = lg ? lg.base : SPEC_BASE;
      brierLocal += (lb.H-y.H)**2 + (lb.D-y.D)**2 + (lb.A-y.A)**2;

      // Spec base (for comparison)
      brierSpec += (SPEC_BASE.H-y.H)**2 + (SPEC_BASE.D-y.D)**2 + (SPEC_BASE.A-y.A)**2;

      const pRes = H > D ? (H > A ? 'H' : 'A') : (D > A ? 'D' : 'A');
      if (pRes === res) dir++;
    }

    return {
      n,
      brier_model: brierM / n,
      brier_local: brierLocal / n,
      brier_spec: brierSpec / n,
      gain_vs_local: ((brierLocal - brierM) / brierLocal) * 100,
      gain_vs_spec: ((brierSpec - brierM) / brierSpec) * 100,
      direction: dir / n
    };
  };

  Engine.calibrateOU = function(predictions) {
    const mkt = { over15: { p:0, a:0 }, over25: { p:0, a:0 }, over35: { p:0, a:0 } };
    for (const x of predictions) {
      const ou = x.prediction.overUnder;
      const t = x.match.hg + x.match.ag;
      mkt.over15.p += ou.over15; mkt.over15.a += (t > 1.5 ? 1 : 0);
      mkt.over25.p += ou.over25; mkt.over25.a += (t > 2.5 ? 1 : 0);
      mkt.over35.p += ou.over35; mkt.over35.a += (t > 3.5 ? 1 : 0);
    }
    const nn = predictions.length;
    const r = {};
    for (const [k, v] of Object.entries(mkt)) {
      r[k] = { n: nn, pred: v.p/nn, actual: v.a/nn, error_pct: Math.abs(v.p/nn - v.a/nn) * 100 };
    }
    return r;
  };

  Engine.prototype.toJSON = function() {
    return {
      att: Object.assign({}, this.att), dfn: Object.assign({}, this.dfn),
      hfa: Object.assign({}, this.hfa), thfa: Object.assign({}, this.thfa),
      mu: Object.assign({}, this.mu), seen: Object.assign({}, this.seen),
      _leagueGoals: Object.assign({}, this._leagueGoals),
      _records: Object.assign({}, this._records)
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
    this._records = Object.assign(Object.create(null), state._records || {});
    return this;
  };

  return Engine;
})();

if (typeof module !== 'undefined' && module.exports) {
  module.exports = PitchEngineV5;
} else if (typeof window !== 'undefined') {
  window.PitchEngineV5 = PitchEngineV5;
}
