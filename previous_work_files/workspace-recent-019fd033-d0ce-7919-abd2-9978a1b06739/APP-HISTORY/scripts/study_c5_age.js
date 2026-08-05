/* study_c5_age.js — follow-up measurement on the shipped engine:
   A) C5-draw sim: post-gate WIN + no h2h -> demote to WIN-DRAW. Effect on both pools.
   B) C6 motive check: median evidence-path age (from path-id dates) vs W/D/L outcome
      inside post-gate WIN+STRONG. If losses skew old, recency weighting is the next
      calibration with measured backing; if not, falsified and dropped. */
const fs = require("fs");
const vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(p, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null };
}
const els = {}, sandbox = {};
sandbox.window = sandbox; sandbox.console = console; sandbox.navigator = {};
sandbox.setTimeout = () => 0; sandbox.confirm = () => true;
sandbox.Blob = function () {}; sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const _s = {};
sandbox.localStorage = { getItem: k => (k in _s ? _s[k] : null), setItem: (k, v) => { _s[k] = String(v); }, removeItem: k => { delete _s[k]; } };
const md = makeEl("matchDate");
md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = md;
sandbox.document = { readyState: "complete", body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(t) { return makeEl(t + Math.random()); },
  querySelector(s) { return makeEl(s); }, querySelectorAll() { return []; }, addEventListener() {} };
vm.createContext(sandbox);
scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "s" + i }));
const S = sandbox, evX = e => vm.runInContext(e, S);
["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
});
const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
const st = S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
const matches = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));

const rows = [];
matches.forEach(m => {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  const r = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
    "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);" +
    "var ds=[];ev.paths.forEach(function(p){(p.ids||[]).forEach(function(id){var d=String(id).split('|')[0];if(/^\\d{4}-\\d{2}-\\d{2}$/.test(d))ds.push(d);});});" +
    "ds.sort();return {S:z.S_,key:z.key,side:z.side,h2hN:ev.ag.phaseCounts.h2h||0,med:ds.length?ds[Math.floor(ds.length/2)]:null,mn:ds.length?ds[0]:null,mx:ds.length?ds[ds.length-1]:null};})()");
  if (!r) return;
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  const leader = r.side === "TA" ? "H" : "A";
  rows.push({ date: m.date, key: r.key, S: r.S, h2hN: r.h2hN, med: r.med, actual, res: actual === leader ? "W" : actual === "D" ? "D" : "L" });
});

/* A) C5-draw sim */
function poolStats(sel) {
  const n = sel.length, w = sel.filter(r => r.res === "W").length, d = sel.filter(r => r.res === "D").length, l = sel.filter(r => r.res === "L").length;
  return { n, w: 100 * w / n, d: 100 * d / n, l: 100 * l / n, pair: 100 * (w + d) / n };
}
const fmt = o => "n=" + o.n + " W " + o.w.toFixed(0) + "% D " + o.d.toFixed(0) + "% L " + o.l.toFixed(0) + "% pair " + o.pair.toFixed(0) + "%";
console.log("=== A) C5 rule: post-gate WIN & no-h2h -> WINDRAW ===");
console.log("current  WIN     :", fmt(poolStats(rows.filter(r => r.key === "win"))));
console.log("current  WINDRAW :", fmt(poolStats(rows.filter(r => r.key === "windraw"))));
console.log("current  STRONG  :", fmt(poolStats(rows.filter(r => r.key === "strong"))));
console.log("demoted cohort (win & h2hN=0):", fmt(poolStats(rows.filter(r => r.key === "win" && r.h2hN === 0))));
console.log("after    WIN     :", fmt(poolStats(rows.filter(r => r.key === "win" && r.h2hN !== 0))));
console.log("after    WINDRAW :", fmt(poolStats(rows.filter(r => r.key === "windraw" || (r.key === "win" && r.h2hN === 0)))));
console.log("after    STRONG  (rule NOT applied to strong):", fmt(poolStats(rows.filter(r => r.key === "strong"))));

/* B) evidence age vs outcome inside post-gate WIN+STRONG */
function medAge(sel) {
  const days = sel.filter(r => r.med).map(r => Math.round((new Date(r.date) - new Date(r.med)) / 864e5));
  days.sort((a, b) => a - b);
  if (!days.length) return null;
  return { med: days[Math.floor(days.length / 2)], p25: days[Math.floor(days.length / 4)], p75: days[Math.floor(3 * days.length / 4)] };
}
const pws = rows.filter(r => r.key === "win" || r.key === "strong");
["W", "D", "L"].forEach(k => {
  const sub = pws.filter(r => r.res === k), a = medAge(sub);
  console.log("B) win+strong " + k + " (n=" + sub.length + "): median evidence age " + a.med + "d (p25 " + a.p25 + " / p75 " + a.p75 + ")");
});
/* split: old-evidence (median path > 180d) vs fresh, win rate */
function fmtL(sel, tag) { const o = poolStats(sel); console.log("   " + tag.padEnd(24), fmt(o)); }
console.log("B2) win+strong pool by median evidence age:");
const ageCut = 180;
fmtL(pws.filter(r => r.med && (new Date(r.date) - new Date(r.med)) / 864e5 > ageCut), "median age > " + ageCut + "d:");
fmtL(pws.filter(r => r.med && (new Date(r.date) - new Date(r.med)) / 864e5 <= ageCut), "median age <= " + ageCut + "d:");
const ageCut2 = 365;
fmtL(pws.filter(r => r.med && (new Date(r.date) - new Date(r.med)) / 864e5 > ageCut2), "median age > " + ageCut2 + "d:");
console.log("games scored:", rows.length);
