/* drop2_backtest.js — user-ordered backtest: drop each side's last TWO results before the
   fixture (earlier masking dropped only the last), so the call is made without the two
   freshest form rows. Compare shipped-zone quality vs the full-history baseline on the
   same 600 evidence games. Strict causality in both variants.
   Per-user scope: "drop the last 2 results so we can check the one before the last also". */
const fs = require("fs");
const vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
function bootNewApp() {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  function makeEl(id) {
    return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
      checked: false, disabled: false, options: [], placeholder: "",
      appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
      insertAdjacentHTML(p, h) { this.innerHTML += h; },
      querySelector() { return null; }, querySelectorAll() { return []; },
      focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
      addEventListener() {}, scrollIntoView() {}, parentNode: null };
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
  return sandbox;
}
const S = bootNewApp();
const evX = e => vm.runInContext(e, S);
["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
});
const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
const st = S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
const ALL = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
const nameOf = id => (st.identities[id] && st.identities[id].name) || id;

/* team's last K results before date D */
function lastKIds(t, D, K) {
  return ALL.filter(x => (x.homeId === t || x.awayId === t) && x.date < D)
    .slice(-K).map(x => x.id);
}

const zones = v => ({});
const tally = {};
let churn = 0, scored = 0, changes = [];
const out = ["date,fixture,K,zoneBase,zoneDrop2,sideBase,shareBase,shareDrop2,actual,resBase,resDrop2"];
for (const m of ALL) {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) continue;
  // baseline: full history before D
  const base = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
    "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);var tw=ev.ag.totalWeight;return {key:z.key,side:z.side,S:100*Math.max(ev.ag.homeW,ev.ag.awayW)/tw};})()");
  // drop-2: remove each side's last 2 results before D from the store, then analyze
  const drop = new Set([...lastKIds(m.homeId, m.date, 2), ...lastKIds(m.awayId, m.date, 2)]);
  st.matches.splice(0, st.matches.length, ...ALL.filter(x => !drop.has(x.id)));
  const d2 = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
    "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);var tw=ev.ag.totalWeight;return {key:z.key,side:z.side,S:100*Math.max(ev.ag.homeW,ev.ag.awayW)/tw};})()");
  st.matches.splice(0, st.matches.length, ...ALL);
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  if (!base && !d2) continue;
  scored++;
  const res = (z, actual) => !z ? "NC" : (actual === (z.side === "TA" ? "H" : "A")) ? "W" : actual === "D" ? "D" : "L";
  const rB = res(base, actual), rD = res(d2, actual);
  const key = z => !z ? "NC" : z.key;
  if (base) { tally["B:" + base.key] = tally["B:" + base.key] || { n: 0, w: 0, d: 0, l: 0 }; tally["B:" + base.key].n++; tally["B:" + base.key][rB.toLowerCase() === "nc" ? "d" : rB.toLowerCase()]++; }
  if (d2) { tally["D2:" + d2.key] = tally["D2:" + d2.key] || { n: 0, w: 0, d: 0, l: 0 }; tally["D2:" + d2.key].n++; tally["D2:" + d2.key][rD.toLowerCase() === "nc" ? "d" : rD.toLowerCase()]++; }
  const kB = key(base), kD = key(d2);
  if (kB !== kD || (base && d2 && base.side !== d2.side)) {
    churn++;
    changes.push(m.date + " " + nameOf(m.homeId).slice(0, 14) + " v " + nameOf(m.awayId).slice(0, 14) + ": " + kB + (base ? " " + base.side : "") + " -> " + kD + (d2 ? " " + d2.side : "") + " [" + rB + " -> " + rD + "]");
  }
  out.push([m.date, nameOf(m.homeId).slice(0, 18) + " v " + nameOf(m.awayId).slice(0, 18), 2,
    kB, kD, base ? base.side : "", base ? base.S.toFixed(1) : "", d2 ? d2.S.toFixed(1) : "", actual, rB, rD].join(","));
}
fs.writeFileSync("/home/user/drop2_log.csv", out.join("\n") + "\n");
console.log("games scored:", scored, "| log: drop2_log.csv");
function show(prefix, label) {
  console.log("\n" + label);
  ["strong", "win", "windraw", "lean", "toss"].forEach(k => {
    const z = tally[prefix + k]; if (!z) return;
    console.log("  " + k.padEnd(8), "n=" + String(z.n).padEnd(4),
      "W " + (100 * z.w / z.n).toFixed(0).padStart(2) + "%",
      "D " + (100 * z.d / z.n).toFixed(0).padStart(2) + "%",
      "L " + (100 * z.l / z.n).toFixed(0).padStart(2) + "%",
      "pair " + (100 * (z.w + z.d) / z.n).toFixed(0) + "%");
  });
}
show("B:", "BASELINE zones (full history):");
show("D2:", "DROP-2 zones (each side's last 2 results removed):");
/* no-calls introduced by dropping */
const ncB = ALL.filter(m => m.homeId !== m.awayId).length - scored - Object.keys(tally).filter(k => k.startsWith("B:")).reduce((a, k) => a, 0);
console.log("\nzone-word or side churn:", churn, "of", scored, "(" + (100 * churn / scored).toFixed(1) + "%)");
/* churn direction quality: when calls changed, which variant was right? */
let baseBetter = 0, dropBetter = 0, bothSame = 0;
changes.forEach(c => { const m = c.match(/\[(.) -> (.)\]$/); if (!m) return;
  const q = r => r === "W";
  if (q(m[1]) && !q(m[2])) baseBetter++; else if (!q(m[1]) && q(m[2])) dropBetter++; });
console.log("churned games where baseline call won:", baseBetter, "| drop2 call won:", dropBetter);
console.log("\nchurn sample (up to 25):");
changes.slice(0, 25).forEach(c => console.log("  " + c));
