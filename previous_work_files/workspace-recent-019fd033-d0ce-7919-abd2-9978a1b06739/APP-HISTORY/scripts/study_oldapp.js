/* study_oldapp.js — run the OLD app (match-audit-tool.html) questionnaire on the ample-data
   RPL games, driving the REAL old-app code in a sandbox, answering every subscale from
   universe results with EXPLICIT, auditable rules (below), strict cutoff = fixture date.
   Audit: sign-consistency of COMMON_OPPONENT vs the new engine's common section,
   shared-count bound check, threshold distributions, 3 fully worked games.
   Also cross-tabs old-app tiers vs new-app zones and compares accuracy.
   ANSWER RULES (mapping choices, disclosed):
     H=home=A ("A" in the old app), A=away=B. All windows end at fixture date (exclusive).
     COMMON_OPPONENT: informative shared opp = both sides' most recent meeting vs it within 548d.
       m = AVG( GD/game A vs opp - GD/game B vs opp ). >=1.5:+2 >=0.5:+1 <=-1.5:-2 <=-0.5:-1 else EVEN.
     SHARED_COUNT = number of informative shared opps (0/1/2-3/4+).
     CURRENT_FORM: last 5 matches (<=120d), need >=3 each; PPG diff >=1.2:+2 >=0.4:+1 symmetric.
     RECENT_FORM:  last 10 (<=300d), need >=8 each; PPG diff >=0.9:+2 >=0.3:+1 symmetric.
     CONDITIONS_FIT: home-PPG(A) vs away-PPG(B) in 365d, need >=3 each; diff >=1.0:+2 >=0.35:+1
       symmetric; rest-day gap >=4d shifts one level toward the better-rested side.
     HEAD_TO_HEAD: prior meetings; PPG_A >=2.5:+2 >=1.75:+1 <=0.5:-2 <=1.25:-1 else EVEN;
       equal PPG (all draws / mirror results) => EVEN; no meetings => NO_DATA.
     BASELINE: live same-season league table at cutoff (need >=4 league games each):
       position gap <=3 => NO_SIGNAL else sign vs the subscale lean.
     RESILIENCE: narrow-games (|GD|<=1) points rate over last 12, need >=6 such games each;
       rate gap >=0.15 => that side, else NEUTRAL. (Results-only proxy for comeback metrics.)
     ANOMALY: a loss in the last 6 to a side >=10 league places below at the time => YES.
     AVAILABILITY_A/B: NO/NO - no lineup feed exists (results-only universe). Disclosed gap.
     ODDS: unset (results-only discipline). Therefore CLEAR_WIN (needs market edge) is
     unreachable; the top reachable tier is STRONG_LEAN. Disclosed.                           */
const fs = require("fs");
const vm = require("vm");
const newHtml = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const oldHtml = fs.readFileSync("/home/user/uploads/match-audit-tool.html", "utf8");

function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(p, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, scrollIntoView() {}, parentNode: null };
}
function bootApp(html, storageObj) {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const els = {}, sandbox = {};
  sandbox.window = sandbox; sandbox.console = console; sandbox.navigator = {};
  sandbox.setTimeout = (fn) => 0; sandbox.setInterval = () => 0; sandbox.confirm = () => true;
  sandbox.Blob = function () {}; sandbox.FileReader = function () { this.readAsText = function () {}; };
  sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
  sandbox.requestAnimationFrame = () => 0;
  sandbox.Option = function (t, v) { return { text: t, value: v }; };
  sandbox.localStorage = { getItem: k => (k in storageObj ? storageObj[k] : null), setItem: (k, v) => { storageObj[k] = String(v); }, removeItem: k => { delete storageObj[k]; } };
  const md = makeEl("matchDate");
  md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
  els["matchDate"] = md;
  sandbox.document = { readyState: "complete", body: makeEl("body"),
    getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
    createElement(t) { return makeEl(t + Math.random()); },
    querySelector(s) { return makeEl(s); }, querySelectorAll() { return []; },
    addEventListener() {}, execCommand() { return false; } };
  vm.createContext(sandbox);
  try { scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "s" + i })); }
  catch (e) { console.log("BOOT ERROR (continuing):", e.message); }
  return sandbox;
}

