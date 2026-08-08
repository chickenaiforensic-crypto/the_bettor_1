/**
 * PITCH RATING v4.2 — L1 + L2 + L3 (Star Draw Correction)
 * Zero-market Dixon-Coles. Written from ENGINE_SPEC.md v1.0 Part D.
 * 
 * L3 adds:
 *   - Star classification: PPG quintile within league, min 5 games, shrunk
 *   - Draw correction: tier+gap table (27 cells), ±0.02 cap, proportional split
 *   - Measured gain: +0.047% full-1X2 (p<0.0001, n=59,615)
 *   - Per-tier weights: 0.2 (tier 1), 0.5 (tier 2), 0.5 (tier 3)
 *   - Falls back to draw_base[tier] when gap cell missing
 */

const PitchEngineV3 = (function() {
  'use strict';

  // ── CONSTANTS ──
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
  const GMU = 2.6186;

  // Star correction constants (ENGINE_SPEC §D3)
  const STAR_SHRINK_WEIGHT = 6;
  const STAR_CAP = 0.02;

  // Per-tier weight for draw correction blend
  const TIER_WEIGHTS = { 1: 0.2, 2: 0.5, 3: 0.5 };

  // Draw base rates per tier (fallback when gap cell missing)
  const DRAW_BASE = { 1: 0.268, 2: 0.287, 3: 0.295 };

  // Draw correction table: draw_table[tier][starGap]
  // Fitted on training data per ENGINE_SPEC §D3
  // 27 cells: tier 1..3 × star_gap 0..4
  const DRAW_TABLE = {
    1: { 0: 0.281, 1: 0.281, 2: 0.263, 3: 0.249, 4: 0.219 },
    2: { 0: 0.297, 1: 0.294, 2: 0.279, 3: 0.265, 4: 0.241 },
    3: { 0: 0.312, 1: 0.308, 2: 0.287, 3: 0.272, 4: 0.253 }
  };

  // ── Factorial cache ──
  const _fact = (function() {
    const f = [1];
    for (let i = 1; i < K_GRID; i++) f[i] = f[i-1] * i;
    return f;
  })();

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

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

  // ── L2: goalsGrid (shrunk) ──
  function goalsGrid(sh, sa) {
    const total = sh + sa;
    const shrunk = GMU + G_K * (total - GMU);
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

  function overUnder(lh, la) {
    const { grid } = goalsGrid(lh, la);
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

  // ── L3: Star Classification (ENGINE_SPEC §D1) ──
  // PPG = (3×won + drawn) / played, shrunk toward league mean

  /**
   * Compute star ratings for all teams in a league.
   * Returns { team → { ppg, shrunk, stars (1-5) } }
   */
  function computeStars(teams, leagueTier) {
    // teams: array of { name, w, d, l, played }
    if (teams.length === 0) return {};

    // Compute raw PPG, qualify teams
    const qualified = teams.filter(t => t.played >= MIN_STAR_GAMES);
    if (qualified.length === 0) return {};

    const rawPPG = qualified.map(t => ({
      name: t.name,
      ppg: (3 * t.w + t.d) / Math.max(t.played, 1),
      played: t.played
    }));

    // League mean PPG
    const leagueMean = rawPPG.reduce((s, t) => s + t.ppg, 0) / rawPPG.length;

    // Shrink toward league mean
    const shrunk = rawPPG.map(t => ({
      name: t.name,
      ppg: t.ppg,
      shrunk: (t.ppg * t.played + leagueMean * STAR_SHRINK_WEIGHT) / (t.played + STAR_SHRINK_WEIGHT),
      played: t.played
    }));

    // Sort by shrunk PPG descending
    shrunk.sort((a, b) => b.shrunk - a.shrunk);

    // Quintile assignment
    const n = shrunk.length;
    const result = {};
    for (let i = 0; i < n; i++) {
      const quintile = Math.floor((i / n) * 5) + 1; // 1 = best (top 20%)
      result[shrunk[i].name] = {
        ppg: shrunk[i].ppg,
        shrunk: shrunk[i].shrunk,
        stars: quintile
      };
    }
    return result;
  }

  /**
   * L3: Apply star draw correction (ENGINE_SPEC §D3)
   * Takes raw H/D/A from L2, applies correction, returns corrected H/D/A.
   */
  function applyStarCorrection(rawH, rawD, rawA, homeStars, awayStars, tier) {
    if (homeStars === null || awayStars === null || homeStars === undefined || awayStars === undefined) {
      return { H: rawH, D: rawD, A: rawA, corrected: false };
    }

    const gap = Math.abs(homeStars - awayStars);
    const drawTable = DRAW_TABLE[tier] || DRAW_TABLE[2];
    const tgt = drawTable[gap] !== undefined ? drawTable[gap] : (DRAW_BASE[tier] || DRAW_BASE[2]);
    const w = TIER_WEIGHTS[tier] || 0.5;

    let D2 = (1 - w) * rawD + w * tgt;

    // Hard cap: ±0.02
    D2 = clamp(D2, rawD - STAR_CAP, rawD + STAR_CAP);

    // Proportional split
    const rem = 1 - D2;
    const ratio = rawH + rawA;
    const H2 = ratio > 0 ? rem * rawH / ratio : 0.5 * rem;
    const A2 = ratio > 0 ? rem * rawA / ratio : 0.5 * rem;

    return { H: H2, D: D2, A: A2, corrected: true, gap, tier };
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
    // Track W-D-L per team per league for star computation
    this._records = Object.create(null); // { 'league|team': { w, d, l, played } }
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
    return d.matchCount === 0 ? GMU : d.totalGoals / d.matchCount;
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

  /**
   * Get star ratings for a league (computed on demand from records).
   * Returns { teamName → { ppg, shrunk, stars } }
   */
  Engine.prototype.getStars = function(league, tier) {
    const teams = [];
    for (const [key, rec] of Object.entries(this._records)) {
      const [lg, team] = key.split('|');
      if (lg === league && rec.played >= MIN_STAR_GAMES) {
        teams.push({ name: team, w: rec.w, d: rec.d, l: rec.l, played: rec.played });
      }
    }
    return computeStars(teams, tier || 1);
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
    const seen_h = this._getSeen(home), seen_a = this._getSeen(away);
    const kh = LR * (seen_h < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);
    const ka = LR * (seen_a < NEW_TEAM_GAMES ? NEW_TEAM_MULT : 1.0);

    this.att[home] = this._get(this.att, home, 0) + kh * eh * 0.5;
    this.dfn[away] = this._get(this.dfn, away, 0) - ka * eh * 0.5;
    this.att[away] = this._get(this.att, away, 0) + ka * ea * 0.5;
    this.dfn[home] = this._get(this.dfn, home, 0) - kh * ea * 0.5;

    this.hfa[league] = clamp(this._getHfa(league) + HFA_LR * (eh - ea) * 0.02, HFA_MIN, HFA_MAX);

    const thfa_old = this._get(this.thfa, home, 0);
    this.thfa[home] = clamp((thfa_old + HFA_LR * (eh - ea) * 0.010) * HOME_EXTRA_DECAY, HOME_EXTRA_MIN, HOME_EXTRA_MAX);

    this.mu[league] = this._getMu(league) + MU_LR * ((eh + ea) / 2);

    for (const t of [home, away]) {
      this.att[t] = (this._get(this.att, t, 0)) * (1 - DECAY);
      this.dfn[t] = (this._get(this.dfn, t, 0)) * (1 - DECAY);
    }

    this.seen[home] = seen_h + 1; this.seen[away] = seen_a + 1;
  };

  // ── Predict (L1 + L2 + L3) ──
  Engine.prototype.predict = function(m, tier) {
    const { league, home, away } = m;
    const seen_h = this._getSeen(home);
    const seen_a = this._getSeen(away);

    if (seen_h < MIN_GAMES || seen_a < MIN_GAMES) return null;

    const { lambda_home: lh, lambda_away: la } = this.lam(league, home, away);
    const raw = scoreGrid(lh, la);

    // L3: Star draw correction
    const tierVal = tier || 1;
    const stars = this.getStars(league, tierVal);
    const homeStars = stars[home] ? stars[home].stars : null;
    const awayStars = stars[away] ? stars[away].stars : null;

    const corrected = applyStarCorrection(raw.H, raw.D, raw.A, homeStars, awayStars, tierVal);

    const expScore = expectedScoreline(lh, la);
    const ous = overUnder(lh, la);

    return {
      // L3: Corrected 1X2
      H: corrected.H, D: corrected.D, A: corrected.A,
      // L3: Raw (uncorrected) values for provenance
      raw_H: raw.H, raw_D: raw.D, raw_A: raw.A,
      lambda_home: lh, lambda_away: la,
      expectedScore: expScore,
      overUnder: {
        over15: ous.over15, over25: ous.over25, over35: ous.over35
      },
      // L3: Star correction metadata
      starCorrection: {
        applied: corrected.corrected,
        home_stars: homeStars,
        away_stars: awayStars,
        star_gap: corrected.gap,
        tier: tierVal,
        draw_adjustment: corrected.D - raw.D
      },
      provenance: {
        home_games: seen_h, away_games: seen_a,
        league: league, gmu_league: this._getGMU(league)
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

  // ── Score ──
  Engine.score = function(predictions) {
    const base = { H: 0.446, D: 0.268, A: 0.286 };
    let brierM = 0, brierB = 0, llM = 0, llB = 0, dir = 0;
    const n = predictions.length;
    for (const p of predictions) {
      const { H, D, A } = p.prediction;
      const res = p.match.res;
      const y = { H: res === 'H' ? 1 : 0, D: res === 'D' ? 1 : 0, A: res === 'A' ? 1 : 0 };
      brierM += (H-y.H)**2 + (D-y.D)**2 + (A-y.A)**2;
      brierB += (base.H-y.H)**2 + (base.D-y.D)**2 + (base.A-y.A)**2;
      const pRes = { H, D, A }[res];
      llM += -Math.log(Math.max(pRes, 1e-12));
      llB += -Math.log(Math.max(base[res], 1e-12));
      const predRes = H > D ? (H > A ? 'H' : 'A') : (D > A ? 'D' : 'A');
      if (predRes === res) dir++;
    }
    return {
      n, brier_model: brierM/n, brier_base: brierB/n,
      brier_gain_pct: ((brierB - brierM)/brierB)*100,
      logloss_model: llM/n, logloss_base: llB/n, direction: dir/n
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
    const n = predictions.length;
    const r = {};
    for (const [k, v] of Object.entries(mkt)) {
      r[k] = { n, pred: v.p/n, actual: v.a/n, error_pct: Math.abs(v.p/n - v.a/n)*100 };
    }
    return r;
  };

  Engine.prototype.toJSON = function() {
    return {
      att: Object.assign({}, this.att),
      dfn: Object.assign({}, this.dfn),
      hfa: Object.assign({}, this.hfa),
      thfa: Object.assign({}, this.thfa),
      mu: Object.assign({}, this.mu),
      seen: Object.assign({}, this.seen),
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
  module.exports = PitchEngineV3;
} else if (typeof window !== 'undefined') {
  window.PitchEngineV3 = PitchEngineV3;
}
