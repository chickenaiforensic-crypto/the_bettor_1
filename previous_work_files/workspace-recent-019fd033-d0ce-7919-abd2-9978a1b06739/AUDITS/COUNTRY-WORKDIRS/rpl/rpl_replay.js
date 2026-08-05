/* rpl_replay.js — masked-replay + blind forward read on the RPL universe (610 matches).
   A) replay: Rubin v Akron 18 Apr 2026, cutoff = match date (everything since stripped)
   B) forward: Akron v Rubin 1 Aug 2026 (today, Samara), cutoff today — result unseen.
   Strict causality via engine's beforeCutoff (m.date < cutoff). */
const fs = require("fs");
const vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(pos, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null };
}
const els = {}; const sandbox = {};
sandbox.window = sandbox; sandbox.console = console; sandbox.navigator = {};
sandbox.setTimeout = () => 0; sandbox.confirm = () => true;
sandbox.Blob = function () {}; sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const _store = {};
sandbox.localStorage = { getItem: k => (k in _store ? _store[k] : null), setItem: (k, v) => { _store[k] = String(v); }, removeItem: k => { delete _store[k]; } };
const md = makeEl("matchDate");
md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = md;
sandbox.document = { readyState: "complete", body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(tag) { return makeEl(tag + ":" + Math.random()); },
  querySelector(sel) { if (!els["q:" + sel]) els["q:" + sel] = makeEl(sel); return els["q:" + sel]; },
  querySelectorAll() { return []; }, addEventListener() {} };
vm.createContext(sandbox);
scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "script" + i + ".js" }));
const S = sandbox, evX = (e) => vm.runInContext(e, sandbox);

const matches = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
const BE = S.BlueprintEmbed;
console.log("API probe:", ["store","analyze","addMatch","addIdentity","applyFullData"].map(f => f + ":" + typeof BE[f]).join("  "));

const store = BE.store();
const ids = store.identities || store.teams || {};
console.log("store shape keys:", Object.keys(store).join(","));

const slugs = new Set(); matches.forEach(m => { slugs.add(m.home); slugs.add(m.away); });
const missing = [...slugs].filter(s => !NAMES[s]);
if (missing.length) console.log("UNNAMED slugs (used raw):", missing.join(", "));
[...slugs].forEach(s => { ids[s] = Object.assign(ids[s] || {}, { id: s, name: NAMES[s] || s }); });

const fp = m => [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|");
store.matches = store.matches || [];
matches.forEach(m => store.matches.push({ id: fp(m), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
console.log("matches loaded:", evX("BlueprintEmbed.store().matches.length"));

function run(home, away, cutoff, label, outFile) {
  const ev = BE.analyze(home, away, cutoff);
  fs.writeFileSync(outFile, JSON.stringify(ev, null, 1));
  console.log("\n=== " + label + "  (" + (NAMES[home] || home) + " v " + (NAMES[away] || away) + ", cutoff " + cutoff + ") ===");
  console.log("ev keys:", ev ? Object.keys(ev).join(",") : "null");
  if (!ev) return;
  if (ev.ag) console.log("aggregate: weighted", ev.ag.weighted, "| effective", ev.ag.effective, "| paths", ev.ag.paths);
  if (ev.cl) console.log("classify:", JSON.stringify(ev.cl));
  const ph = {};
  (ev.paths || []).forEach(p => { (ph[p.phase] = ph[p.phase] || []).push(p); });
  Object.keys(ph).forEach(k => {
    const g = ph[k]; const w = g.reduce((s, p) => s + p.weight, 0); const e = g.reduce((s, p) => s + p.weight * p.estimate, 0);
    console.log("phase " + k + ": n=" + g.length + " sumW=" + w.toFixed(2) + " weightedEst=" + (w ? (e / w).toFixed(2) : "n/a"));
    g.slice(0, 12).forEach(p => console.log("   ", JSON.stringify(p).slice(0, 170)));
  });
}
run("rubin", "akron", "2026-04-18", "REPLAY A — stripped target (actual: Rubin 1-1 Akron)", "/home/user/rpl/ev_A.json");
run("akron", "rubin", "2026-08-01", "FORWARD B — today, blind (Akron home, Samara)", "/home/user/rpl/ev_B.json");