/* ---------- data ---------- */
const NEW = bootApp(newHtml, {});
const evN = e => vm.runInContext(e, NEW);
["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  NEW.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evN("BlueprintEmbed.importData()");
});
const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
const st = NEW.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
const ALL = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
const nameOf = id => (st.identities[id] && st.identities[id].name) || id;

/* ---------- questionnaire answer engine ---------- */
const pool = D => ALL.filter(m => m.date < D);
const days = (a, b) => (new Date(a) - new Date(b)) / 864e5;
function teamRows(t, P) { return P.filter(m => m.homeId === t || m.awayId === t); }
function pts(m, t) { const gd = m.homeId === t ? m.hg - m.ag : m.ag - m.hg; return gd > 0 ? 3 : gd === 0 ? 1 : 0; }
function gd(m, t) { return m.homeId === t ? m.hg - m.ag : m.ag - m.hg; }
function oppOf(m, t) { return m.homeId === t ? m.awayId : m.homeId; }
function ppg(rows, t) { return rows.length ? rows.reduce((a, m) => a + pts(m, t), 0) / rows.length : null; }
function cls(diff, t1, t2) { return diff >= t2 ? 2 : diff >= t1 ? 1 : diff <= -t2 ? -2 : diff <= -t1 ? -1 : 0; }

/* live league table position at cutoff (same-season RPL league rows) */
function livePosComp(t, D, seasonStart) {
  const rows = ALL.filter(m => m.competition === "RPL" && m.date >= seasonStart && m.date < D);
  const tab = {};
  rows.forEach(m => {
    [m.homeId, m.awayId].forEach(t2 => { tab[t2] = tab[t2] || { p: 0, pts: 0, gd: 0 }; });
    tab[m.homeId].p++; tab[m.awayId].p++;
    tab[m.homeId].pts += pts(m, m.homeId); tab[m.awayId].pts += pts(m, m.awayId);
    tab[m.homeId].gd += gd(m, m.homeId); tab[m.awayId].gd += gd(m, m.awayId);
  });
  const order = Object.keys(tab).sort((a, b) => tab[b].pts - tab[a].pts || tab[b].gd - tab[a].gd);
  return { pos: order.indexOf(t) + 1, played: tab[t] ? tab[t].p : 0, tab, order };
}
function seasonStartOf(D) { const y = +D.slice(0, 4); return (D >= "07-01" ? "" : "") , (D.slice(5, 7) >= "07" ? y + "-07-01" : (y - 1) + "-07-01"); }

function form(rows, t, n, win) {
  const rs = teamRows(t, rows).filter(m => days(win.end, m.date) <= win.days).sort((a, b) => b.date.localeCompare(a.date)).slice(0, n);
  return rs;
}

