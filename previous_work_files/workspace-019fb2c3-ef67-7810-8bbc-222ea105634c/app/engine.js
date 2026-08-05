/* ============================================================================
   PITCH RATING ENGINE v1.1  — football only
   Pure functions over MODEL (model_data.js). No network. No bookmaker data.
   ========================================================================== */

const RHO = MODEL.rho;
const SHRINK = MODEL.goals_shrink;
const GMU = MODEL.goals_mu;

const FACT = [1,1,2,6,24,120,720,5040,40320,362880,3628800];
const KMAX = 11;

/* --- Dixon-Coles low-score correction ------------------------------------ */
function tau(i, j, lh, la) {
  if (i === 0 && j === 0) return 1 - lh * la * RHO;
  if (i === 0 && j === 1) return 1 + lh * RHO;
  if (i === 1 && j === 0) return 1 + la * RHO;
  if (i === 1 && j === 1) return 1 - RHO;
  return 1;
}

/* --- expected goals ------------------------------------------------------- */
function lambdas(lg, homeTeam, awayTeam) {
  const L = MODEL.leagues[lg];
  const T = MODEL.teams[lg];
  if (!L || !T || !T[homeTeam] || !T[awayTeam]) return null;
  const [ah, dh, xh] = T[homeTeam];
  const [aa, da] = T[awayTeam];
  let lh = Math.exp(L.mu + ah - da + L.hfa + xh);
  let la = Math.exp(L.mu + aa - dh);
  lh = Math.max(0.05, Math.min(6, lh));
  la = Math.max(0.05, Math.min(6, la));
  return { lh, la };
}

/* --- scoreline grid ------------------------------------------------------- */
function scoreGrid(lh, la) {
  const ph = [], pa = [];
  for (let i = 0; i < KMAX; i++) ph.push(Math.exp(-lh) * Math.pow(lh, i) / FACT[i]);
  for (let j = 0; j < KMAX; j++) pa.push(Math.exp(-la) * Math.pow(la, j) / FACT[j]);
  const g = []; let tot = 0;
  for (let i = 0; i < KMAX; i++) {
    g.push([]);
    for (let j = 0; j < KMAX; j++) {
      const p = ph[i] * pa[j] * tau(i, j, lh, la);
      g[i].push(p); tot += p;
    }
  }
  for (let i = 0; i < KMAX; i++) for (let j = 0; j < KMAX; j++) g[i][j] /= tot;
  return g;
}

/* --- goals-market grid: totals shrunk toward league mean (validated k=0.5) - */
function goalsGrid(lh, la) {
  const t = lh + la;
  const ts = GMU + SHRINK * (t - GMU);
  const r = t > 0 ? ts / t : 1;
  return scoreGrid(lh * r, la * r);
}

/* --- tier lookup ---------------------------------------------------------- */
function tierFor(pHome) {
  for (const t of MODEL.tiers) if (pHome >= t[1]) {
    return { name: t[0], min: t[1], win: t[2], draw: t[3], loss: t[4], n: t[5] };
  }
  const l = MODEL.tiers[MODEL.tiers.length - 1];
  return { name: l[0], min: l[1], win: l[2], draw: l[3], loss: l[4], n: l[5] };
}

/* --- main entry point ----------------------------------------------------- */
function rateFixture(lg, homeTeam, awayTeam) {
  const lam = lambdas(lg, homeTeam, awayTeam);
  if (!lam) return { error: "Unknown team or league. Both teams must be in the rated set." };
  const { lh, la } = lam;

  const g = scoreGrid(lh, la);
  let H = 0, D = 0, A = 0;
  for (let i = 0; i < KMAX; i++) for (let j = 0; j < KMAX; j++) {
    if (i > j) H += g[i][j]; else if (i === j) D += g[i][j]; else A += g[i][j];
  }

  // goals markets use the shrunk grid
  const gg = goalsGrid(lh, la);
  let o15 = 0, o25 = 0, o35 = 0, hm1 = 0;
  for (let i = 0; i < KMAX; i++) for (let j = 0; j < KMAX; j++) {
    const p = gg[i][j], s = i + j;
    if (s > 1.5) o15 += p;
    if (s > 2.5) o25 += p;
    if (s > 3.5) o35 += p;
    if (i - j > 1) hm1 += p;
  }

  // top scorelines from the true grid
  const lines = [];
  for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) lines.push({ s: i + "-" + j, p: g[i][j] });
  lines.sort((a, b) => b.p - a.p);

  const tier = tierFor(H);
  return {
    lg, homeTeam, awayTeam, lh, la, H, D, A,
    points: Math.round(H * 100),
    tier,
    markets: {
      dc1x: H + D,
      dc12: H + A,
      dcx2: D + A,
      dnb: H / (H + A),
      o15, u15: 1 - o15,
      o25, u25: 1 - o25,
      o35, u35: 1 - o35,
      hm1,
    },
    topScores: lines.slice(0, 5),
  };
}

/* --- FLIP DETECTION (audit 05 §7) ----------------------------------------
   Never trusts a parsed venue. Three independent checks.
   ------------------------------------------------------------------------- */
function flipCheck(lg, homeTeam, awayTeam) {
  const out = { level: "ok", messages: [], canAutoDetect: false };
  const hosted = MODEL.hosted[lg] || [];

  // 1. has the stated home team ever hosted in this league?
  if (hosted.length && hosted.indexOf(homeTeam) === -1) {
    out.level = "error";
    out.messages.push(
      '"' + homeTeam + '" has never hosted a match in ' +
      (MODEL.leagues[lg] ? MODEL.leagues[lg].name : lg) +
      " in 23 seasons of data. This is very likely a home/away flip or a parse error."
    );
  }

  // 2. rating asymmetry — would a flip be visible?
  const fwd = lambdas(lg, homeTeam, awayTeam);
  const rev = lambdas(lg, awayTeam, homeTeam);
  if (fwd && rev) {
    const gF = scoreGrid(fwd.lh, fwd.la);
    let Hf = 0, Af = 0;
    for (let i = 0; i < KMAX; i++) for (let j = 0; j < KMAX; j++) {
      if (i > j) Hf += gF[i][j]; else if (i < j) Af += gF[i][j];
    }
    const gap = Math.abs(Hf - Af);
    out.canAutoDetect = gap > 0.15;
    if (!out.canAutoDetect) {
      if (out.level === "ok") out.level = "warn";
      out.messages.push(
        "These sides are closely matched (win-probability gap " +
        (gap * 100).toFixed(1) + "pt). A home/away flip here would be SILENT — " +
        "the model cannot detect it. Venue must be confirmed manually."
      );
    }
  }
  return out;
}

/* --- formatting helpers --------------------------------------------------- */
function pct(x) { return (x * 100).toFixed(1) + "%"; }
function pct0(x) { return Math.round(x * 100) + "%"; }