function answerFixture(H, A, D) {
  const P = pool(D);
  const seasonStart = seasonStartOf(D);
  const out = { audit: {} };
  /* COMMON_OPPONENT */
  const hOpp = {}, aOpp = {};
  teamRows(H, P).forEach(m => { const o = oppOf(m, H); if (o !== A) { (hOpp[o] = hOpp[o] || []).push(m); } });
  teamRows(A, P).forEach(m => { const o = oppOf(m, A); if (o !== H) { (aOpp[o] = aOpp[o] || []).push(m); } });
  let common = Object.keys(hOpp).filter(o => aOpp[o]);
  const inform = [], diffs = [];
  common.forEach(o => {
    const hLast = hOpp[o].slice().sort((x, y) => y.date.localeCompare(x.date))[0];
    const aLast = aOpp[o].slice().sort((x, y) => y.date.localeCompare(x.date))[0];
    if (days(D, hLast.date) <= 548 && days(D, aLast.date) <= 548) {
      const hG = hOpp[o].reduce((a, m) => a + gd(m, H), 0) / hOpp[o].length;
      const aG = aOpp[o].reduce((a, m) => a + gd(m, A), 0) / aOpp[o].length;
      inform.push(o); diffs.push({ o, hG, aG, d: hG - aG, n: hOpp[o].length + aOpp[o].length });
    }
  });
  out.audit.commonDiffs = diffs;
  out.sharedCount = inform.length;
  if (!inform.length) { out.commonOpponent = "no-data"; out.audit.commonM = null; }
  else { const m = diffs.reduce((a, x) => a + x.d, 0) / diffs.length; out.audit.commonM = m; out.commonOpponent = String(cls(m, 0.5, 1.5)); }
  /* CURRENT_FORM */
  const cfH = form(P, H, 5, { end: D, days: 120 }), cfA = form(P, A, 5, { end: D, days: 120 });
  out.audit.cfN = [cfH.length, cfA.length];
  if (cfH.length < 3 || cfA.length < 3) out.currentForm = "no-data";
  else { const d = ppg(cfH, H) - ppg(cfA, A); out.audit.cfDiff = d; out.currentForm = String(cls(d, 0.4, 1.2)); }
  /* RECENT_FORM */
  const rfH = form(P, H, 10, { end: D, days: 300 }), rfA = form(P, A, 10, { end: D, days: 300 });
  out.audit.rfN = [rfH.length, rfA.length];
  if (rfH.length < 8 || rfA.length < 8) out.recentForm = "no-data";
  else { const d = ppg(rfH, H) - ppg(rfA, A); out.audit.rfDiff = d; out.recentForm = String(cls(d, 0.3, 0.9)); }
  /* CONDITIONS_FIT */
  const cfHome = teamRows(H, P).filter(m => m.homeId === H && days(D, m.date) <= 365);
  const cfAway = teamRows(A, P).filter(m => m.awayId === A && days(D, m.date) <= 365);
  out.audit.condN = [cfHome.length, cfAway.length];
  if (cfHome.length < 3 || cfAway.length < 3) out.conditionsFit = "no-data";
  else {
    let v = cls(ppg(cfHome, H) - ppg(cfAway, A), 0.35, 1.0);
    out.audit.condDiff = ppg(cfHome, H) - ppg(cfAway, A);
    const lastH = teamRows(H, P).map(m => m.date).sort().pop(), lastA = teamRows(A, P).map(m => m.date).sort().pop();
    if (lastH && lastA) { const restGap = days(D, lastH) - days(D, lastA); out.audit.restGap = restGap; out.audit.restNudged = (restGap >= 4 || restGap <= -4);
      if (restGap >= 4) v = Math.min(2, v + 1); if (restGap <= -4) v = Math.max(-2, v - 1); }
    out.conditionsFit = String(v);
  }
  /* HEAD_TO_HEAD */
  const h2h = P.filter(m => (m.homeId === H && m.awayId === A) || (m.homeId === A && m.awayId === H));
  out.audit.h2hN = h2h.length;
  if (!h2h.length) out.headToHead = "no-data";
  else {
    const ph = h2h.reduce((a, m) => a + pts(m, H), 0) / h2h.length, pa = h2h.reduce((a, m) => a + pts(m, A), 0) / h2h.length;
    out.audit.h2hPPG = [ph, pa];
    out.headToHead = ph === pa ? "0" : String(cls(ph - 1.5, 0.25, 1.0));
  }
  /* BASELINE (after subscale lean) */
  const sw = { commonOpponent: 0.30, currentForm: 0.25, recentForm: 0.20, conditionsFit: 0.10, headToHead: 0.10 };
  let ws = 0;
  Object.keys(sw).forEach(k => { if (out[k] !== "no-data") ws += sw[k] * parseInt(out[k], 10); });
  out.audit.normScore = ws / 0.95 / 2;
  const lean = ws > 0 ? "H" : ws < 0 ? "A" : null;
  const posH = livePosComp(H, D, seasonStart), posA = livePosComp(A, D, seasonStart);
  out.audit.pos = [posH.pos, posA.pos, posH.played, posA.played];
  if (!lean || posH.played < 4 || posA.played < 4 || !posH.pos || !posA.pos || posH.pos < 0 || posA.pos < 0) out.baseline = "no-signal";
  else {
    const gap = posA.pos - posH.pos; // >0: home side better placed
    if (Math.abs(gap) <= 3) out.baseline = "no-signal";
    else out.baseline = ((gap > 0) === (lean === "H")) ? "agrees" : "conflicts";
  }
  /* RESILIENCE */
  function narrowRate(t) {
    const rs = teamRows(t, P).sort((a, b) => b.date.localeCompare(a.date)).slice(0, 12)
      .filter(m => Math.abs(m.hg - m.ag) <= 1);
    if (rs.length < 6) return null;
    return rs.reduce((a, m) => a + pts(m, t), 0) / (3 * rs.length);
  }
  const nrH = narrowRate(H), nrA = narrowRate(A);
  out.audit.narrow = [nrH && +nrH.toFixed(2), nrA && +nrA.toFixed(2)];
  out.resilience = (nrH === null || nrA === null) ? "neutral" : nrH - nrA >= 0.15 ? "A" : nrA - nrH >= 0.15 ? "B" : "neutral";
  /* ANOMALY */
  ["H", "A"].forEach(side => {
    const t = side === "H" ? H : A;
    const last6 = teamRows(t, P).sort((a, b) => b.date.localeCompare(a.date)).slice(0, 6);
    const flag = last6.some(m => {
      const o = oppOf(m, t);
      if (gd(m, t) >= 0) return false;
      const po = livePosComp(o, m.date, seasonStartOf(m.date)), pt = livePosComp(t, m.date, seasonStartOf(m.date));
      return po.pos >= 1 && pt.pos >= 1 && (po.pos - pt.pos) >= 10 && po.played >= 4;
    });
    out["anomaly" + side] = flag;
  });
  return out;
}

/* ---------- drive the old app ---------- */
const OLD = bootApp(oldHtml, {});
const evO = e => vm.runInContext(e, OLD);
console.log("OLD-APP INTEGRITY: computeVerdict " + evO("typeof computeVerdict") +
  " SUBSCALES " + evO("typeof SUBSCALES==='object'&&SUBSCALES.length") +
  " sigmoid " + evO("typeof sigmoid"));
function oldAppVerdict(H, A, D, comp, ans) {
  evO("document.getElementById('sport').value='football'");
  evO("document.getElementById('nameA').value=" + JSON.stringify(nameOf(H)));
  evO("document.getElementById('nameB').value=" + JSON.stringify(nameOf(A)));
  evO("document.getElementById('tournament').value=" + JSON.stringify(comp));
  ["commonOpponent", "currentForm", "recentForm", "conditionsFit", "headToHead"].forEach(k =>
    evO("document.getElementById('sub_" + k + "').value=" + JSON.stringify(ans[k])));
  evO("document.getElementById('sharedCount').value=" + JSON.stringify(ans.sharedCount >= 4 ? "4+" : String(ans.sharedCount === 1 ? "1" : ans.sharedCount === 0 ? "0" : "2-3")));
  evO("document.getElementById('qualityProxy').value='not-applicable'");
  evO("document.getElementById('baseline').value=" + JSON.stringify(ans.baseline));
  evO("document.getElementById('resilience').value=" + JSON.stringify(ans.resilience));
  evO("document.getElementById('anomalyA').checked=" + (ans.anomalyH ? "true" : "false"));
  evO("document.getElementById('anomalyB').checked=" + (ans.anomalyA ? "true" : "false"));
  evO("computeVerdict()");
  return evO("lastVerdict");
}

/* ---------- run ---------- */
const tiers = {}, zoneXTier = {}, agree = { n: 0, w: 0, d: 0, l: 0 };
let ample = 0, noH2HTrack = 0, rplGames = 0, signAgree = 0, signTotal = 0, countBoundFail = 0;
let signAgreeNZ = 0, signTotalNZ = 0, restNudges = 0, restFlips = 0;
const subDist = { commonOpponent: {}, currentForm: {}, recentForm: {}, conditionsFit: {}, headToHead: {} };
const worked = [];
const outCsv = ["date,fixture,co,cf,rf,cond,h2h,shared,baseline,resilience,anomA,anomB,tier,leader,probLeader,conf,zone,zoneSide,S,actual,resOld,resZone"];
ALL.forEach(m => {
  if (m.competition !== "RPL" && m.competition !== "CUP") return;
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  rplGames++;
  const D = m.date;
  const ans = answerFixture(m.homeId, m.awayId, D);
  const fullData = ans.sharedCount >= 4 && ans.currentForm !== "no-data" && ans.recentForm !== "no-data" &&
    ans.conditionsFit !== "no-data";
  if (!fullData) return;
  const hasH2H = ans.headToHead !== "no-data";
  if (hasH2H) ample++; else noH2HTrack++;
  const v = oldAppVerdict(m.homeId, m.awayId, D, m.competition + " Russia", ans);
  const zn = evN("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(D) + ");" +
    "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);var tw=ev.ag.totalWeight;return {key:z.key,side:z.side,S:100*Math.max(ev.ag.homeW,ev.ag.awayW)/tw,comN:ev.ag.phaseCounts.common||0};})()");
  /* audit: COMMON sign agreement with engine common section + shared-count bound */
  if (ans.commonOpponent !== "no-data" && zn) {
    const evCom = evN("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(D) + ");var s=sectionShares(ev.paths).filter(function(x){return x.phase==='common';})[0];return s?{h:s.hW,a:s.aW}:null;})()");
    if (evCom && (evCom.h !== evCom.a)) {
      signTotal++;
      const mySign = parseInt(ans.commonOpponent, 10);
      if ((evCom.h > evCom.a ? 1 : -1) === (mySign > 0 ? 1 : mySign < 0 ? -1 : mySign)) signAgree++;
      if (mySign !== 0) { signTotalNZ++; if ((evCom.h > evCom.a ? 1 : -1) === (mySign > 0 ? 1 : -1)) signAgreeNZ++; }
    }
    if (zn.comN !== undefined && ans.sharedCount > zn.comN) countBoundFail++;
  }
  ["commonOpponent", "currentForm", "recentForm", "conditionsFit", "headToHead"].forEach(k => {
    subDist[k][ans[k]] = (subDist[k][ans[k]] || 0) + 1;
  });
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  const oldLeader = !v || !v.leader ? null : (v.leader === "A" ? "H" : "A");
  const resOld = !v || !oldLeader ? "NC" : actual === oldLeader ? "W" : actual === "D" ? "D" : "L";
  const tierKey = v ? v.tier : "ERR";
  const tk = tierKey + (hasH2H ? "" : "*");
  tiers[tk] = tiers[tk] || { n: 0, w: 0, d: 0, l: 0 };
  if (resOld !== "NC") { tiers[tk].n++; tiers[tk][resOld.toLowerCase()]++; }
  if (zn) {
    const xk = zn.key + " x " + tierKey;
    zoneXTier[xk] = zoneXTier[xk] || { n: 0, w: 0, d: 0, l: 0 };
    const zoneLeader = zn.side === "TA" ? "H" : "A";
    if ((zn.key === "strong" || zn.key === "win") && tierKey === "STRONG_LEAN") {
      agree.n++; if (actual === zoneLeader && oldLeader === zoneLeader) agree.w++; else if (actual === "D") agree.d++; else agree.l++;
    }
    zoneXTier[xk].n++;
    const sameSide = oldLeader === zoneLeader;
    if (actual === zoneLeader && sameSide) zoneXTier[xk].w++; else if (actual === "D") zoneXTier[xk].d++; else zoneXTier[xk].l++;
  }
  if (worked.length < 3 && ample <= 3) worked.push({ m, ans, v });
  outCsv.push([D, nameOf(m.homeId).slice(0, 16) + " v " + nameOf(m.awayId).slice(0, 16),
    ans.commonOpponent, ans.currentForm, ans.recentForm, ans.conditionsFit, ans.headToHead, ans.sharedCount,
    ans.baseline, ans.resilience, ans.anomalyH ? "Y" : "N", ans.anomalyA ? "Y" : "N",
    tierKey, oldLeader || "", v && v.probA != null ? (100 * Math.max(v.probA3 || v.probA, v.probB3 || (1 - v.probA))).toFixed(0) : "",
    v ? v.confidence : "", zn ? zn.key : "", zn ? zn.side : "", zn ? zn.S.toFixed(0) : "", actual, resOld,
    zn ? (actual === (zn.side === "TA" ? "H" : "A") ? "W" : actual === "D" ? "D" : "L") : ""].join(","));
});
fs.writeFileSync("/home/user/oldapp_log.csv", outCsv.join("\n") + "\n");
console.log("RPL games:", rplGames, "| ample-data subset (>=4 shared + all form windows):", ample, "| same minus h2h present:", noH2HTrack);
console.log("\n=== OLD-APP TIER TABLE (ample subset, * = no-h2h track) ===");
Object.keys(tiers).sort().forEach(k => { const z = tiers[k]; if (!z.n) return;
  console.log("  " + k.padEnd(20), "n=" + String(z.n).padEnd(4),
    "leaderW " + (100 * z.w / z.n).toFixed(0).padStart(2) + "%",
    "D " + (100 * z.d / z.n).toFixed(0).padStart(2) + "%",
    "L " + (100 * z.l / z.n).toFixed(0).padStart(2) + "%"); });
console.log("\n=== ZONE x TIER cross-tab (call direction must agree to count as W) ===");
Object.keys(zoneXTier).sort().forEach(k => { const z = zoneXTier[k]; if (z.n < 3) return;
  console.log("  " + k.padEnd(26), "n=" + String(z.n).padEnd(4),
    "W " + (100 * z.w / z.n).toFixed(0).padStart(2) + "%",
    "D " + (100 * z.d / z.n).toFixed(0).padStart(2) + "%",
    "L " + (100 * z.l / z.n).toFixed(0).padStart(2) + "%"); });
console.log("\n=== DOUBLE-CONFIRMED cohort: zone STRONG/WIN + old STRONG_LEAN agreeing ===");
console.log("  n=" + agree.n, "W " + (100 * agree.w / agree.n).toFixed(0) + "%", "D " + (100 * agree.d / agree.n).toFixed(0) + "%", "L " + (100 * agree.l / agree.n).toFixed(0) + "%");
console.log("\n=== ANSWER AUDIT ===");
console.log("COMMON_OPPONENT sign vs engine common section: " + signAgree + "/" + signTotal + " agree (" + (100 * signAgree / signTotal).toFixed(0) + "%)");
console.log("sharedCount > engine common-path count violations:", countBoundFail);
console.log("nonzero-class sign agreement: " + signAgreeNZ + "/" + signTotalNZ + " (" + (100 * signAgreeNZ / Math.max(1, signTotalNZ)).toFixed(0) + "%)");
console.log("subscale value distributions:", JSON.stringify(subDist, null, 1));
console.log("\n=== WORKED GAMES (full answer trail, first 3 of ample subset) ===");
worked.forEach(wd => {
  const m = wd.m, ans = wd.ans, v = wd.v;
  console.log("\n-- " + m.date + " " + nameOf(m.homeId) + " v " + nameOf(m.awayId) + " => actual " + (m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D") + " (" + m.hg + "-" + m.ag + ")");
  console.log("   COMMON: m=" + (ans.audit.commonM === null ? "n/a" : ans.audit.commonM.toFixed(2)) + " over " + ans.sharedCount + " informative shared opps -> " + ans.commonOpponent);
  ans.audit.commonDiffs.slice(0, 10).forEach(x => console.log("     vs " + nameOf(x.o).slice(0, 20).padEnd(20) + " home-GDpg " + x.hG.toFixed(2) + " away-GDpg " + x.aG.toFixed(2) + " diff " + x.d.toFixed(2)));
  console.log("   CF: n=" + ans.audit.cfN + " diff=" + (ans.audit.cfDiff !== undefined ? ans.audit.cfDiff.toFixed(2) : "-") + " -> " + ans.currentForm +
    " | RF: n=" + ans.audit.rfN + " diff=" + (ans.audit.rfDiff !== undefined ? ans.audit.rfDiff.toFixed(2) : "-") + " -> " + ans.recentForm);
  console.log("   COND: splits n=" + ans.audit.condN + " diff=" + (ans.audit.condDiff !== undefined ? ans.audit.condDiff.toFixed(2) : "-") + " restGap=" + ans.audit.restGap + " -> " + ans.conditionsFit);
  console.log("   H2H: n=" + ans.audit.h2hN + " PPG=" + JSON.stringify(ans.audit.h2hPPG) + " -> " + ans.headToHead);
  console.log("   BASE: pos=" + JSON.stringify(ans.audit.pos) + " normScore=" + ans.audit.normScore.toFixed(3) + " -> " + ans.baseline +
    " | RES: narrow=" + JSON.stringify(ans.audit.narrow) + " -> " + ans.resilience + " | ANOM: " + ans.anomalyH + "/" + ans.anomalyA);
  console.log("   OLD-APP: tier=" + (v && v.tier) + " leader=" + (v && v.leader) + " conf=" + (v && v.confidence) +
    " reasons: " + (v ? v.reasons.join(" | ") : ""));
});
console.log("\nlog: oldapp_log.csv");
